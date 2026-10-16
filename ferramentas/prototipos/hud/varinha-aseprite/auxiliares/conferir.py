"""Confere o PNG exportado contra a leitura do .aseprite reaberto (get_region): mesma cor em todo pixel opaco, e o
que a leitura dá como vazio (000000) tem alfa 0 no PNG; conta as cores e os alfas."""
import json, sys
from PIL import Image
png, leitura = sys.argv[1], sys.argv[2]
im = Image.open(png); print(png.split("/")[-1], im.size, im.mode)
im = im.convert("RGBA"); W, H = im.size
rows = json.load(open(leitura))["rows"].split("|")
dif = 0; alfas = set(); cores = set()
for y, l in enumerate(rows):
    x = 0
    for run in l.split(";"):
        n, c = run.split(","); n = int(n)
        for i in range(n):
            r, g, b, a = im.getpixel((x + i, y)); alfas.add(a)
            if c == "000000":
                dif += a != 0
            else:
                cores.add(c); dif += (a != 255) or ("%02X%02X%02X" % (r, g, b) != c)
        x += n
cheios = sum(1 for p in im.getdata() if p[3])
print(f"  diferenças: {dif}; alfas: {sorted(alfas)}; opacos: {cheios} de {W*H}; cores: {len(cores)} (com o contorno)")
