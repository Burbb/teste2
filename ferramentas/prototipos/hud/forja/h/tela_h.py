"""Uma camada de pixels (RGBA) com o que os desenhos da forja F usam: o pixel, o retângulo, a linha, o polígono e a
grade (um caractere por pixel, como nos outros desenhos à mão do projeto)."""
import numpy as np
from PIL import Image

from paleta_h import hx


def rgba(cor):
    if cor is None:
        return None
    if isinstance(cor, str):
        return (*hx(cor), 255)
    return tuple(cor) if len(cor) == 4 else (*cor, 255)


class Tela:
    def __init__(self, w, h, fundo=None):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.uint8)
        if fundo is not None:
            f = np.asarray(fundo)
            self.a[:, :, :3] = f[:, :, :3]
            self.a[:, :, 3] = f[:, :, 3] if f.shape[2] == 4 else 255

    def px(self, x, y, cor):
        x, y = int(round(x)), int(round(y))
        c = rgba(cor)
        if c and 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = c

    def ret(self, x, y, w, h, cor):
        c = rgba(cor)
        if not c:
            return
        x0, y0, x1, y1 = max(0, x), max(0, y), min(self.w, x + w), min(self.h, y + h)
        if x1 > x0 and y1 > y0:
            self.a[y0:y1, x0:x1] = c

    def linha(self, x0, y0, x1, y1, cor):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.px(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, cor)

    def poligono(self, pts, cor):
        """Preenche o polígono (regra par-ímpar, pelos centros dos pixels)."""
        c = rgba(cor)
        ys = [p[1] for p in pts]
        for y in range(max(0, int(min(ys))), min(self.h, int(max(ys)) + 1)):
            cy = y + 0.5
            xs = []
            for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
                if (ay <= cy < by) or (by <= cy < ay):
                    xs.append(ax + (cy - ay) * (bx - ax) / (by - ay))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                for x in range(max(0, int(np.ceil(a - 0.5))), min(self.w, int(np.floor(b - 0.5)) + 1)):
                    self.a[y, x] = c

    def grade(self, x0, y0, linhas, pal):
        for y, l in enumerate(linhas):
            for x, ch in enumerate(l):
                if ch in pal and pal[ch]:
                    self.px(x0 + x, y0 + y, pal[ch])

    def mistura(self, x, y, rgb, alfa):
        """Pinta por cima com transparência (a luz e a sombra feitas por cima, como as cenas do jogo)."""
        if 0 <= x < self.w and 0 <= y < self.h and self.a[y, x, 3]:
            p = self.a[y, x, :3].astype(float)
            self.a[y, x, :3] = (p + (np.array(rgb, float) - p) * alfa).round().astype(np.uint8)

    def get(self, x, y):
        return tuple(self.a[y, x])

    def sobre(self, outra, x=0, y=0):
        """Põe a outra camada por cima (o alfa é 0 ou 255)."""
        b = outra.a
        h, w = b.shape[:2]
        for yy in range(h):
            for xx in range(w):
                if b[yy, xx, 3] and 0 <= x + xx < self.w and 0 <= y + yy < self.h:
                    self.a[y + yy, x + xx] = b[yy, xx]

    def imagem(self):
        return Image.fromarray(self.a, "RGBA")
