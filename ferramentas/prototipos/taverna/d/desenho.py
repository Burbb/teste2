"""A taverna do Vau, candidata D (estudo estático): a C refeita nos conjuntos (a pessoa, o assento e a mesa
desenhados juntos), na escada, na lareira, no balcão, nas prateleiras e na luz. A régua é a da C.

O que veio da C (o resto desta nota é dela):

O que mudou da B (o histórico em ../LEIA-ME.md): a B tinha profundidade demais (11 px por metro no fundo, 34 na frente)
e quem ficava no fundo, Morel inclusive, virava uma cabeça de três ou quatro pixels; a escada era uma diagonal de
riscos e a galeria, uma faixa sem piso. A C olha do mesmo jeito (de frente, um pouco de cima), mas a régua vai de 13
px por metro no fundo a 30 na borda de baixo, e as pessoas importantes ficam no meio dessa faixa: o taverneiro atrás
do balcão (18), Morel no canto (19), os grupos entre 20 e 30.

**O espaço** (conferido sozinho em `so_o_espaco()`):
- à esquerda, a parede do balcão (pisa em BAR_Y): a porta da rua, as prateleiras, o lampião, a porta da despensa; ela
  vira para o fundo num canto de pedra e o salão continua até a parede do fundo (FUNDO_Y), com a lareira, a escada e
  a galeria dos quartos;
- o piso de tábuas paralelas ao fundo, as juntas um tom só abaixo e nunca a menos de 4 px uma da outra;
- a galeria: o piso dela visto de cima (a faixa por onde se anda entre as portas e o guarda-corpo), a espessura (a
  testeira com as pontas das vigas), dois esteios com mãos-francesas até o chão; a escada: o banzo de fora, os degraus
  (o piso claro, o espelho escuro), o corrimão nos balaústres, o pilar do pé no chão e o do patamar, que é o primeiro
  esteio da galeria;
- a despensa ("um porão baixo", abertura.descer) é a porta baixa entreaberta ao lado do balcão.

**Materiais por valor:** a pedra do fundo fria e escura, o reboco do balcão claro e morno, a madeira dos móveis mais
quente e mais clara que o piso, as roupas em cores contidas e diferentes entre si. A luz: a lareira e as velas fazem
pequenas áreas acesas em volta das mesas; longe delas a sala escurece aos poucos (na D, sem faixas).

As camadas: `fundo(com_morel)` (a sala, os móveis, as pessoas do estudo e a luz), `fogo(i)` e `velas(i)` (4 quadros
cada), por cima. As pessoas são desenhadas à mão em gente.py."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "hud", "forja", "h2"))
from tela_h2 import Tela  # noqa: E402  (a mesma camada de pixels das fontes da forja)

QW, QH = 320, 96
VP = (160, 27)        # o ponto de fuga: o olho a ~2,3 m
METRO = 30.0          # 1 m em pixels na borda de baixo
FUNDO_Y = 57          # onde a parede do fundo encontra o piso (13 px/m)
BAR_Y = 64            # onde a parede do balcão encontra o piso (16 px/m)
RETORNO = (130, 136)  # o canto em que a parede do balcão vira para o fundo
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def m(y):
    """Pixels por metro no que pisa em y (zero no horizonte, METRO na borda de baixo)."""
    return METRO * (y - VP[1]) / (QH - VP[1])


def pont(x, y, n):
    return BAYER[(y & 3) * 4 + (x & 3)] < n


C = {
    # a pedra do fundo (fria) e a da lareira (mais clara, aquecida pelo fogo)
    "pedra": "#33363b", "pedraLuz": "#43464c", "pedraSombra": "#26282c", "junta": "#2d2f34",
    "lareira": "#4e4a46", "lareiraLuz": "#625c55", "lareiraEsc": "#3a3632", "fuligem": "#1a1614",
    # o reboco da parede do balcão e o enxaimel
    "reboco": "#62594b", "rebocoLuz": "#706655", "rebocoSombra": "#4f483d",
    # a madeira da construção (escura) e a dos móveis (mais quente e mais clara que o piso)
    "viga": "#3a2a1e", "vigaLuz": "#503a28", "vigaEsc": "#24190f",
    "movel": "#6e4a2c", "movelLuz": "#8c6238", "movelEsc": "#47301c", "movelTopo": "#9a7044",
    # o piso
    "tabua": "#40322a", "tabuaJunta": "#372a22", "contato": "#1e1812",
    # o ferro, o barro, o estanho, o vidro, a cera, o fogo
    "ferro": "#33343a", "ferroLuz": "#5a5c64", "ferroEsc": "#1c1d22",
    "barro": "#7a4a30", "barroLuz": "#9a6440", "barroEsc": "#4e2e1e",
    "estanho": "#80838a", "estanhoLuz": "#b0b3ba", "estanhoEsc": "#55585e",
    "vidro": "#3e5a4a", "vidroLuz": "#6a8a74",
    "cera": "#d6ccae", "ceraEsc": "#a89e80", "chama": "#ffcc66", "chamaFora": "#e8782a", "chamaMiolo": "#fff2c4",
    "brasa": "#c8501a", "brasaEsc": "#7a2a10",
    "linho": "#b0a68e", "linhoLuz": "#d2c8b0", "linhoSombra": "#857b66",
    "pao": "#a8783a", "paoLuz": "#c89a52", "tigela": "#5a3018", "ensopado": "#8a5a30",
    "vulto": "#0d0b0a",
}


class Pincel:
    def __init__(self, t):
        self.t = t

    def __call__(self, x, y, w=1, h=1, cor=None):
        if cor and w > 0 and h > 0:
            self.t.ret(int(round(x)), int(round(y)), int(round(w)), int(round(h)), C.get(cor, cor))

    def p(self, x, y, cor):
        self(x, y, 1, 1, cor)

    def linha(self, x0, y0, x1, y1, cor, grossa=1):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), 1, grossa, cor)

    def grade(self, x0, y0, linhas, pal):
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])


def retorno_y(x):
    """O piso encontra o retorno (a parede que vai do balcão ao fundo) nesta linha, que corre para VP."""
    x0, x1 = RETORNO
    return BAR_Y - (x - x0) * (BAR_Y - FUNDO_Y) / (x1 - x0)


def atras_do_balcao(x, y):
    return y < BAR_Y and x < RETORNO[1] and y < retorno_y(x)


# ---------------------------------------------------------------- o espaço
def paredes(px):
    """A parede do fundo (pedra em blocos largos), o retorno de pedra e a parede do balcão (reboco entre os esteios do
    enxaimel, o rodapé de tábuas); a viga do teto na frente de tudo."""
    x0, x1 = RETORNO
    px(x1, 0, QW - x1, FUNDO_Y, "pedra")
    for i, y in enumerate(range(FUNDO_Y - 5, -1, -5)):          # fiadas de 5 px, blocos de 10
        px(x1, y, QW - x1, 1, "junta")
        for x in range(x1 + (i % 2) * 5, QW, 10):
            px(x, y + 1, 1, 4, "junta")
    px(x1, FUNDO_Y - 1, QW - x1, 1, "pedraSombra")
    for x in range(x0, x1):                                     # o retorno, de lado para a sala
        yb = round(retorno_y(x))
        px(x, 0, 1, yb, "pedraLuz")
        for y in range(4, yb, 5):
            px.p(x, y, "pedra")
        px(x, yb - 1, 1, 2, "pedraSombra")
    px(0, 0, x0, BAR_Y, "reboco")                               # a parede do balcão
    for xe in (0, 31, 112, x0 - 3):                             # os esteios do enxaimel
        px(xe, 0, 3, BAR_Y, "viga")
        px(xe, 0, 1, BAR_Y, "vigaLuz")
    px(0, 20, x0, 2, "viga")
    px(0, 20, x0, 1, "vigaLuz")
    px(0, BAR_Y - 5, x0, 5, "viga")
    px(0, BAR_Y - 5, x0, 1, "vigaLuz")
    px(0, 0, QW, 3, "vigaEsc")                                  # a viga do teto
    px(0, 2, QW, 1, "viga")


def piso(px):
    """O piso de tábuas paralelas ao fundo: as juntas mais juntas longe (nunca a menos de 4 px) e as emendas,
    desencontradas, correndo para VP. Um tom só abaixo: o piso não disputa com as pessoas."""
    for y in range(FUNDO_Y, QH):
        for x in range(QW):
            if not atras_do_balcao(x, y):
                px.p(x, y, "tabua")
    dist = lambda y: 1 / m(y)
    linhas, d, ultima = [], dist(QH), QH
    while True:
        d += 0.06 * dist(QH)
        y = round(VP[1] + (QH - VP[1]) * dist(QH) / d)
        if y <= FUNDO_Y:
            break
        if ultima - y >= 4:
            linhas.append(y)
            ultima = y
    for y in linhas:
        for x in range(QW):
            if not atras_do_balcao(x, y):
                px.p(x, y, "tabuaJunta")
    for n, (ya, yb) in enumerate(zip(linhas, linhas[1:])):
        for i in range(-12, 13):
            X = (i + (n % 3) / 3) * 2.4
            xa, xb = VP[0] + X * m(ya), VP[0] + X * m(yb)
            if 0 <= xa < QW and not atras_do_balcao(xa, yb):
                px.linha(round(xa), ya - 1, round(xb), yb + 1, "tabuaJunta")


def porta(px, x0, x1, topo, base, arco=True, fresta=0):
    """Uma porta de tábuas num vão (em arco ou reto), com o batente, as duas ferragens, a argola e a soleira; `fresta`
    a deixa entreaberta (o escuro do outro lado aparece daquele tanto)."""
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    for y in range(round(topo - (r if arco else 0)) - 2, base):
        for x in range(x0 - 2, x1 + 2):
            d = math.hypot(x + 0.5 - cx, max(0, topo - y - 0.5)) if arco else 0
            if arco and y < topo and d > r + 2:
                continue
            if not arco and y < topo - 2:
                continue
            dentro = (x0 <= x < x1) and (y >= topo or (arco and d <= r))
            if not dentro:
                px.p(x, y, "pedraLuz" if arco else "vigaEsc")
                continue
            if x >= x1 - fresta:
                px.p(x, y, "vulto")
                continue
            junta = (x - x0) % 4 == 3
            px.p(x, y, "vigaEsc" if junta else "movelLuz" if (x - x0) % 4 == 0 else "movel")
    for yy in (topo + 2, base - 8):
        px(x0, yy, x1 - x0 - fresta, 1, "ferro")
    px(x1 - fresta - 4, (topo + base) // 2, 2, 2, "ferroLuz")
    px(x0 - 2, base, x1 - x0 + 4, 1, "pedraLuz")


# ---------------------------------------------------------------- o balcão e o que fica atrás dele
BALCAO = (38, 92, 74)    # o balcão: de x0 a x1, a frente pisando em y (curto: a cabeceira da mesa fica livre)
LAMPIAO = (72, 3, 22)    # o lampião pendurado na viga: x, de onde sai a corrente, onde fica a chama
DESPENSA = (115, 128)    # a porta da despensa, na parede do balcão


def prateleiras(px):
    """Duas tábuas em mãos de ferro com poucos objetos, cada um pela silhueta: em cima, duas canecas (o corpo e a asa),
    a jarra bojuda de barro (a boca, o bico, a asa) e duas garrafas de gargalo fino; embaixo, uma bilha e um prato de
    pé, com o vão atrás da cabeça do taverneiro."""
    for y, a, b in ((33, 38, 104), (43, 38, 62), (43, 84, 104)):
        px(a, y, b - a, 2, "movel")
        px(a, y, b - a, 1, "movelLuz")
        px(a, y + 2, b - a, 1, "rebocoSombra")
        for xx in (a + 2, b - 3):
            px(xx, y + 2, 1, 3, "ferro")
    for x in (41, 47):                                         # as canecas: o corpo reto e a asa de lado
        px(x, 28, 4, 5, "estanho"); px(x, 28, 1, 5, "estanhoLuz"); px(x + 3, 28, 1, 5, "estanhoEsc")
        px(x + 4, 29, 1, 1, "estanhoEsc"); px(x + 5, 29, 1, 3, "estanhoEsc"); px(x + 4, 31, 1, 1, "estanhoEsc")
    px(58, 25, 2, 1, "barroEsc")                               # a jarra: a boca, o pescoço, o bojo, o bico, a asa
    px(57, 26, 4, 1, "barro"); px(56, 27, 1, 1, "barroEsc")
    px(56, 28, 6, 4, "barro"); px(56, 28, 1, 4, "barroLuz"); px(57, 32, 4, 1, "barroEsc")
    px(62, 27, 1, 4, "barroEsc"); px(61, 27, 1, 1, "barroEsc"); px(61, 30, 1, 1, "barroEsc")
    for x, h in ((88, 9), (93, 8)):                            # as garrafas: o corpo, o ombro, o gargalo, a rolha
        px(x, 33 - h + 4, 4, h - 4, "vidro"); px(x, 33 - h + 4, 1, h - 4, "vidroLuz")
        px(x + 1, 33 - h + 2, 2, 2, "vidro"); px(x + 1, 33 - h, 2, 2, "vidroLuz"); px(x + 1, 33 - h - 1, 2, 1, "barroEsc")
    px(41, 37, 5, 6, "barro"); px(41, 37, 1, 6, "barroLuz"); px(42, 36, 3, 1, "barroEsc")  # a bilha
    px(90, 36, 1, 7, "linho"); px(89, 37, 3, 5, "linho"); px(89, 37, 1, 5, "linhoLuz")    # o prato de pé


def balcao(px):
    """O balcão de tábuas, na proporção de quem atende (1,05 m): o tampo visto de cima, a borda grossa da frente com a
    sombra embaixo (a espessura), o corpo em almofadas mais escuro, o rodapé. Sem banquinhos: a cabeceira da mesa
    comprida fica logo à direita e eles atravessavam o homem sentado nela."""
    x0, x1, pe = BALCAO
    mm = m(pe)
    yt = round(pe - 1.05 * mm)                                # a borda da frente do tampo
    px(x0 - 1, yt - 3, x1 - x0 + 3, 3, "movelTopo")            # o tampo, visto de cima
    px(x0 - 1, yt - 3, x1 - x0 + 3, 1, "movelLuz")
    px(x1 + 1, yt - 2, 1, 4, "movelEsc")                      # a ponta, de lado
    px(x0 - 2, yt, x1 - x0 + 4, 2, "movelLuz")                 # a borda (a espessura)
    px(x0 - 2, yt + 2, x1 - x0 + 4, 1, "movelEsc")
    px(x0, yt + 3, x1 - x0, 2, "vigaEsc")                      # a sombra da borda no corpo
    px(x0, yt + 5, x1 - x0, pe - yt - 5, "movelEsc")           # o corpo, mais escuro que o tampo
    largura = (x1 - x0) // 3
    for i in range(3):
        a = x0 + i * largura + 3
        b = a + largura - 6
        px(a, yt + 8, b - a, pe - yt - 13, "vigaEsc")
        px(a + 1, yt + 9, b - a - 2, pe - yt - 15, "movel")
        px(a + 1, yt + 9, b - a - 2, 1, "movelLuz")
    px(x0, pe - 3, x1 - x0, 3, "vigaEsc")
    px(x0 - 1, pe, x1 - x0 + 2, 1, "contato")
    return yt


def aparador(px):
    """O aparador atrás do balcão, encostado na parede (só o alto aparece por cima do tampo): o barril deitado com a
    torneira e duas canecas esperando."""
    px(40, 46, 12, 9, "movel")                                 # o barril, de lado, com os aros
    px(40, 46, 12, 1, "movelLuz")
    px(40, 54, 12, 1, "movelEsc")
    for xx in (42, 49):
        px(xx, 46, 1, 9, "ferro")
    px(52, 50, 2, 1, "ferroLuz"); px(53, 51, 1, 2, "ferro")   # a torneira
    for x in (80, 85):
        px(x, 49, 3, 4, "estanho"); px(x, 49, 1, 4, "estanhoLuz")


def porta_despensa(px):
    """A despensa: a porta baixa (1,75 m) na parede do balcão, entreaberta, com o escuro da escada na fresta."""
    x0, x1 = DESPENSA
    porta(px, x0, x1, round(BAR_Y - 1.75 * m(BAR_Y)), BAR_Y, arco=False, fresta=4)
    px(x1 - 4, round(BAR_Y - 0.6 * m(BAR_Y)), 4, 1, "vigaEsc")  # na fresta, a borda do primeiro degrau


# ---------------------------------------------------------------- a lareira
LAREIRA = (141, 183)  # o peito de pedra na parede do fundo


def lareira(px):
    """A lareira: a laje de pedra no piso, o peito com a espessura das ombreiras (a aresta clara), a boca funda (as
    faces de dentro em trapézio, acesas pelo fogo; o fundo de fuligem mais escuro e mais estreito), a verga de madeira
    fina com a prateleira, a coifa que abre só embaixo e a chaminé. O fogo, a lenha e o caldeirão vêm na camada fogo."""
    x0, x1 = LAREIRA
    cx = (x0 + x1) // 2
    meia_coifa = lambda y: 6 if y < 26 else round(6 + (y - 26) * ((x1 - x0) / 2 - 9) / 11)
    for y in range(3, 38):
        meia = meia_coifa(y)
        px(cx - meia, y, 2 * meia, 1, "lareira")
        px(cx - meia, y, 1, 1, "lareiraLuz")
        px(cx + meia - 1, y, 1, 1, "lareiraEsc")
    for y in range(6, 38, 5):
        meia = meia_coifa(y)
        px(cx - meia + 1, y, 2 * meia - 2, 1, "lareiraEsc")
    px(x0, 39, x1 - x0, FUNDO_Y - 39, "lareira")               # o peito
    for y in range(43, FUNDO_Y, 4):
        px(x0, y, x1 - x0, 1, "lareiraEsc")
        for x in range(x0 + ((y // 4) % 2) * 4, x1, 8):
            px(x, y + 1, 1, 3, "lareiraEsc")
    px(x0 - 1, 38, x1 - x0 + 2, 1, "movelLuz")                 # a verga fina, com a prateleira
    px(x0 - 1, 39, x1 - x0 + 2, 1, "movelEsc")
    px(x0 + 4, 34, 3, 4, "barro"); px(x0 + 4, 34, 1, 4, "barroLuz")
    # a boca: as ombreiras com a aresta clara, as faces de dentro em trapézio, o fundo
    b0, b1, bt = cx - 10, cx + 10, 43
    px(b0 - 1, bt - 1, b1 - b0 + 2, 1, "lareiraLuz")            # o arco raso
    px(b0, bt, b1 - b0, FUNDO_Y - bt, "fuligem")
    for y in range(bt, FUNDO_Y):
        f = min(4, (y - bt) // 3 + 2)                            # as faces de dentro alargam para baixo (a profundidade)
        px(b0, y, f, 1, "lareiraEsc")
        px(b1 - f, y, f, 1, "lareiraEsc")
        px(b0 + f - 1, y, 1, 1, "brasaEsc")                      # a aresta de dentro, quente
        px(b1 - f, y, 1, 1, "brasaEsc")
    px(b0 - 1, bt, 1, FUNDO_Y - bt, "lareiraLuz")               # a aresta das ombreiras (a espessura da pedra)
    px(b1, bt, 1, FUNDO_Y - bt, "lareiraLuz")
    px(x0 - 3, FUNDO_Y, x1 - x0 + 6, 3, "lareiraLuz")           # a laje
    px(x0 - 3, FUNDO_Y + 3, x1 - x0 + 6, 1, "lareiraEsc")
    for i, n in enumerate((3, 2)):                               # a lenha empilhada à esquerda
        for j in range(n):
            xx = RETORNO[1] - 1 + i * 2 + j * 4
            yy = FUNDO_Y + 1 - 4 - i * 4
            px(xx, yy, 4, 4, "movelEsc")
            px(xx, yy, 3, 3, "movelLuz")
            px(xx + 1, yy + 1, 1, 1, "movel")


# ---------------------------------------------------------------- a escada e a galeria
GAL = dict(x0=242, frente=31, fundo=24, viga=3, pe=60)   # a galeria: onde começa, a borda da frente e a de trás do piso
ESCADA = (196, 242, 10)                                   # do pé (x) ao patamar (x), em n degraus
PORTAS = ((254, 267), (288, 301))                         # as portas dos quartos


def escada_e_galeria(px):
    """A galeria: o piso visto de cima (a faixa por onde se anda), a testeira grossa com as pontas das vigas, dois
    esteios com mãos-francesas, o guarda-corpo; atrás, as portas dos quartos inteiras. A escada: os degraus (o piso
    claro, o espelho escuro), o banzo de fora, o corrimão nos balaústres, o pilar do pé e o do patamar (o primeiro
    esteio da galeria)."""
    g = GAL
    yf, yb, pe = g["frente"], g["fundo"], g["pe"]
    # as portas dos quartos, na parede, em cima do piso da galeria (1,8 m)
    topo = round(yb - 1.65 * m(FUNDO_Y))
    for d0, d1 in PORTAS:
        px(d0 - 1, topo - 1, d1 - d0 + 2, yb - topo + 1, "vigaEsc")
        px(d0 - 1, topo - 2, d1 - d0 + 2, 1, "vigaLuz")
        for x in range(d0, d1):
            px(x, topo, 1, yb - topo, "movelEsc" if (x - d0) % 3 == 2 else "movel")
        px(d0, topo, 1, yb - topo, "movelLuz")
        for yy in (topo + 2, yb - 4):
            px(d0, yy, d1 - d0, 1, "ferro")
        px(d1 - 3, topo + 9, 2, 2, "ferroLuz")
    # o piso da galeria visto de cima: as tábuas, mais claras na borda
    px(g["x0"] - 1, yb, QW - g["x0"] + 1, yf - yb, "movelTopo")
    px(g["x0"] - 1, yb, QW - g["x0"] + 1, 1, "movelEsc")             # a junta com a parede
    for x in range(g["x0"] + 6, QW, 9):
        px(x, yb + 1, 1, yf - yb - 1, "movel")
    # a testeira (a espessura do piso), com as pontas das vigas
    px(g["x0"] - 2, yf, QW - g["x0"] + 2, g["viga"] + 1, "viga")
    px(g["x0"] - 2, yf, QW - g["x0"] + 2, 1, "vigaLuz")
    for x in range(g["x0"] + 3, QW, 8):
        px(x, yf + 1, 2, 2, "vigaEsc")
    yv = yf + g["viga"] + 1                                     # embaixo da testeira
    # os esteios até o chão (sapata de pedra), com as mãos-francesas
    for xe in (g["x0"] + 32, QW - 6):
        px(xe, yv, 3, pe - yv, "viga")
        px(xe, yv, 1, pe - yv, "vigaLuz")
        px(xe - 1, pe - 2, 5, 2, "pedraLuz")
        px(xe - 2, pe, 7, 1, "contato")
        for i in range(5):
            px(xe - 1 - i, yv + i, 1, 1, "viga"); px(xe + 3 + i, yv + i, 1, 1, "viga")
    # o guarda-corpo na borda da frente (0,9 m), discreto: o corrimão fino e balaústres espaçados (o piso por onde se
    # anda aparece entre eles)
    alto = round(0.9 * m(pe))
    px(g["x0"] - 1, yf - alto, QW - g["x0"] + 1, 1, "movel")
    for x in range(g["x0"] + 4, QW, 8):
        px(x, yf - alto + 1, 1, alto - 1, "vigaEsc")
    # a escada: os degraus de baixo para cima, apoiados no banzo
    a, b, n = ESCADA
    passo_x = (b - a) / n
    passo_y = (pe - yf) / n
    for i in range(n):
        xa = round(a + i * passo_x)
        ytopo = round(pe - (i + 1) * passo_y)
        px(xa, ytopo, round(passo_x) + 1, 2, "movelTopo")        # o piso do degrau (largo)
        px(xa, ytopo, round(passo_x) + 1, 1, "movelLuz")
        px(xa, ytopo + 2, round(passo_x) + 1, 1, "movelEsc")     # o espelho (baixo)
    for d in range(3):                                          # o banzo de fora, grosso, por baixo dos degraus
        px.linha(a, pe - 1 + d, b, yf + 1 + d, "viga" if d else "vigaLuz")
    # o corrimão e os balaústres, a cada dois degraus
    for i in range(0, n + 1, 2):
        xs = round(a + i * passo_x)
        ys = round(pe - i * passo_y)
        px(xs, ys - alto + 1, 1, alto - 1, "movel")
    px.linha(a, pe - alto, b, yf - alto, "movelLuz")
    # o pilar do pé (no chão) e o do patamar (o esteio da galeria)
    px(a - 1, pe - alto - 2, 3, alto + 2, "viga"); px(a - 1, pe - alto - 2, 1, alto + 2, "vigaLuz")
    px(a - 2, pe - alto - 3, 5, 1, "movelLuz")
    px(a - 2, pe, 6, 1, "contato")
    px(b - 1, yf - alto - 2, 3, pe - yf + alto + 2, "viga"); px(b - 1, yf - alto - 2, 1, pe - yf + alto + 2, "vigaLuz")
    px(b - 2, yf - alto - 3, 5, 1, "movelLuz")
    px(b - 2, pe, 6, 1, "contato")


# ---------------------------------------------------------------- as mesas e os assentos
def mesa_ret(px, x0, x1, pe_longe, pe_perto, vela=None):
    """Uma mesa de tábuas vista de cima e de frente: o tampo do pé de longe ao de perto, as juntas das tábuas, a borda
    grossa, as pernas da frente inteiras e as de trás até o tampo, a travessa; a vela num castiçal em `vela`."""
    yl = round(pe_longe - 0.75 * m(pe_longe))
    yp = round(pe_perto - 0.75 * m(pe_perto))
    for xx in (x0 + 2, x1 - 4):                                  # as pernas de trás
        px(xx, yl + 2, 2, pe_longe - yl - 2, "movelEsc")
    px(x0 + 1, yl, x1 - x0 - 2, yp - yl, "movelTopo")
    for y in range(yl + 2, yp, 3):
        px(x0 + 1, y, x1 - x0 - 2, 1, "movelLuz")
    px(x0, yp, x1 - x0, 2, "movel")
    px(x0, yp + 2, x1 - x0, 1, "movelEsc")
    for xx in (x0 + 1, x1 - 3):
        px(xx, yp + 3, 2, pe_perto - yp - 3, "movel")
        px(xx, yp + 3, 1, pe_perto - yp - 3, "movelLuz")
        px(xx - 1, pe_perto, 4, 1, "contato")
    px(x0 + 3, pe_perto - round(0.15 * m(pe_perto)) - 1, x1 - x0 - 6, 1, "movelEsc")  # a travessa
    if vela:
        castical(px, *vela)
    return yl, yp


def castical(px, vx, vy):
    px(vx - 1, vy - 1, 4, 1, "barro")
    px(vx, vy - 5, 2, 4, "cera")
    px(vx + 1, vy - 5, 1, 4, "ceraEsc")


def mesa_redonda(px, cx, pe, raio, vela=None):
    """Uma mesa redonda de um pé: o tampo visto de cima (a elipse), a borda grossa, o pé e a base em cruz."""
    mm = m(pe)
    yt = pe - 0.75 * mm
    rx, ry = raio * mm, raio * mm * 0.36
    for y in range(round(yt - ry), round(yt + ry) + 1):
        for x in range(round(cx - rx), round(cx + rx) + 1):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - yt) / ry) ** 2 <= 1:
                px.p(x, y, "movelTopo")
    for x in range(round(cx - rx) + 1, round(cx + rx)):
        y = round(yt + ry * math.sqrt(max(0.0, 1 - ((x + 0.5 - cx) / rx) ** 2)))
        px(x, y, 1, 2, "movel")
        px.p(x, y + 2, "movelEsc")
    px(round(cx) - 1, round(yt + ry) + 3, 3, pe - round(yt + ry) - 3, "movel")
    px(round(cx) - 1, round(yt + ry) + 3, 1, pe - round(yt + ry) - 3, "movelLuz")
    px(round(cx) - 5, pe - 1, 11, 1, "movelEsc")
    px(round(cx) - 6, pe, 13, 1, "contato")
    if vela:
        castical(px, *vela)
    return round(yt - ry), round(yt + ry)


def cadeira_lado(px):
    """A cadeira da cabeceira da mesa comprida, de lado (virada para a mesa, à esquerda): o assento, os pés até o piso
    e o encosto na ponta da direita, atrás das costas de quem senta."""
    x0, x1, pe = 99, 109, 88
    ys = round(pe - 0.47 * m(pe))
    px(x0, ys, x1 - x0, 2, "movelTopo")
    px(x0, ys + 2, x1 - x0, 1, "movelEsc")
    for xx in (x0 + 1, x1 - 2):
        px(xx, ys + 3, 1, pe - ys - 3, "movel")
    px(x0 + 1, pe - 5, x1 - x0 - 2, 1, "movelEsc")
    alto = round(0.5 * m(pe))
    px(x1 - 2, ys - alto, 2, alto, "movel")
    px(x1 - 2, ys - alto, 1, alto, "movelLuz")
    px(x1 - 3, ys - alto, 3, 1, "movelLuz")
    px(x0, pe, x1 - x0, 1, "contato")


def banco(px, x0, x1, pe, alto=0.45):
    mm = m(pe)
    ys = round(pe - alto * mm)
    px(x0, ys, x1 - x0, 2, "movelTopo")
    px(x0, ys + 2, x1 - x0, 1, "movelEsc")
    for xx in (x0 + 1, x1 - 2):
        px(xx, ys + 3, 1, pe - ys - 3, "movel")
    px(x0, pe, x1 - x0, 1, "contato")
    return ys


# Onde fica cada mesa (as pessoas de gente.py sentam nelas)
MESA_FRENTE = (14, 96, 83, 95)    # a mesa comprida da esquerda: x0, x1, o pé de longe, o de perto
MESA_MEIO = (230, 78, 0.55)       # a redonda: o centro, onde pisa, o raio em metros
MESA_CANTO = (264, 290, 68, 74)   # a de Morel
CANTO_BANCO = (294, 314, 76)      # o banco de espaldar do canto, de lado: o espaldar na ponta da direita


def mesa_frente(px):
    """A mesa comprida da esquerda, com a vela na ponta, a tábua com o pão, a jarra e as canecas."""
    x0, x1, pl, pp = MESA_FRENTE
    yl0 = round(pl - 0.75 * m(pl))
    vela = (x0 + 4, yl0 + 2)
    yl, yp = mesa_ret(px, x0, x1, pl, pp, vela=vela)
    px(46, yl + 3, 12, 3, "movelEsc"); px(47, yl + 2, 10, 2, "pao"); px(48, yl + 2, 4, 1, "paoLuz")   # o pão
    px(68, yl, 4, 5, "barro"); px(68, yl, 1, 5, "barroLuz"); px(69, yl - 1, 2, 1, "barroEsc")        # a jarra
    for x, y in ((36, yl + 3), (82, yl + 4)):
        px(x, y - 3, 3, 4, "estanho"); px(x, y - 3, 1, 4, "estanhoLuz"); px(x + 3, y - 2, 1, 2, "estanhoEsc")
    return (yl, yp), (vela[0], vela[1] - 6)


def mesa_meio(px):
    """A redonda: o tabuleiro de jogo no meio (a tábua quadriculada com as peças), uma caneca de cada lado."""
    cx, pe, raio = MESA_MEIO
    a, b = mesa_redonda(px, cx, pe, raio)
    yc = (a + b) // 2
    px(cx - 4, yc - 1, 8, 3, "linhoSombra")
    for xx in range(cx - 4, cx + 4, 2):
        px(xx, yc - 1, 1, 1, "movelEsc"); px(xx + 1, yc, 1, 1, "movelEsc"); px(xx, yc + 1, 1, 1, "movelEsc")
    px(cx - 2, yc - 2, 1, 1, "linhoLuz"); px(cx + 2, yc - 2, 1, 1, "vigaEsc")
    for x in (cx - 9, cx + 7):
        px(x, yc - 3, 2, 3, "estanho"); px(x, yc - 3, 1, 3, "estanhoLuz")
    vela = (cx + 9, yc + 1)
    castical(px, *vela)
    return (a, b), (vela[0], vela[1] - 6)


def mesa_canto(px):
    """O canto de Morel: a mesa pequena, a vela na ponta de longe dele, o pão e a tigela do ensopado na ponta de perto
    dele, onde a mão alcança."""
    x0, x1, pl, pp = MESA_CANTO
    yl0 = round(pl - 0.75 * m(pl))
    vela = (x0 + 3, yl0 + 1)
    yl, yp = mesa_ret(px, x0, x1, pl, pp, vela=vela)
    px(x0 + 9, yl + 1, 5, 2, "pao"); px(x0 + 10, yl + 1, 2, 1, "paoLuz")
    px(x1 - 9, yl + 1, 7, 1, "ensopado"); px(x1 - 9, yl + 2, 7, 1, "tigela"); px(x1 - 8, yl + 3, 5, 1, "tigela")
    return (yl, yp), (vela[0], vela[1] - 6)


def banco_canto(px):
    """O banco de espaldar do canto, de lado: o assento comprido, os pés, e o espaldar alto na ponta da direita (onde
    Morel apoia as costas), com o braço do banco."""
    x0, x1, pe = CANTO_BANCO
    ys = banco(px, x0, x1, pe)
    alto = round(0.85 * m(pe))
    px(x1 - 3, ys - alto, 3, alto + 1, "movel")
    px(x1 - 3, ys - alto, 1, alto + 1, "movelLuz")
    px(x1 - 4, ys - alto - 1, 5, 1, "movelLuz")


def mesas(px):
    """As mesas e os assentos; devolve onde caem os tampos e as chamas das velas."""
    banco_canto(px)
    banco(px, 225, 237, 72)                                     # o banquinho de quem joga atrás da redonda
    canto, c1 = mesa_canto(px)
    banco(px, 246, 255, 84)                                     # o banquinho vazio da redonda, fora do tampo
    meio, c2 = mesa_meio(px)
    frente, c3 = mesa_frente(px)
    return {"canto": canto, "meio": meio, "frente": frente, "chamas": [c1, c2, c3]}


# ---------------------------------------------------------------- a luz
LUZES = [(162, 50, 36, 1.0), (72, 26, 22, 0.5)]          # a lareira e o lampião: x, y, raio, força


def luz(t, velas):
    """A luz: o escuro cresce aos poucos longe do fogo, do lampião e das velas, sem faixas (as faixas lisas da C ainda
    liam como anéis concêntricos no reboco); o calor da lareira e das velas cai suave nas superfícies perto delas. A
    direita ganha a vela de Morel e a da redonda como ilhas de luz."""
    for y in range(QH):
        for x in range(QW):
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.2)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.2)))
            for vx, vy in velas:
                d = math.hypot(x - vx, (y - vy) * 1.3)
                perto = max(perto, 0.6 * max(0.0, 1 - d / 28))
            escuro = max(0.0, 0.46 - perto * 1.05)
            if escuro > 0:
                t.mistura(x, y, (6, 5, 4), escuro)
            calor = 0.0
            for lx, ly, r, f in LUZES:
                d2 = ((x - lx) ** 2 + ((y - ly) * 1.2) ** 2) / (r * r)
                calor = max(calor, f * max(0.0, 1 - d2) * 0.13)
            for vx, vy in velas:
                d2 = ((x - vx) ** 2 + ((y - vy) * 1.3) ** 2) / (16 * 16)
                calor = max(calor, max(0.0, 1 - d2) * 0.1)
            if calor > 0.004:
                t.mistura(x, y, (255, 160, 80), calor)


def lampiao(px):
    """O lampião de ferro pendurado na viga por uma corrente, sobre o balcão (a chama vem na camada velas)."""
    x, y0, yc = LAMPIAO
    for y in range(y0, yc - 3, 2):
        px.p(x, y, "ferroLuz")
        px.p(x, y + 1, "ferro")
    px(x - 2, yc - 3, 5, 1, "ferroLuz")
    px(x - 2, yc - 2, 1, 4, "ferro")
    px(x + 2, yc - 2, 1, 4, "ferro")
    px(x - 2, yc + 2, 5, 1, "ferroLuz")


def chamas_velas():
    """Onde ficam as chamas: o lampião e as velas das três mesas."""
    x, _, yc = LAMPIAO
    return [(x, yc - 1)] + mesas(Pincel(Tela(QW, QH)))["chamas"]


# ---------------------------------------------------------------- as camadas
def so_o_espaco():
    """O espaço sozinho (as paredes, o piso, a viga), sem móveis nem pessoas: a conferência do piso e dos planos."""
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    piso(px)
    return t


def sala(px):
    """A sala com os móveis, sem as pessoas e sem a luz; devolve onde caem os tampos."""
    paredes(px)
    piso(px)
    porta(px, 7, 26, round(BAR_Y - 1.95 * m(BAR_Y)), BAR_Y)   # a porta da rua
    prateleiras(px)
    lareira(px)
    escada_e_galeria(px)
    porta_despensa(px)
    lampiao(px)
    aparador(px)
    r = mesas(px)
    r["balcao"] = balcao(px)
    return r


def fogo(i):
    """O fogo da lareira (4 quadros): a lenha nos cães de ferro, as línguas que afinam para cima e o caldeirão na
    cremalheira, na frente das chamas."""
    t = Tela(QW, QH)
    px = Pincel(t)
    x0, x1 = LAREIRA
    cx = (x0 + x1) // 2
    base = FUNDO_Y - 3
    linguas = [[(cx - 6, 5, 0), (cx - 3, 8, 1), (cx, 9, 0), (cx + 3, 7, -1), (cx + 6, 4, 0)],
               [(cx - 6, 6, 1), (cx - 3, 7, 0), (cx, 8, -1), (cx + 3, 8, 0), (cx + 6, 5, -1)],
               [(cx - 6, 4, 0), (cx - 3, 9, -1), (cx, 8, 1), (cx + 3, 6, 0), (cx + 6, 5, 0)],
               [(cx - 6, 5, -1), (cx - 3, 8, 0), (cx, 10, 0), (cx + 3, 7, 1), (cx + 6, 4, 1)]][i]
    for x, h, pende in linguas:
        for r in range(h):
            f = r / h
            dx = pende if f > 0.6 else 0
            larg = 3 if f < 0.45 else 2 if f < 0.8 else 1
            xa = x - larg // 2 + dx
            px(xa, base - r, larg, 1, "chamaFora")
            if larg >= 3:
                px(xa + 1, base - r, 1, 1, "chama")
            if r < 2 and h >= 7:
                px.p(x, base - r, "chamaMiolo")
    px(cx - 8, FUNDO_Y - 3, 16, 2, "vigaEsc")                  # a lenha atravessada
    px(cx - 8, FUNDO_Y - 3, 2, 2, "brasa")
    px(cx + 6, FUNDO_Y - 3, 2, 2, "brasa")
    px.p(cx - 1 + (i % 2) * 2, FUNDO_Y - 1, "brasa")
    for xx in (cx - 7, cx + 6):                                 # os cães de ferro
        px(xx, FUNDO_Y - 2, 1, 2, "ferro")
    px(cx, 44, 1, 2, "ferro")                                   # a cremalheira e o caldeirão, pequeno e alto:
    px(cx - 3, 46, 7, 1, "ferroLuz")                            # o fogo aparece dos lados e embaixo dele
    px(cx - 3, 47, 7, 2, "ferro")
    px(cx - 2, 49, 5, 1, "ferroEsc")
    return t


def velas(i):
    """As chamas do lampião e das velas (4 quadros, cada uma no seu passo): por cima de tudo."""
    t = Tela(QW, QH)
    px = Pincel(t)
    for j, (x, y) in enumerate(chamas_velas()):
        f = (i + j * 3) % 4
        alto = 3 if f in (0, 2) else 2 if f == 1 else 4
        px(x, y - alto + 2, 1, alto, "chamaFora")
        px.p(x, y + 1, "chama")
        if alto >= 3:
            px.p(x, y, "chamaMiolo" if f == 3 else "chama")
    return t
