# auxiliar: a captura do editor em tamanho real e ampliada 10x sobre o carvão da HUD, ao lado do anterior
import sys
from PIL import Image
N = int(__import__("os").environ.get("N", "24"))
ims = [Image.open(a).convert("RGBA") for a in sys.argv[2:]]
W = 30 + sum(20 + N * 10 + 40 for _ in ims); o = Image.new("RGB", (W, N * 10 + 30), (27, 27, 30)); x = 10
for im in ims:
    o.paste(im, (x, 10), im); x += N + 10
    o.paste(im.resize((N * 10, N * 10), Image.NEAREST), (x, 15), im.resize((N * 10, N * 10), Image.NEAREST)); x += N * 10 + 30
o.save(sys.argv[1])
