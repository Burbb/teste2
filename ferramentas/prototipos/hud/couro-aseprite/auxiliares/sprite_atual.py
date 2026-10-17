"""Desenha um sprite 16×16 do jogo (rpg/web/static/sprites-dados.js, com a PALETA de sprites.js) em 16, 32 e 64 px,
vizinho mais próximo, para comparar com a proposta. Só leitura dos dados do jogo.

    python ferramentas/prototipos/hud/couro-aseprite/auxiliares/sprite_atual.py <nome> <pasta>
"""
import pathlib
import re
import sys

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[5]
STATIC = RAIZ / "rpg" / "web" / "static"


def paleta():
    t = (STATIC / "sprites.js").read_text(encoding="utf-8")
    bloco = t[t.index("const PALETA = {"):t.index("};", t.index("const PALETA = {"))]
    return {k: v for k, v in re.findall(r'(\w): "(#[0-9a-fA-F]{6})"', bloco)}


def grade(nome):
    t = (STATIC / "sprites-dados.js").read_text(encoding="utf-8")
    m = re.search(rf"\n    {nome}: \[\n((?:\s+\"[^\"]*\",\n)+)\s+\]", t)
    return re.findall(r'"([^"]*)"', m.group(1))


if __name__ == "__main__":
    nome, pasta = sys.argv[1], pathlib.Path(sys.argv[2])
    pal, g = paleta(), grade(nome)
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, linha in enumerate(g):
        for x, c in enumerate(linha):
            if c in pal:
                im.putpixel((x, y), tuple(int(pal[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    pasta.mkdir(parents=True, exist_ok=True)
    for n in (16, 32, 64):
        im.resize((n, n), Image.NEAREST).save(pasta / f"{nome}-sprite-{n}.png")
    print(nome, "ok")
