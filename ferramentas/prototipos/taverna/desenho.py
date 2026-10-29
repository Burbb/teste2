"""A taverna do Vau, candidata A: o interior desenhado na linguagem dos ambientes aprovados (a forja, a curandeira, o
templo), na grade de 320×96. A composição vem da referência do Jean (`ferramentas/arte/referencias/cenarios internos/
Taverna medieval entre fogo e sombras.png`), medida na escala do jogo com uma grade por cima e redesenhada aqui; a
imagem nunca é reduzida para virar fundo.

O que o jogo estabelece (o levantamento está no LEIA-ME): o taverneiro ("nem levanta os olhos"), a cama de palha e o
ensopado (Dormir), a bebida e os rumores, a despensa dos ratos (a abertura), o homem do canto (Morel, enquanto não foi
recrutado), as brigas e a queda de braço que a bebida pode virar. O resto é escolha desta candidata.

**O espaço, antes dos objetos** (a lição do templo; conferido sozinho em `so_o_espaco()`):
- o piso de tábuas, horizontal: as tábuas correm para o fundo, convergindo para VP (acima do quadro: a câmera olha um
  pouco de cima), e as emendas transversais ficam mais juntas no fundo;
- a parede de fundo encontra o piso em PAREDE, atrás de tudo; o balcão, a lareira, o barril e o banco encostam nela; as
  mesas e as pessoas pisam mais à frente, com chão entre elas e caminhos livres (a entrada, o corredor até o balcão, o
  pé da escada);
- a escala pela mesma régua do templo (`METRO`, `k`): quem está de pé no fundo tem ~26 px; as mesas da frente, ~1,4 vez
  maiores;
- a madeira do teto: a viga mestra apoiada em três esteios, cada um com as mãos-francesas para os dois vãos; a galeria
  dos quartos apoiada na escada e num esteio;
- as fontes de fogo com suporte: a lareira (a fornalha de pedra, a coifa, o caldeirão no gancho), as arandelas de
  ferro, as velas em castiçais nas mesas.

As camadas: `fundo()` (parado, com a luz), `fogo(i)` (a lareira, 4 quadros), `frente_moveis()` (as mesas e o balcão,
por cima dos corpos), `velas(i)` (4 quadros, por cima de tudo); as pessoas vêm de gente.py, em duas camadas cada (o
corpo, atrás dos móveis; as mãos, na frente)."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "hud", "forja", "h2"))
from tela_h2 import Tela  # noqa: E402  (a mesma camada de pixels das fontes da forja)

QW, QH = 320, 96
PAREDE = 56          # onde a parede de fundo encontra o piso
VP = (160, -18)      # para onde as tábuas convergem (acima do quadro)
METRO = 23.0         # 1 m em pixels na borda de baixo (k = 1)
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def k(y):
    """Quanto o que pisa em y encolhe (1 na borda de baixo), pela mesma conta das tábuas."""
    return (y - VP[1]) / (QH - VP[1])


def pont(x, y, n):
    return BAYER[(y & 3) * 4 + (x & 3)] < n


C = {
    # a parede: o reboco em cima, a pedra embaixo
    "reboco": "#3a332b", "rebocoLuz": "#4a4136", "rebocoSombra": "#2c2721",
    "pedra": "#3a352f", "pedraLuz": "#504940", "pedraSombra": "#25211d", "junta": "#2c2823",
    # a madeira
    "madeira": "#4a3424", "madeiraMeio": "#5c4330", "madeiraLuz": "#755840", "madeiraEsc": "#2a1d13",
    # o piso de tábuas
    "tabua": "#4a3828", "tabuaLuz": "#5a4532", "tabuaJunta": "#2e2218", "contato": "#1c1611",
    # o dia lá fora
    # o ferro, o barro, o estanho, a cera, o fogo
    "ferro": "#33343a", "ferroLuz": "#55575f", "ferroEsc": "#1c1d22",
    "barro": "#6a4230", "barroLuz": "#8a5a3c", "barroEsc": "#43281c",
    "estanho": "#7a7c82", "estanhoLuz": "#a4a6ac", "estanhoEsc": "#4e5056",
    "cera": "#d6ccae", "ceraEsc": "#a89e80", "chama": "#ffcc66", "chamaFora": "#e8782a", "chamaMiolo": "#fff2c4",
    "brasa": "#c8501a", "brasaEsc": "#7a2a10",
    "linho": "#b0a68e", "linhoLuz": "#d2c8b0", "linhoSombra": "#857b66",
    "pao": "#a8783a", "paoLuz": "#c89a52",
    "vulto": "#0b0a0a",
}


class Pincel:
    def __init__(self, t):
        self.t = t

    def __call__(self, x, y, w=1, h=1, cor=None):
        if cor:
            self.t.ret(int(round(x)), int(round(y)), int(round(w)), int(round(h)), C.get(cor, cor))

    def p(self, x, y, cor):
        self(x, y, 1, 1, cor)

    def linha(self, x0, y0, x1, y1, cor):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), cor)

    def grade(self, x0, y0, linhas, pal):
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])


# ---------------------------------------------------------------- o espaço
ESTEIOS = [46, 164, 244]   # os esteios da viga mestra (x da esquerda)


def paredes(px):
    """A parede de fundo: o reboco em cima, a barra de pedra embaixo (a meia altura), o rodapé no encontro com o piso;
    a viga mestra no alto, nos três esteios, com as mãos-francesas retas para cada vão."""
    px(0, 0, QW, PAREDE, "reboco")
    for x, y, w in [(30, 12, 8), (96, 8, 6), (186, 14, 7), (272, 30, 6), (130, 20, 5)]:
        px(x, y, w, 1, "rebocoLuz")
    px(0, 38, QW, PAREDE - 38, "pedra")
    px(0, 38, QW, 1, "pedraLuz")
    for y in range(43, PAREDE, 5):
        for x in range(((y // 5) % 2) * 7 - 14, QW, 14):
            px(x, y, 14, 1, "junta")
            px(x, y, 1, 5, "junta")
    px(0, PAREDE - 2, QW, 2, "pedraSombra")
    # a viga mestra e os esteios
    px(0, 0, QW, 3, "madeiraEsc")
    px(0, 3, QW, 4, "madeira")
    px(0, 3, QW, 1, "madeiraLuz")
    px(0, 6, QW, 1, "madeiraEsc")
    for x0 in ESTEIOS:
        px(x0, 7, 5, PAREDE - 7, "madeira")
        px(x0, 7, 1, PAREDE - 7, "madeiraLuz")
        px(x0 + 4, 7, 1, PAREDE - 7, "madeiraEsc")
        px(x0 - 1, PAREDE - 2, 7, 2, "pedraLuz")       # a sapata de pedra
        px(x0 - 2, PAREDE, 9, 1, "contato")
        for lado in (-1, 1):                            # as mãos-francesas, 45°, para os dois vãos
            for i in range(7):
                x = x0 + 5 + i if lado > 0 else x0 - 2 - i
                px(x, 14 - i, 2, 1, "madeira")
                px(x, 15 - i, 2, 1, "madeiraEsc")


FILAS = [PAREDE, 58, 61, 65, 70, 76, 83, 91]  # as emendas transversais das tábuas: mais juntas no fundo


def piso(px):
    """O piso de tábuas, contínuo da parede até a borda de baixo: as tábuas correm para o fundo (as juntas
    longitudinais convergindo para VP); as emendas transversais (FILAS), desencontradas de uma tábua para a outra."""
    px(0, PAREDE, QW, QH - PAREDE, "tabua")
    xs = list(range(-200, QW + 220, 14))  # o pé de cada junta na borda de baixo
    for y in range(PAREDE, QH):
        kk = k(y)
        for xb in xs:
            x = VP[0] + (xb - VP[0]) * kk
            if 0 <= x < QW:
                px.p(round(x), y, "tabuaJunta")
    for i, y in enumerate(FILAS[1:], 1):  # as emendas: entre duas juntas, uma tábua sim, outra não, em cada fila
        kk = k(y)
        for j, xb in enumerate(xs[:-1]):
            if (j + i) % 2:
                continue
            x0 = round(VP[0] + (xb - VP[0]) * kk)
            x1 = round(VP[0] + (xs[j + 1] - VP[0]) * kk)
            px(x0, y, x1 - x0, 1, "tabuaJunta")
            px(x0, y + 1, x1 - x0, 1, "tabuaLuz")


def entrada(px):
    """A porta da rua, à esquerda: o vão de pedra em arco e a porta de tábuas fechada nele, com as duas ferragens e a
    argola; a soleira de pedra. Fechada, a porta não diz a hora nem o tempo lá fora (a vila
    mostra a noite e a chuva; uma rua de dia na porta aberta contradizia as duas)."""
    x0, x1, y0 = 12, 30, 24
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    for y in range(y0 - round(r), PAREDE):               # as tábuas em pé, presas no arco
        for x in range(x0, x1):
            if y < y0 and math.hypot(x + 0.5 - cx, (y0 - y - 0.5)) > r:
                continue
            junta = (x - x0) % 4 == 3
            px.p(x, y, "madeiraEsc" if junta else "madeiraLuz" if (x - x0) % 4 == 0 else "madeiraMeio")
    for yy in (y0 - 2, PAREDE - 9):                     # as ferragens, de lado a lado
        px(x0, yy, x1 - x0, 2, "ferro")
        px(x0, yy, x1 - x0, 1, "ferroLuz")
    px(x1 - 5, 38, 3, 3, "ferro")                       # a argola, do lado da fechadura
    px(x1 - 4, 39, 1, 1, "madeiraEsc")
    for xx in (x0 - 3, x1):
        px(xx, y0, 3, PAREDE - y0, "pedraLuz")
        px(xx + 2, y0, 1, PAREDE - y0, "pedra")
    for y in range(y0 - round(r) - 3, y0):
        for x in range(x0 - 3, x1 + 3):
            d = math.hypot(x + 0.5 - cx, (y0 - y - 0.5))
            if r <= d < r + 3:
                px.p(x, y, "pedraLuz")
    px(x0 - 3, PAREDE, x1 - x0 + 6, 1, "pedraLuz")     # a soleira
    px(x0 - 3, PAREDE + 1, x1 - x0 + 6, 1, "pedraSombra")


BALCAO = (68, 152, 41)  # o balcão: de x0 a x1, o tampo em y


def balcao(px):
    """O balcão de tábuas encostado na parede (o tampo grosso aceso, a frente de tábuas, o rodapé), as prateleiras
    atrás com as canecas de estanho e as jarras de barro, o barril no cavalete com a torneira na ponta da esquerda e os
    dois banquinhos altos na frente, de pé no piso."""
    x0, x1, yt = BALCAO
    # as prateleiras na parede, atrás do balcão: duas tábuas em mãos de ferro, com canecas e jarras em fila
    for y in (16, 27):
        px(x0 + 8, y, x1 - x0 - 16, 2, "madeiraMeio")
        px(x0 + 8, y, x1 - x0 - 16, 1, "madeiraLuz")
        for xx in (x0 + 10, x1 - 12):
            px(xx, y + 2, 1, 3, "ferro")
    for i, xx in enumerate(range(x0 + 11, x1 - 10, 7)):  # em cima: canecas e jarras, alternadas
        if i % 2:
            px(xx, 10, 4, 6, "barro"); px(xx, 10, 1, 6, "barroLuz"); px(xx + 1, 9, 2, 1, "barroEsc")
        else:
            px(xx, 12, 3, 4, "estanho"); px(xx, 12, 1, 4, "estanhoLuz"); px(xx + 3, 13, 1, 2, "estanhoEsc")
    for xx in range(x0 + 12, x1 - 10, 5):                # embaixo: as canecas emborcadas
        px(xx, 23, 3, 4, "estanho"); px(xx, 23, 1, 4, "estanhoLuz")
    # o barril deitado no cavalete baixo, à esquerda do balcão, com o tampo redondo para a sala e a torneira embaixo
    bcx, bcy, br = x0 - 7, 43, 5.6
    for y in range(round(bcy - br) - 1, round(bcy + br) + 1):
        for x in range(round(bcx - br) - 1, round(bcx + br) + 1):
            d = math.hypot(x + 0.5 - bcx, y + 0.5 - bcy)
            if d <= br:
                junta = (y - round(bcy - br)) % 3 == 2           # as juntas das tábuas do tampo, deitadas
                cor = "ferro" if d > br - 1.1 else "madeiraMeio" if junta else "madeiraLuz"
                if d > br - 1.1 and y < bcy - 2:
                    cor = "ferroLuz"                             # o aro de ferro, aceso em cima
                px.p(x, y, cor)
    px(round(bcx) - 1, round(bcy) + 2, 3, 2, "ferro")            # a torneira de ferro, embaixo do tampo
    px(round(bcx) - 1, round(bcy) + 2, 3, 1, "ferroLuz")
    for xx in (round(bcx - br) + 1, round(bcx + br) - 2):       # o cavalete: duas pernas curtas até o piso
        px(xx, round(bcy + br) - 1, 2, PAREDE - round(bcy + br) + 1, "madeira")
        px(xx, round(bcy + br) - 1, 1, PAREDE - round(bcy + br) + 1, "madeiraLuz")
        px(xx - 1, PAREDE, 4, 1, "contato")
    # o balcão: o tampo (o claro de cima e a espessura), a frente de tábuas, o rodapé no piso
    px(x0 - 1, yt, x1 - x0 + 2, 1, "madeiraLuz")
    px(x0 - 1, yt + 1, x1 - x0 + 2, 2, "madeiraMeio")
    px(x0 - 1, yt + 3, x1 - x0 + 2, 1, "madeiraEsc")
    px(x0, yt + 4, x1 - x0, PAREDE - yt - 4, "madeira")
    for xx in range(x0 + 4, x1, 6):
        px(xx, yt + 4, 1, PAREDE - yt - 4, "madeiraEsc")
    px(x0, PAREDE - 2, x1 - x0, 2, "madeiraEsc")
    px(x0 - 1, PAREDE, x1 - x0 + 2, 1, "contato")
    # os banquinhos altos na frente do balcão, de pé no piso logo à frente
    for xx in (84, 112, 136):
        py = PAREDE + 2
        px(xx, py - 9, 7, 2, "madeiraMeio")
        px(xx, py - 9, 7, 1, "madeiraLuz")
        for pe in (xx + 1, xx + 5):
            px(pe, py - 7, 1, 7, "madeira")
        px(xx, py, 7, 1, "contato")


LAREIRA = (196, 240)  # a lareira: de x0 a x1


def lareira(px):
    """A lareira de pedra encostada na parede: o peito de pedra até o teto, a boca com o lintel, o fogo e o caldeirão
    (camada fogo) preso na cremalheira; a lenha empilhada ao lado, no piso."""
    x0, x1 = LAREIRA
    px(x0 + 4, 7, x1 - x0 - 8, 22, "pedra")                 # a chaminé, mais estreita, até a viga
    px(x0 + 4, 7, 1, 22, "pedraLuz")
    px(x0, 29, x1 - x0, PAREDE - 29, "pedraLuz")            # o peito, mais largo
    for y in range(33, PAREDE, 5):
        for x in range(x0 + ((y // 5) % 2) * 5, x1, 10):
            px(x, y, 10, 1, "pedra")
            px(x, y, 1, 5, "pedra")
    px(x0 - 2, 29, x1 - x0 + 4, 3, "madeiraMeio")           # a cornija de madeira
    px(x0 - 2, 29, x1 - x0 + 4, 1, "madeiraLuz")
    b0, b1, bt = x0 + 8, x1 - 8, 40                          # a boca
    px(b0, bt, b1 - b0, PAREDE - bt, "vulto")
    px(b0 - 1, bt - 2, b1 - b0 + 2, 2, "pedra")              # o lintel
    px(b0 - 1, bt - 2, b1 - b0 + 2, 1, "pedraLuz")
    px(b0, PAREDE - 2, b1 - b0, 2, "brasaEsc")               # a cinza e as brasas no chão da boca
    px(x0 - 1, PAREDE, x1 - x0 + 2, 1, "contato")
    # a lenha empilhada à direita da lareira, no piso: as pontas das achas, em pirâmide (4, 3, 2)
    lx = x1 + 1
    for i, n in enumerate((4, 3, 2)):
        y = PAREDE - 3 - i * 3
        for j in range(n):
            xx = lx + i * 1 + j * 3 + (i > 0)
            px(xx, y, 3, 3, "madeiraEsc")
            px(xx, y, 2, 2, "madeiraLuz")
            px.p(xx + 1, y + 1, "madeiraMeio")
    px(lx, PAREDE, 13, 1, "contato")


ESCADA = (250, 56, 304, 14)  # a escada: do pé (x, y) ao alto (x, y)


def escada(px):
    """A escada para os quartos: a viga lateral (o banzo) subindo do piso até a galeria, os degraus (o piso claro, a
    frente escura), os balaústres e o corrimão; a galeria em cima, apoiada no alto da escada e num esteio, com a porta
    de um quarto; embaixo da escada, o canto mais reservado."""
    (xa, ya, xb, yb) = ESCADA
    n = 12
    for i in range(n):                                  # os degraus
        x = xa + (xb - xa) * i / n
        y = ya - (ya - yb) * (i + 1) / n
        w = (xb - xa) / n + 1
        px(x, y, w + 2, 1, "madeiraLuz")
        px(x, y + 1, w + 2, 2, "madeiraEsc")
    for t in range(0, 101):                             # o banzo (a viga da escada), por baixo dos degraus
        x = xa + (xb - xa) * t / 100
        y = ya - (ya - yb) * t / 100
        px(x, y + 3, 2, 2, "madeira")
    for i in range(0, n + 1, 2):                        # os balaústres e o corrimão
        x = xa + (xb - xa) * i / n
        y = ya - (ya - yb) * i / n
        px(x, y - 7, 1, 7, "madeiraMeio")
    px.linha(xa, ya - 8, xb, yb - 8, "madeiraLuz")
    # a galeria: o piso dela (a viga) e o guarda-corpo, de ponta a ponta à direita, com a porta de um quarto na parede
    gy = yb
    px(xb - 6, gy, QW - xb + 6, 3, "madeira")
    px(xb - 6, gy, QW - xb + 6, 1, "madeiraLuz")
    for x in range(xb - 4, QW, 4):
        px(x, gy - 7, 1, 7, "madeiraMeio")
    px(xb - 6, gy - 8, QW - xb + 6, 1, "madeiraLuz")
    px(306, 0, 12, gy, "madeiraEsc")                    # a porta do quarto, no alto
    px(307, 0, 10, gy, "madeira")
    px(311, 0, 1, gy, "madeiraEsc")
    px(315, gy - 7, 1, 2, "ferroLuz")
    px(QW - 6, gy + 3, 4, PAREDE - gy - 3, "madeira")   # o esteio da galeria, no canto
    px(QW - 6, gy + 3, 1, PAREDE - gy - 3, "madeiraLuz")
    px(QW - 7, PAREDE, 6, 1, "contato")


def arandela(px, x, base):
    """A arandela de ferro na parede: a chapa, o braço, o copo e a vela (a chama vem na camada velas, em (x, base - 7))."""
    px(x + 2, base - 1, 2, 4, "ferro")
    px(x + 2, base - 1, 1, 4, "ferroLuz")
    px(x - 1, base, 4, 1, "ferroLuz")
    px(x - 1, base + 1, 4, 1, "ferro")
    px(x, base - 5, 2, 5, "cera")
    px(x + 1, base - 5, 1, 5, "ceraEsc")


ARANDELAS = [(42, 34), (176, 34), (262, 44)]


def luzes_de_parede(px):
    for x, b in ARANDELAS:
        arandela(px, x, b)


# ---------------------------------------------------------------- as mesas (o fundo tem a mesa; os grupos a refazem)
def mesa(px, x0, x1, pe, alto, vela):
    """Uma mesa de tábuas de pé no piso em `pe`: o tampo (o claro de cima e a espessura), as pernas, a travessa, a
    sombra de contato; a vela no castiçal de barro em `vela` (a chama vem na camada velas) ou, sem vela (a mesa do
    jogo), o tabuleiro no meio."""
    kk = k(pe)
    yt = round(pe - alto * METRO * kk)
    px(x0, yt, x1 - x0, 1, "madeiraLuz")
    px(x0, yt + 1, x1 - x0, 2, "madeiraMeio")
    px(x0, yt + 3, x1 - x0, 1, "madeiraEsc")
    for xx in (x0 + 1, x1 - 3):
        px(xx, yt + 4, 2, pe - yt - 4, "madeira")
        px(xx, yt + 4, 1, pe - yt - 4, "madeiraLuz")
        px(xx - 1, pe, 4, 1, "contato")
    px(x0 + 3, pe - 4, x1 - x0 - 6, 1, "madeiraEsc")
    cx = (x0 + x1) // 2
    if vela is not None:
        px(vela - 1, yt - 1, 4, 1, "barro")
        px(vela, yt - 5, 2, 4, "cera")
        px(vela + 1, yt - 5, 1, 4, "ceraEsc")
    else:  # o tabuleiro: a tábua quadriculada deitada no tampo, com as peças
        px(cx - 4, yt - 1, 9, 1, "linhoSombra")
        for xx in range(cx - 4, cx + 5, 2):
            px.p(xx, yt - 1, "madeiraEsc")
        for xx in (cx - 3, cx + 2):
            px.p(xx, yt - 2, "linhoLuz")
        px.p(cx + 3, yt - 2, "madeiraEsc")
    return yt


MESAS = {  # (x0, x1, onde pisa, altura em m): as três mesas da frente e a do canto de Morel
    "esquerda": (40, 88, 86, 0.75), "meio": (146, 172, 86, 0.75), "direita": (216, 264, 86, 0.75),
    "canto": (276, 298, 58, 0.75),
}


def vela_da_mesa(nome):
    """Onde fica a vela de cada mesa: no meio; na do canto, na ponta (o rosto de Morel fica livre); a do jogo não tem."""
    x0, x1 = MESAS[nome][:2]
    return {"meio": None, "canto": x0 + 3}.get(nome, (x0 + x1) // 2)


def mesas(px):
    return {nome: mesa(px, x0, x1, pe, alto, vela_da_mesa(nome)) for nome, (x0, x1, pe, alto) in MESAS.items()}


def velas_das_mesas():
    """Onde ficam as chamas das velas das mesas (em cima do castiçal)."""
    r = []
    for nome, (x0, x1, pe, alto) in MESAS.items():
        if vela_da_mesa(nome) is None:
            continue
        yt = round(pe - alto * METRO * k(pe))
        r.append((vela_da_mesa(nome), yt - 7))
    return r


# ---------------------------------------------------------------- a luz
LUZES = [(218, 48, 34, 1.0), (42, 30, 12, 0.5), (176, 30, 12, 0.5), (262, 40, 12, 0.5)]


def luz(t):
    """Longe do fogo e das velas, a sala escurece em degraus pontilhados; perto, o halo quente."""
    for y in range(QH):
        for x in range(QW):
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.3)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.6)))
            for vx, vy in velas_das_mesas():
                d = math.hypot(x - vx, (y - vy) * 1.3)
                perto = max(perto, 0.45 * max(0.0, 1 - d / 22))
            escuro = max(0.0, 0.55 - perto * 1.1)
            f5 = escuro / 0.55 * 4
            n = int(f5) + (1 if pont(x, y, int((f5 % 1) * 16)) else 0)
            if n:
                t.mistura(x, y, (4, 3, 2), 0.55 * n / 4)
            for lx, ly, r, f in LUZES:
                d2 = ((x - lx) ** 2 + ((y - ly) * 1.3) ** 2) / (r * r)
                if d2 < 1:
                    al = 0.2 if d2 < 0.08 else 0.12 if d2 < 0.3 else 0.07 if d2 < 0.65 else 0.035
                    t.mistura(x, y, (255, 160, 80), al * f)


ALCAPAO = (104, 120, 60, 63)  # o alçapão da despensa, no caminho livre na frente do balcão: x0, x1, y0 (longe), y1


def alcapao(px):
    """O alçapão da despensa, fechado, deitado no piso na frente do balcão: as tábuas na perspectiva do piso,
    a moldura escura, as dobradiças do lado da parede e a argola de ferro para puxar."""
    x0, x1, y0, y1 = ALCAPAO
    for y in range(y0, y1 + 1):
        a = round(x0 + (y1 - y) * 0.4)
        b = round(x1 - (y1 - y) * 0.4)
        px(a, y, b - a, 1, "madeiraEsc" if y in (y0, y1) else "madeiraMeio")
        px.p(a, y, "madeiraEsc")
        px.p(b - 1, y, "madeiraEsc")
    for xx in range(x0 + 4, x1 - 2, 4):                 # as juntas das tábuas, para o fundo
        px(xx, y0 + 1, 1, y1 - y0 - 1, "madeira")
    px(x0 + 3, y0, 2, 1, "ferro")                       # as dobradiças
    px(x1 - 5, y0, 2, 1, "ferro")
    cx = (x0 + x1) // 2
    px(cx - 1, y1 - 1, 3, 1, "ferroLuz")                 # a argola
    px.p(cx, y1 - 2, "ferro")
    px(x0, y1 + 1, x1 - x0, 1, "contato")


def so_o_espaco():
    """O espaço sozinho (as paredes, o piso, a madeira do teto), sem os móveis: a conferência do piso."""
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    piso(px)
    return t


def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    piso(px)
    entrada(px)
    balcao(px)
    lareira(px)
    escada(px)
    alcapao(px)
    luzes_de_parede(px)
    mesas(px)
    luz(t)
    return t


def fogo(i):
    """O fogo da lareira (as brasas e as línguas baixas, 4 quadros): atrás de quem se aquece na frente dela."""
    t = Tela(QW, QH)
    px = Pincel(t)
    x0, x1 = LAREIRA
    b0, b1 = x0 + 8, x1 - 8
    cx = (b0 + b1) // 2
    base = PAREDE - 4                                       # as chamas nascem da lenha, em cima das brasas
    # as línguas: (o centro, a altura, para onde a ponta pende), cada quadro com outras alturas
    linguas = [[(cx - 7, 5, 0), (cx - 3, 9, 1), (cx + 1, 11, 0), (cx + 5, 8, -1), (cx + 8, 4, 0)],
               [(cx - 7, 6, 1), (cx - 3, 8, 0), (cx + 1, 9, -1), (cx + 5, 10, 0), (cx + 8, 5, -1)],
               [(cx - 7, 4, 0), (cx - 3, 10, -1), (cx + 1, 10, 1), (cx + 5, 7, 0), (cx + 8, 6, 0)],
               [(cx - 7, 5, -1), (cx - 3, 9, 0), (cx + 1, 12, 0), (cx + 5, 8, 1), (cx + 8, 4, 1)]][i]
    for x, h, pende in linguas:
        for r in range(h):                                  # de baixo para cima, afinando
            y = base - r
            f = r / h
            dx = pende if f > 0.6 else 0
            larg = 4 if f < 0.35 else 3 if f < 0.6 else 2 if f < 0.85 else 1
            x0_ = x - larg // 2 + dx
            px(x0_, y, larg, 1, "chamaFora")
            if larg >= 3:
                px(x0_ + 1, y, larg - 2, 1, "chama")
            if r < 3 and h >= 8:
                px.p(x, y, "chamaMiolo")
    # a lenha atravessada na boca, com as pontas em brasa
    px(b0 + 3, PAREDE - 3, b1 - b0 - 6, 2, "madeiraEsc")
    px(b0 + 3, PAREDE - 3, 2, 2, "brasa")
    px(b1 - 5, PAREDE - 3, 2, 2, "brasa")
    for xx in range(b0 + 6, b1 - 6, 4):
        px.p(xx + i % 2, PAREDE - 2, "brasa")
    # a cremalheira de ferro e o caldeirão, na frente das chamas
    bt = 40
    px(cx, bt, 1, 4, "ferro")
    px(cx - 4, bt + 4, 9, 1, "ferroLuz")
    px(cx - 4, bt + 5, 9, 4, "ferro")
    px(cx - 3, bt + 9, 7, 1, "ferroEsc")
    return t


def velas(i):
    """As chamas das velas das arandelas e das mesas (4 quadros, cada uma no seu passo): por cima de tudo."""
    t = Tela(QW, QH)
    px = Pincel(t)
    velas = [(x, b - 7) for x, b in ARANDELAS] + velas_das_mesas()
    for j, (x, y) in enumerate(velas):
        f = (i + j * 3) % 4
        alto = 3 if f in (0, 2) else 2 if f == 1 else 4
        px(x, y - alto + 2, 1, alto, "chamaFora")
        px.p(x, y + 1, "chama")
        if alto >= 3:
            px.p(x, y, "chamaMiolo" if f == 3 else "chama")
    return t


def frente_moveis():
    """Os móveis que ficam na frente dos corpos de quem está atrás deles (as mesas, o balcão): uma Tela com só os
    pixels deles, tirados do fundo já iluminado. A tela desenha esta camada entre os corpos e as mãos."""
    mascara = Tela(QW, QH)
    px = Pincel(mascara)
    mesas(px)
    x0, x1, yt = BALCAO
    px(x0 - 1, yt, x1 - x0 + 2, PAREDE - yt + 1, "vulto")
    f = fundo().imagem()
    m = mascara.imagem().load()
    a = f.load()
    t = Tela(QW, QH)
    for y in range(QH):
        for x in range(QW):
            if m[x, y][3]:
                t.px(x, y, "#%02x%02x%02x" % a[x, y][:3])
    return t
