"""A vida máxima bloqueada (1.115.0, sobrevivencia.vida_bloqueio): o saudável, o limite e as fontes vêm das contas do
motor (totais, fatores multiplicados e arredondados em recalcular); a soma das perdas fecha com o bloqueado; só lê; e
os textos que falam do limite (o motivo da poção, o efeito do Templo) não dizem "cheia" a 104/146."""

import json
import tempfile
import unittest

from rpg import dev, sobrevivencia
from rpg.jogo import Jogo
from tests.test_missoes import Roteiro


def heroi(ferimentos=(), fome=0):
    g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "guerreiro", "turvo")
    dev.subir_ate(g, 8, spec="paladino")
    j = g.j
    for f in ferimentos:
        j.ferimentos.append({"id": f, "dias": 4, "tratado": False})
    j.fome = fome
    j.recalcular()
    return g


class TestVidaBloqueio(unittest.TestCase):
    def test_sem_penalidade(self):
        g = heroi()
        self.assertIsNone(sobrevivencia.vida_bloqueio(g.j))
        g = heroi(["perna"])  # ferimento que não mexe na vida máxima
        self.assertIsNone(sobrevivencia.vida_bloqueio(g.j))

    def test_fontes_combinadas_fecham_a_conta(self):
        g = heroi(["corte", "queimadura"], fome=1)
        j = g.j
        b = sobrevivencia.vida_bloqueio(j)
        totais, _ = j.totais()
        self.assertEqual(b["saudavel"], round(totais["max_hp"]))
        self.assertEqual(b["limite"], j.max_hp)
        self.assertEqual(b["bloqueado"], b["saudavel"] - j.max_hp)
        self.assertEqual(sum(f["perda"] for f in b["fontes"]), b["bloqueado"])
        self.assertEqual([f["nome"] for f in b["fontes"]], ["Corte profundo", "Queimadura grave", "Fome"])
        self.assertEqual([f["pct"] for f in b["fontes"]], [10, 12, 10])
        self.assertIn("Curandeira", b["dica"][1])
        self.assertIn("fome", b["dica"][1])

    def test_so_le(self):
        g = heroi(["corte"], fome=2)
        antes = json.dumps(g.j.para_dict(), sort_keys=True, default=str)
        sobrevivencia.vida_bloqueio(g.j)
        self.assertEqual(json.dumps(g.j.para_dict(), sort_keys=True, default=str), antes)

    def test_textos_do_limite(self):
        g = heroi(["corte"], fome=1)
        j = g.j
        j.hp = j.max_hp
        b = sobrevivencia.vida_bloqueio(j)
        motivo = g.motivo_inutil("pocao_vida")
        self.assertNotIn("cheia", motivo)
        self.assertIn(f"({j.max_hp} de {b['saudavel']})", motivo)
        self.assertTrue(motivo.endswith("bloqueiam o resto."))
        j.hp = j.max_hp - 10
        efeito = next(o[2]["efeito"] for o in g.opcoes_templo() if "alvo" not in o[2])
        self.assertEqual(efeito, f"+10 de vida ({j.max_hp}/{b['saudavel']}: o limite de agora)")
        sem = heroi()
        sem.j.hp = sem.j.max_hp
        self.assertEqual(sem.motivo_inutil("pocao_vida"), "Sua vida já está cheia.")


if __name__ == "__main__":
    unittest.main()
