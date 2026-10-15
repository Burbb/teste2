"""Os candidatos do experimento de itens e ícones (fora do jogo): machado, unguento, bomba de fumaça, espada, escudo e
anel no estilo do mundo, e os ícones de interface Grimório, Talentos, Ataque, Defesa e Fugir.

Cada peça é uma função do lado (32, e 24 ou 36 onde o jogo usa esse tamanho): as formas (traço grosso, disco,
polígono) são pintadas com letras de uma paleta, o contorno escuro de 1 pixel sai sozinho, e a luz vem de cima e da
esquerda, como no martelo e na Pena de Fênix aprovados (desenhos.js). A saída é uma grade de letras por peça, no
formato de arte-teste.js (itens-icones-teste.js); com --png, também as folhas ampliadas para conferência.

    python ferramentas/prototipos/hud/desenhar_itens.py [--png pasta]
"""

import math
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent

# A paleta: a do martelo (ferro, madeira, latão, couro) e o que as peças novas pedem.
CORES = {
    "#": "#121316",
    "W": "#e4e8ee", "S": "#b0b6c0", "s": "#7c838e", "d": "#4e545e", "D": "#33373e",       # ferro
    "M": "#9a6438", "m": "#6e4426", "n": "#4a2c18",                                       # madeira
    "Y": "#e0b850", "y": "#a87c2c", "z": "#6e4e1a",                                       # latão
    "L": "#7a5038", "l": "#4e3022", "k": "#33201a",                                       # couro
    "C": "#c08458", "c": "#94603e", "x": "#64402a",                                       # barro
    "P": "#f2f4f6", "p": "#c4ccd4", "q": "#8e98a4",                                       # unguento de prata
    "F": "#d2cfc6", "f": "#a4a199", "g": "#77756f",                                       # fumaça
    "B": "#5e5e64", "b": "#424248", "v": "#2c2c30",                                       # bomba (barro escuro)
    "O": "#ffe08a", "o": "#e8862e",                                                       # faísca
    "R": "#8a4430", "r": "#64302a", "u": "#421c18",                                       # couro vermelho do livro
    "E": "#e8dcc0", "e": "#b4a684",                                                       # folhas
    "T": "#c8b080",                                                                       # pavio
}
# As rampas de luz: cada letra sabe a de cima (mais clara) e a de baixo (mais escura) do mesmo material.
RAMPAS = ["WSsdD", "Mmn", "Yyz", "Llk", "Ccx", "Ppq", "Ffg", "Bbv", "Rru", "Ee"]
CLARO, ESCURO = {}, {}
for rampa in RAMPAS:
    for i, c in enumerate(rampa):
        CLARO[c] = rampa[max(0, i - 1)]
        ESCURO[c] = rampa[min(len(rampa) - 1, i + 1)]


