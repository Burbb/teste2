# o mapa em sanfona (36): três painéis inclinados, alternando luz e sombra; a espessura do papel embaixo; o percurso
# tracejado até o X
from ver import salvar
n = 36
# os vincos (x) e a altura das bordas em cada vinco: a de cima e a de baixo sobem e descem juntas (o zigue-zague)
VX = [3, 13, 23, 33]
TOPO = [9, 5, 9, 5]
ALT = 21
g = {}
def borda(x):
    for i in range(3):
        if VX[i] <= x <= VX[i + 1]:
            t = (x - VX[i]) / (VX[i + 1] - VX[i])
            return i, TOPO[i] + (TOPO[i + 1] - TOPO[i]) * t
    return None, None
for x in range(n):
    i, top = borda(x + 0.5)
    if i is None: continue
    for y in range(n):
        py = y + 0.5
        if top <= py <= top + ALT:
            v = (py - top) / ALT
            if i % 2 == 0:   # o painel que sobe para a direita olha para a luz
                c = "F" if v < 0.25 else "E" if v < 0.8 else "D"
            else:            # o que desce para a direita fica na sombra
                c = "D" if v < 0.3 else "C" if v < 0.85 else "B"
            g[(x, y)] = c
        elif top + ALT < py <= top + ALT + 1.0:
            g[(x, y)] = "A" if i % 2 else "B"       # a espessura do papel, embaixo
# os vincos: a dobra de dentro escura, a de fora acesa
for y in range(n):
    for x in (13, 23):
        if (x, y) in g and g[(x, y)] not in "AB":
            g[(x, y)] = "C" if x == 13 else "F"
# o terreno, em manchas grandes e suaves (nada de símbolo miúdo): um bosque no painel da esquerda, um lago no do meio
for (x, y, c) in ((5, 12, "w"), (6, 12, "w"), (7, 12, "v"), (4, 13, "w"), (5, 13, "v"), (6, 13, "v"), (7, 13, "v"), (8, 13, "v"),
                  (5, 14, "v"), (6, 14, "v"), (7, 14, "v"), (16, 23, "m"), (17, 23, "m"), (18, 23, "l"), (15, 24, "m"),
                  (16, 24, "l"), (17, 24, "l"), (18, 24, "l"), (19, 24, "l"), (17, 25, "l"), (18, 25, "l")):
    g[(x, y)] = c
# o percurso tracejado (vermelho, 2 px: o traço e a sombra embaixo), subindo até o X do destino
TRACOS = [[(5, 24), (6, 24), (7, 23)], [(9, 22), (10, 22), (11, 21)], [(14, 20), (15, 20)], [(17, 19), (18, 18)],
          [(20, 17), (21, 16)], [(23, 15), (24, 14)]]
for tr in TRACOS:
    for (x, y) in tr:
        g[(x, y)] = "s"; g[(x, y + 1)] = "r"
# o X: duas pinceladas cruzadas, 5×5, a de cima acesa
for i in range(5):
    g[(26 + i, 8 + i)] = "s" if i != 2 else "t"
    g[(30 - i, 8 + i)] = "t" if i < 2 else "s"
for i in range(4):
    g[(27 + i, 8 + i)] = g.get((27 + i, 8 + i)) if (27 + i, 8 + i) in [(26 + j, 8 + j) for j in range(5)] else "r"
salvar(g, n, "mapa36.png")
