"""A folha para a decisão do Lich Menor (lich-decisao.png; nada redesenhado): a L1, a L1b e a L2, identificadas, na mesma
luta a 1920×945 em tamanho real, com o Esqueleto inimigo e o servo aliado (os retratos de produção); a carta do Lich a 2×;
a fileira na caixa da carta; o diagnóstico a 12×, sem suavização; e o que a L1b mudou na L1, pixel a pixel (marcado).
    python prancha_lich.py      (depois do fotografar_lich.mjs, com a pasta capturas-lich)
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas-lich"
RAIZ = AQUI.parents[5]
JOGO = RAIZ / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = [("atual (o jogo)", "atual"), ("L1 (a base)", "l1"), ("L1b (o refinamento da L1)", "l1b"), ("L2 (o grimório)", "l2")]
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
    d.text((20, 10), "Lich Menor — a L1, a L1b e a L2 para a decisão (protótipo; trocado só na página, nada no jogo, "
           "nada redesenhado)", fill=TEXTO, font=f)
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
    d.text((20, y), "a carta do Lich a 2× (a foto de 100%, por vizinho mais próximo): L1 | L1b | L2", fill=TEXTO, font=f2)
    y += 18
    for j, (_, modo) in enumerate(MODOS[1:]):
        cx = Image.open(CAP / f"luta-lich-{modo}.png").convert("RGBA").crop(carta(reg, modo, "Lich Menor"))
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 480, y))
    y += 2 * cx.height + 20
    props = {m: Image.open(PASTA / f"proposta/lich-{m}-16.png").convert("RGBA") for m in ("l1", "l1b", "l2")}
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha += [(f"{m.upper().replace('B', 'b')} (16 ×2)", props[m].resize((32, 32), Image.NEAREST)) for m in ("l1", "l1b", "l2")]
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
    d.text((20, y), "o diagnóstico, sem suavização (a 12×): L1 | L1b | L2 | o que a L1b mudou na L1 (os pixels diferentes "
           "em laranja, sobre a L1 apagada)", fill=TEXTO, font=f2)
    y += 18
    for j, m in enumerate(("l1", "l1b", "l2")):
        out.alpha_composite(grade(props[m], 12), (20 + j * 212, y))
    dif = props["l1"].copy()
    apag = Image.new("RGBA", dif.size, (13, 11, 10, 160))
    dif.alpha_composite(apag)
    n = 0
    for yy in range(16):
        for xx in range(16):
            if props["l1"].getpixel((xx, yy)) != props["l1b"].getpixel((xx, yy)):
                dif.putpixel((xx, yy), (240, 150, 40, 255))
                n += 1
    out.alpha_composite(grade(dif, 12), (20 + 3 * 212, y))
    d.text((20 + 3 * 212, y + 196), f"{n} pixels diferentes", fill=TEXTO2, font=f2)
    y += 192 + 30
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "lich-decisao.png")
    print("lich-decisao.png", out.size, "diferentes L1 × L1b:", n)


if __name__ == "__main__":
    main()
