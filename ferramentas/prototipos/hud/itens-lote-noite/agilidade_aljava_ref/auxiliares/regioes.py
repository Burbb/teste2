# as regiões da bota (polígonos à mão, em unidades do 24) rasterizadas numa grade: auxiliar do rascunho
from PIL import Image, ImageDraw
def regioes(n, R):
    k = n / 24; SS = 8; can = {}
    for L, pts in R:
        im = Image.new("L", (n * SS, n * SS)); ImageDraw.Draw(im).polygon([(x * k * SS, y * k * SS) for x, y in pts], fill=255)
        im = im.resize((n, n), Image.BOX)
        for y in range(n):
            for x in range(n):
                if im.getpixel((x, y)) >= 128: can[(x, y)] = L
    return can
def mostrar(g):
    n = len(g)
    print("    " + "".join(str(x // 10) for x in range(n))); print("    " + "".join(str(x % 10) for x in range(n)))
    for y in range(n): print(f"{y:3d} " + "".join(g[y]))
