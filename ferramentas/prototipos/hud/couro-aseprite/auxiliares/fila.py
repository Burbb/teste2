"""Uma fila de ícones em 1× sobre o carvão da HUD, cada um num nicho de item, e a mesma fila ampliada embaixo (vizinho
mais próximo, só para achar o pixel). Julgue pelo 1×.

    python ferramentas/prototipos/hud/couro-aseprite/auxiliares/fila.py <saida.png> <rótulo>=<png> ...
"""
import pathlib
import sys

from PIL import Image, ImageDraw

RAIZ = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))
from prancha import carvao, NICHO, ARESTA  # noqa: E402

TEXTO = (214, 205, 186)


def fila(saida, pares, z=3):
    ims = [(r, Image.open(p).convert("RGBA")) for r, p in pares]
    lado = max(i.width for _, i in ims)
    col = max(lado + 40, 96, lado * z + 12)
    img = carvao(col * len(ims) + 20, lado + 24 + 30 + lado * z + 30)
    d = ImageDraw.Draw(img)
    for k, (r, i) in enumerate(ims):
        x, n = 10 + k * col, i.width + 24
        d.rectangle((x + (col - n) // 2, 10, x + (col - n) // 2 + n - 1, 10 + n - 1), fill=NICHO, outline=ARESTA)
        img.alpha_composite(i, (x + (col - i.width) // 2, 22))
        d.text((x + 4, 10 + n + 4), r, fill=TEXTO)
        g = i.resize((i.width * z, i.height * z), Image.NEAREST)
        img.alpha_composite(g, (x + (col - g.width) // 2, lado + 24 + 30 + 10))
    img.convert("RGB").save(saida)


if __name__ == "__main__":
    fila(sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]])
