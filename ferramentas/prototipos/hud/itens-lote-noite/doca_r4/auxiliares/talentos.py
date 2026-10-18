# os Talentos (36): uma árvore de latão que se ramifica. O tronco grosso embaixo, os galhos curvos (como um galho de
# verdade), a luz de cima e da esquerda na beira de cada galho; os nós são medalhões: os conquistados (a raiz, o do
# alto e o da direita) com uma gema verde-água acesa, o não escolhido (à esquerda) com o encaixe vazio.
import math, sys, json
from ver import contorno, imagem
n = int(sys.argv[1]); k = n / 36
RAIZ, ESQ, DIR, TOPO = (18, 30.4), (8.2, 14.4), (27.8, 10.2), (17.6, 5.6)
G_ESQ, G_DIR = (17.8, 23.2), (17.6, 16.6)     # os galhos saem do tronco em alturas diferentes
def bezier(a, c, b, m=24):
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1])
            for t in (i / m for i in range(m + 1))]
# (pontos da curva, espessura no começo, no fim): o tronco sobe com uma leve curva; os galhos, curvos para cima
GALHOS = [(bezier(RAIZ, (19.4, 17.0), TOPO), 2.0, 1.4), (bezier(G_ESQ, (11.6, 22.4), ESQ), 1.55, 1.25),
          (bezier(G_DIR, (24.6, 16.4), DIR), 1.55, 1.25)]
NOS = [(RAIZ, True, 3.3), (ESQ, False, 3.6), (DIR, True, 3.6), (TOPO, True, 3.6)]
LUZ = (-0.72, -0.69)
def perto(px, py, pts):
    melhor = None
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        vx, vy = bx - ax, by - ay; t = max(0, min(1, ((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy or 1)))
        qx, qy = ax + t * vx, ay + t * vy; d = math.hypot(px - qx, py - qy)
        if melhor is None or d < melhor[0]: melhor = (d, px - qx, py - qy, (i + t) / (len(pts) - 1))
    return melhor
g = {}; cam = {}
for y in range(n):
    for x in range(n):
        px, py = (x + 0.5) / k, (y + 0.5) / k
        for pts, e0, e1 in GALHOS:
            d, ox, oy, t = perto(px, py, pts)
            esp = e0 + (e1 - e0) * t
            if d <= esp:
                lado = (ox * LUZ[0] + oy * LUZ[1]) / esp       # 1 na beira virada para a luz, -1 na oposta
                g[(x, y)] = "F" if lado > 0.35 else "D" if lado > -0.35 else "B"; cam[(x, y)] = "galhos"
        for (cx, cy), aceso, R in NOS:
            dx, dy = px - cx, py - cy; r = math.hypot(dx, dy)
            if r <= R:
                lado = (dx * LUZ[0] + dy * LUZ[1]) / R
                if r > R - 1.15:   # o aro do medalhão
                    c = "G" if lado > 0.45 else "E" if lado > -0.1 else "C" if lado > -0.6 else "B"
                elif aceso:        # a gema acesa: o brilho em cima à esquerda, o fundo escuro do outro lado
                    c = "M" if (lado > 0.25 and r < 1.6) else "L" if lado > -0.2 else "K" if lado > -0.6 else "J"
                else:              # o encaixe vazio
                    c = "I" if lado > -0.3 else "A"
                g[(x, y)] = c; cam[(x, y)] = "nos"
h = contorno(g, n)
for p, v in h.items():
    if v == "O": cam[p] = "contorno"
imagem(h, n, f"t{n}.png")
json.dump({f"{x},{y}": c for (x, y), c in cam.items()}, open(f"t{n}.cam.json", "w"))
