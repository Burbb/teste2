"""A recuperação da campanha com resgate (E9): a queda em combate, a fome e a infecção levam ao mesmo resgate, na casa
de Marta, no Vau. Os dois dias alimentam o herói e a comitiva sem gastar a bolsa e encerram a emergência (fome,
infecção, feridas abertas); os outros ferimentos seguem as regras. Uma queda, uma recuperação, uma cobrança. O hardcore
e o mundo gerado ficam como eram. E a nota do custo no recrutamento."""

import os
import random
import tempfile
import unittest
from unittest import mock

from rpg import comitiva as cm, sobrevivencia
from rpg.jogo import Jogo
from rpg.regras import Derrota, FimDeJogo
from rpg.ui import BotUI
from tests.test_caspar import resolvida
from tests.test_missoes import Roteiro, ir

INFECCAO = {"id": "infeccao", "dias": None, "tratado": False}


def campanha(classe="guerreiro", ui=None, pasta=None):
    """A campanha no modo resgate (o Jogo nasce em hardcore)."""
    g = Jogo(ui or Roteiro(), seed=5, pasta_saves=pasta or tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", classe, "turvo")
    return g


def no_charco(classe="guerreiro", ui=None, pasta=None, ouro=30, provisoes=3):
    g = campanha(classe, ui or Roteiro(), pasta)
    ir(g, "charco_dos_juncos")
    g.j.ouro, g.j.provisoes = ouro, provisoes
    return g


def faminto(g, vida=4):
    """Três dias sem comer e quase sem vida: a próxima noite mata (a fome tira 20% da vida máxima)."""
    g.j.provisoes, g.j.fome, g.j.hp = 0, 3, vida
    return g


def infeccionado(g, vida=3):
    g.j.ferimentos.append(dict(INFECCAO))
    g.j.recalcular()
    g.j.hp = vida
    return g


def cair_de_noite(g):
    """A noite que derruba: devolve a causa da queda (Derrota), ou None se ninguém caiu."""
    try:
        g.novo_dia(descanso=1)
    except Derrota as d:
        return d.causa
    return None


def resgates(g):
    return [e for e in g.registro if e["t"] == "resgate"]


class TestQuedaSemLuta(unittest.TestCase):
    def test_fome_e_infeccao_viram_queda_na_campanha(self):
        for preparar, causa in ((faminto, "fome"), (infeccionado, "infeccao")):
            g = preparar(no_charco())
            self.assertEqual(cair_de_noite(g), causa)
            self.assertEqual(g.j.hp, 0)
            self.assertIsNone(g.queda_pendente)  # a queda sai uma vez só

    def test_fome_e_infeccao_juntas_sao_uma_queda(self):
        g = infeccionado(faminto(no_charco()), vida=4)
        self.assertEqual(cair_de_noite(g), "fome")  # a primeira que zerou a vida dá a causa
        g.resgate("fome")
        self.assertEqual(len(resgates(g)), 1)
        self.assertEqual((g.j.fome, [f["id"] for f in g.j.ferimentos]), (0, []))

    def test_noite_sem_perigo_nao_cai(self):
        g = no_charco()
        self.assertIsNone(cair_de_noite(g))

    def test_hardcore_e_mundo_gerado_morrem_como_antes(self):
        pasta = tempfile.mkdtemp()
        g = Jogo(Roteiro(), seed=5, pasta_saves=pasta, hardcore=True)
        g.iniciar("Teste", "guerreiro", "turvo")
        faminto(g)
        g.salvar(silencioso=True)
        with self.assertRaises(FimDeJogo):
            g.novo_dia(descanso=1)
        self.assertFalse(any(f.endswith(".json") for f in os.listdir(pasta)))  # o hardcore apaga
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
        g.iniciar("Teste", "guerreiro")
        for preparar in (faminto, infeccionado):
            preparar(g)
            with self.assertRaises(FimDeJogo):
                g.novo_dia(descanso=1)
            self.assertIsNone(g.queda_pendente)

    def test_rodar_leva_a_causa_ao_resgate(self):
        g = faminto(no_charco())
        causas = []
        telas = iter([lambda: g.novo_dia(descanso=1)])

        def tela():
            next(telas, lambda: (_ for _ in ()).throw(FimDeJogo()))()

        with mock.patch.object(g, "tela", tela), mock.patch.object(g, "resgate", causas.append):
            g.rodar()
        self.assertEqual(causas, ["fome"])


class TestResgate(unittest.TestCase):
    def test_queda_em_combate_nao_come_a_bolsa(self):
        g = no_charco(ouro=50, provisoes=3)
        dia = g.dia
        g.resgate()
        self.assertEqual((g.dia, g.loc["chave"], g.j.provisoes, g.j.ouro), (dia + 2, "vau_do_turvo", 3, 35))
        self.assertEqual(g.estatisticas["quedas"], 1)
        self.assertEqual([(e["causa"], e["perda"]) for e in resgates(g)], [("combate", 15)])

    def test_comitiva_come_no_resgate(self):
        g = no_charco(provisoes=0)
        for cid in ("morel", "odete"):
            cm.recrutar(g, cid)
        aprovacao = {m["id"]: m["aprovacao"] for m in cm.membros(g)}
        vida = {m["id"]: m["hp"] for m in cm.membros(g)}
        g.resgate()
        self.assertEqual(g.j.provisoes, 0)
        self.assertEqual({m["id"]: m["aprovacao"] for m in cm.membros(g)}, aprovacao)  # ninguém passou fome
        self.assertEqual({m["id"]: m["hp"] for m in cm.membros(g)}, vida)
        self.assertIn("deu caldo a você e à comitiva", " ".join(g.ui.ditos))

    def test_soldo_do_morel_vem_depois_de_acordar(self):
        # O sétimo dia de Morel cai num dos dois dias do resgate: a cobrança espera o herói ser achado e acordar na
        # casa de Marta (antes, Morel estendia a mão enquanto o herói ainda estava caído). Paga com o ouro que sobrou.
        for dias in (5, 6):  # o sétimo dia no primeiro ou no segundo dia do resgate
            ui = Roteiro(["Pagar"])
            g = no_charco(ui=ui, ouro=100)
            cm.recrutar(g, "morel")["dias"] = dias
            g.resgate()
            ditos = " ".join(ui.ditos)
            self.assertIn("Morel estende a mão aberta", ditos)
            self.assertLess(ditos.index("Alguém do Vau te acha"), ditos.index("Morel estende a mão aberta"), dias)
            self.assertLess(ditos.index("Parte do seu ouro sumiu"), ditos.index("Morel estende a mão aberta"), dias)
            valor = 8 + 3 * g.j.nivel
            self.assertEqual(g.j.ouro, 100 - 30 - valor)  # o resgate leva 30%; o soldo sai do que ficou
            self.assertEqual(ui.ofertas[-1][0], f"Pagar {valor} ouro")

    def test_fome_encerra_a_emergencia(self):
        g = faminto(no_charco(ouro=0))
        g.resgate(cair_de_noite(g))
        j = g.j
        self.assertEqual((j.fome, j.provisoes, g.loc["chave"]), (0, 0, "vau_do_turvo"))
        self.assertNotIn("Fome", [n for fontes in sobrevivencia.fontes_penalidade(j).values() for n, _ in fontes])
        self.assertGreaterEqual(j.hp, int(j.max_hp * 0.4))
        self.assertLessEqual(j.hp, j.max_hp)

    def test_infeccao_tratada_feridas_abertas_enfaixadas_o_resto_fica(self):
        g = no_charco()
        g.j.ferimentos += [{"id": "corte", "dias": 4, "tratado": False}, {"id": "braco", "dias": 8, "tratado": False}]
        infeccionado(g)
        g.resgate(cair_de_noite(g))
        feridas = {f["id"]: f for f in g.j.ferimentos}
        self.assertNotIn("infeccao", feridas)
        self.assertTrue(feridas["corte"]["tratado"])
        self.assertIn("braco", feridas)  # fratura não se resolve no resgate: segue sarando pelos dias
        self.assertLess(feridas["braco"]["dias"], 8)
        self.assertIn("abriu e limpou a ferida infeccionada", " ".join(g.ui.ditos))
        self.assertGreater(g.j.hp, 0)

    def test_nada_derruba_durante_o_proprio_resgate(self):
        g = no_charco()
        g.resgatando = True
        faminto(g)
        self.assertIsNone(cair_de_noite(g))
        self.assertGreaterEqual(g.j.hp, 1)
        g.resgatando = False
        # Mesmo uma ferida aberta sem tratar não infecciona nos dois dias: o resgate enfaixa antes.
        g = no_charco()
        g.j.ferimentos.append({"id": "corte", "dias": 4, "tratado": False})
        g.rng.random = lambda: 0.0  # toda chance de infecção sairia
        g.resgate()
        self.assertEqual([f["id"] for f in g.j.ferimentos], ["corte"])
        self.assertEqual(len(resgates(g)), 1)

    def test_sem_comida_sem_ouro_continua_se_recuperando(self):
        """O herói sem comida, sem ouro e sem nada para vender: a fome volta, mas cada queda dá uma recuperação, e o
        jogo continua (nenhum fim de jogo, a vida sempre válida)."""
        g = faminto(no_charco(ouro=0, provisoes=0))
        g.j.mochila = []
        quedas = 0
        for _ in range(20):
            causa = cair_de_noite(g)
            if causa:
                quedas += 1
                g.resgate(causa)
            self.assertTrue(0 < g.j.hp <= g.j.max_hp)
        self.assertEqual(len(resgates(g)), quedas)
        self.assertGreaterEqual(quedas, 2)

    def test_quem_cuida_marta_ou_pita(self):
        g = no_charco()
        g.resgate()
        texto = " ".join(g.ui.ditos)
        self.assertIn("Pita trocou as faixas", texto)
        self.assertIn("ao lado da cama em que ela ainda está doente", texto)
        g = resolvida("descansada", ui=Roteiro(), dias=5)  # a água já limpou: Marta está de pé
        g.hardcore = False
        ir(g, "charco_dos_juncos")
        g.resgate()
        self.assertIn("Marta trocou as faixas", " ".join(g.ui.ditos))

    def test_o_que_aconteceu_aparece_uma_vez(self):
        g = faminto(no_charco(ouro=20))
        g.resgate(cair_de_noite(g))
        ditos = g.ui.ditos
        self.assertEqual(sum("A fome vence" in d for d in ditos), 1)
        self.assertEqual(sum("Dois dias se passaram" in d for d in ditos), 1)
        self.assertEqual(sum("ouro sumiu" in d for d in ditos), 1)
        self.assertNotIn("Você finalmente come", " ".join(ditos))  # o caldo já disse isso

    def test_um_quadro_de_amanhecer_so(self):
        class Quadros(Roteiro):
            conquistas_na_tela = True

            def __init__(self):
                super().__init__()
                self.quadros = []

            def celebrar(self, tipo, dados=None):
                if tipo == "amanhecer":
                    self.quadros.append(dados["dia"])

        g = no_charco(ui=Quadros())
        dia = g.dia
        g.resgate()
        self.assertEqual(g.ui.quadros, [dia + 2])

    def test_salvar_e_carregar_depois_do_resgate(self):
        pasta = tempfile.mkdtemp()
        g = infeccionado(faminto(no_charco(pasta=pasta)), vida=4)
        g.resgate(cair_de_noite(g))
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(h.j.para_dict(), g.j.para_dict())
        self.assertEqual((h.dia, h.loc["chave"], h.queda_pendente, h.resgatando), (g.dia, "vau_do_turvo", None, False))
        self.assertIsNone(cair_de_noite(h))  # a emergência acabou: a próxima noite não derruba

    def test_robo_atravessa_com_quedas_sem_fim_de_jogo(self):
        """O robô de sempre, no modo resgate: com fome e infecção virando queda, a partida não acaba sozinha."""
        for classe in ("guerreiro", "arqueiro", "mago"):
            g = campanha(classe, BotUI(random.Random(len(classe)), max_decisoes=400))
            g.j.provisoes = 0
            try:
                g.rodar()
            except Exception as e:  # LimiteBot: o robô parou por decisões, não por morte
                self.assertEqual(type(e).__name__, "LimiteBot")
            self.assertNotIn("causa", g.estatisticas)


class TestPrologo(unittest.TestCase):
    def test_prologo_diz_que_fome_e_infeccao_tambem_tem_resgate(self):
        ui = Roteiro()
        g = campanha(ui=ui)
        g.introducao_campanha()
        texto = " ".join(ui.ditos)
        self.assertIn("se você cair em combate, de fome ou de infecção", texto)
        self.assertNotIn("encerram a partida", texto)


class TestNotaDoRecrutamento(unittest.TestCase):
    def test_aceitar_traz_o_custo(self):
        g = campanha()
        visto = []
        g.menu = lambda pergunta, opcoes: visto.extend(opcoes) or "nao"
        cm.oferecer_vaga(g, "odete")
        aceitar = next(o for o in visto if o[1] == "sim")
        self.assertEqual(aceitar[2], {"nota": "Consome 1 provisão por dia."})
        self.assertEqual(len([o for o in visto if len(o) > 2]), 1)  # só a opção de aceitar

    def test_no_texto_a_nota_vai_junto_da_opcao(self):
        ui = Roteiro(["Recusar"])
        g = campanha(ui=ui)
        cm.oferecer_vaga(g, "odete")
        self.assertIn("Aceitar Odette na comitiva — Consome 1 provisão por dia.", ui.ofertas[-1])

    def test_troca_com_comitiva_cheia_nao_leva_a_nota(self):
        g = campanha()
        for cid in ("morel", "odete"):
            cm.recrutar(g, cid)
        self.assertEqual(len(cm.membros(g)), cm.LIMITE)
        visto = []
        g.menu = lambda pergunta, opcoes: visto.extend(opcoes) or None
        cm.oferecer_vaga(g, "yara")
        self.assertFalse([o for o in visto if len(o) > 2 and o[2].get("nota")])


if __name__ == "__main__":
    unittest.main()
