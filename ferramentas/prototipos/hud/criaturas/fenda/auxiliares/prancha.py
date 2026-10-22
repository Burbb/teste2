"""As folhas do Cão infernal e da Cria do Vazio (cao.png, cria.png): por coluna (o jogo de hoje, A e B), a carta na luta a
1920×945 em tamanho real e a 2× (a da cria também como invocada pelo antagonista), o cartão do Bestiário (48) em tamanho
real, a fileira com os retratos aprovados pertinentes (na caixa da carta, real e 3×) e a 12× com a grade, sem
suavização. Tudo trocado só na página (protótipo).
    python prancha.py [cao|cria|cria-a2|cao-t|cao-n|cao-n2|cao-r|cao-ra2|cao-ra3|cao-p ...]      (depois do fotografar.mjs)
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
    "cao": ("Cão infernal", [("atual (o jogo: o demônio)", "atual", None),
                             ("A, o que rosna de perfil", "a", "cao-infernal-a"),
                             ("B, o mastim de cabeça baixa", "b", "cao-infernal-b")],
            ("lobo", "lobo-gelido", "caido", "xama-caido"), ["luta-cao"]),
    "cria": ("Cria do Vazio", [("atual (o jogo: o etéreo)", "atual", None),
                               ("A, o caco da Fenda", "a", "cria-vazio-a"),
                               ("B, a fera que anda", "b", "cria-vazio-b")],
             ("espectro", "cultista", "carnical", "aranha"), ["luta-cria", "luta-invocada"]),
    # a segunda passada: a Cria A × A2 e a referência do Cão × a transposição T
    "cria-a2": ("Cria do Vazio", [("A (a primeira passada)", "a", "cria-vazio-a"),
                                  ("A2, o volume nos cacos", "c", "cria-vazio-a2")],
                ("espectro", "cultista", "carnical", "aranha"), ["luta-cria", "luta-invocada"]),
    "cao-t": ("Cão infernal", [("atual (o jogo: o demônio)", "atual", None),
                               ("T, a transposição da referência", "c", "cao-infernal-t")],
              ("lobo", "lobo-gelido", "caido", "xama-caido"), ["luta-cao"],
              ("Cão infernal em pixel art.png", (50, 40, 1250, 1240), "cao-infernal-t-guia-16.png")),
    # a terceira tentativa do Cão: o T recusado × o N (sem guia: a referência só como direção)
    "cao-n": ("Cão infernal", [("T (recusado)", "c", "cao-infernal-t"),
                               ("N, a construção nova", "d", "cao-infernal-n")],
              ("lobo", "lobo-gelido", "caido"), ["luta-cao"]),
    # o retoque do rosto do N: N × N2, com os mesmos dados e o mesmo enquadramento
    "cao-n2": ("Cão infernal", [("N (a terceira tentativa)", "d", "cao-infernal-n"),
                                ("N2, o retoque do rosto", "e", "cao-infernal-n2")],
               ("lobo", "lobo-gelido", "caido", "xama-caido", "cria-vazio"), ["luta-cao"]),
    # os três rosnados sobre a cabeça nova, ao lado do N2
    "cao-r": ("Cão infernal", [("N2 (o retoque do rosto)", "e", "cao-infernal-n2"),
                               ("RA, a bocarra aberta", "f", "cao-infernal-ra"),
                               ("RB, o lábio repuxado", "g", "cao-infernal-rb"),
                               ("RC, a cabeça baixa", "h", "cao-infernal-rc")],
              ("lobo", "lobo-gelido", "caido", "xama-caido", "cria-vazio"), ["luta-cao"]),
    # a boca da RA refeita: RA × RA2, com os mesmos dados
    "cao-ra2": ("Cão infernal", [("RA (a bocarra aberta)", "f", "cao-infernal-ra"),
                                 ("RA2, a cavidade e a presa", "i", "cao-infernal-ra2")],
                ("lobo", "lobo-gelido", "caido", "xama-caido", "cria-vazio"), ["luta-cao"]),
    # os dentes da RA2 refeitos: RA2 × RA3, com os mesmos dados
    "cao-ra3": ("Cão infernal", [("RA2 (a boca banguela)", "i", "cao-infernal-ra2"),
                                 ("RA3, as presas de obsidiana em cinza", "j", "cao-infernal-ra3")],
                ("lobo", "lobo-gelido", "caido", "xama-caido", "cria-vazio"), ["luta-cao"]),
    # três bocas cheias sobre a cabeça da RA3
    "cao-p": ("Cão infernal", [("RA3", "j", "cao-infernal-ra3"),
                               ("P1, a bocarra de presas", "k", "cao-infernal-p1"),
                               ("P2, a boca fechada", "l", "cao-infernal-p2"),
                               ("P3, o lábio repuxado", "m", "cao-infernal-p3")],
              ("lobo", "lobo-gelido", "caido", "xama-caido", "cria-vazio"), ["luta-cao"]),
}
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
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))

    def caixa_de(sit, modo):  # a carta da criatura (a primeira, se houver duas; a invocada pelo nome com a letra)
        return next(c["caixa"] for c in reg[f"{sit}/{modo}"]["caixas"] if c["nome"].startswith(nome))
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    larg = 460 if len(colunas) <= 3 else 380
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
    for sit in lutas:
        rot_sit = "a carta na luta" if sit != "luta-invocada" else "a carta da cria invocada pelo antagonista"
        d.text((20, y), f"{rot_sit} (1920×945), tamanho real e 2×", fill=TEXTO, font=f2)
        y += 18
        alto = 0
        for j, (rot, modo, _) in enumerate(colunas):
            cx = Image.open(CAP / f"{sit}-{modo}.png").convert("RGBA").crop(caixa_de(sit, modo))
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
        ct = Image.open(CAP / f"bestiario-{modo}.png").convert("RGBA").crop(caixa_de("bestiario", modo))
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
