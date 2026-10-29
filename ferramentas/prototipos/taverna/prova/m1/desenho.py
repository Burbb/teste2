"""M1: Morel, a cadeira e a mesa dele, desenhados juntos na densidade da B4 (2×2 pixels por pixel da sala), estático, no
protótipo. Os jogadores (a B4) não mudam.

O recorte é o canto da direita da sala: de x 248 a 320 e de y 36 a 92 da sala (72×56), ou seja, 144×112 na grade do
conjunto. Ele não segue o 132×84 dos jogadores: as medidas saem da composição do canto.

Este código só semeia a fonte: `fonte.py --criar` monta `aseprite/m1.aseprite` com a guia (o canto da referência geral,
oculto, fora da exportação) e as camadas cadeira, mesa, morel e frente. Depois de criada, a fonte é a autoridade.

**A escala** sai da mesma câmera da sala (a projeção da F, `f.desenho.P`) na profundidade de cada grupo: os jogadores em
Z 3,3 (44,5 pixels da grade por metro), Morel em Z 3,6 (46 por metro), um pouco mais perto. A cabeça dos jogadores fica
a 1,44 m do piso; a de Morel, sentado e inclinado para a tigela, a ~1,45 m, com o corpo mais largo (os ombros com 0,7 m
contra 0,58 m), as coxas e as botas maiores: maior pelo porte, na mesma escala.

**A composição** vem da referência geral ("entre brasas e sombras"): a cadeira de espaldar robusta com as costas à
esquerda, ele de frente para a mesa individual à direita, inclinado sobre o ensopado, a colher na mão de cá e a outra
mão junto da tigela. O conjunto foi aproximado do meio da sala (a cadeira em X 4,6 a 5,15, a mesa em 5,5 a 6,1) para a
mesa ficar inteira, com ~14 pixels de margem à direita. A aparência é a do jogo (retratos.js): o cabelo e a barba
castanhos, a cicatriz clara em diagonal no rosto, a ombreira cinza no ombro de cá (o direito), a pele no de lá, o couro e
a faixa vermelha no peito; nada da capa, das armas e das placas da referência.

Morel em pé de frente para a direita, em três quartos para a câmera (o peito com a faixa vermelha à vista): o ombro de
cá com a ombreira, à esquerda; o braço de cá desce na frente do tronco, num couro mais claro que o do peito, e o
antebraço vai à tigela com a colher; o ombro de lá com a pele, à direita; o braço de lá sai à direita do peito, mais
escuro, e o antebraço pousa no tampo, a mão junto da tigela. As mãos são bolinhas, como nas outras cenas.
"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(AQUI)))

from f import desenho as D  # noqa: E402
from prova import conjunto as C  # noqa: E402

M = (248, 36, 72, 56)                    # o recorte na sala: x, y, largura, altura
S = 2
W, H = M[2] * S, M[3] * S
CADEIRA = (4.6, 5.15, 3.35, 3.9)
ALTURA_ASSENTO, ALTURA_ESPALDAR = 0.47, 1.15
MESA = (5.5, 6.1, 3.3, 3.95)
ALTURA_MESA = 0.75
VELA = (5.95, 3.45)                      # o castiçal (a chama vem da camada de velas da sala, neste ponto)


def Pm(X, Z, Hh):
    x, y = D.P(X, Z, Hh)
    return ((x - M[0]) * S, (y - M[1]) * S)


def vela_sala():
    """A chama da vela de Morel em coordenadas da sala, como o castiçal da F a calcula (para a camada de velas)."""
    x, y = [round(v) for v in D.P(VELA[0], VELA[1], ALTURA_MESA)]
    return (x, y - 6)


def caixa(px, X0, X1, Z0, Z1, H0, H1, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz"):
    """Uma caixa na projeção: a face de cima, a da frente e a lateral que a câmera vê (a da esquerda, à direita da sala)."""
    px.poligono([Pm(X0, Z0, H0), Pm(X0, Z1, H0), Pm(X0, Z1, H1), Pm(X0, Z0, H1)], lado)
    px.poligono([Pm(X0, Z1, H0), Pm(X1, Z1, H0), Pm(X1, Z1, H1), Pm(X0, Z1, H1)], frente)
    if topo:
        px.poligono([Pm(X0, Z0, H1), Pm(X1, Z0, H1), Pm(X1, Z1, H1), Pm(X0, Z1, H1)], topo)
    if aresta:
        (xa, ya), (xb, _) = Pm(X0, Z1, H1), Pm(X1, Z1, H1)
        px(round(xa), round(ya), round(xb) - round(xa), 1, aresta)


def perna(px, X, Z, Hh, larg=0.07, cor="movel", luz=True):
    (x, yt), (_, yp) = Pm(X, Z, Hh), Pm(X, Z, 0)
    w = max(2, round(larg * D.m(Z) * S))
    px(round(x), round(yt), w, round(yp - yt), cor)
    if luz:
        px(round(x), round(yt), 1, round(yp - yt), "movelLuz")


def sombra(px, X0, X1, Z0, Z1):
    px.poligono([Pm(X0 - 0.04, Z0, 0), Pm(X1 + 0.04, Z0, 0), Pm(X1 + 0.06, Z1 + 0.04, 0), Pm(X0, Z1 + 0.04, 0)],
                "contato")


# ---------------------------------------------------------------- a cadeira (atrás dele) e a frente dela
def cadeira(px):
    """A cadeira de espaldar robusta: as pernas de trás, o espaldar (os montantes com o pomo e três travessas), o
    assento grosso e as pernas da frente. O montante da frente do espaldar vem depois de Morel (`cadeira_frente`)."""
    X0, X1, Z0, Z1 = CADEIRA
    Ha = ALTURA_ASSENTO
    sombra(px, X0, X1, Z0, Z1)
    perna(px, X1 - 0.08, Z0 + 0.04, Ha, cor="movelEsc", luz=False)          # as de trás
    perna(px, X0 + 0.02, Z0 + 0.04, ALTURA_ESPALDAR, cor="movelEsc", luz=False)
    for Hh in (Ha + 0.22, Ha + 0.42, ALTURA_ESPALDAR - 0.08):            # as travessas do espaldar
        (xa, ya), (xb, yb) = Pm(X0 + 0.04, Z0 + 0.04, Hh), Pm(X0 + 0.04, Z1 - 0.04, Hh)
        for k in range(3):
            px.linha(xa, ya + k, xb, yb + k, "movelLuz" if k == 0 else "movel")
    (x, y) = Pm(X0 + 0.02, Z0 + 0.04, ALTURA_ESPALDAR + 0.06)            # o pomo do montante de trás
    px(round(x), round(y), 3, 3, "movelLuz")
    (xa, y), (xb, _) = Pm(X0 + 0.03, Z1 - 0.04, 0.16), Pm(X1 - 0.03, Z1 - 0.04, 0.16)
    px(round(xa), round(y), round(xb - xa), 2, "movelEsc")                # a travessa baixa da frente
    caixa(px, X0, X1, Z0, Z1, Ha - 0.07, Ha)
    perna(px, X1 - 0.08, Z1 - 0.05, Ha - 0.07)                           # as da frente
    perna(px, X0 + 0.02, Z1 - 0.05, Ha - 0.07)


def cadeira_frente(px):
    """O montante da frente do espaldar, que passa na frente das costas de Morel, com o pomo."""
    X0, _, _, Z1 = CADEIRA
    (x, yt), (_, yp) = Pm(X0 + 0.02, Z1 - 0.05, ALTURA_ESPALDAR), Pm(X0 + 0.02, Z1 - 0.05, ALTURA_ASSENTO)
    px(round(x), round(yt), 3, round(yp - yt), "movel")
    px(round(x), round(yt), 1, round(yp - yt), "movelLuz")
    px(round(x) + 2, round(yt), 1, round(yp - yt), "movelEsc")
    px(round(x), round(yt) - 3, 3, 3, "movelLuz")
    px(round(x) + 1, round(yt) - 4, 1, 1, "movelLuz")


# ---------------------------------------------------------------- a mesa
def mesa(px):
    """A mesa individual: as quatro pernas, a travessa baixa, o tampo com a espessura e a aresta da frente, e o
    castiçal (a chama vem da camada de velas). A tigela é de Morel (sai quando ele não está)."""
    X0, X1, Z0, Z1 = MESA
    sombra(px, X0, X1, Z0, Z1)
    perna(px, X1 - 0.07, Z0 + 0.04, ALTURA_MESA, cor="movelEsc", luz=False)
    perna(px, X0 + 0.02, Z0 + 0.04, ALTURA_MESA, cor="movelEsc", luz=False)
    (xa, y), (xb, _) = Pm(X0 + 0.04, Z1 - 0.04, 0.14), Pm(X1 - 0.04, Z1 - 0.04, 0.14)
    px(round(xa), round(y), round(xb - xa), 2, "movelEsc")
    perna(px, X1 - 0.07, Z1 - 0.05, ALTURA_MESA)
    perna(px, X0 + 0.02, Z1 - 0.05, ALTURA_MESA)
    caixa(px, X0, X1, Z0, Z1, ALTURA_MESA - 0.06, ALTURA_MESA)
    xs, ys = vela_sala()                                              # o castiçal, nos pixels da sala da chama
    x0, y0 = (xs - M[0]) * S, (ys + 6 - M[1]) * S
    px(x0 - 2, y0 - 2, 8, 2, "barro")
    px(x0 - 2, y0 - 2, 8, 1, "barroLuz")
    px(x0, y0 - 10, 4, 8, "cera")
    px(x0 + 2, y0 - 10, 2, 8, "ceraEsc")


# ---------------------------------------------------------------- Morel, à mão
PAL = {
    "k": "#33231a", "C": "#6a4a2c", "c": "#4e3420",                     # o cabelo
    "b": "#5a3e2a", "B": "#3e2a1c",                                     # a barba
    "P": "#c09070", "p": "#9a6c52", "x": "#d8aa90", "e": "#20160f",     # a pele, a cicatriz, o olho
    "G": "#b0b2b8", "S": "#9a9ca4", "s": "#6e7078", "d": "#4a4c52",     # a ombreira
    "F": "#6a6058", "f": "#4e4640", "n": "#34302c",                     # a pele no ombro de lá
    "L": "#7a5636", "l": "#553a22", "o": "#8e6842", "Y": "#a8804e",     # o couro (o braço de cá mais claro)
    "R": "#8a3428", "r": "#5e241c",                                     # a faixa vermelha
    "t": "#2a1c14", "a": "#9a7c44",                                     # o cinto e a fivela
    "Q": "#5a5048", "q": "#3a322c", "u": "#786c60", "v": "#2c2622",                     # a calça
    "O": "#2e2016", "w": "#5a4030", "W": "#7a5a40", "z": "#1a120c",     # as botas
    "h": "#c4c6cc", "T": "#4a2814", "E": "#b07a3c", "A": "#9a6a3a",     # a colher, a tigela, o ensopado
}


def tom(a, b, esq, meio, dir=""):
    n = b - a + 1 - len(esq) - len(dir)
    return (a, (esq + meio * max(0, n) + dir)[:b - a + 1])


def _morel():
    L = {}

    def por(rows):
        for y, tr in rows.items():
            L.setdefault(y, []).extend(tr if isinstance(tr, list) else [tr])

    # as pernas: a de lá (mais alta na tela, à esquerda, na sombra) e a de cá (mais baixa, à direita, acesa pela vela)
    por({61: tom(66, 77, "q", "Q", "uu"), 62: tom(62, 78, "q", "Q", "uu"), 63: tom(60, 79, "q", "Q", "Qu"),
         64: tom(60, 78, "q", "Q", "Q"), 65: tom(70, 78, "q", "q", "q")})
    por({y: (71, "vqqqqv") for y in range(66, 80)})                    # a canela de lá, recuada
    por({80: (70, "OwwwwwO"), 81: (70, "OwwwwwO"), 82: (70, "zOOOOOz")})
    por({y: (70, "Owwwww") for y in range(83, 87)})
    por({87: (70, "Owwwww"), 88: (70, "Owwwwwwo"), 89: (69, "OOOOOOOOO"), 90: (69, "zzzzzzzzz")})
    por({64: tom(42, 80, "q", "Q", "u"), 65: tom(42, 82, "q", "Q", "uu"), 66: tom(42, 83, "q", "Q", "uu"),
         67: tom(42, 83, "q", "Q", "Qu"), 68: tom(42, 83, "q", "Q", "Q"), 69: tom(44, 83, "q", "Q", "q"),
         70: tom(46, 82, "q", "q", "q")})
    for x in range(48, 78):                                          # a luz da vela no alto da coxa de cá
        L[64].append((x, "u"))
    por({y: (77, "vQQQuu") for y in range(71, 83)})                    # a canela de cá, com a frente acesa
    por({71: (77, "vQQQQu"), 72: (77, "vQQQQu")})
    por({83: (76, "OWWWWWWO"), 84: (76, "OwwwwwWO"), 85: (76, "zOOOOOOz")})
    por({y: (76, "OwwwwwWw") for y in range(86, 90)})
    por({90: (76, "OwwwwwwWw"), 91: (75, "OOwwwwwwW"), 92: (75, "OOOOOOOOOO"), 93: (75, "zzzzzzzzzz")})
    por({64: (79, "uuuu"), 65: (80, "uuu"), 66: (81, "uu")})                        # o joelho de cá
    # o tronco: as costas afastadas do espaldar no alto (inclinado para a tigela), a frente do peito para a mesa
    bordas = {39: (47, 73), 40: (46, 74), 41: (45, 74), 42: (45, 74), 43: (44, 75), 44: (44, 75), 45: (44, 75),
              46: (43, 75)}
    bordas.update({y: (43, 76) for y in range(47, 56)})
    bordas.update({56: (43, 75), 57: (43, 74), 58: (43, 73), 59: (43, 72), 60: (43, 72), 61: (43, 72), 62: (44, 70),
                   63: (44, 66)})
    por({y: tom(a, b, "ll", "L", "oY") for y, (a, b) in bordas.items()})
    for y in range(39, 60):                                          # a faixa vermelha no meio do peito
        x0 = 63 if y < 45 else 62 if y < 53 else 61
        L[y].append((x0, "RRRrr"))
    por({60: (43, "t" * 30), 61: (43, "t" * 19 + "aa" + "t" * 9)})
    por({62: (44, "l" + "L" * 25 + "l"), 63: (44, "l" * 23)})
    # o ombro de lá, com a pele, à direita do pescoço
    por({36: (68, "nfFFf"), 37: (67, "nfFFFFf"), 38: (67, "fFFFFFFf"), 39: (68, "fFFFFFn"), 40: (70, "fFFFn")})
    # o braço de lá: sai à direita do peito, mais escuro; o antebraço pousa no tampo, a mão junto da tigela
    por({41: (73, "lLLl"), 42: (74, "lLLl"), 43: (75, "lLLl"), 44: (75, "lLLLl"), 45: (76, "lLLLl"), 46: (76, "lLLLl"),
         47: (77, "lLLLl"), 48: (77, "lLLLl"), 49: (78, "lLLLl"), 50: (78, "lLLLLl"), 51: (78, "lLLLLLl"),
         52: (78, "lLLLLLLLLLl"), 53: (78, "llLLLLLLLLLl"), 54: (79, "llllllllll")})
    por({53: (89, "pPP"), 54: (89, "pPPp"), 55: (90, "pp")})
    # a cabeça: o cabelo curto, a orelha, a sobrancelha, o olho, a cicatriz clara em diagonal, o nariz, a barba cheia
    cabeca = {
        23: (57, "kkCCCk"),
        24: (55, "kCCCCCCCk"),
        25: (54, "kCCcCCCCCck"),
        26: (54, "kCcCCCCCCCCk"),
        27: (54, "kcCCCCCCPPPP"),
        28: (54, "kcCCCCCxPPPPP"),
        29: (54, "kCCCCCCPxPPPPP"),
        30: (54, "kcCCCCpPPxPeeeP"),
        31: (54, "kcCCCppPPPxPePPx"),
        32: (54, "kCCCbpPPPPPxPPPP"),
        33: (55, "kCbbBbPPPPPxpPp"),
        34: (55, "kbBbbbbPPbbbbbb"),
        35: (56, "BbbbbbbbbBBbbb"),
        36: (57, "Bbbbbbbbbbbb"),
        37: (59, "BbbbbbbbB"),
        38: (61, "BbbbbB"),
    }
    por({y + 1: (x + 2, txt) for y, (x, txt) in cabeca.items()})       # a cabeça adiante e baixa: debruçado na tigela
    # o ombro de cá com a ombreira cinza (a luz por cima, a lâmina de baixo)
    por({35: (47, "sGGGs"), 36: (45, "sGGGGGs"), 37: (44, "sGGGGGGSs"), 38: (43, "sSGGGGGSSs"),
         39: (43, "sSSGGSSSSSs"), 40: (43, "sSSSSSSSSSs"), 41: (43, "dsssssssssd"), 42: (43, "sSSSSSSSSs"),
         43: (44, "dssssssd")})
    # o braço de cá, num couro mais claro, na frente do tronco: do ombro ao cotovelo, o antebraço até a tigela
    sup = {44: (45, 51), 45: (46, 52), 46: (46, 52), 47: (47, 53), 48: (47, 53), 49: (48, 54), 50: (48, 55),
           51: (49, 56), 52: (50, 58), 53: (51, 59), 54: (52, 59)}
    por({y: tom(a, b, "l", "o", "Y") for y, (a, b) in sup.items()})
    por({48: (71, "oooooY"), 49: (61, "ooooooooooooooY"), 50: (56, "ooooooooooooooooooY"),
         51: (56, "loooooooooooooooool"), 52: (58, "llllllllllllll")})
    return L


def _maos():
    """A tigela com o ensopado (por cima do braço de lá), a mão de cá com a colher dentro dela."""
    return {
        52: [(80, "AAAAAAA"), (81, "h")],
        53: [(79, "AEEEEEEEA")],
        54: [(79, "TTTTTTTTT")],
        55: [(80, "TTTTTTT")],
        56: [(81, "TTTTT")],
        47: [(76, "PP")], 48: [(75, "PPPp")], 49: [(75, "PPPp")], 50: [(76, "pp"), (79, "h")], 51: [(80, "h")],
    }


MOREL, MAOS = _morel(), _maos()


# ---------------------------------------------------------------- a luz e as camadas
def chamas():
    """As fontes de luz da sala com o canto da prova: as da F, com a vela de Morel no castiçal novo."""
    D.SEM_CANTO, D.VELA_MOREL = True, vela_sala()
    try:
        r = D.sala(D.Pincel(D.Tela(D.QW, D.QH)))
    finally:
        D.SEM_CANTO, D.VELA_MOREL = False, None
    return r["boca"], r["chamas"]


def luz(t):
    """A luz da sala no ponto de cada pixel (a mesma conta de conjunto.luz, neste recorte)."""
    boca, chs = chamas()
    fontes = [(boca[0], boca[1] - 6, 40, 1.0)] + [(x, y, 22, 0.6) for x, y in chs]
    for j in range(t.h):
        for i in range(t.w):
            x, y = M[0] + (i + 0.5) / S, M[1] + (j + 0.5) / S
            perto = max(f * max(0.0, 1 - math.hypot(x - fx, (y - fy) * 1.2) / (rr * 2)) for fx, fy, rr, f in fontes)
            escuro = max(0.0, 0.46 - perto * 1.05)
            if escuro > 0:
                t.mistura(i, j, (6, 5, 4), escuro)
            calor = max(f * max(0.0, 1 - ((x - fx) ** 2 + ((y - fy) * 1.2) ** 2) / (rr * rr)) * 0.12
                        for fx, fy, rr, f in fontes)
            if calor > 0.004:
                t.mistura(i, j, (255, 160, 80), calor)


def camadas():
    """{nome: Tela 144×84}: as camadas da fonte, de baixo para cima, já com a luz da sala."""
    r = {}
    for nome, fazer in (("cadeira", cadeira), ("mesa", mesa)):
        t = D.Tela(W, H)
        fazer(C.Pincel(t))
        r[nome] = t
    t = D.Tela(W, H)
    px = C.Pincel(t)
    px.trechos(MOREL, PAL)
    px.trechos(MAOS, PAL)
    r["morel"] = t
    t = D.Tela(W, H)
    cadeira_frente(C.Pincel(t))
    r["frente"] = t
    for t in r.values():
        luz(t)
    return r


PRESENTE = ("cadeira", "mesa", "morel", "frente")   # Morel no canto
AUSENTE = ("cadeira", "mesa", "frente")            # recrutado: a cadeira e a mesa, sem nada dele


def composto(cs, nomes):
    t = D.Tela(W, H)
    for n in nomes:
        t.sobre(cs[n])
    return t
