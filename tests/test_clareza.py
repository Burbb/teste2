"""A clareza da campanha (1.60, revista na 1.60.1): as correntes como uma ação só, de rótulos curtos (o como é escolhido
dentro, com custo e risco na nota, e deixar como está não gasta nada), o rito só depois de Vó Berta, a amostra do lodo
com a finalidade no Diário, o Diário na ordem de quem volta ao jogo (objetivo, o mais recente, caminhos,
histórico), a Vigília de Caspar aguardando a febre e o cartão de atualização de missão (um por cena, com o dia no
histórico, sem repetir ao carregar um save e sem datas inventadas em saves antigos)."""

import json
import tempfile
import unittest

from rpg import caspar, missoes
from rpg.jogo import Jogo
from rpg.web.estado import estado
from tests.test_caspar import investigando
from tests.test_missoes import MID, Roteiro, fazer, lutas, na_capela

CASPAR = caspar.MID


class Anotador(Roteiro):
    """O Roteiro, guardando os cartões de missão em vez de escrevê-los."""

    def __init__(self, roteiro=()):
        super().__init__(roteiro)
        self.cartoes = []

    def missao_atualizada(self, cartoes):
        self.cartoes.append(cartoes)


def foto(g):
    return (json.dumps(g.mundo["missoes"], sort_keys=True), json.dumps(g.j.consumiveis, sort_keys=True), g.j.flechas,
            g.j.hp, g.periodo, g.dia, g.rng.getstate())


class TestCorrentes(unittest.TestCase):
    def test_uma_acao_so_e_os_metodos_dentro(self):
        """Rótulos curtos e fáceis de comparar; o custo e o risco ficam na nota de cada um, antes da escolha."""
        for classe in ("guerreiro", "mago", "arqueiro"):
            g = na_capela(classe, etapa="fundo")
            lutas(g)
            rotulos = [o[0] for o in missoes.opcoes(g)]
            self.assertEqual(rotulos[:3], ["Soltar as correntes", "Descer ao fundo alagado", "Recolher uma amostra do lodo"])
            fazer(g, "correntes", "Deixar")
            metodos = g.ui.ofertas[-1]  # no modo texto, a nota vem junto, depois do travessão
            principais = [m.split(" — ")[0] for m in metodos]
            self.assertEqual(principais[0], "Desenrolar as correntes à mão")
            self.assertTrue(principais[1].startswith(missoes.METODO_CLASSE[classe].split(" (")[0]))
            self.assertRegex(principais[1], r"\((Força|Arcano|Destreza) [+-]\d+ no d20\)")
            self.assertEqual(principais[2], "Deixar como está")
            self.assertIn("afogados", metodos[0])  # o risco do jeito manual
            self.assertNotIn("sempre funciona", metodos[0].lower())
            self.assertIn("Se falhar", metodos[1])  # o risco do atalho
            self.assertEqual("Gasta 1 flecha" in metodos[1], classe == "arqueiro")  # o consumo, à vista

    def test_a_cena_nao_ensina_o_rito_antes_de_berta(self):
        g = na_capela(etapa="fundo")
        fazer(g, "correntes", "Deixar")
        texto = " ".join(g.ui.ditos)
        self.assertIn("trava de ferro", texto)
        self.assertNotIn("descanso", texto)
        self.assertNotIn("preparo", texto)
        g = na_capela(etapa="fundo")
        missoes.registro(g, MID)["pistas"] += ["ilse", "verdade_de_ilse", "nome_e_fita"]
        fazer(g, "correntes", "Deixar")
        self.assertIn("Vó Berta disse que um afogado descansa", " ".join(g.ui.ditos))

    def test_abrir_e_deixar_nao_gasta_nada(self):
        """Abrir a escolha e deixar como está não muda a missão, a bolsa, as flechas, a hora nem o sorteio; não há
        Continuar nem cartão de missão."""
        for classe in ("guerreiro", "mago", "arqueiro"):
            ui = Anotador()
            g = na_capela(classe, ui=ui, etapa="fundo")
            vistas = lutas(g)
            antes, continuares = foto(g), len(ui.continuares)
            self.assertTrue(fazer(g, "correntes", "Deixar"))
            self.assertEqual(foto(g), antes)
            self.assertEqual((len(ui.continuares), ui.cartoes, vistas), (continuares, [], []))
            self.assertIn("correntes", [o[1][2] for o in missoes.opcoes(g)])  # a ação continua lá

    def test_os_metodos_deixam_o_mesmo_preparo(self):
        for classe in ("guerreiro", "mago", "arqueiro"):
            for como in ("Desenrolar", missoes.METODO_CLASSE[classe].split(" (")[0]):
                ui = Anotador()
                g = na_capela(classe, ui=ui, etapa="fundo")
                lutas(g, "vitoria")
                g.teste = lambda a, cd: True
                fazer(g, "correntes", como)
                self.assertEqual(missoes.registro(g, MID)["preparos"], ["corpo_solto"])
                self.assertEqual([c["itens"] for c in ui.cartoes[-1]], [["As correntes estão soltas"]])
                self.assertEqual([c["objetivo"] for c in ui.cartoes[-1]], [None])  # o objetivo não mudou


