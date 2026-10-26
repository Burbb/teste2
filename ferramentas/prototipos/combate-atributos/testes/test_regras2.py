"""Testes dirigidos da segunda versão do protótipo de combate e atributos (fora da suíte do jogo).

    python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
"""
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

os.environ.setdefault("DEMO_SAVES", tempfile.mkdtemp(prefix="combate-atributos-teste-"))

from motor2 import conteudo as C  # noqa: E402
from motor2 import regras as R  # noqa: E402
from motor2.regras import Combate  # noqa: E402

BASICO = {"heroi": "atacar", "odete": "atacar", "morel": "atacar"}
FORCA = C.BUILDS["forca"]


def atr(**mudar):
    """A distribuição da Força com pontos trocados de lugar (a soma continua 30)."""
    a = dict(FORCA["atributos"])
    a.update(mudar)
    return a


def basico(cb, alvo=None):
    return cb.agir(cb.turno_id, "atacar", alvo or cb.vivos("inimigo")[0])


def defender(cb):
    return cb.agir(cb.turno_id, "defender", cb.aguardando)


def ate(cb, quem, passar=None):
    for _ in range(60):
        if cb.fim or cb.aguardando == quem:
            return
        (passar or basico)(cb)
    raise AssertionError(f"a vez de {quem} não chegou")


class Atributos(unittest.TestCase):
    def test_atributos_ofensivos_entram_no_dano_ponto_a_ponto(self):
        h = C.HABILIDADES
        anterior = None
        for f in range(1, 11):
            cb = Combate("e2", atributos=dict(forca=f, agilidade=3, constituicao=7, intelecto=1, percepcao=4,
                                                vontade=6), kit=[], soma_exata=False)
            p = cb.c["heroi"].potencia("fisico")
            if anterior is not None:
                self.assertEqual(p - anterior, 1)  # cada ponto de Força, +1 de potência física
            anterior = p
            self.assertEqual(p, cb.c["heroi"].arma + cb.c["heroi"].nivel + f)
        a, b = Combate("e2", atributos=atr(forca=9, intelecto=1)), Combate("e2", atributos=atr(forca=5, intelecto=5))
        alvo = a.c["bruto#1"]
        self.assertGreater(a.prever_golpe(a.c["heroi"], alvo, h["golpe_pesado"])["normal"],
                           b.prever_golpe(b.c["heroi"], b.c["bruto#1"], h["golpe_pesado"])["normal"])
        self.assertLess(a.prever_golpe(a.c["heroi"], alvo, h["lamina"])["normal"],
                        b.prever_golpe(b.c["heroi"], b.c["bruto#1"], h["lamina"])["normal"])

    def test_beneficios_graduais_sem_desbloqueio(self):
        """Cada ponto soma o mesmo até o teto: nenhum salto num valor de atributo."""
        for f, por, teto, chave in ((R.critico, R.CRITICO_POR_PONTO, R.CRITICO_TETO, "percepcao"),
                                    (R.ponto_fraco, R.PONTO_FRACO_POR_PONTO, R.PONTO_FRACO_TETO, "percepcao"),
                                    (R.corporal, R.CORPORAL_POR_PONTO, R.CORPORAL_TETO, "constituicao")):
            vals = [f({chave: v}) for v in range(1, 11)]
            for v, x in zip(range(1, 11), vals):
                self.assertAlmostEqual(x, min(teto, por * v))
        for v in range(1, 11):
            cb = Combate("e1", atributos=dict(forca=1, agilidade=1, constituicao=1, intelecto=1, percepcao=1, vontade=v),
                         kit=[], soma_exata=False)
            self.assertAlmostEqual(R.tenacidade_de(cb.c["heroi"]), min(R.TENACIDADE_TETO, 0.04 * v))
            self.assertLess(R.tenacidade_de(cb.c["heroi"]), 1)  # nunca imunidade
            self.assertEqual(cb.c["heroi"].vida_max, 40 + 6 * 3 + 4 * 1)

    def test_presenca_nao_muda_a_luta(self):
        def jogar(p):
            cb = Combate("e2", "forca", presenca=p)
            for _ in range(25):
                if cb.fim:
                    break
                basico(cb)
            return [e["texto"] for e in cb.eventos], cb.derivados(cb.c["heroi"])
        self.assertEqual(jogar(1), jogar(10))
        f1, f10 = R.ficha(FORCA["atributos"], FORCA["kit"], presenca=1), R.ficha(FORCA["atributos"], FORCA["kit"], presenca=10)
        self.assertEqual(f1["dano"], f10["dano"])
        self.assertEqual(f1["derivados"], f10["derivados"])
        self.assertNotIn("presenca", C.ATRIBUTOS)

    def test_comando_sem_presenca(self):
        self.assertEqual(C.HABILIDADES["comando"]["bonus"], 0.3)
        cb = Combate("e2", "forca", presenca=10)
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "comando", "morel")
        self.assertEqual(cb.c["morel"].estados["comando"]["bonus"], 0.3)

    def test_ordem_pela_agilidade_calculada_uma_vez(self):
        cb = Combate("e3", "precisao")
        antes = list(cb.ordem)
        cb.c["heroi"].atr["agilidade"] = 1
        for _ in range(12):
            if cb.fim:
                break
            defender(cb)
        self.assertEqual(cb.ordem[:len(antes)], antes)
        self.assertEqual(Combate("e2", "precisao").ordem[0], "heroi")
        self.assertEqual(Combate("e2", "baluarte").ordem.index("heroi"), 4)


