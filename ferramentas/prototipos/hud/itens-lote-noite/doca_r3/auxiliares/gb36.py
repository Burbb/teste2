# o Grimório, rodada 2 (36): o livro fechado como um objeto só, visto de cima e da esquerda. A profundidade vai para
# cima e para a esquerda (DX, DY): à vista ficam a capa da frente, a lombada (a face da esquerda) e, em cima, a borda
# das folhas entre a beira da capa da frente e a da contracapa. Primeiro os volumes; as ferragens depois.
import sys
from rotulos import Grade
from ver import salvar
g = Grade()
X0, X1, Y0, Y1 = 12, 28, 9, 32         # a capa da frente
DX, DY = -6, -5                        # a profundidade do livro (a espessura), para cima e para a esquerda
ETAPA = sys.argv[1] if len(sys.argv) > 1 else "tudo"
def em_quad(px, py, p0, p1, p2, p3):   # dentro do quadrilátero convexo p0-p1-p2-p3
    pts = [p0, p1, p2, p3]; s = []
    for i in range(4):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % 4]
        s.append((bx - ax) * (py - ay) - (by - ay) * (px - ax))
    return all(v >= -1e-9 for v in s) or all(v <= 1e-9 for v in s)
# a lombada: a face da esquerda, entre a beira esquerda da capa da frente e a da contracapa
g.atual = "lombada"
for y in range(0, 36):
    for x in range(0, 36):
        px, py = x + 0.5, y + 0.5
        if em_quad(px, py, (X0, Y0), (X0, Y1 + 1), (X0 + DX, Y1 + 1 + DY), (X0 + DX, Y0 + DY)):
            t = (X0 - px) / -DX                       # 0 junto da capa, 1 junto da contracapa
            g[(x, y)] = "4" if t < 0.2 else "6" if t < 0.55 else "5" if t < 0.85 else "3"   # o dorso redondo
# a borda de cima: as folhas entre as duas capas (as linhas das folhas correm junto da beira da capa)
for y in range(0, 36):
    for x in range(0, 36):
        px, py = x + 0.5, y + 0.5
        if em_quad(px, py, (X0, Y0), (X1 + 1, Y0), (X1 + 1 + DX, Y0 + DY), (X0 + DX, Y0 + DY)):
            t = (Y0 - py) / -DY                       # 0 junto da capa da frente, 1 junto da contracapa
            if t < 0.2: g.atual = "capa"; g[(x, y)] = "7"                     # a beira da capa da frente, acesa
            elif t > 0.82: g.atual = "contracapa"; g[(x, y)] = "4"            # a beira da contracapa
            else: g.atual = "paginas"; g[(x, y)] = "s" if y % 2 == 0 else "q"
# a capa da frente: poucos planos de luz (o alto e o lado da lombada mais claros, a beira oposta na sombra)
g.atual = "capa"
for y in range(Y0, Y1 + 1):
    for x in range(X0, X1 + 1):
        u, v = (x - X0) / (X1 - X0), (y - Y0) / (Y1 - Y0)
        k = u * 0.9 + v * 0.6
        g[(x, y)] = "6" if k < 0.35 else "5" if k < 0.95 else "4"
        if x == X1 or y == Y1: g[(x, y)] = "3"                               # a beira oposta, na sombra
        if x == X0: g[(x, y)] = "7" if y < Y1 - 6 else "6"                  # a quina da lombada, acesa
# as nervuras da lombada: as faixas em relevo, inclinadas como a profundidade (acesas em cima, sombra embaixo)
g.atual = "lombada"
for yb in (Y0 + 4, Y0 + 12, Y1 - 5):
    for x in range(X0 + DX, X0):
        y = yb + round((x - X0) * DY / DX)
        if (x, y) in g and g.cam[(x, y)] == "lombada":
            g[(x, y)] = "7"
            if (x, y + 1) in g and g.cam[(x, y + 1)] == "lombada": g[(x, y + 1)] = "2"
if ETAPA == "volumes":
    salvar(g, 36, "gb36v.png"); raise SystemExit
# a moldura em relevo (1 px aceso em cima e à esquerda, 1 px escuro embaixo e à direita), dentro da capa
for x in range(X0 + 2, X1 - 1):
    g[(x, Y0 + 2)] = "7"; g[(x, Y1 - 2)] = "2"
for y in range(Y0 + 2, Y1 - 1):
    g[(X0 + 2, y)] = "7"; g[(X1 - 2, y)] = "2"
# as cantoneiras de latão nos quatro cantos da capa (3 px), acesas do lado da luz
g.atual = "cantoneiras"
for (cx, cy, sx, sy) in ((X0, Y0, 1, 1), (X1, Y0, -1, 1), (X0, Y1, 1, -1), (X1, Y1, -1, -1)):
    for i in range(3):
        for j in range(3 - i):
            g[(cx + sx * i, cy + sy * j)] = "f" if (i == 0 and j == 0) else ("e" if (sx > 0 or sy > 0) and not (sx < 0 and sy < 0) else "c")
# o fecho: a tira de couro vem de trás, dá a volta na beira da direita (o pedaço que sobra para fora, na sombra) e
# se deita sobre a capa até a placa de latão com o pino
g.atual = "fecho"
FY0, FY1 = 18, 22
for y in range(FY0, FY1 + 1):
    g[(X1 + 1, y)] = "k"                                   # a volta da tira por fora da beira
    for x in range(X1 - 2, X1 + 1):
        g[(x, y)] = "m" if y == FY0 else "k" if y == FY1 else "l"
for y in range(FY0, FY1 + 1):                              # a placa de latão na ponta da tira
    for x in (X1 - 4, X1 - 3):
        g[(x, y)] = "f" if (y == FY0 or x == X1 - 4) and y < FY1 else "d" if y < FY1 else "c"
g[(X1 - 3, FY0 + 2)] = "g"                                 # o pino
# o emblema: menor, centrado no plano útil da capa (entre a lombada e o fecho), a gema violeta no engaste em losango
g.atual = "gema"
cx, cy, R = 19, 20, 3
for dy in range(-R, R + 1):
    w = R - abs(dy)
    for dx in range(-w, w + 1):
        x, y = cx + dx, cy + dy
        d = abs(dx) + abs(dy)
        if d == R: g[(x, y)] = "f" if (dx <= 0 and dy <= 0) else "c" if (dx > 0 and dy > 0) else "e"
        elif d == R - 1: g[(x, y)] = "b"
        else: g[(x, y)] = "Z" if (dx, dy) in ((-1, -1), (0, -2)) else "Y" if dx + dy < 0 else "X" if dx + dy < 2 else "W"
salvar(g, 36, "gb36.png")
import json; json.dump({f"{x},{y}": c for (x, y), c in g.cam.items()}, open("gb36.cam.json", "w"))
