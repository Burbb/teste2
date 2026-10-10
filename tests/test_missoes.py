"""A missão "A Febre do Turvo" (primeira entrega da E3): o registro com etapas, a cena de abertura no Vau, o objetivo no
Diário e no estado da tela, o exame da Fonte Nova, o save e os saves da campanha de antes das missões."""

import json
import os
import random
import tempfile
import unittest

from rpg import missoes
from rpg.jogo import Jogo
from rpg.ui import BotUI
from rpg.web.estado import estado

CLASSES = ("guerreiro", "arqueiro", "mago")
MID = "febre_do_turvo"


class Roteiro(BotUI):
    """Escolhe pelo texto (o próximo trecho do roteiro); anota o que foi dito, as opções e os painéis."""

    def __init__(self, roteiro=()):
        super().__init__(random.Random(1), max_decisoes=200)
        self.roteiro = list(roteiro)
        self.ditos, self.ofertas, self.paineis, self.cenas = [], [], [], []

    def dizer(self, texto="", cor=None):
        self.ditos.append(texto)

    narrar = dizer

    def cena(self, titulo, subtitulo=None, tipo="evento"):
        self.cenas.append(titulo)

    def painel(self, tipo, dados):
        self.paineis.append((tipo, dados))
        return False

    def escolher(self, pergunta, opcoes):
        self.ofertas.append(list(opcoes))
        alvo = self.roteiro.pop(0)
        return next(i for i, o in enumerate(opcoes) if o.startswith(alvo))


def campanha(classe="guerreiro", ui=None, pasta=None):
    g = Jogo(ui or Roteiro(), seed=5, pasta_saves=pasta or tempfile.mkdtemp())
    g.iniciar("Teste", classe, "turvo")
    return g


def lugar(g, chave):
    return next(l for l in g.mundo["locais"] if l.get("chave") == chave)


