"""Retorno visual pedido no teste de Jean (E9): a teia da aranha que voa e, quando não prende, diz isso na carta do
alvo; e a bolsa que diz o que cada item trata agora (a bandagem com ferida aberta) ou que a bandagem só cura um pouco
(as feridas já enfaixadas)."""

import random
import tempfile
import unittest

from rpg import inimigos
from rpg.jogo import Jogo
from rpg.ui import BotUI
from rpg.web.estado import estado


def jogo():
    g = Jogo(BotUI(random.Random(1)), seed=4, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", "guerreiro")
    return g


class Combate:
    """O mínimo que a teia usa do combate: dizer, aplicar (sorteio decidido pelo teste), lance e nome."""

    def __init__(self, prende):
        self.prende, self.lances, self.ditos = prende, [], []

    def dizer(self, texto, cor=None):
        self.ditos.append(texto)

    def nome(self, c):
        return "Você"

    def uid(self, c):
        return id(c)

    def lance(self, tipo, **dados):
        self.lances.append(tipo)

    def aplicar(self, alvo, efeito, turnos, chance=1.0, rotulo=None, **k):
        return self.prende


class TestTeia(unittest.TestCase):
    def test_teia_voa_e_diz_quando_nao_prende(self):
        g = jogo()
        aranha = g.inimigo("aranha", nivel=2)
        for prende, esperado in ((True, ["arremesso"]), (False, ["arremesso", "escapou"])):
            cb = Combate(prende)
            inimigos._teia(cb, aranha, g.j)
            self.assertEqual(cb.lances, esperado)

    def test_firme_nao_repete_o_aviso(self):
        """Quem acabou de se soltar (firme) já tem o aviso dele na tela: a teia não acrescenta outro."""
        from rpg.estados import ESTADOS
        g = jogo()
        guarda = next(k for k, v in ESTADOS.items() if "atordoado" in v.get("protege", ()))
        g.j.aplicar(guarda, 1, 0)
        cb = Combate(False)
        inimigos._teia(cb, g.inimigo("aranha", nivel=2), g.j)
        self.assertEqual(cb.lances, ["arremesso"])


class TestBolsa(unittest.TestCase):
    def bolsa(self, g, k):
        return next(b for b in estado(g)["heroi"]["bolsa"] if b["id"] == k)

    def test_bandagem_com_ferida_aberta_diz_o_que_trata(self):
        g = jogo()
        g.j.consumiveis["bandagem"] = 2
        g.j.ferimentos.append({"id": "queimadura", "dias": 5, "tratado": False})
        self.assertEqual(self.bolsa(g, "bandagem")["trata"], "Trata: queimadura grave.")
        g.j.aplicar("sangramento", 2, 2)
        self.assertEqual(self.bolsa(g, "bandagem")["trata"], "Trata: sangramento e queimadura grave.")

    def test_bandagem_sem_nada_para_tratar_avisa_que_so_cura(self):
        g = jogo()
        g.j.consumiveis["bandagem"] = 1
        g.j.ferimentos.append({"id": "queimadura", "dias": 5, "tratado": True})
        g.j.hp = 10
        b = self.bolsa(g, "bandagem")
        self.assertNotIn("trata", b)
        self.assertIn("só cura", b["so_cura"])

    def test_antidoto_e_unguento(self):
        g = jogo()
        g.j.consumiveis.update(antidoto=1, unguento=1)
        self.assertNotIn("trata", self.bolsa(g, "antidoto"))
        g.j.aplicar("veneno", 2, 2)
        g.j.ferimentos.append({"id": "infeccao", "dias": None, "tratado": False})
        self.assertEqual(self.bolsa(g, "antidoto")["trata"], "Trata: veneno.")
        self.assertEqual(self.bolsa(g, "unguento")["trata"], "Trata: infecção.")


if __name__ == "__main__":
    unittest.main()
