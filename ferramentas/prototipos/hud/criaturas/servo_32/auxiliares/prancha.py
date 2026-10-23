"""A folha compacta do servo esquelético (comparacao.png): a referência da anatomia e do material (a caveira nua), a guia
de 32 e o Esqueleto inimigo aprovado (o de elmo, de quem ele precisa se distinguir); a luta, a 1920×945, em tamanho real,
com os mesmos dados, a coluna aliada com os dois servos (o "Esqueleto (Invocado)" do Erguer Servo e o "Lobo (servo)" do
Rei dos Mortos) no jogo de hoje, na SV2b anterior, no estudo nativo de 32 e na proposta de 16 (com a demonstração: o
retrato novo só no Esqueleto invocado, o lobo erguido com o da espécie); a carta a 2× com o inimigo ao lado; a fileira
na caixa da carta com retratos aprovados, real e a 3×; e o diagnóstico: a SV2b, o N32 e o N16 sem suavização.
Com --b, a do ajuste local (ajuste.png): o N16 × o N16B na mesma carta, com o N32 ao lado, a carta a 2×, a fileira e o
diagnóstico.
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
REF = RAIZ / "ferramentas/arte/referencias/icones/Caveira esquelética sombria em pixel art.png"
SV2B = AQUI.parents[1] / "chefes_e_especiais/proposta/servo-sv2b-16.png"
N32 = PASTA / "proposta/servo-n32-32.png"
N16 = PASTA / "proposta/servo-n16-16.png"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = [("atual (o jogo: os dois na caveira)", "atual"), ("SV2b (a anterior, de elmo)", "sv2b"),
         ("N32, o estudo nativo de 32", "n32"), ("N16, a proposta de 16 (o 16 ×2)", "n16")]
FILEIRA = ["esqueleto", "caido", "espectro", "lobo", "carnical", "cultista"]


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


def carta(reg, modo, nome):
    c = next(c for c in reg[f"{modo}/100"]["cartas"] if c["nome"] == nome)
    return c["caixa"]


def foto(modo):
    return Image.open(CAP / f"luta-servos-{modo}.png").convert("RGBA")


def main():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1500), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O servo esquelético — o estudo nativo de 32 e a proposta de 16 (protótipo; trocado só na página, "
           "nada no jogo)", fill=TEXTO, font=f)
    y = 38
    d.text((20, y), "a referência da anatomia e do osso (reduzida só para olhar) | a guia de 32, oculta na fonte | o "
           "Esqueleto inimigo aprovado (o de elmo), de quem o servo se distingue, a 6×", fill=TEXTO, font=f2)
    y += 18
    ref = Image.open(REF).convert("RGBA")
    fundo = Image.new("RGBA", ref.size, CARVAO)
    fundo.alpha_composite(ref)
    out.alpha_composite(fundo.resize((192, 192), Image.LANCZOS), (20, y))
    out.alpha_composite(grade(Image.open(PASTA / "guias/servo-guia-32.png").convert("RGBA"), 6), (232, y))
    out.alpha_composite(grade(Image.open(JOGO / "retrato-esqueleto-16.png").convert("RGBA"), 12), (444, y))
    y += 212
    d.text((20, y), "a luta, 1920×945 a 100%, tamanho real, os mesmos dados: a coluna aliada com o Esqueleto (Invocado) "
           "e o Lobo (servo), os dois do tipo \"servo\"", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (rot, modo) in enumerate(MODOS):
        a = carta(reg, modo, "Esqueleto (Invocado)")
        b = carta(reg, modo, "Lobo (servo)")
        cx = foto(modo).crop((min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])))
        d.text((20 + j * 370, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (20 + j * 370, y + 16))
        alto = max(alto, 16 + cx.height)
    y += alto + 8
    d.text((20, y), "nos modos de proposta, a demonstração da seleção futura: o retrato novo só no Esqueleto invocado "
           "(o Erguer Servo); o lobo erguido pelo Rei dos Mortos com o retrato da espécie", fill=TEXTO2, font=f2)
    y += 26
    d.text((20, y), "a carta a 2× (a foto de 100%, por vizinho mais próximo): SV2b | N32 | N16; embaixo, o Esqueleto "
           "inimigo da mesma luta", fill=TEXTO, font=f2)
    y += 18
    for j, modo in enumerate(("sv2b", "n32", "n16")):
        cx = foto(modo).crop(carta(reg, modo, "Esqueleto (Invocado)"))
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 480, y))
    y += 2 * cx.height + 8
    ini = foto("n32").crop(carta(reg, "n32", "Esqueleto"))
    out.alpha_composite(ini.resize((ini.width * 2, ini.height * 2), Image.NEAREST), (20, y))
    y += 2 * ini.height + 20
    sv2b = Image.open(SV2B).convert("RGBA")
    n32 = Image.open(N32).convert("RGBA")
    n16 = Image.open(N16).convert("RGBA")
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha += [("SV2b (16 ×2)", sv2b.resize((32, 32), Image.NEAREST)), ("N32", n32),
              ("N16 (16 ×2)", n16.resize((32, 32), Image.NEAREST))]
    d.text((20, y), "a fileira na caixa da carta, com retratos aprovados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 18
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(caixa(im), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(caixa(im).resize((108, 108), Image.NEAREST), (20 + j * 122, y))
        d.text((20 + j * 122, y + 112), rot, fill=TEXTO2, font=f2)
    y += 136
    d.text((20, y), "o diagnóstico, sem suavização: SV2b (a 12×) | N32 (a 6×) | N16 (a 12×)", fill=TEXTO, font=f2)
    y += 18
    for j, (im, z) in enumerate(((sv2b, 12), (n32, 6), (n16, 12))):
        out.alpha_composite(grade(im, z), (20 + j * 212, y))
    y += 192 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "comparacao.png")
    print("comparacao.png", out.size)


def ajuste():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    nome = "Esqueleto (Invocado)"
    assert carta(reg, "n16", nome) == carta(reg, "n16b", nome)  # a mesma carta
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O servo esquelético — o ajuste local do N16: N16 (anterior) × N16B, com o N32 ao lado (protótipo; "
           "trocado só na página, nada no jogo)", fill=TEXTO, font=f)
    y = 38
    modos = [("N16 (anterior)", "n16"), ("N16B (os dentes, a mordida e as órbitas)", "n16b"), ("N32 (a referência)", "n32")]
    d.text((20, y), "a luta, 1920×945 a 100%, tamanho real, os mesmos dados: a coluna aliada (o Lobo erguido com o "
           "retrato da espécie, a demonstração da seleção)", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, modo) in enumerate(modos):
        a = carta(reg, modo, nome)
        b = carta(reg, modo, "Lobo (servo)")
        cx = foto(modo).crop((min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])))
        d.text((20 + j * 370, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (20 + j * 370, y + 16))
    y += 16 + cx.height + 20
    d.text((20, y), "a carta a 2× (a foto de 100%, por vizinho mais próximo): N16 | N16B | N32", fill=TEXTO, font=f2)
    y += 18
    for j, (_, modo) in enumerate(modos):
        cx = foto(modo).crop(carta(reg, modo, nome))
        out.alpha_composite(cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST), (20 + j * 480, y))
    y += 2 * cx.height + 20
    n16 = Image.open(N16).convert("RGBA")
    n16b = Image.open(PASTA / "proposta/servo-n16b-16.png").convert("RGBA")
    n32 = Image.open(N32).convert("RGBA")
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha += [("N16 (anterior)", n16.resize((32, 32), Image.NEAREST)), ("N16B", n16b.resize((32, 32), Image.NEAREST)),
              ("N32", n32)]
    d.text((20, y), "a fileira na caixa da carta, com retratos aprovados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 18
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(caixa(im), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(caixa(im).resize((108, 108), Image.NEAREST), (20 + j * 122, y))
        d.text((20 + j * 122, y + 112), rot, fill=TEXTO2, font=f2)
    y += 136
    d.text((20, y), "o diagnóstico, sem suavização: N16 (a 12×) | N16B (a 12×; as linhas mudadas, 4, 5 e 9 a 11, marcadas "
           "à esquerda) | N32 (a 6×)", fill=TEXTO, font=f2)
    y += 18
    for j, (im, z) in enumerate(((n16, 12), (n16b, 12), (n32, 6))):
        out.alpha_composite(grade(im, z), (20 + j * 212, y))
    for a, b in ((4, 6), (9, 12)):
        d.line([(228, y + a * 12), (228, y + b * 12)], fill=(230, 160, 60, 255), width=3)
    y += 192 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "ajuste.png")
    print("ajuste.png", out.size)


if __name__ == "__main__":
    ajuste() if "--b" in sys.argv else main()
