"""A campanha escrita (protótipo da E2): o Vale do Turvo como mapa fixo, a viagem, a saída fechada, os eventos que
ficam de fora e o save. O mundo gerado continua igual (o gabarito confere)."""

import os
import random
import tempfile
import unittest
from unittest import mock

from rpg import campanha, mapa
from rpg.eventos import motor
from rpg.eventos.vila import ouvir_rumor
from rpg.jogo import Jogo
from rpg.mundo import nivel_regiao
from rpg.regras import FimDeJogo
from rpg.sistemas.persistencia import resumo_save
from rpg.ui import BotUI, LimiteBot

CLASSES = ("guerreiro", "arqueiro", "mago")


class Roteiro(BotUI):
    """Robô que escolhe pelo texto: a primeira opção que contém o próximo trecho do roteiro (senão, ao acaso).
    Guarda tudo o que foi dito e as opções oferecidas, para conferir."""

    def __init__(self, roteiro=(), seed=1):
        super().__init__(random.Random(seed), max_decisoes=400)
        self.roteiro = list(roteiro)
        self.ditos = []
        self.ofertas = []

    def dizer(self, texto="", cor=None):
        self.ditos.append(texto)

    narrar = dizer

    def escolher(self, pergunta, opcoes):
        self.ofertas.append(list(opcoes))
        if self.roteiro:
            alvo = self.roteiro[0]
            for i, o in enumerate(opcoes):
                if alvo in o:
                    self.roteiro.pop(0)
                    self.decisoes += 1
                    return i
        return super().escolher(pergunta, opcoes)


def lugar(g, chave):
    return next(l for l in g.mundo["locais"] if l.get("chave") == chave)


def nova_campanha(classe="guerreiro", ui=None, pasta=None, hardcore=False):
    g = Jogo(ui or Roteiro(), seed=5, pasta_saves=pasta or tempfile.mkdtemp(), hardcore=hardcore)
    g.iniciar("Teste", classe, "turvo")
    return g


