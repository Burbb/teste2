"""A folha do antagonista em 32 nativos (comparacao.png; protótipo): a luta a 1920×945 em tamanho real com a Cria do
Vazio (o jogo hoje e o estudo, com um título feminino e um masculino), a carta a 2×, a fileira na caixa da carta com os
retratos aprovados vizinhos (a Cria do Vazio, o Caído, o Profeta das Cinzas, o Lich Menor, a Ilse), e o diagnóstico
sem suavização.
    python prancha.py      (depois do fotografar.mjs)
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
RAIZ = AQUI.parents[5]
JOGO = RAIZ / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = [("o jogo hoje (o sprite humano)", "atual"), ("o estudo, Noiva da Peste", "n32-f"),
         ("o estudo, Rei Enforcado", "n32-m")]
NOME = "Vharuk"
FILEIRA = ["cria-vazio", "caido", "profeta-das-cinzas", "lich-menor", "ilse", "senhor-da-guerra"]
ESTUDO = "antagonista-n32"


def caixa(im32):
    cx = Image.new("RGBA", (36, 36), (58, 61, 67, 255))
    cx.paste((10, 11, 13, 255), (2, 2, 34, 34))
    cx.alpha_composite(im32, (2, 2))
    return cx


def grade(im, z):
    out = Image.new("RGBA", (im.width * z, im.height * z), CARVAO)
    out.alpha_composite(im.resize((im.width * z, im.height * z), Image.NEAREST))
    d = ImageDraw.Draw(out)
    for k in range(0, out.width + 1, z):
        d.line([(k, 0), (k, out.height)], fill=(255, 255, 255, 22))
        d.line([(0, k), (out.width, k)], fill=(255, 255, 255, 22))
    return out


def cartas(reg, modo):
    return reg[modo]["cartas"]


def main():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1340, 1400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{NOME} — o estudo em 32 nativos (protótipo; trocado só na página, nada no jogo)", fill=TEXTO, font=f)
    y = 38
    d.text((20, y), "a luta, 1920×945 a 100%, tamanho real: o antagonista (montado pelo jogo) e a Cria do Vazio (o retrato de produção)", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, modo) in enumerate(MODOS):
        im = Image.open(CAP / f"luta-antagonista-{modo}.png").convert("RGBA")
        cs = [c["caixa"] for c in cartas(reg, modo) if c["nome"] != "Jean"]
        ini = im.crop((min(c[0] for c in cs), min(c[1] for c in cs), max(c[2] for c in cs), max(c[3] for c in cs)))
        d.text((20 + j * 300, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(ini, (20 + j * 300, y + 16))
    y += 16 + ini.height + 20
    d.text((20, y), "a carta do antagonista a 2× (a foto de 100%, por vizinho mais próximo): hoje | o estudo (f) | o estudo (m)", fill=TEXTO, font=f2)
    y += 18
    for j, (_, modo) in enumerate(MODOS):
        c = next(c["caixa"] for c in cartas(reg, modo) if c["nome"].startswith(NOME))
        cx = Image.open(CAP / f"luta-antagonista-{modo}.png").convert("RGBA").crop(c)
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 435, y))
    y += 2 * cx.height + 20
    n32 = Image.open(PASTA / f"proposta/{ESTUDO}-32.png").convert("RGBA")
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha.insert(3, ("estudo N32", n32))
    d.text((20, y), "a fileira na caixa da carta, com retratos aprovados (no jogo, o 16 ×2) — tamanho real e 3×", fill=TEXTO,
           font=f2)
    y += 18
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(caixa(im), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(caixa(im).resize((108, 108), Image.NEAREST), (20 + j * 122, y))
        d.text((20 + j * 122, y + 112), rot, fill=TEXTO2, font=f2)
    y += 136
    d.text((20, y), "a ampliação sem suavização (a 10×, com a grade dos pixels)", fill=TEXTO, font=f2)
    y += 18
    out.alpha_composite(grade(n32, 10), (20, y))
    y += 320 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "comparacao.png")
    print("comparacao.png", out.size)


if __name__ == "__main__":
    main()
