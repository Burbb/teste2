"""As folhas do segundo par, uma por criatura (lobo.png, bandido.png): a carta da luta a 1920×945, atual × A × B, em
tamanho real e a 2×; o Bestiário (a 3×, o tamanho real do cartão) com a vizinha que continua com o desenho do traço; a
luta inteira com o animal do herói (o "fera", que não troca); a fileira na caixa da carta ao lado do Morel, da Odette e do
herói, em tamanho real e a 3×; e a 12× sem suavização, só para achar o pixel.
    python prancha.py
As folhas da segunda rodada (lobo-r2.png, bandido-r2.png): o Lobo A original × só a base nova × ajustado (a base e o
olhar), com a silhueta numa cor só e os pixels mudados marcados; os três Bandidos novos ao lado do atual e dos A e B da
primeira rodada (o histórico); a carta e o Bestiário a 1920×945, a fileira e a 12×.
    python prancha.py r2
"""
import pathlib
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont

from previa import amplia, imagem

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
MODOS = (("atual", "atual (traço)"), ("a", "proposta A"), ("b", "proposta B"))
# por criatura: o recorte da carta na luta, o do cartão no Bestiário, o da vizinha que não troca e o rótulo das propostas
CRIATURAS = {
    "lobo": dict(carta=(830, 38, 1042, 90), cartao=(945, 413, 1296, 564), vizinha=(585, 248, 936, 399),
                 vizinha_nome="Aranha gigante", a="A, de frente", b="B, de perfil"),
    "bandido": dict(carta=(612, 38, 824, 90), cartao=(945, 248, 1296, 399), vizinha=(585, 413, 936, 564),
                    vizinha_nome="Cultista", a="A, o desertor", b="B, a salteadora"),
}


def abre(n):
    return Image.open(CAP / n).convert("RGBA")


def nicho(nome):
    """A caixa do retrato (38 px) na carta da luta: onde a foto atual e a da proposta A diferem."""
    x0, y0, x1, y1 = CRIATURAS[nome]["carta"]
    a, b = abre("luta-atual-palco.png").crop((x0, y0, x1, y1)), abre("luta-a-palco.png").crop((x0, y0, x1, y1))
    bx = ImageChops.difference(a.convert("RGB"), b.convert("RGB")).getbbox()
    cx, cy = x0 + (bx[0] + bx[2]) // 2, y0 + (bx[1] + bx[3]) // 2
    return (cx - 19, cy - 19, cx + 19, cy + 19)


def grade12(im16):
    g = amplia(im16, 12)
    fundo = Image.new("RGBA", g.size, (24, 21, 19, 255))
    fundo.alpha_composite(g)
    dd = ImageDraw.Draw(fundo)
    for i in range(1, 16):
        dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255)); dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
    return fundo


