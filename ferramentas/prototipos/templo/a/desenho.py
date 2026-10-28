"""O templo do Vau, candidata A: o interior desenhado na linguagem dos ambientes aprovados (a forja H2, a curandeira):
cada material em dois ou três tons chapados, os objetos lidos pela silhueta e pelo valor, quase sem contorno preto, e a
luz feita por cima (o quente das velas e das janelas, a sala escurecendo em degraus pontilhados longe delas).

O que o jogo estabelece (o levantamento está no LEIA-ME): a igreja da vila (a nave de telhado de duas águas, o
campanário com o sino e a cruz, duas janelas estreitas acesas em amarelo quente, a porta); "velas, incenso e um
clérigo cansado, de mãos firmes"; ele trata "com unguentos e orações" o herói e quem anda com ele. O resto é escolha
desta candidata: a nave vista de lado, as paredes caiadas, as tesouras do telhado, o velário na entrada, os bancos, o
canto de atendimento (o catre, a mesa dos unguentos e das ataduras), o presbitério um degrau acima com o altar e o
incensário, a base do campanário com a corda do sino.

A câmera é mais aberta que a da curandeira (o clérigo tem ~42 px dos pés ao alto da cabeça; Marta, 52): a altura das
paredes acima das pessoas dá o pé-direito. O quadro é o mesmo (320×96), para os cartões ficarem no mesmo lugar.

As camadas: `fundo()` (parado), `velas(i)` (as chamas, 4 quadros), `fumaca(i)` (o incenso, 8 quadros), `poeira(i)` (o pó
nos feixes de luz, 8 quadros) e `frente()` (as silhuetas de baixo, por cima de tudo)."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "hud", "forja", "h2"))
from tela_h2 import Tela  # noqa: E402  (a mesma camada de pixels das fontes da forja)

QW, QH = 320, 96
P = 72        # a linha do chão da nave (a parede encontra o chão)
PES = 86      # onde pisam o clérigo, o catre e a mesa
DEGRAU = 80   # o chão do presbitério (um degrau acima: o altar fica mais alto que a nave)
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def pont(x, y, n):
    return BAYER[(y & 3) * 4 + (x & 3)] < n


C = {
    # a parede caiada: a cal clara em cima, o rodapé de pedra embaixo
    "cal": "#5a5248", "calLuz": "#6e655a", "calSombra": "#433d36", "calFundo": "#3a352f",
    "pedra": "#3a352f", "pedraLuz": "#504940", "pedraSombra": "#25211d", "junta": "#2a2621",
    # a madeira (tesouras, bancos, catre, mesa, porta)
    "madeira": "#4a3424", "madeiraMeio": "#5c4330", "madeiraLuz": "#755840", "madeiraEsc": "#2a1d13",
    # o chão de lajes
    "chao": "#3a342d", "chaoLuz": "#4b443b", "chaoJunta": "#28241f",
    # o dia lá fora (frio)
    "ceuAlto": "#c4d0d8", "ceu": "#9eb0be", "neve": "#d2dbe1", "neveSombra": "#a6b4be", "longe": "#7d8d9a",
    # a luz das janelas (a cor das janelas acesas da vila, #e8a050) e o vidro
    "janela": "#e8a050", "janelaLuz": "#ffd070", "janelaEsc": "#b06a2a", "chumbo": "#3a2a1c",
    # o linho do altar, do catre e das ataduras
    "linho": "#b0a68e", "linhoLuz": "#d2c8b0", "linhoSombra": "#857b66",
    "la": "#5a4a3a", "laLuz": "#6e5c48", "laEsc": "#3e3226",       # o cobertor de lã do catre
    "palha": "#7a6638", "palhaEsc": "#55462a",
    # o ferro (o velário, o incensário, as dobradiças) e o latão (os castiçais)
    "ferro": "#33343a", "ferroLuz": "#55575f", "ferroEsc": "#1c1d22",
    "latao": "#8a6a2a", "lataoLuz": "#c09a48", "lataoEsc": "#5a4418",
    # o barro dos potes de unguento, a bacia
    "barro": "#6a4230", "barroLuz": "#8a5a3c", "barroEsc": "#43281c", "agua": "#3a5662",
    # a cera, as chamas
    "cera": "#d6ccae", "ceraEsc": "#a89e80", "chama": "#ffcc66", "chamaFora": "#e8782a", "chamaMiolo": "#fff2c4",
    "corda": "#8a7650", "cordaEsc": "#5e5034",
    "vulto": "#0b0a0a", "vultoLuz": "#1a1816",
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

    def grade(self, x0, y0, linhas, pal):
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])


# ---------------------------------------------------------------- a nave
JANELAS = [(84, 14), (136, 14)]  # o x da esquerda e o alto do arco das duas janelas (as duas da fachada da vila)
JW, JH = 6, 30                  # a largura e a altura do vão de vidro


def sala(px):
    """A parede caiada da nave, alta (a cal clara, mais escura no alto, longe das velas), o rodapé de pedra, as
    pilastras, as tesouras do telhado e o chão de lajes."""
    px(0, 0, QW, P, "cal")
    for y in range(0, 22):  # o alto da parede, mais escuro (longe das velas e embaixo do telhado)
        for x in range(QW):
            if pont(x, y, int((22 - y) / 22 * 12)):
                px.p(x, y, "calSombra")
    for x, y, w in [(30, 40, 7), (112, 52, 5), (180, 30, 8), (210, 48, 6), (62, 30, 4)]:  # a cal gasta
        px(x, y, w, 1, "calLuz")
    # o rodapé de pedra (a meia altura de um homem), as fiadas desencontradas
    px(0, 58, QW, P - 58, "pedra")
    px(0, 58, QW, 1, "pedraLuz")
    for y in range(63, P, 5):
        for x in range(((y // 5) % 2) * 7 - 14, QW, 14):
            px(x, y, 14, 1, "junta")
            px(x, y, 1, 5, "junta")
    # as pilastras de pedra que sobem até as tesouras (entre as janelas e no canto do presbitério)
    for x0 in (58, 112, 238):
        px(x0, 6, 8, P - 6, "pedra")
        px(x0, 6, 1, P - 6, "pedraLuz")
        px(x0 + 6, 6, 2, P - 6, "pedraSombra")
        for y in range(10, P, 9):
            px(x0 + 1, y, 5, 1, "junta")
        px(x0 - 1, 6, 10, 2, "pedraLuz")  # o capitel simples
    # as tesouras do telhado: a linha (viga) de lado a lado e as pernas inclinadas, de madeira escura
    px(0, 0, QW, 3, "madeiraEsc")
    px(0, 5, QW, 3, "madeira")
    px(0, 5, QW, 1, "madeiraLuz")
    px(0, 7, QW, 1, "madeiraEsc")
    for x0 in (62, 116, 242):
        px.linha(x0 - 14, 0, x0 + 3, 5, "madeira")
        px.linha(x0 + 18, 0, x0 + 3, 5, "madeira")
    # o chão de lajes (as fiadas crescem para a frente)
    px(0, P, QW, QH - P, "chao")
    px(0, P, QW, 1, "chaoLuz")
    y, i = P + 4, 0
    while y < QH:
        px(0, y, QW, 1, "chaoJunta")
        if y + 1 < QH:
            px(0, y + 1, QW, 1, "chaoLuz")
        passo = 20 + i * 5
        for x in range((i * 11) % passo, QW, passo):
            px(x, y - (4 + i), 1, 4 + i, "chaoJunta")
        y += 5 + i
        i += 1


def janelas(px):
    """As duas janelas estreitas e altas, de arco redondo, fundas na parede grossa (o derrame claro em volta): o vidro
    em losangos de chumbo, aceso do lado de fora (a cor das janelas acesas da vila)."""
    for x0, y0 in JANELAS:
        # o derrame (o corte da parede grossa, mais largo que o vidro): a cal clara, a sombra do lado direito
        px(x0 - 3, y0 + 1, JW + 6, JH + 2, "calLuz")
        px(x0 + JW + 1, y0 + 2, 2, JH, "calSombra")
        px(x0 - 3, y0 + JH + 1, JW + 6, 2, "pedraLuz")  # o peitoril
        for k, (m, h) in enumerate([(2, 0), (1, 1)]):  # o arco do derrame
            px(x0 - 3 + m, y0 - 1 + k, JW + 6 - 2 * m, 1, "calLuz")
        # o vidro: o arco e o vão
        px(x0 + 1, y0, JW - 2, 1, "janela")
        px(x0, y0 + 1, JW, JH, "janela")
        for y in range(y0 + 1, y0 + JH + 1):  # o claro no meio, mais quente embaixo
            px(x0 + 2, y, 2, 1, "janelaLuz" if (y - y0) % 7 < 5 else "janela")
        # os losangos de chumbo
        for y in range(y0 + 3, y0 + JH, 5):
            px(x0, y, JW, 1, "chumbo")
        px(x0 + JW // 2, y0 + 1, 1, JH, "chumbo")
        px(x0, y0 + JH, JW, 1, "janelaEsc")


def entrada(px):
    """A entrada, à esquerda: o arco largo da porta, aberto para a rua de inverno (só a luz de fora), a folha de tábuas
    aberta para dentro com as dobradiças de ferro."""
    x0, x1, y0 = 10, 34, 26
    for y in range(y0, P):
        t = (y - y0) / (P - y0)
        for x in range(x0, x1):
            px.p(x, y, "ceu" if pont(x, y, int(t * 26)) else "ceuAlto")
    px(x0, 54, x1 - x0, 2, "longe")
    px(x0, 56, x1 - x0, P - 56, "neve")
    px(x0, P - 2, x1 - x0, 2, "neveSombra")
    # o arco de pedra (as aduelas) e as ombreiras
    for k, w in enumerate([14, 20, 22, 24]):
        px((x0 + x1) / 2 - w / 2, y0 - 4 + k, w, 1, "ceuAlto")
    for xx in (x0 - 4, x1):
        px(xx, y0 - 2, 4, P - y0 + 2, "pedra")
        px(xx, y0 - 2, 1, P - y0 + 2, "pedraLuz")
        px(xx + 3, y0 - 2, 1, P - y0 + 2, "pedraSombra")
    for k in range(7):  # as aduelas do arco
        a = math.pi * (1 - k / 6)
        cx, cy = (x0 + x1) / 2 + math.cos(a) * 14, y0 - 2 - math.sin(a) * 6
        px(cx - 2, cy - 1, 4, 3, "pedra")
        px(cx - 2, cy - 1, 4, 1, "pedraLuz")
    # a folha aberta, de quina, encostada na parede de dentro
    px(2, y0 + 2, 5, P - y0 - 2, "madeiraMeio")
    px(2, y0 + 2, 1, P - y0 - 2, "madeiraLuz")
    px(6, y0 + 2, 1, P - y0 - 2, "madeiraEsc")
    for yy in (y0 + 8, P - 10):
        px(2, yy, 6, 2, "ferro")


def velario(px):
    """O velário junto da entrada: o suporte de ferro com três degraus de velas votivas acesas (as chamas vêm na camada
    velas), a caixa das velas novas embaixo."""
    x0 = 40
    for k, (y, w) in enumerate([(66, 18), (61, 14), (56, 10)]):  # os degraus, de baixo para cima
        xx = x0 + (18 - w) // 2
        px(xx, y, w, 2, "ferro")
        px(xx, y, w, 1, "ferroLuz")
        for c in range(xx + 1, xx + w - 1, 3):  # as velas pequenas, de alturas diferentes (gastas)
            h = 2 + (c * 7 + k) % 3
            px(c, y - h, 2, h, "cera")
            px(c + 1, y - h, 1, h, "ceraEsc")
            px.p(c, y - h - 1, "ferroEsc")  # o pavio
    px(x0 + 8, 68, 2, PES - 68, "ferro")      # a haste e o pé
    px(x0 + 3, PES - 1, 12, 1, "ferro")
    px(x0 + 3, PES - 2, 12, 1, "ferroLuz")
    # a caixa de madeira com as velas novas, no chão ao lado
    px(x0 - 6, 78, 8, 7, "madeira")
    px(x0 - 6, 78, 8, 1, "madeiraLuz")
    for c in range(x0 - 5, x0 + 1, 2):
        px(c, 75, 1, 3, "cera")


VELARIO_CHAMAS = []  # as posições das chamas do velário (preenchido por velario_chamas)


def velario_chamas():
    pos = []
    x0 = 40
    for k, (y, w) in enumerate([(66, 18), (61, 14), (56, 10)]):
        xx = x0 + (18 - w) // 2
        for c in range(xx + 1, xx + w - 1, 3):
            h = 2 + (c * 7 + k) % 3
            pos.append((c, y - h - 2))
    return pos


def bancos(px):
    """Os bancos atravessam a nave (de frente para o altar, à direita): da lateral se vê a cabeceira de cada um, o
    painel de tábua com o alto arredondado do lado do encosto e o assento saindo para a frente. Atrás de cada um, um
    pedaço do banco da fileira de trás (mais escuro), para a nave ter fundo."""
    PERFIL = [  # a cabeceira de um banco: o encosto à esquerda, o assento à direita (um caractere por pixel)
        ".LMM.......",
        "LMMMe......",
        "LMMMe......",
        "LMMMe......",
        "LMMMe......",
        "LMMMe......",
        "LMMMe......",
        "LMMMe......",
        "LMMMMMMMMMe",
        "LMMMMMMMMMe",
        "LMMMMMMMMMe",
        "LMMMMMMMMMe",
        "LMMeeeeeMMe",
        "LMMe....LMe",
        "LMMe....LMe",
    ]
    for x0 in (64, 88, 112, 136):
        # o banco de trás: só a borda do encosto e do assento, mais escura, acima e à direita (mais fundo)
        px(x0 + 3, PES - 19, 2, 11, "madeiraEsc")
        px(x0 + 3, PES - 12, 10, 2, "madeiraEsc")
        px.grade(x0, PES - 15, PERFIL, {"L": "madeiraLuz", "M": "madeiraMeio", "e": "madeiraEsc"})


def atendimento(px):
    """O canto de atendimento, entre a nave e o presbitério: o catre de madeira com o colchão de palha, o lençol, o
    cobertor dobrado e o travesseiro; a mesa dos unguentos (a bacia, os potes de barro, as ataduras enroladas, a pilha
    de tiras de linho para enrolar) onde o clérigo trabalha."""
    # o catre (x 154 a 192)
    x0, x1, y = 154, 192, 72
    px(x0, y, x1 - x0, 5, "palha")                # o colchão de palha
    px(x0, y, x1 - x0, 1, "palhaEsc")
    px(x0, y - 2, x1 - x0, 3, "linho")            # o lençol
    px(x0, y - 2, x1 - x0, 1, "linhoLuz")
    px(x0 + 1, y - 5, 8, 4, "linho")              # o travesseiro, na cabeceira (à esquerda)
    px(x0 + 1, y - 5, 8, 1, "linhoLuz")
    px(x0 + 8, y - 4, 1, 3, "linhoSombra")
    px(x1 - 14, y - 4, 12, 3, "la")               # o cobertor dobrado, nos pés
    px(x1 - 14, y - 4, 12, 1, "laLuz")
    px(x1 - 14, y - 2, 12, 1, "laEsc")
    px(x0 - 1, y + 5, x1 - x0 + 2, 2, "madeira")  # a armação
    px(x0 - 1, y + 5, x1 - x0 + 2, 1, "madeiraLuz")
    for xx in (x0, x1 - 2):
        px(xx, y + 7, 2, PES - y - 7, "madeira")
        px(xx + 1, y + 7, 1, PES - y - 7, "madeiraEsc")
    px(x0 - 2, y - 7, 3, PES - y + 7, "madeiraMeio")  # a cabeceira
    px(x0 - 2, y - 7, 1, PES - y + 7, "madeiraLuz")
    # a mesa dos unguentos (x 198 a 222), o tampo na altura da cintura do clérigo
    m0, m1, mt = 198, 222, MESA
    px(m0, mt, m1 - m0, 3, "madeiraMeio")
    px(m0, mt, m1 - m0, 1, "madeiraLuz")
    px(m0, mt + 2, m1 - m0, 1, "madeiraEsc")
    for xx in (m0 + 1, m1 - 3):
        px(xx, mt + 3, 2, PES - mt - 3, "madeira")
        px(xx + 1, mt + 3, 1, PES - mt - 3, "madeiraEsc")
    px(m0 + 2, 80, m1 - m0 - 4, 2, "madeira")     # a prateleira de baixo, com o cesto das tiras limpas
    px(m0 + 4, 76, 12, 4, "palha")
    px(m0 + 4, 76, 12, 1, "palhaEsc")
    px(m0 + 5, 75, 10, 1, "linho")
    # em cima: a bacia de barro com água, dois potes de unguento e a pilha de ataduras prontas
    px(m0 + 1, mt - 3, 8, 3, "barro")
    px(m0 + 1, mt - 3, 8, 1, "barroLuz")
    px(m0 + 2, mt - 3, 6, 1, "agua")
    px(m0 + 10, mt - 4, 3, 4, "barro")
    px(m0 + 10, mt - 4, 3, 1, "barroLuz")
    px(m0 + 10, mt - 5, 3, 1, "linhoSombra")
    px(m0 + 14, mt - 3, 2, 3, "barroEsc")
    px(m0 + 14, mt - 3, 2, 1, "barro")


MESA = 66  # o tampo da mesa dos unguentos


def presbiterio(px):
    """O presbitério, um degrau acima da nave: o degrau de pedra, o altar com a toalha de linho, os dois castiçais de
    latão e as velas altas (as chamas vêm na camada velas), a cruz simples de madeira na parede (a mesma do campanário),
    o incensário de ferro pendurado na corrente (a fumaça vem na camada fumaca) e, no fim, a base do campanário: o arco
    escuro e a corda do sino descendo, com o nó."""
    # o degrau
    px(232, DEGRAU - 3, QW - 232, 3, "pedraLuz")
    px(232, DEGRAU, QW - 232, QH - DEGRAU, "pedra")
    px(232, DEGRAU - 3, QW - 232, 1, "calLuz")
    # o altar de pedra com a toalha
    a0, a1, at = 254, 290, 62
    px(a0 + 2, at, a1 - a0 - 4, DEGRAU - 3 - at, "pedra")
    px(a0 + 2, at, 1, DEGRAU - 3 - at, "pedraLuz")
    px(a1 - 4, at, 2, DEGRAU - 3 - at, "pedraSombra")
    px(a0, at - 2, a1 - a0, 3, "linho")
    px(a0, at - 2, a1 - a0, 1, "linhoLuz")
    px(a0, at + 1, 4, 8, "linho")                 # a toalha caindo nas pontas
    px(a1 - 4, at + 1, 4, 8, "linhoSombra")
    px(a0 + 2, at + 1, 1, 8, "linhoLuz")
    # os castiçais e as velas altas
    for cx in (a0 + 5, a1 - 7):
        px(cx - 1, at - 3, 4, 1, "latao")
        px(cx, at - 6, 2, 3, "latao")
        px(cx, at - 6, 1, 3, "lataoLuz")
        px(cx, at - 14, 2, 8, "cera")
        px(cx + 1, at - 14, 1, 8, "ceraEsc")
    # o livro aberto no meio do altar
    px((a0 + a1) // 2 - 4, at - 4, 8, 2, "linhoLuz")
    px((a0 + a1) // 2, at - 4, 1, 2, "linhoSombra")
    px((a0 + a1) // 2 - 4, at - 2, 8, 1, "madeiraEsc")
    # a cruz de madeira na parede, acima do altar
    cx = (a0 + a1) // 2
    px(cx - 1, 22, 3, 22, "madeira")
    px(cx - 1, 22, 1, 22, "madeiraLuz")
    px(cx - 7, 28, 15, 3, "madeira")
    px(cx - 7, 28, 15, 1, "madeiraLuz")
    # o incensário pendurado da tesoura, na corrente, ao lado do altar
    ix = INCENSO[0]
    for y in range(8, INCENSO[1] - 3):
        px.p(ix, y, "ferro" if y % 2 else "ferroLuz")
    px(ix - 2, INCENSO[1] - 3, 5, 1, "ferroLuz")
    px(ix - 3, INCENSO[1] - 2, 7, 4, "ferro")
    px(ix - 3, INCENSO[1] - 2, 7, 1, "ferroLuz")
    px(ix - 2, INCENSO[1] + 2, 5, 1, "ferroEsc")
    px.p(ix - 1, INCENSO[1], "chamaFora")         # a brasa pela grade
    px.p(ix + 1, INCENSO[1], "chamaFora")
    # a base do campanário: o arco escuro, a corda do sino com o nó, presa num gancho na parede
    b0 = 300
    px(b0, 14, QW - b0, DEGRAU - 14, "vulto")
    px(b0, 14, QW - b0, 1, "pedraLuz")
    px(b0 - 3, 10, 3, DEGRAU - 10, "pedra")
    px(b0 - 3, 10, 1, DEGRAU - 10, "pedraLuz")
    for y in range(14, 66):
        px.p(310, y, "corda" if y % 3 else "cordaEsc")
    px(309, 66, 3, 3, "corda")                    # o nó
    px(310, 69, 1, 4, "cordaEsc")
    px(306, 50, 2, 1, "ferroLuz")                 # o gancho, com a corda presa de lado
    px.linha(307, 50, 310, 46, "cordaEsc")


INCENSO = (244, 46)  # o incensário (o centro da caçoleta)


# ---------------------------------------------------------------- a luz
LUZES = [(271, 47, 26, 0.85), (49, 56, 18, 0.7), (210, 60, 16, 0.4)]  # o altar, o velário, a mesa (x, y, raio, força)


def luz(t):
    """Longe das velas, a sala escurece em degraus pontilhados; perto, o halo quente em anéis; da porta, o frio no chão.
    As janelas acendem a parede em volta (o claro do derrame) e jogam o feixe de luz no chão (camada poeira)."""
    for y in range(QH):
        for x in range(QW):
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.4)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.6)))
            for jx, jy in JANELAS:
                d = math.hypot(x - (jx + JW / 2), (y - (jy + JH / 2)) * 0.8)
                perto = max(perto, 0.55 * max(0.0, 1 - d / 34))
            frio = max(0.0, 1 - math.hypot(x - 22, (y - 74) * 2.0) / 40) if y > P - 30 else 0.0
            escuro = max(0.0, 0.5 - perto * 1.1 - frio * 0.8)
            f5 = escuro / 0.5 * 4
            n = int(f5) + (1 if pont(x, y, int((f5 % 1) * 16)) else 0)
            if n:
                t.mistura(x, y, (4, 4, 6), 0.5 * n / 4)
            for lx, ly, r, f in LUZES:
                d2 = ((x - lx) ** 2 + ((y - ly) * 1.4) ** 2) / (r * r)
                if d2 < 1:
                    al = 0.18 if d2 < 0.08 else 0.11 if d2 < 0.3 else 0.06 if d2 < 0.65 else 0.03
                    t.mistura(x, y, (255, 170, 90), al * f)
            if frio > 0 and y >= P and pont(x, y, int(frio * 8)):
                t.mistura(x, y, (190, 210, 228), 0.12)


def feixes(t, forca=1.0):
    """Os feixes das duas janelas, descendo na diagonal até o chão (a luz entra alta, de fora para dentro): uma faixa
    quente e rala, mais forte perto da janela."""
    for jx, jy in JANELAS:
        for y in range(jy + JH + 2, QH):
            k = (y - (jy + JH)) / (QH - jy - JH)
            x0 = jx - 2 + (y - jy - JH) * 0.55
            for x in range(int(x0), int(x0 + JW + 4 + k * 6)):
                if 0 <= x < QW and pont(x, y, int((1 - k) * 7 * forca) + 3):
                    t.mistura(x, y, (255, 200, 120), 0.16 * (1 - k * 0.5))


def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    sala(px)
    janelas(px)
    entrada(px)
    velario(px)
    presbiterio(px)
    bancos(px)
    atendimento(px)
    luz(t)
    feixes(t)
    return t


# ---------------------------------------------------------------- as camadas que se mexem
def velas(i):
    """As chamas (4 quadros): as do velário, as duas do altar e a vela da mesa; cada uma pisca no seu passo, pouco."""
    t = Tela(QW, QH)
    px = Pincel(t)
    chamas = velario_chamas() + [(260, 46), (284, 46)]
    for k, (x, y) in enumerate(chamas):
        f = (i + k * 3) % 4
        alto = 3 if f in (0, 2) else 2 if f == 1 else 4
        px(x, y - alto + 2, 1, alto, "chamaFora")
        px.p(x, y + 1, "chama")
        if alto >= 3:
            px.p(x, y, "chamaMiolo" if f == 3 else "chama")
    return t


def fumaca(i):
    """O incenso (8 quadros, um ciclo de 16 px que emenda): dois fiapos de 1 px saindo do incensário e subindo devagar,
    ondulando, apagando no alto."""
    t = Tela(QW, QH)
    ix, iy = INCENSO
    for k in range(2):
        cabeca = iy - 3 - (i * 2 + k * 8) % 16
        for s in range(6):
            y = cabeca + s
            if y >= iy - 3 or y < iy - 22:
                continue
            x = ix + (1 if ((y + k * 2) // 3) % 2 else 0) - k
            a = 1 - (iy - y) / 22
            t.px(x, y, (int(170 * a + 60), int(166 * a + 58), int(156 * a + 56)))
    return t


def poeira(i):
    """O pó nos feixes de luz (8 quadros): uns pontos claros descendo devagar dentro de cada feixe."""
    t = Tela(QW, QH)
    for n, (jx, jy) in enumerate(JANELAS):
        for k in range(4):
            y = jy + JH + 4 + ((k * 7 + i + n * 3) % 22)
            x = int(jx + (y - jy - JH) * 0.55 + 1 + (k * 3 + n) % (JW + 2))
            if y < QH:
                t.px(x, y, (232, 196, 140))
    return t


def frente():
    """As silhuetas de baixo, por cima de tudo: a ponta de um banco mais perto, à esquerda."""
    t = Tela(QW, QH)
    px = Pincel(t)
    v = "vulto"
    px(0, 88, 40, 3, v)       # o assento de um banco mais perto, cortado pela borda
    px(0, 88, 40, 1, "vultoLuz")
    px(6, 91, 3, QH - 91, v)
    px(30, 91, 3, QH - 91, v)
    return t
