"""A B2: os dois jogadores refinados na grade B (132×84), pela referência "Jogo de tabuleiro na taverna" (poses, volumes
e a relação com a mesa e os banquinhos), com o acabamento das cenas aprovadas (a forja, a curandeira, o templo).

Este código só semeia a fonte: `fonte.py --criar` monta `aseprite/b2.aseprite` com as camadas que ele desenha (os
banquinhos, a mesa, o de verde, o de ocre) e a guia (a referência na grade, oculta, fora da exportação). Depois de
criada, a fonte é a autoridade; os retoques se fazem nela.

As pessoas são desenhadas à mão, parte por parte, em trechos por linha (`{y: (x, "pixels")}`, coordenadas do quadro
132×84), pintadas na ordem de trás para a frente. A faixa `faixa(a, b, ...)` só enche uma linha de a até b com a borda
de sombra, o meio e a borda acesa; os volumes, as dobras, o rosto e as mãos são escritos pixel a pixel por cima.

A geometria que decide (medida na grade sobre a guia):
- o de verde: o quadril no banquinho (o assento em y 49 a 54), as costas curvas de (12, 47) aos ombros em (25, 23); o
  braço da mesa com o ombro em (37, 27), o cotovelo **no tampo** em (46, 39) e o punho debaixo do queixo em (43, 26):
  braço 13 px, antebraço 11 px (a mesma conta da referência, com o cotovelo baixado ~7 px até o tampo e o tronco mais
  inclinado para chegar lá); o outro braço pelas costas, a mão na coxa em (25, 44); a perna de perto com a canela
  para trás (a bota em y 75), a de lá com a canela em pé (a bota em y 72);
- o de ocre: mais magro, as costas de (104, 46) aos ombros em (95, 25); o braço estendido do ombro em (82, 29) ao
  cotovelo em (71, 33) e à mão na peça em (62, 37); a outra mão na coxa em (92, 44); as pernas espelhando as do de
  verde.
"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(AQUI)))

from f import desenho as D  # noqa: E402
from prova import conjunto as C  # noqa: E402

W, H = 132, 84
S = 2                                            # a grade B: 2×2 pixels por pixel da sala
# os banquinhos afastados da mesa, como na referência (os centros em x 17 e 104 da grade), mais estreitos e mais altos
BANCO_ESQ = (0.86, 1.20, 3.1, 3.5)
BANCO_DIR = (2.80, 3.14, 3.1, 3.5)
ALTURA_BANCO = 0.5


def faixa(a, b, e="z", m="N", d="Z", ne=1, nd=1):
    """Uma linha de a até b (inclusive): ne pixels de sombra à esquerda, o meio, nd pixels de luz à direita."""
    n = b - a + 1
    ne, nd = min(ne, n), min(nd, max(0, n - ne))
    return (a, e * ne + m * (n - ne - nd) + d * nd)


def tom(a, b, esq, meio, dir=""):
    """Uma linha de a até b (inclusive): a borda esquerda (texto), o meio repetido, a borda direita (texto)."""
    n = b - a + 1 - len(esq) - len(dir)
    return (a, (esq + meio * max(0, n) + dir)[:b - a + 1])


def partes(*ps):
    """Junta as partes na ordem (as de depois por cima): {y: [(x, "pixels"), ...]}."""
    L = {}
    for p in ps:
        for y, tr in p.items():
            L.setdefault(y, []).extend(tr if isinstance(tr, list) else [tr])
    return L


# ---------------------------------------------------------------- o de verde
PAL_VERDE = {
    "k": "#1e150d", "K": "#3a2a1e", "H": "#56402c",                     # o cabelo
    "b": "#24190f", "B": "#3a2a1e", "j": "#4e3a28",                     # a barba
    "S": "#94684c", "s": "#c4946e", "l": "#e2b490", "e": "#22160e", "m": "#6e4632",   # a pele, o olho, a boca
    "z": "#1f2c22", "n": "#2f4532", "N": "#45633e", "Z": "#5f8352", "W": "#7fa86a",   # a túnica
    "c": "#2e1c10", "C": "#4a3020", "f": "#9a7c44",                     # o cinto
    "p": "#2a2420", "P": "#3e3630", "q": "#554a40",                     # a calça
    "d": "#1a120c", "O": "#3a281a", "o": "#5a4030", "u": "#7a5a40",      # as botas
}


def verde_partes():
    """As partes do de verde, na ordem de pintura ({nome: trechos}); a B3 troca algumas."""
    # as pernas primeiro (a túnica vem por cima no quadril): a coxa de lá e o joelho dela, a canela em pé, a bota
    coxa_la = {44: (38, "pPPPPPqq"), 45: (33, "pPPPPPPPPPPPqqq"), 46: (28, "p" + "P" * 18 + "qq"),
               47: [(24, "p" * 18), (42, "PPPPPqq")], 48: (43, "pPPPqq"), 49: (45, "Pqp"), 50: (46, "Pp")}
    canela_la = {y: (42, "pPPPqq") for y in range(51, 59)}
    bota_la = {59: (41, "OOoooouO"), 60: (41, "OooooouO"), 61: (42, "dOOOOOd")}
    bota_la.update({y: (42, "OOooouO") for y in range(62, 68)})
    bota_la.update({68: (42, "OOoooouuo"), 69: (41, "OOOooooouuo"), 70: (41, "OOOoooooouuo"), 71: (41, "O" * 12),
                    72: (41, "d" * 12)})
    # a coxa de cá (a de baixo na tela), com a luz da vela por cima, o joelho; a canela para trás; a bota no piso
    coxa_ca = {47: (13, "pPPPPPPPPP"), 48: (12, "p" + "P" * 11 + "q" * 19), 49: (12, "p" + "P" * 29 + "qqq"),
               50: (12, "p" + "P" * 29 + "qqqp"), 51: (12, "pp" + "P" * 28 + "Pqqp"), 52: (12, "pp" + "P" * 29 + "qPp"),
               53: (14, "p" * 26 + "PPqPp"), 54: (36, "pPPPqPPp")}
    canela_ca = {55: (36, "pPPPPPqq"), 56: (35, "pPPPPPqq"), 57: (34, "ppPPPPPqq"), 58: (34, "pPPPPPqq"),
                 59: (33, "pPPPPPqq"), 60: (33, "pPPPPPqq"), 61: (32, "pPPPPPqq"), 62: (32, "pPPPPPqq")}
    bota_ca = {63: (31, "OOooooouuO"), 64: (31, "OooooooouO"), 65: (32, "dOOOOOOd")}
    bota_ca.update({y: (32, "OOooooou") for y in range(66, 71)})
    bota_ca.update({71: (32, "OOooooouo"), 72: (32, "OOoooooouo"), 73: (31, "OOOoooooouuo"), 74: (31, "O" * 13),
                    75: (31, "d" * 13)})
    # o tronco: as costas curvas (a esquerda, na sombra), a frente para a mesa (a direita, acesa pela vela)
    bordas = {23: (25, 31), 24: (23, 33), 25: (21, 35), 26: (20, 36), 27: (18, 37), 28: (17, 38), 29: (16, 38),
              30: (15, 39), 31: (14, 39), 32: (14, 40), 33: (13, 40), 34: (13, 41)}
    bordas.update({y: (12, 41) for y in range(35, 40)})
    bordas.update({40: (12, 40), 41: (12, 39), 42: (12, 39), 43: (12, 39), 44: (12, 37), 45: (12, 34), 46: (12, 30),
                   47: (12, 26), 48: (13, 22)})
    tronco = {y: [tom(a, b, "zn", "N", "ZZ")] for y, (a, b) in bordas.items()}
    tronco[23] = [(25, "nNNZZZZ")]                                  # o alto dos ombros
    tronco[24] = [(23, "znNNNZZZZZN")]
    for y, b in ((27, 34), (28, 35), (29, 36), (30, 37), (31, 37), (32, 38), (33, 39), (34, 40), (35, 40), (36, 41),
                 (37, 41)):                                         # a sombra do braço da mesa no peito
        tronco[y].append((b - 4, "nnnz"))
    for x, y in ((24, 33), (25, 34), (25, 35), (26, 36), (26, 37), (27, 38), (27, 39), (31, 38), (32, 39), (32, 40)):
        tronco[y].append((x, "n"))                                  # as dobras da túnica
    for y in (42, 43):                                              # o cinto
        tronco[y].append((13, "c" + "C" * 13 + "f" + "C" * 11 + "c"))
    tronco[44].append((13, "n"))
    tronco[48].append((13, "zzzzzzzzzz"))                           # a barra da túnica no assento
    # o braço de trás, pelas costas (a dobra separa a manga das costas): o punho dobrado, o antebraço, a mão na coxa
    manga = {26: (19, 24), 27: (17, 23), 28: (16, 22), 29: (15, 21), 30: (14, 20), 31: (13, 19), 32: (13, 19),
             33: (12, 18), 34: (11, 18), 35: (11, 18)}
    braco_tras = {y: tom(a, b, "z", "n", "Nz") for y, (a, b) in manga.items()}
    braco_tras.update({36: (11, "nNNNNNNz"), 37: (11, "znnnnnnz"), 38: (12, "zzzzzz")})
    mao_coxa = {38: (14, "Sssl"), 39: (15, "Sssssl"), 40: (16, "Sssssll"), 41: (18, "Ssssssl"),
                42: (20, "Sssssll"), 43: (21, "SsssslllS"), 44: (22, "SsSsSsS"), 45: (23, "SSsSsS"), 46: (24, "SS")}
    # a cabeça inclinada para o tabuleiro: o cabelo, a orelha, a sobrancelha, o olho, o nariz, a barba cheia
    cabeca = {
        11: (32, "kkkkk"),
        12: (30, "kkKKKKKk"),
        13: (29, "kKKHHHKKKk"),
        14: (28, "kKKHHHHHKKKk"),
        15: (28, "kKKKHHHKKKKKk"),
        16: (28, "kKKKKKKKKKKKss"),
        17: (28, "kKKKKKKKKssslll"),
        18: (28, "kKKKKSsKsssKKKsl"),
        19: (28, "kKKKSSsKssseeSll"),
        20: (29, "kKKKSKBsssssSlll"),
        21: (29, "kKKKKBBBsssSSllS"),
        22: (30, "kKKBBBBBjBBBBB"),
        23: (31, "kkbBBBBjBBBb"),
        24: (33, "bbBBBBBBb"),
        25: (35, "bBBBb"),
    }
    # o braço da mesa: a manga do ombro ao cotovelo, que pousa no tampo; o antebraço sobe até o punho no queixo
    sup = {25: (33, 39), 26: (33, 40), 27: (34, 40), 28: (35, 41), 29: (36, 41), 30: (37, 42), 31: (37, 43),
           32: (38, 43), 33: (39, 44), 34: (40, 45), 35: (40, 46), 36: (41, 46), 37: (42, 47), 38: (43, 48)}
    braco = {y: faixa(a, b, "z", "N", "W" if y < 29 else "Z", 1, 1) for y, (a, b) in sup.items()}
    braco[39] = faixa(44, 48, "n", "n", "n")                           # o cotovelo no tampo
    ante = {29: faixa(42, 45, "S", "s", "l"), 30: faixa(43, 46, "S", "s", "l"), 31: faixa(43, 46, "S", "s", "l"),
            32: faixa(43, 46, "S", "s", "l"), 33: faixa(44, 47, "S", "s", "l"), 34: faixa(44, 47, "Z", "W", "W"),
            35: faixa(45, 48, "Z", "W", "W"), 36: faixa(45, 48, "N", "Z", "Z"), 37: faixa(46, 48, "N", "Z", "Z")}
    punho = {24: (41, "slll"), 25: (40, "sllllsS"), 26: (40, "SsSlllS"), 27: (40, "sSsllsS"), 28: (41, "SsllsS")}
    return dict(coxa_la=coxa_la, canela_la=canela_la, bota_la=bota_la, coxa_ca=coxa_ca, canela_ca=canela_ca,
                bota_ca=bota_ca, tronco=tronco, braco_tras=braco_tras, mao_coxa=mao_coxa, cabeca=cabeca, braco=braco,
                ante=ante, punho=punho)


# ---------------------------------------------------------------- o de ocre
PAL_OCRE = {
    "k": "#4a2c12", "K": "#74491f", "H": "#966434",
    "S": "#9c6e50", "s": "#cc9c78", "l": "#e6bc98", "e": "#22160e", "m": "#7a4a34",
    "x": "#4e3c1e", "y": "#76602f", "Y": "#a2843f", "X": "#c4a457", "W": "#dcc070",
    "c": "#2e1c10", "C": "#4a3020", "f": "#9a7c44", "r": "#b0603a", "R": "#7a3a22",
    "p": "#25232a", "P": "#38353f", "q": "#4c4854",
    "d": "#1a120c", "O": "#3a281a", "o": "#5a4030", "u": "#7a5a40",
}


def ocre_partes():
    """As partes do de ocre, na ordem de pintura ({nome: trechos}); a B3 troca algumas."""
    # o espelho do de verde, mais magro: a coxa de lá com o joelho à frente, a canela em pé, a bota
    coxa_la = {44: (76, "qqPPPPPPPPp"), 45: (74, "qqq" + "P" * 13 + "p"), 46: (73, "qq" + "P" * 20 + "p"),
               47: [(73, "qqPPPPP"), (80, "p" * 20)], 48: (73, "qqPPPp"), 49: (74, "qPp"), 50: (74, "pP")}
    canela_la = {y: (74, "qqPPPp") for y in range(51, 59)}
    bota_la = {59: (73, "OuooooOO"), 60: (73, "OuoooooO"), 61: (73, "dOOOOOd")}
    bota_la.update({y: (73, "OuoooOO") for y in range(62, 68)})
    bota_la.update({68: (72, "ouuooooOO"), 69: (71, "ouuoooooOOO"), 70: (70, "ouuooooooOOO"), 71: (69, "O" * 12),
                    72: (69, "d" * 12)})
    coxa_ca = {47: (99, "PPPPPPPPPp"), 48: (79, "q" * 19 + "P" * 10 + "p"), 49: (77, "qqq" + "P" * 29 + "p"),
               50: (76, "pqqq" + "P" * 29 + "p"), 51: (76, "pqqP" + "P" * 28 + "pp"), 52: (76, "pPq" + "P" * 28 + "pp"),
               53: (77, "pPqPP" + "p" * 25), 54: (77, "pPPqPPPp")}
    canela_ca = {55: (78, "qqPPPPPp"), 56: (79, "qqPPPPPp"), 57: (79, "qqPPPPPpp"), 58: (80, "qqPPPPPp"),
                 59: (81, "qqPPPPPp"), 60: (81, "qqPPPPPp"), 61: (82, "qqPPPPPp"), 62: (82, "qqPPPPPp")}
    bota_ca = {63: (81, "OuuoooooOO"), 64: (81, "OuoooooooO"), 65: (82, "dOOOOOOd")}
    bota_ca.update({y: (82, "uoooooOO") for y in range(66, 71)})
    bota_ca.update({71: (81, "ouoooooOO"), 72: (80, "ouuoooooOO"), 73: (79, "ouuooooooOOO"), 74: (78, "O" * 13),
                    75: (78, "d" * 13)})
    # o tronco inclinado para o tabuleiro: a frente (a esquerda) acesa, as costas na sombra
    bordas = {24: (84, 92), 25: (82, 95), 26: (81, 97), 27: (80, 98), 28: (80, 99), 29: (80, 100), 30: (80, 100),
              31: (81, 101), 32: (81, 101), 33: (82, 102), 34: (82, 102), 35: (83, 102), 36: (83, 103), 37: (84, 103),
              38: (84, 103), 39: (85, 103), 40: (85, 104), 41: (86, 104), 42: (86, 104), 43: (87, 104), 44: (89, 104),
              45: (92, 105), 46: (96, 105), 47: (99, 105)}
    tronco = {y: [tom(a, b, "XX", "Y", "yx")] for y, (a, b) in bordas.items()}
    tronco[24] = [(84, "YXXXXYYyy")]
    tronco[25] = [(82, "XXXXXYYYYYYyyx")]
    for y, a in ((35, 83), (36, 83), (37, 84), (38, 84)):              # a sombra do braço estendido no peito
        tronco[y].append((a, "yyyY"))
    for x, y in ((90, 33), (89, 34), (89, 35), (88, 36), (88, 37), (87, 38), (93, 36), (92, 37), (92, 38)):
        tronco[y].append((x, "y"))                                  # as dobras da camisa
    for y in (41, 42):
        tronco[y].append((86, "c" + "C" * 5 + "f" + "C" * 11 + "c"))
    tronco[47].append((99, "xxxxxxx"))                              # a barra da camisa no assento
    tronco[24].append((85, "Ssl"))                                  # a gola aberta
    tronco[25].append((84, "SsS"))
    tronco[26] = tronco[26] + [(85, "S")]
    manga = {26: (95, 99), 27: (96, 100), 28: (97, 101), 29: (97, 101), 30: (98, 102), 31: (98, 102), 32: (98, 103),
             33: (98, 103), 34: (99, 103), 35: (99, 103)}
    braco_tras = {y: tom(a, b, "xY", "y", "x") for y, (a, b) in manga.items()}
    braco_tras.update({36: (99, "xyYYyx"), 37: (99, "xyyyyx"), 38: (99, "xxxxx")})
    mao_coxa = {38: (98, "lssS"), 39: (96, "lsssS"), 40: (95, "llsssS"), 41: (94, "lsssssS"), 42: (93, "llsssS"),
                43: (90, "SllssssS"), 44: (89, "SsSsSsSS"), 45: (89, "SsSsSS"), 46: (90, "SS")}
    cabeca = {
        10: (81, "kkkkkk"),
        11: (79, "kkKKKKKKk"),
        12: (77, "kKKKHHHKKKKk"),
        13: (76, "kKKHHHHHKKKKk"),
        14: (75, "kKKKHHHHKKKKKk"),
        15: (74, "kKKKKKHHKKKKKKk"),
        16: (74, "KKKsKKKKKKKKKKKk"),
        17: (74, "lSSsSKKKKKKKKKKk"),
        18: (74, "lseesSKKKKKKKKKk"),
        19: (73, "llssssSsKKKKKKKKk"),
        20: (73, "SssssssSKKKKKKKk"),
        21: (74, "SssssssKKKKKKKk"),
        22: (75, "SsssssSKKKKKKk"),
        23: (76, "sssssSSKKKKKk"),
        24: (77, "SSSSSSSKKKk"),
        25: [(80, "SSSS"), (84, "kk")],
    }
    sup = {28: (80, 85), 29: (77, 85), 30: (74, 85), 31: (72, 84), 32: (71, 83), 33: (70, 80), 34: (71, 77)}
    braco = {y: faixa(a, b, "W", "X", "Y", 1, 2) for y, (a, b) in sup.items()}
    braco[33] = faixa(70, 80, "X", "Y", "y")
    braco[34] = faixa(71, 77, "y", "y", "x")
    punho_manga = {31: (70, "WXX"), 32: (69, "WXXY"), 33: (69, "XYYy"), 34: (70, "yy")}
    ante = {32: faixa(66, 68, "l", "s", "s"), 33: faixa(64, 68, "l", "s", "S"), 34: faixa(63, 69, "l", "s", "S"),
            35: faixa(62, 66, "l", "s", "S")}
    mao = {36: (61, "lssS"), 37: [(61, "rsSr")], 38: (61, "RRR")}
    return dict(coxa_la=coxa_la, canela_la=canela_la, bota_la=bota_la, coxa_ca=coxa_ca, canela_ca=canela_ca,
                bota_ca=bota_ca, tronco=tronco, braco_tras=braco_tras, mao_coxa=mao_coxa, cabeca=cabeca, braco=braco,
                punho_manga=punho_manga, ante=ante, mao=mao)


VERDE, OCRE = partes(*verde_partes().values()), partes(*ocre_partes().values())


# ---------------------------------------------------------------- os móveis
def banquinho(px, X0, X1, Z0, Z1, H=ALTURA_BANCO):
    """O banquinho de quatro pés da prova, mais estreito e mais alto (o da referência)."""
    C.sombra(px, S, (X0 + X1) / 2, (Z0 + Z1) / 2, 0.24, 0.22)
    for X, Z, cor in ((X0 + 0.03, Z0 + 0.04, "movelEsc"), (X1 - 0.07, Z0 + 0.04, "movelEsc"),
                      (X0 + 0.03, Z1 - 0.04, "movel"), (X1 - 0.07, Z1 - 0.04, "movel")):
        (x, yt), (_, yp) = C.Pl(X, Z, H - 0.06, S), C.Pl(X, Z, 0, S)
        px(round(x), round(yt), 2, round(yp - yt), cor)
        if cor == "movel":
            px(round(x), round(yt), 1, round(yp - yt), "movelLuz")
    (xa, y), (xb, _) = C.Pl(X0 + 0.03, Z1 - 0.04, 0.17, S), C.Pl(X1 - 0.03, Z1 - 0.04, 0.17, S)
    px(round(xa), round(y), round(xb - xa), 2, "movelEsc")             # a travessa da frente
    C.caixa(px, S, X0, X1, Z0, Z1, H - 0.07, H, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz")


def mesa(px):
    """A mesa redonda de um pé (a da F): a base em cruz, o pé torneado, o tampo com 3 px de espessura, o tabuleiro e
    o castiçal (a chama vem da camada velas da sala)."""
    X, Z, raio, Hm = C.MESA
    C.sombra(px, S, X, Z, 0.42, 0.3)
    for dx, dz in ((-0.32, 0), (0.32, 0), (0, -0.25), (0, 0.25)):
        (xa, ya), (xb, yb) = C.Pl(X, Z, 0.04, S), C.Pl(X + dx, Z + dz, 0.04, S)
        px.linha(xa, ya, xb, yb, "movelEsc")
        px.linha(xa, ya - 1, xb, yb - 1, "movel")
        px.linha(xa, ya - 2, xb, yb - 2, "movel")
    (x, yt), (_, yp) = C.Pl(X, Z, Hm - 0.07, S), C.Pl(X, Z, 0.04, S)
    x, w = round(x), 4
    px(x - 2, round(yt), w, round(yp - yt), "movel")
    px(x - 2, round(yt), 1, round(yp - yt), "movelLuz")
    px(x + 1, round(yt), 1, round(yp - yt), "movelEsc")
    ym = round(yt) + 4                                                 # o anel torneado
    px(x - 3, ym, w + 2, 2, "movelEsc")
    px(x - 3, ym, w + 2, 1, "movel")
    borda = [C.Pl(X + raio * math.cos(2 * math.pi * i / 48), Z + raio * math.sin(2 * math.pi * i / 48), Hm - 0.07, S)
             for i in range(48)]
    topo = [C.Pl(X + raio * math.cos(2 * math.pi * i / 48), Z + raio * math.sin(2 * math.pi * i / 48), Hm, S)
            for i in range(48)]
    px.poligono(borda, "movel")
    px.poligono(topo, "movelTopo")
    for i in range(48):                                                # a aresta da frente, clara
        a = 2 * math.pi * i / 48
        if math.sin(a) > 0.1:
            x0, y0 = C.Pl(X + raio * math.cos(a), Z + raio * math.sin(a), Hm, S)
            px(round(x0), round(y0) - 1, 1, 1, "movelLuz")
    # o tabuleiro, à mão: 4 colunas e 2 fileiras de casas grandes, a moldura e a espessura; as peças em disco
    tab = {37: (51, "c" * 17), 38: (51, "cLLLLDDDDLLLLDDDDc"), 39: (52, "cLLLLDDDDLLLLDDDDc"),
           40: (52, "cDDDDLLLLDDDDLLLLc"), 41: (53, "cDDDDLLLLDDDDLLLLc"), 42: (53, "a" * 18), 43: (54, "c" * 18)}
    cores = {"c": "vigaEsc", "a": "movelLuz", "L": "linho", "D": "movelEsc"}
    for y, (x0, txt) in tab.items():
        for i, ch in enumerate(txt):
            px.p(x0 + i, y, cores[ch])
    # as peças: uma clara atrás, uma escura na frente; a de barro fica na mão do de ocre (desenhada com ele)
    pecas = {36: [(54, "121")], 37: [(54, "222")], 39: [(66, "343")], 40: [(66, "444")]}
    cp = {"1": "linhoLuz", "2": "linhoSombra", "3": "movelLuz", "4": "contato"}
    for y, trs in pecas.items():
        for x0, txt in trs:
            for i, ch in enumerate(txt):
                px.p(x0 + i, y, cp[ch])
    x0, y0 = C.Pl(X + 0.05, Z - 0.3, Hm, S)                            # o castiçal
    x0, y0 = round(x0), round(y0)
    px(x0 - 2, y0 - 2, 8, 2, "barro")
    px(x0 - 2, y0 - 2, 8, 1, "barroLuz")
    px(x0, y0 - 10, 4, 8, "cera")
    px(x0 + 2, y0 - 10, 2, 8, "ceraEsc")


# ---------------------------------------------------------------- as camadas
def camadas():
    """{nome: Tela 132×84}: as camadas da fonte, de baixo para cima, já com a luz da sala."""
    r = {}
    t = D.Tela(W, H)
    px = C.Pincel(t)
    banquinho(px, *BANCO_ESQ)
    banquinho(px, *BANCO_DIR)
    r["bancos"] = t
    t = D.Tela(W, H)
    mesa(C.Pincel(t))
    r["mesa"] = t
    for nome, linhas, pal in (("verde", VERDE, PAL_VERDE), ("ocre", OCRE, PAL_OCRE)):
        t = D.Tela(W, H)
        C.Pincel(t).trechos(linhas, pal)
        r[nome] = t
    for t in r.values():
        C.luz(t, S)
    return r


def composto(cs=None):
    t = D.Tela(W, H)
    for c in (cs or camadas()).values():
        t.sobre(c)
    return t

