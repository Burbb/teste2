"""Testes dirigidos do protótipo de combate e atributos (fora da suíte do jogo: o jogo não carrega nada daqui).

    python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
"""
import json
import os
import tempfile
import threading
import unittest
import urllib.request

os.environ.setdefault("DEMO_SAVES", tempfile.mkdtemp(prefix="combate-atributos-teste-"))

from motor import conteudo as C  # noqa: E402
from motor.regras import Combate, critico, custo_mult, reducao_defesa  # noqa: E402

BASICO = {"heroi": "atacar", "odete": "bastao", "morel": "golpe"}


def basico(cb, alvo=None):
    """O ataque básico do aliado da vez no primeiro inimigo vivo (ou no alvo dado)."""
    a = cb.aguardando
    return cb.agir(cb.turno_id, BASICO[a], alvo or cb.vivos("inimigo")[0])


def ate(cb, quem, passar=None):
    """Passa as vezes dos outros aliados (com o ataque básico, ou `passar`) até ser a vez de `quem`."""
    for _ in range(40):
        if cb.fim or cb.aguardando == quem:
            return
        (passar or basico)(cb)
    raise AssertionError(f"a vez de {quem} não chegou")


def defender(cb):
    """Passa a vez do aliado sem bater (para os inimigos não morrerem no meio do teste)."""
    return cb.agir(cb.turno_id, "defender", cb.aguardando)


class Ordem(unittest.TestCase):
    def test_ordem_pela_agilidade_e_desempates(self):
        cb = Combate("e1", "A")
        agi = [cb.c[i].atr["agilidade"] for i in cb.ordem]
        self.assertEqual(agi, sorted(agi, reverse=True))
        # B tem Agilidade 6 e Percepção 6: empata com o Lobo Alfa (6, 4) e passa pela Percepção
        self.assertEqual(Combate("e1", "B").ordem[0], "heroi")
        self.assertEqual(Combate("e1", "A").ordem[-1], "heroi")

    def test_ordem_calculada_uma_vez(self):
        cb = Combate("e3", "A")
        antes = list(cb.ordem)
        cb.c["heroi"].atr["agilidade"] = 8  # mudar a Agilidade no meio da luta não reordena
        for _ in range(4):
            ate(cb, "heroi")
            defender(cb)
        self.assertEqual(cb.ordem[:len(antes)], antes)
        self.assertGreater(len(cb.ordem), len(antes))  # a invocação entrou no fim

    def test_invocacao_entra_no_fim_e_age_na_rodada_seguinte(self):
        cb = Combate("e3", "A")
        while not any(e["tipo"] == "invoca" for e in cb.eventos):
            defender(cb)
        ev = next(e for e in cb.eventos if e["tipo"] == "invoca")
        self.assertEqual(ev["rodada"], 1)
        self.assertEqual(cb.ordem[-1], "afogado#1")
        self.assertEqual(cb.c["afogado#1"].entra_rodada, 2)
        while cb.rodada == 1:
            defender(cb)
        self.assertFalse(any(e.get("ator") == "afogado#1" and e["rodada"] == 1 for e in cb.eventos))
        while cb.rodada == 2 and not cb.fim:
            defender(cb)
        self.assertTrue(any(e.get("ator") == "afogado#1" and e["rodada"] == 2 for e in cb.eventos))


class VezPerdidaEFimDaRodada(unittest.TestCase):
    def test_atordoado_perde_a_vez_e_a_rodada_termina(self):
        cb = Combate("t1", "A")  # Jean começa atordoado e é o último da ordem
        while cb.rodada == 1:
            basico(cb, "lobo#1") if cb.aguardando else None
        perdeu = [e for e in cb.eventos if e["tipo"] == "perde" and e.get("ator") == "heroi"]
        self.assertEqual(len(perdeu), 1)
        self.assertEqual(perdeu[0]["rodada"], 1)
        self.assertEqual(cb.rodada, 2)
        self.assertNotIn("atordoado", cb.c["heroi"].estados)
        ate(cb, "heroi")  # na rodada 2 ele age
        self.assertEqual(cb.rodada, 2)

    def test_caido_e_pulado_sem_recuperar_a_vez(self):
        cb = Combate("t3", "A")
        self.assertTrue(any(e["tipo"] == "pula" and e.get("ator") == "morel" for e in cb.eventos))


