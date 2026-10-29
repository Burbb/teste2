"""O taverneiro da candidata H: o mesmo homem da G, do mesmo tamanho e na mesma pose (o desenho dela, `g/taverneiro.py`),
mais para cima e para a esquerda (`desenho.TAV`), com os refinamentos pedidos pelo Jean depois da G:
- a pele e a camisa sem o pontilhado da luz: um tom de luz só para a figura (`desenho.luz_lisa`), com a modelagem nos
  planos de luz e sombra do desenho;
- a barba, o pescoço, o peito e a gola ligados: a sombra da barba no pescoço, os lados do pescoço, o peito no V da
  gola com a linha do meio, as duas abas da gola deitadas para fora, acompanhando o V até o peitilho;
- as dobras das mangas acompanhando cada braço: arcos atravessando a manga, perpendiculares ao braço, acima do rolo
  da manga (onde o cotovelo dobra), com a luz em cima de cada dobra.
A identidade (o rosto, a calva, a barba, as roupas, as mãos, a caneca e o pano) não muda."""
import math

from g import taverneiro as GT
from tela_h2 import Tela

from . import desenho as D

COR = GT.COR
PELES = {COR["peleLuz"], COR["pele"], COR["peleSombra"]}
CAMISAS = {COR["camisaLuz"], COR["camisa"], COR["camisaSombra"]}
BARBAS = {COR["barbaLuz"], COR["barba"], COR["barbaSombra"]}


def gola(f):
    """O pescoço e a gola: a sombra que a barba faz no pescoço, os lados do pescoço, o V do peito até o peitilho com a
    linha do meio, as abas da gola deitadas dos dois lados do V."""
    cx = GT.CX
    # a sombra embaixo da barba, um pixel, onde a barba acaba sobre a pele
    for x in range(cx - 8, cx + 9):
        ys = [y for y in range(30, 46) if f.px.get((x, y)) in BARBAS]
        if ys and f.px.get((x, max(ys) + 1)) in PELES:
            f.p(x, max(ys) + 1, "peleEscura")
    # os lados do pescoço
    for y in range(39, 43):
        if f.px.get((cx - 7, y)) in PELES:
            f.p(cx - 7, y, "pele")
        if f.px.get((cx + 6, y)) in PELES:
            f.p(cx + 6, y, "peleSombra")
            f.p(cx + 7, y, "peleSombra")
    # o V do peito: da base do pescoço (y 42) ao ponto no peitilho (y 49)
    for y in range(42, 49):
        a, b = cx - 7 + (y - 42), cx + 7 - (y - 42)
        for x in range(a, b + 1):
            f.p(x, y, "pele" if x < cx else "peleSombra")
        # as abas da gola: dois pixels de linho deitados para fora, a sombra deles na camisa
        f.p(a - 1, y, "camisaLuz")
        f.p(a - 2, y, "camisaLuz")
        f.p(a - 3, y, "camisaSombra")
        f.p(b + 1, y, "camisa")
        f.p(b + 2, y, "camisa")
        f.p(b + 3, y, "camisaSombra")
    for y in range(44, 48):
        f.p(cx, y, "peleSombra")  # a linha do meio do peito
    # a gola de trás, subindo dos lados do pescoço
    for x, c in ((cx - 9, "camisaLuz"), (cx - 8, "camisaLuz"), (cx + 8, "camisa"), (cx + 9, "camisa")):
        f.p(x, 41, c)


def dobras(f):
    """As dobras das mangas, braço a braço: dois arcos atravessando a manga, perpendiculares ao braço, acima do rolo
    (onde o cotovelo dobra e o linho se junta), curvados para o cotovelo, com a luz em cima de cada um. Só sobre a
    manga."""
    for ombro, cotovelo in (((141, 50), (135, 66)), ((179, 50), (185, 66))):
        (ax, ay), (bx, by) = ombro, cotovelo
        comp = math.hypot(bx - ax, by - ay)
        dx, dy = (bx - ax) / comp, (by - ay) / comp
        nx, ny = -dy, dx  # atravessando o braço
        for t, curva in ((0.5, 1.2), (0.68, 1.6)):
            cx, cy = ax + (bx - ax) * t, ay + (by - ay) * t
            r = 7 - t
            for k in range(-8, 9):
                s = k / 8
                x = cx + nx * s * r * 0.8 + dx * curva * (1 - s * s)
                y = cy + ny * s * r * 0.8 + dy * curva * (1 - s * s)
                xi, yi = round(x - 0.5), round(y - 0.5)
                if f.px.get((xi, yi)) in CAMISAS and f.px.get((xi, yi - 1)) in CAMISAS:
                    f.p(xi, yi, "camisaSombra")
                    if f.px.get((xi, yi - 1)) != COR["camisaSombra"]:
                        f.p(xi, yi - 1, "camisaLuz")


def figura():
    f = GT.Figura()
    GT.tronco(f)
    GT.cabeca(f)
    GT.bracos(f)
    dobras(f)
    gola(f)
    GT.mao_direita(f)
    GT.caneca(f)
    GT.mao_esquerda(f)
    return f


def camada():
    """A figura no lugar da H (o corte no tampo de trás do balcão, como na G), com a luz lisa."""
    f = figura()
    t = Tela(D.QW, D.QH)
    dx, dy = D.TAV
    for (x, y), c in f.px.items():
        if y < D.G.BT:
            t.px(x + dx, y + dy, c)
    return D.luz_lisa(t)
