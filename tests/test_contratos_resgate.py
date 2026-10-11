"""Contratos cumpridos e o resgate (E9, a partida da Quibia): quem acorda na vila depois de uma queda recebe os
contratos cumpridos como quem chega viajando, uma vez só, depois da cobrança do resgate e sem viagem nem evento de
chegada. Vale para a campanha (combate, fome, infecção), para o mundo gerado no modo brando e para os saves feitos na
vila com contrato cumprido e ainda não pago."""

import random
import tempfile
import unittest
from unittest import mock

from rpg.jogo import Jogo
from tests.test_recompensas import AnotadorGrafico
from tests.test_recuperacao import cair_de_noite, faminto, infeccionado, no_charco
from tests.test_missoes import Roteiro


def cumpridos(g, n):
    """n contratos cumpridos (e um aberto, que não paga): o que eles prometem."""
    for _ in range(n):
        c = g.gerar_contrato()
        c["concluido"] = True
        g.contratos.append(c)
    aberto = g.gerar_contrato()
    g.contratos.append(aberto)
    feitos = [c for c in g.contratos if c.get("concluido")]
    return sum(c["ouro"] for c in feitos), sum(c["xp"] for c in feitos), aberto


def menu(g):
    """O ciclo principal até o menu do lugar (que não abre aqui): antes dele, as cenas de missão pendentes no lugar."""
    chegou = []
    with mock.patch.object(g, "menu_vila", lambda: chegou.append(1)), \
            mock.patch.object(g, "menu_selvagem", lambda: chegou.append(1)):
        for _ in range(6):
            g.tela()
            if chegou:
                return
    raise AssertionError("o menu do lugar não chegou")


def resgatar(g, causa):
    if causa == "fome":
        faminto(g)
    elif causa == "infeccao":
        infeccionado(g)
    g.resgate(causa if causa == "combate" else cair_de_noite(g))


def estado(g):
    return g.j.ouro, g.j.xp, g.j.nivel, g.j.reputacao


class TestCampanha(unittest.TestCase):
    def test_um_dois_ou_nenhum_contrato_em_cada_queda(self):
        for causa in ("combate", "fome", "infeccao"):
            for n in (0, 1, 2):
                g = no_charco(ouro=100)
                ouro, xp, aberto = cumpridos(g, n)
                g.j.xp = 0
                resgatar(g, causa)
                self.assertEqual(g.loc["chave"], "vau_do_turvo")
                cobranca = [e for e in g.registro if e["t"] == "resgate"][-1]["perda"]
                self.assertEqual(cobranca, 30)  # a cobrança é sobre o ouro de antes: o pagamento vem depois
                rep = g.j.reputacao
                menu(g)
                self.assertEqual(g.contratos, [aberto], (causa, n))
                self.assertEqual(g.j.ouro, 70 + ouro, (causa, n))
                self.assertEqual(g.j.reputacao, min(50, rep + 3 * n), (causa, n))
                self.assertTrue(g.j.xp == xp or g.j.nivel > 1, (causa, n))
                antes = estado(g)
                menu(g)  # a próxima volta não paga de novo
                self.assertEqual(estado(g), antes)

    def test_sem_viagem_nem_evento_de_chegada(self):
        g = no_charco(ouro=100)
        cumpridos(g, 1)
        resgatar(g, "combate")
        with mock.patch("rpg.eventos.disparar") as disparar, mock.patch.object(g, "chegar") as chegar:
            menu(g)
        disparar.assert_not_called()
        chegar.assert_not_called()
        self.assertFalse([e for e in g.registro if e["t"] == "chegada" and e["dia"] == g.dia])

    def test_ordem_resgate_depois_o_pagamento(self):
        g = no_charco(ouro=100)
        cumpridos(g, 2)
        resgatar(g, "fome")
        menu(g)
        texto = " ".join(g.ui.ditos)
        self.assertLess(texto.index("Dois dias se passaram"), texto.index("Recompensa de contrato"))
        self.assertEqual(texto.count("Recompensa de contrato"), 2)

    def test_tela_grafica_um_quadro_depois_do_amanhecer_e_na_pagina_da_vila(self):
        ui = AnotadorGrafico(random.Random(1))
        ordem = []
        ui.cena = lambda titulo, sub=None, tipo="evento": ordem.append(("cena", tipo))
        celebrar = ui.celebrar
        ui.celebrar = lambda tipo, dados: (ordem.append(("festa", tipo)), celebrar(tipo, dados))
        g = Jogo(ui, seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
        g.iniciar("Teste", "guerreiro", "turvo")
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["chave"] == "charco_dos_juncos")["id"]
        ouro, xp, _ = cumpridos(g, 2)
        ordem.clear()
        g.resgate("combate")
        menu(g)
        festas = [d for t, d in ui.festas if t == "contratos"]
        self.assertEqual(len(festas), 1)
        self.assertEqual((festas[0]["ouro"], festas[0]["xp"], len(festas[0]["contratos"])), (ouro, xp, 2))
        i = ordem.index(("festa", "contratos"))
        self.assertIn(("festa", "amanhecer"), ordem[:i])
        self.assertEqual(ordem[i - 1], ("cena", "local"))  # a página da vila, depois do texto do resgate

    def test_salvar_e_carregar_depois_do_pagamento(self):
        pasta = tempfile.mkdtemp()
        g = no_charco(ouro=100, pasta=pasta)
        cumpridos(g, 2)
        resgatar(g, "combate")
        menu(g)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual((estado(h), len(h.contratos)), (estado(g), 1))
        menu(h)
        self.assertEqual(estado(h), estado(g))  # não paga de novo

    def test_save_na_vila_com_contrato_cumprido_e_nao_pago(self):
        """Um save de antes desta correção: o resgate já tinha deixado o herói no Vau, com os contratos por pagar."""
        pasta = tempfile.mkdtemp()
        g = no_charco(ouro=100, pasta=pasta)
        ouro, _, _ = cumpridos(g, 1)
        resgatar(g, "combate")
        g.salvar(silencioso=True)  # antes da primeira volta do menu
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        menu(h)
        self.assertEqual((h.j.ouro, len(h.contratos)), (70 + ouro, 1))
        menu(h)
        self.assertEqual(h.j.ouro, 70 + ouro)

    def test_fora_da_vila_nao_paga(self):
        g = no_charco(ouro=100)
        cumpridos(g, 1)
        menu(g)
        self.assertEqual((g.j.ouro, len(g.contratos)), (100, 2))


class TestMundoGerado(unittest.TestCase):
    def test_resgate_brando_tambem_paga(self):
        g = Jogo(Roteiro(), seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
        g.iniciar("Teste", "guerreiro")
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")["id"]
        g.j.ouro = 100
        ouro, _, aberto = cumpridos(g, 2)
        g.resgate("combate")
        self.assertEqual((g.loc["tipo"], g.j.ouro), ("vila", 70))  # a derrota custa como antes
        menu(g)
        self.assertEqual((g.j.ouro, g.contratos), (70 + ouro, [aberto]))


if __name__ == "__main__":
    unittest.main()