class TestMissao(unittest.TestCase):
    def test_tres_classes_iniciam_e_avancam(self):
        for classe in CLASSES:
            ui = Roteiro(["Examinar a Fonte Nova"])
            g = campanha(classe, ui)
            self.assertEqual(missoes.registro(g, MID), {"etapa": "fonte", "cenas": [], "pistas": []})
            g.tela()  # a cena de abertura toca no lugar do menu
            self.assertEqual(ui.cenas[-1], "A Febre do Turvo")
            self.assertEqual(missoes.registro(g, MID)["cenas"], ["abertura"])
            g.tela()  # agora o menu da vila, com o passo da missão; o roteiro escolhe examinar
            self.assertIn("Examinar a Fonte Nova", ui.ofertas[-1])
            m = missoes.registro(g, MID)
            self.assertEqual((m["etapa"], m["pistas"]), ("canal", ["agua_do_leste"]))
            self.assertIn("A Fonte Nova", ui.cenas)

    def test_repetir_nao_anda_de_novo(self):
        ui = Roteiro(["Examinar a Fonte Nova"])
        g = campanha(ui=ui)
        g.tela(); g.tela()
        antes = json.dumps(missoes.registro(g, MID))
        registros = len([e for e in g.registro if e["t"] == "missao"])
        self.assertFalse(missoes.cena_pendente(g))  # a abertura não toca outra vez
        self.assertFalse(missoes.opcoes(g))  # e o exame some do menu
        self.assertFalse(missoes.executar(g, MID, "examinar_fonte"))  # um pedido atrasado não faz nada
        self.assertFalse(missoes.avancar(g, MID, "fonte", "canal"))
        self.assertEqual(json.dumps(missoes.registro(g, MID)), antes)
        self.assertEqual(len([e for e in g.registro if e["t"] == "missao"]), registros)

    def test_diario_e_tela_concordam_com_a_etapa(self):
        for passos in ([], ["Examinar a Fonte Nova"]):
            ui = Roteiro(passos)
            g = campanha(ui=ui)
            g.tela()
            if passos:
                g.tela()
            etapa = missoes.registro(g, MID)["etapa"]
            objetivo = missoes.MISSOES[MID]["etapas"][etapa]["objetivo"]
            cartao = estado(g)["missoes"][0]
            self.assertEqual((cartao["etapa"], cartao["objetivo"]), (etapa, objetivo))
            lugar_alvo = lugar(g, missoes.MISSOES[MID]["etapas"][etapa]["lugar"])
            self.assertEqual(cartao["lugar_id"], lugar_alvo["id"])
            ui.roteiro = ["Fechar"]
            g.diario()
            self.assertEqual(ui.paineis[-1][1]["missoes"], estado(g)["missoes"])
            self.assertIn(objetivo, " ".join(ui.ditos))

    def test_save_preserva_o_avanco(self):
        pasta = tempfile.mkdtemp()
        ui = Roteiro(["Examinar a Fonte Nova"])
        g = campanha("arqueiro", ui, pasta)
        g.tela(); g.tela()
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(missoes.registro(h, MID), {"etapa": "canal", "cenas": ["abertura"], "pistas": ["agua_do_leste"]})
        self.assertFalse(missoes.cena_pendente(h))
        self.assertFalse(missoes.opcoes(h))

    def test_save_da_campanha_de_antes_das_missoes(self):
        """Um save da 1.48–1.49 (sem missões) carrega com a missão na primeira etapa e nada mais muda; a abertura toca
        quando a pessoa estiver no Vau, não no lugar onde o save parou."""
        pasta = tempfile.mkdtemp()
        g = campanha("mago", Roteiro(), pasta)
        del g.mundo["missoes"]
        bosque = lugar(g, "bosque_do_moinho")
        g.mundo["atual"], bosque["visitado"] = bosque["id"], True
        g.j.ouro, g.dia = 77, 9
        g.salvar(silencioso=True)
        with open(g.caminho_save(), encoding="utf-8") as f:
            self.assertNotIn("missoes", json.load(f)["mundo"])
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(missoes.registro(h, MID), {"etapa": "fonte", "cenas": [], "pistas": []})
        self.assertEqual((h.loc["chave"], h.j.ouro, h.dia, h.j.classe), ("bosque_do_moinho", 77, 9, "mago"))
        self.assertEqual({l["chave"] for l in h.mundo["locais"] if l["visitado"]}, {"vau_do_turvo", "bosque_do_moinho"})
        self.assertFalse(missoes.cena_pendente(h))  # no bosque, não
        h.mundo["atual"] = lugar(h, "vau_do_turvo")["id"]
        self.assertTrue(missoes.cena_pendente(h))  # no Vau, sim

    def test_cena_respeita_lugar_e_situacao(self):
        g = campanha()
        g.mundo["atual"] = lugar(g, "charco_dos_juncos")["id"]
        self.assertFalse(missoes.cena_pendente(g))
        self.assertFalse(missoes.opcoes(g))
        g.mundo["atual"] = lugar(g, "vau_do_turvo")["id"]
        g.combate_ativo = object()
        self.assertFalse(missoes.cena_pendente(g))
        g.combate_ativo, g.na_estrada = None, True
        self.assertFalse(missoes.cena_pendente(g))
        g.na_estrada = False
        self.assertEqual(missoes.registro(g, MID)["cenas"], [])

    def test_procedural_nao_tem_missao(self):
        pasta = tempfile.mkdtemp()
        ui = Roteiro(["Fechar"])
        g = Jogo(ui, seed=5, pasta_saves=pasta)
        g.iniciar("Teste", "guerreiro")
        self.assertNotIn("missoes", g.mundo)
        self.assertNotIn("missoes", estado(g))
        self.assertFalse(missoes.cena_pendente(g))
        self.assertEqual(missoes.opcoes(g), [])
        g.diario()
        self.assertNotIn("missoes", ui.paineis[-1][1])
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertNotIn("missoes", h.mundo)
        self.assertTrue(os.path.exists(g.caminho_save()))


if __name__ == "__main__":
    unittest.main()
