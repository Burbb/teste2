"""Combate por turnos."""

from contextlib import contextmanager

from . import texto as tx
from .classes import CLASSES
from .habilidades import HABILIDADES, descricao_habilidade
from .grimorio import chance_critico, mult_critico
from .modificadores import disparar, mod, mult, nomes
from .estados import ESTADOS, NOMES
from .dados import TRACOS
from .entidades import Combatente
from .inimigos import HABS_INIMIGO, NOMES_HABS_INIMIGO, ROTULOS_HABS_INIMIGO
from .itens import CONSUMIVEIS, PENA_FENIX_AGE_SOZINHA, ficha
from . import comitiva, sobrevivencia, telemetria
from .talentos import custo_habilidade
from . import balanceamento as bal

NOMES_EFEITOS = NOMES  # o catálogo de estados mora em estados.py
USAVEIS_EM_COMBATE = ("pocao_vida", "tonico", "antidoto", "bandagem", "bomba_fumaca")


def mult_tracos(alvo, tipo, alcance):
    m = 1.0
    t = alvo.tracos
    if "voador" in t:
        m *= 0.7 if alcance == "corpo" else 1.25
    if "blindado" in t:
        m *= 0.75 if tipo == "fisico" else 1.15
    if "morto-vivo" in t:
        m *= {"sagrado": 1.7, "sombra": 0.5, "veneno": 0}.get(tipo, 1)
    if "etereo" in t:
        m *= {"fisico": 0.75, "arcano": 1.3, "sagrado": 1.3}.get(tipo, 1)
    if "planta" in t and tipo == "fogo":
        m *= 1.5
    if "construto" in t:
        m *= {"veneno": 0, "arcano": 1.2}.get(tipo, 1)
    if "demonio" in t:
        m *= {"sagrado": 1.5, "fogo": 0.8}.get(tipo, 1)
    if "corrompido" in t:
        m *= {"sagrado": 1.4, "sombra": 0.6}.get(tipo, 1)
    return m * alvo.resist.get(tipo, 1)


class Aliado(Combatente):
    def __init__(self, nome, hp, atk, agi=4, tipo="servo", alcance="corpo", crit=0.0):
        super().__init__(nome, hp, atk, 3, agi, 0)
        self.tipo = tipo
        self.alcance = alcance
        self.crit = crit


_SERIE = [0]