class Tela:
    def __init__(self, n):
        self.n = n
        self.k = n / 32            # as medidas são escritas para 32 e escalam para o lado pedido
        self.g = [["."] * n for _ in range(n)]
        self.sem_contorno = set()

    def p(self, v):
        return v * self.k

    def por(self, x, y, c):
        if 0 <= x < self.n and 0 <= y < self.n and c:
            self.g[y][x] = c

    def cada(self, teste, cor):
        """Pinta os pixels cujo centro passa no teste (em coordenadas de 32); `cor` é letra ou função (x, y) -> letra."""
        for y in range(self.n):
            for x in range(self.n):
                cx, cy = (x + 0.5) / self.k, (y + 0.5) / self.k
                if teste(cx, cy):
                    self.por(x, y, cor(cx, cy) if callable(cor) else cor)

    def disco(self, x0, y0, r, cor):
        self.cada(lambda x, y: (x - x0) ** 2 + (y - y0) ** 2 <= r * r, cor)

    def elipse(self, x0, y0, rx, ry, cor):
        self.cada(lambda x, y: ((x - x0) / rx) ** 2 + ((y - y0) / ry) ** 2 <= 1, cor)

    def traco(self, a, b, larg, cor):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy

        def dentro(x, y):
            t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / L2))
            return (x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2 <= (larg / 2) ** 2
        self.cada(dentro, cor)

    def poli(self, pts, cor):
        def dentro(x, y):
            c, j = False, len(pts) - 1
            for i in range(len(pts)):
                (xi, yi), (xj, yj) = pts[i], pts[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                    c = not c
                j = i
            return c
        self.cada(dentro, cor)

    def risco(self, a, b, cor):
        """Uma linha de 1 pixel, sem contorno (fumaça, rastros)."""
        (ax, ay), (bx, by) = [(self.p(u), self.p(v)) for u, v in (a, b)]
        passos = int(max(abs(bx - ax), abs(by - ay))) + 1
        for i in range(passos + 1):
            x, y = round(ax + (bx - ax) * i / passos - 0.5), round(ay + (by - ay) * i / passos - 0.5)
            self.por(x, y, cor)
            self.sem_contorno.add((x, y))

    def fumaca(self, x0, y0, r):
        """Um rolo de fumaça: claro, sem o contorno escuro e sem facetas (com eles, vira pedra); a borda de baixo e a
        da direita um tom abaixo (sombrear() depois de todos os rolos)."""
        for y in range(self.n):
            for x in range(self.n):
                cx, cy = (x + 0.5) / self.k, (y + 0.5) / self.k
                if (cx - x0) ** 2 + (cy - y0) ** 2 <= r * r:
                    self.por(x, y, "F")
                    self.sem_contorno.add((x, y))

    def sombrear(self):
        fum = {(x, y) for (x, y) in self.sem_contorno if self.g[y][x] == "F"}
        for (x, y) in fum:
            if (x, y + 1) not in fum or (x + 1, y) not in fum:
                self.g[y][x] = "f"

    def luz(self, letras=None):
        """O pixel com o fundo em cima ou à esquerda clareia um degrau; com o fundo embaixo ou à direita, escurece."""
        vazio = lambda x, y: not (0 <= x < self.n and 0 <= y < self.n) or self.g[y][x] in ".#"
        novo = [linha[:] for linha in self.g]
        for y in range(self.n):
            for x in range(self.n):
                c = self.g[y][x]
                if c in ".#" or (letras and c not in letras) or (x, y) in self.sem_contorno:
                    continue
                if vazio(x - 1, y) or vazio(x, y - 1):
                    novo[y][x] = CLARO.get(c, c)
                elif vazio(x + 1, y) or vazio(x, y + 1):
                    novo[y][x] = ESCURO.get(c, c)
        self.g = novo

    def contorno(self):
        novo = [linha[:] for linha in self.g]
        for y in range(self.n):
            for x in range(self.n):
                if self.g[y][x] != ".":
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    u, v = x + dx, y + dy
                    if 0 <= u < self.n and 0 <= v < self.n and self.g[v][u] not in ".#" and (u, v) not in self.sem_contorno:
                        novo[y][x] = "#"
                        break
        self.g = novo

    def grade(self):
        return ["".join(linha) for linha in self.g]


def esfera(x0, y0, r, tons):
    """A cor de um ponto numa esfera com a luz de cima-esquerda, em len(tons) degraus (o primeiro é o brilho)."""
    lx, ly, lz = -0.55, -0.6, 0.58

    def cor(x, y):
        nx, ny = (x - x0) / r, (y - y0) / r
        nz = math.sqrt(max(0, 1 - nx * nx - ny * ny))
        i = nx * lx + ny * ly + nz * lz
        limites = [0.93, 0.6, 0.2, -0.2, -2]
        for k, t in enumerate(tons):
            if i >= limites[k + (5 - len(tons))]:
                return t
        return tons[-1]
    return cor


def ao_longo(a, b, cor_lados):
    """Para traços: a posição do pixel atravessando o traço (-1 de um lado, +1 do outro) escolhe a cor."""
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy)
    px, py = -dy / L, dx / L      # a normal; para traços que sobem para a direita, aponta para cima-esquerda

    def cor(x, y):
        return cor_lados(-((x - ax) * px + (y - ay) * py))
    return cor


# ---------------------------------------------------------------------------------------------------------- as peças

def machado(n=32):
    t = Tela(n)
    t.traco((6, 27), (22, 5), 3.2, ao_longo((6, 27), (22, 5), lambda v: "M" if v < -0.6 else "m" if v < 0.7 else "n"))
    t.traco((6, 27), (10, 21.4), 3.4, ao_longo((6, 27), (10, 21.4), lambda v: "L" if v < -0.5 else "l" if v < 0.8 else "k"))
    t.disco(5.5, 27.8, 1.8, "y")
    # a cabeça: a lâmina em meia-lua caindo para a direita (a ponta de cima e a barba), o fio claro no arco, o talão atrás
    cx, cy, r = 20.6, 9.8, 9.2
    arco = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(-58, 84, 8)]
    t.poli([(18.8, 5.8), (22.4, 4.6)] + arco + [(21.6, 15.6), (21, 12), (19.2, 10.6)],
           lambda x, y: "W" if (x - cx) ** 2 + (y - cy) ** 2 > (r - 1.5) ** 2 else "S" if y < 8.4 else "s" if y < 12.6 else "d")
    t.poli([(16.6, 6.2), (19.4, 4.2), (21.8, 8.2), (19.6, 10.8)], "D")
    t.poli([(15.4, 5.6), (17.4, 3.8), (19, 5.6), (17, 7.6)], "d")
    t.luz("Mmn")
    t.contorno()
    return t.grade()


