# a Mana (20): a gota de energia líquida, azul (a cor da barra); a ponta em cima curvando um pouco, o fundo redondo, o
# miolo aceso (a energia), o reflexo em crescente do lado da luz, a beira escura do outro; o contorno comum.
import math, json
from PIL import Image
RAMPA = {"1": "10183E", "2": "1C2A6B", "3": "2E4AB0", "4": "4D74E0", "5": "7FA4F4", "6": "A8C4FF", "7": "E6F0FF", "O": "08080A"}
CX, CY, R = 9.5, 12.3, 6.3          # o fundo redondo
TOPO = 1.2                          # a ponta
def dentro(px, py):
    if math.hypot(px - CX, py - CY) <= R: return True
    if TOPO <= py < CY:
        t = (CY - py) / (CY - TOPO)                     # 0 no meio do círculo, 1 na ponta
        meia = R * (1 - t) ** 1.25 * (1 + 0.25 * t)
        centro = CX + 0.9 * t ** 2                      # a ponta curva um pouco para a direita
        return abs(px - centro) <= meia
    return False
forma = {(x, y) for y in range(20) for x in range(20) if dentro(x + 0.5, y + 0.5)}
g, cam = {}, {}
for (x, y) in forma:
    px, py = x + 0.5, y + 0.5
    t = (px - CX) * 0.6 + (py - CY) * 0.75
    r = math.hypot(px - (CX + 0.4), py - (CY + 0.6))
    c = "6" if r < 1.1 else "5" if r < 2.3 else ("4" if t < 1.0 else "3")    # o miolo aceso, em volta mais fundo
    if t > 3.4: c = "2"                                                      # a beira do lado de trás
    if (x + 1, y) not in forma and x > 9 or (x, y + 1) not in forma: c = "2" if c != "1" else c
    if (x - 1, y) not in forma and y < 9: c = "3"
    g[(x, y)] = c; cam[(x, y)] = "gota"
for (x, y) in ((5, 9), (4, 10), (4, 11), (4, 12), (5, 13)):                  # o reflexo em crescente, do lado da luz
    if (x, y) in g: g[(x, y)] = "7" if y in (10, 11) else "6"; cam[(x, y)] = "brilho"
for (x, y) in ((9, 4), (9, 5)):                                               # o brilho na ponta
    if (x, y) in g: g[(x, y)] = "5"; cam[(x, y)] = "brilho"
for y in range(20):
    for x in range(20):
        if (x, y) not in g and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            g[(x, y)] = "O"; cam[(x, y)] = "contorno"
im = Image.new("RGBA", (20, 20))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(RAMPA[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save("mana20.png")
for camada in ("gota", "brilho", "contorno"):
    txt = ";".join(f"{x},{y},{RAMPA[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == camada)
    open(f"mana_{camada}.lua", "w").write(f'return "{txt}"\n')
print("".join("\n" + "".join(g.get((x, y), ".") for x in range(20)) for y in range(20)))
