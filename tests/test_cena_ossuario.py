"""A cena interativa do ossuário (1.72.0, roadmapIDEIAS/20): o motor diz à tela gráfica como está o sarilho (correntes
presas ou soltas, pelo preparo gravado) e o que o ponto clicável faz agora (a mesma ação do menu). A animação da
corrente descendo só é pedida depois de o preparo ser gravado, e só quando houve sucesso de verdade."""

import unittest

from rpg import missoes
from rpg.regras import Derrota
from tests.test_missoes import MID, Roteiro, fazer, lutas, na_capela


class Tela(Roteiro):
    """O roteiro de sempre, como a tela gráfica: guarda as celebrações e o preparo no momento de cada uma."""
    conquistas_na_tela = True

    def __init__(self, roteiro=()):
        super().__init__(roteiro)
        self.celebradas = []

    def celebrar(self, tipo, dados):
        self.celebradas.append((tipo, list(missoes.registro(self.jogo_, MID)["preparos"])))


def no_ossuario(classe="guerreiro"):
    ui = Tela()
    g = na_capela(classe, ui=ui, etapa="fundo")
    ui.jogo_ = g
    missoes.registro(g, MID)["pistas"].append("correntes")  # o ossuário já foi visto
    return g


def cenas(g):
    return [d for t, d in g.ui.paineis if t == "cena"]


class TestCenaOssuario(unittest.TestCase):
    def test_presas_com_o_ponto_que_faz_a_acao_do_menu(self):
        g = no_ossuario()
        d = missoes.cena_ossuario(g)
        self.assertEqual((d["cena"], d["correntes"], d["foco"]), ("ossuario", "presas", None))
        ponto = d["pontos"][0]
        self.assertEqual(ponto["acao"], {"missao": MID, "acao_missao": "correntes"})
        # a mesma ação do menu: a opção traz o mesmo endereço na meta
        metas = [o[1] for o in missoes.opcoes(g)]
        self.assertTrue(any(m[1] == MID and m[2] == "correntes" for m in metas))
        self.assertIn("presas", ponto["estado"])

    def test_de_perto_o_ponto_nao_age_e_soltas_dizem_o_estado(self):
        g = no_ossuario()
        self.assertIsNone(missoes.cena_ossuario(g, foco="sarilho")["pontos"][0]["acao"])
        missoes.registro(g, MID)["preparos"].append("corpo_solto")
        d = missoes.cena_ossuario(g)
        self.assertEqual((d["correntes"], d["pontos"][0]["acao"]), ("soltas", None))
        self.assertIn("soltas", d["pontos"][0]["estado"])

    def test_so_na_capela_e_depois_do_ossuario(self):
        g = no_ossuario()
        missoes.mostrar_cena(g)
        self.assertEqual(len(cenas(g)), 1)
        missoes.registro(g, MID)["pistas"].remove("correntes")
        missoes.mostrar_cena(g)
        self.assertEqual(len(cenas(g)), 1)  # sem ter visto o ossuário, a página é a de sempre

    def test_clicar_e_voltar_nao_gasta_nem_celebra(self):
        g = no_ossuario()
        antes = (g.j.consumiveis.get("tocha"), g.j.flechas, g.periodo)
        fazer(g, "correntes", "Deixar")
        self.assertEqual((g.j.consumiveis.get("tocha"), g.j.flechas, g.periodo), antes)
        self.assertEqual(missoes.registro(g, MID)["preparos"], [])
        self.assertEqual(g.ui.celebradas, [])
        self.assertEqual(cenas(g)[-1]["foco"], "sarilho")  # a tela enquadra o mecanismo enquanto se escolhe

    def test_corrente_desce_so_depois_do_preparo(self):
        for passa in (True, False):
            g = no_ossuario()
            lutas(g, "vitoria")
            g.teste = lambda a, cd, p=passa: p
            fazer(g, "correntes", "Arrancar")
            self.assertEqual(g.ui.celebradas, [("correntes", ["corpo_solto"])])

    def test_luta_perdida_ou_fuga_nao_solta(self):
        for fim in ("fuga", "derrota"):
            g = no_ossuario()
            lutas(g, fim)
            g.teste = lambda a, cd: False
            try:
                fazer(g, "correntes", "Arrancar")
            except Derrota:  # a derrota sobe para o jogo (o resgate)
                pass
            self.assertEqual((missoes.registro(g, MID)["preparos"], g.ui.celebradas), ([], []))
            self.assertEqual(missoes.cena_ossuario(g)["correntes"], "presas")

    def test_texto_sem_animacao(self):
        g = no_ossuario()
        g.ui.conquistas_na_tela = False  # o terminal: nem cena desenhada nem celebração
        lutas(g, "vitoria")
        g.teste = lambda a, cd: True
        fazer(g, "correntes", "Arrancar")
        self.assertEqual(g.ui.celebradas, [])
        self.assertEqual(missoes.registro(g, MID)["preparos"], ["corpo_solto"])


if __name__ == "__main__":
    unittest.main()
