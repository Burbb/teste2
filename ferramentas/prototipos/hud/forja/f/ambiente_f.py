"""O ambiente da forja F: o fundo, a bigorna com o toco, a espada e a tenaz, o fogo e o primeiro plano. O fundo é a
base (base_f.py: a referência reduzida, sem o ferreiro, em superpixels e na paleta), com o suporte de ferramentas
continuado atrás da cabeça dele. Desenhados aqui, à mão ou em código: a bigorna e o toco, a lâmina em brasa e a tenaz
(por estado), o fogo da boca da fornalha (4 quadros) e o recorte das silhuetas da frente (uma camada por cima)."""
import numpy as np

import base_f
from paleta_f import RAMPAS as R, K
from tela_f import Tela

QW, QH = base_f.QW, base_f.QH


def h(*args):
    """Um sorteio fixo por posição (o mesmo desenho sempre)."""
    v = 0
    for a in args:
        v = (v * 1103515245 + int(a) * 2654435761 + 12345) & 0xFFFFFFFF
    v ^= v >> 13
    v = (v * 1274126177) & 0xFFFFFFFF
    return (v >> 8) / float(1 << 24)


# ---------------------------------------------------------------- a parede do fundo, no meio (atrás do ferreiro)
def suporte_ferramentas(t):
    """O suporte de ferramentas na parede do fundo continua atrás da cabeça do ferreiro (a referência o mostra de x 165
    em diante; o trecho que o ferreiro escondia é desenhado aqui): a barra de madeira e, penduradas, um martelo, um
    cinzel comprido e uma espada, escuros como as outras ferramentas do suporte."""
    M, Fe = R["madeira"], R["ferro"]
    t.ret(160, 13, 28, 1, K)
    t.ret(160, 14, 28, 1, M[3])
    t.ret(160, 15, 28, 1, M[2])
    t.ret(160, 16, 28, 1, K)
    pal = {"k": K, "a": Fe[0], "b": Fe[1], "c": Fe[2], "d": Fe[3], "m": M[1], "n": M[2]}
    t.grade(165, 16, ["kkkkkkk", "kcddcck", "kbccbbk", "kkkkkkk", "..knk..", "..knk..", "..kmk..", "..knk..", "..kmk..",
                      "..knk..", "..kmk..", "..kmk..", "..kkk.."], pal)
    t.grade(174, 16, ["kk", "kc", "kb", "kb", "kb", "kb", "kb", "kb", "kb", "kb", "kb", "ka", "kk"], pal)
    t.grade(179, 16, [".knk.", ".kmk.", "kkkkk", "kcddk", "kkkkk", ".kck.", ".kbk.", ".kck.", ".kbk.", ".kck.", ".kbk.",
                      ".kck.", ".kbk.", ".kck.", ".kbk.", ".kak.", "..k.."], pal)


def desenhar_fundo():
    t = Tela(QW, QH, base_f.base())
    suporte_ferramentas(t)
    return t


if __name__ == "__main__":
    import sys
    import pathlib
    from PIL import Image
    saida = pathlib.Path(sys.argv[1])
    im = desenhar_fundo().imagem()
    im.save(saida / "fundo.png")
    im.resize((QW * 4, QH * 4), Image.NEAREST).save(saida / "fundo-x4.png")


# ---------------------------------------------------------------- a bigorna no toco (camada própria)
# Linhas por y: trechos (x0, x1, letra), de x0 a x1 inclusive, desenhados em ordem. As letras: o ferro (f a L), o
# reflexo quente do fogo na face (v, V), a madeira do toco (m a P) e o contorno (k).
PAL_BIGORNA = {"k": K, "f": R["pedra"][1], "g": R["ferro"][0], "h": R["ferro"][1], "i": R["ferro"][2], "I": R["ferro"][4],
               "J": R["ferro"][6], "L": R["ferro"][7], "v": R["quente"][2], "V": R["quente"][3], "W": R["quente"][4],
               "m": R["madeira"][0], "M": R["madeira"][1], "n": R["madeira"][2], "N": R["madeira"][3], "o": R["madeira"][4],
               "P": R["madeira"][5], "q": R["quente"][5], "Q": R["quente"][6]}