class Estados(unittest.TestCase):
    def test_defesa_dura_ate_o_inicio_do_proximo_turno(self):
        cb = Combate("e1", "A")
        ate(cb, "heroi")
        r = cb.rodada
        defender(cb)
        self.assertIn("defesa", cb.c["heroi"].estados)  # vale durante os turnos dos outros
        ate(cb, "heroi")
        self.assertEqual(cb.rodada, r + 1)
        self.assertNotIn("defesa", cb.c["heroi"].estados)  # acabou quando a vez dele começou
        self.assertTrue(any(e["tipo"] == "expira" and "Defendendo" in e["texto"] and "início do turno de Jean" in e["texto"]
                            for e in cb.eventos))

    def test_escudo_e_marca_ate_o_fim_da_rodada_seguinte(self):
        cb = Combate("e2", "C")
        ate(cb, "morel")
        r = cb.rodada
        cb.agir(cb.turno_id, "marcar", "bruto#1")
        ate(cb, "odete")
        cb.agir(cb.turno_id, "escudo_luz", "heroi")
        self.assertEqual(cb.c["bruto#1"].estados["marca"]["rodada"], r + 1)
        # ninguém bate no bruto: a marca fica até o fim da rodada r + 1
        while cb.rodada <= r + 1 and not cb.fim:
            cb.agir(cb.turno_id, "defender", cb.aguardando)
            if cb.rodada == r + 1:
                self.assertIn("marca", cb.c["bruto#1"].estados)
        self.assertNotIn("marca", cb.c["bruto#1"].estados)
        self.assertTrue(any(e["tipo"] == "expira" and f"fim da rodada {r + 1}" in e["texto"] for e in cb.eventos))

    def test_marca_e_gasta_no_golpe_de_outro_aliado(self):
        cb = Combate("e2", "A")
        ate(cb, "morel")
        cb.agir(cb.turno_id, "marcar", "bruto#1")
        ate(cb, "heroi", defender)
        cb.agir(cb.turno_id, "atacar", "bruto#1")
        golpe = [e for e in cb.eventos if e["tipo"] == "dano" and e.get("ator") == "heroi"][-1]
        self.assertIn("marca +50%", golpe["conta"])
        self.assertNotIn("marca", cb.c["bruto#1"].estados)

    def test_abalado_vale_no_proximo_turno_e_acaba_nele(self):
        cb = Combate("e3", "C")  # Vontade 6: o Grito de Terror só abala
        while not any(e["tipo"] == "resolve" for e in cb.eventos):
            defender(cb)
        self.assertIn("abalado", cb.c["heroi"].estados)
        self.assertIn("aterrorizado", cb.c["morel"].estados)  # Vontade 3
        ate(cb, "heroi")
        self.assertIn("abalado", cb.c["heroi"].estados)
        cb.agir(cb.turno_id, "atacar", cb.vivos("inimigo")[0])
        golpe = [e for e in cb.eventos if e["tipo"] == "dano" and e.get("ator") == "heroi"][-1]
        self.assertIn("abalado −25%", golpe["conta"])
        self.assertNotIn("abalado", cb.c["heroi"].estados)

    def test_terror_custa_a_vez_com_vontade_baixa(self):
        cb = Combate("e3", "A")
        while not any(e["tipo"] == "resolve" for e in cb.eventos):
            defender(cb)
        self.assertIn("aterrorizado", cb.c["heroi"].estados)
        n = len(cb.eventos)
        while cb.aguardando != "heroi" and not any(e["tipo"] == "perde" and e.get("ator") == "heroi" for e in cb.eventos[n:]):
            defender(cb)
        self.assertTrue(any(e["tipo"] == "perde" and e.get("ator") == "heroi" for e in cb.eventos[n:]))


