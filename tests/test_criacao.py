"""A criação do personagem numa tela só (criacao.py, a tela gráfica): os dados que a tela mostra vêm das regras, e o
motor confere a resposta, começa a campanha uma vez só e volta ao título no Voltar."""

import tempfile
import unittest

from rpg import abertura, criacao
from rpg.classes import CLASSES, SPECS
from rpg.jogo import Jogo
from tests.test_abertura import Jogador


class Tela(Jogador):
    """A tela da criação: devolve as respostas na ordem (a que não serve volta à tela) e anota quantas vezes perguntou."""
    criacao_na_tela = True

    def __init__(self, respostas):
        super().__init__([])
        self.respostas, self.vezes, self.dados = list(respostas), 0, None

    def criar_personagem(self, dados):
        self.vezes += 1
        self.dados = dados
        return self.respostas.pop(0)


def jogo(ui):
    return Jogo(ui, seed=4, pasta_saves=tempfile.mkdtemp())


class TestDados(unittest.TestCase):
    def test_as_classes_com_os_numeros_das_regras(self):
        d = criacao.dados("turvo")
        self.assertEqual(d["regiao"], "Vale do Turvo")
        self.assertEqual([c["id"] for c in d["classes"]], list(CLASSES))
        for c in d["classes"]:
            base = CLASSES[c["id"]]
            self.assertEqual(c["frase"], base["frase"])
            self.assertEqual((c["recurso"]["total"], c["recurso"]["regen"]), (base["base"]["max_rec"], base["base"]["regen"]))
            self.assertEqual(c["ataque"]["nome"], base["ataque"][0])
            self.assertEqual(c["specs"], [SPECS[s]["nome"] for s in base["specs"]])
        self.assertEqual([m["id"] for m in d["modo"]["opcoes"]], ["resgate", "hardcore"])
        self.assertEqual(d["modo"]["padrao"], "resgate")
        self.assertTrue(d["tutorial"]["marcada"])


class TestConferir(unittest.TestCase):
    def test_o_nome_em_branco_vira_o_padrao_e_o_longo_e_cortado(self):
        r = {"classe": "mago", "modo": "resgate", "tutorial": True}
        self.assertEqual(criacao.conferir({**r, "nome": "   "})[0], "Aventureiro")
        longo = "Maria da Conceição Albuquerque de Figueiredo Brás"
        self.assertEqual(criacao.conferir({**r, "nome": longo})[0], longo[:40].strip())

    def test_classe_ou_modo_que_nao_existem_nao_servem(self):
        self.assertIsNone(criacao.conferir({"nome": "Ana", "classe": "bardo", "modo": "resgate"}))
        self.assertIsNone(criacao.conferir({"nome": "Ana", "classe": "mago", "modo": "facil"}))
        self.assertIsNone(criacao.conferir("Ana"))

    def test_hardcore_e_tutorial(self):
        self.assertEqual(criacao.conferir({"nome": "Ana", "classe": "arqueiro", "modo": "hardcore", "tutorial": False}),
                         ("Ana", "arqueiro", True, False))


class TestNovoJogoNaTela(unittest.TestCase):
    def test_comeca_uma_vez_com_o_que_se_escolheu(self):
        ui = Tela([{"nome": "Ana", "classe": "bardo", "modo": "resgate"},  # não serve: a tela pergunta de novo
                   {"nome": "Ana", "classe": "arqueiro", "modo": "hardcore", "tutorial": False}])
        g = jogo(ui)
        self.assertTrue(g.novo_jogo("turvo"))
        self.assertEqual(ui.vezes, 2)
        self.assertEqual((g.j.nome, g.j.classe, g.hardcore), ("Ana", "arqueiro", True))
        self.assertFalse(abertura.tutorial(g))
        self.assertEqual(abertura.estado(g)["despensa"], "nova")

    def test_resgate_com_tutorial(self):
        g = jogo(Tela([{"nome": "Bento", "classe": "guerreiro", "modo": "resgate", "tutorial": True}]))
        self.assertTrue(g.novo_jogo("turvo"))
        self.assertFalse(g.hardcore)
        self.assertTrue(abertura.tutorial(g))

    def test_voltar_volta_ao_titulo(self):
        ui = Tela([{"voltar": True}])
        g = jogo(ui)
        self.assertFalse(g.novo_jogo("turvo"))
        self.assertIsNone(g.mundo)
        self.assertEqual(ui.vezes, 1)


if __name__ == "__main__":
    unittest.main()
