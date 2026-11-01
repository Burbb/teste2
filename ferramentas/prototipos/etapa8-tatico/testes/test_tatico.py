"""Testes do protótipo tático da etapa 8 (fora da suíte do jogo): a geometria (visão, caminhos, zona de controle), os
limites da vez, os deslocamentos forçados, a ocupação depois de mortes e invocações, a prévia igual ao efeito, o chão em
chamas, os golpes preparados, a IA que não fica presa e a verificação de fuga repetida.

    python -m unittest discover -s ferramentas/prototipos/etapa8-tatico/testes -t ferramentas/prototipos/etapa8-tatico
"""
import pathlib
import unittest

from motor import conteudo as C
from motor.combate import Combate
from motor.grade import Arena, atravessadas

RAIZ = pathlib.Path(__file__).resolve().parents[4]


def ate(cb, quem):
    for _ in range(80):
        if cb.fim or cb.aguardando == quem:
            return
        assert cb.encerrar()["ok"]
    raise AssertionError(f"a vez de {quem} não chegou")


def parados(*ids):
    return {i: {"parado": True} for i in ids}


def danos(cb, desde, causa=None):
    return [e for e in cb.eventos[desde:] if e["tipo"] == "dano" and (causa is None or e["causa"] == causa)]


class Geometria(unittest.TestCase):
    def test_visao(self):
        a = Arena(9, 7, rochas=[(4, 3)], agua=[(4, 5)])
        self.assertFalse(a.visao((2, 3), (6, 3), set()))          # a rocha no meio
        self.assertTrue(a.visao((2, 5), (6, 5), set()))           # a água deixa ver
        self.assertFalse(a.visao((2, 5), (6, 5), {(3, 5)}))       # uma unidade no meio bloqueia
        self.assertTrue(a.visao((2, 5), (6, 5), {(2, 5), (6, 5)}))  # as pontas não contam
        self.assertIn(("canto", (1, 0), (0, 1)), atravessadas((0, 0), (2, 2)))
        canto = Arena(9, 7, rochas=[(1, 0)])
        self.assertTrue(canto.visao((0, 0), (2, 2), set()))       # um lado do canto livre: vê
        canto = Arena(9, 7, rochas=[(1, 0), (0, 1)])
        self.assertFalse(canto.visao((0, 0), (2, 2), set()))      # os dois lados fechados: não vê

    def test_caminhos(self):
        a = Arena(9, 7, rochas=[(1, 0), (1, 1), (1, 2)], agua=[(1, 3)])
        tab = a.caminhos((0, 0), 6, {}, "aliado")
        self.assertNotIn((1, 0), tab)
        self.assertNotIn((1, 3), tab)
        self.assertEqual(tab[(2, 4)][0], 6)                       # contorna a parede e a água por baixo
        ocup = {(0, 1): "inimigo"}
        tab = a.caminhos((0, 0), 6, ocup, "aliado")
        self.assertNotIn((0, 2), tab)                              # inimigo fecha a coluna
        tab = a.caminhos((0, 0), 6, {(0, 1): "aliado"}, "aliado")
        self.assertIn((0, 2), tab)                                 # aliado se atravessa

    def test_zona_de_controle(self):
        cb = Combate("piromante", "aberto", inicio={"lobo#1": {"pos": (2, 3), "parado": True},
                                                     "lobo#2": {"parado": True}, "lobo#3": {"parado": True}})
        ate(cb, "heroi")
        mov = cb.movimentos()
        self.assertEqual(mov[(0, 3)]["custo"], 2)                  # sair de perto do lobo: 1 + 1
        self.assertNotIn((1, 6), mov)
        cb2 = Combate("piromante", "aberto", zona=0, inicio={"lobo#1": {"pos": (2, 3), "parado": True},
                                                             "lobo#2": {"parado": True}, "lobo#3": {"parado": True}})
        ate(cb2, "heroi")
        self.assertEqual(cb2.movimentos()[(0, 3)]["custo"], 1)