class Tenacidade(unittest.TestCase):
    def test_chance_final_mostrada_e_usada(self):
        cb = Combate("e2", "baluarte")  # Vontade 10: 40%; o Esmagador aplica 10%
        while not cb.c["bruto#1"].preparando:
            defender(cb)
        am = cb.estado()["ameacas"][0]
        quem = cb.c[am["quem"]]
        self.assertAlmostEqual(am["resiste"], max(0, R.tenacidade_de(quem) - 0.10))
        quem.vida = quem.vida_max = 999  # condição de teste: o alvo aguenta o golpe, para o controle ser sorteado
        while cb.c["bruto#1"].preparando:
            cb.agir(cb.turno_id, "atacar", "besteiro#1" if cb.c["besteiro#1"].vivo else cb.vivos("inimigo")[0])
        ev = [e for e in cb.eventos if e["tipo"] == "efeito" and e.get("alvo") == quem.id][-1]
        self.assertIn(R.pct(am["resiste"]), ev["texto"])

    def test_aplicacao_do_atacante_desconta_uma_vez(self):
        cb = Combate("e2", "baluarte")
        h = cb.c["heroi"]
        self.assertAlmostEqual(cb.chance_resistir(h, 0.10), 0.30)
        self.assertAlmostEqual(cb.chance_resistir(h, 0.0), 0.40)
        self.assertEqual(cb.chance_resistir(cb.c["morel"], 0.20), 0.0)  # nunca negativa

    def test_sorteio_unico_e_juramento_impede(self):
        cb = Combate("e3", "baluarte")
        o = cb.c["morel"]
        n = []
        cb.rng.random = lambda: (n.append(1), 0.99)[1]  # nunca resiste
        cb._controlar(o, "atordoado", 0.0, "teste")
        self.assertEqual(len(n), 1)
        self.assertIn("atordoado", o.estados)
        o.estados = {"juramento": {"marco": "inicio_turno", "de": "heroi", "red": 0.5}}
        cb._controlar(o, "atordoado", 0.0, "teste")
        self.assertNotIn("atordoado", o.estados)

    def test_defesa_deliberada_nao_depende_da_sorte(self):
        cb = Combate("e2", "forca")
        while not cb.c["bruto#1"].preparando:
            defender(cb)
        mira = cb.estado()["ameacas"][0]["mira"]
        ate(cb, "heroi", defender)
        if mira != "heroi":
            cb.agir(cb.turno_id, "proteger", mira)
        while cb.c["bruto#1"].preparando:
            defender(cb)
        golpe = [e for e in cb.eventos if e["tipo"] == "dano" and "Esmagador" in e["texto"]][-1]
        self.assertEqual(golpe["alvo"], "heroi")  # o Proteger leva o golpe, sem sorteio


