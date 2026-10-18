# rascunho do corpo da aljava (auxiliar): o tubo inclinado, a base redonda, a boca elíptica, as cintas e a alça
# em coordenadas da grade (n = 32 ou 24); grava o mapa em texto para a edição à mão
import math, sys
from regioes import mostrar
n = int(sys.argv[1]); k = n / 32
B = (8.0 * k, 30.0 * k); M = (20.4 * k, 13.6 * k)
dx, dy = M[0] - B[0], M[1] - B[1]; L = math.hypot(dx, dy); d = (dx / L, dy / L); nn = (-d[1], d[0])
if nn[0] < 0: nn = (-nn[0], -nn[1])
SS = 6
def sw(x, y):
    vx, vy = x - B[0], y - B[1]
    return vx * d[0] + vy * d[1], vx * nn[0] + vy * nn[1]
g = [["."] * n for _ in range(n)]
hw0 = 3.9 * k
def regiao(x, y):
    s, w = sw(x, y)
    # a boca: elipse no fim do tubo
    ea, eb = 4.8 * k, 2.0 * k
    em = ((w + 0.0) / ea) ** 2 + ((s - L) / eb) ** 2
    ia, ib = 3.6 * k, 1.2 * k
    ei = ((w - 0.1 * k) / ia) ** 2 + ((s - L - 0.15 * k) / ib) ** 2
    if ei <= 1: return "i", s, w
    if em <= 1: return "b", s, w
    hw = hw0 + 0.025 * s
    cap = 3.0 * k
    if s < cap:
        if s < 0: return None, s, w
        hw = hw * math.sqrt(max(0.0, 1 - ((cap - s) / cap) ** 2))
    if 0 <= s <= L and abs(w) <= hw:
        for c0, c1 in ((L - 6.9 * k, L - 5.0 * k), (3.6 * k, 5.5 * k)):
            if c0 <= s <= c1: return "a", s, w
        return "k", s, w
    if 0 <= s <= L:
        for c0, c1 in ((L - 6.9 * k, L - 5.0 * k), (3.6 * k, 5.5 * k)):
            if c0 <= s <= c1 and abs(w) <= hw + 0.5 * k: return "a", s, w
    return None, s, w
for y in range(n):
    for x in range(n):
        votos = {}
        for i in range(SS):
            for j in range(SS):
                r, s, w = regiao(x + (i + 0.5) / SS, y + (j + 0.5) / SS)
                votos[r] = votos.get(r, 0) + 1
        r = max(votos, key=votos.get)
        if r is None: continue
        _, s, w = regiao(x + 0.5, y + 0.5)
        if r == "k":
            c = "5" if w < -2.6 * k else ("6" if w < -1.0 * k else ("4" if w < 1.0 * k else ("3" if w < 2.6 * k else "2")))
        elif r == "a":
            c = "A" if w > 2 * k else "B"
        elif r == "b":
            c = "6" if s < L else "4"
            if w > 2.6 * k: c = "3" if s >= L else "4"
        else:
            c = "i"
        g[y][x] = c
mostrar(g)
open(f"c{n}.txt", "w").write("\n".join("".join(r) for r in g) + "\n")
