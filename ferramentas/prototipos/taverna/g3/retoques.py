"""Os retoques da G3: a G2 aprovada (composição, câmera e acabamento) com três correções locais pedidas pelo Jean, sobre
as células da fonte da G2 (`g2/aseprite/taverna-g2.aseprite`). Fora das regiões abaixo, a G3 é a G2 pixel a pixel. Cada
parte nova é desenhada com a paleta e a luz da G (`g.desenho.luz`), para entrar no mesmo acabamento.

- `garrafas`: a garrafa de vinho verde e a bojuda de âmbar tinham o gargalo de 2 px sobre um corpo de largura ímpar
  (o gargalo meio pixel fora do eixo, parecendo inclinado). As duas são refeitas no eixo: a base apoiada na tábua, o
  corpo, os ombros afinando, o gargalo, a boca com o anel e a rolha.
- `pano`: o pano saía da mão como um bloco quadrado. Agora ele passa por cima da borda da caneca (a dobra entrando na
  boca), desce pelo lado dela até a mão, que o aperta, e pende da mão em pregas que convergem para o punho, com a ponta
  mais baixa e a barra em diagonal.
- `fregues_esquerda`: o freguês da esquerda refeito pela anatomia de quem está sentado ao balcão, perto da câmera: a
  cabeça do tamanho da de um adulto nessa distância (como na G), o pescoço, a gola, a linha dos ombros quase
  horizontal, o ombro de cá redondo e o braço descendo do ombro para fora do quadro (o cotovelo, apoiado no balcão,
  fica abaixo da borda), as costas entre a gola e o braço. Continua uma silhueta escura e secundária, no mesmo canto,
  sem cobrir mais a lareira; o contorno do lado do fogo pega a luz dela."""
import numpy as np

from g import desenho as G, taverneiro as GT
from g2 import retoques as R2
from tela_h2 import Tela


def _colar(destino, tela, mascara=None):
    """Copia os pixels da tela (opacos, ou os da máscara) para a camada destino (numpy RGBA)."""
    m = tela.a[:, :, 3] > 0 if mascara is None else mascara
    destino[m] = tela.a[m]
    return int(m.sum())


# ---------------------------------------------------------------- as garrafas
CAIXA_GARRAFAS = (178, 8, 200, G.PR)  # x0, y0, x1, y1: a de vinho e a bojuda, na prateleira da direita


def _garrafas_novas(px):
    y0 = G.PR  # a tábua: o fundo das garrafas pousa na linha de cima dela
    # a garrafa de vinho, verde, no eixo x 182,5: a base e o corpo (6 px), os ombros, o gargalo, a boca, a rolha
    px(180, y0 - 10, 6, 10, "vidro")
    px(180, y0 - 10, 1, 10, "vidroLuz")
    px(185, y0 - 10, 1, 10, "#18301f")
    px(181, y0 - 9, 1, 6, "vidroBrilho")
    px(180, y0 - 1, 6, 1, "#18301f")              # a base, mais escura, apoiada
    px(181, y0 - 11, 4, 1, "vidro")               # os ombros
    px(181, y0 - 11, 1, 1, "vidroLuz")
    px(182, y0 - 12, 2, 1, "vidro")
    px(182, y0 - 16, 2, 4, "vidro")               # o gargalo
    px(182, y0 - 16, 1, 4, "vidroLuz")
    px(181, y0 - 17, 4, 1, "vidroLuz")            # o anel da boca
    px(182, y0 - 18, 2, 1, "rolha")
    # a bojuda de âmbar, no eixo x 193: o bojo simétrico, a base reta, o gargalo, o anel, a rolha
    for y, w in zip(range(y0 - 8, y0), (6, 8, 10, 10, 10, 10, 8, 8)):
        a = 193 - w // 2
        px(a, y, w, 1, "ambar")
        px(a, y, 1, 1, "ambarLuz")
        px(a + w - 1, y, 1, 1, "paoEsc")
    px(190, y0 - 6, 1, 2, "ambarBrilho")
    px(191, y0 - 9, 4, 1, "ambar")                # os ombros
    px(192, y0 - 12, 2, 3, "ambar")               # o gargalo
    px(192, y0 - 12, 1, 3, "ambarLuz")
    px(191, y0 - 13, 4, 1, "ambarLuz")            # o anel da boca
    px(192, y0 - 14, 2, 1, "rolha")


def garrafas(fundo):
    """As duas garrafas refeitas no eixo: onde as da G estavam, volta a parede (com a luz da G); por cima, as novas."""
    parede = Tela(G.QW, G.QH)
    G.sala(G.Pincel(parede))
    G.luz(parede)
    x0, y0, x1, y1 = CAIXA_GARRAFAS
    fundo[y0:y1, x0:x1] = parede.a[y0:y1, x0:x1]
    novas = Tela(G.QW, G.QH)
    _garrafas_novas(G.Pincel(novas))
    G.luz(novas)
    return (x1 - x0) * (y1 - y0) + _colar(fundo, novas)


