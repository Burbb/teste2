"""A noite e a falta de tocha ditas antes da luta (E9): a nota das salas da capela (a tocha que se gasta, ou o inimigo
que ataca primeiro sem ela, e o que a noite muda), as linhas do lugar ao lado do nível-base, a dica do modificador da
noite sem prometer bando maior onde o tamanho é fixo, e o texto de quem entra sem luz. Nada disso muda a luta."""

import tempfile
import unittest

from rpg import balanceamento as bal, missoes, sobrevivencia
from rpg.jogo import Jogo
from rpg.web.estado import estado, modificadores
from tests.test_missoes import Roteiro, ir


def na_capela(etapa="capela", periodo=1, tochas=3):
    g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", "guerreiro", "turvo")
    missoes.registro(g, "febre_do_turvo").update(etapa=etapa, cenas=["abertura", "capela_exterior"])
    ir(g, "capela_afogada")
    g.periodo, g.j.consumiveis["tocha"] = periodo, tochas
    return g


def riscos(g):
    return next(o[2].get("riscos") for o in missoes.opcoes(g) if o[1][2] in ("nave", "sacristia", "ossuario"))


class TestSalas(unittest.TestCase):
    def test_indicadores_da_sala_de_dia_e_de_noite(self):
        dia = riscos(na_capela())  # a capela é escura de dia também
        self.assertEqual([(r["icone"], r["texto"], r["tipo"]) for r in dia], [("tocha", "−1 tocha", "custo")])
        self.assertIn("você tem 3", dia[0]["dica"])
        noite = riscos(na_capela(periodo=3))
        self.assertEqual([(r["icone"], r["texto"], r["tipo"]) for r in noite],
                         [("tocha", "−1 tocha", "custo"), ("lua", "+1 nível · +10% dano", "noite")])
        sem = riscos(na_capela(tochas=0))
        self.assertEqual([(r["icone"], r["texto"], r["tipo"]) for r in sem],
                         [("tocha_apagada", "Sem luz: inimigo age primeiro", "perigo")])
        self.assertIn("o inimigo mais rápido ataca antes de você", sem[0]["dica"])
        for etapa in ("sacristia", "ossuario"):
            self.assertEqual(riscos(na_capela(etapa))[0]["texto"], "−1 tocha")

    def test_texto_junta_os_riscos_ao_rotulo(self):
        g = na_capela(periodo=3, tochas=0)
        g.ui.roteiro = ["Explorar"]
        g.menu("O que você faz?", missoes.opcoes(g) + [("Explorar a região", "explorar")])
        self.assertIn("Entrar na capela pelo buraco do canal — Sem tocha: o inimigo mais rápido ataca primeiro. Noite: "
                      "inimigos +1 nível e +10% de dano.", g.ui.ofertas[-1])

    def test_guardia_so_o_dano(self):
        g = na_capela(periodo=3)
        r = sobrevivencia.riscos_sala(g, guardiao=True)
        self.assertEqual([x["texto"] for x in r], ["−1 tocha", "+10% dano"])
        self.assertIn("o nível dela não muda", r[1]["dica"])
        self.assertEqual(sobrevivencia.nota_sala(g, guardiao=True),
                         "Gasta 1 tocha (você tem 3). Noite: +10% de dano dos inimigos.")

    def test_sarilho_so_o_que_vale_para_cada_opcao(self):
        g = na_capela("fundo", periodo=3)
        metas = []
        g.ui.escolher = lambda p, o: (metas.append(list(g.ui.meta_opcoes or [])), len(o) - 1)[1]
        missoes._soltar_correntes(g, "febre_do_turvo")
        mao, classe = metas[0][0], metas[0][1]
        self.assertEqual([r["texto"] for r in mao["riscos"]], ["−1 tocha", "+1 nível · +10% dano"])  # à mão, a luta vem
        self.assertNotIn("riscos", classe)  # pela classe, só se a trava não ceder: sem custo de luz prometido
        self.assertNotIn("tocha", classe["nota"])

    def test_sem_tocha_na_sala_o_texto_diz_a_emboscada_certa(self):
        g = na_capela(tochas=0)
        self.assertFalse(sobrevivencia.acender_tocha(g, sala=True))
        self.assertIn("o inimigo mais rápido ataca antes de você", g.ui.ditos[-1])
        g.sem_luz = False
        sobrevivencia.acender_tocha(g)
        self.assertIn("emboscadas mais prováveis", g.ui.ditos[-1])  # fora das salas, só mais provável


class TestLugar(unittest.TestCase):
    def test_nivel_base_e_o_que_a_noite_soma(self):
        g = na_capela(periodo=3)
        local = estado(g)["local"]
        self.assertEqual(local["nivel"], g.nivel_local())  # o nível-base não muda
        textos = [r["texto"] for r in local["riscos"]]
        self.assertEqual(textos[0], "Noite: inimigos +1 nível e +10% de dano")
        self.assertIn("cada sala", textos[1])
        g.periodo = 1
        self.assertEqual([r["texto"] for r in estado(g)["local"]["riscos"]],
                         ["Escuro: explorar, caçar, viajar e cada sala gastam 1 tocha por vez (você tem 3)"])

    def test_tipo_de_cada_aviso_para_a_cor(self):
        # a noite em amarelo, o gasto normal de tocha neutro, a falta de luz em vermelho (a tela só pinta)
        g = na_capela(periodo=3)
        self.assertEqual([r["tipo"] for r in estado(g)["local"]["riscos"]], ["noite", "custo"])
        g.j.consumiveis["tocha"] = 0
        self.assertEqual([r["tipo"] for r in estado(g)["local"]["riscos"]], ["noite", "perigo"])

    def test_vila_e_dia_claro_sem_linhas(self):
        g = na_capela()
        ir(g, "bosque_do_moinho")
        self.assertEqual(estado(g)["local"]["riscos"], [])
        ir(g, "vau_do_turvo")
        g.periodo = 3
        self.assertEqual(estado(g)["local"]["riscos"], [])

    def test_cabecalho_do_texto(self):
        g = na_capela(periodo=3)
        subs = []
        g.ui.cena = lambda titulo, sub=None, tipo="evento": subs.append(sub)
        g.cabecalho()
        self.assertIn("inimigos Nv.3 (+1 à noite)", subs[-1])
        self.assertIn("Noite: inimigos +1 nível e +10% de dano", " ".join(g.ui.ditos))

    def test_dica_da_noite_nao_promete_bando_onde_e_fixo(self):
        g = na_capela(periodo=3)
        noite = next(m for m in modificadores(g) if m["icone"] == "lua")
        self.assertNotIn("mais vezes em bando", noite["detalhe"])
        self.assertIn("nas salas, o número é o mesmo", noite["detalhe"])
        self.assertIn(f"{round((bal.NOITE_INIMIGOS - 1) * 100)}% mais dano", noite["detalhe"])


if __name__ == "__main__":
    unittest.main()
