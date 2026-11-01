"""Testes do protótipo X1 da etapa 8 (fora da suíte do jogo): a montagem (orçamento, exclusões, alcance dos talentos,
a equivalência entre as estruturas), a regra das cadeias (identidade dos efeitos) e as interações do repertório:
camadas (Queimadura, Sangramento, Frio), invocações, mortes simultâneas e geração de recurso.

    python -m unittest discover -s ferramentas/prototipos/etapa8-builds/testes -t ferramentas/prototipos/etapa8-builds
"""
import pathlib
import unittest

from motor import conteudo as C
from motor import montagem as M
from motor.combate import Combate

RAIZ = pathlib.Path(__file__).resolve().parents[4]


def pir(nos, kit=("brasa", "chuva", "combustao", "bola_fogo", "lanca"), ult="conflagracao", est="t4"):
    return {"estrutura": est, "spec": "piromante", "kit": list(kit), "ultimate": ult, "nos": dict(nos)}


def ber(nos, kit=("golpe_pesado", "joelho", "quebra_guarda", "rugido", "redemoinho"), ult="furia_cega", est="t4"):
    return {"estrutura": est, "spec": "berserker", "kit": list(kit), "ultimate": ult, "nos": dict(nos)}


def ate(cb, quem):
    """Passa as vezes do grupo com Defender até chegar a de `quem`."""
    for _ in range(60):
        if cb.fim or cb.aguardando == quem:
            return
        assert cb.agir("defender")["ok"]
    raise AssertionError(f"a vez de {quem} não chegou")


def gatilhos(cb, efeito, desde=0):
    return [e for e in cb.eventos[desde:] if e["tipo"] == "gatilho" and e["efeito"] == efeito]


def barrados(cb, efeito, desde=0):
    return [e for e in cb.eventos[desde:] if e["tipo"] == "barrado" and e["efeito"] == efeito]


def parados(ids, **extra):
    return {i: {"parado": True, **extra.get(i, {})} for i in ids}


def encontro(lista, semente=1):
    """Um encontro de teste com inimigos do catálogo (registrado só durante o teste)."""
    C.ENCONTROS["_teste"] = {"nome": "teste", "semente": semente, "inimigos": list(lista)}
    return "_teste"


class Base(unittest.TestCase):
    def tearDown(self):
        C.ENCONTROS.pop("_teste", None)