BIGORNA = {
    60: [(109, 117, "k"), (151, 158, "k")],
    61: [(108, 108, "k"), (109, 157, "J"), (124, 131, "L"), (152, 157, "I"), (158, 158, "I"), (159, 159, "k")],
    62: [(108, 109, "k"), (110, 123, "i"), (124, 124, "h"), (125, 125, "I"), (126, 146, "i"), (130, 141, "V"), (147, 147, "I"),
         (148, 157, "h"), (158, 158, "k")],
    63: [(109, 110, "k"), (111, 123, "h"), (124, 124, "g"), (125, 125, "I"), (126, 146, "h"), (129, 136, "v"), (139, 143, "v"),
         (147, 147, "i"), (148, 156, "g"), (157, 157, "k")],
    64: [(111, 112, "k"), (113, 123, "g"), (124, 124, "f"), (125, 125, "i"), (126, 146, "h"), (132, 134, "v"), (147, 147, "i"),
         (148, 155, "g"), (156, 156, "k")],
    65: [(113, 115, "k"), (116, 123, "g"), (124, 124, "f"), (125, 125, "i"), (126, 146, "h"), (147, 147, "h"),
         (148, 153, "f"), (154, 154, "k")],
    66: [(116, 118, "k"), (119, 123, "f"), (124, 124, "f"), (125, 125, "i"), (126, 146, "g"), (128, 145, "h"), (147, 147, "h"),
         (148, 151, "f"), (152, 152, "k")],
    67: [(119, 121, "k"), (122, 124, "f"), (125, 125, "h"), (126, 146, "g"), (147, 147, "g"), (148, 149, "f"), (150, 150, "k")],
    68: [(122, 127, "k"), (128, 128, "h"), (129, 143, "g"), (144, 144, "f"), (145, 149, "k")],
    69: [(127, 127, "k"), (128, 128, "h"), (129, 143, "g"), (131, 133, "h"), (144, 144, "f"), (145, 145, "k")],
    70: [(127, 127, "k"), (128, 128, "h"), (129, 143, "g"), (144, 144, "f"), (145, 145, "k")],
    71: [(125, 126, "k"), (127, 127, "i"), (128, 144, "g"), (145, 145, "f"), (146, 147, "k")],
    72: [(119, 147, "k"), (124, 124, "k"), (125, 146, "f"), (148, 153, "k")],
    # o toco: o tampo aceso pela fornalha, a casca em tiras, a cinta de ferro com o rebite
    73: [(119, 119, "k"), (120, 152, "N"), (120, 127, "o"), (124, 146, "k"), (147, 152, "n"), (153, 153, "k")],
    74: [(119, 119, "k"), (120, 152, "n"), (120, 126, "N"), (153, 153, "k")],
}
for _y in range(75, 90):
    _l = [(119 if _y < 86 else 120, 119 if _y < 86 else 120, "k")]
    for _x in range(120 if _y < 86 else 121, 153 if _y < 86 else 152):
        _tira = (_x * 7 + (_x // 3) * 5) % 6
        _luz = 2 if _x < 126 else 1 if _x < 136 else 0
        _c = ("nNo"[min(2, _luz - 1 + (1 if _tira == 0 else 0))] if _luz else ("MmM"[_tira % 3] if _x > 145 else "MnM"[_tira % 3]))             if _tira % 3 else ("M" if _luz else "m")
        _l.append((_x, _x, _c))
    _l.append((153 if _y < 86 else 152, 153 if _y < 86 else 152, "k"))
    BIGORNA[_y] = _l
for _y in (77, 78, 79):  # a cinta de ferro, do lado aceso até o meio
    BIGORNA[_y] += [(120, 136, "h" if _y == 77 else "g"), (137, 137, "k")]
BIGORNA[76] += [(120, 137, "k")]
BIGORNA[80] += [(120, 137, "k")]
BIGORNA[78] += [(134, 134, "I")]
BIGORNA[90] = [(121, 151, "k")]


def bigorna():
    t = Tela(QW, QH)
    for y, trechos in BIGORNA.items():
        for x0, x1, ch in trechos:
            for x in range(x0, x1 + 1):
                t.px(x, y, PAL_BIGORNA[ch])
    return t


# ---------------------------------------------------------------- a espada em fabricação e a tenaz (por quadro)
LAMINA = (118, 150, 59)  # da ponta até onde a tenaz pega, a linha de cima


def espada(t, brasa_x, forte=False, virada=False):
    """A lâmina deitada na bigorna: a ponta à esquerda, o fio de cima com a luz, o trecho batido em brasa (mais vivo
    logo depois do golpe), a espiga entrando na tenaz. Virada (a pausa): de lado, só o fio, mais fina."""
    x0, x1, y = LAMINA
    F, Fe = R["fogo"], R["ferro"]
    for x in range(x0, x1 + 1):
        d = abs(x - brasa_x)
        if d < 3:
            cima, baixo = (F[6], F[5]) if forte else (F[5], F[4])
        elif d < 6:
            cima, baixo = F[5] if forte else F[4], F[3]
        elif d < 10:
            cima, baixo = F[4], F[3]
        elif d < 14:
            cima, baixo = F[3], F[2]
        elif d < 18:
            cima, baixo = F[2], F[1]
        else:
            cima, baixo = Fe[4], Fe[2]
        if x == x0:  # a ponta
            t.px(x, y + 1, cima)
            t.px(x - 1, y + 1, K)
            t.px(x, y, K)
            continue
        if virada:
            t.px(x, y, K)
            t.px(x, y + 1, cima)
        else:
            t.px(x, y - 1, K)
            t.px(x, y, cima)
            t.px(x, y + 1, baixo)


def tenaz(t, mao_y=59, virada=False):
    """A tenaz: as duas hastes da luva (x 161) até as garras na espiga (x 149), a de cima com o brilho."""
    Fe = R["ferro"]
    yb = mao_y
    for x in range(150, 162):
        t.px(x, yb - 1, K)
        t.px(x, yb, Fe[4] if x % 4 else Fe[5])
        t.px(x, yb + 1, Fe[1])
        t.px(x, yb + 2, K)
    # as garras fechadas na espiga
    for dy in range(-1 if not virada else 0, 3):
        t.px(148, yb + dy, K)
        t.px(149, yb + dy, Fe[3] if dy <= 0 else Fe[2])


# ---------------------------------------------------------------- o fogo da fornalha (4 quadros)
BOCA = (100, 123, 37, 55)  # a boca do arco por dentro: x0, x1, o alto do arco, o leito


def _dentro_da_boca(x, y):
    x0, x1, yt, yl = BOCA
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    if y < yt + r * 0.55:  # o arco
        return ((x + 0.5 - cx) / r) ** 2 + ((y + 0.5 - (yt + r * 0.55)) / (r * 0.55)) ** 2 <= 1
    return x0 <= x <= x1 and y <= yl


def fogo(t, k):
    """A boca acesa no quadro k (0 a 3): o fundo em brasa escura, as línguas de fogo (a altura e o balanço de cada
    uma mudam por quadro) e o leito de carvão com as brasas piscando."""
    F = R["fogo"]
    x0, x1, yt, yl = BOCA
    for y in range(yt, yl - 2):
        for x in range(x0, x1 + 1):
            if _dentro_da_boca(x, y):
                f = (y - yt) / (yl - yt)
                t.px(x, y, F[0] if f < 0.35 else F[1] if f < 0.7 else F[2])
    # as línguas: (centro, meia largura, alturas por quadro, balanço por quadro)
    linguas = [(102, 1.5, (7, 9, 6, 8), (0, 1, 0, -1)), (106, 2.2, (11, 13, 14, 10), (1, 0, -1, 0)),
               (110, 2.6, (15, 12, 16, 14), (0, -1, 0, 1)), (114, 2.4, (12, 15, 11, 13), (-1, 0, 1, 0)),
               (118, 2.0, (9, 8, 11, 10), (0, 1, 0, -1)), (121, 1.4, (6, 7, 5, 8), (1, 0, -1, 0))]
    base = yl - 3
    for cx, mw, hs, bal in linguas:
        hgt, b = hs[k % 4], bal[k % 4]
        for r in range(hgt):
            f = r / hgt
            meia = mw * (1 - f) ** 0.7
            sx = cx + b * f * 2
            for x in range(int(round(sx - meia)), int(round(sx + meia)) + 1):
                if not _dentro_da_boca(x, base - r):
                    continue
                borda = abs(x - sx) > meia - 0.8
                cor = (F[4] if borda else F[6] if f < 0.2 else F[5]) if f < 0.35 else \
                      (F[3] if borda else F[4]) if f < 0.7 else (F[2] if borda else F[3])
                t.px(x, base - r, cor)
    # o leito: o carvão escuro com brasas
    for y in range(yl - 2, yl + 1):
        for x in range(x0 - 1, x1 + 2):
            v = h(x, y, 31)
            luz = (x * 3 + y * 5 + k * 7) % 11
            cor = F[5] if luz == 0 else F[4] if luz < 3 else F[3] if v > 0.5 else R["pedra"][1] if v < 0.2 else F[1]
            t.px(x, y, cor)


# ---------------------------------------------------------------- o primeiro plano (as silhuetas da frente)
ZONAS_FRENTE = [(0, 64, 150, 96), (150, 86, 216, 96), (216, 50, 320, 96)]
LIVRES = [(119, 60, 154, 92), (148, 30, 192, 89), (196, 60, 224, 93), (238, 52, 320, 79)]  # bigorna, ferreiro, tina, bancada


def frente(base):
    """As silhuetas escuras de baixo (o jarro e as caixas à esquerda, os vultos e a roda à direita): os pixels escuros
    ligados à borda de baixo do quadro, fora da bigorna, do ferreiro, da tina e da bancada. Viram uma camada por cima
    de tudo (enquadram a cena sem cobrir a ação)."""
    a = np.asarray(base.a if hasattr(base, "a") else base)
    lum = a[:, :, 0] * 0.299 + a[:, :, 1] * 0.587 + a[:, :, 2] * 0.114
    livre = lambda x, y: any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in LIVRES)
    pode = lambda x, y: lum[y, x] < 30 and any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in ZONAS_FRENTE) and not livre(x, y)
    vistos, pilha = set(), [(x, QH - 1) for x in range(QW) if pode(x, QH - 1)]
    while pilha:
        x, y = pilha.pop()
        if (x, y) in vistos:
            continue
        vistos.add((x, y))
        for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + ox, y + oy)
            if 0 <= q[0] < QW and 0 <= q[1] < QH and q not in vistos and pode(*q):
                pilha.append(q)
    t = Tela(QW, QH)
    for x, y in vistos:
        t.a[y, x] = a[y, x]
    return t