def folha(nome):
    c = CRIATURAS[nome]
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"Criaturas, segundo par: o {nome.capitalize()} — atual × {c['a']} × {c['b']}; 16×16 a 2× na carta e "
                     "3× no Bestiário; proposta, nada no jogo", fill=TEXTO, font=f)
    y = 44
    # 1. a carta da luta em tamanho real e a 2×
    d.text((20, y), "a carta na luta (1920×945, os mesmos dados) — tamanho real e 2×", fill=TEXTO, font=f2)
    y += 20
    for j, (modo, rot) in enumerate(MODOS):
        carta = abre(f"luta-{modo}-palco.png").crop(c["carta"])
        x = 20 + j * 520
        d.text((x, y), rot if modo == "atual" else f"{rot}: {c[modo]}", fill=TEXTO2, font=f2)
        out.alpha_composite(carta, (x, y + 16)); out.alpha_composite(amplia(carta, 2), (x, y + 16 + carta.height + 8))
    y += 16 + 3 * 52 + 24
    # 2. o Bestiário: o cartão em tamanho real (o retrato a 3×) e a vizinha, que continua com o desenho do traço
    d.text((20, y), f"o Bestiário (o retrato a 3×) — tamanho real; à esquerda, {c['vizinha_nome']}, que continua com o "
                    "desenho do traço", fill=TEXTO, font=f2)
    y += 20
    out.alpha_composite(abre("bestiario-atual-pagina.png").crop(c["vizinha"]), (20, y + 16))
    d.text((20, y), c["vizinha_nome"], fill=TEXTO2, font=f2)
    for j, (modo, rot) in enumerate(MODOS):
        x = 400 + j * 370
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(abre(f"bestiario-{modo}-pagina.png").crop(c["cartao"]), (x, y + 16))
    y += 16 + 151 + 24
    # 3. a fileira na caixa da carta: Morel, Odette, o herói (o patrulheiro da foto) e o atual, A e B
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    caixa_nicho = nicho(nome)
    caixas = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272))),
              ("o herói", abre("luta-atual-palco.png").crop((46, 54, 84, 92)))] + \
        [(rot, abre(f"luta-{modo}-palco.png").crop(caixa_nicho)) for modo, rot in MODOS]
    d.text((20, y), "a fileira, na mesma caixa da carta (as do jogo e as das fotos) — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (rot, cx) in enumerate(caixas):
        out.alpha_composite(cx, (20 + j * 46, y))
        out.alpha_composite(amplia(cx, 3), (360 + j * 124, y))
        d.text((360 + j * 124, y + 118), rot, fill=TEXTO2, font=f2)
    y += 3 * 38 + 40
    # 4. a luta inteira em tamanho real (as cartas inimigas e o animal do herói)
    d.text((20, y), "a luta inteira (tamanho real): o Lobo Cinzento do herói e a aranha continuam no \"fera\"; o cultista no "
                    "\"humano\"", fill=TEXTO, font=f2)
    y += 20
    for j, (modo, rot) in enumerate(MODOS):
        luta = abre(f"luta-{modo}-palco.png").crop((30, 30, 1050, 210))
        d.text((20, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(luta, (20, y + 16))
        y += 16 + luta.height + 10
    y += 14
    # 5. a 12×
    d.text((20, y), "A e B a 12× (sem suavização, só para achar o pixel)", fill=TEXTO, font=f2)
    y += 20
    for j, ident in enumerate((f"{nome}-a", f"{nome}-b")):
        d.text((20 + j * 230, y), ident, fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(imagem(ident)), (20 + j * 230, y + 16))
    y += 16 + 192 + 20
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / f"{nome}.png")
    print(f"{nome}.png", out.size)


def silhueta(im16):
    """A figura numa cor só (a forma, sem a luz), a 6×."""
    sil = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            if im16.getpixel((x, y))[3]:
                sil.putpixel((x, y), (190, 186, 176, 255))
    return amplia(sil, 6)


def caixa(im16):
    """A caixa escura da carta (38 px) com a cabeça a 2×."""
    cx = Image.new("RGBA", (38, 38), (42, 36, 32, 255))
    cx.paste((13, 11, 10, 255), (2, 2, 36, 36))
    cx.alpha_composite(amplia(im16, 2), (3, 3))
    return cx


def fileira_modos(out, d, y, f2, modos, recorte, arquivo):
    """Uma fileira de recortes das fotos, um por modo, com o rótulo em cima; devolve o y de baixo."""
    alto = 0
    for j, (modo, rot) in enumerate(modos):
        im = abre(arquivo.format(modo=modo)).crop(recorte)
        x = 20 + j * (im.width + 20)
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(im, (x, y + 16))
        alto = im.height
    return y + 16 + alto + 16


def cartas_2x(out, y, modos, recorte):
    """As cartas da luta a 2×, duas por linha; devolve o y de baixo."""
    for j, (modo, _) in enumerate(modos):
        im = amplia(abre(f"luta-{modo}-palco.png").crop(recorte), 2)
        out.alpha_composite(im, (20 + (j % 2) * (im.width + 20), y + (j // 2) * (im.height + 12)))
    return y + ((len(modos) + 1) // 2) * (2 * (recorte[3] - recorte[1]) + 12) + 16


def fileira_caixas(out, d, y, f2, caixas):
    """As caixas em tamanho real numa linha e a 3× na de baixo, com o rótulo; devolve o y de baixo."""
    for j, (_, cx) in enumerate(caixas):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(caixas):
        out.alpha_composite(amplia(cx, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot, fill=TEXTO2, font=f2)
    return y + 3 * 38 + 40


def comitiva():
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    return [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272))),
            ("o herói", abre("luta-atual-palco.png").crop((46, 54, 84, 92)))]


def folha_lobo_r2():
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2200), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Lobo, segunda rodada: a cabeça A preservada; embaixo, o começo do pescoço de um quadrúpede no lugar do "
                     "busto — proposta, nada no jogo", fill=TEXTO, font=f)
    y = 44
    versoes = (("lobo-a", "A original (a primeira rodada)"), ("lobo-a-base", "só a base nova"),
               ("lobo-a-ajustado", "ajustado: a base, o olhar e o focinho"))
    d.text((20, y), "a silhueta numa cor só (6×); 1×, a carta (2×) e a 12× com os pixels diferentes do original em vermelho",
           fill=TEXTO, font=f2)
    y += 20
    orig = imagem("lobo-a")
    for j, (ident, rot) in enumerate(versoes):
        x = 20 + j * 330
        im = imagem(ident)
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(silhueta(im), (x, y + 16))
        g = grade12(im)
        dd = ImageDraw.Draw(g)
        for py in range(16):
            for px in range(16):
                if im.getpixel((px, py)) != orig.getpixel((px, py)):
                    dd.rectangle([px * 12, py * 12, px * 12 + 11, py * 12 + 11], outline=(220, 40, 40, 255))
        out.alpha_composite(im, (x + 110, y + 16)); out.alpha_composite(caixa(im), (x + 140, y + 16))
        out.alpha_composite(g, (x + 100, y + 16 + 96 + 10))
    y += 16 + 96 + 10 + 192 + 20
    modos = (("atual", "atual (traço)"), ("a", "A original"), ("r2-base", "só a base"), ("r2-brutamontes", "ajustado"))
    d.text((20, y), "a carta na luta a 1920×945 (os mesmos dados) — tamanho real", fill=TEXTO, font=f2)
    y = fileira_modos(out, d, y + 20, f2, modos, CRIATURAS["lobo"]["carta"], "luta-{modo}-palco.png")
    d.text((20, y), "a carta a 2×", fill=TEXTO, font=f2)
    y = cartas_2x(out, y + 20, modos, CRIATURAS["lobo"]["carta"])
    d.text((20, y), "o Bestiário (o retrato a 3×) — tamanho real", fill=TEXTO, font=f2)
    y = fileira_modos(out, d, y + 20, f2, modos, CRIATURAS["lobo"]["cartao"], "bestiario-{modo}-pagina.png")
    nic = nicho("lobo")
    caixas = comitiva() + [(rot, abre(f"luta-{modo}-palco.png").crop(nic)) for modo, rot in modos]
    d.text((20, y), "a fileira, na caixa da carta, com os retratos aprovados — tamanho real e 3×", fill=TEXTO, font=f2)
    y = fileira_caixas(out, d, y + 20, f2, caixas)
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "lobo-r2.png")
    print("lobo-r2.png", out.size)


def folha_bandido_r2():
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Bandido, segunda rodada: três direções novas (o brutamontes, o do chapéu, o da faca); o A e o B da "
                     "primeira ficam como histórico — proposta, nada no jogo", fill=TEXTO, font=f)
    y = 44
    novos = (("bandido-brutamontes", "1, o brutamontes"), ("bandido-chapeu", "2, o do chapéu"), ("bandido-faca", "3, o da faca"))
    d.text((20, y), "os três novos: 1×, a carta (2×), a caixa a 3× e a 12×", fill=TEXTO, font=f2)
    y += 20
    for j, (ident, rot) in enumerate(novos):
        x = 20 + j * 420
        im = imagem(ident)
        d.text((x, y), rot, fill=TEXTO, font=f2)
        out.alpha_composite(im, (x, y + 20)); out.alpha_composite(caixa(im), (x + 24, y + 20))
        out.alpha_composite(amplia(caixa(im), 3), (x + 70, y + 20)); out.alpha_composite(grade12(imagem(ident)), (x + 200, y + 20))
    y += 20 + 192 + 20
    modos = (("atual", "atual (traço)"), ("r2-brutamontes", "1, o brutamontes"), ("r2-chapeu", "2, o do chapéu"),
             ("r2-faca", "3, o da faca"))
    d.text((20, y), "a carta na luta a 1920×945 (os mesmos dados) — tamanho real", fill=TEXTO, font=f2)
    y = fileira_modos(out, d, y + 20, f2, modos, CRIATURAS["bandido"]["carta"], "luta-{modo}-palco.png")
    d.text((20, y), "a carta a 2×", fill=TEXTO, font=f2)
    y = cartas_2x(out, y + 20, modos, CRIATURAS["bandido"]["carta"])
    d.text((20, y), "o Bestiário (o retrato a 3×) — tamanho real", fill=TEXTO, font=f2)
    y = fileira_modos(out, d, y + 20, f2, modos, CRIATURAS["bandido"]["cartao"], "bestiario-{modo}-pagina.png")
    nic = nicho("bandido")
    caixas = comitiva() + [("A (histórico)", abre("luta-a-palco.png").crop(nic)),
                           ("B (histórico)", abre("luta-b-palco.png").crop(nic))] + \
        [(rot, abre(f"luta-{modo}-palco.png").crop(nic)) for modo, rot in modos]
    d.text((20, y), "a fileira, na caixa da carta, com os retratos aprovados e o histórico — tamanho real e 3×", fill=TEXTO,
           font=f2)
    y = fileira_caixas(out, d, y + 20, f2, caixas)
    luta = abre("luta-r2-faca-palco.png").crop((30, 30, 1050, 210))
    d.text((20, y), "a luta inteira com o 3 e o Lobo ajustado (tamanho real): o cultista continua no \"humano\", a aranha e o "
                    "Lobo Cinzento no \"fera\"", fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "bandido-r2.png")
    print("bandido-r2.png", out.size)


