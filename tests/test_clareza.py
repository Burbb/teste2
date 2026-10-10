"""A clareza da campanha (1.60): as correntes como uma ação só (o como é escolhido dentro, e voltar não gasta nada), o
frasco do lodo dizendo para que serve, o Diário na ordem de quem volta ao jogo (objetivo, o mais recente, caminhos,
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
        for classe in ("guerreiro", "mago", "arqueiro"):
            g = na_capela(classe, etapa="fundo")
            lutas(g)
            rotulos = [o[0] for o in missoes.opcoes(g) if o[1][1] == MID]
            self.assertEqual(len([r for r in rotulos if "correntes" in r.lower()]), 1)
            fazer(g, "correntes", "Voltar")
            metodos = g.ui.ofertas[-1]
            self.assertTrue(metodos[0].startswith("À mão"))
            self.assertIn("afogados", metodos[0])  # o custo e o risco do jeito manual
            self.assertTrue(metodos[1].startswith(missoes.METODO_CLASSE[classe][:12]))
            self.assertIn("Se falhar", metodos[1])  # o risco do atalho
            self.assertTrue(metodos[2].startswith("Voltar"))

    def test_abrir_e_voltar_nao_gasta_nada(self):
        """Abrir a escolha e voltar não muda a missão, a bolsa, as flechas, a hora nem o sorteio; não há Continuar nem
        cartão de missão."""
        for classe in ("guerreiro", "mago", "arqueiro"):
            ui = Anotador()
            g = na_capela(classe, ui=ui, etapa="fundo")
            vistas = lutas(g)
            antes, continuares = foto(g), len(ui.continuares)
            self.assertTrue(fazer(g, "correntes", "Voltar"))
            self.assertEqual(foto(g), antes)
            self.assertEqual((len(ui.continuares), ui.cartoes, vistas), (continuares, [], []))
            self.assertIn("correntes", [o[1][2] for o in missoes.opcoes(g)])  # a ação continua lá

    def test_os_dois_metodos_deixam_o_mesmo_preparo(self):
        for como in ("À mão", "Arrancar"):
            ui = Anotador()
            g = na_capela(ui=ui, etapa="fundo")
            lutas(g, "vitoria")
            g.teste = lambda a, cd: True
            fazer(g, "correntes", como)
            self.assertEqual(missoes.registro(g, MID)["preparos"], ["corpo_solto"])
            self.assertEqual([c["itens"] for c in ui.cartoes[-1]], [[missoes.titulo(MID, "corpo_solto")]])


class TestLodo(unittest.TestCase):
    def test_o_frasco_diz_para_que_serve_so_quando_se_sabe(self):
        g = na_capela(etapa="fundo")
        rotulo = lambda: next(o[0] for o in missoes.opcoes(g) if o[1][1] == CASPAR)  # noqa: E731
        self.assertNotIn("Caspar", rotulo())  # antes da acusação, ainda não se conhece Caspar
        self.assertIn("prova", rotulo())
        caspar.registro(g)["etapa"] = "acusacao"
        self.assertIn("prova para a decisão sobre Caspar", rotulo())


class TestDiario(unittest.TestCase):
    def test_vigilia_aguardando_a_febre(self):
        g = investigando()
        missoes.cena_pendente(g)  # a acusação
        cartao = next(c for c in missoes.cartoes(g, todas=True) if c["id"] == CASPAR)
        self.assertIn("Aguardando", cartao["aguardando"])
        self.assertIn("febre", cartao["aguardando"])
        missoes.registro(g, MID)["desfecho"] = "destruida"
        caspar.sincronizar(g)
        cartao = next(c for c in missoes.cartoes(g, todas=True) if c["id"] == CASPAR)
        self.assertIsNone(cartao["aguardando"])

    def test_rito_como_caminho_opcional(self):
        g = investigando()
        req = missoes.cartoes(g)[0]["requisitos"]
        self.assertTrue(req["opcional"])
        self.assertIn("opcional", req["titulo"])
        self.assertIn("dois caminhos", req["titulo"])

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
        self.assertTrue(rotulos[0].startswith("Soltar as correntes"))
        self.assertTrue(rotulos[1].startswith("Descer ao fundo alagado"))
        self.assertTrue(rotulos[2].startswith("Recolher um frasco do lodo"))

if __name__ == "__main__":
    unittest.main()
