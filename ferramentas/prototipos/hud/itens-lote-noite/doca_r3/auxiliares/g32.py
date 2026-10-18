# o Grimório 36 à mão: o livro fechado em pé, um pouco virado (a lombada à esquerda, o bloco de páginas à direita)
from ver import salvar
from rotulos import Grade
g = Grade()
X0, X1, Y0, Y1 = 9, 23, 3, 27          # a capa da frente
g.atual = "contracapa"
# a contracapa: uma fatia à direita e embaixo (a espessura)
for y in range(Y0 + 2, Y1 + 2): g[(X1 + 4, y)] = "2"
for x in range(X0 + 1, X1 + 5): g[(x, Y1 + 1)] = "2"
g.atual = "paginas"
# o bloco de páginas (a borda das folhas), entre as capas: creme com as linhas das folhas
for y in range(Y0 + 1, Y1 + 1):
    for x in range(X1 + 1, X1 + 4):
        g[(x, y)] = "q" if (y % 2 == 0) else "p"
        if x == X1 + 3: g[(x, y)] = "r" if y % 2 else "p"
    if y == Y0 + 1: g[(X1 + 1, y)] = "s"; g[(X1 + 2, y)] = "s"
g.atual = "lombada"
# a lombada redonda à esquerda, com as nervuras
for y in range(Y0, Y1 + 1):
    for x, c in ((X0 - 4, "3"), (X0 - 3, "5"), (X0 - 2, "6"), (X0 - 1, "4")):
        g[(x, y)] = c
for yb in (Y0 + 4, Y0 + 11, Y1 - 4):
    for x, c in ((X0 - 4, "5"), (X0 - 3, "7"), (X0 - 2, "7"), (X0 - 1, "6")): g[(x, yb)] = c
    for x, c in ((X0 - 4, "1"), (X0 - 3, "2"), (X0 - 2, "3"), (X0 - 1, "2")): g[(x, yb + 1)] = c
g.atual = "capa"
# a capa: o couro aceso à esquerda e em cima, escurecendo para a direita e para baixo; a moldura em relevo
for y in range(Y0, Y1 + 1):
    for x in range(X0, X1 + 1):
        u, v = (x - X0) / (X1 - X0), (y - Y0) / (Y1 - Y0)
        c = 6 if u + 0.6 * v < 0.45 else 5 if u + 0.6 * v < 0.95 else 4 if u + 0.6 * v < 1.35 else 3
        g[(x, y)] = str(c)
        if x in (X0 + 2, X1 - 2) and Y0 + 2 <= y <= Y1 - 2 or y in (Y0 + 2, Y1 - 2) and X0 + 2 <= x <= X1 - 2:
            g[(x, y)] = "7" if (x == X0 + 2 or y == Y0 + 2) else "2"      # a moldura: acesa em cima à esquerda
for x in range(X0, X1 + 1): g[(x, Y0)] = "7" if x < X1 - 4 else "6"     # a beira de cima da capa, acesa
for y in range(Y0, Y1 + 1): g[(X1, y)] = "3"                            # a beira da direita, na sombra
for y in range(Y0, Y1 + 1): g[(X0, y)] = "2"                            # o sulco da dobradiça, entre a lombada e a capa
g.atual = "cantoneiras"
# as cantoneiras de latão
for (cx, cy, sx, sy) in ((X0, Y0, 1, 1), (X1, Y0, -1, 1), (X0, Y1, 1, -1), (X1, Y1, -1, -1)):
    for i in range(3):
        for j in range(3 - i):
            x, y = cx + sx * i, cy + sy * j
            g[(x, y)] = "f" if (i == 0 and j == 0) else ("e" if sx > 0 and sy > 0 else "d" if sy > 0 or sx > 0 else "c")
g.atual = "fecho"
# o fecho: a tira de couro vindo de trás, por cima das folhas, e a fivela de latão na capa
for y in range(14, 19):
    for x in range(X1 - 2, X1 + 5):
        g[(x, y)] = "l" if y == 14 else "k" if y == 18 else "m" if x > X1 else "l"
for (x, y, c) in ((X1 - 3, 14, "f"), (X1 - 2, 14, "f"), (X1 - 3, 15, "e"), (X1 - 3, 16, "e"), (X1 - 3, 17, "d"),
                  (X1 - 3, 18, "c"), (X1 - 2, 18, "c"), (X1 - 2, 16, "g")):
    g[(x, y)] = c
g.atual = "gema"
# a gema mágica no centro, num engaste de latão em losango, com o brilho violeta
cx, cy = 15, 15
for dy in range(-5, 6):
    w = 5 - abs(dy)
    for dx in range(-w, w + 1):
        x, y = cx + dx, cy + dy
        if abs(dx) + abs(dy) >= 4: g[(x, y)] = "f" if (dx <= 0 and dy <= 0) else "d" if (dx > 0 and dy > 0) else "e"
        elif abs(dx) + abs(dy) == 3: g[(x, y)] = "b"
        else:
            g[(x, y)] = "Z" if (dx, dy) in ((-1, -2), (-1, -1), (0, -2)) else "Y" if dx + dy < -1 else "X" if dx + dy < 1 else "W" if dx + dy < 3 else "V"
salvar(g, 32, "g32.png")
import json; json.dump({f"{x},{y}": c for (x, y), c in g.cam.items()}, open("g32.cam.json", "w"))
