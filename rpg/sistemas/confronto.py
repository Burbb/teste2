"""Inimigos do lugar, grupos, o combate em si, abates e saque."""

from .. import balanceamento as bal
from .. import texto as tx
from ..combate import Combate
from ..dados import BIOMAS, FAMILIAS
from .. import inimigos
from ..inimigos import criar
from ..itens import gerar_equip
from ..mundo import nivel_regiao, vizinhos
from ..regras import NIVEL_MIN_FAMILIA, Derrota


# Criaturas da Fenda e o perigo mínimo do lugar para elas aparecerem fora do bioma delas.
CRIATURAS_DA_FENDA = ((3, "caido"), (4, "cao_infernal"), (4, "cria_vazio"), (5, "abominacao"))


class Confronto:
    # ================================================================ inimigos e combate
    def nivel_inimigo(self, bonus=0):
        variacao = [-1, 0, 0] if self.nivel_local() <= 2 else [-1, 0, 0, 1]
        n = self.nivel_local() + self.rng.choice(variacao) + bonus
        return max(1, min(15, n))

    def mundo_vizinhos(self):
        return vizinhos(self.mundo, self.loc)

    def nivel_local(self):
        return nivel_regiao(self.loc)

    def inimigo(self, familia, bonus=0, afixo=None, nome_unico=None, nivel=None):
        return criar(self.rng, familia, nivel or self.nivel_inimigo(bonus), afixo, nome_unico)

    def afixo_aleatorio(self):
        p = 0.10 + self.loc["perigo"] * 0.03
        if self.j.nivel <= 1 or not self.chance(p):
            return None
        if self.loc["perigo"] >= 4 and self.chance(0.3):  # perto da Fenda, o Vazio toca as feras
            return "corrompido"
        return self.sortear(["feroz", "robusto", "agil", "venenoso", "anciao", "flamejante"])

    def familias_locais(self):
        nv = self.nivel_local()
        familias = [f for f in BIOMAS[self.bioma]["familias"] if NIVEL_MIN_FAMILIA.get(f, 1) <= nv]
        # Quanto mais perto da Fenda (os lugares perigosos, a caminho da Cidadela), mais criaturas dela.
        familias += [f for perigo, f in CRIATURAS_DA_FENDA
                     if self.loc["perigo"] >= perigo and NIVEL_MIN_FAMILIA.get(f, 1) <= nv and f not in familias]
        if self.noite and self.bioma in ("ruinas", "pantano", "planicie"):
            familias.append("espectro")
        return familias

    def grupo(self, familia=None, n=None, bonus=0):
        """Gera um encontro: grupo comum, bando de campeões ou um único nomeado com escolta."""
        familia = familia or self.sortear(self.familias_locais())
        f = FAMILIAS[familia]
        nv = self.nivel_local()
        tipo = "normal"
        if n is None:
            lo, hi = f["grupo"]
            n = self.rng.randint(lo, hi)
            if nv <= 2:
                n = 1 if self.chance(bal.GRUPO_SOZINHO_INICIO) else min(n, bal.GRUPO_MAX_CEDO)
            elif nv <= 4:
                n = 1 if self.chance(bal.GRUPO_SOZINHO_MEIO) else min(n, bal.GRUPO_MAX_CEDO)
            for _ in self.comitiva:  # uma comitiva chama atenção: mais inimigos aparecem
                if self.chance(bal.COMITIVA_ATRAI):
                    n = min(n + 1, hi + 1)
            r = self.rng.random()
            if nv >= 5 and r < 0.03 + nv * 0.006:
                tipo = "unico"
            elif nv >= 4 and r < 0.08 + nv * 0.012:
                tipo = "campeoes"

        if tipo == "campeoes":
            afixo = self.sortear(["feroz", "robusto", "agil", "venenoso", "flamejante", "corrompido"])
            grupo = [self.inimigo(familia, bonus, afixo) for _ in range(max(2, min(n, 3)))]
            for e in grupo:
                e.max_hp = int(e.max_hp * 1.25)
                e.hp = e.max_hp
                e.xp = int(e.xp * 1.4)
                e.nome = "Campeão " + e.nome if e.g == "m" else "Campeã " + e.nome
            self.dizer("Um bando de CAMPEÕES: eles se movem juntos, com um brilho azulado nos olhos.",
                       "azul+negrito")
        elif tipo == "unico":
            a1, a2 = self.rng.sample(["feroz", "robusto", "agil", "venenoso", "anciao", "flamejante", "corrompido"], 2)
            chefe = self.inimigo(familia, bonus + 1, a1, nome_unico=tx.nome_proprio(self.rng))
            inimigos.adicionar_afixo(chefe, a2)
            escolta = []
            if f["grupo"][1] > 1:
                escolta = [self.inimigo(familia, bonus) for _ in range(self.rng.randint(1, 2))]
            grupo = [chefe] + escolta
            self.dizer(f"Um nome sussurrado com medo nas vilas: {chefe.nome}. Uma criatura ÚNICA.",
                       "amarelo+negrito")
        else:
            grupo = [self.inimigo(familia, bonus, self.afixo_aleatorio()) for _ in range(n)]
            if n == 1 and f["grupo"][1] == 1 and nv >= 3 and self.chance(0.25):
                outra = self.sortear(BIOMAS[self.bioma]["familias"])
                if FAMILIAS[outra]["grupo"][1] > 1:
                    grupo.append(self.inimigo(outra, bonus))
        if familia == "caido" and self.chance(0.35 if nv <= 4 else 0.6):
            grupo.append(self.inimigo("xama_caido", bonus))
        return grupo

    def combate(self, inimigos, emboscada=None, pode_fugir=True, titulo=None, sozinho=False):
        self.fechar_espolio()  # o espólio de uma luta anterior aparece antes da próxima começar
        r = Combate(self, inimigos, emboscada, pode_fugir, titulo, sozinho=sozinho).executar()
        if r == "derrota":
            causa = f"Você tombou diante de {tx.lista_natural([e.nome for e in inimigos])}."
            if self.hardcore:
                self.fim_de_jogo(causa)
            self.dizer(causa, "vermelho+negrito")
            raise Derrota()
        if r == "fuga" and not self.nemesis:
            elite = next((e for e in inimigos if e.vivo and (e.afixo or e.unico) and not e.chefe
                          and e.familia in FAMILIAS and not e.chave), None)
            if elite:
                nome = elite.nome.split(",")[0] if elite.unico else tx.nome_proprio(self.rng)
                self.nemesis = {"familia": elite.familia, "afixo": elite.afixo or "feroz", "nome": nome,
                                "nivel": elite.nivel + 1, "pronto": self.passos + 4, "vezes": 0}
                self.dizer("Enquanto foge, você ouve um rugido às suas costas. Algo te marcou como presa. "
                           "Você ainda vai rever essa criatura...", "magenta")
        return r

    def registrar_abates(self, derrotados):
        self.estatisticas["abates"] += len(derrotados)
        for e in derrotados:
            if e.familia in self.bestiario:
                self.bestiario[e.familia]["abates"] += 1
                if self.bestiario[e.familia]["abates"] == 5:
                    f = FAMILIAS[e.familia]
                    if self.ui.conquistas_na_tela:  # uma faixa com a criatura, como as outras conquistas
                        self.ui.celebrar("mestre", {"familia": e.familia, "plural": f["plural"], "tracos": f["tracos"]})
                    else:
                        self.dizer(f"Você agora conhece {f['plural']} como ninguém. "
                                   f"(mestre caçador: +10% de dano contra eles)", "verde")
            if e.chave == "nemesis":
                self.nemesis = None
                self.dizer("Seu nêmesis finalmente tomba. Você sente um peso sair dos ombros.", "verde+negrito")
                self.ganhar_ouro(30 + 10 * self.j.nivel)
        # Contratos: conta a luta inteira de uma vez e anuncia uma vez só (ou progresso, ou concluído).
        for c in self.contratos:
            if c.get("concluido"):
                continue
            if c["tipo"] == "caca" and self.loc["id"] == c["local"]:
                n = sum(1 for e in derrotados if e.familia == c["familia"])
                if not n:
                    continue
                c["feito"] = min(c["total"], c["feito"] + n)
                if c["feito"] >= c["total"]:
                    c["concluido"] = True
                self.anunciar_contrato(c, f"{c['feito']}/{c['total']} {FAMILIAS[c['familia']]['plural']}")
            elif c["tipo"] == "alvo" and any(e.chave == c["chave"] for e in derrotados):
                c["concluido"] = True
                self.anunciar_contrato(c)

    def anunciar_contrato(self, c, progresso=""):
        """O contrato andou nesta luta: entra no quadro do espólio (tela gráfica) ou vira uma linha (texto)."""
        if self.espolio_aberto is not None:
            self.espolio_aberto["contratos"].append({"desc": c["desc"], "progresso": progresso,
                                                     "concluido": bool(c.get("concluido"))})
        elif c.get("concluido"):
            self.dizer(f"Contrato concluído: {c['desc']} Receba a recompensa em qualquer vila.", "verde")
        else:
            self.ui.efeito(f"Contrato: {progresso}", "info")

    def saque_de_combate(self, derrotados):
        elites = sum(1 for e in derrotados if e.afixo or e.unico)
        chefe = any(e.chefe for e in derrotados)
        if any("humano" in e.tracos for e in derrotados) and self.chance(0.35):
            self.contar_achado(tx.concordar("Nos alforjes {do morto|dos mortos}, um pouco de comida.", derrotados), "cinza")
            self.dar_provisoes(1)
        if self.chance(0.15 + 0.1 * elites):
            self.dar(self.sortear(["bandagem", "bandagem", "tocha", "tocha", "pocao_vida", "tonico", "antidoto"]))
        if self.j.classe == "arqueiro" and any(e.familia in ("bandido", "mercenario") for e in derrotados) \
                and self.chance(0.3):
            self.contar_achado(tx.concordar("Você encontra algumas flechas entre os pertences {do inimigo|dos inimigos}.",
                                            derrotados), "verde")
            self.dar_flechas(self.rng.randint(2, 5))
        if chefe or self.chance(0.07 + 0.2 * elites):
            nivel = min(max(e.nivel for e in derrotados), self.j.nivel + 2)
            self.oferecer_equip(gerar_equip(self.rng, self.j.classe, nivel, qualidade=1 if chefe else 0))
