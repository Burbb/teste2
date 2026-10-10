"""A luta: quem está nela, o laço dos turnos, os lances que a tela anima e o fim (recompensas e o que sobra)."""

from contextlib import contextmanager

from .. import texto as tx
from ..modificadores import disparar, mod, nomes
from ..estados import ESTADOS, NOMES, NOMES as NOMES_EFEITOS, dano_do_tique
from ..entidades import Combatente
from .. import comitiva, telemetria
from .. import balanceamento as bal
from .golpe import Golpes
from .heroi import AcoesDoHeroi
from .turnos import TurnosDosOutros



class Aliado(Combatente):
    def __init__(self, nome, hp, atk, agi=4, tipo="servo", alcance="corpo", crit=0.0):
        super().__init__(nome, hp, atk, 3, agi, 0)
        self.tipo = tipo
        self.alcance = alcance
        self.crit = crit


_SERIE = [0]


class Combate(Golpes, AcoesDoHeroi, TurnosDosOutros):
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
        self.motivo_abertura = ", ".join(nomes(self.j, "abertura")) or None  # quem dá o crítico (Tiro de Abertura...)
        # O que talentos, itens e passivas lembram durante esta luta ("já usei o Martírio", as cargas do Frenesi):
        # cada um guarda o seu pelo próprio id, e a luta seguinte começa do zero (talentos.uma_vez_por_luta).
        self.memoria = {}
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
    def salva(self, hab=None, anim=None):
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
                self.ui.lance("salva", hab=hab, lances=lances, **({"anim": anim} if anim else {}))
            self.ui.fim_salva()
            for fn, texto, cor in textos:
                fn(texto, cor)
            self.ui.atualizar()

    @contextmanager
    def agindo(self, u, nome=None, alvo=None, area=False, hab=None, anim=None):
        """anim: o jeito de a tela animar a ação (o `anim` do catálogo da habilidade: "grito", "redemoinho"...)."""
        self.lance("acao", de=self.uid(u), nome=nome, alvo=self.uid(alvo), area=area, hab=hab,
                   **({"anim": anim} if anim else {}))
        try:
            if area:  # golpes em área acertam todos juntos (no Redemoinho, giro a giro)
                with self.salva(hab, anim):
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

    def invocar_aliado(self, nome, hp, atk, tipo="servo"):
        a = Aliado(nome, hp, atk, 3, tipo)
        self.aliados.append(a)
        self.ui.atualizar()  # a carta entra na arena já, antes de o invocado agir (a tela a faz subir da terra)
        return a

    # ------------------------------------------------------------ fluxo
    def executar(self):
        self.ui.cena(self.titulo, tx.lista_natural([f"{e.nome} (Nv.{e.nivel})" for e in self.inimigos]), "combate")
        if not self.ui.hud:
            self.dizer(tx.concordar("{Inimigo|Inimigos}: ", self.inimigos) + ", ".join(f"{e.nome} (Nv.{e.nivel})" for e in self.inimigos), "vermelho")
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
            # Como a sua surpresa: um golpe livre, do mais rápido deles, e não a rodada do bando inteiro
            # (quatro cães de uma vez matavam antes de você agir uma vez).
            primeiro = max(self.inimigos_vivos(), key=lambda e: e.agi)
            if not self.ui.surpresa_na_tela:  # na tela gráfica, a surpresa é a sua carta tremendo (o lance abaixo)
                self.dizer(f"Você foi pego de surpresa! {tx.maiuscula(self.nome(primeiro))} ataca antes que você reaja.",
                           "vermelho+negrito")
            self.lance("surpresa", de=self.uid(primeiro), alvos=["j"])
            self.fase_inimigos(apenas=primeiro)
            r = self._checar_fim()
            if r:
                return self.fim(r)
        elif self.emboscada == "jogador":
            if not self.ui.surpresa_na_tela:
                self.dizer(tx.concordar("Você tem a iniciativa! Um turno livre antes que {reaja|reajam}: ataque agora e "
                                        "o golpe sai {bonus}% mais forte.", self.inimigos,
                                        bonus=round(bal.INICIATIVA_BONUS * 100)), "verde+negrito")
            pular_inimigos = True
            # A iniciativa é um estado à vista na sua carta (o tique do começo do seu turno a deixa em 1) e a tela
            # mostra os inimigos pegos de surpresa, no lugar da frase.
            self.j.aplicar("iniciativa", 2, bal.INICIATIVA_BONUS)
            self.lance("surpresa", de="j", alvos=[self.uid(e) for e in self.inimigos_vivos()])
        disparar(self, self.j, "inicio_combate")  # Aura de Proteção, Armadilheiro...

        while True:
            self.turno += 1
            if self.fase_jogador() == "fuga":
                return self.fim("fuga")
            # A surpresa é aquele turno: quem o usa para outra coisa (um buff, uma poção) perde o bônus, em vez
            # de guardá-lo para o golpe do turno seguinte.
            self.j.remover("iniciativa")
            self.checar_limiares()
            r = self._checar_fim()
            if r:
                return self.fim(r)
            if not pular_inimigos:  # o turno da surpresa é só seu: a comitiva e o animal entram no seguinte
                self.fase_aliados()
                self.checar_limiares()
                r = self._checar_fim()
                if r:
                    return self.fim(r)
            if pular_inimigos:
                pular_inimigos = False
            else:
                self.fase_inimigos()
                self.checar_limiares()
                r = self._checar_fim()
                if r:
                    return self.fim(r)
            self.j.rec = min(self.j.max_rec, self.j.rec + self.j.regen)

    def checar_limiares(self):
        """Um inimigo com piso de vida (Inimigo.piso) que chegou nele tem o seu momento, uma vez, no primeiro ponto
        seguro depois do golpe: o fim da sua vez, da vez da comitiva, ou antes de qualquer inimigo agir. O que
        acontece ali (o rito da guardiã) é decisão do conteúdo que pôs o piso (`ao_limiar`)."""
        for e in list(self.inimigos):
            if e.vivo and e.piso is not None and e.hp <= e.piso and e.ao_limiar:
                momento, e.ao_limiar = e.ao_limiar, None
                momento(self, e)

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
                dano = dano_do_tique(self, nome, ef)
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
            if ESTADOS[trava]["depois"]:  # firme até o próximo turno dele: um turno perdido de cada vez
                c.aplicar(ESTADOS[trava]["depois"], 1)
        return pular or not c.vivo

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
                self.dizer(f"Você recolhe {tx.plural(recuperadas, 'flecha intacta', 'flechas intactas')} do campo.", "verde")

        if resultado == "vitoria":
            derrotados = [e for e in self.inimigos if not e.fugiu]
            self.ui.separador("verde")
            if not g.ui.conquistas_na_tela:  # na tela, a faixa de Vitória e o quadro do espólio dizem isso
                self.dizer("VITÓRIA!", "verde+negrito")
            ouro = sum(e.ouro + e.roubado for e in derrotados)
            if any(e.roubado for e in derrotados):
                self.dizer("Você recupera o ouro que lhe foi roubado.", "verde")
            g.ui.celebrar("vitoria", {"inimigos": len(derrotados), "chefe": any(e.chefe for e in derrotados)})
            # O espólio: o ouro, o XP, os contratos que andaram e o que se acha nos corpos. Na tela gráfica tudo
            # isso (e o que o evento ainda der logo depois) vai para um quadro só, antes da próxima pergunta.
            g.abrir_espolio()
            xp = int(comitiva.parte_do_xp(g) * sum(e.xp * bal.fator_xp(e.nivel - j.nivel) for e in derrotados))
            g.ganhar_ouro(ouro, fonte="lutas")
            g.registrar_abates(derrotados)
            g.ganhar_xp(xp)
            g.saque_de_combate(derrotados)
        return resultado
