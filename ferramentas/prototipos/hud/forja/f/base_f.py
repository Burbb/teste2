"""A base do ambiente da forja F: a referência reduzida por área à grade do jogo (320 de largura; a altura do quadro da
forja, 96, recortada da redução de 320×107), mapeada na paleta por materiais e limpa dos pixels soltos. É o subdesenho:
os retoques à mão (retoques_f.py) corrigem por cima os planos, as silhuetas e os objetos."""
import pathlib

import numpy as np
from PIL import Image

from paleta_f import TODAS, hx

RAIZ = pathlib.Path(__file__).resolve().parents[5]
REFERENCIA = RAIZ / "ferramentas" / "arte" / "referencias" / "forja" / "A forja sombria do ferreiro.png"
QW, QH = 320, 96
TOPO = 4  # as linhas de cima da redução (320×107) que ficam fora do quadro: só a viga mais alta

P = np.array([hx(c) for c in TODAS], float)
PESO = np.array([0.30, 0.59, 0.11]) ** 0.5


# O ferreiro sai do fundo (ele é camada própria, com as poses): a área dele (em pixels do quadro), pintada na
# resolução da referência com a parede de pedra e o chão de lajes antes da redução, para o remendo ter a mesma textura.
AREA_FERREIRO = [(146, 12), (168, 12), (168, 28), (178, 31), (187, 36), (190, 48), (190, 64), (190, 76), (190, 90),
                 (150, 90), (150, 66), (143, 64), (143, 54), (153, 52), (150, 44), (144, 40), (144, 24)]
CHAO_Y = 73  # onde a parede encontra o chão, em pixels do quadro


def _sorteio(*a):
    v = 0
    for n in a:
        v = (v * 1103515245 + int(n) * 2654435761 + 12345) & 0xFFFFFFFF
    v ^= v >> 13
    return ((v * 1274126177) & 0xFFFFFFFF) / 4294967296.0


def sem_ferreiro(im):
    """A referência com a área do ferreiro repintada: pedras (as cores tiradas da parede à direita dele, na mesma luz)
    e, abaixo da linha do chão, lajes (as cores do chão perto dele)."""
    from PIL import ImageDraw
    a = np.asarray(im).copy()
    sx, sy = im.width / QW, im.height / 107
    mascara = Image.new("L", im.size, 0)
    ImageDraw.Draw(mascara).polygon([(x * sx, (y + TOPO) * sy) for x, y in AREA_FERREIRO], fill=255)
    m = np.asarray(mascara) > 0
    # a parede atrás do suporte de ferramentas (sem as ferramentas: só a metade mais escura), o chão entre as botas e a tina
    parede = a[int((14 + TOPO) * sy):int((60 + TOPO) * sy), int(186 * sx):int(211 * sx)].reshape(-1, 3)
    parede = parede[parede.sum(1) < np.percentile(parede.sum(1), 50)]
    chao = a[int((CHAO_Y + TOPO + 10) * sy):int((CHAO_Y + TOPO + 18) * sy), int(186 * sx):int(197 * sx)].reshape(-1, 3)
    pm, cm = parede.mean(0), chao.mean(0)
    yy, xx = np.nonzero(m)
    linha_chao = (CHAO_Y + TOPO) * sy
    for y, x in zip(yy, xx):
        if y < linha_chao:  # pedras de ~7×5 px do quadro, fiadas desencontradas
            fi = int(y / (5 * sy)); off = _sorteio(fi) * 7 * sx
            col = int((x + off) / (7 * sx))
            dy, dx = y - fi * 5 * sy, (x + off) - col * 7 * sx
            junta = dy > 4.2 * sy or dx > 6.3 * sx
            v = 0.45 if junta else 0.7 + _sorteio(fi, col) * 0.3 + (0.12 if dy < 0.8 * sy else 0)
            a[y, x] = np.clip(pm * v, 0, 255)
        else:
            fi = int((y - linha_chao) / (5 * sy)); off = _sorteio(fi, 3) * 14 * sx
            col = int((x + off) / (14 * sx))
            dy, dx = (y - linha_chao) - fi * 5 * sy, (x + off) - col * 14 * sx
            junta = dy > 4.2 * sy or dx > 13.3 * sx
            v = 0.4 if junta else 0.65 + _sorteio(fi, col, 5) * 0.35
            a[y, x] = np.clip(cm * v, 0, 255)
    return Image.fromarray(a)


