"""As folhas de antes × depois da terceira rodada (<criatura>.png): a carta na luta a 1920×945 (o jogo × antes × depois;
as propostas trocadas só na página: protótipo), em tamanho real e a 2×; o cartão do Bestiário (48 px); a fileira, na
caixa da carta, com retratos integrados; e a 12× com a grade, sem suavização. O espectro também com a referência e a
guia.
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
CRI = AQUI.parents[1]
JOGO = AQUI.parents[5] / "rpg/web/static/hud/icones"
REF = AQUI.parents[5] / "ferramentas/arte/referencias/icones/Espectro do Manto Inflado.png"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
# a criatura: o nome na carta, antes (pasta, id), depois (id), o que mudou, os retratos da fileira
CRIATURAS = {
    "carnical": ("Carniçal", ("segunda_rodada", "carnical-a2"), "carnical-a3", "a bochecha direita recolhida",
                 ("afogado", "cultista", "bandido")),
    "javali": ("Javali selvagem", ("segunda_rodada", "javali-a2"), "javali-a3", "as presas em arco", ("troll", "rei-troll", "rato")),
    "espectro": ("Espectro", ("quatro_pares", "espectro-a"), "espectro-m", "o retrato do manto inflado",
                 ("afogado", "ilse", "cultista")),
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
    nome, (pasta_antes, antes), depois, mudou, aprovados = CRIATURAS[chave]
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))
    caixa_de = lambda sit, modo: next(c["caixa"] for c in reg[f"{sit}/{modo}"]["caixas"] if c["nome"].startswith(nome.split()[0]))
    im_antes = Image.open(CRI / pasta_antes / "proposta" / f"{antes}-16.png").convert("RGBA")
    im_depois = gr.imagem(depois)
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1600), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{nome}: antes ({antes}) × depois ({depois}, {mudou}) — proposta, nada no jogo; trocados só na página (protótipo)",
           fill=TEXTO, font=f)
    y = 38
    colunas = (("atual (o jogo)", "atual"), (f"antes: {antes}", "antes"), (f"depois: {depois}", "depois"))
    d.text((20, y), "a carta na luta (1920×945), tamanho real e 2×", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, modo) in enumerate(colunas):
        cx = Image.open(CAP / f"luta-{modo}.png").convert("RGBA").crop(caixa_de("luta", modo))
        x = 20 + j * 470
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(cx, (x, y + 16)); out.alpha_composite(amplia(cx, 2), (x, y + 16 + cx.height + 6))
    y += 16 + 3 * 50 + 24
    d.text((20, y), "o Bestiário (48 px), tamanho real", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (rot, modo) in enumerate(colunas):
        ct = Image.open(CAP / f"bestiario-{modo}.png").convert("RGBA").crop(caixa_de("bestiario", modo))
        out.alpha_composite(ct, (20 + j * 470, y)); alto = max(alto, ct.height)
    y += alto + 20
    linha = [(a, Image.open(JOGO / f"retrato-{a}-16.png").convert("RGBA")) for a in aprovados] + [(antes, im_antes), (depois, im_depois)]
    d.text((20, y), "a fileira, na caixa da carta, com retratos integrados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(nicho(im, 32), (20 + j * 44, y))
    y += 48
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(amplia(nicho(im, 32), 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 116), rot, fill=TEXTO2, font=f2)
    y += 140
    d.text((20, y), "antes e depois a 12× com a grade" + (" | a referência (reduzida) e a guia de 16 (oculta na fonte)" if chave == "espectro" else ""),
           fill=TEXTO, font=f2)
    y += 18
    pecas = [(antes, im_antes), (depois, im_depois)]
    for j, (rot, im) in enumerate(pecas):
        d.text((20 + j * 220, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(im), (20 + j * 220, y + 16))
    if chave == "espectro":
        ref = Image.open(REF).convert("RGBA"); fundo = Image.new("RGBA", ref.size, (13, 11, 10, 255)); fundo.alpha_composite(ref)
        fundo.thumbnail((192, 192), Image.LANCZOS)
        out.alpha_composite(fundo, (460, y + 16))
        guia = Image.new("RGBA", (16, 16), (24, 21, 19, 255))
        guia.alpha_composite(Image.open(PASTA / "guias/espectro-guia-16.png").convert("RGBA"))
        out.alpha_composite(amplia(guia, 12), (600, y + 16))
    y += 16 + 192 + 20
    out = out.crop((0, 0, 1500, y))
    out.save(PASTA / f"{chave}.png")
    print(f"{chave}.png", out.size)


if __name__ == "__main__":
    for c in sys.argv[1:] or CRIATURAS:
        folha(c)
