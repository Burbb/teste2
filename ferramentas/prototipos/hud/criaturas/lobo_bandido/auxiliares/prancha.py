"""As folhas do segundo par, uma por criatura (lobo.png, bandido.png): a carta da luta a 1920×945, atual × A × B, em
tamanho real e a 2×; o Bestiário (a 3×, o tamanho real do cartão) com a vizinha que continua com o desenho do traço; a
luta inteira com o animal do herói (o "fera", que não troca); a fileira na caixa da carta ao lado do Morel, da Odette e do
herói, em tamanho real e a 3×; e a 12× sem suavização, só para achar o pixel.
    python prancha.py
"""
import pathlib

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


if __name__ == "__main__":
    for nome in CRIATURAS:
        folha(nome)
