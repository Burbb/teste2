"""Sobe o protótipo da comitiva: a página daqui e o CSS, os ícones e os scripts de tela do jogo (rpg/web/static), sem
copiar nada. Gera os dados (gerar_dados.py) e imprime o endereço.

    python ferramentas/prototipos/comitiva-gerenciamento/servidor.py   (na raiz do repositório; PORTA=8765 opcional)
"""

import http.server
import os
import socketserver
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTATICO = os.path.abspath(os.path.join(AQUI, "..", "..", "..", "rpg", "web", "static"))
sys.path.insert(0, AQUI)


class Pagina(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        caminho = path.split("?", 1)[0]
        if caminho.startswith("/static/"):
            return os.path.join(ESTATICO, *caminho[len("/static/"):].split("/"))
        if caminho in ("", "/"):
            caminho = "/index.html"
        return os.path.join(AQUI, *caminho.lstrip("/").split("/"))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    import gerar_dados
    import json
    with open(os.path.join(AQUI, "dados.json"), "w", encoding="utf-8") as f:
        json.dump(gerar_dados.montar(), f, ensure_ascii=False, indent=1)
    porta = int(os.environ.get("PORTA", "0"))
    with socketserver.TCPServer(("127.0.0.1", porta), Pagina) as srv:
        print(f"http://127.0.0.1:{srv.server_address[1]}/", flush=True)
        srv.serve_forever()
