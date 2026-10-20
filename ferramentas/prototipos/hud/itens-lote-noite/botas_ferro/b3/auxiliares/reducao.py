"""O ponto de partida da B3 (20/10/2026): a referência gerada do Jean (ferramentas/arte/referencias/botas/Botas
blindadas de ferro pesado.png, 1254×1254, pixel art ampliada com o pixel de ~17,6 px: um desenho de ~58 px) reduzida
proporcionalmente para o quadro de 32, sem esticar: a caixa do desenho (quadrada) em LADO px, centrada, com a média de
cada bloco sobre o fundo transparente. Depois, cada pixel vai para o material e o tom da paleta do conjunto:
  contorno (o preto da linha), interior (o escuro das aberturas), couro (as tiras, as solas), fivela, aço (a rampa de
  ferro pela luminosidade).
Cada pixel do 32 fica com o material que mais aparece no bloco correspondente da referência (o tom pela média só
desse material), e não com a média das cores: a média misturava o contorno preto com o aço e embarrava as bordas.
O resultado é só o rascunho: a grade final (grades/B3.txt) é ajustada à mão.
    python reducao.py <pasta da B3> [LADO]       # grava previa/guia-32.png (as cores da referência) e grades/rascunho.txt
"""
import pathlib
import sys

import numpy as np
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[7]
REF = RAIZ / "ferramentas/arte/referencias/botas/Botas blindadas de ferro pesado.png"
CAIXA = (145, 143, 1159, 1159)   # a caixa do desenho (o alfa), medida


def reduzir(lado):
    """A guia: a caixa do desenho reduzida para lado × lado (a média de cada bloco, premultiplicada), centrada no 32."""
    im = Image.open(REF).convert("RGBA").crop(CAIXA)
    a = np.array(im).astype(float)
    a[..., :3] *= a[..., 3:] / 255
    r = np.array(Image.fromarray(a.astype("uint8"), "RGBA").resize((lado, lado), Image.BOX)).astype(float)
    alfa = r[..., 3:]
    cor = np.where(alfa > 0, r[..., :3] * 255 / np.maximum(alfa, 1), 0)
    out = np.zeros((32, 32, 4))
    o = (32 - lado) // 2
    out[o:o + lado, o:o + lado, :3] = cor; out[o:o + lado, o:o + lado, 3] = alfa[..., 0]
    return out


# os materiais de cada pixel da referência, pelas cores medidas nela: o contorno (preto neutro), o interior das aberturas
# (castanho muito escuro), o couro (castanho), a fivela (ouro), o aço (cinza-azulado, do escuro ao quase branco)
VAZIO, CONTORNO, INTERIOR, COURO, FIVELA, ACO = range(6)


def classificar():
    a = np.array(Image.open(REF).convert("RGBA").crop(CAIXA)).astype(float)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    quente = (r - b > 15) & (r >= g)
    m = np.full(lum.shape, ACO)
    m[quente & (lum >= 34)] = COURO
    m[quente & (lum < 34)] = INTERIOR
    m[(r > 150) & (b < 100) & (r - b > 60)] = FIVELA
    m[(lum < 22) & ~quente] = CONTORNO
    m[al < 128] = VAZIO
    return m, lum


# as rampas do conjunto (as do grade.lua) e a luminosidade de cada tom: o pixel vai para o tom de luminosidade mais perto
RAMPA_FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
RAMPA_COURO = dict(a="140b09", b="251412", c="3a1f1a", d="522c23", e="6b3b2d", f="86503c")
_l = lambda h: 0.3 * int(h[0:2], 16) + 0.59 * int(h[2:4], 16) + 0.11 * int(h[4:6], 16)
def tom_aco(l): return min(range(2, 9), key=lambda t: abs(_l(RAMPA_FERRO[t]) - l))
def tom_couro(l): return min("bcdef", key=lambda t: abs(_l(RAMPA_COURO[t]) - l))


def paleta():
    """As cores possíveis: a rampa de ferro (2..8), a de couro (b..f), o interior das aberturas e o contorno."""
    h = lambda c: tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    P = {str(t): h(RAMPA_FERRO[t]) for t in range(2, 9)}
    P.update({k: h(v) for k, v in RAMPA_COURO.items() if k != "a"})
    P["i"] = h("100a08"); P["#"] = (8, 8, 10)
    return P


