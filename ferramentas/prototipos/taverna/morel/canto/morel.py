"""Morel no canto da taverna (protótipo): o tronco, a cabeça, as ombreiras, a espada e os braços, na escala da cena nova.

Na referência "Encontro com Morel na taverna" (na altura das cenas, 240 de largura, mais 40 px de borda), Morel ocupa
o meio do quadro, grande: a cabeça tem uns 27×34 (na vista aprovada do balcão, 21×25). Ele é **desenhado de novo**, por
partes, nesta escala, com as paletas e o jeito da vista aprovada (as fontes de `morel/vista/`): nada da imagem gerada é
reduzido para virar arte; ela dá as posições, as proporções e a distribuição dos materiais.

- **A identidade** (conferida com a vista aprovada e o retrato do jogo): o cabelo castanho curto, a barba castanha
  cheia, a cicatriz em diagonal da testa à bochecha atravessando a sobrancelha, o colete vermelho com as duas tiras e as
  fivelas, as mangas e o casaco de couro, as duas ombreiras diferentes (a do ombro direito em aço claro, com rebites; a
  do esquerdo escura), a espada às costas com o pomo acima do ombro direito.
- **A cabeça** (`CABECA`, numa grade à mão, um caractere por pixel): o mesmo desenho da aprovada levado à escala nova
  (os três tons do cabelo, a pele com o lado da vela claro, a cicatriz num traço claro e rosado, as sobrancelhas, a
  barba em dois tons com a boca num traço). Variantes: `baixo` (os olhos na tigela, as pálpebras), `olha` (os olhos
  abertos, o branco e a pupila), `boca` (a boca aberta para a colher), `mastiga` (o queixo 1 px abaixo).
- **O tronco** (`tronco`): o casaco em blocos de couro, a luz da vela pela esquerda, as lapelas com a borda clara, o
  colete vermelho com a costura no meio e o lado da luz mais claro, as duas tiras de couro com as fivelas de aço, a
  gola. O braço direito sai do tronco: o tronco é desenhado inteiro, também atrás dele (quando a colher vai à boca,
  aparece o que estava atrás).
- **Os braços** pela função da manga aprovada (`morel/vista/manga.py`: uma forma só do ombro ao punho, a curva por
  fora do cotovelo, a dobra curta por dentro, o antebraço escurecendo depois da junta), com os raios desta escala; as
  mãos em bolinha de pele, sem dedos."""
import math
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "vista"))

import manga as MG  # noqa: E402
from espaco import h  # noqa: E402

COURO = {"j": h("8a5a38"), "a": h("6a4a2c"), "b": h("4e3420"), "c": h("33231a"), "l": h("2a1c14"), "w": h("1f150e")}
COLETE = [h("b84c40"), h("a8443a"), h("8a3428"), h("5e241c"), h("3e1610")]
ACO = [h("e0e2e6"), h("c4c6cc"), h("9a9ca4"), h("7a7c84"), h("6e7078"), h("4a4c54")]
PLACA = [h("8a8078"), h("6a6058"), h("4e4640"), h("34302c"), h("221e1b")]
PELE = {"e": h("d8aa90"), "d": h("c09070"), "f": h("9a6c52"), "h": h("6c4a38"), "g": h("9a6656"), "x": h("b07a60")}
PELO = {"a": h("6a4a30"), "b": h("4a3220"), "c": h("33231a"), "n": h("7a5a3a")}
BARBA = {"l": h("3e2a1c"), "m": h("5a3e2a"), "i": h("2a1c14"), "o": h("20160f"), "n": h("6a4a30")}
OLHO = {"j": h("20160f"), "w": h("d8c8b8"), "k": h("20160f"), "q": h("2a1c14")}
MADEIRA_ESPADA = [h("7a5034"), h("5a3a22"), h("3a2414"), h("24160c")]