class Ameacas(unittest.TestCase):
    def test_inimigo_derrotado_antes_da_preparacao(self):
        cb = Combate("t4", "A")
        self.assertTrue(cb.estado()["ameacas"])
        basico(cb, "lobo_alfa#1")
        while not cb.fim:
            basico(cb)
        self.assertEqual(cb.fim, "vitoria")
        self.assertFalse(any(e["tipo"] == "resolve" for e in cb.eventos))
        self.assertEqual(cb.resumo["preparos_desfeitos"], 1)

    def test_joelho_desfaz_e_atordoa(self):
        cb = Combate("e2", "A")
        while not cb.c["bruto#1"].preparando:
            defender(cb)
        ate(cb, "morel")
        cb.c["morel"].recurso = 60
        cb.agir(cb.turno_id, "joelho", "bruto#1")
        self.assertIsNone(cb.c["bruto#1"].preparando)
        self.assertIn("atordoado", cb.c["bruto#1"].estados)

    def test_previsao_bate_com_o_dano_real(self):
        cb = Combate("e2", "A")
        while not cb.c["bruto#1"].preparando:
            defender(cb)
        previsto = cb.estado()["ameacas"][0]["previsto"]
        while cb.c["bruto#1"].preparando:  # ninguém responde nem se defende; a previsão acompanha (a defesa expira)
            cb.agir(cb.turno_id, BASICO[cb.aguardando], "besteiro#1" if cb.c["besteiro#1"].vivo else cb.vivos("inimigo")[0])
            if cb.c["bruto#1"].preparando:
                previsto = cb.estado()["ameacas"][0]["previsto"]
        ev = next(e for e in cb.eventos if e["tipo"] == "dano" and "Golpe Esmagador" in e["texto"])
        self.assertIn(f": {previsto['agora']} de dano", ev["texto"])


class QuedaERetorno(unittest.TestCase):
    def test_retorno_antes_da_posicao_age_na_mesma_rodada(self):
        cb = Combate("t2", "A")  # Jean (Agilidade 6) antes de Morel
        self.assertEqual(cb.aguardando, "heroi")
        cb.agir(cb.turno_id, "item:pena", "morel")
        self.assertFalse(cb.c["morel"].caido)
        self.assertEqual(cb.rodada, 1)
        self.assertEqual(cb.aguardando, "morel")  # na posição dele, ainda na rodada 1
        self.assertEqual(cb.ordem.index("morel"), 1)
        self.assertEqual(cb.consumiveis["pena"], 0)

    def test_retorno_depois_da_posicao_so_na_proxima_rodada(self):
        cb = Combate("t3", "A")  # Morel (2º) já foi pulado quando Odette age
        ate(cb, "odete")
        self.assertEqual(cb.rodada, 1)
        cb.agir(cb.turno_id, "reerguer", "morel")
        self.assertFalse(cb.c["morel"].caido)
        acoes_r1 = [e for e in cb.eventos if e.get("ator") == "morel" and e["rodada"] == 1 and e["tipo"] != "pula"]
        while cb.rodada == 1:
            basico(cb)
        self.assertEqual([e for e in cb.eventos if e.get("ator") == "morel" and e["rodada"] == 1 and e["tipo"] != "pula"], acoes_r1)
        ate(cb, "morel")
        self.assertEqual(cb.rodada, 2)
        self.assertIn("reerguer", cb.c["odete"].usadas)
        self.assertEqual(cb.motivo(cb.c["odete"], "reerguer"), "Já usada nesta luta.")

    def test_queda_do_companheiro_nao_encerra_a_do_protagonista_sim(self):
        cb = Combate("e1", "A")
        cb.c["odete"].vida = 1
        cb._perder_vida(cb.c["odete"], 5, None)
        self.assertTrue(cb.c["odete"].caido)
        self.assertFalse(cb.fim)
        cb._perder_vida(cb.c["heroi"], 999, None)
        self.assertTrue(cb._conferir_fim())
        self.assertEqual(cb.fim, "derrota")


class Duplicadas(unittest.TestCase):
    def test_mesmo_turno_duas_vezes(self):
        cb = Combate("e1", "A")
        t = cb.turno_id
        self.assertTrue(cb.agir(t, BASICO[cb.aguardando], "lobo#1")["ok"])
        n = len(cb.eventos)
        r = cb.agir(t, "atacar", "lobo#1")
        self.assertFalse(r["ok"])
        self.assertEqual(len(cb.eventos), n)

    def test_acao_fora_do_kit_e_alvo_invalido(self):
        cb = Combate("e1", "A")
        self.assertFalse(cb.agir(cb.turno_id, "curar", "heroi")["ok"] if cb.aguardando != "odete" else False)
        self.assertFalse(cb.agir(cb.turno_id, BASICO[cb.aguardando], cb.aguardando)["ok"])