def unguento(n=32):
    t = Tela(n)
    # o pote de barro de barriga larga, o gargalo curto com o cordão, a boca aberta e o unguento de prata em monte,
    # com a espátula de madeira
    t.traco((18.6, 12), (25.4, 3.6), 2.2, ao_longo((18.6, 12), (25.4, 3.6), lambda v: "M" if v < 0 else "m"))
    t.elipse(16, 22.2, 10.8, 7, lambda x, y: "C" if (x - 11.5) ** 2 + (y - 19.5) ** 2 < 12 else "x" if x > 22.5 or y > 26.4 else "c")
    t.cada(lambda x, y: y > 27.6, ".")
    t.cada(lambda x, y: 26.4 < y < 28.6 and abs(x - 16) < 7.6, "x")
    t.cada(lambda x, y: 13.6 < y < 17 and abs(x - 16) < 6.2, lambda x, y: "C" if x < 13 else "x" if x > 20 else "c")
    t.cada(lambda x, y: 15.6 < y < 16.8 and abs(x - 16) < 6.6, "l")
    t.elipse(16, 13.6, 7.8, 2.4, lambda x, y: "C" if x < 18 else "c")
    t.elipse(16, 13.5, 6, 1.4, "x")
    t.cada(lambda x, y: y < 13.6 and ((x - 16) / 5.2) ** 2 + ((y - 13.6) / 4.2) ** 2 <= 1,
           lambda x, y: "P" if (x - 14) ** 2 + (y - 11) ** 2 < 3.2 else "p" if x < 17.6 else "q")
    t.luz("Ccx")
    t.contorno()
    return t.grade()