# ------------------------------------------------------------------ a cabeça
CABECA_POS = (157, 2)   # o canto de cima à esquerda da grade (a cabeça vai de x 157 a 184)
# a, b, c: o cabelo (claro, médio, sombra); d pele, e luz, x meio-tom quente, f sombra, h sombra funda, g a cicatriz
# rosada; i a sobrancelha; j a pálpebra baixa; w o branco do olho, k a pupila; l, m, n a barba (sombra, meio, luz);
# o a boca; "." vazio
CABECA = [
    "...........aaabbbb..........",
    "........aaaaaabbbbbbb.......",
    "......baaaaabbbbbbbbbbc.....",
    ".....baaabbbbbbbbbbbbbcc....",
    "....baabbbbbbbbbbbbbbbbcc...",
    "....babbbbbbbbbbbbbbbbbbcc..",
    "...bbbbbbbbbbbbbbbbbbbbbcc..",
    "...bbbbbbbbbbbbbbbbbbbbbbcc.",
    "...bbbdeeddddddddddddfbbbcc.",
    "...bbdeegdddddddddddddffbcc.",
    "...bbdddegddddddddddddddfcc.",
    "...bddddddgdddddddddddddffhc",
    "..bddiiiiiigiddddiiiiiifffhc",
    "..hdddddddddgddddddddddfffh.",
    ".fhddjjjjddddgddddjjjjjfffhh",
    ".fddddddddddddgdddddddddffhh",
    ".fdddddddddddhfgdddddddffhhc",
    "..dddddddddhhffhgddddddfffh.",
    "..ddddddddhffffhhgdddddffhh.",
    "..llddddddddhhhhhddgdddfflli",
    "..lllddddddddddddddddddfllli",
    "..llllnnmmmmmmmmmmmmnnfllli.",
    "..lllllmmmmmmmmmmmmmmmllllii",
    "..llllmmmmooooooommmmmmllli.",
    "..llllmmmmmmmmmmmmmmmmmllli.",
    "...llllnmmmmmmmmmmmmmmllli..",
    "...lllllnmmmmmmmmmmmmlllii..",
    "....lllllmmmmmmmmmmmllllii..",
    "....llllllmmmmmmmmmllllii...",
    ".....lllllllmmmmmlllllii....",
    "......lllllllllllllllii.....",
    ".......llllllllllllii.......",
    ".........lllllllllii........",
    "...........iiiiiii..........",
]


def cabeca(variante="baixo", dy=0):
    """A cabeça em {(x, y): cor}: `baixo` (os olhos na tigela), `olha` (para quem está à mesa: os olhos abertos),
    `boca` (aberta para a colher), `mastiga` (o queixo 1 px abaixo)."""
    linhas = [list(r) for r in CABECA]
    if variante == "olha":
        # os olhos abertos: a sobrancelha 1 px acima, o branco e a pupila (olhando para a frente, um pouco para baixo)
        linhas[14] = list(".fhddqwkwddddgddddqwkwqfffhh")
    elif variante == "boca":
        linhas[23] = list("..llllmmmmoooooooommmmmllli.")
        linhas[24] = list("..llllmmmmmoooooommmmmmllli.")
    # o lado da sombra (longe da vela): a pele da metade da direita desce um degrau, e mais junto da orelha
    for y in range(8, 21):
        for x, ch in enumerate(linhas[y]):
            if ch == "d" and x >= 22:
                linhas[y][x] = "h" if x >= 24 else "f"
            elif ch == "d" and x >= 19 and y >= 13:
                linhas[y][x] = "f"
    out = {}
    x0, y0 = CABECA_POS
    for y, linha in enumerate(linhas):
        for x, ch in enumerate(linha):
            cor = PELO.get(ch) if ch in "abc" else PELE.get(ch) if ch in "edxfhg" else \
                BARBA.get(ch) if ch in "lmnio" else OLHO.get(ch) if ch in "jwkq" else None
            if cor is None:
                continue
            yy = y0 + y + dy
            if variante == "mastiga" and y >= 23:
                yy += 1  # o queixo e a barba de baixo descem 1 px
            out[(x0 + x, yy)] = cor
    if variante == "mastiga":  # o vão que o queixo deixou embaixo da boca, na barba
        for x in range(x0 + 6, x0 + 22):
            out.setdefault((x, y0 + 23 + dy), BARBA["m"])
    return out


