# o Foco (20): o alvo da concentração e da precisão; um disco de anéis concêntricos (claro, fundo, claro, fundo e o
# centro aceso) com a luz de cima e da esquerda, e quatro marcas curtas da mira saindo do disco nos quatro lados; o
# contorno comum. Verde, as cores da barra de foco (#b8f0a0, #62b86e, #1f4a25).
import math
from PIL import Image
RAMPA = {"1": "0E2A14", "2": "1F4A25", "3": "2F7A3A", "4": "4FA45C", "5": "7CCB78", "6": "B8F0A0", "7": "EEFFE0", "O": "08080A"}
C = 9.5
g, cam = {}, {}
for y in range(20):
    for x in range(20):
        px, py = x - C, y - C
        r = math.hypot(px, py)
        luz = -(px + py) / max(r, 0.01)                     # +1 para cima e a esquerda, -1 para baixo e a direita
        if r <= 6.9:
            if r > 5.2:   claro, faixa = True, "anel"           # o anel de fora
            elif r > 3.6: claro, faixa = False, "anel"          # o vão fundo
            elif r > 2.1: claro, faixa = True, "anel"           # o anel de dentro
            elif r > 1.2: claro, faixa = False, "anel"
            else:         claro, faixa = None, "centro"
            if claro is None: c = "7" if px < 0 and py < 0 else "6"
            elif claro: c = "6" if luz > 0.3 else "5" if luz > -0.5 else "4"
            else: c = "2"                                     # o vão, fundo e liso: separa os anéis
            if claro and r > 6.2 and luz < -0.35: c = "3"     # a beira de fora, do lado da sombra
            g[(x, y)] = c; cam[(x, y)] = faixa
        elif (abs(px) < 1 and abs(py) < 7.9) or (abs(py) < 1 and abs(px) < 7.9):   # as marcas da mira, fora do disco
            lado = py if abs(py) > abs(px) else px
            g[(x, y)] = "6" if lado < 0 else "4"; cam[(x, y)] = "marcas"
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
