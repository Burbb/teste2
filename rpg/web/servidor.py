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

# As preferências da tela guardadas em disco (a porta muda a cada vez que o jogo abre, e o armazenamento do navegador
# vai junto): só as chaves e os valores daqui, cada uma gravada sem mexer nas outras. 1.202.0: o dado dos testes
# (d20/dado.js); 1.202.2: a velocidade do texto, o som e o "Destacar interações". Até o menu de configurações.
PREFERENCIAS = {"d20": ("classico", "marfim", "vidro"), "velocidade": ("lento", "normal", "rapido", "instantaneo"),
                "som": ("1", "0"), "destacar": ("1", "0")}


def ler_preferencias(caminho):
    """As preferências válidas do arquivo (as outras, e um arquivo ausente ou estragado, ficam de fora)."""
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError, TypeError):
        return {}
    if not isinstance(dados, dict):
        return {}
    return {k: v for k, v in dados.items() if v in PREFERENCIAS.get(k, ())}


class Servidor:
    def __init__(self, ui, porta=0, config=None, preferencias=None):
        self.ui = ui
        self.token = secrets.token_urlsafe(16)
        self.config = config or {}
        # `preferencias`: o arquivo delas (sem ele, nada vai para o disco: os testes e os cenários)
        self.arquivo_preferencias = preferencias
        self.config["preferencias"] = ler_preferencias(preferencias) if preferencias else {}
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
                if url.path not in ("/responder", "/orientacao", "/preferencia") or not self._token_ok({}):
                    return self._responder(403)
                if url.path == "/preferencia":  # {"chave": "d20", "valor": "marfim"}: vale a partir da próxima abertura
                    try:
                        tamanho = min(int(self.headers.get("Content-Length", 0)), 1_000)
                        dados = json.loads(self.rfile.read(tamanho) or b"{}")
                        servidor.guardar_preferencia(dados["chave"], dados["valor"])
                    except (ValueError, KeyError, TypeError):
                        return self._responder(400)
                    return self._responder(204)
                if url.path == "/orientacao":  # dispensar ou religar as orientações (abertura.py)
                    try:
                        tamanho = min(int(self.headers.get("Content-Length", 0)), 1_000)
                        servidor.ui.orientacao(json.loads(self.rfile.read(tamanho) or b"{}").get("acao"))
                    except (ValueError, TypeError, AttributeError):
                        return self._responder(400)
                    return self._responder(204)
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

    def guardar_preferencia(self, chave, valor):
        """Guarda uma preferência da tela; uma chave ou um valor desconhecido é ValueError."""
        if valor not in PREFERENCIAS.get(chave, ()):
            raise ValueError(chave)
        self.config["preferencias"][chave] = valor
        if self.arquivo_preferencias:
            os.makedirs(os.path.dirname(self.arquivo_preferencias), exist_ok=True)
            with open(self.arquivo_preferencias, "w", encoding="utf-8") as f:
                json.dump(self.config["preferencias"], f, ensure_ascii=False, indent=1)

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
