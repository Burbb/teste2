"""As folhas por criatura da segunda rodada (<criatura>.png): a carta na luta a 1920×945 (o jogo × a base escolhida no
primeiro lote × os candidatos desta rodada; trocados só na página: protótipo), em tamanho real e a 2×; o cartão do
Bestiário; a fileira, na caixa da carta, com retratos integrados; e a 12× com a grade, sem suavização.
    python prancha.py [<criatura> ...]
"""
import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

import grades as gr

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
BASES = AQUI.parents[1] / "quatro_pares/proposta"
JOGO = AQUI.parents[5] / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
# a criatura: o nome na carta, a base (quatro_pares), os candidatos [(id, rótulo, modo da foto)], os retratos da fileira
CRIATURAS = {
    "cultista": ("Cultista", "cultista-a", [("cultista-c1", "c1, o capuz pontudo", "v1"), ("cultista-c2", "c2, o capuz largo", "v2"),
                                            ("cultista-c3", "c3, o capuz que avança", "v3")], ("bandido", "afogado", "ilse")),
    "bruxa": ("Bruxa do pântano", "bruxa-a", [("bruxa-b1", "b1, o nariz adunco", "v1"), ("bruxa-b2", "b2, o olho leitoso", "v2"),
                                              ("bruxa-b3", "b3, o sorriso banguela", "v3")], ("bandido", "ilse", "afogado")),
    "carnical": ("Carniçal", "carnical-a", [("carnical-a2", "A2, a boca refeita", "v1")], ("afogado", "lobo", "bandido")),
    "espectro": ("Espectro", "espectro-a", [("espectro-a2", "A2, o olho na cavidade", "v1")], ("afogado", "ilse", "lobo")),
    "javali": ("Javali selvagem", "javali-a", [("javali-a2", "A2, as presas grandes", "v1")], ("troll", "rei-troll", "lobo")),
    "rato": ("Rato gigante", "rato-a", [("rato-r1", "r1, de perfil farejando", "v1"), ("rato-r2", "r2, de frente, a cabeça baixa", "v2"),
                                        ("rato-r3", "r3, sibilando", "v3")], ("lobo", "urso", "aranha")),
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


def folha(chave):
    nome, base, cands, aprovados = CRIATURAS[chave]
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    caixa_de = lambda sit, modo: next(c["caixa"] for c in reg[f"{sit}/{modo}"]["caixas"] if c["nome"].startswith(nome.split()[0]))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (2400, 1600), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{nome}, segunda rodada — proposta, nada no jogo; as propostas trocadas só na página (protótipo), os mesmos dados",
           fill=TEXTO, font=f)
    colunas = [("atual (o jogo)", "atual"), (f"base: {base}", "base")] + [(f"{rot} ({i})", modo) for i, rot, modo in cands]
    y = 40
    d.text((20, y), "a carta na luta (1920×945), tamanho real e 2×", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, modo) in enumerate(colunas):
        cx = Image.open(CAP / f"luta-{modo}.png").convert("RGBA").crop(caixa_de("luta", modo))
        x = 20 + j * 440
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (x, y + 16)); out.alpha_composite(amplia(cx, 2), (x, y + 16 + cx.height + 6))
    y += 16 + 3 * 50 + 24
    d.text((20, y), "o Bestiário (48 px), tamanho real", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (rot, modo) in enumerate(colunas):
        ct = Image.open(CAP / f"bestiario-{modo}.png").convert("RGBA").crop(caixa_de("bestiario", modo))
        out.alpha_composite(ct, (20 + j * 380, y)); alto = max(alto, ct.height)
    y += alto + 20
    linha = [(a, Image.open(JOGO / f"retrato-{a}-16.png").convert("RGBA")) for a in aprovados] + \
        [(base, Image.open(BASES / f"{base}-16.png").convert("RGBA"))] + [(i, gr.imagem(i)) for i, _, _ in cands]
    d.text((20, y), "a fileira, na caixa da carta, com retratos integrados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(nicho(im, 32), (20 + j * 44, y))
    y += 48
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(amplia(nicho(im, 32), 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 116), rot, fill=TEXTO2, font=f2)
    y += 140
    d.text((20, y), "a base e os candidatos a 12× com a grade", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, im) in enumerate(linha[len(aprovados):]):
        d.text((20 + j * 220, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(im), (20 + j * 220, y + 16))
    y += 16 + 192 + 20
    largura = max(20 + len(colunas) * 440, 20 + len(linha) * 124) + 20
    out = out.crop((0, 0, largura, y))
    out.save(PASTA / f"{chave}.png")
    print(f"{chave}.png", out.size)


if __name__ == "__main__":
    for c in sys.argv[1:] or CRIATURAS:
        folha(c)
