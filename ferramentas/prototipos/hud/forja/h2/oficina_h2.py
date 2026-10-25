"""A oficina da forja H (a mesma da G), redesenhada na linguagem dos ambientes do jogo (a capela, a prisão da Ilse, a cidade, o
mercado): os materiais em dois ou três tons chapados (a pedra em blocos com as juntas um tom abaixo, a madeira com a
aresta acesa e o lado escuro, o ferro com o brilho de um pixel), os objetos lidos pela silhueta e pelo valor, quase
sem contorno preto, e a luz feita por cima: o halo quente da fornalha e da lanterna em anéis, o frio da porta, e a sala
escurecendo em degraus pontilhados longe delas. A composição é a da referência do Jean (a porta fria à esquerda, a
fornalha atrás, o meio para o ferreiro, o armazém e a bancada à direita, as silhuetas da frente); nada vem da redução
da imagem: cada coisa é desenhada aqui.

`fundo()` é a camada parada de trás (o ferreiro, a bigorna, a espada e o fogo vêm por cima); `frente()` são as
silhuetas de baixo, por cima de tudo."""
import math

from tela_h2 import Tela

QW, QH = 320, 96
P = 73  # a linha do chão (a parede encontra o chão)
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def pont(x, y, n):
    return BAYER[(y & 3) * 4 + (x & 3)] < n


C = {
    # a pedra e a parede (as da sacristia, um pouco mais quentes)
    "parede": "#211e1c", "junta": "#171513", "pedra": "#2d2926", "pedraLuz": "#47413b", "pedraSombra": "#151311",
    # a madeira
    "madeira": "#3a2a1c", "madeiraMeio": "#4a3624", "madeiraLuz": "#5e4632", "madeiraEsc": "#1c140d",
    # o ferro
    "ferro": "#3a3c42", "ferroLuz": "#5e6068", "ferroBrilho": "#9a9ca6", "ferroEsc": "#24252a",
    # o tijolo da fornalha e a fuligem
    "tijolo": "#4a2e22", "tijoloLuz": "#6e4430", "tijoloQuente": "#8e5634", "tijoloJunta": "#2a1a14", "fuligem": "#141213",
    # o chão
    "chao": "#29251f", "chaoLuz": "#3d362d", "chaoJunta": "#1a1714",
    # o dia lá fora (frio)
    "ceuAlto": "#c4d0d8", "ceu": "#9eb0be", "neve": "#d2dbe1", "neveSombra": "#a6b4be", "torre": "#6a7884",
    "torreEsc": "#56636e", "folha": "#3b3632", "folhaLuz": "#55504a",
    # o resto
    "couro": "#4a3020", "couroEsc": "#2a1a10", "pano": "#6a5a44", "panoEsc": "#4e4232", "papel": "#b8ae98",
    "agua": "#121e24", "aguaLuz": "#2e4652", "carvao": "#131315", "carvaoLuz": "#2a2a2e", "brasa": "#c8501a",
    "chama": "#ffcc66", "chamaFora": "#e8782a", "vidro": "#ffb85a",
    "vulto": "#09090b", "vultoLuz": "#18181c",
}


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


