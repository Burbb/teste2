"""A bandagem só enfaixa (1.70.0): uma ferida aberta do herói (corte, mordida, queimadura) ainda sem tratar, uma por
uso, a primeira da lista. Não recupera vida, não estanca o sangramento da luta, não cura infecção, não serve na comitiva
nem no animal. Sem ferida para enfaixar, o item fica à vista e apagado, com o motivo; tentar não gasta item, tempo nem
sorteio. E as flechas recolhidas do campo, que na tela vão para o quadro do espólio."""

import random
import tempfile
import unittest
from unittest import mock

from rpg import balanceamento as bal
from rpg import sobrevivencia
from rpg.combate import Combate
from rpg.itens import CONSUMIVEIS, EM_ALIADO
from rpg.jogo import Jogo
from rpg.ui import BotUI
from rpg.web.estado import estado
from tests.test_abertura_feridas import ferir
from tests.test_abertura_parte2 import depois_da_despensa

NADA = "Nenhuma ferida aberta para enfaixar."


def jogo(classe="guerreiro"):
    g = Jogo(BotUI(random.Random(4)), seed=4, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Robô", classe)
    g.j.consumiveis["bandagem"] = 3
    return g


def bolsa(g):
    return next(b for b in estado(g)["heroi"]["bolsa"] if b["id"] == "bandagem")


def retrato(g):
    """O que uma tentativa de uso não pode mudar: o item, a vida, o tempo e o sorteio."""
    return (g.j.consumiveis["bandagem"], g.j.hp, g.dia, g.periodo, g.rng.getstate(),
            [dict(f) for f in g.j.ferimentos])


class TestBandagem(unittest.TestCase):
    def test_ferida_aberta_enfaixa_sem_curar_nem_sarar(self):
        g = jogo()
        ferir(g, "corte")
        g.j.hp = 10
        max_hp, dias = g.j.max_hp, g.j.ferimentos[0]["dias"]
        self.assertIsNone(bolsa(g)["motivo"])
        self.assertEqual(bolsa(g)["trata"], "Enfaixa: corte profundo.")
        self.assertTrue(g.usar_consumivel("bandagem"))
        f = g.j.ferimentos[0]
        self.assertEqual((f["tratado"], f["dias"]), (True, dias))  # protegida; o tempo de sarar é o mesmo
        self.assertEqual((g.j.hp, g.j.max_hp), (10, max_hp))  # nenhuma vida; a penalidade fica até sarar
        self.assertEqual(g.j.consumiveis["bandagem"], 2)

    def test_sem_ferida_ou_so_perna_torcida_fica_indisponivel(self):
        for fids in ((), ("perna",), ("braco", "costelas", "concussao"), ("infeccao",)):
            g = jogo()
            ferir(g, *fids)
            g.j.hp = 5  # vida baixa: ainda assim, nada
            b = bolsa(g)
            self.assertEqual(b["motivo"], NADA, fids)
            self.assertNotIn("trata", b)  # sem pulso
            antes = retrato(g)
            self.assertFalse(g.usar_consumivel("bandagem"))
            self.assertEqual(retrato(g), antes, fids)

    def test_ferida_ja_enfaixada(self):
        g = jogo()
        ferir(g, "queimadura")
        g.usar_consumivel("bandagem")
        self.assertEqual(bolsa(g)["motivo"], NADA)
        antes = retrato(g)
        g.executar_comum(("usar", "bandagem"))  # o clique da bolsa (opção escondida do menu)
        self.assertEqual(retrato(g), antes)

    def test_varias_feridas_uma_por_uso(self):
        g = jogo()
        ferir(g, "mordida", "perna", "corte")
        self.assertEqual(bolsa(g)["trata"], "Enfaixa: mordida dilacerada.")
        g.usar_consumivel("bandagem")
        self.assertEqual([f["tratado"] for f in g.j.ferimentos], [True, False, False])
        self.assertEqual(bolsa(g)["trata"], "Enfaixa: corte profundo.")
        g.usar_consumivel("bandagem")
        self.assertEqual([f["tratado"] for f in g.j.ferimentos], [True, False, True])
        self.assertEqual(g.j.consumiveis["bandagem"], 1)
        self.assertEqual(bolsa(g)["motivo"], NADA)

    def test_infeccao_fica_depois_de_enfaixar_outra(self):
        g = jogo()
        ferir(g, "infeccao", "corte")
        g.usar_consumivel("bandagem")
        ids = {f["id"]: f["tratado"] for f in g.j.ferimentos}
        self.assertEqual(ids, {"infeccao": False, "corte": True})  # a bandagem não cura infecção

    def test_nao_estanca_nem_serve_em_aliado(self):
        self.assertNotIn("bandagem", EM_ALIADO)
        self.assertNotIn("vida", CONSUMIVEIS["bandagem"]["desc"].replace("Não recupera vida", ""))
        g = jogo()
        g.j.aplicar("sangramento", 2, 2)
        g.j.hp = 10
        self.assertEqual(g.motivo_inutil("bandagem"), NADA)
        self.assertFalse(g.usar_consumivel("bandagem"))
        self.assertTrue(g.j.efeito("sangramento"))
        from rpg import comitiva
        m = comitiva.recrutar(g, "odete")
        m["hp"], m["ferido"] = 1, True
        self.assertEqual(bolsa(g)["alvos"], [])
        self.assertFalse(g.usar_em_companheiro("bandagem", "odete"))
        self.assertEqual((m["hp"], m["ferido"], g.j.consumiveis["bandagem"]), (1, True, 3))

    def test_na_luta_indisponivel_nao_gasta_o_turno(self):
        g = jogo()
        cb = Combate(g, [g.inimigo("lobo", nivel=1)], None)
        g.combate_ativo = cb
        self.assertEqual(cb.motivo_item("bandagem"), NADA)
        usaveis, _ = cb.itens_da_luta()
        self.assertIn("bandagem", usaveis)  # à vista, apagada
        g.ui.escolher = lambda pergunta, opcoes: usaveis.index("bandagem")
        antes = retrato(g)
        self.assertIsNone(cb.menu_itens())  # sem turno gasto
        self.assertEqual(retrato(g), antes)
        ferir(g, "corte")  # com ferida aberta, enfaixa (e gasta o turno, como qualquer item)
        self.assertEqual(cb.menu_itens(), "turno")
        self.assertTrue(g.j.ferimentos[0]["tratado"])

    def test_salvar_e_carregar_guardam_a_ferida_enfaixada(self):
        g = jogo()
        ferir(g, "corte", "mordida")
        g.usar_consumivel("bandagem")
        g.salvar(silencioso=True)
        h = Jogo.carregar(BotUI(random.Random(1)), g.caminho_save(), pasta_saves=g.pasta_saves)
        self.assertEqual([f["tratado"] for f in h.j.ferimentos], [True, False])
        self.assertEqual(h.j.consumiveis["bandagem"], 2)
        self.assertEqual(h.o_que_trata("bandagem"), {"trata": "Enfaixa: mordida dilacerada."})

    def test_tutorial_ligado_ou_nao_a_regra_e_a_mesma(self):
        for tutorial in (True, False):
            g = depois_da_despensa(tutorial=tutorial)
            g.j.consumiveis["bandagem"] = 1
            self.assertEqual(g.motivo_inutil("bandagem"), NADA)
            ferir(g, "corte")
            self.assertIsNone(g.motivo_inutil("bandagem"))
            g.executar_comum(("usar", "bandagem"))
            self.assertTrue(g.j.ferimentos[0]["tratado"])
            self.assertIn("F2", g.mundo["abertura"]["vistas"])

    def test_f2_so_marca_visto_quando_enfaixa(self):
        g = depois_da_despensa()
        g.j.consumiveis["bandagem"] = 1
        g.executar_comum(("usar", "bandagem"))  # nada para enfaixar: a orientação continua valendo
        self.assertNotIn("F2", g.mundo["abertura"]["vistas"])

    def test_textos_nao_prometem_vida(self):
        g = jogo()
        ferir(g, "corte")
        textos = [CONSUMIVEIS["bandagem"]["desc"], *sobrevivencia.explicar(g.j.ferimentos[0], "Vigor", g.j)]
        for t in textos:
            self.assertNotIn("cura", t.lower().replace("curandeir", ""))
            self.assertNotIn("estanca", t.lower())


class TestFlechasNoEspolio(unittest.TestCase):
    def vitoria(self, chance, gastas=3, tela=True):
        g = Jogo(BotUI(random.Random(2)), seed=2, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Robô", "arqueiro")
        g.j.flechas = 10
        g.ui.conquistas_na_tela = tela
        festas, ditos = [], []
        g.ui.celebrar = lambda tipo, dados: festas.append((tipo, dados))
        g.dizer = g.ui.dizer = lambda texto, *a, **k: ditos.append(texto)  # o motor e as linhas da luta
        cb = Combate(g, [g.inimigo("lobo", nivel=1)], None, saque=False)
        g.combate_ativo = cb
        cb.flechas_gastas = gastas
        for e in cb.inimigos:
            e.hp = 0
        with mock.patch.object(bal, "RECOLHER_FLECHA", chance):
            cb.fim("vitoria")
        g.fechar_espolio()
        espolio = next((d for t, d in festas if t == "espolio"), {})
        flechas = [x["qtd"] for x in espolio.get("itens", []) if x["id"] == "flechas"]
        return g, flechas, ditos

    def test_zero_uma_varias(self):
        g, flechas, ditos = self.vitoria(0.0)
        self.assertEqual((g.j.flechas, flechas), (10, []))  # nada recolhido: nada no quadro
        g, flechas, ditos = self.vitoria(1.0, gastas=1)
        self.assertEqual((g.j.flechas, flechas), (11, [1]))
        g, flechas, ditos = self.vitoria(1.0, gastas=3)
        self.assertEqual((g.j.flechas, flechas), (13, [3]))
        self.assertFalse([d for d in ditos if "recolhe" in d])  # na tela, não vira linha da página

    def test_no_texto_a_linha_de_sempre(self):
        g, flechas, ditos = self.vitoria(1.0, gastas=2, tela=False)
        self.assertEqual(g.j.flechas, 12)
        self.assertIn("Você recolhe 2 flechas intactas do campo.", ditos)

    def test_o_quadro_nao_devolve_de_novo(self):
        g, flechas, _ = self.vitoria(1.0, gastas=2)
        self.assertEqual(g.j.flechas, 12)
        g.fechar_espolio()  # fechar (ou redesenhar a tela) de novo: as flechas já estão na aljava, uma vez só
        self.assertEqual(g.j.flechas, 12)


if __name__ == "__main__":
    unittest.main()
