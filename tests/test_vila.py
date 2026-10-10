"""Serviços da vila e o item achado: o que o motor pergunta e manda para a tela."""

import random
import tempfile
import unittest

from rpg import comitiva as cm
from rpg.itens import gerar_equip
from rpg.jogo import Jogo
from rpg.ui import BotUI


class Roteiro(BotUI):
    """Escolhe pelo texto (o primeiro trecho do roteiro que aparece nas opções); anota perguntas, opções e painéis."""

    def __init__(self, roteiro=()):
        super().__init__(random.Random(1), max_decisoes=60)
        self.roteiro = list(roteiro)
        self.perguntas, self.paineis = [], []

    def escolher(self, pergunta, opcoes):
        self.perguntas.append((pergunta, list(opcoes), self.meta_opcoes))
        alvo = self.roteiro.pop(0)
        return next(i for i, o in enumerate(opcoes) if alvo in o)

    def painel(self, tipo, dados):
        self.paineis.append((tipo, dados))
        return False


def na_vila(ui):
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", "guerreiro")
    g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")["id"]
    return g


class TestVila(unittest.TestCase):
    def test_templo_fica_no_balcao_ate_voltar(self):
        """Depois de cuidar de alguém, o templo pergunta de novo com o ouro e os preços de agora e só quem ainda
        precisa; sem ninguém, sobra o Voltar (com a meta do balcão, que a tela usa para continuar diante dele)."""
        ui = Roteiro(["cuidar de Odette", "Voltar à vila"])
        g = na_vila(ui)
        g.j.ouro = 200
        g.j.hp = g.j.max_hp // 2
        cm.recrutar(g, "odete")["hp"] -= 10
        escolha = next(o[1] for o in g.opcoes_templo() if o[1][1] is None)
        g.balcao_templo(escolha[1:])
        self.assertEqual(g.j.hp, g.j.max_hp)
        self.assertEqual(cm.membro(g, "odete")["hp"], cm.membro(g, "odete")["max_hp"])
        (p1, o1, m1), (p2, o2, m2) = ui.perguntas
        self.assertEqual(p1, "Mais alguém precisa de cuidados?")
        self.assertEqual([o.split(" (")[0] for o in o1 if "Templo" in o], ["Templo: cuidar de Odette"])  # você já foi
        self.assertEqual(m1[-1], {"voltar": True, "balcao": "templo"})
        self.assertEqual((p2, o2), ("Ninguém mais precisa de cuidados.", ["Voltar à vila"]))
        self.assertLess(g.j.ouro, 200)

    def test_achado_manda_os_rotulos_dos_botoes(self):
        """O cartão do item achado leva os rótulos das ações que vão chegar: a janela reserva o lugar exato delas."""
        for cheia in (False, True):
            ui = Roteiro(["Guardar" if not cheia else "Deixar"])
            g = na_vila(ui)
            if cheia:
                g.j.mochila = [gerar_equip(random.Random(i), "guerreiro", 1) for i in range(12)]
            g.oferecer_equip(gerar_equip(random.Random(3), "guerreiro", 2, "armadura"))
            tipo, dados = ui.paineis[-1]
            self.assertEqual(tipo, "achado")
            self.assertEqual(dados["acoes"], ui.perguntas[-1][1])


if __name__ == "__main__":
    unittest.main()
