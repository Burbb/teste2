"""A folha de um par (par<n>.png): para cada criatura, a carta na luta a 1920×945 (atual × A × B, os mesmos dados; as
propostas trocadas só na página: protótipo), em tamanho real e a 2×; o cartão do Bestiário (48 px); a fileira, na caixa
da carta, com retratos aprovados; e a 12× com a grade, sem suavização.
    python prancha.py <n>
"""
import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

import grades as gr

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
JOGO = AQUI.parents[5] / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
# o par: (título, [(nome na carta, id das propostas, rótulo A, rótulo B)], retratos aprovados para a fileira)
PARES = {
    1: ("Par 1, o pântano: o sapo-touro gigante e a sanguessuga gigante",
        [("Sapo-touro gigante", "sapo", "A, de frente (a cabeçorra)", "B, de perfil (o papo)"),
         ("Sanguessuga gigante", "sanguessuga", "A, empinada (a ventosa)", "B, em curva"),],
        ("afogado", "lobo", "troll", "aranha")),
    2: ("Par 2, os conjuradores humanos: o cultista e a bruxa do pântano",
        [("Cultista", "cultista", "A, encapuzado (a marca da Fenda)", "B, sem capuz (a cicatriz ritual)"),
         ("Bruxa do pântano", "bruxa", "A, a velha do chapéu", "B, encapuzada com o frasco")],
        ("bandido", "ilse", "afogado", "troll")),
    3: ("Par 3, os mortos-vivos: o carniçal e o espectro",
        [("Carniçal", "carnical", "A, de frente (a mandíbula)", "B, de perfil (mordendo)"),
         ("Espectro", "espectro", "A, o capuz de névoa", "B, o grito")],
        ("afogado", "ilse", "lobo", "bandido")),
    4: ("Par 4, as feras comuns: o javali selvagem e o rato gigante",
        [("Javali selvagem", "javali", "A, de frente (a investida)", "B, de perfil"),
         ("Rato gigante", "rato", "A, de perto (os dentes)", "B, o corpo agachado")],
        ("lobo", "urso", "aranha", "troll")),
}


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


def nicho(im16, lado):
    cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
    cx.alpha_composite(amplia(im16, lado // 16), (3, 3))
    return cx


def grade12(im16):
    g = amplia(im16, 12)
    fundo = Image.new("RGBA", g.size, (24, 21, 19, 255)); fundo.alpha_composite(g)
    dd = ImageDraw.Draw(fundo)
    for i in range(1, 16):
        dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255)); dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
    return fundo


def folha(n):
    titulo, bichos, aprovados = PARES[n]
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    caixa_de = lambda sit, modo, nome: next(c["caixa"] for c in reg[f"par{n}/{sit}/{modo}"]["caixas"] if c["nome"].startswith(nome))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1600, 2600), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{titulo} — proposta, nada no jogo; as propostas trocadas só na página (protótipo), os mesmos dados", fill=TEXTO, font=f)
    y = 40
    for nome, ident, ra, rb in bichos:
        d.text((20, y), f"{nome}: a carta na luta (1920×945) — atual | {ra} | {rb}; tamanho real e 2×", fill=TEXTO, font=f2)
        y += 18
        for j, (modo, rot) in enumerate((("atual", "atual (o traço)"), ("a", ra), ("b", rb))):
            cx = Image.open(CAP / f"par{n}-luta-{modo}.png").convert("RGBA").crop(caixa_de("luta", modo, nome))
            x = 20 + j * 470
            d.text((x, y), rot, fill=TEXTO2, font=f2)
            out.alpha_composite(cx, (x, y + 16)); out.alpha_composite(amplia(cx, 2), (x, y + 16 + cx.height + 6))
        y += 16 + 3 * 50 + 24
        d.text((20, y), f"{nome}: o Bestiário (48 px), tamanho real — atual | A | B", fill=TEXTO, font=f2)
        y += 18
        alto = 0
        for j, modo in enumerate(("atual", "a", "b")):
            ct = Image.open(CAP / f"par{n}-bestiario-{modo}.png").convert("RGBA").crop(caixa_de("bestiario", modo, nome.split()[0]))
            out.alpha_composite(ct, (20 + j * 380, y)); alto = max(alto, ct.height)
        y += alto + 20
    d.text((20, y), "a fileira, na caixa da carta, com retratos aprovados do jogo — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    linha = [(a, Image.open(JOGO / f"retrato-{a}-16.png").convert("RGBA")) for a in aprovados] + \
        [(f"{ident}-{m}", gr.imagem(f"{ident}-{m}")) for _, ident, _, _ in bichos for m in "ab"]
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(nicho(im, 32), (20 + j * 44, y))
    y += 48
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(amplia(nicho(im, 32), 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 116), rot, fill=TEXTO2, font=f2)
    y += 140
    d.text((20, y), "as propostas a 12× com a grade (para achar o pixel)", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, im) in enumerate(linha[len(aprovados):]):
        d.text((20 + j * 220, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(im), (20 + j * 220, y + 16))
    y += 16 + 192 + 20
    out = out.crop((0, 0, 1600, y))
    out.save(PASTA / f"par{n}.png")
    print(f"par{n}.png", out.size)


if __name__ == "__main__":
    folha(int(sys.argv[1]))