def bomba(n=32):
    t = Tela(n)
    # a fumaça atrás, a bola de barro escuro com a corda, o tampão e o pavio aceso
    for (x, y, r) in ((23.6, 26, 4.2), (27.6, 22.2, 3.2), (28.6, 27.4, 3), (6.4, 27, 3.6), (3.2, 24, 2.4)):
        t.fumaca(x, y, r)
    t.sombrear()
    t.disco(14.5, 19.5, 9.2, esfera(14.5, 19.5, 9.2, "sBbv"))
    t.cada(lambda x, y: abs((y - 19.5) - 0.18 * (x - 14.5) - (1.2 - ((x - 14.5) / 9.2) ** 2 * 2.4)) < 0.75
           and (x - 14.5) ** 2 + (y - 19.5) ** 2 < 9.2 ** 2, lambda x, y: "L" if x < 13 else "l")
    t.poli([(11.6, 8.4), (17.4, 8.4), (17.8, 11.4), (11.2, 11.4)], lambda x, y: "M" if x < 13.5 else "m" if x < 16.4 else "n")
    t.contorno()
    t.risco((15.5, 8), (17, 5.5), "T")
    t.risco((17, 5.5), (19.5, 4), "T")
    t.disco(21, 3, 1.9, "o")
    t.por(round(t.p(21) - 0.5), round(t.p(3) - 0.5), "O")
    for x, y in ((24, 1), (23.5, 5.5), (18.8, 1.5)):
        t.risco((x, y), (x, y), "O")
    return t.grade()


def espada(n=32):
    t = Tela(n)
    # a lâmina reta com o sulco, a guarda de latão, o punho de couro com voltas e o pomo
    lam = lambda v: "W" if v < -0.75 else "S" if v < 0.1 else "s" if v < 0.85 else "d"
    t.traco((10.5, 21.5), (25.4, 6.6), 3.4, ao_longo((10.5, 21.5), (25.4, 6.6), lam))
    t.poli([(24, 6.2), (28.6, 3.4), (25.8, 8)], "S")
    t.risco((12.5, 19.5), (22, 10), "s")
    t.traco((7.2, 18.2), (13.8, 24.8), 2.6, ao_longo((7.2, 18.2), (13.8, 24.8), lambda v: "y" if v < -0.3 else "Y"))
    t.traco((10, 22), (5.6, 26.4), 2.6, lambda x, y: "L" if int(x + y + 0.5) % 3 else "k")
    t.disco(4.6, 27.4, 2, esfera(4.6, 27.4, 2, "Yyz"))
    t.contorno()
    return t.grade()


