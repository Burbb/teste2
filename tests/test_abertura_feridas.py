"""Ferimentos e descanso na abertura guiada (roadmapIDEIAS/18, seção 20): o primeiro ferimento (F1), a bandagem (F2),
a Curandeira (F3) e o cartão dela (F4), o primeiro tratamento grátis, e o descanso (D1 na taverna, D2 no Acampar, D3 na
fogueira) com os números das regras. Nada é provocado: as orientações seguem o estado real."""

import tempfile
import unittest

from rpg import abertura as ab
from rpg import balanceamento as bal
from rpg import sobrevivencia
from rpg.jogo import Jogo
from tests.test_abertura import Jogador
from tests.test_abertura_parte2 import depois_da_despensa, oid
from tests.test_missoes import ir


def ferir(g, *fids):
    for fid in fids:
        g.j.ferimentos.append({"id": fid, "dias": sobrevivencia.FERIMENTOS[fid]["dias"], "tratado": False})
    g.j.recalcular()
    g.j.hp = min(g.j.hp, g.j.max_hp)


def visto(g, *ids):
    g.mundo["abertura"]["vistas"].extend(ids)


class TestFerimento(unittest.TestCase):
    def test_sem_ferimento_nada(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        self.assertNotIn(oid(g), ("F1", "F2", "F3"))

    def test_f1_o_ferimento_real_na_ficha(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        ferir(g, "costelas")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("F1", "ferimento:costelas"))
        self.assertIn("**Costelas quebradas** fica na ficha depois da luta (não passa como o sangramento)", o["texto"])
        self.assertIn("−25% Defesa", o["texto"])
        self.assertIn("Sara em 8 dias de descanso. A **Curandeira** trata na hora.", o["texto"])
        self.assertNotIn("bandagem", o["texto"].lower())  # fratura: a bandagem não trata

    def test_f1_infeccao_nao_passa_sozinha(self):
        g = depois_da_despensa()
        ferir(g, "infeccao")
        self.assertIn("Não passa sozinha: um unguento cura", ab.atual(g)["texto"])

    def test_f1_espera_a_luta_acabar(self):
        from rpg.combate import Combate
        g = depois_da_despensa()
        ferir(g, "corte")
        g.combate_ativo = Combate(g, [g.inimigo("lobo", nivel=1)], None, titulo="Teste")
        self.assertNotEqual(oid(g), "F1")  # na luta, nada de ferimento: o quadro vem depois

    def test_f2_bandagem_na_ferida_aberta(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        ferir(g, "corte")
        visto(g, "F1")
        g.j.consumiveis["bandagem"] = 1
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("F2", "bolsa:bandagem"))
        self.assertEqual(o["texto"], "A bandagem protege a ferida contra infecção. O ferimento ainda precisa sarar.")
        g.executar_comum(("usar", "bandagem"))
        self.assertTrue(g.j.ferimentos[0]["tratado"])  # o estado tratado confirma o resultado
        self.assertIn("F2", g.mundo["abertura"]["vistas"])

    def test_f2_duas_feridas_a_bandagem_trata_a_primeira(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        ferir(g, "mordida", "corte")
        visto(g, "F1")
        g.j.consumiveis["bandagem"] = 2
        self.assertIn("a começar por **Mordida dilacerada**", ab.atual(g)["texto"])
        self.assertEqual(g.o_que_trata("bandagem"), {"trata": "Trata: mordida dilacerada."})  # sem prometer as duas
        g.executar_comum(("usar", "bandagem"))
        self.assertEqual([f["tratado"] for f in g.j.ferimentos], [True, False])

    def test_f2_sem_bandagem_a_alternativa_na_ferida(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        ferir(g, "corte")
        visto(g, "F1")
        g.j.consumiveis["bandagem"] = 0
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"], o["entendi"]), ("F2", "ferimento:corte", True))
        self.assertIn("O **Mercado** vende bandagens", o["texto"])

    def test_f2_nao_para_fratura_nem_infeccao(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        ferir(g, "concussao", "infeccao")
        visto(g, "F1")
        g.j.consumiveis["bandagem"] = 2
        self.assertNotEqual(oid(g), "F2")
        ferir(g, "queimadura")  # depois, a primeira ferida aberta de verdade
        self.assertEqual(ab.atual(g)["ancora"], "bolsa:bandagem")

    def test_f3_curandeira_na_vila_e_some_se_sarou(self):
        g = depois_da_despensa()
        ferir(g, "perna")
        visto(g, "F1")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("F3", "predio:curandeiro"))
        self.assertEqual(o["texto"], "A **Curandeira** trata ferimentos na hora; o Templo só recupera vida. O primeiro "
                                     "tratamento é grátis.")
        g.j.ferimentos = []  # sarou (ou o resgate resolveu) antes de entrar: nada pede tratamento
        self.assertNotEqual(oid(g), "F3")


class TestCurandeiraGratis(unittest.TestCase):
    def cabana(self, roteiro, ouro=0, fids=("corte", "costelas"), tutorial=True):
        g = depois_da_despensa(roteiro=list(roteiro), tutorial=tutorial)
        ferir(g, *fids)
        g.j.ouro = ouro
        g.curandeiro()
        return g

    def test_um_so_de_graca_e_o_resto_cobrado_na_mesma_tela(self):
        g = self.cabana(["Corte profundo — primeiro tratamento, grátis", "Costelas quebradas — ", "Voltar"], ouro=200)
        ofertas = g.ui.ofertas
        self.assertIn("Costelas quebradas — primeiro tratamento, grátis", ofertas[0])  # todos os elegíveis dizem
        preco = ab.custo_tratamento(g, {"id": "costelas"})
        self.assertIn(f"Costelas quebradas — {preco} ouro", ofertas[1])  # depois do grátis, o preço de sempre
        self.assertEqual(g.j.ferimentos, [])
        self.assertEqual(g.j.ouro, 200 - preco)
        self.assertTrue(g.flag("curandeira_gratis_usado"))
        self.assertFalse(g.flag("templo_gratis_usado"))  # separado do grátis do templo

    def test_gratis_com_zero_ouro(self):
        g = self.cabana(["Costelas quebradas — primeiro tratamento, grátis", "Voltar"], ouro=0)
        self.assertEqual([f["id"] for f in g.j.ferimentos], ["corte"])
        self.assertEqual(g.j.ouro, 0)

    def test_abrir_e_sair_nao_gasta(self):
        g = self.cabana(["Voltar"], ouro=50)
        self.assertFalse(g.flag("curandeira_gratis_usado"))
        self.assertTrue(ab.curandeira_gratis(g))

    def test_igual_com_tutorial_desligado(self):
        g = self.cabana(["Corte profundo — primeiro tratamento, grátis", "Voltar"], ouro=0, tutorial=False)
        self.assertTrue(g.flag("curandeira_gratis_usado"))

    def test_nao_renova_ao_carregar_nem_religar(self):
        pasta = tempfile.mkdtemp()
        g = depois_da_despensa(roteiro=["Corte profundo — primeiro tratamento, grátis", "Voltar"], pasta=pasta)
        ferir(g, "corte", "perna")
        g.curandeiro()
        g.salvar(silencioso=True)
        h = Jogo.carregar(Jogador(), g.caminho_save(), pasta)
        ab.ligar(h, False)
        ab.ligar(h, True)
        self.assertFalse(ab.curandeira_gratis(h))
        self.assertEqual([f["id"] for f in h.j.ferimentos], ["perna"])

    def test_so_na_campanha(self):
        g = Jogo(Jogador([]), seed=3, pasta_saves=tempfile.mkdtemp(), hardcore=False)
        g.iniciar("Teste", "mago")
        self.assertFalse(ab.curandeira_gratis(g))

    def test_f4_no_cartao_e_passa_ao_responder(self):
        g = depois_da_despensa()
        ferir(g, "corte")
        visto(g, "F1", "F2", "F3")
        ab.contexto(g, "curandeira")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("F4", "tratar:corte"))
        self.assertIn("o primeiro tratamento é grátis", o["texto"])
        ab.contexto(g, None)


class TestDescanso(unittest.TestCase):
    def test_d1_taverna_com_os_numeros_das_regras(self):
        g = depois_da_despensa()
        j = g.j
        j.hp, j.rec = 10, 0
        o = next(c for c in ab.contextuais(g) if c["id"] == "D1")
        vida = int(j.max_hp * bal.TAVERNA_VIDA)
        self.assertIn(f"custa {ab.preco_dormir(g)} de ouro e vai até amanhã: devolve {vida} de vida e todo o Vigor",
                      o["texto"])
        self.assertIn("nenhuma provisão gasta", o["texto"])
        self.assertEqual(o["ancora"], "servico:dormir")
        g.descansar(bal.TAVERNA_VIDA)  # o descanso da taverna devolve exatamente isso
        self.assertEqual((j.hp, j.rec), (10 + vida, j.max_rec))

    def test_d1_com_fome_nao_promete_tudo(self):
        g = depois_da_despensa()
        j = g.j
        j.hp, j.fome = 10, 1
        o = next(c for c in ab.contextuais(g) if c["id"] == "D1")
        vida = int(j.max_hp * bal.TAVERNA_VIDA * sobrevivencia.FOME_DESCANSO)
        self.assertIn(f"devolve {vida} de vida", o["texto"])
        self.assertIn("Com fome, a vida volta menos.", o["texto"])
        g.descansar(bal.TAVERNA_VIDA)
        self.assertEqual(j.hp, 10 + vida)

    def test_d1_ferimento_diferencia_descanso_e_curandeira(self):
        g = depois_da_despensa()
        ferir(g, "perna")
        o = next(c for c in ab.contextuais(g) if c["id"] == "D1")
        self.assertIn("Descansar ajuda os ferimentos a sararem com o tempo; a Curandeira trata na hora.", o["texto"])

    def test_d2_acampar_fora_da_vila_com_algo_a_recuperar(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        visto(g, "V5")
        g.j.hp = g.j.max_hp
        g.j.rec = g.j.max_rec
        self.assertNotEqual(oid(g), "D2")  # nada a recuperar: não chama para dormir
        g.j.hp -= 10
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("D2", "opcao:Acampar"))

    def test_d3_fogueira_numeros_provisoes_e_mau_tempo(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        j = g.j
        j.hp, j.rec, j.provisoes = 20, 0, 3
        g.na_fogueira = True
        g.clima = "limpo"
        o = ab.atual(g)
        vida, rec = int(j.max_hp * bal.ACAMPAR_VIDA), int(j.max_rec * bal.ACAMPAR_FOLEGO)
        self.assertEqual((o["id"], o["ancora"]), ("D3", "dormir:fogueira"))
        self.assertIn(f"devolve {vida} de vida e {rec} de Vigor; o amanhecer come 1 provisão sua (você tem 3).", o["texto"])
        g.clima = "chuva"
        self.assertIn(f"devolve {int(j.max_hp * bal.ACAMPAR_VIDA_RUIM)} de vida", ab.atual(g)["texto"])
        j.provisoes = 0
        self.assertIn("sem provisão, você acorda com fome", ab.atual(g)["texto"])
        g.descansar(bal.ACAMPAR_VIDA_RUIM, mana=bal.ACAMPAR_MANA, folego=bal.ACAMPAR_FOLEGO)
        self.assertEqual((j.hp, j.rec), (20 + int(j.max_hp * bal.ACAMPAR_VIDA_RUIM), rec))

    def test_desligado_nada_aparece_mas_o_descanso_e_igual(self):
        g = depois_da_despensa(tutorial=False)
        g.j.hp = 10
        self.assertEqual(ab.contextuais(g), [])
        self.assertIsNone(ab.atual(g))


if __name__ == "__main__":
    unittest.main()
