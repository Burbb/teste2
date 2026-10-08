"""O juízo dos inimigos: habilidade só quando faz sentido, e o golpe que derruba antes de qualquer firula."""

import random
import tempfile
import unittest

from rpg.combate import Combate
from rpg.inimigos import HABS
from rpg.jogo import Jogo
from rpg.ui import BotUI


def _luta(familia="lobo", nivel=3):
    g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "guerreiro")
    e = g.inimigo(familia, nivel=nivel)
    cb = Combate(g, [e])
    g.combate_ativo = cb
    return g, cb, e


class TestJuizo(unittest.TestCase):
    def test_todo_inimigo_tem_habilidades_do_catalogo(self):
        from rpg.dados import FAMILIAS, GUARDIOES
        habs = {h for f in FAMILIAS.values() for h in f.get("habs", [])}
        habs |= {h for lista in GUARDIOES.values() for t in lista for h in t.get("habs", [])}
        self.assertTrue(habs <= set(HABS), habs - set(HABS))

    def test_bando_ja_furioso_nao_uiva_de_novo(self):
        g, cb, e = _luta()
        self.assertTrue(HABS["uivo"]["quando"](cb, e, g.j))
        e.aplicar("fortalecido", 2, 0.3)
        self.assertFalse(HABS["uivo"]["quando"](cb, e, g.j))
        g.combate_ativo = None

    def test_nao_trava_quem_esta_firme(self):
        g, cb, e = _luta("aranha")
        self.assertTrue(HABS["teia"]["quando"](cb, e, g.j))
        g.j.aplicar("firme", 1)
        self.assertFalse(HABS["teia"]["quando"](cb, e, g.j))
        g.combate_ativo = None

    def test_com_o_heroi_a_um_golpe_so_ataca(self):
        """Com você quase morto, o lobo nunca gasta a vez uivando: sempre fere."""
        for semente in range(40):
            g, cb, e = _luta()
            g.rng.seed(semente)
            e.habilidades = ["uivo"]
            g.j.hp = 1
            cb.agir_inimigo(e)
            self.assertFalse(e.efeito("fortalecido"), f"semente {semente}: uivou em vez de atacar")
            g.combate_ativo = None

    def test_previsao_de_dano_acompanha_os_estados(self):
        g, cb, e = _luta()
        base = cb.dano_previsto(e, g.j)
        e.aplicar("fortalecido", 2, 0.3)
        self.assertAlmostEqual(cb.dano_previsto(e, g.j), base * 1.3)
        g.j.aplicar("barreira", 2, 1000)
        self.assertLess(cb.dano_previsto(e, g.j), 0)
        g.combate_ativo = None


if __name__ == "__main__":
    unittest.main()
