"""Rodada 2 do peitoral de couro (o desenho "gibao") e das botas de couro ("bota"): as listas de pixels por camada que
o pintar.lua (ferramentas/arte/aseprite/) escreve no Aseprite pelo MCP. O Python só calcula; quem pinta é o Aseprite.
A rodada 1 (couro_r1.py, histórico) fez o 32 e o 64; aqui o 64 e as botas de 32 saem iguais a ela, o fechamento do
gibão de 32 vira um cordão em zigue-zague (os pontos soltos liam como botões) e entram o 40 e o 48, com a mesma
construção. O que cada tamanho simplifica e os pixels de ajuste de cada um estão em MEDIDAS_GIBAO e MEDIDAS_BOTA.

    python ferramentas/prototipos/hud/couro-aseprite/auxiliares/couro_r2.py <pasta> [gibao|bota] [32|40|48|64]

Grava <pasta>/<peça>-<lado>/<camada>.lua ("return \"x,y,RRGGBB;...\"") e .txt, e previa.png (o composto, para
conferir a leitura do Aseprite). Cada tamanho é desenhado na própria grade: as formas são polígonos num espaço de 100
unidades, rasterizados pelo centro de cada pixel; a luz é por planos (poucas faixas largas por parte), não por
gradiente; o que não cabe no 32 sai dele (MEDIDAS) e as correções olhando cada tamanho vão em AJUSTES.
A luz é a da família: de cima e da esquerda.
"""
import pathlib
import sys

from PIL import Image

CONTORNO = "08080A"

# --- as rampas (do escuro ao claro) --------------------------------------------------------------------------------
COURO = ["1C120C", "2E1E13", "45301E", "604229", "7C5634", "986C42", "B48752"]       # o couro do gibão (curtido)
BORDA = ["140C08", "22150D", "321F13", "45301E"]                                      # as tiras de borda, mais escuras
FORRO = ["0F0906", "1E130C", "2E1E13"]                                                # o avesso, visto pela gola
CORDAO = ["5E472E", "8E7250", "BFA27A"]                                               # o cordão do fechamento
GASTO = ["8A6A4C", "A07E5C"]                                                          # o couro raspado, fosco
BOTA = ["1A110B", "2A1A10", "3E2716", "57381F", "724B2A", "8E6236", "AE7E47"]        # o couro da bota (mais escuro)
DOBRA = ["3F2C1C", "5C4129", "7A5838", "97724C", "B08C62"]                            # o cano dobrado (o avesso, camurça)
SOLA = ["0E0A08", "1C1510", "2B221A", "3D3226"]                                       # a sola e o salto
FIVELA = ["3A2E18", "6E5C38", "A8925C", "D6C48E"]                                     # a fivela de bronze velho


