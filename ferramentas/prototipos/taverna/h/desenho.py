"""A candidata H da taverna (29/10/2026): a G com a câmera um pouco mais afastada e deslocada para a direita, para dar
volume ao balcão e lugar aos fregueses de perto. A G é a base (os objetos, a organização, o taverneiro); a referência de
três quartos ("Taverna sombria e o estalajadeiro desconfiado-2") apoia a profundidade do tampo e a presença dos
fregueses. Não é o salão: sem mesas, galeria, escada nem Morel.

A câmera: uma perspectiva simplificada de um ponto, o ponto de fuga à direita, na beira do quadro (`PF`). A parede, as
prateleiras e a frente do balcão ficam de frente; o que corre para o fundo (o tampo, a ponta do balcão) converge para
`PF`. Por isso o balcão termina antes da despensa e mostra a lateral curta da ponta da direita, e o tampo aparece mais
fundo que na G. Os planos, da frente para o fundo:
- os dois fregueses sentados ao balcão, recortados pela borda de baixo (a cabeça, os ombros, parte do tronco, o braço
  apoiado no tampo);
- o balcão: o tampo fundo, a borda, a frente em tábuas, a ponta com a lateral; no tampo, a tábua do pão e do queijo e
  as canecas dos fregueses;
- o taverneiro (do mesmo tamanho da G: a presença dele não diminui) e a bancada de trabalho;
- a parede com as prateleiras (em duas partes, com o vão atrás da cabeça), a lareira, a despensa.

Os objetos da G entram aqui pelo desenho dela (`G`), copiados para o novo lugar (`de_g`); o que muda com a câmera (o
balcão, a porta da despensa, o lampião, os fregueses, a luz) é desenhado aqui. As camadas são as da G: `fundo`, `fogo`,
`lampiao`, `caldeirao`, `taverneiro` e `frente`."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))

from g import desenho as G  # noqa: E402
from tela_h2 import Tela  # noqa: E402

QW, QH = G.QW, G.QH
C, Pincel, pont = G.C, G.Pincel, G.pont
PF = (320, 32)  # o ponto de fuga (o olho de quem está sentado ao balcão, um pouco à direita)
BT = 68         # a borda de trás do tampo (o taverneiro some aqui, como na G em y 74)
BF = 80         # a borda da frente do tampo
PONTA = 268     # a quina da frente da ponta do balcão
BB = 60         # o tampo da bancada de trabalho
PR = 30         # o tampo das prateleiras
TAV = (-10, -6)  # onde o taverneiro da G cai na H (o mesmo tamanho, mais para cima e para a esquerda)


def fuga(x, y, y_alvo):
    """O ponto da linha que vai de (x, y) ao ponto de fuga, na altura y_alvo."""
    t = (y - y_alvo) / (y - PF[1])
    return x + t * (PF[0] - x)


PONTA_FUNDO = round(fuga(PONTA, BF, BT))  # a quina de trás da ponta (a lateral vai de PONTA a PONTA_FUNDO)


def de_g(t, desenhar, caixa, dx, dy):
    """Desenha uma parte da G numa tela à parte e a copia para a H, deslocada: só os pixels do desenho, dentro da
    caixa (x0, y0, x1, y1) da G."""
    tmp = Tela(QW, QH)
    r = desenhar(G.Pincel(tmp))
    if isinstance(r, Tela):
        tmp = r
    x0, y0, x1, y1 = caixa
    for y in range(max(0, y0), min(QH, y1)):
        for x in range(max(0, x0), min(QW, x1)):
            if tmp.a[y, x, 3] and 0 <= x + dx < QW and 0 <= y + dy < QH:
                t.a[y + dy, x + dx] = tmp.a[y, x]


# ---------------------------------------------------------------- a sala
def sala(px):
    """A parede de pedra de cima a baixo (entre a ponta do balcão e a despensa ela aparece até o fim do quadro), a viga
    do teto com as pontas dos caibros."""
    px(0, 0, QW, QH, "parede")
    for y in range(3, QH, 6):
        for x in range(((y // 6) % 2) * 7 - 14, QW, 14):
            px(x, y, 14, 1, "junta")
            px(x, y, 1, 6, "junta")
    for x, y in [(60, 9), (102, 45), (186, 3), (228, 39), (300, 51), (8, 3), (290, 81)]:
        px(x + 1, y + 1, 12, 1, "pedra")
    px(0, 0, QW, 5, "madeiraEsc")
    px(0, 4, QW, 1, "madeira")
    px(0, 5, QW, 1, "pedraSombra")
    for x in range(4, QW, 40):
        px(x, 0, 6, 4, "madeira")
        px(x, 0, 1, 4, "madeiraLuz")
        px(x + 5, 0, 1, 4, "madeiraEsc")


def esteio(px, x0, w, ate):
    px(x0, 0, w, ate, "madeira")
    px(x0, 0, 1, ate, "madeiraLuz")
    px(x0 + w - 2, 0, 2, ate, "madeiraEsc")
    for y in (12, 38, 70):
        px(x0 + w // 2, y, 1, 6, "madeiraEsc")


def prateleiras(px):
    """A prateleira alta em duas partes, com o vão atrás da cabeça do taverneiro: a da esquerda (a louça) e a da
    direita (as garrafas), cada uma com as mãos-francesas na pedra. Nenhuma linha passa atrás da cabeça."""
    for x0, x1, maos in ((53, 128, (62, 114)), (170, 246, (180, 234))):
        px(x0, PR, x1 - x0, 1, "madeiraLuz")
        px(x0, PR + 1, x1 - x0, 2, "madeira")
        px(x0, PR + 3, x1 - x0, 1, "pedraSombra")
        for x in maos:
            for k in range(5):
                px(x + k, PR + 3 + k, 2, 1, "madeira")
            px(x, PR + 3, 1, 1, "madeiraLuz")


def bancada(px):
    """A bancada de trabalho entre os esteios: o tampo visto um pouco de cima (abaixo do olho), a frente escura."""
    px(53, BB, PONTA_FUNDO + 2 - 53, 1, "madeiraMeio")
    px(53, BB + 1, PONTA_FUNDO + 2 - 53, 2, "madeira")
    px(53, BB + 3, PONTA_FUNDO + 2 - 53, BT - BB - 3, "madeiraEsc")


def lampiao(px):
    """O lampião no braço de ferro que sai do esteio da direita para a esquerda, em cima da ponta do balcão."""
    x = 274
    px(x, 19, 10, 1, "ferroLuz")
    px(x, 20, 10, 1, "ferro")
    px(x + 1, 21, 1, 2, "ferro")
    px(x - 2, 23, 7, 2, "ferro")
    px(x - 1, 22, 5, 1, "ferroLuz")
    px(x - 2, 25, 1, 9, "ferroEsc")
    px(x + 4, 25, 1, 9, "ferroEsc")
    px(x - 1, 25, 5, 9, "#d89040")
    px(x - 1, 25, 1, 9, "#f0b860")
    px(x - 2, 34, 7, 2, "ferro")
    px(x - 2, 34, 7, 1, "ferroLuz")
    px(x, 36, 3, 1, "ferroEsc")


LAMPIAO_X = 275  # o meio da chama


def chama_lampiao(i):
    t = Tela(QW, QH)
    h = (4, 5, 4, 3)[i]
    for d in range(h):
        w = 2 if d < h - 1 else 1
        t.ret(LAMPIAO_X - (1 if w == 2 and i % 2 else 0), 32 - d, w, 1, (*_hx(G.FOGO[6 if d < 2 else 5]), 255))
    t.px(LAMPIAO_X, 33, G.FOGO[4])
    return t


def _hx(s):
    return tuple(int(s[k:k + 2], 16) for k in (1, 3, 5))


def despensa(px):
    """A porta da despensa, na parede, atrás da passagem entre a ponta do balcão e o esteio: a verga, o batente, as
    tábuas em pé até o fim do quadro, as dobradiças com os cravos e a argola."""
    x0, x1, y0 = 294, 316, 13
    px(x0 - 3, y0 - 3, x1 - x0 + 6, 3, "madeira")
    px(x0 - 3, y0 - 3, x1 - x0 + 6, 1, "madeiraLuz")
    px(x0 - 3, y0, 3, QH - y0, "madeira")
    px(x0 - 3, y0, 1, QH - y0, "madeiraLuz")
    px(x1, y0, 3, QH - y0, "madeiraEsc")
    for x in range(x0, x1):
        k = (x - x0) % 6
        px(x, y0, 1, QH - y0, "madeiraLuz" if k == 0 else "madeiraEsc" if k == 5 else "madeiraMeio")
    for y in (24, 66):
        px(x0, y, 14, 2, "ferro")
        px(x0, y, 14, 1, "ferroLuz")
        for x in (x0 + 2, x0 + 7, x0 + 12):
            px(x, y + 1, 1, 1, "ferroBrilho")
    px(x1 - 6, 44, 3, 1, "ferroLuz")
    for a in range(0, 360, 30):
        px.p(round(x1 - 5 + math.cos(math.radians(a)) * 2), round(48 + math.sin(math.radians(a)) * 2.5), "ferro")
    px(x1 - 7, 47, 1, 2, "ferroLuz")


# ---------------------------------------------------------------- o balcão
def balcao(px):
    """O balcão: o tampo fundo visto de cima (a borda de trás acesa, as tábuas ao comprido em valores próximos), uma
    só aresta forte na frente, a frente escura em tábuas em pé; a ponta da direita com a lateral curta (a quina da
    frente acesa, a aresta de cima subindo para o ponto de fuga)."""
    # o tampo, até a quina de trás da ponta
    for y in range(BT, BF):
        xd = round(fuga(PONTA, BF, y))
        px(0, y, xd, 1, "balcao")
    px(0, BT, PONTA_FUNDO, 1, "balcaoLuz")
    for y, (a, b) in ((72, (0, 140)), (72, (190, 255)), (76, (60, 230))):  # as emendas, discretas
        px(a, y, b - a, 1, "balcaoEsc" if y == 76 else "#4e3622")
    # a borda da frente: uma aresta clara e a espessura
    px(0, BF, PONTA + 1, 1, "balcaoLuz")
    px(0, BF + 1, PONTA + 1, 2, "balcao")
    # a frente em tábuas, escura
    for x in range(0, PONTA + 1):
        k = x % 18
        px(x, BF + 3, 1, QH - BF - 3, "balcaoJunta" if k == 0 else "balcaoEsc")
    px(0, BF + 3, PONTA + 1, 1, "balcaoJunta")
    # a lateral da ponta: entre a quina da frente e a de trás, do tampo até o fim do quadro
    for x in range(PONTA + 1, PONTA_FUNDO + 1):
        topo = round(BF - (x - PONTA) * (BF - BT) / (PONTA_FUNDO - PONTA))
        px(x, topo, 1, 1, "balcaoLuz")
        px(x, topo + 1, 1, QH - topo - 1, "balcao" if x < PONTA + 4 else "madeiraMeio")
    px(PONTA, BF, 1, QH - BF, "balcaoBrilho")  # a quina da frente, acesa pelo lampião
    px(PONTA_FUNDO, BT, 1, QH - BT, "madeiraEsc")
    for x in (PONTA + 6,):
        px(x, BF - 4, 1, QH - BF + 4, "madeira")


def tabua_do_pao(px):
    """A tábua com o pão e o queijo da G, agora no tampo, entre o freguês da esquerda e o taverneiro (a área de
    servir)."""
    de_g(px.t, G.comida_e_jarra, (210, 50, 254, 67), -132, 10)


def caneca_esquerda(px):
    G.caneca(px, 63, 76, 7, 9, asa="dir")
    px(62, 76, 10, 1, "balcaoJunta")


def caneca_direita(px):
    G.caneca(px, 200, 75, 6, 8, asa="esq")
    px(199, 75, 8, 1, "balcaoJunta")


# ---------------------------------------------------------------- os fregueses
FG = {  # os fregueses: escuros, mas cada material em três tons, para o corpo ler como corpo e não como mancha
    "capaLuz": "#3a4a38", "capa": "#212b22", "capaSombra": "#141a15",
    "cabeloLuz": "#4a3220", "cabelo": "#22180f", "cabeloSombra": "#140e0a",
    "peleLuz": "#7a4a2e", "pele": "#4e3020", "peleSombra": "#2e1c13",
    "gibaoLuz": "#5e4432", "gibao": "#33261d", "gibaoSombra": "#1e1612",
    "capuzLuz": "#5a5562", "capuz": "#2a2831", "capuzSombra": "#18171d", "dentro": "#070608",
}


class Vulto:
    """Uma figura de freguês construída por partes (a cabeça, o pescoço, o tronco, os braços), em três tons pelo lado
    virado para a luz (lx, ly), como as figuras do jogo, só que no escuro."""

    def __init__(self, lx, ly):
        self.px, self.lx, self.ly = {}, lx, ly

    def p(self, x, y, cor):
        self.px[(int(x), int(y))] = FG.get(cor, C.get(cor, cor))

    def _tom(self, base, s, luz, sombra):
        return base + "Luz" if s > luz else base + "Sombra" if s < sombra else base

    def elipse(self, cx, cy, rx, ry, base, luz=0.55, sombra=-0.25):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                ox, oy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if ox * ox + oy * oy <= 1:
                    self.p(x, y, self._tom(base, ox * self.lx + oy * self.ly, luz, sombra))

    def membro(self, a, b, ra, rb, base, luz=0.6, sombra=-0.2):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        l2 = dx * dx + dy * dy or 1
        r = max(ra, rb)
        for y in range(int(min(ay, by) - r) - 1, int(max(ay, by) + r) + 2):
            for x in range(int(min(ax, bx) - r) - 1, int(max(ax, bx) + r) + 2):
                cx, cy = x + 0.5, y + 0.5
                t = max(0, min(1, ((cx - ax) * dx + (cy - ay) * dy) / l2))
                rr = ra + (rb - ra) * t
                ox, oy = cx - (ax + t * dx), cy - (ay + t * dy)
                if math.hypot(ox, oy) <= rr:
                    self.p(x, y, self._tom(base, (ox * self.lx + oy * self.ly) / rr, luz, sombra))

    def tronco(self, ombros, cintura, y0, base, borda=2):
        """O tronco de costas: dos ombros (x0, x1 em y0) à cintura (x0, x1 no fim do quadro), a borda virada para a
        luz acesa e a de lá na sombra."""
        (a0, a1), (b0, b1) = ombros, cintura
        for y in range(y0, QH):
            t = (y - y0) / (QH - y0)
            x0, x1 = round(a0 + (b0 - a0) * t), round(a1 + (b1 - a1) * t)
            for x in range(x0, x1 + 1):
                lado = (x - x0) if self.lx < 0 else (x1 - x)
                outro = (x1 - x) if self.lx < 0 else (x - x0)
                self.p(x, y, base + "Luz" if lado < borda and y < y0 + 10 else base + "Sombra" if outro < 3 else base)

    def desenhar(self, t):
        for (x, y), c in self.px.items():
            t.px(x, y, c)


def fregues_esquerda(px):
    """Sentado ao balcão, à esquerda, de três quartos de costas, virado para o taverneiro: a cabeça (o cabelo, a
    orelha e a bochecha do lado do balcão), o pescoço, os ombros na capa verde-escura, as costas estreitando para a
    cintura; o braço de cá sai do ombro, o cotovelo pousa na borda do tampo e o antebraço vai pelo tampo até a caneca. A
    lareira, atrás e à esquerda, acende o contorno de cima."""
    v = Vulto(-0.7, -0.7)
    v.tronco((-8, 36), (-6, 32), 68, "capa")
    v.elipse(34, 71, 6.5, 5.2, "capa")                       # o ombro de cá, redondo
    v.membro((35, 72), (46, 82), 6, 5.5, "capa")             # o braço, até o cotovelo na borda do tampo
    v.membro((46, 81), (60, 73), 4.5, 3.5, "capa")           # o antebraço no tampo
    v.elipse(62, 72, 3, 2.8, "pele")                         # a mão na caneca
    v.membro((15, 61), (16, 68), 5.5, 6, "pele")             # o pescoço
    for x in range(3, 30):                                   # a gola da capa em volta do pescoço
        y = 67 + round(abs(x - 16) / 6)
        v.p(x, y, "capaLuz" if x < 16 else "capa")
    v.elipse(15, 53, 9, 10.5, "cabelo")                      # a cabeça
    for x, y in ((22, 51), (23, 52), (23, 53), (23, 54), (23, 55), (22, 56), (22, 57), (21, 58), (21, 59)):
        v.p(x, y, "pele" if y < 57 else "cabelo")            # a bochecha e a barba rala, do lado do balcão
    v.p(23, 53, "peleLuz")
    v.p(23, 54, "peleLuz")
    for y in (52, 53, 54, 55):                               # a orelha
        v.p(20, y, "pele" if y in (52, 55) else "peleSombra")
    for x, y in ((8, 46), (13, 44), (6, 51), (17, 45), (10, 49)):  # o crespo
        v.p(x, y, "cabeloLuz")
    px.linha(13, 76, 17, 95, FG["capaSombra"])               # a dobra das costas
    v.desenhar(px.t)


def fregues_direita(px):
    """Sentado ao balcão, à direita, de três quartos de costas, virado para o taverneiro: o capuz (a ponta caída para
    trás, a abertura para a esquerda, o rosto no escuro), os ombros no gibão, as costas estreitando para a cintura; o
    braço de cá vai do ombro ao cotovelo na borda do tampo e o antebraço até a caneca. O lampião, em cima e à direita,
    acende a borda do capuz e o ombro de lá."""
    v = Vulto(0.7, -0.7)
    v.tronco((211, 256), (215, 258), 69, "gibao")
    v.elipse(215, 72, 6.5, 5.2, "gibao")                     # o ombro de cá
    v.membro((214, 73), (207, 82), 6, 5.5, "gibao")          # o braço, até o cotovelo na borda do tampo
    v.membro((207, 81), (204, 74), 4.5, 3.5, "gibao")        # o antebraço no tampo
    v.elipse(203, 72, 3, 2.8, "pele")                        # a mão na caneca
    # a gola do capuz em volta do pescoço, caindo nos ombros
    for x in range(216, 253):
        y = 67 + round(abs(x - 234) / 7)
        v.p(x, y, "capuzLuz" if x > 242 else "capuz")
        v.p(x, y + 1, "capuzSombra")
    v.elipse(234, 55, 9.5, 11, "capuz")                      # o capuz
    for y in range(47, 66):                                  # a ponta caída para trás e para cima
        for x in range(237, 250):
            if (x - 237) < (y - 45) * 0.6 and ((x + 0.5 - 234) / 13) ** 2 + ((y + 0.5 - 55) / 11) ** 2 <= 1:
                v.p(x, y, "capuzLuz" if x > 245 else "capuz")
    for y in range(48, 64):                                  # a abertura para a esquerda, com o escuro de dentro
        meia = 3.8 * math.sqrt(max(0.0, 1 - ((y + 0.5 - 56) / 8) ** 2))
        for x in range(round(227 - meia), round(227 + meia)):
            v.p(x, y, "dentro")
        v.p(round(227 + meia), y, "capuzSombra")
    v.p(225, 57, "pele")                                     # a ponta do nariz, no escuro
    v.p(225, 58, "peleSombra")
    px.linha(238, 76, 241, 95, FG["gibaoSombra"])            # a dobra das costas
    v.desenhar(px.t)


# ---------------------------------------------------------------- a luz
LUZES = [  # (x, y, raio, força): a lareira, o lampião, a luz geral sobre o balcão
    (20, 48, 66, 1.0), (275, 30, 46, 0.9), (150, 46, 96, 0.55),
]


def luz(t):
    """A luz da G (os degraus pontilhados longe das fontes, o halo quente em anéis), com as fontes no lugar da H."""
    salvas = G.LUZES[:]
    G.LUZES[:] = LUZES
    try:
        return G.luz(t)
    finally:
        G.LUZES[:] = salvas


def luz_lisa(t, escuro=0.1, quente=0.05):
    """A luz de quem está no meio da cena (o taverneiro): um tom só, sem pontilhado, com o calor da lareira e do lampião
    por igual; a modelagem fica nos planos de luz e sombra do próprio desenho."""
    for y in range(QH):
        for x in range(QW):
            if t.a[y, x, 3]:
                t.mistura(x, y, (4, 3, 4), escuro)
                t.mistura(x, y, (255, 150, 70), quente)
    return t


# ---------------------------------------------------------------- as camadas
def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    sala(px)
    # o canto de preparo da G (a lareira elevada, a concha, a frigideira), um pouco para a esquerda e para cima
    de_g(t, G.lareira, (0, 7, 57, 69), -6, -8)
    de_g(t, G.utensilios, (0, 30, 57, 60), -6, -8)
    bancada(px)
    prateleiras(px)
    # a louça, as garrafas e as canecas penduradas da G, nas prateleiras novas
    de_g(t, G.objetos_prateleira, (62, 8, 136, G.PR), -12, PR - G.PR)
    de_g(t, G.objetos_prateleira, (176, 8, 234, G.PR), -6, PR - G.PR)
    de_g(t, G.canecas_penduradas, (104, G.PR + 3, 130, G.PR + 16), -12, PR - G.PR)
    # o barril no berço e a jarra, na bancada
    de_g(t, G.barril, (60, 36, 114, G.BB), -12, BB - G.BB)
    de_g(t, G.comida_e_jarra, (196, 40, 210, G.BB), -10, BB - G.BB)
    esteio(px, 47, 7, BT)
    esteio(px, 284, 7, QH)
    de_g(t, G.pendurados, (230, 4, 258, 44), 14, -1)
    despensa(px)
    lampiao(px)
    return luz(t)


def camada_caldeirao():
    t = Tela(QW, QH)
    de_g(t, G.caldeirao, (0, 30, 57, 69), -6, -8)
    return luz(t)


def frente():
    t = Tela(QW, QH)
    px = Pincel(t)
    balcao(px)
    tabua_do_pao(px)
    caneca_esquerda(px)
    caneca_direita(px)
    luz(t)
    gente = Tela(QW, QH)
    pg = Pincel(gente)
    fregues_esquerda(pg)
    fregues_direita(pg)
    t.sobre(gente)  # os fregueses têm a luz deles no desenho (o escuro com o contorno aceso)
    return t


def fogo(i):
    t = Tela(QW, QH)
    de_g(t, lambda px: G.chamas(i), (0, 30, 57, 69), -6, -8)
    return t


def lampiao_chama(i):
    return chama_lampiao(i)
