"""As folhas da Abominação e do Cavaleiro Sombrio (abominacao.png, cavaleiro.png): por coluna (o jogo de hoje, A e B),
a carta na luta a 1920×945 em tamanho real e a 2×, o cartão do Bestiário (48) em tamanho real, a fileira com os retratos
aprovados pertinentes (na caixa da carta, real e 3×) e a 12× com a grade, sem suavização. Tudo trocado só na página
(protótipo).
Na quarta, abominacao-c3.png (a C × a C2 × a C3) e cavaleiro-t2.png (a referência, também no tamanho do retrato, × o T ×
o T2). Na terceira, abominacao-c2.png (a C × a C2) e cavaleiro-t.png (a referência, a guia e o T; o jogo de hoje × o T).
Na segunda rodada, abominacao-cde.png (o jogo de hoje × C × D × E) e cavaleiro-a2.png (o jogo de hoje × o A original ×
o A2), das fotos em capturas-2/.
    python prancha.py [abominacao|cavaleiro|abominacao-cde|cavaleiro-a2|abominacao-c2|cavaleiro-t|abominacao-c3|cavaleiro-t2 ...]      (depois do fotografar.mjs)
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
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
# a criatura: o nome na carta, as colunas (rótulo, modo da foto, o desenho: (pasta, id) ou None para o do jogo), os
# retratos do jogo na fileira
CRIATURAS = {
    "abominacao": ("Abominação", [("atual (o jogo: o corrompido)", "atual", None),
                                  ("A, a boca costurada", "a", "abominacao-a"),
                                  ("B, o brutamontes curvado", "b", "abominacao-b")],
                   ("carnical", "afogado", "troll", "cria-vazio"), ["luta-abominacao"]),
    "cavaleiro": ("Cavaleiro sombrio", [("atual (o jogo: a caveira)", "atual", None),
                                        ("A, o elmo fechado", "a", "cavaleiro-a"),
                                        ("B, a espada e a crista", "b", "cavaleiro-b")],
                  ("esqueleto", "mercenario", "espectro", "bandido"), ["luta-cavaleiro"]),
    "abominacao-cde": ("Abominação", [("atual (o jogo: o corrompido)", "atual", None),
                                      ("C, a mandíbula torta", "c", "abominacao-c"),
                                      ("D, as duas cabeças", "d", "abominacao-d"),
                                      ("E, os espinhos", "e", "abominacao-e")],
                       ("carnical", "afogado", "troll", "cria-vazio"), ["luta-abominacao"]),
    "cavaleiro-a2": ("Cavaleiro sombrio", [("atual (o jogo: a caveira)", "atual", None),
                                           ("A original (a direção escolhida)", "a", "cavaleiro-a"),
                                           ("A2, o A refinado", "a2", "cavaleiro-a2")],
                     ("esqueleto", "mercenario", "espectro", "bandido"), ["luta-cavaleiro"]),
    # a terceira rodada, compacta: a C × a C2; o jogo de hoje × o T, com a referência, a guia e o T a 12×
    "abominacao-c2": ("Abominação", [("C, a anterior", "c", "abominacao-c"), ("C2, a C refinada", "c2", "abominacao-c2")],
                      ("carnical", "afogado", "troll", "cria-vazio"), ["luta-abominacao"]),
    "cavaleiro-t": ("Cavaleiro sombrio", [("atual (o jogo: a caveira)", "atual", None),
                                          ("T, a transposição da referência", "t", "cavaleiro-t")],
                    ("esqueleto", "mercenario", "espectro", "bandido"), ["luta-cavaleiro"],
                    ("Cavaleiro sombrio do Vazio.png", (27, 54, 1227, 1254), "cavaleiro-t-guia-16.png")),
    # a quarta: a C × a C2 × a C3; a referência × o T × o T2 (com a referência no tamanho do retrato)
    "abominacao-c3": ("Abominação", [("C, a base", "c", "abominacao-c"), ("C2, a anterior", "c2", "abominacao-c2"),
                                     ("C3, a nova", "c3", "abominacao-c3")],
                      ("carnical", "afogado", "troll", "cria-vazio"), ["luta-abominacao"]),
    "cavaleiro-t2": ("Cavaleiro sombrio", [("T, o anterior", "t", "cavaleiro-t"), ("T2, o novo", "t2", "cavaleiro-t2")],
                     ("esqueleto", "mercenario", "espectro", "bandido"), ["luta-cavaleiro"],
                     ("Cavaleiro sombrio do Vazio.png", (27, 54, 1227, 1254), "cavaleiro-t-guia-16.png")),
}
FOTOS = {"abominacao-cde": "capturas-2", "cavaleiro-a2": "capturas-2", "abominacao-c2": "capturas-2",
         "cavaleiro-t": "capturas-2", "abominacao-c3": "capturas-2", "cavaleiro-t2": "capturas-2"}
ORIENTACAO = {"cavaleiro-t2"}  # a referência reduzida ao tamanho do retrato (32 e 48), ao lado dos desenhos  # a pasta das fotos, se não for a capturas/
REFERENCIAS = AQUI.parents[5] / "ferramentas/arte/referencias/icones"


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


def nicho(im16, lado):
    cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255))
    cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
    cx.alpha_composite(amplia(im16, lado // 16), (3, 3))
    return cx


def grade12(im16):
    g = amplia(im16, 12)
    fundo = Image.new("RGBA", g.size, (24, 21, 19, 255))
    fundo.alpha_composite(g)
    dd = ImageDraw.Draw(fundo)
    for i in range(1, 16):
        dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255))
        dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
    return fundo


def desenho(ident):
    return gr.imagem(ident)


def folha(chave):
    nome, colunas, aprovados, lutas, *ref = CRIATURAS[chave]
    cap = PASTA / FOTOS[chave] if chave in FOTOS else CAP
    reg = json.loads((cap / "registro.json").read_text(encoding="utf-8"))

    def caixa_de(sit, modo):  # a carta da criatura (a primeira, se houver duas; a invocada pelo nome com a letra)
        return next(c["caixa"] for c in reg[f"{sit}/{modo}"]["caixas"] if c["nome"].startswith(nome))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    larg = 460 if len(colunas) <= 3 else 440
    out = Image.new("RGBA", (max(1500, 20 + len(colunas) * larg), 2000), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{nome} — trocados só na página (protótipo); nada no jogo", fill=TEXTO, font=f)
    y = 38
    if ref:  # a referência (o recorte da guia, reduzido só para olhar), a guia de 16 (oculta na fonte) e a proposta, a 12×
        arquivo, corte, guia = ref[0]
        d.text((20, y), "a referência (imagem gerada; o recorte da guia, reduzido só para olhar) | a guia de 16, oculta na "
               "fonte (o recorte reduzido por média) | a transposição — a 12×", fill=TEXTO, font=f2)
        im = Image.open(REFERENCIAS / arquivo).convert("RGBA")
        fundo = Image.new("RGBA", im.size, CARVAO)
        fundo.alpha_composite(im)
        out.alpha_composite(fundo.crop(corte).resize((192, 192), Image.LANCZOS), (20, y + 18))
        out.alpha_composite(grade12(Image.open(PASTA / "guias" / guia).convert("RGBA")), (232, y + 18))
        out.alpha_composite(grade12(desenho(colunas[-1][2])), (444, y + 18))
        y += 18 + 192 + 24
        if chave in ORIENTACAO:  # a orientação: a referência reduzida (só para olhar) e cada desenho, a 32 e a 48
            d.text((20, y), "a orientação no tamanho do retrato, na caixa da carta: a referência reduzida (LANCZOS, só "
                   "para olhar) e cada desenho, a 32 e a 48", fill=TEXTO, font=f2)
            y += 18
            pequena = fundo.crop(corte)
            itens = [("referência", lambda l: pequena.resize((l, l), Image.LANCZOS))] + [
                (f, lambda l, f=f: amplia(desenho(f), l // 16)) for _, _, f in colunas if f]
            for j, (rot, faz) in enumerate(itens):
                x = 20 + j * 130
                for i, lado in enumerate((32, 48)):
                    cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255))
                    cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
                    cx.alpha_composite(faz(lado), (3, 3))
                    out.alpha_composite(cx, (x + i * 44, y + (48 - lado) // 2))
                d.text((x, y + 58), rot, fill=TEXTO2, font=f2)
            y += 58 + 24
    for sit in lutas:
        rot_sit = "a carta na luta" if sit != "luta-invocada" else "a carta da cria invocada pelo antagonista"
        d.text((20, y), f"{rot_sit} (1920×945), tamanho real e 2×", fill=TEXTO, font=f2)
        y += 18
        alto = 0
        for j, (rot, modo, _) in enumerate(colunas):
            cx = Image.open(cap / f"{sit}-{modo}.png").convert("RGBA").crop(caixa_de(sit, modo))
            x = 20 + j * larg
            d.text((x, y), rot, fill=TEXTO2, font=f2)
            out.alpha_composite(cx, (x, y + 16))
            dois = amplia(cx, 2)
            if dois.width > larg - 10:
                dois = dois.crop((0, 0, larg - 10, dois.height))
            out.alpha_composite(dois, (x, y + 16 + cx.height + 6))
            alto = max(alto, 16 + cx.height + 6 + dois.height)
        y += alto + 24
    d.text((20, y), "o Bestiário (48 px), tamanho real", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (rot, modo, _) in enumerate(colunas):
        ct = Image.open(cap / f"bestiario-{modo}.png").convert("RGBA").crop(caixa_de("bestiario", modo))
        if ct.width > larg - 10:
            ct = ct.crop((0, 0, larg - 10, ct.height))
        out.alpha_composite(ct, (20 + j * larg, y))
        alto = max(alto, ct.height)
    y += alto + 20
    novos = [(fonte, desenho(fonte)) for _, _, fonte in colunas if fonte]
    linha = [(a, Image.open(JOGO / f"retrato-{a}-16.png").convert("RGBA")) for a in aprovados] + novos
    d.text((20, y), "a fileira, na caixa da carta, com retratos do jogo — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (_, im) in enumerate(linha):
        out.alpha_composite(nicho(im, 32), (20 + j * 44, y))
    y += 48
    for j, (rot, im) in enumerate(linha):
        out.alpha_composite(amplia(nicho(im, 32), 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 116), rot, fill=TEXTO2, font=f2)
    y += 140
    d.text((20, y), "a 12× com a grade", fill=TEXTO, font=f2)
    y += 18
    for j, (rot, im) in enumerate(novos):
        d.text((20 + j * 220, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(im), (20 + j * 220, y + 16))
    y += 16 + 192 + 20
    out = out.crop((0, 0, out.width, y))
    out.save(PASTA / f"{chave}.png")
    print(f"{chave}.png", out.size)


if __name__ == "__main__":
    for c in sys.argv[1:] or CRIATURAS:
        folha(c)