# ---------------------------------------------------------------- o pano
def _mao(f):
    """A mão de cá da G (a direita dele), igual: o dorso, o polegar por cima, a sombra embaixo."""
    f.grade(148, 55, [".lll.", "lllmm", "lmmmm", "lmmms", "mmmss", ".mss."],
            {"l": "peleLuz", "m": "pele", "s": "peleSombra"})
    f.p(152, 55, "peleSombra")


def _pano_pendente(f):
    """A parte que pende da mão: sai do punho fechado, cai pelo peso em pregas que convergem para a mão, a ponta mais
    baixa à esquerda e a barra subindo em diagonal para a direita."""
    linhas = {  # y: (x da borda de lá, x da borda de cá)
        60: (149, 155), 61: (149, 155), 62: (149, 156), 63: (149, 156), 64: (149, 156), 65: (150, 156), 66: (150, 156),
        67: (150, 155), 68: (150, 154), 69: (150, 153), 70: (150, 152), 71: (150, 151), 72: (150, 150),
    }
    for y, (a, b) in linhas.items():
        for x in range(a, b + 1):
            f.p(x, y, "panoLuz" if x == a else "panoSombra" if x == b else "pano")
    # as pregas: duas sombras que sobem estreitando para o punho
    for x, y in ((153, 61), (153, 62), (152, 63), (152, 64), (152, 65), (152, 66), (151, 67), (151, 68),
                 (155, 62), (155, 63), (154, 64), (154, 65), (154, 66)):
        f.p(x, y, "panoSombra")
    for x, y in ((151, 62), (151, 63), (150, 64)):  # a luz entre as pregas
        f.p(x, y, "panoLuz")


def _pano_na_caneca(f):
    """A parte que a mão empurra para dentro da caneca: a dobra por cima da borda (a luz em cima, a sombra onde entra
    na boca) e o pano descendo pelo lado da caneca até a mão."""
    f.grade(153, 48, [
        "..LLp.",
        ".LLppS",
        "LppSS.",
        "LpS...",
        "LpS...",
        "LpS...",
        "Lp....",
    ], {"L": "panoLuz", "p": "pano", "S": "panoSombra"})


def _figura_com_pano():
    f = GT.Figura()
    GT.tronco(f)
    GT.cabeca(f)
    GT.bracos(f)
    GT.dobras(f)
    _pano_pendente(f)
    _mao(f)
    GT.caneca(f)
    _pano_na_caneca(f)
    GT.mao_esquerda(f)
    return f


def pano(tav):
    """O pano novo: onde o desenho da G com o pano novo difere do da G (o pano, o que ele cobria e o que agora cobre),
    entram os pixels novos, com a luz da G; o resto da camada (com os retoques da G2) fica. A pele que o pano antigo
    cobria passa pelo mesmo retoque da G2 (`pele_lisa`)."""
    antiga = G.luz(GT.figura().tela())
    nova = G.luz(_figura_com_pano().tela())
    x0, y0, x1, y1 = 144, 44, 172, G.BT
    caixa = np.zeros(antiga.a.shape[:2], bool)
    caixa[y0:y1, x0:x1] = True
    muda = caixa & (antiga.a != nova.a).any(axis=2)
    tav[muda] = nova.a[muda]
    R2.pele_lisa(tav)
    return int(muda.sum())


# ---------------------------------------------------------------- o freguês da esquerda
class _Vulto:
    """Uma figura escura construída por partes, no espaço da cena: três tons do escuro da G (vulto, vultoMeio,
    vultoLuz), o lado virado para o fogo (lx, ly) mais claro."""

    def __init__(self, lx=0.75, ly=-0.65):
        self.px, self.lx, self.ly = {}, lx, ly

    def p(self, x, y, cor):
        self.px[(int(x), int(y))] = G.C.get(cor, cor)

    def _tom(self, s, luz, sombra):
        return "vultoLuz" if s > luz else "vulto" if s < sombra else "vultoMeio"

    def elipse(self, cx, cy, rx, ry, luz=0.72, sombra=0.1):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                ox, oy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if ox * ox + oy * oy <= 1:
                    self.p(x, y, self._tom(ox * self.lx + oy * self.ly, luz, sombra))

    def membro(self, a, b, r, luz=0.72, sombra=0.1):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        l2 = dx * dx + dy * dy or 1
        for y in range(int(min(ay, by) - r) - 1, int(max(ay, by) + r) + 2):
            for x in range(int(min(ax, bx) - r) - 1, int(max(ax, bx) + r) + 2):
                cx, cy = x + 0.5, y + 0.5
                t = max(0, min(1, ((cx - ax) * dx + (cy - ay) * dy) / l2))
                ox, oy = cx - (ax + t * dx), cy - (ay + t * dy)
                if (ox * ox + oy * oy) ** 0.5 <= r:
                    self.p(x, y, self._tom((ox * self.lx + oy * self.ly) / r, luz, sombra))

    def poligono(self, pts, cor):
        t = Tela(G.QW, G.QH)
        t.poligono(pts, G.C.get(cor, cor))
        for y, x in zip(*np.nonzero(t.a[:, :, 3])):
            self.px[(int(x), int(y))] = G.C.get(cor, cor)

    def tela(self):
        t = Tela(G.QW, G.QH)
        for (x, y), c in self.px.items():
            t.px(x, y, c)
        return t


