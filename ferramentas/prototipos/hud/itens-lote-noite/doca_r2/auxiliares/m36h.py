# a mochila 36 à mão, região por região (de trás para a frente)
from ver import salvar
g = {}
def faixa(y, x0, x1, f):
    for x in range(x0, x1 + 1): g[(x, y)] = f(x) if callable(f) else f
# o corpo: o saco de couro, aceso à esquerda, escuro à direita e embaixo; os painéis do lado (as costuras de volume)
CORPO = {9: (10, 25), 10: (9, 26), **{y: (8, 27) for y in range(11, 18)}, **{y: (7, 28) for y in range(18, 30)}, 30: (7, 28), 31: (8, 27), 32: (10, 25)}
for y, (a, b) in CORPO.items():
    def t(x, y=y):
        c = 5 if x <= 10 else 4 if x <= 17 else 3 if x <= 23 else 2
        if y >= 29: c -= 1
        return str(max(1, c))
    faixa(y, a, b, t)
for y in range(17, 30):
    g[(10, y)] = "6" if y < 28 else "4"           # a costura do painel da esquerda pega luz
    g[(25, y)] = "1"                               # a do painel da direita, na sombra
# os bolsos dos lados, por fora do corpo: a abinha acesa em cima com a beira escura, a costura junto do corpo
BOLSO_E = {21: (4, 6), 22: (3, 6), **{y: (2, 6) for y in range(23, 30)}, 30: (3, 6), 31: (4, 6)}
BOLSO_D = {21: (29, 31), 22: (29, 32), **{y: (29, 33) for y in range(23, 30)}, 30: (29, 32), 31: (29, 31)}
for y in range(21, 32):
    for x in range(BOLSO_E[y][0], BOLSO_E[y][1] + 1):
        g[(x, y)] = "6" if y == 21 else "5" if y == 22 else "2" if y == 23 else ("5" if x < 4 else "4" if x < 5 else "3") if y < 30 else "2"
    g[(7, y)] = "2" if 21 <= y <= 30 else g.get((7, y), "2")
    for x in range(BOLSO_D[y][0], BOLSO_D[y][1] + 1):
        g[(x, y)] = "4" if y == 21 else "3" if y == 22 else "1" if y == 23 else ("2" if x < 32 else "1") if y < 30 else "1"
    g[(28, y)] = "1" if 21 <= y <= 30 else g.get((28, y), "1")
# a aba: a dobra de cima acesa, o corpo dela pela luz, a borda de baixo em U (escura) e a sombra no corpo
FUNDO = {9: 17, 10: 17, 11: 18, 12: 18, 13: 19, 14: 19, **{x: 20 for x in range(15, 21)}, 21: 19, 22: 19, 23: 18, 24: 18, 25: 17, 26: 17}
for x, yb in FUNDO.items():
    for y in range(9, yb + 1):
        c = "7" if y == 9 else ("6" if x <= 12 else "5" if x <= 19 else "4" if x <= 23 else "3")
        if y == 10 and x <= 19: c = "7" if x <= 12 else "6"
        if y == yb: c = "2"
        g[(x, y)] = c
    g[(x, yb + 1)] = "2" if x > 18 else "3"
# a cinta do meio, por cima da aba e do corpo
for y in range(15, 30):
    g[(17, y)] = "3"; g[(18, y)] = "2"
# a fivela vazada (latão): a cinta passa por dentro, o pino no meio
for (x, y, c) in ((15, 21, "z"), (16, 21, "z"), (17, 21, "z"), (18, 21, "y"), (19, 21, "y"), (20, 21, "x"),
                  (15, 22, "z"), (20, 22, "x"), (15, 23, "y"), (20, 23, "x"), (15, 24, "y"), (20, 24, "x"),
                  (15, 25, "y"), (16, 25, "x"), (17, 25, "x"), (18, 25, "x"), (19, 25, "x"), (20, 25, "x"),
                  (16, 22, "1"), (19, 22, "1"), (16, 23, "1"), (19, 23, "1"), (16, 24, "1"), (19, 24, "1"),
                  (17, 23, "z"), (18, 23, "y")):
    g[(x, y)] = c
# o cobertor enrolado em cima, preso por duas tiras de couro; as pontas em espiral
ROLO = {2: (10, 25), 3: (9, 26), 4: (8, 27), 5: (8, 27), 6: (8, 27), 7: (8, 27), 8: (9, 26)}
TOM = {2: "k", 3: "k", 4: "j", 5: "j", 6: "i", 7: "h", 8: "h"}
for y, (a, b) in ROLO.items():
    faixa(y, a, b, TOM[y])
    for x in (a, b): g[(x, y)] = "h" if x == b or y > 5 else "i"
g[(8, 5)] = "j"; g[(9, 5)] = "g"; g[(27, 5)] = "i"; g[(26, 5)] = "g"
for y in range(2, 9):
    for x in (12, 13, 22, 23):
        g[(x, y)] = ("4" if x in (12, 22) else "3") if y <= 4 else ("3" if x in (12, 22) else "2")
salvar(g, 36, "m36h.png")
