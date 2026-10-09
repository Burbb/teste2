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

    def test_xama_so_reza_pelos_caidos_quando_ha_quem_levantar(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        xama, caido = g.inimigo("xama_caido", nivel=3), g.inimigo("caido", nivel=3)
        cb = Combate(g, [xama, caido])
        g.combate_ativo = cb
        self.assertFalse(HABS["reviver"]["quando"](cb, xama, g.j))  # sem a faixa "Reviver" à toa
        caido.hp = 0
        self.assertTrue(HABS["reviver"]["quando"](cb, xama, g.j))
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


class TestIniciativa(unittest.TestCase):
    """A surpresa é o primeiro turno: atacar nele leva o bônus; usar para outra coisa o perde."""

    def _luta(self, buff_primeiro):
        golpes = []

        class Roteiro(BotUI):
            def escolher(self, pergunta, opcoes):
                metas = self.meta_opcoes or []
                if pergunta == "Sua ação:":
                    return 1 if buff_primeiro and cb.turno == 1 else 0
                if pergunta == "Habilidades:":
                    return next(i for i, m in enumerate(metas) if m and m.get("habilidade") == "erguer_escudo")
                return super().escolher(pergunta, opcoes)

            def lance(self, tipo, **d):
                if tipo == "golpe" and d.get("de") == "j":
                    golpes.append(d)

        g = Jogo(Roteiro(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        e = g.inimigo("lobo", nivel=1)
        e.hp = e.max_hp = 500
        cb = Combate(g, [e], emboscada="jogador", pode_fugir=False)
        g.combate_ativo = cb
        try:
            original = cb.fase_inimigos
            cb.fase_inimigos = lambda *a, **k: (original(*a, **k), setattr(e, "hp", 0) if cb.turno >= 2 else None)
            cb.executar()
        finally:
            g.combate_ativo = None
        return golpes

    def test_atacando_no_turno_livre_o_golpe_sai_reforcado(self):
        golpes = self._luta(buff_primeiro=False)
        self.assertEqual(golpes[0].get("bonus_motivo"), "Iniciativa!")

    def test_buff_no_turno_livre_perde_o_bonus(self):
        golpes = self._luta(buff_primeiro=True)
        self.assertTrue(golpes)
        self.assertFalse(any(x.get("bonus_motivo") for x in golpes))
