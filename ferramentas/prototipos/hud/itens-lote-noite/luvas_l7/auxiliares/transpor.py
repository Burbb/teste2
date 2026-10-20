"""A L7, o par de luvas de couro com a malha (20/10/2026): a transposição do recorte escolhido pelo Jean
(ferramentas/arte/referencias/Luvas/luvas-par-recorte.png: uma captura de pixel art, o pixel de ~3,45 px de tela, sobre
um fundo azul-acinzentado e com marca d'água) para a grade de 32, pelo processo das botas B3.
  1. a grade nativa: em cada célula do pixel do recorte (o período e a fase medidos), a cor mediana do miolo (fora do
     borrão da captura); o par dá ~29 × 30 px, que cabe no 32 na escala 1:1: só deslocado para centrar, sem esticar;
  2. o fundo (perto da cor dele) e a marca d'água fora do par saem: a guia (previa/guia-32.png);
  3. cada pixel na cor mais perto da paleta do conjunto (o couro b..f, o ferro 1..8 da malha e das ferragens, o
     contorno): o rascunho (grades/rascunho.txt). A malha nativa já é o xadrez de dois tons, na escala do jogo.
Os ajustes à mão vêm depois (ajustes.py).
    python transpor.py <pasta da L7>
"""
import pathlib
import sys

import numpy as np
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[6]
REF = RAIZ / "ferramentas/arte/referencias/Luvas/luvas-par-recorte.png"
PERIODO, FX, FY = 3.45, 1.65, 1.3          # o pixel do recorte em pixels de tela e a fase da grade (medidos)
FUNDO = np.array([157, 174, 183.])
DESLOCA = (0, -1)                           # a grade nativa no 32: só centrar (x, y)
RAMPA_FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
RAMPA_COURO = dict(b="251412", c="3a1f1a", d="522c23", e="6b3b2d", f="86503c")
h = lambda c: np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], float)
PALETA = {str(t): h(RAMPA_FERRO[t]) for t in range(1, 9)}
PALETA.update({k: h(v) for k, v in RAMPA_COURO.items()})
PALETA["#"] = h("08080a")


def nativa():
    a = np.array(Image.open(REF).convert("RGB")).astype(float)
    nx = int((a.shape[1] - FX) / PERIODO); ny = int((a.shape[0] - FY) / PERIODO)
    n = np.zeros((ny, nx, 3))
    for j in range(ny):
        for i in range(nx):
            x0 = FX + i * PERIODO; y0 = FY + j * PERIODO
            bloco = a[int(np.ceil(y0 + 0.6)):int(np.floor(y0 + PERIODO - 0.6)) + 1,
                      int(np.ceil(x0 + 0.6)):int(np.floor(x0 + PERIODO - 0.6)) + 1]
            n[j, i] = np.median(bloco.reshape(-1, 3), axis=0)
    return n


def guia():
    n = nativa()
    d = np.sqrt(((n - FUNDO) ** 2).sum(axis=2)); lum = n @ [0.3, 0.59, 0.11]
    fundo = d < 30
    # a marca d'água (clara) e o borrão que só encosta no fundo saem; dentro do par, fica (ajustado à mão)
    clara = lum > 165
    out = np.zeros((32, 32, 4))
    dx, dy = DESLOCA
    for y in range(n.shape[0]):
        for x in range(n.shape[1]):
            X, Y = x + dx, y + dy
            if not (0 <= X < 32 and 0 <= Y < 32) or fundo[y, x] or clara[y, x]: continue
            out[Y, X, :3] = n[y, x]; out[Y, X, 3] = 255
    return out


def rascunho(g):
    linhas = []
    for y in range(32):
        l = ""
        for x in range(32):
            if g[y, x, 3] < 128: l += "."; continue
            c = g[y, x, :3]
            l += min(PALETA, key=lambda k: (((c - PALETA[k]) ** 2) * [3, 4, 2]).sum())
        linhas.append(l)
    return linhas


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g = guia()
    (base / "previa").mkdir(exist_ok=True); (base / "grades").mkdir(exist_ok=True)
    Image.fromarray(g.astype("uint8"), "RGBA").save(base / "previa/guia-32.png")
    r = rascunho(g)
    (base / "grades/rascunho.txt").write_text("\n".join(r) + "\n", encoding="utf-8")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(r)))
