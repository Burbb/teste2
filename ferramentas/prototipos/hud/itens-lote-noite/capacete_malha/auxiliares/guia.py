"""A guia do C1, o capacete com malha da imagem gerada do Jean (20/10/2026,
ferramentas/arte/referencias/capacete/capacete-malha-gerada.webp: pixel art ampliada, o pixel de ~24 px, um desenho de
~36 × 44 px; não é uma grade de 32). A caixa do desenho (o opaco, fora do halo claro do fundo transparente) reduzida
pela média de cada bloco, na proporção dela (ALTURA px de altura, a largura pela mesma escala: sem esticar nem alargar), centrada no quadro de 32.
Grava previa/guia-32.png e imprime, para a grade à mão (grade.py):
  - a silhueta (a cobertura de cada pixel: '#' cheio, '+' meio, '.' fora);
  - o material provável (c: couro, pelo tom quente) e o tom de ferro mais perto pela luminosidade (0 a 8), que dá o
    volume de cada parte.
    python guia.py <pasta do C1>
"""
import pathlib
import sys

import numpy as np
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[6]
REF = RAIZ / "ferramentas/arte/referencias/capacete/capacete-malha-gerada.webp"
ALTURA = 30
FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
LUM = [0.3 * int(c[0:2], 16) + 0.59 * int(c[2:4], 16) + 0.11 * int(c[4:6], 16) for c in FERRO]


def guia():
    a = np.array(Image.open(REF).convert("RGBA")).astype(float)
    # o desenho: opaco e fora do branco em volta (a imagem tem fundo transparente com um halo claro)
    d = np.where(a[..., 3] >= 128, np.sqrt(((a[..., :3] - 255) ** 2).sum(axis=2)), 0)
    ys, xs = np.where(d > 60)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    c = a[y0:y1, x0:x1].copy()
    c[..., 3] = np.where(d[y0:y1, x0:x1] > 60, 255, 0)
    c[..., :3] *= c[..., 3:] / 255
    w = round((x1 - x0) * ALTURA / (y1 - y0))
    r = np.array(Image.fromarray(c.astype("uint8"), "RGBA").resize((w, ALTURA), Image.BOX)).astype(float)
    al = r[..., 3:]
    r[..., :3] = np.where(al > 0, r[..., :3] * 255 / np.maximum(al, 1), 0)
    out = np.zeros((32, 32, 4))
    ox, oy = (32 - w) // 2, (32 - ALTURA) // 2
    out[oy:oy + ALTURA, ox:ox + w] = r
    return out, (x0, y0, x1, y1), (ox, oy, w)


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g, cx, (ox, oy, w) = guia()
    (base / "previa").mkdir(exist_ok=True)
    Image.fromarray(g.astype("uint8"), "RGBA").save(base / "previa/guia-32.png")
    print("caixa na referência", cx, "; no 32: x", ox, "a", ox + w - 1, ", linhas", oy, "a", oy + ALTURA - 1)
    print("    " + "".join(str(x % 10) for x in range(32)))
    for y in range(32):
        sil, ton = "", ""
        for x in range(32):
            r, gg, b, al = g[y, x]
            sil += "#" if al >= 192 else "+" if al >= 64 else "."
            l = 0.3 * r + 0.59 * gg + 0.11 * b
            ton += "." if al < 64 else "c" if r - b > 25 else str(min(range(9), key=lambda t: abs(LUM[t] - l)))
        print(f"{y:2d}  {sil}   {ton}")
