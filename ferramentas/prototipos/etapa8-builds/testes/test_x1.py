"""Testes do protótipo X1 da etapa 8 (fora da suíte do jogo): a montagem (orçamento, linhas, exclusões, o que cada nó
muda), a regra das cadeias (identidade dos efeitos) e as interações das builds de exemplo.

    python -m unittest discover -s ferramentas/prototipos/etapa8-builds/testes -t ferramentas/prototipos/etapa8-builds
"""
import pathlib
import unittest

from motor import conteudo as C
from motor import montagem as M
from motor.combate import Combate

RAIZ = pathlib.Path(__file__).resolve().parents[4]


def pir(nos, kit=("brasa", "chuva", "combustao", "bola_fogo", "lanca")):
    return {"estrutura": "t4", "spec": "piromante", "kit": list(kit), "nos": dict(nos)}


def ber(nos, kit=("golpe_pesado", "joelho", "quebra_guarda", "rugido", "redemoinho")):
    return {"estrutura": "t4", "spec": "berserker", "kit": list(kit), "nos": dict(nos)}


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


class Montagem(unittest.TestCase):
    def test_exemplos_validos_com_o_orcamento_inteiro(self):
        for ex in C.EXEMPLOS:
            m = M.de_exemplo(ex["id"])
            self.assertEqual(M.erros(m), [], ex["id"])
            self.assertEqual(M.pontos_gastos(m), C.PONTOS, ex["id"])
            self.assertEqual(len(m["kit"]), C.ESPACOS, ex["id"])

    def test_nao_cabe_tudo(self):
        """Regras e princípios, mais uma versão de cada habilidade que tem versão, passam do orçamento; na híbrida,
        só as regras já passam."""
        for chave, arvore in C.ARVORES.items():
            fortes = sum(n["custo"] for n in arvore if n["tipo"] in ("R", "P"))
            versoes = len({n["versao"] for n in arvore if n.get("versao")})
            self.assertGreater(fortes + versoes, C.PONTOS, chave)
            if chave[0] == "t4":
                self.assertGreater(fortes, C.PONTOS, chave)

    def test_estruturas_comparaveis(self):
        for spec in ("berserker", "piromante"):
            t4, t1 = C.ARVORES[("t4", spec)], C.ARVORES[("t1", spec)]
            self.assertLessEqual(abs(len(t4) - len(t1)), 1, spec)

    def test_orcamento_estourado(self):
        m = pir({"paciente": 1, "partilhado": 1, "fornalha": 1, "estouro": 1})
        self.assertTrue(any("orçamento" in e for e in M.erros(m)))
        m = pir({"paciente": 1, "partilhado": 1, "fornalha": 1})
        no = next(n for n in M.estado_arvore(m) if n["id"] == "estouro")
        self.assertFalse(no["pode_mais"])
        self.assertEqual(no["motivo_mais"], "Falta 1 ponto")

    def test_linhas(self):
        m = pir({"estouro": 1})
        self.assertTrue(any("linha 2" in e for e in M.erros(m)))
        m = pir({"chama_viva": 1})
        no = next(n for n in M.estado_arvore(m) if n["id"] == "estouro")
        self.assertFalse(no["pode_mais"])
        self.assertIn("Requer 2 pontos", no["motivo_mais"])
        m = pir({"fornalha": 1, "estouro": 1})
        self.assertEqual(M.erros(m), [])
        no = next(n for n in M.estado_arvore(m) if n["id"] == "fornalha")
        self.assertFalse(no["pode_menos"])  # sustenta a linha 2
        self.assertEqual(no["motivo_menos"], "Sustenta a linha 2")

    def test_versoes_se_excluem(self):
        m = pir({"chama_viva": 2, "pavio": 1, "contagio": 1})
        self.assertTrue(any("Versões da mesma habilidade" in e for e in M.erros(m)))
        m = pir({"chama_viva": 2, "pavio": 1})
        no = next(n for n in M.estado_arvore(m) if n["id"] == "contagio")
        self.assertEqual(no["motivo_mais"], "Exclui Pavio Curto")

    def test_o_que_cada_no_muda_no_kit(self):
        m = M.de_exemplo("pavio")
        kit = {k["id"]: k for k in M.kit_descrito(m)}
        self.assertEqual(kit["combustao"]["versao"], "Pavio Curto")
        for h in ("brasa", "chuva", "bola_fogo"):
            self.assertTrue(any("Fogo Paciente" in n for n in kit[h]["notas"]), h)
        self.assertFalse(any("Fogo Paciente" in n for n in kit["lanca"]["notas"]))
        arv = {n["id"]: n for n in M.estado_arvore(m)}
        self.assertIn("golpes de Morel e Odette", arv["partilhado"]["afeta"])
        self.assertIn("Brasa", arv["paciente"]["afeta"])

    def test_avisos_de_no_sem_efeito(self):
        m = ber({"sangue_quente": 1}, kit=("golpe_pesado", "joelho", "quebra_guarda", "provocar", "redemoinho"))
        no = next(n for n in M.estado_arvore(m) if n["id"] == "sangue_quente")
        self.assertIn("Rugido não está no kit", no["aviso"])
        m = pir({"chama_viva": 2, "pavio": 1}, kit=("brasa", "chuva", "bola_fogo", "lanca", "barreira"))
        no = next(n for n in M.estado_arvore(m) if n["id"] == "pavio")
        self.assertEqual(no["aviso"], "Combustão não está no kit")

    def test_numeros_somam_e_custos_de_versao(self):
        self.assertEqual(M.efeitos(pir({"chama_viva": 2}))["chama_viva"], 2)
        m = {"estrutura": "t1", "spec": "piromante", "kit": ["bola_fogo"], "nos": {"v_pesada": 1}}
        self.assertEqual(next(k for k in M.kit_descrito(m) if k["id"] == "bola_fogo")["custo"], 16)

    def test_jogo_nao_carrega_o_prototipo(self):
        for p in (RAIZ / "rpg").rglob("*.py"):
            self.assertNotIn("etapa8-builds", p.read_text(encoding="utf-8"), p)


