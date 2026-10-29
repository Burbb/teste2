"""A taverna do Vau, candidata B (estudo estático): o salão em profundidade, na grade de 320×96.

O que mudou da A (o histórico em ../LEIA-ME.md): a A punha tudo numa faixa só (a parede de fundo e as três mesas quase
na mesma distância), com o balcão enorme e as pessoas estreitas, de perfil. Aqui a câmera olha de frente, um pouco de
cima (o olho a ~2 m: o ponto de fuga em VP, dentro do quadro), e a profundidade é grande: a parede do fundo fica longe
(11 px por metro) e a borda de baixo, perto (34 px por metro). Quem senta na frente fica três vezes maior que quem está
no fundo, na mesma conta.

**O espaço** (conferido sozinho em `so_o_espaco()`):
- a parede do balcão, à esquerda, mais perto (pisa em BAR_Y): a porta da rua, as prateleiras e os barris atrás do
  balcão; ela vira para o fundo num canto de pedra (o retorno, de x 128 a 138) e o salão continua até a parede do fundo
  (pisa em FUNDO_Y), com a lareira, a escada e a galeria dos quartos;
- o piso de tábuas que correm para VP, com poucas emendas e as juntas um tom só abaixo (o piso não disputa com as
  pessoas);
- a escada encostada na parede do fundo, subindo da esquerda para a direita até o patamar e a galeria, apoiada em dois
  esteios; na galeria, as portas de dois quartos; debaixo dela, o canto de Morel, de costas para a parede;
- a despensa (um "porão baixo", abertura.descer) é o alçapão aberto no piso atrás da ponta do balcão: a tampa erguida
  contra a parede e a escada de mão saindo do buraco.

**Materiais por valor:** a pedra do fundo fria e escura, o reboco do balcão claro e morno, a madeira dos móveis mais
quente que o piso, as roupas em cores contidas e diferentes entre si. A lareira é o foco quente; os cantos escurecem.

As camadas: `fundo(com_morel)` (parado: a sala, os móveis, as pessoas do estudo e a luz), `fogo(i)` (4 quadros) e
`velas(i)` (4 quadros), por cima. As pessoas são desenhadas à mão em gente.py."""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "hud", "forja", "h2"))
from tela_h2 import Tela  # noqa: E402  (a mesma camada de pixels das fontes da forja)

QW, QH = 320, 96
VP = (160, 25)        # o ponto de fuga: a altura do olho (~2,1 m), um pouco acima das cabeças
METRO = 34.0          # 1 m em pixels na borda de baixo
FUNDO_Y = 48          # onde a parede do fundo (o salão) encontra o piso
BAR_Y = 58            # onde a parede do balcão encontra o piso
RETORNO = (128, 138)  # o canto em que a parede do balcão vira para o fundo
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]


def m(y):
    """Pixels por metro no que pisa em y (a mesma conta das tábuas: zero no horizonte, METRO na borda de baixo)."""
    return METRO * (y - VP[1]) / (QH - VP[1])


def pont(x, y, n):
    return BAYER[(y & 3) * 4 + (x & 3)] < n


C = {
    # a pedra do fundo (fria) e a do canto
    "pedra": "#35373b", "pedraLuz": "#45474c", "pedraSombra": "#28292c", "junta": "#2b2c30",
    # o reboco da parede do balcão (morno, mais claro) e o enxaimel
    "reboco": "#5e574b", "rebocoLuz": "#6d6556", "rebocoSombra": "#4b453c",
    # a madeira da construção (escura) e a dos móveis (mais quente)
    "viga": "#3a2a1e", "vigaLuz": "#4c3828", "vigaEsc": "#24190f",
    "movel": "#6e4a2c", "movelLuz": "#8c6238", "movelEsc": "#47301c", "movelTopo": "#9a7044",
    # o piso
    "tabua": "#45362a", "tabuaJunta": "#3b2e23", "tabuaLuz": "#4f3e2f", "contato": "#1e1812",
    # o ferro, o barro, o estanho, o vidro, a cera, o fogo
    "ferro": "#33343a", "ferroLuz": "#5a5c64", "ferroEsc": "#1c1d22",
    "barro": "#7a4a30", "barroLuz": "#9a6440", "barroEsc": "#4e2e1e",
    "estanho": "#80838a", "estanhoLuz": "#b0b3ba", "estanhoEsc": "#55585e",
    "vidro": "#3e5a4a", "vidroLuz": "#6a8a74",
    "cera": "#d6ccae", "ceraEsc": "#a89e80", "chama": "#ffcc66", "chamaFora": "#e8782a", "chamaMiolo": "#fff2c4",
    "brasa": "#c8501a", "brasaEsc": "#7a2a10",
    "linho": "#b0a68e", "linhoLuz": "#d2c8b0", "linhoSombra": "#857b66",
    "pao": "#a8783a", "paoLuz": "#c89a52",
    "vulto": "#0d0b0a",
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
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), cor)

    def grade(self, x0, y0, linhas, pal):
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])


