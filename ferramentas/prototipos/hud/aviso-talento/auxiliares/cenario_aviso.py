"""CENÁRIO DO AVISO DE PONTO DE TALENTO (protótipo, 24/10/2026; nada no jogo). A campanha de teste do cenário
`tutorial` (tests/navegador/cenarios.py) com PONTOS de talento para gastar, os saves numa pasta temporária: os seus
saves não são tocados.

    python cenario_aviso.py        # sobe o servidor e imprime o endereço na primeira linha

PROPOSTA=r põe aviso.css do protótipo depois das folhas do jogo e troca o HTML do aviso em app/paineis.js (um <button>
com o ícone dos Talentos da doca e a seta dentro; o número e o texto, os mesmos); vazia: o aviso de hoje. O arquivo do
jogo não muda.
"""
import os
import pathlib
import sys
import threading
import time

RAIZ = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(RAIZ))
PROTO = pathlib.Path(__file__).resolve().parents[1]
AVISO_HOJE = ('<div class="talento-aviso" role="button" tabindex="0" data-atalho="Talentos"><span class="estrela">${spr("estrela", 2)}'
              '</span><span>${Texto.plural(h.pontos_talento, "ponto de talento", "pontos de talento")}</span></div>'
              '<span class="seta-pendencia" aria-hidden="true">${spr("seta_esq", 2)}</span>')
AVISO_R = ('<button type="button" class="talento-aviso" data-atalho="Talentos"><span class="estrela">'
           '${Icones.atalho("Talentos", 32) || spr("estrela", 2)}</span><span class="talento-texto">'
           r'${Texto.plural(h.pontos_talento, "ponto de talento", "pontos de talento").replace(/^\d+/, (n) => `<b>${n}</b>`)}'
           '</span><span class="talento-abrir" aria-hidden="true">▸</span></button>')


def demonstracao(srv):
    """Só neste servidor: o CSS do protótipo em /static/prototipo-aviso/ e, com PROPOSTA, a página com ele."""
    from rpg.web.servidor import Servidor
    proposta = os.environ.get("PROPOSTA", "")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo == "app/paineis.js" and proposta == "r":
            js = (pasta / "app" / "paineis.js").read_text(encoding="utf-8")
            # desde a 1.207.0 o jogo já tem o aviso da R (a troca não acha nada e o arquivo vai como está)
            assert AVISO_HOJE in js or AVISO_R in js, "paineis.js mudou: não achei o aviso de talento"
            return self._responder(200, js.replace(AVISO_HOJE, AVISO_R).encode("utf-8"), "text/javascript; charset=utf-8")
        if relativo == "prototipo-aviso/aviso.css":
            return self._responder(200, (PROTO / "aviso.css").read_bytes(), "text/css; charset=utf-8")
        if relativo == "index.html" and proposta:
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            marca = '<link rel="stylesheet" href="/static/css/23-faixas.css">'
            assert marca in pagina, "index.html mudou: não achei 23-faixas.css"
            pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-aviso/aviso.css">')
            pagina = pagina.replace("<html", f'<html data-aviso="{proposta}"', 1)
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    from tests.navegador.cenarios import tutorial
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=tutorial, args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
