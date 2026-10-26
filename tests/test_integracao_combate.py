"""A integração do combate (etapa 4, 1.211.0; roadmapIDEIAS/26): a ordem fixa pela Agilidade, a rodada, o Defender, a
ultimate uma vez por luta, o kit, os pontos de atributo, a vez da comitiva, a Pena num companheiro caído, a debandada e
o save (de agora e o migrado)."""

import copy
import random
import tempfile
import unittest

from rpg import atributos as atr
from rpg import balanceamento as bal
from rpg import comitiva as cm
from rpg import dev
from rpg import kit
from rpg.combate import Combate
from rpg.entidades import Jogador
from rpg.jogo import Jogo
from rpg.migracoes import migrar
from rpg.ui import BotUI


class Roteiro(BotUI):
    """Responde pela meta: a ação de quem age (`acao`), a habilidade (`habilidade`), o item (`usar_item`), o alvo
    (o primeiro) e quem recebe (`alvo` com o uid pedido). Sem roteiro, ataca."""

    def __init__(self, acoes=()):
        super().__init__(random.Random(1), max_decisoes=10 ** 6)
        self.acoes, self.lances, self.perguntas = list(acoes), [], []

    def escolher(self, pergunta, opcoes):
        self.perguntas.append(pergunta)
        metas = self.meta_opcoes or [None] * len(opcoes)
        if pergunta in ("Sua ação:",) or pergunta.startswith("Vez de "):
            quero = self.acoes.pop(0) if self.acoes else ("acao", "atacar")
            self.plano = quero
            chave, valor = quero[0], quero[1]
            if chave == "acao":
                return next(i for i, m in enumerate(metas) if m and m.get("acao") == valor)
            grupo = "habilidades" if chave == "habilidade" else "itens"
            return next(i for i, m in enumerate(metas) if m and m.get("acao") == grupo)
        if pergunta.startswith("Habilidades") or pergunta == "Usar qual item?":
            chave, valor = self.plano[0], self.plano[1]
            return next(i for i, m in enumerate(metas) if m and m.get(chave) == valor)
        if pergunta == "Em quem?" and len(self.plano) > 2:
            return next(i for i, m in enumerate(metas) if m and m.get("alvo") == self.plano[2])
        return 0

    def lance(self, tipo, **d):
        self.lances.append((tipo, d))


