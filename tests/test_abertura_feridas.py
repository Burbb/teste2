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
        self.assertEqual((o["id"], o["ancora"], o["texto"]), ("F4", "tratar:corte", "Clique neste cartão para tratar o corte."))
        ab.contexto(g, None)


class TestDescanso(unittest.TestCase):
    def test_cartao_da_taverna_com_os_numeros_das_regras(self):
        g = depois_da_despensa()
        j = g.j
        j.hp, j.rec = 10, 0
        vida = int(j.max_hp * bal.TAVERNA_VIDA)
        self.assertEqual(g.linhas_descanso("taverna"), [
            {"icone": "coracao", "rotulo": "Recuperação", "texto": f"+{vida} vida · Vigor completo"},
            {"icone": "pernil", "rotulo": "Provisões", "texto": "nenhuma consumida"}])
        g.descansar(bal.TAVERNA_VIDA)  # o descanso da taverna devolve exatamente isso
        self.assertEqual((j.hp, j.rec), (10 + vida, j.max_rec))

    def test_vida_cheia_sem_mais_zero(self):
        g = depois_da_despensa("mago")
        g.j.rec = 0
        self.assertEqual(g.linhas_descanso("taverna")[0]["texto"], "Mana completa")
        g.j.rec = g.j.max_rec
        self.assertEqual(g.linhas_descanso("taverna")[0]["texto"], "Mana completa")

    def test_fome_so_quando_reduz(self):
        g = depois_da_despensa()
        j = g.j
        j.hp, j.fome = 10, 1
        vida = int(j.max_hp * bal.TAVERNA_VIDA * sobrevivencia.FOME_DESCANSO)
        linhas = g.linhas_descanso("taverna")
        self.assertEqual(linhas[0]["texto"], f"+{vida} vida · Vigor completo")
        self.assertIn({"nota": "Recuperação de vida reduzida pela fome."}, linhas)
        g.descansar(bal.TAVERNA_VIDA)
        self.assertEqual(j.hp, 10 + vida)
        j.hp = j.max_hp  # com a vida cheia, a fome não reduz nada: sem nota
        self.assertNotIn({"nota": "Recuperação de vida reduzida pela fome."}, g.linhas_descanso("taverna"))

    def test_nunca_zero_com_vida_faltando(self):
        # A conta da taverna e da fogueira, com fome e com mau tempo, nas três classes e no nível 1: sempre volta vida.
        for classe in ("guerreiro", "arqueiro", "mago"):
            g = depois_da_despensa(classe)
            g.j.fome = 2
            g.clima = "tempestade"
            for fracao in (bal.TAVERNA_VIDA, bal.ACAMPAR_VIDA_RUIM):
                g.j.hp = 1
                self.assertGreater(g.previsao_descanso(fracao, 0.5)[0], 0, (classe, fracao))

    def test_ferimentos_saram_quando_ha_comida(self):
        # No amanhecer a comida vem antes dos ferimentos: a taverna serve o ensopado e a fogueira gasta uma provisão;
        # só quem fica sem comer não sara.
        g = depois_da_despensa()
        g.j.fome = 1
        ferir(g, "perna")
        sara = {"nota": "Ferimentos: o descanso ajuda a sarar com o tempo."}
        self.assertIn(sara, g.linhas_descanso("taverna"))
        self.assertIn(sara, g.linhas_descanso("fogueira"))
        g.j.provisoes = 0
        self.assertIn({"nota": "Ferimentos: sem comer, não saram esta noite."}, g.linhas_descanso("fogueira"))
        dias = g.j.ferimentos[0]["dias"]
        g.novo_dia(descanso=1)
        self.assertEqual(g.j.ferimentos[0]["dias"], dias)  # de fato, não sarou

    def test_d1_so_a_acao_no_quadro(self):
        g = depois_da_despensa()
        g.j.hp = 10
        o = next(c for c in ab.contextuais(g) if c["id"] == "D1")
        self.assertEqual((o["texto"], o["ancora"]), ("Clique neste cartão para dormir aqui até o amanhecer.", "servico:dormir"))
        ferir(g, "perna")
        o = next(c for c in ab.contextuais(g) if c["id"] == "D1")
        self.assertIn("_A Curandeira trata ferimentos na hora.", o["texto"])

    def test_d2_acampar_fora_da_vila_com_algo_a_recuperar(self):
        g = depois_da_despensa("arqueiro")
        ir(g, "charco_dos_juncos")
        visto(g, "V5")
        g.j.hp = g.j.max_hp
        g.j.rec = g.j.max_rec
        self.assertNotEqual(oid(g), "D2")  # nada a recuperar: não chama para dormir
        g.j.hp -= 10
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("D2", "opcao:Acampar"))
        self.assertEqual(o["texto"], "Acampe para montar uma fogueira. Lá, você pode dormir para recuperar vida e Foco.")

    def test_d3_fogueira_linhas_provisoes_e_mau_tempo(self):
        from rpg import comitiva as cm
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        j = g.j
        j.hp, j.rec, j.provisoes = 20, 0, 3
        g.na_fogueira = True
        g.clima = "limpo"
        o = ab.atual(g)
        vida, rec = int(j.max_hp * bal.ACAMPAR_VIDA), int(j.max_rec * bal.ACAMPAR_FOLEGO)
        self.assertEqual((o["id"], o["ancora"]), ("D3", "dormir:fogueira"))
        self.assertEqual(o["texto"], f"**Dormir até o amanhecer**\nRecuperação: +{vida} vida · +{rec} Vigor\n"
                                     "Provisões: 1 consumida · restam 2")
        g.clima = "chuva"
        self.assertIn(f"+{int(j.max_hp * bal.ACAMPAR_VIDA_RUIM)} vida", ab.atual(g)["texto"])
        self.assertIn("_Recuperação de vida reduzida pelo mau tempo.", ab.atual(g)["texto"])
        cm.recrutar(g, "morel")
        cm.recrutar(g, "odete")
        self.assertIn("Provisões: 3 consumidas (você e 2 companheiros) · restam 0", ab.atual(g)["texto"])
        j.provisoes = 2
        self.assertIn("Provisões: 2 consumidas: não dão para todos", ab.atual(g)["texto"])
        j.provisoes = 0
        self.assertIn("Provisões: nenhuma: todos acordam com fome", ab.atual(g)["texto"])
        g.descansar(bal.ACAMPAR_VIDA_RUIM, mana=bal.ACAMPAR_MANA, folego=bal.ACAMPAR_FOLEGO)
        self.assertEqual((j.hp, j.rec), (20 + int(j.max_hp * bal.ACAMPAR_VIDA_RUIM), rec))

    def test_desligado_nada_aparece_mas_o_descanso_e_igual(self):
        g = depois_da_despensa(tutorial=False)
        g.j.hp = 10
        self.assertEqual(ab.contextuais(g), [])
        self.assertIsNone(ab.atual(g))


if __name__ == "__main__":
    unittest.main()
