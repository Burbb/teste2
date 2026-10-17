"""Servidor local da bancada do teste do pen.dev (experimento): esta pasta na raiz e o static do jogo em /static/
(as folhas de estilo, as fontes e as texturas do jogo, sem cópia). Só biblioteca padrão.

    python ferramentas/prototipos/hud/pen-composicao/servir.py        # http://localhost:8771/bancada.html
"""
import functools
import http.server
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "..", "rpg", "web", "static"))
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 8771


class Bancada(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        caminho = path.split("?", 1)[0].split("#", 1)[0]
        if caminho.startswith("/static/"):
            base, resto = STATIC, caminho[len("/static/"):]
        else:
            base, resto = AQUI, caminho.lstrip("/")
        alvo = os.path.normpath(os.path.join(base, *resto.split("/")))
        return alvo if alvo.startswith(base) else base

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # cada ajuste aparece no recarregar
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), functools.partial(Bancada, directory=AQUI))
    print(f"http://localhost:{PORTA}/bancada.html", flush=True)
    servidor.serve_forever()
