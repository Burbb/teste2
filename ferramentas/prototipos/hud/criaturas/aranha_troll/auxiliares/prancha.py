"""As folhas da Aranha Gigante e do Troll (aranha.png, troll.png): a carta da luta a 1920×945, atual × A × B, em
tamanho real e a 2×; o Bestiário (o retrato a 3×) com o vizinho aprovado; a fileira na caixa da carta com os retratos
aprovados (Morel, Odette e os das criaturas e dos animais, dos PNGs de produção) em tamanho real e a 3×; e a 12× sem
suavização. Os recortes vêm das caixas que o fotografar.mjs grava no registro.
    python prancha.py
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

from previa import amplia, imagem

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
JOGO = AQUI.parents[5] / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = (("atual", "atual (traço)"), ("a", "proposta A"), ("b", "proposta B"))
CRIATURAS = {
    "aranha": dict(nome="Aranha gigante", a="A, de frente", b="B, de lado em ameaça", vizinho="Afogado"),
    "troll": dict(nome="Troll da montanha", a="A, de frente", b="B, de perfil com a corcunda", vizinho="Lobo"),
}
REG = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))


def abre(n):
    return Image.open(CAP / n).convert("RGBA")


def caixa_de(sit, modo, nome, campo="caixa"):
    return next(c[campo] for c in REG[f"{sit}/{modo}"]["caixas"] if c["nome"] == nome)


def nicho(r):
    """A caixa do retrato (38 px) em volta da imagem dele (32 px)."""
    return (r[0] - 3, r[1] - 3, r[2] + 3, r[3] + 3)


def caixa(im16):
    cx = Image.new("RGBA", (38, 38), (42, 36, 32, 255))
    cx.paste((13, 11, 10, 255), (2, 2, 36, 36))
    cx.alpha_composite(amplia(im16, 2), (3, 3))
    return cx


def grade12(im16):
    g = amplia(im16, 12)
    fundo = Image.new("RGBA", g.size, (24, 21, 19, 255))
    fundo.alpha_composite(g)
    dd = ImageDraw.Draw(fundo)
    for i in range(1, 16):
        dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255)); dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
    return fundo


def folha(chave):
    c = CRIATURAS[chave]
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 1600), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{c['nome']} — atual × {c['a']} × {c['b']}; 16×16 a 2× na carta e 3× no Bestiário; proposta, nada no jogo",
           fill=TEXTO, font=f)
    y = 44
    d.text((20, y), "a carta na luta (1920×945, os mesmos dados) — tamanho real e 2×", fill=TEXTO, font=f2)
    y += 20
    for j, (modo, rot) in enumerate(MODOS):
        cx = abre(f"luta-{modo}-palco.png").crop(caixa_de("luta", modo, c["nome"]))
        x = 20 + j * 520
        d.text((x, y), rot if modo == "atual" else f"{rot}: {c[modo]}", fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (x, y + 16)); out.alpha_composite(amplia(cx, 2), (x, y + 16 + cx.height + 8))
    y += 16 + 3 * 50 + 24
    d.text((20, y), f"o Bestiário (o retrato a 3×) — tamanho real; à esquerda, o {c['vizinho']} (aprovado)", fill=TEXTO, font=f2)
    y += 20
    viz = abre("bestiario-atual-pagina.png").crop(caixa_de("bestiario", "atual", c["vizinho"]))
    out.alpha_composite(viz, (20, y + 16))
    alto = viz.height
    for j, (modo, rot) in enumerate(MODOS):
        x = 400 + j * 370
        cartao = abre(f"bestiario-{modo}-pagina.png").crop(caixa_de("bestiario", modo, c["nome"]))
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cartao, (x, y + 16))
        alto = max(alto, cartao.height)
    y += 16 + alto + 24
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    aprovados = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] + \
        [(n.capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")))
         for n in ("afogado", "ilse", "lobo", "bandido", "urso", "falcao")]
    novos = [(rot, abre(f"luta-{modo}-palco.png").crop(nicho(caixa_de("luta", modo, c["nome"], "retrato"))))
             for modo, rot in MODOS]
    d.text((20, y), "a fileira, na caixa da carta: os retratos aprovados | atual, A e B (das fotos) — tamanho real e 3×",
           fill=TEXTO, font=f2)
    y += 20
    linha = aprovados + novos
    for j, (_, cx) in enumerate(linha):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(linha):
        out.alpha_composite(amplia(cx, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot, fill=TEXTO2, font=f2)
    y += 3 * 38 + 40
    luta = abre("luta-atual-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "a luta (atual, tamanho real): duas aranhas, o troll e o lobo aprovado", fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    d.text((20, y), "A e B a 12× (sem suavização, só para achar o pixel)", fill=TEXTO, font=f2)
    y += 20
    for j, ident in enumerate((f"{chave}-a", f"{chave}-b")):
        d.text((20 + j * 230, y), ident, fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(imagem(ident)), (20 + j * 230, y + 16))
    y += 16 + 192 + 20
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / f"{chave}.png")
    print(f"{chave}.png", out.size)


REFS = {"aranha": "Retrato pixelado da aranha sombria-1.png", "troll": "Retrato pixelado de troll montanhês-2.png"}
ROTULOS_R2 = {"aranha": ("1, a transposição de frente", "2, o rosto de perto", "3, as patas erguidas em arco"),
              "troll": ("1, a transposição em três quartos", "2, de frente", "3, de perfil")}


def folha_r2(chave):
    """A segunda rodada (aranha-r2.png, troll-r2.png): a referência gerada e a guia; as três propostas na carta a 32 px
    (tamanho real e 2×) e no Bestiário a 48 px, com os mesmos dados; a fileira com os retratos aprovados; e a 12×."""
    c = CRIATURAS[chave]
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    modos = [("atual", "atual (traço)")] + [(f"r2-{i}", r) for i, r in zip("123", ROTULOS_R2[chave])]
    out = Image.new("RGBA", (1800, 1700), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{c['nome']}, segunda rodada: três propostas pela referência gerada — proposta, nada no jogo",
           fill=TEXTO, font=f)
    y = 40
    ref = Image.open(AQUI.parents[4] / "arte/referencias/icones" / REFS[chave]).convert("RGBA")
    fundo = Image.new("RGBA", ref.size, CARVAO); fundo.alpha_composite(ref)
    guia = Image.open(PASTA / f"guias/{chave}-guia-16.png").convert("RGBA")
    d.text((20, y), "a referência (reduzida, só para olhar) | a guia a 16 (oculta nas fontes) | as três: 1×, a carta (2×) e a 12×",
           fill=TEXTO, font=f2)
    out.alpha_composite(fundo.resize((192, 192), Image.LANCZOS), (20, y + 18))
    g = Image.new("RGBA", (192, 192), CARVAO); g.alpha_composite(amplia(guia, 12)); out.alpha_composite(g, (222, y + 18))
    for j, i in enumerate("123"):
        im = imagem(f"{chave}-{i}")
        x = 440 + j * 290
        d.text((x, y + 18), ROTULOS_R2[chave][j], fill=TEXTO2, font=f2)
        out.alpha_composite(im, (x, y + 36)); out.alpha_composite(caixa(im), (x + 22, y + 36))
        out.alpha_composite(grade12(im), (x + 66, y + 36))
    y += 36 + 192 + 20
    d.text((20, y), "a carta na luta a 1920×945 (os mesmos dados), a 32 px — tamanho real e 2×", fill=TEXTO, font=f2)
    y += 20
    for j, (modo, rot) in enumerate(modos):
        cx = abre(f"luta-{modo}-palco.png").crop(caixa_de("luta", modo, c["nome"]))
        x = 20 + (j % 2) * 460
        yy = y + (j // 2) * (16 + 52 + 2 * 50 + 16)
        d.text((x, yy), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (x, yy + 16)); out.alpha_composite(amplia(cx, 2), (x, yy + 16 + cx.height + 6))
    y += 2 * (16 + 52 + 2 * 50 + 16) + 8
    d.text((20, y), "o Bestiário, o retrato a 48 px — tamanho real", fill=TEXTO, font=f2)
    y += 20
    alto = 0
    for j, (modo, rot) in enumerate(modos):
        cartao = abre(f"bestiario-{modo}-pagina.png").crop(caixa_de("bestiario", modo, c["nome"]))
        x = 20 + j * 370
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cartao, (x, y + 16))
        alto = max(alto, cartao.height)
    y += 16 + alto + 24
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    aprovados = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] + \
        [(n.capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")))
         for n in ("afogado", "ilse", "lobo", "bandido", "urso", "falcao")]
    novos = [(rot.split(",")[0], abre(f"luta-{modo}-palco.png").crop(nicho(caixa_de("luta", modo, c["nome"], "retrato"))))
             for modo, rot in modos]
    d.text((20, y), "a fileira, na caixa da carta: os retratos aprovados | atual, 1, 2 e 3 (das fotos) — tamanho real e 3×",
           fill=TEXTO, font=f2)
    y += 20
    linha = aprovados + novos
    for j, (_, cx) in enumerate(linha):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(linha):
        out.alpha_composite(amplia(cx, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot, fill=TEXTO2, font=f2)
    y += 3 * 38 + 40
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / f"{chave}-r2.png")
    print(f"{chave}-r2.png", out.size)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["r2"]:
        for chave in CRIATURAS:
            folha_r2(chave)
    else:
        for chave in CRIATURAS:
            folha(chave)