def escudo(n=32):
    t = Tela(n)
    # o escudo redondo de tábuas com o aro de ferro, cravos de latão e a bossa de ferro no meio
    tabua = lambda x, y: "n" if abs(((x - 3.5) % 6.4) - 6.2) < 0.5 else ("M" if int((x - 3.5) // 6.4) % 2 == 0 else "m")
    t.disco(16, 16, 13.4, lambda x, y: "S" if x + y < 22 else "s" if x + y < 40 else "d")
    t.disco(16, 16, 11.3, lambda x, y: ESCURO[tabua(x, y)] if (x - 16) + (y - 16) > 9 and tabua(x, y) != "n" else tabua(x, y))
    for ang in range(0, 360, 60):
        r = math.radians(ang + 30)
        t.disco(16 + 12.35 * math.cos(r), 16 + 12.35 * math.sin(r), 0.75, "Y")
    t.disco(16, 16, 4.3, esfera(16, 16, 4.3, "WSsdD"))
    t.contorno()
    return t.grade()


def anel(n=32):
    t = Tela(n)
    # o sinete de latão em três quartos: o aro grosso com o furo, e em cima o selo oval com a borda e uma cruz gravada
    t.elipse(16, 20.8, 10.4, 8, lambda x, y: "Y" if x + y < 30 else "y" if x + y < 41 else "z")
    t.cada(lambda x, y: ((x - 16) / 6.6) ** 2 + ((y - 21.6) / 4.8) ** 2 <= 1, lambda x, y: "z" if y < 19.6 else ".")
    t.elipse(16, 11.8, 7.2, 4.4, "z")
    t.elipse(16, 10.6, 7.2, 4.2, lambda x, y: "y" if x > 19.5 or y > 12.6 else "Y")
    t.elipse(16, 10.8, 4.8, 2.5, "z")
    t.contorno()
    for (x, y) in ((16, 9.5), (16, 10.5), (16, 11.5), (14.5, 10.5), (17.5, 10.5)):
        t.risco((x, y), (x, y), "Y")
    return t.grade()


def grimorio(n=32):
    t = Tela(n)
    # o livro de couro vermelho-escuro, de lado: a lombada com nervuras, as folhas à mostra, cantos e fecho de latão
    t.poli([(24, 4), (27.4, 5.6), (27.4, 29), (24, 27.6)], lambda x, y: "e" if int(y) % 2 else "E")
    t.poli([(6, 3.6), (25.2, 3.6), (25.2, 27.4), (6, 27.4)], lambda x, y: "R" if x < 12 and y < 12 else "u" if x > 22 or y > 24 else "r")
    t.poli([(4.2, 4.6), (7.8, 3.6), (7.8, 27.4), (4.2, 28.4)], lambda x, y: "u" if int(y) in (8, 15, 22) else "r")
    t.poli([(20.4, 3.6), (25.2, 3.6), (25.2, 8.4)], "Y")
    t.poli([(20.4, 27.4), (25.2, 27.4), (25.2, 22.6)], "y")
    t.poli([(18.6, 13.8), (28.6, 13.8), (28.6, 17.2), (18.6, 17.2)], lambda x, y: "Y" if y < 15 else "y")
    t.disco(14.2, 15.5, 3.4, esfera(14.2, 15.5, 3.4, "Yyz"))
    t.disco(14.2, 15.5, 1.4, "u")
    t.luz("Rru")
    t.contorno()
    return t.grade()


def talentos(n=32):
    t = Tela(n)
    # a árvore: o tronco e três galhos de madeira que acabam em três nós de latão (os ramos da árvore de talentos)
    madeira = lambda a, b: ao_longo(a, b, lambda v: "M" if v < -0.3 else "m" if v < 0.6 else "n")
    t.traco((16, 29), (16, 17), 3.6, lambda x, y: "M" if x < 15.4 else "m" if x < 16.8 else "n")
    t.traco((16, 20), (8.2, 10.4), 2.4, madeira((16, 20), (8.2, 10.4)))
    t.traco((16, 20), (23.8, 10.4), 2.4, madeira((16, 20), (23.8, 10.4)))
    t.traco((16, 18), (16, 8), 2.4, lambda x, y: "M" if x < 16 else "m")
    t.traco((12, 29.4), (20, 29.4), 1.6, "m")
    for (x, y) in ((7.2, 8.6), (16, 6), (24.8, 8.6)):
        t.disco(x, y, 3.6, esfera(x, y, 3.6, "WYYyz"))
    t.contorno()
    return t.grade()


def ataque(n=32):
    t = Tela(n)
    # duas espadas cruzadas (a força do golpe, não um item): lâminas de ferro e guardas de latão
    for (a, b, g1, g2, p1, p2) in (((7, 25), (26, 6), (5, 20.6), (11.4, 27), (7, 25), (4.2, 27.8)),
                                   ((25, 25), (6, 6), (20.6, 27), (27, 20.6), (25, 25), (27.8, 27.8))):
        t.traco(a, b, 2.8, ao_longo(a, b, lambda v: "W" if v < -0.4 else "S" if v < 0.5 else "s"))
        t.traco(g1, g2, 2.2, "Y")
        t.traco(p1, p2, 2.4, "l")
    t.luz("Y")
    t.contorno()
    return t.grade()


def defesa(n=32):
    t = Tela(n)
    # o escudo de bico em dois planos (a luz na metade da esquerda), a borda de latão e a faixa do meio
    forma = [(5, 4.2), (16, 2.6), (27, 4.2), (27, 15), (16, 29.6), (5, 15)]
    t.poli(forma, "Y")
    meio = [(7, 6), (16, 4.7), (25, 6), (25, 15), (16, 27), (7, 15)]
    t.poli(meio, lambda x, y: "S" if x < 15.4 else "s")
    t.cada(lambda x, y: abs(x - 16) < 1.2 and 4.4 < y < 27, lambda x, y: "W" if x < 16 else "d")
    t.luz("Yy")
    t.contorno()
    return t.grade()


def fugir(n=32):
    t = Tela(n)
    # a bota em passo largo, o calcanhar no ar, a poeira levantada atrás e os rastros do movimento (sem o raio da Agilidade)
    for (x, y, r) in ((8.6, 27, 3.4), (4.2, 24.4, 2.6), (3.4, 29, 2)):
        t.fumaca(x, y, r)
    t.sombrear()
    ang = math.radians(-14)
    rot = lambda pts: [(16 + (x - 16) * math.cos(ang) - (y - 16) * math.sin(ang),
                        16 + (x - 16) * math.sin(ang) + (y - 16) * math.cos(ang)) for x, y in pts]
    t.poli(rot([(11, 4), (20, 4), (20.4, 16), (27.6, 18.6), (29, 22.4), (28.6, 24.6), (11.4, 24.6), (10.6, 16)]),
           lambda x, y: "L" if x < 15 else "l" if y < 24.6 else "k")
    t.poli(rot([(10.6, 22.8), (29, 22.8), (28.6, 25.4), (10.8, 25.4)]), "k")
    t.poli(rot([(10.6, 3.4), (20.6, 3.4), (20.6, 6.6), (10.6, 6.6)]), lambda x, y: "M" if x < 16 else "m")
    t.luz("Ll")
    t.contorno()
    for y, x0, x1 in ((9, 2, 7), (13, 1, 6.5), (17, 3, 7.5)):
        t.risco((x0, y), (x1, y), "f")
    return t.grade()


PECAS = {
    "machado": (machado, [32]), "unguento": (unguento, [32]), "bomba": (bomba, [32]),
    "espada": (espada, [32]), "escudo": (escudo, [32]), "anel": (anel, [32]),
    "grimorio": (grimorio, [32, 36]), "talentos": (talentos, [32, 36]),
    "ataque": (ataque, [24, 32]), "defesa": (defesa, [24, 32]), "fugir": (fugir, [32]),
}


def gerar():
    return {f"{nome}-{lado}": f(lado) for nome, (f, lados) in PECAS.items() for lado in lados}


def js(pecas):
    usadas = sorted({c for g in pecas.values() for linha in g for c in linha} - {"."})
    cores = ", ".join(f'"{c}": "{CORES[c]}"' for c in usadas)
    linhas = ["/* Gerado por desenhar_itens.py (não editar à mão): os candidatos do experimento de itens e ícones, em",
              "   ArteTeste.PECAS (arte-teste.js). itens-icones-teste.html mostra; itens-icones-no-jogo.js veste o jogo. */",
              '"use strict";', "", "(() => {", f"  const CORES = {{{cores}}};"]
    for nome, g in pecas.items():
        linhas.append(f'  ArteTeste.PECAS["cand-{nome}"] = {{ cores: CORES, grade: [')
        linhas += [f'    "{l}",' for l in g[:-1]] + [f'    "{g[-1]}"] }};']
    linhas.append("})();")
    return "\n".join(linhas) + "\n"


def png(pecas, pasta):
    from PIL import Image
    pasta = pathlib.Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    E = 8
    larg = sum(len(g) * E + 16 for g in pecas.values())
    folha = Image.new("RGBA", (larg, 36 * E + 16), (14, 15, 17, 255))
    x = 8
    for g in pecas.values():
        for j, linha in enumerate(g):
            for i, c in enumerate(linha):
                if c != ".":
                    h = CORES[c]
                    folha.paste((int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255), (x + i * E, 8 + j * E, x + (i + 1) * E, 8 + (j + 1) * E))
        x += len(g) * E + 16
    folha.save(pasta / "candidatos-ampliados.png")


if __name__ == "__main__":
    pecas = gerar()
    (AQUI / "itens-icones-teste.js").write_text(js(pecas), encoding="utf-8")
    if "--png" in sys.argv:
        png(pecas, sys.argv[sys.argv.index("--png") + 1])
    print(len(pecas), "peças")
