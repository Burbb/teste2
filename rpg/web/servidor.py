"""Servidor HTTP local (só biblioteca padrão): entrega a página, transmite mensagens por SSE e recebe respostas.

Escuta apenas em 127.0.0.1. Cada sessão tem um token: sem ele, nenhuma página
de fora consegue ler o jogo ou responder por você.
"""

import json
import mimetypes
import os
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/ttf", ".ttf")
mimetypes.add_type("text/javascript", ".js")


class Servidor:
    def __init__(self, ui, porta=0, config=None):
        self.ui = ui
        self.token = secrets.token_urlsafe(16)
        self.config = config or {}
        servidor = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _token_ok(self, qs):
                return self.headers.get("X-Token") == servidor.token or qs.get("token", [""])[0] == servidor.token

            def _responder(self, codigo, corpo=b"", tipo="text/plain; charset=utf-8"):
                self.send_response(codigo)
                self.send_header("Content-Type", tipo)
                self.send_header("Content-Length", str(len(corpo)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(corpo)

            def do_GET(self):
                url = urlparse(self.path)
                qs = parse_qs(url.query)
                if url.path in ("/", "/index.html"):
                    return self._arquivo("index.html")
                if url.path.startswith("/static/"):
                    return self._arquivo(url.path[len("/static/"):])
                if url.path == "/config":
                    if not self._token_ok(qs):
                        return self._responder(403)
                    return self._responder(200, json.dumps(servidor.config).encode(), "application/json")
                if url.path == "/eventos":
                    if not self._token_ok(qs):
                        return self._responder(403)
                    return self._eventos()
                self._responder(404, b"nada aqui")

            def do_POST(self):
                url = urlparse(self.path)
                if url.path != "/responder" or not self._token_ok({}):
                    return self._responder(403)
                try:
                    tamanho = min(int(self.headers.get("Content-Length", 0)), 10_000)
                    dados = json.loads(self.rfile.read(tamanho) or b"{}")
                    servidor.ui.responder(int(dados["id"]), dados.get("valor"))
                except (ValueError, KeyError, TypeError):
                    return self._responder(400)
                self._responder(204)

            def _arquivo(self, relativo):
                caminho = os.path.normpath(os.path.join(PASTA, relativo))
                if not caminho.startswith(PASTA + os.sep) or not os.path.isfile(caminho):
                    return self._responder(404)
                tipo = mimetypes.guess_type(caminho)[0] or "application/octet-stream"
                if tipo.startswith("text/") or tipo.endswith("javascript"):
                    tipo += "; charset=utf-8"
                with open(caminho, "rb") as f:
                    self._responder(200, f.read(), tipo)

            def _eventos(self):
                canal = servidor.ui.canal
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                ultimo = self.headers.get("Last-Event-ID")
                try:
                    if ultimo is not None and ultimo.isdigit():
                        cursor = int(ultimo) + 1  # reconexão automática: continua de onde parou
                    else:
                        # Conexão nova (ou página recarregada): repete a cena atual sem animação.
                        cursor, estado = canal.ponto_de_entrada()
                        if estado:
                            self._mandar({**estado, "replay": True})
                        fim = len(canal.mensagens)
                        for m in canal.mensagens[cursor:fim]:
                            self._mandar({**m, "replay": True})
                        cursor = fim
                        self._mandar({"t": "sincronizado"})
                    while True:
                        novas, encerrado = canal.esperar(cursor)
                        for m in novas:
                            self._mandar(m)
                        cursor += len(novas)
                        if encerrado and not novas:
                            return
                        if not novas:
                            self.wfile.write(b": ping\n\n")
                            self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    return

            def _mandar(self, m):
                linha = json.dumps(m, ensure_ascii=False)
                cab = f"id: {m['seq']}\n" if "seq" in m else ""
                self.wfile.write(f"{cab}data: {linha}\n\n".encode("utf-8"))
                self.wfile.flush()

        self.httpd = ThreadingHTTPServer(("127.0.0.1", porta), Handler)
        self.httpd.daemon_threads = True
        self.thread = None

    @property
    def url(self):
        host, porta = self.httpd.server_address[:2]
        return f"http://{host}:{porta}/?token={self.token}"

    def iniciar(self):
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        return self

    def parar(self):
        self.httpd.shutdown()
        self.httpd.server_close()
