"""O laboratório do encantamento (gravação): as ações conferidas e os efeitos na luta.

    python -m unittest discover -s ferramentas/prototipos/reforco/testes -t ferramentas/prototipos/reforco
"""

import os
import random
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.dirname(AQUI)
RAIZ = os.path.normpath(os.path.join(PASTA, "..", "..", ".."))
for p in (RAIZ, PASTA):
    if p not in sys.path:
        sys.path.insert(0, p)

import demo as D  # noqa: E402
import encanto as E  # noqa: E402
from rpg.inimigos import criar  # noqa: E402
from rpg.jogo import Jogo  # noqa: E402
from rpg.ui import BotUI  # noqa: E402

D.ativar()
FICHA = D.FICHA


def jogo(seed=11):
    g = Jogo(BotUI(random.Random(seed), max_decisoes=10 ** 6), seed=seed, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    D.preparar(g)
    D.dar_uid(g)
    for k in E.ORDEM:
        D.materiais(g)[E.ESSENCIAS[k]["material"]] = 2
    return g


def lutar(g, n=2, nivel=None):
    """Uma luta de verdade (o robô joga), com o grupo inteiro e cheio de vida, contra Esqueletos resistentes e de golpe
    fraco (a luta dura e todos agem: o robô sozinho perde para os do nível dele); devolve o que as gravações fizeram."""
    g.encanto_log = []
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    for m in D.comitiva.membros(g):
        m["hp"] = m["max_hp"]
    rng = random.Random(g.rng.random())
    try:
        inimigos = [criar(rng, "esqueleto", nivel or g.j.nivel) for _ in range(n)]
        for e in inimigos:
            e.max_hp = e.hp = 70
            e.atk = max(1, e.atk * 0.3)
        g.combate(inimigos, pode_fugir=False, titulo="teste", saque=False)
    except Exception as e:  # a derrota não importa aqui, só o que disparou
        if type(e).__name__ != "Derrota":
            raise
    return list(g.encanto_log)


class TestGravar(unittest.TestCase):
    def test_grava_uma_vez_cobra_essencia_e_ouro(self):
        g = jogo()
        arma = g.j.equip["arma"]
        ouro, ess = g.j.ouro, D.materiais(g)["essencia_brasa"]
        ok, _ = D.encantar(g, arma["uid"], "brasa", pedido="a")
        self.assertTrue(ok)
        self.assertEqual(arma["encantos"][0], "brasa")
        self.assertEqual(g.j.ouro, ouro - g.preco(E.CUSTO_OURO))
        self.assertEqual(D.materiais(g)["essencia_brasa"], ess - 1)
        # o mesmo pedido de novo (clique duplo, tecla segurada): nada
        self.assertEqual(D.encantar(g, arma["uid"], "carrasco", pedido="a"), (False, None))
        self.assertEqual(arma["encantos"][0], "brasa")
        self.assertEqual(g.j.ouro, ouro - g.preco(E.CUSTO_OURO))

    def test_substituir_pede_a_gravacao_vista_e_apaga_a_anterior(self):
        g = jogo()
        arma = g.j.equip["arma"]
        D.encantar(g, arma["uid"], "brasa", pedido="a")
        ouro = g.j.ouro
        # sem dizer o que substitui (a tela não mostrou a confirmação): recusa, sem cobrar
        ok, _ = D.encantar(g, arma["uid"], "carrasco", pedido="b")
        self.assertFalse(ok)
        self.assertEqual((arma["encantos"][0], g.j.ouro), ("brasa", ouro))
        ok, _ = D.encantar(g, arma["uid"], "carrasco", pedido="c", substitui="brasa")
        self.assertTrue(ok)
        self.assertEqual(arma["encantos"][0], "carrasco")
        self.assertEqual(D.materiais(g)["essencia_brasa"], 1)  # a Brasa gasta não volta
        self.assertEqual(g.forja_ultimo["de"]["id"], "brasa")
        # a mesma essência que já está: recusa (no mesmo sulco e no outro)
        self.assertFalse(D.encantar(g, arma["uid"], "carrasco", pedido="d", substitui="carrasco")[0])
        self.assertFalse(D.encantar(g, arma["uid"], "carrasco", 1, pedido="e")[0])

    def test_sulcos_sorteados_e_o_segundo_sulco(self):
        g = jogo()
        arma = g.j.equip["arma"]
        self.assertEqual(arma["encantos"], [None, None])  # o cenário: a arma do herói com 2 sulcos
        for it, _, _ in D.pecas(g):
            if E.tipo(it):
                self.assertTrue(1 <= len(it["encantos"]) <= 3, it["nome"])
        self.assertTrue(D.encantar(g, arma["uid"], "brasa", 0, pedido="a")[0])
        self.assertTrue(D.encantar(g, arma["uid"], "eco", 1, pedido="b")[0])
        self.assertEqual(arma["encantos"], ["brasa", "eco"])
        self.assertFalse(D.encantar(g, arma["uid"], "carrasco", 2, pedido="c")[0])  # não há terceiro sulco
        # as duas valem na luta (cada uma uma vez)
        self.assertEqual(E.encantos(g.j), {"brasa", "eco"})

    def test_elegibilidade_e_falta(self):
        g = jogo()
        arma, peito = g.j.equip["arma"], g.j.equip["armadura"]
        self.assertFalse(D.encantar(g, arma["uid"], "geada", pedido="a")[0])  # Geada: só peito
        self.assertTrue(D.encantar(g, peito["uid"], "geada", pedido="b")[0])
        anel = next(it for it in g.j.mochila if it.get("slot") == "anel")
        self.assertIsNotNone(E.motivo(anel))
        D.materiais(g)["essencia_eco"] = 0
        ouro = g.j.ouro
        self.assertFalse(D.encantar(g, arma["uid"], "eco", pedido="c")[0])
        self.assertEqual(g.j.ouro, ouro)

    def test_a_gravacao_vai_com_a_peca_e_some_ao_desmontar(self):
        g = jogo()
        arma = g.j.equip["arma"]
        D.encantar(g, arma["uid"], "eco", pedido="a")
        FICHA.tirar(g, FICHA.HEROI, "arma")
        self.assertIn(arma, g.j.mochila)
        FICHA.vestir(g, "morel", arma)
        self.assertIs(FICHA.corpo(g, "morel")["arma"], arma)
        self.assertEqual(arma["encantos"][0], "eco")
        # na ficha das telas (dicas, inventário), a gravação aparece
        self.assertEqual(D.itens.ficha(arma)["encantos"][0]["id"], "eco")
        self.assertIn("Gravação · Eco", D.itens.ficha(arma)["efeito"])
        # desmontar uma peça gravada: rende o mesmo do reforço; a gravação some com a peça
        FICHA.tirar(g, "morel", "arma")
        antes = D.materiais(g).get("essencia_eco", 0)
        ok, _ = D.desmontar(g, arma["uid"], arma["nome"])
        if ok:
            self.assertEqual(D.materiais(g).get("essencia_eco", 0), antes)


class TestNaLuta(unittest.TestCase):
    def test_cada_gravacao_dispara_numa_luta_de_verdade(self):
        g = jogo()
        g.j.equip["arma"]["encantos"] = ["brasa"]
        g.j.equip["armadura"]["encantos"] = ["vigilia"]
        FICHA.corpo(g, "morel")["armadura"]["encantos"] = ["revide"]
        FICHA.corpo(g, "odete")["arma"]["encantos"] = ["eco"]
        visto = set()
        for _ in range(8):
            visto |= {k for k, _ in lutar(g, n=3)}
            if {"brasa", "vigilia", "revide"} <= visto:
                break
        self.assertTrue({"brasa", "vigilia", "revide"} <= visto, visto)

    def test_geada_numa_luta_de_verdade(self):
        g = jogo()
        g.j.equip["armadura"]["encantos"] = ["geada"]
        visto = set()
        for _ in range(10):
            visto |= {k for k, _ in lutar(g, n=3)}
            if "geada" in visto:
                break
        self.assertIn("geada", visto)

    def _luta_montada(self, g):
        from rpg.combate import Combate
        cb = Combate(g, [criar(random.Random(2), "esqueleto", g.j.nivel)])
        cb.memoria = getattr(cb, "memoria", None) or {}
        return cb, cb.inimigos[0]

    def test_carrasco_soma_30_por_cento_abaixo_de_35(self):
        g = jogo()
        cb, alvo = self._luta_montada(g)
        alvo.hp = int(alvo.max_hp * 0.3)
        danos = []
        for gravado in (None, "carrasco"):
            g.j.equip["arma"]["encantos"] = [gravado]
            alvo.hp = int(alvo.max_hp * 0.3)
            g.rng.seed(5)
            danos.append(cb.atacar(cb.j, alvo, 1.0, pode_esquivar=False))
        self.assertAlmostEqual(danos[1] / danos[0], 1.3, delta=0.08)
        # acima de 35% da vida, igual
        alvo.hp = alvo.max_hp
        g.rng.seed(5)
        cheio = cb.atacar(cb.j, alvo, 1.0, pode_esquivar=False)
        g.j.equip["arma"]["encantos"] = [None]
        alvo.hp = alvo.max_hp
        g.rng.seed(5)
        self.assertEqual(cb.atacar(cb.j, alvo, 1.0, pode_esquivar=False), cheio)

    def test_eco_devolve_recurso_ate_duas_vezes(self):
        g = jogo()
        cb, _ = self._luta_montada(g)
        g.j.equip["arma"]["encantos"] = ["eco"]
        ganhos = []
        for i in range(3):
            e = criar(random.Random(10 + i), "esqueleto", 1)
            cb.inimigos.append(e)
            g.j.rec = 0
            e.hp = 0
            cb.ao_morrer(e, por=cb.j)
            ganhos.append(g.j.rec)
        self.assertEqual(ganhos[:2], [round(g.j.max_rec * 0.25)] * 2)
        self.assertEqual(ganhos[2], 0)

    def test_limites_e_nada_acumula_entre_lutas(self):
        g = jogo()
        g.j.equip["armadura"]["encantos"] = ["vigilia"]
        g.j.equip["arma"]["encantos"] = ["eco"]
        for _ in range(3):
            log = lutar(g, n=3)
            self.assertEqual(sum(1 for k, q in log if k == "vigilia"), 1)  # uma barreira por luta
            self.assertLessEqual(sum(1 for k, q in log if k == "eco" and q == g.j.nome), 2)  # até 2 por luta

    def test_o_mesmo_efeito_conta_uma_vez_e_o_revide_nao_se_repete(self):
        g = jogo()
        corpo = FICHA.corpo(g, "morel")
        corpo["armadura"]["encantos"] = ["revide", "revide"]  # mesmo forçado em dois sulcos
        if corpo.get("secundaria"):
            corpo["secundaria"]["encantos"] = ["revide"]
        self.assertEqual(E.encantos(type("U", (), {"equip": corpo})()), {"revide"})
        for _ in range(4):
            log = lutar(g, n=3)
            self.assertLess(sum(1 for k, _ in log if k == "revide"), 40)

    def test_luta_de_teste_devolve_o_grupo_como_estava(self):
        g = jogo()
        g.j.equip["armadura"]["encantos"] = ["vigilia"]
        g.ui.efeito = lambda *a, **k: None
        antes = (g.j.hp, g.j.rec, g.j.xp, g.j.ouro)
        D.luta_de_teste(g)
        self.assertEqual((g.j.hp, g.j.rec, g.j.xp, g.j.ouro), antes)
        self.assertNotIn("barreira", g.j.efeitos)
        self.assertIn("vigilia", [k for k, _ in g.lutas_teste[-1]])


if __name__ == "__main__":
    unittest.main()