def retorno_y(x):
    """O piso encontra o retorno (a parede que vai do balcão ao fundo) nesta linha, que corre para VP."""
    x0, x1 = RETORNO
    return BAR_Y - (x - x0) * (BAR_Y - FUNDO_Y) / (x1 - x0)


# ---------------------------------------------------------------- o espaço
def paredes(px):
    """A parede do fundo (pedra), o retorno (pedra, de lado para a sala) e a parede do balcão (reboco com o enxaimel);
    a viga do teto que atravessa o quadro."""
    x0, x1 = RETORNO
    # a parede do fundo, em fiadas de pedra (as juntas um tom abaixo)
    px(x1, 0, QW - x1, FUNDO_Y, "pedra")
    for i, y in enumerate(range(FUNDO_Y - 4, -1, -4)):
        px(x1, y, QW - x1, 1, "junta")
        for x in range(x1 + (i % 2) * 4, QW, 8):
            px(x, y + 1, 1, 3, "junta")
    px(x1, FUNDO_Y - 1, QW - x1, 1, "pedraSombra")
    # o retorno: a pedra de lado, um pouco mais clara (a lareira está à direita)
    for x in range(x0, x1):
        yb = round(retorno_y(x))
        px(x, 0, 1, yb, "pedraLuz")
        for y in range(3, yb, 4):
            px.p(x, y, "pedra")
    # a parede do balcão: o reboco claro entre os esteios do enxaimel e a barra de madeira embaixo
    px(0, 0, x0, BAR_Y, "reboco")
    for x, y, w in [(30, 10, 7), (58, 16, 5), (96, 12, 8), (118, 20, 4)]:
        px(x, y, w, 1, "rebocoLuz")
    for xe in (0, 28, 104, x0 - 3):                    # os esteios do enxaimel
        px(xe, 0, 3, BAR_Y, "viga")
        px(xe, 0, 1, BAR_Y, "vigaLuz")
    px(0, 18, x0, 2, "viga")                            # a travessa do enxaimel
    px(0, 18, x0, 1, "vigaLuz")
    px(0, BAR_Y - 5, x0, 5, "viga")                     # o rodapé de tábuas
    px(0, BAR_Y - 5, x0, 1, "vigaLuz")
    # a viga do teto, na frente de tudo
    px(0, 0, QW, 3, "vigaEsc")
    px(0, 2, QW, 1, "viga")


def piso(px):
    """O piso de tábuas da parede até a borda de baixo. As tábuas correm de lado (paralelas ao fundo): as juntas ficam
    mais juntas longe e mais abertas perto, nunca a menos de 3 px uma da outra; as emendas, desencontradas de uma
    tábua para a outra, correm para VP. Um tom só abaixo: o piso não disputa com as pessoas."""
    x0, x1 = RETORNO
    fora = lambda x, y: y < BAR_Y and x < x1 and y < retorno_y(x)  # atrás do retorno (a parede do balcão)
    for y in range(FUNDO_Y, QH):
        for x in range(QW):
            if not fora(x, y):
                px.p(x, y, "tabua")
    # as juntas: a cada 0,3 m de distância (a distância é o inverso da escala)
    dist = lambda y: 1 / m(y)
    linhas, d, ultima = [], dist(QH), QH
    while True:
        d += 0.3 / 4.7 * dist(QH)
        y = round(VP[1] + (QH - VP[1]) * dist(QH) / d)
        if y <= FUNDO_Y:
            break
        if ultima - y >= 3:
            linhas.append(y)
            ultima = y
    for y in linhas:
        for x in range(QW):
            if not fora(x, y):
                px.p(x, y, "tabuaJunta")
    # as emendas: a cada 2,4 m de tábua, desencontradas de uma fileira para a outra
    for n, (ya, yb) in enumerate(zip(linhas, linhas[1:])):
        for i in range(-12, 13):
            X = (i + (n % 3) / 3) * 2.4
            xa, xb = VP[0] + X * m(ya), VP[0] + X * m(yb)
            if 0 <= xa < QW and not fora(xa, yb):
                px.linha(round(xa), ya - 1, round(xb), yb + 1, "tabuaJunta")


