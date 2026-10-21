"""Bancada: as cabeças de grades.py numa caixa de carta escura (36 px, a 2×) ao lado da carta aprovada da Odette e dos
sprites atuais (o recorte da captura a 1920×945), a 3× do Bestiário e a 12× com a grade.
    python previa.py <saida.png>
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

import grades as gr

AQUI = pathlib.Path(__file__).resolve().parent
CRIATURAS = AQUI.parents[1]
CARVAO, CAIXA, BORDA = (13, 11, 10, 255), (13, 11, 10, 255), (42, 36, 32, 255)


def imagem(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(gr.CAMADAS[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                c = gr.CORES[ch]
                im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


if __name__ == "__main__":
    f = ImageFont.truetype("arial.ttf", 13)
    out = Image.new("RGBA", (900, 520), CARVAO)
    d = ImageDraw.Draw(out)
    ali = Image.open(CRIATURAS / "capturas/aliados-palco.png").convert("RGBA")
    odette = ali.crop((55, 252, 93, 290))
    d.text((20, 10), "a carta (36 px, a arte a 2×): Odette aprovada | proposta", fill=(210, 210, 214, 255), font=f)
    out.alpha_composite(odette, (20, 34))
    for j, ident in enumerate(gr.CAMADAS):
        x = 80 + j * 60
        d.rectangle([x, 34, x + 35, 69], fill=CAIXA, outline=BORDA, width=2)
        out.alpha_composite(amplia(imagem(ident), 2), (x + 2, 36))
    d.text((220, 34), "1×:", fill=(140, 140, 148, 255), font=f)
    for j, ident in enumerate(gr.CAMADAS):
        out.alpha_composite(imagem(ident), (250 + j * 24, 36))
        out.alpha_composite(amplia(imagem(ident), 3), (320 + j * 60, 24))
    y = 100
    for j, ident in enumerate(gr.CAMADAS):
        g = amplia(imagem(ident), 12)
        fundo = Image.new("RGBA", g.size, (24, 21, 19, 255))
        fundo.alpha_composite(g)
        dd = ImageDraw.Draw(fundo)
        for i in range(1, 16):
            dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255)); dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
        out.alpha_composite(fundo, (20 + j * 220, y))
        d.text((20 + j * 220, y + 196), ident, fill=(210, 210, 214, 255), font=f)
    out.save(sys.argv[1])
