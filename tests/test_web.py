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

    def test_chegada_vira_a_pagina_da_estrada_e_fica_com_o_menu(self):
        # A viagem: o que aconteceu na estrada pede leitura; a chegada é página nova. O menu do lugar, logo depois,
        # é a mesma página da chegada (o que se leu ao chegar fica junto das opções).
        def passos(ui):
            ui.cena("Rumo a Abrigo Branco")
            ui.dizer("Um clique sob a sua bota.")
            ui.pausar()
            ui.cena("Abrigo Branco", tipo="local")
            ui.dizer("Os muros são brancos de cal.")
            ui.pausar()
            ui.cena("Abrigo Branco", tipo="local")
        self.assertEqual(self.cenas(passos)[-2:], [("nova_cena", "Abrigo Branco", True), ("cabecalho", "Abrigo Branco", False)])

    def test_cena_que_pede_confirmacao_espera_o_continuar(self):
        # A cena de missão declara `confirmar`: o fim dela é um Continuar marcado (a tela só o aceita depois da guarda
        # de leitura) e a volta ao lugar não vira a página por tempo. O Continuar do prólogo segue como era.
        def passos(ui):
            ui.respostas.put((1, None))
            ui.respostas.put((2, None))
            ui.cena("A fonte nova")
            ui.dizer("A fonte nova brota entre pedras soltas.")
            ui.continuar(confirmar=True)
            ui.cena("Vau do Turvo", tipo="local")
            ui.cena("O vale")
            ui.dizer("Protótipo.")
            ui.continuar()
        ui = WebUI()
        ui.jogo = None
        passos(ui)
        continuares = [m for m in ui.canal.mensagens if m["t"] == "continuar"]
        self.assertEqual([m.get("confirmar") for m in continuares], [True, None])
        voltas = [(m["t"], m.get("virar", False)) for m in ui.canal.mensagens if m.get("titulo") == "Vau do Turvo"]
        self.assertEqual(voltas, [("nova_cena", False)])

    def test_carregar_o_mesmo_save_depois_do_titulo_manda_o_estado(self):
        # Salvar, sair para o título e carregar o mesmo save: o estado é idêntico ao último enviado, mas a tela o
        # apagou no título; a ponte tem de mandá-lo de novo antes do lugar aparecer.
        from rpg.jogo import Jogo
        from rpg.ui import BotUI
        g = Jogo(BotUI(random.Random(1)), seed=6, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Jean", "guerreiro", "turvo")
        ui = WebUI()
        ui.jogo = g
        ui.cena("Vau do Turvo", tipo="local")
        ui.jogo = None
        ui.cena("Crônicas da Fenda", None, "titulo")
        ui.jogo = g
        ui.cena("Vau do Turvo", tipo="local")
        tipos = [m["t"] for m in ui.canal.mensagens]
        titulo = next(i for i, m in enumerate(ui.canal.mensagens) if m.get("titulo") == "Crônicas da Fenda")
        self.assertIn("estado", tipos[titulo:])

    def mensagens(self, passos, respostas=3):
        ui = WebUI()
        ui.jogo = None
        for k in range(1, respostas + 1):
            ui.respostas.put((k, None))
        passos(ui)
        return [(m["t"], m.get("titulo") or m.get("tipo"), m.get("virar", False)) for m in ui.canal.mensagens
                if m["t"] in ("nova_cena", "cabecalho", "continuar", "celebrar")]

    def luta_vencida(self, ui, depois=()):
        ui.cena("Explorando")
        ui.dizer("Dois lobos saem do mato.")
        ui.cena("COMBATE", tipo="combate")
        ui.detalhe("Você acerta o lobo: 12 de dano.")
        ui.dizer("O lobo cai.")
        ui.fim_combate("vitoria")
        ui.celebrar("vitoria", {"inimigos": 2})
        for f in depois:
            f(ui)
        ui.celebrar("espolio", {"ouro": 5, "xp": 20})

    def test_depois_do_relatorio_so_com_a_luta_a_pagina_vira_sem_continuar(self):
        # A luta comum do explorar: o relatório (com o Continuar dele) e a pausa do fim do evento. Na página só ficou o
        # registro da luta: o lugar abre direto (sem o segundo Continuar nem a espera de leitura).
        def passos(ui):
            self.luta_vencida(ui)
            ui.celebrar("nivel", {"nivel": 2})  # a subida de nível é faixa: já foi vista
            ui.pausar()
            ui.cena("Vale do Corvo", tipo="local")
        ms = self.mensagens(passos)
        self.assertNotIn("continuar", [t for t, _, _ in ms])
        self.assertEqual(ms[-1], ("nova_cena", "Vale do Corvo", False))

    def test_depois_do_relatorio_o_exausto_nao_pede_continuar(self):
        # O caso achado na varredura: a luta, a pausa e o "Exausto" (que manda um separador): o Continuar caía na
        # página com só o registro da luta.
        def passos(ui):
            self.luta_vencida(ui)
            ui.pausar()
            ui.separador()
            ui.celebrar("exausto", {})
            ui.cena("Fogueira", tipo="menu")
        self.assertNotIn("continuar", [t for t, _, _ in self.mensagens(passos)])

    def test_narracao_depois_da_luta_guarda_a_leitura(self):
        # O evento continua depois da vitória (o mercador agradece): esse texto é novo e pede leitura antes do lugar.
        def passos(ui):
            self.luta_vencida(ui, [lambda u: u.dizer("O mercador te cobre de agradecimentos.")])
            ui.pausar()
            ui.cena("Vale do Corvo", tipo="local")
        self.assertEqual(self.mensagens(passos)[-1], ("nova_cena", "Vale do Corvo", True))

    def test_cena_de_missao_depois_da_luta_mantem_o_continuar(self):
        # A luta seguida de cena de missão: a cena abre página e o Continuar dela (confirmar) continua lá.
        def passos(ui):
            self.luta_vencida(ui)
            ui.cena("A capela")
            ui.dizer("Atrás do altar, uma porta baixa leva à sacristia.")
            ui.continuar(confirmar=True)
            ui.cena("Vau do Turvo", tipo="local")
        ms = self.mensagens(passos)
        self.assertEqual([t for t, _, _ in ms].count("continuar"), 1)
        self.assertLess([t for t, _, _ in ms].index("celebrar"), [t for t, _, _ in ms].index("continuar"))

    def test_luta_sem_vitoria_segue_como_era(self):
        # Fugir não mostra relatório: a página da fuga continua pedindo leitura antes da próxima cena.
        def passos(ui):
            ui.cena("Explorando")
            ui.cena("COMBATE", tipo="combate")
            ui.dizer("Você foge.")
            ui.fim_combate("fuga")
            ui.pausar()
            ui.cena("Rumo a Abrigo Branco")
        self.assertIn("continuar", [t for t, _, _ in self.mensagens(passos)])

    def test_introducao_sem_texto_so_troca_o_titulo(self):
        def passos(ui):
            ui.cena("Estrada")
            ui.cena("Vale do Corvo", tipo="local")
        self.assertEqual(self.cenas(passos)[-1], ("cabecalho", "Vale do Corvo", False))


class TestHudExperimental(unittest.TestCase):
    """A HUD experimental (ferramentas/prototipos/hud) só entra com o pedido explícito: sem ele, a página é a padrão e
    a pasta do protótipo não é servida; com ele, a mesma página ganha um script no fim e nada sai da pasta."""

    def abrir(self, hud):
        srv = Servidor(WebUI(), hud_experimental=hud).iniciar()
        self.addCleanup(srv.parar)
        return srv.url.split("/?")[0]

    def ler(self, url):
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.read().decode("utf-8")

    def test_padrao_sem_experimento(self):
        base = self.abrir(False)
        self.assertNotIn("/experimento/", self.ler(base + "/"))
        with self.assertRaises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(base + "/experimento/jogo/ligar.js", timeout=10)
        self.assertEqual(e.exception.code, 404)

    def test_experimental_liga_e_fica_na_pasta(self):
        base = self.abrir(True)
        pagina = self.ler(base + "/")
        self.assertIn('<script src="/experimento/jogo/ligar.js"></script>', pagina)
        self.assertEqual(pagina.count("/experimento/"), 1)
        self.assertIn("Icones4p", self.ler(base + "/experimento/icones.js"))
        self.assertIn("HUD experimental", self.ler(base + "/experimento/jogo/ligar.js"))
        for fora in ("/experimento/../../../rpg/jogo.py", "/experimento/%2e%2e/%2e%2e/%2e%2e/rpg/jogo.py"):
            with self.assertRaises(urllib.error.HTTPError) as e:
                urllib.request.urlopen(base + fora, timeout=10)
            self.assertEqual(e.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