def folha_limpeza():
    """O Lobo "só a base" (antes) × o do jogo (depois, sem as três sobras soltas): sobre o fundo da carta e sobre um
    magenta, a 2×, 3× e 12×, com os pixels removidos marcados."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    antes = imagem("lobo-a-base")
    depois = Image.open(AQUI.parents[5] / "rpg/web/static/hud/icones/retrato-lobo-16.png").convert("RGBA")
    tirados = [(x, y) for y in range(16) for x in range(16) if antes.getpixel((x, y)) != depois.getpixel((x, y))]
    out = Image.new("RGBA", (1100, 640), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Lobo: a limpeza localizada (as sobras apontadas pelo Jean) — antes (\"só a base\", ef15d91d) × depois "
                     "(no jogo)", fill=TEXTO, font=f)
    d.text((20, 30), "removidos: " + ", ".join(f"({x},{y})" for x, y in tirados) + "; o resto igual pixel a pixel",
           fill=TEXTO2, font=f2)
    y = 56
    for fundo, rot in (((13, 11, 10, 255), "sobre o fundo da carta"), ((200, 40, 170, 255), "sobre magenta (contraste)")):
        d.text((20, y), rot, fill=TEXTO, font=f2)
        for j, (im, nome) in enumerate(((antes, "antes"), (depois, "depois"))):
            x = 20 + j * 520
            d.text((x, y + 16), nome, fill=TEXTO2, font=f2)
            for k, z in enumerate((2, 3)):
                q = Image.new("RGBA", (16 * z + 8, 16 * z + 8), fundo)
                q.alpha_composite(amplia(im, z), (4, 4))
                out.alpha_composite(q, (x + k * 50, y + 34))
            g = Image.new("RGBA", (192, 192), fundo)
            g.alpha_composite(amplia(im, 12))
            dd = ImageDraw.Draw(g)
            for px, py in tirados:
                dd.rectangle([px * 12, py * 12, px * 12 + 11, py * 12 + 11], outline=(255, 255, 255, 255) if fundo[0] > 100
                             else (230, 40, 40, 255))
            out.alpha_composite(g, (x + 120, y + 34))
        y += 34 + 192 + 30
    out = out.crop((0, 0, 1100, y))
    out.save(PASTA / "lobo-limpeza.png")
    print("lobo-limpeza.png", out.size, tirados)


def folha_final():
    """A integração (1.163.0, o modo "final" das fotos, o jogo sem troca): os PNGs do jogo × os aprovados, a fileira com
    os vizinhos que continuam no traço, a luta, o Bestiário e o rastro do contrato a 1920×945."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    jogo = AQUI.parents[5] / "rpg/web/static/hud/icones"
    out = Image.new("RGBA", (1800, 2000), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Lobo e o Bandido no jogo (1.163.0): o Lobo \"só a base\" sem as três sobras, o Bandido da faca sem "
                     "retoques", fill=TEXTO, font=f)
    y = 44
    for j, (aprovado, arq, rot) in enumerate((("lobo-a-base", "retrato-lobo-16.png", "Lobo: aprovado (só a base) | no jogo"),
                                              ("bandido-faca", "retrato-bandido-16.png", "Bandido: aprovado (o da faca) | no jogo"))):
        x = 20 + j * 600
        a, b = imagem(aprovado), Image.open(jogo / arq).convert("RGBA")
        dif = [(px, py) for py in range(16) for px in range(16) if a.getpixel((px, py)) != b.getpixel((px, py))]
        d.text((x, y), rot, fill=TEXTO, font=f2)
        d.text((x, y + 16), "idêntico" if not dif else "diferentes (as sobras removidas): " +
               ", ".join(f"({px},{py})" for px, py in dif), fill=TEXTO2, font=f2)
        for k, im in enumerate((a, b)):
            out.alpha_composite(caixa(im), (x + k * 250, y + 36))
            out.alpha_composite(grade12(im), (x + k * 250 + 46, y + 36))
    y += 36 + 192 + 20
    luta = "luta-final-palco.png"
    vizinhos = [("Lobo Cinzento (fera)", (52, 147, 90, 185))]
    caixas = comitiva() + [(rot, abre(luta).crop(r)) for rot, r in vizinhos] + \
        [("aranha (fera)", abre(luta).crop(nicho_abaixo("lobo"))),
         ("cultista (humano)", abre(luta).crop(nicho_abaixo("bandido"))),
         ("Lobo", abre(luta).crop(nicho("lobo"))), ("Bandido", abre(luta).crop(nicho("bandido")))]
    d.text((20, y), "a fileira: os retratos aprovados, os vizinhos que continuam no traço e os novos — tamanho real e 3×",
           fill=TEXTO, font=f2)
    y = fileira_caixas(out, d, y + 20, f2, caixas)
    c = abre(luta).crop((30, 30, 1050, 210))
    d.text((20, y), "a luta a 1920×945 — tamanho real", fill=TEXTO, font=f2)
    out.alpha_composite(c, (20, y + 18))
    y += 18 + c.height + 16
    c = abre(luta).crop((600, 30, 1050, 210))
    d.text((20, y), "as cartas inimigas a 2×", fill=TEXTO, font=f2)
    out.alpha_composite(amplia(c, 2), (20, y + 18))
    y += 18 + 2 * c.height + 16
    b = abre("bestiario-final-pagina.png").crop((585, 248, 1296, 564))
    k = abre("contrato-final-pagina.png").crop((1505, 490, 1800, 600))
    d.text((20, y), "o Bestiário (tamanho real) | o rastro do contrato de caça de bandidos (tamanho real e 2×)", fill=TEXTO, font=f2)
    out.alpha_composite(b, (20, y + 18)); out.alpha_composite(k, (760, y + 18)); out.alpha_composite(amplia(k, 2), (1080, y + 18))
    y += 18 + b.height + 16
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "lobo-bandido-final.png")
    print("lobo-bandido-final.png", out.size)


def nicho_abaixo(nome):
    """A caixa do retrato da carta logo abaixo da de `nome` (a terceira fileira da luta: a aranha sob o lobo, o cultista
    sob o bandido): o mesmo nicho, 116 px mais baixo (duas cartas)."""
    x0, y0, x1, y1 = nicho(nome)
    return (x0, y0 + 116, x1, y1 + 116)


if __name__ == "__main__" and sys.argv[1:] == ["final"]:
    folha_final()
elif __name__ == "__main__" and sys.argv[1:] == ["limpeza"]:
    folha_limpeza()
elif __name__ == "__main__" and sys.argv[1:] == ["r2"]:
    folha_lobo_r2()
    folha_bandido_r2()
elif __name__ == "__main__":
    for nome in CRIATURAS:
        folha(nome)
