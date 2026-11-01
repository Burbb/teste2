"""DEMONSTRAÇÃO do protótipo de campo livre da etapa 8 (nada no jogo): o herói em tempo real no meio de tropas pequenas.

    python ferramentas/prototipos/etapa8-campo/servidor.py

Só serve arquivos: a batalha inteira roda no navegador (tela/sim.js), em tempo real, sem passar pelo motor do jogo.
Tenta a porta 8801 (ou DEMO_PORTA). Se ela estiver ocupada, diz quem está nela e usa a próxima livre, abrindo o
navegador na porta certa. A versão (tela/conteudo.js, VERSAO) aparece no terminal, no título e no topo da página.
DEMO_SEM_NAVEGADOR=1 não abre o navegador. As fontes e a paleta da interface vêm de rpg/web/static (só leitura)."""
import json
import mimetypes
import os
import pathlib
import re
import socket
import threading
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
JOGO = RAIZ / "rpg" / "web" / "static"
TELA = AQUI / "tela"
TELA_V1 = AQUI / "tela-v1"   # a primeira versão jogável (Campo Livre 1), congelada para comparar: /v1/
TELA_V4 = AQUI / "tela-v4"   # o Campo Livre 4 (o básico antigo, Corte e Faísca), congelado para comparar: /v4/
PORTA = int(os.environ.get("DEMO_PORTA", "8801"))
VERSAO = re.search(r'VERSAO = "([^"]+)"', (TELA / "conteudo.js").read_text(encoding="utf-8")).group(1)
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/javascript", ".mjs")


class Demo(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _arquivo(self, caminho):
        if not caminho.is_file():
            self.send_error(404)
            return
        dados = caminho.read_bytes()
        tipo = mimetypes.guess_type(str(caminho))[0] or "application/octet-stream"
        if tipo.startswith("text/") or tipo == "application/json":
            tipo += "; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        rota = unquote(urlparse(self.path).path)
        if rota in ("/", "/index.html"):
            return self._arquivo(TELA / "index.html")
        if rota == "/api/versao":
            corpo = json.dumps({"prototipo": "etapa8-campo", "versao": VERSAO}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
            return
        for nome, pasta in (("v1", TELA_V1), ("v4", TELA_V4)):
            if rota in (f"/{nome}", f"/{nome}/"):
                return self._arquivo(pasta / "index.html")
            if rota.startswith(f"/{nome}/"):
                alvo = (pasta / rota[len(nome) + 2:]).resolve()
                return self._arquivo(alvo) if pasta.resolve() in alvo.parents else self.send_error(404)
        if rota.startswith("/static/"):
            alvo = (JOGO / rota[len("/static/"):]).resolve()
            return self._arquivo(alvo) if JOGO.resolve() in alvo.parents else self.send_error(404)
        alvo = (TELA / rota.lstrip("/")).resolve()
        if TELA.resolve() in alvo.parents:
            return self._arquivo(alvo)
        self.send_error(404)


def _quem_esta(porta):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{porta}/api/versao", timeout=1) as r:
            d = json.loads(r.read())
            return f"{d.get('prototipo')} · {d.get('versao')}"
    except Exception:
        return "outro programa (sem /api/versao)"


def _livre(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", porta)) != 0


def servir(porta=PORTA, tentativas=11):
    for p in range(porta, porta + tentativas):
        if not _livre(p):
            print(f"porta {p} ocupada por: {_quem_esta(p)}", flush=True)
            continue
        srv = ThreadingHTTPServer(("127.0.0.1", p), Demo)
        srv.daemon_threads = True
        return srv
    raise SystemExit(f"nenhuma porta livre entre {porta} e {porta + tentativas - 1}")


def main():
    srv = servir()
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    print(f"Protótipo de campo livre · {VERSAO}", flush=True)
    print(url, flush=True)
    print(f"a primeira versão (Campo Livre 1), para comparar: {url}v1/", flush=True)
    print(f"o Campo Livre 4 (o básico antigo), para comparar: {url}v4/", flush=True)
    if not os.environ.get("DEMO_SEM_NAVEGADOR"):
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