def jogo(classe="guerreiro", acoes=(), nivel=1, spec=None):
    g = Jogo(Roteiro(acoes), seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Teste", classe)
    if nivel > 1:
        dev.subir_ate(g, nivel, spec=spec)
    return g


def lobos(g, n=2, nivel=1):
    lista = [g.inimigo("lobo", nivel=nivel) for _ in range(n)]
    for e in lista:
        e.hp = e.max_hp = 500
    return lista


class TestOrdem(unittest.TestCase):
    def test_ordem_pela_agilidade_e_fixa(self):
        g = jogo()
        inimigos = lobos(g)
        inimigos[0].agi, inimigos[1].agi = g.j.agi + 5, 0
        cb = Combate(g, inimigos, pode_fugir=False)
        cb.ordem = cb._ordem_inicial()
        self.assertEqual(cb.ordem, [inimigos[0], g.j, inimigos[1]])
        inimigos[1].agi = 99  # a Agilidade muda no meio da luta: a ordem não
        self.assertEqual(cb.ordem[0], inimigos[0])

    def test_a_rodada_termina_depois_de_todos_inclusive_quem_perdeu_a_vez(self):
        g = jogo()
        rapido, lento = lobos(g)
        rapido.agi, lento.agi = g.j.agi + 5, 0
        rapido.aplicar("atordoado", 1)  # perde a vez da rodada 1
        cb = Combate(g, [rapido, lento], pode_fugir=False)

        class Para(Exception):
            pass
        vezes = []

        def escolher(pergunta, opcoes, original=g.ui.escolher):
            if pergunta == "Sua ação:":
                vezes.append(cb.turno)
                if len(vezes) == 2:
                    raise Para()
            return original(pergunta, opcoes)
        g.ui.escolher = escolher
        with self.assertRaises(Para):
            cb.executar()
        seq = [(t, d.get("de"), d.get("n")) for t, d in g.ui.lances if t in ("rodada", "acao", "pula")]
        r2 = seq.index(("rodada", None, 2))
        rodada1 = [de for t, de, _ in seq[:r2] if t == "acao"]
        self.assertNotIn(cb.uid(rapido), rodada1)  # atordoado: não agiu
        self.assertEqual(rodada1, ["j", cb.uid(lento)])  # a rodada só acaba depois do lento
        self.assertEqual(vezes, [1, 2])


class TestAcoes(unittest.TestCase):
    def test_defender_reduz_e_gasta_a_vez(self):
        g = jogo()
        (lobo,) = lobos(g, 1)
        cb = Combate(g, [lobo], pode_fugir=False)
        g.ui.acoes = [("acao", "defender")]
        cb.fase_jogador()
        ef = g.j.efeito("defendendo")
        self.assertIsNotNone(ef)
        self.assertEqual(ef["v"], bal.DEFENDER)
        self.assertEqual([t for t, _ in g.ui.lances].count("acao"), 1)

    def test_ultimate_uma_vez_por_luta(self):
        g = jogo("mago", nivel=6, spec="piromante")
        g.j.kit = ["conflagracao"]
        g.j.rec = g.j.max_rec = 500
        cb = Combate(g, lobos(g), pode_fugir=False)
        self.assertIsNone(cb.motivo_bloqueio("conflagracao"))
        g.ui.acoes = [("habilidade", "conflagracao")]
        cb.fase_jogador()
        self.assertEqual(cb.motivo_bloqueio("conflagracao"), "Ultimate já usada nesta luta")
        # na luta seguinte ela volta
        self.assertIsNone(Combate(g, lobos(g), pode_fugir=False).motivo_bloqueio("conflagracao"))

    def test_so_o_kit_vai_para_a_luta(self):
        g = jogo("mago", nivel=6, spec="piromante")
        g.j.kit = ["bola_fogo", "meditar"]
        cb = Combate(g, lobos(g), pode_fugir=False)
        self.assertEqual([m["habilidade"] for m in cb.metas_habilidades()], ["bola_fogo", "meditar"])


class TestKit(unittest.TestCase):
    def test_orcamento_espacos_e_uma_ultimate(self):
        g = jogo("mago", nivel=8, spec="piromante")
        j = g.j
        self.assertIsNone(kit.motivo_kit(j, ["conflagracao", "barreira", "brasa", "combustao"]))
        self.assertIn("orçamento", kit.motivo_kit(j, ["conflagracao", "barreira", "nevasca", "chuva_brasas"]))
        self.assertIn("No máximo 5", kit.motivo_kit(j, ["bola_fogo", "meditar", "lanca_gelo", "runa_fragil", "sifao",
                                                        "brasa"]))
        self.assertIn("Só habilidades", kit.motivo_kit(j, ["julgamento"]))

    def test_trocar_so_na_vila_e_na_fogueira(self):
        g = jogo("mago", nivel=4, spec="piromante")
        self.assertEqual(g.opcoes_kit()[0][1], ("kit", None))  # no texto, a linha do menu
        g.j.kit = ["bola_fogo"]
        g.mexer_kit("meditar")
        self.assertEqual(g.j.kit, ["bola_fogo", "meditar"])
        g.mexer_kit("bola_fogo")
        self.assertEqual(g.j.kit, ["meditar"])

    def test_aprender_entra_no_kit_se_couber(self):
        g = jogo("guerreiro")
        self.assertEqual(g.j.kit, ["golpe_pesado", "erguer_escudo"])
        g.subir_nivel()
        self.assertIn("investida", g.j.kit)


class TestAtributos(unittest.TestCase):
    def test_nivel_um_igual_ao_de_antes(self):
        for classe, (hp, atk, agi, rec) in {"guerreiro": (60, 9, 3, 30), "arqueiro": (52, 8, 8, 25),
                                            "mago": (42, 3, 4, 40)}.items():
            j = Jogador("T", classe)
            totais, _ = j.totais()
            self.assertEqual((totais["max_hp"], totais["atk"], totais["agi"], totais["max_rec"]), (hp, atk, agi, rec),
                             classe)
            self.assertEqual((j.hp, j.rec), (j.max_hp, j.max_rec), classe)

    def test_pontos_de_nivel_e_gasto(self):
        g = jogo()
        g.subir_nivel()
        self.assertEqual(g.j.pontos_atributo, atr.PONTOS_POR_NIVEL)
        atk = g.j.atk
        self.assertTrue(g.gastar_atributo("forca"))
        self.assertEqual(g.j.atk, atk + 1)
        self.assertEqual(g.j.pontos_atributo, atr.PONTOS_POR_NIVEL - 1)

    def test_tenacidade_pela_vontade_com_teto(self):
        j = Jogador("T", "guerreiro")
        self.assertAlmostEqual(atr.tenacidade(j), 5 * atr.TENACIDADE_POR_PONTO)
        j.atributos["vontade"] = 20
        self.assertEqual(atr.tenacidade(j), atr.TENACIDADE_TETO)

    def test_presenca_so_nos_testes_de_carisma(self):
        g = jogo()
        antes = g.mod_teste("carisma")
        g.j.presenca = atr.PRESENCA_INICIAL + 2
        self.assertEqual(g.mod_teste("carisma"), antes + 2)
        self.assertEqual(g.mod_teste("forca"), g.mod_teste("forca"))


class TestComitiva(unittest.TestCase):
    def test_pena_levanta_o_companheiro_no_mesmo_lugar(self):
        g = jogo()
        cm.recrutar(g, "morel")
        g.j.consumiveis["pena_fenix"] = 1
        cb = Combate(g, lobos(g), pode_fugir=False)
        cm.preparar_combate(cb)
        cb.ordem = cb._ordem_inicial()
        morel = next(a for a in cb.aliados if a.cid == "morel")
        lugar = cb.ordem.index(morel)
        morel.hp = 0
        g.ui.acoes = [("usar_item", "pena_fenix", cb.uid(morel))]
        cb.fase_jogador()
        self.assertTrue(morel.vivo)
        self.assertEqual(morel.hp, max(1, round(morel.max_hp * bal.PENA_COMPANHEIRO)))
        self.assertEqual(cb.ordem.index(morel), lugar)
        self.assertEqual(g.j.consumiveis["pena_fenix"], 0)

    def test_caido_fica_fora_ate_descansar(self):
        g = jogo()
        cm.recrutar(g, "morel")
        cb = Combate(g, lobos(g), pode_fugir=False)
        cm.preparar_combate(cb)
        next(a for a in cb.aliados if a.cid == "morel").hp = 0
        cm.encerrar_combate(cb, "vitoria")
        self.assertTrue(cm.membro(g, "morel")["ferido"])
        cb2 = Combate(g, lobos(g), pode_fugir=False)
        cm.preparar_combate(cb2)
        self.assertFalse([a for a in cb2.aliados if getattr(a, "cid", None) == "morel"])


class TestFimDaLuta(unittest.TestCase):
    def test_recurso_volta_cheio_e_a_vida_nao(self):
        g = jogo()
        (lobo,) = lobos(g, 1)
        lobo.hp = lobo.max_hp = 1
        g.j.rec, g.j.hp = 3, g.j.max_hp - 10
        Combate(g, [lobo], pode_fugir=False).executar()
        self.assertEqual(g.j.rec, g.j.max_rec)
        self.assertLess(g.j.hp, g.j.max_hp)

    def test_debandada_so_na_luta_comum(self):
        g = jogo()
        inimigos = lobos(g, 3)
        cb = Combate(g, inimigos, pode_fugir=True)
        cb.vida_inicial = sum(e.max_hp for e in inimigos)
        inimigos[0].hp = 0
        cb.mortos.append(inimigos[0])
        for e in inimigos[1:]:
            e.hp = 10
        self.assertTrue(cb._debandada())
        g2 = jogo()
        inimigos = lobos(g2, 3)
        cena = Combate(g2, inimigos, pode_fugir=True, titulo="A Despensa")
        cena.vida_inicial = sum(e.max_hp for e in inimigos)
        inimigos[0].hp = 0
        cena.mortos.append(inimigos[0])
        for e in inimigos[1:]:
            e.hp = 10
        self.assertFalse(cena._debandada())


class TestSave(unittest.TestCase):
    def test_salvar_e_carregar_atributos_kit_e_pontos(self):
        g = jogo("mago", nivel=4, spec="piromante")
        g.j.pontos_atributo = 3
        g.j.kit = ["bola_fogo", "brasa"]
        g.salvar(silencioso=True)
        g2 = Jogo.carregar(Roteiro(), g.caminho_save(), g.pasta_saves)
        self.assertEqual((g2.j.atributos, g2.j.kit, g2.j.pontos_atributo, g2.j.presenca),
                         (g.j.atributos, ["bola_fogo", "brasa"], 3, g.j.presenca))

    def test_migracao_mantem_os_totais_e_troca_o_fogo(self):
        g = jogo("mago", nivel=7, spec="piromante")
        d = {"versao": 6, "seed": 1, "jogador": copy.deepcopy(g.j.para_dict()), "mundo": {"locais": []}}
        j = d["jogador"]
        for k in ("atributos", "kit", "presenca", "pontos_atributo"):
            j.pop(k, None)
        j["habilidades"] = ["bola_fogo", "meditar", "inferno", "fenix"]
        # o herói de antes: a base com tudo (sem atributos)
        for stat, v in atr.contribuicao(g.j).items():
            j["base"][stat] += v
        antes = {k: round(getattr(g.j, k), 2) for k in ("max_hp", "atk", "poder", "max_rec", "agi")}
        m = migrar(d)["jogador"]
        self.assertIn("chuva_brasas", m["habilidades"])
        self.assertIn("conflagracao", m["habilidades"])
        self.assertNotIn("inferno", m["habilidades"])
        self.assertFalse(kit.motivo_kit(Jogador.de_dict(copy.deepcopy(m)), m["kit"]))
        novo = Jogador.de_dict(m)
        novo.recalcular()
        depois = {k: round(getattr(novo, k), 2) for k in antes}
        self.assertEqual(depois, antes)
        self.assertEqual(migrar(copy.deepcopy(migrar(copy.deepcopy(d)))), migrar(copy.deepcopy(d)))


if __name__ == "__main__":
    unittest.main()