# ------------------------------------------------------------------ o tronco
def _poligono(pts):
    """Os pixels dentro de um polígono (regra par-ímpar, pelo centro do pixel)."""
    ys = [p[1] for p in pts]
    out = set()
    for y in range(math.floor(min(ys)), math.ceil(max(ys)) + 1):
        cy = y + 0.5
        xs = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            if (y1 <= cy < y2) or (y2 <= cy < y1):
                xs.append(x1 + (cy - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            for x in range(math.ceil(a - 0.5), math.floor(b - 0.5) + 1):
                out.add((x, y))
    return out


TRONCO = [(126, 48), (134, 38), (148, 33), (160, 34), (184, 34), (196, 33), (210, 38), (216, 48), (218, 80),
          (126, 80)]
COLETE_X = (158, 184)
TIRAS_Y = (49, 61)


def tronco(dy=0):
    """O tronco em {(x, y): cor}: o casaco, o colete com as tiras e as fivelas, a gola."""
    out = {}
    corpo = _poligono([(x, y + dy) for x, y in TRONCO])
    cx = 171
    for (x, y) in corpo:
        u = (x - cx) / 40       # -1 à esquerda (a vela), +1 à direita
        cor = COURO["a"] if u < -0.45 else COURO["b"] if u < 0.35 else COURO["c"]
        if u < -0.75:
            cor = COURO["j"] if (y - dy) < 58 else COURO["a"]
        out[(x, y)] = cor
    # o colete: a faixa do meio, com a costura e o lado da luz
    for (x, y) in list(corpo):
        if COLETE_X[0] <= x < COLETE_X[1] and y - dy >= 36:
            k = x - COLETE_X[0]
            cor = COLETE[0] if k in (2, 3) else COLETE[1] if k < 11 else COLETE[2] if k < 20 else COLETE[3]
            if k == 12:
                cor = COLETE[3]     # a costura do meio
            if k in (0, 25):
                cor = COLETE[4]     # a borda que entra embaixo da lapela
            out[(x, y)] = cor
    # as lapelas do casaco: a borda clara do lado da vela, a sombra que fazem no colete
    for y in range(36 + dy, 81 + dy):
        for x, cor in ((COLETE_X[0] - 1, COURO["j"]), (COLETE_X[0] - 2, COURO["a"]), (COLETE_X[1], COURO["l"]),
                       (COLETE_X[1] + 1, COURO["b"])):
            if (x, y) in corpo:
                out[(x, y)] = cor
    # as tiras com as fivelas
    for ty in TIRAS_Y:
        for y in range(ty + dy, ty + 3 + dy):
            for x in range(COLETE_X[0] - 1, COLETE_X[1] + 1):
                out[(x, y)] = COURO["c"] if y == ty + dy else COURO["b"] if y == ty + 1 + dy else COURO["l"]
        bx = 167
        for y in range(ty - 1 + dy, ty + 4 + dy):  # a fivela: o aro de aço, o vão escuro no meio
            for x in range(bx, bx + 8):
                k, j = x - bx, y - (ty - 1 + dy)
                aro = k in (0, 7) or j in (0, 4)
                if aro:
                    out[(x, y)] = ACO[1] if (j == 0 or k == 0) else ACO[3]
                else:
                    out[(x, y)] = COURO["l"] if k < 4 else ACO[4]
    # a gola: o couro dobrado em volta do pescoço, embaixo da barba
    for x in range(152, 192):
        for y in range(34 + dy, 38 + dy):
            if (x, y) in out or abs(x - 171) < 21:
                out[(x, y)] = COURO["a"] if x < 165 else COURO["b"] if x < 180 else COURO["c"]
    return out


# ------------------------------------------------------------------ as ombreiras e a espada
# as ombreiras: cascos medidos na referência (no ombro de repouso), como polígonos; a crista de cima acesa do lado
# da vela, o corpo, a faixa de baixo um tom abaixo, a borda escura e a fileira de rebites
OMBREIRA_DIR = [(117, 44), (119, 40), (125, 35), (133, 30), (141, 27), (147, 28), (149, 34), (148, 45), (133, 47),
                (118, 46)]
OMBREIRA_ESQ = [(190, 40), (192, 33), (198, 29), (207, 28), (213, 30), (218, 37), (220, 48), (211, 50), (197, 48)]
OMBRO_REPOUSO = (138, 44)  # a junta do ombro direito na pose de repouso (a ombreira acompanha a junta)


def _casco(pts, tons, rebites_y, dx=0, dy=0):
    """Uma ombreira: o polígono com a crista de cima (os 2 px mais altos de cada coluna) acesa, o corpo, a faixa de
    baixo, a borda de baixo escura; os rebites numa fileira."""
    area = _poligono([(x + dx, y + dy) for x, y in pts])
    out = {}
    cols = {}
    for x, y in area:
        cols.setdefault(x, []).append(y)
    xs = sorted(cols)
    for x in xs:
        ys = sorted(cols[x])
        topo, fundo = ys[0], ys[-1]
        for y in ys:
            k = y - topo
            u = (x - xs[0]) / max(1, xs[-1] - xs[0])
            if k <= 1:
                cor = tons[0] if u < 0.6 else tons[1]
            elif y >= fundo:
                cor = tons[4]
            elif y >= fundo - 2:
                cor = tons[3]
            else:
                cor = tons[1] if u < 0.35 else tons[2]
            out[(x, y)] = cor
    for x in range(xs[0] + 4, xs[-1] - 2, 5):
        y = rebites_y + dy
        if (x, y) in out:
            out[(x, y)] = tons[4]
            if (x - 1, y - 1) in out:
                out[(x - 1, y - 1)] = tons[0]
    return out


def ombreira_direita(S):
    """A ombreira de aço claro: acompanha a junta do ombro direito (`S` na tela)."""
    dx, dy = round(S[0] - OMBRO_REPOUSO[0]), round(S[1] - OMBRO_REPOUSO[1])
    return _casco(OMBREIRA_DIR, (ACO[0], ACO[1], ACO[2], ACO[3], ACO[5]), 40, dx, dy)


def ombreira_esquerda(dy=0, dx=0):
    return _casco(OMBREIRA_ESQ, (PLACA[0], PLACA[1], PLACA[2], PLACA[3], PLACA[4]), 42, dx, dy)


def espada(dy=0):
    """A espada às costas, saindo acima do ombro direito: o pomo redondo de aço e o cabo enrolado em couro, inclinado."""
    out = {}
    for y in range(10, 31):  # o cabo
        x = 137 + (y - 10) * 0.32
        for k in range(3):
            cor = MADEIRA_ESPADA[0] if k == 0 else MADEIRA_ESPADA[1] if k == 1 else MADEIRA_ESPADA[3]
            if (y - 10) % 4 == 3:
                cor = MADEIRA_ESPADA[2]  # o enrolado
            out[(round(x) + k - 1, y + dy)] = cor
    for (x, y) in [(134 + i, 4 + j) for j in range(6) for i in range(6)]:  # o pomo
        u, v = (x - 136.5) / 3, (y - 6.5) / 3
        if u * u + v * v <= 1:
            out[(x, y + dy)] = ACO[0] if u + v < -0.6 else ACO[2] if u + v < 0.6 else ACO[4]
    return out


# ------------------------------------------------------------------ os braços
R_MOREL = {"ombro": 9.5, "cotovelo": 8.4, "cotoveloPerto": 8.8, "antebraco": 7.8, "punho": 6.0}
PELE_MAO = (h("c89878"), h("a87250"), h("7a5440"))


def braco(S, E, W, corpo, extra=None):
    """Um braço vestido pela manga aprovada (os raios desta escala) em {(x, y): cor}, e os pixels do antebraço."""
    r0 = dict(MG.R4)
    MG.R4.update(R_MOREL)
    try:
        m = MG.manga(S, E, W, lambda x, y: (x, y) in corpo)
    finally:
        MG.R4.clear()
        MG.R4.update(r0)
    return m, set(MG.manga.antebraco)


COLHER = [h("b08050"), h("8a5e38"), h("5e3e22")]


def colher(W, T):
    """A colher de madeira, rígida: o cabo do punho (`W`) à ponta (`T`), dois pixels de grosso (a aresta de cima
    acesa), e a concha na ponta, uma elipse pequena com a borda de baixo escura."""
    out = {}
    n = int(max(abs(T[0] - W[0]), abs(T[1] - W[1]))) + 1
    for i in range(n + 1):
        t = i / n
        x, y = W[0] + (T[0] - W[0]) * t, W[1] + (T[1] - W[1]) * t
        out[(math.floor(x), math.floor(y))] = COLHER[0]
        out[(math.floor(x), math.floor(y) + 1)] = COLHER[1]
    for y in range(math.floor(T[1] - 1.5), math.ceil(T[1] + 1.5) + 1):
        for x in range(math.floor(T[0] - 2.5), math.ceil(T[0] + 2.5) + 1):
            u, v = (x + 0.5 - T[0]) / 2.6, (y + 0.5 - T[1]) / 1.6
            if u * u + v * v <= 1:
                out[(x, y)] = COLHER[0] if v < -0.2 else COLHER[1] if v < 0.5 else COLHER[2]
    return out


def mao(c, rx=5.0, ry=4.2):
    """A mão em bolinha de pele: a luz em cima à esquerda (a vela), a sombra embaixo à direita."""
    out = {}
    for y in range(math.floor(c[1] - ry), math.ceil(c[1] + ry) + 1):
        for x in range(math.floor(c[0] - rx), math.ceil(c[0] + rx) + 1):
            u, v = (x + 0.5 - c[0]) / rx, (y + 0.5 - c[1]) / ry
            if u * u + v * v <= 1:
                s = -u * 0.7 - v * 0.7
                out[(x, y)] = PELE_MAO[0] if s > 0.3 else PELE_MAO[1] if s > -0.5 else PELE_MAO[2]
    return out