class Montagem(Base):
    def test_repertorio(self):
        for spec, pool in C.POOL.items():
            self.assertEqual(len(pool) + len(C.HEROI[spec]["ultimates"]), 16, spec)
        descs = [h["desc"] for h in C.HABILIDADES.values()]
        self.assertEqual(len(descs), len(set(descs)) + 1)  # Erguer Escudo e Barreira: o mesmo efeito, classes diferentes

    def test_exemplos_validos_sem_no_parado(self):
        for ex in C.EXEMPLOS:
            m = M.de_exemplo(ex["id"])
            self.assertEqual(M.erros(m), [], ex["id"])
            if ex.get("comparacao"):
                continue  # os equivalentes do protótipo tático: sem talentos
            self.assertIn(M.pontos_gastos(m), (C.PONTOS - 1, C.PONTOS), ex["id"])
            self.assertEqual(len(m["kit"]), C.ESPACOS, ex["id"])
            parados_ = [n["nome"] for n in M.estado_arvore(m) if n["rank"] and n["aviso"]]
            self.assertEqual(parados_, [], ex["id"])

    def test_nao_cabe_tudo(self):
        """Regras e princípios, mais uma versão de cada habilidade com versão, passam muito do orçamento; na híbrida,
        só as regras já passam."""
        for chave, arvore in C.ARVORES.items():
            fortes = sum(n["custo"] for n in arvore if n["tipo"] in ("R", "P"))
            versoes = len({n["versao"] for n in arvore if n.get("versao")})
            self.assertGreater(fortes + versoes, C.PONTOS + 5, chave)
            if chave[0] == "t4":
                self.assertGreater(fortes, 2 * C.PONTOS, chave)

    def test_sem_ordem_de_compra(self):
        for chave, arvore in C.ARVORES.items():
            for n in arvore:
                m = {"estrutura": chave[0], "spec": chave[1], "kit": [], "nos": {n["id"]: 1}}
                self.assertEqual(M.erros(m), [], n["id"])

    def test_estruturas_equivalentes(self):
        for spec in ("berserker", "piromante"):
            t4, t1 = C.ARVORES[("t4", spec)], C.ARVORES[("t1", spec)]
            self.assertEqual([n["id"] for n in t4 if n["tipo"] == "N"], [n["id"] for n in t1 if n["tipo"] == "N"])
            equivalencias = " + ".join(n["equivale"] for n in t1 if n.get("equivale"))
            for n in t4:
                if n["tipo"] in ("R", "V"):
                    self.assertIn(n["nome"], equivalencias, f"{spec}: {n['nome']} sem equivalente")
            locais = {"revide": "provoca_revide", "folego": "sede_rubra", "ate_o_fim": "desesperada",
                      "escudeiro": "escudo_duplo", "estouro": "estrondosa", "cinza_fria": "lanca_termica",
                      "vapor": "bola_vapor", "frio_penetrante": "sentinela_cortante"}
            b1 = {k for n in t1 for k in n["efeitos"]}
            for n in t4:
                for k in n["efeitos"]:
                    self.assertTrue(k in b1 or locais.get(k) in b1, f"{spec}: {k}")

    def test_exclusoes(self):
        self.assertTrue(any("Não combinam" in e for e in M.erros(pir({"pavio": 1, "contagio": 1}))))
        self.assertTrue(any("Não combinam" in e for e in M.erros(pir({"paciente": 1, "fornalha": 1}))))
        self.assertTrue(any("Não combinam" in e for e in M.erros(ber({"furia_contida": 1, "furia_sem_freio": 1}))))
        m = pir({"paciente": 1})
        no = next(n for n in M.estado_arvore(m) if n["id"] == "fornalha")
        self.assertEqual(no["motivo_mais"], "Não combina com Fogo Paciente")
        m = pir({"chama_viva": 2, "paciente": 1, "partilhado": 1, "estouro": 1})
        no = next(n for n in M.estado_arvore(m) if n["id"] == "cinza_fria")
        self.assertEqual(no["motivo_mais"], "Falta 1 ponto")

    def test_alcance_e_descricao_efetiva(self):
        m = M.de_exemplo("pavio")
        arv = {n["id"]: n for n in M.estado_arvore(m)}
        alc = {h["nome"]: h["no_kit"] for h in arv["paciente"]["alcance"]}
        self.assertTrue(alc["Brasa"])
        self.assertFalse(alc["Bola de Fogo"])          # do repertório, fora do kit
        self.assertIn("Alastrar", alc)
        self.assertIn("golpes de Morel e Odette", arv["partilhado"]["outros"])
        d = M.descrever(m, "combustao")
        self.assertEqual(d["versao"], "Pavio Curto")
        self.assertTrue(any("Chama Viva" in x for x in d["notas"]))
        self.assertTrue(any("Fogo Paciente" in x for x in M.descrever(m, "bola_fogo")["notas"]))

    def test_ultimate_escolhida(self):
        m = ber({}, ult="muralha_viva")
        self.assertEqual(M.erros(m), [])
        self.assertIn("muralha_viva", M.equipadas(m))
        self.assertTrue(M.erros(ber({}, ult="conflagracao")))

    def test_jogo_nao_carrega_o_prototipo(self):
        for p in (RAIZ / "rpg").rglob("*.py"):
            self.assertNotIn("etapa8-builds", p.read_text(encoding="utf-8"), p)