def porta_rua(px):
    """A porta da rua na parede do balcão, à esquerda: o vão em arco no reboco, a porta de tábuas fechada com as duas
    ferragens e a argola, a soleira de pedra."""
    x0, x1, topo = 7, 25, 26
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    for y in range(round(topo - r) - 2, BAR_Y):
        for x in range(x0 - 2, x1 + 2):
            d = math.hypot(x + 0.5 - cx, max(0, topo - y - 0.5))
            if y < topo and d > r + 2:
                continue
            dentro = (x0 <= x < x1) and (y >= topo or d <= r)
            if not dentro:
                px.p(x, y, "pedraLuz")
                continue
            junta = (x - x0) % 4 == 3
            px.p(x, y, "vigaEsc" if junta else "movelLuz" if (x - x0) % 4 == 0 else "movel")
    for yy in (topo - 2, BAR_Y - 9):
        px(x0, yy, x1 - x0, 2, "ferro")
        px(x0, yy, x1 - x0, 1, "ferroLuz")
    px(x1 - 5, 40, 3, 3, "ferro")
    px(x1 - 4, 41, 1, 1, "vigaEsc")
    px(x0 - 2, BAR_Y, x1 - x0 + 4, 1, "pedraLuz")


# ---------------------------------------------------------------- o balcão e o que está atrás dele
BALCAO = (40, 108, 64)  # o balcão: de x0 a x1, a frente pisando em y
LAMPIAO = (78, 3, 20)   # o lampião pendurado na viga: x, de onde sai a corrente, onde fica a chama


def prateleiras(px):
    """Duas tábuas na parede atrás do balcão, em mãos de ferro, com grupos de coisas reconhecíveis (não uma fila):
    canecas de estanho emborcadas, uma jarra de barro, duas garrafas, um barrilete, uma pilha de pratos."""
    for y, a, b in ((29, 36, 72), (29, 88, 102), (37, 36, 102)):
        px(a, y, b - a, 2, "movel")
        px(a, y, b - a, 1, "movelLuz")
        for xx in (a + 2, b - 3):
            px(xx, y + 2, 1, 2, "ferro")
    # em cima: três canecas emborcadas, a jarra, um vão, as garrafas
    for x in (38, 42, 46):
        px(x, 25, 3, 4, "estanho")
        px(x, 25, 1, 4, "estanhoLuz")
    px(53, 23, 5, 6, "barro"); px(53, 23, 1, 6, "barroLuz"); px(54, 22, 3, 1, "barroEsc"); px(58, 24, 1, 3, "barroEsc")
    for x in (64, 68):
        px(x, 22, 2, 7, "vidro"); px(x, 22, 1, 7, "vidroLuz"); px(x, 20, 2, 2, "barroEsc")
    px(90, 23, 9, 6, "movel"); px(90, 23, 9, 1, "movelLuz")       # o barrilete deitado, com os aros
    px(92, 23, 1, 6, "ferro"); px(96, 23, 1, 6, "ferro")
    # embaixo: os pratos de pé, duas canecas, a jarra pequena
    for x in (38, 40, 42):
        px(x, 31, 1, 6, "linho"); px(x, 31, 1, 1, "linhoLuz")
    for x in (88, 92):
        px(x, 33, 3, 4, "estanho"); px(x, 33, 1, 4, "estanhoLuz")
    px(97, 32, 4, 5, "barro"); px(97, 32, 1, 5, "barroLuz")


def barris(px):
    """Dois barris em pé no canto entre a porta e o balcão (0,85 m): as aduelas abauladas, os aros de ferro, o tampo
    visto de cima. Em pé, de lado: deitados com o tampo para a sala, liam como rodas."""
    for x0 in (26, 34):
        alto = round(0.85 * m(BAR_Y))
        topo = BAR_Y - alto
        for i in range(alto):
            bojo = 1 if 2 <= i <= alto - 3 else 0                     # o bojo no meio
            a, b = x0 - bojo, x0 + 7 + bojo
            px(a, topo + i, b - a, 1, "movel")
            px(a, topo + i, 1, 1, "movelLuz")
            px(b - 1, topo + i, 1, 1, "movelEsc")
            for xx in range(a + 2, b - 1, 2):
                px.p(xx, topo + i, "movelEsc" if (xx - a) % 4 == 0 else "movel")
        for yy in (topo + 2, BAR_Y - 3):
            px(x0 - 1, yy, 9, 1, "ferro")
        px(x0, topo - 1, 7, 1, "movelTopo")                          # o tampo
        px(x0 - 1, BAR_Y, 9, 1, "contato")


