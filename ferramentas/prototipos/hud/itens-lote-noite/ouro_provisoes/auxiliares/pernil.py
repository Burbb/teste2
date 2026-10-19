# as Provisões (24 e 32): o pernil curado amarrado, a comida de viagem; o mesmo modelo nos dois tamanhos. Ao longo de
# um eixo diagonal: o corpo de carne embaixo à esquerda (a casca curada, com a luz de cima e da esquerda), o osso
# subindo para a direita até a ponta dupla (no creme do osso do topo, o desenho de quando a comida acaba) e dois
# (rodada 2: sem os barbantes, a pedido do Jean). Uso: python pernil.py <24|32> [silhueta]. Grava as listas por camada e a prévia.
import sys, math
from PIL import Image
N = int(sys.argv[1]); ETAPA = sys.argv[2] if len(sys.argv) > 2 else "final"
R = {"c1": "4A1A0C", "c2": "7A2E16", "c3": "A84A24", "c4": "C86A34", "c5": "E2925A", "c6": "F4BC88",
     "o2": "A8865A", "o3": "D2B488", "o4": "F8E2B6", "o5": "FFF4DA",
     "b2": "8A6A3A", "b3": "C8B080", "b4": "EEDCB0", "O": "08080A"}
A = (0.19 * N, 0.81 * N); B = (0.88 * N, 0.12 * N)            # o eixo: da ponta da carne à ponta do osso
L = math.hypot(B[0] - A[0], B[1] - A[1]); ux, uy = (B[0] - A[0]) / L, (B[1] - A[1]) / L
vx, vy = -uy, ux                                               # o lado de cima e da esquerda do eixo é v < 0
def coord(px, py):
    dx, dy = px - A[0], py - A[1]
    return (dx * ux + dy * uy) / L, (dx * vx + dy * vy) / N     # u de 0 a 1 ao longo; v em frações do quadro
def carne(u):                                                  # a meia-largura do corpo de carne em u (0 fora)
    if u < -0.02 or u > 0.58: return 0
    if u < 0.22: return 0.19 * math.sqrt(max(0, 1 - ((u - 0.22) / 0.23) ** 2))    # a ponta redonda
    t = (u - 0.22) / 0.36
    return 0.19 * (1 - t) ** 0.9 + 0.05 * t                                        # afinando até o osso
OSSO_U0, OSSO_U1, OSSO_W = 0.50, 0.90, 0.042
g, cam = {}, {}
def pinta(x, y, c, k):
    g[(x, y)] = c; cam[(x, y)] = k
for y in range(N):
    for x in range(N):
        u, v = coord(x + 0.5, y + 0.5)
        w = carne(u)
        if w and abs(v) <= w:
            if ETAPA == "silhueta": pinta(x, y, "c4", "carne"); continue
            t = v / w                                          # -1 no lado da luz, +1 na sombra
            c = "c5" if t < -0.45 else "c4" if t < 0.2 else "c3" if t < 0.7 else "c2"
            if u < 0.06 and t > -0.2: c = "c2"                 # a ponta de baixo, virando para longe da luz
            pinta(x, y, c, "carne")
            continue
        if OSSO_U0 <= u <= OSSO_U1 and abs(v) <= OSSO_W:       # a haste do osso
            pinta(x, y, "o4" if v < 0 else "o3", "osso"); continue
        for sv in (-1, 1):                                     # a ponta dupla do osso
            cxu, cvy = 0.90, sv * 0.058
            if math.hypot((u - cxu) * L / N, v - cvy) <= 0.052:
                pinta(x, y, "o5" if (sv < 0 and v < cvy) else "o4" if sv < 0 or v < cvy else "o3", "osso")
if ETAPA != "silhueta":                                        # o brilho da casca, em cima da parte larga
    for (x, y), c in list(g.items()):
        u, v = coord(x + 0.5, y + 0.5)
        if cam[(x, y)] == "carne" and 0.06 < u < 0.26 and -0.85 < v / max(carne(u), 0.01) < -0.5:
            pinta(x, y, "c6", "carne")
forma = set(g)
for y in range(N):
    for x in range(N):
        if (x, y) not in g and any((x + a, y + b) in forma for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            pinta(x, y, "O", "contorno")
im = Image.new("RGBA", (N, N))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(R[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save(f"pernil{N}_{ETAPA}.png")
for k in set(cam.values()):
    open(f"pernil{N}_{k}.lua", "w").write('return "' + ";".join(f"{x},{y},{R[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == k) + '"\n')
leg = {"c1": "1", "c2": "2", "c3": "3", "c4": "4", "c5": "5", "c6": "6", "o2": "a", "o3": "b", "o4": "c", "o5": "d", "b2": "x", "b3": "y", "b4": "z", "O": "O"}
print(sorted(set(cam.values())))
print("".join("\n" + "".join(leg.get(g.get((x, y)), ".") for x in range(N)) for y in range(N)))
