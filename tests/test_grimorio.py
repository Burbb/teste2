"""O Grimório monta a página de toda habilidade, de toda especialização, sem erro e com números coerentes."""

import random
import tempfile
import unittest

from rpg import grimorio
from rpg.classes import SPECS, habilidades_ate
from rpg.habilidades import HABILIDADES
from rpg.jogo import Jogo
from rpg.ui import BotUI


class TestGrimorio(unittest.TestCase):
    def test_todas_as_habilidades_tem_pagina(self):
        vistas = set()
        for spec, d in SPECS.items():
            g = Jogo(BotUI(random.Random(1)), seed=3, pasta_saves=tempfile.mkdtemp())
            g.iniciar("Teste", d["classe"])
            g.j.nivel, g.j.spec = 8, spec
            g.j.habilidades = habilidades_ate(d["classe"], spec, 8)
            g.j.recalcular()
            livro = grimorio.dados(g.j)
            for pagina in [livro["basico"]] + livro["habilidades"]:
                self.assertTrue(pagina["linhas"], pagina["id"])
                for linha in pagina["linhas"]:
                    if linha["tipo"] == "dano":
                        self.assertLessEqual(linha["min"], linha["max"])
                        self.assertGreater(linha["critico"], linha["medio"])
                vistas.add(pagina["id"])
        self.assertEqual(set(HABILIDADES) - vistas, set())


if __name__ == "__main__":
    unittest.main()
