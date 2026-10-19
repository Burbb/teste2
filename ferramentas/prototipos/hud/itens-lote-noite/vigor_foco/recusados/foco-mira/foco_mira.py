# o Foco (20): a mira da concentração e da precisão; o anel com a luz de cima e da esquerda e a volta de baixo e da
# direita na sombra, as quatro marcas que cruzam o anel e apontam para o centro, e o ponto aceso no meio, separado
# das marcas por um vão; o contorno comum. Verde, as cores da barra de foco (#b8f0a0, #62b86e, #1f4a25).
import math
from PIL import Image
RAMPA = {"1": "0E2A14", "2": "1F4A25", "3": "2F7A3A", "4": "4FA45C", "5": "7CCB78", "6": "B8F0A0", "7": "EEFFE0", "O": "08080A"}
C = 9.5
g, cam = {}, {}
for y in range(20):
    for x in range(20):
        px, py = x + 0.5 - C - 0.5, y + 0.5 - C - 0.5      # o centro entre os pixels 9 e 10
        px, py = x - C, y - C
        r = math.hypot(px, py)
        luz = -(px + py) / max(r, 0.01)                  # 1 virado para cima e para a esquerda, -1 para baixo e a direita
        if 4.6 <= r <= 6.9:                              # o anel, 2 px
            c = "6" if luz > 0.55 else "5" if luz > -0.1 else "4" if luz > -0.6 else "3"
            if r > 6.2 and luz < -0.1: c = "3" if c == "4" else "2"   # a beira de fora no lado da sombra
            g[(x, y)] = c; cam[(x, y)] = "anel"
        marca = (abs(px) < 1 and 2.5 < abs(py) < 9.0) or (abs(py) < 1 and 2.5 < abs(px) < 9.0)
        if marca:
            lado = py if abs(py) > abs(px) else px
            na_luz = (lado < 0)                           # as marcas de cima e da esquerda pegam a luz
            esq = (px < 0) if abs(py) > abs(px) else (py < 0)
            c = ("6" if esq else "5") if na_luz else ("5" if esq else "4")
            if 4.6 <= r <= 6.9: c = "7" if na_luz and esq else "6"   # onde a marca cruza o anel, mais acesa
            g[(x, y)] = c; cam[(x, y)] = "marcas"
        if abs(px) < 1 and abs(py) < 1:
            g[(x, y)] = "7" if (px < 0 and py < 0) else "6"; cam[(x, y)] = "centro"
forma = set(g)
for y in range(20):
    for x in range(20):
        if (x, y) not in g and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            g[(x, y)] = "O"; cam[(x, y)] = "contorno"
im = Image.new("RGBA", (20, 20))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(RAMPA[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save("foco20.png")
for camada in ("anel", "marcas", "centro", "contorno"):
    txt = ";".join(f"{x},{y},{RAMPA[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == camada)
    open(f"foco_{camada}.lua", "w").write(f'return "{txt}"\n')
print("".join("\n" + "".join(g.get((x, y), ".") for x in range(20)) for y in range(20)))