def dentro(pol, x, y):
    """O ponto (x, y) está dentro do polígono (lista de (x, y))? Regra par-ímpar."""
    d = False
    for i in range(len(pol)):
        (x1, y1), (x2, y2) = pol[i], pol[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            d = not d
    return d


class Desenho:
    """A grade de um tamanho: para cada pixel, a camada, a rampa e o tom."""

    def __init__(self, n):
        self.n, self.px = n, {}

    def u(self, x, y):
        """O centro do pixel (x, y) no espaço de 100 unidades."""
        return (x + 0.5) * 100 / self.n, (y + 0.5) * 100 / self.n

    def pintar(self, cond, camada, rampa, tom):
        """Cada pixel em que cond(ux, uy, x, y) vale: tom pode ser um número ou uma função (ux, uy, x, y)."""
        for y in range(self.n):
            for x in range(self.n):
                ux, uy = self.u(x, y)
                if cond(ux, uy, x, y):
                    t = tom(ux, uy, x, y) if callable(tom) else tom
                    if t is not None:
                        self.px[(x, y)] = (camada, rampa, max(0, min(len(rampa) - 1, t)))

    def ajustar(self, ajustes):
        for (x, y), v in ajustes.items():
            if v is None: self.px.pop((x, y), None)
            else: self.px[(x, y)] = v

    def contornar(self, separar=()):
        """O contorno de 1 px pelos lados; e, onde uma camada de `separar` (a da frente) encosta numa de trás, a linha
        escura que separa as duas peças."""
        cheio = dict(self.px)
        for (x, y) in cheio:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if p not in cheio and 0 <= p[0] < self.n and 0 <= p[1] < self.n:
                    self.px[p] = ("contorno", None, 0)
        for frente, tras in separar:
            for (x, y), (c, _, _) in cheio.items():
                if c not in tras: continue
                if any(cheio.get((x + dx, y + dy), ("",))[0] in frente for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    self.px[(x, y)] = ("contorno", None, 0)

    def camadas(self):
        out = {}
        for (x, y), (c, rampa, t) in self.px.items():
            out.setdefault(c, {})[(x, y)] = CONTORNO if c == "contorno" else rampa[t]
        return out


# --- o gibão ---------------------------------------------------------------------------------------------------------
# De frente, sem mangas: a pala dos ombros costurada sobre o corpo, a gola aberta mostrando o avesso das costas, o
# fechamento da frente amarrado com cordão, a cintura costurada e a saia em quatro abas. Bordas de tira mais escura
# nas cavas, na gola, na frente e na barra.
CORPO = [(41, 14), (30, 12), (28, 15), (28, 24), (27, 31), (25, 36), (21, 40), (22, 48), (25, 60), (22, 72),
         (19, 85), (34, 88), (47, 89), (50, 82), (53, 89), (66, 88), (81, 85), (78, 72), (75, 60), (78, 48),
         (79, 40), (75, 36), (73, 31), (72, 24), (72, 15), (70, 12), (59, 14), (55, 19), (50, 20), (45, 19)]
GOLA = [(41, 14), (59, 14), (56, 22), (52, 29), (50, 31), (48, 29), (44, 22)]   # o decote em V (dentro, o avesso)
CAVA_E = [(28, 15), (28, 24), (27, 31), (25, 36), (21, 40)]          # a cava esquerda (para a borda)
CAVA_D = [(72, 15), (72, 24), (73, 31), (75, 36), (79, 40)]
GOLA_FRENTE = [(41, 14), (44, 22), (48, 29), (50, 31), (52, 29), (56, 22), (59, 14)]
BARRA = [[(19, 85), (34, 88), (47, 89), (50, 82), (53, 89), (66, 88), (81, 85)]]

# cordao: "olhos" (ilhós dos dois lados da fenda e o cordão em X entre eles) ou "zigue" (o cordão em zigue-zague
# dentro da fenda, um traço só); desgaste: os pixels do couro raspado na aba da direita, com o tom.
MEDIDAS_GIBAO = {
    64: dict(borda=2.4, pala=27, cintura=61, laco=(32, 58), abas=(36, 50, 64), corte_aba=74, costura=True,
             desgaste={(41, 49): 1, (42, 49): 0, (42, 50): 0, (43, 50): 0, (44, 51): 0}, cordao="olhos", ilhoses=6,
             pala_inteira=False),
    48: dict(borda=2.8, pala=27, cintura=61, laco=(32, 58), abas=(36, 50, 64), corte_aba=75, costura=True,
             desgaste={(31, 37): 1, (32, 37): 0, (32, 38): 0}, cordao="olhos", ilhoses=4, pala_inteira=False),
    40: dict(borda=3.0, pala=28, cintura=61, laco=(32, 57), abas=(50,), corte_aba=76, costura=False,
             desgaste={}, cordao="zigue", pala_inteira=True),
    32: dict(borda=3.2, pala=28, cintura=61, laco=(32, 56), abas=(50,), corte_aba=76, costura=False,
             desgaste={}, cordao="zigue", pala_inteira=True),
}


def perto_da_linha(pts, ux, uy, d):
    """Distância de (ux, uy) até a poligonal pts é menor que d?"""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        vx, vy = x2 - x1, y2 - y1
        t = max(0, min(1, ((ux - x1) * vx + (uy - y1) * vy) / (vx * vx + vy * vy)))
        if (ux - x1 - t * vx) ** 2 + (uy - y1 - t * vy) ** 2 < d * d:
            return True
    return False


def gibao(n):
    m, d = MEDIDAS_GIBAO[n], Desenho(n)
    b = m["borda"]
    corpo = lambda ux, uy, x, y: dentro(CORPO, ux, uy) and not dentro(GOLA, ux, uy)

    def tom_corpo(ux, uy, x, y):
        # o tronco em faixas verticais: aceso à esquerda, na sombra à direita; o peito esquerdo um degrau acima
        t = 5 if ux < 36 else 4 if ux < 62 else 3 if ux < 71 else 2
        if 30 <= uy < 46 and 28 <= ux < 47: t += 1                         # o plano do peito, virado para a luz
        if uy >= m["cintura"]:                                             # a saia: um degrau abaixo, aba por aba
            t -= 1
        return t

    d.pintar(corpo, "corpo", COURO, tom_corpo)
    # a pala dos ombros: uma peça por cima, mais clara em cima (o ombro recebe a luz de frente)
    d.pintar(lambda ux, uy, x, y: corpo(ux, uy, x, y) and uy < m["pala"], "pala", COURO,
             lambda ux, uy, x, y: (6 if ux < 40 else 5 if ux < 58 else 3) if uy < m["pala"] - 4 or m["pala_inteira"] else
             (5 if ux < 40 else 4 if ux < 58 else 3))
    # a sombra da pala sobre o corpo (uma linha) e a da cintura sobre a saia
    d.pintar(lambda ux, uy, x, y: corpo(ux, uy, x, y) and m["pala"] <= uy < m["pala"] + 100 / n, "corpo", COURO,
             lambda ux, uy, x, y: (3 if ux < 50 else 1))
    d.pintar(lambda ux, uy, x, y: corpo(ux, uy, x, y) and m["cintura"] <= uy < m["cintura"] + 100 / n, "abas", BORDA,
             lambda ux, uy, x, y: 2 if ux < 50 else 1)
    # as abas da saia: cada uma com a borda da esquerda acesa; o corte entre elas, escuro
    cortes = m["abas"]
    def tom_aba(ux, uy, x, y):
        t = 4 if ux < 36 else 3 if ux < 62 else 2
        for c in (20,) + cortes:
            if c <= ux < c + 100 / n * 1.01: t += 1                       # a beira acesa de cada aba
        return t
    d.pintar(lambda ux, uy, x, y: corpo(ux, uy, x, y) and uy >= m["cintura"] + 100 / n, "abas", COURO, tom_aba)
    d.pintar(lambda ux, uy, x, y: corpo(ux, uy, x, y) and uy >= m["corte_aba"] and
             any(abs(ux - c) < 50 / n for c in cortes), "abas", BORDA, 0)
    # o avesso das costas, visto pela gola; a borda de cima dela é a gola das costas, acesa
    d.pintar(lambda ux, uy, x, y: dentro(GOLA, ux, uy) and dentro(CORPO, ux, uy), "forro", FORRO,
             lambda ux, uy, x, y: 2 if uy < 20 + 100 / n * 1.2 else (1 if ux < 50 else 0))
    # as bordas de tira: cavas, gola (a frente dela), barra
    def eh_borda(ux, uy, x, y):
        if not corpo(ux, uy, x, y): return False
        return any(perto_da_linha(l, ux, uy, b) for l in (CAVA_E, CAVA_D, GOLA_FRENTE, *BARRA))
    d.pintar(eh_borda, "bordas", BORDA, lambda ux, uy, x, y: 3 if ux < 50 else 1)
    # o fechamento: a fenda da frente (do decote à barra) e o cordão cruzado de ilhós a ilhós até a cintura
    fenda = lambda ux, uy, x, y: corpo(ux, uy, x, y) and abs(ux - 50) < 50 / n * 1.01 and uy > 30
    d.pintar(fenda, "fecho", FORRO, 0)
    l0, l1 = m["laco"]
    xe, xd = n // 2 - 1, n // 2                                            # as duas colunas da fenda
    if m["cordao"] == "olhos":
        passo = (l1 - l0) / m["ilhoses"]
        for k in range(m["ilhoses"] + 1):
            yy = int((l0 + k * passo) * n / 100)
            for xx in (xe - 1, xd + 1):                                    # os ilhós dos dois lados da fenda
                d.px[(xx, yy)] = ("fecho", BORDA, 0)
            if k < m["ilhoses"]:                                           # o cordão em X entre um par e o próximo
                y2 = int((l0 + (k + 1) * passo) * n / 100)
                meio = (yy + y2) // 2
                d.px[(xe, meio)] = ("fecho", CORDAO, 2)
                d.px[(xd, meio)] = ("fecho", CORDAO, 1)
                if y2 - yy >= 4:
                    d.px[(xe, meio - 1)] = ("fecho", CORDAO, 1); d.px[(xd, meio + 1)] = ("fecho", CORDAO, 0)
    else:
        # o cordão num traço só: um pixel por linha, alternando as duas colunas da fenda (os pixels se tocam na
        # diagonal); claro do lado aceso, médio do lado da sombra
        for k, yy in enumerate(range(int(l0 * n / 100) + 1, int(l1 * n / 100))):
            d.px[(xe if k % 2 == 0 else xd, yy)] = ("fecho", CORDAO, 2 if k % 2 == 0 else 1)
    if m["costura"]:
        # a costura da pala e a da cintura: pontos de linha clara, um sim um não, só nas faixas acesas
        for x in range(n):
            for uy0, cam in ((m["pala"], "pala"), (m["cintura"], "abas")):
                y = int(uy0 * n / 100) - 1
                if (x, y) in d.px and d.px[(x, y)][0] in ("pala", "abas", "corpo") and x % 2 == 0 and x < n * 0.47:
                    d.px[(x, y)] = ("costuras", COURO, 6 if cam == "pala" else 5)
    # o couro raspado na aba da direita (onde a mão e o arco batem)
    for (x, y), t in m["desgaste"].items():
        if (x, y) in d.px: d.px[(x, y)] = ("costuras", GASTO, t)
    d.ajustar(AJUSTES_GIBAO.get(n, {}))
    d.contornar()
    return d


# --- as botas ------------------------------------------------------------------------------------------------------
# Um par de perfil, a bico para a esquerda: a da frente inteira; a de trás deslocada para cima e para a direita, com o
# cano, o calcanhar e a sola aparecendo. Cano alto com o topo dobrado (o avesso de camurça, mais claro e fosco),
# tornozelo com a dobra do couro, peito do pé aceso, sola grossa com salto, uma tira com fivela no tornozelo.
BOTA_F = [(33, 8), (62, 8), (63, 22), (60, 24), (59, 34), (58, 48), (57, 62), (60, 70), (61, 78), (61, 88),
          (13, 88), (11, 84), (12, 79), (16, 74), (24, 69), (32, 65), (38, 60), (38, 45), (37, 30), (36, 24),
          (32, 22)]
DESLOCA = (15, -6)
BAIXA = {64: 3, 48: 2, 40: 2, 32: 1}   # o par pronto desce esses pixels: a bota de trás não encosta no topo

# fivela: o canto da fivela (unidades); furo, brilho e desgaste: pixels antes de o par descer (BAIXA); vincos: as
# dobras do tornozelo (segmentos em unidades) e se cada uma ganha a linha clara em cima
MEDIDAS_BOTA = {
    64: dict(dobra=22, sola=83.5, salto_x=47, tira=(55, 61), fivela=(40, 55), furo=[(27, 36), (27, 37)],
             vincos=[((33, 64), (40, 66)), ((29, 67), (37, 69))], vinco_luz=True,
             brilho=[(9, 47), (10, 47), (10, 46), (25, 14), (25, 15), (25, 16)],
             desgaste=[(12, 50), (13, 50), (13, 51), (12, 51)]),
    48: dict(dobra=22, sola=83, salto_x=47, tira=(55, 61), fivela=(40, 55), furo=[(20, 27)],
             vincos=[((33, 64), (40, 66)), ((29, 67), (37, 69))], vinco_luz=True,
             brilho=[(6, 35), (7, 35), (7, 34), (19, 10), (19, 11), (19, 12)],
             desgaste=[(9, 38), (10, 38)]),
    40: dict(dobra=22, sola=82.5, salto_x=47, tira=(55, 61), fivela=(39, 55), furo=[],
             vincos=[((32, 65), (40, 67))], vinco_luz=False,
             brilho=[(5, 29), (15, 9), (15, 10)], desgaste=[]),
    32: dict(dobra=22, sola=82, salto_x=47, tira=(55, 61), fivela=(39, 55), furo=[],
             vincos=[((32, 65), (40, 67))], vinco_luz=False,
             brilho=[(5, 23), (12, 7), (12, 8)], desgaste=[]),
}


def uma_bota(d, m, dx, dy, nome, escurecer):
    n = d.n
    pol = [(x + dx, y + dy) for x, y in BOTA_F]
    dent = lambda ux, uy: dentro(pol, ux, uy)
    lx, ly = lambda ux: ux - dx, lambda uy: uy - dy                       # de volta às medidas da bota da frente

    def tom(ux, uy, x, y):
        X, Y = lx(ux), ly(uy)
        if Y < 64:   # o cano: um cilindro em três planos
            t = 5 if X < 43 else 4 if X < 51 else 3 if X < 56 else 2
        else:        # o pé: o peito virado para cima, aceso; mais baixo, a lateral
            topo = 64 + (36 - X) * 0.45 if X < 36 else 64
            t = 5 if Y < topo + 6 else 4 if Y < topo + 12 else 3
            if X > 50: t = min(t, 3)
        return t - escurecer

    d.pintar(lambda ux, uy, x, y: dent(ux, uy), nome, BOTA, tom)
    # o cano dobrado: o avesso de camurça, mais claro e fosco; a beira de cima é a dobra, a de baixo faz sombra
    d.pintar(lambda ux, uy, x, y: dent(ux, uy) and ly(uy) < m["dobra"], nome + "_dobra", DOBRA,
             lambda ux, uy, x, y: (4 if lx(ux) < 44 else 3 if lx(ux) < 53 else 2) - escurecer)
    d.pintar(lambda ux, uy, x, y: dent(ux, uy) and m["dobra"] <= ly(uy) < m["dobra"] + 100 / n, nome, BOTA,
             lambda ux, uy, x, y: 2 - escurecer)
    # a boca do cano: o escuro de dentro, numa elipse vista de cima
    d.pintar(lambda ux, uy, x, y: ((lx(ux) - 47.5) / 12) ** 2 + ((ly(uy) - 10.5) / 2.4) ** 2 < 1, nome + "_dobra", FORRO,
             lambda ux, uy, x, y: 1 if lx(ux) < 48 else 0)
    # a sola e o salto
    d.pintar(lambda ux, uy, x, y: dent(ux, uy) and ly(uy) >= m["sola"], nome + "_sola", SOLA,
             lambda ux, uy, x, y: (2 if ly(uy) < m["sola"] + 100 / n else 1) - escurecer // 2)
    d.pintar(lambda ux, uy, x, y: dent(ux, uy) and lx(ux) >= m["salto_x"] and ly(uy) >= m["sola"] - 4, nome + "_sola",
             SOLA, lambda ux, uy, x, y: (3 if ly(uy) < m["sola"] - 4 + 100 / n else 1) - escurecer // 2)
    return pol


def bota(n):
    m, d = MEDIDAS_BOTA[n], Desenho(n)
    dx, dy = DESLOCA
    uma_bota(d, m, dx, dy, "tras", 1)
    tras = dict(d.px)
    d.px = {}
    uma_bota(d, m, 0, 0, "frente", 0)
    front = dict(d.px)
    d.px = {**{p: v for p, v in tras.items() if p not in front}, **front}
    # a tira do tornozelo, com a fivela de bronze do lado de fora
    t0, t1 = m["tira"]
    d.pintar(lambda ux, uy, x, y: dentro(BOTA_F, ux, uy) and t0 <= uy + (ux - 36) * 0.12 < t1 and ux > 36, "tira",
             BORDA, lambda ux, uy, x, y: 3 if ux < 45 else 2 if ux < 54 else 1)
    fx, fy = m["fivela"]
    d.pintar(lambda ux, uy, x, y: fx <= ux < fx + 7 and fy - 1 <= uy < fy + 6, "tira", FIVELA,
             lambda ux, uy, x, y: 3 if ux < fx + 2.5 and uy < fy + 2 else 2 if ux < fx + 3.5 else 1)
    for p in m["furo"]:
        d.px[p] = ("tira", FIVELA, 0)                                      # o furo da fivela
    if m["vincos"]:
        # a dobra do couro no tornozelo: uma linha (duas nos maiores) no peito do pé, logo abaixo da tira
        for (x1, y1), (x2, y2) in m["vincos"]:
            for k in range(12):
                ux, uy = x1 + (x2 - x1) * k / 11, y1 + (y2 - y1) * k / 11
                p = (int(ux * n / 100), int(uy * n / 100))
                if p in d.px and d.px[p][0] == "frente": d.px[p] = ("detalhes", BOTA, 2)
                q = (p[0], p[1] - 1)
                if m["vinco_luz"] and q in d.px and d.px[q][0] == "frente": d.px[q] = ("detalhes", BOTA, 6)
    # o reflexo discreto do couro: no bico e no cano, do lado da luz
    for p in m["brilho"]:
        if p in d.px and d.px[p][0] in ("frente",): d.px[p] = ("detalhes", BOTA, 6)
    # o bico raspado (fosco, sem brilho)
    for p in m["desgaste"]:
        if p in d.px and d.px[p][0] == "frente": d.px[p] = ("detalhes", GASTO, 0)
    d.px = {(x, y + BAIXA[n]): v for (x, y), v in d.px.items() if y + BAIXA[n] < n}
    d.ajustar(AJUSTES_BOTA.get(n, {}))
    d.contornar(separar=[({"frente", "frente_dobra", "frente_sola", "tira", "detalhes"},
                          {"tras", "tras_dobra", "tras_sola"})])
    return d


AJUSTES_GIBAO = {64: {}, 48: {}, 32: {},
                 40: {(8, 16): None, (31, 16): None}}   # no 40, a axila virava uma ponta solta de 1 px
AJUSTES_BOTA = {64: {}, 48: {}, 40: {}, 32: {}}

PECAS = {"gibao": (gibao, ["forro", "corpo", "abas", "pala", "bordas", "fecho", "costuras", "contorno"]),
         "bota": (bota, ["tras", "tras_dobra", "tras_sola", "frente", "frente_dobra", "frente_sola", "tira",
                         "detalhes", "contorno"])}


def gravar(peca, n, pasta):
    fazer, ordem = PECAS[peca]
    cam = fazer(n).camadas()
    pasta.mkdir(parents=True, exist_ok=True)
    previa = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    for c in ordem:
        px = cam.get(c, {})
        texto = ";".join(f"{x},{y},{k}" for (x, y), k in sorted(px.items()))
        (pasta / f"{c}.txt").write_text(texto)
        (pasta / f"{c}.lua").write_text(f'return "{texto}"\n')
        for (x, y), k in px.items():
            previa.putpixel((x, y), tuple(int(k[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    previa.save(pasta / "previa.png")
    (pasta / "camadas.txt").write_text(",".join(ordem))
    cores = {k for v in cam.values() for k in v.values()}
    return previa.getbbox(), sum(len(v) for v in cam.values()), len(cores)


if __name__ == "__main__":
    saida = pathlib.Path(sys.argv[1])
    pecas = [a for a in sys.argv[2:] if a in PECAS] or list(PECAS)
    lados = [int(a) for a in sys.argv[2:] if a.isdigit()] or [32, 40, 48, 64]
    for p in pecas:
        for n in lados:
            print(p, n, *gravar(p, n, saida / f"{p}-{n}"))
