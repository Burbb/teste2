"""Guardiões dos covis e a batalha final."""

from .. import balanceamento as bal
from .. import texto as tx
from ..dados import GUARDIOES
from ..inimigos import instanciar_antagonista, instanciar_guardiao
from .. import comitiva
from ..mundo import nivel_regiao


class Chefes:
    # ================================================================ chefes
    def nivel_guardiao(self, loc):
        return nivel_regiao(loc) + 1

    def enfrentar_guardiao(self):
        loc = self.loc
        gspec = loc["guardiao"]
        t = GUARDIOES[gspec["bioma"]][gspec["idx"]]
        self.ui.cena(gspec["nome"], f"guardião · {loc['nome']}", "chefe")
        self.narrar(t["intro"], "vermelho")
        chave = f"guardiao:{loc['id']}"
        if self.flag(f"fraqueza:{chave}"):
            self.dizer("Você se lembra do que ouviu sobre o ponto fraco desta criatura.", "verde")
        if not self.menu("Não haverá como fugir depois de começar.", [("Lutar!", True), ("Recuar por enquanto",
                                                                                         False)]):
            return
        nivel = self.nivel_guardiao(loc)
        chefe = instanciar_guardiao(gspec, nivel)
        chefe.chave = chave
        r = self.combate([chefe], pode_fugir=False, titulo=f"Guardião: {gspec['nome']}")
        if r == "vitoria":
            gspec["derrotado"] = True
            self.j.sigilos.append(loc["bioma"])
            self.estatisticas["chefes"] += 1
            festa = self.ui.conquistas_na_tela  # a festa do Sigilo já mostra a runa e o ponto de talento
            if not festa:
                self.ui.titulo(f"SIGILO OBTIDO ({len(self.j.sigilos)}/3)", "amarelo+negrito")
                self.dizer("Uma runa ardente se grava na palma da sua mão.", "amarelo")
            self.mudar_reputacao(5)
            self.ganhar_ponto_talento(anunciar=not festa)
            self.ui.celebrar("sigilo", {"sigilos": len(self.j.sigilos), "guardiao": gspec["nome"],
                                        "pontos": self.j.pontos_talento})
            if len(self.j.sigilos) >= 3:
                self.dizer(f"Os três Sigilos pulsam juntos. O caminho para {self.mundo['locais'][-1]['nome']} "
                           f"está aberto!", "magenta+negrito")
        self.avancar_periodo()
        self.pausar()

    def batalha_final(self):
        a = self.antagonista
        j = self.j
        self.ui.cena(a["nome"], "o salão do trono", "chefe")
        falas = {
            "guerreiro": "Tanto aço, tanta coragem. Eu também empunhei uma espada, um dia.",
            "arqueiro": "Você mira bem. Mas como se acerta o que não tem coração?",
            "mago": "Você sente, não sente? O poder do Vazio chamando por você. Somos iguais.",
        }
        self.narrar(f"No topo da escadaria, {a['curto']} te espera num trono de pedra rachada.", "magenta")
        self.narrar(f"\"{j.nome}. {falas[j.classe]}\"", "magenta+negrito")
        if j.reputacao <= -20:
            self.narrar("\"E que reputação a sua! Matou, roubou, mentiu. Junte-se a mim — você já está no "
                        "meio do caminho.\"", "magenta")
        if j.reputacao >= 20:
            self.narrar("\"Herói do povo, é? Vamos ver se as preces deles te salvam.\"", "magenta")
        self.pausar()

        guarda = self.inimigo("cavaleiro_sombrio", nome_unico=tx.nome_proprio(self.rng),
                             nivel=self.nivel_local() + 1)
        self.dizer("Um cavaleiro de armadura negra se coloca entre vocês.", "vermelho")
        self.combate([guarda], pode_fugir=False, titulo="O ÚLTIMO GUARDA")

        chefe = instanciar_antagonista(a, bal.ANTAGONISTA_NIVEL)
        traidores = comitiva.antes_da_batalha_final(self)
        extras = []
        if "yara" in traidores:
            yara = self.inimigo("bruxa_brejo", nome_unico="Yara", nivel=chefe.nivel - 1)
            yara.nome = "Yara, Voz da Fenda"
            yara.max_hp = yara.hp = int(yara.max_hp * 1.6)
            yara.poder = int(yara.poder * 1.4)
            extras.append(yara)
        if self.aliados_finais:
            self.ui.separador("verde")
            self.dizer("Mas você não está só.", "verde+negrito")
            dano_max = int(chefe.max_hp * 0.45)  # os aliados ajudam, mas o golpe final é seu
            for al in self.aliados_finais:
                self.narrar(al["texto"], "verde")
                if al["efeito"] == "dano":
                    perda = min(int(chefe.max_hp * al["valor"]), dano_max - (chefe.max_hp - chefe.hp))
                    if perda > 0:
                        chefe.hp -= perda
                        self.dizer(f"  ({a['curto']} perde {perda} de vida)", "verde")
                elif al["efeito"] == "cura":
                    j.hp = j.max_hp
                    self.dizer("  (vida restaurada)", "verde")
                elif al["efeito"] == "forca":
                    atual = j.efeito("fortalecido")
                    bonus = min(0.3, (atual["v"] if atual else 0) + 0.1)
                    j.aplicar("fortalecido", 99, bonus)
                    j.efeitos["fortalecido"]["v"] = bonus
                    self.dizer(f"  (seu dano aumenta em {int(bonus * 100)}% nesta batalha)", "verde")
            self.pausar()
        j.hp = max(j.hp, j.max_hp // 2)
        self.combate([chefe] + extras, pode_fugir=False, titulo="O FIM DE TODAS AS COISAS")
        self.vitoria()
