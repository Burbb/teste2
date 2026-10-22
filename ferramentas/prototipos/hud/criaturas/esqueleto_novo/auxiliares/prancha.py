"""A folha do Esqueleto do zero (esqueleto-novo.png): E1, E2 e E3 na caixa da carta (32) e no Bestiário (48) em tamanho
real, as mesmas caixas a 4× e a 12× com a grade, sem suavização; a fileira com os retratos do jogo, na caixa da carta.
    python prancha.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

import grades as gr

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
JOGO = AQUI.parents[5] / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
IDS = (("esqueleto-e1", "E1, o guarda morto"), ("esqueleto-e2", "E2, o encapuzado"), ("esqueleto-e3", "E3, a caveira nua"))
JOGO_IDS = ("afogado", "ilse", "lobo", "bandido", "troll", "rei-troll", "aranha", "rainha-aracnidea", "urso", "falcao")


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


def nicho(im16, lado):
    cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
    cx.alpha_composite(amplia(im16, lado // 16), (3, 3))
    return cx


def grade12(im16):
    g = amplia(im16, 12)
    fundo = Image.new("RGBA", g.size, (24, 21, 19, 255)); fundo.alpha_composite(g)
    dd = ImageDraw.Draw(fundo)
    for i in range(1, 16):
        dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255)); dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
    return fundo


if __name__ == "__main__":
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1400, 1200), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Esqueleto do zero: três direções na linguagem dos retratos do jogo; proposta, nada no jogo", fill=TEXTO, font=f)
    y = 40
    for j, (_, rot) in enumerate(IDS):
        d.text((20 + j * 320, y), rot, fill=TEXTO2, font=f2)
    y += 18
    d.text((20, y), "tamanho real: a carta (32) e o Bestiário (48)", fill=TEXTO, font=f2)
    for j, (ident, _) in enumerate(IDS):
        out.alpha_composite(nicho(gr.imagem(ident), 32), (20 + j * 320, y + 18))
        out.alpha_composite(nicho(gr.imagem(ident), 48), (70 + j * 320, y + 18))
    y += 18 + 54 + 16
    d.text((20, y), "as mesmas caixas a 4× (vizinho mais próximo)", fill=TEXTO, font=f2)
    for j, (ident, _) in enumerate(IDS):
        out.alpha_composite(amplia(nicho(gr.imagem(ident), 32), 4), (20 + j * 320, y + 18))
    y += 18 + 38 * 4 + 12
    for j, (ident, _) in enumerate(IDS):
        out.alpha_composite(amplia(nicho(gr.imagem(ident), 48), 4), (20 + j * 320, y))
    y += 54 * 4 + 16
    d.text((20, y), "a 12× com a grade", fill=TEXTO, font=f2)
    for j, (ident, _) in enumerate(IDS):
        out.alpha_composite(grade12(gr.imagem(ident)), (20 + j * 320, y + 18))
    y += 18 + 192 + 20
    d.text((20, y), "a fileira, na caixa da carta, com os retratos do jogo — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")) for n in JOGO_IDS] + \
        [(rot.split(",")[0], gr.imagem(i)) for i, rot in IDS]
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(nicho(im, 32), (20 + j * 44, y))
    y += 48
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(amplia(nicho(im, 32), 3), (20 + (j % 11) * 124, y + (j // 11) * 136))
        d.text((20 + (j % 11) * 124, y + (j // 11) * 136 + 116), rot, fill=TEXTO2, font=f2)
    y += ((len(linha) + 10) // 11) * 136 + 10
    out = out.crop((0, 0, 1400, y))
    out.save(PASTA / "esqueleto-novo.png")
    print("esqueleto-novo.png", out.size)
