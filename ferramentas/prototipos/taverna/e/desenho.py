"""A taverna do Vau, candidata E (estudo estático): o salão reconstruído numa projeção só, na grade de 320×96.

Por que outra construção (o histórico em ../LEIA-ME.md): da B à D, o piso seguia uma perspectiva verdadeira com o olho
baixo, mas os tampos, os assentos, o balcão e a galeria mostravam a face de cima em quantidades escolhidas uma a uma;
a parede parecia frontal e os móveis, cada um num grau. Ajustar as pessoas no lugar não resolvia: a escala de Morel e
a da mesa do lado não concordavam.

**A projeção** (a mesma para tudo, em `P`): um ponto a X metros do eixo da sala (negativo à esquerda), Z metros à
frente da parede do fundo e H metros de altura cai em

    x = 160 + X · m(Z)        y = PAREDE + PISO · Z − H · m(Z)        m(Z) = M0 + M1 · Z

uma perspectiva simplificada e consistente: a câmera um pouco elevada (cada metro de piso desce PISO px; as faces de
cima de mesas, bancos, degraus e da galeria aparecem pela mesma conta), a escala crescendo pouco do fundo (14 px/m) à
borda de baixo (22), e as paredes do lado convergindo. Os móveis são caixas projetadas (`caixa`): a face de cima, a da
frente e a do lado que olha para o meio da sala.

**A planta** (em metros; a sala tem 16 de largura):
- no fundo, da esquerda para a direita: a porta da despensa (atrás do balcão), a porta da rua, a lareira, a escada
  encostada na parede subindo até o patamar e a galeria dos quartos, com duas portas;
- à esquerda, o balcão (a 3 m do fundo), o taverneiro atrás dele e o aparador com as prateleiras; na frente, a mesa
  comprida com três;
- à direita, a mesa redonda dos jogadores e, contra a parede do lado, o banco de espaldar e a mesa de Morel;
- no meio, a passagem livre da porta da rua até a frente, o balcão, as mesas e o pé da escada.

As camadas: `fundo(com_morel)` (a sala, os móveis, as pessoas do estudo e a luz), `fogo(i)` e `velas(i)` por cima."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "hud", "forja", "h2"))
from tela_h2 import Tela  # noqa: E402  (a mesma camada de pixels das fontes da forja)

QW, QH = 320, 96
PAREDE = 56        # onde a parede do fundo encontra o piso
PISO = 5.33        # quanto o piso desce por metro para a frente
M0, M1 = 14.0, 1.0  # a escala: 14 px/m no fundo, +1 por metro para a frente
LARGURA = 8.0      # meia largura da sala (as paredes do lado em X = ±8)


def m(Z):
    return M0 + M1 * Z


def P(X, Z, H=0.0):
    """O ponto da sala (X à direita do eixo, Z à frente do fundo, H de altura) no quadro."""
    return (160 + X * m(Z), PAREDE + PISO * Z - H * m(Z))


def Zdo(y):
    """A profundidade do piso que cai na linha y."""
    return (y - PAREDE) / PISO


C = {
    "pedra": "#34373c", "pedraLuz": "#43464c", "pedraSombra": "#27292d", "junta": "#2d2f34",
    "lareira": "#4e4a46", "lareiraLuz": "#625c55", "lareiraEsc": "#3a3632", "fuligem": "#1a1614",
    "reboco": "#5c5447", "rebocoLuz": "#6a6152", "rebocoSombra": "#4a443a",
    "viga": "#3a2a1e", "vigaLuz": "#503a28", "vigaEsc": "#24190f",
    "movel": "#6e4a2c", "movelLuz": "#8c6238", "movelEsc": "#47301c", "movelTopo": "#9a7044",
    "tabua": "#40322a", "tabuaJunta": "#382b23", "contato": "#1e1812",
    "ferro": "#33343a", "ferroLuz": "#5a5c64", "ferroEsc": "#1c1d22",
    "barro": "#7a4a30", "barroLuz": "#9a6440", "barroEsc": "#4e2e1e",
    "estanho": "#80838a", "estanhoLuz": "#b0b3ba", "estanhoEsc": "#55585e",
    "vidro": "#3e5a4a", "vidroLuz": "#6a8a74",
    "cera": "#d6ccae", "ceraEsc": "#a89e80", "chama": "#ffcc66", "chamaFora": "#e8782a", "chamaMiolo": "#fff2c4",
    "brasa": "#c8501a", "brasaEsc": "#7a2a10",
    "linho": "#b0a68e", "linhoLuz": "#d2c8b0", "linhoSombra": "#857b66",
    "pao": "#a8783a", "paoLuz": "#c89a52", "tigela": "#5a3018", "ensopado": "#8a5a30",
    "vulto": "#0d0b0a", "ref": "#8a9aa8", "refEsc": "#5a6a78",
}


class Pincel:
    def __init__(self, t):
        self.t = t

    def __call__(self, x, y, w=1, h=1, cor=None):
        if cor and w > 0 and h > 0:
            self.t.ret(int(round(x)), int(round(y)), int(round(w)), int(round(h)), C.get(cor, cor))

    def p(self, x, y, cor):
        self(x, y, 1, 1, cor)

    def linha(self, x0, y0, x1, y1, cor):
        n = max(abs(round(x1) - round(x0)), abs(round(y1) - round(y0)), 1)
        for i in range(n + 1):
            self.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), cor)

    def poligono(self, pts, cor):
        """Preenche o polígono (os centros dos pixels de dentro, par-ímpar)."""
        ys = [p[1] for p in pts]
        xs = [p[0] for p in pts]
        for y in range(max(0, math.floor(min(ys))), min(QH, math.ceil(max(ys)) + 1)):
            cy = y + 0.5
            cortes = []
            for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
                if (y0 <= cy < y1) or (y1 <= cy < y0):
                    cortes.append(x0 + (cy - y0) * (x1 - x0) / (y1 - y0))
            cortes.sort()
            for a, b in zip(cortes[::2], cortes[1::2]):
                xa, xb = max(math.ceil(a - 0.5), math.floor(min(xs))), min(math.floor(b - 0.5), math.ceil(max(xs)))
                if xb >= xa:
                    self(xa, y, xb - xa + 1, 1, cor)

    def grade(self, x0, y0, linhas, pal):
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])


def caixa(px, X0, X1, Z0, Z1, H0, H1, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz"):
    """Uma caixa da sala projetada: a face do lado que olha para o meio, a da frente e a de cima (nessa ordem), com a
    aresta clara entre a de cima e a da frente."""
    if X1 < 0 and lado:
        px.poligono([P(X1, Z0, H0), P(X1, Z1, H0), P(X1, Z1, H1), P(X1, Z0, H1)], lado)
    if X0 > 0 and lado:
        px.poligono([P(X0, Z0, H0), P(X0, Z1, H0), P(X0, Z1, H1), P(X0, Z0, H1)], lado)
    if frente:
        px.poligono([P(X0, Z1, H0), P(X1, Z1, H0), P(X1, Z1, H1), P(X0, Z1, H1)], frente)
    if topo:
        px.poligono([P(X0, Z0, H1), P(X1, Z0, H1), P(X1, Z1, H1), P(X0, Z1, H1)], topo)
    if aresta:
        (xa, ya), (xb, _) = P(X0, Z1, H1), P(X1, Z1, H1)
        px(round(xa), round(ya), round(xb) - round(xa), 1, aresta)


def sombra(px, X0, X1, Z0, Z1):
    """A sombra de contato no piso, embaixo de um móvel."""
    px.poligono([P(X0, Z0), P(X1, Z0), P(X1, Z1), P(X0, Z1)], "contato")


# ---------------------------------------------------------------- o espaço
def paredes(px):
    """O fundo de pedra em blocos largos, as paredes do lado em reboco com os esteios do enxaimel, a viga do teto."""
    xa, _ = P(-LARGURA, 0)
    xb, _ = P(LARGURA, 0)
    px(xa, 0, xb - xa, PAREDE, "pedra")
    for i, y in enumerate(range(PAREDE - 5, -1, -5)):
        px(xa, y, xb - xa, 1, "junta")
        for x in range(round(xa) + (i % 2) * 5, round(xb), 10):
            px(x, y + 1, 1, 4, "junta")
    px(xa, PAREDE - 1, xb - xa, 1, "pedraSombra")
    for lado in (-1, 1):
        Zfim = (160 / LARGURA - M0) / M1                     # onde a parede sai do quadro
        base = [P(lado * LARGURA, 0), P(lado * LARGURA, Zfim)]
        canto = 0 if lado < 0 else QW
        px.poligono([(canto, 0), (base[0][0], 0), base[0], base[1], (canto, base[1][1])], "reboco")
        for Ze in (0.0, 2.5, 5.0):                           # os esteios do enxaimel, em pé
            x, y = P(lado * LARGURA, Ze)
            px(round(x) - 1, 0, 3, round(y), "viga")
            px(round(x) - (1 if lado < 0 else -1), 0, 1, round(y), "vigaLuz")
        px.linha(base[0][0], base[0][1] - 1, base[1][0], base[1][1] - 1, "viga")     # o rodapé
        for H in (2.6,):                                     # a travessa do enxaimel, correndo para a frente
            (x0, y0), (x1, y1) = P(lado * LARGURA, 0, H), P(lado * LARGURA, Zfim, H)
            px.linha(x0, y0, x1, y1, "viga")
    px(0, 0, QW, 3, "vigaEsc")
    px(0, 2, QW, 1, "viga")


def piso(px):
    """O piso de tábuas paralelas ao fundo, as juntas um tom só abaixo, a cada 0,75 m; as emendas, desencontradas,
    correndo para a frente pela mesma projeção."""
    Zfim = (160 / LARGURA - M0) / M1
    px.poligono([P(-LARGURA, 0), P(LARGURA, 0), P(LARGURA, Zfim), (QW, QH), (0, QH), P(-LARGURA, Zfim)], "tabua")
    Z = 0.75
    n = 0
    while PAREDE + PISO * Z < QH:
        y = round(PAREDE + PISO * Z)
        xa = max(0, P(-LARGURA, Z)[0])
        xb = min(QW, P(LARGURA, Z)[0])
        px(xa, y, xb - xa, 1, "tabuaJunta")
        for i in range(-8, 9):
            X = i * 2.0 + (n % 2)
            (x0, y0), (x1, y1) = P(X, Z), P(X, Z + 0.75)
            if abs(X) < LARGURA and y1 < QH:
                px.linha(x0, y0 + 1, x1, y1 - 1, "tabuaJunta")
        Z += 0.75
        n += 1


def porta(px, X0, X1, alto, arco=True, fresta=0.0):
    """Uma porta de tábuas na parede do fundo (em arco ou reta): o batente, as ferragens, a argola, a soleira;
    `fresta` (em metros) a deixa entreaberta, com o escuro do outro lado."""
    (x0, base), (x1, _) = P(X0, 0), P(X1, 0)
    x0, x1, base = round(x0), round(x1), round(base)
    topo = round(base - alto * m(0))
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    abre = round(fresta * m(0))
    for y in range(topo - (round(r) if arco else 0) - 2, base):
        for x in range(x0 - 2, x1 + 2):
            d = math.hypot(x + 0.5 - cx, max(0, topo - y - 0.5)) if arco else 0
            if arco and y < topo and d > r + 2:
                continue
            if not arco and y < topo - 2:
                continue
            dentro = (x0 <= x < x1) and (y >= topo or (arco and d <= r))
            if not dentro:
                px.p(x, y, "pedraLuz" if arco else "vigaEsc")
            elif x >= x1 - abre:
                px.p(x, y, "vulto")
            else:
                px.p(x, y, "vigaEsc" if (x - x0) % 4 == 3 else "movelLuz" if (x - x0) % 4 == 0 else "movel")
    for yy in (topo + 2, base - 7):
        px(x0, yy, x1 - x0 - abre, 1, "ferro")
    px(x1 - abre - 3, (topo + base) // 2, 2, 2, "ferroLuz")
    px(x0 - 2, base, x1 - x0 + 4, 1, "pedraLuz")
    return x0, x1, topo


# ---------------------------------------------------------------- a lareira
LAREIRA = (0.2, 2.8)   # o peito de pedra na parede do fundo: de X0 a X1


def lareira(px):
    """A lareira saindo 0,5 m da parede: a laje no piso, o peito com as ombreiras (a espessura), a boca funda (as faces
    de dentro e o fundo de fuligem), a verga fina com a prateleira, a coifa e a chaminé até a viga."""
    X0, X1 = LAREIRA
    caixa(px, X0 - 0.3, X1 + 0.3, 0.5, 1.1, 0.0, 0.06, topo="lareiraLuz", frente="lareiraEsc", lado="lareiraEsc",
          aresta=None)                                       # a laje
    caixa(px, X0, X1, 0.0, 0.5, 0.0, 1.35, topo="lareira", frente="lareira", lado="lareiraEsc", aresta="lareiraLuz")
    (xa, ya), (xb, yb) = P(X0, 0.5, 1.35), P(X1, 0.5, 0)
    for y in range(round(ya) + 4, round(yb), 4):             # as fiadas do peito
        px(xa, y, xb - xa, 1, "lareiraEsc")
    b0, b1 = X0 + 0.7, X1 - 0.7                             # a boca
    (x0, yt), (x1, yp) = P(b0, 0.5, 1.0), P(b1, 0.5, 0)
    x0, x1, yt, yp = round(x0), round(x1), round(yt), round(yp)
    px(x0, yt, x1 - x0, yp - yt, "fuligem")
    for y in range(yt, yp):
        f = min(4, (y - yt) // 3 + 2)
        px(x0, y, f, 1, "lareiraEsc")
        px(x1 - f, y, f, 1, "lareiraEsc")
        px(x0 + f - 1, y, 1, 1, "brasaEsc")
        px(x1 - f, y, 1, 1, "brasaEsc")
    px(x0 - 1, yt, 1, yp - yt, "lareiraLuz")
    px(x1, yt, 1, yp - yt, "lareiraLuz")
    px(x0 - 1, yt - 1, x1 - x0 + 2, 1, "lareiraLuz")
    (xv, yv), (xw, _) = P(X0 - 0.1, 0.55, 1.4), P(X1 + 0.1, 0.55, 1.4)   # a verga fina e a prateleira
    px(xv, yv - 1, xw - xv, 1, "movelLuz")
    px(xv, yv, xw - xv, 1, "movelEsc")
    px(xv + 5, yv - 5, 3, 4, "barro"); px(xv + 5, yv - 5, 1, 4, "barroLuz")
    cx = (P(X0, 0.3)[0] + P(X1, 0.3)[0]) / 2               # a coifa e a chaminé
    for y in range(3, round(yv) - 1):
        meia = 6 if y < round(yv) - 12 else round(6 + (y - (round(yv) - 12)) * ((xw - xv) / 2 - 8) / 12)
        px(cx - meia, y, 2 * meia, 1, "lareira")
        px(cx - meia, y, 1, 1, "lareiraLuz")
        px(cx + meia - 1, y, 1, 1, "lareiraEsc")
        if y % 5 == 0:
            px(cx - meia + 1, y, 2 * meia - 2, 1, "lareiraEsc")
    for i, n in enumerate((3, 2)):                           # a lenha empilhada à esquerda
        for j in range(n):
            x, y = P(X0 - 0.95 + j * 0.28 + i * 0.14, 0.4, 0.22 + i * 0.25)
            px(round(x), round(y), 4, 4, "movelEsc")
            px(round(x), round(y), 3, 3, "movelLuz")
            px(round(x) + 1, round(y) + 1, 1, 1, "movel")
    return (x0 + x1) // 2, yp


# ---------------------------------------------------------------- a escada e a galeria
ESCADA = (3.3, 5.6, 0.0, 0.9, 10)   # a escada: de X0 (o pé) a X1 (o patamar), a faixa de Z, os degraus
GALERIA = (5.6, 8.0, 0.0, 1.4, 2.2)  # a galeria: de X0 a X1, de Z0 (a parede) a Z1 (a borda), a altura do piso
PORTAS = ((5.85, 6.75), (7.0, 7.9))  # as portas dos quartos, na parede do fundo, em cima da galeria


def escada_e_galeria(px):
    """A galeria: as portas dos quartos na parede, o piso visto de cima (a faixa por onde se anda até elas, ligada ao
    patamar), a testeira com as pontas das vigas (a espessura), dois esteios com mãos-francesas e o guarda-corpo
    discreto. A escada: os degraus (o piso largo, o espelho baixo, na mesma projeção), o banzo de fora, o corrimão nos
    balaústres, o pilar do pé no chão e o do patamar, que é o primeiro esteio da galeria."""
    G0, G1, GZ0, GZ1, GH = GALERIA
    for d0, d1 in PORTAS:                                   # as portas dos quartos (1,65 m)
        (x0, yb), (x1, _) = P(d0, 0, GH), P(d1, 0, GH)
        x0, x1, yb = round(x0), round(x1), round(yb)
        topo = round(yb - 1.65 * m(0))
        px(x0 - 1, topo - 1, x1 - x0 + 2, yb - topo + 1, "vigaEsc")
        for x in range(x0, x1):
            px(x, topo, 1, yb - topo, "movelEsc" if (x - x0) % 3 == 2 else "movel")
        px(x0, topo, 1, yb - topo, "movelLuz")
        px(x0, topo + 2, x1 - x0, 1, "ferro"); px(x0, yb - 4, x1 - x0, 1, "ferro")
        px(x1 - 3, (topo + yb) // 2, 2, 2, "ferroLuz")
    # o piso da galeria (a face de cima), a testeira (a espessura) e as pontas das vigas
    caixa(px, G0, G1, GZ0, GZ1, GH - 0.25, GH, topo="movelTopo", frente="viga", lado=None, aresta="movelLuz")
    (xa, yf), (xb, _) = P(G0, GZ1, GH - 0.25), P(G1, GZ1, GH - 0.25)
    for x in range(round(xa) + 3, round(xb), 7):
        px(x, round(yf) - 3, 2, 2, "vigaEsc")
    for Z in (0.45, 0.9):                                  # as tábuas do piso da galeria, correndo de lado
        (x0, y0), (x1, _) = P(G0, Z, GH), P(G1, Z, GH)
        px(x0, y0, x1 - x0, 1, "movel")
    # os esteios até o chão, com as sapatas de pedra e as mãos-francesas
    for Xe in (G0, G1 - 0.15):
        (x, yt), (_, yp) = P(Xe, GZ1, GH - 0.25), P(Xe, GZ1, 0)
        px(round(x) - 1, round(yt), 3, round(yp - yt), "viga")
        px(round(x) - 1, round(yt), 1, round(yp - yt), "vigaLuz")
        px(round(x) - 2, round(yp) - 2, 5, 2, "pedraLuz")
        px(round(x) - 3, round(yp), 7, 1, "contato")
        for i in range(4):
            px.p(round(x) + 2 + i, round(yt) + i, "viga")
            if Xe > G0:
                px.p(round(x) - 2 - i, round(yt) + i, "viga")
    # o guarda-corpo (0,9 m) na borda: o corrimão fino e os balaústres espaçados
    (xa, yr), (xb, _) = P(G0, GZ1, GH + 0.9), P(G1, GZ1, GH + 0.9)
    px(xa, yr, xb - xa, 1, "movel")
    for X in [G0 + 0.3 * i for i in range(1, 30)]:
        if X > G1 - 0.1:
            break
        (x, y0), (_, y1) = P(X, GZ1, GH + 0.9), P(X, GZ1, GH)
        px(round(x), round(y0) + 1, 1, round(y1 - y0) - 1, "vigaEsc")
    # a escada: os degraus, de baixo para cima
    X0, X1, Z0, Z1, n = ESCADA
    for i in range(n):
        Xa, Xb = X0 + i * (X1 - X0) / n, X0 + (i + 1) * (X1 - X0) / n
        Ha, Hb = i * GH / n, (i + 1) * GH / n
        caixa(px, Xa, Xb + 0.02, Z0, Z1, Ha, Hb, topo="movelTopo", frente="movelEsc", lado=None, aresta="movelLuz")
    for d in range(2):                                       # o banzo de fora, por baixo dos degraus
        (x0, y0), (x1, y1) = P(X0, Z1, 0), P(X1, Z1, GH)
        px.linha(x0, y0 + d, x1, y1 + d, "viga" if d else "vigaLuz")
    for i in range(0, n + 1, 2):                             # os balaústres e o corrimão
        X = X0 + i * (X1 - X0) / n
        (x, y0), (_, y1) = P(X, Z1, i * GH / n + 0.9), P(X, Z1, i * GH / n)
        px(round(x), round(y0), 1, round(y1 - y0), "movel")
    (x0, y0), (x1, y1) = P(X0, Z1, 0.9), P(X1, Z1, GH + 0.9)
    px.linha(x0, y0, x1, y1, "movelLuz")
    for Xp, Hp in ((X0, 0.0), (X1, 0.0)):                    # os pilares: o do pé e o do patamar
        (x, yt), (_, yp) = P(Xp, Z1, (Hp if Xp == X0 else GH) + 1.0), P(Xp, Z1, 0)
        px(round(x) - 1, round(yt), 3, round(yp - yt), "viga")
        px(round(x) - 1, round(yt), 1, round(yp - yt), "vigaLuz")
        px(round(x) - 2, round(yt) - 1, 5, 1, "movelLuz")
        px(round(x) - 2, round(yp), 6, 1, "contato")


# ---------------------------------------------------------------- o balcão
DESPENSA = (-4.4, -3.6)              # a porta da despensa, na parede do fundo, na ponta de trás do balcão
RUA = (-2.4, -1.2)                   # a porta da rua
BALCAO = (-7.6, -4.4, 3.0, 3.6)      # o balcão: de X0 a X1, de Z0 a Z1 (a frente), 1,05 m
APARADOR = (-7.6, -4.8, 2.0, 2.4)   # o aparador com as prateleiras, atrás do taverneiro


def aparador(px):
    """O aparador atrás do balcão (0,9 m) com duas prateleiras em cima, nos montantes: poucos objetos de silhueta
    própria (as canecas com a asa, a jarra bojuda, as garrafas de gargalo fino, a bilha)."""
    X0, X1, Z0, Z1 = APARADOR
    caixa(px, X0, X1, Z0, Z1, 0, 0.9)
    for X in (X0 + 0.05, X1 - 0.12):                         # os montantes até 2,1 m
        (x, yt), (_, yp) = P(X, Z0 + 0.1, 2.1), P(X, Z0 + 0.1, 0.9)
        px(round(x), round(yt), 2, round(yp - yt), "movelEsc")
    for H in (1.45, 2.0):                                    # as tábuas
        (xa, y), (xb, _) = P(X0, Z0 + 0.1, H), P(X1, Z0 + 0.1, H)
        px(xa, y, xb - xa, 2, "movel")
        px(xa, y, xb - xa, 1, "movelLuz")
    def obj(X, H):
        return [round(v) for v in P(X, Z0 + 0.1, H)]
    for X in (-7.3, -6.9):                                   # as canecas, com a asa
        x, y = obj(X, 2.0)
        px(x, y - 4, 3, 4, "estanho"); px(x, y - 4, 1, 4, "estanhoLuz"); px(x + 3, y - 3, 1, 2, "estanhoEsc")
    x, y = obj(-6.3, 2.0)                                    # a jarra bojuda
    px(x + 1, y - 7, 2, 1, "barroEsc"); px(x, y - 6, 4, 1, "barro"); px(x - 1, y - 5, 6, 5, "barro")
    px(x - 1, y - 5, 1, 5, "barroLuz"); px(x + 5, y - 5, 1, 3, "barroEsc")
    for X in (-5.6, -5.3):                                   # as garrafas
        x, y = obj(X, 2.0)
        px(x, y - 5, 3, 5, "vidro"); px(x, y - 5, 1, 5, "vidroLuz"); px(x + 1, y - 8, 1, 3, "vidro"); px(x + 1, y - 9, 1, 1, "barroEsc")
    x, y = obj(-7.2, 1.45)                                   # a bilha
    px(x, y - 5, 4, 5, "barro"); px(x, y - 5, 1, 5, "barroLuz"); px(x + 1, y - 6, 2, 1, "barroEsc")
    x, y = obj(-5.4, 1.45)                                   # um prato de pé
    px(x + 1, y - 6, 1, 6, "linho"); px(x, y - 5, 3, 4, "linho"); px(x, y - 5, 1, 4, "linhoLuz")
    sombra(px, X0, X1, Z0, Z1)


def balcao(px):
    """O balcão (1,05 m): a face de cima clara (o tampo, com a borda grossa), a frente em almofadas, o lado da ponta que
    olha para a sala; o barril de torneira em cima, na ponta da parede."""
    X0, X1, Z0, Z1 = BALCAO
    sombra(px, X0, X1 + 0.1, Z0, Z1 + 0.1)
    caixa(px, X0, X1, Z0, Z1, 0, 0.95, topo=None, frente="movelEsc", lado="vigaEsc", aresta=None)
    (xa, ya), (xb, yb) = P(X0, Z1, 0.9), P(X1, Z1, 0.1)
    w = (xb - xa) / 4
    for i in range(4):                                       # as almofadas
        a, b = round(xa + i * w + 2), round(xa + (i + 1) * w - 2)
        px(a, round(ya) + 2, b - a, round(yb - ya) - 3, "vigaEsc")
        px(a + 1, round(ya) + 3, b - a - 2, round(yb - ya) - 5, "movel")
    caixa(px, X0 - 0.05, X1 + 0.05, Z0 - 0.05, Z1 + 0.05, 0.95, 1.05, topo="movelTopo", frente="movelLuz",
          lado="movel", aresta="movelLuz")                   # o tampo grosso
    x, y = [round(v) for v in P(X0 + 0.4, Z0 + 0.3, 1.05)]  # o barril deitado, com a torneira
    px(x, y - 6, 9, 6, "movel"); px(x, y - 6, 9, 1, "movelLuz"); px(x, y - 1, 9, 1, "movelEsc")
    for xx in (x + 2, x + 6):
        px(xx, y - 6, 1, 6, "ferro")
    px(x + 9, y - 4, 2, 1, "ferroLuz")


# ---------------------------------------------------------------- as mesas e os assentos
def perna(px, X, Z, H, larg=0.07):
    (x, yt), (_, yp) = P(X, Z, H), P(X, Z, 0)
    px(round(x), round(yt), max(1, round(larg * m(Z))), round(yp - yt), "movel")


def mesa(px, X0, X1, Z0, Z1, H=0.75):
    """Uma mesa de tábuas: as pernas de trás, o tampo (a face de cima, a borda), as pernas da frente, a travessa."""
    sombra(px, X0 + 0.05, X1 - 0.05, Z0 + 0.05, Z1 - 0.02)
    for X in (X0 + 0.05, X1 - 0.12):
        perna(px, X, Z0 + 0.06, H)
    caixa(px, X0, X1, Z0, Z1, H - 0.05, H, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz")
    for X in (X0 + 0.05, X1 - 0.12):
        perna(px, X, Z1 - 0.06, H - 0.05)
    (xa, yt), (xb, _) = P(X0 + 0.1, Z1 - 0.06, 0.18), P(X1 - 0.1, Z1 - 0.06, 0.18)
    px(xa, yt, xb - xa, 1, "movelEsc")


def mesa_redonda(px, X, Z, raio=0.5, H=0.75):
    """A mesa redonda de um pé: o tampo (a elipse da face de cima, pela mesma projeção), a borda, o pé e a base."""
    sombra(px, X - 0.3, X + 0.3, Z - 0.2, Z + 0.2)
    perna(px, X - 0.04, Z, H, larg=0.1)
    (xb0, yb), (xb1, _) = P(X - 0.3, Z, 0.03), P(X + 0.3, Z, 0.03)
    px(xb0, yb, xb1 - xb0, 1, "movelEsc")
    pts = []
    for i in range(24):
        a = 2 * math.pi * i / 24
        pts.append(P(X + raio * math.cos(a), Z + raio * math.sin(a), H))
    borda = [P(X + raio * math.cos(2 * math.pi * i / 24), Z + raio * math.sin(2 * math.pi * i / 24), H - 0.05)
             for i in range(24)]
    px.poligono(borda, "movel")
    px.poligono(pts, "movelTopo")
    return pts


def banco(px, X0, X1, Z0, Z1, H=0.45, encosto=None):
    """Um banco (ou banquinho) de tábua: as pernas, o assento (a face de cima e a borda); `encosto` ("direita") põe o
    espaldar alto na ponta da direita, de lado, como o do canto de Morel."""
    sombra(px, X0, X1, Z0, Z1)
    for X in (X0 + 0.04, X1 - 0.1):
        for Z in (Z0 + 0.05, Z1 - 0.05):
            perna(px, X, Z, H - 0.04, larg=0.06)
    caixa(px, X0, X1, Z0, Z1, H - 0.05, H, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz")
    if encosto == "fundo":                                   # o espaldar alto atrás do assento (encostado na parede)
        caixa(px, X0, X1, Z0 - 0.08, Z0, H, H + 0.75, topo="movelLuz", frente="movel", lado="movelEsc", aresta=None)


def castical(px, X, Z, H=0.75):
    x, y = [round(v) for v in P(X, Z, H)]
    px(x - 1, y - 1, 4, 1, "barro")
    px(x, y - 5, 2, 4, "cera")
    px(x + 1, y - 5, 1, 4, "ceraEsc")
    return (x, y - 6)


# Os grupos, em metros (as pessoas de gente.py sentam nestes móveis)
MESA_LONGA = (-5.2, -2.2, 5.5, 6.3)     # a mesa comprida da esquerda
BANCO_LONGE = (-5.0, -2.6, 4.95, 5.3)    # o banco do outro lado
BANCO_PERTO = (-4.9, -2.4, 6.75, 7.1)    # o banco da frente
CADEIRA_PONTA = (-1.95, -1.55, 5.7, 6.1)  # a cadeira da cabeceira (a da direita)
REDONDA = (2.7, 5.2)                     # a mesa redonda: o centro
BANCO_RODA_ATRAS = (2.45, 2.95, 4.4, 4.75)
BANCO_RODA_LADO = (1.65, 2.05, 5.05, 5.4)
BANCO_VAZIO = (3.45, 3.85, 5.85, 6.2)
MESA_MOREL = (5.5, 6.5, 4.0, 5.0)         # a mesa de Morel
BANCO_MOREL = (6.75, 7.55, 3.8, 5.2)     # o banco de espaldar, contra a parede da direita
BANQUINHO_FOGO = (-0.75, -0.35, 1.4, 1.75)  # o do velho, à esquerda da laje, virado para o fogo


def banco_morel(px):
    """O banco robusto de Morel, contra a parede da direita: o assento largo (0,8 m) e o espaldar alto do lado da
    parede, inteiro, de tábuas grossas."""
    X0, X1, Z0, Z1 = BANCO_MOREL
    sombra(px, X0, X1, Z0, Z1)
    caixa(px, X1 - 0.12, X1, Z0, Z1, 0, 1.25, topo="movelLuz", frente="movel", lado="movelEsc", aresta=None)
    for Z in (Z0 + 0.06, Z1 - 0.06):
        perna(px, X0 + 0.05, Z, 0.42, larg=0.09)
    caixa(px, X0, X1 - 0.12, Z0, Z1, 0.4, 0.47, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz")


def mesas(px, parte=None):
    """Os móveis dos grupos; `parte` desenha só um (para gente.py redesenhar por cima de quem está atrás)."""
    feito = {}
    if parte in (None, "morel"):
        banco_morel(px)
        mesa(px, *MESA_MOREL)
        x, y = [round(v) for v in P(6.25, 4.4, 0.75)]       # a tigela do ensopado, na ponta perto dele, e o pão
        px(x, y - 1, 7, 1, "ensopado"); px(x, y, 7, 1, "tigela"); px(x + 1, y + 1, 5, 1, "tigela")
        x, y = [round(v) for v in P(5.8, 4.3, 0.75)]
        px(x, y - 1, 5, 2, "pao"); px(x + 1, y - 1, 2, 1, "paoLuz")
        feito["vela_morel"] = castical(px, 5.65, 4.65)
    if parte in (None, "roda"):
        for b in (BANCO_RODA_ATRAS, BANCO_RODA_LADO):
            banco(px, *b)
    if parte in (None, "roda", "roda_mesa"):
        mesa_redonda(px, *REDONDA)
        x, y = [round(v) for v in P(REDONDA[0], REDONDA[1], 0.75)]
        px(x - 4, y - 1, 8, 3, "linhoSombra")                # o tabuleiro e as peças
        for xx in range(x - 4, x + 4, 2):
            px(xx, y - 1, 1, 1, "movelEsc"); px(xx + 1, y, 1, 1, "movelEsc"); px(xx, y + 1, 1, 1, "movelEsc")
        px(x - 2, y - 2, 1, 1, "linhoLuz"); px(x + 2, y - 2, 1, 1, "vigaEsc")
        feito["vela_roda"] = castical(px, REDONDA[0] + 0.35, REDONDA[1] + 0.15)
    if parte in (None, "roda"):
        banco(px, *BANCO_VAZIO)
    if parte in (None, "longa_fundo"):
        banco(px, *BANCO_LONGE)
    if parte in (None, "longa"):
        mesa(px, *MESA_LONGA)
        x, y = [round(v) for v in P(-4.3, 5.85, 0.75)]       # a tábua com o pão, a jarra, a vela
        px(x, y, 10, 2, "movelEsc"); px(x + 1, y - 1, 8, 2, "pao"); px(x + 2, y - 1, 3, 1, "paoLuz")
        x, y = [round(v) for v in P(-3.2, 5.75, 0.75)]
        px(x, y - 5, 4, 5, "barro"); px(x, y - 5, 1, 5, "barroLuz"); px(x + 1, y - 6, 2, 1, "barroEsc")
        feito["vela_longa"] = castical(px, -2.55, 5.8)
    if parte in (None, "cadeira_ponta"):
        X0, X1, Z0, Z1 = CADEIRA_PONTA
        banco(px, X0, X1, Z0, Z1)
        caixa(px, X1 - 0.06, X1, Z0, Z1, 0.45, 1.0, topo="movelLuz", frente="movel", lado="movelEsc", aresta=None)
    if parte in (None, "longa_perto"):
        banco(px, *BANCO_PERTO)
    if parte in (None, "fogo"):
        banco(px, *BANQUINHO_FOGO, H=0.4)
    return feito


# ---------------------------------------------------------------- a figura de referência (o estudo de construção)
def referencia(px, X, Z, sentado=False, alto=1.75):
    """Uma pessoa de referência, cinza e sem detalhe, em pé ou sentada (o quadril a 0,45 m), para conferir a escala dos
    móveis, das portas e dos degraus em cada lugar da sala. Não entra na candidata."""
    mm = m(Z)
    x, yp = P(X, Z)
    cab = 0.24 * mm
    if sentado:
        quadril = yp - 0.45 * mm
        ombro = quadril - 0.55 * mm
        px(x - 0.2 * mm, ombro, 0.4 * mm, quadril - ombro, "ref")
        px(x - 0.2 * mm, quadril - 0.1 * mm, 0.45 * mm, 0.12 * mm, "refEsc")
    else:
        ombro = yp - 1.45 * mm
        px(x - 0.2 * mm, ombro, 0.4 * mm, 0.6 * mm, "ref")
        px(x - 0.15 * mm, ombro + 0.6 * mm, 0.3 * mm, yp - ombro - 0.6 * mm, "refEsc")
    px(x - cab / 2, ombro - cab - 1, cab, cab, "ref")


# ---------------------------------------------------------------- a luz
def luz(t, chamas, fogo):
    """O escuro cresce aos poucos longe do fogo e das velas (sem faixas); o calor cai suave perto deles."""
    fontes = [(fogo[0], fogo[1] - 6, 40, 1.0)] + [(x, y, 22, 0.6) for x, y in chamas]
    for y in range(QH):
        for x in range(QW):
            perto = max(f * max(0.0, 1 - math.hypot(x - fx, (y - fy) * 1.2) / (r * 2)) for fx, fy, r, f in fontes)
            escuro = max(0.0, 0.46 - perto * 1.05)
            if escuro > 0:
                t.mistura(x, y, (6, 5, 4), escuro)
            calor = max(f * max(0.0, 1 - ((x - fx) ** 2 + ((y - fy) * 1.2) ** 2) / (r * r)) * 0.12 for fx, fy, r, f in fontes)
            if calor > 0.004:
                t.mistura(x, y, (255, 160, 80), calor)


# ---------------------------------------------------------------- as camadas
LAMPIAO = (-6.0, 2.8, 2.5)   # o lampião pendurado na viga, sobre o balcão (X, Z, H da chama)


def lampiao(px):
    x, yc = [round(v) for v in P(*LAMPIAO)]
    for y in range(3, yc - 3, 2):
        px.p(x, y, "ferroLuz"); px.p(x, y + 1, "ferro")
    px(x - 2, yc - 3, 5, 1, "ferroLuz"); px(x - 2, yc - 2, 1, 4, "ferro"); px(x + 2, yc - 2, 1, 4, "ferro")
    px(x - 2, yc + 2, 5, 1, "ferroLuz")
    return (x, yc - 1)


def so_o_espaco():
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    piso(px)
    return t


def sala(px):
    """A sala com os móveis, sem as pessoas e sem a luz; devolve onde ficam as chamas e a boca da lareira."""
    paredes(px)
    piso(px)
    porta(px, *DESPENSA, 1.75, arco=False, fresta=0.25)    # a despensa, na ponta de trás do balcão
    porta(px, *RUA, 2.3)                                     # a porta da rua
    boca = lareira(px)
    escada_e_galeria(px)
    aparador(px)
    lamp = lampiao(px)
    balcao(px)
    feito = mesas(px)
    return {"chamas": [lamp, feito["vela_morel"], feito["vela_roda"], feito["vela_longa"]], "boca": boca}


def fogo(i):
    t = Tela(QW, QH)
    px = Pincel(t)
    cx, base = lareira(Pincel(Tela(QW, QH)))
    base -= 2
    linguas = [[(cx - 5, 5, 0), (cx - 2, 8, 1), (cx + 1, 9, 0), (cx + 4, 6, -1)],
               [(cx - 5, 6, 1), (cx - 2, 7, 0), (cx + 1, 8, -1), (cx + 4, 7, 0)],
               [(cx - 5, 4, 0), (cx - 2, 9, -1), (cx + 1, 8, 1), (cx + 4, 5, 0)],
               [(cx - 5, 5, -1), (cx - 2, 8, 0), (cx + 1, 10, 0), (cx + 4, 6, 1)]][i]
    for x, h, pende in linguas:
        for r in range(h):
            f = r / h
            dx = pende if f > 0.6 else 0
            larg = 3 if f < 0.45 else 2 if f < 0.8 else 1
            xa = x - larg // 2 + dx
            px(xa, base - r, larg, 1, "chamaFora")
            if larg >= 3:
                px(xa + 1, base - r, 1, 1, "chama")
            if r < 2 and h >= 7:
                px.p(x, base - r, "chamaMiolo")
    px(cx - 7, base + 1, 14, 2, "vigaEsc")
    px(cx - 7, base + 1, 2, 2, "brasa"); px(cx + 5, base + 1, 2, 2, "brasa")
    px.p(cx - 1 + (i % 2) * 2, base + 2, "brasa")
    px(cx, base - 12, 1, 3, "ferro")                         # o caldeirão, pequeno e alto
    px(cx - 3, base - 9, 7, 1, "ferroLuz"); px(cx - 3, base - 8, 7, 2, "ferro"); px(cx - 2, base - 6, 5, 1, "ferroEsc")
    return t


def velas(i):
    t = Tela(QW, QH)
    px = Pincel(t)
    for j, (x, y) in enumerate(sala(Pincel(Tela(QW, QH)))["chamas"]):
        f = (i + j * 3) % 4
        alto = 3 if f in (0, 2) else 2 if f == 1 else 4
        px(x, y - alto + 2, 1, alto, "chamaFora")
        px.p(x, y + 1, "chama")
        if alto >= 3:
            px.p(x, y, "chamaMiolo" if f == 3 else "chama")
    return t
