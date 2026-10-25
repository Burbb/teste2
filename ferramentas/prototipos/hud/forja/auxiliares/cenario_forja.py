"""CENÁRIO DA FORJA (protótipo, 25/10/2026; nada no jogo). Uma campanha de teste no Vau do Turvo (o cenário `tutorial`
dos testes, com o tutorial desligado, o Guerreiro com arma, peito e escudo vestidos), os saves numa pasta temporária:
os seus saves não são tocados. Clique no prédio do ferreiro (ou escolha "Ferreiro" no menu) para entrar na forja.

    python cenario_forja.py        # sobe o servidor e imprime o endereço na primeira linha

PROPOSTA=a ou b: a forja com o ambiente (forja-arte.js, forja.js, forja.css). Só neste processo, o motor manda o
painel "cena" da forja logo antes do balcão (`forja_<proposta>`, com os pontos Ferreiro e Saída); o balcão, os
cartões, os preços e o reforço são os do jogo. Vazia: a forja de hoje (sem arte). OURO (padrão 300; 30 para ver os
cartões sem ouro), CLASSE (padrão guerreiro). PAINEL=<endereço> põe a faixa da demonstração no canto.
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
TIPOS = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}
ROTULOS = {"": "a forja de hoje (sem arte)", "a": "A · a bancada de trabalho", "b": "B · o interior da oficina"}
CENAS_JS = "  const CENAS = {"


def cena_da_forja(proposta):
    """O painel "cena" da forja (o que o motor mandaria na integração): o ambiente e os dois pontos."""
    return {"cena": f"forja_{proposta}", "titulo": "A forja", "pagina": True, "momento": "visita", "pontos": [
        # o ferreiro: o reforço mora nos cartões embaixo (forja.js leva o foco até eles); `olhar` só o deixa ativo
        {"id": "ferreiro", "nome": "Ferreiro", "estado": "O ferreiro, na bigorna.", "acao": None, "olhar": True},
        {"id": "saida", "nome": "Saída", "faz": "voltar à vila", "estado": "A porta para a rua do Vau.",
         "acao": {"voltar": True}},
    ]}


def demonstracao(srv):
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    if proposta:
        original_painel = WebUI.painel

        def painel_com_cena(self, tipo, dados):
            if tipo == "ferreiro":  # só aqui: o ambiente da forja antes do balcão
                original_painel(self, "cena", cena_da_forja(proposta))
            return original_painel(self, tipo, dados)

        WebUI.painel = painel_com_cena
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo == "telas/cenas.js" and proposta:
            js = (pasta / "telas" / "cenas.js").read_text(encoding="utf-8")
            assert CENAS_JS in js, "cenas.js mudou: não achei o registro das cenas"
            return self._responder(200, js.replace(CENAS_JS, "  const CENAS = window.__CENAS = {").encode("utf-8"), TIPOS[".js"])
        if relativo.startswith("prototipo-forja/"):
            alvo = (PROTO / relativo.split("/", 1)[1]).resolve()
            if PROTO in alvo.parents and alvo.suffix in TIPOS and alvo.is_file():
                return self._responder(200, alvo.read_bytes(), TIPOS[alvo.suffix])
            return self._responder(404, b"")
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                marca = '<link rel="stylesheet" href="/static/css/25-carregar.css">'
                assert marca in pagina, "index.html mudou: não achei 25-carregar.css"
                pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-forja/forja.css">')
                pagina = pagina.replace("</body>", '<script src="/static/prototipo-forja/forja-arte.js"></script>'
                                        '<script src="/static/prototipo-forja/forja.js"></script></body>')
                pagina = pagina.replace("<html", f'<html data-forja="{proposta}"', 1)
            if painel:
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Forja: {html.escape(ROTULOS[proposta])} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    os.environ.setdefault("TUTORIAL", "0")
    os.environ.setdefault("LUGAR", "vau")
    os.environ.setdefault("OURO", "300")
    os.environ.setdefault("VITRINE", "2")  # a arma, o peito e o escudo vestidos: três cartões na forja
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
