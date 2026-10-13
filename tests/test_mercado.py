"""A tela do mercado (1.71.0): o que ela mostra vem pronto do motor. Cada suprimento diz o que você carrega (`tem`,
com o `teto` na comida e nas flechas) separado do que o mercador ainda tem (`estoque`), e o que não se compra agora
traz o motivo escrito (esgotado, carga cheia, ouro); as peças à venda e a recompra também. As regras de compra, venda e
recompra não mudaram: os motivos são as mesmas contas."""

import random
import tempfile
import unittest

from rpg import sobrevivencia
from rpg.itens import gerar_equip
from rpg.jogo import Jogo
from rpg.regras import LIMITE_MOCHILA
from rpg.ui import BotUI


def no_mercado(classe="arqueiro", ouro=300):
    g = Jogo(BotUI(random.Random(3)), seed=3, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Robô", classe)
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    g.j.ouro = ouro
    g.recompra = []
    return g


def suprimento(g, k):
    return next(c for c in g.dados_loja()["consumiveis"] if c["id"] == k)


class TestSuprimentos(unittest.TestCase):
    def test_tem_e_estoque_separados(self):
        g = no_mercado()
        c = suprimento(g, "provisoes")
        self.assertEqual((c["tem"], c["teto"]), (g.j.provisoes, sobrevivencia.MAX_PROVISOES))
        self.assertEqual(c["estoque"], g.estoque_suprimentos()["provisoes"])
        f = suprimento(g, "flechas")
        self.assertEqual((f["tem"], f["teto"]), (g.j.flechas, g.max_flechas()))
        self.assertIsNone(suprimento(g, "tocha")["teto"])

    def test_motivos(self):
        g = no_mercado()
        g.j.provisoes = sobrevivencia.MAX_PROVISOES
        self.assertEqual(suprimento(g, "provisoes")["motivo"], "Você já carrega o máximo de comida.")
        g.j.flechas = g.max_flechas()
        self.assertEqual(suprimento(g, "flechas")["motivo"], "A aljava está cheia.")
        g.j.ouro = 0
        self.assertEqual(suprimento(g, "tocha")["motivo"], "Ouro insuficiente.")
        g.j.ouro = 300
        estoque = g.estoque_suprimentos()["tocha"]
        self.assertTrue(g.comprar_suprimento("tocha", estoque))  # leva tudo o que havia hoje
        self.assertEqual(suprimento(g, "tocha")["motivo"], "Esgotado: o mercador reabastece amanhã cedo.")
        self.assertFalse(g.comprar_suprimento("tocha"))  # a regra de sempre recusa do mesmo jeito

    def test_compra_atualiza_tem_e_estoque(self):
        g = no_mercado()
        antes = suprimento(g, "bandagem")
        if antes["estoque"] < 1:
            self.skipTest("sem bandagem hoje nesta semente")
        g.comprar_suprimento("bandagem", 1)
        depois = suprimento(g, "bandagem")
        self.assertEqual((depois["tem"], depois["estoque"]), (antes["tem"] + 1, antes["estoque"] - 1))
        self.assertEqual(g.j.ouro, 300 - antes["preco"])


class TestEquipamentosERecompra(unittest.TestCase):
    def test_motivo_da_peca_a_venda(self):
        g = no_mercado(ouro=0)
        self.assertTrue(all(e["motivo"] == "Ouro insuficiente." for e in g.dados_loja()["equipamentos"]))
        g.j.ouro = 10000
        rng = random.Random(1)
        while len(g.j.mochila) < LIMITE_MOCHILA:
            g.j.mochila.append(gerar_equip(rng, "arqueiro", 1))
        for it, d in zip(g.estoque(), g.dados_loja()["equipamentos"]):
            vago = g.pode_usar(it) and not g.j.equip.get(g.espaco_para(it))
            self.assertEqual(d["motivo"], None if vago else "Mochila cheia: venda ou largue algo antes.")
            if not vago:
                self.assertFalse(g.comprar_equipamento(it, g.estoque()))  # a regra concorda

    def test_recompra_pelo_mesmo_preco_com_motivo(self):
        g = no_mercado()
        it = gerar_equip(random.Random(2), "arqueiro", 1)
        g.j.mochila.append(it)
        g.vender_item(it)
        r = g.dados_loja()["recompra"]
        self.assertEqual((len(r), r[0]["preco"], r[0]["motivo"]), (1, it["preco"] // 2, None))
        g.j.ouro = 0
        self.assertEqual(g.dados_loja()["recompra"][0]["motivo"], "Ouro insuficiente.")
        g.j.ouro = 300
        self.assertTrue(g.recomprar_item(0))
        self.assertIn(it, g.j.mochila)


if __name__ == "__main__":
    unittest.main()
