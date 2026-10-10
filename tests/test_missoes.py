"""A missão "A Febre do Turvo" (E3): o registro com etapas, a cena de abertura no Vau, o objetivo no Diário e no estado
da tela, o exame da Fonte Nova, o canal no Bosque do Moinho, o exterior da Capela Afogada, as visitas antecipadas, o
save e os saves da campanha de antes das missões."""

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
        self.ditos, self.ofertas, self.paineis, self.cenas, self.continuares = [], [], [], [], []

    def dizer(self, texto="", cor=None):
        self.ditos.append(texto)

    narrar = dizer

    def cena(self, titulo, subtitulo=None, tipo="evento"):
        self.cenas.append(titulo)

    def painel(self, tipo, dados):
        self.paineis.append((tipo, dados))
        return False

    def continuar(self, confirmar=False):
        self.continuares.append((self.cenas[-1] if self.cenas else None, confirmar))

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


def ir(g, chave):
    g.mundo["atual"] = lugar(g, chave)["id"]
    lugar(g, chave)["visitado"] = True


CANAL = "Seguir a água e examinar o canal"


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

    def test_tres_classes_vao_da_fonte_ao_exterior_da_capela(self):
        for classe in CLASSES:
            ui = Roteiro(["Examinar a Fonte Nova", CANAL])
            g = campanha(classe, ui)
            g.tela(); g.tela()  # abertura; exame da fonte
            ir(g, "bosque_do_moinho")
            antes = len(ui.ditos)
            g.tela()  # o menu do bosque, com o passo da missão; o roteiro segue o canal
            self.assertIn(CANAL, ui.ofertas[-1])
            m = missoes.registro(g, MID)
            self.assertEqual((m["etapa"], m["pistas"]), ("capela", ["agua_do_leste", "represa", "canal_da_capela"]))
            self.assertEqual(ui.cenas[-1], "O Canal do Moinho")
            texto = " ".join(ui.ditos[antes:])
            self.assertIn("represa", texto)
            self.assertNotIn("Ilse", texto)  # o canal mostra o caminho da água, não a causa
            self.assertNotIn("Sigilo do", texto)
            ir(g, "capela_afogada")
            g.tela()  # a cena de fora da capela, uma vez
            self.assertEqual(ui.cenas[-1], "A Capela Afogada")
            self.assertEqual(m["cenas"], ["abertura", "capela_exterior"])
            self.assertIn("O canal que você seguiu desde o moinho", " ".join(ui.ditos))
            self.assertFalse(missoes.cena_pendente(g))
            self.assertFalse(missoes.opcoes(g))  # o interior ainda não existe: nada a fazer aqui por ora
            cartao = estado(g)["missoes"][0]
            self.assertEqual((cartao["etapa"], cartao["lugar_id"]), ("capela", lugar(g, "capela_afogada")["id"]))
            self.assertEqual(len(cartao["pistas"]), 3)

    def test_visitar_antes_nao_adianta_nem_gasta(self):
        """Passar pelo bosque e pela capela antes da hora não mostra nem consome nada; voltando na etapa certa, a ação
        e a cena estão lá."""
        ui = Roteiro(["Examinar a Fonte Nova", CANAL])
        g = campanha(ui=ui)
        g.tela()  # abertura
        for chave in ("bosque_do_moinho", "capela_afogada"):  # etapa "fonte"
            ir(g, chave)
            self.assertFalse(missoes.cena_pendente(g))
            self.assertFalse(missoes.opcoes(g))
            self.assertFalse(missoes.executar(g, MID, "seguir_canal"))
        ir(g, "vau_do_turvo")
        g.tela()  # exame: etapa "canal"
        ir(g, "capela_afogada")  # a capela antes do canal: ainda nada
        self.assertFalse(missoes.cena_pendente(g))
        self.assertEqual(missoes.registro(g, MID)["cenas"], ["abertura"])
        ir(g, "bosque_do_moinho")
        g.tela()
        self.assertEqual(missoes.registro(g, MID)["etapa"], "capela")
        self.assertFalse(missoes.opcoes(g))  # repetir no bosque: a ação some
        self.assertFalse(missoes.executar(g, MID, "seguir_canal"))
        self.assertFalse(missoes.avancar(g, MID, "canal", "capela"))
        self.assertEqual(missoes.registro(g, MID)["pistas"], ["agua_do_leste", "represa", "canal_da_capela"])
        self.assertEqual(len([e for e in g.registro if e["t"] == "missao"]), 2)
        ir(g, "capela_afogada")
        self.assertTrue(missoes.cena_pendente(g))
        self.assertFalse(missoes.cena_pendente(g))

    def test_cenas_da_missao_pedem_confirmacao(self):
        """Toda cena e ação da missão declara `confirmar` e termina num Continuar que pede confirmação explícita (a
        tela gráfica não vira a página sozinha)."""
        self.assertTrue(all(d["confirmar"] for d in missoes.CENAS + missoes.ACOES))
        ui = Roteiro(["Examinar a Fonte Nova", CANAL])
        g = campanha(ui=ui)
        g.tela(); g.tela()
        ir(g, "bosque_do_moinho"); g.tela()
        ir(g, "capela_afogada"); g.tela()
        self.assertEqual(ui.continuares[-4:], [("A Febre do Turvo", True), ("A Fonte Nova", True),
                                               ("O Canal do Moinho", True), ("A Capela Afogada", True)])

    def test_fonte_respeita_a_hora(self):
        for periodo, hora in enumerate(("a manhã", "a tarde", "o anoitecer", "a noite")):
            ui = Roteiro(["Examinar a Fonte Nova"])
            g = campanha(ui=ui)
            g.tela()
            g.periodo = periodo
            g.tela()
            texto = " ".join(ui.ditos)
            self.assertIn(f"fria demais para {hora}.", texto)
            self.assertNotIn("fim da tarde", texto)

    def test_save_da_etapa_canal_continua(self):
        """Um save da 1.50 (etapa "canal", com a pista da fonte) segue de onde parou, sem perder a pista."""
        pasta = tempfile.mkdtemp()
        ui = Roteiro(["Examinar a Fonte Nova"])
        g = campanha("mago", ui, pasta)
        g.tela(); g.tela()
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro([CANAL]), g.caminho_save(), pasta)
        self.assertEqual(missoes.registro(h, MID), {"etapa": "canal", "cenas": ["abertura"], "pistas": ["agua_do_leste"]})
        ir(h, "bosque_do_moinho")
        h.tela()
        h.salvar(silencioso=True)
        k = Jogo.carregar(Roteiro(), h.caminho_save(), pasta)
        self.assertEqual(missoes.registro(k, MID),
                         {"etapa": "capela", "cenas": ["abertura"], "pistas": ["agua_do_leste", "represa", "canal_da_capela"]})
        ir(k, "capela_afogada")
        self.assertTrue(missoes.cena_pendente(k))
        k.salvar(silencioso=True)
        z = Jogo.carregar(Roteiro(), k.caminho_save(), pasta)
        self.assertEqual(missoes.registro(z, MID)["cenas"], ["abertura", "capela_exterior"])
        self.assertFalse(missoes.cena_pendente(z))

    def test_diario_diz_o_que_voce_sabe(self):
        ui = Roteiro(["Examinar a Fonte Nova", "Fechar"])
        g = campanha(ui=ui)
        g.diario()
        self.assertNotIn("O que você sabe:", " ".join(ui.ditos))  # nada descoberto ainda
        g.tela(); g.tela()
        ui.ditos.clear()
        g.diario()
        self.assertIn("O que você sabe:", " ".join(ui.ditos))
        self.assertNotIn("Pistas", " ".join(ui.ditos))
        self.assertEqual(ui.paineis[-1][1]["missoes"][0]["pistas"], [missoes.MISSOES[MID]["pistas"]["agua_do_leste"]])

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
