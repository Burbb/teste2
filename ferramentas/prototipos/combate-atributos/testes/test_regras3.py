"""Testes dirigidos da terceira versão do protótipo de combate e atributos (fora da suíte do jogo).

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

from motor3 import conteudo as C  # noqa: E402
from motor3 import regras as R  # noqa: E402
from motor3.regras import Combate  # noqa: E402

H = C.HABILIDADES


def atr(base="forca", **mudar):
    a = dict(C.BUILDS[base]["atributos"])
    a.update(mudar)
    return a


def basico(cb, alvo=None):
    return cb.agir(cb.turno_id, "atacar", alvo or cb.vivos("inimigo")[0])


def defender(cb):
    return cb.agir(cb.turno_id, "defender", cb.aguardando)


def ate(cb, quem, passar=None):
    for _ in range(80):
        if cb.fim or cb.aguardando == quem:
            return
        (passar or basico)(cb)
    raise AssertionError(f"a vez de {quem} não chegou")


def dano_do_evento(ev):
    return int(ev["texto"].split(": ")[-1].split(" ")[0])


class TiposEDefesas(unittest.TestCase):
    def test_previsao_igual_ao_real_por_tipo_e_alvo(self):
        casos = (("e2", "forca", "golpe_pesado", "bruto#1"), ("e3", "runa", "lamina", "xama#1"),
                 ("e4", "chama", "brasa", "cao#1"), ("e4", "runa", "lamina", "cao#2"), ("e3", "forca", "atacar", "esqueleto#1"))
        for enc, b, hid, alvo in casos:
            cb = Combate(enc, b)
            ate(cb, "heroi", defender)
            x = next(a for a in cb.estado()["acoes"] if a["id"] == hid)
            p = x["previsoes"][alvo]
            n = len(cb.eventos)
            cb.agir(cb.turno_id, hid, alvo)
            ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e.get("alvo") == alvo)
            self.assertEqual(dano_do_evento(ev), p["critico"] if "crítico" in ev["conta"] else p["normal"], (enc, hid, ev))

    def test_resistencia_e_penetracao_na_ordem_e_no_teto(self):
        cb = Combate("e3", "runa")
        h, xama = cb.c["heroi"], cb.c["xama#1"]
        pot = h.potencia(H["lamina"]) * H["lamina"]["mult"]
        d, partes = cb.conta_golpe(h, xama, H["lamina"], False)
        self.assertEqual(d, max(1, round(pot * (1 - (0.30 - 0.10)))))  # 30% − penetração 10%
        xama.res["arcano"] = 0.95
        d2, _ = cb.conta_golpe(h, xama, H["lamina"], False)
        self.assertEqual(d2, max(1, round(pot * (1 - C.RESISTENCIA_TETO))))  # nunca acima do teto
        xama.res["arcano"] = 0.05
        self.assertEqual(xama.resistencia("arcano", 0.10), 0.0)  # penetração não deixa negativo

    def test_sem_mitigacao_duplicada(self):
        cb = Combate("e3", "runa")
        h, xama = cb.c["heroi"], cb.c["xama#1"]
        antes, _ = cb.conta_golpe(h, xama, H["lamina"], False)
        xama.protecao = 50  # a proteção não toca o arcano
        self.assertEqual(cb.conta_golpe(h, xama, H["lamina"], False)[0], antes)
        xama.protecao, xama.res = 1, {"fisico": 0.9}  # e resistência de outro tipo não toca o físico
        fis = cb.conta_golpe(h, xama, H["atacar"], False)[0]
        self.assertEqual(fis, max(1, round(h.potencia(H["atacar"])) - 1))

    def test_resistencia_do_equipamento_reduz_o_dano_recebido(self):
        a = Combate("e4", "forca", equip={"manto": "comum"})
        b = Combate("e4", "forca", equip={"manto": "salamandra"})
        self.assertLess(b.dano_inimigo(b.c["heroi"], 16, "fogo")[0], a.dano_inimigo(a.c["heroi"], 16, "fogo")[0])
        self.assertEqual(a.dano_inimigo(a.c["heroi"], 16, "fisico")[0], b.dano_inimigo(b.c["heroi"], 16, "fisico")[0])
        self.assertEqual(b.c["heroi"].resistencia("fogo"), 0.35)

    def test_toda_habilidade_de_dano_diz_tipo_escala_e_defesa(self):
        for k, h in H.items():
            if "mult" in h:
                d = R.descrever(h)
                self.assertTrue(d["tipo"] and d["escala"] and d["defesa"], k)


class Atributos(unittest.TestCase):
    def test_vontade_aumenta_a_reserva_sem_mudar_o_resto(self):
        a = Combate("e2", atributos=dict(forca=9, agilidade=3, constituicao=7, intelecto=1, percepcao=4, vontade=6), kit=[])
        b = Combate("e2", atributos=dict(forca=9, agilidade=3, constituicao=7, intelecto=1, percepcao=4, vontade=9),
                    kit=[], soma_exata=False)
        self.assertEqual(b.c["heroi"].recurso_max - a.c["heroi"].recurso_max, 3 * C.RECURSO_VONTADE)
        self.assertEqual(a.c["heroi"].recurso, a.c["heroi"].recurso_max)  # começa cheio
        da = {d["id"]: d["valor"] for d in a.derivados(a.c["heroi"])}
        db = {d["id"]: d["valor"] for d in b.derivados(b.c["heroi"])}
        mudou = {k for k in da if da[k] != db[k]}
        self.assertEqual(mudou, {"recurso_max", "tenacidade"})

    def test_reserva_basica_faz_a_combinacao_sem_ataque_basico(self):
        cb = Combate("t6", atributos=atr("chama", vontade=1, constituicao=9), kit=["brasa", "combustao"])
        h = cb.c["heroi"]
        self.assertEqual(h.recurso_max, C.RECURSO_BASE + C.RECURSO_NIVEL * 3 + C.RECURSO_VONTADE)
        for hid in ("brasa", "brasa", "combustao"):
            ate(cb, "heroi", defender)
            self.assertIsNone(cb.motivo(h, hid))
            cb.agir(cb.turno_id, hid, "esqueleto#1")
        self.assertEqual(cb.resumo["acoes"].get("atacar", 0), 0)
        self.assertNotIn("queimadura", cb.c["esqueleto#1"].estados)  # consumida

    def test_combinacao_soma_e_consome(self):
        cb = Combate("t6", "chama")
        h, alvo = cb.c["heroi"], cb.c["esqueleto#1"]
        sem, _ = cb.conta_golpe(h, alvo, H["combustao"], False)
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "brasa", "esqueleto#1")
        ate(cb, "heroi", defender)
        q = cb.queima_restante(alvo)
        self.assertGreater(q, 0)
        com, partes = cb.conta_golpe(h, alvo, H["combustao"], False)
        esperado = (h.potencia(H["combustao"]) * H["combustao"]["mult"] + 2.0 * q) * (1 + R.ponto_fraco(h.atr))
        self.assertEqual(com, round(esperado))  # o Soldado tem ponto fraco; fogo sem resistência nele
        self.assertGreater(com, sem)

    def test_avanco_pela_vida_sem_bonus_global(self):
        a = Combate("e2", atributos=atr("baluarte"), kit=["avanco"])
        b = Combate("e2", atributos=atr("baluarte", constituicao=8, forca=6), kit=["avanco"])
        ha, hb = a.c["heroi"], b.c["heroi"]
        self.assertEqual(round(ha.potencia(H["avanco"]) - hb.potencia(H["avanco"]), 2), round(0.25 * R.VIDA_POR_PONTO, 2))
        self.assertEqual(hb.potencia(H["atacar"]) - ha.potencia(H["atacar"]), 1)  # o Atacar não liga para a vida
        self.assertEqual(ha.potencia(H["lamina"]), hb.potencia(H["lamina"]))
        self.assertNotIn("forca", H["avanco"]["escala"])

    def test_sem_desbloqueios_e_presenca_fora(self):
        for v in range(1, 11):
            self.assertAlmostEqual(R.critico({"percepcao": v}), min(0.25, 0.02 * v))
            self.assertAlmostEqual(R.ponto_fraco({"percepcao": v}), min(0.30, 0.03 * v))
        def jogar(p):
            cb = Combate("e2", "forca", presenca=p)
            for _ in range(20):
                if cb.fim:
                    break
                basico(cb)
            return [e["texto"] for e in cb.eventos]
        self.assertEqual(jogar(1), jogar(10))


class Ultimate(unittest.TestCase):
    def test_disponivel_desde_o_inicio_uma_vez(self):
        cb = Combate("e2", "forca")
        ate(cb, "heroi", defender)
        h = cb.c["heroi"]
        self.assertIsNone(cb.motivo(h, "furia"))
        cb.agir(cb.turno_id, "furia", "heroi")
        ate(cb, "heroi", defender)
        self.assertEqual(cb.motivo(h, "furia"), "Ultimate já usada nesta luta.")
        u = cb.resumo["ultimates"]["heroi"]
        self.assertEqual(u["uso"]["rodada"], 1)
        self.assertGreaterEqual(u["turnos_ja_usada"], 1)
        self.assertIsNone(Combate("e2", "precisao").estado_ultimate(Combate("e2", "precisao").c["heroi"]))

    def test_queda_e_retorno_nao_devolvem(self):
        cb = Combate("t5", "forca")
        o = cb.c["odete"]
        o.vida = o.vida_max  # para chegar viva à vez dela; a queda vem depois, à mão
        ate(cb, "odete")
        cb.agir(cb.turno_id, "luz_restauradora", "odete")
        self.assertTrue(o.ultimate_usada)
        cb._perder_vida(o, 999, None)
        self.assertTrue(o.caido)
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "item:pena", "odete")
        self.assertFalse(o.caido)
        ate(cb, "odete")
        self.assertEqual(cb.motivo(o, "luz_restauradora"), "Ultimate já usada nesta luta.")
        self.assertTrue(any("continua gasta" in e["texto"] for e in cb.eventos if e["tipo"] == "retorno"))

    def test_falta_recurso_aparece(self):
        cb = Combate("e2", "forca")
        ate(cb, "heroi", defender)
        cb.c["heroi"].recurso = 5
        self.assertEqual(cb.estado_ultimate(cb.c["heroi"])["estado"], "recurso")


class AmeacasDoBruto(unittest.TestCase):
    def test_atordoar_no_turno_da_preparacao_adia_nao_apaga(self):
        cb = Combate("e2", "precisao")
        for _ in range(200):
            if cb.fim or len(cb.resumo["ameacas"]) >= 2:
                break
            if cb.aguardando == "morel" and cb.c["bruto#1"].turnos_agidos == 1 and not cb.c["bruto#1"].estados:
                cb.c["morel"].recurso = 60
                cb.agir(cb.turno_id, "joelho", "bruto#1")
            else:
                defender(cb)
        self.assertTrue(cb.resumo["adiamentos"], "o turno perdido do Bruto foi anotado")
        self.assertTrue(cb.resumo["ameacas"], "a preparação veio depois do atordoamento")
        self.assertGreater(cb.resumo["controles"]["inimigos"]["sofridos"], 0)

    def test_interrupcao_registrada_e_sem_firme_geral(self):
        cb = Combate("e2", "forca")
        for vez in (1, 2):
            while not cb.c["bruto#1"].preparando:
                defender(cb)
            ate(cb, "morel", defender)
            cb.c["morel"].recurso = 60
            cb.agir(cb.turno_id, "joelho", "bruto#1")
            self.assertIsNone(cb.c["bruto#1"].preparando)  # a segunda também se desfaz
        res = [a["resultado"] for a in cb.resumo["ameacas"]]
        self.assertEqual(res[:2], ["interrompida", "interrompida"])

    def test_furioso_ininterruptivel_sinalizado(self):
        cb = Combate("e2", "forca")
        cb.c["bruto#1"].vida = 100  # condição de teste: abaixo da metade
        while not cb.c["bruto#1"].preparando:
            defender(cb)
        self.assertTrue(cb.estado()["ameacas"][0]["ininterruptivel"])
        ate(cb, "morel", defender)
        cb.c["morel"].recurso = 60
        cb.agir(cb.turno_id, "joelho", "bruto#1")
        self.assertIsNotNone(cb.c["bruto#1"].preparando)
        self.assertNotIn("atordoado", cb.c["bruto#1"].estados)

    def test_telemetria_das_acoes(self):
        cb = Combate("e1", "forca")
        ate(cb, "heroi")
        antes = cb.c["heroi"].recurso
        cb.agir(cb.turno_id, "golpe_pesado", "lobo#1")
        l = cb.resumo["linha"][-1]
        self.assertEqual((l["ator"], l["acao"], l["antes"], l["depois"]), ("heroi", "golpe_pesado", antes, antes - 25))


class Combinado(unittest.TestCase):
    def test_kit(self):
        self.assertIsNone(R.validar_kit(C.BUILDS["chama"]["kit"]))  # Guerreiro + especialização juntos
        self.assertIn("ultimate", R.validar_kit(["furia", "conflagracao"]))
        self.assertIsNotNone(R.validar_kit(["defender"]))
        caras = [k for k, h in H.items() if h.get("tier") in (2, 3, "ultimate")]
        self.assertGreater(R.pontos_kit(caras), C.KIT_PONTOS)

    def test_ordem_rodada_retorno_e_gestos(self):
        cb = Combate("t1", "forca")
        while cb.rodada == 1:
            basico(cb, "lobo#1")
        self.assertEqual(len([e for e in cb.eventos if e["tipo"] == "perde" and e.get("ator") == "heroi"]), 1)
        cb = Combate("t2", "forca")
        cb.agir(cb.turno_id, "item:pena", "morel")
        self.assertEqual((cb.aguardando, cb.rodada), ("morel", 1))
        cb = Combate("e1", "forca")
        t = cb.turno_id
        self.assertTrue(basico(cb)["ok"])
        self.assertFalse(cb.agir(t, "atacar", "lobo#1")["ok"])
        cb = Combate("t4", "forca")
        basico(cb, "lobo_alfa#1")
        self.assertEqual(cb.fim, "vitoria")
        self.assertEqual(cb.resumo["ameacas"][0]["resultado"], "desfeita: inimigo caiu")


class Servidor3(unittest.TestCase):
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

    def test_tres_versoes(self):
        for rota, marca in (("/", "v3"), ("/v2/", "v2"), ("/v1/", "v1")):
            with urllib.request.urlopen(self.url + rota) as r:
                self.assertIn(marca, r.read().decode())

    def test_luta_e_resultados(self):
        e = self.pedir("/api3/iniciar", {"encontro": "e2", "build": "forca", "equip": {"manto": "salamandra"}})
        acao = {"turno_id": e["turno_id"], "acao": "atacar", "alvo": "besteiro#1"}
        self.assertTrue(self.pedir("/api3/agir", acao)["ok"])
        self.assertFalse(self.pedir("/api3/agir", acao)["ok"])
        self.pedir("/api3/iniciar", {"encontro": "e1", "build": "forca"})
        r = self.pedir("/api3/resultados")["resultados"][-1]
        for k in ("ameacas", "adiamentos", "ultimates", "linha", "equip"):
            self.assertIn(k, r)
        f = self.pedir("/api3/ficha", {"build": "chama"})
        self.assertTrue(f["combo"])
        self.assertEqual(set(f["equipamento"]), {"arma", "foco", "manto"})


if __name__ == "__main__":
    unittest.main()
