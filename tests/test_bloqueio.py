"""O bloqueio de um destino (1.200.0): a mesma regra para a viagem recusar e para a tela desenhar (mapa.bloqueio, o
campo `bloqueio` de cada lugar no mapa da tela). A saída fechada da campanha vem do `fechado` do lugar, não do nome; a
cidadela do mundo gerado, dos três Sigilos, depois da confirmação do perigo, como sempre. O lugar só conhecido, o que
não é vizinho e o perigoso não são bloqueio."""

import random
import tempfile
import unittest

from rpg import mapa
from rpg.jogo import Jogo
from rpg.ui import BotUI
from rpg.web.estado import mapa_conhecido


class Roteiro(BotUI):
    """Escolhe pelo texto (a primeira opção que contém o próximo trecho); guarda o que foi dito e as ofertas."""

    def __init__(self, roteiro=()):
        super().__init__(random.Random(1), max_decisoes=100)
        self.roteiro, self.ditos, self.ofertas = list(roteiro), [], []

    def dizer(self, texto="", cor=None):
        self.ditos.append(texto)

    narrar = dizer

    def escolher(self, pergunta, opcoes):
        self.ofertas.append(list(opcoes))
        if self.roteiro:
            for i, o in enumerate(opcoes):
                if self.roteiro[0] in o:
                    self.roteiro.pop(0)
                    self.decisoes += 1
                    return i
        return super().escolher(pergunta, opcoes)


def lugar(g, chave):
    return next(l for l in g.mundo["locais"] if l.get("chave") == chave)


def campanha(ui=None):
    g = Jogo(ui or Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", "guerreiro", "turvo")
    return g


def nos(g):
    return {n["nome"]: n for n in mapa_conhecido(g)["nos"]}


class TestBloqueio(unittest.TestCase):
    def test_a_saida_fechada_e_so_ela(self):
        g = campanha()
        n = nos(g)
        self.assertEqual(n["Estrada de Varn"]["bloqueio"], "fechado")
        for nome in ("Vau do Turvo", "Charco dos Juncos", "Bosque do Moinho"):
            self.assertIsNone(n[nome]["bloqueio"], nome)

    def test_conhecido_nao_vizinho_e_perigoso_nao_sao_bloqueio(self):
        g = campanha()
        bosque = lugar(g, "bosque_do_moinho")
        bosque["visitado"] = True
        g.mundo["atual"] = bosque["id"]
        n = nos(g)
        capela = n["Capela Afogada"]  # conhecida (vizinha do Bosque), ainda não visitada, nível 3 (perigosa no nível 1)
        self.assertFalse(capela["visitado"])
        self.assertEqual(capela["distancia"], 1)
        self.assertGreaterEqual(capela["nivel"], g.j.nivel + 2)
        self.assertIsNone(capela["bloqueio"])
        charco = n["Charco dos Juncos"]  # conhecido pelo Vau, mas não é vizinho do Bosque
        self.assertIsNone(charco["distancia"])
        self.assertIsNone(charco["bloqueio"])

    def test_vem_da_regra_e_nao_do_nome(self):
        """Um lugar qualquer com `fechado` vira bloqueado na tela e na viagem; o nome não importa."""
        ui = Roteiro(["Charco dos Juncos"])
        g = campanha(ui)
        charco = lugar(g, "charco_dos_juncos")
        charco["fechado"] = "A ponte caiu; por enquanto não se passa."
        self.assertEqual(nos(g)["Charco dos Juncos"]["bloqueio"], "fechado")
        antes = (g.loc["id"], g.dia, g.periodo)
        g.viajar()
        self.assertEqual((g.loc["id"], g.dia, g.periodo), antes)
        self.assertIn(charco["fechado"], ui.ditos)
        # e a Estrada de Varn sem o `fechado` deixa de ser bloqueio, com o mesmo nome
        del lugar(g, "estrada_de_varn")["fechado"]
        self.assertIsNone(nos(g)["Estrada de Varn"]["bloqueio"])

    def test_a_cidadela_selada_pelos_sigilos(self):
        """Mundo gerado: a cidadela é bloqueio sem os três Sigilos; a viagem pergunta do perigo antes, como sempre."""
        ui = Roteiro(["CIDADELA", "Ir mesmo assim"])
        g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp(), hardcore=False)
        g.iniciar("Teste", "guerreiro")
        cid = next(l for l in g.mundo["locais"] if l["tipo"] == "cidadela")
        self.assertEqual(mapa.bloqueio(g, cid), "selada")
        vizinho = next(l for l in g.mundo["locais"] if str(cid["id"]) in l["con"])
        vizinho["visitado"] = True
        g.mundo["atual"] = vizinho["id"]
        self.assertEqual(nos(g)[cid["nome"]]["bloqueio"], "selada")
        g.viajar()
        self.assertEqual(g.loc["id"], vizinho["id"])  # não foi
        perguntas = [o for oferta in ui.ofertas for o in oferta if "Ir mesmo assim" in o]
        self.assertTrue(perguntas, "a confirmação do perigo vem antes do bloqueio")
        self.assertTrue(any("muralha de sombras" in d for d in ui.ditos))
        g.j.sigilos += ["a", "b", "c"]
        self.assertIsNone(mapa.bloqueio(g, cid))
        self.assertIsNone(nos(g)[cid["nome"]]["bloqueio"])


if __name__ == "__main__":
    unittest.main()
