"""PROTÓTIPO do redesenho do d20 (etapa 2, 24/10/2026; nada no jogo). Constrói o dado das duas propostas em pixel art e
grava `d20-dados.js` (as grades de texto, um caractere por pixel, como sprites-dados.js) e as pranchas de conferência.

A construção (dita no LEIA-ME, separada do retoque):
- a geometria é a do icosaedro de verdade (os 12 vértices, as 20 faces), visto de frente para uma face, um pouco de
  cima e da esquerda; no repouso, os três vértices da face da frente se abrem um pouco (FRENTE) para o número de dois
  dígitos caber, sem mudar a ligação das faces (o mesmo dado; a tirinha usa a mesma conta);
- o tom de cada face do repouso é escolhido à mão (TONS_*), pela luz comum (de cima e da esquerda, um pouco de frente);
  nos quadros do giro, o tom sai da luz em faixas (é movimento: some em 60 ms);
- as arestas: um pixel por aresta, na face mais escura das duas (a sombra da quina) ou mais clara (o fio de luz),
  conforme a quina vira para a luz; o contorno de 1 pixel por fora;
- os retoques pixel a pixel vão em AJUSTES, com o porquê.

    python ferramentas/prototipos/hud/d20/desenhar_d20.py          # grava d20-dados.js e pranchas/
"""
import itertools
import json
import math
import pathlib

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
LUZ = np.array([-0.58, -0.62, 0.53]); LUZ = LUZ / np.linalg.norm(LUZ)  # a de ferramentas/arte/pixel_comum.py
FI = (1 + 5 ** 0.5) / 2
VERT = np.array([(0, 1, FI), (0, -1, FI), (0, 1, -FI), (0, -1, -FI), (1, FI, 0), (-1, FI, 0), (1, -FI, 0),
                 (-1, -FI, 0), (FI, 0, 1), (-FI, 0, 1), (FI, 0, -1), (-FI, 0, -1)], float)
FACES = [f for f in itertools.combinations(range(12), 3)
         if all(abs(np.linalg.norm(VERT[a] - VERT[b]) - 2) < 1e-6 for a, b in itertools.combinations(f, 2))]


def rot(eixo, ang):
    eixo = np.asarray(eixo, float); eixo = eixo / np.linalg.norm(eixo)
    x, y, z = eixo; c, s = math.cos(ang), math.sin(ang); C = 1 - c
    return np.array([[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
                     [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
                     [z * x * C - y * s, z * y * C + x * s, c + z * z * C]])


def de_frente():
    """A rotação que põe a face 0 de frente (o normal em +z, a tela tem y para baixo) com um vértice para cima."""
    f = FACES[0]
    n = VERT[list(f)].mean(0); n = n / np.linalg.norm(n)
    # leva n a +z
    eixo = np.cross(n, [0, 0, 1]); ang = math.acos(np.clip(n @ [0, 0, 1], -1, 1))
    R = rot(eixo, ang) if np.linalg.norm(eixo) > 1e-9 else np.eye(3)
    v = (R @ VERT[f[0]].T)
    # gira em torno de z até o vértice f[0] ficar em cima (y negativo na tela)
    a = math.atan2(v[1], v[0]); R = rot([0, 0, 1], -math.pi / 2 - a) @ R
    return R


BASE = de_frente()
FRENTE_FACE = FACES[0]
# o repouso: um pouco de cima (a face de cima aparece mais) e da esquerda
REPOUSO = rot([0, 1, 0], math.radians(-5)) @ rot([1, 0, 0], math.radians(-6)) @ BASE


def projetar(R, N, raio, frente=1.0):
    """Os vértices na grade N×N (centro no meio), com o raio da silhueta em pixels. `frente` abre os três vértices da
    face da frente (só no repouso)."""
    P = (R @ VERT.T).T
    xy = P[:, :2].copy()
    if frente != 1.0:
        for i in FRENTE_FACE:
            xy[i] *= frente
    esc = raio / np.max(np.linalg.norm(P[:, :2], axis=1))
    c = (N - 1) / 2
    return P, xy * esc + c


def rasterizar(R, N, raio, frente=1.0):
    """Para cada pixel: a face visível (−1 fora), o normal de cada face e os vértices projetados."""
    P, xy = projetar(R, N, raio, frente)
    ident = -np.ones((N, N), int)
    normais = []
    for k, f in enumerate(FACES):
        n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); n = n / np.linalg.norm(n)
        if n @ P[list(f)].mean(0) < 0:
            n = -n
        normais.append(n)
    vis = [k for k in range(20) if normais[k][2] > 1e-6]
    ys, xs = np.mgrid[0:N, 0:N]
    for k in vis:
        a, b, c = (xy[i] for i in FACES[k])
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        l1 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / d
        l2 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / d
        l3 = 1 - l1 - l2
        dentro = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9)
        ident[dentro & (ident < 0)] = k
    return ident, normais, vis, xy, P


