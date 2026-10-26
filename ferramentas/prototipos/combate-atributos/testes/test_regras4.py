"""Testes dirigidos da quarta versão do protótipo de combate e atributos (fora da suíte do jogo): o que ela muda em
relação à terceira (sem a Marca, o Golpe Oportuno do Morel, a Chuva de Brasas) e o que precisa continuar valendo.

    python -m unittest discover -s ferramentas/prototipos/combate-atributos/testes -t ferramentas/prototipos/combate-atributos
"""
import json
import os
import tempfile
import threading
import unittest
import urllib.request

os.environ.setdefault("DEMO_SAVES", tempfile.mkdtemp(prefix="combate-atributos-teste-"))

from motor3 import conteudo as C3  # noqa: E402
from motor4 import conteudo as C  # noqa: E402
from motor4 import regras as R  # noqa: E402
from motor4.regras import Combate  # noqa: E402

H = C.HABILIDADES
CHAMA = C.BUILDS["chama"]


def defender(cb):
    return cb.agir(cb.turno_id, "defender", cb.aguardando)


def ate(cb, quem):
    for _ in range(80):
        if cb.fim or cb.aguardando == quem:
            return
        defender(cb)
    raise AssertionError(f"a vez de {quem} não chegou")


def dano_do_evento(ev):
    return int(ev["texto"].split(": ")[-1].split(" ")[0])


class SemMarca(unittest.TestCase):
    def test_marca_saiu_so_da_v4(self):
        self.assertNotIn("marcar", H)
        self.assertNotIn("marcar", C.GRUPO["morel"]["kit"])
        self.assertFalse(any("arca" in h["desc"] and "Marca" in h["desc"] for h in H.values()))
        self.assertIn("marcar", C3.HABILIDADES)  # a v3 continua como estava
        self.assertIn("marcar", C3.GRUPO["morel"]["kit"])

    def test_golpe_oportuno(self):
        cb = Combate("e2", "forca")
        ate(cb, "morel")
        m, bruto = cb.c["morel"], cb.c["bruto#1"]
        normal, _ = cb.conta_golpe(m, bruto, H["oportuno"], False)
        bruto.estados["atordoado"] = {"marco": "proxima_vez"}
        com, partes = cb.conta_golpe(m, bruto, H["oportuno"], False)
        self.assertGreater(com, normal)
        self.assertTrue(any("atordoado ou preparando" in p for p in partes))
        del bruto.estados["atordoado"]
        p = next(a for a in cb.estado()["acoes"] if a["id"] == "oportuno")["previsoes"]["bruto#1"]
        n = len(cb.eventos)
        cb.agir(cb.turno_id, "oportuno", "bruto#1")
        ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e.get("alvo") == "bruto#1")
        self.assertEqual(dano_do_evento(ev), p["critico"] if "crítico" in ev["conta"] else p["normal"])


