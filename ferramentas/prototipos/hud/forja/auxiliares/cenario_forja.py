"""CENÁRIO DA FORJA (protótipo, 25/10/2026; nada no jogo). Uma campanha de teste no Vau do Turvo (o cenário `tutorial`
dos testes, com o tutorial desligado, o Guerreiro com arma, peito e escudo vestidos), os saves numa pasta temporária:
os seus saves não são tocados. Clique no prédio do ferreiro (ou escolha "Ferreiro" no menu) para entrar na forja.

    python cenario_forja.py        # sobe o servidor e imprime o endereço na primeira linha

PROPOSTA=a ou b: a forja com o ambiente (forja-arte.js, forja.js, forja.css); r: a B refinada (forja-r.js); f: a transposição
fiel da referência (forja-f.js, as camadas de f/camadas; o quadro de 96 de altura); g: a F corrigida, na arte do jogo, a
candidata anterior (forja-g.js, g/camadas); h: a G com o ferreiro no estilo
do jogo e o corpo animado, a candidata (forja-h.js, h/camadas). Só neste processo, o motor manda o
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
TIPOS = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".png": "image/png"}
ROTULOS = {"": "a forja de hoje (sem arte)", "a": "A · a bancada de trabalho", "b": "B · o interior da oficina",
           "r": "R · a B refinada, o ferreiro forjando", "f": "F · a transposição fiel da referência",
           "g": "G · a F corrigida, na arte do jogo",
           "h": "H · o ferreiro no estilo do jogo, o corpo animado (a candidata)"}
CENAS_JS = "  const CENAS = {"
# A F e a G têm o quadro mais alto (320×96) que as paisagens (320×72): só neste processo, a vista (vista.js) passa a usar a
# altura do ambiente à vista (a da base dele) para a arte, a câmera e a caixa; sem ambiente, os 72 de sempre. Cada
# troca é conferida (o vista.js mudou: o cenário para, em vez de servir uma vista meio trocada).
VISTA_ALTA = [
    ("const W = 320, H = 72;", "const W = 320, H = 72;\n  let HA = H;  // (protótipo da forja F) a altura da arte: a do ambiente à vista"),
    ("c.drawImage(quadroBuf, cam.x, cam.y, W / cam.s, H / cam.s, 0, 0, W, H);", "c.drawImage(quadroBuf, cam.x, cam.y, W / cam.s, HA / cam.s, 0, 0, W, HA);"),
    ("quadroBuf.width = W; quadroBuf.height = H; }", "quadroBuf.width = W; quadroBuf.height = HA; }"),
    ("ctx.clearRect(0, 0, W, H);", "ctx.clearRect(0, 0, W, HA);"),
    ("mascara.width = W; mascara.height = H; }", "mascara.width = W; mascara.height = HA; }"),
    ("m.clearRect(0, 0, W, H)", "m.clearRect(0, 0, W, HA)"),
    ("m.fillRect(0, 0, W, H);", "m.fillRect(0, 0, W, HA);"),
    ("const esc = Math.max(cw / W, ch / H), dw = Math.round(W * esc), dh = Math.round(H * esc);",
     "const esc = Math.max(cw / W, ch / HA), dw = Math.round(W * esc), dh = Math.round(HA * esc);"),
    ("ey: (dh / H) * ky", "ey: (dh / HA) * ky"),
    ("arte.width = W; arte.height = H;", "arte.width = W; arte.height = HA;"),
    ("return { s: 2, x: Math.max(0, Math.min(W / 2, Math.round(fx - W / 4))), y: Math.max(0, Math.min(H / 2, Math.round(fy - H / 4))) };",
     "return { s: 2, x: Math.max(0, Math.min(W / 2, Math.round(fx - W / 4))), y: Math.max(0, Math.min(HA / 2, Math.round(fy - HA / 4))) };"),
    ("getImageData(W >> 1, H - 1, 1, 1)", "getImageData(W >> 1, (ambiente ? ambiente.base.height : H) - 1, 1, 1)"),
    ("    ambiente = a;", "    ambiente = a;\n    HA = a && a.base ? a.base.height : H;\n"
     "    if (arte && arte.height !== HA) arte.height = HA;\n    if (quadroBuf && quadroBuf.height !== HA) quadroBuf.height = HA;\n"
     "    if (mascara && mascara.height !== HA) mascara.height = HA;"),
]


def vista_alta(js):
    for velho, novo in VISTA_ALTA:
        assert js.count(velho) == 1, f"vista.js mudou: não achei (uma vez) {velho!r}"
        js = js.replace(velho, novo)
    return js


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
        if relativo == "vista.js" and proposta in ("f", "g", "h"):
            js = vista_alta((pasta / "vista.js").read_text(encoding="utf-8"))
            return self._responder(200, js.encode("utf-8"), TIPOS[".js"])
        if relativo.startswith("prototipo-forja/"):
            alvo = (PROTO / relativo.split("/", 1)[1]).resolve()
            if PROTO in alvo.parents and alvo.suffix in TIPOS and alvo.is_file():  # (f/camadas/*.png inclusive)
                return self._responder(200, alvo.read_bytes(), TIPOS[alvo.suffix])
            return self._responder(404, b"")
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                marca = '<link rel="stylesheet" href="/static/css/25-carregar.css">'
                assert marca in pagina, "index.html mudou: não achei 25-carregar.css"
                pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-forja/forja.css">')
                pagina = pagina.replace("</body>", '<script src="/static/prototipo-forja/forja-arte.js"></script>'
                                        '<script src="/static/prototipo-forja/forja-r.js"></script>'
                                        '<script src="/static/prototipo-forja/forja-f.js"></script>'
                                        '<script src="/static/prototipo-forja/forja-g.js"></script>'
                                        '<script src="/static/prototipo-forja/forja-h.js"></script>'
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
