"""Interface web: protocolo, segurança do servidor local e uma partida jogada por HTTP."""

import argparse
import json
import random
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

from rpg.__main__ import menu_principal
from rpg.web.ponte import WebUI
from rpg.web.servidor import Servidor


def eventos(base, token, cabecalhos=None):
    req = urllib.request.Request(f"{base}/eventos?token={token}", headers=cabecalhos or {})
    resp = urllib.request.urlopen(req, timeout=30)
    for linha in resp:
        linha = linha.decode("utf-8")
        if linha.startswith("data: "):
            yield json.loads(linha[6:])


class TestWeb(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.mkdtemp()
        args = argparse.Namespace(seed=11, brando=False, saves=self.pasta, velocidade="normal")
        self.ui = WebUI()
        self.ui.jogo = None
        self.srv = Servidor(self.ui).iniciar()
        self.base = self.srv.url.split("/?")[0]

        def rodar():
            try:
                menu_principal(self.ui, args)
            except SystemExit:
                pass
            finally:
                self.ui.fim()

        self.jogo = threading.Thread(target=rodar, daemon=True)
        self.jogo.start()

    def tearDown(self):
        self.ui.respostas.put((None, None))
        self.jogo.join(5)
        self.srv.parar()

    def responder(self, pid, valor, token=None):
        req = urllib.request.Request(f"{self.base}/responder", method="POST",
                                     data=json.dumps({"id": pid, "valor": valor}).encode(),
                                     headers={"X-Token": token or self.srv.token})
        return urllib.request.urlopen(req, timeout=10).status

    def test_arquivos_e_token(self):
        for caminho in ("/", "/static/app/nucleo.js", "/static/app/controles.js", "/static/css/01-base.css", "/static/css/12-acoes-combate.css", "/static/css/13-realce.css", "/static/realce.js", "/static/sprites-dados.js", "/static/som.js", "/static/sprites.js", "/static/vista.js", "/static/mapa.js", "/static/telas/base.js", "/static/telas/celebracoes.js", "/static/batalha.js", "/static/fontes/alegreya-latin-400-normal.woff2",
                        "/static/fontes/pixelify-sans-latin-400-normal.woff2"):
            with urllib.request.urlopen(self.base + caminho, timeout=10) as r:
                self.assertEqual(r.status, 200, caminho)
        for caminho in ("/static/../servidor.py", "/eventos", "/config"):
            with self.assertRaises(urllib.error.HTTPError, msg=caminho):
                urllib.request.urlopen(self.base + caminho, timeout=10)
        with self.assertRaises(urllib.error.HTTPError):
            self.responder(1, 0, token="errado")

    def test_partida_pelo_navegador(self):
        rng = random.Random(3)
        decisoes = 0
        vistos = set()
        estados = 0
        for m in eventos(self.base, self.srv.token):
            vistos.add(m["t"])
            self.assertNotEqual(m["t"], "erro", m)
            if m["t"] == "estado":
                estados += 1
                e = m["estado"]
                self.assertIn("heroi", e)
                self.assertTrue(any(n["atual"] for n in e["mapa"]["nos"]))
            elif m["t"] == "opcoes":
                decisoes += 1
                textos = [o["texto"] for o in m["opcoes"]]
                validas = [i for i, t in enumerate(textos) if not t.startswith(("Sair", "Como jogar"))]
                if "Novo jogo" in textos:
                    validas = [textos.index("Novo jogo")]
                self.assertEqual(self.responder(m["id"], rng.choice(validas)), 204)
            elif m["t"] == "continuar":
                self.responder(m["id"], None)
            elif m["t"] == "pergunta":
                self.responder(m["id"], "Teste")
            if decisoes >= 150 or m["t"] == "fim":
                break
        self.assertGreaterEqual(decisoes, 150)
        self.assertGreater(estados, 5)
        self.assertTrue({"nova_cena", "texto", "opcoes", "estado", "escolhido"} <= vistos, vistos)

    def test_recarregar_repete_a_cena(self):
        primeira = eventos(self.base, self.srv.token)
        for m in primeira:
            if m["t"] == "opcoes":
                break
        # Um segundo navegador (ou a página recarregada) recebe a cena atual, marcada como repetição.
        segunda = eventos(self.base, self.srv.token)
        repetidas = []
        for m in segunda:
            if m["t"] == "sincronizado":
                break
            repetidas.append(m)
        self.assertTrue(repetidas and all(m.get("replay") for m in repetidas))
        self.assertEqual(repetidas[-1]["t"], "opcoes")


class TestPagina(unittest.TestCase):
    """Quando a ponte abre página nova e quando só troca o título."""

    def cenas(self, passos):
        ui = WebUI()
        ui.jogo = None
        passos(ui)
        return [(m["t"], m.get("titulo"), m.get("virar", False)) for m in ui.canal.mensagens
                if m["t"] in ("nova_cena", "cabecalho")]

    def test_fim_de_evento_sem_escolha_vira_a_pagina(self):
        # O "Exausto" e a noite no acampamento: a cena abre, o texto conta o que houve e o jogo pausa, sem ninguém
        # ter escolhido nada. A volta ao lugar é página nova (a tela deixa ler e vira); antes, o texto do evento
        # ficava embaixo do título do lugar, empurrando as opções.
        def passos(ui):
            ui.cena("Exausto")
            ui.dizer("A noite passou e você não parou para dormir.")
            ui.pausar()
            ui.cena("Vale do Corvo", tipo="local")
        self.assertEqual(self.cenas(passos)[-1], ("nova_cena", "Vale do Corvo", True))

    def test_introducao_sem_texto_so_troca_o_titulo(self):
        def passos(ui):
            ui.cena("Estrada")
            ui.cena("Vale do Corvo", tipo="local")
        self.assertEqual(self.cenas(passos)[-1], ("cabecalho", "Vale do Corvo", False))


if __name__ == "__main__":
    unittest.main()