def balcao(px):
    """O balcão de tábuas na frente das prateleiras, na proporção de quem está atrás dele (1,05 m): o tampo visto de
    cima (o claro), a frente de tábuas, o rodapé; dois banquinhos altos na frente, um vazio."""
    x0, x1, pe = BALCAO
    mm = m(pe)
    yt = round(pe - 1.05 * mm)                         # o tampo (a borda da frente)
    px(x0 - 1, yt - 2, x1 - x0 + 2, 2, "movelTopo")    # o tampo visto de cima
    px(x0 - 1, yt, x1 - x0 + 2, 2, "movelLuz")
    px(x0, yt + 2, x1 - x0, pe - yt - 2, "movel")
    for xx in range(x0 + 5, x1, 7):
        px(xx, yt + 2, 1, pe - yt - 3, "movelEsc")
    px(x0, pe - 2, x1 - x0, 2, "movelEsc")
    px(x0 - 1, pe, x1 - x0 + 2, 1, "contato")
    for xb in (70, 92):                                 # os banquinhos altos (0,75 m), na frente do balcão
        pb = pe + 3
        ys = round(pb - 0.75 * m(pb))
        px(xb, ys, 8, 2, "movelLuz")
        px(xb, ys + 2, 8, 1, "movelEsc")
        px(xb + 1, ys + 3, 1, pb - ys - 3, "movel")
        px(xb + 6, ys + 3, 1, pb - ys - 3, "movel")
        px(xb + 1, pb - 4, 6, 1, "movelEsc")
        px(xb, pb, 8, 1, "contato")
    return yt


DESPENSA = (111, 125)  # a porta da despensa, na parede do balcão, entre a ponta dele e o canto: de x0 a x1


def porta_despensa(px):
    """A despensa ("um porão baixo", abertura.descer): uma porta baixa de tábuas (1,75 m) na parede do balcão, no
    batente escuro, entreaberta para dentro (o escuro da escada que desce aparece na fresta do lado da fechadura), com
    as duas ferragens e a soleira de pedra."""
    x0, x1 = DESPENSA
    topo = round(BAR_Y - 1.75 * m(BAR_Y))
    px(x0 - 1, topo - 1, x1 - x0 + 2, BAR_Y - topo + 1, "vigaEsc")      # o batente
    px(x0 - 1, topo - 2, x1 - x0 + 2, 1, "vigaLuz")
    px(x0, topo, x1 - x0, BAR_Y - topo, "vulto")                        # o vão escuro
    folha = x1 - x0 - 4                                                 # a folha, aberta para dentro: mais estreita
    for x in range(x0, x0 + folha):
        px(x, topo + 1, 1, BAR_Y - topo - 1, "movelEsc" if (x - x0) % 3 == 2 else "movel")
    px(x0, topo + 1, 1, BAR_Y - topo - 1, "movelLuz")
    for yy in (topo + 5, BAR_Y - 7):
        px(x0, yy, folha, 1, "ferro")
    px(x0 + folha - 2, topo + 13, 1, 2, "ferroLuz")                     # a argola
    px(x0 + folha, topo + 14, 4, 1, "vigaEsc")                          # na fresta, a borda do primeiro degrau
    px(x0 - 2, BAR_Y, x1 - x0 + 4, 1, "pedraLuz")                       # a soleira


# ---------------------------------------------------------------- o salão do fundo
LAREIRA = (148, 182)  # a lareira na parede do fundo: de x0 a x1 (o peito de pedra)


