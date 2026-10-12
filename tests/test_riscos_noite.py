"""A noite e a falta de tocha ditas antes da luta (E9): a nota das salas da capela (a tocha que se gasta, ou o inimigo
que ataca primeiro sem ela, e o que a noite muda), as linhas do lugar ao lado do nível-base, a dica do modificador da
noite sem prometer bando maior onde o tamanho é fixo, e o texto de quem entra sem luz. Nada disso muda a luta."""

import tempfile
import unittest

from rpg import balanceamento as bal, missoes, sobrevivencia
from rpg.jogo import Jogo
from rpg.web.estado import estado, modificadores
from tests.test_missoes import Roteiro, ir


def na_capela(etapa="capela", periodo=1, tochas=3):
    g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", "guerreiro", "turvo")
    missoes.registro(g, "febre_do_turvo").update(etapa=etapa, cenas=["abertura", "capela_exterior"])
    ir(g, "capela_afogada")
    g.periodo, g.j.consumiveis["tocha"] = periodo, tochas
    return g


def nota(g):
    return next(o[2].get("nota") for o in missoes.opcoes(g) if o[1][2] in ("nave", "sacristia", "ossuario"))


class TestSalas(unittest.TestCase):
    def test_nota_da_sala_de_dia_e_de_noite(self):
        self.assertEqual(nota(na_capela()), "Gasta 1 tocha (você tem 3).")  # a capela é escura de dia também
        self.assertEqual(nota(na_capela(periodo=3)), "Gasta 1 tocha (você tem 3). Noite: inimigos +1 nível e +10% de "
                                                     "dano.")
        self.assertEqual(nota(na_capela(tochas=0)), "Sem tocha: o inimigo mais rápido ataca primeiro.")
        for etapa in ("sacristia", "ossuario"):
            self.assertIn("tocha", nota(na_capela(etapa)))

    def test_guardia_so_o_dano(self):
        g = na_capela(periodo=3)
        self.assertEqual(sobrevivencia.nota_sala(g, guardiao=True),
                         "Gasta 1 tocha (você tem 3). Noite: +10% de dano dos inimigos.")

    def test_sem_tocha_na_sala_o_texto_diz_a_emboscada_certa(self):
        g = na_capela(tochas=0)
        self.assertFalse(sobrevivencia.acender_tocha(g, sala=True))
        self.assertIn("o inimigo mais rápido ataca antes de você", g.ui.ditos[-1])
        g.sem_luz = False
        sobrevivencia.acender_tocha(g)
        self.assertIn("emboscadas mais prováveis", g.ui.ditos[-1])  # fora das salas, só mais provável


class TestLugar(unittest.TestCase):
    def test_nivel_base_e_o_que_a_noite_soma(self):
        g = na_capela(periodo=3)
        local = estado(g)["local"]
        self.assertEqual(local["nivel"], g.nivel_local())  # o nível-base não muda
        textos = [r["texto"] for r in local["riscos"]]
        self.assertEqual(textos[0], "Noite: inimigos +1 nível e +10% de dano")
        self.assertIn("cada sala", textos[1])
        g.periodo = 1
        self.assertEqual([r["texto"] for r in estado(g)["local"]["riscos"]],
                         ["Escuro: explorar, caçar, viajar e cada sala gastam 1 tocha por vez (você tem 3)"])

    def test_vila_e_dia_claro_sem_linhas(self):
        g = na_capela()
        ir(g, "bosque_do_moinho")
        self.assertEqual(estado(g)["local"]["riscos"], [])
        ir(g, "vau_do_turvo")
        g.periodo = 3
        self.assertEqual(estado(g)["local"]["riscos"], [])

    def test_cabecalho_do_texto(self):
        g = na_capela(periodo=3)
        subs = []
        g.ui.cena = lambda titulo, sub=None, tipo="evento": subs.append(sub)
        g.cabecalho()
        self.assertIn("inimigos Nv.3 (+1 à noite)", subs[-1])
        self.assertIn("Noite: inimigos +1 nível e +10% de dano", " ".join(g.ui.ditos))

    def test_dica_da_noite_nao_promete_bando_onde_e_fixo(self):
        g = na_capela(periodo=3)
        noite = next(m for m in modificadores(g) if m["icone"] == "lua")
        self.assertNotIn("mais vezes em bando", noite["detalhe"])
        self.assertIn("nas salas, o número é o mesmo", noite["detalhe"])
        self.assertIn(f"{round((bal.NOITE_INIMIGOS - 1) * 100)}% mais dano", noite["detalhe"])


if __name__ == "__main__":
    unittest.main()
