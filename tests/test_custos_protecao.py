"""Custos de consumíveis, a proteção que levanta uma vez e o fluxo da exaustão (1.61.0).

A opção que gasta um item diz qual e quanto antes da escolha; sem o item, ela continua à vista, indisponível, com o
motivo, e nem a tela nem o robô a escolhem. A proteção (a flag `bencao_fenix`) guarda a origem, avisa quando chega e
aparece na luta quando levanta você; um save de antes, sem origem, tem frase neutra. A faixa "Exausto" não pede um
Continuar a mais nem passa por cima do texto do evento anterior."""

import random
import tempfile
import unittest

from rpg import comitiva as cm
from rpg.combate import Combate
from rpg.combate.luta import ORIGEM_PROTECAO
from rpg.eventos import classe as ev_classe, comitiva as ev_comitiva, comuns as ev_comuns, vila as ev_vila
from rpg.jogo import Jogo
from rpg.ui import BotUI
from rpg.web.ponte import WebUI
from tests.test_missoes import Roteiro


class Anotador(Roteiro):
    """Escolhe pelo texto; guarda as metas das opções, os efeitos, os lances e as cenas e festas na ordem."""

    def __init__(self, roteiro=()):
        super().__init__(roteiro)
        self.metas, self.efeitos, self.lances, self.ordem = [], [], [], []

    def escolher(self, pergunta, opcoes):
        self.metas.append(self.meta_opcoes)
        return super().escolher(pergunta, opcoes)

    def efeito(self, texto, tipo="info", item=None):
        self.efeitos.append((texto, tipo))

    def lance(self, tipo, **dados):
        self.lances.append((tipo, dados))

    def cena(self, titulo, subtitulo=None, tipo="evento"):
        self.ordem.append(("cena", titulo))
        super().cena(titulo, subtitulo, tipo)

    def celebrar(self, tipo, dados):
        self.ordem.append(("celebrar", tipo))


