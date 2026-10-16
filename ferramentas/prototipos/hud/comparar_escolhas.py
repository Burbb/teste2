"""Monta as comparações dos ícones das escolhas a partir de fotografar_escolhas.mjs (capturas-escolhas/):
  - comparacao-<janela>-<caso>.png: atual, 16 e 24, um embaixo do outro, em tamanho real (a lista de opções inteira);
  - prancha-zoom.png: só a opção de cada caso, nas três versões, ampliada 3× sem suavizar, para achar o pixel (julgue
    pelo tamanho real).

    python ferramentas/prototipos/hud/comparar_escolhas.py [pasta]   (padrão: capturas-escolhas/; só as versões que
                                                                      estiverem na pasta, como em capturas-escolhas-24/)
"""

import pathlib
import sys

from PIL import Image, ImageDraw

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "capturas-escolhas"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
VERSOES = (("atual", "atual (sprite 16)"), ("p16", "proposta 16"), ("p24", "proposta 24"))
CASOS = ("bandagem", "pocao", "pocao-sem", "bomba-simulada")


def coluna(imgs, rotulos, z=1):
    imgs = [i.resize((i.width * z, i.height * z), Image.NEAREST) for i in imgs]
    out = Image.new("RGB", (max(i.width for i in imgs) + 24, sum(i.height + 22 for i in imgs) + 6), FUNDO)
    d, y = ImageDraw.Draw(out), 4
    for i, r in zip(imgs, rotulos):
        d.text((12, y), r, fill=TEXTO)
        out.paste(i, (12, y + 16))
        y += i.height + 22
    return out


def main():
    global VERSOES
    VERSOES = tuple((v, r) for v, r in VERSOES if any(FOTOS.glob(f"*-{v}-*.png")))
    for jan in ("normal", "baixa"):
        for caso in CASOS:
            ps = [FOTOS / f"{jan}-{v}-{caso}-opcoes.png" for v, _ in VERSOES]
            if all(p.exists() for p in ps):
                coluna([Image.open(p).convert("RGB") for p in ps], [f"{jan} · {caso} · {r}" for _, r in VERSOES]).save(
                    FOTOS / f"comparacao-{jan}-{caso}.png")
    cols = []
    for caso in CASOS:
        ps = [FOTOS / f"zoom-normal-{v}-{caso}.png" for v, _ in VERSOES]
        cols.append(coluna([Image.open(p).convert("RGB") for p in ps], [f"{caso} · {r}" for _, r in VERSOES], 3))
    w, h = sum(c.width for c in cols), max(c.height for c in cols)
    prancha = Image.new("RGB", (w, h), FUNDO)
    x = 0
    for c in cols:
        prancha.paste(c, (x, 0))
        x += c.width
    prancha.save(FOTOS / "prancha-zoom.png")
    print(f"comparações e prancha em {FOTOS}")


if __name__ == "__main__":
    main()
