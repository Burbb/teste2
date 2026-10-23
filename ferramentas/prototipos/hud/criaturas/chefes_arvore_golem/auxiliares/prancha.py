"""As folhas da Árvore Anciã e do Golem Primordial (anciaa.png, primordial.png): por coluna (o jogo de hoje, 1 e 2), a
luta a 1920×945 em tamanho real (o grupo: o guardião com o comum correspondente e outro da região) e a carta do guardião
a 2×, a fileira com o comum,
os chefes aprovados e os comuns pertinentes (na caixa da carta, real e 3×) e a 12× com a grade, sem suavização. Os
guardiões não entram no Bestiário. Tudo trocado só na página (protótipo).
Na segunda rodada, anciaa-r.png e primordial-r.png (a referência, a guia e as três tentativas a 12×; R1 × R2 × R3 na luta).
E anciaa-r2.png e primordial-r2.png (a R2 e as três variações dela).
    python prancha.py [anciaa|primordial|anciaa-r|primordial-r|anciaa-r2|primordial-r2 ...]      (depois do fotografar.mjs)
"""
import json
import pathlib
import re
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
    "anciaa": ("Árvore Anciã", [("atual (o jogo: a planta)", "atual", None),
                                ("AA1, o rosto-rei", "a", "anciaa-aa1"),
                                ("AA2, a árvore imensa", "b", "anciaa-aa2")],
               ("arvore-desperta", "rei-troll", "rainha-aracnidea", "lobo"), ["luta-anciaa"]),
    "primordial": ("Golem Primordial", [("atual (o jogo: o construto)", "atual", None),
                                        ("GP1, a parede que se levanta", "a", "primordial-gp1"),
                                        ("GP2, o ídolo", "b", "primordial-gp2")],
                   ("golem", "rei-troll", "rainha-aracnidea", "esqueleto"), ["luta-primordial"]),
}
CRIATURAS["anciaa-r"] = ("Árvore Anciã", [  # a segunda rodada: as três tentativas de copiar a referência em close
    ("R1, pela guia limpa", "r1", "anciaa-r1"), ("R2, por volumes", "r2", "anciaa-r2"),
    ("R3, pelas linhas", "r3", "anciaa-r3")],
    ("arvore-desperta", "rei-troll", "rainha-aracnidea", "lobo"), ["luta-anciaa"],
    ("Rosto da árvore ancestral-1.png", (27, 27, 1227, 1227), "anciaa-r-guia-16.png",
     ["anciaa-r1", "anciaa-r2", "anciaa-r3"]))
CRIATURAS["primordial-r"] = ("Golem Primordial", [
    ("R1, pela guia limpa", "r1", "primordial-r1"), ("R2, por volumes", "r2", "primordial-r2"),
    ("R3, pelas linhas", "r3", "primordial-r3")],
    ("golem", "rei-troll", "rainha-aracnidea", "esqueleto"), ["luta-primordial"],
    ("Rosto do Golem de Pedra Primordial-2.png", (27, 27, 1227, 1227), "primordial-r-guia-16.png",
     ["primordial-r1", "primordial-r2", "primordial-r3"]))
CRIATURAS["anciaa-r2"] = ("Árvore Anciã", [  # as três variações da R2, ao lado dela
    ("R2, por volumes", "r2", "anciaa-r2"), ("R2a, a luz lateral", "r2a", "anciaa-r2a"),
    ("R2b, o olhar mais pesado", "r2b", "anciaa-r2b"), ("R2c, a silhueta dos galhos", "r2c", "anciaa-r2c")],
    ("arvore-desperta", "rei-troll", "rainha-aracnidea", "lobo"), ["luta-anciaa"],
    ("Rosto da árvore ancestral-1.png", (27, 27, 1227, 1227), "anciaa-r-guia-16.png",
     ["anciaa-r2", "anciaa-r2a", "anciaa-r2b", "anciaa-r2c"]))
CRIATURAS["primordial-r2"] = ("Golem Primordial", [
    ("R2, por volumes", "r2", "primordial-r2"), ("R2a, o close mais fechado", "r2a", "primordial-r2a"),
    ("R2b, os três quartos", "r2b", "primordial-r2b"), ("R2c, as pedras mais brutas", "r2c", "primordial-r2c")],
    ("golem", "rei-troll", "rainha-aracnidea", "esqueleto"), ["luta-primordial"],
    ("Rosto do Golem de Pedra Primordial-2.png", (27, 27, 1227, 1227), "primordial-r-guia-16.png",
     ["primordial-r2", "primordial-r2a", "primordial-r2b", "primordial-r2c"]))