class Kit(unittest.TestCase):
    def test_orcamento_espacos_e_uma_ultimate(self):
        self.assertIsNone(R.validar_kit(FORCA["kit"]))
        self.assertIn("ultimate", R.validar_kit(["furia", "juramento"]))
        self.assertIn("orçamento", R.validar_kit(["golpe_pesado", "lamina", "escudo_golpe", "desafio", "corte", "proteger"]))
        self.assertIn("No máximo 6", R.validar_kit(["corte", "proteger", "comando", "golpe_pesado", "lamina",
                                                    "escudo_golpe", "desafio"]))
        self.assertEqual(R.validar_kit(["corte", "corte"]), "Habilidade repetida.")
        self.assertIsNotNone(R.validar_kit(["atacar"]))  # os básicos não entram no kit
        caras = [k for k, h in C.HABILIDADES.items() if h.get("tier") in (2, 3, "ultimate")]
        self.assertGreater(R.pontos_kit(caras), C.KIT_PONTOS)  # não dá para levar todas as caras
        with self.assertRaises(ValueError):
            Combate("e1", "forca", kit=["furia", "tempestade"])

    def test_basicos_fora_do_kit_e_gastam_a_acao(self):
        cb = Combate("e1", "forca", kit=[])
        ate(cb, "heroi")
        ids = [a["id"] for a in cb.estado()["acoes"]]
        self.assertEqual(ids[:2], ["atacar", "defender"])
        self.assertIn("item:pocao", ids)
        t = cb.turno_id
        cb.agir(t, "defender", "heroi")
        self.assertNotEqual(cb.aguardando, "heroi")
        self.assertFalse(cb.agir(cb.turno_id, "golpe_pesado", "lobo#1")["ok"])  # fora do kit

    def test_ultimate_pede_impeto_e_zera(self):
        cb = Combate("t5", "forca")
        ate(cb, "heroi")
        self.assertEqual(cb.c["heroi"].impeto, 3)
        self.assertIsNone(cb.motivo(cb.c["heroi"], "furia"))
        n = len(cb.inimigos)
        cb.agir(cb.turno_id, "furia", "heroi")
        self.assertEqual(cb.c["heroi"].impeto, 0)
        self.assertEqual(len([e for e in cb.eventos if e["tipo"] == "dano" and e.get("ator") == "heroi"]), n)
        self.assertIn("Ímpeto 0", Combate("e1", "forca").motivo(Combate("e1", "forca").c["heroi"], "furia"))

    def test_impeto_sobe_com_queda_e_ameaca_desfeita(self):
        cb = Combate("t4", "forca")
        basico(cb, "lobo_alfa#1")
        self.assertEqual(cb.c["heroi"].impeto, 2)  # o Bote desfeito e o lobo caído


class Recurso(unittest.TestCase):
    def test_recupera_no_turno_e_no_basico(self):
        cb = Combate("e1", "forca")
        ate(cb, "heroi")
        h = cb.c["heroi"]
        self.assertEqual(h.recurso, C.RECURSO_INICIO + C.RECURSO_TURNO)
        cb.agir(cb.turno_id, "golpe_pesado", "lobo#1")
        depois = h.recurso
        ate(cb, "heroi")
        self.assertEqual(h.recurso, depois + C.RECURSO_TURNO)
        cb.agir(cb.turno_id, "atacar", cb.vivos("inimigo")[0])
        self.assertEqual(h.recurso, depois + C.RECURSO_TURNO + C.RECURSO_BASICO)
        r = cb.resumo["recurso"]["heroi"]
        self.assertEqual(r["gasto"], 25)
        self.assertEqual(r["basico"], C.RECURSO_BASICO)


class Previsao(unittest.TestCase):
    def test_previsao_igual_ao_dano_real(self):
        for b in C.BUILDS:
            cb = Combate("e2", b)
            vistos = 0
            for _ in range(40):
                if cb.fim:
                    break
                a = cb.estado()["acoes"]
                golpes = [x for x in a if x.get("previsoes") and not x["motivo"] and x["alvo"] == "inimigo"]
                x = golpes[-1]
                alvo = sorted(x["previsoes"])[0]
                p = x["previsoes"][alvo]
                n = len(cb.eventos)
                cb.agir(cb.turno_id, x["id"], alvo)
                ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e.get("alvo") == alvo)
                real = int(ev["texto"].split(": ")[-1].split(" ")[0])
                self.assertEqual(real, p["critico"] if "crítico" in ev["conta"] else p["normal"], (b, x["id"], ev))
                vistos += 1
            self.assertGreater(vistos, 5)

    def test_previsao_da_ameaca_igual_ao_real(self):
        cb = Combate("e2", "forca")
        while not cb.c["bruto#1"].preparando:
            defender(cb)
        prev = cb.estado()["ameacas"][0]
        while cb.c["bruto#1"].preparando:
            cb.agir(cb.turno_id, "atacar", "besteiro#1" if cb.c["besteiro#1"].vivo else cb.vivos("inimigo")[0])
            if cb.c["bruto#1"].preparando:
                prev = cb.estado()["ameacas"][0]
        ev = next(e for e in cb.eventos if e["tipo"] == "dano" and "Esmagador" in e["texto"])
        self.assertIn(f": {prev['agora']} de dano", ev["texto"])

    def test_tabela_da_ficha_bate_com_a_luta(self):
        f = R.ficha(FORCA["atributos"], FORCA["kit"])
        cb = Combate("e2", "forca")
        h, alvo = cb.c["heroi"], cb.c["bruto#1"]
        for x in f["dano"]:
            self.assertEqual(x["normal"], cb.prever_golpe(h, alvo, C.HABILIDADES[x["id"]])["normal"])

    def test_equipamento_aumenta_o_resultado(self):
        eq = R.comparar_equipamento(FORCA["atributos"], FORCA["kit"], "arma")
        atacar = [next(d["normal"] for d in l["dano"] if d["id"] == "atacar") for l in eq["linhas"]]
        self.assertEqual(atacar, sorted(atacar))
        self.assertGreater(atacar[-1], atacar[0])


