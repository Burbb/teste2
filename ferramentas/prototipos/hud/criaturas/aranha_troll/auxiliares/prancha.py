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


def folha_troll_final():
    """O Troll no jogo (1.166.0, troll-final.png): o aprovado × o PNG de produção; a carta e o Bestiário com os
    arquivos reais (o modo "final", sem troca); a luta com o Rei Troll, que continua na caveira; a fileira."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 1200), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Troll da montanha no jogo (1.166.0): o troll-1 da segunda rodada, sem retoques, pela família",
           fill=TEXTO, font=f)
    a, b = imagem("troll-1"), Image.open(JOGO / "retrato-troll-16.png").convert("RGBA")
    d.text((20, 32), f"troll-1 (aprovado) | retrato-troll-16 (no jogo): {'idênticos' if a.tobytes() == b.tobytes() else 'DIFERENTES'}",
           fill=TEXTO2, font=f2)
    out.alpha_composite(grade12(a), (20, 50)); out.alpha_composite(grade12(b), (230, 50))
    y = 50 + 192 + 20
    carta = abre("luta-final-palco.png").crop(caixa_de("luta", "final", "Troll da montanha"))
    cartao = abre("bestiario-final-pagina.png").crop(caixa_de("bestiario", "final", "Troll da montanha"))
    d.text((20, y), "a carta (32 px, tamanho real e 2×) e o Bestiário (48 px, tamanho real), com os arquivos de produção",
           fill=TEXTO, font=f2)
    out.alpha_composite(carta, (20, y + 18)); out.alpha_composite(amplia(carta, 2), (20, y + 18 + carta.height + 8))
    out.alpha_composite(cartao, (480, y + 18))
    y += 18 + max(3 * carta.height + 8, cartao.height) + 20
    luta = abre("rei-final-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "o Rei Troll (o guardião) continua na caveira; o troll da montanha ao lado, com o retrato — tamanho real",
           fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    linha = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] + \
        [(n.capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")))
         for n in ("afogado", "ilse", "lobo", "bandido", "urso", "falcao", "troll")]
    d.text((20, y), "a fileira dos retratos do jogo, na caixa da carta — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, cx) in enumerate(linha):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(linha):
        out.alpha_composite(amplia(cx, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot, fill=TEXTO2, font=f2)
    y += 3 * 38 + 40
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "troll-final.png")
    print("troll-final.png", out.size)


def folha_r3():
    """A terceira rodada (rei-aranha.png): o Troll comum (no jogo) × a proposta do Rei Troll, e a Aranha 2 anterior × a
    2B; 1×, a caixa da carta, a 3× e a 12×; a carta a 32 px (e o Bestiário a 48, a aranha; o Rei é guardião e não tem
    Bestiário) com os mesmos dados a 1920×945; a fileira com os retratos do jogo."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2000), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Rei Troll (a partir do Troll 2) e a Aranha 2B — propostas, nada no jogo", fill=TEXTO, font=f)
    y = 40
    pares = (("Troll comum (no jogo, 1.166.0)", Image.open(JOGO / "retrato-troll-16.png").convert("RGBA"),
              "Rei Troll (proposta: o Troll 2 com a coroa de sucata)", imagem("rei-troll")),
             ("Aranha 2 (anterior)", imagem("aranha-2"), "Aranha 2B (proposta)", imagem("aranha-2b")))
    for ra, a, rb, b in pares:
        for k, (rot, im) in enumerate(((ra, a), (rb, b))):
            x = 20 + k * 660
            d.text((x, y), rot, fill=TEXTO, font=f2)
            out.alpha_composite(im, (x, y + 18)); out.alpha_composite(caixa(im), (x + 22, y + 18))
            out.alpha_composite(amplia(caixa(im), 3), (x + 66, y + 18)); out.alpha_composite(grade12(im), (x + 190, y + 18))
        y += 18 + 192 + 22
    d.text((20, y), "a luta do Rei Troll a 1920×945 (os mesmos dados): no jogo (a caveira) × a proposta — a carta em tamanho real e 2×",
           fill=TEXTO, font=f2)
    y += 20
    for k, modo in enumerate(("final", "rei")):
        # a caixa do modo "rei" vale para os dois: a mesma luta, os mesmos dados, o mesmo lugar da carta
        cx = abre(f"rei-{modo}-palco.png").crop(caixa_de("rei", "rei", "Rei Troll"))
        out.alpha_composite(cx, (20 + k * 460, y)); out.alpha_composite(amplia(cx, 2), (20 + k * 460, y + cx.height + 6))
    y += 3 * 50 + 30
    luta = abre("rei-rei-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "a luta com a proposta do Rei (tamanho real): o Rei ao lado do Troll comum do jogo", fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    d.text((20, y), "a Aranha a 1920×945: anterior (2) × nova (2B) — a carta a 32 px e o Bestiário a 48 px", fill=TEXTO, font=f2)
    y += 20
    for k, modo in enumerate(("r2-2", "r3")):
        cx = abre(f"luta-{modo}-palco.png").crop(caixa_de("luta", modo, "Aranha gigante"))
        cartao = abre(f"bestiario-{modo}-pagina.png").crop(caixa_de("bestiario", modo, "Aranha gigante"))
        x = 20 + k * 760
        out.alpha_composite(cx, (x, y)); out.alpha_composite(amplia(cx, 2), (x, y + cx.height + 6))
        out.alpha_composite(cartao, (x, y + 3 * cx.height + 20))
    y += 3 * 50 + 20 + 160 + 20
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    linha = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] + \
        [(n.capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")))
         for n in ("afogado", "ilse", "lobo", "bandido", "urso", "falcao", "troll")] + \
        [("Rei Troll (proposta)", caixa(imagem("rei-troll"))), ("Aranha 2B (proposta)", caixa(imagem("aranha-2b")))]
    d.text((20, y), "a fileira, na caixa da carta, com os retratos do jogo — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, cx) in enumerate(linha):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(linha):
        out.alpha_composite(amplia(cx, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot[:18], fill=TEXTO2, font=f2)
    y += 3 * 38 + 40
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "rei-aranha.png")
    print("rei-aranha.png", out.size)


def folha_coroa(ref):
    """A coroa dourada do Rei Troll (rei-coroa.png): a referência; o Troll comum do jogo, a base sem coroa (o Troll 2), a
    proposta anterior (a sucata) e a nova (o ouro) na caixa da carta, em tamanho real, a 3× e a 12×; e a carta na luta do
    Rei a 1920×945 (tamanho real e 2×), a anterior e a nova."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 1200), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Rei Troll: a coroa dourada pela referência, sobre o Troll 2 sem mexer no rosto — proposta, nada no jogo",
           fill=TEXTO, font=f)
    r = Image.open(ref).convert("RGBA")
    fundo = Image.new("RGBA", r.size, CARVAO); fundo.alpha_composite(r)
    d.text((20, 32), "a referência (reduzida, só para olhar)", fill=TEXTO2, font=f2)
    out.alpha_composite(fundo.resize((192, 192), Image.LANCZOS), (20, 50))
    y = 50 + 192 + 20
    linha = (("Troll comum (no jogo)", Image.open(JOGO / "retrato-troll-16.png").convert("RGBA")),
             ("base: o Troll 2, sem coroa", imagem("troll-2")), ("anterior: a sucata", imagem("rei-troll")),
             ("nova: a coroa dourada", imagem("rei-troll-ouro")))
    d.text((20, y), "na caixa da carta: tamanho real, 3× e 12× (na nova, os pixels que mudaram em relação à base em vermelho: "
                    "só as quatro linhas da coroa)", fill=TEXTO, font=f2)
    y += 20
    base = imagem("troll-2")
    for j, (rot, im) in enumerate(linha):
        x = 20 + j * 440
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(caixa(im), (x, y + 18)); out.alpha_composite(amplia(caixa(im), 3), (x + 46, y + 18))
        g = grade12(im)
        if rot.startswith("nova"):
            dd = ImageDraw.Draw(g)
            for py in range(16):
                for px in range(16):
                    if im.getpixel((px, py)) != base.getpixel((px, py)):
                        dd.rectangle([px * 12, py * 12, px * 12 + 11, py * 12 + 11], outline=(230, 40, 40, 255))
        out.alpha_composite(g, (x + 170, y + 18))
    y += 18 + 192 + 24
    d.text((20, y), "a carta na luta do Rei a 1920×945 (os mesmos dados): a anterior × a nova — tamanho real e 2×", fill=TEXTO, font=f2)
    y += 20
    for k, modo in enumerate(("rei", "rei2")):
        cx = abre(f"rei-{modo}-palco.png").crop(caixa_de("rei", modo, "Rei Troll"))
        out.alpha_composite(cx, (20 + k * 460, y)); out.alpha_composite(amplia(cx, 2), (20 + k * 460, y + cx.height + 6))
    y += 3 * 50 + 20
    luta = abre("rei-rei2-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "a luta (tamanho real): o Rei com a coroa nova ao lado do Troll comum do jogo", fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "rei-coroa.png")
    print("rei-coroa.png", out.size)


def folha_pontas(ref):
    """O ajuste das pontas da coroa (rei-pontas.png): a referência × a coroa anterior × a ajustada, na caixa da carta em
    tamanho real e a 3×, e a 12× (na ajustada, os pixels mudados em vermelho)."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1400, 400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Rei Troll: as pontas da coroa — a referência × a anterior × a ajustada (proposta, nada no jogo)",
           fill=TEXTO, font=f)
    r = Image.open(ref).convert("RGBA")
    fundo = Image.new("RGBA", r.size, CARVAO); fundo.alpha_composite(r)
    d.text((20, 34), "a referência", fill=TEXTO2, font=f2)
    out.alpha_composite(fundo.resize((192, 192), Image.LANCZOS), (20, 52))
    antes, depois = imagem("rei-troll-ouro"), imagem("rei-troll-ouro2")
    for j, (rot, im) in enumerate((("anterior", antes), ("ajustada", depois))):
        x = 240 + j * 560
        d.text((x, 34), f"{rot}: a carta (tamanho real), a caixa a 3× e a 12×", fill=TEXTO2, font=f2)
        out.alpha_composite(caixa(im), (x, 52)); out.alpha_composite(amplia(caixa(im), 3), (x + 46, 52))
        g = grade12(im)
        if rot == "ajustada":
            dd = ImageDraw.Draw(g)
            for py in range(16):
                for px in range(16):
                    if im.getpixel((px, py)) != antes.getpixel((px, py)):
                        dd.rectangle([px * 12, py * 12, px * 12 + 11, py * 12 + 11], outline=(230, 40, 40, 255))
        out.alpha_composite(g, (x + 170, 52))
    out = out.crop((0, 0, 1400, 52 + 192 + 16))
    out.save(PASTA / "rei-pontas.png")
    print("rei-pontas.png", out.size)


def folha_final_rei_aranha():
    """O Rei Troll e a Aranha no jogo (1.167.0, rei-aranha-final.png): os aprovados × os PNGs de produção; o Rei ao lado
    do Troll comum; a aranha na carta, no Bestiário e no rastro do contrato; a Rainha (no "fera") com as aranhas
    invocadas. Tudo com os arquivos reais (o modo "final", sem troca)."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 1500), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Rei Troll e a Aranha gigante no jogo (1.167.0): o rei-troll-ouro2 e a aranha-2b, sem retoques",
           fill=TEXTO, font=f)
    y = 36
    for j, (aprovado, arq) in enumerate((("rei-troll-ouro2", "retrato-rei-troll"), ("aranha-2b", "retrato-aranha"))):
        a, b = imagem(aprovado), Image.open(JOGO / f"{arq}-16.png").convert("RGBA")
        x = 20 + j * 620
        d.text((x, y), f"{aprovado} (aprovado) | {arq}-16 (no jogo): {'idênticos' if a.tobytes() == b.tobytes() else 'DIFERENTES'}",
               fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(a), (x, y + 18)); out.alpha_composite(grade12(b), (x + 210, y + 18))
    y += 18 + 192 + 20
    rei = abre("rei-final-palco.png")
    d.text((20, y), "o Rei Troll ao lado do Troll comum (a carta a 32 px, tamanho real e 2×)", fill=TEXTO, font=f2)
    y += 20
    for k, nome in enumerate(("Rei Troll", "Troll da montanha")):
        cx = rei.crop(caixa_de("rei", "final", nome))
        out.alpha_composite(cx, (20 + k * 460, y)); out.alpha_composite(amplia(cx, 2), (20 + k * 460, y + cx.height + 6))
    y += 3 * 50 + 20
    d.text((20, y), "a Aranha: a carta (32 px, real e 2×) | o Bestiário (48 px) | o rastro do contrato de caça (32 px, real e 2×)",
           fill=TEXTO, font=f2)
    y += 20
    cx = abre("luta-final-palco.png").crop(caixa_de("luta", "final", "Aranha gigante"))
    cartao = abre("bestiario-final-pagina.png").crop(caixa_de("bestiario", "final", "Aranha gigante"))
    rastro = abre("contrato-final-pagina.png").crop((1505, 480, 1800, 610))
    out.alpha_composite(cx, (20, y)); out.alpha_composite(amplia(cx, 2), (20, y + cx.height + 6))
    out.alpha_composite(cartao, (470, y)); out.alpha_composite(rastro, (840, y)); out.alpha_composite(amplia(rastro, 2), (1150, y))
    y += max(3 * 50 + 6, cartao.height, 2 * rastro.height) + 20
    luta = abre("rainha-final-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "a Rainha Aracnídea (o guardião, continua no \"fera\") com duas aranhas invocadas (o retrato da família) — "
                    "tamanho real", fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    linha = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] + \
        [(n.replace("-", " ").capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")))
         for n in ("afogado", "ilse", "lobo", "bandido", "urso", "falcao", "troll", "rei-troll", "aranha")]
    d.text((20, y), "a fileira dos retratos do jogo, na caixa da carta — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, c2) in enumerate(linha):
        out.alpha_composite(c2, (20 + j * 46, y))
    y += 50
    for j, (rot, c2) in enumerate(linha):
        out.alpha_composite(amplia(c2, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot, fill=TEXTO2, font=f2)
    y += 3 * 38 + 40
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "rei-aranha-final.png")
    print("rei-aranha-final.png", out.size)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["final"]:
        folha_final_rei_aranha()
    elif sys.argv[1:2] == ["pontas"]:
        folha_pontas(sys.argv[2])
    elif sys.argv[1:2] == ["coroa"]:
        folha_coroa(sys.argv[2])
    elif sys.argv[1:] == ["r3"]:
        folha_r3()
    elif sys.argv[1:] == ["troll"]:
        folha_troll_final()
    elif sys.argv[1:] == ["r2"]:
        for chave in CRIATURAS:
            folha_r2(chave)
    else:
        for chave in CRIATURAS:
            folha(chave)
