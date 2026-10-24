"""CENÁRIOS DO LIVRO DA CAPELA (protótipo, 24/10/2026; nada no jogo). Sobe o jogo de verdade na sacristia da Capela
Afogada, pelo cenário `capela` dos testes (tests/navegador/cenarios.py), com o save numa pasta temporária, e põe na
página o livro de uma das propostas.

    python cenarios_livro.py <caso>        # sobe o servidor e imprime o endereço na primeira linha

Casos: "primeira" (a sacristia vencida, o livro ainda por ler: a primeira leitura grava Ilse e o Sigilo) e
"releitura" (o livro já lido: reler não muda nada). PROPOSTA=a, b ou c põe livro.css e livro.js do protótipo depois de
telas/cenas.js (vazia: o livro de hoje); PAINEL=<endereço> põe a faixa da demonstração no canto. Nada é gravado no jogo.
"""
import html
import os
import pathlib
import sys
import threading
import time

RAIZ = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(RAIZ))
PROTO = pathlib.Path(__file__).resolve().parents[1]

CASOS = {
    "primeira": ("Primeira leitura: a sacristia vencida, o livro ainda embrulhado",
                 {"ETAPA": "ossuario", "LIVRO": "0", "SALA": "sacristia"}),
    "releitura": ("Releitura: o livro já lido (nada muda ao reler)",
                  {"ETAPA": "ossuario", "SALA": "sacristia"}),
}
ROTULOS = {"": "o livro de hoje", "a": "A · registro", "a2": "A refinada", "b": "B · registro que vira confissão", "c": "C · leitura próxima"}
TIPOS = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".png": "image/png",
         ".json": "application/json", ".woff2": "font/woff2"}


def demonstracao(srv, caso):
    """Só neste servidor: os arquivos do protótipo em /static/prototipo-livro/ e, com PROPOSTA, a página com eles."""
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo.startswith("prototipo-livro/"):
            alvo = (PROTO / relativo.split("/", 1)[1]).resolve()
            if PROTO in alvo.parents and alvo.suffix in TIPOS and alvo.is_file():
                return self._responder(200, alvo.read_bytes(), TIPOS[alvo.suffix])
            return self._responder(404, b"")
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                marca = '<script src="/static/telas/cenas.js"></script>'
                assert marca in pagina, "index.html mudou: não achei telas/cenas.js"
                pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-livro/livro.css">\n'
                                        '<script src="/static/prototipo-livro/livro.js"></script>\n'
                                        f'<script>LivroProto.usar({proposta!r});</script>')
            if painel:
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Livro da capela: {html.escape(CASOS[caso][0])} · {html.escape(ROTULOS[proposta])} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    caso = sys.argv[1] if len(sys.argv) > 1 else "primeira"
    os.environ.update(CASOS[caso][1])
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    from tests.navegador.cenarios import capela
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv, caso)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=capela, args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
