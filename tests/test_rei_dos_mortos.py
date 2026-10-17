"""O Rei dos Mortos (talento senhor_mortos do necromante): "O primeiro inimigo a cair em cada combate se ergue como seu
servo." Uma vez por combate: o xamã reviver o primeiro caído (a lista de mortos encolhe) não abre uma segunda vez; e
o combate seguinte começa de novo."""

import tempfile
import unittest

from rpg import dev, inimigos, talentos
from rpg.combate import Combate
from rpg.jogo import Jogo
from tests.test_missoes import Roteiro


def necromante():
    g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "mago", "turvo")
    dev.subir_ate(g, 12, spec="necromante")
    if not g.j.tal("senhor_mortos"):
        talentos.aprender(g.j, next(t for t in talentos.TALENTOS["mago"] if t["id"] == "senhor_mortos"))
    return g


def servos_do_talento(cb):
    return [a for a in cb.aliados if a.nome.endswith("(servo)")]


def cair(cb, e):
    e.hp = 0
    cb.ao_morrer(e, por=cb.j)


class TestReiDosMortos(unittest.TestCase):
    def test_reviver_do_xama_nao_abre_segunda_vez(self):
        g = necromante()
        a, b = g.inimigo("caido", nivel=5), g.inimigo("caido", nivel=5)
        xama = g.inimigo("xama_caido", nivel=5)
        cb = Combate(g, [a, b, xama])
        cair(cb, a)  # o primeiro a cair: vira servo
        self.assertEqual([s.nome for s in servos_do_talento(cb)], [f"{a.nome} (servo)"])
        self.assertEqual(cb.mortos, [a])
        inimigos._reviver(cb, xama, None)  # o xamã levanta o caído: a lista de mortos fica vazia de novo
        self.assertTrue(a.vivo)
        self.assertEqual(cb.mortos, [])
        cair(cb, b)  # outra morte, que antes contava como "a primeira" (len(mortos) == 1)
        cair(cb, a)  # e o revivido de novo
        self.assertEqual(len(servos_do_talento(cb)), 1)

    def test_combate_novo_ativa_de_novo(self):
        g = necromante()
        cb = Combate(g, [g.inimigo("caido", nivel=5), g.inimigo("caido", nivel=5)])
        cair(cb, cb.inimigos[0])
        self.assertEqual(len(servos_do_talento(cb)), 1)
        novo = Combate(g, [g.inimigo("caido", nivel=5), g.inimigo("caido", nivel=5)])
        cair(novo, novo.inimigos[1])
        self.assertEqual([s.nome for s in servos_do_talento(novo)], [f"{novo.inimigos[1].nome} (servo)"])

    def test_chefe_primeiro_consome_a_vez(self):
        """Como antes: se o primeiro a cair é um chefe, ele não se ergue, e ninguém depois dele."""
        g = necromante()
        chefe, outro = g.inimigo("caido", nivel=5), g.inimigo("caido", nivel=5)
        chefe.chefe = True
        cb = Combate(g, [chefe, outro])
        cair(cb, chefe)
        cair(cb, outro)
        self.assertEqual(servos_do_talento(cb), [])


if __name__ == "__main__":
    unittest.main()
