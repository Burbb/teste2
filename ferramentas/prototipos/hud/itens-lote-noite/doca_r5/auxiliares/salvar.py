# o Salvar (36): o baú aberto, de frente e um pouco de cima, e a seta de aço descendo para dentro dele. O baú inteiro
# à vista (a tampa aberta para trás, a boca escura com a borda acesa, a frente de madeira com as cintas e a fechadura);
# a seta contida no meio, fria (aço), para se separar da madeira e do latão e do Sair (a seta quente).
import sys, json
from ver import contorno, imagem
n = int(sys.argv[1]); k = n / 36
def r(v): return int(round(v * k))
g = {}; cam = {}
def pinta(x, y, c, camada):
    if 0 <= x < n and 0 <= y < n: g[(x, y)] = c; cam[(x, y)] = camada
X0, X1 = r(5), r(30)
# a tampa aberta: a face de dentro, um pouco mais estreita em cima (vai para trás), madeira escura com a beira de latão
TY0, TY1 = r(8), r(15)
for y in range(TY0, TY1 + 1):
    recuo = 1 if y < TY0 + 2 else 0                       # a tampa vai um pouco para trás em cima
    for x in range(X0 + 1 + recuo, X1 - recuo):
        borda = y == TY0 or x in (X0 + 1 + recuo, X1 - 1 - recuo)
        c = ("y" if x < (X0 + X1) // 2 else "x") if borda else ("g" if x < (X0 + X1) * 0.45 else "f")
        if not borda and y == (TY0 + TY1) // 2 + 1: c = "e"           # a junta das tábuas de dentro
        pinta(x, y, c, "tampa")
# a boca: o fundo escuro, com a borda de trás e a da frente (acesa) de madeira
BY0, BY1 = r(16), r(20)
for y in range(BY0, BY1 + 1):
    for x in range(X0, X1 + 1):
        pinta(x, y, "v" if BY0 < y < BY1 else ("w" if y == BY0 else "j" if x < X1 - 4 else "i"), "corpo")
# a frente do baú: as tábuas (a luz da esquerda, a junta escura), a base mais escura
FY0, FY1 = BY1 + 1, r(32)
for y in range(FY0, FY1 + 1):
    for x in range(X0, X1 + 1):
        u = (x - X0) / (X1 - X0)
        c = "i" if u < 0.3 else "h" if u < 0.72 else "g"
        if y == r(26): c = "f"                                   # a junta entre as tábuas
        if y >= FY1 - 1: c = "f" if u < 0.5 else "e"             # a base, na sombra
        if x in (X0, X1): c = "g" if x == X0 else "e"
        pinta(x, y, c, "corpo")
# as cintas de latão (verticais) e a fechadura no meio
for cx in (r(9.5), r(25.5)):
    for y in range(FY0, FY1 + 1):
        pinta(cx, y, "z" if y < r(24) else "y", "latao"); pinta(cx + 1, y, "y" if y < r(24) else "x", "latao")
LX0, LX1, LY0, LY1 = r(15), r(20), r(23), r(28)
for y in range(LY0, LY1 + 1):
    for x in range(LX0, LX1 + 1):
        pinta(x, y, "z" if (x == LX0 or y == LY0) and not (x == LX1 or y == LY1) else "x" if (x == LX1 or y == LY1) else "y", "latao")
pinta((LX0 + LX1) // 2, LY0 + 2, "v", "latao"); pinta((LX0 + LX1) // 2, LY0 + 3, "v", "latao")   # o buraco da chave
base = contorno(dict(g), n)
# a seta: o cabo e a ponta, descendo para dentro da boca (contorno próprio por cima do baú)
s = {}
SX = (X0 + X1) / 2
for y in range(n):
    for x in range(n):
        px, py = (x + 0.5) / k, (y + 0.5) / k
        cabo = abs(px - 17.75) <= 2.1 and 2.0 <= py <= 11.0
        ponta = 10.0 <= py <= 19.6 and abs(px - 17.75) <= (19.6 - py) * 0.6
        if cabo or ponta:
            u = (px - 17.75)
            s[(x, y)] = "P" if u < -0.9 else "o" if u < 0.9 else "n"
seta = contorno(s, n)
h = dict(base)
for p, v in seta.items():
    h[p] = v; cam[p] = "seta" if v != "O" else "contorno"
for p, v in h.items():
    if v == "O" and p not in seta: cam[p] = "contorno"
imagem(h, n, f"s{n}.png")
json.dump({f"{x},{y}": c for (x, y), c in cam.items()}, open(f"s{n}.cam.json", "w"))
