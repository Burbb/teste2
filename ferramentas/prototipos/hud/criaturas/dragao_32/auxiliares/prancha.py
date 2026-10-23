"""A folha compacta do teste do Dragão em 32 nativos (comparacao.png): a luta em tamanho real, com os mesmos dados, no
jogo de hoje, na transposição de 16 (`dragao-t`, o 16 ×2) e na proposta nativa de 32, a 1920×945 (100%) e a 1536×756
(125%, a foto no tamanho do aparelho); a fileira na caixa da carta com os retratos aprovados (o Grifo e o Lobo Gélido
entre eles), real e a 3×; e o diagnóstico: a referência (o recorte da guia, reduzido só para olhar), a guia de 32
(oculta na fonte) e os dois desenhos, ampliados por fator inteiro, sem suavização, com a grade.
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
REF = RAIZ / "ferramentas/arte/referencias/icones/Cabeça ancestral de dragão de gelo-2.png"
T16 = AQUI.parents[1] / "chefes_e_especiais/proposta/dragao-t-16.png"
N32 = PASTA / "proposta/dragao-n32-32.png"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = [("atual (o jogo: o sprite do voador)", "atual"), ("T, a transposição de 16 (o 16 ×2)", "t16"),
         ("N32, a proposta nativa de 32", "n32")]
FILEIRA = ["grifo", "lobo-gelido", "harpia", "rei-troll", "rainha-aracnidea", "golem-primordial"]


def caixa(im32):
    """O nicho do retrato na carta: 36 px, a borda de 2 px, o fundo carvão, o retrato de 32 no meio."""
    cx = Image.new("RGBA", (36, 36), (58, 61, 67, 255))
    cx.paste((10, 11, 13, 255), (2, 2, 34, 34))
    cx.alpha_composite(im32, (2, 2))
    return cx


def grade(im, z):
    out = im.resize((im.width * z, im.height * z), Image.NEAREST)
    d = ImageDraw.Draw(out)
    passo = z * (2 if im.width == 32 and z < 6 else 1)
    for k in range(0, out.width + 1, z):
        d.line([(k, 0), (k, out.height)], fill=(255, 255, 255, 22))
        d.line([(0, k), (out.width, k)], fill=(255, 255, 255, 22))
    del passo
    return out


def main():
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Dragão de Gelo — o teste em 32×32 nativos (protótipo; trocado só na página, nada no jogo)", fill=TEXTO, font=f)
    y = 38
    for tela, rot in (("100", "1920×945 a 100% (a janela do Jean)"), ("125", "1536×756 a 125% (a foto no tamanho do aparelho)")):
        d.text((20, y), f"a luta, {rot}, tamanho real; os mesmos dados nos três", fill=TEXTO, font=f2)
        y += 18
        alto = 0
        for j, (rot_m, modo) in enumerate(MODOS):
            r = reg[f"{modo}/{tela}"]
            foto = Image.open(CAP / f"luta-dragao-{modo}-{tela}.png").convert("RGBA")
            esc = r["dpr"]
            cs = [[round(v * esc) for v in c["caixa"]] for c in r["cartas"]]
            grupo = foto.crop((min(c[0] for c in cs), min(c[1] for c in cs), max(c[2] for c in cs), max(c[3] for c in cs)))
            x = 20 + j * 480
            d.text((x, y), rot_m, fill=TEXTO2, font=f2)
            out.alpha_composite(grupo, (x, y + 16))
            alto = max(alto, 16 + grupo.height)
        y += alto + 20
    d.text((20, y), "a carta do Dragão a 2× (a foto de 100%, ampliada por vizinho mais próximo, só para olhar)", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (_, modo) in enumerate(MODOS):
        r = reg[f"{modo}/100"]
        c = next(c["caixa"] for c in r["cartas"] if c["nome"].startswith("Dragão"))
        cx = Image.open(CAP / f"luta-dragao-{modo}-100.png").convert("RGBA").crop(c)
        dois = cx.resize((cx.width * 2, cx.height * 2), Image.NEAREST)
        out.alpha_composite(dois, (20 + j * 480, y))
        alto = max(alto, dois.height)
    y += alto + 20
    t16 = Image.open(T16).convert("RGBA")
    n32 = Image.open(N32).convert("RGBA")
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA").resize((32, 32), Image.NEAREST)) for n in FILEIRA]
    linha += [("dragao-t (16 ×2)", t16.resize((32, 32), Image.NEAREST)), ("dragao-n32 (32)", n32)]
    d.text((20, y), "a fileira na caixa da carta, com retratos aprovados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 18
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(caixa(im), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        tres = caixa(im).resize((108, 108), Image.NEAREST)
        out.alpha_composite(tres, (20 + j * 122, y))
        d.text((20 + j * 122, y + 112), rot, fill=TEXTO2, font=f2)
    y += 136
    d.text((20, y), "o diagnóstico: a referência (o recorte da guia, reduzido só para olhar) | a guia de 32, oculta na fonte | "
           "T (16, a 12×) | N32 (32, a 6×) — sem suavização", fill=TEXTO, font=f2)
    y += 18
    ref = Image.open(REF).convert("RGBA")
    fundo = Image.new("RGBA", ref.size, CARVAO)
    fundo.alpha_composite(ref)
    out.alpha_composite(fundo.crop((27, 27, 1227, 1227)).resize((192, 192), Image.LANCZOS), (20, y))
    out.alpha_composite(grade(Image.open(PASTA / "guias/dragao-guia-32.png").convert("RGBA"), 6), (232, y))
    out.alpha_composite(grade(t16, 12), (444, y))
    out.alpha_composite(grade(n32, 6), (656, y))
    y += 192 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / "comparacao.png")
    print("comparacao.png", out.size)


if __name__ == "__main__":
    main()
