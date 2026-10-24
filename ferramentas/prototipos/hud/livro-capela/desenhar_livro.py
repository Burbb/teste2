"""O livro da capela aberto (protótipo, 24/10/2026; nada no jogo): o registro de couro castanho da sacristia, visto de
cima, desenhado pelo método das cenas (cada parte em px deliberados; a textura do papel num ladrilho escrito à mão).
O texto não está na imagem: a página o escreve por cima (livro.js), nas áreas que `AREAS` diz.

    python desenhar_livro.py            # grava propostas/*.png e propostas/areas.json

- `livro-a.png`: as duas páginas pautadas (A · o registro);
- `livro-b.png`: as duas páginas lisas (B · o registro que vira confissão);
- `livro-c-1.png`, `livro-c-2.png`: a página próxima (C), na primeira e na segunda entrada (mais folhas viradas para a
  esquerda na segunda).

O couro é o da cena (`telas/cenas.js`: a capa #5a3422, a luz #7a4c30), sem dourado nem ferragens. A escala no jogo é
3 (cada pixel daqui vira 3×3 px de CSS), igual nas duas janelas.
"""
import json
import pathlib

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI / "propostas"

C = {
    "sombra": (10, 7, 5, 150),
    "contorno": (26, 15, 10, 255),
    "couro_esc": (58, 32, 22, 255), "couro": (90, 52, 34, 255), "couro_luz": (122, 76, 48, 255),
    "couro_gasto": (138, 96, 66, 255),
    "folha_beira": (201, 184, 140, 255), "folha_beira_esc": (168, 148, 104, 255),
    "papel": (232, 217, 175, 255), "papel_esc": (224, 207, 163, 255), "papel_luz": (238, 225, 186, 255),
    "dobra1": (219, 201, 155, 255), "dobra2": (205, 186, 139, 255), "dobra3": (186, 166, 120, 255),
    "umidade": (226, 209, 164, 255), "umidade_linha": (208, 187, 140, 255),
    "pauta": (214, 198, 156, 255), "margem": (204, 168, 140, 255),
}

# O grão do papel, desenhado à mão: '.' o papel, 'e' um tom abaixo, 'l' um acima. Ralo, para não brigar com a letra.
GRAO = [
    "..........e.....",
    "...l............",
    "............e...",
    "......e.........",
    ".l..............",
    "..........l.....",
    "....e...........",
    "..............e.",
    "........e.......",
    "..e.............",
    "...........l....",
    "......l.........",
    ".e..............",
    "..........e.....",
    "....l...........",
    ".............e..",
]

# A marca de umidade no canto de baixo de fora (a capela alagada), à mão: 'x' a linha da maré, 'u' dentro dela.
# Linhas de cima para baixo, encostada no canto; espelhada para o lado esquerdo.
UMIDADE = [
    "...............xx",
    "...........xxxxuu",
    "........xxxuuuuuu",
    "......xxuuuuuuuuu",
    ".....xuuuuuuuuuuu",
    "...xxuuuuuuuuuuuu",
    "..xuuuuuuuuuuuuuu",
    ".xuuuuuuuuuuuuuuu",
]


class Tela:
    def __init__(self, w, h):
        self.im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.w, self.h = w, h

    def px(self, x, y, cor, w=1, h=1):
        cor = C.get(cor, cor)
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if 0 <= xx < self.w and 0 <= yy < self.h:
                    self.im.putpixel((xx, yy), cor)

    def salvar(self, nome):
        SAIDA.mkdir(exist_ok=True)
        self.im.save(SAIDA / nome)


def capa(t, x0, y0, x1, y1):
    """A capa de couro aberta por baixo das folhas: o contorno, a beira de cima na luz, a de baixo e a da direita na
    sombra, os cantos gastos (o couro mais claro onde a mão pega)."""
    t.px(x0 + 2, y0 + 2, "sombra", x1 - x0 + 1, y1 - y0 + 1)          # a sombra no véu, para baixo e para a direita
    t.px(x0, y0, "contorno", x1 - x0 + 1, y1 - y0 + 1)
    t.px(x0 + 1, y0 + 1, "couro", x1 - x0 - 1, y1 - y0 - 1)
    t.px(x0 + 1, y0 + 1, "couro_luz", x1 - x0 - 1, 1)                  # a beira de cima pega a luz
    t.px(x0 + 1, y0 + 2, "couro_luz", 1, y1 - y0 - 3)                   # a da esquerda também
    t.px(x0 + 1, y1 - 1, "couro_esc", x1 - x0 - 1, 1)                   # a de baixo e a da direita na sombra
    t.px(x1 - 1, y0 + 2, "couro_esc", 1, y1 - y0 - 3)
    for cx, cy, dx, dy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        t.px(cx, cy, (0, 0, 0, 0))                                       # o canto arredondado
        t.px(cx + dx, cy + dy, "couro_gasto")                            # o couro gasto na quina
        t.px(cx + 2 * dx, cy + dy, "couro_gasto")
        t.px(cx + dx, cy + 2 * dy, "couro_gasto")
    # dois riscos no couro, onde o livro ficou caído no buraco da parede
    t.px(x0 + 9, y1 - 3, "couro_esc", 4, 1)
    t.px(x1 - 14, y0 + 3, "couro_esc", 3, 1)