class TestCampanha(unittest.TestCase):
    def test_comeca_no_vau_com_as_tres_classes(self):
        for classe in CLASSES:
            g = nova_campanha(classe)
            self.assertEqual(g.campanha, "turvo")
            self.assertEqual(g.j.classe, classe)
            self.assertEqual(g.loc["chave"], "vau_do_turvo")
            self.assertEqual(g.loc["tipo"], "vila")
            self.assertTrue(g.loc["visitado"])
            self.assertIsNone(g.antagonista)
            self.assertEqual({l["chave"] for l in g.mundo["locais"]},
                             {"vau_do_turvo", "charco_dos_juncos", "bosque_do_moinho", "capela_afogada",
                              "estrada_de_varn"})
            self.assertIsNotNone(g.j.equip["arma"])

    def test_criacao_escolhe_o_modo(self):
        for modo, hardcore in (("Resgate", False), ("Hardcore", True)):
            ui = Roteiro(["Arqueiro", modo])
            g = Jogo(ui, seed=2, pasta_saves=tempfile.mkdtemp(), hardcore=not hardcore)
            self.assertTrue(g.novo_jogo("turvo"))
            self.assertEqual((g.campanha, g.j.classe, g.hardcore), ("turvo", "arqueiro", hardcore))
            self.assertTrue(any(("Hardcore:" if hardcore else "Resgate:") in d for d in ui.ditos))
            self.assertTrue(any("Estrada de Varn" in d for d in ui.ditos))
            self.assertIn("Resgate", ui.ofertas[-1][0])  # o resgate é o padrão: vem primeiro

    def test_voltar_no_modo_volta_para_a_classe(self):
        ui = Roteiro(["Mago", "Voltar", "Guerreiro", "Resgate"])
        g = Jogo(ui, seed=2, pasta_saves=tempfile.mkdtemp())
        self.assertTrue(g.novo_jogo("turvo"))
        self.assertEqual((g.j.classe, g.hardcore), ("guerreiro", False))

    def test_nivel_fixo_por_lugar(self):
        g = nova_campanha()
        niveis = {l["chave"]: nivel_regiao(l) for l in g.mundo["locais"]}
        self.assertEqual(niveis["vau_do_turvo"], 1)
        self.assertEqual(niveis["charco_dos_juncos"], 1)
        self.assertEqual(niveis["bosque_do_moinho"], 2)
        self.assertEqual(niveis["capela_afogada"], 3)

    @mock.patch("rpg.sistemas.navegacao.eventos.disparar", lambda g, contexto: None)
    def test_viajar_descobrir_e_voltar(self):
        ui = Roteiro()
        g = nova_campanha(ui=ui)
        capela = lugar(g, "capela_afogada")
        self.assertNotIn(capela["id"], mapa.conhecidos(g))  # a capela só aparece depois do bosque
        for destino, chave in (("Bosque do Moinho", "bosque_do_moinho"), ("Capela Afogada", "capela_afogada"),
                               ("Bosque do Moinho", "bosque_do_moinho"), ("Vau do Turvo", "vau_do_turvo"),
                               ("Charco dos Juncos", "charco_dos_juncos"), ("Vau do Turvo", "vau_do_turvo")):
            ui.roteiro = [destino]
            g.viajar()
            self.assertEqual(g.loc["chave"], chave)
            self.assertTrue(g.loc["visitado"])
            if chave == "bosque_do_moinho":
                self.assertIn(capela["id"], mapa.conhecidos(g))
        self.assertFalse(lugar(g, "estrada_de_varn")["visitado"])

    def test_estrada_de_varn_fica_fechada(self):
        ui = Roteiro(["Estrada de Varn"])
        g = nova_campanha(ui=ui)
        dia, periodo = g.dia, g.periodo
        g.viajar()
        self.assertEqual(g.loc["chave"], "vau_do_turvo")
        self.assertEqual((g.dia, g.periodo), (dia, periodo))  # nem saiu da vila
        self.assertIn(campanha.REGIOES["turvo"]["fechados"]["estrada_de_varn"], ui.ditos)
        varn = next(o for o in ui.ofertas[0] if "Estrada de Varn" in o)
        self.assertNotIn("Nv.", varn)
        self.assertNotIn("PERIGOSO", varn)
        self.assertEqual(mapa.descricao(g, lugar(g, "estrada_de_varn")), "saída, fechada por enquanto")
        from rpg.web.estado import mapa_conhecido
        no = next(n for n in mapa_conhecido(g)["nos"] if n["nome"] == "Estrada de Varn")
        self.assertIsNone(no["nivel"])

    def test_eventos_do_mundo_gerado_que_ficam_de_fora(self):
        g = nova_campanha()
        for contexto in ("explorar", "viagem", "acampamento", "vila", "taverna"):
            ids = {ev.id for ev, _ in motor.candidatos(g, contexto)}
            self.assertFalse(ids & campanha.EVENTOS_FORA, contexto)
        ids = {ev.id for ev in motor.REGISTRO}
        self.assertLessEqual(campanha.EVENTOS_FORA, ids)  # todo id da lista existe
        procedural = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp())
        procedural.iniciar("Teste", "guerreiro")
        self.assertIsNone(procedural.campanha)
        self.assertEqual(procedural.eventos_fora(), frozenset())

    def test_rumores_e_contratos_ficam_no_vale(self):
        g = nova_campanha()
        for _ in range(40):
            ouvir_rumor(g)  # sem vilão, o rumor de lore não aparece (antes: KeyError)
        validos = {l["id"] for l in g.mundo["locais"] if l["tipo"] == "selvagem"}
        for r in g.rumores:
            if "local" in r:
                self.assertIn(r["local"], validos)
        for _ in range(40):
            c = g.gerar_contrato()
            self.assertIn(c["tipo"], ("caca", "alvo"))  # entrega pede outra vila
            self.assertIn(c["local"], validos)
        g.diario = g.diario  # o diário sem vilão não quebra
        g.ui.roteiro = ["Fechar"]
        g.diario()

    def test_salvar_e_carregar(self):
        pasta = tempfile.mkdtemp()
        g = nova_campanha("mago", pasta=pasta, hardcore=True)
        bosque = lugar(g, "bosque_do_moinho")
        g.mundo["atual"] = bosque["id"]
        bosque["visitado"] = True
        g.dia = 4
        g.salvar(silencioso=True)
        caminho = g.caminho_save()
        self.assertTrue(os.path.basename(caminho).startswith("turvo_"))
        h = Jogo.carregar(Roteiro(), caminho, pasta)
        self.assertEqual((h.campanha, h.hardcore, h.loc["chave"], h.dia, h.j.classe),
                         ("turvo", True, "bosque_do_moinho", 4, "mago"))
        self.assertEqual({l["chave"] for l in h.mundo["locais"] if l["visitado"]},
                         {"vau_do_turvo", "bosque_do_moinho"})
        self.assertIn("fechado", lugar(h, "estrada_de_varn"))
        r = resumo_save(caminho)
        self.assertEqual((r["campanha"], r["hardcore"], r["lugar"]), ("Vale do Turvo", True, "Bosque do Moinho"))

    def test_save_do_mundo_gerado_nao_e_sobrescrito(self):
        pasta = tempfile.mkdtemp()
        p = Jogo(Roteiro(), seed=5, pasta_saves=pasta)
        p.iniciar("Teste", "guerreiro")
        p.salvar(silencioso=True)
        c = nova_campanha("arqueiro", pasta=pasta)
        c.salvar(silencioso=True)
        self.assertNotEqual(p.caminho_save(), c.caminho_save())
        self.assertEqual(sorted(os.listdir(pasta)), ["teste.json", "turvo_teste.json"])
        r = resumo_save(p.caminho_save())
        self.assertNotIn("campanha", r)
        self.assertEqual(r["classe"], "guerreiro")
        self.assertIsNone(Jogo.carregar(Roteiro(), p.caminho_save(), pasta).campanha)

    def test_titulo_oferece_a_campanha(self):
        import argparse
        from rpg.__main__ import CAMPANHA, menu_principal
        pasta = tempfile.mkdtemp()
        ui = Roteiro([CAMPANHA, "Guerreiro", "Resgate"])
        ui.max_decisoes = 30
        with mock.patch.object(Jogo, "rodar", side_effect=FimDeJogo), mock.patch.object(Roteiro, "interativo", False):
            ui.roteiro.append("Sair")  # depois de começar, volta ao título e sai
            menu_principal(ui, argparse.Namespace(seed=3, saves=pasta, brando=False, dev=None))
        self.assertIn(CAMPANHA, ui.ofertas[0])
        self.assertIn("Novo jogo", ui.ofertas[0])

    def test_robo_atravessa_o_vale(self):
        """O robô joga ao acaso (eventos, lutas, vila, resgate): nada quebra e ninguém para na saída fechada."""
        for classe in CLASSES:
            for hardcore in (False, True):
                g = nova_campanha(classe, ui=BotUI(random.Random(len(classe)), max_decisoes=250),
                                  hardcore=hardcore)
                try:
                    g.rodar()
                except LimiteBot:
                    pass
                self.assertNotEqual(g.loc["tipo"], "saida")
                self.assertFalse(set(g.contagem) & campanha.EVENTOS_FORA)


if __name__ == "__main__":
    unittest.main()