def arestas_ocultas(R, N, raio, frente=1.0):
    """As arestas de trás (as que o vidro deixa ver), em pixels (Bresenham)."""
    P, xy = projetar(R, N, raio, frente)
    normais = []
    for f in FACES:
        n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); n = n / np.linalg.norm(n)
        if n @ P[list(f)].mean(0) < 0:
            n = -n
        normais.append(n)
    tras = {frozenset(e) for k, f in enumerate(FACES) if normais[k][2] < -1e-6 for e in itertools.combinations(f, 2)}
    frente_ = {frozenset(e) for k, f in enumerate(FACES) if normais[k][2] > 1e-6 for e in itertools.combinations(f, 2)}
    pix = set()
    for e in tras - frente_:
        a, b = (xy[i] for i in e)
        x0, y0, x1, y1 = round(a[0]), round(a[1]), round(b[0]), round(b[1])
        dx, dy = abs(x1 - x0), -abs(y1 - y0); sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1; err = dx + dy
        while True:
            pix.add((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy
    return pix


# ------------------------------------------------------------------ os materiais
# Cada material: a rampa das faces (do claro ao escuro), o fio de luz das quinas, a sombra das quinas e o contorno.
MATERIAIS = {
    # A: osso polido, marfim quente (o marfim das faixas de Sucesso e das escolhas marcadas)
    "marfim": {"rampa": ["#fff8e6", "#f1e4c4", "#e0cfa4", "#c8b283", "#a88f63", "#806a48", "#5a4a34"],
               "luz": "#fffdf4", "sombra": "#4a3c2a", "contorno": "#0d0b0a"},
    # B: vidro fumê (um carvão violeta translúcido), com as quinas de trás à vista e o brilho nas de cima
    # (o violeta do arcano das celebrações, escurecido; a luz que atravessa no violeta da paleta, "m")
    "vidro": {"rampa": ["#7d6cae", "#5f5190", "#463c72", "#342b58", "#261f44", "#1a1530", "#110d20"],
              "luz": "#e4dcff", "sombra": "#0a0812", "contorno": "#050409", "atravessa": "#8e6fd8", "brilho": "#ffffff"},
}
LETRAS = "1234567"  # os tons da rampa nas grades; "L" o fio de luz, "S" a sombra da quina, "k" o contorno, "o" a quina
# de trás (vidro), "." transparente


def tom_luz(n, nt=7, minimo=-0.15, maximo=0.95):
    v = (n @ LUZ - minimo) / (maximo - minimo)
    return int(np.clip(round((1 - v) * (nt - 1)), 0, nt - 1))


def quadro(R, N, raio, frente=1.0, tons=None, vidro=False, arestas=None):
    """Uma grade (lista de strings) do dado na orientação R. `tons`: {face: índice} escolhidos à mão (o repouso);
    `arestas`: {(face, face): "L" ou "S"} as quinas desenhadas à mão (o repouso; as outras ficam só na troca de tom).
    Sem eles (o giro), o tom sai da luz em faixas e a quina pela direção dela.
    Uma quina "L" (o fio de luz) é um tom mais claro que a face mais clara das duas (a luz, se já é a mais clara); uma
    "S" (a sombra), um tom mais escuro que a mais escura. O traço fica de um lado só (um pixel)."""
    ident, normais, vis, xy, P = rasterizar(R, N, raio, frente)
    t = {k: (tons[k] if tons and k in tons else tom_luz(normais[k])) for k in vis}
    g = [["." for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):
            k = ident[y, x]
            if k >= 0:
                g[y][x] = LETRAS[t[k]]
    if vidro:  # as quinas de trás, vistas através do vidro: um tom mais claro que a face da frente
        for (x, y) in arestas_ocultas(R, N, raio, frente):
            if 0 <= x < N and 0 <= y < N and ident[y, x] >= 0 and t[ident[y, x]] >= 2 and not (tons and ident[y, x] == 0):
                g[y][x] = LETRAS[t[ident[y, x]] - 1]
    for y in range(N):
        for x in range(N):
            k = ident[y, x]
            if k < 0:
                continue
            for dx, dy in ((1, 0), (0, 1)):
                xx, yy = x + dx, y + dy
                if xx >= N or yy >= N:
                    continue
                k2 = ident[yy, xx]
                if k2 < 0 or k2 == k:
                    continue
                if arestas is not None:
                    tipo = arestas.get((k, k2)) or arestas.get((k2, k))
                else:
                    quina = normais[k] + normais[k2]; quina = quina / np.linalg.norm(quina)
                    tipo = "L" if quina @ LUZ > 0.8 else "S" if abs(t[k] - t[k2]) <= 1 and quina @ LUZ < 0.3 else None
                if not tipo:
                    continue
                claro, escuro = ((x, y), (xx, yy)) if t[k] <= t[k2] else ((xx, yy), (x, y))
                if tipo == "L":
                    tc = min(t[k], t[k2])
                    g[claro[1]][claro[0]] = "L" if tc == 0 else LETRAS[tc - 1]
                else:
                    te = max(t[k], t[k2])
                    g[escuro[1]][escuro[0]] = "S" if te == 6 else LETRAS[te + 1]
    if vidro and tons:  # o repouso do vidro: a luz que atravessa sai pela borda de baixo e da direita, como num dado de
        # resina: faixas por dentro do contorno (sem pontilhado, que ali vira areia), mais largas embaixo à direita
        c = (N - 1) / 2
        for y in range(N):
            for x in range(N):
                k = ident[y, x]
                lado = (x - c) * 0.7 + (y - c)  # quanto o pixel está para baixo e para a direita
                if k < 0 or g[y][x] not in LETRAS or lado < N * 0.14:
                    continue
                dist = min((max(abs(dx), abs(dy)) for dx in range(-4, 5) for dy in range(-4, 5)
                            if not (0 <= x + dx < N and 0 <= y + dy < N) or ident[y + dy, x + dx] < 0), default=9)
                largura = 1 + round(2 * min(1.0, (lado - N * 0.14) / (N * 0.3)))  # 1 a 3 pixels
                if N < 40:  # na tirinha e na ficha, um pixel só (três seriam metade do dado)
                    largura = 1 if lado > N * 0.3 else 0
                tom = LETRAS.index(g[y][x])
                if dist == 1 and largura >= 2:
                    g[y][x] = "T" if largura == 3 else LETRAS[max(0, tom - 2)]
                elif dist <= largura:
                    g[y][x] = LETRAS[max(0, tom - (2 if dist == 1 else 1))]
    # o contorno por fora (só pelos lados)
    for y in range(N):
        for x in range(N):
            if g[y][x] == "." and any(0 <= x + dx < N and 0 <= y + dy < N and ident[y + dy, x + dx] >= 0
                                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = "k"
    return ["".join(r) for r in g], ident, normais, vis, xy


def png(grade, pal, escala, caminho=None):
    N = len(grade)
    im = Image.new("RGBA", (len(grade[0]), N), (0, 0, 0, 0))
    for y, r in enumerate(grade):
        for x, ch in enumerate(r):
            if ch in pal:
                c = pal[ch]
                im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im = im.resize((im.width * escala, im.height * escala), Image.NEAREST)
    if caminho:
        im.save(caminho)
    return im


def paleta(mat):
    m = MATERIAIS[mat]
    p = {LETRAS[i]: c for i, c in enumerate(m["rampa"])}
    p.update(L=m["luz"], S=m["sombra"], k=m["contorno"])
    if "atravessa" in m:
        p["T"] = m["atravessa"]; p["W"] = m["brilho"]
    return p


# ------------------------------------------------------------------ o repouso: os tons de cada face, à mão
# As faces visíveis no repouso (o número é o de FACES): 0 a da frente; 2 e 3 em cima à esquerda (de frente para a luz);
# 4 em cima à direita; 16 a da esquerda; 1 a da direita; 18, 6 e 5 embaixo (da esquerda para a direita); 7 a da
# direita de baixo, a mais escura.
TONS = {
    # o marfim: a face da frente clara (o número entalhado escuro em cima dela), as de cima mais claras, as de baixo
    # caindo para o castanho; a da esquerda clara (a luz vem dela) e a da direita na meia-sombra
    "marfim": {2: 0, 3: 0, 0: 1, 4: 2, 16: 2, 1: 3, 18: 3, 6: 4, 7: 5, 5: 6},
    # o vidro: a face da frente na meia-luz (o número aceso dentro dela é o mais claro), o brilho nas de cima à
    # esquerda, as de baixo quase pretas
    "vidro": {3: 1, 2: 1, 4: 2, 16: 2, 0: 3, 1: 4, 6: 4, 18: 5, 5: 5, 7: 6},
}
# as quinas do repouso, à mão: "L" o fio de luz (a quina vira para a luz), "S" a sombra (separa duas faces de tom
# vizinho); as outras ficam só na troca de tom
ARESTAS = {
    # o marfim: o fio na quina de cima da face da frente (a que pega a luz) e no cume de cima; as sombras macias
    # separam as faces de tom parecido (as duas de cima à esquerda, e as de baixo entre si)
    "marfim": {(0, 3): "L", (2, 4): "L", (2, 3): "S", (4, 1): "S", (16, 18): "S", (18, 6): "S", (7, 5): "S"},
    # o vidro: o brilho só nas quinas de cima à esquerda (o resto é o vidro, com as quinas de trás à vista)
    "vidro": {(0, 3): "L", (2, 3): "L", (2, 4): "L", (3, 16): "L", (0, 1): "L"},
}
FRENTE = 1.12  # os vértices da face da frente, abertos para o número de dois dígitos

# os tamanhos: o centro (70, ampliado 2×: 140 px; o dado de hoje tem 128, e o número cresce com ele), a tirinha do texto (30, 2×: 60 px) e o
# ícone da ficha (22, 1×)
TAMANHOS = {"centro": (70, 34.5), "tirinha": (30, 14.5), "ficha": (22, 10.5)}
GIRO = 6  # quadros do giro: meia volta em torno de um eixo de simetria (180°, o dado volta a ser igual): o laço fecha


def eixo_do_giro():
    """O eixo de ordem 2 (pelo meio de uma aresta) mais deitado na tela e mais perto do horizontal: o dado tomba para
    a frente e para o lado, e a meia volta fecha o laço."""
    P = (REPOUSO @ VERT.T).T
    melhor = None
    for a, b in itertools.combinations(range(12), 2):
        if abs(np.linalg.norm(VERT[a] - VERT[b]) - 2) > 1e-6:
            continue
        m = (P[a] + P[b]) / 2; m = m / np.linalg.norm(m)
        nota = abs(m[0]) * 2 + abs(m[1]) - abs(m[2]) * 3
        if melhor is None or nota > melhor[0]:
            melhor = (nota, m)
    return melhor[1]


# ------------------------------------------------------------------ os algarismos, à mão
# O grande (8×13, traço de 2): o número do centro. O pequeno (3×5): o da tirinha.
ALG_G = {
    "0": ['..####..', '.##..##.', '##....##', '##....##', '##....##', '##....##', '##....##', '##....##', '##....##', '##....##', '##....##', '.##..##.', '..####..'],
    "1": ['...##...', '..###...', '.####...', '##.##...', '...##...', '...##...', '...##...', '...##...', '...##...', '...##...', '...##...', '.######.', '.######.'],
    "2": ['..####..', '.##..##.', '##....##', '......##', '......##', '.....##.', '....##..', '...##...', '..##....', '.##.....', '##......', '########', '########'],
    "3": ['.######.', '########', '.....##.', '....##..', '...##...', '..####..', '.....##.', '......##', '......##', '##....##', '###..###', '.######.', '..####..'],
    "4": ['.....##.', '....###.', '...####.', '..##.##.', '.##..##.', '##...##.', '##...##.', '########', '########', '.....##.', '.....##.', '.....##.', '.....##.'],
    "5": ['########', '########', '##......', '##......', '##......', '######..', '#######.', '.....###', '......##', '......##', '##...###', '.######.', '..####..'],
    "6": ['...####.', '..##....', '.##.....', '##......', '##......', '######..', '#######.', '###..###', '##....##', '##....##', '###..###', '.######.', '..####..'],
    "7": ['########', '########', '......##', '.....##.', '.....##.', '....##..', '....##..', '...##...', '...##...', '..##....', '..##....', '..##....', '..##....'],
    "8": ['..####..', '.##..##.', '##....##', '##....##', '.##..##.', '..####..', '.######.', '##....##', '##....##', '##....##', '##....##', '.##..##.', '..####..'],
    "9": ['..####..', '.######.', '###..###', '##....##', '##....##', '###..###', '.#######', '..######', '......##', '......##', '.....##.', '....##..', '..###...'],
}
ALG_P = {
    "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["###", "..#", "###", "#..", "###"], "3": ["###", "..#", ".##", "..#", "###"],
    "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
    "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", "..#", ".#.", ".#."],
    "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "###"],
}

# Os retoques pixel a pixel do repouso, por material e tamanho: {(x, y): letra}, com o porquê.
AJUSTES = {
    ("marfim", "centro"): {},
    # o vidro: o reflexo da janela (um risco curto, branco, na face de cima à esquerda, paralelo à quina) e um ponto
    # no vértice de cima: o que diz "vidro" de longe
    ("vidro", "centro"): {(23, 11): "L", (24, 11): "W", (25, 10): "W", (26, 10): "W", (27, 9): "L", (34, 1): "W"},
    ("marfim", "tirinha"): {},
    ("vidro", "tirinha"): {},
    ("marfim", "ficha"): {},
    ("vidro", "ficha"): {},
}


def repouso(mat, tam):
    N, raio = TAMANHOS[tam]
    g, ident, normais, vis, xy = quadro(REPOUSO, N, raio, frente=FRENTE, tons=TONS[mat], vidro=(mat == "vidro"),
                                        arestas=ARESTAS[mat])
    g = [list(r) for r in g]
    for (x, y), ch in AJUSTES[(mat, tam)].items():
        g[y][x] = ch
    # a face da frente, em pixels: onde o número pode ir (sem as quinas)
    frente = [[1 if ident[y, x] == 0 and g[y][x] not in "LSk" else 0 for x in range(N)] for y in range(N)]
    return ["".join(r) for r in g], frente, xy[list(FRENTE_FACE)].round(2).tolist()


def giro(mat, tam):
    N, raio = TAMANHOS[tam]
    e = eixo_do_giro()
    quadros = []
    for i in range(GIRO):
        R = rot(e, math.pi * i / GIRO) @ REPOUSO
        g, ident, normais, vis, xy = quadro(R, N, raio, vidro=(mat == "vidro"))
        g = [list(r) for r in g]
        if mat == "marfim" and tam != "ficha":  # as marcas dos números nas faces que olham para a frente (o entalhe)
            for k in vis:
                if normais[k][2] > 0.62:
                    cx, cy = xy[list(FACES[k])].mean(0)
                    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)) if tam == "centro" else ((0, 0),):
                        x, y = int(round(cx)) + dx - (1 if tam == "centro" else 0), int(round(cy)) + dy
                        if 0 <= x < N and 0 <= y < N and ident[y, x] == k:
                            g[y][x] = "S"
        quadros.append(["".join(r) for r in g])
    return quadros


def caber(frente, alg, digitos="20"):
    """Onde o número cabe na face da frente, inteiro e com um pixel de folga: o canto (x, y) do bloco mais baixo
    possível perto do centro da face (os dois dígitos com 1 pixel entre eles)."""
    w = sum(len(alg[d][0]) for d in digitos) + len(digitos) - 1
    h = len(alg[digitos[0]])
    N = len(frente)
    pts = [(x, y) for y in range(N) for x in range(N) if frente[y][x]]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    melhor = None
    for y0 in range(N - h):
        for x0 in range(N - w):
            ok = all(frente[y][x] for y in range(y0 - 1, y0 + h + 1) for x in range(x0 - 1, x0 + w + 1)
                     if 0 <= y < N and 0 <= x < N) and y0 > 0 and x0 > 0
            if ok:
                d = (x0 + w / 2 - cx) ** 2 + (y0 + h / 2 - cy) ** 2
                if melhor is None or d < melhor[0]:
                    melhor = (d, x0, y0)
    return melhor and {"x": melhor[1], "y": melhor[2], "w": w, "h": h}


if __name__ == "__main__":
    sai = AQUI / "pranchas"; sai.mkdir(exist_ok=True)
    # a tinta do número por estado (numero.json: a mesma tabela da prancha)
    dados = {"materiais": {}, "algarismos": {"g": ALG_G, "p": ALG_P},
             "tintas": json.loads((AQUI / "numero.json").read_text(encoding="utf-8"))}
    for mat in MATERIAIS:
        m = {"paleta": paleta(mat), "tamanhos": {}}
        for tam in TAMANHOS:
            g, frente, tri = repouso(mat, tam)
            lugar = None
            if tam != "ficha":
                lugar = caber(frente, ALG_G if tam == "centro" else ALG_P)
                print(mat, tam, "o número cabe em", lugar)
            m["tamanhos"][tam] = {"repouso": g, "giro": giro(mat, tam) if tam != "ficha" else [], "numero": lugar}
            png(g, paleta(mat), 4 if tam != "centro" else 3, sai / f"{mat}-{tam}.png")
        dados["materiais"][mat] = m
    js = ("/* GERADO por desenhar_d20.py (protótipo do d20, etapa 2; nada no jogo): as grades do dado nas duas propostas,\n"
          "   um caractere por pixel. Não edite à mão: os retoques vão em AJUSTES. */\n"
          "const D20_DADOS = " + json.dumps(dados, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (AQUI / "d20-dados.js").write_text(js, encoding="utf-8")
    # a cópia do jogo (1.202.0: o Marfim e o Vidro integrados), com o cabeçalho de lá; as duas saem sempre iguais
    jogo = js.replace("/* GERADO por desenhar_d20.py (protótipo do d20, etapa 2; nada no jogo): as grades do dado nas duas propostas,",
                      "/* GERADO por ferramentas/prototipos/hud/d20/desenhar_d20.py (o d20 do Marfim e do Vidro, 1.202.0): as grades do dado,")
    (AQUI.parents[3] / "rpg" / "web" / "static" / "d20" / "dados.js").write_text(jogo, encoding="utf-8")
    print("ok")
