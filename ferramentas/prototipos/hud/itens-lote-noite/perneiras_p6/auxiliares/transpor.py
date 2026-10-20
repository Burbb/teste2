"""A P6, as perneiras de malha com os reforços de aço (20/10/2026): a transposição da imagem gerada do Jean
(ferramentas/arte/referencias/calça/perneiras-gerada.webp, pixel art ampliada, o pixel de ~11,8 px: um desenho de
~48 × 81 px) para o 32, pelo processo das botas B3:
  1. a guia: a caixa do desenho (o alfa) reduzida pela média de cada bloco, na proporção dela (a altura de ALTURA px, a
     largura pela mesma escala: sem esticar nem alargar as pernas), centrada no quadro;
  2. o rascunho: cada pixel na cor mais perto da paleta do conjunto (o ferro, o couro, o contorno); a malha (a textura de
     xadrez da referência, achada pelo contraste entre vizinhos na imagem grande) refeita como na cota: o xadrez de dois
     tons vizinhos, o tom do volume (a luminosidade da guia) e o de baixo;
  3. o contorno por dentro (a beira da silhueta da guia vira contorno, como o desenho da referência).
Os ajustes à mão vêm depois (ajustes.py). Grava previa/guia-32.png e grades/rascunho.txt.
    python transpor.py <pasta da P6>
"""
import pathlib
import sys

import numpy as np
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[6]
REF = RAIZ / "ferramentas/arte/referencias/calça/perneiras-gerada.webp"
ALTURA = 30
RAMPA_FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
RAMPA_COURO = dict(b="251412", c="3a1f1a", d="522c23", e="6b3b2d", f="86503c")
h = lambda c: np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], float)
PALETA = {str(t): h(RAMPA_FERRO[t]) for t in range(1, 9)}
PALETA.update({k: h(v) for k, v in RAMPA_COURO.items()})
PALETA["#"] = h("08080a")
LUM = lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def caixa(a):
    rgb = a[..., :3]; d = np.sqrt(((rgb - 255) ** 2).sum(axis=2))
    ys, xs = np.where((a[..., 3] >= 128) & (d > 40))
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def guia_e_malha():
    a = np.array(Image.open(REF).convert("RGBA")).astype(float)
    x0, y0, x1, y1 = caixa(a)
    s = ALTURA / (y1 - y0); w = round((x1 - x0) * s)
    c = a[y0:y1, x0:x1].copy(); c[..., :3] *= c[..., 3:] / 255
    r = np.array(Image.fromarray(c.astype("uint8"), "RGBA").resize((w, ALTURA), Image.BOX)).astype(float)
    al = r[..., 3:]; cor = np.where(al > 0, r[..., :3] * 255 / np.maximum(al, 1), 0)
    # a malha: o contraste entre pixels vizinhos (o xadrez de 1 px nativo) na imagem grande, por bloco
    g = (a[y0:y1, x0:x1, :3] @ [0.3, 0.59, 0.11]); qx = np.abs(np.diff(g, axis=1))[:-1] + np.abs(np.diff(g, axis=0))[:, :-1]
    H, W = qx.shape
    malha = np.zeros((ALTURA, w))
    for Y in range(ALTURA):
        for X in range(w):
            malha[Y, X] = qx[int(Y * H / ALTURA):int((Y + 1) * H / ALTURA), int(X * W / w):int((X + 1) * W / w)].mean()
    out = np.zeros((32, 32, 4)); m = np.zeros((32, 32))
    ox, oy = (32 - w) // 2, (32 - ALTURA) // 2
    out[oy:oy + ALTURA, ox:ox + w, :3] = cor; out[oy:oy + ALTURA, ox:ox + w, 3] = al[..., 0]
    m[oy:oy + ALTURA, ox:ox + w] = malha
    return out, m


def rascunho(g, m, limiar):
    S = {(x, y) for y in range(32) for x in range(32) if g[y, x, 3] >= 128}
    lin = []
    for y in range(32):
        l = ""
        for x in range(32):
            if (x, y) not in S: l += "."; continue
            if any((x + dx, y + dy) not in S for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): l += "#"; continue
            c = g[y, x, :3]
            k = min(PALETA, key=lambda k: (((c - PALETA[k]) ** 2) * [3, 4, 2]).sum())
            if k.isdigit() and m[y, x] > limiar:      # a malha: o volume pela luminosidade, o xadrez por cima
                t = min(range(2, 8), key=lambda t: abs(LUM(PALETA[str(t)]) - LUM(c)))
                k = str(t if (x + y) % 2 == 0 else max(t - 1, 2))   # como a cota: o tom do volume e o de baixo
            l += k
        lin.append(l)
    return lin


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1]); limiar = float(sys.argv[2]) if len(sys.argv) > 2 else 40
    g, m = guia_e_malha()
    (base / "previa").mkdir(exist_ok=True); (base / "grades").mkdir(exist_ok=True)
    Image.fromarray(g.astype("uint8"), "RGBA").save(base / "previa/guia-32.png")
    np.save(base / "previa/malha.npy", m)
    r = rascunho(g, m, limiar)
    (base / "grades/rascunho.txt").write_text("\n".join(r) + "\n", encoding="utf-8")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(r)))
    print("contraste (malha): min", round(m[m > 0].min(), 1), "méd", round(m[m > 0].mean(), 1), "máx", round(m.max(), 1))
