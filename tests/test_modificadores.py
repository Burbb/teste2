"""Modificadores e gatilhos: cada talento faz alguma coisa, com chaves que o jogo de fato pergunta."""

import random
import tempfile
import unittest

from rpg import itens, modificadores as M
from rpg.classes import CLASSES, SPECS
from rpg.habilidades import HABILIDADES
from rpg.jogo import Jogo
from rpg.talentos import PASSIVAS, POR_ID, TALENTOS, custo_habilidade
from rpg.ui import BotUI


def _fontes():
    yield from ((t["id"], t) for lista in TALENTOS.values() for t in lista)
    yield from ((f"passiva:{k}", p) for k, p in PASSIVAS.items())


class TestModificadores(unittest.TestCase):
    def test_todo_talento_faz_algo(self):
        for tid, t in _fontes():
            self.assertTrue(t.get("stats") or t.get("mods") or t.get("mults") or t.get("gatilhos"), tid)

    def test_chaves_e_eventos_conhecidos(self):
        """Uma chave com erro de digitação não faria nada em silêncio: aqui ela falha."""
        for tid, t in _fontes():
            for chave in t.get("mods", {}):
                if chave.startswith(M.PREFIXOS):
                    self.assertIn(chave.split(":", 1)[1], HABILIDADES, f"{tid}: {chave}")
                else:
                    self.assertIn(chave, M.CHAVES, f"{tid}: {chave}")
            for chave in t.get("mults", {}):
                self.assertIn(chave, M.MULTS, f"{tid}: {chave}")
            for ev in t.get("gatilhos", {}):
                self.assertIn(ev, M.EVENTOS, f"{tid}: {ev}")

    def test_soma_por_ponto_e_fixo(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        j = g.j
        self.assertEqual(M.mod(j, "dano_corpo"), 0)
        j.talentos["golpe_brutal"] = 3
        self.assertAlmostEqual(M.mod(j, "dano_corpo"), 0.18)
        self.assertEqual(M.nomes(j, "dano_corpo"), ["Golpe Brutal"])
        base = custo_habilidade(j, "erguer_escudo")
        j.talentos["muralha"] = 1  # Fixo(-4): vale uma vez
        self.assertEqual(custo_habilidade(j, "erguer_escudo"), base - 4)
        self.assertEqual(M.mod(j, "escudo_turnos"), 1)

    def test_passiva_da_especializacao(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        self.assertEqual(M.mod(g.j, "dano_ferido"), 0)
        g.j.spec = "berserker"
        self.assertEqual(M.mod(g.j, "dano_ferido"), 0.6)
        self.assertIn("Pacto de Sangue", M.nomes(g.j, "dano_ferido"))

    def test_gatilho_imortal_salva_do_golpe_fatal(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        g.j.spec, g.j.talentos["imortal"] = "berserker", 1
        e = g.inimigo("lobo", nivel=1)
        from rpg.combate import Combate
        cb = Combate(g, [e])
        g.j.hp = 5
        d = M.disparar(cb, g.j, "golpe_fatal", dano=50, de=e)
        self.assertEqual(d["dano"], 4)
        self.assertTrue(cb.usou_imortal)
        self.assertEqual(M.disparar(cb, g.j, "golpe_fatal", dano=50, de=e)["dano"], 50)  # só uma vez por luta
        g.combate_ativo = None

    def test_itens_so_com_chaves_conhecidas(self):
        for k in itens.ESPECIAIS:
            self.assertIn(k, M.CHAVES, k)
        for u in itens.UNICOS:
            for chave in u.get("mods", {}):
                self.assertIn(chave, M.CHAVES, f"{u['nome']}: {chave}")
            for chave in u.get("mults", {}):
                self.assertIn(chave, M.MULTS, f"{u['nome']}: {chave}")
            for ev in u.get("gatilhos", {}):
                self.assertIn(ev, M.EVENTOS, f"{u['nome']}: {ev}")

    def test_classe_e_especializacao_so_com_chaves_conhecidas(self):
        for k, c in list(CLASSES.items()) + list(SPECS.items()):
            for chave in c.get("mods", {}):
                self.assertIn(chave, M.CHAVES, f"{k}: {chave}")

    def test_fe_do_paladino(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        self.assertEqual(M.mod(g.j, "resiste_terror"), 0)
        g.j.spec = "paladino"
        self.assertEqual(M.mod(g.j, "resiste_terror"), 0.6)
        self.assertIn(("paladino", 3), g.partes_teste("vontade"))

    def test_item_vestido_e_fonte(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        j = g.j
        j.equip["anel1"] = {"nome": "Anel do Vampiro", "slot": "anel", "raridade": "magico",
                            "bonus": {"atk": 2, "roubo_vida": 5, "espinhos": 3}}
        self.assertAlmostEqual(M.mod(j, "roubo_vida"), 0.05)  # no item em %, no modificador em fração
        self.assertEqual(M.mod(j, "espinhos"), 3)
        self.assertEqual(M.mod(j, "atk"), 0)  # atributo comum não é modificador: entra em recalcular()
        self.assertEqual(M.contribuicoes(j, "roubo_vida"), [("Anel do Vampiro", 0.05)])

    def test_unico_declara_gatilho(self):
        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Teste", "guerreiro")
        visto = []
        unico = dict(nome="Teste Único", slot="anel", classe=None, base="Anel", bonus={"atk": 1}, lore="",
                     mods={"mult_critico": 0.3}, gatilhos={"abate": lambda cb, u, rank, d: visto.append(d["alvo"])})
        itens.UNICOS_POR_NOME[unico["nome"]] = unico
        try:
            g.j.equip["anel1"] = {"nome": "Teste Único", "slot": "anel", "raridade": "lendario", "bonus": {"atk": 2}}
            self.assertAlmostEqual(M.mod(g.j, "mult_critico"), 0.3)
            M.disparar(None, g.j, "abate", alvo="lobo", tipo="fisico")
            self.assertEqual(visto, ["lobo"])
        finally:
            del itens.UNICOS_POR_NOME[unico["nome"]]

    def test_ids_unicos(self):
        self.assertEqual(len(POR_ID), sum(len(l) for l in TALENTOS.values()))


if __name__ == "__main__":
    unittest.main()
