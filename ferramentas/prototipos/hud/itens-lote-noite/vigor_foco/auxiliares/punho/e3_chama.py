# etapa 3: o fogo atrás do punho, secundário e assimétrico (uma língua alta por trás, à direita; uma menor à
# esquerda), sem nada sobre o centro dos nós; laranja do vigor, mais quente junto da mão; o contorno da chama por fora
import math
from PIL import Image
ocupado = set()              # o punho (com o contorno dele), das listas da etapa 2
for n in ("pulso", "dedos", "polegar", "dobras", "contorno"):
    txt = open(n + ".lua").read().split('"')[1]
    ocupado |= {(int(p.split(",")[0]), int(p.split(",")[1])) for p in txt.split(";")}
CORES = {"2": "9A2C0A", "3": "D24A12", "4": "F57A20", "5": "FFA838", "6": "FFD266"}
def chama(px, py):        # uma labareda só, atrás do lado direito do punho e mais alta que ele, a ponta curvando
    if py > 15.5: return False
    if math.hypot((px - 13.4) / 5.0, (py - 10.6) / 5.0) <= 1: return True
    if 0 <= py < 10.6:
        t = py / 10.6
        if abs(px - (13.2 - 2.4 * (1 - t) ** 2)) <= 5.0 * t ** 1.0: return True       # o corpo subindo até a ponta
    return False
g = {}
for y in range(20):
    for x in range(20):
        if (x, y) in ocupado or not chama(x + 0.5, y + 0.5): continue
        d = min(abs(x - a) + abs(y - b) for (a, b) in ocupado)       # a distância até o punho (o contorno dele)
        c = "6" if d <= 1 else "5" if d <= 2 else "4" if d <= 4 else "3"
        if y <= 1: c = "3"
        if y >= 13 and c in "345": c = "3" if y < 15 else "2"
        g[(x, y)] = c
forma = set(g)
cont = {(x, y) for y in range(20) for x in range(20) if (x, y) not in forma and (x, y) not in ocupado
        and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
open("chama.lua", "w").write('return "' + ";".join(f"{x},{y},{CORES[c]}" for (x, y), c in sorted(g.items())) + '"\n')
open("contorno_chama.lua", "w").write('return "' + ";".join(f"{x},{y},08080A" for (x, y) in sorted(cont)) + '"\n')
print(len(g), len(cont))
print("".join("\n" + "".join(g.get((x, y), "#" if (x, y) in ocupado else ("O" if (x, y) in cont else ".")) for x in range(20)) for y in range(20)))
