"""A folha compacta da Hidra do Brejo (comparacao.png): a referência (o material, a anatomia e a expressão; a direção das
cabeças foi corrigida pelo Jean: todas para a esquerda) e a guia de 32; a luta pela guardiã, a 1920×945, em tamanho real,
com os mesmos dados, no jogo de hoje, na T recusada (o 16 ×2), no estudo nativo de 32 e na proposta de 16 (o 16 ×2); a
carta a 2×; a fileira na caixa da carta com retratos aprovados, real e a 3×; e o diagnóstico: a T, o N32 e o N16
ampliados por fator inteiro, sem suavização.
Com --b, a da segunda construção de 32 (construcao-32.png): o N32 anterior × o N32B na mesma luta, a carta a 2×, a
fileira e o diagnóstico (sem nova adaptação para 16).
    python prancha.py [--b]      (depois do fotografar.mjs)
"""
import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
RAIZ = AQUI.parents[5]
JOGO = RAIZ / "rpg/web/static/hud/icones"
REF = RAIZ / "ferramentas/arte/referencias/icones/Hidra do pântano de três cabeças-1.png"
RECORTE = (20, 40, 1240, 1260)
T16 = AQUI.parents[1] / "chefes_e_especiais/proposta/hidra-t-16.png"
N32 = PASTA / "proposta/hidra-n32-32.png"
N16 = PASTA / "proposta/hidra-n16-16.png"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = [("atual (o jogo: a fera)", "atual"), ("T (a transposição recusada)", "t"),
         ("N32, o estudo nativo de 32", "n32"), ("N16, a proposta de 16 (o 16 ×2)", "n16")]
FILEIRA = ["sapo", "sanguessuga", "dragao-de-gelo", "rei-troll", "rainha-aracnidea", "senhor-da-guerra"]


def caixa(im32):
    """O nicho do retrato na carta: 36 px, a borda de 2 px, o fundo carvão, o retrato de 32 no meio."""
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


def foto(reg, modo):
    carta = next(c for c in reg[f"{modo}/100"]["cartas"] if c["nome"].startswith("Hidra do Brejo"))
    return Image.open(CAP / f"luta-hidra-{modo}.png").convert("RGBA").crop(carta["caixa"])


def main():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Hidra do Brejo — o estudo nativo de 32 e a proposta de 16 (protótipo; trocado só na página, "
           "nada no jogo)", fill=TEXTO, font=f)
    y = 38
    d.text((20, y), "a referência (o recorte de 1220 px a partir de (20, 40), reduzido só para olhar; as cabeças dela "
           "olham para lados diferentes, o Jean corrigiu: todas para a esquerda) e a guia de 32, oculta na fonte", fill=TEXTO, font=f2)
    y += 18
    ref = Image.open(REF).convert("RGBA")
    fundo = Image.new("RGBA", ref.size, CARVAO)
    fundo.alpha_composite(ref)
    out.alpha_composite(fundo.crop(RECORTE).resize((192, 192), Image.LANCZOS), (20, y))
    out.alpha_composite(grade(Image.open(PASTA / "guias/hidra-guia-32.png").convert("RGBA"), 6), (232, y))
    y += 212
    d.text((20, y), "a luta da guardiã, 1920×945 a 100%, tamanho real; os mesmos dados", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (rot, modo) in enumerate(MODOS):
        cx = foto(reg, modo)
        d.text((20 + j * 370, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (20 + j * 370, y + 16))
        alto = max(alto, 16 + cx.height)
    y += alto + 20
    d.text((20, y), "a carta a 2× (a foto de 100%, por vizinho mais próximo, só para olhar): T | N32 | N16", fill=TEXTO,
           font=f2)
    y += 18
    for j, modo in enumerate(("t", "n32", "n16")):
        cx = foto(reg, modo)
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 480, y))
    y += 2 * cx.height + 20
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
    d.text((20, y), "o diagnóstico, sem suavização: T (a 12×) | N32 (a 6×) | N16 (a 12×)", fill=TEXTO, font=f2)
    y += 18
    for j, (im, z) in enumerate(((t16, 12), (n32, 6), (n16, 12))):
        out.alpha_composite(grade(im, z), (20 + j * 212, y))
    y += 192 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "comparacao.png")
    print("comparacao.png", out.size)


def segunda():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    assert foto(reg, "n32").size == foto(reg, "n32b").size  # a mesma carta
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Hidra do Brejo — a segunda construção de 32: N32 (anterior) × N32B (protótipo; trocado só na página, "
           "nada no jogo)", fill=TEXTO, font=f)
    y = 38
    d.text((20, y), "a referência (o material e a anatomia; a direção corrigida pelo Jean: todas para a esquerda)",
           fill=TEXTO, font=f2)
    y += 18
    ref = Image.open(REF).convert("RGBA")
    fundo = Image.new("RGBA", ref.size, CARVAO)
    fundo.alpha_composite(ref)
    out.alpha_composite(fundo.crop(RECORTE).resize((192, 192), Image.LANCZOS), (20, y))
    y += 212
    d.text((20, y), "a luta da guardiã, 1920×945 a 100%, tamanho real; os mesmos dados", fill=TEXTO, font=f2)
    y += 18
    modos = [("atual (o jogo: a fera)", "atual"), ("N32 (anterior)", "n32"), ("N32B (a construção nova)", "n32b")]
    for j, (rot, modo) in enumerate(modos):
        d.text((20 + j * 370, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(foto(reg, modo), (20 + j * 370, y + 16))
    y += 16 + foto(reg, "n32").height + 20
    d.text((20, y), "a carta a 2× (a foto de 100%, por vizinho mais próximo): N32 | N32B", fill=TEXTO, font=f2)
    y += 18
    for j, modo in enumerate(("n32", "n32b")):
        cx = foto(reg, modo)
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 480, y))
    y += 2 * cx.height + 20
    n32 = Image.open(N32).convert("RGBA")
    n32b = Image.open(PASTA / "proposta/hidra-n32b-32.png").convert("RGBA")
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha += [("N32 (anterior)", n32), ("N32B", n32b)]
    d.text((20, y), "a fileira na caixa da carta, com retratos aprovados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 18
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(caixa(im), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(caixa(im).resize((108, 108), Image.NEAREST), (20 + j * 122, y))
        d.text((20 + j * 122, y + 112), rot, fill=TEXTO2, font=f2)
    y += 136
    d.text((20, y), "o diagnóstico, sem suavização: N32 (a 8×) | N32B (a 8×)", fill=TEXTO, font=f2)
    y += 18
    for j, im in enumerate((n32, n32b)):
        out.alpha_composite(grade(im, 8), (20 + j * 276, y))
    y += 256 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "construcao-32.png")
    print("construcao-32.png", out.size)


if __name__ == "__main__":
    segunda() if "--b" in sys.argv else main()