def lareira(px):
    """A lareira de pedra na parede do fundo: a chaminé até o teto, o peito com a cornija, a boca escura com a lenha,
    a pedra da lareira no piso; a lenha empilhada ao lado. O fogo e o caldeirão vêm na camada fogo."""
    x0, x1 = LAREIRA
    px(x0 + 5, 0, x1 - x0 - 10, 24, "pedraLuz")          # a chaminé
    px(x0 + 5, 0, 1, 24, "pedra")
    px(x0, 24, x1 - x0, FUNDO_Y - 24, "pedraLuz")        # o peito
    for y in range(28, FUNDO_Y, 4):
        for x in range(x0 + ((y // 4) % 2) * 3, x1, 6):
            px(x, y, 6, 1, "pedra")
            px(x, y, 1, 4, "pedra")
    px(x0 - 2, 23, x1 - x0 + 4, 2, "movel")              # a cornija
    px(x0 - 2, 23, x1 - x0 + 4, 1, "movelLuz")
    b0, b1, bt = x0 + 8, x1 - 8, 35                      # a boca
    px(b0, bt, b1 - b0, FUNDO_Y - bt, "vulto")
    px(b0 - 1, bt - 1, b1 - b0 + 2, 1, "pedra")
    px(x0 - 2, FUNDO_Y, x1 - x0 + 4, 2, "pedraLuz")      # a pedra da lareira, no piso
    # a lenha empilhada à esquerda, entre o canto e a lareira (as pontas das achas): à direita senta quem se aquece
    for i, n in enumerate((3, 2)):
        for j in range(n):
            xx = RETORNO[1] + 1 + i + j * 3
            px(xx, FUNDO_Y - 3 - i * 3, 3, 3, "movelEsc")
            px(xx, FUNDO_Y - 3 - i * 3, 2, 2, "movelLuz")


GALERIA_Y = 24               # o piso da galeria dos quartos (2,2 m: as portas cabem inteiras), na parede do fundo
ESCADA = (200, 246)          # a escada: do pé (x) ao patamar (x), subindo da esquerda para a direita
PORTAS = ((262, 273), (292, 303))  # as portas dos quartos, na galeria


def escada(px):
    """A escada encostada na parede do fundo: o banzo (a viga lateral) do piso ao patamar, os degraus (o piso claro, a
    frente escura), o corrimão nos balaústres; o patamar e a galeria da direita, apoiados em dois esteios, com o
    guarda-corpo; na parede da galeria, as portas de dois quartos."""
    a, b = ESCADA
    n = 9
    for i in range(n):                                   # os degraus
        xs = a + i * (b - a) / n
        ys = FUNDO_Y - (i + 1) * (FUNDO_Y - GALERIA_Y) / n
        px(round(xs), round(ys), round((b - a) / n) + 1, 1, "movelLuz")
        px(round(xs), round(ys) + 1, round((b - a) / n) + 1, 2, "movelEsc")
    px.linha(a, FUNDO_Y, b, GALERIA_Y + 1, "movel")      # o banzo
    px.linha(a, FUNDO_Y - 1, b, GALERIA_Y, "movelLuz")
    px.linha(a + 1, FUNDO_Y - 1, b + 1, GALERIA_Y, "movel")
    for i in range(0, n + 1, 3):                         # os balaústres e o corrimão
        xs = round(a + i * (b - a) / n)
        ys = round(FUNDO_Y - i * (FUNDO_Y - GALERIA_Y) / n)
        px(xs, ys - 9, 1, 9, "movelEsc")
    px.linha(a, FUNDO_Y - 10, b, GALERIA_Y - 10, "movelLuz")
    # o patamar e a galeria: o piso (a viga de borda), o guarda-corpo, os esteios até o chão
    px(b - 2, GALERIA_Y, QW - b + 2, 3, "viga")
    px(b - 2, GALERIA_Y, QW - b + 2, 1, "vigaLuz")
    px(b - 2, GALERIA_Y - 10, QW - b + 2, 1, "movelLuz")
    for xx in range(b, QW, 5):
        px(xx, GALERIA_Y - 9, 1, 9, "movelEsc")
    for xe in (b - 1, QW - 4):
        px(xe, GALERIA_Y + 3, 3, FUNDO_Y - GALERIA_Y - 3, "viga")
        px(xe, GALERIA_Y + 3, 1, FUNDO_Y - GALERIA_Y - 3, "vigaLuz")
        px(xe - 1, FUNDO_Y, 5, 1, "contato")
    # as portas dos quartos, na parede atrás do guarda-corpo (o guarda-corpo passa na frente delas)
    topo = round(GALERIA_Y - 1.8 * m(FUNDO_Y))           # 1,8 m: a porta inteira, com a verga embaixo da viga
    for d0, d1 in PORTAS:
        px(d0 - 1, topo - 1, d1 - d0 + 2, GALERIA_Y - topo + 1, "vigaEsc")   # o batente e a verga
        px(d0 - 1, topo - 2, d1 - d0 + 2, 1, "vigaLuz")
        for x in range(d0, d1):                           # as tábuas
            px(x, topo, 1, GALERIA_Y - topo, "movelEsc" if (x - d0) % 3 == 2 else "movel")
        px(d0, topo, 1, GALERIA_Y - topo, "movelLuz")
        for yy in (topo + 2, GALERIA_Y - 4):              # as ferragens
            px(d0, yy, d1 - d0, 1, "ferro")
        px(d1 - 3, topo + 9, 2, 2, "ferroLuz")            # a argola
    for xx in range(b, QW, 5):                           # o guarda-corpo por cima das portas
        px(xx, GALERIA_Y - 9, 1, 9, "movelEsc")
    px(b - 2, GALERIA_Y - 10, QW - b + 2, 1, "movelLuz")


# ---------------------------------------------------------------- as mesas e os assentos
def mesa_ret(px, x0, x1, pe_longe, pe_perto, vela=None):
    """Uma mesa retangular vista de cima e de frente: o tampo do pé de longe ao de perto (a profundidade em pixels), a
    espessura, as pernas da frente (as de trás escondidas); a vela num castiçal em `vela`."""
    yl = round(pe_longe - 0.75 * m(pe_longe))
    yp = round(pe_perto - 0.75 * m(pe_perto))
    px(x0 + 1, yl, x1 - x0 - 2, yp - yl, "movelTopo")
    for y in range(yl + 1, yp, 3):
        px(x0 + 1, y, x1 - x0 - 2, 1, "movelLuz")
    px(x0, yp, x1 - x0, 2, "movel")
    px(x0, yp + 2, x1 - x0, 1, "movelEsc")
    for xx in (x0 + 1, x1 - 3):
        px(xx, yp + 3, 2, pe_perto - yp - 3, "movel")
        px(xx, yp + 3, 1, pe_perto - yp - 3, "movelLuz")
        px(xx - 1, pe_perto, 4, 1, "contato")
    if vela:
        vx, vy = vela
        px(vx - 1, vy - 1, 4, 1, "barro")
        px(vx, vy - 5, 2, 4, "cera")
        px(vx + 1, vy - 5, 1, 4, "ceraEsc")
    return yl, yp


def mesa_redonda(px, cx, pe, raio, vela=None):
    """Uma mesa redonda de um pé: o tampo como elipse (achatada pela altura do olho), a borda, o pé central e a base."""
    mm = m(pe)
    yt = pe - 0.75 * mm
    rx, ry = raio * mm, raio * mm * 0.32
    for y in range(round(yt - ry), round(yt + ry) + 1):
        for x in range(round(cx - rx), round(cx + rx) + 1):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - yt) / ry) ** 2 <= 1:
                px.p(x, y, "movelTopo")
    for x in range(round(cx - rx) + 1, round(cx + rx)):
        y = round(yt + ry * math.sqrt(max(0.0, 1 - ((x + 0.5 - cx) / rx) ** 2)))
        px(x, y, 1, 2, "movel")
        px.p(x, y + 2, "movelEsc")
    px(round(cx) - 1, round(yt + ry) + 3, 3, pe - round(yt + ry) - 3, "movel")
    px(round(cx) - 4, pe - 1, 9, 1, "movelEsc")
    px(round(cx) - 5, pe, 11, 1, "contato")
    if vela:
        vx, vy = vela
        px(vx - 1, vy - 1, 4, 1, "barro")
        px(vx, vy - 4, 2, 3, "cera")
        px(vx + 1, vy - 4, 1, 3, "ceraEsc")
    return round(yt - ry), round(yt + ry)


def banco(px, x0, x1, pe, alto=0.45, encosto=False):
    """Um banco de tábua (ou uma cadeira, com encosto) de pé no piso em `pe`."""
    mm = m(pe)
    ys = round(pe - alto * mm)
    px(x0, ys, x1 - x0, 2, "movelLuz")
    px(x0, ys + 2, x1 - x0, 1, "movelEsc")
    for xx in (x0 + 1, x1 - 2):
        px(xx, ys + 3, 1, pe - ys - 3, "movel")
    px(x0, pe, x1 - x0, 1, "contato")
    if encosto:
        ye = round(pe - 0.95 * mm)
        px(x0, ye, 1, ys - ye, "movel")
        px(x1 - 1, ye, 1, ys - ye, "movel")
        px(x0, ye, x1 - x0, 2, "movelLuz")
        px(x0, ye + 4, x1 - x0, 1, "movel")
    return ys


# Onde fica cada mesa (as pessoas de gente.py sentam nelas)
MESA_FRENTE = (128, 214, 92, 104)   # x0, x1, o pé de longe, o de perto (fora do quadro)
MESA_MEIO = (236, 71, 0.55)         # o centro, onde pisa, o raio em metros
MESA_FOGO = (196, 53)               # o banquinho de quem se aquece
MESA_CANTO = (276, 304, 54, 57)     # a mesa de Morel, debaixo da galeria


def mesa_canto(px):
    """O canto de Morel: o banco encostado na parede do fundo e a mesa pequena, com a vela na ponta."""
    x0, x1, pl, pp = MESA_CANTO
    vela = (x0 + 3, round(pl - 0.75 * m(pl)))
    return mesa_ret(px, x0, x1, pl, pp, vela=vela), (vela[0], vela[1] - 6)


def mesa_meio(px):
    """A mesa redonda do meio, com a vela e a jarra."""
    cx, pe, raio = MESA_MEIO
    vela = (cx - 8, round(pe - 0.75 * m(pe)) + 1)
    a, b = mesa_redonda(px, cx, pe, raio, vela=vela)
    px(229, a - 2, 4, 4, "barro"); px(229, a - 2, 1, 4, "barroLuz"); px(230, a - 3, 2, 1, "barroEsc")  # a jarra
    return (a, b), (vela[0], vela[1] - 5)


def mesa_frente(px):
    """A mesa comprida da frente (o pé de perto sai do quadro), com a vela, a tábua com o pão e uma caneca."""
    x0, x1, pl, pp = MESA_FRENTE
    vela = (x0 + 5, round(pl - 0.75 * m(pl)) + 2)
    yl, yp = mesa_ret(px, x0, x1, pl, pp, vela=vela)
    px(160, yl + 2, 9, 3, "movelEsc"); px(161, yl + 1, 7, 2, "pao"); px(162, yl + 1, 3, 1, "paoLuz")  # o pão
    px(196, yl + 2 - 3, 3, 4, "estanho"); px(196, yl - 1, 1, 4, "estanhoLuz")                        # a caneca
    return (yl, yp), (vela[0], vela[1] - 6)


def mesas(px):
    """As mesas em três distâncias; devolve onde caem os tampos e as chamas das velas."""
    banco(px, 278, 302, 50, alto=0.45)
    canto, c1 = mesa_canto(px)
    meio, c2 = mesa_meio(px)
    x0, x1, pl, pp = MESA_FRENTE
    banco(px, x0 + 4, x0 + 40, pl - 3)
    frente, c3 = mesa_frente(px)
    return {"canto": canto, "meio": meio, "frente": frente, "chamas": [c1, c2, c3]}


def cadeira_vazia(px):
    """A cadeira vazia na frente da mesa do meio, de costas para nós (o encosto de duas tábuas, as pernas)."""
    pe = 80
    mm = m(pe)
    x0 = 218
    ys = round(pe - 0.45 * mm)
    ye = round(pe - 1.0 * mm)
    px(x0, ys, 11, 2, "movelLuz")
    for xx in (x0, x0 + 10):
        px(xx, ye, 1, pe - ye, "movel")
    px(x0, ye, 11, 2, "movelLuz")
    px(x0, ye + 4, 11, 2, "movel")
    px(x0 + 1, ys + 2, 9, 1, "movelEsc")
    px(x0 - 1, pe, 13, 1, "contato")


# ---------------------------------------------------------------- a luz
LUZES = [(165, 42, 40, 1.0), (78, 22, 26, 0.7)]          # a lareira e o lampião do balcão: x, y, raio, força


def luz(t, velas):
    """Longe do fogo, do lampião e das velas, a sala escurece em degraus pontilhados; perto, o halo quente."""
    for y in range(QH):
        for x in range(QW):
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.2)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.2)))
            for vx, vy in velas:
                d = math.hypot(x - vx, (y - vy) * 1.2)
                perto = max(perto, 0.5 * max(0.0, 1 - d / 24))
            escuro = max(0.0, 0.5 - perto * 1.0)
            f5 = escuro / 0.5 * 4
            n = int(f5) + (1 if pont(x, y, int((f5 % 1) * 16)) else 0)
            if n:
                t.mistura(x, y, (6, 5, 4), 0.5 * n / 4)
            for lx, ly, r, f in LUZES:
                d2 = ((x - lx) ** 2 + ((y - ly) * 1.2) ** 2) / (r * r)
                if d2 < 1:
                    al = 0.16 if d2 < 0.08 else 0.1 if d2 < 0.3 else 0.06 if d2 < 0.65 else 0.03
                    t.mistura(x, y, (255, 160, 80), al * f)


