"""As folhas da rodada depois do Caído CA (<criatura>.png): por coluna (o jogo de hoje, a proposta da rodada anterior e as
desta), a carta na luta a 1920×945 em tamanho real e a 2×, o cartão do Bestiário (48) em tamanho real, a fileira com os
retratos aprovados pertinentes (na caixa da carta, real e 3×) e a 12× com a grade, sem suavização. Tudo trocado só na
página (protótipo).
    python prancha.py [<criatura> ...]      (depois do fotografar.mjs; a segunda rodada: harpia-t grifo-ga3 xama-x1r)
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
    "grifo": ("Grifo", [("antes: GA (rodada anterior)", "antes", ("harpia_grifo", "grifo-ga")),
                        ("depois: GA2, a ponta do bico limpa", "a", ("rodada_23_10", "grifo-ga2"))],
              ("falcao", "urso", "lobo-gelido")),
    "harpia": ("Harpia", [("atual (o jogo: o voador)", "atual", None),
                          ("histórico: HA (não escolhida)", "antes", ("harpia_grifo", "harpia-ha")),
                          ("H1, a abutre de rosto humano", "a", ("rodada_23_10", "harpia-h1")),
                          ("H2, a da asa erguida", "b", ("rodada_23_10", "harpia-h2")),
                          ("H3, a de bico", "c", ("rodada_23_10", "harpia-h3"))],
               ("bruxa", "falcao", "espectro")),
    "xama": ("Xamã caído", [("atual (o jogo: o demônio)", "atual", None),
                            ("histórico: XA (não escolhido)", "antes", ("caidos", "xama-caido-xa")),
                            ("X1, o velho do capuz", "a", ("rodada_23_10", "xama-caido-x1")),
                            ("X2, o do cajado", "b", ("rodada_23_10", "xama-caido-x2")),
                            ("X3, o das penas", "c", ("rodada_23_10", "xama-caido-x3"))],
             ("caido", "cultista", "troll")),
    # a segunda rodada: cada folha compara a anterior com a nova; a da Harpia abre com a referência e a guia
    "harpia-t": ("Harpia", [("atual (o jogo: o voador)", "atual", None),
                            ("T, a transposição da referência nova", "d", ("rodada_23_10", "harpia-t"))],
                 ("bruxa", "ilse", "cultista", "falcao", "espectro", "caido"), "harpia-t-guia-16.png"),
    "grifo-ga3": ("Grifo", [("antes: GA2, a ponta do bico limpa", "a", ("rodada_23_10", "grifo-ga2")),
                            ("depois: GA3, o gancho descendo", "d", ("rodada_23_10", "grifo-ga3"))],
                  ("falcao", "urso", "lobo-gelido")),
    "xama-x1r": ("Xamã caído", [("X1, o velho do capuz", "a", ("rodada_23_10", "xama-caido-x1")),
                                ("X1r, o colar menor e o pescoço livre", "d", ("rodada_23_10", "xama-caido-x1r"))],
                 ("caido", "cultista", "troll")),
}
REFERENCIA = AQUI.parents[5] / "ferramentas/arte/referencias/icones/Harpia vulturina em pixel art.png"


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


def desenho(fonte):
    pasta, ident = fonte
    if pasta == "rodada_23_10":
        return gr.imagem(ident)
    return Image.open(CRI / pasta / "proposta" / f"{ident}-16.png").convert("RGBA")


def folha(chave):
    nome, colunas, aprovados, *guia = CRIATURAS[chave]
    reg = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))

    def caixa_de(sit, modo):
        return next(c["caixa"] for c in reg[f"{sit}/{modo}"]["caixas"] if c["nome"] == nome)
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    larg = 460 if len(colunas) <= 3 else 380
    out = Image.new("RGBA", (max(1500, 20 + len(colunas) * larg), 1700), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{nome} — trocados só na página (protótipo); nada no jogo", fill=TEXTO, font=f)
    y = 38
    if guia:  # a referência (reduzida, só para olhar), a guia de 16 que mediu (oculta na fonte) e a proposta, a 12×
        d.text((20, y), "a referência nova (imagem gerada; reduzida só para olhar) | a guia de 16, oculta na fonte "
               "(o recorte quadrado reduzido por média) | a proposta — a 12×", fill=TEXTO, font=f2)
        ref = Image.open(REFERENCIA).convert("RGBA")
        fundo = Image.new("RGBA", ref.size, CARVAO)
        fundo.alpha_composite(ref)
        out.alpha_composite(fundo.resize((192, 192), Image.LANCZOS), (20, y + 18))
        out.alpha_composite(grade12(Image.open(PASTA / "guias" / guia[0]).convert("RGBA")), (232, y + 18))
        out.alpha_composite(grade12(desenho(colunas[-1][2])), (444, y + 18))
        y += 18 + 192 + 24
    d.text((20, y), "a carta na luta (1920×945), tamanho real e 2×", fill=TEXTO, font=f2)
    y += 18
    alto = 0
    for j, (rot, modo, _) in enumerate(colunas):
        cx = Image.open(CAP / f"luta-{modo}.png").convert("RGBA").crop(caixa_de("luta", modo))
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
    novos = [(fonte[1], desenho(fonte)) for _, _, fonte in colunas if fonte]
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
    if guia:  # a 12× da proposta já abre a folha
        out.crop((0, 0, out.width, y)).save(PASTA / f"{chave}.png")
        print(f"{chave}.png", (out.width, y))
        return
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