class Cadeias(unittest.TestCase):
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
        self.assertEqual(len(explosoes), 2)
        # a do Lobo B chega primeiro: ele morre no meio da explosão do A e explode antes de ela terminar
        self.assertEqual({e["texto"].split(":")[0] for e in explosoes}, {"Explosão de Lobo A", "Explosão de Lobo B"})
        self.assertEqual(len(gatilhos(cb, "estouro", n)), 2)
        cad = cb.eventos[n]["cadeia"]
        self.assertTrue(all(e["cadeia"] == cad for e in explosoes + gatilhos(cb, "estouro", n)))
        # cada inimigo dá 1 Calor por cadeia: o Lobo A foi detonado e explodiu
        self.assertEqual(cb.heroi.calor, 2)
        self.assertEqual(len(barrados(cb, "fornalha", n)), 1)

    def test_explosoes_matam_e_a_cadeia_acaba(self):
        ini = {f"rato#{i}": {"parado": True, "vida": 4, "camadas": 1} for i in range(1, 5)}
        C.ENCONTROS["_ratos"] = {"nome": "teste", "semente": 1, "inimigos": ["rato"] * 4}
        try:
            cb = Combate(pir({"fornalha": 1, "estouro": 1}), "_ratos", inicio=ini)
            ate(cb, "heroi")
            n = len(cb.eventos)
            cb.agir("combustao", "rato#1")
        finally:
            del C.ENCONTROS["_ratos"]
        self.assertEqual(cb.fim, "vitoria")
        self.assertEqual(len(gatilhos(cb, "estouro", n)), 4)
        cad = cb.cadeias[-1]
        self.assertLess(cad["elos"], 20)
        self.assertEqual(cb.heroi.calor, 3)

    def test_espinhos_e_revides_nao_se_respondem(self):
        ini = {"bandido#1": {"vida": 500, "vida_max": 500, "espinhos": 5, "revida": 6, "parado": True},
               "bandido#2": {"parado": True}}
        cb = Combate(ber({"couro": 2, "revide": 1}), "mercenario", inicio=dict(
            ini, **{"mercenario#1": {"parado": True}}))
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("golpe_pesado", "bandido#1")
        self.assertEqual(len(gatilhos(cb, "espinhos", n)), 1)
        self.assertEqual(len(gatilhos(cb, "revide_inimigo", n)), 1)
        self.assertEqual(gatilhos(cb, "revide", n), [])  # nem os espinhos nem o revide dele são golpe de ação

    def test_sem_a_regra_de_tipo_a_identidade_ainda_fecha_o_laco(self):
        ini = {"bandido#1": {"vida": 500, "vida_max": 500, "espinhos": 5, "revida": 6, "parado": True},
               "bandido#2": {"parado": True}, "mercenario#1": {"parado": True}}
        cb = Combate(ber({"couro": 2, "revide": 1}), "mercenario", inicio=ini)
        cb.reacoes_respondem_reacoes = True
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("golpe_pesado", "bandido#1")
        for ef in ("espinhos", "revide_inimigo", "revide"):
            self.assertEqual(len(gatilhos(cb, ef, n)), 1, ef)
        self.assertTrue(barrados(cb, "revide_inimigo", n) or barrados(cb, "espinhos", n))
        self.assertIsNone(cb.fim)

    def test_cura_e_recurso_nao_fazem_laco(self):
        cb = Combate(ber({"couro": 2, "revide": 1}), "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
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
        self.assertEqual(len(barrados(cb, "teste_recurso", n)), 1)

    def test_folego_rubro_uma_vez_por_rodada(self):
        cb = Combate(ber({"couro": 2, "sangue_frio": 1, "folego": 1}), "lobos",
                     inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        cb.heroi.vida, cb.heroi.recurso = 20, 0
        ate(cb, "odete")
        cb.curar(cb.heroi, 5, cb.c["odete"], "prece")  # na cadeia do começo da vez de Odette
        self.assertEqual(len(gatilhos(cb, "folego")), 1)
        rodada = cb.rodada
        cb.agir("prece", "heroi")                       # outra cadeia, mesma rodada
        self.assertEqual(next(e for e in cb.eventos if e["tipo"] == "barrado")["rodada"], rodada)
        self.assertEqual(len(gatilhos(cb, "folego")), 1)
        self.assertEqual(barrados(cb, "folego")[-1]["motivo"], "rodada")


class Interacoes(unittest.TestCase):
    def test_pavio_detona_com_as_camadas_da_hora(self):
        cb = Combate(M.de_exemplo("pavio"), "troll", inicio=parados(["troll#1"]))
        ate(cb, "heroi")
        cb.agir("brasa", "troll#1")
        ate(cb, "heroi")
        self.assertEqual(cb.c["troll#1"].queima["camadas"], 1)
        cb.agir("combustao", "troll#1")  # acende o pavio
        self.assertIn("pavio", cb.c["troll#1"].estados)
        self.assertEqual(cb.aguardando, "odete")
        n = len(cb.eventos)
        cb.agir("bastao", "troll#1")     # Calor Partilhado: 2 camadas; depois, o começo da vez do troll
        self.assertEqual(len(gatilhos(cb, "partilhado", n)), 1)
        det = next(e for e in cb.eventos[n:] if e["tipo"] == "detona")
        self.assertIn("2 camadas", det["texto"])
        ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e["causa"] == "pavio")
        self.assertEqual(ev["valor"], round(cb.base_detonacao(cb.c["troll#1"], camadas=2) * 1.5 * 1.4))
        self.assertIsNone(cb.c["troll#1"].queima)

    def test_fogo_paciente(self):
        com = Combate(M.de_exemplo("pavio"), "troll", inicio={"troll#1": {"parado": True, "camadas": 3}})
        sem = Combate(pir({"chama_viva": 2}), "troll", inicio={"troll#1": {"parado": True, "camadas": 3}})
        for cb in (com, sem):
            for _ in range(4):
                ate(cb, "heroi")
                cb.agir("defender")
        self.assertIsNotNone(com.c["troll#1"].queima)
        self.assertIsNone(sem.c["troll#1"].queima)

    def test_calor_paga_o_proximo_fogo(self):
        cb = Combate(M.de_exemplo("fornalha"), "troll", inicio=parados(["troll#1"]))
        cb.heroi.calor = 3
        ate(cb, "heroi")
        a = next(x for x in cb.acoes() if x["id"] == "chuva")
        self.assertEqual(a["pagamento"], "Grátis: 3 Calor")
        rec = cb.heroi.recurso
        cb.agir("chuva")
        self.assertEqual(cb.heroi.recurso, rec)
        self.assertEqual(cb.heroi.calor, 0)

    def test_queimar_a_si_mesmo_paga_com_vida(self):
        cb = Combate(M.de_exemplo("fornalha"), "troll", inicio=parados(["troll#1"]))
        ate(cb, "heroi")
        cb.heroi.recurso = 5
        a = next(x for x in cb.acoes() if x["id"] == "bola_fogo")
        self.assertEqual(a["pagamento"], "5 de Mana + 7 de vida")
        vida = cb.heroi.vida
        cb.agir("bola_fogo", "troll#1")
        self.assertEqual(cb.heroi.vida, vida - 7)

    def test_peso_do_golpe_e_forca(self):
        cb = Combate(M.de_exemplo("quebrador"), "mercenario",
                     inicio=parados(["mercenario#1", "bandido#1", "bandido#2"]))
        ate(cb, "heroi")
        prox = cb._proximo_aliado()
        cb.agir("quebra_guarda", "bandido#1")
        self.assertEqual(prox.fichas["forca"], 1)
        self.assertEqual(cb.c["bandido#1"].fichas["exposto"], 1)
        ate(cb, prox.id)
        hid = "bastao" if prox.id == "odete" else "atacar"
        prev = next(a for a in cb.acoes() if a["id"] == hid)["previsao"]["bandido#1"]
        n = len(cb.eventos)
        cb.agir(hid, "bandido#1")
        ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano")
        self.assertEqual(str(ev["valor"]), prev)
        self.assertIn("Força", ev["texto"])
        self.assertIn("Exposto", ev["texto"])

    def test_desequilibra_interrompe_gigante_firme(self):
        cb = Combate(M.de_exemplo("quebrador"), "troll", inicio={"troll#1": {"parado": True, "prep": True}})
        cb.c["troll#1"].estados["firme"] = {"vezes": 2}
        ate(cb, "heroi")
        cb.agir("golpe_pesado", "troll#1")
        self.assertIsNone(cb.c["troll#1"].prep)
        self.assertEqual(len(gatilhos(cb, "peso_golpe")), 1)

    def test_joelho_interrompe_quem_prepara(self):
        C.ENCONTROS["_bandido"] = {"nome": "teste", "semente": 1, "inimigos": ["mercenario"]}
        try:
            cb = Combate(M.de_exemplo("quebrador"), "_bandido", inicio={"mercenario#1": {"parado": True, "prep": True}})
        finally:
            del C.ENCONTROS["_bandido"]
        ate(cb, "heroi")
        cb.agir("joelho", "mercenario#1")
        m = cb.c["mercenario#1"]
        self.assertIsNone(m.prep)
        self.assertIn("atordoado", m.estados)

    def test_sangue_quente_por_alvo_e_furia_cega_uma_vez(self):
        cb = Combate(M.de_exemplo("furia"), "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        ate(cb, "heroi")
        cb.agir("rugido", "lobo#1")
        cb.heroi.vida = 10
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("redemoinho")
        self.assertEqual(len(gatilhos(cb, "sangue_quente", n)), 3)
        for i in (1, 2, 3):
            cb.c[f"lobo#{i}"].vida = 3
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir("furia_cega", "lobo#1")
        self.assertEqual(len(gatilhos(cb, "furia_cega", n)), 1)
        self.assertTrue(cb.c["lobo#3"].vivo or cb.c["lobo#2"].vivo)

    def test_provocacao_com_revide_uma_vez_por_inimigo(self):
        m = M.de_exemplo("quebrador_t1")
        self.assertEqual(M.erros(m), [])
        self.assertTrue(all(n["aviso"] is None for n in M.estado_arvore(m) if n["rank"]))
        cb = Combate(m, "lobos")
        ate(cb, "heroi")
        cb.agir("provocar")
        self.assertIn("rancor", cb.heroi.estados)
        revides = [e for e in cb.eventos if e["tipo"] == "dano" and e["causa"] == "revide"]
        golpeado = {e["alvo"] for e in cb.eventos if e["tipo"] == "dano" and e.get("alvo") == "heroi" and e["golpe"]}
        self.assertTrue(golpeado)
        self.assertLessEqual(len(revides), 3)  # no máximo um por lobo
        ate(cb, "heroi")
        self.assertNotIn("rancor", cb.heroi.estados)

    def test_exemplos_sem_no_parado(self):
        for ex in C.EXEMPLOS:
            m = M.de_exemplo(ex["id"])
            parados_ = [n["nome"] for n in M.estado_arvore(m) if n["rank"] and n["aviso"]]
            self.assertEqual(parados_, [], ex["id"])

    def test_sair_da_furia(self):
        cb = Combate(M.de_exemplo("furia"), "lobos", inicio=parados(["lobo#1", "lobo#2", "lobo#3"]))
        ate(cb, "heroi")
        cb.agir("rugido", "lobo#1")
        ate(cb, "heroi")
        self.assertTrue(cb.pode_sair_furia())
        guarda_morel = cb.c["morel"].fichas["guarda"]
        cb.sair_furia()
        self.assertNotIn("furia", cb.heroi.estados)
        self.assertEqual(cb.heroi.fichas["guarda"], 1)
        self.assertEqual(cb.c["morel"].fichas["guarda"], min(C.FICHA_TETO, guarda_morel + 1))  # Sangue Frio
        self.assertEqual(cb.aguardando, "heroi")             # não gastou a ação

    def test_mesma_semente_mesma_luta(self):
        def jogar():
            cb = Combate(M.de_exemplo("pavio"), "mercenario", semente=77)
            for _ in range(200):
                if cb.fim:
                    break
                a = next(x for x in cb.acoes() if x["disponivel"] and x["id"] in ("atacar", "bastao", "brasa"))
                cb.agir(a["id"], a["alvos"][0])
            return [e["texto"] for e in cb.eventos]
        self.assertEqual(jogar(), jogar())


if __name__ == "__main__":
    unittest.main()