class Combinado(unittest.TestCase):
    """O que a v1 já garantia e a v2 preserva."""

    def test_atordoado_perde_a_vez_e_rodada_fecha(self):
        cb = Combate("t1", "forca")
        while cb.rodada == 1:
            basico(cb, "lobo#1")
        self.assertEqual(len([e for e in cb.eventos if e["tipo"] == "perde" and e.get("ator") == "heroi"]), 1)

    def test_retorno_antes_e_depois_da_posicao(self):
        cb = Combate("t2", "forca")
        self.assertEqual(cb.aguardando, "heroi")
        cb.agir(cb.turno_id, "item:pena", "morel")
        self.assertEqual((cb.aguardando, cb.rodada), ("morel", 1))
        cb = Combate("t3", "forca")
        ate(cb, "odete")
        cb.agir(cb.turno_id, "reerguer", "morel")
        while cb.rodada == 1:
            basico(cb)
        self.assertFalse([e for e in cb.eventos if e.get("ator") == "morel" and e["rodada"] == 1 and e["tipo"] != "pula"])

    def test_inimigo_derrotado_antes_da_preparacao(self):
        cb = Combate("t4", "forca")
        basico(cb, "lobo_alfa#1")
        self.assertEqual(cb.fim, "vitoria")
        self.assertFalse([e for e in cb.eventos if e["tipo"] == "resolve"])

    def test_interrupcao_uma_vez_depois_firme(self):
        cb = Combate("e2", "forca")
        for vez in (1, 2):
            while not cb.c["bruto#1"].preparando:
                defender(cb)
            ate(cb, "morel", defender)
            cb.c["morel"].recurso = 60
            cb.agir(cb.turno_id, "joelho", "bruto#1")
            if vez == 1:
                self.assertIsNone(cb.c["bruto#1"].preparando)
            else:
                self.assertTrue(cb.c["bruto#1"].preparando["firme"])

    def test_mesma_vez_duas_vezes(self):
        cb = Combate("e1", "forca")
        t = cb.turno_id
        self.assertTrue(basico(cb)["ok"])
        n = len(cb.eventos)
        self.assertFalse(cb.agir(t, "atacar", "lobo#1")["ok"])
        self.assertEqual(len(cb.eventos), n)

    def test_invocacao_no_fim_da_ordem(self):
        cb = Combate("e3", "forca")
        while not any(e["tipo"] == "invoca" for e in cb.eventos):
            defender(cb)
        self.assertEqual(cb.ordem[-1], "afogado#1")
        self.assertEqual(cb.c["afogado#1"].entra_rodada, 2)


class Servidor2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import servidor
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

    def test_as_duas_versoes(self):
        with urllib.request.urlopen(self.url + "/") as r:
            self.assertIn("v2", r.read().decode())
        with urllib.request.urlopen(self.url + "/v1/") as r:
            self.assertIn("v1", r.read().decode())

    def test_iniciar_reiniciar_e_clique_duplo(self):
        e = self.pedir("/api2/iniciar", {"encontro": "e2", "build": "precisao", "kit": C.BUILDS["precisao"]["kit"]})
        n = len(e["eventos"])
        acao = {"turno_id": e["turno_id"], "acao": "atacar", "alvo": "besteiro#1"}
        r1, r2 = self.pedir("/api2/agir", acao), self.pedir("/api2/agir", acao)
        self.assertTrue(r1["ok"])
        self.assertFalse(r2["ok"])
        antes = len(self.pedir("/api2/resultados")["resultados"])
        for _ in range(3):
            e2 = self.pedir("/api2/iniciar", {"encontro": "e2", "build": "precisao"})
        self.assertEqual(len(e2["eventos"]), n)
        res = self.pedir("/api2/resultados")["resultados"]
        self.assertEqual(len(res), antes + 3)
        self.assertIn("kit", res[-1])
        self.assertIn("recurso", res[-1])

    def test_kit_invalido_recusado_e_ficha_parcial(self):
        with self.assertRaises(urllib.error.HTTPError):
            self.pedir("/api2/iniciar", {"encontro": "e1", "build": "forca", "kit": ["furia", "tempestade"]})
        f = self.pedir("/api2/ficha", {"atributos": dict(FORCA["atributos"], forca=5), "kit": FORCA["kit"]})
        self.assertIn("A soma", f["erro_atributos"])
        self.assertTrue(f["dano"])
        self.assertEqual(len(self.pedir("/api2/comparar", {})["colunas"]), len(C.BUILDS))


if __name__ == "__main__":
    unittest.main()
