"""A folha do Lich Menor em 32 e em 16 (comparacao.png; protótipo): a L1b (a base de identidade), o N32 e o N16 (no 32 da
carta), identificados, na mesma luta a 1920×945 em tamanho real, com o Esqueleto inimigo e o servo aliado (os retratos de
produção); a carta do Lich a 2×; a fileira na caixa da carta; e o diagnóstico sem suavização.
    python prancha.py      (depois do fotografar.mjs)
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
CHEFES = AQUI.parents[1] / "chefes_e_especiais"
RAIZ = AQUI.parents[5]
JOGO = RAIZ / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = [("atual (o jogo)", "atual"), ("L1b (a base de identidade)", "l1b"), ("N32, o estudo nativo de 32", "n32"),
         ("N16, a adaptação (o 16 ×2)", "n16")]
FILEIRA = ["esqueleto", "servo-esqueletico", "espectro", "carnical", "golem-primordial", "profeta-das-cinzas"]


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


def carta(reg, modo, nome):
    """A caixa da carta pelo nome exato ("Esqueleto" não é o "Esqueleto (Invocado)")."""
    return next(c["caixa"] for c in reg[f"{modo}/100"]["cartas"] if c["nome"] == nome)


def main():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1500), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Lich Menor — L1b × o estudo nativo de 32 × a adaptação para 16 (protótipo; trocado só na página, "
           "nada no jogo)", fill=TEXTO, font=f)
    y = 38
    d.text((20, y), "a luta, 1920×945 a 100%, tamanho real, os mesmos dados: o servo aliado (o Erguer Servo) à esquerda; "
           "o Lich e o Esqueleto inimigo à direita", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, modo) in enumerate(MODOS):
        im = Image.open(CAP / f"luta-lich-{modo}.png").convert("RGBA")
        s = carta(reg, modo, "Esqueleto (Invocado)")
        a, b = carta(reg, modo, "Lich Menor"), carta(reg, modo, "Esqueleto")
        ini = im.crop((min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])))
        ali = im.crop(s)
        x = 20 + j * 370
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(ali, (x, y + 16))
        out.alpha_composite(ini, (x, y + 16 + ali.height + 6))
    y += 16 + ali.height + 6 + ini.height + 20
    d.text((20, y), "a carta do Lich a 2× (a foto de 100%, por vizinho mais próximo): L1b | N32 | N16", fill=TEXTO, font=f2)
    y += 18
    for j, (_, modo) in enumerate(MODOS[1:]):
        cx = Image.open(CAP / f"luta-lich-{modo}.png").convert("RGBA").crop(carta(reg, modo, "Lich Menor"))
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 480, y))
    y += 2 * cx.height + 20
    l1b = Image.open(CHEFES / "proposta/lich-l1b-16.png").convert("RGBA")
    n32 = Image.open(PASTA / "proposta/lich-n32-32.png").convert("RGBA")
    n16 = Image.open(PASTA / "proposta/lich-n16-16.png").convert("RGBA")
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha += [("L1b (16 ×2)", l1b.resize((32, 32), Image.NEAREST)), ("N32", n32),
              ("N16 (16 ×2)", n16.resize((32, 32), Image.NEAREST))]
    d.text((20, y), "a fileira na caixa da carta, com retratos aprovados (o esqueleto inimigo e o servo ao lado) — tamanho "
           "real e 3×", fill=TEXTO, font=f2)
    y += 18
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(caixa(im), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(caixa(im).resize((108, 108), Image.NEAREST), (20 + j * 122, y))
        d.text((20 + j * 122, y + 112), rot, fill=TEXTO2, font=f2)
    y += 136
    d.text((20, y), "o diagnóstico, sem suavização: L1b (a 12×) | N32 (a 6×) | N16 (a 12×)", fill=TEXTO, font=f2)
    y += 18
    for j, (im, z) in enumerate(((l1b, 12), (n32, 6), (n16, 12))):
        out.alpha_composite(grade(im, z), (20 + j * 212, y))
    y += 192 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "comparacao.png")
    print("comparacao.png", out.size)


if __name__ == "__main__":
    main()
