# a primeira passada de tons sobre as regiões (auxiliar): grava o mapa em texto para a edição à mão
import sys
from PIL import Image, ImageDraw
n = int(sys.argv[1]); k = n / 24; SS = 8
R = [
 ("K", [(9.6,4.6),(17.6,8.6),(17.0,13.5),(9.0,12.5)]),
 ("F", [(8.8,11.5),(17.0,12.8),(17.2,15.6),(19.5,16.6),(21.8,17.6),(23.0,19.0),(23.0,20.6),(13,20.4),(6.2,17.6),(6.0,14.5),(7.4,12.6)]),
 ("H", [(5.8,16.8),(11.0,17.2),(11.0,20.2),(7.0,20.0),(5.8,18.6)]),
 ("S", [(11,19.4),(17.8,20.2),(22.6,20.4),(23.2,20.2),(23.0,22.2),(22,23.0),(18,22.8),(13,21.8),(11,20.8)]),
 ("C", [(11.0,0.8),(20.8,4.4),(19.8,9.0),(9.6,4.8)]),
 ("I", [(12.2,1.8),(19.9,4.7),(19.5,6.0),(12.0,3.0)]),
 ("T", [(8.0,11.6),(17.0,13.0),(17.0,14.9),(7.8,13.6)]),
 ("B", [(10.0,11.8),(13.2,12.3),(13.0,15.2),(9.8,14.8)]),
]
can = {}
for L, pts in R:
    im = Image.new("L", (n * SS, n * SS)); ImageDraw.Draw(im).polygon([(x * k * SS, y * k * SS) for x, y in pts], fill=255)
    im = im.resize((n, n), Image.BOX)
    for y in range(n):
        for x in range(n):
            if im.getpixel((x, y)) >= 128: can[(x, y)] = L
g = [["."] * n for _ in range(n)]
reg = lambda x, y: can.get((x, y), ".")
for y in range(n):
    for x in range(n):
        r = reg(x, y)
        if r == ".": continue
        col = [yy for yy in range(n) if reg(x, yy) == r]
        row = [xx for xx in range(n) if reg(xx, y) == r]
        if r in "CI":
            ccol = [yy for yy in range(n) if reg(x, yy) in "CI"]; t0, t1 = min(ccol), max(ccol)
            if r == "I": c = "i"
            elif y == t0: c = "6" if x < 0.7 * n else "5"
            elif reg(x, y - 1) == "I": c = "7" if x < 0.6 * n else "6"
            elif y == t1: c = "3" if x < 0.55 * n else "2"
            else: c = "5" if x < 0.5 * n else ("4" if x < 0.72 * n else "3")
            if x == max(xx for xx in range(n) if reg(xx, y) in "CI") and x > 0.7 * n and r == "C": c = str(max(1, int(c) - 1)) if c.isdigit() else c
        elif r == "K":
            a, b = min(row), max(row); p = (x - a) / max(1, b - a)
            c = "5" if p < 0.3 else ("4" if p < 0.65 else ("3" if p < 0.9 else "2"))
            if reg(x, y - 1) in "CI": c = "2"
        elif r == "T": c = "3" if reg(x, y - 1) not in "TB" else "2"
        elif r == "B": c = "y"
        elif r == "F":
            top = min(col)
            d = y - top
            c = "6" if d == 0 else ("5" if d <= 1 else "4")
            if reg(x, y + 1) in "SH" or reg(x, y + 2) in "SH": c = "3"
            if x == min(row): c = "5"
        elif r in "SH":
            top = min(yy for yy in range(n) if reg(x, yy) == r)
            c = "e" if y == top else ("q" if reg(x, y + 1) == "." else "w")
        g[y][x] = c
open(sys.argv[2], "w").write("\n".join("".join(r) for r in g) + "\n")
print("\n".join("".join(r) for r in g))
