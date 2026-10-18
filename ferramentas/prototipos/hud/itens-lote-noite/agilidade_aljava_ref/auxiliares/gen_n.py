# os intermediários (40, 48) da aljava aprovada: o corpo do corpo.py na grade do tamanho e as partes à mão do 32
# (ed32.py) levadas para a grade por n/32, com as regras que o 32 seguiu; grava c<n>m.txt para o retoque
import subprocess, sys
from regioes import mostrar
n = int(sys.argv[1]); k = n / 32
subprocess.run([sys.executable, "corpo.py", str(n)], capture_output=True)
g = [list(l) for l in open(f"c{n}.txt", encoding="utf-8").read().split("\n") if l]
def p(x, y, c):
    if 0 <= x < n and 0 <= y < n: g[y][x] = c
esc = lambda x, y: (int(round((x + 0.5) * k - 0.5)), int(round((y + 0.5) * k - 0.5)))
def linha(a, b):
    (x0, y0), (x1, y1) = a, b; m = max(abs(x1 - x0), abs(y1 - y0)); pts = []
    for i in range(m + 1):
        t = i / m if m else 0; q = (int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t)))
        if q not in pts: pts.append(q)
    return pts
# a boca: as bordas pelas regras do 32 (a borda da frente acesa logo abaixo do fundo; a de trás acesa por dentro)
BOCA = {"3": "P", "4": "Q", "5": "U", "6": "V", "7": "W"}
cols = [x for y in range(n) for x in range(n) if g[y][x] in "i"]
xi0, xi1 = min(cols), max(cols)
# (a borda vem do corpo.py: 6 na frente, 4 atrás; aqui só a luz da beira da frente e as letras da camada boca)
for y in range(n):
    for x in range(n):
        if g[y][x] in "46" and any(0 <= y + dy < n and 0 <= x + dx < n and g[y + dy][x + dx] == "i"
                                   for dx, dy in ((0, -1), (1, -1), (-1, 0), (1, 0), (0, 1), (-1, 1))):
            frente = any(0 <= y - 1 and g[y - 1][xx] == "i" for xx in (x, x + 1) if xx < n)
            c = "7" if frente and x < xi0 + 0.7 * (xi1 - xi0) else ("5" if g[y][x] == "4" and x < xi0 + 0.5 * (xi1 - xi0) else g[y][x])
            if x > xi1: c = "3"
            g[y][x] = BOCA[c]
        elif g[y][x] == "6" and y < n * 0.5: g[y][x] = "V"
        elif g[y][x] == "4" and y < n * 0.42: g[y][x] = "Q"
# as cintas: a beira de cima acesa, a de baixo escura
for y in range(1, n - 1):
    for x in range(n):
        if g[y][x] == "B" and g[y - 1][x] not in "AB" and g[y + 1][x] in "AB": p(x, y, "C")
        elif g[y][x] == "B" and g[y + 1][x] not in "ABC": p(x, y, "A")
# o latão: a argola na cinta de cima, o rebite na de baixo (2 px por lado a partir do 40)
for (x, y) in ((14, 16), (10, 26)):
    X, Y = esc(x, y)
    p(X, Y, "z"); p(X + 1, Y, "y"); p(X, Y + 1, "y"); p(X + 1, Y + 1, "x")
# a alça: o caminho do 32 na grade, 1 px
ALCA = [(20, 21), (21, 22), (22, 23), (22, 24), (22, 25), (21, 26), (20, 27), (19, 27), (18, 27), (17, 28)]
pts = []
for a, b in zip(ALCA, ALCA[1:]):
    for q in linha(esc(*a), esc(*b)):
        if q not in pts: pts.append(q)
for i, (x, y) in enumerate(pts):
    p(x, y, "F" if i < len(pts) * 0.35 else ("E" if i < len(pts) * 0.7 else "D"))
# as flechas: o caminho de cada haste do 32 na grade; as penas nos F px de trás, largas atrás e afinando
F = {40: 5, 48: 6}[n]
def flecha(base, nock, claras, deitada):
    pts = linha(esc(*base), esc(*nock))
    sombra = len(pts) * 0.35
    for i, (x, y) in enumerate(pts): p(x, y, "j" if i < sombra else "l")
    pena = pts[-F - 1:-1]          # o último pixel (o entalhe) fica só haste
    luz, med, esc_ = ("o", "n", "m") if claras else ("T", "S", "R")
    for j, (x, y) in enumerate(pena):   # j=0 é o da frente (afina), o último é o de trás (largo)
        L = (x, y - 1) if deitada else (x - 1, y)
        R = (x + 1, y) if deitada else (x + 1, y)
        if j == 0:
            p(*L, esc_)
            continue
        p(*L, luz if j >= F // 2 else med); p(*R, med if j >= F // 2 else esc_)
        largas = 1 if n < 48 else 2          # atrás, a pena de cá ganha um pixel (no 48, nas duas últimas linhas)
        if j >= len(pena) - largas:
            if deitada: p(x - 1, y - 1, med)
            else: p(x - 2, y, med)
flecha((18, 11), (20, 1), True, False)
flecha((20, 12), (25, 3), False, False)
flecha((22, 14), (29, 7), True, True)
mostrar(g)
open(f"c{n}m.txt", "w", encoding="utf-8").write("\n".join("".join(r) for r in g) + "\n")