class Combate:
    def __init__(self, g, inimigos, emboscada=None, pode_fugir=True, titulo=None, sozinho=False):
        self.g = g
        self.sozinho = sozinho  # duelo: nem comitiva nem animal entram na luta
        self.ui = g.ui
        self.rng = g.rng
        self.j = g.j
        self.inimigos = list(inimigos)
        self.aliados = []
        self.mortos = []
        self.companheiro = None
        self.emboscada = emboscada
        self.pode_fugir = pode_fugir and not any(e.chefe for e in self.inimigos)
        self.titulo = titulo or "COMBATE"
        self.flechas_gastas = 0
        self.turno = 0
        self.abertura = bool(mod(self.j, "abertura"))
        self.iniciativa = False  # pegou o inimigo de surpresa: o primeiro golpe sai mais forte
        self.motivo_abertura = "Tiro de Abertura" if self.abertura else None
        self.usou_martirio = False
        self.usou_imortal = False
        self.frenesi = 0
        self.explodindo = False
        self._n_uid = 0
        self._por_uid = {}
        _SERIE[0] += 1
        self._serie = _SERIE[0]
        self._fala_turno = -1
        self._cura_j = 0
        self._salva = self._salva_textos = None
        self._nomear()
        for e in self.inimigos:
            g.ver_criatura(e.familia)
        c = self.j.companheiro
        if c and c["hp"] > 0 and not sozinho:
            laco = 1 + mod(self.j, "laco_animal")
            self.companheiro = Aliado(c["nome"], int(c["max_hp"] * laco), c["atk"] * laco, c["agi"], c["tipo"],
                                      c["alcance"], c["crit"])
            self.companheiro.hp = int(c["hp"] * laco)
            self.aliados.append(self.companheiro)
            if c.pop("animado", False):  # o carinho da noite: entra na luta com vontade
                self.companheiro.aplicar("fortalecido", 3, 0.15)
        g.combate_ativo = self
        telemetria.novo_combate(self)

    # ------------------------------------------------------------ utilidades
    def dizer(self, texto, cor=None):
        if self._salva is not None:
            self._salva_textos.append((self.ui.dizer, texto, cor))
            return
        self.ui.dizer(texto, cor)
        self.ui.atualizar()  # a barra de vida acompanha cada linha do combate

    def detalhe(self, texto, cor=None):
        if self._salva is not None:
            self._salva_textos.append((self.ui.detalhe, texto, cor))
            return
        self.ui.detalhe(texto, cor)
        self.ui.atualizar()

    # Lances: o que aconteceu, com quem e em quem, para a interface animar as cartas.
    def uid(self, c):
        if c is None:
            return None
        if c is self.j:
            return "j"
        u = getattr(c, "uid", None)
        if u is None or u not in self._por_uid:
            self._n_uid += 1
            u = c.uid = f"c{self._serie}-{self._n_uid}"
            self._por_uid[u] = c
        return u

    def objeto(self, uid):
        if uid == "j":
            return self.j
        return self._por_uid.get(uid)

    def lance(self, tipo, **dados):
        telemetria.lance(self, tipo, dados)
        if self._salva is not None:
            self._salva.append(dict(dados, tipo=tipo))
            return
        self.ui.lance(tipo, **dados)

    @contextmanager
    def salva(self, hab=None):
        """Golpes em área saem juntos: os lances (e as linhas do registro) ficam guardados e vão à interface
        num só lance "salva", que anima todos os alvos ao mesmo tempo, como uma chuva de flechas de verdade."""
        if self._salva is not None:
            yield
            return
        self._salva, self._salva_textos = [], []
        self.ui.iniciar_salva()
        try:
            yield
        finally:
            lances, textos = self._salva, self._salva_textos
            self._salva = self._salva_textos = None
            if lances:
                self.ui.lance("salva", hab=hab, lances=lances)
            self.ui.fim_salva()
            for fn, texto, cor in textos:
                fn(texto, cor)
            self.ui.atualizar()

    @contextmanager
    def agindo(self, u, nome=None, alvo=None, area=False, hab=None):
        self.lance("acao", de=self.uid(u), nome=nome, alvo=self.uid(alvo), area=area, hab=hab)
        try:
            if area:  # golpes em área acertam todos juntos (no Redemoinho, giro a giro)
                with self.salva(hab):
                    yield
            else:
                yield
        finally:
            self.lance("fim_acao", de=self.uid(u))

    def curou(self, c, valor, tipo="cura", de=None, rotulo=None, fonte=None):
        """fonte: de quem a vida foi tirada (roubo de vida), para a tela desenhar o sangue voltando."""
        if valor and valor > 0:
            if c is self.j:
                self._cura_j += valor
            self.lance("cura", em=self.uid(c), de=self.uid(de), valor=int(valor), modo=tipo, rotulo=rotulo,
                       fonte=self.uid(fonte), hp=max(0, c.hp), max_hp=c.max_hp)

    def recuperou(self, c, valor, rotulo=None, discreto=False):
        """Ganho de recurso (mana, vigor, foco) visível na carta: Meditar, Tônico, talentos. Discreto: o pouco que
        o ataque básico devolve, só o número e a barra (sem aura nem som, que cansariam a cada golpe)."""
        if valor and valor > 0 and c is self.j:
            self.lance("recurso", em=self.uid(c), valor=int(valor), rotulo=rotulo, recurso=c.nome_recurso,
                       rec=c.rec, max_rec=c.max_rec, discreto=discreto)

    def nome(self, c, obj=False):
        if c is self.j:
            return "você" if obj else "Você"
        return c.nome

    def inimigos_vivos(self):
        return [e for e in self.inimigos if e.vivo]

    def _nomear(self):
        # No modo texto, a letra é o que diferencia os alvos no menu; onde o alvo é uma carta, só poluiria.
        if not self.ui.letras_nos_alvos:
            return
        contagem = {}
        for e in self.inimigos:
            contagem[e.nome] = contagem.get(e.nome, 0) + 1
        letras = {}
        for e in self.inimigos:
            if contagem[e.nome] > 1:
                n = letras.get(e.nome, 0)
                letras[e.nome] = n + 1
                e.nome = f"{e.nome} {'ABCDEFGHIJ'[min(n, 9)]}"

    MAX_CHAMAS = bal.MAX_CHAMAS  # o mesmo teto de camadas do catálogo (estados.py)

    def valor_queimadura(self, u):
        """Dano por turno de UMA camada de chamas. É pouco de propósito: o fogo do mago rende quando as
        camadas se acumulam (até 3) e a Combustão as detona de uma vez."""
        v = max(2, u.poder * bal.QUEIMADURA_POR_PODER)
        v *= mult(u, "queimadura_mult")
        return v * (1 + mod(u, "queimadura_dano"))

    def camadas(self, alvo):
        ef = alvo.efeito("queimadura")
        return ef.get("s", 1) if ef else 0

    def restante_queimadura(self, alvo):
        """Quanto a queimadura ainda causaria se ardesse até o fim (é o que a Combustão detona)."""
        ef = alvo.efeito("queimadura")
        return int(ef["v"]) * ef["t"] if ef else 0

    def duracao_queimadura(self, u):
        return 3 + mod(u, "queimadura_turnos")

    def invocar_aliado(self, nome, hp, atk, tipo="servo"):
        a = Aliado(nome, hp, atk, 3, tipo)
        self.aliados.append(a)
        return a

    # ------------------------------------------------------------ dano
    def atacar(self, u, alvo, mult, tipo="fisico", alcance="corpo", stat="atk", crit_extra=0.0, bonus=0,
               rotulo=None, pode_esquivar=True, detalhar=True):
        if alvo is None or not alvo.vivo:
            return 0
        prefixo = f"[{rotulo}] " if rotulo else ""
        quem = self.nome(u)
        if pode_esquivar and not alvo.efeito("atordoado"):
            esq = min(bal.ESQUIVA_MAX_AGI, alvo.agi * bal.ESQUIVA_POR_AGI)
            if alvo.efeito("esquiva"):
                esq += alvo.efeito("esquiva")["v"]
            if self.g.clima == "nevoa":
                esq += 0.05
            esq = min(bal.MAX_ESQUIVA, esq)
            if self.rng.random() < esq:
                self.lance("erro", de=self.uid(u), em=self.uid(alvo), motivo="esquiva", rotulo=rotulo)
                if detalhar:
                    self.detalhe(f"{prefixo}{quem} erra — {self.nome(alvo, True)} se esquiva!", "cinza")
                return 0
        eficacia = mult_tracos(alvo, tipo, alcance)
        if eficacia == 0:
            self.lance("erro", de=self.uid(u), em=self.uid(alvo), motivo="imune", rotulo=rotulo)
            self.detalhe(f"{prefixo}{self.nome(alvo)} é imune!", "cinza")
            return 0
        m = eficacia
        f = u.efeito("fortalecido")
        if f:
            m *= 1 + f["v"]
        if u.efeito("enfraquecido"):
            m *= 0.75
        ferido = mod(u, "dano_ferido") if u.jogador else 0
        if ferido:
            m *= 1 + ferido * (1 - u.hp / u.max_hp)
        if not u.jogador and u not in self.aliados and self.g.noite:
            m *= bal.NOITE_INIMIGOS
        clima = self.g.clima
        if clima == "chuva":
            m *= {"fogo": 0.8, "gelo": 1.1}.get(tipo, 1)
        elif clima == "neve":
            m *= {"fogo": 0.85, "gelo": 1.2}.get(tipo, 1)
        elif clima == "tempestade" and alcance == "distancia":
            m *= 0.85
        marcado = alvo.efeito("marcado")
        if marcado:
            m *= 1 + marcado["v"]
        if getattr(alvo, "chave", None) and self.g.flag(f"fraqueza:{alvo.chave}"):
            m *= 1.25
        if u.jogador and self.g.mestre_caca(getattr(alvo, "familia", None)):
            m *= 1.1
        bonus_motivo = None  # um bônus que não é crítico, mas a tela anuncia (a iniciativa)
        if u.jogador:
            m *= 1 + mod(u, "dano_corpo" if alcance == "corpo" else "dano_distancia")
            m *= bal.DANO_HEROI
            if self.iniciativa:
                self.iniciativa = False
                m *= 1 + bal.INICIATIVA_BONUS
                bonus_motivo = "Iniciativa!"

        defesa = alvo.defesa * (0.6 if alvo.efeito("maldito") else 1.0)
        furtivo = u.efeito("furtivo")
        abertura = u.jogador and self.abertura
        self.abertura = self.abertura and not u.jogador
        chance_crit = chance_critico(u, crit_extra)  # a mesma conta que o Grimório e a ficha mostram
        crit = bool(furtivo) or abertura or self.rng.random() < chance_crit
        # Crítico garantido diz de onde veio: sem isso, parece que a sorte ignora a chance da ficha.
        motivo_crit = ("Furtivo" if furtivo else self.motivo_abertura or "Iniciativa") if (furtivo or abertura) else None
        base = getattr(u, stat) * mult + bonus
        inimigo = not u.jogador and u not in self.aliados
        dano = base * m * self.rng.uniform(0.85, 1.15) * bal.fator_defesa(defesa, u.nivel if inimigo else None)
        if crit:
            dano *= mult_critico(u, furtivo=bool(furtivo))
        if furtivo:
            u.remover("furtivo")
        guarda = alvo.efeito("guarda")
        if guarda:
            dano *= 1 - guarda["v"]
        dano = max(1, round(dano))
        absorvido = 0
        barreira = alvo.efeito("barreira")
        if barreira:
            absorvido = min(barreira["v"], dano)
            barreira["v"] -= absorvido
            dano -= absorvido
            if barreira["v"] <= 0:
                alvo.remover("barreira")
        if alvo is self.j and dano >= alvo.hp:
            dano = disparar(self, alvo, "golpe_fatal", dano=dano, de=u)["dano"]  # Imortal...
        alvo.hp = max(0, alvo.hp - dano)
        telemetria.contabilizar_dano(self, u, alvo, dano, crit)

        txt = f"{prefixo}{quem} atinge {self.nome(alvo, True)}: {dano} de dano"
        if tipo != "fisico":
            txt += f" ({tipo})"
        if crit:
            txt = (f"CRÍTICO ({motivo_crit})! " if motivo_crit else "CRÍTICO! ") + txt
        if bonus_motivo:
            txt = f"{bonus_motivo} " + txt
        if absorvido:
            txt += f" [{absorvido} absorvido]"
        if eficacia >= 1.3:
            txt += " — super eficaz!"
        elif eficacia <= 0.7:
            txt += " — pouco eficaz."
        defensor = alvo is self.j or alvo in self.aliados
        self.lance("golpe", de=self.uid(u), em=self.uid(alvo), dano=dano, crit=crit, crit_motivo=motivo_crit, elemento=tipo,
                   alcance=alcance, absorvido=absorvido, eficacia="super" if eficacia >= 1.3 else "pouco" if eficacia <= 0.7 else None,
                   rotulo=rotulo, hp=max(0, alvo.hp), max_hp=alvo.max_hp,
                   **({"bonus_motivo": bonus_motivo} if bonus_motivo else {}))
        if detalhar:
            self.detalhe(txt, "vermelho" if defensor else "amarelo")
        else:
            self.ui.atualizar()
        if u is self.j and dano:
            roubo = mod(u, "roubo_vida")
            if roubo:
                # arredonda (e pelo menos 1): truncar zerava o roubo dos golpes pequenos e a build parecia não funcionar
                self.curou(u, u.curar(max(1, round(dano * roubo))), "roubo", fonte=alvo,
                           rotulo=(nomes(u, "roubo_vida") or ["Roubo de vida"])[0])
        espinhos = mod(alvo, "espinhos") if alvo is self.j and dano and alcance == "corpo" and u in self.inimigos else 0
        if espinhos and u.vivo:
            u.hp = max(0, u.hp - espinhos)
            self.lance("golpe", de=None, em=self.uid(u), dano=espinhos, crit=False, elemento="fisico", alcance="corpo",
                       absorvido=0, eficacia=None, rotulo="Espinhos", hp=u.hp, max_hp=u.max_hp,
                       refletido=self.uid(alvo))
            self.detalhe(f"Espinhos ferem {u.nome}. ({espinhos})", "amarelo")
            if not u.vivo:
                self.ao_morrer(u, por=alvo)
        if alvo is self.j and alvo.vivo:
            disparar(self, alvo, "golpe_recebido", de=u, alcance=alcance, dano=dano)  # Martírio, Contra-ataque...
        if alvo is self.j and dano:
            sobrevivencia.talvez_ferir(self.g, dano, tipo, crit, u)
        if not alvo.vivo:
            self.ao_morrer(alvo, por=u, tipo=tipo)
        return dano

    def aplicar(self, alvo, efeito, turnos, valor=0, chance=1.0, rotulo=None, acumula=False):
        if not alvo.vivo:
            return False
        if chance < 1 and self.rng.random() >= chance:
            return False
        est = ESTADOS[efeito]
        if est["imune"] and est["imune"](alvo):
            self.detalhe(f"{self.nome(alvo)} não é afetad{'o' if alvo.g == 'm' else 'a'} ({NOMES_EFEITOS[efeito]}).",
                         "cinza")
            return False
        if est["resiste"] and est["resiste"](self, alvo):
            self.detalhe(f"{self.nome(alvo)} resiste ao {'atordoamento' if efeito == 'atordoado' else est['nome']}!", "cinza")
            return False
        atual = alvo.efeitos.get(efeito)
        if acumula and atual and est["camadas"]:
            # Mais uma camada: o dano por turno soma (até o teto) e a duração se renova.
            s = min(est["camadas"], atual.get("s", 1) + 1)
            base = max(atual.get("b", atual["v"]), valor)
            atual.update(s=s, b=base, v=base * s, t=max(atual["t"], turnos))
            rotulo = est["rotulo_camadas"].format(s=s)
        else:
            alvo.aplicar(efeito, turnos, valor)
            if acumula and est["camadas"]:
                alvo.efeitos[efeito].setdefault("s", 1)
                alvo.efeitos[efeito].setdefault("b", valor)
        if rotulo:
            alvo.efeitos[efeito]["r"] = rotulo
        self.lance("efeito", em=self.uid(alvo), efeito=efeito, rotulo=rotulo or NOMES_EFEITOS[efeito])
        self.detalhe(f"{self.nome(alvo)} fica {rotulo or NOMES_EFEITOS[efeito]}!", "magenta")
        return True

    def ao_morrer(self, c, por=None, tipo=None):
        if c is self.j:
            return
        if c in self.aliados:
            self.dizer(f"{c.nome} cai!", "vermelho")
            return
        if c in self.mortos:
            return
        self.mortos.append(c)
        o = "o" if c.g == "m" else "a"
        self.dizer(self.rng.choice([
            f"{c.nome} desaba sem um som.", f"{c.nome} cai num jorro de sangue escuro.",
            f"{c.nome} se contorce no chão e fica imóvel.", f"{c.nome} é derrubad{o} e não se levanta mais.",
            f"{c.nome} solta um último grito gorgolejante.",
        ]), "verde+negrito")
        j = self.j
        disparar(self, j, "morte", alvo=c, por=por, tipo=tipo)  # Colheita, Rei dos Mortos...
        if por is not j:
            return
        if mod(j, "vida_abate"):
            j.curar(mod(j, "vida_abate"))
        disparar(self, j, "abate", alvo=c, tipo=tipo)  # Frenesi, Assassino, Coração Ardente...

    # ------------------------------------------------------------ fluxo
    def executar(self):
        self.ui.cena(self.titulo, tx.lista_natural([f"{e.nome} (Nv.{e.nivel})" for e in self.inimigos]), "combate")
        if not self.ui.hud:
            self.dizer("Inimigos: " + ", ".join(f"{e.nome} (Nv.{e.nivel})" for e in self.inimigos), "vermelho")
        if self.companheiro:
            animado = self.companheiro.efeito("fortalecido")
            self.dizer(f"{self.companheiro.nome} " + ("salta à frente, animado depois da noite ao seu lado. (+15% de dano)"
                                                      if animado else "rosna ao seu lado."), "verde")
        if self.sozinho:
            if comitiva.membros(self.g) or self.j.companheiro:
                self.dizer("Um duelo é coisa de dois. Os seus ficam de fora, assistindo.", "cinza")
        else:
            comitiva.preparar_combate(self)
        pular_inimigos = False
        if self.emboscada == "inimigo":
            self.dizer("Você foi pego de surpresa!", "vermelho+negrito")
            self.fase_inimigos()
            r = self._checar_fim()
            if r:
                return self.fim(r)
        elif self.emboscada == "jogador":
            self.dizer(f"Você tem a iniciativa! Um ataque livre antes que reajam, e o primeiro golpe sai "
                       f"{round(bal.INICIATIVA_BONUS * 100)}% mais forte.", "verde+negrito")
            pular_inimigos = True
            self.iniciativa = True
        disparar(self, self.j, "inicio_combate")  # Aura de Proteção, Armadilheiro...

        while True:
            self.turno += 1
            if self.fase_jogador() == "fuga":
                return self.fim("fuga")
            r = self._checar_fim()
            if r:
                return self.fim(r)
            self.fase_aliados()
            r = self._checar_fim()
            if r:
                return self.fim(r)
            if pular_inimigos:
                pular_inimigos = False
            else:
                self.fase_inimigos()
                r = self._checar_fim()
                if r:
                    return self.fim(r)
            self.j.rec = min(self.j.max_rec, self.j.rec + self.j.regen)

    def _checar_fim(self):
        j = self.j
        if not j.vivo:
            if j.tem("pena_fenix"):
                j.consumiveis["pena_fenix"] -= 1
                j.hp = j.max_hp // 2
                j.limpar_negativos()
                self.dizer("A Pena de Fênix arde em chamas douradas e você se ergue das cinzas!", "amarelo+negrito")
                return None
            if self.g.flag("bencao_fenix"):
                self.g.marcar("bencao_fenix", False)
                j.hp = j.max_hp // 2
                j.limpar_negativos()
                self.dizer("Uma luz antiga — a bênção do santuário — te puxa de volta da escuridão!", "amarelo+negrito")
                return None
            return "derrota"
        if not self.inimigos_vivos():
            return "vitoria"
        return None

    def mostrar_estado(self):
        j = self.j
        ui = self.ui
        ui.novo_turno(self.turno)
        if ui.hud:
            return  # o painel lateral mostra vida, efeitos e inimigos
        linha = (f"  Você  {ui.barra(j.hp, j.max_hp, 14, 'verde')} {j.hp}/{j.max_hp}  "
                 f"{j.nome_recurso} {j.rec}/{j.max_rec}")
        if j.classe == "arqueiro":
            linha += f"  Flechas {j.flechas}"
        ui._imprimir(linha + self._efeitos_txt(j))
        for a in self.aliados:
            if a.vivo:
                ui._imprimir(f"  {a.nome}  {ui.barra(a.hp, a.max_hp, 10, 'ciano')} {a.hp}/{a.max_hp}"
                             + self._efeitos_txt(a))
        for e in self.inimigos_vivos():
            extra = "  << preparando golpe! >>" if e.carregando else ""
            ui._imprimir(f"  {ui.pintar(e.nome, 'vermelho')}  {ui.barra(e.hp, e.max_hp, 14, 'vermelho')} "
                         f"{e.hp}/{e.max_hp}{self._efeitos_txt(e)}{ui.pintar(extra, 'amarelo')}")

    def _efeitos_txt(self, c):
        if not c.efeitos:
            return ""
        partes = [f"{ef.get('r', NOMES_EFEITOS.get(n, n))}({ef['t']})" for n, ef in c.efeitos.items()]
        return "  " + self.ui.pintar("[" + ", ".join(partes) + "]", "magenta")

    def processar_efeitos(self, c):
        """Aplica efeitos de início de turno. Devolve True se o turno é perdido."""
        # Perde o turno quem tem um estado que tira o turno (o rótulo diz como: "congelado", "preso na armadilha").
        trava = next((n for n in c.efeitos if ESTADOS.get(n, {}).get("perde_turno")), None)
        pular = trava is not None
        rotulo = c.efeitos[trava].get("r", NOMES[trava]) if trava else ""
        for nome in list(c.efeitos):
            ef = c.efeitos[nome]
            est = ESTADOS.get(nome, {})
            if est.get("tique") and c.vivo:
                dano = max(1, int(ef["v"]))
                if est["ajuste_tique"]:
                    dano = est["ajuste_tique"](self, dano)
                c.hp = max(0, c.hp - dano)
                rot, cor = est["tique"]
                self.lance("tique", em=self.uid(c), dano=dano, efeito=nome, hp=c.hp, max_hp=c.max_hp)
                self.detalhe(f"{self.nome(c)} sofre {dano} de dano ({rot}).", cor)
                if not c.vivo:
                    self.ao_morrer(c)
            ef["t"] -= 1
            if ef["t"] <= 0:
                del c.efeitos[nome]
        if pular and c.vivo:
            self.lance("atordoado", em=self.uid(c), rotulo=rotulo)
            self.detalhe(f"{self.nome(c)} está {rotulo} e perde o turno!", "magenta")
        return pular or not c.vivo

    # ------------------------------------------------------------ jogador
    def fase_jogador(self):
        j = self.j
        self.mostrar_estado()
        if mod(j, "regen_vida") and j.hp < j.max_hp:
            j.curar(mod(j, "regen_vida"))
        if self.processar_efeitos(j) or not j.vivo:
            return None
        while True:
            nome_atk = CLASSES[j.classe]["ataque"][0]
            if j.classe == "arqueiro" and j.flechas <= 0:
                nome_atk = "Golpe de Adaga — sem flechas!"
            analisar = self.ui.analisar_no_menu
            opcoes = [f"Atacar ({nome_atk})", "Habilidades", "Itens"] + (["Analisar inimigos"] if analisar else [])
            # Na tela gráfica as ações viram uma barra dentro da arena, com as habilidades já à mostra.
            metas = [{"acao": "atacar", "nome": nome_atk}, {"acao": "habilidades", "habilidades": self.metas_habilidades()},
                     {"acao": "itens", "itens": self.metas_itens()}] + ([{"acao": "analisar"}] if analisar else [])
            if self.pode_fugir:
                opcoes.append("Fugir")
                metas.append({"acao": "fugir"})
            self.ui.meta_opcoes = metas
            try:
                esc = self.ui.escolher("Sua ação:", opcoes)
            finally:
                self.ui.meta_opcoes = None
            if esc >= 3 and not analisar:
                esc += 1  # mantém a numeração das ações abaixo
            if esc == 0:
                alvo = self.escolher_alvo(cancelavel=True)
                if alvo is None:
                    continue
                self.ataque_basico(alvo)
                return None
            if esc == 1:
                if self.menu_habilidades():
                    return None
            elif esc == 2:
                r = self.menu_itens()
                if r == "fuga":
                    return "fuga"
                if r:
                    return None
            elif esc == 3:
                self.analisar()
            elif esc == 4:
                return "fuga" if self.tentar_fuga() else None

    def escolher_alvo(self, cancelavel=False):
        """Com cancelavel, a lista ganha "Voltar" e devolve None se a pessoa desistir (nada foi gasto ainda)."""
        vivos = self.inimigos_vivos()
        if len(vivos) == 1:
            return vivos[0]
        self.ui.meta_opcoes = [{"alvo": self.uid(e)} for e in vivos] + ([{"voltar": True}] if cancelavel else [])
        try:
            esc = self.ui.escolher("Alvo:", [f"{e.nome} ({e.hp}/{e.max_hp})" for e in vivos] + (["Voltar"] if cancelavel else []))
        finally:
            self.ui.meta_opcoes = None
        return vivos[esc] if esc < len(vivos) else None

    def ataque_basico(self, alvo):
        j = self.j
        nome, alcance, tipo, stat, mult = CLASSES[j.classe]["ataque"]
        if j.classe == "arqueiro":
            if j.flechas > 0:
                j.flechas -= 1
                self.flechas_gastas += 1
            else:
                nome, alcance, mult = "Adaga", "corpo", 0.6
        with self.agindo(j, nome, alvo, hab="ataque"):
            dano = self.atacar(j, alvo, mult, tipo=tipo, alcance=alcance, stat=stat, rotulo=nome)
            if dano:
                disparar(self, j, "ataque_basico", alvo=alvo)  # Pontas Venenosas...
            if dano and j.rec < j.max_rec:
                ganho = min(j.max_rec - j.rec, max(bal.ATAQUE_RECURSO_MIN, round(j.max_rec * bal.ATAQUE_RECURSO)))
                j.rec += ganho
                self.recuperou(j, ganho, discreto=True)

    def motivo_bloqueio(self, h_id):
        """Por que não dá para usar a habilidade agora (ou None se dá)."""
        j, h = self.j, HABILIDADES[h_id]
        if j.rec < custo_habilidade(j, h_id):
            return f"{j.nome_recurso} insuficiente"
        if h.get("flechas", 0) > j.flechas:
            return "Flechas insuficientes"
        if h.get("req"):
            return h["req"](self)
        return None

    def metas_habilidades(self):
        """Cada habilidade como a interface gráfica a desenha: ícone, custo, alvo, dica e se dá para usar agora."""
        j = self.j
        metas = []
        for h_id in j.habilidades:
            h = HABILIDADES[h_id]
            motivo = self.motivo_bloqueio(h_id)
            metas.append({"habilidade": h_id, "nome": h["nome"], "custo": custo_habilidade(j, h_id),
                          "recurso": j.nome_recurso, "flechas": h.get("flechas", 0), "alvo_tipo": h["alvo"],
                          "desc": descricao_habilidade(h_id, j), "pode": motivo is None, "motivo": motivo})
        return metas

    def menu_habilidades(self):
        j = self.j
        ids = list(j.habilidades)
        opcoes = []
        for h_id in ids:
            h = HABILIDADES[h_id]
            custo = f"{custo_habilidade(j, h_id)} {j.nome_recurso}"
            if h.get("flechas"):
                custo += f", {h['flechas']} flecha{'s' if h['flechas'] > 1 else ''}"
            opcoes.append(f"{h['nome']} [{custo}] — {h['desc']}")
        metas = self.metas_habilidades()
        opcoes.append("Voltar")
        self.ui.meta_opcoes = metas + [None]
        try:
            esc = self.ui.escolher("Habilidades:", opcoes)
        finally:
            self.ui.meta_opcoes = None
        if esc == len(ids):
            return False
        h = HABILIDADES[ids[esc]]
        custo = custo_habilidade(j, ids[esc])
        if j.rec < custo:
            self.dizer(f"{j.nome_recurso} insuficiente.", "cinza")
            return False
        if h.get("flechas", 0) > j.flechas:
            self.dizer("Flechas insuficientes!", "cinza")
            return False
        if h.get("req"):
            erro = h["req"](self)
            if erro:
                self.dizer(erro, "cinza")
                return False
        alvo = None
        if h["alvo"] == "inimigo":
            alvo = self.escolher_alvo(cancelavel=True)
            if alvo is None:
                return False
        j.rec -= custo
        self.tel["habilidades"][ids[esc]] = self.tel["habilidades"].get(ids[esc], 0) + 1
        self.tel["rec_gasto"] += custo
        j.flechas -= h.get("flechas", 0)
        self.flechas_gastas += h.get("flechas", 0)
        with self.agindo(j, h["nome"], alvo, area=h["alvo"] == "todos", hab=ids[esc]):
            antes, self._cura_j = j.hp, 0
            efeitos_antes = {k: dict(v) for k, v in j.efeitos.items()}
            h["fn"](self, j, alvo)
            self.curou(j, j.hp - antes - self._cura_j, rotulo=h["nome"])
            # Buffs em si mesmo (grito, escudo, esquiva, sombras) também viram um lance: a tela anima e espera.
            novos = [k for k, v in j.efeitos.items() if efeitos_antes.get(k) != v]
            if novos:
                self.lance("buff", em="j", efeitos=novos, rotulo=h["nome"], hab=ids[esc])
        return True

    def itens_da_luta(self):
        """Consumíveis que servem em luta e armas (ou escudo/aljava/grimório) da mochila para trocar.
        Trocar de arma gasta o turno; armadura não: ninguém veste uma cota de malha com um lobo no pescoço."""
        j = self.j
        usaveis = [k for k in USAVEIS_EM_COMBATE if j.consumiveis.get(k, 0) > 0]
        armas = [it for it in j.mochila if it["slot"] in ("arma", "secundaria") and self.g.pode_usar(it)]
        return usaveis, armas

    def metas_itens(self):
        """Cada item usável na luta como a interface gráfica o desenha (ícone, quantidade, dica, se serve agora)."""
        j = self.j
        usaveis, armas = self.itens_da_luta()
        metas = [{"usar_item": k, "item": k, "qtd": j.consumiveis[k], "nome": CONSUMIVEIS[k]["nome"],
                  "desc": CONSUMIVEIS[k]["desc"],
                  "motivo": self.motivo_item(k)}
                 for k in usaveis]
        metas += [{"trocar": j.mochila.index(it), "equip": ficha(it, j.nome_recurso)} for it in armas]
        return metas

    def motivo_item(self, k):
        """Por que o item não serve agora, na luta (ou None). A bolsa do painel e o menu de itens dizem o mesmo."""
        if k == "pena_fenix":
            return PENA_FENIX_AGE_SOZINHA
        if k not in USAVEIS_EM_COMBATE:
            return "Isso não se usa no meio da luta."
        if k == "bomba_fumaca" or self.aliados_precisam(k):
            return None
        return self.g.motivo_inutil(k)

    def menu_itens(self):
        j = self.j
        usaveis, armas = self.itens_da_luta()
        if not usaveis and not armas:
            self.dizer("Sua bolsa não tem nada útil agora.", "cinza")
            return None
        opcoes = [f"{CONSUMIVEIS[k]['nome']} x{j.consumiveis[k]} — {CONSUMIVEIS[k]['desc']}" for k in usaveis]
        opcoes += [f"Trocar para {it['nome']} (gasta o turno)" for it in armas]
        metas = self.metas_itens()
        self.ui.meta_opcoes = metas + [None]
        try:
            esc = self.ui.escolher("Usar qual item?", opcoes + ["Voltar"])
        finally:
            self.ui.meta_opcoes = None
        if esc == len(opcoes):
            return None
        if esc >= len(usaveis):
            it = armas[esc - len(usaveis)]
            with self.agindo(j, "Troca de arma", hab="item"):
                self.g.equipar(it)
            return "turno"
        k = usaveis[esc]
        if k == "bomba_fumaca":
            if not self.pode_fugir:
                self.dizer("Não há como fugir desta luta!", "vermelho")
                return None
            j.consumiveis[k] -= 1
            self.dizer("Você estoura a bomba de fumaça e some na nuvem cinzenta!", "cinza")
            return "fuga"
        motivo = self.g.motivo_inutil(k)
        if k in ("pocao_vida", "bandagem"):
            # Poção e bandagem também servem em quem luta ao seu lado (comitiva e animal); servos não.
            precisam = self.aliados_precisam(k)
            if precisam:
                quem = self.escolher_quem_trata(k, ([] if motivo else [j]) + precisam)
                if quem is None:
                    return None
                if quem is not j:
                    return self.tratar_aliado(k, quem)
                motivo = None
        if motivo:
            self.dizer(motivo, "cinza")
            return None
        with self.agindo(j, CONSUMIVEIS[k]["nome"], hab="item"):
            antes, antes_rec = j.hp, j.rec
            self.g.usar_consumivel(k)
            self.curou(j, j.hp - antes, rotulo=CONSUMIVEIS[k]["nome"])
            self.recuperou(j, j.rec - antes_rec, rotulo=CONSUMIVEIS[k]["nome"])
        return "turno"

    def aliados_precisam(self, k):
        """Quem luta ao seu lado (comitiva e animal; servos não) e precisa da poção ou da bandagem agora."""
        if k not in ("pocao_vida", "bandagem"):
            return []
        return [a for a in self.aliados if a.vivo and a.tipo != "servo"
                and (a.hp < a.max_hp or (k == "bandagem" and a.efeito("sangramento")))]

    def escolher_quem_trata(self, k, candidatos):
        """Em quem usar a poção ou a bandagem. Na tela gráfica, as cartas acendem como na mira de um golpe."""
        self.ui.meta_opcoes = [{"alvo": self.uid(c)} for c in candidatos] + [{"voltar": True}]
        try:
            esc = self.ui.escolher(f"Em quem usar {CONSUMIVEIS[k]['nome']}?",
                                   [("Você" if c is self.j else c.nome) + f" ({c.hp}/{c.max_hp})" for c in candidatos]
                                   + ["Voltar"])
        finally:
            self.ui.meta_opcoes = None
        return candidatos[esc] if esc < len(candidatos) else None

    def tratar_aliado(self, k, a):
        j = self.j
        nome = CONSUMIVEIS[k]["nome"]
        j.consumiveis[k] -= 1
        telemetria.registrar(self.g, "consumivel", item=k, em_combate=True, em=getattr(a, "cid", None) or a.tipo)
        with self.agindo(j, nome, a, hab="item"):
            antes = a.hp
            if k == "pocao_vida":
                a.curar(a.max_hp * bal.POCAO_VIDA)
                self.dizer(f"Você joga a {nome} para {a.nome}, que bebe num gole. (+{a.hp - antes} vida)", "verde")
            else:
                estancou = a.efeito("sangramento")
                a.remover("sangramento")
                a.curar(bal.BANDAGEM_VIDA)
                self.dizer(f"Você enfaixa {a.nome} às pressas{', e o sangue para' if estancou else ''}. "
                           f"(+{a.hp - antes} vida)", "verde")
            self.curou(a, a.hp - antes, de=j, rotulo=nome)
        return "turno"

    def analisar(self):
        for e in self.inimigos_vivos():
            self.ui.separador()
            self.dizer(f"{e.nome} — Nível {e.nivel} — Vida {e.hp}/{e.max_hp}", "vermelho+negrito")
            for t in e.tracos:
                self.dizer(f"  • {TRACOS.get(t, t)}", "cinza")
            if not self.g.conhece(e.familia):
                self.dizer("  Fraquezas e habilidades: ??? (derrote mais destas criaturas para aprender)", "cinza")
                continue
            fracos = [k for k, v in e.resist.items() if v > 1]
            fortes = [k for k, v in e.resist.items() if v < 1]
            if fracos:
                self.dizer(f"  Fraco contra: {', '.join(fracos)}", "verde")
            if fortes:
                self.dizer(f"  Resiste a: {', '.join(fortes)}", "amarelo")
            if e.habilidades:
                self.dizer("  Habilidades: " + ", ".join(NOMES_HABS_INIMIGO.get(h, h) for h in e.habilidades), "cinza")
            if getattr(e, "chave", None) and self.g.flag(f"fraqueza:{e.chave}"):
                self.dizer("  Você conhece o ponto fraco desta criatura! (+25% de dano)", "verde+negrito")

    def tentar_fuga(self):
        vivos = self.inimigos_vivos()
        media = sum(e.agi for e in vivos) / len(vivos)
        chance = max(0.15, min(0.85, 0.5 + (self.j.agi - media) * 0.03))
        if any(f["id"] == "perna" for f in self.j.ferimentos):
            chance -= 0.2
        if self.rng.random() < chance:
            self.dizer("Você recua e consegue escapar!", "verde")
            comitiva.reagir(self.g, "fuga", forca=0.5)
            return True
        self.dizer("Você tenta fugir, mas é cercado!", "vermelho")
        return False

    # ------------------------------------------------------------ aliados e inimigos
    def fase_aliados(self):
        for a in list(self.aliados):
            if not a.vivo or not self.inimigos_vivos():
                continue
            if self.processar_efeitos(a):
                continue
            if a.tipo == "comitiva":
                with self.agindo(a):
                    comitiva.agir(self, a)
                continue
            ataques = 1 + mod(self.j, "ataques_fera") if a is self.companheiro else 1
            for _ in range(ataques):
                if not self.inimigos_vivos():
                    break
                alvo = self.rng.choice(self.inimigos_vivos())
                with self.agindo(a, alvo=alvo):
                    dano = self.atacar(a, alvo, 1.0, alcance=a.alcance, crit_extra=a.crit, rotulo=a.nome)
                    if dano and a.tipo == "lobo":
                        self.aplicar(alvo, "sangramento", 2, valor=max(1, a.atk * 0.3), chance=0.3)
                    elif dano and a.tipo == "urso":
                        self.aplicar(alvo, "atordoado", 1, chance=0.15)

    def fase_inimigos(self):
        for e in list(self.inimigos):
            if not e.vivo or not self.j.vivo:
                continue
            if self.processar_efeitos(e):
                if e.vivo and e.carregando:  # atordoado no meio da preparação: o golpe devastador se perde
                    e.carregando = None
                    self.lance("atordoado", em=self.uid(e), rotulo="golpe interrompido!")
                    self.dizer(f"Atordoad{'o' if e.g == 'm' else 'a'}, {self.nome(e, True)} perde o golpe que "
                               "preparava!", "verde+negrito")
                continue
            self.checar_fase(e)
            self.agir_inimigo(e)

    def checar_fase(self, e):
        while e.fase_atual < len(e.fases) and e.hp <= e.max_hp * e.fases[e.fase_atual]["limiar"]:
            f = e.fases[e.fase_atual]
            e.fase_atual += 1
            self.ui.separador("vermelho")
            self.lance("fase", em=self.uid(e))
            self.dizer(f["texto"], "vermelho+negrito")
            e.atk *= f.get("atk", 1)
            e.poder *= f.get("poder", 1)
            e.defesa *= f.get("defesa", 1)
            e.habilidades += [h for h in f.get("habs", []) if h not in e.habilidades]
            e.tracos += [t for t in f.get("tracos", []) if t not in e.tracos]
            if e.invoca:
                HABS_INIMIGO["invocar"](self, e, None)

    def escolher_alvo_inimigo(self, e=None):
        aliados = [a for a in self.aliados if a.vivo]
        provocador = next((a for a in aliados if a.efeito("provocando")), None)
        if provocador and (e is None or not e.chefe or self.rng.random() < 0.5):
            return provocador  # o urso de pé, rugindo: todo mundo olha para ele (chefes, só às vezes)
        tanque = comitiva.alvo_inimigo(self, aliados, e)
        if tanque:
            return tanque
        if aliados:
            chance = 0.45 if any(a.tipo == "urso" for a in aliados) else 0.25
            if e is not None and e.chefe:
                chance = 0.15  # chefes sabem quem está por trás dos servos
            if self.rng.random() < chance:
                return self.rng.choice(aliados)
        return self.j

    def agir_inimigo(self, e):
        alvo = self.escolher_alvo_inimigo(e)
        if e.carregando:
            c = e.carregando
            e.carregando = None
            with self.agindo(e, c["rotulo"], alvo, hab="carregado"):
                self.atacar(e, alvo, c["mult"], rotulo=c["rotulo"])
            return
        if e.habilidades and self.rng.random() < (0.45 if e.chefe else 0.35):
            h = self.rng.choice(e.habilidades)
            with self.agindo(e, ROTULOS_HABS_INIMIGO.get(h), alvo, area=h == "varredura", hab=h):
                if HABS_INIMIGO[h](self, e, alvo) is not False:
                    return
        magico = e.ataque != "fisico" and e.poder > e.atk
        with self.agindo(e, None, alvo, hab="ataque"):
            self.atacar(e, alvo, 1.0, tipo=e.ataque if magico else "fisico",
                        alcance="distancia" if magico else "corpo", stat="poder" if magico else "atk")

    # ------------------------------------------------------------ fim
    def fim(self, resultado):
        j = self.j
        g = self.g
        telemetria.fim_combate(self, resultado)
        self.ui.atualizar()
        self.ui.fim_combate(resultado)  # o último golpe aparece antes da vitória
        g.combate_ativo = None
        comitiva.encerrar_combate(self, resultado)
        if resultado == "vitoria" and any(e.chefe for e in self.inimigos):
            comitiva.reagir(g, "coragem", forca=0.75)
        if self.companheiro:
            laco = 1 + mod(j, "laco_animal")
            j.companheiro["hp"] = min(j.companheiro["max_hp"], int(self.companheiro.hp / laco))
            if not self.companheiro.vivo:
                self.dizer(f"{self.companheiro.nome} está ferido demais para lutar até você descansar.", "cinza")
        j.efeitos = {}
        if j.classe != "mago":  # o fôlego volta em parte; a mana, devagar
            j.rec = min(j.max_rec, j.rec + int(j.max_rec * bal.FOLEGO_POS_LUTA))
        else:
            j.rec = min(j.max_rec, j.rec + int(j.max_rec * bal.MANA_POS_LUTA))
        if j.classe == "arqueiro" and self.flechas_gastas and resultado == "vitoria":
            chance = bal.RECOLHER_FLECHA + mod(j, "recolher_flecha")
            recuperadas = sum(1 for _ in range(self.flechas_gastas) if self.rng.random() < chance)
            recuperadas = min(recuperadas, self.g.max_flechas() - j.flechas)
            if recuperadas > 0:
                j.flechas += recuperadas
                self.dizer(f"Você recolhe {recuperadas} flecha(s) intacta(s) do campo.", "verde")

        if resultado == "vitoria":
            derrotados = [e for e in self.inimigos if not e.fugiu]
            self.ui.separador("verde")
            self.dizer("VITÓRIA!", "verde+negrito")
            ouro = sum(e.ouro + e.roubado for e in derrotados)
            if any(e.roubado for e in derrotados):
                self.dizer("Você recupera o ouro que lhe foi roubado.", "verde")
            g.ui.celebrar("vitoria", {"inimigos": len(derrotados), "chefe": any(e.chefe for e in derrotados)})
            g.ganhar_ouro(ouro)
            g.registrar_abates(derrotados)
            g.saque_de_combate(derrotados)
            g.ganhar_xp(comitiva.parte_do_xp(g) *
                        sum(e.xp * bal.fator_xp(e.nivel - j.nivel) for e in derrotados))
        return resultado
