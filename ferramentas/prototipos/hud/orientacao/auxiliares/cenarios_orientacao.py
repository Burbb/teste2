"""CENÁRIOS DOS QUADROS DE ORIENTAÇÃO (protótipo, 24/10/2026; nada no jogo). Cada caso é a abertura guiada de
verdade, pelo cenário `tutorial` dos testes (tests/navegador/cenarios.py), numa campanha de teste com os saves numa
pasta temporária: os seus saves e o tutorial deles não são tocados. O motor decide qual quadro vale (abertura.py); o
caso só monta o estado em que ele aparece (as orientações já vistas, o lugar, a hora, a bolsa...).

    python cenarios_orientacao.py <caso>        # sobe o servidor e imprime o endereço na primeira linha

PROPOSTA=a ou b põe orientacao.css do protótipo e marca a página (html[data-orientacao]); vazia: os quadros de hoje.
PAINEL=<endereço> põe a faixa da demonstração no canto. Nada é gravado no jogo.
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

# id: (rótulo, onde o quadro mora, o ambiente do cenário `tutorial`). O V1 (o mural) e a luta guiada (C1–C4) não
# entram: o cenário `tutorial` já parte com eles vistos.
CASOS = {
    "a1": ("A1 · a velocidade do texto (no alto, o botão Texto)", "alto", {}),
    "v2": ("V2 · o Templo (um prédio da vila, na faixa abaixo do cenário)", "página", {"VISTAS": "A1", "VIDA": "0.5"}),
    "b1": ("B1 · o baú na bolsa (a coluna da esquerda; texto curto)", "lateral esquerda", {"VISTAS": "A1,V1", "BAUS": "1"}),
    "k2": ("K2 · o contrato aceito (a coluna da direita; texto longo)", "lateral direita", {"VISTAS": "A1", "CONTRATO": "aceito"}),
    "v4": ("V4 · a Comitiva (a doca, embaixo; texto longo)", "embaixo", {"VISTAS": "A1,V1", "COMITIVA": "morel"}),
    "t1": ("T1 · os Talentos (a doca, embaixo)", "embaixo", {"VISTAS": "A1,V1", "PONTOS": "1"}),
    "n1": ("N1 · a noite (os riscos do lugar, na coluna da direita)", "lateral direita", {"VISTAS": "A1,V1", "LUGAR": "charco", "PERIODO": "3"}),
    "al": ("AL · na luta, acelerar a animação (a faixa abaixo da arena, sem seta)", "luta",
           {"VISTAS": "A1", "LUTA": "lobo", "QUANTOS": "3", "NIVEL_LUTA": "2", "LUTA_APOS_ESCOLHA": "1"}),
    "e1": ("E1 · o item achado (abaixo da janela do achado)", "janela", {"VISTAS": "A1,V1", "ITEM": "1"}),
}
ROTULOS = {"": "os quadros de hoje", "a": "A · quadro da HUD", "b": "B · chamada contextual"}
TIPOS = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".png": "image/png"}


def demonstracao(srv, caso):
    """Só neste servidor: o CSS do protótipo em /static/prototipo-orientacao/ e, com PROPOSTA, a página com ele."""
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo.startswith("prototipo-orientacao/"):
            alvo = (PROTO / relativo.split("/", 1)[1]).resolve()
            if PROTO in alvo.parents and alvo.suffix in TIPOS and alvo.is_file():
                return self._responder(200, alvo.read_bytes(), TIPOS[alvo.suffix])
            return self._responder(404, b"")
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                marca = '<link rel="stylesheet" href="/static/css/23-faixas.css">'
                assert marca in pagina, "index.html mudou: não achei 23-faixas.css"
                pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-orientacao/orientacao.css">')
                pagina = pagina.replace("<html", f'<html data-orientacao="{proposta}"', 1)
            if painel:
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Orientação: {html.escape(CASOS[caso][0])} · {html.escape(ROTULOS[proposta])} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    caso = sys.argv[1] if len(sys.argv) > 1 else "a1"
    os.environ.update(CASOS[caso][2])
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    from tests.navegador.cenarios import tutorial
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv, caso)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=tutorial, args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
