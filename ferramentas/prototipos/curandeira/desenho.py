"""A cabana da curandeira do Vau, candidata A: o interior desenhado na linguagem dos ambientes do jogo (a forja H2, a
capela, a prisão da Ilse): os materiais em dois ou três tons chapados, os objetos lidos pela silhueta e pelo valor,
quase sem contorno preto, e a luz feita por cima (o halo quente do fogão e da lamparina, o frio da porta, a sala
escurecendo em degraus pontilhados longe deles).

A composição vem da referência do Jean (`ferramentas/arte/referencias/cenarios internos/A herbalista e o almofariz.png`),
só como composição: a porta fria à esquerda, a pia com os panos, as ervas secando numa vara, a bancada no meio com o
almofariz e quem trabalha na ponta dela, as prateleiras de potes, o fogão baixo com a panela e a coifa, a passagem para
o quarto dos fundos com a cortina, o armário de potes à direita. Nada vem da redução da imagem: cada coisa é desenhada
aqui, na grade de 320×96.

Escala: Marta (~1,65 m) tem 52 px dos pés ao alto do lenço; a bancada, ~85 cm, tem o tampo 27 px acima do chão; o
almofariz, 5 px. As camadas: `fundo()` (parado), `fogo(i)` (4 quadros), `vapor(i, forte)` (4 quadros), `baldes()` (a
noite da água escura) e `frente()` (as silhuetas de
baixo, por cima de tudo)."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "hud", "forja", "h2"))
from tela_h2 import Tela  # noqa: E402  (a mesma camada de pixels das fontes da forja)

import botica  # noqa: E402

QW, QH = 320, 96
P = 73       # a linha do chão (a parede encontra o chão)
PES = 82     # onde pisam a figura e a bancada
TAMPO = 55   # o tampo da bancada
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def pont(x, y, n):
    return BAYER[(y & 3) * 4 + (x & 3)] < n


C = {
    # a parede: o reboco em cima, a pedra embaixo (o rodapé de pedra que segura a umidade)
    "reboco": "#332d27", "rebocoLuz": "#3f3830", "rebocoSombra": "#26211c", "racha": "#221d19",
    "parede": "#211e1c", "junta": "#171513", "pedra": "#2d2926", "pedraLuz": "#47413b", "pedraSombra": "#151311",
    # a madeira
    "madeira": "#3a2a1c", "madeiraMeio": "#4a3624", "madeiraLuz": "#5e4632", "madeiraEsc": "#1c140d",
    # o chão de lajes
    "chao": "#29251f", "chaoLuz": "#3d362d", "chaoJunta": "#1a1714",
    # o dia lá fora (frio, sem a vila: só a luz)
    "ceuAlto": "#c4d0d8", "ceu": "#9eb0be", "neve": "#d2dbe1", "neveSombra": "#a6b4be", "longe": "#7d8d9a",
    # o ferro e a pedra do fogão
    "ferro": "#3a3c42", "ferroLuz": "#5e6068", "ferroBrilho": "#9a9ca6", "ferroEsc": "#1e1f24",
    "fogao": "#3a3530", "fogaoLuz": "#56504a", "fogaoJunta": "#25211d", "fuligem": "#141213",
    # o pano e o linho
    "linho": "#a89c84", "linhoLuz": "#c8bea6", "linhoSombra": "#7e735f", "cortina": "#8e8470", "cortinaLuz": "#a89e88",
    "cortinaSombra": "#6a6152",
    # as ervas (sem neon: verdes, ocres e um lilás apagado)
    "erva": "#3e4c26", "ervaLuz": "#5a6a32", "ervaEsc": "#28321a",
    "ocre": "#7a6228", "ocreLuz": "#9e8236", "ocreEsc": "#4e3e1a",
    "lilas": "#4e4058", "lilasLuz": "#6a5876", "lilasEsc": "#33293a",
    "palha": "#6e5a34", "palhaLuz": "#8e7646", "palhaEsc": "#45381f",
    # os maços secando (as cores de planta seca: o verde acinzentado, o roxo apagado, o branco do alho, o vermelho da
    # baga, o creme da flor)
    "salvia": "#56604a", "salviaLuz": "#76825e", "salviaEsc": "#373d2e", "salviaTalo": "#4c4630",
    "lavanda": "#5a4868", "lavandaLuz": "#7a6690", "lavandaEsc": "#3a2e46",
    "lavandaHaste": "#55553a", "lavandaHasteEsc": "#3a3a26",
    "alho": "#a89e88", "alhoLuz": "#cec6ae", "alhoEsc": "#6e6656",
    "galho": "#4a3626", "folha": "#3a4628", "folhaLuz": "#566238",
    "camomilaTalo": "#5e5c38", "flor": "#b4aa84", "florLuz": "#d4caa4", "florMiolo": "#b08a2e",
    "barbanteLuz": "#8e826a",
    # o barro, o vidro e a pedra do almofariz
    "barro": "#6a4230", "barroLuz": "#8a5a3c", "barroEsc": "#43281c",
    "vidroVerde": "#2c4030", "vidroVerdeLuz": "#4a6a4e", "vidroEsc": "#1e2832", "vidroEscLuz": "#3a4e5e",
    "almofariz": "#5c5a56", "almofarizLuz": "#7c7a74", "almofarizEsc": "#3a3936",
    "rolha": "#7a5e3e",
    # a água
    "agua": "#1e2e36", "aguaLuz": "#3a5662", "aguaEscura": "#141615", "aguaEscuraLuz": "#2a2a24",
    # o fogo e as luzes
    "brasa": "#c8501a", "chama": "#ffcc66", "chamaFora": "#e8782a", "chamaMiolo": "#fff2c4",
    "vulto": "#09090b", "vultoLuz": "#18181c",
}


C.update(botica.C)  # os objetos da botica (botica.py)


class Pincel:
    def __init__(self, t):
        self.t = t

    def __call__(self, x, y, w=1, h=1, cor=None):
        if cor:
            self.t.ret(int(round(x)), int(round(y)), w, h, C.get(cor, cor))

    def p(self, x, y, cor):
        self(x, y, 1, 1, cor)

    def linha(self, x0, y0, x1, y1, cor):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), cor)


# ---------------------------------------------------------------- a sala
def sala(px):
    """O reboco em cima (calmo, umas rachas), o rodapé de pedra em blocos, o teto de vigas e o chão de lajes."""
    px(0, 0, QW, 44, "reboco")
    for x, y, w in [(52, 14, 9), (118, 33, 7), (176, 12, 6), (300, 30, 8), (150, 20, 5)]:  # o reboco gasto
        px(x, y, w, 1, "rebocoLuz")
    for x, y in [(66, 20), (200, 38), (284, 8)]:  # as rachas, curtas
        px.linha(x, y, x + 2, y + 4, "racha")
        px.p(x + 3, y + 5, "racha")
    px(0, 43, QW, 1, "rebocoSombra")
    # o rodapé de pedra: fiadas de 6, juntas desencontradas, a aresta de cima de umas pedras acesa
    px(0, 44, QW, P - 44, "parede")
    px(0, 44, QW, 1, "pedraLuz")
    for y in range(49, P, 6):
        for x in range(((y // 6) % 2) * 8 - 16, QW, 16):
            px(x, y, 16, 1, "junta")
            px(x, y, 1, 6, "junta")
    for x, y in [(18, 50), (90, 56), (170, 62), (250, 50), (306, 62), (128, 62)]:
        px(x + 1, y, 14, 1, "pedra")
    # o teto: a viga grande e a sombra embaixo
    px(0, 0, QW, 4, "madeiraEsc")
    px(0, 3, QW, 1, "madeira")
    px(0, 4, QW, 1, "rebocoSombra")
    # o chão de lajes (as fiadas crescem para a frente)
    px(0, P, QW, QH - P, "chao")
    px(0, P, QW, 1, "chaoLuz")
    y, i = P + 4, 0
    while y < QH:
        px(0, y, QW, 1, "chaoJunta")
        if y + 1 < QH:
            px(0, y + 1, QW, 1, "chaoLuz")
        passo = 18 + i * 4
        for x in range((i * 13) % passo, QW, passo):
            px(x, y - (4 + i), 1, 4 + i, "chaoJunta")
        y += 5 + i
        i += 1


def esteios(px):
    """Os esteios de madeira: a beira esquerda, o do meio da parede (entre a pia e as ervas) e o da direita (entre o
    fogão e a passagem), cada um com a base de pedra e a mão-francesa até a viga."""
    px(0, 4, 6, P - 4, "madeira")
    px(5, 4, 1, P - 4, "madeiraEsc")
    px(0, 4, 1, P - 4, "madeiraLuz")
    for x0 in (76, 258):
        px(x0, 0, 7, P + 2, "madeira")
        px(x0, 0, 1, P + 2, "madeiraLuz")
        px(x0 + 5, 0, 2, P + 2, "madeiraEsc")
        px(x0 + 3, 22, 1, 6, "madeiraEsc")  # a fenda
        px(x0 - 1, P, 9, 3, "pedra")
        px(x0 - 1, P, 9, 1, "pedraLuz")
        for i in range(8):  # a mão-francesa da direita, do esteio até a viga
            px(x0 + 7 + i, 12 - i, 2, 2, "madeira")
            px(x0 + 8 + i, 13 - i, 1, 1, "madeiraEsc")


# ---------------------------------------------------------------- a porta, à esquerda: a luz fria
def porta(px):
    """A porta aberta para a rua: só a luz de fora (o céu claro, o chão de neve), sem desenhar a vila; o batente e a
    verga de madeira e a folha aberta para dentro, encostada na parede."""
    x0, x1, y0 = 15, 35, 14
    for y in range(y0, P):
        t = (y - y0) / (P - y0)
        for x in range(x0, x1):
            px.p(x, y, "ceu" if pont(x, y, int(t * 26)) else "ceuAlto")
    px(x0, 50, x1 - x0, 2, "longe")      # o muro baixo do outro lado da rua, apagado na luz
    px(x0, 52, x1 - x0, P - 52, "neve")
    for x in range(x0, x1):
        if pont(x, 53, 6):
            px.p(x, 53, "neveSombra")
    px(x0, P - 2, x1 - x0, 2, "neveSombra")  # a soleira
    for xx in (10, 35):  # o batente
        px(xx, y0 - 3, 5, P - y0 + 3, "madeira")
        px(xx, y0 - 3, 1, P - y0 + 3, "madeiraLuz")
        px(xx + 4, y0 - 3, 1, P - y0 + 3, "madeiraEsc")
    px(8, y0 - 5, 34, 3, "madeira")
    px(8, y0 - 5, 34, 1, "madeiraLuz")
    px(8, y0 - 3, 34, 1, "madeiraEsc")
    # a folha aberta para dentro, vista de quina, encostada na parede (as tábuas e a ferragem)
    px(6, y0, 4, P - y0, "madeiraMeio")
    px(6, y0, 1, P - y0, "madeiraLuz")
    for yy in (24, 58):
        px(6, yy, 4, 2, "ferro")


def pia(px):
    """A pia de pedra num suporte de madeira, com água, o pano pendurado num pino, os panos dobrados na prateleira de
    baixo e o balde de água no chão."""
    # o pano no pino da parede, ao lado da porta
    px(44, 26, 2, 2, "madeiraEsc")
    px(42, 28, 6, 12, "linho")
    px(42, 28, 1, 12, "linhoLuz")
    px(47, 28, 1, 12, "linhoSombra")
    px(43, 40, 4, 1, "linho")
    px(44, 33, 3, 1, "linhoSombra")  # a dobra
    # o suporte: as pernas, a prateleira de baixo
    for xx in (50, 70):
        px(xx, 55, 3, PES - 55, "madeira")
        px(xx, 55, 1, PES - 55, "madeiraLuz")
        px(xx + 2, 55, 1, PES - 55, "madeiraEsc")
    px(49, 70, 25, 3, "madeiraMeio")
    px(49, 70, 25, 1, "madeiraLuz")
    # os panos dobrados na prateleira
    px(52, 64, 14, 6, "linho")
    px(52, 64, 14, 1, "linhoLuz")
    px(52, 67, 14, 1, "linhoSombra")
    # a pia: a pedra cavada, a borda de cima acesa, a água dentro
    px(47, 50, 29, 6, "pedra")
    px(47, 50, 29, 1, "pedraLuz")
    px(47, 55, 29, 1, "pedraSombra")
    px(49, 51, 25, 2, "agua")
    px(51, 51, 8, 1, "aguaLuz")
    # o pano jogado na borda da pia, caindo pela frente
    px(64, 49, 7, 2, "linhoLuz")
    px(66, 51, 5, 8, "linho")
    px(70, 51, 1, 8, "linhoSombra")
    # o balde de água no chão, de aduelas com o aro de ferro
    bx, by = 56, 74
    px(bx, by, 11, PES - by, "madeira")
    px(bx, by, 1, PES - by, "madeiraLuz")
    px(bx + 10, by, 1, PES - by, "madeiraEsc")
    px(bx, by + 2, 11, 1, "ferro")
    px(bx, PES - 2, 11, 1, "ferro")
    px(bx + 1, by - 1, 9, 1, "agua")
    px(bx + 2, by - 1, 3, 1, "aguaLuz")
    px.linha(bx, by - 1, bx + 5, by - 6, "ferroEsc")  # a alça
    px.linha(bx + 5, by - 6, bx + 10, by - 1, "ferroEsc")


# ---------------------------------------------------------------- as ervas secando
# Cada maço desenhado à mão (um caractere por pixel), de cabeça para baixo como se seca: o barbante descendo da vara,
# as voltas da amarração em volta dos talos juntos e, embaixo, o que se reconhece da planta. A leitura vem da
# silhueta, não da cor: a sálvia em leque de folhas pontudas, a lavanda em hastes finas com a espiga na ponta, a
# réstia de alho em cabeças redondas presas na trança de palha, o raminho de bagas em cachos de bolinhas com duas
# folhas, a camomila em talos curtos com as flores miúdas embaixo. Comprimentos e espaços diferentes de propósito.
# Comuns a todos: "=" o barbante, "+" a volta acesa da amarração.
MACOS = [
    (90, 12, {"t": "salviaTalo", "G": "salviaLuz", "g": "salvia", "d": "salviaEsc"}, [  # a sálvia
        "....=....",
        "....=....",
        "...=+=...",
        "...tdt...",
        "...=+=...",
        "..t.d.t..",
        ".tG.d.gt.",
        "GGg.dGgd.",
        "Gg.Ggdgdd",
        ".gGg.gGd.",
        "GgG.Ggdd.",
        "G.gGg.Gd.",
        ".Gg.gGgdd",
        "..G.Gg.d.",
        "..g.g..d.",
        "....g....",
    ]),
    (101, 12, {"t": "lavandaHaste", "T": "lavandaHasteEsc", "L": "lavandaLuz", "l": "lavanda", "k": "lavandaEsc"}, [
        "...=...",  # a lavanda
        "...=...",
        "..=+=..",
        "..tTt..",
        "..=+=..",
        "..tTt..",
        ".t.T.t.",
        ".t.t.t.",
        "t..t.t.",
        "t..t..t",
        "L..t..t",
        "l.Lt..L",
        "k.lt..l",
        "l.kL..k",
        "k.ll..l",
        "..kk..k",
        "...l...",
        "...k...",
    ]),
    (110, 12, {"p": "palha", "P": "palhaEsc", "A": "alhoLuz", "a": "alho", "d": "alhoEsc"}, [  # a réstia de alho
        "....=....",
        "....=....",
        "...=+=...",
        "....pP...",
        "...pPp...",
        "..aAp....",
        ".aAAad...",
        ".aAadd...",
        "..ddpPp..",
        "....pAa..",
        "...pAAad.",
        "....aadd.",
        "...PpddP.",
        "..aAPp...",
        ".aAAad...",
        "..add....",
    ]),
    (121, 12, {"w": "galho", "R": "bagaLuz", "r": "baga", "q": "bagaEsc", "F": "folhaLuz", "f": "folha"}, [
        "...=....",  # o raminho de bagas
        "...=....",
        "..=+=...",
        "..wqw...",
        "...w....",
        "..w.w...",
        ".w..wF..",
        ".w.f.wf.",
        "RrfF.w..",
        "rqf.Rrw.",
        ".w..rqRr",
        ".Rr..qrq",
        "Rrq...q.",
        ".qr.....",
        "..q.....",
    ]),
    (131, 12, {"h": "camomilaTalo", "F": "florLuz", "f": "flor", "m": "florMiolo"}, [  # a camomila
        "....=...",
        "...=+=..",
        "...hhh..",
        "...=+=..",
        "..h.h.h.",
        ".h.h.h.h",
        "fFh.hFf.",
        "fmf.fmff",
        ".f.fFh.m",
        "...fmf.f",
        "....f...",
    ]),
]


def ervas(px):
    """A vara presa em dois ganchos na parede e os maços pendurados nela (MACOS)."""
    px(88, 9, 58, 3, "madeira")
    px(88, 9, 58, 1, "madeiraLuz")
    px(88, 11, 58, 1, "madeiraEsc")
    for xx in (90, 142):  # os ganchos
        px(xx, 6, 1, 4, "ferro")
        px(xx, 6, 2, 1, "ferro")
    for x0, y0, pal, linhas in MACOS:
        pal = dict(pal, **{"=": "barbante", "+": "barbanteLuz"})
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    px.p(x0 + dx, y0 + dy, pal[ch])
        # a laçada do barbante por cima da vara
        xb = x0 + linhas[0].index("=")
        px.p(xb, 10, "barbanteLuz")
        px.p(xb, 11, "barbante")


# ---------------------------------------------------------------- a bancada
def bancada(px):
    """A mesa de trabalho: o tampo grosso com a aresta acesa, as pernas, a travessa de baixo com o cesto de ervas, e em
    cima o alambique sobre a lamparina (botica.py), a tábua com as ervas picadas e o almofariz (a figura trabalha nele).
    O pano dobrado cai pela frente do tampo."""
    x0, x1 = 92, 158
    # as pernas e a travessa
    for xx in (94, 153):
        px(xx, TAMPO + 3, 3, PES - TAMPO - 3, "madeira")
        px(xx, TAMPO + 3, 1, PES - TAMPO - 3, "madeiraLuz")
        px(xx + 2, TAMPO + 3, 1, PES - TAMPO - 3, "madeiraEsc")
    px(96, 74, 57, 2, "madeiraMeio")
    px(96, 74, 57, 1, "madeiraLuz")
    # o cesto de vime embaixo, com as ervas por cima
    cx = 104
    px(cx, 66, 26, 8, "palha")
    px(cx, 66, 26, 1, "palhaLuz")
    for xx in range(cx + 1, cx + 26, 3):
        px(xx, 67, 1, 7, "palhaEsc")
    px(cx + 2, 63, 22, 3, "erva")
    for xx in range(cx + 2, cx + 24, 4):
        px.p(xx, 62, "ervaLuz")
        px.p(xx + 2, 63, "ervaEsc")
    # o tampo: a face de cima (vista de leve por cima), a aresta acesa e a frente
    px(x0, TAMPO - 1, x1 - x0, 2, "madeiraMeio")
    px(x0, TAMPO - 1, x1 - x0, 1, "madeiraLuz")
    px(x0, TAMPO + 1, x1 - x0, 2, "madeira")
    px(x0, TAMPO + 2, x1 - x0, 1, "madeiraEsc")
    botica.alambique(px)
    # a tábua com as ervas picadas
    px(119, 52, 15, 2, "madeiraLuz")
    px(119, 53, 15, 1, "madeiraMeio")
    for xx in range(120, 133, 2):
        px.p(xx, 51, "ervaLuz" if xx % 4 else "erva")
    px(130, 49, 1, 3, "ferroLuz")  # a faquinha
    px(130, 52, 3, 1, "madeiraEsc")
    # o pano dobrado caindo pela frente do tampo
    px(135, TAMPO - 1, 6, 2, "linhoLuz")
    px(136, TAMPO + 1, 5, 7, "linho")
    px(140, TAMPO + 1, 1, 7, "linhoSombra")
    px(136, TAMPO + 8, 4, 1, "linhoSombra")
    almofariz(px)


AL = (145, 154)  # o almofariz: da esquerda à direita (a boca)


def almofariz(px):
    """O almofariz de pedra no tampo: o lábio largo e aceso, o bojo arredondado que estreita, o pé curto."""
    a, b = AL
    y = TAMPO - 6
    px(a, y, b - a + 1, 1, "almofarizLuz")              # o lábio
    px(a + 2, y, b - a - 3, 1, "almofarizEsc")           # a boca, por dentro
    px(a + 3, y, 2, 1, "ervaEsc")                        # as ervas moídas
    for k, (m, n) in enumerate([(0, 0), (0, 0), (1, 1), (2, 2)]):
        px(a + m, y + 1 + k, b - a + 1 - m - n, 1, "almofariz")
        px(a + m, y + 1 + k, 1, 1, "almofarizLuz")
        px(b - n, y + 1 + k, 1, 1, "almofarizEsc")
    px(a + 3, y + 5, b - a - 5, 1, "almofarizEsc")       # o pé


# ---------------------------------------------------------------- as prateleiras e o fogão
def coifa(px):
    """A coifa de reboco sobre o fogão, no eixo da panela, subindo estreita até a viga (a fumaça e o vapor saem por ela)."""
    for y in range(4, 31):
        t = (y - 4) / 26
        a, b = round(234 - t * 12), round(244 + t * 12)
        px(a, y, b - a, 1, "rebocoLuz")
        px(a, y, 2, 1, "#4c443a")
        px(b - 2, y, 2, 1, "reboco")
    px(221, 30, 36, 2, "madeira")   # a cinta de madeira na boca da coifa
    px(221, 30, 36, 1, "madeiraLuz")
    px(225, 32, 28, 1, "fuligem")


FOG = (224, 252)  # o fogão: da esquerda à direita


def fogao(px):
    """O fogão baixo de pedra: o bloco com as juntas, a boca em arco com as brasas (o fogo é outra camada) e a panela de
    ferro em cima, com a borda acesa. Um feixe de lenha encostado."""
    a, b = FOG
    top = 52
    px(a, top, b - a, PES - top, "fogao")
    px(a, top, b - a, 1, "fogaoLuz")
    for y in range(top + 6, PES, 6):
        for x in range(a + ((y // 6) % 2) * 5, b, 10):
            px(x, y, 1, 6, "fogaoJunta")
        px(a, y, b - a, 1, "fogaoJunta")
    px(a, top, 1, PES - top, "fogaoLuz")
    px(b - 1, top, 1, PES - top, "fuligem")
    # a boca em arco
    for y in range(62, 79):
        meia = 7 if y > 65 else [3, 5, 6, 7][y - 62]
        px(238 - meia, y, meia * 2, 1, "fuligem")
    px(231, 78, 14, 2, "fogaoLuz")  # a soleira da boca
    # o caldeirão de ferro sobre o fogão: o bojo redondo, a boca com a borda acesa, as alças e a concha de pau
    cx, cy = 238, 46
    for y in range(41, 52):
        meia = round(10 * (1 - ((y - cy) / 6.2) ** 2) ** 0.5) if abs(y - cy) < 6.2 else 0
        meia = max(meia, 7) if y <= 43 else meia
        px(cx - meia, y, meia * 2, 1, "ferro")
        px(cx - meia, y, 1, 1, "ferroLuz")
        px(cx + meia - 2, y, 2, 1, "ferroEsc")
    px(cx - 6, 47, 3, 2, "ferroLuz")        # o brilho do bojo
    px(cx - 7, 41, 14, 1, "ferroBrilho")    # a borda
    px(cx - 6, 42, 12, 1, "ferroEsc")       # a boca, por dentro
    px(cx - 11, 44, 2, 2, "ferroEsc")       # as alças
    px(cx + 9, 44, 2, 2, "ferroEsc")
    px(cx - 3, 52, 2, 1, "ferroEsc")        # os pés
    px(cx + 2, 52, 2, 1, "ferroEsc")
    px.linha(cx + 3, 41, cx + 8, 35, "madeiraLuz")  # a concha encostada na borda
    px.linha(cx + 4, 41, cx + 9, 35, "madeira")
    # a lenha encostada ao lado
    for i, (dx, cor) in enumerate([(0, "madeira"), (3, "madeiraMeio"), (6, "madeira")]):
        px.linha(254 + dx, PES - 1, 252 + dx + i, 64, cor)
        px.linha(255 + dx, PES - 1, 253 + dx + i, 64, "madeiraEsc")


def passagem(px):
    """A passagem para o quarto dos fundos: o vão escuro, o batente e a verga, e a cortina de linho numa vara, puxada
    para um lado (atrás, só o escuro: nada de cama nem de gente)."""
    x0, x1, y0 = 271, 293, 14
    px(x0, y0, x1 - x0, P - y0, "#0e0c0b")
    px(x0, P - 6, x1 - x0, 6, "#151210")      # o chão do quarto, um tom acima
    for xx in (267, 293):
        px(xx, y0 - 3, 4, P - y0 + 3, "madeira")
        px(xx, y0 - 3, 1, P - y0 + 3, "madeiraLuz")
        px(xx + 3, y0 - 3, 1, P - y0 + 3, "madeiraEsc")
    px(265, y0 - 5, 34, 3, "madeira")
    px(265, y0 - 5, 34, 1, "madeiraLuz")
    # a vara e a cortina, franzida em pregas, puxada para a esquerda (o vão aparece à direita)
    px(270, y0 + 1, 24, 1, "ferroEsc")
    for x in range(271, 287):
        cor = "cortinaLuz" if x % 4 == 0 else "cortinaSombra" if x % 4 == 2 else "cortina"
        px(x, y0 + 2, 1, P - y0 - 4 + (x % 2), cor)
    px(286, y0 + 2, 1, P - y0 - 3, "cortinaSombra")
    px(271, P - 3, 16, 1, "cortinaSombra")


def tapete(px):
    """A esteira de palha trançada diante do fogão, no chão onde se circula."""
    for y in range(84, 90):
        for x in range(190 + (89 - y), 230 - (89 - y)):
            px.p(x, y, "palhaLuz" if (x + y) % 4 == 0 else "palha" if (x // 2 + y) % 2 else "palhaEsc")


# ---------------------------------------------------------------- a luz
LUZES = [(238, 68, 30, 1.0), (112, 47, 22, 0.75), (211, 16, 14, 0.55)]  # e a vela da botica  # o fogão, a lamparina (x, y, raio, força)


def luz(t):
    """Longe das luzes, a sala escurece em degraus pontilhados; perto, o halo quente em anéis; da porta, o frio no chão
    e no batente. A mesma luz feita por cima da forja."""
    for y in range(QH):
        for x in range(QW):
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.4)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.6)))
            frio = max(0.0, 1 - math.hypot(x - 26, (y - 70) * 2.0) / 46) if y > P - 34 else 0.0
            escuro = max(0.0, 0.6 - perto * 1.1 - frio * 0.8)
            f5 = escuro / 0.6 * 5
            n = int(f5) + (1 if pont(x, y, int((f5 % 1) * 16)) else 0)
            if n:
                t.mistura(x, y, (3, 4, 6), 0.55 * n / 5)
            for lx, ly, r, f in LUZES:
                d2 = ((x - lx) ** 2 + ((y - ly) * 1.4) ** 2) / (r * r)
                if d2 < 1:
                    al = 0.2 if d2 < 0.08 else 0.12 if d2 < 0.3 else 0.07 if d2 < 0.65 else 0.035
                    t.mistura(x, y, (255, 160, 80), al * f)
            if frio > 0 and y >= P and pont(x, y, int(frio * 8)):
                t.mistura(x, y, (190, 210, 228), 0.12)


def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    sala(px)
    porta(px)
    ervas(px)
    botica.enfiada(px)
    botica.prateleiras(px)
    coifa(px)
    botica.cranio(px)
    passagem(px)
    botica.armario(px)
    botica.protecoes(px)
    esteios(px)
    pia(px)
    fogao(px)
    bancada(px)
    tapete(px)
    luz(t)
    # a chama da lamparina debaixo do balão (depois do escuro: a luz não escurece)
    px(112, 49, 2, 2, "chamaFora")
    px(112, 49, 1, 2, "chama")
    px(211, 15, 1, 2, "chamaFora")  # a vela acesa na tábua de cima
    px.p(211, 16, "chama")
    return t


# ---------------------------------------------------------------- o fogo, o vapor, os baldes
def fogo(i):
    """As brasas e as chamas baixas na boca do fogão (4 quadros): fogo de cozinhar, pequeno."""
    t = Tela(QW, QH)
    px = Pincel(t)
    px(232, 74, 12, 4, "brasa")
    for k in range(12):
        px.p(232 + k, 74 + ((k + i) % 2), "chamaFora" if (k + i) % 3 else "brasa")
    alturas = [[4, 7, 5, 8, 6, 3], [6, 5, 8, 6, 4, 5], [3, 6, 7, 5, 8, 6], [5, 8, 4, 7, 5, 4]][i]
    for k, h in enumerate(alturas):
        x = 233 + k * 2
        px(x, 74 - h, 2, h, "chamaFora")
        px(x, 74 - h + 2, 1, max(0, h - 3), "chama")
        if h >= 7:
            px.p(x, 74 - h + 4, "chamaMiolo")
    return t


def vapor(i, forte=False):
    """O vapor saindo da panela e subindo para a coifa (4 quadros, um ciclo de 12 px que emenda): fiapos curtos de 1 px
    que sobem ondulando, claros perto da panela e apagando no alto. Na noite da água escura, a fervura forte (mais
    fiapos, mais compridos)."""
    t = Tela(QW, QH)
    n, comp = (4, 6) if forte else (2, 4)
    for k in range(n):
        x0 = 233 + k * (11 // (n - 1) if n > 1 else 0)
        cabeca = 42 - (i * 3 + k * 5) % 12          # o alto do fiapo neste quadro
        for s_ in range(comp):
            y = cabeca + s_
            if y < 31 or y > 42:
                continue
            x = x0 + (1 if ((y + k) // 2) % 2 else 0)
            t.px(x, y, (198, 196, 186) if y > 38 else (160, 158, 150) if y > 34 else (118, 116, 110))
    return t


def baldes():
    """A noite da água escura: dois baldes de água do rio junto do fogão, para ferver (Pita ferve água para os
    doentes), e a água da panela borbulhando escura."""
    t = Tela(QW, QH)
    px = Pincel(t)
    for bx in (198, 210):
        by = 72
        px(bx, by, 9, PES - by, "madeira")
        px(bx, by, 1, PES - by, "madeiraLuz")
        px(bx + 8, by, 1, PES - by, "madeiraEsc")
        px(bx, by + 2, 9, 1, "ferro")
        px(bx, PES - 2, 9, 1, "ferro")
        px(bx + 1, by - 1, 7, 1, "aguaEscura")
        px(bx + 2, by - 1, 2, 1, "aguaEscuraLuz")
    px(232, 42, 12, 1, "aguaEscura")  # a água escura na boca do caldeirão
    px(235, 42, 2, 1, "aguaEscuraLuz")
    return t


# ---------------------------------------------------------------- a frente
def frente():
    """As silhuetas de baixo: o cesto de ervas à esquerda e o jarro grande à direita."""
    t = Tela(QW, QH)
    px = Pincel(t)
    v = "vulto"
    for y in range(84, QH):  # o cesto
        px(2, y, 30, 1, v)
    for x in range(4, 30, 3):
        px.p(x, 83, v)
        px.p(x + 1, 82, v)
    px.linha(5, 84, 16, 76, v)  # a alça
    px.linha(16, 76, 28, 84, v)
    px(3, 85, 28, 1, "vultoLuz")
    for y in range(80, QH):  # o jarro
        meia = 9 * math.sqrt(max(0.0, 1 - ((y - 90) / 11) ** 2))
        px(round(308 - meia), y, round(meia * 2), 1, v)
    px(304, 76, 8, 5, v)
    px(303, 75, 10, 2, v)
    px(304, 75, 8, 1, "vultoLuz")
    return t

