"""A candidata G da taverna (29/10/2026): o balcão de perto, de frente, como quem está sentado diante dele. A
composição vem da referência "Taverneiro desconfiado atrás do balcão-1" (`ferramentas/arte/referencias/cenarios
internos`); o acabamento, das cenas aprovadas (a forja, a curandeira, o templo): cada material em dois ou três tons
chapados, a pedra em blocos com as juntas um tom abaixo, a madeira com a aresta acesa e o lado escuro, o metal com o
brilho de um pixel, quase sem contorno preto, a luz feita por cima. Nada vem da redução da imagem: cada coisa é
desenhada aqui, na grade do jogo (320×96, o pixel das outras cenas).

O espaço, de trás para a frente:
- a parede de pedra, a viga do teto e os dois esteios (o da lareira e o da despensa);
- à esquerda, o canto de preparo: a lareira com a verga, o caldeirão na corrente da cremalheira, a lenha e o fogo; a
  frigideira e a concha penduradas;
- atrás do taverneiro, a prateleira alta (as jarras e as canecas à esquerda, as garrafas à direita, o vão atrás da
  cabeça) e a bancada de trabalho (o barril deitado no berço com a torneira, o pão e o queijo na tábua, a jarra); as
  canecas penduradas embaixo da prateleira, as linguiças e o alho na viga;
- à direita, o lampião no esteio e a porta da despensa;
- na frente, o balcão de um lado a outro (o tampo visto um pouco de cima, a borda grossa, as tábuas da frente), a
  caneca de um freguês, e as silhuetas dos fregueses nos cantos.

As camadas (de baixo para cima, as da fonte em Aseprite): `fundo` (a sala parada), `fogo` (4 quadros, as chamas),
`lampiao` (4 quadros, a chama do lampião), `caldeirao` (o caldeirão, a corrente e a lenha da frente: na frente das
chamas), `taverneiro` (taverneiro.py) e `frente` (o balcão e os fregueses). Cada uma já vem com a luz."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "hud", "forja", "h2"))

from tela_h2 import Tela  # noqa: E402

QW, QH = 320, 96
BT = 74   # a borda de trás do tampo do balcão (onde o corpo do taverneiro some)
BB = 66   # o tampo da bancada de trabalho, atrás dele
PR = 27   # o tampo da prateleira alta
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def pont(x, y, n):
    return BAYER[(y & 3) * 4 + (x & 3)] < n


C = {
    # a pedra (a da forja, um pouco mais quente) e o escuro
    "parede": "#221e1b", "junta": "#171412", "pedra": "#2e2925", "pedraLuz": "#4a423a", "pedraSombra": "#141210",
    # a madeira da estrutura (os esteios, a viga, a prateleira, a bancada)
    "madeira": "#3a2a1c", "madeiraMeio": "#4a3624", "madeiraLuz": "#5e4632", "madeiraEsc": "#1c140d",
    # o balcão: uma madeira mais quente e mais clara (o plano mais perto)
    "balcao": "#5a3e26", "balcaoLuz": "#76522f", "balcaoBrilho": "#946a3c", "balcaoEsc": "#3c2918",
    "balcaoJunta": "#281b10",
    # o ferro e o estanho das canecas
    "ferro": "#3a3c42", "ferroLuz": "#5e6068", "ferroBrilho": "#9a9ca6", "ferroEsc": "#24252a",
    "estanho": "#6e7078", "estanhoLuz": "#9a9ca4", "estanhoBrilho": "#cfd1d6", "estanhoEsc": "#45474e",
    # o latão da torneira
    "latao": "#8a6a26", "lataoLuz": "#c09a40", "lataoEsc": "#5a4418",
    # a louça (o grés claro com a faixa azul) e o barro
    "louca": "#b0a48c", "loucaLuz": "#d0c6ae", "loucaSombra": "#80765f", "azul": "#3e5470",
    "barro": "#7a4a2c", "barroLuz": "#9c6438", "barroSombra": "#4c2c18",
    # o vidro das garrafas, a rolha e o vime
    "vidro": "#23402c", "vidroLuz": "#3c6a44", "vidroBrilho": "#8ab68a",
    "ambar": "#5a3214", "ambarLuz": "#8a5222", "ambarBrilho": "#d09050", "rolha": "#a07a50",
    "vime": "#76592e", "vimeLuz": "#9a7a42", "vimeEsc": "#4a3818",
    # a comida: o pão, o queijo, as linguiças, o alho
    "pao": "#9e5c28", "paoLuz": "#c4843e", "paoEsc": "#68381a", "miolo": "#d4b67e",
    "queijo": "#d0a440", "queijoLuz": "#ecca66", "queijoEsc": "#9a7426",
    "linguica": "#6a2418", "linguicaLuz": "#943a26", "linguicaEsc": "#42140e",
    "alho": "#c8bea6", "alhoLuz": "#e6dec8", "alhoEsc": "#8e8470", "barbante": "#8a7a58",
    # a lareira: a fuligem, as brasas, a lenha
    "fuligem": "#120f0e", "brasa": "#c8501a", "brasaEsc": "#7a2a10", "lenha": "#3a2416", "lenhaLuz": "#5a3a22",
    "cinza": "#4a4440",
    # os fregueses da frente
    "vulto": "#0b0a0b", "vultoMeio": "#151314", "vultoLuz": "#2a221c",
}
FOGO = ["#3f1006", "#7a240a", "#b8400f", "#e86a18", "#ff9a30", "#ffcc66", "#fff2c4"]


class Pincel:
    def __init__(self, t):
        self.t = t

    def __call__(self, x, y, w=1, h=1, cor=None):
        if cor:
            self.t.ret(int(round(x)), int(round(y)), w, h, C.get(cor, cor))

    def p(self, x, y, cor):
        self(x, y, 1, 1, cor)

    def deslocado(self, dx):
        """O mesmo pincel com tudo dx px para o lado (o caldeirão no eixo da boca)."""
        return _Deslocado(self.t, dx)

    def linha(self, x0, y0, x1, y1, cor):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), cor)

    def elipse(self, cx, cy, rx, ry, cor):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                    self.p(x, y, cor)

    def grade(self, x0, y0, linhas, pal):
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])


class _Deslocado(Pincel):
    def __init__(self, t, dx):
        super().__init__(t)
        self.dx = dx

    def __call__(self, x, y, w=1, h=1, cor=None):
        super().__call__(x + self.dx, y, w, h, cor)


# ---------------------------------------------------------------- a sala: a parede, a viga, os esteios
def sala(px):
    """A parede de pedra em fiadas de 6 px (as juntas desencontradas, um tom abaixo), a viga do teto com os caibros e a
    sombra embaixo."""
    px(0, 0, QW, BT, "parede")
    for y in range(9, BT, 6):
        for x in range(((y // 6) % 2) * 7 - 14, QW, 14):
            px(x, y, 14, 1, "junta")
            px(x, y, 1, 6, "junta")
    for x, y in [(70, 15), (112, 39), (196, 9), (238, 45), (126, 51), (210, 51), (300, 9), (8, 9)]:
        px(x + 1, y + 1, 12, 1, "pedra")
    # a viga do teto e as pontas dos caibros
    px(0, 0, QW, 6, "madeiraEsc")
    px(0, 5, QW, 1, "madeira")
    px(0, 6, QW, 1, "pedraSombra")
    for x in range(14, QW, 40):
        px(x, 0, 6, 5, "madeira")
        px(x, 0, 1, 5, "madeiraLuz")
        px(x + 5, 0, 1, 5, "madeiraEsc")


def esteio(px, x0, w):
    """Um esteio do teto ao balcão: a face da frente, a aresta acesa à esquerda e o lado escuro, as fendas."""
    px(x0, 0, w, BT, "madeira")
    px(x0, 0, 1, BT, "madeiraLuz")
    px(x0 + w - 2, 0, 2, BT, "madeiraEsc")
    for y in (14, 40, 58):
        px(x0 + w // 2, y, 1, 6, "madeiraEsc")


# ---------------------------------------------------------------- à esquerda: a lareira e o canto de preparo
BOCA = (12, 44, 36, 64)  # a boca por dentro: x0, x1, o alto, o leito
DX_FOGO = -3             # o caldeirão e o fogo, no eixo da boca


def lareira(px):
    """A lareira de pedra: as ombreiras com a aresta clara, a verga de madeira com a prateleirinha, a chaminé até a viga,
    a boca com o fundo de fuligem e as faces de dentro, a laje do leito; a cremalheira presa na ombreira de cá."""
    x0, x1, yt, yl = BOCA
    # a chaminé e as ombreiras, em pedra mais clara (blocos grandes)
    px(6, 7, 48, yl + 4 - 7, "pedra")
    for y in range(7, yl + 4):
        if (y - 7) % 7 == 6:
            px(6, y, 48, 1, "junta")
        else:
            off = 0 if ((y - 7) // 7) % 2 else 6
            for x in range(6 + off, 54, 12):
                px(x, y, 1, 1, "junta")
    px(6, 7, 1, yl - 3, "pedraLuz")
    px(53, 7, 1, yl - 3, "pedraSombra")
    # a verga de madeira, com a prateleirinha em cima (o pote de sal, a vela apagada)
    px(4, 28, 52, 5, "madeira")
    px(4, 28, 52, 1, "madeiraLuz")
    px(4, 32, 52, 1, "madeiraEsc")
    px(10, 23, 6, 5, "barro")
    px(10, 23, 2, 5, "barroLuz")
    px(11, 22, 4, 1, "barroSombra")
    px(40, 24, 4, 4, "louca")
    px(40, 24, 1, 4, "loucaLuz")
    px(39, 27, 6, 1, "loucaSombra")
    # a boca: o fundo de fuligem, as faces de dentro (mais largas embaixo) com a aresta quente
    px(x0, yt, x1 - x0, yl - yt, "fuligem")
    for y in range(yt, yl):
        k = (y - yt) * 3 // (yl - yt)
        px(x0, y, 2 + k, 1, "cinza")
        px(x1 - 2 - k, y, 2 + k, 1, "pedraSombra")
        px(x0 + 2 + k, y, 1, 1, "brasaEsc")
    # o arco raso de pedras em cima da boca
    for x in range(x0 - 1, x1 + 1, 4):
        px(x, yt - 3, 4, 3, "pedraLuz" if (x // 4) % 2 else "pedra")
        px(x, yt - 1, 4, 1, "pedraSombra")
    # a laje do leito: o piso claro e a frente
    px(4, yl, 52, 2, "pedraLuz")
    px(4, yl + 2, 52, 2, "pedraSombra")
    # as brasas e a cinza no leito
    for x in range(x0 + 3, x1 - 3):
        px.p(x, yl - 1, "brasa" if x % 3 else "brasaEsc")
    px(x0 + 2, yl - 1, 2, 1, "cinza")


def utensilios(px):
    """A concha e a frigideira penduradas em pregos na pedra, dos dois lados da boca."""
    # a concha, à esquerda: o prego, o cabo e a cuba
    px(2, 34, 2, 1, "ferroLuz")
    px(2, 35, 1, 14, "ferro")
    px(3, 35, 1, 14, "ferroEsc")
    px(1, 49, 4, 3, "ferro")
    px(1, 49, 4, 1, "ferroLuz")
    px(2, 52, 2, 1, "ferroEsc")
    # a frigideira, entre a boca e o esteio: o prego, o cabo para cima, a frigideira de frente (o fundo em disco, a
    # borda acesa em cima)
    px(48, 34, 2, 1, "ferroLuz")
    px(48, 35, 1, 9, "ferro")
    px(49, 35, 1, 9, "ferroEsc")
    for y in range(44, 54):
        for x in range(44, 54):
            d = ((x + 0.5 - 49) / 4.6) ** 2 + ((y + 0.5 - 48.6) / 4.6) ** 2
            if d <= 1:
                px.p(x, y, "ferroLuz" if d > 0.62 and x < 49 and y < 49 else "ferroEsc" if d > 0.62 else "ferro")
    px(46, 47, 1, 2, "ferroBrilho")


def caldeirao(px):
    """O caldeirão na frente das chamas: a cremalheira (o braço de ferro preso na ombreira de lá, a corrente), a alça, o
    bojo de ferro com a borda acesa e o reflexo do fogo embaixo; os cães de ferro com a lenha."""
    px = px.deslocado(DX_FOGO)
    # a cremalheira: o pino na ombreira e o braço até o meio da boca
    px(44, 38, 3, 3, "ferroEsc")
    px(30, 39, 15, 1, "ferroLuz")
    px(30, 40, 15, 1, "ferro")
    # a corrente, em elos alternados
    for y in range(41, 47):
        px(30 + (y % 2), y, 1, 1, "ferroLuz" if y % 2 else "ferro")
    # a alça em arco
    for x in range(24, 38):
        dy = round(4 * ((x + 0.5 - 31) / 7) ** 2)
        px(x, 47 + dy, 1, 1, "ferroLuz" if x < 31 else "ferro")
    # o bojo: mais largo no meio, a borda com a aresta clara, o reflexo quente embaixo
    for y in range(50, 61):
        t = (y - 50) / 10
        meia = 7 + 2 * math.sin(math.pi * min(1, t * 1.3))
        a, b = round(31 - meia), round(31 + meia)
        for x in range(a, b):
            u = (x - a) / max(1, b - a - 1)
            cor = "ferroLuz" if u < 0.18 else "ferroEsc" if u > 0.72 else "ferro"
            if y >= 58:
                cor = "brasaEsc" if u < 0.7 else "ferroEsc"
            px.p(x, y, cor)
    px(23, 49, 17, 2, "ferroEsc")
    px(23, 49, 17, 1, "ferroLuz")
    px(25, 52, 1, 3, "ferroBrilho")
    # os cães de ferro e a lenha cruzada embaixo
    for x in (20, 41):
        px(x, 59, 2, 6, "ferroEsc")
        px(x - 1, 59, 4, 1, "ferro")
    px(17, 62, 28, 2, "lenha")
    px(17, 62, 28, 1, "lenhaLuz")
    px.linha(21, 64, 40, 60, "lenha")
    px(17, 62, 1, 2, "brasa")


def chamas(i):
    """As chamas da lareira (o quadro i de 4): línguas que afinam para cima, a ponta pendendo, em volta e atrás do
    caldeirão; o miolo claro embaixo."""
    t = Tela(QW, QH)
    linguas = [  # (x da base, altura, largura, a ponta pende para)
        (18, 14, 4, 1), (23, 9, 4, -1), (38, 10, 4, 1), (43, 15, 4, -1), (30, 6, 5, 1), (34, 7, 4, -1),
    ]
    base = 63
    for k, (bx, alt, larg, lado) in enumerate(linguas):
        bx += DX_FOGO
        f = (i + k) % 4
        alt2 = alt + (0, 2, 1, -1)[f]
        sw = (0, 1, 0, -1)[(f + k) % 4]
        for d in range(alt2):
            y = base - d
            u = d / max(1, alt2 - 1)
            meia = larg / 2 * (1 - u) ** 0.8
            cx = bx + sw * u + lado * 1.5 * u * u
            for x in range(round(cx - meia), round(cx + meia) + 1):
                n = 6 if u < 0.25 and abs(x - cx) < meia * 0.5 else 5 if u < 0.45 else 4 if u < 0.7 else 3
                if abs(x - cx) > meia - 0.6 and n > 3:
                    n -= 1
                t.px(x, y, FOGO[n])
        if f in (1, 2):  # a ponta solta, de vez em quando
            t.px(round(bx + sw + lado * 2), base - alt2 - 1, FOGO[3])
    return t


# ---------------------------------------------------------------- atrás do taverneiro: a prateleira e a bancada
def prateleira(px):
    """A prateleira alta de uma ponta a outra entre os esteios: a aresta acesa, a tábua, a sombra embaixo, as
    mãos-francesas presas na pedra."""
    px(62, PR, 200, 1, "madeiraLuz")
    px(62, PR + 1, 200, 2, "madeira")
    px(62, PR + 3, 200, 1, "pedraSombra")
    for x in (76, 140, 182, 248):
        for k in range(5):
            px(x + k, PR + 3 + k, 2, 1, "madeira")
        px(x, PR + 3, 1, 1, "madeiraLuz")


def jarra(px, x, y0, base="louca", faixa=True):
    """Uma jarra bojuda de pé na prateleira (o fundo em y0): o bico à esquerda, a asa à direita, o gargalo estreito."""
    luz, meio, sombra = base + "Luz", base, base + "Sombra"
    for y in range(y0 - 10, y0):
        u = (y - (y0 - 10)) / 9
        meia = 2.5 + 2.5 * math.sin(math.pi * min(1, u * 1.15))
        a, b = round(x - meia), round(x + meia)
        for xx in range(a, b):
            px.p(xx, y, luz if xx - a < 2 else sombra if b - xx <= 1 else meio)
    px(x - 2, y0 - 12, 4, 2, meio)
    px(x - 2, y0 - 12, 1, 2, luz)
    px(x - 3, y0 - 12, 1, 1, luz)  # o bico
    px(x + 3, y0 - 10, 2, 1, meio)  # a asa
    px(x + 5, y0 - 9, 1, 4, sombra)
    px(x + 4, y0 - 5, 1, 1, sombra)
    if faixa:
        px(x - 3, y0 - 6, 6, 1, "azul")
        px(x - 1, y0 - 8, 1, 1, "azul")


def caneca(px, x, y0, w=6, h=8, asa="dir", tampa=False):
    """Uma caneca de estanho de pé (o fundo em y0): o corpo com a aresta acesa, o brilho de um pixel, os aros, a asa."""
    px(x, y0 - h, w, h, "estanho")
    px(x, y0 - h, 1, h, "estanhoLuz")
    px(x + w - 1, y0 - h, 1, h, "estanhoEsc")
    px(x + 1, y0 - h + 2, 1, 2, "estanhoBrilho")
    px(x, y0 - h, w, 1, "estanhoLuz")
    px(x, y0 - 2, w, 1, "estanhoEsc")
    ax = x + w if asa == "dir" else x - 2
    px(ax, y0 - h + 1, 2, 1, "estanhoEsc")
    px(ax + (1 if asa == "dir" else 0), y0 - h + 1, 1, h - 3, "estanhoEsc")
    px(ax, y0 - 3, 2, 1, "estanhoEsc")
    if tampa:
        px(x - 1, y0 - h - 1, w + 2, 1, "estanhoLuz")
        px(x + w - 1, y0 - h - 2, 2, 1, "estanho")


def garrafa(px, x, y0, alt, larg, base="vidro"):
    """Uma garrafa (o fundo em y0): o corpo, o ombro, o gargalo, a rolha, o brilho comprido."""
    luz, meio = base + "Luz", base
    corpo = alt - 6
    px(x, y0 - corpo, larg, corpo, meio)
    px(x, y0 - corpo, 1, corpo, luz)
    px(x + 1, y0 - corpo + 1, 1, corpo - 3, base + "Brilho")
    px(x + 1, y0 - corpo - 2, larg - 2, 2, meio)
    gx = x + larg // 2 - 1
    px(gx, y0 - alt, 2, 4, meio)
    px(gx, y0 - alt, 1, 4, luz)
    px(gx, y0 - alt - 1, 2, 2, "rolha")


def objetos_prateleira(px):
    """Na prateleira, por grupos: à esquerda a louça (a jarra de grés, a jarra de barro, as canecas, as tigelas); o vão
    atrás da cabeça; à direita as garrafas (de vinho, a bojuda de âmbar, o garrafão empalhado, a alta) e o pote."""
    y0 = PR
    jarra(px, 70, y0)
    jarra(px, 86, y0, "barro", faixa=False)
    caneca(px, 96, y0, 7, 9, tampa=True)
    caneca(px, 108, y0, 5, 6)
    # as tigelas de madeira empilhadas
    for k, (w, cor) in enumerate([(12, "madeiraMeio"), (10, "madeiraLuz")]):
        px(119 + k, y0 - 2 - k * 2, w, 2, cor)
        px(119 + k, y0 - 1 - k * 2, w, 1, "madeiraEsc")
    # as garrafas
    garrafa(px, 180, y0, 16, 5)
    # a bojuda de âmbar
    for y in range(y0 - 8, y0):
        u = (y - (y0 - 8)) / 7
        meia = 2 + 3 * math.sin(math.pi * min(1, u * 1.1))
        a, b = round(193 - meia), round(193 + meia)
        px(a, y, b - a, 1, "ambar")
        px(a, y, 1, 1, "ambarLuz")
    px(191, y0 - 6, 1, 2, "ambarBrilho")
    px(192, y0 - 12, 2, 4, "ambar")
    px(192, y0 - 13, 2, 1, "rolha")
    # o garrafão empalhado: o vime em tramas, o gargalo de vidro
    for y in range(y0 - 11, y0):
        u = (y - (y0 - 11)) / 10
        meia = 3 + 3 * math.sin(math.pi * min(1, u * 1.1))
        a, b = round(207 - meia), round(207 + meia)
        for xx in range(a, b):
            px.p(xx, y, "vimeLuz" if xx - a < 2 else "vimeEsc" if (xx + y) % 3 == 0 or b - xx <= 1 else "vime")
    px(206, y0 - 15, 3, 4, "vidro")
    px(206, y0 - 15, 1, 4, "vidroLuz")
    px(206, y0 - 16, 3, 1, "rolha")
    garrafa(px, 216, y0, 18, 4)
    # o pote de barro com a tampa
    px(222, y0 - 7, 8, 7, "barro")
    px(222, y0 - 7, 2, 7, "barroLuz")
    px(229, y0 - 7, 1, 7, "barroSombra")
    px(221, y0 - 8, 10, 1, "barroLuz")
    px(225, y0 - 9, 2, 1, "barroSombra")


def canecas_penduradas(px):
    """Duas canecas penduradas pela asa nos ganchos embaixo da prateleira: o gancho entra na asa, o corpo de pé ao lado,
    a borda de cima acesa com a boca escura."""
    for x in (108, 119):
        px(x + 7, PR + 4, 1, 3, "ferroLuz")  # o gancho
        px(x + 6, PR + 6, 1, 1, "ferroLuz")
        px(x + 5, PR + 7, 3, 1, "estanhoEsc")  # a asa
        px(x + 7, PR + 7, 1, 5, "estanhoEsc")
        px(x + 5, PR + 11, 3, 1, "estanhoEsc")
        px(x, PR + 7, 6, 8, "estanho")
        px(x, PR + 7, 1, 8, "estanhoLuz")
        px(x + 5, PR + 7, 1, 8, "estanhoEsc")
        px(x + 1, PR + 9, 1, 2, "estanhoBrilho")
        px(x - 1, PR + 6, 8, 1, "estanhoLuz")
        px(x, PR + 13, 6, 1, "estanhoEsc")


def bancada(px):
    """A bancada de trabalho encostada na parede, entre os esteios: o tampo com a aresta acesa e a frente escura (o resto
    fica atrás do balcão)."""
    px(62, BB, 200, 1, "madeiraLuz")
    px(62, BB + 1, 200, 2, "madeiraMeio")
    px(62, BB + 3, 200, BT - BB - 3, "madeiraEsc")
    for x in range(70, 262, 24):
        px(x, BB + 3, 1, BT - BB - 3, "pedraSombra")


def barril(px):
    """O barril deitado no berço, com o eixo ao longo da parede: o bojo (mais alto no meio que nas pontas), as aduelas
    correndo para os lados, os aros de ferro aos pares perto das pontas, o tampo da direita (o que olha para o meio da
    sala) com a torneira de latão embaixo, e espaço para a caneca."""
    x0, x1, cy, r = 66, 102, 53, 11.5
    def bojo(x):
        u = (x + 0.5 - x0) / (x1 - x0)
        return r * (0.8 + 0.2 * math.sin(math.pi * u))
    for x in range(x0, x1):
        h = bojo(x)
        for y in range(round(cy - h), round(cy + h)):
            v = (y + 0.5 - (cy - h)) / (2 * h)
            cor = "balcaoBrilho" if v < 0.1 else "balcaoLuz" if v < 0.3 else "balcao" if v < 0.6 else                 "madeiraMeio" if v < 0.82 else "madeiraEsc"
            if round((y - cy) * 3 / h) != round((y + 1 - cy) * 3 / h):  # as juntas das aduelas, ao comprido
                cor = "madeiraMeio" if v < 0.6 else "madeiraEsc"
            px.p(x, y, cor)
    for ax in (68, 73, 95, 100):  # os aros: um pixel de ferro escuro, acesos em cima
        h = bojo(ax)
        px(ax, round(cy - h), 1, round(2 * h), "ferroEsc")
        px(ax, round(cy - h), 1, round(h * 0.5), "ferro")
        px(ax, round(cy - h), 1, 1, "ferroLuz")
    # as pontas das aduelas passando do tampo, à esquerda
    px(x0 - 1, round(cy - bojo(x0)) + 1, 1, round(2 * bojo(x0)) - 2, "madeiraEsc")
    # o tampo da direita, de lado: uma elipse estreita, mais clara, com o aro e a borda das aduelas
    hp = bojo(x1 - 1)
    for y in range(round(cy - hp), round(cy + hp)):
        meia = 3.5 * math.sqrt(max(0.0, 1 - ((y + 0.5 - cy) / hp) ** 2))
        if meia < 0.5:
            continue
        px(x1, y, round(meia), 1, "madeiraLuz" if y < cy + 3 else "madeiraMeio")
        px(x1 + round(meia), y, 1, 1, "madeiraEsc")
    px(x1 - 1, round(cy - hp), 1, round(2 * hp), "ferroEsc")
    # a torneira de latão no tampo, embaixo do meio: o corpo, a chave em cima, a bica para baixo
    tx = x1 + 2
    px(tx, cy + 3, 4, 2, "latao")
    px(tx, cy + 3, 4, 1, "lataoLuz")
    px(tx + 2, cy + 1, 1, 2, "lataoLuz")
    px(tx + 1, cy + 1, 3, 1, "latao")
    px(tx + 3, cy + 5, 2, 3, "latao")
    px(tx + 3, cy + 5, 1, 3, "lataoLuz")
    px(tx + 3, cy + 8, 2, 1, "lataoEsc")
    # o berço: dois calços com o recorte
    for bx in (72, 92):
        px(bx, BB - 3, 6, 3, "madeiraMeio")
        px(bx, BB - 3, 6, 1, "madeiraLuz")
        px(bx + 5, BB - 3, 1, 3, "madeiraEsc")


def pendurados(px):
    """Na viga, à direita: as linguiças em gomos e a trança de alho, cada uma no seu gancho e no barbante."""
    # as linguiças: duas fieiras de gomos com a amarração
    for k, (x, n) in enumerate([(234, 4), (240, 3)]):
        px(x + 1, 6, 1, 3, "barbante")
        y = 9
        for g in range(n):
            px(x, y, 3, 7, "linguica")
            px(x, y + 1, 1, 5, "linguicaLuz")
            px(x + 2, y + 1, 1, 6, "linguicaEsc")
            px(x + 1, y + 7, 1, 1, "barbante")
            y += 8
    # a trança de alho: as cabeças em zigue-zague, a palha no meio
    px(250, 6, 1, 3, "barbante")
    px(250, 9, 1, 30, "barbante")
    for g in range(6):
        gx, gy = 246 + (g % 2) * 5, 9 + g * 5
        px.grade(gx, gy, [".a..", "ALaa", "Aaae", "Laee", ".ee."], {"a": "alho", "A": "alhoLuz", "L": "alhoLuz",
                                                                   "e": "alhoEsc"})


def comida_e_jarra(px):
    """Na bancada da direita: a jarra de grés e a tábua com o pão (a casca, o corte com o miolo) e a cunha de queijo."""
    # a jarra
    px(198, BB - 11, 8, 11, "louca")
    px(198, BB - 11, 2, 11, "loucaLuz")
    px(205, BB - 11, 1, 11, "loucaSombra")
    px(199, BB - 13, 6, 2, "louca")
    px(199, BB - 13, 1, 2, "loucaLuz")
    px(198, BB - 13, 1, 1, "loucaLuz")  # o bico
    px(206, BB - 10, 2, 1, "loucaSombra")
    px(207, BB - 9, 1, 5, "loucaSombra")
    px(198, BB - 6, 8, 1, "azul")
    px(201, BB - 8, 1, 1, "azul")
    # a tábua
    px(212, BB - 2, 40, 2, "madeiraLuz")
    px(212, BB - 1, 40, 1, "madeiraMeio")
    # o pão: o filão arredondado, com o corte na ponta da direita
    for x in range(214, 233):
        u = (x - 214) / 18
        alt = round(6 + 2 * math.sin(math.pi * u))
        px(x, BB - 2 - alt, 1, alt, "pao")
        px(x, BB - 2 - alt, 1, 1, "paoLuz")
        if alt > 6:
            px(x, BB - 1 - alt, 1, 1, "paoLuz")
    for x in (218, 223, 228):  # os talhos da casca
        px(x, BB - 9, 2, 1, "paoEsc")
    px(229, BB - 7, 3, 5, "miolo")
    px(232, BB - 7, 1, 5, "paoEsc")
    px(214, BB - 3, 19, 1, "paoEsc")
    # uma fatia caída
    px(234, BB - 4, 4, 2, "miolo")
    px(234, BB - 4, 4, 1, "paoLuz")
    # a cunha de queijo: a face cortada clara, a casca embaixo
    for k in range(6):
        px(240 + k, BB - 3 - k, 10 - k, 1, "queijoLuz" if k > 3 else "queijo")
    px(240, BB - 3, 10, 1, "queijoEsc")
    px(249, BB - 8, 1, 5, "queijoEsc")
    px(243, BB - 5, 1, 1, "queijoEsc")


def lampiao(px):
    """O lampião no esteio da direita: o braço de ferro com o gancho, o chapéu, as hastes, o vidro aceso e a base."""
    px(268, 19, 9, 1, "ferroLuz")
    px(268, 20, 9, 1, "ferro")
    px(275, 21, 1, 2, "ferro")
    px(272, 23, 7, 2, "ferro")
    px(273, 22, 5, 1, "ferroLuz")
    px(272, 25, 1, 9, "ferroEsc")
    px(278, 25, 1, 9, "ferroEsc")
    px(273, 25, 5, 9, "#d89040")
    px(273, 25, 1, 9, "#f0b860")
    px(272, 34, 7, 2, "ferro")
    px(272, 34, 7, 1, "ferroLuz")
    px(274, 36, 3, 1, "ferroEsc")


def chama_lampiao(i):
    t = Tela(QW, QH)
    h = (4, 5, 4, 3)[i]
    for d in range(h):
        y = 32 - d
        w = 2 if d < h - 1 else 1
        t.ret(275 - (1 if w == 2 and i % 2 else 0), y, w, 1, (*_hx(FOGO[6 if d < 2 else 5]), 255))
    t.px(275, 33, FOGO[4])
    return t


def _hx(s):
    return tuple(int(s[k:k + 2], 16) for k in (1, 3, 5))


def despensa(px):
    """A porta da despensa, na parede da direita, atrás da ponta do balcão: a verga, o batente, as tábuas em pé, as duas
    dobradiças de ferro com os cravos e a argola."""
    x0, x1, y0 = 284, 308, 15
    px(x0 - 3, y0 - 3, x1 - x0 + 6, 3, "madeira")
    px(x0 - 3, y0 - 3, x1 - x0 + 6, 1, "madeiraLuz")
    px(x0 - 3, y0, 3, BT - y0, "madeira")
    px(x0 - 3, y0, 1, BT - y0, "madeiraLuz")
    px(x1, y0, 3, BT - y0, "madeiraEsc")
    for x in range(x0, x1):
        k = (x - x0) % 6
        px(x, y0, 1, BT - y0, "madeiraLuz" if k == 0 else "madeiraEsc" if k == 5 else "madeiraMeio")
    for y in (24, 58):
        px(x0, y, 15, 2, "ferro")
        px(x0, y, 15, 1, "ferroLuz")
        for x in (x0 + 2, x0 + 8, x0 + 13):
            px(x, y + 1, 1, 1, "ferroBrilho")
    px(x1 - 6, 42, 3, 1, "ferroLuz")
    for a in range(0, 360, 30):
        px.p(round(x1 - 5 + math.cos(math.radians(a)) * 2), round(46 + math.sin(math.radians(a)) * 2.5), "ferro")
    px(x1 - 7, 45, 1, 2, "ferroLuz")


# ---------------------------------------------------------------- a frente: o balcão e os fregueses
def balcao(px):
    """O balcão de um lado a outro: o tampo visto um pouco de cima (as tábuas ao comprido, a luz na borda de trás), a
    borda grossa da frente com a aresta acesa, a sombra dela e as tábuas da frente em pé, com a travessa."""
    y_frente = BT + 6
    px(0, BT, QW, y_frente - BT, "balcao")
    px(0, BT, QW, 1, "balcaoLuz")
    px(0, BT + 3, QW, 1, "balcaoJunta")
    for x in range(-20, QW, 46):  # as emendas das tábuas do tampo, desencontradas
        px(x, BT + 1, 1, 2, "balcaoJunta")
        px(x + 23, BT + 4, 1, 2, "balcaoJunta")
    # a borda da frente, grossa, e a sombra embaixo dela
    px(0, y_frente, QW, 4, "balcaoLuz")
    px(0, y_frente, QW, 1, "balcaoBrilho")
    px(0, y_frente + 3, QW, 1, "balcao")
    px(0, y_frente + 4, QW, 2, "balcaoJunta")
    # as tábuas em pé
    for x in range(0, QW):
        k = x % 16
        cor = "balcaoJunta" if k == 0 else "balcao" if k == 1 else "balcaoEsc"
        px(x, y_frente + 6, 1, QH - y_frente - 6, cor)
    px(0, y_frente + 11, QW, 2, "balcao")
    px(0, y_frente + 11, QW, 1, "balcaoLuz")
    px(0, y_frente + 13, QW, 1, "balcaoJunta")


def caneca_do_fregues(px):
    """A caneca do freguês da direita, no tampo, com a sombra de contato."""
    caneca(px, 254, BT + 4, 7, 9, asa="esq")
    px(253, BT + 4, 10, 1, "balcaoJunta")


def _forma(px, pts, cor):
    px.t.poligono(pts, C.get(cor, cor))


def fregues_esquerda(px):
    """De costas, à esquerda, virado para o balcão: a cabeça redonda com o cabelo, a orelha de lá (a do lado do fogo)
    acesa, a nuca, o capuz caído amontoado no pescoço e o ombro da capa descendo até a borda; no escuro, com a lareira
    só no contorno do lado dela."""
    # a capa: do pescoço, o ombro desce para a direita e sai pelo canto de baixo
    _forma(px, [(-1, 78), (8, 75), (20, 76), (30, 80), (40, 86), (48, 92), (52, QH), (-1, QH)], "vulto")
    # o capuz caído, amontoado atrás do pescoço, e uma dobra da capa
    _forma(px, [(0, 75), (10, 72), (22, 74), (26, 79), (16, 81), (4, 81)], "vultoMeio")
    px.linha(26, 82, 44, 94, "vultoMeio")
    for x, y in ((21, 75), (24, 77), (27, 80)):
        px.p(x, y, "vultoLuz")
    # a cabeça: o cabelo, a nuca
    px.elipse(11, 64, 9, 10.5, "vulto")
    px(6, 72, 11, 4, "vulto")
    # o contorno aceso do lado do fogo (a direita da cabeça) e o alto
    for y in range(54, 74):
        for x in range(0, 22):
            d = ((x + 0.5 - 11) / 9) ** 2 + ((y + 0.5 - 64) / 10.5) ** 2
            if 0.7 < d <= 1 and (x > 12 or y < 57):
                px.p(x, y, "vultoLuz")
    for x, y in ((8, 56), (13, 57), (16, 60), (6, 58)):  # o crespo do cabelo
        px.p(x, y, "vultoMeio")
    # a orelha de lá, contra o fogo
    px(19, 62, 2, 5, "vultoLuz")
    px(19, 63, 1, 3, "#3a2416")


def fregues_direita(px):
    """À direita, de três quartos de costas, virado para o taverneiro: o capuz com a ponta caída para trás e a abertura
    para a esquerda (o rosto no escuro), o ombro largo descendo até o canto; o lampião acende a borda de cima do capuz."""
    # o ombro e as costas
    _forma(px, [(QW + 1, 74), (310, 76), (298, 78), (288, 82), (278, 90), (274, QH), (QW + 1, QH)], "vulto")
    # o capuz: a ponta para trás e para cima, a abertura virada para a esquerda
    _forma(px, [(300, 60), (306, 55), (313, 54), (319, 57), (QW + 1, 62), (QW + 1, 79), (308, 79), (298, 77), (295, 70)],
           "vulto")
    # a abertura do capuz: a borda dobrada, um tom acima, e o escuro de dentro
    px.linha(300, 60, 296, 70, "vultoMeio")
    px.linha(296, 70, 299, 77, "vultoMeio")
    _forma(px, [(301, 61), (303, 61), (300, 70), (302, 76), (299, 76), (297, 70)], "#050405")
    # a luz do lampião na borda de cima
    for x, y in ((301, 59), (302, 58), (303, 57), (304, 56), (305, 56), (306, 55), (307, 55), (308, 54), (309, 54),
                 (310, 54), (311, 54)):
        px.p(x, y, "vultoLuz")
    # a dobra do capuz nas costas e a costura do ombro
    px.linha(310, 60, 316, 72, "vultoMeio")
    px.linha(288, 83, 304, 79, "vultoMeio")
    px.linha(279, 90, 286, 84, "vultoLuz")


# ---------------------------------------------------------------- a luz
LUZES = [  # (x, y, raio, força): a lareira, o lampião, a luz geral sobre o balcão
    (29, 56, 70, 1.0), (275, 30, 46, 0.9), (160, 50, 96, 0.55),
]


def luz(t, emissivo=False):
    """Longe das luzes, a sala escurece em degraus pontilhados (a viga, os cantos de cima, a frente do balcão embaixo);
    perto da lareira e do lampião, o halo quente em anéis. Nas chamas (emissivo) nada escurece."""
    if emissivo:
        return t
    for y in range(QH):
        for x in range(QW):
            if not t.a[y, x, 3]:
                continue
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.5)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.2)))
            escuro = max(0.0, 0.6 - perto * 1.15)
            if y > BT + 12:  # a frente do balcão, longe do tampo
                escuro += 0.08 * (y - BT - 12) / (QH - BT - 12)
            f5 = escuro / 0.6 * 5
            n = int(f5) + (1 if pont(x, y, int((f5 % 1) * 16)) else 0)
            if n:
                t.mistura(x, y, (4, 3, 4), 0.5 * n / 5)
            for lx, ly, r, f in LUZES[:2]:
                d2 = ((x - lx) ** 2 + ((y - ly) * 1.3) ** 2) / (r * r)
                if d2 < 1:
                    al = 0.26 if d2 < 0.1 else 0.17 if d2 < 0.3 else 0.1 if d2 < 0.6 else 0.05
                    t.mistura(x, y, (255, 150, 70), al * f)
    return t


# ---------------------------------------------------------------- as camadas
def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    sala(px)
    lareira(px)
    utensilios(px)
    bancada(px)
    prateleira(px)
    objetos_prateleira(px)
    canecas_penduradas(px)
    barril(px)
    comida_e_jarra(px)
    esteio(px, 54, 8)
    esteio(px, 262, 7)
    pendurados(px)
    despensa(px)
    lampiao(px)
    return luz(t)


def camada_caldeirao():
    t = Tela(QW, QH)
    caldeirao(Pincel(t))
    return luz(t)


def frente():
    t = Tela(QW, QH)
    px = Pincel(t)
    balcao(px)
    caneca_do_fregues(px)
    fregues_esquerda(px)
    fregues_direita(px)
    return luz(t)


def fogo(i):
    return chamas(i)


def lampiao_chama(i):
    return chama_lampiao(i)
