"""Os testes do d20 na ficha (web/estado.py, explicar_testes): o que a tela mostra é o que o motor soma no teste, com
as partes do personagem separadas da situação de agora (sem luz) e o atributo abaixo do normal explicado."""

import random
import tempfile
import unittest

from rpg import sobrevivencia
from rpg.jogo import Jogo
from rpg.regras import NOMES_TESTE
from rpg.ui import BotUI
from rpg.web.estado import estado


def jogo(classe="guerreiro", nivel=1):
    g = Jogo(BotUI(random.Random(2)), seed=2, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", classe)
    for _ in range(nivel - 1):
        g.subir_nivel()
    return g


def testes(g):
    """Como a tela recebe (as partes em listas, como no JSON)."""
    t = estado(g)["heroi"]["testes"]
    for x in t.values():
        for k in ("partes", "fixas", "situacao"):
            x[k] = [list(p) for p in x[k]]
    return t


class TestTestesNaFicha(unittest.TestCase):
    def conferir_com_o_motor(self, g):
        t = testes(g)
        self.assertEqual(set(t), set(NOMES_TESTE.values()))
        for attr, nome in NOMES_TESTE.items():
            x = t[nome]
            # o total de agora e as partes são as do teste (o que soma no d20), sem conta nova na tela
            self.assertEqual(x["mod"], g.mod_teste(attr), nome)
            self.assertEqual(x["partes"], [list(p) for p in g.partes_teste(attr)], nome)
            self.assertEqual(x["fixo"] + sum(v for _, v in x["situacao"]), x["mod"], nome)
            # a chance numa dificuldade típica: a regra do teste, face a face
            cd = g.dificuldade(g.CD_MEDIA)
            faces = sum(1 for d in range(1, 21) if d == 20 or (d != 1 and d + x["mod"] >= cd))
            self.assertEqual(x["chance_media"], faces * 5, nome)
            self.assertTrue(x["uso"], nome)
        return t

    def test_caso_basico(self):
        t = self.conferir_com_o_motor(jogo())
        self.assertEqual(t["Percepção"]["situacao"], [])
        self.assertEqual(t["Percepção"]["abaixo"], [])

    def test_bonus_de_classe_e_nivel(self):
        g = jogo("arqueiro", nivel=5)
        t = self.conferir_com_o_motor(g)
        self.assertIn(["olhos de arqueiro", 3], t["Percepção"]["fixas"])
        self.assertIn(["nível", 2], t["Percepção"]["fixas"])

    def test_escuridao_e_da_situacao_nao_do_personagem(self):
        g = jogo()
        claro = testes(g)
        g.sem_luz = True
        t = self.conferir_com_o_motor(g)
        for nome in ("Percepção", "Destreza"):
            self.assertEqual(t[nome]["fixo"], claro[nome]["fixo"], nome)          # o do personagem não muda
            self.assertEqual(t[nome]["situacao"], [["escuridão", -4]], nome)
            self.assertEqual(t[nome]["mod"], claro[nome]["mod"] - 4, nome)
        # a dica da Agilidade diz a parte dela, que a escuridão não toca
        info = estado(g)["heroi"]["atributos_info"]["Agilidade"]
        g.sem_luz = False
        self.assertEqual(info, estado(g)["heroi"]["atributos_info"]["Agilidade"])

    def test_atributo_abaixo_do_normal(self):
        g = jogo("arqueiro", nivel=5)
        sobrevivencia.ferir(g, "perna")
        t = self.conferir_com_o_motor(g)
        # a Percepção é atributo próprio (etapa 4): a perna torcida tira da Agilidade e, com ela, da Destreza
        self.assertTrue(any("Agilidade abaixo do normal" in l and "Perna torcida" in l for l in t["Destreza"]["abaixo"]))
        self.assertEqual(t["Percepção"]["abaixo"], [])
        self.assertEqual(t["Força"]["abaixo"], [])


if __name__ == "__main__":
    unittest.main()
