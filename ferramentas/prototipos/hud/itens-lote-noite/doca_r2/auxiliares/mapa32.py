# o mapa em sanfona (36): três painéis inclinados, alternando luz e sombra; a espessura do papel embaixo; o percurso
# tracejado até o X
from ver import salvar
n = 32
# os vincos (x) e a altura das bordas em cada vinco: a de cima e a de baixo sobem e descem juntas (o zigue-zague)
VX = [3, 12, 21, 30]
TOPO = [8, 4, 8, 4]
ALT = 19
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
    for x in (12, 21):
        if (x, y) in g and g[(x, y)] not in "AB":
            g[(x, y)] = "C" if x == 12 else "F"
# o terreno, em manchas grandes e suaves (nada de símbolo miúdo): um bosque no painel da esquerda, um lago no do meio
for (x, y, c) in ((5, 11, "w"), (6, 11, "v"), (4, 12, "w"), (5, 12, "v"), (6, 12, "v"), (7, 12, "v"), (5, 13, "v"), (6, 13, "v"),
                  (14, 20, "m"), (15, 20, "m"), (16, 20, "l"), (13, 21, "m"), (14, 21, "l"), (15, 21, "l"), (16, 21, "l"), (15, 22, "l")):
    g[(x, y)] = c
# o percurso tracejado (vermelho, 2 px: o traço e a sombra embaixo), subindo até o X do destino
TRACOS = [[(5, 22), (6, 22)], [(8, 21), (9, 20)], [(11, 19), (12, 19)], [(14, 18), (15, 17)], [(17, 16), (18, 15)],
          [(20, 14), (21, 13)]]
for tr in TRACOS:
    for (x, y) in tr:
        g[(x, y)] = "s"; g[(x, y + 1)] = "r"
# o X: duas pinceladas cruzadas, 5×5, a de cima acesa
for i in range(5):
    g[(23 + i, 7 + i)] = "s" if i != 2 else "t"
    g[(27 - i, 7 + i)] = "t" if i < 2 else "s"
salvar(g, n, "mapa32.png")