# ---------------------------------------------------------------- a sala: paredes, teto, chão
def sala(px):
    """A parede em blocos (fiadas de 6 px, juntas desencontradas, um tom abaixo), o teto de vigas e o chão de lajes."""
    px(0, 0, QW, P, "parede")
    for y in range(5, P, 6):
        for x in range(((y // 6) % 2) * 7 - 14, QW, 14):
            px(x, y, 14, 1, "junta")
            px(x, y, 1, 6, "junta")
    # umas pedras com a aresta de cima mais clara (não todas: a parede é calma)
    for i, (x, y) in enumerate([(22, 35), (50, 11), (64, 47), (78, 23), (144, 41), (158, 11), (186, 59), (240, 11),
                                (262, 53), (298, 29), (134, 65), (304, 65)]):
        px(x + 1, y + 1, 12, 1, "pedra")
    # o teto: a viga grande e a sombra embaixo
    px(0, 0, QW, 4, "madeiraEsc")
    px(0, 3, QW, 1, "madeira")
    px(0, 4, QW, 1, "pedraSombra")
    # o chão de lajes: fiadas que crescem para a frente, juntas desencontradas, a aresta de cima de cada fiada
    px(0, P, QW, QH - P, "chao")
    px(0, P, QW, 1, "chaoLuz")
    y, i = P + 4, 0
    while y < QH:
        px(0, y, QW, 1, "chaoJunta")
        px(0, y + 1, QW, 1, "chaoLuz") if y + 1 < QH else None
        passo = 16 + i * 4
        for x in range((i * 11) % passo, QW, passo):
            px(x, y - (4 + i), 1, 4 + i, "chaoJunta")
        y += 5 + i
        i += 1


def esteios(px):
    """A estrutura de madeira: o esteio da esquerda, o batente e a verga da porta, o esteio grande do meio com as duas
    mãos-francesas até a viga, e o caibro da direita."""
    # o esteio da esquerda, na beira
    px(0, 4, 6, P - 4, "madeira")
    px(5, 4, 1, P - 4, "madeiraEsc")
    px(0, 4, 1, P - 4, "madeiraLuz")
    # o batente da porta e a verga
    for x0 in (11, 38):
        px(x0, 10, 5, P - 10, "madeira")
        px(x0, 10, 1, P - 10, "madeiraLuz")
        px(x0 + 4, 10, 1, P - 10, "madeiraEsc")
    px(9, 7, 37, 4, "madeira")
    px(9, 7, 37, 1, "madeiraLuz")
    px(9, 10, 37, 1, "madeiraEsc")
    # o esteio grande do meio, à frente da parede, até o chão (com a base), e as mãos-francesas
    px(212, 0, 11, 82, "madeira")
    px(212, 0, 2, 82, "madeiraLuz")
    px(220, 0, 3, 82, "madeiraEsc")
    for y in (18, 41, 63):  # as fendas da madeira
        px(216, y, 1, 7, "madeiraEsc")
    px(210, 80, 15, 2, "pedra")
    px(210, 80, 15, 1, "pedraLuz")
    for i in range(12):  # as mãos-francesas: do esteio (y 16) subindo para os lados até a viga do teto (y 4)
        px(210 - i, 15 - i, 3, 2, "madeira")
        px(210 - i, 15 - i, 1, 1, "madeiraLuz")
        px(222 + i, 15 - i, 3, 2, "madeira")
        px(224 + i, 16 - i, 1, 1, "madeiraEsc")


# ---------------------------------------------------------------- a porta, à esquerda: o dia frio lá fora
def porta(px):
    x0, x1, y0 = 16, 38, 11
    for y in range(y0, P):
        t = (y - y0) / (P - y0)
        for x in range(x0, x1):
            px.p(x, y, "ceu" if pont(x, y, int(t * 30)) else "ceuAlto")
    # lá fora: a vila no frio, a torre da igreja com a cruz, os telhados baixos e a neve no chão
    px(20, 22, 5, 30, "torre")
    px(24, 22, 1, 30, "torreEsc")
    px(21, 19, 3, 3, "torre")
    px(22, 15, 1, 5, "torreEsc")
    px(21, 16, 3, 1, "torreEsc")
    px(21, 28, 2, 3, "torreEsc")  # a janela da torre
    for x, y, w in [(16, 44, 4), (25, 41, 7), (31, 46, 7)]:
        px(x, y, w, 52 - y, "torre")
        px(x, y, w, 1, "neve")
    px(x0, 52, x1 - x0, P - 52, "neve")
    for y in range(52, P, 3):
        px(x0 + (y * 5) % 9, y, 6, 1, "neveSombra")
    # a folha da porta, aberta para dentro: tábuas, as duas ferragens com os cravos
    for y in range(14, P - 1):
        a = 27 + (1 if y < 16 else 0)
        for x in range(a, 38):
            px.p(x, y, "folhaLuz" if x == a else "madeiraEsc" if (x - 27) % 4 == 3 else "folha")
    for y in (26, 52):
        px(27, y, 11, 2, "ferro")
        px(27, y, 11, 1, "ferroLuz")
        px(29, y + 1, 1, 1, "ferroBrilho")
        px(35, y + 1, 1, 1, "ferroBrilho")
    px(16, P - 1, 22, 1, "neveSombra")  # a soleira
    px(13, P, 30, 2, "pedraLuz")


# ---------------------------------------------------------------- a parede da esquerda: a prateleira, o barril, o atiçador
def parede_esquerda(px):
    # a tenaz pendurada num prego e a argola grande com os ganchos (presa por uma corrente)
    px(48, 13, 2, 2, "ferroLuz")
    px.linha(48, 15, 46, 33, "ferro")
    px.linha(49, 15, 51, 33, "ferro")
    px(45, 32, 2, 2, "ferroLuz")
    px(51, 32, 2, 2, "ferroLuz")
    for y in range(5, 10, 2):
        px(66, y, 1, 2, "ferro")
    cx, cy, r = 66, 16, 5
    for a in range(0, 360, 12):
        px.p(round(cx + math.cos(math.radians(a)) * r), round(cy + math.sin(math.radians(a)) * r), "ferroLuz" if 150 < a < 300 else "ferro")
    for gx in (61, 66, 71):
        px(gx, 21, 1, 4, "ferro")
        px(gx - 1, 24, 2, 1, "ferroLuz")
    # a prateleira com a vela e os potes
    px(50, 42, 33, 1, "madeiraLuz")
    px(50, 43, 33, 2, "madeira")
    px(52, 45, 29, 1, "pedraSombra")
    px(53, 45, 2, 2, "ferro")
    px(78, 45, 2, 2, "ferro")
    px(56, 37, 3, 5, "papel")
    px(56, 37, 1, 5, "#d8d0bc")
    px(55, 41, 5, 1, "ferro")
    for x, y, w, h, cor, luz in [(63, 37, 5, 5, "#4a4038", "#6a5e50"), (69, 39, 4, 3, "couro", "#6a4a30"), (74, 36, 6, 6, "#3e4448", "#5a6268")]:
        px(x, y, w, h, cor)
        px(x, y, w, 1, luz)
        px(x + 1, y - 1, w - 2, 1, cor)
    # o barril com a ferragem em cima (um bloco de ferro para dobrar), as aduelas e os aros
    bx, by, bw = 49, 57, 18
    px(bx + 1, by, bw - 2, 1, "madeiraLuz")
    for y in range(by + 1, P):
        for x in range(bx, bx + bw):
            px.p(x, y, "madeiraEsc" if (x - bx) % 4 == 3 else "madeiraMeio" if x - bx < 5 else "madeira")
    for y in (60, 68):
        px(bx, y, bw, 1, "ferro")
        px(bx, y, 6, 1, "ferroLuz")
    px(bx + 4, by - 5, 9, 5, "ferro")
    px(bx + 4, by - 5, 9, 1, "ferroLuz")
    px(bx + 12, by - 4, 1, 4, "ferroEsc")
    # o atiçador e a pá, de pé, encostados
    px(72, 52, 1, P - 52, "ferro")
    px(71, 51, 3, 1, "ferroLuz")
    px(76, 54, 1, P - 54, "madeira")
    px(75, 69, 3, 4, "ferro")


# ---------------------------------------------------------------- a fornalha
BOCA = (100, 123, 37, 55)  # a boca do arco por dentro: x0, x1, o alto do arco, o leito


def dentro_da_boca(x, y):
    x0, x1, yt, yl = BOCA
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    if y < yt + r * 0.55:
        return ((x + 0.5 - cx) / r) ** 2 + ((y + 0.5 - (yt + r * 0.55)) / (r * 0.55)) ** 2 <= 1
    return x0 <= x <= x1 and y <= yl


def fornalha(px):
    """A chaminé, a coifa de ferro com a borda rebitada, a fornalha de tijolo com o arco aceso, o parapeito e a base;
    a fuligem em cima da boca; o carvão na tina ao lado e as tenazes num balde."""
    # tudo no eixo da boca (x 111,5): a chaminé, a coifa e a borda
    eixo = 111.5
    # a chaminé, de pedra escura
    px(107, 0, 10, 9, "pedra")
    px(107, 0, 1, 9, "pedraLuz")
    px(116, 0, 1, 9, "pedraSombra")
    for y in (2, 5):
        px(108, y, 8, 1, "junta")
    # a coifa: o trapézio de ferro, simétrico, mais claro embaixo (a luz do fogo), as emendas rebitadas
    for y in range(8, 24):
        t = (y - 8) / 15
        meia = 6 + 13.5 * t
        a, b = round(eixo - meia), round(eixo + meia)
        px(a, y, b - a, 1, "ferroEsc" if t < 0.3 else "ferro")
        px(a, y, 1, 1, "ferroLuz")
        px(b - 1, y, 1, 1, "ferroEsc")
    for y in (13, 18):
        meia = 6 + 13.5 * (y - 8) / 15
        n = int(meia * 2 // 4)
        for k in range(n + 1):
            px(round(eixo - meia + 2 + k * (2 * meia - 4) / n), y, 1, 1, "ferroLuz")
    # a borda da coifa: a faixa de ferro com a aresta acesa embaixo
    px(91, 24, 41, 6, "ferroEsc")
    px(91, 24, 41, 1, "ferroLuz")
    px(91, 24, 1, 6, "ferroLuz")
    px(91, 29, 41, 1, "tijoloQuente")
    for x in range(94, 131, 6):
        px(x, 26, 1, 1, "ferroBrilho")
    # a fornalha de tijolo: fiadas de 3 px, o tijolo mais quente perto da boca
    px(90, 30, 42, P - 30, "tijolo")
    for y in range(30, P):
        if (y - 30) % 3 == 2:
            px(90, y, 42, 1, "tijoloJunta")
        else:
            off = 0 if ((y - 30) // 3) % 2 else 4
            for x in range(90 + off, 132, 8):
                px(x, y, 1, 1, "tijoloJunta")
    for y in range(30, 56):
        for x in range(90, 132):
            d = math.hypot(x - 111.5, (y - 45) * 1.3)
            if 14 < d < 22 and (y - 30) % 3 != 2 and pont(x, y, int((22 - d) * 2)):
                px.p(x, y, "tijoloLuz")
    px(90, 30, 1, P - 30, "tijoloLuz")
    px(131, 30, 1, P - 30, "tijoloJunta")
    # a fuligem acima da boca
    for y in range(30, 37):
        for x in range(100, 124):
            if pont(x, y, 14 - (y - 30) * 2) and abs(x - 111.5) < 13 - (y - 30):
                px.p(x, y, "fuligem")
    # o arco: as aduelas em volta da boca (tijolo aceso, as juntas para o centro)
    x0, x1, yt, yl = BOCA
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    for y in range(yt - 3, yl + 1):
        for x in range(x0 - 3, x1 + 4):
            if dentro_da_boca(x, y):
                continue
            perto = any(dentro_da_boca(x + ox, y + oy) for ox in (-3, -2, -1, 0, 1, 2, 3) for oy in (-3, -2, -1, 0, 1, 2, 3)
                        if abs(ox) + abs(oy) <= 3)
            if perto:
                ang = math.degrees(math.atan2(y + 0.5 - (yt + r * 0.55), x + 0.5 - cx))
                px.p(x, y, "tijoloJunta" if round(ang) % 18 < 2 and y < yt + 8 else "tijoloQuente")
    for y in range(yt, yl + 1):
        for x in range(x0, x1 + 1):
            if dentro_da_boca(x, y):
                px.p(x, y, "#2a0c06")
    # o parapeito na frente da boca e a base
    px(92, 56, 38, 3, "pedra")
    px(92, 56, 38, 1, "tijoloQuente")
    px(92, 58, 38, 1, "pedraSombra")
    # a tina do carvão ao lado da fornalha: o monte com umas brasas
    tx, ty, tw = 78, 62, 18
    for y in range(ty, P):
        for x in range(tx, tx + tw):
            px.p(x, y, "madeiraEsc" if (x - tx) % 4 == 3 else "madeira")
    px(tx, ty, tw, 1, "madeiraLuz")
    px(tx, ty + 6, tw, 1, "ferro")
    for y in range(55, ty + 1):
        meia = (y - 54) * 1.3 + 2
        for x in range(round(tx + tw / 2 - meia), round(tx + tw / 2 + meia)):
            px.p(x, y, "carvaoLuz" if pont(x, y, 4) else "carvao")
    for x, y in [(83, 60), (88, 58), (91, 61), (86, 61)]:
        px(x, y, 1, 1, "brasa")
    # o balde com as tenazes de pé, encostado na fornalha
    px(129, 54, 8, 7, "ferro")
    px(129, 54, 8, 1, "ferroLuz")
    px(129, 54, 1, 7, "ferroLuz")
    for x, y in [(130, 44), (132, 46), (134, 43), (135, 47)]:
        px(x, y, 1, 54 - y, "ferro")
        px(x, y, 1, 1, "ferroLuz")
    # a corrente pendurada ao lado da coifa
    for i, y in enumerate(range(5, 38, 2)):
        px(139 + (i % 2), y, 1, 2, "ferro" if i % 2 else "ferroLuz")


# ---------------------------------------------------------------- o meio: o suporte de ferramentas e a prateleira baixa
def suporte(px):
    px(160, 13, 54, 1, "madeiraLuz")
    px(160, 14, 54, 2, "madeira")
    px(160, 16, 54, 1, "pedraSombra")
    for x in range(163, 212, 7):
        px(x, 16, 1, 2, "ferro")
    # o martelo, o cinzel, as três espadas (a guarda em cima, presas pelo gancho), a tenaz e o atiçador
    px(164, 17, 6, 3, "ferro")
    px(164, 17, 6, 1, "ferroLuz")
    px(166, 20, 2, 10, "madeira")
    px(166, 20, 1, 10, "madeiraLuz")
    px(173, 18, 2, 14, "ferro")
    px(173, 18, 1, 14, "ferroLuz")
    for x, comp in [(180, 23), (187, 26), (194, 21)]:
        px(x + 1, 17, 1, 3, "madeiraLuz")
        px(x - 1, 20, 5, 1, "ferroLuz")
        px(x, 21, 3, comp, "ferro")
        px(x, 21, 1, comp, "ferroBrilho")
        px(x + 1, 21 + comp, 1, 1, "ferro")
    px.linha(201, 18, 199, 38, "ferro")
    px.linha(203, 18, 205, 38, "ferro")
    px(200, 17, 4, 2, "ferroLuz")
    px(209, 18, 1, 17, "ferro")
    px(208, 17, 3, 1, "ferroLuz")
    # a prateleira baixa com os cabos de pé
    px(174, 52, 38, 1, "madeiraLuz")
    px(174, 53, 38, 2, "madeira")
    px(176, 55, 34, 1, "pedraSombra")
    for i, x in enumerate([178, 182, 186, 191, 195, 200, 204, 208]):
        alt = 6 + (i * 5) % 5
        px(x, 52 - alt, 2, alt, "madeiraMeio" if i % 2 else "madeira")
        px(x, 52 - alt, 1, alt, "madeiraLuz")
        if i % 3 == 0:
            px(x - 1, 52 - alt - 2, 4, 2, "ferro")


def lanterna(px):
    """A lanterna pendurada no braço de ferro do esteio, acesa."""
    px(206, 22, 7, 1, "ferro")
    px(206, 23, 1, 3, "ferro")
    px(204, 26, 5, 1, "ferroLuz")
    px(204, 27, 5, 7, "ferroEsc")
    px(205, 28, 3, 5, "vidro")
    px(206, 29, 1, 3, "chama")
    px(204, 34, 5, 1, "ferro")
    px(205, 35, 3, 1, "ferroEsc")


# ---------------------------------------------------------------- a tina de têmpera
def tina(px):
    x0, x1, y0, y1 = 196, 222, 64, 90
    for y in range(y0 + 2, y1):
        for x in range(x0, x1):
            px.p(x, y, "madeiraEsc" if (x - x0) % 4 == 3 else "madeiraMeio" if x - x0 < 6 else "madeira")
    for y in (70, 83):
        px(x0, y, x1 - x0, 2, "ferro")
        px(x0, y, 8, 1, "ferroLuz")
    px(x0, y0, x1 - x0, 2, "madeiraLuz")
    px(x0 + 1, y0 + 2, x1 - x0 - 2, 2, "agua")
    px(x0 + 4, y0 + 2, 8, 1, "aguaLuz")
    px(x0 + 15, y0 + 3, 4, 1, "aguaLuz")
    px(x0, y1, x1 - x0, 1, "chaoJunta")
    # a tenaz encostada dentro da tina
    px.linha(201, 59, 199, 80, "ferroLuz")
    px.linha(203, 59, 205, 80, "ferro")
    px(200, 58, 4, 2, "ferro")


# ---------------------------------------------------------------- o armazém e a bancada, à direita
def armazem(px):
    # a prateleira de cima com as caixas e o baú pequeno; a roldana pendurada
    px(236, 27, 50, 1, "madeiraLuz")
    px(236, 28, 50, 2, "madeira")
    px(238, 30, 46, 1, "pedraSombra")
    px(246, 20, 11, 7, "madeira")
    px(246, 20, 11, 1, "madeiraLuz")
    px(250, 22, 3, 1, "ferro")
    px(262, 23, 8, 4, "madeiraMeio")
    px(262, 23, 8, 1, "madeiraLuz")
    px(272, 19, 12, 8, "couro")
    px(272, 19, 12, 2, "#6a4a30")
    px(277, 22, 2, 2, "#a8904c")
    # a prateleira do meio: os lingotes empilhados, o elmo para consertar e a caixa com a cinta
    px(236, 44, 50, 1, "madeiraLuz")
    px(236, 45, 50, 2, "madeira")
    px(238, 47, 46, 1, "pedraSombra")
    for x, y in [(242, 41), (249, 41), (256, 41), (245, 38), (252, 38)]:
        px(x, y, 6, 3, "ferro")
        px(x, y, 6, 1, "ferroBrilho")
        px(x + 5, y, 1, 3, "ferroEsc")
    ex, ey = 266, 33  # o elmo de pé: a cúpula, a fresta da viseira, os furos
    for i, (a, w) in enumerate([(3, 5), (1, 9), (0, 11), (0, 11), (0, 11), (0, 11), (0, 11), (1, 9), (1, 9), (1, 9), (2, 7)]):
        px(ex + a, ey + i, w, 1, "ferro")
        px(ex + a, ey + i, 2 if i < 6 else 1, 1, "ferroBrilho" if i < 3 else "ferroLuz")
    px(ex + 1, ey + 5, 9, 1, "ferroEsc")
    for x in (ex + 3, ex + 5, ex + 7):
        px(x, ey + 8, 1, 1, "ferroEsc")
    px(278, 36, 8, 8, "madeira")
    px(278, 36, 8, 1, "madeiraLuz")
    px(278, 39, 8, 1, "ferro")
    px(281, 38, 2, 3, "#a8904c")
    # o cavalete das espadas, de pé em cima da bancada: os dois montantes, a trave de cima com os encaixes e o trilho de
    # baixo onde as pontas descansam; as quatro espadas (o cabo, a guarda, a lâmina com o fio aceso)
    for x in (289, 318):
        px(x, 31, 2, 26, "madeira")
        px(x, 31, 1, 26, "madeiraLuz")
    px(289, 33, 31, 2, "madeira")
    px(289, 33, 31, 1, "madeiraLuz")
    px(291, 53, 27, 3, "madeira")
    px(291, 53, 27, 1, "madeiraLuz")
    for i, x in enumerate([294, 300, 306, 312]):
        topo = 20 + (i * 3) % 7
        px(x, topo, 2, 6, "couroEsc")
        px(x - 1, topo + 6, 4, 1, "ferroLuz")
        px(x, topo + 7, 2, 53 - topo - 7, "ferro")
        px(x, topo + 7, 1, 53 - topo - 7, "ferroBrilho")
    # a bancada: o tampo, a frente, as pernas e a travessa; em cima, o martelo, as barras e o pano caindo pela borda
    px(248, 57, 72, 1, "madeiraLuz")
    px(248, 58, 72, 3, "madeiraMeio")
    px(248, 61, 72, 1, "madeiraEsc")
    for x in (252, 300):
        px(x, 62, 5, P + 8 - 62, "madeira")
        px(x, 62, 1, P + 8 - 62, "madeiraLuz")
    px(252, 74, 53, 2, "madeira")
    px(252, 74, 53, 1, "madeiraLuz")
    px(256, 53, 7, 3, "ferro")  # o martelo deitado: a cabeça e o cabo
    px(256, 53, 7, 1, "ferroLuz")
    px(263, 55, 7, 1, "madeiraLuz")
    for i, (x, w) in enumerate([(272, 12), (274, 10), (271, 9)]):  # as barras, empilhadas, longe do cavalete
        px(x, 56 - i, w, 1, "ferroBrilho" if i == 2 else "ferroLuz")
    for y in range(57, 71):
        px(272, y, 8 - (y - 57) // 5, 1, "pano" if y % 3 else "panoEsc")
    # embaixo da bancada: um saco e um barril pequeno, no escuro
    px(286, 66, 10, 15, "panoEsc")
    px(287, 64, 8, 2, "pano")
    px(306, 62, 12, 19, "madeira")
    px(306, 62, 12, 1, "madeiraLuz")
    px(306, 67, 12, 1, "ferro")
    px(306, 75, 12, 1, "ferro")


# ---------------------------------------------------------------- a luz
LUZES = [  # (x, y, raio do halo, força) — a fornalha, a lanterna, a vela
    (111.5, 48, 74, 1.0), (206, 30, 22, 0.7), (57, 36, 13, 0.5),
]


def luz(t):
    """Longe das luzes, a sala escurece em cinco degraus pontilhados (como na capela); perto, o halo quente em anéis
    (como a tocha do ossuário); da porta, o frio no chão e no batente."""
    a = t.a
    for y in range(QH):
        for x in range(QW):
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.4)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.4)))
            frio = max(0.0, 1 - math.hypot(x - 27, (y - 74) * 2.2) / 40) if y > P - 30 else 0.0
            escuro = max(0.0, 0.62 - perto * 1.1 - frio * 0.8)
            f5 = escuro / 0.62 * 5
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
    return a


def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    sala(px)
    parede_esquerda(px)
    fornalha(px)
    suporte(px)
    armazem(px)
    esteios(px)
    tina(px)  # a tina fica na frente do esteio (mais perto de quem olha): vem depois dele
    lanterna(px)
    porta(px)
    luz(t)
    # a luz própria das fontes (depois do escuro: elas não escurecem)
    lanterna(px)
    px(56, 34, 3, 3, "chamaFora")
    px(57, 34, 1, 2, "chama")
    return t


# ---------------------------------------------------------------- a frente: as silhuetas de baixo
def frente():
    t = Tela(QW, QH)
    px = Pincel(t)
    v = "vulto"
    # o jarro: o bojo, o gargalo e a asa
    for y in range(76, QH):
        meia = 11 * math.sqrt(max(0.0, 1 - ((y - 88) / 13) ** 2))
        px(round(14 - meia), y, round(meia * 2), 1, v)
    px(10, 70, 8, 7, v)
    px(9, 69, 10, 2, v)
    for a in range(-90, 91, 4):  # a asa, cheia
        for r in (4, 5):
            px.p(round(24 + math.cos(math.radians(a)) * r), round(81 + math.sin(math.radians(a)) * (r + 1)), v)
    px(10, 69, 8, 1, "vultoLuz")
    # as caixas e o banco, a alturas diferentes; uma garrafa
    for x, y, w in [(30, 86, 30), (56, 83, 32), (86, 89, 30), (122, 92, 22)]:
        px(x, y, w, QH - y, v)
        px(x, y, w, 1, "vultoLuz")
    px(112, 82, 5, 14, v)
    px(113, 79, 3, 3, v)
    px(176, 92, 24, 4, v)
    px(176, 92, 24, 1, "vultoLuz")
    # à direita: o rebolo no cavalete e a roda de carroça encostada
    px(226, 56, 4, 40, v)
    px(240, 64, 4, 32, v)
    for y in range(57, 76):
        for x in range(226, 245):
            if (x + 0.5 - 235) ** 2 + (y + 0.5 - 66) ** 2 <= 81:
                px.p(x, y, v)
    for a in range(200, 300, 8):
        px.p(round(235 + math.cos(math.radians(a)) * 9), round(66 + math.sin(math.radians(a)) * 9), "vultoLuz")
    px(226, 75, 18, 3, v)
    cx, cy, R = 300, 96, 26
    for r in (R, R - 1, R - 2):
        for a in range(180, 361, 2):
            px.p(round(cx + math.cos(math.radians(a)) * r), round(cy + math.sin(math.radians(a)) * r), v)
    for a in range(190, 360, 30):
        px.linha(cx, cy, round(cx + math.cos(math.radians(a)) * R), round(cy + math.sin(math.radians(a)) * R), v)
    px(cx - 3, cy - 3, 6, 3, v)
    for a in range(200, 300, 4):
        px.p(round(cx + math.cos(math.radians(a)) * R), round(cy + math.sin(math.radians(a)) * R) - 1, "vultoLuz")
    return t