def jogo(ui=None, classe="guerreiro", **bolsa):
    g = Jogo(ui or Anotador(), seed=3, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", classe)
    g.j.consumiveis.update(bolsa)
    return g


class TestCustoDosItens(unittest.TestCase):
    def test_bandagem_da_odette_diz_o_custo_e_gasta_uma(self):
        ui = Anotador(["Estancar o sangue", "Recusar", "Não"])
        g = jogo(ui, bandagem=3)
        ev_comitiva.odete_na_estrada(g)
        meta = ui.metas[0][0]
        self.assertEqual(meta["nota"], "Usa 1 bandagem da bolsa (você tem 3).")
        self.assertIn("Usa 1 bandagem da bolsa (você tem 3).", ui.ofertas[0][0])  # no texto, a nota vem junto
        self.assertEqual(g.j.consumiveis["bandagem"], 2)  # exatamente uma

    def test_sem_bandagem_a_opcao_fica_indisponivel_e_nao_se_escolhe(self):
        ui = Anotador(["Estancar o sangue", "Seguir seu caminho"])  # tenta a indisponível, depois segue
        g = jogo(ui, bandagem=0)
        ev_comitiva.odete_na_estrada(g)
        self.assertEqual(ui.ofertas[0][0], "Estancar o sangue com uma bandagem — indisponível: Você não tem "
                                           "bandagem na bolsa.")
        self.assertEqual(ui.metas[0][0]["indisponivel"], "Você não tem bandagem na bolsa.")
        self.assertIn("Você não tem bandagem na bolsa.", ui.ditos)  # o motivo, e a pergunta de novo
        self.assertEqual(len(ui.ofertas), 2)
        self.assertEqual(g.j.consumiveis["bandagem"], 0)
        self.assertEqual(g.flag("comitiva:odete"), "recusou")  # seguiu o caminho: o resto do encontro igual

    def test_os_outros_caminhos_da_odette_continuam(self):
        for bandagens in (0, 2):
            ui = Anotador(["Perguntar quem ela é", "Seguir seu caminho"])
            g = jogo(ui, bandagem=bandagens)
            ev_comitiva.odete_na_estrada(g)
            self.assertIn("Irmã Odette", " ".join(ui.ditos))
            self.assertEqual(g.j.consumiveis["bandagem"], bandagens)


class TestPerguntarAOdette(unittest.TestCase):
    """Perguntar o nome não resolve o encontro: ela responde e as ações voltam, sem a pergunta."""

    def rodar(self, roteiro, **bolsa):
        ui = Anotador(roteiro)
        g = jogo(ui, **bolsa)
        g.comitiva.clear()
        ev_comitiva.odete_na_estrada(g)
        return ui, g

    def estado(self, g):
        return (g.rng.getstate(), g.dia, g.periodo, g.j.reputacao, g.j.ouro, dict(g.j.consumiveis))

    def test_perguntar_nao_muda_nada(self):
        class Para(Exception):
            pass

        class AteOSegundoMenu(Anotador):  # pergunta e para quando as ações voltam, para conferir o estado ali
            def escolher(self, pergunta, opcoes):
                if self.ofertas:
                    self.ofertas.append(list(opcoes))
                    raise Para
                return super().escolher(pergunta, opcoes)
        ui = AteOSegundoMenu(["Perguntar quem ela é"])
        g = jogo(ui, bandagem=1)
        antes = self.estado(g)
        with self.assertRaises(Para):
            ev_comitiva.odete_na_estrada(g)
        self.assertEqual(self.estado(g), antes)  # nem sorteio, nem tempo, nem reputação, nem ouro, nem item
        self.assertIsNone(g.flag("comitiva:odete"))  # o encontro segue aberto
        self.assertEqual(len(ui.ofertas[1]), 4)

    def test_perguntar_depois_bandagem(self):
        ui, g = self.rodar(["Perguntar quem ela é", "Estancar o sangue", "Aceitar"], bandagem=2)
        self.assertEqual(len(ui.ofertas[0]), 5)
        self.assertEqual(len(ui.ofertas[1]), 4)  # a pergunta sai; o resto fica
        self.assertFalse(any("Perguntar" in o for o in ui.ofertas[1]))
        self.assertTrue(any("Estancar" in o for o in ui.ofertas[1]))
        texto = " ".join(ui.ditos)
        self.assertEqual(texto.count("Irmã Odette"), 1)  # a apresentação, uma vez
        self.assertIn("Ele ainda respira", texto)
        self.assertNotIn("Não dá mais para salvar", texto)
        self.assertIn("Você vai para onde está a dor", texto)  # a oferta acompanha a ajuda
        self.assertEqual(g.j.consumiveis["bandagem"], 1)
        self.assertEqual(g.j.reputacao, 2)
        self.assertEqual(cm.membro(g, "odete")["aprovacao"], 12)

    def test_perguntar_nao_muda_a_ajuda(self):
        # o mesmo sorteio e o mesmo resultado, perguntando antes ou não
        for roteiro in (["Segurar a ferida", "Aceitar"], ["Estancar o sangue", "Aceitar"]):
            pela_direta = self.rodar(roteiro, bandagem=1)[1]
            perguntando = self.rodar(["Perguntar quem ela é"] + roteiro, bandagem=1)[1]
            self.assertEqual(self.estado(perguntando), self.estado(pela_direta))
            self.assertEqual(cm.membro(perguntando, "odete")["aprovacao"],
                             cm.membro(pela_direta, "odete")["aprovacao"])

    def test_perguntar_depois_oracao(self):
        for seed in range(1, 40):
            ui = Anotador(["Perguntar quem ela é", "Segurar a ferida", "Aceitar"])
            g = Jogo(ui, seed=seed, pasta_saves=tempfile.mkdtemp())
            g.iniciar("Teste", "guerreiro")
            g.comitiva.clear()
            ev_comitiva.odete_na_estrada(g)
            texto = " ".join(ui.ditos)
            m = cm.membro(g, "odete")
            if "Fraco, mas respira" in texto:
                self.assertIn("Você vai para onde está a dor", texto)
                self.assertEqual((g.j.reputacao, m["aprovacao"]), (2, 10))
            else:
                self.assertIn("Você ficou até o fim", texto)
                self.assertEqual((g.j.reputacao, m["aprovacao"]), (0, 5))

    def test_perguntar_depois_seguir_ou_revistar(self):
        ui, g = self.rodar(["Perguntar quem ela é", "Seguir seu caminho"])
        self.assertIn("Você segue. Atrás de você, Odette começa a rezar.", ui.ditos)
        self.assertEqual(g.flag("comitiva:odete"), "recusou")
        self.assertEqual(g.j.reputacao, 0)
        ui, g = self.rodar(["Seguir seu caminho"])
        self.assertIn("Você segue. Atrás de você, uma voz de mulher começa a rezar.", ui.ditos)  # sem o nome, ninguém o sabe
        ui, g = self.rodar(["Revistar o moribundo"])
        self.assertTrue(any("A mulher se levanta" in d for d in ui.ditos))
        ui, g = self.rodar(["Perguntar quem ela é", "Revistar o moribundo"])
        self.assertTrue(any("Odette se levanta" in d for d in ui.ditos))
        self.assertEqual(g.flag("comitiva:odete"), "recusou")

    def test_remedios_na_porta(self):
        ui = Anotador(["Deixar remédios"])
        g = jogo(ui, pocao_vida=2)
        ev_classe.os_enfermos(g)
        self.assertEqual(ui.metas[0][1]["nota"], "Usa 1 poção de vida da bolsa (você tem 2).")
        self.assertEqual(g.j.consumiveis["pocao_vida"], 1)
        ui = Anotador(["Deixar remédios", "Seguir em frente"])
        g = jogo(ui, pocao_vida=0)
        ev_classe.os_enfermos(g)
        self.assertEqual(ui.metas[0][1]["indisponivel"], "Você não tem poção de vida na bolsa.")
        self.assertEqual(g.j.consumiveis["pocao_vida"], 0)
        self.assertEqual(len(ui.ofertas), 2)

    def test_o_robo_nunca_escolhe_a_indisponivel(self):
        ui = BotUI(random.Random(1))
        ui.meta_opcoes = [{"indisponivel": "x"}, None, None]
        self.assertTrue(all(ui.escolher("?", ["a", "b", "c"]) != 0 for _ in range(200)))


class TestProtecao(unittest.TestCase):
    def test_o_mendigo_avisa_o_que_deu_sem_item_na_bolsa(self):
        ui = Anotador(["Pagar uma refeição"])
        g = jogo(ui)
        g.j.ouro = 50
        bolsa = dict(g.j.consumiveis)
        ev_vila.mendigo_misterioso(g)
        self.assertEqual(g.flag("bencao_fenix"), "mendigo")
        self.assertIn((Jogo.AVISO_PROTECAO, "protecao"), ui.efeitos)
        self.assertEqual(g.j.consumiveis, bolsa)  # nenhum item: é uma bênção
        self.assertNotIn("bolso", " ".join(ui.ditos))

    def test_o_santuario_guarda_a_origem(self):
        ui = Anotador(["Rezar"])
        g = jogo(ui)
        g.teste = lambda *a, **k: True
        g.sortear = lambda xs: "fenix" if "fenix" in xs else xs[0]
        ev_comuns.santuario_antigo(g)
        self.assertEqual(g.flag("bencao_fenix"), "santuario")
        self.assertIn((Jogo.AVISO_PROTECAO, "protecao"), ui.efeitos)

    def levantar(self, origem, pena=0):
        ui = Anotador()
        g = jogo(ui, pena_fenix=pena)
        g.marcar("bencao_fenix", origem)
        cb = Combate(g, [g.inimigo("lobo")])
        g.j.hp = 0
        self.assertIsNone(cb._checar_fim())
        g.combate_ativo = None
        return g, ui

    def test_ao_cair_a_protecao_levanta_e_aparece_na_luta(self):
        for origem, frase in (("santuario", "bênção do santuário"), ("mendigo", "calor que ficou no seu peito"),
                              (True, "Uma força que você carregava")):  # True: save de antes, sem origem
            g, ui = self.levantar(origem)
            self.assertEqual(g.j.hp, g.j.max_hp // 2)
            self.assertFalse(g.flag("bencao_fenix"))  # usada
            texto = " ".join(ui.ditos)
            self.assertIn(frase, texto)
            if origem != "santuario":
                self.assertNotIn("santuário", texto)
            cura = [d for t, d in ui.lances if t == "cura"]
            self.assertEqual((cura[-1]["em"], cura[-1]["valor"], cura[-1]["rotulo"]), ("j", g.j.max_hp // 2, "De pé outra vez"))
            self.assertTrue(any(t == "protecao" and "se foi" in x for x, t in ui.efeitos))
        self.assertEqual(ORIGEM_PROTECAO[None], "Uma força que você carregava te puxa de volta da escuridão!")

    def test_a_pena_vem_antes_da_bencao(self):
        g, ui = self.levantar("mendigo", pena=1)
        self.assertEqual((g.j.consumiveis["pena_fenix"], g.flag("bencao_fenix")), (0, "mendigo"))
        self.assertIn("Pena de Fênix", [d["rotulo"] for t, d in ui.lances if t == "cura"])

    def test_um_uso_so(self):
        g, ui = self.levantar("mendigo")
        cb = Combate(g, [g.inimigo("lobo")])
        g.j.hp = 0
        self.assertEqual(cb._checar_fim(), "derrota")
        g.combate_ativo = None


class TestExausto(unittest.TestCase):
    def test_a_faixa_nao_pede_um_continuar_a_mais(self):
        ui = WebUI()
        ui.novo_desde_escolha = False
        ui.celebrar("exausto", {"texto": "Não dá para seguir: é preciso acampar."})
        self.assertFalse(ui.novo_desde_escolha)
        ui.celebrar("nivel", {"nivel": 2})  # as festas que esperam leitura continuam pedindo
        self.assertTrue(ui.novo_desde_escolha)

    def test_na_vila_a_faixa_vem_na_pagina_da_cena(self):
        ui = Anotador()
        ui.conquistas_na_tela = True
        g = jogo(ui)
        vila = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")
        g.mundo["atual"], g.periodo = vila["id"], 4
        dia, hp = g.dia, g.j.hp
        g.exausto()
        self.assertEqual(ui.ordem[:2], [("cena", "Exausto"), ("celebrar", "exausto")])
        self.assertEqual((g.dia, g.periodo), (dia + 1, 0))  # o dia passa como antes
        self.assertGreaterEqual(g.j.hp, hp)


if __name__ == "__main__":
    unittest.main()
