"""Monta capela.html (a página única, com as fontes embutidas) a partir de pagina.html e cena.js.
    python ferramentas/prototipos/capela-afogada-ensaio/fonte/montar.py"""
import base64, pathlib
aqui = pathlib.Path(__file__).parent
fontes = aqui.parents[3] / "rpg" / "web" / "static" / "fontes"  # as fontes do jogo (as mesmas da época)
t = (aqui / "pagina.html").read_text()
t = t.replace(".ponto:focus-visible { outline", "#pontos.focado .ponto { display: none; }\n.ponto:focus-visible { outline")
t += "\n<script>\n" + (aqui / "cena.js").read_text() + "</script>\n"
for k, n in [("ALAGARD", "alagard-pt.ttf"), ("ALEGREYA400I", "alegreya-latin-400-italic.woff2"), ("ALEGREYA400", "alegreya-latin-400-normal.woff2"), ("ALEGREYA600", "alegreya-latin-600-normal.woff2")]:
    t = t.replace("{{" + k + "}}", base64.b64encode((fontes / n).read_bytes()).decode())
(aqui.parent / "capela.html").write_text(t)
print(len(t))
