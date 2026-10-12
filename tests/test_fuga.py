"""A fuga do herói: a tela recebe um lance só dela (concluída ou cercada), para mostrar e soar a retirada sem
depender da linha do histórico. O sorteio e a chance de escapar não mudam."""

import tempfile
import unittest

from rpg.combate import Combate
from rpg.jogo import Jogo
from tests.test_missoes import Roteiro


class Lances(Roteiro):
    def __init__(self):
        super().__init__([])
        self.lances = []

    def lance(self, tipo, **dados):
        self.lances.append((tipo, dados))


class TestFuga(unittest.TestCase):
    def tentar(self, sorte):
        g = Jogo(Lances(), seed=3, pasta_saves=tempfile.mkdtemp(), hardcore=False)
        g.iniciar("Teste", "guerreiro", "turvo")
        cb = Combate(g, [g.inimigo("lobo", nivel=1)], None, titulo="Teste")
        cb.rng.random = lambda: sorte  # 0: escapa sempre; 0.99: a chance não passa de 85%
        return cb.tentar_fuga(), [d for t, d in g.ui.lances if t == "fuga_heroi"], g.ui.ditos

    def test_concluida_e_cercada_sao_lances_diferentes(self):
        ok, lances, ditos = self.tentar(0.0)
        self.assertTrue(ok)
        self.assertEqual(lances, [{"de": "j", "ok": True}])
        self.assertIn("Você recua e consegue escapar!", ditos)  # o histórico continua com a linha
        ok, lances, _ = self.tentar(0.99)
        self.assertFalse(ok)
        self.assertEqual(lances, [{"de": "j", "ok": False}])


if __name__ == "__main__":
    unittest.main()
