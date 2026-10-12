"""A abertura guiada da campanha (E9, roadmapIDEIAS/18): a caixa "Mostrar tutorial", a despensa da taverna (a mesma
com e sem tutorial), a caneca por conta da casa, Morel previsível sem duplicar nem reabrir o que já se resolveu, as
orientações da primeira luta e do Mural, dispensar e religar, salvar e carregar."""

import json
import random
import tempfile
import unittest

from rpg import abertura, comitiva as cm
from rpg.jogo import Jogo
from rpg.regras import Derrota, FimDeJogo
from rpg.web.estado import estado
from tests.test_missoes import Roteiro


class Jogador(Roteiro):
    """O roteiro pelo texto; na luta, sem roteiro para a vez, ataca o primeiro inimigo."""

    def escolher(self, pergunta, opcoes):
        self.ofertas.append(list(opcoes))
        if self.roteiro and any(o.startswith(self.roteiro[0]) for o in opcoes):
            alvo = self.roteiro.pop(0)
            return next(i for i, o in enumerate(opcoes) if o.startswith(alvo))
        if pergunta in ("Sua ação:", "Alvo:"):
            return 0
        if pergunta == "Habilidades:":
            return 0
        raise FimDeJogo(f"sem roteiro para {pergunta!r}: {opcoes}")


