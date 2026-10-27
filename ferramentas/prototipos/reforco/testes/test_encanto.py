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
        for t in E.TIERS:
            D.materiais(g)[E.material(k, t)] = 2
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

    def test_substituicao_identica_e_recusada_sem_cobrar(self):
        g = jogo()
        arma = g.j.equip["arma"]
        D.materiais(g)["essencia_carrasco_3"] = 3
        self.assertTrue(D.encantar(g, arma["uid"], "carrasco:3", 0, pedido="a")[0])
        ouro, qtd = g.j.ouro, D.materiais(g)["essencia_carrasco_3"]
        self.assertEqual(D.encantar(g, arma["uid"], "carrasco:3", 0, pedido="b", substitui="carrasco:3"), (False, "Já gravado."))
        self.assertEqual((g.j.ouro, D.materiais(g)["essencia_carrasco_3"], arma["encantos"][0]), (ouro, qtd, "carrasco:3"))
        # outro tier da mesma essência muda o nível: é uma substituição de verdade
        self.assertTrue(D.encantar(g, arma["uid"], "carrasco", 0, pedido="c", substitui="carrasco:3")[0])

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
        # repetir é permitido (28/10): a mesma essência no outro sulco; substituir por ela mesma num tier maior também
        self.assertTrue(D.encantar(g, arma["uid"], "carrasco", 1, pedido="d")[0])
        D.materiais(g)["essencia_carrasco_2"] = 1
        self.assertTrue(D.encantar(g, arma["uid"], "carrasco:2", 0, pedido="e", substitui="carrasco")[0])
        self.assertEqual(arma["encantos"], ["carrasco:2", "carrasco"])
        self.assertEqual(E.niveis_peca(arma), {"carrasco": 3})

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
        # as duas valem na luta, cada uma no nível dela
        self.assertEqual((E.nivel(g.j, "brasa"), E.nivel(g.j, "eco"), E.nivel(g.j, "carrasco")), (1, 1, 0))

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
        self.assertNotIn("Gravação", D.itens.ficha(arma).get("efeito") or "")  # a gravação tem a seção dela, fora do efeito
        # desmontar uma peça gravada: rende o mesmo do reforço; a gravação some com a peça
        FICHA.tirar(g, "morel", "arma")
        antes = D.materiais(g).get("essencia_eco", 0)
        ok, _ = D.desmontar(g, arma["uid"], arma["nome"])
        if ok:
            self.assertEqual(D.materiais(g).get("essencia_eco", 0), antes)


class TestSulcosDaPeca(unittest.TestCase):
    def test_nascem_com_a_peca_e_a_ficha_so_le(self):
        g = jogo()
        r1, r2 = random.Random(9), random.Random(9)
        nova = D.itens.gerar_equip(r1, "guerreiro", 5, slot="arma", raridade="raro")
        self.assertTrue(1 <= len(nova["encantos"]) <= 3)  # a capacidade nasce com a peça (o drop)
        primeiro = list(nova["encantos"])
        # o sorteio dos sulcos não gasta o sorteio do jogo: o mesmo estado que a criação sem o laboratório deixaria
        import rpg.itens as itens_jogo
        original = itens_jogo.gerar_equip.__closure__[0].cell_contents if itens_jogo.gerar_equip.__closure__ else None
        if callable(original):
            original(r2, "guerreiro", 5, slot="arma", raridade="raro")
            self.assertEqual(r1.getstate(), r2.getstate())
        nova["nome"] += " +2"  # consultar ou redesenhar a ficha, mesmo com a peça mudada, não mexe na capacidade
        for _ in range(5):
            self.assertEqual(D.itens.ficha(nova)["encantos"], [None] * len(primeiro))
        self.assertEqual(nova["encantos"], primeiro)
        sem = {k: v for k, v in nova.items() if k != "encantos"}
        D.itens.ficha(sem)
        self.assertNotIn("encantos", sem)  # a ficha nunca decide a capacidade
        for it, _, _ in D.pecas(g):  # as peças do cenário já têm os delas antes de qualquer tela
            if E.tipo(it):
                self.assertIn("encantos", it)

    def test_todo_lugar_que_cria_pecas_usa_a_criacao_com_sulcos(self):
        # o mercado e o saque importaram a função pelo nome: o estoque e o espólio também nascem com os sulcos
        for nome, m in list(sys.modules.items()):
            if nome.startswith("rpg") and getattr(m, "gerar_equip", None) is not None:
                self.assertIs(m.gerar_equip, D.itens.gerar_equip, nome)
        g = jogo()
        estoque = g.estoque()  # o mercado da vila (o Jogo é a Loja)
        self.assertTrue(estoque)
        for it in estoque:
            if E.tipo(it):
                self.assertIn("encantos", it)

    def test_salvar_e_carregar_mantem_sulcos_gravacoes_e_reforco(self):
        g = jogo()
        arma = g.j.equip["arma"]
        D.encantar(g, arma["uid"], "brasa", 1, pedido="a")
        D.materiais(g)["fragmento"] = 9
        D.reforcar(g, arma["uid"], veio="fio", pedido="b")
        g.salvar(silencioso=True)
        from rpg.jogo import Jogo as J
        h = J.carregar(BotUI(random.Random(1)), g.caminho_save(), pasta_saves=g.pasta_saves)
        arma2 = h.j.equip["arma"]
        self.assertEqual(arma2["encantos"], [None, "brasa"])
        self.assertEqual(arma2["reforco"], 1)
        self.assertEqual(D.itens.ficha(arma2)["encantos"][1]["id"], "brasa")
        self.assertEqual(D.itens.ficha(arma2)["reforco"], 1)