def lampiao(px):
    """O lampião de ferro pendurado na viga por uma corrente, sobre o balcão (a chama vem na camada velas)."""
    x, y0, yc = LAMPIAO
    for y in range(y0, yc - 3, 2):
        px.p(x, y, "ferroLuz")
        px.p(x, y + 1, "ferro")
    px(x - 2, yc - 3, 5, 1, "ferroLuz")
    px(x - 2, yc - 2, 1, 4, "ferro")
    px(x + 2, yc - 2, 1, 4, "ferro")
    px(x - 2, yc + 2, 5, 1, "ferroLuz")


def chamas_velas():
    """Onde ficam as chamas: o lampião e as velas das três mesas."""
    x, _, yc = LAMPIAO
    return [(x, yc - 1)] + mesas(Pincel(Tela(QW, QH)))["chamas"]


# ---------------------------------------------------------------- as camadas
def so_o_espaco():
    """O espaço sozinho (as paredes, o piso, a viga), sem móveis nem pessoas: a conferência do piso e dos planos."""
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    piso(px)
    return t


def sala(px):
    """A sala com os móveis, sem as pessoas e sem a luz; devolve onde caem os tampos."""
    paredes(px)
    piso(px)
    porta_rua(px)
    prateleiras(px)
    barris(px)
    lareira(px)
    escada(px)
    porta_despensa(px)
    lampiao(px)
    r = mesas(px)
    cadeira_vazia(px)
    r["balcao"] = balcao(px)
    return r


