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
        self.assertEqual(o["texto"], "**Costelas quebradas**\n−25% de Defesa e −15% de Vigor máximo.\n"
                                     "Sara com descanso ou na Curandeira.")
        self.assertNotIn("bandagem", o["texto"].lower())  # fratura: a bandagem não trata

    def test_f1_corte_com_os_numeros_reais(self):
        g = depois_da_despensa("mago")
        ferir(g, "corte")
        self.assertEqual(ab.atual(g)["texto"], "**Corte profundo**\n−10% de vida máxima.\n"
                                               "Sara com descanso ou na Curandeira.")
        g = depois_da_despensa("mago")
        ferir(g, "concussao")
        self.assertIn("−25% de Poder e −15% de Mana máxima.", ab.atual(g)["texto"])

    def test_f1_infeccao_nao_passa_sozinha(self):
        g = depois_da_despensa()
        ferir(g, "infeccao")
        texto = ab.atual(g)["texto"]
        self.assertIn("Não sara com descanso: use unguento ou vá à Curandeira.", texto)
        self.assertNotIn("Precisa de descanso", texto)  # nada de prometer que o descanso cura

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
        self.assertEqual(g.o_que_trata("bandagem"), {"trata": "Enfaixa: mordida dilacerada."})  # sem prometer as duas
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

    def test_tratar_nao_tira_da_cabana(self):
        """Depois de cada tratamento a cabana continua aberta, com o ouro e os ferimentos de agora; tratado o último,
        quem atende diz que não há mais nada, fica só o Voltar, e é quem joga que sai. Nenhuma cobrança a mais."""
        g = depois_da_despensa(roteiro=[])
        g.marcar("curandeira_gratis_usado")
        ferir(g, "corte", "costelas")
        g.j.ouro = 200
        preco = sum(ab.custo_tratamento(g, {"id": f}) for f in ("corte", "costelas"))
        paineis, efeitos = [], []
        g.ui.painel = lambda tipo, dados: paineis.append(dados) or True
        g.ui.efeito = lambda texto, tipo="info", item=None: efeitos.append(texto)
        ofertas = []

        def menu(_, opcoes):
            ofertas.append([o[0] for o in opcoes])
            return next((o[1] for o in opcoes if o[0].startswith("Tratar")), None)  # trata o que houver; senão, Voltar
        g.menu = menu
        g.curandeiro()
        self.assertEqual(ofertas, [["Tratar Corte profundo", "Tratar Costelas quebradas", "Voltar"],
                                   ["Tratar Costelas quebradas", "Voltar"], ["Voltar"]])
        self.assertEqual([len(d["ferimentos"]) for d in paineis], [2, 1, 0])
        self.assertEqual([d["ouro"] for d in paineis][1:], [200 - ab.custo_tratamento(g, {"id": "corte"}), 200 - preco])
        self.assertEqual(paineis[-1]["fala"], '"Pronto. Por aqui, terminamos."')  # a Pita, no Vau: tratou e terminou
        self.assertEqual((g.j.ferimentos, g.j.ouro), ([], 200 - preco))
        # o resultado de cada um numa confirmação curta, com o custo à parte (o "−N ouro" de sempre)
        self.assertEqual([e for e in efeitos if "tratado" in e], ["Corte profundo: tratado", "Costelas quebradas: tratado"])
        self.assertEqual(len([e for e in efeitos if e.endswith(" ouro")]), 2)

    def test_sem_ouro_nao_trata_nem_sai(self):
        g = depois_da_despensa(roteiro=[])
        g.marcar("curandeira_gratis_usado")
        ferir(g, "corte")
        g.j.ouro = 0
        respostas = iter([("corte", ab.custo_tratamento(g, {"id": "corte"})), None])
        g.menu = lambda _, opcoes: next(respostas)
        g.curandeiro()
        self.assertEqual(([f["id"] for f in g.j.ferimentos], g.j.ouro), (["corte"], 0))

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


class TestSoOQueDaParaPagar(unittest.TestCase):
    """Os quadros que mandam usar um serviço pago (D1, F3, F4, V2) só aparecem quando ele dá para usar agora. Sem ouro,
    o cartão e o "Ouro insuficiente" continuam; o quadro fica pendente (não conta como visto) e volta quando der, sem
    segurar os outros. O grátis continua sendo mostrado."""

    def test_d1_sem_ouro_espera_e_volta_com_ouro(self):
        g = depois_da_despensa()
        g.j.hp = 10
        g.j.ouro = ab.preco_dormir(g) - 1
        self.assertFalse([c for c in ab.contextuais(g) if c["id"] == "D1"])
        self.assertNotIn("D1", g.mundo["abertura"]["vistas"])  # pendente
        g.j.ouro = ab.preco_dormir(g)
        self.assertTrue([c for c in ab.contextuais(g) if c["id"] == "D1"])

    def test_d1_sem_ouro_nao_segura_as_outras(self):
        g = depois_da_despensa()
        g.j.ouro = 0
        ferir(g, "perna")
        self.assertEqual(oid(g), "F1")  # a fila segue: o D1 é da taverna aberta e, sem ouro, nem entra

    def test_f3_sem_ouro_espera_e_o_gratis_continua(self):
        g = depois_da_despensa()
        ferir(g, "perna")
        visto(g, "F1")
        g.marcar("curandeira_gratis_usado")
        g.j.ouro = 0
        self.assertNotEqual(oid(g), "F3")
        self.assertNotIn("F3", g.mundo["abertura"]["vistas"])
        g.j.ouro = 999
        self.assertEqual(oid(g), "F3")
        h = depois_da_despensa()  # com o primeiro tratamento grátis, sem ouro nenhum: aparece, e diz que é grátis
        ferir(h, "perna")
        visto(h, "F1")
        h.j.ouro = 0
        self.assertTrue(ab.atual(h)["texto"].endswith("O primeiro tratamento é grátis."))

    def test_f4_aponta_o_que_da_para_pagar_e_sem_nenhum_nao_conta_como_visto(self):
        g = depois_da_despensa(roteiro=["Voltar"])
        ferir(g, "infeccao", "corte")
        visto(g, "F1", "F2", "F3")
        g.marcar("curandeira_gratis_usado")
        g.j.ouro = ab.custo_tratamento(g, {"id": "corte"})  # dá para o corte, não para a infecção (mais cara)
        ab.contexto(g, "curandeira")
        self.assertEqual(ab.atual(g)["ancora"], "tratar:corte")
        g.j.ouro = 0
        self.assertIsNone(ab.atual(g))
        ab.contexto(g, None)
        g.curandeiro()  # entrou e saiu sem ouro: o quadro nem apareceu, então não passa
        self.assertNotIn("F4", g.mundo["abertura"]["vistas"])
        g.j.ouro = 999
        g.ui.roteiro = ["Voltar"]
        g.curandeiro()  # com ouro, o quadro aparece; sair passa a ocasião, como antes
        self.assertIn("F4", g.mundo["abertura"]["vistas"])

    def test_v2_segue_a_regra_dos_cartoes(self):
        g = depois_da_despensa()
        g.j.hp = int(g.j.max_hp * 0.4)
        g.marcar("templo_gratis_usado")
        g.j.ouro = 0
        self.assertNotEqual(oid(g), "V2")
        self.assertNotIn("V2", g.mundo["abertura"]["vistas"])
        g.j.ouro = ab.preco_dormir(g)
        self.assertEqual((ab.atual(g)["id"], ab.atual(g)["ancora"]), ("V2", "predio:taverna"))
