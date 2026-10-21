"""A folha do primeiro par (afogado-ilse.png): as cartas na luta a 1920×945, atual (o retrato do traço) × proposta, em
tamanho real e a 2×; o Afogado no Bestiário (a 3×); a Ilse com a cena dela no mesmo quadro; as duas cabeças ao lado das
cartas aprovadas da comitiva (a mesma caixa); e a 12× com a grade, só para achar o pixel.
    python prancha.py
A folha da segunda rodada (afogado-ilse-r2.png): a Ilse da primeira proposta × a ajustada (os fios de alga soltos),
junto da arte da cena; o Afogado da primeira proposta × a alternativa B; as duas na carta (a 2×) e na caixa a 3× (a do
Bestiário e do mural), ao lado das cartas aprovadas da comitiva; a luta e o Bestiário a 1920×945, com os mesmos dados.
    python prancha.py r2
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

from previa import amplia, imagem

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)


def abre(n):
    return Image.open(CAP / n).convert("RGBA")


def caixa(im16, z):
    """A caixa escura da carta (36 px a 2×), com a borda; a 3× sai 54 px, a mesma conta."""
    cx = Image.new("RGBA", (38, 38), (42, 36, 32, 255))
    cx.paste((13, 11, 10, 255), (2, 2, 36, 36))
    cx.alpha_composite(amplia(im16, 2), (3, 3))
    return amplia(cx, z)


def folha_r2():
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2600), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Criaturas, segunda rodada: a Ilse com os fios de alga soltos e o Afogado B — primeira proposta × "
                     "ajuste; nada no jogo", fill=TEXTO, font=f)
    y = 44
    # 1. a Ilse com a cena dela: a figura da cena ampliada a 3× e as duas cabeças a 1×, 2× (a carta) e 3×
    cena = Image.open(PASTA.parent / "capturas/capela-fundo-pagina.png").convert("RGBA").crop((930, 175, 1010, 275))
    d.text((20, y), "a Ilse da cena (3×) | primeira proposta | ajustada — 1×, a carta (2×) e a caixa a 3×; ampliações sem "
                    "suavização", fill=TEXTO, font=f2)
    y += 20
    out.alpha_composite(amplia(cena, 3), (20, y))
    for j, ident in enumerate(("ilse", "ilse-r2")):
        x = 300 + j * 300
        d.text((x, y), ("primeira proposta" if j == 0 else "ajustada (r2)"), fill=TEXTO2, font=f2)
        out.alpha_composite(imagem(ident), (x, y + 24))
        out.alpha_composite(caixa(imagem(ident), 1), (x + 30, y + 24))
        out.alpha_composite(caixa(imagem(ident), 3), (x + 80, y + 24))
        out.alpha_composite(amplia(imagem(ident), 6), (x + 80, y + 150))
    y += 300 + 16
    # 2. o Afogado: primeira proposta × B, do mesmo jeito
    d.text((20, y), "o Afogado: primeira proposta | alternativa B — 1×, a carta (2×), a caixa a 3× e a 6×", fill=TEXTO, font=f2)
    y += 20
    for j, ident in enumerate(("afogado", "afogado-b")):
        x = 20 + j * 300
        d.text((x, y), ("primeira proposta" if j == 0 else "alternativa B"), fill=TEXTO2, font=f2)
        out.alpha_composite(imagem(ident), (x, y + 24))
        out.alpha_composite(caixa(imagem(ident), 1), (x + 30, y + 24))
        out.alpha_composite(caixa(imagem(ident), 3), (x + 80, y + 24))
        out.alpha_composite(amplia(imagem(ident), 6), (x + 80, y + 150))
    y += 300 + 16
    # 3. na mesma caixa da comitiva aprovada, tamanho real e 3×
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    d.text((20, y), "na mesma caixa: Morel e Odette aprovados | Afogado (1ª, B) | Ilse (1ª, r2) — tamanho real e 3×",
           fill=TEXTO, font=f2)
    y += 20
    caixas = [ali.crop((46, 176, 84, 214)), ali.crop((46, 234, 84, 272))] + [caixa(imagem(i), 1) for i in
                                                                              ("afogado", "afogado-b", "ilse", "ilse-r2")]
    for j, cx in enumerate(caixas):
        out.alpha_composite(cx, (20 + j * 46, y))
        out.alpha_composite(amplia(cx, 3), (320 + j * 124, y))
    y += 3 * 38 + 24
    # 4. a luta e o Bestiário a 1920×945, tamanho real e 2×
    for rot, n in (("primeira proposta", "afogado-luta-proposta-palco.png"), ("alternativa B", "afogado-luta-r2-palco.png")):
        c = abre(n).crop((600, 40, 1060, 210))
        d.text((20, y), f"Afogado na luta ({rot}) — tamanho real e 2×", fill=TEXTO, font=f2)
        out.alpha_composite(c, (20, y + 18)); out.alpha_composite(amplia(c, 2), (500, y + 18))
        y += 18 + 2 * c.height + 16
    for rot, n in (("primeira proposta", "afogado-bestiario-proposta-pagina.png"), ("alternativa B", "afogado-bestiario-r2-pagina.png")):
        c = abre(n).crop((585, 248, 1296, 404))
        d.text((20, y), f"Bestiário ({rot}) — tamanho real", fill=TEXTO, font=f2)
        out.alpha_composite(c, (20, y + 18))
        y += 18 + c.height + 12
    for rot, n in (("primeira proposta", "ilse-luta-proposta-palco.png"), ("ajustada", "ilse-luta-r2-palco.png")):
        c = abre(n).crop((0, 0, 1088, 230))
        carta = abre(n).crop((826, 92, 1030, 150))
        d.text((20, y), f"Ilse na luta, a cena e a carta ({rot}) — tamanho real; a carta a 3×", fill=TEXTO, font=f2)
        out.alpha_composite(c, (20, y + 18)); out.alpha_composite(amplia(carta, 3), (1130, y + 18))
        y += 18 + c.height + 16
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "afogado-ilse-r2.png")
    print("afogado-ilse-r2.png", out.size)


if __name__ == "__main__" and sys.argv[1:] == ["r2"]:
    folha_r2()
elif __name__ == "__main__":
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Criaturas, primeiro par: Afogado e a carta da Ilse — 16×16 a 2× na carta (32 px), 3× no Bestiário; "
                     "proposta, nada no jogo", fill=TEXTO, font=f)
    y = 44
    # 1. o Afogado na luta (com o esqueleto, que continua a caveira, e a sanguessuga)
    for rot, n in (("atual", "afogado-luta-atual-palco.png"), ("proposta", "afogado-luta-proposta-palco.png")):
        c = abre(n).crop((600, 40, 1060, 210))
        d.text((20, y), f"Afogado na luta ({rot}) — tamanho real e 2×", fill=TEXTO, font=f2)
        out.alpha_composite(c, (20, y + 18)); out.alpha_composite(amplia(c, 2), (500, y + 18))
        y += 18 + 2 * c.height + 16
    # 2. o Bestiário
    for rot, n in (("atual", "afogado-bestiario-atual-pagina.png"), ("proposta", "afogado-bestiario-proposta-pagina.png")):
        c = abre(n).crop((585, 248, 1296, 404))
        d.text((20, y), f"Bestiário ({rot}) — tamanho real", fill=TEXTO, font=f2)
        out.alpha_composite(c, (20, y + 18))
        y += 18 + c.height + 12
    # 3. a Ilse na luta do fundo da capela: a cena e a carta
    for rot, n in (("atual", "ilse-luta-atual-palco.png"), ("proposta", "ilse-luta-proposta-palco.png")):
        c = abre(n).crop((0, 0, 1088, 230))
        carta = abre(n).crop((826, 92, 1030, 150))
        d.text((20, y), f"Ilse na luta, a cena e a carta ({rot}) — tamanho real; a carta a 3×", fill=TEXTO, font=f2)
        out.alpha_composite(c, (20, y + 18)); out.alpha_composite(amplia(carta, 3), (1130, y + 18))
        y += 18 + c.height + 16
    # 4. as cabeças ao lado das cartas aprovadas da comitiva, na mesma caixa
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    d.text((20, y), "na mesma caixa (36 px): Morel e Odette aprovados | Afogado e Ilse propostos — tamanho real e 3×",
           fill=TEXTO, font=f2)
    y += 20
    caixas = [ali.crop((46, 176, 84, 214)), ali.crop((46, 234, 84, 272))]
    for ident in ("afogado", "ilse"):
        cx = Image.new("RGBA", (38, 38), (42, 36, 32, 255))
        cx.paste((13, 11, 10, 255), (2, 2, 36, 36))
        cx.alpha_composite(amplia(imagem(ident), 2), (3, 3))
        caixas.append(cx)
    for j, cx in enumerate(caixas):
        out.alpha_composite(cx, (20 + j * 50, y))
        out.alpha_composite(amplia(cx, 3), (260 + j * 130, y))
    y += 3 * 38 + 24
    # 5. a 12×
    for j, ident in enumerate(("afogado", "ilse")):
        g = amplia(imagem(ident), 12)
        fundo = Image.new("RGBA", g.size, (24, 21, 19, 255))
        fundo.alpha_composite(g)
        dd = ImageDraw.Draw(fundo)
        for i in range(1, 16):
            dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255)); dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
        d.text((20 + j * 220, y), f"{ident} (12×)", fill=TEXTO2, font=f2)
        out.alpha_composite(fundo, (20 + j * 220, y + 18))
    y += 18 + 192 + 20
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "afogado-ilse.png")
    print("afogado-ilse.png", out.size)