class TestNaLuta(unittest.TestCase):
    def test_cada_gravacao_dispara_numa_luta_de_verdade(self):
        g = jogo()
        g.j.equip["arma"]["encantos"] = ["brasa"]
        g.j.equip["armadura"]["encantos"] = ["vigilia"]
        FICHA.corpo(g, "morel")["armadura"]["encantos"] = ["revide"]
        FICHA.corpo(g, "odete")["arma"]["encantos"] = ["eco"]
        visto = set()
        for _ in range(8):
            visto |= {k for k, *_ in lutar(g, n=3)}
            if {"brasa", "vigilia", "revide"} <= visto:
                break
        self.assertTrue({"brasa", "vigilia", "revide"} <= visto, visto)

    def test_geada_numa_luta_de_verdade(self):
        g = jogo()
        g.j.equip["armadura"]["encantos"] = ["geada"]
        visto = set()
        for _ in range(10):
            visto |= {k for k, *_ in lutar(g, n=3)}
            if "geada" in visto:
                break
        self.assertIn("geada", visto)

    def _luta_montada(self, g):
        from rpg.combate import Combate
        cb = Combate(g, [criar(random.Random(2), "esqueleto", g.j.nivel)])
        cb.memoria = getattr(cb, "memoria", None) or {}
        return cb, cb.inimigos[0]

    def test_carrasco_pela_tabela_abaixo_de_35(self):
        g = jogo()
        cb, alvo = self._luta_montada(g)
        for gravado, esperado in ((["carrasco", None], 1.20), (["carrasco:2", "carrasco"], 1.30)):  # nível 1: +20%; 3: +30%
            danos = []
            for lista in ([None, None], gravado):
                g.j.equip["arma"]["encantos"] = lista
                alvo.hp = int(alvo.max_hp * 0.3)
                alvo.max_hp = alvo.hp = 10000
                alvo.hp = 3000
                g.rng.seed(5)
                danos.append(cb.atacar(cb.j, alvo, 8.0, pode_esquivar=False))  # um golpe grande: o arredondamento some
            self.assertAlmostEqual(danos[1] / danos[0], esperado, delta=0.03)
        g.j.equip["arma"]["encantos"] = ["carrasco"]
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
        self.assertEqual(ganhos[:2], [round(g.j.max_rec * 0.15)] * 2)  # Eco 1: 15% (a tabela)
        self.assertEqual(ganhos[2], 0)

    def test_limites_e_nada_acumula_entre_lutas(self):
        g = jogo()
        g.j.equip["armadura"]["encantos"] = ["vigilia"]
        g.j.equip["arma"]["encantos"] = ["eco"]
        for _ in range(3):
            log = lutar(g, n=3)
            self.assertEqual(sum(1 for k, q, _ in log if k == "vigilia"), 1)  # uma barreira por luta
            self.assertLessEqual(sum(1 for k, q, _ in log if k == "eco" and q == g.j.nome), 2)  # até 2 por luta

    def test_revide_pelo_nivel_total_e_no_maximo_2_por_rodada(self):
        g = jogo()
        corpo = FICHA.corpo(g, "morel")
        corpo["armadura"]["encantos"] = ["revide:3", "revide:2", "revide"]  # 6 níveis: o teto (5) vale
        u = type("U", (), {"equip": corpo})()
        self.assertEqual((E.niveis_equip(corpo)["revide"], E.nivel(u, "revide")), (6, 5))
        for _ in range(3):
            log = lutar(g, n=3)
            # um efeito só (não uma instância por essência), sempre no nível 5
            self.assertTrue(all(n == 5 for k, _, n in log if k == "revide"))
        # 30 golpes corpo a corpo na mesma rodada: no máximo 2 respostas
        g.j.equip["armadura"]["encantos"] = ["revide:3", "revide:2"]
        cb, e = self._luta_montada(g)
        g.encanto_log = []
        g.rng.seed(1)
        for _ in range(30):
            e.hp, cb.j.hp = e.max_hp, cb.j.max_hp
            E.ao_golpear(cb, e, cb.j, 5, "corpo", False, None)
        self.assertLessEqual(sum(1 for k, *_ in g.encanto_log if k == "revide"), 2)

    def test_luta_de_teste_devolve_o_grupo_como_estava(self):
        g = jogo()
        g.j.equip["armadura"]["encantos"] = ["vigilia"]
        g.ui.efeito = lambda *a, **k: None
        antes = (g.j.hp, g.j.rec, g.j.xp, g.j.ouro)
        D.luta_de_teste(g)
        self.assertEqual((g.j.hp, g.j.rec, g.j.xp, g.j.ouro), antes)
        self.assertNotIn("barreira", g.j.efeitos)
        self.assertIn("vigilia", [k for k, *_ in g.lutas_teste[-1]])



