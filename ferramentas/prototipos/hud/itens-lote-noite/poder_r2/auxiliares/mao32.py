# a chama 32: a silhoueta à mão (linha: trechos x0-x1) e os tons pela regra do 24 (miolo creme embaixo, a luz subindo
# pelo eixo da língua principal, violetas escurecendo para fora, a beira escura); depois os retoques (AJUSTES)
import math
n = 32
S = {1: [(18, 18)], 2: [(17, 18)], 3: [(16, 18)], 4: [(15, 18)], 5: [(14, 18)], 6: [(13, 18)], 7: [(13, 18)],
     8: [(12, 18), (24, 24)], 9: [(12, 19), (23, 24)], 10: [(11, 19), (22, 24)], 11: [(11, 20), (21, 24)],
     12: [(7, 7), (11, 23)], 13: [(7, 8), (10, 24)], 14: [(7, 8), (10, 24)], 15: [(6, 25)],
     16: [(5, 26)], 17: [(5, 26)], 18: [(5, 26)], 19: [(5, 26)], 20: [(5, 26)], 21: [(5, 26)], 22: [(6, 25)],
     23: [(6, 25)], 24: [(7, 24)], 25: [(8, 23)], 26: [(10, 21)]}
forma = {(x, y) for y, ts in S.items() for a, b in ts for x in range(a, b + 1)}
cx, cy = 15.4, 19.2
def eixo(y):   # o centro da língua principal em cada linha (curva para a direita na ponta)
    return 15.6 + (19.6 - y) * 0.08 + max(0, 9 - y) * 0.28
g = [["."] * n for _ in range(n)]
for (x, y) in forma:
    px, py = x + 0.5, y + 0.5
    dy = (py - cy) / (6.4 if py < cy else 4.6)
    r = math.hypot((px - cx) / 5.2, dy)
    if py < 15:
        r = min(r, 0.8 + abs(px - eixo(py)) / 1.7 + (15 - py) * 0.085)
    t = 8 if r < 0.6 else 7 if r < 0.92 else 6 if r < 1.25 else 5 if r < 1.6 else 4 if r < 2.1 else 3
    viz = sum((x + dx, y + dy_) in forma for dx, dy_ in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    if viz < 4:
        t = min(t, 1 if py > 25 else 2 if py > 20 else 3)
    elif any((x + dx, y + dy_) not in forma for dx in (-2, -1, 0, 1, 2) for dy_ in (-2, -1, 0, 1, 2) if abs(dx) + abs(dy_) == 2):
        t = min(t, 2 if py > 23 else 4)
    if px > cx + 5 and 2 < t <= 5: t -= 1          # o lado de trás, um tom abaixo
    g[y][x] = str(t)
AJUSTES = {(7, 6): "6",      # a faísca solta, à esquerda da língua principal
           # a língua da direita acesa por dentro, como no 24 (a regra a deixava só na beira escura)
           (24, 8): "3", (23, 9): "3", (24, 9): "4", (23, 10): "4", (24, 10): "5", (22, 11): "4", (23, 11): "5",
           (24, 11): "4", (21, 12): "4", (22, 12): "4"}
for (x, y), c in AJUSTES.items(): g[y][x] = c
open("t32.txt", "w").write("\n".join("".join(r) for r in g) + "\n")
print("    " + "".join(str(x % 10) for x in range(n)))
for y in range(n): print(f"{y:3d} " + "".join(g[y]))