class TestLodo(unittest.TestCase):
    def test_a_amostra_tem_rotulo_curto_e_a_finalidade_no_diario(self):
        g = na_capela(etapa="fundo")
        self.assertIn("Recolher uma amostra do lodo", [o[0] for o in missoes.opcoes(g)])
        caspar.registro(g)["etapa"] = "acusacao"
        req = next(c for c in missoes.cartoes(g) if c["id"] == CASPAR)["requisitos"]
        self.assertIn("praça", req["titulo"])
        self.assertIn("lodo", req["itens"][1]["texto"])
        self.assertTrue(all(i["onde"] is None for i in req["itens"]))


class TestDiario(unittest.TestCase):
    def test_vigilia_aguardando_a_febre(self):
        g = investigando()
        missoes.cena_pendente(g)  # a acusação
        cartao = next(c for c in missoes.cartoes(g, todas=True) if c["id"] == CASPAR)
        self.assertIn("Aguardando o fim da febre", cartao["aguardando"])
        self.assertNotIn("(", cartao["aguardando"])
        missoes.registro(g, MID)["desfecho"] = "destruida"
        caspar.sincronizar(g)
        cartao = next(c for c in missoes.cartoes(g, todas=True) if c["id"] == CASPAR)
        self.assertIsNone(cartao["aguardando"])

    def test_o_rito_so_depois_de_berta_e_atribuido_a_ela(self):
        g = na_capela(etapa="fundo")
        m = missoes.registro(g, MID)
        m["pistas"] += ["agua_da_capela", "ilse", "sigilo_do_turvo", "marcados", "correntes"]
        c = missoes.cartoes(g)[0]
        self.assertIsNone(c["requisitos"])  # antes de Berta: sem receita
        self.assertEqual(len(c["perguntas"]), 3)  # a noite do afogamento, as correntes, os homens marcados
        self.assertTrue(all("Berta" not in q and "fita" not in q for q in c["perguntas"]))
        m["pistas"] += ["verdade_de_ilse", "nome_e_fita"]
        m["preparos"] += ["fita"]
        c = missoes.cartoes(g)[0]
        self.assertIn("Vó Berta contou", c["requisitos"]["titulo"])
        self.assertEqual([i["feito"] for i in c["requisitos"]["itens"]], [True, True, False])
        self.assertEqual(c["requisitos"]["itens"][2]["onde"], "as correntes do sarilho, no ossuário")
        self.assertEqual(len(c["perguntas"]), 1)  # sobram os homens marcados
        m["preparos"] += ["corpo_solto"]
        self.assertTrue(missoes.descanso_pronto(m))
        self.assertTrue(missoes.cartoes(g)[0]["requisitos"]["itens"][2]["feito"])

    def test_preparo_feito_antes_de_berta_continua_marcado(self):
        ui = Roteiro(["Fechar"])
        g = na_capela(ui=ui, etapa="fundo")
        missoes.registro(g, MID)["preparos"] += ["corpo_solto"]
        c = missoes.cartoes(g)[0]
        self.assertIsNone(c["requisitos"])
        self.assertEqual(c["preparos"], [missoes.MISSOES[MID]["preparos"]["corpo_solto"]])  # "O que você já fez"
        g.diario()
        self.assertIn("O que você já fez:", " ".join(ui.ditos))

    def test_historico_com_dia_e_o_mais_recente(self):
        ui = Anotador(["Examinar a Fonte Nova"])
        g = Jogo(ui, seed=5, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro", "turvo")
        g.tela()  # abertura
        g.dia = 3
        g.tela()  # examinar a fonte
        m = missoes.cartoes(g)[0]
        self.assertEqual(m["recente"], {"dia": 3, "texto": missoes.MISSOES[MID]["pistas"]["agua_do_leste"]})
        self.assertEqual([e["dia"] for e in m["historico"]], [1, 3])
        self.assertEqual(m["historico"][0]["itens"][0], "A missão começou.")

    def test_save_antigo_sem_datas_inventadas(self):
        """Um save de antes do histórico: o que já se sabia aparece, sem dia; nada de cronologia nova."""
        pasta = tempfile.mkdtemp()
        g = na_capela(pasta=pasta)
        for m in g.mundo["missoes"].values():
            m.pop("historico", None)
        g.salvar(silencioso=True)
        ui = Anotador(["Fechar"])
        h = Jogo.carregar(ui, g.caminho_save(), pasta)
        m = missoes.cartoes(h)[0]
        self.assertEqual(m["historico"], [{"dia": None, "itens": [missoes.MISSOES[MID]["pistas"][p] for p in
                                                                   ("agua_do_leste", "represa", "canal_da_capela")]}])
        self.assertIsNone(m["recente"]["dia"])
        h.diario()
        texto = " ".join(ui.ditos)
        self.assertIn("sem data", texto)
        self.assertNotIn("Dia 1:", texto)
        self.assertEqual(ui.paineis[-1][1]["missoes"], estado(h)["missoes"])


class TestCartao(unittest.TestCase):
    def test_um_cartao_por_cena_com_o_objetivo_novo(self):
        ui = Anotador()
        g = na_capela(ui=ui)
        lutas(g, "vitoria")
        fazer(g, "nave")
        self.assertEqual(len(ui.cartoes), 1)
        [c] = ui.cartoes[0]
        self.assertEqual(c["itens"], [missoes.titulo(MID, "agua_da_capela")])
        self.assertEqual(c["objetivo"], missoes.MISSOES[MID]["etapas"]["sacristia"]["objetivo"])
        self.assertEqual(missoes.registro(g, MID)["historico"][-1]["dia"], g.dia)

    def test_varias_pistas_da_mesma_cena_num_cartao(self):
        ui = Anotador()
        g = na_capela(ui=ui, etapa="sacristia")
        lutas(g, "vitoria")
        fazer(g, "sacristia")
        self.assertEqual(len(ui.cartoes), 1)
        self.assertGreater(len(ui.cartoes[0][0]["itens"]), 1)

    def test_fuga_nao_gera_cartao(self):
        ui = Anotador()
        g = na_capela(ui=ui)
        lutas(g, "fuga")
        fazer(g, "nave")
        self.assertEqual(ui.cartoes, [])

    def test_carregar_nao_repete(self):
        pasta = tempfile.mkdtemp()
        ui = Anotador()
        g = na_capela(ui=ui, pasta=pasta)
        lutas(g, "vitoria")
        fazer(g, "nave")
        g.salvar(silencioso=True)
        k = Anotador(["Fechar"])
        h = Jogo.carregar(k, g.caminho_save(), pasta)
        self.assertFalse(missoes.cena_pendente(h))
        h.diario()
        self.assertEqual(k.cartoes, [])
        self.assertEqual(missoes.registro(h, MID)["historico"], missoes.registro(g, MID)["historico"])

    def test_texto_do_cartao_no_modo_texto(self):
        g = na_capela()
        lutas(g, "vitoria")
        fazer(g, "nave")
        texto = " ".join(g.ui.ditos)
        self.assertIn("◆ Diário: A Febre do Turvo", texto)
        self.assertIn("Objetivo: " + missoes.MISSOES[MID]["etapas"]["sacristia"]["objetivo"], texto)

    def test_menu_da_capela_poe_a_missao_primeiro(self):
        """No menu do lugar, as ações da missão vêm antes dos contratos e do resto, marcadas para a tela."""
        g = na_capela(etapa="fundo")

        class Parar(Exception):
            pass

        def escolher(pergunta, opcoes):
            g.ui.ofertas.append(list(opcoes))
            raise Parar()
        g.ui.escolher = escolher
        with self.assertRaises(Parar):
            g.tela()
        rotulos = g.ui.ofertas[-1]
        self.assertEqual(rotulos[:3], ["Soltar as correntes", "Descer ao fundo alagado", "Recolher uma amostra do lodo"])

if __name__ == "__main__":
    unittest.main()