class TestTiers(unittest.TestCase):
    def test_tiers_somam_e_so_conta_o_que_o_personagem_veste(self):
        g = jogo()
        arma, peito = g.j.equip["arma"], g.j.equip["armadura"]
        arma["encantos"] = ["brasa", "brasa"]  # duas Brasas I: Brasa 2
        self.assertEqual(E.nivel(g.j, "brasa"), 2)
        arma["encantos"] = ["brasa:2", "brasa"]  # Brasa II + Brasa I: Brasa 3
        self.assertEqual(E.nivel(g.j, "brasa"), 3)
        odete = FICHA.corpo(g, "odete")  # entre peças: o Eco na arma e no tomo de quem veste os dois
        odete["arma"]["encantos"] = ["eco:2"]
        odete["secundaria"]["encantos"] = ["eco:3", "eco:2"]
        self.assertEqual(E.niveis_equip(odete)["eco"], 7)
        self.assertEqual(E.nivel(type("U", (), {"equip": odete})(), "eco"), E.TETO)
        bolsa = next(it for it in g.j.mochila if E.tipo(it))  # a bolsa e as peças dos outros não contam
        bolsa["encantos"] = ["vigilia:3"] + [None] * (len(bolsa["encantos"]) - 1)
        self.assertEqual(E.nivel(g.j, "vigilia"), 0)
        peito["encantos"] = ["vigilia"] + [None] * (len(peito["encantos"]) - 1)
        self.assertEqual(E.nivel(g.j, "vigilia"), 1)

    def test_brasa_em_area_aplica_uma_vez_por_rodada(self):
        g = jogo()
        g.j.equip["arma"]["encantos"] = ["brasa:3", "brasa:2"]  # Brasa 5: 53%
        from rpg.combate import Combate
        alvos = [criar(random.Random(20 + i), "esqueleto", g.j.nivel) for i in range(4)]
        cb = Combate(g, alvos)
        cb.memoria = getattr(cb, "memoria", None) or {}
        for rodada in (1, 2):
            cb.turno = rodada
            g.encanto_log = []
            for _ in range(5):  # um golpe em área: os quatro alvos, cinco vezes na mesma rodada
                for a in alvos:
                    a.hp = a.max_hp
                    E.ao_golpear(cb, cb.j, a, 5, "corpo", False, None)
            self.assertEqual(sum(1 for k, *_ in g.encanto_log if k == "brasa"), 1)

    def test_os_textos_saem_da_tabela_de_cada_nivel(self):
        for k in E.ORDEM:
            textos = [E.texto(k, n)[0] for n in range(1, E.TETO + 1)]
            self.assertEqual(len(set(textos)), E.TETO, k)  # cada nível diz o seu número
        self.assertEqual(E.texto("eco", 1), ("Ao abater um inimigo, recupera 15% do recurso máximo.", "Até 2 vezes por luta."))
        self.assertEqual(E.texto("brasa", 9), E.texto("brasa", E.TETO))  # acima do teto, o do teto

    def test_a_ficha_mostra_o_total_de_quem_veste(self):
        g = jogo()
        g.j.equip["arma"]["encantos"] = ["brasa:2", "brasa"]
        D.JOGO[0] = g
        f = D.itens.ficha(g.j.equip["arma"])
        tot = {x["id"]: x for x in f["gravacao_total"]}
        self.assertEqual((tot["brasa"]["total"], tot["brasa"]["efetivo"]), (3, 3))
        self.assertEqual([x["titulo"] for x in f["encantos"]], ["Brasa II", "Brasa I"])
        bolsa = next(it for it in g.j.mochila if E.tipo(it))
        self.assertEqual(D.itens.ficha(bolsa)["gravacao_total"], [])  # na bolsa: ninguém veste

    def test_o_saque_de_verdade_da_materiais_pela_criatura(self):
        g = jogo()
        g.ui.efeito = lambda *a, **k: None
        antes = dict(D.materiais(g))
        chefe = criar(random.Random(4), "lobo_gelido", 6)
        chefe.chefe = True
        g.saque_de_combate([chefe])
        m = D.materiais(g)
        self.assertGreaterEqual(m.get("fragmento", 0) - antes.get("fragmento", 0), 3)  # o chefe: 2 + 1 no nível 6
        self.assertEqual(m.get("essencia_geada_3", 0) - antes.get("essencia_geada_3", 0), 1)  # lobo gélido: Geada; II + 1


if __name__ == "__main__":
    unittest.main()
