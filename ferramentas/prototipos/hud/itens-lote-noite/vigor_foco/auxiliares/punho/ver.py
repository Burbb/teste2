# auxiliar: a captura do editor em tamanho real e ampliada 10x sobre o carvão da HUD, ao lado do anterior
import sys
from PIL import Image
ims = [Image.open(a).convert("RGBA") for a in sys.argv[2:]]
W = 30 + sum(20 + 20 * 10 + 40 for _ in ims); o = Image.new("RGB", (W, 230), (27, 27, 30)); x = 10
for im in ims:
    o.paste(im, (x, 10), im); x += 30
    o.paste(im.resize((200, 200), Image.NEAREST), (x, 15), im.resize((200, 200), Image.NEAREST)); x += 230
o.save(sys.argv[1])
