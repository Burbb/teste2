# o Vigor (20): o raio de energia física, grosso e com volume; a face com a luz de cima e da esquerda em faixas, o
# bisel escuro nas beiras de baixo e da direita, o fio aceso na beira de cima da parte de cima; o contorno comum.
# Dourado e laranja, as cores da barra de vigor (#ffe08a, #e0a22d, #8a5a0c).
from PIL import Image
RAMPA = {"1": "4A2606", "2": "8A5A0C", "3": "C2790F", "4": "E0A22D", "5": "FFC548", "6": "FFE08A", "7": "FFF8D8", "O": "08080A"}
POLI = [(11, 1), (16.2, 1), (12.4, 7.6), (16.8, 7.6), (5.6, 19.4), (9.4, 11), (4.4, 11)]
def dentro(px, py):
    c, n = False, len(POLI)
    for i in range(n):
        (x1, y1), (x2, y2) = POLI[i], POLI[(i + 1) % n]
        if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c
forma = {(x, y) for y in range(20) for x in range(20) if dentro(x + 0.5, y + 0.5)}
g, cam = {}, {}
for (x, y) in forma:
    t = (x - 9.5) * 0.45 + (y - 9.5) * 0.7
    c = "6" if t < -3.5 else "5" if t < 0.5 else "4" if t < 3.5 else "3"
    if (x + 1, y) not in forma or ((x, y + 1) not in forma and (x - 1, y + 1) not in forma):    # o bisel do lado da sombra
        c = "2" if c in "34" else "3"                                       # (a escada da diagonal fica na face)
        if (x - 2, y) not in forma: c = "3"           # no trecho estreito da cauda, o bisel no tom do meio, para não sumir
    g[(x, y)] = c; cam[(x, y)] = "raio"
for (x, y) in sorted(forma):                                   # o fio aceso: a beira de cima e da esquerda da parte de cima
    if y <= 9 and ((x - 1, y) not in forma or (x, y - 1) not in forma) and (x + 1, y) in forma and (x, y + 1) in forma:
        g[(x, y)] = "7" if y <= 4 else "6"; cam[(x, y)] = "brilho"
for y in range(20):
    for x in range(20):
        if (x, y) not in g and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            g[(x, y)] = "O"; cam[(x, y)] = "contorno"
im = Image.new("RGBA", (20, 20))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(RAMPA[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save("vigor20.png")
for camada in ("raio", "brilho", "contorno"):
    txt = ";".join(f"{x},{y},{RAMPA[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == camada)
    open(f"vigor_{camada}.lua", "w").write(f'return "{txt}"\n')
print("".join("\n" + "".join(g.get((x, y), ".") for x in range(20)) for y in range(20)))
