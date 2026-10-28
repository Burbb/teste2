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
        g.j.nivel = 9  # o requisito do tier III (vestida)
        D.materiais(g)["essencia_carrasco_3"] = 3
        self.assertTrue(D.encantar(g, arma["uid"], "carrasco:3", 0, pedido="a")[0])
        ouro, qtd = g.j.ouro, D.materiais(g)["essencia_carrasco_3"]
        self.assertEqual(D.encantar(g, arma["uid"], "carrasco:3", 0, pedido="b", substitui="carrasco:3"), (False, "Já gravado."))
        self.assertEqual((g.j.ouro, D.materiais(g)["essencia_carrasco_3"], arma["encantos"][0]), (ouro, qtd, "carrasco:3"))
        # outro tier da mesma essência muda o valor: é uma substituição de verdade
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
        g.j.nivel = 5  # o requisito do tier II (vestida)
        D.materiais(g)["essencia_carrasco_2"] = 1
        self.assertTrue(D.encantar(g, arma["uid"], "carrasco:2", 0, pedido="e", substitui="carrasco")[0])
        self.assertEqual(arma["encantos"], ["carrasco:2", "carrasco"])
        self.assertEqual(E.soma_peca(arma), {"carrasco": 22 + 15})  # Carrasco II + Carrasco I: os valores somam

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
        # as duas valem na luta, cada uma com o valor do tier dela
        self.assertEqual((E.valor(g.j, "brasa"), E.valor(g.j, "eco"), E.valor(g.j, "carrasco")), (20, 10, 0))

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
        for gravado, esperado in ((["carrasco", None], 1.15), (["carrasco:2", "carrasco"], 1.37)):  # I: +15%; II + I: +37%
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
        self.assertEqual(ganhos[:2], [round(g.j.max_rec * 0.10)] * 2)  # Eco I: 10% (a tabela)
        self.assertEqual(ganhos[2], 0)

    def test_limites_e_nada_acumula_entre_lutas(self):
        g = jogo()
        g.j.equip["armadura"]["encantos"] = ["vigilia"]
        g.j.equip["arma"]["encantos"] = ["eco"]
        for _ in range(3):
            log = lutar(g, n=3)
            self.assertEqual(sum(1 for k, q, _ in log if k == "vigilia"), 1)  # uma barreira por luta
            self.assertLessEqual(sum(1 for k, q, _ in log if k == "eco" and q == g.j.nome), 2)  # até 2 por luta

    def test_revide_pela_soma_ate_o_limite_e_no_maximo_2_por_rodada(self):
        g = jogo()
        corpo = FICHA.corpo(g, "morel")
        corpo["armadura"]["encantos"] = ["revide:3", "revide:2", "revide"]  # 24 + 18 + 12 = 54%: o limite (40%) vale
        u = type("U", (), {"equip": corpo})()
        self.assertEqual((E.soma_equip(corpo)["revide"], E.valor(u, "revide")), (54, 40))
        for _ in range(3):
            log = lutar(g, n=3)
            # um efeito só (não uma instância por essência), sempre com 40%
            self.assertTrue(all(n == 40 for k, _, n in log if k == "revide"))
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
    def test_cada_tier_tem_o_seu_valor_e_a_repeticao_soma_ate_o_limite(self):
        g = jogo()
        arma, peito = g.j.equip["arma"], g.j.equip["armadura"]
        for lista, esperado in ((["brasa", None], 20), (["brasa:2", None], 28), (["brasa:3", None], 36),  # um de cada
                                (["brasa", "brasa"], 40), (["brasa:2", "brasa"], 48),  # iguais e misturados
                                (["brasa:3", "brasa:3"], 60)):  # 72%: o limite da Brasa (60%) corta
            arma["encantos"] = lista
            self.assertEqual(E.valor(g.j, "brasa"), esperado, lista)
        odete = FICHA.corpo(g, "odete")  # entre peças: o Eco na arma e no tomo de quem veste os dois
        odete["arma"]["encantos"] = ["eco:2"]
        odete["secundaria"]["encantos"] = ["eco:3", "eco:2"]
        self.assertEqual(E.soma_equip(odete)["eco"], 15 + 20 + 15)
        self.assertEqual(E.valor(type("U", (), {"equip": odete})(), "eco"), 35)  # o limite do Eco
        bolsa = next(it for it in g.j.mochila if E.tipo(it))  # a bolsa e as peças dos outros não contam
        bolsa["encantos"] = ["vigilia:3"] + [None] * (len(bolsa["encantos"]) - 1)
        self.assertEqual(E.valor(g.j, "vigilia"), 0)
        peito["encantos"] = ["vigilia"] + [None] * (len(peito["encantos"]) - 1)
        self.assertEqual(E.valor(g.j, "vigilia"), 8)
        for k, e in E.ESSENCIAS.items():  # o tier maior vale mais; três do maior passam do limite
            self.assertTrue(e["valores"][0] < e["valores"][1] < e["valores"][2] < e["limite"] <= 3 * e["valores"][2], k)

    def test_brasa_em_area_aplica_uma_vez_por_rodada(self):
        g = jogo()
        g.j.equip["arma"]["encantos"] = ["brasa:3", "brasa:2"]  # 64%: o limite, 60%
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

    def test_os_textos_saem_do_valor_de_cada_tier(self):
        for k in E.ORDEM:
            textos = [D.encanto_tela(E.chave(k, t))["efeito"] for t in E.TIERS]
            self.assertEqual(len(set(textos)), 3, k)  # cada tier diz o seu número
        self.assertEqual(E.texto("eco", 10), ("Ao abater um inimigo, recupera 10% do recurso máximo.", "Até 2 vezes por luta."))
        self.assertEqual(D.encanto_tela("revide:3")["efeito"],
                         "Ao receber um golpe corpo a corpo, 24% de chance de revidar com 60% do Ataque.")

    def test_a_ficha_mostra_o_que_a_peca_fornece(self):
        g = jogo()
        g.j.equip["arma"]["encantos"] = ["brasa:2", "brasa"]
        D.JOGO[0] = g
        f = D.itens.ficha(g.j.equip["arma"])
        self.assertEqual([x["titulo"] for x in f["encantos"]], ["Brasa II", "Brasa I"])
        self.assertEqual([(x["id"], x["valor"]) for x in f["efeitos"]], [("brasa", "48%")])  # a peça, sem totais
        self.assertEqual(f["gravacao_total"], [])  # nenhum total de quem veste na ficha (o campo é das versões guardadas)
        g.j.equip["arma"]["encantos"] = ["brasa:3", "brasa:3"]
        ef = D.itens.ficha(g.j.equip["arma"])["efeitos"][0]
        self.assertEqual((ef["valor"], ef["excede"]), ("60%", True))  # nunca um número acima do limite como o ativo

    def test_previa_da_troca_e_do_limite(self):
        g = jogo()
        arma = g.j.equip["arma"]
        arma["encantos"] = ["brasa:3", "carrasco"]
        p = D.previsao(g, arma, D.HEROI, 1, "brasa:2")  # Carrasco I sai, Brasa II entra
        self.assertEqual([(x["rotulo"], x["antes"], x["depois"]) for x in p["linhas"]],
                         [("Brasa", "36%", "60%"), ("Carrasco", "15%", "—")])  # o nome basta na peça escolhida
        self.assertIn("Limite 60%", p["aviso"])  # 36 + 28 = 64: 4% não valem
        self.assertEqual(D.previsao(g, arma, D.HEROI, 0, "brasa:3")["bloqueio"], "Já gravado.")