class Cadeias(Base):
    def test_duas_mortes_duas_explosoes_no_mesmo_sobrevivente(self):
        ini = parados(["lobo#1", "lobo#2", "lobo#3"],
                      **{"lobo#1": {"vida": 5, "camadas": 3}, "lobo#2": {"vida": 5, "camadas": 2},
                         "lobo#3": {"vida": 300, "vida_max": 300}})
        cb = Combate(pir({"fornalha": 1, "estouro": 1}), "lobos", inicio=ini)
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("combustao", "lobo#1")
        explosoes = [e for e in cb.eventos[n:] if e["tipo"] == "dano" and e["causa"] == "estouro"
                     and e["alvo"] == "lobo#3"]
        self.assertEqual({e["texto"].split(":")[0] for e in explosoes}, {"Explosão de Lobo A", "Explosão de Lobo B"})
        self.assertEqual(cb.heroi.calor, 2)
        self.assertEqual(len(barrados(cb, "fornalha", n)), 1)

    def test_mortes_simultaneas_na_conflagracao(self):
        ini = {f"rato#{i}": {"parado": True, "vida": 10, "camadas": 2} for i in range(1, 5)}
        cb = Combate(pir({"fornalha": 1, "estouro": 1}), encontro(["rato"] * 4), inicio=ini)
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("conflagracao")
        self.assertEqual(cb.fim, "vitoria")
        self.assertEqual(len(gatilhos(cb, "estouro", n)), 4)        # cada morto explode uma vez
        self.assertEqual(cb.heroi.calor, 3)                          # 4 mortos, teto 3
        self.assertLess(max(c["elos"] for c in cb.cadeias), 20)

    def test_espinhos_e_revides_nao_se_respondem(self):
        ini = {"bandido#1": {"vida": 500, "vida_max": 500, "espinhos": 5, "revida": 6, "parado": True},
               "bandido#2": {"parado": True}, "mercenario#1": {"parado": True}}
        for regra in (False, True):
            cb = Combate(ber({"revide": 1}), "mercenario", inicio=ini)
            cb.reacoes_respondem_reacoes = regra
            ate(cb, "heroi")
            n = len(cb.eventos)
            cb.agir("golpe_pesado", "bandido#1")
            self.assertEqual(len(gatilhos(cb, "espinhos", n)), 1)
            self.assertEqual(len(gatilhos(cb, "revide_inimigo", n)), 1)
            self.assertEqual(len(gatilhos(cb, "revide", n)), 1 if regra else 0)

    def test_cura_e_recurso_nao_fazem_laco(self):
        cb = Combate(ber({"revide": 1}), "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        h = cb.heroi
        h.vida, h.recurso = 20, 10

        def laco(cb, evento, alvo, valor):
            if alvo is not cb.heroi:
                return
            if evento == "cura":
                cb.disparar("teste_recurso", h, h, lambda: cb.ganhar_recurso(h, 5, "teste"), "ser curado dá recurso")
            elif evento == "recurso":
                cb.disparar("teste_cura", h, h, lambda: cb.curar(h, 5, h, "teste"), "ganhar recurso cura")
        cb.gatilhos_extra.append(laco)
        ate(cb, "odete")
        n = len(cb.eventos)
        cb.agir("prece", "heroi")
        self.assertEqual(len(gatilhos(cb, "teste_recurso", n)), 1)
        self.assertEqual(len(gatilhos(cb, "teste_cura", n)), 1)

    def test_folego_rubro_uma_vez_por_rodada(self):
        cb = Combate(ber({"folego": 1}), "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        cb.heroi.vida, cb.heroi.recurso = 20, 0
        ate(cb, "odete")
        cb.curar(cb.heroi, 5, cb.c["odete"], "prece")
        cb.agir("prece", "heroi")
        self.assertEqual(len(gatilhos(cb, "folego")), 1)
        self.assertEqual(barrados(cb, "folego")[-1]["motivo"], "rodada")

    def test_banho_de_sangue_tambem_quando_as_feridas_sao_abertas(self):
        ini = parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"vida": 4, "sangra": 3},
                                                         "lobo#2": {"sangra": 1}})
        cb = Combate(ber({"banho_sangue": 1}, kit=("abrir_feridas", "talho", "rugido", "sede", "redemoinho")), "lobos",
                     inicio=ini)
        ate(cb, "heroi")
        cb.agir("abrir_feridas", "lobo#1")
        self.assertFalse(cb.c["lobo#1"].vivo)
        self.assertEqual(cb.c["lobo#2"].sangra["camadas"], 3)   # fica com o maior: as 3 do morto
        self.assertEqual(cb.c["lobo#3"].sangra["camadas"], 3)

    def test_mortos_vivos_nao_sangram(self):
        cb = Combate(ber({}, kit=("talho", "abrir_feridas", "rugido", "sede", "redemoinho")), "cultista",
                     inicio=parados(["cultista#1", "esqueleto#1", "esqueleto#2"]))
        ate(cb, "heroi")
        cb.agir("talho", "esqueleto#1")
        self.assertIsNone(cb.c["esqueleto#1"].sangra)


