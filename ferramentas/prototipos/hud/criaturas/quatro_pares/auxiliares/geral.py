"""A prancha geral dos quatro pares (geral.png): os 16 candidatos na caixa da carta (32 px) e a 3×, com o nome, o id
e a minha preferência marcada (preferida); embaixo, a fileira dos retratos do jogo, para a escala e o acabamento.
    python geral.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

import grades as gr

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
JOGO = AQUI.parents[5] / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2, OURO = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255), (214, 170, 90, 255)
PARES = (("Par 1, o pântano", (("Sapo-touro gigante", "sapo", "a"), ("Sanguessuga gigante", "sanguessuga", "a"))),
         ("Par 2, os conjuradores", (("Cultista", "cultista", "a"), ("Bruxa do pântano", "bruxa", "b"))),
         ("Par 3, os mortos-vivos", (("Carniçal", "carnical", "a"), ("Espectro", "espectro", "a"))),
         ("Par 4, as feras comuns", (("Javali selvagem", "javali", "a"), ("Rato gigante", "rato", "b"))))
JOGO_IDS = ("afogado", "ilse", "lobo", "bandido", "urso", "falcao", "troll", "rei-troll", "aranha", "rainha-aracnidea")


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


def nicho(im16, lado):
    cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
    cx.alpha_composite(amplia(im16, lado // 16), (3, 3))
    return cx


if __name__ == "__main__":
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1700, 1300), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Os quatro pares da madrugada de 22/10/2026 — 16 candidatos, propostas em avaliação, nada no jogo; "
                     "em dourado, a minha preferência", fill=TEXTO, font=f)
    y = 40
    for titulo, bichos in PARES:
        d.text((20, y), titulo, fill=TEXTO, font=f2)
        y += 18
        x = 20
        for nome, ident, pref in bichos:
            for m in "ab":
                im = gr.imagem(f"{ident}-{m}")
                out.alpha_composite(nicho(im, 32), (x, y)); out.alpha_composite(amplia(nicho(im, 32), 3), (x + 44, y))
                marca = " (preferida)" if m == pref else ""
                d.text((x, y + 118), f"{nome} {m.upper()}{marca}", fill=OURO if marca else TEXTO2, font=f2)
                d.text((x, y + 134), f"{ident}-{m}", fill=TEXTO2, font=f2)
                x += 410
        y += 160
    d.text((20, y), "os retratos do jogo (integrados), na caixa da carta — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 18
    for j, n in enumerate(JOGO_IDS):
        im = Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")
        out.alpha_composite(nicho(im, 32), (20 + j * 44, y))
        out.alpha_composite(amplia(nicho(im, 32), 3), (20 + j * 124, y + 48))
        d.text((20 + j * 124, y + 48 + 116), n, fill=TEXTO2, font=f2)
    y += 48 + 140
    out = out.crop((0, 0, 1700, y))
    out.save(PASTA / "geral.png")
    print("geral.png", out.size)