class Vez(unittest.TestCase):
    def test_limites_de_movimento_e_acao(self):
        cb = Combate("piromante", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        self.assertFalse(cb.mover((5, 3))["ok"])                    # 4 casas com 3 PM
        self.assertTrue(cb.mover((1, 1))["ok"])                     # 2 PM
        self.assertEqual(cb.heroi.pm, 1)
        self.assertFalse(cb.mover((3, 1))["ok"])                    # só sobra 1
        self.assertTrue(cb.mover((2, 1))["ok"])
        self.assertEqual(cb.heroi.pm, 0)

    def test_agir_encerra_o_movimento_e_uma_acao_por_vez(self):
        for depois in (False, True):
            cb = Combate("piromante", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"), mover_depois=depois)
            ate(cb, "heroi")
            self.assertTrue(cb.agir("defender", None)["ok"])
            self.assertEqual(cb.heroi.pm, 3 if depois else 0)
            self.assertFalse(cb.agir("defender", None)["ok"])

    def test_alvos(self):
        cb = Combate("piromante", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        bola = cb.alvos_validos(cb.heroi, "bola_fogo")
        self.assertNotIn(cb.u["morel"].pos, bola)                  # só inimigos
        self.assertNotIn(cb.u["lobo#1"].pos, bola)                 # a 6: fora do alcance
        cb.u["lobo#1"].pos = (4, 3)
        self.assertIn((4, 3), cb.alvos_validos(cb.heroi, "bola_fogo"))
        cb.u["morel"].pos = (2, 3)
        self.assertNotIn((4, 3), cb.alvos_validos(cb.heroi, "bola_fogo"))  # Morel no meio tapa a visão

    def test_investida_e_corrente_em_linha(self):
        cb = Combate("berserker", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        cb.u["lobo#1"].pos = (4, 3)
        self.assertIn((4, 3), cb.alvos_validos(cb.heroi, "investida"))
        cb.u["lobo#2"].pos = (5, 2)
        self.assertNotIn((5, 2), cb.alvos_validos(cb.heroi, "investida"))   # fora da linha
        cb.agir("investida", (4, 3))
        self.assertEqual(cb.heroi.pos, (3, 3))
        self.assertEqual(cb.heroi.pm, 0)                                     # agir encerra o movimento


class Deslocamentos(unittest.TestCase):
    def test_empurrao_contra_rocha_e_colisao(self):
        cb = Combate("berserker", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        lobo = cb.u["lobo#1"]
        cb.heroi.pos, lobo.pos = (2, 1), (3, 1)                    # rocha em (4, 1)
        vida = lobo.vida
        n = len(cb.eventos)
        cb.agir("golpe_escudo", (3, 1))
        self.assertEqual(lobo.pos, (3, 1))                          # não andou: bateu logo
        col = danos(cb, n, "colisao")
        self.assertEqual(col[0]["valor"], 2 * C.COLISAO_CASA)
        self.assertEqual(lobo.vida, vida - danos(cb, n, "golpe_escudo")[0]["valor"] - 2 * C.COLISAO_CASA)

    def test_colisao_brutal_e_arremesso(self):
        cb = Combate("berserker", "aberto", ["colisao_brutal"], inicio={"lobo#1": {"parado": True, "prep": [(0, 0)]},
                                                                         "lobo#2": {"parado": True},
                                                                         "lobo#3": {"parado": True}})
        ate(cb, "heroi")
        lobo = cb.u["lobo#1"]
        cb.heroi.pos, lobo.pos = (2, 1), (3, 1)
        cb.agir("golpe_escudo", (3, 1))
        self.assertEqual(danos(cb, 0, "colisao")[0]["valor"], 4 * C.COLISAO_CASA)
        self.assertIn("atordoado", lobo.estados)
        self.assertIsNone(lobo.prep)
        cb = Combate("berserker", "aberto", ["arremesso"], inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        a, b = cb.u["lobo#1"], cb.u["lobo#2"]
        cb.heroi.pos, a.pos, b.pos = (1, 3), (2, 3), (4, 3)
        cb.agir("golpe_escudo", (2, 3))
        self.assertEqual(a.pos, (3, 3))                             # andou 1 de 4 e bateu no outro lobo
        col = danos(cb, 0, "colisao")
        self.assertEqual(len(col), 2)
        self.assertEqual(col[0]["valor"], 3 * C.COLISAO_CASA)

    def test_corrente_puxa_ate_o_lado(self):
        cb = Combate("berserker", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        lobo = cb.u["lobo#1"]
        lobo.pos = (5, 3)
        cb.agir("corrente", (5, 3))
        self.assertEqual(lobo.pos, (2, 3))

    def test_explosao_de_calor_empurra_aliados_menos_com_seletivas(self):
        for talentos, morel_anda in (([], True), (["seletivas"], False)):
            cb = Combate("piromante", "aberto", talentos, inicio=parados("lobo#1", "lobo#2", "lobo#3"))
            ate(cb, "heroi")
            cb.u["morel"].pos = (1, 2)
            cb.u["lobo#1"].pos = (2, 3)
            prev = cb.previa(cb.heroi, "explosao_calor", cb.heroi.pos)
            cb.agir("explosao_calor", None)
            self.assertEqual(cb.u["lobo#1"].pos, (4, 3))
            self.assertEqual(cb.u["morel"].pos != (1, 2), morel_anda)
            self.assertEqual("morel" in prev["atingidos"], morel_anda)


class Previa(unittest.TestCase):
    def test_area_da_previa_igual_ao_efeito(self):
        cb = Combate("piromante", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        cb.u["lobo#1"].pos, cb.u["lobo#2"].pos, cb.u["morel"].pos = (3, 3), (3, 4), (3, 2)
        prev = cb.previa(cb.heroi, "chuva", (3, 3))
        self.assertEqual(set(prev["atingidos"]), {"lobo#1", "lobo#2", "morel"})
        self.assertEqual(prev["aliados"], ["morel"])
        n = len(cb.eventos)
        cb.agir("chuva", (3, 3))
        reais = {e["alvo"]: e["valor"] for e in danos(cb, n, "chuva")}
        self.assertEqual(reais, prev["dano"])

    def test_labareda_e_combustao_em_area(self):
        cb = Combate("piromante", "aberto", ["labareda"], inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        self.assertEqual(len(cb.previa(cb.heroi, "chuva", (4, 3))["casas"]), 13)
        cb = Combate("piromante", "aberto", ["combustao_area"], inicio={
            "lobo#1": {"parado": True, "pos": (4, 3), "camadas": 2},
            "lobo#2": {"parado": True, "pos": (4, 4), "camadas": 3}, "lobo#3": {"parado": True}})
        ate(cb, "heroi")
        prev = cb.previa(cb.heroi, "combustao", (4, 3))
        self.assertEqual(set(prev["atingidos"]), {"lobo#1", "lobo#2"})
        cb.agir("combustao", (4, 3))
        self.assertIsNone(cb.u["lobo#2"].queima)


class Ocupacao(unittest.TestCase):
    def test_casa_liberada_depois_da_morte(self):
        cb = Combate("berserker", "aberto", inicio={"lobo#1": {"parado": True, "pos": (2, 3), "vida": 1},
                                                     "lobo#2": {"parado": True}, "lobo#3": {"parado": True}})
        ate(cb, "heroi")
        self.assertNotIn((2, 3), cb.movimentos())
        cb.mover((1, 2))
        cb2 = Combate("berserker", "aberto", inicio={"lobo#1": {"parado": True, "pos": (2, 3), "vida": 1},
                                                      "lobo#2": {"parado": True}, "lobo#3": {"parado": True}},
                      mover_depois=True)
        ate(cb2, "heroi")
        cb2.agir("golpe_pesado", (2, 3))
        self.assertFalse(cb2.u["lobo#1"].vivo)
        self.assertIn((2, 3), cb2.movimentos())

    def test_sentinela_casa_vazia_troca_e_bloqueia(self):
        cb = Combate("piromante", "passagem", inicio=parados("mercenario#1", "bandido#1", "bandido#2"))
        ate(cb, "heroi")
        self.assertNotIn(cb.u["morel"].pos, cb.alvos_validos(cb.heroi, "sentinela"))
        cb.agir("sentinela", (4, 3))                                # fecha a passagem
        s1 = next(x for x in cb.vivos("aliado") if x.invocacao)
        self.assertNotIn(s1, cb.ordem)
        cb.encerrar()
        ate(cb, "heroi")
        cb.agir("sentinela", (3, 4))
        self.assertFalse(s1.vivo)
        self.assertIsNone(cb.em((4, 3)))                            # a casa da anterior ficou livre

    def test_inimigos_atacam_a_sentinela_que_fecha_o_caminho(self):
        cb = Combate("piromante", "passagem")
        ate(cb, "heroi")
        cb.agir("sentinela", (4, 3))
        s = next(x for x in cb.vivos("aliado") if x.invocacao)
        for _ in range(4):
            ate(cb, "heroi")
            cb.encerrar()
            if not s.vivo or s.vida < s.vida_max:
                break
        self.assertTrue(not s.vivo or s.vida < s.vida_max)
        self.assertTrue(any("Sentinela: 1 PM a menos" in e["texto"] or "ao lado da Sentinela" in e["texto"]
                            for e in cb.eventos))


class Chao(unittest.TestCase):
    def test_muralha_entrar_comecar_e_expirar(self):
        cb = Combate("piromante", "aberto", inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        cb.agir("muralha_fogo", (3, 3))
        self.assertEqual(set(cb.chamas), {(3, 2), (3, 3), (3, 4)})
        cb.encerrar()
        ate(cb, "morel")
        vida = cb.u["morel"].vida
        cb.mover((3, 2))                                            # entra: fogo e 1 camada, uma vez nesta vez
        self.assertEqual(cb.u["morel"].vida, vida - C.FOGO_CHAO)
        self.assertEqual(cb.u["morel"].queima["camadas"], 1)
        for _ in range(3):
            ate(cb, "heroi")
            cb.encerrar()
        self.assertEqual(cb.chamas, {})                             # durou 2 rodadas

    def test_fogo_eterno(self):
        cb = Combate("piromante", "aberto", ["fogo_eterno"], inicio=parados("lobo#1", "lobo#2", "lobo#3"))
        ate(cb, "heroi")
        cb.agir("muralha_fogo", (3, 3))
        for _ in range(4):
            ate(cb, "heroi")
            cb.encerrar()
        self.assertEqual(len(cb.chamas), 3)

    def test_estouro_nas_casas_vizinhas(self):
        cb = Combate("piromante", "aberto", ["estouro"], inicio={
            "lobo#1": {"parado": True, "pos": (4, 3), "vida": 3, "camadas": 2},
            "lobo#2": {"parado": True, "pos": (5, 3), "vida": 5, "camadas": 1},
            "lobo#3": {"parado": True, "pos": (7, 3)}})
        ate(cb, "heroi")
        cb.agir("bola_fogo", (4, 3))
        self.assertFalse(cb.u["lobo#1"].vivo)
        self.assertFalse(cb.u["lobo#2"].vivo)                       # explodiu pelo vizinho
        self.assertTrue(cb.u["lobo#3"].vivo)                        # a 2 casas do segundo: fora


class Preparos(unittest.TestCase):
    def test_sair_das_casas_marcadas_escapa(self):
        cb = Combate("berserker", "troll", inicio={"troll#1": {"pos": (3, 3), "prep": [(2, 3), (3, 2), (3, 4)]}})
        ate(cb, "morel")
        cb.u["morel"].pos = (3, 2)
        cb.u["odete"].pos = (0, 0)
        cb.heroi.pos = (2, 3)
        cb.mover((2, 1))                                            # Morel sai da casa marcada
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.encerrar()                                               # Jean fica em (2, 3)
        cb.encerrar()                                               # Odette; depois, o troll
        golpe = [e for e in danos(cb, n, "inimigo") if "Esmagador" in e["texto"]]
        self.assertEqual([e["alvo"] for e in golpe], ["heroi"])


class Talentos(unittest.TestCase):
    def test_cacador_da_pm_depois_de_agir(self):
        cb = Combate("berserker", "aberto", ["cacador"], inicio={"lobo#1": {"parado": True, "pos": (2, 3), "vida": 1},
                                                                 "lobo#2": {"parado": True}, "lobo#3": {"parado": True}})
        ate(cb, "heroi")
        cb.agir("golpe_pesado", (2, 3))
        self.assertEqual(cb.heroi.pm, 3)
        self.assertTrue(cb.mover((4, 3))["ok"])

    def test_ancora(self):
        cb = Combate("berserker", "aberto", ["ancora"], inicio={"lobo#1": {"pos": (2, 3)}})
        lobo = cb.u["lobo#1"]
        f = cb.saida(lobo)
        self.assertEqual(f((2, 3)), 3)                              # vizinho de Jean (1, 3): 1 + 2
        cb2 = Combate("berserker", "aberto", inicio={"lobo#1": {"pos": (2, 3)}})
        self.assertEqual(cb2.saida(cb2.u["lobo#1"])((2, 3)), 1)


class Inimigos(unittest.TestCase):
    def test_ninguem_fica_parado_nos_encontros(self):
        import sys
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ferramentas"))
        from simular import partida
        for spec in C.HEROI:
            for enc in C.ENCONTROS:
                cb = partida(spec, enc, 7)
                self.assertLessEqual(cb.m["inimigo_parado"], cb.m["vezes_inimigo"] * 0.15, (spec, enc))

    def test_fuga_repetida_nao_domina_com_as_regras_padrao(self):
        import sys
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ferramentas"))
        from simular import partida
        vitorias = sum(partida("piromante", "prioridades", 1000 + s, "recuo").fim == "vitoria" for s in range(6))
        self.assertLess(vitorias, 4)

    def test_mesma_semente_mesma_luta(self):
        def jogar():
            cb = Combate("berserker", "prioridades", semente=9)
            for _ in range(300):
                if cb.fim:
                    break
                cb.encerrar()
            return [e["texto"] for e in cb.eventos]
        self.assertEqual(jogar(), jogar())

    def test_jogo_nao_carrega_o_prototipo(self):
        for p in (RAIZ / "rpg").rglob("*.py"):
            self.assertNotIn("etapa8-tatico", p.read_text(encoding="utf-8"), p)


if __name__ == "__main__":
    unittest.main()