class Invocacoes(Base):
    def test_fatuo_acende_no_fim_da_vez_e_explode_ao_cair(self):
        cb = Combate(pir({"elo_elemental": 1}, kit=("fogo_fatuo", "brasa", "combustao", "chuva", "lanca")), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        ate(cb, "heroi")
        cb.agir("fogo_fatuo")
        fatuo = cb.invocacoes(cb.heroi)[0]
        self.assertEqual(sum(1 for e in cb.vivos("inimigo") if e.queima), 1)  # acendeu um, no fim da vez
        self.assertNotIn(fatuo, cb.ordem)                                      # não tem vez própria
        mana = cb.heroi.recurso
        cb._nova_cadeia("teste")
        cb.golpe(cb.c["lobo#1"], fatuo, 100, "fisico", "inimigo")
        self.assertFalse(fatuo.vivo)
        self.assertEqual(len([e for e in cb.eventos if e["tipo"] == "dano" and e["causa"] == "fatuo"]), 3)
        self.assertEqual(cb.heroi.recurso, min(cb.heroi.recurso_max, mana + 12))
        self.assertEqual(cb.heroi.fichas["forca"], 1)
        self.assertNotIn(fatuo.id, [c["id"] for c in cb.estado()["combatentes"]])

    def test_sacrificio_dobra_e_trocar_nao_explode(self):
        kit = ("fogo_fatuo", "brasa", "combustao", "chuva", "lanca")
        cb = Combate(pir({"elo_elemental": 1, "sacrificio": 1}, kit=kit), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        ate(cb, "heroi")
        cb.agir("fogo_fatuo")
        primeiro = cb.invocacoes(cb.heroi)[0]
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("fogo_fatuo")                                   # troca: o anterior se desfaz sem explodir
        self.assertFalse(primeiro.vivo)
        self.assertEqual(gatilhos(cb, "invocacao_cai", n), [])
        self.assertEqual(gatilhos(cb, "elo_elemental", n), [])
        ate(cb, "heroi")
        fatuo = cb.invocacoes(cb.heroi)[0]
        self.assertIn(fatuo.id, next(a for a in cb.acoes() if a["id"] == "combustao")["alvos"])
        n = len(cb.eventos)
        cb.agir("combustao", fatuo.id)
        explosoes = [e for e in cb.eventos[n:] if e["tipo"] == "dano" and e["causa"] == "fatuo"]
        self.assertEqual(len(explosoes), 3)
        self.assertTrue(all(e["valor"] == 16 for e in explosoes))
        self.assertEqual(len(gatilhos(cb, "elo_elemental", n)), 1)

    def test_explosao_da_invocacao_inicia_cadeia_de_estouros(self):
        kit = ("fogo_fatuo", "brasa", "combustao", "chuva", "lanca")
        cb = Combate(pir({"estouro": 1, "sacrificio": 1}, kit=kit), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        ate(cb, "heroi")
        cb.agir("fogo_fatuo")
        ate(cb, "heroi")
        for i, (vida, camadas) in ((1, (6, 2)), (2, (6, 1)), (3, (300, 0))):
            lobo = cb.c[f"lobo#{i}"]
            lobo.vida_max, lobo.vida = max(lobo.vida_max, vida), vida
            lobo.queima = {"camadas": camadas, "pingos": 3} if camadas else None
        n = len(cb.eventos)
        cb.agir("combustao", cb.invocacoes(cb.heroi)[0].id)
        self.assertEqual(len(gatilhos(cb, "estouro", n)), 2)
        self.assertFalse(cb.c["lobo#1"].vivo or cb.c["lobo#2"].vivo)

    def test_sentinela_atrai_e_esfria(self):
        kit = ("sentinela", "lanca", "nevasca", "barreira", "meditar")
        cb = Combate(pir({}, kit=kit, ult="inverno"), encontro(["bandido"], 3))
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("sentinela")                                   # o bandido age logo depois de Jean
        sentinela = cb.invocacoes(cb.heroi)[0]
        golpe = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e["causa"] == "inimigo")
        self.assertEqual(golpe["alvo"], sentinela.id)
        self.assertEqual(len(gatilhos(cb, "sentinela", n)), 1)
        self.assertEqual(cb.c["bandido#1"].frio, 1)

    def test_congelar_interrompe_e_firme_segura_o_frio(self):
        cb = Combate(pir({}), encontro(["mercenario"]), inicio={"mercenario#1": {"parado": True, "prep": True,
                                                                                 "frio": 1}})
        ate(cb, "heroi")
        cb.agir("lanca", "mercenario#1")                       # 2 Frio em quem prepara: chega a 3
        m = cb.c["mercenario#1"]
        self.assertIsNone(m.prep)
        self.assertEqual(m.estados["atordoado"]["rotulo"], "Congelado")
        self.assertEqual(m.frio, 0)
        m.estados.pop("atordoado")
        m.estados["firme"] = {"vezes": 2}
        cb.resfriar(m, 3, cb.heroi, "teste")
        self.assertEqual(m.frio, 2)
        self.assertNotIn("atordoado", m.estados)


class Camadas(Base):
    def test_fogo_e_frio_se_anulam(self):
        cb = Combate(pir({}), "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"],
                                                      **{"lobo#1": {"frio": 2}, "lobo#2": {"camadas": 2}}))
        h = cb.heroi
        cb.acender(cb.c["lobo#1"], 1, h, "teste")
        self.assertEqual(cb.c["lobo#1"].frio, 1)
        self.assertIsNone(cb.c["lobo#1"].queima)
        cb.resfriar(cb.c["lobo#2"], 1, h, "teste")
        self.assertEqual(cb.c["lobo#2"].queima["camadas"], 1)
        self.assertEqual(cb.c["lobo#2"].frio, 0)

    def test_cinza_fria_e_vapor_convertem(self):
        cb = Combate(pir({"cinza_fria": 1, "vapor": 1}), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"camadas": 2, "vida": 300,
                                                                                  "vida_max": 300},
                                                                       "lobo#2": {"frio": 2}}))
        h = cb.heroi
        cb._nova_cadeia("teste")
        vida = cb.c["lobo#1"].vida
        cb.resfriar(cb.c["lobo#1"], 1, h, "teste")
        self.assertIsNone(cb.c["lobo#1"].queima)
        self.assertEqual(cb.c["lobo#1"].vida, vida - 2 * C.DETONA_CAMADA)
        self.assertEqual(cb.c["lobo#1"].estados["atordoado"]["rotulo"], "Congelado")  # 2 + 1 Frio: congelou
        cb.acender(cb.c["lobo#2"], 1, h, "teste")
        self.assertEqual(cb.c["lobo#2"].frio, 0)
        self.assertEqual(cb.c["lobo#2"].fichas["exposto"], 2)
        self.assertEqual(cb.c["lobo#2"].queima["camadas"], 1)

    def test_versoes_locais_valem_so_na_sua_habilidade(self):
        cb = Combate(pir({"v_vapor": 1}, est="t1"), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"frio": 2}, "lobo#2": {"frio": 2}}))
        h = cb.heroi
        cb.acender(cb.c["lobo#1"], 1, h, "brasa", hid="brasa")
        self.assertEqual(cb.c["lobo#1"].fichas["exposto"], 0)   # a Brasa anula
        cb.acender(cb.c["lobo#2"], 1, h, "bola_fogo", hid="bola_fogo")
        self.assertEqual(cb.c["lobo#2"].fichas["exposto"], 2)   # a Bola de Vapor converte

    def test_frio_penetrante_na_previsao_e_no_dano(self):
        cb = Combate(pir({"frio_penetrante": 1}), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"frio": 2, "vida": 300,
                                                                                  "vida_max": 300}}))
        ate(cb, "morel")
        prev = next(a for a in cb.acoes() if a["id"] == "atacar")["previsao"]["lobo#1"]
        self.assertEqual(int(prev), round(11 * 1.2))
        n = len(cb.eventos)
        cb.agir("atacar", "lobo#1")
        self.assertEqual(str(next(e for e in cb.eventos[n:] if e["tipo"] == "dano")["valor"]), prev)

    def test_alastrar_transfere(self):
        cb = Combate(pir({}, kit=("alastrar", "brasa", "combustao", "chuva", "lanca")), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"camadas": 3},
                                                                       "lobo#2": {"camadas": 1}}))
        ate(cb, "heroi")
        cb.agir("alastrar", "lobo#1")
        self.assertIsNone(cb.c["lobo#1"].queima)
        self.assertEqual(cb.c["lobo#2"].queima["camadas"], 3)
        self.assertEqual(cb.c["lobo#3"].queima["camadas"], 3)

    def test_arma_flamejante_e_calor_partilhado_somam(self):
        cb = Combate(pir({"partilhado": 1}, kit=("arma_flamejante", "brasa", "combustao", "chuva", "lanca")),
                     "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"camadas": 1}}))
        ate(cb, "heroi")
        cb.agir("arma_flamejante", "morel")
        ate(cb, "morel")
        n = len(cb.eventos)
        cb.agir("atacar", "lobo#1")
        dano = next(e for e in cb.eventos[n:] if e["tipo"] == "dano")
        self.assertIn("de fogo", dano["texto"])
        self.assertEqual(cb.c["lobo#1"].queima["camadas"], 3)
        self.assertNotIn("flamejante", cb.c["morel"].estados)   # acabou no fim da vez dele


class Berserker(Base):
    def test_furia_grito_contagiante_uma_vez_e_sem_freio(self):
        cb = Combate(ber({"grito_contagiante": 1, "furia_sem_freio": 1}), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        ate(cb, "heroi")
        cb.agir("rugido", "lobo#1")
        self.assertEqual(cb.c["morel"].fichas["forca"], 1)
        ate(cb, "heroi")
        self.assertIn("Sem Freio", cb.motivo_sair_furia())
        cb.agir("rugido", "lobo#1")                              # já na Fúria: não dá Força de novo
        self.assertEqual(len(gatilhos(cb, "grito_contagiante")), 1)
        ate(cb, "heroi")
        self.assertIsNone(cb.motivo_sair_furia())

    def test_escudeiro_e_escudo_alto(self):
        cb = Combate(ber({"escudeiro": 1}, kit=("erguer_escudo", "escudo_alto", "provocar", "rugido", "sede")),
                     "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"vida": 300,
                                                                                         "vida_max": 300}}))
        ate(cb, "heroi")
        cb.agir("erguer_escudo", "odete")
        self.assertEqual(cb.c["odete"].fichas["guarda"], 1)
        self.assertEqual(cb.heroi.fichas["guarda"], 1)
        ate(cb, "heroi")
        g = cb.heroi.fichas["guarda"]
        prev = next(a for a in cb.acoes() if a["id"] == "escudo_alto")["previsao"]["lobo#1"]
        self.assertEqual(int(prev), round(14 * 0.3 + 12 * g))
        cb.agir("escudo_alto", "lobo#1")
        self.assertEqual(cb.heroi.fichas["guarda"], 0)

    def test_muralha_viva_puxa_todos_os_golpes(self):
        cb = Combate(ber({}, kit=("cerrar_dentes", "golpe_pesado", "provocar", "rugido", "sede"), ult="muralha_viva"),
                     "lobos")
        ate(cb, "heroi")
        cb.agir("muralha_viva")
        golpes = []
        for _ in range(10):
            if cb.aguardando == "heroi" or cb.fim:
                break
            n = len(cb.eventos)
            cb.agir("defender")
            golpes += [e for e in cb.eventos[n:] if e["tipo"] == "dano" and e["causa"] == "inimigo"]
        self.assertTrue(golpes)
        self.assertTrue(all(e["alvo"] == "heroi" for e in golpes))

    def test_cerrar_os_dentes_da_vigor_por_golpe(self):
        cb = Combate(ber({}, kit=("cerrar_dentes", "golpe_pesado", "provocar", "rugido", "sede")), "lobos")
        ate(cb, "heroi")
        cb.heroi.recurso = 0
        cb.agir("cerrar_dentes")
        n = len(cb.eventos)
        ate(cb, "heroi")
        golpes = [e for e in cb.eventos[n:] if e["tipo"] == "dano" and e["alvo"] == "heroi" and e["golpe"]]
        self.assertEqual(len(gatilhos(cb, "cerrar", n)), len(golpes))

    def test_estandarte_e_estandarte_sangrento(self):
        kit = ("estandarte", "golpe_pesado", "provocar", "rugido", "sede")
        cb = Combate(ber({}, kit=kit), "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        ate(cb, "heroi")
        cb.agir("estandarte")
        self.assertEqual(sum(a.fichas["forca"] for a in cb.grupo()), 1)
        cb = Combate(ber({"estandarte_sangrento": 1}, kit=kit), "cultista",
                     inicio=parados(["cultista#1", "esqueleto#1", "esqueleto#2"]))
        ate(cb, "heroi")
        cb.agir("estandarte")
        self.assertIsNotNone(cb.c["cultista#1"].sangra)          # os esqueletos não sangram: vai no cultista

    def test_fio_cortante(self):
        cb = Combate(ber({"fio_cortante": 1}, kit=("talho", "golpe_pesado", "provocar", "rugido", "redemoinho")),
                     "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"], **{"lobo#1": {"vida": 300,
                                                                                         "vida_max": 300}}))
        ate(cb, "heroi")
        cb.agir("talho", "lobo#1")
        self.assertEqual(cb.c["lobo#1"].sangra["camadas"], 1)    # não sangrava antes
        ate(cb, "heroi")
        cb.agir("golpe_pesado", "lobo#1")
        self.assertEqual(cb.c["lobo#1"].sangra["camadas"], 2)
        ate(cb, "heroi")
        cb.agir("redemoinho")                                    # em área, o Fio não vale
        self.assertEqual(cb.c["lobo#1"].sangra["camadas"], 2)


