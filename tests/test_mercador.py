"""O mercador ambulante (E9): a compra fica à vista, indisponível quando falta ouro, com o que falta; depois do exame,
o preço atualizado e a despedida, com ou sem ouro. Os sorteios do evento seguem os de antes."""

import tempfile
import unittest

from rpg.eventos import comuns
from rpg.jogo import Jogo
from tests.test_missoes import Roteiro


class Gravando(Roteiro):
    def __init__(self, roteiro=()):
        super().__init__(roteiro)
        self.metas = []

    def escolher(self, pergunta, opcoes):
        self.metas.append(self.meta_opcoes)
        return super().escolher(pergunta, opcoes)


def mercador(ouro, roteiro, teste=True, legitima=True):
    ui = Gravando(roteiro)
    g = Jogo(ui, seed=3, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", "guerreiro")
    g.j.ouro = ouro
    g.teste = lambda attr, cd: teste
    g.chance = lambda p: not legitima if p == 0.4 else False
    g.oferecer_equip = lambda it: ui.ditos.append(f"recebeu {it['nome']}")
    comuns.mercador_ambulante(g)
    return g, ui


class TestMercador(unittest.TestCase):
    def test_sem_ouro_as_compras_ficam_a_vista_indisponiveis(self):
        g, ui = mercador(0, ["Recusar"])
        rotulos = ui.ofertas[0]
        self.assertTrue(rotulos[0].startswith("Comprar ("))
        self.assertIn("indisponível: Faltam", rotulos[0])
        self.assertIn("Comprar uma poção de vida", rotulos[2])
        self.assertIn("Você se despede", " ".join(ui.ditos))

    def test_exame_legitimo_sem_ouro_mostra_o_preco_e_deixa_despedir(self):
        g, ui = mercador(0, ["Examinar", "Despedir-se"])
        texto = " ".join(ui.ditos)
        self.assertIn("A peça é legítima", texto)
        self.assertRegex(texto, r"por \d+ ouro\.")  # o preço com o desconto
        segunda = ui.ofertas[1]
        self.assertTrue(segunda[0].startswith("Comprar (") and "indisponível: Faltam" in segunda[0])
        self.assertEqual(segunda[1], "Despedir-se")
        self.assertIn("Você se despede", texto)
        self.assertEqual(g.j.ouro, 0)

    def test_exame_legitimo_com_ouro_compra_pelo_preco_novo(self):
        g, ui = mercador(500, ["Examinar", "Comprar"])
        preco = int(ui.ofertas[1][0].split("(")[1].split(" ")[0])
        self.assertEqual(g.j.ouro, 500 - preco)
        self.assertIn("recebeu", " ".join(ui.ditos))
        self.assertIsNone(ui.metas[1][0] if ui.metas[1] else None)  # disponível: sem motivo

    def test_exame_malsucedido_sem_ouro_tambem_responde(self):
        g, ui = mercador(0, ["Examinar", "Despedir-se"], teste=False)
        self.assertIn("Parece tudo certo", " ".join(ui.ditos))
        self.assertIn("indisponível", ui.ofertas[1][0])
        self.assertIn("Você se despede", " ".join(ui.ditos))

    def test_texto_nao_deixa_escolher_a_indisponivel(self):
        g, ui = mercador(0, ["Examinar", "Comprar", "Despedir-se"])
        self.assertEqual(g.j.ouro, 0)
        self.assertIn("Faltam", " ".join(ui.ditos))  # o motivo, e a pergunta de novo

    def test_sorteios_iguais_com_e_sem_ouro(self):
        """Mostrar a compra indisponível não gasta sorteio: o jogo segue igual depois do evento."""
        estados = []
        for ouro in (0, 3):
            ui = Roteiro(["Recusar"])
            g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp(), hardcore=False)
            g.iniciar("Teste", "guerreiro")
            g.j.ouro = ouro
            comuns.mercador_ambulante(g)
            estados.append(g.rng.random())
        self.assertEqual(estados[0], estados[1])


if __name__ == "__main__":
    unittest.main()