def nova(classe="guerreiro", tutorial=True, roteiro=(), seed=7, pasta=None):
    g = Jogo(Jogador(roteiro), seed=seed, pasta_saves=pasta or tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", classe, "turvo")
    abertura.comecar(g, tutorial)
    return g


def telas(g, n=8):
    """O ciclo principal, n voltas (ou até o roteiro acabar)."""
    for _ in range(n):
        try:
            g.tela()
        except FimDeJogo:
            return


def jogo_sem_orientacao(g):
    """O estado de jogo, sem os campos das orientações (ligado, vistas): o que tem de ser igual com e sem tutorial."""
    mundo = json.loads(json.dumps(g.mundo))
    a = mundo.get("abertura", {})
    for k in ("tutorial",):
        a.pop(k, None)
    return (json.dumps(g.j.para_dict(), sort_keys=True), json.dumps(mundo, sort_keys=True), g.rng.getstate(),
            dict(g.contagem), g.dia, g.periodo, g.j.ouro, g.j.xp, g.j.reputacao)


ROTEIRO = ["Descer à despensa", "Taverna: sentar", "Recusar", "Taverna: uma bebida", "Mural", "Voltar",
           "Examinar a fonte nova"]


class TestCriacao(unittest.TestCase):
    def test_caixa_no_texto_vira_pergunta_e_a_abertura_e_a_mesma(self):
        for resposta, ligado in (("Sim", True), ("Não", False)):
            ui = Jogador(["Guerreiro", "Resgate", resposta])
            ui.perguntar = lambda *a, **k: "Teste"
            g = Jogo(ui, seed=2, pasta_saves=tempfile.mkdtemp())
            self.assertTrue(g.novo_jogo("turvo"))
            self.assertEqual(abertura.estado(g)["despensa"], "nova")
            self.assertEqual(abertura.tutorial(g), ligado)
            self.assertIn(["Sim", "Não"], ui.ofertas)

    def test_caixa_na_tela_grafica(self):
        from rpg.web.ponte import WebUI
        ui = WebUI()
        ui.caixa = {"id": "tutorial", "rotulo": "Mostrar tutorial", "marcada": True, "pergunta": "?"}
        ui.extra_resposta = {"i": 0, "caixa": False}
        self.assertFalse(ui.ler_caixa())
        ui.extra_resposta = {"i": 0}  # sem a caixa na resposta, vale como estava (marcada)
        self.assertTrue(ui.ler_caixa())

    def test_mundo_gerado_e_save_antigo_sem_despensa(self):
        g = Jogo(Jogador(), seed=3, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        self.assertIsNone(abertura.estado(g))
        self.assertFalse(abertura.cena_pendente(g))
        abertura.ligar(g, True)  # a Ajuda liga as orientações num jogo que não tinha
        self.assertTrue(abertura.tutorial(g))
        self.assertNotIn("despensa", abertura.estado(g))


class TestIgualComESemTutorial(unittest.TestCase):
    def test_mesmo_roteiro_mesmo_jogo(self):
        for classe in ("guerreiro", "arqueiro", "mago"):
            resultados = []
            for tutorial in (True, False):
                g = nova(classe, tutorial, ROTEIRO)
                telas(g, 12)
                self.assertEqual((abertura.estado(g)["despensa"], g.contagem.get("morel_na_taverna")), ("feita", 1))
                self.assertIn("V1", abertura.estado(g)["vistas"])  # o roteiro chegou ao Mural
                resultados.append(jogo_sem_orientacao(g))
            self.assertEqual(resultados[0], resultados[1], classe)


class TestDespensa(unittest.TestCase):
    def test_uma_vez_xp_sem_ouro_nem_saque(self):
        g = nova(roteiro=["Descer à despensa"])
        ouro, itens = g.j.ouro, dict(g.j.consumiveis)
        telas(g, 3)
        a = abertura.estado(g)
        self.assertEqual((a["despensa"], a["caneca"]), ("feita", True))
        self.assertEqual(g.j.xp, 12)  # o XP de sempre dos dois ratos
        self.assertEqual(g.j.ouro, ouro)
        self.assertEqual({k: v for k, v in g.j.consumiveis.items() if v}, {k: v for k, v in itens.items() if v})
        self.assertFalse(abertura.cena_pendente(g))
        self.assertFalse([o for o in abertura.opcoes(g) if o[1][1] == "despensa"])

    def test_os_ratos_dizem_o_que_sao(self):
        g = nova()
        rato = abertura._rato(g)
        self.assertTrue(rato.nome.startswith("Rato da despensa"))
        self.assertEqual((rato.habilidades, rato.ouro, rato.nivel), ([], 0, 1))

    def test_agora_nao_deixa_a_acao_na_taverna(self):
        g = nova(roteiro=["Agora não"])
        telas(g, 3)
        self.assertEqual(abertura.estado(g)["despensa"], "adiada")
        acao = next(o for o in abertura.opcoes(g) if o[1][1] == "despensa")
        self.assertEqual(acao[2]["predio"], "taverna")
        g.ui.roteiro = ["Taverna: descer à despensa"]
        telas(g, 2)
        self.assertEqual(abertura.estado(g)["despensa"], "feita")

    def test_fugir_deixa_a_despensa_para_depois(self):
        g = nova(roteiro=["Descer à despensa", "Fugir", "Fugir", "Fugir", "Fugir", "Fugir", "Fugir"])
        g.chance = lambda p: True  # a fuga dá certo
        telas(g, 2)
        self.assertEqual(abertura.estado(g)["despensa"], "adiada")
        self.assertFalse(abertura.caneca(g))

    def test_perder_leva_ao_resgate_e_a_despensa_fica(self):
        g = nova(roteiro=["Descer à despensa"])
        original = abertura._rato

        def rato_bravo(g):  # só para o teste: ratos que derrubam, para ver a derrota passar pelo resgate de sempre
            e = original(g)
            e.atk, e.hp = 500, 500
            return e
        abertura._rato = rato_bravo
        try:
            with self.assertRaises(Derrota):
                for _ in range(4):
                    g.tela()
        finally:
            abertura._rato = original
        self.assertEqual(abertura.estado(g)["despensa"], "adiada")
        g.resgate("combate")  # o modo resgate, como sempre
        self.assertEqual(g.loc["chave"], "vau_do_turvo")
        self.assertTrue([o for o in abertura.opcoes(g) if o[1][1] == "despensa"])
        self.assertFalse(abertura.caneca(g))


class TestMorel(unittest.TestCase):
    def morel_na_taverna(self, g):
        return [o for o in abertura.opcoes(g) if o[1][1] == "morel"]

    def test_sentar_toca_o_evento_uma_vez(self):
        g = nova(roteiro=["Descer à despensa", "Taverna: sentar", "Recusar"])
        telas(g, 6)
        self.assertEqual(g.contagem.get("morel_na_taverna"), 1)
        self.assertFalse(self.morel_na_taverna(g))  # recusou: não reabre aqui (a bebida segue a regra de hoje)
        self.assertFalse(cm.membro(g, "morel"))

    def test_quem_ja_resolveu_morel_nao_ve_a_acao(self):
        casos = {"recrutado": lambda g: (cm.recrutar(g, "morel"), g.contagem.__setitem__("morel_na_taverna", 1)),
                 "rumores": lambda g: g.contagem.__setitem__("morel_na_taverna", 1),
                 "saiu": lambda g: g.marcar("comitiva:morel", "dispensado")}
        for nome, preparar in casos.items():
            g = nova(roteiro=["Descer à despensa"])
            preparar(g)
            telas(g, 3)
            self.assertEqual(abertura.estado(g)["despensa"], "feita", nome)
            self.assertFalse(self.morel_na_taverna(g), nome)
            self.assertFalse(any("Rato é fácil" in d for d in g.ui.ditos), nome)

    def test_adiar_a_despensa_e_achar_morel_pelos_rumores(self):
        g = nova(roteiro=["Agora não"])
        telas(g, 2)
        g.dia = 2
        g.j.ouro = 50
        for ev in ("briga_de_taverna", "queda_de_braco"):  # os outros eventos da taverna em recarga: sai o de Morel
            g.historico[ev] = g.passos
        g.ui.roteiro = ["Recusar"]
        g.ouvir_rumores()  # a regra de hoje: enquanto ele nunca apareceu, a bebida o chama
        self.assertEqual(g.contagem.get("morel_na_taverna"), 1)
        abertura.estado(g)["despensa"] = "feita"
        self.assertFalse(self.morel_na_taverna(g))

    def test_caneca_e_o_servico_uma_vez(self):
        g = nova(roteiro=["Descer à despensa"])
        telas(g, 3)
        ouro = g.j.ouro
        g.chance = lambda p: False  # sem a briga de taverna: um rumor
        g.ouvir_rumores()  # dia 1: a bebida não chama Morel (a regra dele pede o dia 2)
        self.assertEqual(g.j.ouro, ouro)
        self.assertFalse(abertura.caneca(g))
        self.assertEqual(g.contagem.get("morel_na_taverna", 0), 0)
        self.assertTrue(self.morel_na_taverna(g))  # a apresentação continua de pé
        g.ouvir_rumores()
        self.assertEqual(g.j.ouro, ouro - g.preco(3))  # a segunda já é paga


class TestOrientacoes(unittest.TestCase):
    def test_desligado_nao_mostra_nada(self):
        g = nova(tutorial=False)
        g.combate_ativo = object()
        self.assertIsNone(abertura.atual(g))
        self.assertFalse(abertura.para_tela(g)["ligado"])
        g.combate_ativo = None
        self.assertFalse(estado(g)["orientacao"]["ligado"])

    def test_textos_da_luta_pelas_regras_da_classe(self):
        for classe, hab, trecho in (("guerreiro", "Golpe Pesado", "10 de Vigor. **Atacar** não gasta Vigor"),
                                    ("mago", "Bola de Fogo", "14 de Mana. **Atacar** não gasta Mana"),
                                    ("arqueiro", "Tiro Certeiro", "8 de Foco e 1 flecha. **Atacar** também gasta 1 flecha")):
            g = nova(classe)
            g.combate_ativo = object()
            o = abertura.atual(g)
            self.assertEqual(o["passos"]["C1"], "Clique em **Habilidades** (tecla 2).")
            self.assertEqual(o["passos"]["C2"], f"Clique em **{hab}** (tecla 1).")
            self.assertIn(trecho, o["passos"]["C4"][o["hab"]], classe)

    def test_a_luta_com_habilidade_cumpre_e_sem_ela_conta(self):
        g = nova()
        abertura.depois_da_luta(g, False)
        abertura.depois_da_luta(g, False)
        g.combate_ativo = object()
        self.assertIsNone(abertura.atual(g))  # duas lutas sem abrir Habilidades: o quadro para de insistir
        g = nova()
        abertura.depois_da_luta(g, True)
        g.combate_ativo = object()
        self.assertIsNone(abertura.atual(g))
        self.assertIn("combate", abertura.estado(g)["vistas"])

    def test_v1_depois_da_despensa_e_some_com_o_mural(self):
        g = nova(roteiro=["Agora não"])
        self.assertIsNone(abertura.atual(g))  # antes do pedido do taverneiro, nada
        telas(g, 2)
        self.assertEqual(abertura.atual(g)["id"], "V1")
        g.ui.roteiro = ["Voltar"]
        g.mural()
        self.assertIsNone(abertura.atual(g))
        self.assertIn("V1", abertura.estado(g)["vistas"])

    def test_dispensar_e_religar_pela_tela(self):
        from rpg.web.ponte import WebUI
        g = nova()
        ui = WebUI()
        ui.jogo = g
        ui.orientacao("dispensar")
        self.assertFalse(abertura.tutorial(g))
        ui.orientacao("ligar")
        self.assertTrue(abertura.tutorial(g))
        ui.orientacao("qualquer coisa")
        self.assertTrue(abertura.tutorial(g))

    def test_ajuda_lista_o_que_foi_visto(self):
        g = nova()
        self.assertEqual(abertura.ajuda(g)["linhas"], [])
        abertura.depois_da_luta(g, True)
        abertura.visto(g, "V1")
        grupos = [l["grupo"] for l in abertura.ajuda(g)["linhas"]]
        self.assertEqual(grupos, ["Luta", "Luta", "Vila"])
        self.assertIn("gasta 10 de Vigor", abertura.ajuda(g)["linhas"][1]["texto"])


class TestSave(unittest.TestCase):
    def test_salvar_e_carregar_guarda_tudo(self):
        pasta = tempfile.mkdtemp()
        g = nova(roteiro=["Agora não"], pasta=pasta, tutorial=False)
        telas(g, 2)
        abertura.visto(g, "V1")
        g.salvar(silencioso=True)
        h = Jogo.carregar(Jogador(["Taverna: descer à despensa"]), g.caminho_save(), pasta)
        self.assertEqual(abertura.estado(h), abertura.estado(g))
        self.assertFalse(abertura.tutorial(h))
        telas(h, 2)
        self.assertEqual(abertura.estado(h)["despensa"], "feita")
        h.salvar(silencioso=True)
        k = Jogo.carregar(Jogador(), h.caminho_save(), pasta)
        self.assertEqual((abertura.estado(k)["despensa"], abertura.caneca(k)), ("feita", True))


if __name__ == "__main__":
    random.seed(0)
    unittest.main()