class TestRequisitos(unittest.TestCase):
    def test_a_tabela_e_o_requisito_da_peca_gravada(self):
        self.assertEqual((E.REQUISITO[1], E.REQUISITO[2], E.REQUISITO[3]), (1, 5, 9))
        it = {"nivel": 5, "encantos": [None, None]}
        self.assertEqual(E.requisito(it), 4)  # um abaixo do nível em que a peça nasceu
        self.assertEqual(E.requisito({"nivel": 1}), 1)
        self.assertEqual(E.requisito(it, ["brasa:2", None]), 5)  # o maior entre a peça e as gravações
        self.assertEqual(E.requisito(it, ["brasa", "eco:3"]), 9)
        it["reforco"] = 12
        self.assertEqual(E.requisito(it), 4)  # o reforço não muda o requisito

    def test_bloqueia_vestir_abaixo_do_nivel_em_todos_os_caminhos(self):
        g = jogo()
        alta = next(it for it in g.j.mochila if it["slot"] == "arma" and E.requisito(it) > g.j.nivel)  # a substituta
        motivo = f"Requer nível {E.requisito(alta)}."
        self.assertEqual(FICHA.motivo_nao_veste(g, D.HEROI, alta), motivo)
        self.assertEqual(FICHA.vestir(g, D.HEROI, alta), (False, motivo))  # Inventário: duplo clique, menu, arrastar
        self.assertEqual(FICHA.vestir(g, "morel", alta), (False, motivo))  # o companheiro, pelo nível dele
        self.assertFalse(g.pode_usar(alta))  # o achado, o mercado e a troca de arma na luta
        self.assertIn(alta, g.j.mochila)
        baixa = next(it for it in g.j.mochila if it["slot"] == "arma" and it is not alta and not D.FICHA._nao_veste_classe(g, D.HEROI, it)
                     and E.requisito(it) <= g.j.nivel)
        self.assertTrue(FICHA.vestir(g, D.HEROI, baixa)[0])

    def test_achado_acima_do_nivel_diz_o_requisito(self):
        g = jogo()
        alta = next(it for it in g.j.mochila if it["slot"] == "arma" and E.requisito(it) > g.j.nivel)
        g.j.mochila.remove(alta)
        vistos = []
        menu = g.menu
        g.menu = lambda titulo, opcoes, *a, **k: (vistos.extend(o[0] for o in opcoes), "guardar")[1]
        try:
            g.oferecer_equip(alta)
        finally:
            g.menu = menu
        self.assertIn(f"Guardar na mochila (requer nível {E.requisito(alta)})", vistos)
        self.assertNotIn("Equipar agora", vistos)

    def test_gravar_em_peca_vestida_respeita_o_nivel_e_na_bolsa_prepara(self):
        g = jogo()
        arma = g.j.equip["arma"]
        ouro, mat = g.j.ouro, D.materiais(g)["essencia_brasa_3"]
        ok, texto = D.encantar(g, arma["uid"], "brasa:3", 0, pedido="a")
        self.assertFalse(ok)
        self.assertTrue(texto.startswith("Requer nível 9"), texto)
        self.assertEqual((g.j.ouro, D.materiais(g)["essencia_brasa_3"], arma["encantos"][0]), (ouro, mat, None))  # nada cobrado
        self.assertTrue(D.encantar(g, arma["uid"], "brasa", 0, pedido="b")[0])  # o tier I serve no nível 4
        bolsa = next(it for it in g.j.mochila if it["slot"] == "arma" and E.tipo(it) and not D.FICHA._nao_veste_classe(g, D.HEROI, it))
        self.assertTrue(D.encantar(g, bolsa["uid"], "brasa:3", 0, pedido="c")[0])  # na bolsa: preparar para depois
        self.assertEqual(FICHA.motivo_nao_veste(g, D.HEROI, bolsa), "Requer nível 9.")
        D.nivel_de_teste(g)
        D.nivel_de_teste(g)  # 4 → 8 → 12
        self.assertIsNone(FICHA.motivo_nao_veste(g, D.HEROI, bolsa))
        self.assertTrue(FICHA.vestir(g, D.HEROI, bolsa)[0])


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