def guia(com_ferreiro=True):
    """A redução por área (a média de cada bloco de 6,8 px da referência), no recorte do quadro."""
    im = Image.open(REFERENCIA).convert("RGB")
    if not com_ferreiro:
        im = sem_ferreiro(im)
    return im.resize((QW, 107), Image.BOX).crop((0, TOPO, QW, TOPO + QH))


def mapear(img, cores=None):
    """Cada pixel na cor mais próxima da paleta (distância pesada pela luminância), sem pontilhado."""
    pal = P if cores is None else np.array([hx(c) for c in cores], float)
    a = np.asarray(img, float)
    d = (((a[:, :, None, :] - pal[None, None]) * PESO) ** 2).sum(-1)
    return pal[d.argmin(-1)].astype(np.uint8)


def superpixels(img, passo=3, m=8.0, voltas=6):
    """Agrupa a guia em superpixels (SLIC: pela cor e pela distância, um a cada `passo` px) e pinta cada um com a cor
    média: os planos ficam inteiros e as bordas dos objetos continuam onde estão."""
    a = np.asarray(img, float)
    h, w, _ = a.shape
    ys, xs = np.mgrid[0:h, 0:w]
    cy, cx = np.mgrid[passo // 2:h:passo, passo // 2:w:passo]
    cy, cx = cy.ravel().astype(float), cx.ravel().astype(float)
    cc = a[cy.astype(int), cx.astype(int)]
    rot = np.zeros((h, w), int)
    for _ in range(voltas):
        dist = np.full((h, w), np.inf)
        for i in range(len(cy)):
            y0, y1 = int(max(0, cy[i] - 2 * passo)), int(min(h, cy[i] + 2 * passo + 1))
            x0, x1 = int(max(0, cx[i] - 2 * passo)), int(min(w, cx[i] + 2 * passo + 1))
            d = ((a[y0:y1, x0:x1] - cc[i]) ** 2).sum(-1) + (m / passo) ** 2 * ((ys[y0:y1, x0:x1] - cy[i]) ** 2 + (xs[y0:y1, x0:x1] - cx[i]) ** 2)
            mk = d < dist[y0:y1, x0:x1]
            dist[y0:y1, x0:x1][mk] = d[mk]
            rot[y0:y1, x0:x1][mk] = i
        for i in range(len(cy)):
            mk = rot == i
            if mk.any():
                cy[i], cx[i] = ys[mk].mean(), xs[mk].mean()
                cc[i] = a[mk].mean(0)
    out = np.zeros_like(a)
    for i in range(len(cy)):
        mk = rot == i
        if mk.any():
            out[mk] = a[mk].mean(0)
    return Image.fromarray(out.astype(np.uint8))


def realcar(img, contraste=0.6, saturacao=1.15, gama=0.9):
    """Devolve à guia um pouco do contraste local e da cor que a média por bloco tira (os realces e os contornos da
    referência se misturam na redução)."""
    from PIL import ImageFilter
    a = np.asarray(img, float)
    borr = np.asarray(img.filter(ImageFilter.GaussianBlur(2.0)), float)
    a = a + contraste * (a - borr)
    cinza = a.mean(-1, keepdims=True)
    a = cinza + saturacao * (a - cinza)
    a = 255 * (np.clip(a, 0, 255) / 255) ** gama
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def base():
    """O subdesenho: a guia sem o ferreiro, realçada, em superpixels, na paleta."""
    return mapear(superpixels(realcar(guia(com_ferreiro=False))))


if __name__ == "__main__":
    import sys
    saida = pathlib.Path(sys.argv[1])
    b = Image.fromarray(base())
    b.save(saida / "base.png")
    b.resize((QW * 4, QH * 4), Image.NEAREST).save(saida / "base-x4.png")
