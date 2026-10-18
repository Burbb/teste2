"""A rolagem dos testes de atributo: o "precisa de N ou mais" que a tela mostra vem do motor e segue a regra do teste."""

import random
import tempfile
import unittest

from rpg.jogo import Jogo
from rpg.sistemas.testes import Testes
from rpg.ui import BotUI


class Anota(BotUI):
    def __init__(self, rng):
        super().__init__(rng)
        self.rolagens = []

    def rolagem(self, atributo, cd, d20, mod, total, sucesso, precisa=None):
        self.rolagens.append((d20, sucesso, precisa))
        super().rolagem(atributo, cd, d20, mod, total, sucesso, precisa=precisa)


class TestRolagem(unittest.TestCase):
    def test_precisa_e_o_menor_d20_que_passa(self):
        # a regra de teste (sistemas/testes.py): o 20 sempre passa, o 1 sempre falha, o resto soma o bônus
        for cd in range(-5, 45):
            for mod in range(-12, 30):
                menor = min(d for d in range(1, 21) if d == 20 or (d != 1 and d + mod >= cd))
                self.assertEqual(Testes.precisa_no_dado(cd, mod), menor, (cd, mod))

    def test_o_teste_manda_o_precisa_coerente_com_o_resultado(self):
        ui = Anota(random.Random(1))
        g = Jogo(ui, seed=3, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        for cd in (2, 10, 12, 18, 30):
            for _ in range(40):
                g.teste("percepcao", cd)
        self.assertEqual(len(ui.rolagens), 200)
        for d20, sucesso, precisa in ui.rolagens:
            self.assertEqual(sucesso, d20 >= precisa, (d20, sucesso, precisa))


if __name__ == "__main__":
    unittest.main()
