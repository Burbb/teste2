"""A prova de qualidade da taverna: os dois jogadores, a mesa redonda e os banquinhos da candidata F, em duas grades
nativas, na mesma área da tela (o recorte R da sala de 320×96: de x 174 a 240, de y 42 a 84).

- **A**: a grade atual, 1 pixel do conjunto = 1 pixel da sala (66×42);
- **B**: o dobro em cada eixo, 2×2 pixels do conjunto por pixel da sala (132×84), mostrados no mesmo tamanho.

As duas usam a mesma câmera e a mesma composição (a projeção da F, `f.desenho.P`, com as mesmas posições da mesa, dos
banquinhos e das pessoas), as mesmas poses, a mesma paleta e a mesma luz (a da sala, calculada no ponto da sala de cada
pixel). Os móveis saem da projeção nas duas escalas; as pessoas são desenhadas à mão em cada grade (nenhuma é a outra
ampliada ou reduzida), em listas de trechos por linha (`(x, "pixels")`), no espaço local de cada grade.

    python ferramentas/prototipos/taverna/prova/conjunto.py      (exporta para camadas/prova/)

Saem: `a.png` e `b.png` (o conjunto, fundo transparente, já com a luz), `chao-a.png` e `chao-b.png` (o trecho de piso
para a vista isolada) e a sala da F sem o conjunto (`fundo.png`, `fundo-sem-morel.png`), para o entorno provisório."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

from f import desenho as D, gente as G  # noqa: E402

R = (174, 42, 66, 42)                    # o recorte na sala: x, y, largura, altura
CAMADAS = os.path.join(os.path.dirname(AQUI), "camadas", "prova")


def Pl(X, Z, H, s):
    """A projeção da F no espaço local do recorte, na escala s (1 = A, 2 = B)."""
    x, y = D.P(X, Z, H)
    return ((x - R[0]) * s, (y - R[1]) * s)


class Pincel(D.Pincel):
    """O pincel da F, num quadro do tamanho do recorte."""

    def poligono(self, pts, cor):
        ys = [p[1] for p in pts]
        for y in range(max(0, math.floor(min(ys))), min(self.t.h, math.ceil(max(ys)) + 1)):
            cy = y + 0.5
            cortes = []
            for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
                if (y0 <= cy < y1) or (y1 <= cy < y0):
                    cortes.append(x0 + (cy - y0) * (x1 - x0) / (y1 - y0))
            cortes.sort()
            for a, b in zip(cortes[::2], cortes[1::2]):
                xa, xb = math.ceil(a - 0.5), math.floor(b - 0.5)
                if xb >= xa:
                    self(xa, y, xb - xa + 1, 1, cor)

    def trechos(self, linhas, pal):
        """As pessoas: para cada linha y, os trechos (x, "pixels"); '.' é transparente."""
        for y, trechos in linhas.items():
            for x0, txt in trechos:
                for i, ch in enumerate(txt):
                    if ch in pal:
                        self.p(x0 + i, y, pal[ch])


def caixa(px, s, X0, X1, Z0, Z1, H0, H1, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz"):
    if X1 < 0 and lado:
        px.poligono([Pl(X1, Z0, H0, s), Pl(X1, Z1, H0, s), Pl(X1, Z1, H1, s), Pl(X1, Z0, H1, s)], lado)
    if X0 > 0 and lado:
        px.poligono([Pl(X0, Z0, H0, s), Pl(X0, Z1, H0, s), Pl(X0, Z1, H1, s), Pl(X0, Z0, H1, s)], lado)
    if frente:
        px.poligono([Pl(X0, Z1, H0, s), Pl(X1, Z1, H0, s), Pl(X1, Z1, H1, s), Pl(X0, Z1, H1, s)], frente)
    if topo:
        px.poligono([Pl(X0, Z0, H1, s), Pl(X1, Z0, H1, s), Pl(X1, Z1, H1, s), Pl(X0, Z1, H1, s)], topo)
    if aresta:
        (xa, ya), (xb, _) = Pl(X0, Z1, H1, s), Pl(X1, Z1, H1, s)
        px(round(xa), round(ya), round(xb) - round(xa), s, aresta)


# ---------------------------------------------------------------- os móveis (a mesma geometria nas duas grades)
MESA = (2.0, 3.3, 0.45, 0.75)             # o centro, o raio, a altura do tampo
BANCO_ESQ = (1.05, 1.45, 3.1, 3.5)        # os banquinhos (os da F)
BANCO_DIR = (2.55, 2.95, 3.1, 3.5)


def sombra(px, s, X, Z, rx, rz):
    """A sombra de contato no piso: uma elipse escura e baixa embaixo do móvel ou dos pés."""
    pts = [Pl(X + rx * math.cos(2 * math.pi * i / 20), Z + rz * math.sin(2 * math.pi * i / 20), 0, s) for i in range(20)]
    px.poligono(pts, "contato")


def banquinho(px, s, X0, X1, Z0, Z1, H=0.45):
    """Um banquinho de quatro pés: as pernas (as de trás mais escuras), as travessas, o assento grosso (a face de cima,
    a borda clara)."""
    sombra(px, s, (X0 + X1) / 2, (Z0 + Z1) / 2, 0.28, 0.24)
    for X, Z, cor in ((X0 + 0.04, Z0 + 0.05, "movelEsc"), (X1 - 0.08, Z0 + 0.05, "movelEsc"),
                      (X0 + 0.04, Z1 - 0.05, "movel"), (X1 - 0.08, Z1 - 0.05, "movel")):
        (x, yt), (_, yp) = Pl(X, Z, H - 0.05, s), Pl(X, Z, 0, s)
        px(round(x), round(yt), max(1, round(0.05 * D.m(Z) * s)), round(yp - yt), cor)
        if cor == "movel" and s > 1:
            px(round(x), round(yt), 1, round(yp - yt), "movelLuz")
    (xa, y), (xb, _) = Pl(X0 + 0.04, Z1 - 0.05, 0.16, s), Pl(X1 - 0.04, Z1 - 0.05, 0.16, s)
    px(round(xa), round(y), round(xb - xa), s, "movelEsc")             # a travessa da frente
    caixa(px, s, X0, X1, Z0, Z1, H - 0.06, H, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz")


def mesa(px, s):
    """A mesa redonda de um pé: a base em cruz no piso, o pé torneado, o tampo grosso (a borda) e a face de cima (a
    elipse), com o tabuleiro, as peças, as duas canecas e o castiçal."""
    X, Z, raio, H = MESA
    sombra(px, s, X, Z, 0.42, 0.3)
    for dx, dz in ((-0.32, 0), (0.32, 0), (0, -0.25), (0, 0.25)):        # a base em cruz
        (xa, ya), (xb, yb) = Pl(X, Z, 0.04, s), Pl(X + dx, Z + dz, 0.04, s)
        px.linha(xa, ya, xb, yb, "movelEsc")
        if s > 1:
            px.linha(xa, ya - 1, xb, yb - 1, "movel")
    (x, yt), (_, yp) = Pl(X, Z, H - 0.06, s), Pl(X, Z, 0.04, s)          # o pé
    w = max(2, round(0.08 * D.m(Z) * s))
    px(round(x) - w // 2, round(yt), w, round(yp - yt), "movel")
    px(round(x) - w // 2, round(yt), 1, round(yp - yt), "movelLuz")
    if s > 1:                                                          # o anel torneado no meio do pé
        ym = round((yt + yp) / 2)
        px(round(x) - w // 2 - 1, ym, w + 2, 2, "movelEsc")
    borda = [Pl(X + raio * math.cos(2 * math.pi * i / 32), Z + raio * math.sin(2 * math.pi * i / 32), H - 0.06, s)
             for i in range(32)]
    topo = [Pl(X + raio * math.cos(2 * math.pi * i / 32), Z + raio * math.sin(2 * math.pi * i / 32), H, s)
            for i in range(32)]
    px.poligono(borda, "movelEsc")
    px.poligono(topo, "movelTopo")
    for i in range(32):                                                # a borda da frente, clara
        a = 2 * math.pi * i / 32
        if math.sin(a) > 0.2:
            x0, y0 = Pl(X + raio * math.cos(a), Z + raio * math.sin(a), H, s)
            px(round(x0), round(y0) - (1 if s > 1 else 0), 1, 1, "movelLuz")
    # o tabuleiro: 0,36 m, oito casas no B, quatro no A; as peças em pé
    lado = 0.18
    cantos = [Pl(X - lado, Z - lado, H, s), Pl(X + lado, Z - lado, H, s), Pl(X + lado, Z + lado, H, s),
              Pl(X - lado, Z + lado, H, s)]
    px.poligono(cantos, "linhoSombra")
    n = 8 if s > 1 else 4
    for i in range(n):
        for j in range(n):
            if (i + j) % 2:
                Xa, Za = X - lado + 2 * lado * i / n, Z - lado + 2 * lado * j / n
                q = [Pl(Xa, Za, H, s), Pl(Xa + 2 * lado / n, Za, H, s), Pl(Xa + 2 * lado / n, Za + 2 * lado / n, H, s),
                     Pl(Xa, Za + 2 * lado / n, H, s)]
                px.poligono(q, "movelEsc")
    for Xp, Zp, cor in ((X - 0.1, Z - 0.1, "linhoLuz"), (X + 0.06, Z - 0.12, "linhoLuz"), (X - 0.12, Z + 0.08, "vigaEsc"),
                        (X + 0.1, Z + 0.06, "vigaEsc")):
        x0, y0 = Pl(Xp, Zp, H, s)
        px(round(x0), round(y0) - 2 * s, s, 2 * s, cor)
        if s > 1:
            px(round(x0) - 1, round(y0) - 1, 3, 1, cor)
    for Xc in (X - 0.33, X + 0.3):                                     # as canecas
        x0, y0 = Pl(Xc, Z - 0.1, H, s)
        px(round(x0), round(y0) - 3 * s, 2 * s, 3 * s, "estanho")
        px(round(x0), round(y0) - 3 * s, s, 3 * s, "estanhoLuz")
        px(round(x0) + 2 * s, round(y0) - 2 * s, s, s, "estanhoEsc")
    x0, y0 = Pl(X + 0.05, Z - 0.3, H, s)                               # o castiçal (a chama vem da camada velas)
    px(round(x0) - s, round(y0) - s, 4 * s, s, "barro")
    px(round(x0), round(y0) - 5 * s, 2 * s, 4 * s, "cera")
    px(round(x0) + s, round(y0) - 5 * s, s, 4 * s, "ceraEsc")


def chao(px, s):
    """O trecho de piso de lajes embaixo do conjunto (para a vista isolada), pela mesma conta do piso da F."""
    pts = [Pl(0.7, 2.6, 0, s), Pl(3.3, 2.6, 0, s), Pl(3.5, 3.9, 0, s), Pl(0.5, 3.9, 0, s)]
    px.poligono(pts, "laje")
    Z = 0.0
    while Z < 4.0:
        if 2.6 <= Z <= 3.9:
            (xa, y), (xb, _) = Pl(0.6, Z, 0, s), Pl(3.4, Z, 0, s)
            px(round(xa), round(y), round(xb - xa), 1, "lajeJunta")
            px(round(xa), round(y) + 1, round(xb - xa), 1, "lajeLuz")
        Z += 0.6


# ---------------------------------------------------------------- os jogadores, à mão
# Os dois de frente para o tabuleiro: o de verde, à esquerda, de perfil, inclinado, o cotovelo no tampo e o punho no
# queixo (pensa a jogada); o de ocre, à direita, de três quartos, estende o braço e pega uma peça. Portes diferentes:
# o de verde mais largo e mais baixo de tronco, o de ocre mais magro e alto. O quadril no banquinho, as coxas para a
# frente debaixo da borda, as canelas até as botas no piso.
PAL_VERDE = {"K": "#3a2a1e", "k": "#24190f", "H": "#4e3a28", "B": "#33241a", "s": "#c99a78", "S": "#9a6e52",
             "l": "#e0b494", "e": "#24170f", "N": "#46643f", "n": "#30463a", "Z": "#74996a", "z": "#26362a",
             "c": "#3a2416", "f": "#8a7040", "P": "#4a4038", "p": "#332c26", "O": "#2a1e16", "o": "#46342a"}
PAL_OCRE = {"K": "#7a5228", "k": "#523416", "H": "#946a38", "B": "#6a4824", "s": "#d0a080", "S": "#a07456",
            "l": "#e6bc9c", "e": "#24170f", "Y": "#a88a4e", "y": "#7a6236", "X": "#c4a464", "x": "#5e4a28",
            "c": "#3a2416", "f": "#8a7040", "P": "#3e3a44", "p": "#2a2830", "O": "#1e1812", "o": "#3a2e26"}

# ---- A (1×): 66×42. O de verde: o quadril em x 13, o assento em y 26; a cabeça de y 7 a 12; o cotovelo no tampo em
# (23, 19); o joelho em (23, 25) debaixo da borda; a bota em y 36. A manga do braço da frente é mais clara que o tronco
# (nessa grade o braço dobrado inteiro cabe em ~5×6 pixels: o valor é o que o separa do corpo); os ombros arredondados.
VERDE_A = {
    7: [(14, "kKKk")],
    8: [(13, "kKHKKs")],
    9: [(13, "kKKKss")],
    10: [(13, "kKSsel")],
    11: [(13, "kKKsss"), (19, "s")],
    12: [(14, "kBBB"), (18, "ll")],
    13: [(15, "Ss"), (18, "ls")],
    14: [(13, "nNNN"), (17, "zZZ")],
    15: [(12, "nNNNNN"), (18, "zZ")],
    16: [(11, "nNNNNNNz"), (19, "ZZ")],
    17: [(11, "nNNNNNNzZ"), (20, "ZZ")],
    18: [(11, "nNNNNNNNnZZZ")],
    19: [(11, "nNNNNNNnzZZZZ")],
    20: [(10, "nNNNNNNN")],
    21: [(10, "nNNNNNNN")],
    22: [(10, "nNNNNNNN")],
    23: [(10, "nNNNNNNz")],
    24: [(10, "ccccfccc")],
    25: [(10, "pPPPPPPPPPPPPp")],
    26: [(10, "pPPPPPPPPPPPPPp")],
    **{y: [(22, "pPP")] for y in range(27, 33)},
    **{y: [(22, "oOO")] for y in range(33, 36)},
    36: [(21, "OOOOo")],
}
# O de ocre: o quadril em x 47, a cabeça de y 7 a 12, o braço estendido até a peça em (32, 18), o joelho em (37, 25).
OCRE_A = {
    7: [(44, "kKKKk")],
    8: [(43, "sKHKKKk")],
    9: [(43, "ssKKKKk")],
    10: [(42, "lesSsKKk")],
    11: [(43, "sssSKKk")],
    12: [(43, "sBBBKk")],
    13: [(45, "sS")],
    14: [(43, "XYYYYy")],
    15: [(41, "XXYYYYYYy")],
    16: [(38, "XXX"), (41, "YYYYYYYy")],
    17: [(35, "XXX"), (41, "YyYYYYYy")],
    18: [(32, "ls"), (34, "X"), (41, "YyYYYYYy")],
    19: [(41, "YyYYYYYy")],
    20: [(41, "YyYYYYYy")],
    21: [(41, "YyYYYYYy")],
    22: [(41, "YyYYYYYy")],
    23: [(41, "YyYYYYYy")],
    24: [(42, "cccfccc")],
    25: [(37, "pPPPPPPPPPPPp")],
    26: [(36, "pPPPPPPPPPPPPp")],
    **{y: [(36, "PPp")] for y in range(27, 33)},
    **{y: [(36, "OOo")] for y in range(33, 36)},
    36: [(34, "oOOOO")],
}


# ---- B (2×): 132×84. As mesmas posições, em dobro, com o que a grade maior permite: a orelha, o olho com a
# sobrancelha, o nariz, a barba pela linha do queixo, o punho fechado, a manga com o punho da camisa, o volume do
# ombro, as dobras do cinto, o joelho redondo, a panturrilha, o cano e a sola das botas.
def _verde_b():
    L = {}
    L.update({
        13: [(29, "kKKKKk")],
        14: [(27, "kKKHHKKKk")],
        15: [(26, "kKKKHHKKKKs")],
        16: [(26, "kKKKKKKKKss")],
        17: [(26, "kKKKKKKKSssl")],
        18: [(26, "kKKKSSKSsssl")],
        19: [(26, "kKKSsSssSel"), (37, "ls")],
        20: [(26, "kKKSSssssss"), (37, "ss")],
        21: [(27, "kKKsssssssS")],
        22: [(27, "kKBBsssssB")],
        23: [(28, "kBBBBssBB")],
        24: [(29, "BBBBBB"), (35, "llls")],
        25: [(30, "BBBB"), (34, "lsssS")],
        26: [(30, "sSs"), (34, "lsssS")],
        27: [(30, "sSs"), (35, "sSSZ")],
        28: [(25, "nNNNNNs"), (35, "ZZNn")],
    })
    # o tronco (as costas arredondadas, inclinado para a mesa), o braço de cima e o antebraço até o queixo
    tronco = {29: (23, 31), 30: (22, 32), 31: (21, 31), 32: (21, 31), 33: (21, 31), 34: (21, 31), 35: (21, 31),
              36: (20, 30), 37: (20, 30), 38: (20, 30), 39: (20, 30), 40: (20, 30)}
    for y in range(41, 47):
        tronco[y] = (19, 30)
    for y, (a, b) in tronco.items():
        linha = "n" + "N" * (b - a - 1) + "Z"
        L.setdefault(y, []).insert(0, (a, linha))
        if y in (33, 38, 43):                                         # as dobras da túnica
            L[y].append((a + 3, "n" * 3))
    braco = {30: (29, 33), 31: (31, 35), 32: (33, 37), 33: (35, 39), 34: (37, 41), 35: (39, 43), 36: (41, 45),
             37: (42, 46), 38: (43, 47)}
    for y, (a, b) in braco.items():
        L.setdefault(y, []).append((a, "z" + "N" * (b - a - 1) + "n"))
    ante = {28: (35, 38), 29: (36, 39), 30: (37, 40), 31: (38, 41), 32: (39, 42), 33: (40, 43), 34: (41, 44),
            35: (42, 45), 36: (43, 46), 37: (44, 47), 38: (44, 48)}
    for y, (a, b) in ante.items():
        L.setdefault(y, []).append((a, "Z" + "N" * (b - a - 1) + "z"))
    L.setdefault(39, []).append((44, "zNNz"))                       # o cotovelo no tampo
    L[47] = [(19, "cccccfccccc"), (30, "c")]
    L[48] = [(19, "ccccccccccc"), (30, "c")]
    L[49] = [(19, "nNNNNNNNNNNNz")]                                 # a barra da túnica no banquinho
    coxa = {50: (20, 44, "P"), 51: (19, 46, "P"), 52: (19, 47, "P"), 53: (19, 47, "P"), 54: (20, 46, "p")}
    for y, (a, b, c) in coxa.items():
        L[y] = [(a, ("P" if c == "P" else "p") * (b - a + 1))]
    L[50] = [(20, "P" * 24 + "p")]
    L[54] = [(20, "p" * 27)]
    for y in range(55, 66):                                         # a canela, com a panturrilha
        a = 43 if 57 <= y <= 62 else 44
        L[y] = [(a, "p" + "P" * (48 - a - 1) + "p")]
    for y in range(66, 72):                                         # o cano da bota
        L[y] = [(43, "oOOOOO")]
    L[72] = [(43, "oOOOOOOOOO")]
    L[73] = [(43, "OOOOOOOOOOO")]
    L[74] = [(43, "kkkkkkkkkkk")]
    return L


def _ocre_b():
    L = {
        13: [(87, "kKKKKk")],
        14: [(85, "kKHHKKKKk")],
        15: [(84, "sKKHHKKKKk")],
        16: [(84, "ssKKKKKKKk")],
        17: [(83, "lssKKKKKKKk")],
        18: [(83, "lSSsSKKKKKk")],
        19: [(82, "lseSSesKKKk")],
        20: [(82, "lsssSsSKKSk")],
        21: [(83, "sssSsSKKSk")],
        22: [(83, "sBsssBKKk")],
        23: [(84, "BBBBBBKk")],
        24: [(85, "BBBBBk")],
        25: [(87, "BBB")],
        26: [(88, "sSs")],
        27: [(88, "sSs")],
        28: [(84, "XYYYYYYYYy")],
    }
    tronco = {29: (82, 97), 30: (81, 98), 31: (81, 98), 32: (82, 98), 33: (82, 98), 34: (82, 98), 35: (82, 98),
              36: (83, 98), 37: (83, 98), 38: (83, 98)}
    for y in range(39, 47):
        tronco[y] = (84, 98)
    for y, (a, b) in tronco.items():
        L.setdefault(y, []).insert(0, (a, "X" + "Y" * (b - a - 1) + "y"))
        if y in (34, 40):                                           # as dobras da camisa e a costura da manga
            L[y].append((a + 9, "yy"))
    for y in range(31, 44):                                         # o braço de lá, junto do corpo
        L.setdefault(y, []).append((95, "yYYy"))
    braco = {31: (80, 85), 32: (78, 83), 33: (76, 81), 34: (74, 79), 35: (72, 77), 36: (70, 75)}
    for y, (a, b) in braco.items():                                 # o braço estendido até a peça
        L.setdefault(y, []).append((a, "X" + "Y" * (b - a - 1) + "y"))
    L.setdefault(36, []).append((68, "ls"))
    L.setdefault(37, []).append((65, "lssS"))                     # a mão pegando a peça
    L.setdefault(38, []).append((66, "sS"))
    L[47] = [(84, "ccccfcccccccccc")]
    L[48] = [(84, "ccccccccccccccc")]
    L[49] = [(83, "XYYYYYYYYYYYYYYy")]
    L[50] = [(76, "P" * 23 + "p")]
    L[51] = [(74, "P" * 25 + "p")]
    L[52] = [(73, "P" * 26 + "p")]
    L[53] = [(73, "P" * 26 + "p")]
    L[54] = [(74, "p" * 25)]
    for y in range(55, 66):
        b = 78 if 57 <= y <= 62 else 77
        L[y] = [(73, "p" + "P" * (b - 73 - 1) + "p")]
    for y in range(66, 72):
        L[y] = [(72, "OOOOOo")]
    L[72] = [(68, "OOOOOOOOOo")]
    L[73] = [(67, "OOOOOOOOOOO")]
    L[74] = [(67, "kkkkkkkkkkk")]
    return L


VERDE_B, OCRE_B = _verde_b(), _ocre_b()


# ---------------------------------------------------------------- a luz da sala, no ponto de cada pixel
def luz(t, s):
    """A mesma luz da F (o escuro longe do fogo e das velas, o calor perto), calculada no ponto da sala que cada pixel
    do conjunto ocupa (x / s, y / s), para A e B terem a mesma luz."""
    tf = D.Tela(D.QW, D.QH)
    r = D.sala(D.Pincel(tf))
    fogo = r["boca"]
    fontes = [(fogo[0], fogo[1] - 6, 40, 1.0)] + [(x, y, 22, 0.6) for x, y in r["chamas"]]
    for j in range(t.h):
        for i in range(t.w):
            x, y = R[0] + (i + 0.5) / s, R[1] + (j + 0.5) / s
            perto = max(f * max(0.0, 1 - math.hypot(x - fx, (y - fy) * 1.2) / (rr * 2)) for fx, fy, rr, f in fontes)
            escuro = max(0.0, 0.46 - perto * 1.05)
            if escuro > 0:
                t.mistura(i, j, (6, 5, 4), escuro)
            calor = max(f * max(0.0, 1 - ((x - fx) ** 2 + ((y - fy) * 1.2) ** 2) / (rr * rr)) * 0.12
                        for fx, fy, rr, f in fontes)
            if calor > 0.004:
                t.mistura(i, j, (255, 160, 80), calor)


def conjunto(s, com_chao=False):
    """O conjunto na escala s: o piso (só na vista isolada), os banquinhos, os jogadores, a mesa por cima das coxas e
    das canelas de trás, as mãos por cima do tampo, e a luz."""
    t = D.Tela(R[2] * s, R[3] * s)
    px = Pincel(t)
    if com_chao:
        chao(px, s)
        luz(t, s)
        return t
    banquinho(px, s, *BANCO_ESQ)
    banquinho(px, s, *BANCO_DIR)
    verde, ocre = (VERDE_A, OCRE_A) if s == 1 else (VERDE_B, OCRE_B)
    px.trechos(verde, PAL_VERDE)
    px.trechos(ocre, PAL_OCRE)
    mesa(px, s)
    # os braços que pousam no tampo vêm por cima dele: o cotovelo do de verde e a mão do de ocre
    if s == 1:
        px.trechos({18: [(20, "nZZZ")], 19: [(19, "nzZZZ")]}, PAL_VERDE)
        px.trechos({17: [(35, "XXX")], 18: [(32, "ls"), (34, "X")]}, PAL_OCRE)
    else:
        px.trechos({y: VERDE_B[y][-1:] for y in range(34, 40)}, PAL_VERDE)
        px.trechos({y: [tr for tr in OCRE_B[y] if tr[0] < 82] for y in range(33, 39)}, PAL_OCRE)
    luz(t, s)
    return t


def exportar():
    os.makedirs(CAMADAS, exist_ok=True)
    for nome, s in (("a", 1), ("b", 2)):
        conjunto(s).imagem().save(os.path.join(CAMADAS, f"{nome}.png"))
        conjunto(s, com_chao=True).imagem().save(os.path.join(CAMADAS, f"chao-{nome}.png"))
    D.SEM_RODA = True                                                 # a sala da F sem o conjunto (o entorno provisório)
    try:
        for nome, morel in (("fundo", True), ("fundo-sem-morel", False)):
            t = D.Tela(D.QW, D.QH)
            px = D.Pincel(t)
            r = D.sala(px)
            G.desenhar(px, r, morel=morel)
            D.luz(t, r["chamas"], r["boca"])
            t.imagem().save(os.path.join(CAMADAS, f"{nome}.png"))
    finally:
        D.SEM_RODA = False


if __name__ == "__main__":
    exportar()
    print("ok")
