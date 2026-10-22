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


if __name__ == "__main__":
    folha_rainha()
    folha_esqueleto()
