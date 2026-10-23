"""A folha compacta do Espantalho (comparacao.png): a luta pelo evento real, a 1920×945, em tamanho real, com os mesmos
dados, no jogo de hoje, na T anterior (o 16 ×2), no estudo nativo de 32 e na proposta de 16 (o 16 ×2); a carta a 2×; a
fileira na caixa da carta com retratos aprovados, real e a 3×; e o diagnóstico: a referência (o recorte da guia,
reduzido só para olhar), a guia de 32 (oculta na fonte) e os três desenhos ampliados por fator inteiro, sem suavização.
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
REF = RAIZ / "ferramentas/arte/referencias/icones/Espantalho possuído em pixel art-5.png"
T16 = AQUI.parents[1] / "chefes_e_especiais/proposta/espantalho-t-16.png"
N32 = PASTA / "proposta/espantalho-n32-32.png"
N16 = PASTA / "proposta/espantalho-n16-16.png"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = [("atual (o jogo: o sprite da planta)", "atual"), ("T, a transposição anterior (o 16 ×2)", "t"),
         ("N32, o estudo nativo de 32", "n32"), ("N16, a proposta de 16 (o 16 ×2)", "n16")]
FILEIRA = ["arvore-desperta", "bandido", "caido", "cultista", "golem-primordial", "dragao-de-gelo"]


def caixa(im32):
    """O nicho do retrato na carta: 36 px, a borda de 2 px, o fundo carvão, o retrato de 32 no meio."""
    cx = Image.new("RGBA", (36, 36), (58, 61, 67, 255))
    cx.paste((10, 11, 13, 255), (2, 2, 34, 34))
    cx.alpha_composite(im32, (2, 2))
    return cx


def grade(im, z):
    out = im.resize((im.width * z, im.height * z), Image.NEAREST)
    d = ImageDraw.Draw(out)
    for k in range(0, out.width + 1, z):
        d.line([(k, 0), (k, out.height)], fill=(255, 255, 255, 22))
        d.line([(0, k), (out.width, k)], fill=(255, 255, 255, 22))
    return out


def main():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1200), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Espantalho Possuído — o estudo nativo de 32 e a proposta de 16 (protótipo; trocado só na página, nada no jogo)",
           fill=TEXTO, font=f)
    y = 38
    d.text((20, y), "a luta pelo evento real, 1920×945 a 100%, tamanho real; os mesmos dados", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (rot, modo) in enumerate(MODOS):
        c = reg[f"{modo}/100"]["cartas"][0]["caixa"]
        cx = Image.open(CAP / f"espantalho-{modo}.png").convert("RGBA").crop(c)
        d.text((20 + j * 370, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (20 + j * 370, y + 16))
        alto = max(alto, 16 + cx.height)
    y += alto + 20
    d.text((20, y), "a carta a 2× (a foto de 100%, por vizinho mais próximo, só para olhar)", fill=TEXTO, font=f2)
    y += 18
    for j, (_, modo) in enumerate(MODOS[1:]):
        c = reg[f"{modo}/100"]["cartas"][0]["caixa"]
        cx = Image.open(CAP / f"espantalho-{modo}.png").convert("RGBA").crop(c)
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 480, y))
    y += 2 * (c[3] - c[1]) + 20
    t16 = Image.open(T16).convert("RGBA")
    n32 = Image.open(N32).convert("RGBA")
    n16 = Image.open(N16).convert("RGBA")
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha += [("T (16 ×2)", t16.resize((32, 32), Image.NEAREST)), ("N32", n32), ("N16 (16 ×2)", n16.resize((32, 32), Image.NEAREST))]
    d.text((20, y), "a fileira na caixa da carta, com retratos aprovados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 18
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(caixa(im), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(caixa(im).resize((108, 108), Image.NEAREST), (20 + j * 122, y))
        d.text((20 + j * 122, y + 112), rot, fill=TEXTO2, font=f2)
    y += 136
    d.text((20, y), "o diagnóstico, sem suavização: a referência (o recorte da guia, reduzido só para olhar) | a guia de 32, "
           "oculta na fonte | T (a 12×) | N32 (a 6×) | N16 (a 12×)", fill=TEXTO, font=f2)
    y += 18
    ref = Image.open(REF).convert("RGBA")
    fundo = Image.new("RGBA", ref.size, CARVAO)
    fundo.alpha_composite(ref)
    out.alpha_composite(fundo.crop((27, 27, 1227, 1227)).resize((192, 192), Image.LANCZOS), (20, y))
    out.alpha_composite(grade(Image.open(PASTA / "guias/espantalho-guia-32.png").convert("RGBA"), 6), (232, y))
    out.alpha_composite(grade(t16, 12), (444, y))
    out.alpha_composite(grade(n32, 6), (656, y))
    out.alpha_composite(grade(n16, 12), (868, y))
    y += 192 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "comparacao.png")
    print("comparacao.png", out.size)


if __name__ == "__main__":
    main()
