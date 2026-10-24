"""PROTÓTIPO do d20: a prancha de construção (o dado sozinho, sem a tela). Cada material: o repouso com números de um e
dois dígitos nos estados (rolando, neutro, sucesso, falha, crítico, desastre), os quadros do giro, a tirinha e o
ícone da ficha, em tamanho de uso (2×, como na tela; a ficha 1×) e ampliados para achar o pixel. A tinta do número sai
de numero.json, a mesma tabela que d20.js usa (a tela é a prova; esta prancha só ajuda a desenhar).

    python ferramentas/prototipos/hud/d20/prancha_d20.py      # grava pranchas/construcao.png
"""
import json
import pathlib
import re

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
D = json.loads(re.search(r"const D20_DADOS = (.*);\n", (AQUI / "d20-dados.js").read_text(encoding="utf-8")).group(1))
TINTAS = json.loads((AQUI / "numero.json").read_text(encoding="utf-8"))
FUNDO = (18, 17, 16, 255)


def rgb(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def grade_png(grade, pal):
    im = Image.new("RGBA", (len(grade[0]), len(grade)), (0, 0, 0, 0))
    for y, r in enumerate(grade):
        for x, ch in enumerate(r):
            if ch in pal:
                im.putpixel((x, y), rgb(pal[ch]))
    return im


def com_numero(mat, tam, n, estado):
    """O repouso com o número `n` gravado, pelas regras de d20.js (numero.json)."""
    m = D["materiais"][mat]; t = m["tamanhos"][tam]
    im = grade_png(t["repouso"], m["paleta"])
    alg = D["algarismos"]["g" if tam == "centro" else "p"]
    lugar = t["numero"]
    s = str(n)
    w = sum(len(alg[c][0]) for c in s) + len(s) - 1
    x0 = lugar["x"] + (lugar["w"] - w) // 2; y0 = lugar["y"]
    tinta = TINTAS[mat][estado]
    pix = set()
    x = x0
    for c in s:
        for yy, r in enumerate(alg[c]):
            for xx, ch in enumerate(r):
                if ch == "#":
                    pix.add((x + xx, y0 + yy))
        x += len(alg[c][0]) + 1
    W, H = im.size
    if tinta.get("luz"):  # o entalhe: o lábio de baixo e da direita pega a luz
        for (px, py) in pix:
            q = (px + 1, py + 1)
            if q not in pix and 0 <= q[0] < W and 0 <= q[1] < H and im.getpixel(q)[3]:
                im.putpixel(q, rgb(tinta["luz"]))
    if tinta.get("halo"):  # o brilho em volta (o vidro): os vizinhos acesos
        for (px, py) in pix:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (px + dx, py + dy)
                if q not in pix and 0 <= q[0] < W and 0 <= q[1] < H and im.getpixel(q)[3]:
                    im.putpixel(q, rgb(tinta["halo"]))
    for (px, py) in pix:
        im.putpixel((px, py), rgb(tinta["tinta"]))
    if tinta.get("miolo"):  # o miolo mais claro do traço (o vidro): a coluna da esquerda de cada traço
        for (px, py) in pix:
            if (px - 1, py) not in pix and (px + 1, py) in pix:
                im.putpixel((px, py), rgb(tinta["miolo"]))
    return im


def colar(base, im, x, y, esc):
    im = im.resize((im.width * esc, im.height * esc), Image.NEAREST)
    base.alpha_composite(im, (x, y))
    return im.width, im.height


if __name__ == "__main__":
    ESTADOS = [("neutro", 20), ("neutro", 7), ("sucesso", 13), ("falha", 9), ("critico", 20), ("desastre", 1)]
    larg = 40 + len(ESTADOS) * 150
    alt = 40 + 2 * (150 + 300 + 150 + 30)
    folha = Image.new("RGBA", (larg, alt), FUNDO)
    d = ImageDraw.Draw(folha)
    y = 20
    for mat in D["materiais"]:
        d.text((20, y), f"{mat}: o repouso a 2x (tamanho de uso)", fill=(230, 220, 190))
        y += 16
        for i, (est, n) in enumerate(ESTADOS):
            colar(folha, com_numero(mat, "centro", n, est), 20 + i * 150, y, 2)
            d.text((20 + i * 150, y + 130), f"{est} {n}", fill=(170, 160, 140))
        y += 150
        d.text((20, y), "ampliado 4x", fill=(230, 220, 190))
        y += 16
        for i, (est, n) in enumerate(ESTADOS[:3]):
            colar(folha, com_numero(mat, "centro", n, est), 20 + i * 270, y, 4)
        y += 270
        m = D["materiais"][mat]
        d.text((20, y), "o giro (2x), a tirinha (2x) e a ficha (1x)", fill=(230, 220, 190))
        y += 16
        x = 20
        for q in m["tamanhos"]["centro"]["giro"]:
            w, _ = colar(folha, grade_png(q, m["paleta"]), x, y, 2)
            x += w + 6
        x += 10
        for est, n in (("neutro", 20), ("sucesso", 14), ("falha", 3)):
            w, _ = colar(folha, com_numero(mat, "tirinha", n, est), x, y, 2)
            x += w + 6
        colar(folha, grade_png(m["tamanhos"]["ficha"]["repouso"], m["paleta"]), x + 10, y, 1)
        y += 150
    folha.save(AQUI / "pranchas" / "construcao.png")
    print("ok")
