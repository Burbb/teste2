"""Bancada: as grades de icones16.py em tamanho real (num chip escuro como o da carta), a 2× e a 12×, ao lado dos três
estados finais e do sprite atual. Só para trabalhar; as folhas de entrega são da prancha.py.
    python previa.py <saida.png> [<id> ...]
"""
import sys

from PIL import Image, ImageDraw

import icones16 as ic
from comum import CARVAO, TEXTO, amplia, final, fonte, grade_px, sprite, ATUAL

CHIP = (10, 11, 13, 255)


def imagem(ident):
    grade = ic.ICONES[ident][0]
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                c = ic.CORES[ch]
                im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


if __name__ == "__main__":
    saida, ids = sys.argv[1], sys.argv[2:] or list(ic.ICONES)
    Z = 10
    linha = 16 * Z + 50
    out = Image.new("RGBA", (40 + 3 * 70 + 16 * Z + 300, 60 + len(ids) * linha), CARVAO)
    d = ImageDraw.Draw(out)
    f = fonte()
    finais = [final(k) for k in ("firme", "guarda", "esquiva")]
    for i, ident in enumerate(ids):
        y = 20 + i * linha
        im = imagem(ident)
        d.text((20, y), ident, fill=TEXTO, font=f)
        # a fileira da carta: Firme, Em guarda, Esquiva e o novo, em chips escuros, 1× e 2×
        for k, o in enumerate(finais + [im]):
            d.rectangle([20 + k * 24, y + 20, 20 + k * 24 + 19, y + 39], fill=CHIP)
            out.alpha_composite(o, (22 + k * 24, y + 22))
            out.alpha_composite(amplia(o, 2), (20 + k * 40, y + 50))
        atual = ATUAL.get(ic.ESTADO_DE.get(ident, ident))
        if atual:
            d.text((20, y + 90), "atual:", fill=TEXTO, font=f)
            out.alpha_composite(sprite(atual), (70, y + 90))
            out.alpha_composite(amplia(sprite(atual), 2), (95, y + 82))
        out.alpha_composite(grade_px(im, Z), (200, y + 20))
    out.save(saida)
