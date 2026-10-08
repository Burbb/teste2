"""Recompensas: o contrato paga o que o cartaz promete, e a tela gráfica festeja em vez de encher o registro."""

import random
import tempfile
import unittest

from rpg.jogo import Jogo
from rpg.ui import BotUI, InterfaceGrafica


class Anotador(BotUI):
    def __init__(self, rng):
        super().__init__(rng)
        self.textos, self.festas = [], []

    def dizer(self, texto="", cor=None):
        self.textos.append(str(texto))

    def efeito(self, texto, tipo="info"):
        self.textos.append(str(texto))

    def celebrar(self, tipo, dados):
        self.festas.append((tipo, dados))


class AnotadorGrafico(InterfaceGrafica, Anotador):
    pass


def _jogo(ui):
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "guerreiro")
    for _ in range(2):
        c = g.gerar_contrato()
        c["concluido"] = True
        g.contratos.append(c)
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    return g


class TestContratos(unittest.TestCase):
    def test_paga_o_que_o_cartaz_promete(self):
        g = _jogo(Anotador(random.Random(1)))
        prometido = sum(c["ouro"] for c in g.contratos)
        antes = g.j.ouro
        g.receber_contratos()
        self.assertEqual(g.j.ouro - antes, prometido)
        self.assertEqual(g.contratos, [])

    def test_texto_conta_cada_contrato(self):
        g = _jogo(Anotador(random.Random(1)))
        g.receber_contratos()
        self.assertEqual(sum(t.startswith("Recompensa de contrato") for t in g.ui.textos), 2)

    def test_tela_grafica_festeja_uma_vez_sem_texto(self):
        ui = AnotadorGrafico(random.Random(1))
        g = _jogo(ui)
        ouro, xp = sum(c["ouro"] for c in g.contratos), sum(c["xp"] for c in g.contratos)
        ui.textos.clear()
        g.receber_contratos()
        festas = [d for t, d in ui.festas if t == "contratos"]
        self.assertEqual(len(festas), 1)
        self.assertEqual((festas[0]["ouro"], festas[0]["xp"], len(festas[0]["contratos"])), (ouro, xp, 2))
        self.assertFalse([t for t in ui.textos if "contrato" in t.lower() or "ouro" in t or "XP" in t], ui.textos)


class TestNivel(unittest.TestCase):
    def test_tela_grafica_nao_repete_a_festa_no_texto(self):
        ui = AnotadorGrafico(random.Random(1))
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        ui.textos.clear()
        g.subir_nivel()
        self.assertTrue(any(t == "nivel" for t, _ in ui.festas))
        self.assertFalse([t for t in ui.textos if "ponto de talento" in t or "Nova habilidade" in t], ui.textos)

    def test_texto_continua_contando(self):
        ui = Anotador(random.Random(1))
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.subir_nivel()
        self.assertTrue(any("ponto de talento" in t for t in ui.textos))


if __name__ == "__main__":
    unittest.main()
