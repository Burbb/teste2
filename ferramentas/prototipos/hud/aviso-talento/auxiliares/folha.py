"""Monta a folha do aviso de ponto de talento a partir de ../capturas/ (fotografar.mjs): hoje e a candidata R, parados e
com o foco do Tab, a 1920×945 (em cima) e a 1280×720 (embaixo), em tamanho real. Grava ../folha-aviso.png.

    python ferramentas/prototipos/hud/aviso-talento/auxiliares/folha.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"


def fonte(t):
    try:
        return ImageFont.truetype("georgia.ttf", t)
    except OSError:
        return ImageFont.load_default()


def main():
    linhas = [[Image.open(CAP / f"{j}-{v}-{e}.png").convert("RGB") for v in ("atual", "r") for e in ("parado", "foco")]
              for j in ("1920", "1280")]
    M, ROT = 12, 22
    largura = max(sum(i.width for i in l) for l in linhas) + M * 5
    altura = 40 + sum(max(i.height for i in l) + ROT + M for l in linhas)
    folha = Image.new("RGB", (largura, altura), (22, 18, 14))
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "O aviso de ponto de talento na ficha: hoje × R (parado e com o foco do Tab), no jogo, tamanho real",
           fill=(220, 200, 150), font=fonte(16))
    y = 40
    for jan, l in zip(("1920×945", "1280×720"), linhas):
        x = M
        for im, rot in zip(l, ("hoje", "hoje · foco", "R", "R · foco")):
            d.text((x, y), f"{rot} · {jan}", fill=(150, 140, 120), font=fonte(13))
            folha.paste(im, (x, y + ROT))
            x += im.width + M
        y += max(i.height for i in l) + ROT + M
    folha.save(AQUI.parent / "folha-aviso.png")
    print(folha.size)


if __name__ == "__main__":
    main()
