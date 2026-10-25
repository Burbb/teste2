"""Monta a folha B anterior × R (a candidata) a partir de ../capturas/ (fotografar.mjs com VERSOES=b,r): as duas no
jogo, no mesmo contexto (a mesma campanha de teste, o mesmo balcão), a 1920×945 e a 1280×720 (reduzidas à metade), e a
arte de cada uma em tamanho real, recortada do jogo a 1920. O movimento está na folha-movimento.png. Grava
../folha-forja-r.png.

    python ferramentas/prototipos/hud/forja/auxiliares/folha_r.py
"""
import pathlib

from PIL import Image, ImageDraw

from folha import fonte

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"


def main():
    metade = lambda n: (lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS))(Image.open(CAP / f"{n}.png").convert("RGB"))
    arte = lambda n: Image.open(CAP / f"{n}.png").convert("RGB").crop((408, 138, 1472, 372))
    linhas = [
        ("1920×945 · a B anterior × a R (a candidata), no mesmo contexto", [(metade("1920-b-forja"), "B anterior"), (metade("1920-r-forja"), "R")]),
        ("1280×720 · a B anterior × a R", [(metade("1280-b-forja"), "B anterior"), (metade("1280-r-forja"), "R")]),
        ("a B anterior, a arte em tamanho real (1920)", [(arte("1920-b-forja"), "B")]),
        ("a R, a arte em tamanho real (1920), num quadro do ciclo", [(arte("1920-r-forja"), "R")]),
    ]
    M, ROT = 12, 22
    largura = max(sum(im.width for im, _ in ims) + M * (len(ims) + 1) for _, ims in linhas)
    altura = 40 + sum(max(im.height for im, _ in ims) + 2 * ROT + M for _, ims in linhas)
    folha = Image.new("RGB", (largura, altura), (22, 18, 14))
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "A forja: a B anterior × a R (a B refinada, o ferreiro forjando), a mesma campanha de teste e os mesmos serviços",
           fill=(220, 200, 150), font=fonte(16))
    y = 40
    for rot, ims in linhas:
        d.text((M, y), rot, fill=(220, 200, 150), font=fonte(14))
        x = M
        for im, r in ims:
            d.text((x, y + ROT), r, fill=(150, 140, 120), font=fonte(13))
            folha.paste(im, (x, y + 2 * ROT))
            x += im.width + M
        y += max(im.height for im, _ in ims) + 2 * ROT + M
    folha.save(AQUI.parent / "folha-forja-r.png", optimize=True)
    print(folha.size)


if __name__ == "__main__":
    main()