class ChuvaDeBrasas(unittest.TestCase):
    def test_papel_no_kit(self):
        self.assertEqual(H["chuva"]["alvo"], "inimigos")
        self.assertGreater(H["chuva"]["custo"], H["brasa"]["custo"])
        self.assertEqual(C.PONTOS_TIER[H["chuva"]["tier"]], 2)
        self.assertLess(H["chuva"]["mult"], H["brasa"]["mult"])
        self.assertIsNone(R.validar_kit(CHAMA["kit"]))
        caras = ["brasa", "chuva", "combustao", "lamina", "conflagracao"]
        self.assertIsNotNone(R.validar_kit(caras))  # tudo de fogo junto não cabe

    def test_uma_camada_em_cada_inimigo_mesmo_com_resistencia(self):
        cb = Combate("t8", "chama")  # Cães de Brasa: 60% de fogo
        ate(cb, "heroi")
        x = next(a for a in cb.estado()["acoes"] if a["id"] == "chuva")
        n = len(cb.eventos)
        cb.agir(cb.turno_id, "chuva")
        for i in ("cao#1", "cao#2"):
            self.assertEqual(cb.c[i].estados["queimadura"]["pilhas"], 1)
            ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e.get("alvo") == i and e.get("ator") == "heroi")
            p = x["previsoes"][i]
            self.assertEqual(dano_do_evento(ev), p["critico"] if "crítico" in ev["conta"] else p["normal"])
            self.assertIn("resistência fogo 60%", ev["conta"])
        # o pingo previsto é o que sai
        q = x["queima"]["cao#1"]
        ate(cb, "heroi")
        pingos = [e for e in cb.eventos[n:] if e.get("periodico") and e.get("alvo") == "cao#1"]
        self.assertTrue(pingos)
        self.assertEqual(pingos[0]["valor"], q["por_pingo"])

    def test_pilhas_teto_e_expiracao(self):
        cb = Combate("t7", "chama")
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "chuva")
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "brasa", "lobo#1")
        self.assertEqual(cb.c["lobo#1"].estados["queimadura"]["pilhas"], 2)
        self.assertEqual(cb.c["lobo#2"].estados["queimadura"]["pilhas"], 1)
        for _ in range(3):
            ate(cb, "heroi")
            cb.agir(cb.turno_id, "brasa", "lobo#1")
        self.assertEqual(cb.c["lobo#1"].estados["queimadura"]["pilhas"], R.QUEIMA_PILHAS)  # teto
        for _ in range(20):
            if "queimadura" not in cb.c["lobo#2"].estados:
                break
            defender(cb)
        self.assertNotIn("queimadura", cb.c["lobo#2"].estados)  # expirou sozinha
        pingos = [e for e in cb.eventos if e.get("periodico") and e.get("alvo") == "lobo#2"]
        self.assertEqual(len(pingos), R.QUEIMA_VEZES)

    def test_conflagracao_consome_por_alvo_sem_contar_duas_vezes(self):
        cb = Combate("t7", "chama")
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "chuva")
        ate(cb, "heroi")
        restante = {i: cb.queima_restante(cb.c[i]) for i in cb.inimigos}
        x = next(a for a in cb.estado()["acoes"] if a["id"] == "conflagracao")
        vida = {i: cb.c[i].vida for i in cb.inimigos}
        n = len(cb.eventos)
        cb.agir(cb.turno_id, "conflagracao")
        for i in cb.inimigos:
            self.assertGreater(restante[i], 0)
            self.assertNotIn("queimadura", cb.c[i].estados)
            ev = next(e for e in cb.eventos[n:] if e["tipo"] == "dano" and e.get("alvo") == i and e.get("ator") == "heroi")
            p = x["previsoes"][i]
            self.assertEqual(dano_do_evento(ev), p["critico"] if "crítico" in ev["conta"] else p["normal"])
            self.assertIn(f"Queimadura restante ({R.fmt(restante[i])})", ev["conta"])
        for _ in range(12):  # depois da explosão, nenhum pingo
            defender(cb)
        depois = [e for e in cb.eventos[n:] if e.get("periodico")]
        self.assertEqual(depois, [])
        perdido = sum(vida[i] - cb.c[i].vida for i in cb.inimigos)
        direto = sum(e["valor"] for e in cb.eventos[n:] if e["tipo"] == "dano" and e.get("ator") == "heroi")
        self.assertEqual(perdido, direto)

    def test_inimigo_morto_antes_da_explosao(self):
        cb = Combate("t7", "chama")
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "chuva")
        cb.c["lobo#2"].vida = 1
        cb._perder_vida(cb.c["lobo#2"], 1, None)
        ate(cb, "heroi")
        n = len(cb.eventos)
        cb.agir(cb.turno_id, "conflagracao")
        self.assertFalse([e for e in cb.eventos[n:] if e.get("alvo") == "lobo#2"])
        self.assertEqual(len([e for e in cb.eventos[n:] if e["tipo"] == "dano" and e.get("ator") == "heroi"]), 2)

    def test_sequencia_num_encontro_normal_com_a_reserva_basica(self):
        cb = Combate("e3", "chama")  # sem condição de teste: o xamã, o soldado e o afogado que ele chama
        h = cb.c["heroi"]
        self.assertGreaterEqual(h.recurso_max, H["chuva"]["custo"] + H["conflagracao"]["custo"])
        ate(cb, "heroi")
        cb.agir(cb.turno_id, "chuva")
        ate(cb, "heroi")
        queimando = [i for i in cb.vivos("inimigo") if "queimadura" in cb.c[i].estados]
        self.assertGreaterEqual(len(queimando), 2)
        self.assertIsNone(cb.motivo(h, "conflagracao"))
        cb.agir(cb.turno_id, "conflagracao")
        self.assertFalse(any("queimadura" in cb.c[i].estados for i in queimando))
        ate(cb, "heroi")
        self.assertEqual(cb.motivo(h, "conflagracao"), "Ultimate já usada nesta luta.")


class Comparacao(unittest.TestCase):
    def test_papeis_aparecem_nos_numeros(self):
        L = {(l["grupo"], l["rotulo"]): l for l in R.comparar_fogo(CHAMA["atributos"], CHAMA["kit"])}
        bc = L[("um", "Brasa → Combustão")]
        cc = L[("um", "Chuva de Brasas → Combustão (área num alvo só)")]
        self.assertGreater(bc["total"] / bc["custo"], cc["total"] / cc["custo"])  # num alvo só, a Brasa rende mais
        ch = L[("grupo", "Chuva de Brasas → Conflagração")]
        b3 = L[("grupo", "Brasa em cada um (3) → Conflagração")]
        self.assertLess(ch["acoes"], b3["acoes"])
        self.assertGreaterEqual(ch["total"] / ch["acoes"], b3["total"] / b3["acoes"])
        rs = L[("resistente", "Chuva de Brasas → Conflagração")]
        self.assertLess(rs["total"] / rs["alvos"], ch["total"] / ch["alvos"])
        for l in L.values():
            self.assertEqual(l["total"], l["direto"] + l["periodico"])
            self.assertLessEqual(l["custo"], l["recurso_antes"] + 6 * l["acoes"])


class Servidor4(unittest.TestCase):
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

    def test_v4_na_raiz_e_v3_preservada(self):
        for rota, marca in (("/", "v4"), ("/v3/", "v3"), ("/v2/", "v2"), ("/v1/", "v1")):
            with urllib.request.urlopen(self.url + rota) as r:
                self.assertIn(marca, r.read().decode())
        self.assertTrue(any(h["id"] == "chuva" for h in self.pedir("/api4/catalogo")["habilidades"]))
        self.assertFalse(any(h["id"] == "chuva" for h in self.pedir("/api3/catalogo")["habilidades"]))

    def test_luta_gesto_duplo_e_ficha_com_fogo(self):
        e = self.pedir("/api4/iniciar", {"encontro": "e3", "build": "chama"})
        acao = {"turno_id": e["turno_id"], "acao": "chuva"}
        self.assertTrue(self.pedir("/api4/agir", acao)["ok"])
        self.assertFalse(self.pedir("/api4/agir", acao)["ok"])
        f = self.pedir("/api4/ficha", {"build": "chama"})
        self.assertTrue(f["fogo"])


if __name__ == "__main__":
    unittest.main()