class Derivados(unittest.TestCase):
    def test_derivados_batem_com_o_estado_real(self):
        for d in ("A", "B", "C"):
            cb = Combate("e2", d)
            h = cb.c["heroi"]
            der = {x["id"]: x["valor"] for x in cb.derivados(h)}
            self.assertEqual(der["vida"], h.vida_max)
            self.assertEqual(der["iniciativa"], cb.ordem.index("heroi") + 1)
            self.assertEqual(der["potencia"], h.arma + h.nivel)
            self.assertEqual(der["critico"], f"{round(critico(h.atr) * 100)}%")
            self.assertEqual(der["defesa"], f"{round(reducao_defesa(h.atr) * 100)}%")
            self.assertEqual(der["custo"], f"{round(custo_mult(h.atr) * 100)}%")
            ate(cb, "heroi")
            antes = h.recurso
            custo = next(a["custo"] for a in cb.estado()["acoes"] if a["id"] == "comando")
            alvo = next(a for a in cb.aliados if a != "heroi" and not cb.c[a].caido)
            cb.agir(cb.turno_id, "comando", alvo)
            self.assertEqual(h.recurso, antes - custo)
            ate(cb, "heroi")
            cb.agir(cb.turno_id, "defender", "heroi")
            self.assertEqual(f"{round(h.estados['defesa']['red'] * 100)}%", der["defesa"])

    def test_mesmo_nivel_equipamento_e_companheiros(self):
        a, b = Combate("e1", "A"), Combate("e1", "B")
        for k in ("nivel", "arma", "protecao", "kit", "recurso_max"):
            self.assertEqual(getattr(a.c["heroi"], k), getattr(b.c["heroi"], k))
        for cid in ("odete", "morel"):
            self.assertEqual(a.c[cid].atr, b.c[cid].atr)

    def test_distribuicoes_validas(self):
        for d in C.DISTRIBUICOES.values():
            self.assertEqual(sum(d["atributos"].values()), C.PONTOS_PROTAGONISTA)
        with self.assertRaises(ValueError):
            Combate("e1", atributos=dict(C.DISTRIBUICOES["A"]["atributos"], forca=8))


class Servidor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import servidor
        cls.mod = servidor
        cls.srv = servidor.servir(0)
        cls.url = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def pedir(self, caminho, corpo=None):
        req = urllib.request.Request(self.url + caminho, data=json.dumps(corpo).encode() if corpo is not None else None,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())

    def test_reiniciar_nao_acumula_eventos(self):
        e1 = self.pedir("/api/iniciar", {"encontro": "e2", "distribuicao": "B"})
        n = len(e1["eventos"])
        self.pedir("/api/agir", {"turno_id": e1["turno_id"], "acao": "atacar", "alvo": "besteiro#1"})
        antes = len(self.pedir("/api/resultados")["resultados"])
        for _ in range(3):
            e2 = self.pedir("/api/iniciar", {"encontro": "e2", "distribuicao": "B"})
        self.assertEqual(len(e2["eventos"]), n)
        self.assertEqual(e2["rodada"], 1)
        self.assertEqual(len(self.pedir("/api/resultados")["resultados"]), antes + 3)

    def test_clique_duplo_no_servidor(self):
        e = self.pedir("/api/iniciar", {"encontro": "e1", "distribuicao": "A"})
        acao = {"turno_id": e["turno_id"], "acao": e["acoes"][0]["id"], "alvo": "lobo#1"}
        r1, r2 = self.pedir("/api/agir", acao), self.pedir("/api/agir", acao)
        self.assertTrue(r1["ok"])
        self.assertFalse(r2["ok"])
        self.assertEqual(len(r1["estado"]["eventos"]), len(r2["estado"]["eventos"]))

    def test_livre_e_comparar(self):
        livre = dict(forca=4, agilidade=4, constituicao=4, intelecto=3, percepcao=3, vontade=3, presenca=3)
        e = self.pedir("/api/iniciar", {"encontro": "e1", "distribuicao": "livre", "atributos": livre})
        self.assertEqual(e["distribuicao"], "livre")
        cols = self.pedir("/api/comparar", {"atributos": livre})["colunas"]
        self.assertEqual([c["id"] for c in cols], ["A", "B", "C", "livre"])

    def test_estaticos_do_jogo_so_leitura_e_sem_escapar(self):
        with urllib.request.urlopen(self.url + "/static/icones.js") as r:
            self.assertEqual(r.status, 200)
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(self.url + "/static/../../__init__.py")


class Isolamento(unittest.TestCase):
    def test_o_jogo_nao_carrega_o_prototipo(self):
        raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
        for pasta in ("rpg",):
            for base, _, arquivos in os.walk(os.path.join(raiz, pasta)):
                for a in arquivos:
                    if a.endswith((".py", ".js", ".html", ".css")):
                        with open(os.path.join(base, a), encoding="utf-8", errors="ignore") as f:
                            self.assertNotIn("combate-atributos", f.read(), os.path.join(base, a))


if __name__ == "__main__":
    unittest.main()