def fogo(i):
    """O fogo da lareira (4 quadros): as línguas que afinam para cima, a lenha com as pontas em brasa e o caldeirão na
    cremalheira, na frente das chamas."""
    t = Tela(QW, QH)
    px = Pincel(t)
    x0, x1 = LAREIRA
    b0, b1 = x0 + 8, x1 - 8
    cx = (b0 + b1) // 2
    base = FUNDO_Y - 3
    linguas = [[(cx - 5, 4, 0), (cx - 2, 7, 1), (cx + 1, 8, 0), (cx + 4, 5, -1)],
               [(cx - 5, 5, 1), (cx - 2, 6, 0), (cx + 1, 7, -1), (cx + 4, 6, 0)],
               [(cx - 5, 3, 0), (cx - 2, 8, -1), (cx + 1, 7, 1), (cx + 4, 5, 0)],
               [(cx - 5, 4, -1), (cx - 2, 7, 0), (cx + 1, 9, 0), (cx + 4, 4, 1)]][i]
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
    px(b0 + 2, FUNDO_Y - 2, b1 - b0 - 4, 2, "vigaEsc")
    px(b0 + 2, FUNDO_Y - 2, 2, 2, "brasa")
    px(b1 - 4, FUNDO_Y - 2, 2, 2, "brasa")
    px.p(cx + (i % 2), FUNDO_Y - 1, "brasa")
    px(cx, 35, 1, 3, "ferro")                           # a cremalheira e o caldeirão
    px(cx - 3, 38, 7, 1, "ferroLuz")
    px(cx - 3, 39, 7, 3, "ferro")
    px(cx - 2, 42, 5, 1, "ferroEsc")
    return t


def velas(i):
    """As chamas do lampião e das velas (4 quadros, cada uma no seu passo): por cima de tudo."""
    t = Tela(QW, QH)
    px = Pincel(t)
    for j, (x, y) in enumerate(chamas_velas()):
        f = (i + j * 3) % 4
        alto = 3 if f in (0, 2) else 2 if f == 1 else 4
        px(x, y - alto + 2, 1, alto, "chamaFora")
        px.p(x, y + 1, "chama")
        if alto >= 3:
            px.p(x, y, "chamaMiolo" if f == 3 else "chama")
    return t