def bloco(t, x0, y0, x1, y1, fora, camadas, fundo_camadas=2):
    """O bloco de folhas de uma página: as folhas de baixo saindo um pouco pela beira de fora e pela de baixo (camadas),
    a página de cima por cima. `fora` é o lado da beira solta: -1 à esquerda, +1 à direita. Devolve o retângulo da
    página de cima."""
    for i in range(camadas, 0, -1):                                     # as folhas de baixo, uma por linha
        cor = "folha_beira_esc" if i % 2 else "folha_beira"
        if fora < 0:
            t.px(x0 - i, y0 + 1, cor, x1 - x0 + 1, y1 - y0 + 1)
        else:
            t.px(x0 + i, y0 + 1, cor, x1 - x0 + 1, y1 - y0 + 1)
    for i in range(fundo_camadas, 0, -1):
        t.px(x0, y1 + i - 1, "folha_beira_esc" if i % 2 else "folha_beira", x1 - x0 + 1, 1)
    t.px(x0, y0, "papel", x1 - x0 + 1, y1 - y0 + 1)
    return x0, y0, x1, y1


def grao(t, x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = GRAO[y % 16][x % 16]
            if c != ".":
                t.px(x, y, "papel_esc" if c == "e" else "papel_luz")


def dobra(t, x_meio, y0, y1):
    """A dobra do meio: a coluna do meio mais escura e o papel clareando em três passos de cada lado, sem faixa."""
    t.px(x_meio, y0, "dobra3", 1, y1 - y0 + 1)
    for i, cor in enumerate(("dobra2", "dobra1", "papel_esc"), start=1):
        t.px(x_meio - i, y0, cor, 1, y1 - y0 + 1)
        t.px(x_meio + i, y0, cor, 1, y1 - y0 + 1)


def curva(t, x_meio, y_cima, y_baixo):
    """As folhas descem para a dobra: junto dela, a beira de cima e a de baixo recuam num V curto (3, 2, 1 px), e o
    couro da capa aparece no vão, na sombra."""
    for dx, d in ((0, 3), (1, 2), (-1, 2), (2, 1), (-2, 1)):
        x = x_meio + dx
        t.px(x, y_cima, "couro_esc", 1, d)
        t.px(x, y_baixo - d + 1, "couro_esc", 1, d)


def umidade(t, x, y, espelhado):
    """A marca de umidade no canto de baixo de fora; (x, y) é o canto de baixo da página."""
    n = len(UMIDADE[0])
    for j, linha in enumerate(UMIDADE):
        yy = y - len(UMIDADE) + 1 + j
        for i, c in enumerate(linha):
            if c == ".":
                continue
            xx = x - n + 1 + i if not espelhado else x + n - 1 - i
            t.px(xx, yy, "umidade_linha" if c == "x" else "umidade")


def pauta(t, x0, y0, x1, y1, passo, margem):
    """O registro pautado: as linhas a cada `passo` px e a linha da margem (A)."""
    for y in range(y0, y1 + 1, passo):
        t.px(x0, y, "pauta", x1 - x0 + 1, 1)
    t.px(margem, y0 - 6, "margem", 1, y1 - y0 + 10)


def duas_paginas(nome, pautado, H):
    """A e B: 290 de largura, as duas páginas lado a lado sobre a capa; a altura pelo texto (a A, mais alta, pela
    pauta de 11 px: as duas entradas cabem nas linhas)."""
    W = 290
    t = Tela(W, H)
    capa(t, 0, 0, W - 3, H - 3)
    meio = (W - 3) // 2
    e = bloco(t, 8, 6, meio, H - 10, -1, 3)
    d = bloco(t, meio, 6, W - 11, H - 10, +1, 3)
    for (x0, y0, x1, y1) in (e, d):
        grao(t, x0, y0, x1, y1)
    umidade(t, e[0], e[3], True)
    umidade(t, d[2], d[3], False)
    dobra(t, meio, 6, H - 10)
    curva(t, meio, 6, H - 10)
    areas = {}
    for lado, (x0, y0, x1, y1) in (("esquerda", e), ("direita", d)):
        tx0 = x0 + (14 if lado == "esquerda" else 12)
        tx1 = x1 - (10 if lado == "esquerda" else 14)
        if pautado:
            pauta(t, x0 + 6, y0 + 19, x1 - 6, y1 - 8, 11, tx0 - 4)
        areas[lado] = [tx0, y0 + 10, tx1, y1 - 8]
    t.salvar(nome)
    return {"tamanho": [W, H], "paginas": areas, "pauta": {"primeira": e[1] + 19, "passo": 11} if pautado else None}


def pagina_proxima(nome, viradas):
    """C: 214×156. A página da direita inteira e, à esquerda da dobra, uma faixa da página anterior com o
    bloco das folhas já viradas (`viradas` camadas) e a capa por baixo."""
    W, H = 214, 156
    t = Tela(W, H)
    capa(t, 0, 0, W - 3, H - 3)
    dobra_x = 50
    e = bloco(t, 6 + viradas, 7, dobra_x, H - 10, -1, viradas)
    d = bloco(t, dobra_x, 7, W - 11, H - 10, +1, 3)
    for (x0, y0, x1, y1) in (e, d):
        grao(t, x0, y0, x1, y1)
    umidade(t, d[2], d[3], False)
    umidade(t, e[0], e[3], True)
    dobra(t, dobra_x, 7, H - 10)
    curva(t, dobra_x, 7, H - 10)
    t.salvar(nome)
    x0, y0, x1, y1 = d
    return {"tamanho": [W, H], "paginas": {"direita": [x0 + 14, y0 + 12, x1 - 12, y1 - 10]}, "pauta": None}


def main():
    areas = {
        "a": duas_paginas("livro-a.png", True, 170),
        "b": duas_paginas("livro-b.png", False, 134),
        "c1": pagina_proxima("livro-c-1.png", 2),
        "c2": pagina_proxima("livro-c-2.png", 6),
    }
    (SAIDA / "areas.json").write_text(json.dumps(areas, indent=1), encoding="utf-8")
    for k, v in areas.items():
        print(k, v)


if __name__ == "__main__":
    main()
