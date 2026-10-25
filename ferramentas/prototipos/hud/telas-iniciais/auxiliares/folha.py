"""Monta a folha das telas iniciais a partir de ../capturas/ (fotografar.mjs): a 1920×945, o título, os saves e a
mensagem do save do mundo gerado (iguais nas duas versões) e a criação (a classe e o modo), hoje × R; a 1280×720, a
criação, hoje × R. Reduzidas à metade (a página inteira); os detalhes, nas capturas em tamanho real. Grava
../folha-telas-iniciais.png.

    python ferramentas/prototipos/hud/telas-iniciais/auxiliares/folha.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
LINHAS = [
    ("1920×945 · o título, os saves e o save do mundo gerado (iguais hoje e na R)",
     [("1920-atual-1-titulo", "título"), ("1920-atual-2-saves", "saves"), ("1920-atual-3-save-incompativel", "save recusado")]),
    ("1920×945 · a classe e o modo: hoje × R",
     [("1920-atual-5-classe", "hoje · classe"), ("1920-r-5-classe", "R · classe"), ("1920-r-6-modo", "R · modo")]),
    ("1280×720 · a classe e o modo: hoje × R",
     [("1280-atual-5-classe", "hoje · classe"), ("1280-r-5-classe", "R · classe"), ("1280-atual-6-modo", "hoje · modo"),
      ("1280-r-6-modo", "R · modo")]),
]


def fonte(t):
    try:
        return ImageFont.truetype("georgia.ttf", t)
    except OSError:
        return ImageFont.load_default()


def main():
    blocos = [(rot, [(Image.open(CAP / f"{n}.png").convert("RGB"), r) for n, r in ims]) for rot, ims in LINHAS]
    blocos = [(rot, [(im.resize((im.width // 2, im.height // 2), Image.LANCZOS), r) for im, r in ims]) for rot, ims in blocos]
    M, ROT = 12, 22
    largura = max(sum(im.width for im, _ in ims) + M * (len(ims) + 1) for _, ims in blocos)
    altura = 40 + sum(max(im.height for im, _ in ims) + 2 * ROT + M for _, ims in blocos)
    folha = Image.new("RGB", (largura, altura), (22, 18, 14))
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "As telas iniciais depois da retirada do mundo gerado (1.206.0): o jogo de hoje e a criação em cartões (R)",
           fill=(220, 200, 150), font=fonte(16))
    y = 40
    for rot, ims in blocos:
        d.text((M, y), rot, fill=(220, 200, 150), font=fonte(14))
        x = M
        for im, r in ims:
            d.text((x, y + ROT), r, fill=(150, 140, 120), font=fonte(13))
            folha.paste(im, (x, y + 2 * ROT))
            x += im.width + M
        y += max(im.height for im, _ in ims) + 2 * ROT + M
    folha.save(AQUI.parent / "folha-telas-iniciais.png")
    print(folha.size)


if __name__ == "__main__":
    main()
