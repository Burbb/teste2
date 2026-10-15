"""Uma prancha para conferir desenhos de item em tamanho real: cada arquivo em 1× num nicho de item da HUD sobre o
carvão da interface (a textura do painel com o véu escuro, como no jogo), e ao lado a ampliação sem suavizar, para
achar o pixel. Julgue pelo 1×; a ampliação é só para localizar.

    python ferramentas/arte/prancha.py rpg/web/static/hud/icones/escudo-32.png <outra.png> ... -o prancha.png
    python ferramentas/arte/prancha.py ... -o prancha.png --zoom 6

Os arquivos ficam numa linha cada, na ordem dada (o atual e a proposta lado a lado: passe os dois)."""

import argparse
import pathlib

from PIL import Image, ImageDraw

RAIZ = pathlib.Path(__file__).resolve().parents[2]
TEXTURA = RAIZ / "rpg" / "web" / "static" / "hud" / "textura-painel.png"
NICHO, ARESTA = (10, 11, 13), (58, 61, 67)  # o fundo e a aresta do espaço de item da HUD


def carvao(w, h):
    t = Image.open(TEXTURA).convert("RGB")
    s = Image.new("RGB", (w, h))
    for y in range(0, h, t.height):
        for x in range(0, w, t.width):
            s.paste(t, (x, y))
    return Image.blend(s, Image.new("RGB", (w, h), (15, 16, 19)), 0.55).convert("RGBA")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pngs", nargs="+")
    ap.add_argument("-o", "--saida", required=True)
    ap.add_argument("--zoom", type=int, default=8)
    a = ap.parse_args()
    imgs = [(pathlib.Path(p).name, Image.open(p).convert("RGBA")) for p in a.pngs]
    nicho = max(max(i.size) for _, i in imgs) + 24  # um espaço com folga, como o de 56 a 60 px do Inventário
    lado_z = max(max(i.size) for _, i in imgs) * a.zoom
    alt_linha = max(nicho, lado_z) + 26
    img = carvao(nicho + lado_z + 60, 10 + alt_linha * len(imgs))
    d = ImageDraw.Draw(img)
    for k, (nome, i) in enumerate(imgs):
        y = 10 + k * alt_linha
        d.rectangle((10, y, 10 + nicho - 1, y + nicho - 1), fill=NICHO, outline=ARESTA)
        img.alpha_composite(i, (10 + (nicho - i.width) // 2, y + (nicho - i.height) // 2))
        img.alpha_composite(i.resize((i.width * a.zoom, i.height * a.zoom), Image.NEAREST), (nicho + 40, y))
        d.text((10, y + max(nicho, lado_z) + 6), f"{nome}  {i.width}×{i.height}", fill=(200, 192, 176))
    img.convert("RGB").save(a.saida)
    print(a.saida)


if __name__ == "__main__":
    main()
