"""A taverna do Vau, candidata F (estudo estático): a composição da referência aprovada pelo Jean ("Taverna medieval
entre brasas e sombras", em ferramentas/arte/referencias/cenarios internos), transposta para a grade de 320×96 e para o
acabamento da forja, da curandeira e do templo. A imagem não é reduzida para virar cenário: ela foi medida na grade do
jogo (as posições, os tamanhos) e cada coisa foi construída aqui.

**A projeção** é a da E (uma conta só para tudo, em `P`), com outra câmera: mais perto e mais alta, como a da
referência. Um ponto a X metros do eixo, Z à frente da parede do fundo e H de altura cai em

    x = 160 + X · m(Z)        y = PAREDE + PISO · Z − H · m(Z)        m(Z) = M0 + M1 · Z

com 14 px por metro no fundo e 28 na borda de baixo; o olho a 3 m (PISO / M1), de onde se veem os tampos, os assentos,
os degraus e o piso da galeria. As pessoas da frente têm a cabeça de ~7 px, as do meio de 6, as do fundo de 4 a 5.

**A planta, pela referência** (em metros):
- no fundo, da esquerda para a direita: a porta da rua (fechada), as prateleiras e a porta da despensa atrás do balcão,
  a lareira grande com o caldeirão, e à direita a galeria dos quartos (duas portas), com a escada subindo da direita
  para a esquerda até o patamar;
- o balcão à esquerda (a 2 m do fundo), o taverneiro atrás dele, dois banquinhos vazios na frente;
- na frente à esquerda, a mesa comprida com três; no meio, a passagem até a lareira, com o velho que se aquece; à
  direita, a mesa redonda dos jogadores; na beira direita, Morel na cadeira de espaldar, com a mesa dele inteira.

**O que não veio da referência:** os estandartes, a cabeça de cervo, o tapete, as armas e a armadura de Morel (ele segue
a aparência do jogo); a galeria baixa demais para a profundidade em que fica (aqui ela tem a altura que a projeção dá:
2,1 m, com as portas inteiras); a mesa de Morel cortada pela borda.

As camadas: `fundo(com_morel)`, `fogo(i)` e `velas(i)`. As pessoas são desenhadas à mão em gente.py."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "hud", "forja", "h2"))
from tela_h2 import Tela  # noqa: E402  (a mesma camada de pixels das fontes da forja)

QW, QH = 320, 96
PAREDE = 54        # onde a parede do fundo encontra o piso
PISO = 7.5         # quanto o piso desce por metro para a frente (o olho a PISO / M1 = 3 m)
M0, M1 = 14.0, 2.5  # a escala: 14 px/m no fundo, 28 na borda de baixo
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
    "laje": "#3c3a38", "lajeLuz": "#46433f", "lajeJunta": "#2c2a28",
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
    """O piso de lajes de pedra, como o da referência: fiadas paralelas ao fundo (mais baixas longe), as lajes
    desencontradas, as juntas um tom abaixo e a aresta de cima de cada laje um tom acima, sem textura dentro delas."""
    Zfim = (160 / LARGURA - M0) / M1
    px.poligono([P(-LARGURA, 0), P(LARGURA, 0), P(LARGURA, Zfim), (QW, QH), (0, QH), P(-LARGURA, Zfim)], "laje")
    Z, n = 0.0, 0
    while PAREDE + PISO * Z < QH:
        Zb = Z + 0.6
        ya = P(0, Z)[1]
        xa, xb = max(0, P(-LARGURA, Z)[0]), min(QW, P(LARGURA, Z)[0])
        px(xa, round(ya), xb - xa, 1, "lajeJunta")
        px(xa, round(ya) + 1, xb - xa, 1, "lajeLuz")
        for i in range(-10, 11):
            X = i * 0.9 + (0.45 if n % 2 else 0)
            if abs(X) >= LARGURA:
                continue
            (x0, y0), (x1, y1) = P(X, Z), P(X, Zb)
            px.linha(x0, y0 + 1, x1, min(y1 - 1, QH - 1), "lajeJunta")
        Z, n = Zb, n + 1


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
LAREIRA = (-1.2, 2.2)  # o peito de pedra na parede do fundo: de X0 a X1


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
ESCADA = (3.0, 5.9, 1.4, 2.3, 10)   # a escada: do patamar (X0, em cima) ao pé (X1, no chão), a faixa de Z, os degraus
PATAMAR = (2.2, 3.0, 0.0, 2.3)       # o patamar, em cima, na ponta esquerda da galeria
GALERIA = (3.0, 8.0, 0.0, 1.4, 2.1)  # a galeria: de X0 a X1, de Z0 (a parede) a Z1 (a borda), a altura do piso
PORTAS = ((3.9, 4.8), (6.0, 6.9))    # as portas dos quartos, na parede do fundo, em cima da galeria


def escada_e_galeria(px):
    """A galeria dos quartos: as portas inteiras na parede (o batente, as ferragens, a argola), o piso visto de cima (a
    faixa por onde se anda), a testeira com as pontas das vigas, os esteios com as mãos-francesas e o guarda-corpo. O
    patamar na ponta esquerda, num esteio. A escada sobe da direita (o pé, no chão) para a esquerda (o patamar): os
    degraus com o piso claro e a frente escura, o banzo, o corrimão nos balaústres, o pilar do pé."""
    G0, G1, GZ0, GZ1, GH = GALERIA
    for d0, d1 in PORTAS:
        (x0, yb), (x1, _) = P(d0, 0, GH), P(d1, 0, GH)
        x0, x1, yb = round(x0), round(x1), round(yb)
        topo = round(yb - 1.65 * m(0))
        px(x0 - 1, topo - 1, x1 - x0 + 2, yb - topo + 1, "vigaEsc")
        px(x0 - 1, topo - 2, x1 - x0 + 2, 1, "vigaLuz")
        for x in range(x0, x1):
            px(x, topo, 1, yb - topo, "movelEsc" if (x - x0) % 3 == 2 else "movel")
        px(x0, topo, 1, yb - topo, "movelLuz")
        px(x0, topo + 2, x1 - x0, 1, "ferro"); px(x0, yb - 4, x1 - x0, 1, "ferro")
        px(x1 - 3, (topo + yb) // 2, 2, 2, "ferroLuz")
    # debaixo da galeria, a sombra da parede (o vão escuro onde a escada começa)
    px.poligono([P(G0, 0, 0), P(G1, 0, 0), P(G1, 0, GH - 0.25), P(G0, 0, GH - 0.25)], "pedraSombra")
    # o patamar e a galeria: o piso visto de cima, a testeira, as pontas das vigas
    P0, P1, PZ0, PZ1 = PATAMAR
    caixa(px, P0, P1, PZ0, PZ1, GH - 0.25, GH, topo="movelTopo", frente="viga", lado="vigaEsc", aresta="movelLuz")
    caixa(px, G0, G1, GZ0, GZ1, GH - 0.25, GH, topo="movelTopo", frente="viga", lado=None, aresta="movelLuz")
    for Z in (0.45, 0.9):
        (x0, y0), (x1, _) = P(G0, Z, GH), P(G1, Z, GH)
        px(x0, y0, x1 - x0, 1, "movel")
    (xa, yf), (xb, _) = P(G0, GZ1, GH - 0.25), P(G1, GZ1, GH - 0.25)
    for x in range(round(xa) + 3, round(xb), 8):
        px(x, round(yf) - 3, 2, 2, "vigaEsc")
    # os esteios: o do patamar (na frente dele) e os da galeria, com as mãos-francesas
    for Xe, Ze in ((P0 + 0.05, PZ1), (G1 - 1.3, GZ1), (5.0, GZ1)):
        (x, yt), (_, yp) = P(Xe, Ze, GH - 0.25), P(Xe, Ze, 0)
        px(round(x) - 1, round(yt), 3, round(yp - yt), "viga")
        px(round(x) - 1, round(yt), 1, round(yp - yt), "vigaLuz")
        px(round(x) - 2, round(yp) - 2, 5, 2, "pedraLuz")
        px(round(x) - 3, round(yp), 7, 1, "contato")
        for i in range(4):
            px.p(round(x) + 2 + i, round(yt) + i, "viga")
            px.p(round(x) - 2 - i, round(yt) + i, "viga")
    # os guarda-corpos (0,9 m): na borda da galeria e na frente do patamar
    for (Xa, Za), (Xb, Zb) in (((G0, GZ1), (G1, GZ1)), ((P0, PZ1), (P0, PZ0 + 0.2))):
        (xa, ya), (xb, yb) = P(Xa, Za, GH + 0.9), P(Xb, Zb, GH + 0.9)
        px.linha(xa, ya, xb, yb, "movel")
        n = max(2, round(abs(xb - xa) / 6))
        for i in range(n + 1):
            X, Z = Xa + (Xb - Xa) * i / n, Za + (Zb - Za) * i / n
            (x, y0), (_, y1) = P(X, Z, GH + 0.9), P(X, Z, GH)
            px(round(x), round(y0) + 1, 1, round(y1 - y0) - 1, "vigaEsc")
    # a escada: os degraus, do de cima (à esquerda) ao de baixo (à direita)
    X0, X1, Z0, Z1, n = ESCADA
    for i in range(n):
        Xa, Xb = X0 + i * (X1 - X0) / n, X0 + (i + 1) * (X1 - X0) / n
        H = GH * (n - i) / n
        caixa(px, Xa, Xb + 0.02, Z0, Z1, H - 0.08, H, topo="movelTopo", frente="movelEsc", lado=None, aresta="movelLuz")
    for d in range(2):                                       # o banzo de fora, por baixo dos degraus
        (x0, y0), (x1, y1) = P(X0, Z1, GH - 0.1), P(X1, Z1, 0)
        px.linha(x0, y0 + d, x1, y1 + d, "viga" if d else "vigaLuz")
    for i in range(0, n + 1, 2):                             # os balaústres e o corrimão
        X, H = X0 + i * (X1 - X0) / n, GH * (n - i) / n
        (x, y0), (_, y1) = P(X, Z1, H + 0.9), P(X, Z1, H)
        px(round(x), round(y0), 1, round(y1 - y0), "movel")
    (x0, y0), (x1, y1) = P(X0, Z1, GH + 0.9), P(X1, Z1, 0.9)
    px.linha(x0, y0, x1, y1, "movelLuz")
    (x, yt), (_, yp) = P(X1, Z1, 1.0), P(X1, Z1, 0)           # o pilar do pé
    px(round(x) - 1, round(yt), 3, round(yp - yt), "viga")
    px(round(x) - 1, round(yt), 1, round(yp - yt), "vigaLuz")
    px(round(x) - 2, round(yt) - 1, 5, 1, "movelLuz")
    px(round(x) - 2, round(yp), 6, 1, "contato")


# ---------------------------------------------------------------- o balcão
RUA = (-7.4, -6.2)                   # a porta da rua, na ponta esquerda do fundo (fechada)
DESPENSA = (-2.9, -2.1)              # a porta da despensa, no fundo, atrás da ponta direita do balcão
BALCAO = (-6.0, -2.2, 1.9, 2.5)      # o balcão: de X0 a X1, de Z0 a Z1 (a frente), 1,05 m
PRATELEIRAS = (-5.9, -3.2)           # as prateleiras na parede do fundo, atrás do taverneiro


def aparador(px):
    """As prateleiras na parede do fundo, atrás do balcão (três tábuas em mãos de ferro), com poucos objetos de silhueta
    própria: as canecas com a asa, as jarras bojudas, as garrafas de gargalo fino, a bilha, o barrilete de torneira."""
    X0, X1 = PRATELEIRAS
    for H in (1.25, 1.75, 2.25):
        (xa, y), (xb, _) = P(X0, 0.05, H), P(X1, 0.05, H)
        px(xa, y, xb - xa, 2, "movel")
        px(xa, y, xb - xa, 1, "movelLuz")
        px(xa, y + 2, xb - xa, 1, "pedraSombra")
        for X in (X0 + 0.15, X1 - 0.2):
            x, _ = P(X, 0.05, H)
            px(round(x), y + 2, 1, 3, "ferro")
    def obj(X, H):
        return [round(v) for v in P(X, 0.05, H)]
    for X in (-5.6, -5.2, -3.8):                             # as canecas, com a asa
        x, y = obj(X, 2.25)
        px(x, y - 4, 3, 4, "estanho"); px(x, y - 4, 1, 4, "estanhoLuz"); px(x + 3, y - 3, 1, 2, "estanhoEsc")
    for X in (-4.6, -3.5):                                   # as jarras bojudas
        x, y = obj(X, 1.75)
        px(x + 1, y - 7, 2, 1, "barroEsc"); px(x, y - 6, 4, 1, "barro"); px(x - 1, y - 5, 6, 5, "barro")
        px(x - 1, y - 5, 1, 5, "barroLuz"); px(x + 5, y - 5, 1, 3, "barroEsc")
    for X in (-5.5, -5.25, -5.0):                            # as garrafas
        x, y = obj(X, 1.75)
        px(x, y - 5, 2, 5, "vidro"); px(x, y - 5, 1, 5, "vidroLuz"); px(x, y - 8, 1, 3, "vidro"); px(x, y - 9, 1, 1, "barroEsc")
    x, y = obj(-4.4, 2.25)                                   # a bilha
    px(x, y - 5, 4, 5, "barro"); px(x, y - 5, 1, 5, "barroLuz"); px(x + 1, y - 6, 2, 1, "barroEsc")
    x, y = obj(-4.2, 1.25)                                   # o barrilete deitado, com a torneira
    px(x, y - 6, 9, 6, "movel"); px(x, y - 6, 9, 1, "movelLuz"); px(x, y - 1, 9, 1, "movelEsc")
    for xx in (x + 2, x + 6):
        px(xx, y - 6, 1, 6, "ferro")
    px(x + 9, y - 3, 2, 1, "ferroLuz")
    for X in (-5.7, -5.35):                                  # dois pratos de pé
        x, y = obj(X, 1.25)
        px(x, y - 5, 3, 4, "linho"); px(x, y - 5, 1, 4, "linhoLuz")


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
    for X in (X0 + 0.5, X1 - 0.6):                           # duas canecas e o pano em cima do tampo
        x, y = [round(v) for v in P(X, Z0 + 0.3, 1.05)]
        px(x, y - 3, 3, 3, "estanho"); px(x, y - 3, 1, 3, "estanhoLuz")
    x, y = [round(v) for v in P(X1 - 1.2, Z1 - 0.05, 1.05)]
    px(x, y, 5, 3, "linho"); px(x, y, 5, 1, "linhoLuz")


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
MESA_LONGA = (-5.7, -2.3, 4.3, 5.1)      # a mesa comprida da frente, à esquerda
BANCO_LONGE = (-5.6, -4.6, 3.75, 4.1)    # o banco do outro lado (o da freguesa, na ponta esquerda)
BANCO_PERTO = (-5.4, -2.7, 5.5, 5.85)    # o banco da frente (o do freguês de costas)
CADEIRA_PONTA = (-2.05, -1.6, 4.5, 4.95)  # a cadeira de espaldar da cabeceira (a da direita)
BANQUINHOS_BALCAO = ((-5.0, 2.95), (-3.6, 2.95))   # os banquinhos altos vazios, na frente do balcão
REDONDA = (2.0, 3.3)                     # a mesa redonda dos jogadores: o centro
BANCO_RODA_ESQ = (1.05, 1.45, 3.1, 3.5)  # o banquinho do jogador de verde
BANCO_RODA_DIR = (2.55, 2.95, 3.1, 3.5)  # o do jogador de ocre
MESA_MOREL = (5.85, 6.5, 3.3, 3.95)       # a mesa individual de Morel, inteira, com margem à direita
CADEIRA_MOREL = (4.95, 5.55, 3.3, 3.9)   # a cadeira robusta de espaldar dele
BANQUINHO_FOGO = (-1.75, -1.35, 1.0, 1.35)  # o do velho, na frente da lareira, à esquerda da boca


def cadeira(px, X0, X1, Z0, Z1, espaldar="esquerda", alto=1.15, H=0.47):
    """Uma cadeira de espaldar robusta: as quatro pernas, o assento (a face de cima e a borda), o espaldar de tábuas
    grossas do lado `espaldar` (o lado das costas de quem senta), com os montantes até `alto` e as travessas."""
    sombra(px, X0, X1, Z0, Z1)
    for X in (X0 + 0.04, X1 - 0.1):
        for Z in (Z0 + 0.05, Z1 - 0.05):
            perna(px, X, Z, H - 0.04, larg=0.08)
    caixa(px, X0, X1, Z0, Z1, H - 0.06, H, topo="movelTopo", frente="movel", lado="movelEsc", aresta="movelLuz")
    if espaldar == "esquerda":
        caixa(px, X0, X0 + 0.07, Z0, Z1, H, alto, topo="movelLuz", frente="movel", lado="movelEsc", aresta=None)
        for Hh in (H + 0.3, alto - 0.12):
            (xa, ya), (xb, yb) = P(X0 + 0.07, Z0, Hh), P(X0 + 0.07, Z1, Hh)
            px.linha(xa, ya, xb, yb, "movelLuz")
        for Z in (Z0, Z1 - 0.06):                           # os montantes, um pouco mais altos, com o pomo
            (x, yt), (_, yp) = P(X0 + 0.03, Z, alto + 0.08), P(X0 + 0.03, Z, H)
            px(round(x), round(yt), 2, round(yp - yt), "movelEsc")
            px(round(x), round(yt) - 1, 2, 1, "movelLuz")
    elif espaldar == "direita_lado":                         # o espaldar do lado direito (quem senta olha para a esquerda)
        caixa(px, X1 - 0.07, X1, Z0, Z1, H, alto, topo="movelLuz", frente="movel", lado="movelEsc", aresta=None)
        for Z in (Z0, Z1 - 0.06):
            (x, yt), (_, yp) = P(X1 - 0.05, Z, alto + 0.08), P(X1 - 0.05, Z, H)
            px(round(x), round(yt), 2, round(yp - yt), "movelEsc")
            px(round(x), round(yt) - 1, 2, 1, "movelLuz")


def mesas(px, parte=None):
    """Os móveis dos grupos; `parte` desenha só um (para gente.py redesenhar por cima de quem está atrás)."""
    feito = {}
    if parte in (None, "balcao_banquinhos"):
        for X, Z in BANQUINHOS_BALCAO:
            banco(px, X - 0.2, X + 0.2, Z - 0.2, Z + 0.2, H=0.75)
    if parte in (None, "fogo"):
        banco(px, *BANQUINHO_FOGO, H=0.4)
    if parte in (None, "roda"):
        for b in (BANCO_RODA_ESQ, BANCO_RODA_DIR):
            banco(px, *b)
    if parte in (None, "roda", "roda_mesa"):
        mesa_redonda(px, *REDONDA, raio=0.45)
        x, y = [round(v) for v in P(REDONDA[0], REDONDA[1], 0.75)]
        px(x - 4, y - 1, 9, 3, "linhoSombra")                # o tabuleiro e as peças
        for xx in range(x - 4, x + 5, 2):
            px(xx, y - 1, 1, 1, "movelEsc"); px(xx + 1, y, 1, 1, "movelEsc"); px(xx, y + 1, 1, 1, "movelEsc")
        px(x - 2, y - 3, 1, 2, "linhoLuz"); px(x + 2, y - 3, 1, 2, "vigaEsc"); px(x + 3, y - 2, 1, 1, "linhoLuz")
        for X in (REDONDA[0] - 0.33, REDONDA[0] + 0.3):
            xx, yy = [round(v) for v in P(X, REDONDA[1] - 0.1, 0.75)]
            px(xx, yy - 3, 2, 3, "estanho"); px(xx, yy - 3, 1, 3, "estanhoLuz")
        feito["vela_roda"] = castical(px, REDONDA[0] + 0.05, REDONDA[1] - 0.3)
    if parte in (None, "morel"):
        cadeira(px, *CADEIRA_MOREL)
    if parte in (None, "morel", "morel_mesa"):
        mesa(px, *MESA_MOREL)
        x, y = [round(v) for v in P(5.95, 3.55, 0.75)]       # a tigela do ensopado, perto dele, e o pão
        px(x, y - 1, 7, 1, "ensopado"); px(x, y, 7, 1, "tigela"); px(x + 1, y + 1, 5, 1, "tigela")
        x, y = [round(v) for v in P(6.15, 3.4, 0.75)]
        px(x, y - 1, 5, 2, "pao"); px(x + 1, y - 1, 2, 1, "paoLuz")
        feito["vela_morel"] = castical(px, 6.35, 3.5)
    if parte in (None, "longa_fundo"):
        banco(px, *BANCO_LONGE)
    if parte in (None, "longa", "longa_mesa"):
        mesa(px, *MESA_LONGA)
        x, y = [round(v) for v in P(-4.9, 4.65, 0.75)]       # a tigela com o pão, a jarra, as canecas, a vela
        px(x, y, 11, 2, "movelEsc"); px(x + 1, y - 2, 9, 2, "pao"); px(x + 2, y - 2, 3, 1, "paoLuz")
        x, y = [round(v) for v in P(-5.45, 4.55, 0.75)]
        px(x, y - 6, 5, 6, "estanho"); px(x, y - 6, 1, 6, "estanhoLuz"); px(x + 1, y - 7, 3, 1, "estanhoEsc")
        feito["vela_longa"] = castical(px, -2.75, 4.45)
    if parte in (None, "cadeira_ponta"):
        cadeira(px, *CADEIRA_PONTA, espaldar="direita_lado")
    if parte in (None, "longa_perto"):
        banco(px, *BANCO_PERTO)
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
LAMPIAO = (-4.0, 1.9, 2.75)  # o lampião pendurado na viga, sobre o balcão (X, Z, H da chama)


ARANDELA = (-8.0, 1.2, 2.0)  # a arandela na parede da esquerda, perto da porta da rua (X, Z, H)


def arandela(px):
    """A arandela de ferro na parede da esquerda: a chapa, o braço, o copo e a vela (a chama vem na camada velas)."""
    x, y = [round(v) for v in P(*ARANDELA)]
    px(x - 1, y - 2, 2, 5, "ferro"); px(x - 1, y - 2, 1, 5, "ferroLuz")
    px(x, y, 4, 1, "ferroLuz"); px(x + 2, y - 4, 2, 4, "cera"); px(x + 3, y - 4, 1, 4, "ceraEsc")
    return (x + 2, y - 5)


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
    porta(px, *RUA, 2.3)                                     # a porta da rua, fechada
    aparador(px)
    porta(px, *DESPENSA, 1.75, arco=False, fresta=0.25)    # a despensa, atrás da ponta do balcão
    boca = lareira(px)
    escada_e_galeria(px)
    lamp = lampiao(px)
    aran = arandela(px)
    balcao(px)
    feito = mesas(px)
    return {"chamas": [lamp, aran, feito["vela_morel"], feito["vela_roda"], feito["vela_longa"]], "boca": boca}


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
