"""Monta a folha do "Carregar jogo" a partir de ../capturas/ (fotografar.mjs): hoje × R com os mesmos saves (dez
partidas, duas do mundo gerado e uma danificada), nas duas janelas; o fim da lista (os que não abrem), uma partida, 22
partidas e o foco do teclado na R; o título sem saves. As páginas a 1920 reduzidas à metade e as de 1280 a três quartos.
Grava ../folha-saves.png.

    python ferramentas/prototipos/hud/carregar-jogo/auxiliares/folha.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
LINHAS = [
    ("1920×945 · dez partidas: hoje × R", [("1920-atual-varias", "hoje"), ("1920-r-varias", "R")]),
    ("1280×720 · dez partidas: hoje × R", [("1280-atual-varias", "hoje"), ("1280-r-varias", "R")]),
    ("1280×720 · o fim da lista (o danificado e os do mundo gerado): hoje × R",
     [("1280-atual-varias-fim", "hoje"), ("1280-r-varias-fim", "R")]),
    ("R · uma partida (1920) e 22 partidas, a lista rolando (1280)", [("1920-r-uma", "1920 · uma"), ("1280-r-muitas", "1280 · 22")]),
    ("R · o foco do teclado (a seta para baixo) e o título sem saves (sem \"Carregar jogo\")",
     [("1280-r-varias-foco", "1280 · foco no segundo cartão"), ("1280-r-vazia", "1280 · sem saves")]),
]


def fonte(t):
    try:
        return ImageFont.truetype("georgia.ttf", t)
    except OSError:
        return ImageFont.load_default()


def reduzir(im):
    f = 0.5 if im.width > 1600 else 0.75
    return im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)


def main():
    blocos = [(rot, [(reduzir(Image.open(CAP / f"{n}.png").convert("RGB")), r) for n, r in ims]) for rot, ims in LINHAS]
    M, ROT = 12, 22
    largura = max(sum(im.width for im, _ in ims) + M * (len(ims) + 1) for _, ims in blocos)
    altura = 40 + sum(max(im.height for im, _ in ims) + 2 * ROT + M for _, ims in blocos)
    folha = Image.new("RGB", (largura, altura), (22, 18, 14))
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "Carregar jogo: o de hoje × a proposta R, os mesmos saves temporários (SIMULAÇÃO: progresso escrito direto)",
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
    folha.save(AQUI.parent / "folha-saves.png", optimize=True)
    print(folha.size)


if __name__ == "__main__":
    main()
