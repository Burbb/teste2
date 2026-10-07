"""Modificadores e gatilhos: cada talento faz alguma coisa, com chaves que o jogo de fato pergunta."""

import random
import tempfile
import unittest

from rpg import modificadores as M
from rpg.habilidades import HABILIDADES
from rpg.jogo import Jogo
from rpg.talentos import PASSIVAS, POR_ID, TALENTOS, custo_habilidade
from rpg.ui import BotUI


def _fontes():
    yield from ((t["id"], t) for lista in TALENTOS.values() for t in lista)
    yield from ((f"passiva:{k}", p) for k, p in PASSIVAS.items())


class TestModificadores(unittest.TestCase):
    def test_todo_talento_faz_algo(self):
        for tid, t in _fontes():
            self.assertTrue(t.get("stats") or t.get("mods") or t.get("mults") or t.get("gatilhos"), tid)

    def test_chaves_e_eventos_conhecidos(self):
        """Uma chave com erro de digitação não faria nada em silêncio: aqui ela falha."""
        for tid, t in _fontes():
            for chave in t.get("mods", {}):
                if chave.startswith(M.PREFIXOS):
                    self.assertIn(chave.split(":", 1)[1], HABILIDADES, f"{tid}: {chave}")
                else:
                    self.assertIn(chave, M.CHAVES, f"{tid}: {chave}")
            for chave in t.get("mults", {}):
                self.assertIn(chave, M.MULTS, f"{tid}: {chave}")
            for ev in t.get("gatilhos", {}):
                self.assertIn(ev, M.EVENTOS, f"{tid}: {ev}")

    def test_soma_por_ponto_e_fixo(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        j = g.j
        self.assertEqual(M.mod(j, "dano_corpo"), 0)
        j.talentos["golpe_brutal"] = 3
        self.assertAlmostEqual(M.mod(j, "dano_corpo"), 0.18)
        self.assertEqual(M.nomes(j, "dano_corpo"), ["Golpe Brutal"])
        base = custo_habilidade(j, "erguer_escudo")
        j.talentos["muralha"] = 1  # Fixo(-4): vale uma vez
        self.assertEqual(custo_habilidade(j, "erguer_escudo"), base - 4)
        self.assertEqual(M.mod(j, "escudo_turnos"), 1)

    def test_passiva_da_especializacao(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        self.assertEqual(M.mod(g.j, "dano_ferido"), 0)
        g.j.spec = "berserker"
        self.assertEqual(M.mod(g.j, "dano_ferido"), 0.6)
        self.assertIn("Pacto de Sangue", M.nomes(g.j, "dano_ferido"))

    def test_gatilho_imortal_salva_do_golpe_fatal(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.j.spec, g.j.talentos["imortal"] = "berserker", 1
        e = g.inimigo("lobo", nivel=1)
        from rpg.combate import Combate
        cb = Combate(g, [e])
        g.j.hp = 5
        d = M.disparar(cb, g.j, "golpe_fatal", dano=50, de=e)
        self.assertEqual(d["dano"], 4)
        self.assertTrue(cb.usou_imortal)
        self.assertEqual(M.disparar(cb, g.j, "golpe_fatal", dano=50, de=e)["dano"], 50)  # só uma vez por luta
        g.combate_ativo = None

    def test_ids_unicos(self):
        self.assertEqual(len(POR_ID), sum(len(l) for l in TALENTOS.values()))


if __name__ == "__main__":
    unittest.main()