def _fregues_novo():
    """Sentado ao balcão, de três quartos de costas, virado para o taverneiro. A anatomia primeiro: a cabeça (~19×22
    px, a de um adulto a essa distância), o pescoço, os ombros quase horizontais (o de lá sai do quadro), o ombro de cá
    redondo, o braço descendo do ombro para baixo do quadro (o cotovelo apoiado no balcão fica abaixo da borda), as
    costas entre a gola e o braço; depois a roupa por cima (a capa com a gola amontoada, a dobra entre as costas e o
    braço). A lareira, à direita e acima dele, acende o contorno da cabeça, da orelha, do ombro e do braço."""
    v = _Vulto()
    QH = G.QH
    # as costas, da gola até a borda de baixo, entre o canto e o braço
    v.poligono([(-1, 76), (6, 74), (16, 75), (25, 77), (30, 80), (31, QH), (-1, QH)], "vulto")
    # o braço de cá: o ombro redondo e o braço descendo, um pouco para a frente (para o balcão)
    v.membro((33, 83), (38, 99), 6.2)
    v.elipse(32, 81, 6.8, 5.6)
    # a dobra entre as costas e o braço
    for x, y in ((28, 86), (28, 87), (29, 88), (29, 89), (29, 90), (30, 91), (30, 92), (30, 93), (31, 94), (31, 95)):
        v.p(x, y, "vulto")
    # o pescoço e a gola da capa amontoada em volta dele
    v.poligono([(7, 70), (18, 70), (19, 77), (7, 77)], "vulto")
    v.poligono([(-1, 74), (6, 72), (15, 73), (22, 76), (17, 79), (5, 79), (-1, 78)], "vultoMeio")
    for x, y in ((17, 73), (19, 74), (21, 75), (24, 77), (27, 78), (29, 79)):  # a luz no alto da gola e do ombro
        v.p(x, y, "vultoLuz")
    # a cabeça, de três quartos de costas: o cabelo, a orelha de cá, a linha da barba atrás da orelha
    v.elipse(11, 63, 9.5, 10.5, luz=0.7, sombra=0.0)
    for x, y in ((6, 56), (10, 54), (4, 61), (13, 57)):  # o crespo do cabelo
        v.p(x, y, "vultoMeio")
    for y in range(61, 66):  # a orelha
        v.p(19, y, "#3a2416" if y in (62, 63) else "vultoLuz")
    v.p(18, 63, "vulto")
    for x, y in ((19, 67), (19, 68), (18, 69), (17, 70)):  # a linha da barba, do queixo até a orelha
        v.p(x, y, "vultoMeio")
    return v.tela()


def fregues_esquerda(frente):
    """Troca o freguês da G2 pelo novo: onde o da G e o da G2 estavam, volta o balcão (pelo desenho da G, com a luz
    dela); por cima, o novo, com a mesma luz."""
    antigo = Tela(G.QW, G.QH)
    G.fregues_esquerda(G.Pincel(antigo))
    g2 = Tela(G.QW, G.QH)
    R2._vulto_esquerda(G.Pincel(g2))
    atras = Tela(G.QW, G.QH)
    pa = G.Pincel(atras)
    G.balcao(pa)
    G.caneca_do_fregues(pa)
    G.luz(atras)
    tirar = (antigo.a[:, :, 3] > 0) | (g2.a[:, :, 3] > 0)
    frente[tirar] = atras.a[tirar]
    novo = G.luz(_fregues_novo())
    return int(tirar.sum()) + _colar(frente, novo)


def aplicar(q):
    """{camada: [imagem, ...]} da G2 → as mesmas camadas com as correções da G3 (cópias; a G2 não muda)."""
    from PIL import Image
    tav = np.array(q["taverneiro"][0].convert("RGBA"))
    fundo = np.array(q["fundo"][0].convert("RGBA"))
    frente = np.array(q["frente"][0].convert("RGBA"))
    feitos = {"garrafas": garrafas(fundo), "pano": pano(tav), "fregues": fregues_esquerda(frente)}
    novo = dict(q)
    novo["taverneiro"] = [Image.fromarray(tav, "RGBA")]
    novo["fundo"] = [Image.fromarray(fundo, "RGBA")]
    novo["frente"] = [Image.fromarray(frente, "RGBA")]
    return novo, feitos