CRIATURAS["primordial-r1b"] = ("Golem Primordial", [  # a R1 (a base escolhida) × a R1b (o olhar mais pesado)
    ("R1, a base escolhida", "r1", "primordial-r1"), ("R1b, o olhar mais pesado", "r1b", "primordial-r1b")],
    ("golem", "arvore-ancia", "rei-troll", "rainha-aracnidea"), ["luta-primordial"])
FOTOS = {}  # todas em capturas/
ORIENTACAO = set()  # sem referência neste par
EXTRAS = {}  # sem retratos do herói na fileira
SEM_BESTIARIO = {"anciaa", "primordial", "anciaa-r", "primordial-r", "anciaa-r2", "primordial-r2", "primordial-r1b"}  # os guardiões não entram no Bestiário
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


def heroi(classe):
    """A carta de 16 do herói (retratos.js: a grade <CLASSE>_CARTA e a paleta dela), como está no jogo."""
    js = (AQUI.parents[5] / "rpg/web/static/retratos.js").read_text(encoding="utf-8")
    nome = re.search(classe + r': \{ cores: (\w+)', js).group(1)
    pal = dict(re.findall(r'(\w): "#(\w{6})"', re.search(r"const " + nome + r" = \{(.*?)\};", js, re.S).group(1)))
    grade = re.findall(r'"([^"]{16})"', re.search(r"const " + classe.upper() + r"_CARTA = \[(.*?)\];", js, re.S).group(1))
    im = Image.new("RGBA", (16, 16))
    for y, linha in enumerate(grade):
        for x, ch in enumerate(linha):
            if ch != ".":
                im.putpixel((x, y), tuple(int(pal[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


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
    for r in ref:  # cada referência (o recorte da guia, reduzido só para olhar), a guia de 16 (oculta) e a proposta, a 12×
        arquivo, corte, guia, *qual = r
        d.text((20, y), "a referência (imagem gerada; o recorte da guia, reduzido só para olhar) | a guia de 16, oculta na "
               "fonte (o recorte reduzido por média) | a transposição — a 12×", fill=TEXTO, font=f2)
        im = Image.open(REFERENCIAS / arquivo).convert("RGBA")
        fundo = Image.new("RGBA", im.size, CARVAO)
        fundo.alpha_composite(im)
        out.alpha_composite(fundo.crop(corte).resize((192, 192), Image.LANCZOS), (20, y + 18))
        out.alpha_composite(grade12(Image.open(PASTA / "guias" / guia).convert("RGBA")), (232, y + 18))
        quais = qual[0] if qual and isinstance(qual[0], list) else [qual[0] if qual else colunas[-1][2]]
        for i, q in enumerate(quais):  # uma ou várias transposições da mesma referência, lado a lado
            out.alpha_composite(grade12(desenho(q)), (444 + i * 212, y + 18))
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
            foto = Image.open(cap / f"{sit}-{modo}.png").convert("RGBA")
            cx = foto.crop(caixa_de(sit, modo))
            x = 20 + j * larg
            d.text((x, y), rot, fill=TEXTO2, font=f2)
            # em tamanho real, o grupo inteiro da luta (o guardião com o comum correspondente ao lado); a 2×, o guardião
            cs = [c["caixa"] for c in reg[f"{sit}/{modo}"]["caixas"]]
            grupo = foto.crop((min(c[0] for c in cs), min(c[1] for c in cs), max(c[2] for c in cs), max(c[3] for c in cs)))
            out.alpha_composite(grupo, (x, y + 16))
            dois = amplia(cx, 2)
            if dois.width > larg - 10:
                dois = dois.crop((0, 0, larg - 10, dois.height))
            out.alpha_composite(dois, (x, y + 16 + grupo.height + 6))
            alto = max(alto, 16 + grupo.height + 6 + dois.height)
        y += alto + 24
    if chave not in SEM_BESTIARIO:
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

    novos = [(f"{c} (aprovado)", heroi(c)) for c in EXTRAS.get(chave, [])] + [
        (fonte, desenho(fonte)) for _, _, fonte in colunas if fonte]
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
