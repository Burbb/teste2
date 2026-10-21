"""A folha do primeiro par (afogado-ilse.png): as cartas na luta a 1920×945, atual (o retrato do traço) × proposta, em
tamanho real e a 2×; o Afogado no Bestiário (a 3×); a Ilse com a cena dela no mesmo quadro; as duas cabeças ao lado das
cartas aprovadas da comitiva (a mesma caixa); e a 12× com a grade, só para achar o pixel.
    python prancha.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

from previa import amplia, imagem

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)


def abre(n):
    return Image.open(CAP / n).convert("RGBA")


if __name__ == "__main__":
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
