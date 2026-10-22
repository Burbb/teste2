"""As folhas da Rainha Aracnídea e do Esqueleto (rainha.png, esqueleto.png): a carta a 1920×945, atual × A × B, em tamanho
real e a 2×; a Rainha ao lado da Aranha gigante (a invocada, com o retrato da 1.167.0); o Esqueleto no Bestiário (48 px)
e nos papéis separados (o inimigo, os invocados pelo Lich, o servo aliado do Necromante, o chefe); a fileira com os
retratos aprovados (dos PNGs de produção); e a 12× sem suavização. Os recortes vêm das caixas do registro.
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
REG = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
APROVADOS = ("afogado", "ilse", "lobo", "bandido", "urso", "falcao", "troll", "rei-troll", "aranha")


def abre(n):
    return Image.open(CAP / n).convert("RGBA")


def caixa_de(sit, modo, nome, campo="caixa"):
    return next(c[campo] for c in REG[f"{sit}/{modo}"]["caixas"] if c["nome"] == nome)


def nicho(r):
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


def cartas(out, d, y, f2, sit, nome, rotulos):
    """A carta de `nome` na situação, atual × A × B, em tamanho real e a 2×; devolve o y de baixo."""
    for j, (modo, rot) in enumerate(MODOS):
        cx = abre(f"{sit}-{modo}-palco.png").crop(caixa_de(sit, modo, nome))
        x = 20 + j * 470
        d.text((x, y), rot if modo == "atual" else f"{rot}: {rotulos[modo]}", fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (x, y + 16)); out.alpha_composite(amplia(cx, 2), (x, y + 16 + cx.height + 6))
    return y + 16 + 3 * 50 + 24


def fileira(out, d, y, f2, extras):
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    linha = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] + \
        [(n.replace("-", " ").capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA"))) for n in APROVADOS] + \
        [(rot, caixa(imagem(i))) for i, rot in extras]
    d.text((20, y), "a fileira, na caixa da carta, com os retratos do jogo — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, cx) in enumerate(linha):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(linha):
        out.alpha_composite(amplia(cx, 3), (20 + (j % 13) * 124, y + (j // 13) * 140))
        d.text((20 + (j % 13) * 124, y + (j // 13) * 140 + 118), rot[:18], fill=TEXTO2, font=f2)
    return y + ((len(linha) + 12) // 13) * 140 + 10


def a12(out, d, y, f2, ids):
    d.text((20, y), "A e B a 12× (sem suavização, só para achar o pixel)", fill=TEXTO, font=f2)
    y += 20
    for j, ident in enumerate(ids):
        d.text((20 + j * 230, y), ident, fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(imagem(ident)), (20 + j * 230, y + 16))
    return y + 16 + 192 + 20


def folha_rainha():
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 1800), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "A Rainha Aracnídea — atual × A, de frente e enorme × B, descendo pelo fio; o guardião só aparece na carta "
                     "(32 px); proposta, nada no jogo", fill=TEXTO, font=f)
    y = cartas(out, d, 40, f2, "rainha", "Rainha Aracnídea", {"a": "A, de frente e enorme", "b": "B, descendo pelo fio"})
    d.text((20, y), "ao lado da Aranha gigante do jogo (a invocada, a mesma espécie) — a caixa a 3×: aranha | Rainha A | Rainha B",
           fill=TEXTO, font=f2)
    y += 20
    aranha = abre("rainha-a-palco.png").crop(nicho(caixa_de("rainha", "a", "Aranha gigante A (invocado)", "retrato")))
    for j, cx in enumerate((aranha, caixa(imagem("rainha-a")), caixa(imagem("rainha-b")))):
        out.alpha_composite(amplia(cx, 3), (20 + j * 130, y))
    y += 3 * 38 + 20
    for modo, rot in (("a", "A"), ("b", "B")):
        luta = abre(f"rainha-{modo}-palco.png").crop((30, 30, 1060, 210))
        d.text((20, y), f"a luta com a Rainha {rot} e duas aranhas invocadas (tamanho real)", fill=TEXTO2, font=f2)
        out.alpha_composite(luta, (20, y + 16))
        y += 16 + luta.height + 10
    y = fileira(out, d, y + 10, f2, (("rainha-a", "Rainha A"), ("rainha-b", "Rainha B")))
    y = a12(out, d, y, f2, ("rainha-a", "rainha-b"))
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "rainha.png")
    print("rainha.png", out.size)


def folha_esqueleto():
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Esqueleto — atual × A, de frente × B, em três quartos; a carta (32 px) e o Bestiário (48 px); proposta, "
                     "nada no jogo", fill=TEXTO, font=f)
    y = cartas(out, d, 40, f2, "luta", "Esqueleto", {"a": "A, de frente", "b": "B, em três quartos"})
    d.text((20, y), "o Bestiário (o retrato a 48 px) — tamanho real; à esquerda, o carniçal (outro morto-vivo, continua na caveira)",
           fill=TEXTO, font=f2)
    y += 20
    out.alpha_composite(abre("bestiario-atual-pagina.png").crop(caixa_de("bestiario", "atual", "Carniçal")), (20, y + 16))
    alto = 0
    for j, (modo, rot) in enumerate(MODOS):
        cartao = abre(f"bestiario-{modo}-pagina.png").crop(caixa_de("bestiario", modo, "Esqueleto"))
        d.text((400 + j * 370, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cartao, (400 + j * 370, y + 16))
        alto = max(alto, cartao.height)
    y += 16 + alto + 24
    d.text((20, y), "os papéis, separados (a proposta A nas fotos): o esqueleto inimigo e o carniçal; o servo aliado do Necromante "
                    "(outro papel, fica com o sprite); o Lich Menor (chefe, fica) com dois esqueletos invocados", fill=TEXTO, font=f2)
    y += 20
    for arq in ("luta-a-palco.png", "lich-a-palco.png"):
        luta = abre(arq).crop((30, 30, 1060, 210))
        out.alpha_composite(luta, (20, y))
        y += luta.height + 10
    y = fileira(out, d, y + 10, f2, (("esqueleto-a", "Esqueleto A"), ("esqueleto-b", "Esqueleto B")))
    y = a12(out, d, y, f2, ("esqueleto-a", "esqueleto-b"))
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "esqueleto.png")
    print("esqueleto.png", out.size)


def folha_rainha_final():
    """A Rainha Aracnídea no jogo (1.168.0, rainha-final.png): a aprovada × o PNG de produção; a luta com as aranhas
    invocadas, com os arquivos reais (o modo "final"); a carta a 32 px; a fileira dos retratos do jogo."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 1000), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "A Rainha Aracnídea no jogo (1.168.0): a rainha-a, sem retoques, pelo id da guardiã", fill=TEXTO, font=f)
    a, b = imagem("rainha-a"), Image.open(JOGO / "retrato-rainha-aracnidea-16.png").convert("RGBA")
    d.text((20, 32), f"rainha-a (aprovada) | retrato-rainha-aracnidea-16 (no jogo): {'idênticas' if a.tobytes() == b.tobytes() else 'DIFERENTES'}",
           fill=TEXTO2, font=f2)
    out.alpha_composite(grade12(a), (20, 50)); out.alpha_composite(grade12(b), (230, 50))
    y = 50 + 192 + 20
    d.text((20, y), "a Rainha e uma aranha invocada (o retrato da Aranha gigante) na carta — tamanho real e 2×", fill=TEXTO, font=f2)
    y += 20
    for k, nome in enumerate(("Rainha Aracnídea", "Aranha gigante A (invocado)")):
        cx = abre("rainha-final-palco.png").crop(caixa_de("rainha", "final", nome))
        out.alpha_composite(cx, (20 + k * 460, y)); out.alpha_composite(amplia(cx, 2), (20 + k * 460, y + cx.height + 6))
    y += 3 * 50 + 20
    luta = abre("rainha-final-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "a luta com os arquivos de produção (tamanho real)", fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    linha = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] + \
        [(n.replace("-", " ").capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")))
         for n in APROVADOS + ("rainha-aracnidea",)]
    d.text((20, y), "a fileira dos retratos do jogo, na caixa da carta — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, cx) in enumerate(linha):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(linha):
        out.alpha_composite(amplia(cx, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot[:18], fill=TEXTO2, font=f2)
    y += 3 * 38 + 40
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "rainha-final.png")
    print("rainha-final.png", out.size)


def folha_esqueleto_a2():
    """O Esqueleto A × A2 (esqueleto-a2.png): a referência gerada e a guia; a carta (tamanho real e 2×) e o Bestiário
    (48 px); as lutas com o A2 (o servo, o carniçal e o Lich com o sprite de hoje); a fileira com os retratos do jogo
    (a Rainha da 1.168.0 inclusive); as ampliações inteiras 1×, 2× e 3×; a 12×."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (2020, 2600), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Esqueleto — A (anterior) × A2 (a transposição da referência gerada); proposta, nada no jogo",
           fill=TEXTO, font=f)
    ref = Image.open(AQUI.parents[5] / "ferramentas/arte/referencias/icones/Esqueleto frontal em pixel art.png").convert("RGBA")
    fundo = Image.new("RGBA", ref.size, (0, 0, 0, 255)); fundo.alpha_composite(ref)
    guia = Image.open(PASTA / "guias/esqueleto-guia-16.png").convert("RGBA")
    d.text((20, 32), "a referência (reduzida, só para olhar) | a guia a 16 (oculta na fonte) | A | A2, a 12×", fill=TEXTO2, font=f2)
    out.alpha_composite(fundo.resize((192, 192), Image.LANCZOS), (20, 50))
    out.alpha_composite(grade12(guia), (232, 50))
    out.alpha_composite(grade12(imagem("esqueleto-a")), (444, 50)); out.alpha_composite(grade12(imagem("esqueleto-a2")), (656, 50))
    y = 50 + 192 + 20
    d.text((20, y), "a carta na luta (1920×945), tamanho real e 2×", fill=TEXTO, font=f2)
    y += 18
    for j, (modo, rot) in enumerate((("a", "A"), ("a2", "A2"))):
        cx = abre(f"luta-{modo}-palco.png").crop(caixa_de("luta", modo, "Esqueleto"))
        x = 20 + j * 470
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (x, y + 16)); out.alpha_composite(amplia(cx, 2), (x, y + 16 + cx.height + 6))
    y += 16 + 3 * 50 + 24
    d.text((20, y), "o Bestiário (48 px), tamanho real: A | A2 (o carniçal ao lado continua na caveira)", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, modo in enumerate(("a", "a2")):
        cartao = abre(f"bestiario-{modo}-pagina.png").crop(caixa_de("bestiario", modo, "Esqueleto"))
        out.alpha_composite(cartao, (20 + j * 380, y)); alto = max(alto, cartao.height)
    car = abre("bestiario-a2-pagina.png").crop(caixa_de("bestiario", "a2", "Carniçal"))
    out.alpha_composite(car, (780, y)); alto = max(alto, car.height)
    y += alto + 24
    d.text((20, y), "as lutas com o A2 (tamanho real): o Necromante com o servo aliado (fica com o sprite), dois esqueletos, o "
                    "carniçal e o afogado; o Lich Menor (fica) com dois esqueletos invocados", fill=TEXTO, font=f2)
    y += 18
    for arq in ("luta-a2-palco.png", "lich-a2-palco.png"):
        luta = abre(arq).crop((30, 30, 1060, 210))
        out.alpha_composite(luta, (20, y))
        y += luta.height + 10
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    linha = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272)))] +         [(n.replace("-", " ").capitalize(), caixa(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")))
         for n in APROVADOS + ("rainha-aracnidea",)] +         [("Esqueleto A", caixa(imagem("esqueleto-a"))), ("Esqueleto A2", caixa(imagem("esqueleto-a2")))]
    d.text((20, y + 10), "a fileira, na caixa da carta, com os retratos do jogo — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 30
    for j, (_, cx) in enumerate(linha):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(linha):
        out.alpha_composite(amplia(cx, 3), (20 + (j % 16) * 124, y + (j // 16) * 140))
        d.text((20 + (j % 16) * 124, y + (j // 16) * 140 + 118), rot[:18], fill=TEXTO2, font=f2)
    y += ((len(linha) + 15) // 16) * 140 + 10
    d.text((20, y), "A2 nas ampliações inteiras dos PNGs exportados: 16 (1×) | 32 (2×, a carta) | 48 (3×, o Bestiário)",
           fill=TEXTO, font=f2)
    y += 18
    x = 20
    for lado in (16, 32, 48):
        im = Image.open(PASTA / f"proposta/esqueleto-a2-{lado}.png").convert("RGBA")
        cx = Image.new("RGBA", (lado + 12, lado + 12), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 10, lado + 10))
        cx.alpha_composite(im, (6, 6)); out.alpha_composite(cx, (x, y)); x += lado + 30
    y += 48 + 12 + 20
    out = out.crop((0, 0, 2020, y))
    out.save(PASTA / "esqueleto-a2.png")
    print("esqueleto-a2.png", out.size)


def folha_nariz():
    """O nariz do A2 (esqueleto-a2n.png): a referência × A2 × A2n; a carta (32 px) e o Bestiário (48 px) em tamanho real,
    a mesma caixa ampliada 4× e a 12× com a grade, sem suavização (a referência é a imagem original reduzida)."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1000, 900), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O nariz do Esqueleto A2: referência × A2 (2d7cacb3) × A2n (só as linhas 8 e 9); proposta, nada no jogo",
           fill=TEXTO, font=f)
    ref = Image.open(AQUI.parents[5] / "ferramentas/arte/referencias/icones/Esqueleto frontal em pixel art.png").convert("RGBA")
    fundo = Image.new("RGBA", ref.size, (13, 11, 10, 255)); fundo.alpha_composite(ref)

    def nicho_de(im, lado):
        cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
        cx.alpha_composite(im, (3, 3)); return cx
    colunas = [("referência (reduzida)", lambda lado: fundo.resize((lado, lado), Image.LANCZOS), None),
               ("A2 anterior", lambda lado: amplia(imagem("esqueleto-a2"), lado // 16), "esqueleto-a2"),
               ("A2n, o nariz refeito", lambda lado: amplia(imagem("esqueleto-a2n"), lado // 16), "esqueleto-a2n")]
    y = 40
    for j, (rot, _, _) in enumerate(colunas):
        d.text((20 + j * 320, y), rot, fill=TEXTO2, font=f2)
    y += 18
    d.text((20, y), "tamanho real: a carta (32) e o Bestiário (48)", fill=TEXTO, font=f2)
    for j, (_, im, _) in enumerate(colunas):
        out.alpha_composite(nicho_de(im(32), 32), (20 + j * 320, y + 18)); out.alpha_composite(nicho_de(im(48), 48), (70 + j * 320, y + 18))
    y += 18 + 54 + 16
    d.text((20, y), "as mesmas caixas a 4× (vizinho mais próximo)", fill=TEXTO, font=f2)
    for j, (_, im, _) in enumerate(colunas):
        out.alpha_composite(amplia(nicho_de(im(32), 32), 4), (20 + j * 320, y + 18))
    y += 18 + 38 * 4 + 12
    for j, (_, im, _) in enumerate(colunas):
        out.alpha_composite(amplia(nicho_de(im(48), 48), 4), (20 + j * 320, y))
    y += 54 * 4 + 16
    d.text((20, y), "a 12× com a grade (a referência: a guia de 16 que mediu)", fill=TEXTO, font=f2)
    guia = Image.open(PASTA / "guias/esqueleto-guia-16.png").convert("RGBA")
    for j, (_, _, ident) in enumerate(colunas):
        out.alpha_composite(grade12(imagem(ident) if ident else guia), (20 + j * 320, y + 18))
    y += 18 + 192 + 20
    out = out.crop((0, 0, 1000, y))
    out.save(PASTA / "esqueleto-a2n.png")
    print("esqueleto-a2n.png", out.size)


def folha_sorriso():
    """O sorriso (esqueleto-sorriso.png): A2n × S1 (contido) × S2 (marcado); a carta (32 px) e o Bestiário (48 px) em
    tamanho real, as mesmas caixas a 4× e a 12× com a grade, sem suavização."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1000, 900), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O sorriso do Esqueleto: A2n (ee82b54a) × S1, contido × S2, marcado (só a boca e a mandíbula); proposta, "
                     "nada no jogo", fill=TEXTO, font=f)

    def nicho_de(im, lado):
        cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
        cx.alpha_composite(amplia(im, lado // 16), (3, 3)); return cx
    colunas = (("esqueleto-a2n", "A2n (a base)"), ("esqueleto-s1", "S1, contido"), ("esqueleto-s2", "S2, marcado"))
    y = 40
    for j, (_, rot) in enumerate(colunas):
        d.text((20 + j * 320, y), rot, fill=TEXTO2, font=f2)
    y += 18
    d.text((20, y), "tamanho real: a carta (32) e o Bestiário (48)", fill=TEXTO, font=f2)
    for j, (ident, _) in enumerate(colunas):
        out.alpha_composite(nicho_de(imagem(ident), 32), (20 + j * 320, y + 18))
        out.alpha_composite(nicho_de(imagem(ident), 48), (70 + j * 320, y + 18))
    y += 18 + 54 + 16
    d.text((20, y), "as mesmas caixas a 4× (vizinho mais próximo)", fill=TEXTO, font=f2)
    for j, (ident, _) in enumerate(colunas):
        out.alpha_composite(amplia(nicho_de(imagem(ident), 32), 4), (20 + j * 320, y + 18))
    y += 18 + 38 * 4 + 12
    for j, (ident, _) in enumerate(colunas):
        out.alpha_composite(amplia(nicho_de(imagem(ident), 48), 4), (20 + j * 320, y))
    y += 54 * 4 + 16
    d.text((20, y), "a 12× com a grade", fill=TEXTO, font=f2)
    for j, (ident, _) in enumerate(colunas):
        out.alpha_composite(grade12(imagem(ident)), (20 + j * 320, y + 18))
    y += 18 + 192 + 20
    out = out.crop((0, 0, 1000, y))
    out.save(PASTA / "esqueleto-sorriso.png")
    print("esqueleto-sorriso.png", out.size)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["rainha-final"]:
        folha_rainha_final()
    elif sys.argv[1:] == ["esqueleto-a2"]:
        folha_esqueleto_a2()
    elif sys.argv[1:] == ["esqueleto-a2n"]:
        folha_nariz()
    elif sys.argv[1:] == ["esqueleto-sorriso"]:
        folha_sorriso()
    else:
        folha_rainha()
        folha_esqueleto()
