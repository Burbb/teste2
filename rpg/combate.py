"""Combate por turnos."""

from contextlib import contextmanager

from . import texto as tx
from .classes import CLASSES, HABILIDADES
from .dados import TRACOS
from .entidades import Combatente
from .inimigos import HABS_INIMIGO, NOMES_HABS_INIMIGO, ROTULOS_HABS_INIMIGO
from .itens import CONSUMIVEIS
from . import comitiva, sobrevivencia, telemetria
from .talentos import custo_habilidade

DOTS = {
    "veneno": ("veneno", "verde"),
    "sangramento": ("sangramento", "vermelho"),
    "queimadura": ("queimadura", "amarelo"),
    "maldito": ("maldição", "magenta"),
}
NOMES_EFEITOS = {
    "veneno": "envenenado", "sangramento": "sangrando", "queimadura": "em chamas", "atordoado": "atordoado",
    "enfraquecido": "enfraquecido", "maldito": "amaldiçoado", "marcado": "marcado", "guarda": "em guarda",
    "fortalecido": "fortalecido", "esquiva": "esquivo", "barreira": "com barreira", "furtivo": "furtivo",
}
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
    def __init__(self, g, inimigos, emboscada=None, pode_fugir=True, titulo=None):
        self.g = g
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
        self.abertura = bool(self.j.tal("tiro_abertura"))
        self.usou_martirio = False
        self.usou_imortal = False
        self.frenesi = 0
        self.explodindo = False
        self._n_uid = 0
        _SERIE[0] += 1
        self._serie = _SERIE[0]
        self._fala_turno = -1
        self._cura_j = 0
        self._nomear()
        for e in self.inimigos:
            g.ver_criatura(e.familia)
        c = self.j.companheiro
        if c and c["hp"] > 0:
            laco = 1 + 0.2 * self.j.tal("laco_animal")
            self.companheiro = Aliado(c["nome"], int(c["max_hp"] * laco), c["atk"] * laco, c["agi"], c["tipo"],
                                      c["alcance"], c["crit"])
            self.companheiro.hp = int(c["hp"] * laco)
            self.aliados.append(self.companheiro)
        g.combate_ativo = self
        telemetria.novo_combate(self)

    # ------------------------------------------------------------ utilidades
    def dizer(self, texto, cor=None):
        self.ui.dizer(texto, cor)
        self.ui.atualizar()  # a barra de vida acompanha cada linha do combate

    def detalhe(self, texto, cor=None):
        self.ui.detalhe(texto, cor)
        self.ui.atualizar()

    # Lances: o que aconteceu, com quem e em quem, para a interface animar as cartas.
    def uid(self, c):
        if c is None:
            return None
        if c is self.j:
            return "j"
        u = getattr(c, "uid", None)
        if u is None:
            self._n_uid += 1
            u = c.uid = f"c{self._serie}-{self._n_uid}"
        return u

    def lance(self, tipo, **dados):
        self.ui.lance(tipo, **dados)

    @contextmanager
    def agindo(self, u, nome=None, alvo=None, area=False, hab=None):
        self.lance("acao", de=self.uid(u), nome=nome, alvo=self.uid(alvo), area=area, hab=hab)
        try:
            yield
        finally:
            self.lance("fim_acao", de=self.uid(u))

    def curou(self, c, valor, tipo="cura", de=None, rotulo=None):
        if valor and valor > 0:
            if c is self.j:
                self._cura_j += valor
            self.lance("cura", em=self.uid(c), de=self.uid(de), valor=int(valor), modo=tipo, rotulo=rotulo,
                       hp=max(0, c.hp), max_hp=c.max_hp)

    def nome(self, c, obj=False):
        if c is self.j:
            return "você" if obj else "Você"
        return c.nome

    def inimigos_vivos(self):
        return [e for e in self.inimigos if e.vivo]

    def _nomear(self):
        contagem = {}
        for e in self.inimigos:
            contagem[e.nome] = contagem.get(e.nome, 0) + 1
        letras = {}
        for e in self.inimigos:
            if contagem[e.nome] > 1:
                n = letras.get(e.nome, 0)
                letras[e.nome] = n + 1
                e.nome = f"{e.nome} {'ABCDEFGHIJ'[min(n, 9)]}"

    def valor_queimadura(self, u):
        v = max(2, u.poder * 0.4)
        if getattr(u, "spec", None) == "piromante":
            v *= 1.5
        return v * (1 + 0.3 * u.tal("brasas"))

    def duracao_queimadura(self, u):
        return 3 + (1 if u.tal("brasas") else 0)

    def invocar_aliado(self, nome, hp, atk, tipo="servo"):
        self.aliados.append(Aliado(nome, hp, atk, 3, tipo))

    # ------------------------------------------------------------ dano
    def atacar(self, u, alvo, mult, tipo="fisico", alcance="corpo", stat="atk", crit_extra=0.0, bonus=0,
               rotulo=None, pode_esquivar=True, detalhar=True):
        if alvo is None or not alvo.vivo:
            return 0
        prefixo = f"[{rotulo}] " if rotulo else ""
        quem = self.nome(u)
        if pode_esquivar and not alvo.efeito("atordoado"):
            esq = min(0.4, alvo.agi * 0.012)
            if alvo.efeito("esquiva"):
                esq += alvo.efeito("esquiva")["v"]
            if self.g.clima == "nevoa":
                esq += 0.05
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
        if u.jogador and u.spec == "berserker":
            m *= 1 + 0.6 * (1 - u.hp / u.max_hp)
        if not u.jogador and u not in self.aliados and self.g.noite:
            m *= 1.1
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
        if u.jogador:
            m *= 1 + (0.06 * u.tal("golpe_brutal") if alcance == "corpo" else 0.08 * u.tal("mira_firme"))

        defesa = alvo.defesa * (0.6 if alvo.efeito("maldito") else 1.0)
        furtivo = u.efeito("furtivo")
        abertura = u.jogador and self.abertura
        self.abertura = self.abertura and not u.jogador
        chance_crit = 0.05 + u.agi * 0.01 + crit_extra + 0.04 * u.tal("olho_aguia") + u.especial("critico") / 100
        crit = bool(furtivo) or abertura or self.rng.random() < chance_crit
        base = getattr(u, stat) * mult + bonus
        dano = base * m * self.rng.uniform(0.85, 1.15) * 100 / (100 + defesa * 6)
        if crit:
            dano *= (2.3 if furtivo else 1.6) + 0.2 * u.tal("golpe_sombras")
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
        if alvo is self.j and dano >= alvo.hp and alvo.tal("imortal") and not self.usou_imortal:
            self.usou_imortal = True
            dano = alvo.hp - 1
            alvo.aplicar("fortalecido", 3, 0.5)
            self.dizer("Um golpe que deveria te matar... mas você se recusa a cair! (Imortal)", "vermelho+negrito")
        alvo.hp = max(0, alvo.hp - dano)
        telemetria.contabilizar_dano(self, u, alvo, dano, crit)

        txt = f"{prefixo}{quem} atinge {self.nome(alvo, True)}: {dano} de dano"
        if tipo != "fisico":
            txt += f" ({tipo})"
        if crit:
            txt = "CRÍTICO! " + txt
        if absorvido:
            txt += f" [{absorvido} absorvido]"
        if eficacia >= 1.3:
            txt += " — super eficaz!"
        elif eficacia <= 0.7:
            txt += " — pouco eficaz."
        defensor = alvo is self.j or alvo in self.aliados
        self.lance("golpe", de=self.uid(u), em=self.uid(alvo), dano=dano, crit=crit, elemento=tipo, alcance=alcance,
                   absorvido=absorvido, eficacia="super" if eficacia >= 1.3 else "pouco" if eficacia <= 0.7 else None,
                   rotulo=rotulo, hp=max(0, alvo.hp), max_hp=alvo.max_hp)
        if detalhar:
            self.detalhe(txt, "vermelho" if defensor else "amarelo")
        else:
            self.ui.atualizar()
        if u is self.j and dano:
            roubo = 0.05 * u.tal("sede_insaciavel") + u.especial("roubo_vida") / 100
            if roubo:
                self.curou(u, u.curar(dano * roubo), "roubo")
        if alvo is self.j and dano and alcance == "corpo" and u in self.inimigos and u.vivo and alvo.especial("espinhos"):
            espinhos = alvo.especial("espinhos")
            u.hp = max(0, u.hp - espinhos)
            self.lance("golpe", de=None, em=self.uid(u), dano=espinhos, crit=False, elemento="fisico", alcance="corpo",
                       absorvido=0, eficacia=None, rotulo="Espinhos", hp=u.hp, max_hp=u.max_hp)
            self.detalhe(f"Espinhos ferem {u.nome}. ({espinhos})", "amarelo")
            if not u.vivo:
                self.ao_morrer(u, por=alvo)
        if alvo is self.j and alvo.vivo:
            if (alvo.tal("martirio") and not self.usou_martirio and alvo.hp < alvo.max_hp * 0.25):
                self.usou_martirio = True
                cura = alvo.curar(alvo.max_hp * 0.4)
                self.curou(alvo, cura, rotulo="Martírio")
                self.dizer(f"Seu sacrifício é visto. Uma luz desce e te restaura. (Martírio, +{cura} vida)",
                           "amarelo+negrito")
            if (alcance == "corpo" and alvo.tal("contra_ataque") and u in self.inimigos and u.vivo
                    and self.rng.random() < 0.15 * alvo.tal("contra_ataque")):
                self.atacar(alvo, u, 0.7, rotulo="Contra-ataque")
        if alvo is self.j and dano:
            sobrevivencia.talvez_ferir(self.g, dano, tipo, crit, u)
        if not alvo.vivo:
            self.ao_morrer(alvo, por=u, tipo=tipo)
        return dano

    def aplicar(self, alvo, efeito, turnos, valor=0, chance=1.0, rotulo=None):
        if not alvo.vivo:
            return False
        if chance < 1 and self.rng.random() >= chance:
            return False
        t = alvo.tracos
        imune = (
            (efeito == "veneno" and ("morto-vivo" in t or "construto" in t))
            or (efeito == "sangramento" and ("construto" in t or "etereo" in t))
            or (efeito == "queimadura" and alvo.resist.get("fogo", 1) < 0.5)
        )
        if imune:
            self.detalhe(f"{self.nome(alvo)} não é afetad{'o' if alvo.g == 'm' else 'a'} ({NOMES_EFEITOS[efeito]}).",
                         "cinza")
            return False
        if efeito == "atordoado" and (alvo.chefe or "gigante" in t) and self.rng.random() < 0.5:
            self.detalhe(f"{self.nome(alvo)} resiste ao atordoamento!", "cinza")
            return False
        alvo.aplicar(efeito, turnos, valor)
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
        if j.spec == "necromante":
            j.rec = min(j.max_rec, j.rec + 5)
        if j.tal("senhor_mortos") and len(self.mortos) == 1 and not c.chefe:
            self.dizer(f"{c.nome} se ergue de novo — agora sob o seu comando!", "magenta")
            self.invocar_aliado(f"{c.nome} (servo)", hp=int(c.max_hp * 0.4), atk=c.atk * 0.5)
        if por is not j:
            return
        if j.especial("vida_abate"):
            j.curar(j.especial("vida_abate"))
        if j.tal("frenesi"):
            self.frenesi = min(3, self.frenesi + 1)
            j.aplicar("fortalecido", 99, 0)
            j.efeitos["fortalecido"]["v"] = 0.1 * j.tal("frenesi") * self.frenesi
            self.dizer(f"O sangue ferve: Frenesi x{self.frenesi}!", "vermelho")
        if j.tal("assassino"):
            j.rec = min(j.max_rec, j.rec + j.max_rec // 2)
            j.aplicar("furtivo", 2, 1)
            self.dizer("Você some antes que o corpo toque o chão. (Assassino)", "magenta")
        if tipo == "fogo" and j.tal("coracao_ardente") and not self.explodindo:
            self.explodindo = True
            self.dizer(f"{c.nome} explode em chamas!", "vermelho+negrito")
            for outro in self.inimigos_vivos():
                self.atacar(j, outro, 0.6, tipo="fogo", alcance="distancia", stat="poder", pode_esquivar=False,
                            rotulo="Explosão")
            self.explodindo = False

    # ------------------------------------------------------------ fluxo
    def executar(self):
        self.ui.cena(self.titulo, tx.lista_natural([f"{e.nome} (Nv.{e.nivel})" for e in self.inimigos]), "combate")
        if not getattr(self.ui, "hud", False):
            self.dizer("Inimigos: " + ", ".join(f"{e.nome} (Nv.{e.nivel})" for e in self.inimigos), "vermelho")
        if self.companheiro:
            self.dizer(f"{self.companheiro.nome} rosna ao seu lado.", "verde")
        comitiva.preparar_combate(self)
        pular_inimigos = False
        if self.emboscada == "inimigo":
            self.dizer("Você foi pego de surpresa!", "vermelho+negrito")
            self.fase_inimigos()
            r = self._checar_fim()
            if r:
                return self.fim(r)
        elif self.emboscada == "jogador":
            self.dizer("Você tem a iniciativa! Um ataque livre antes que reajam.", "verde+negrito")
            pular_inimigos = True
        if self.j.tal("aura_protecao"):
            self.j.aplicar("barreira", 99, int(self.j.poder * 2.5))
            self.dizer(f"Uma aura dourada te envolve. (barreira de {int(self.j.poder * 2.5)})", "amarelo")
        if self.j.tal("armadilheiro"):
            alvo = self.rng.choice(self.inimigos_vivos())
            self.dizer(f"{alvo.nome} pisa numa das suas armadilhas!", "verde")
            self.aplicar(alvo, "atordoado", 1, rotulo="preso na armadilha")
            self.aplicar(alvo, "sangramento", 3, valor=max(2, self.j.atk * 0.3))

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
        if getattr(ui, "hud", False):
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
        pular = "atordoado" in c.efeitos
        rotulo = c.efeitos.get("atordoado", {}).get("r", "atordoado")
        for nome in list(c.efeitos):
            ef = c.efeitos[nome]
            if nome in DOTS and c.vivo:
                dano = max(1, int(ef["v"]))
                if nome == "queimadura" and self.g.clima == "chuva":
                    dano = max(1, int(dano * 0.7))
                c.hp = max(0, c.hp - dano)
                rot, cor = DOTS[nome]
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
        if j.especial("regen_vida") and j.hp < j.max_hp:
            j.curar(j.especial("regen_vida"))
        if self.processar_efeitos(j) or not j.vivo:
            return None
        while True:
            nome_atk = CLASSES[j.classe]["ataque"][0]
            if j.classe == "arqueiro" and j.flechas <= 0:
                nome_atk = "Golpe de Adaga — sem flechas!"
            opcoes = [f"Atacar ({nome_atk})", "Habilidades", "Itens", "Analisar inimigos"]
            if self.pode_fugir:
                opcoes.append("Fugir")
            esc = self.ui.escolher("Sua ação:", opcoes)
            if esc == 0:
                self.ataque_basico(self.escolher_alvo())
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

    def escolher_alvo(self):
        vivos = self.inimigos_vivos()
        if len(vivos) == 1:
            return vivos[0]
        self.ui.meta_opcoes = [{"alvo": self.uid(e)} for e in vivos]
        try:
            esc = self.ui.escolher("Alvo:", [f"{e.nome} ({e.hp}/{e.max_hp})" for e in vivos])
        finally:
            self.ui.meta_opcoes = None
        return vivos[esc]

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
            if dano and j.tal("laminas_envenenadas"):
                self.aplicar(alvo, "veneno", 3, valor=max(2, j.atk * 0.35), chance=0.2 * j.tal("laminas_envenenadas"))

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
        opcoes.append("Voltar")
        esc = self.ui.escolher("Habilidades:", opcoes)
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
        alvo = self.escolher_alvo() if h["alvo"] == "inimigo" else None
        j.rec -= custo
        self.tel["habilidades"][ids[esc]] = self.tel["habilidades"].get(ids[esc], 0) + 1
        self.tel["rec_gasto"] += custo
        j.flechas -= h.get("flechas", 0)
        self.flechas_gastas += h.get("flechas", 0)
        with self.agindo(j, h["nome"], alvo, area=h["alvo"] == "todos", hab=ids[esc]):
            antes, self._cura_j = j.hp, 0
            h["fn"](self, j, alvo)
            self.curou(j, j.hp - antes - self._cura_j, rotulo=h["nome"])
        return True

    def menu_itens(self):
        j = self.j
        usaveis = [k for k in USAVEIS_EM_COMBATE if j.consumiveis.get(k, 0) > 0]
        if not usaveis:
            self.dizer("Sua bolsa não tem nada útil agora.", "cinza")
            return None
        opcoes = [f"{CONSUMIVEIS[k]['nome']} x{j.consumiveis[k]} — {CONSUMIVEIS[k]['desc']}" for k in usaveis]
        esc = self.ui.escolher("Usar qual item?", opcoes + ["Voltar"])
        if esc == len(usaveis):
            return None
        k = usaveis[esc]
        if k == "bomba_fumaca":
            if not self.pode_fugir:
                self.dizer("Não há como fugir desta luta!", "vermelho")
                return None
            j.consumiveis[k] -= 1
            self.dizer("Você estoura a bomba de fumaça e some na nuvem cinzenta!", "cinza")
            return "fuga"
        with self.agindo(j, CONSUMIVEIS[k]["nome"], hab="item"):
            antes = j.hp
            self.g.usar_consumivel(k)
            self.curou(j, j.hp - antes, rotulo=CONSUMIVEIS[k]["nome"])
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
            ataques = 2 if a is self.companheiro and self.j.tal("matilha") else 1
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
            laco = 1 + 0.2 * j.tal("laco_animal")
            j.companheiro["hp"] = min(j.companheiro["max_hp"], int(self.companheiro.hp / laco))
            if not self.companheiro.vivo:
                self.dizer(f"{self.companheiro.nome} está ferido demais para lutar até você descansar.", "cinza")
        j.efeitos = {}
        if j.classe != "mago":  # o fôlego volta em minutos; a mana, devagar
            j.rec = j.max_rec
        else:
            j.rec = min(j.max_rec, j.rec + j.max_rec // 5)
        if j.classe == "arqueiro" and self.flechas_gastas and resultado == "vitoria":
            chance = 0.5 + 0.2 * j.tal("aljava_funda")
            recuperadas = sum(1 for _ in range(self.flechas_gastas) if self.rng.random() < chance)
            if recuperadas:
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
                        sum(e.xp * max(0.2, min(1.25, 1 + 0.08 * (e.nivel - j.nivel))) for e in derrotados))
        return resultado
