# a Vida (20): o coração; os lobos e a ponta por linha (à mão), a luz de cima e da esquerda em poucos planos, o brilho
# no lobo da esquerda; o contorno comum. Grava as listas por camada (coracao, brilho, contorno) e uma prévia.
import json
from PIL import Image
RAMPA = {"1": "460810", "2": "7C1018", "3": "B41A24", "4": "E0262E", "5": "F24A44", "6": "FFB8A0", "O": "08080A"}
LINHAS = {3: [(4, 7), (12, 15)], 4: [(3, 8), (11, 16)], 5: [(2, 17)], 6: [(2, 17)], 7: [(2, 17)], 8: [(2, 17)],
          9: [(3, 16)], 10: [(4, 15)], 11: [(5, 14)], 12: [(6, 13)], 13: [(7, 12)], 14: [(8, 11)], 15: [(9, 10)]}
forma = {(x, y) for y, ts in LINHAS.items() for a, b in ts for x in range(a, b + 1)}
g, cam = {}, {}
for (x, y) in forma:
    t = (x - 9.5) * 0.55 + (y - 7.5) * 0.85         # a luz de cima e da esquerda: mais escuro para baixo e à direita
    c = "5" if t < -3.2 else "4" if t < 1.5 else "3" if t < 4.6 else "2"
    if (x + 1, y) not in forma and x > 9 or (x, y + 1) not in forma and y > 9: c = "2" if c in "345" else "1"   # a volta
    g[(x, y)] = c; cam[(x, y)] = "coracao"
for (x, y) in ((4, 4), (5, 4), (4, 5), (6, 3)):     # o brilho no lobo da esquerda
    g[(x, y)] = "6"; cam[(x, y)] = "brilho"
g[(13, 4)] = "5"; cam[(13, 4)] = "brilho"           # um reflexo pequeno no lobo da direita
for y in range(20):
    for x in range(20):
        if (x, y) not in g and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            g[(x, y)] = "O"; cam[(x, y)] = "contorno"
im = Image.new("RGBA", (20, 20))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(RAMPA[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save("vida20.png")
for camada in ("coracao", "brilho", "contorno"):
    txt = ";".join(f"{x},{y},{RAMPA[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == camada)
    open(f"vida_{camada}.lua", "w").write(f'return "{txt}"\n')
print("".join("\n" + "".join(g.get((x, y), ".") for x in range(20)) for y in range(20)))