class Interacoes(Base):
    def test_pavio_detona_com_as_camadas_da_hora(self):
        cb = Combate(M.de_exemplo("pavio"), "troll", inicio=parados(["troll#1"]))
        ate(cb, "heroi")
        cb.agir("brasa", "troll#1")
        ate(cb, "heroi")
        cb.agir("combustao", "troll#1")
        n = len(cb.eventos)
        cb.agir("bastao", "troll#1")
        self.assertEqual(len(gatilhos(cb, "partilhado", n)), 1)
        ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e["causa"] == "pavio")
        self.assertEqual(ev["valor"], round(cb.base_detonacao(cb.c["troll#1"], camadas=2) * 1.5 * 1.4))

    def test_fogo_paciente(self):
        com = Combate(pir({"paciente": 1}), "troll", inicio={"troll#1": {"parado": True, "camadas": 3}})
        sem = Combate(pir({}), "troll", inicio={"troll#1": {"parado": True, "camadas": 3}})
        for cb in (com, sem):
            for _ in range(4):
                ate(cb, "heroi")
                cb.agir("defender")
        self.assertIsNotNone(com.c["troll#1"].queima)
        self.assertIsNone(sem.c["troll#1"].queima)

    def test_calor_e_vida_pagam_o_fogo(self):
        cb = Combate(M.de_exemplo("fornalha"), "troll", inicio=parados(["troll#1"]))
        cb.heroi.calor = 3
        ate(cb, "heroi")
        self.assertEqual(next(x for x in cb.acoes() if x["id"] == "chuva")["pagamento"], "Grátis: 3 Calor")
        cb.agir("chuva")
        self.assertEqual(cb.heroi.calor, 0)
        ate(cb, "heroi")
        cb.heroi.recurso = 5
        self.assertEqual(next(x for x in cb.acoes() if x["id"] == "combustao")["pagamento"], "5 de Mana + 9 de vida")

    def test_peso_do_golpe_e_previsao(self):
        cb = Combate(M.de_exemplo("quebrador"), "mercenario",
                     inicio=parados(["mercenario#1", "bandido#1", "bandido#2"]))
        ate(cb, "heroi")
        prox = cb._proximo_aliado()
        cb.agir("quebra_guarda", "bandido#1")
        self.assertEqual(prox.fichas["forca"], 1)
        ate(cb, prox.id)
        hid = "bastao" if prox.id == "odete" else "atacar"
        prev = next(a for a in cb.acoes() if a["id"] == hid)["previsao"]["bandido#1"]
        n = len(cb.eventos)
        cb.agir(hid, "bandido#1")
        self.assertEqual(str(next(e for e in cb.eventos[n:] if e["tipo"] == "dano")["valor"]), prev)

    def test_desequilibra_interrompe_gigante_firme(self):
        cb = Combate(M.de_exemplo("quebrador"), "troll", inicio={"troll#1": {"parado": True, "prep": True}})
        cb.c["troll#1"].estados["firme"] = {"vezes": 2}
        ate(cb, "heroi")
        cb.agir("golpe_pesado", "troll#1")
        self.assertIsNone(cb.c["troll#1"].prep)

    def test_mesma_semente_mesma_luta(self):
        def jogar():
            cb = Combate(M.de_exemplo("invocador"), "mercenario", semente=77)
            for _ in range(200):
                if cb.fim:
                    break
                a = next(x for x in cb.acoes() if x["disponivel"] and x["id"] in
                         ("fogo_fatuo", "atacar", "bastao", "brasa"))
                cb.agir(a["id"], a["alvos"][0] if a["alvo"] != "proprio" else None)
            return [e["texto"] for e in cb.eventos]
        self.assertEqual(jogar(), jogar())


if __name__ == "__main__":
    unittest.main()
