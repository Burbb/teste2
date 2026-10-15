"""Pinta grades de retratos (do extrair.mjs ou de candidatos) numa folha, em tamanho de exibição (a escala do jogo) e
ampliadas para inspeção, sobre o carvão. Só para estudo; a avaliação é no jogo.
    python ver.py <json> <saida.png> nome-papel:escala [...]"""
import json, sys
from PIL import Image, ImageDraw

def pintar(g, cores, e):
    h, w = len(g), len(g[0])
    im = Image.new("RGBA", (w * e, h * e), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for y, linha in enumerate(g):
        for x, c in enumerate(linha):
            if c != "." and c in cores:
                d.rectangle((x * e, y * e, x * e + e - 1, y * e + e - 1), fill=cores[c])
    return im

def folha(dados, itens, saida, zoom=6):
    pecas = [(n, pintar(dados[n]["grade"], dados[n]["cores"], e), pintar(dados[n]["grade"], dados[n]["cores"], e * zoom)) for n, e in itens]
    W = sum(max(a.width, b.width) + 24 for _, a, b in pecas) + 20
    H = max(b.height for _, a, b in pecas) + max(a.height for _, a, b in pecas) + 60
    im = Image.new("RGBA", (W, H), (19, 20, 23, 255)); d = ImageDraw.Draw(im); x = 12
    for n, a, b in pecas:
        im.alpha_composite(a, (x, 10)); im.alpha_composite(b, (x, 20 + a.height)); d.text((x, H - 16), n, fill=(200, 192, 176))
        x += max(a.width, b.width) + 24
    im.save(saida)

if __name__ == "__main__":
    dados = json.load(open(sys.argv[1]))
    itens = [(a.split(":")[0], int(a.split(":")[1])) for a in sys.argv[3:]]
    folha(dados, itens, sys.argv[2])
