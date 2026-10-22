"""A comparação do espectro (espectro-ap.png: o A original × o AP, o pano continuando até a borda de baixo; com
`ap2`, espectro-ap2.png: o AP × o AP2, sem as dobras escuras e com a cavidade mais larga), na caixa
da carta (32) e no Bestiário (48) em tamanho real, na fileira com retratos integrados, e a 12× com a grade; embaixo, a
referência do manto inflado, guardada como conceito do corpo (não dita as proporções do ícone).
    python espectro_ap.py [ap2]
"""
import importlib.util
import pathlib

from PIL import Image, ImageDraw, ImageFont


AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
JOGO = AQUI.parents[5] / "rpg/web/static/hud/icones"
REF = AQUI.parents[5] / "ferramentas/arte/referencias/icones/Espectro do Manto Inflado.png"
_sp = importlib.util.spec_from_file_location("g1", AQUI.parents[1] / "quatro_pares/auxiliares/grades.py")
g1 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(g1)
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)


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


if __name__ == "__main__":
    import sys
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    segunda = sys.argv[1:] == ["ap2"]
    a, ap = g1.imagem("espectro-a"), Image.open(PASTA / "proposta/espectro-ap-16.png").convert("RGBA")
    nome_a, nome_b, saida = "espectro-a (o original)", "espectro-ap", "espectro-ap.png"
    titulo = "O Espectro: A original × AP (o pano continua até a borda de baixo; as linhas 0 a 10 iguais) — proposta, nada no jogo"
    if segunda:
        a, ap = ap, Image.open(PASTA / "proposta/espectro-ap2-16.png").convert("RGBA")
        nome_a, nome_b, saida = "espectro-ap (antes)", "espectro-ap2", "espectro-ap2.png"
        titulo = "O Espectro: AP × AP2 (sem as dobras escuras de baixo; a cavidade mais larga, o olho no lugar) — proposta, nada no jogo"
    out = Image.new("RGBA", (1000, 900), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), titulo, fill=TEXTO, font=f)
    y = 38
    for j, (rot, im) in enumerate(((nome_a, a), (nome_b, ap))):
        x = 20 + j * 300
        d.text((x, y), rot + " — carta 32 | Bestiário 48", fill=TEXTO2, font=f2)
        out.alpha_composite(nicho(im, 32), (x, y + 18)); out.alpha_composite(nicho(im, 48), (x + 46, y + 18))
    y += 18 + 54 + 18
    d.text((20, y), "a fileira, na caixa da carta, com retratos integrados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 18
    linha = [(n, Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA")) for n in ("afogado", "ilse", "cultista", "carnical")] + \
        [(nome_a.split()[0], a), (nome_b, ap)]
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(nicho(im, 32), (20 + j * 44, y))
    y += 46
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(amplia(nicho(im, 32), 3), (20 + j * 124, y)); d.text((20 + j * 124, y + 116), rot, fill=TEXTO2, font=f2)
    y += 140
    d.text((20, y), f"a 12× com a grade: {nome_a.split()[0]} e {nome_b} | a referência do corpo (conceito, para a arte de cenário)",
           fill=TEXTO, font=f2)
    y += 18
    out.alpha_composite(grade12(a), (20, y)); out.alpha_composite(grade12(ap), (230, y))
    ref = Image.open(REF).convert("RGBA"); fundo = Image.new("RGBA", ref.size, CARVAO); fundo.alpha_composite(ref)
    fundo.thumbnail((192, 192), Image.LANCZOS); out.alpha_composite(fundo, (450, y))
    y += 192 + 20
    out = out.crop((0, 0, 1000, y))
    out.save(PASTA / saida)
    print(saida, out.size)