def rascunho_guia(lado):
    """Da guia (a média de cada bloco): cada pixel com metade ou mais de cobertura vai para a cor mais perto da paleta
    (pela distância de cor); o contorno de fora com 1 px, pelos lados, em volta do que ficou."""
    r = reduzir(lado); P = paleta()
    g = [["."] * 32 for _ in range(32)]
    for y in range(32):
        for x in range(32):
            if r[y, x, 3] < 128: continue
            c = r[y, x, :3]
            g[y][x] = min(P, key=lambda k: sum((c[i] - P[k][i]) ** 2 * (3, 4, 2)[i] for i in range(3)))
    antes = [l[:] for l in g]                     # o contorno olha a grade antes dele (senão se espalha)
    cheio = lambda x, y: 0 <= x < 32 and 0 <= y < 32 and antes[y][x] != "."
    for y in range(32):
        for x in range(32):
            if antes[y][x] == "." and (cheio(x - 1, y) or cheio(x + 1, y) or cheio(x, y - 1) or cheio(x, y + 1)): g[y][x] = "#"
    return ["".join(l) for l in g]


def rascunho(lado):
    """Cada pixel do lado × lado: o material que mais aparece no bloco da referência (o vazio só se for a maioria; o
    contorno se cobrir um terço do bloco), o tom pela média da luminosidade daquele material no bloco."""
    m, lum = classificar()
    H, W = m.shape
    g = [["."] * 32 for _ in range(32)]
    o = (32 - lado) // 2
    for Y in range(lado):
        for X in range(lado):
            bm = m[int(Y * H / lado):int((Y + 1) * H / lado), int(X * W / lado):int((X + 1) * W / lado)]
            bl = lum[int(Y * H / lado):int((Y + 1) * H / lado), int(X * W / lado):int((X + 1) * W / lado)]
            n = np.bincount(bm.ravel(), minlength=6) / bm.size
            if n[VAZIO] > 0.5: continue
            if n[CONTORNO] > 0.33: ch = "#"
            else:
                k = max((INTERIOR, COURO, FIVELA, ACO), key=lambda c: n[c])
                l = bl[bm == k].mean()
                ch = {INTERIOR: "i", FIVELA: "Y"}.get(k) or (tom_couro(l) if k == COURO else str(tom_aco(l)))
            g[o + Y][o + X] = ch
    return ["".join(l) for l in g]


def linhas(lado):
    """Quanto de cada pixel do lado × lado é linha preta na referência (o contorno e as junções das placas)."""
    m, _ = classificar()
    H, W = m.shape
    f = np.zeros((32, 32)); o = (32 - lado) // 2
    for Y in range(lado):
        for X in range(lado):
            bm = m[int(Y * H / lado):int((Y + 1) * H / lado), int(X * W / lado):int((X + 1) * W / lado)]
            f[o + Y, o + X] = (bm == CONTORNO).mean()
    return f


def com_linhas(g, f, forte=0.25):
    """As linhas da referência sobre o rascunho: onde a linha preta cobre `forte` do pixel, ele vira contorno (encostando
    no lado de fora) ou a junção escura das placas (por dentro, o tom 1); o interior das aberturas, o couro e a fivela
    ficam."""
    g = [list(l) for l in g]
    fora = lambda x, y: not (0 <= x < 32 and 0 <= y < 32) or g[y][x] in ".#"
    for y in range(32):
        for x in range(32):
            ch = g[y][x]
            if ch in ".#i" or ch in "cdef" or f[y, x] < forte: continue
            borda = any(fora(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            g[y][x] = "#" if borda else "1"
    return ["".join(l) for l in g]


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1]); lado = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    r = reduzir(lado)
    (base / "previa").mkdir(exist_ok=True); (base / "grades").mkdir(exist_ok=True)
    Image.fromarray(np.clip(r, 0, 255).astype("uint8"), "RGBA").save(base / "previa/guia-32.png")
    g = rascunho_guia(lado) if "--materiais" not in sys.argv else rascunho(lado)
    (base / "grades/rascunho.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    g = com_linhas(g, linhas(lado))
    (base / "grades/rascunho-linhas.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(g)))
