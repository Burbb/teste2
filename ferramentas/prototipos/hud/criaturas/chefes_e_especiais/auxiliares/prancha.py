"""As folhas dos seis chefes restantes e dos três especiais: por criatura (o jogo de hoje, A e B), a luta a 1920×945 em
tamanho real (o grupo: o guardião com o comum da região; no servo, o lado aliado) e a carta a 2×, a fileira com os
retratos aprovados pertinentes (na caixa da carta, real e 3×) e a 12× com a grade, sem suavização. Uma folha por par
(par1-hidra-dragao.png, par2-senhor-profeta.png, par3-bruxa-lich.png), a dos especiais (especiais.png) e a prancha geral
dos candidatos novos (candidatos.png, com o Golem R1b). Tudo trocado só na página (protótipo).
    python prancha.py      (depois do fotografar.mjs)
"""
import json
import pathlib
import re

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
    "hidra": ("Hidra do Brejo", [("atual (o jogo: a fera)", "atual", None), ("H1, as três cabeças", "a", "hidra-h1"),
                                 ("H2, a serpente de perto", "b", "hidra-h2")],
              ("sapo", "sanguessuga", "rei-troll", "arvore-ancia"), ["luta-hidra"]),
    "dragao": ("Dragão de Gelo", [("atual (o jogo: o voador)", "atual", None), ("D1, a cabeça de perfil", "a", "dragao-d1"),
                                  ("D2, de frente", "b", "dragao-d2")],
               ("grifo", "lobo-gelido", "harpia", "rei-troll"), ["luta-dragao"]),
    "senhor": ("Senhor da Guerra", [("atual (o jogo: o humano)", "atual", None), ("S1, o elmo e o troféu", "a", "senhor-s1"),
                                    ("S2, o veterano caolho", "b", "senhor-s2")],
               ("mercenario", "bandido", "rei-troll", "cavaleiro-sombrio"), ["luta-senhor"]),
    "profeta": ("Profeta das Cinzas", [("atual (o jogo: o humano)", "atual", None), ("P1, o cego encapuzado", "a", "profeta-p1"),
                                       ("P2, os olhos brancos", "b", "profeta-p2")],
                ("cultista", "xama-caido", "espectro", "arvore-ancia"), ["luta-profeta"]),
    "bruxa": ("Bruxa Afogada", [("atual (o jogo: a caveira)", "atual", None), ("B1, a cantora", "a", "bruxa-afogada-b1"),
                                ("B2, a cabeça na água", "b", "bruxa-afogada-b2")],
              ("ilse", "bruxa", "afogado", "rainha-aracnidea"), ["luta-bruxa"]),
    "lich": ("Lich Menor", [("atual (o jogo: a caveira)", "atual", None), ("L1, o rei-esqueleto", "a", "lich-l1"),
                            ("L2, o grimório", "b", "lich-l2")],
             ("esqueleto", "cultista", "cavaleiro-sombrio", "rei-troll"), ["luta-lich"]),
    "espantalho": ("Espantalho Possuído", [("atual (o jogo: a planta)", "atual", None), ("E1, o saco com chapéu", "a", "espantalho-e1"),
                                           ("E2, a brasa dentro", "b", "espantalho-e2")],
                   ("arvore-desperta", "bandido", "caido"), ["espantalho"]),
    "mimico": ("Mímico", [("atual (o jogo: o construto)", "atual", None), ("M1, o baú de frente", "a", "mimico-m1"),
                          ("M2, o baú mordendo", "b", "mimico-m2")],
               ("golem", "sapo", "cao-infernal"), ["mimico"]),
    "servo": ("Esqueleto (Invocado)", [("atual (o jogo: a caveira)", "atual", None), ("SV1, o crânio erguido", "a", "servo-sv1"),
                                       ("SV2, o E1 sob o feitiço", "b", "servo-sv2")],
              ("esqueleto", "cultista", "espectro"), ["servo"]),
}
FOTOS = {}  # todas em capturas/
ORIENTACAO = set()  # sem referência neste lote
EXTRAS = {}  # sem retratos do herói na fileira
SEM_BESTIARIO = set(CRIATURAS)  # nenhum deles entra no Bestiário
LADO = {"servo": "aliado"}  # o grupo da luta em tamanho real: o lado da carta (o servo, os aliados)
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
            cs = [c["caixa"] for c in reg[f"{sit}/{modo}"]["caixas"] if c.get("lado", "inimigo") == LADO.get(chave, "inimigo")]
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


FOLHAS = {"par1-hidra-dragao": ("hidra", "dragao"), "par2-senhor-profeta": ("senhor", "profeta"),
          "par3-bruxa-lich": ("bruxa", "lich"), "especiais": ("espantalho", "mimico", "servo")}


def juntar(nome, chaves):
    """A folha de um par (ou dos especiais): as folhas de cada criatura, uma embaixo da outra."""
    partes = [Image.open(PASTA / f"{c}.png") for c in chaves]
    out = Image.new("RGBA", (max(p.width for p in partes), sum(p.height for p in partes) + 16 * len(partes)), CARVAO)
    y = 0
    for p in partes:
        out.alpha_composite(p.convert("RGBA"), (0, y))
        y += p.height + 16
    out.save(PASTA / f"{nome}.png")
    for c in chaves:
        (PASTA / f"{c}.png").unlink()  # só a folha do par fica
    print(f"{nome}.png", out.size)


def candidatos():
    """A prancha geral dos candidatos novos (os 18 deste lote e o Golem R1b), cada um na caixa da carta a 32 e a 3×, com o
    nome do arquivo."""
    golem = Image.open(AQUI.parents[1] / "chefes_arvore_golem/proposta/primordial-r1b-16.png").convert("RGBA")
    itens = [(f, desenho(f)) for chave in CRIATURAS for _, _, f in CRIATURAS[chave][1] if f] + [("primordial-r1b", golem)]
    f2 = ImageFont.truetype("arial.ttf", 12)
    por = 6
    out = Image.new("RGBA", (20 + por * 150, 40 + ((len(itens) + por - 1) // por) * 190), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "os candidatos novos (protótipo; nada no jogo): na caixa da carta a 32 e a 3×", fill=TEXTO, font=f2)
    for k, (rot, im) in enumerate(itens):
        x, y = 20 + (k % por) * 150, 34 + (k // por) * 190
        out.alpha_composite(nicho(im, 32), (x, y))
        out.alpha_composite(amplia(nicho(im, 32), 3), (x + 2, y + 42))
        d.text((x, y + 160), rot, fill=TEXTO2, font=f2)
    out.save(PASTA / "candidatos.png")
    print("candidatos.png", out.size)


if __name__ == "__main__":
    for nome, chaves in FOLHAS.items():
        for c in chaves:
            folha(c)
        juntar(nome, chaves)
    candidatos()
