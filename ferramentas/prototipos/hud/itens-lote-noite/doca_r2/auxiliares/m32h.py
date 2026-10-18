# a mochila 36 à mão, região por região (de trás para a frente)
from ver import salvar
g = {}
def faixa(y, x0, x1, f):
    for x in range(x0, x1 + 1): g[(x, y)] = f(x) if callable(f) else f
# o corpo: o saco de couro, aceso à esquerda, escuro à direita e embaixo; os painéis do lado (as costuras de volume)
CORPO = {8: (9, 22), 9: (8, 23), **{y: (7, 24) for y in range(10, 16)}, **{y: (6, 25) for y in range(16, 26)}, 26: (6, 25), 27: (7, 24), 28: (9, 22)}
for y, (a, b) in CORPO.items():
    def t(x, y=y):
        c = 5 if x <= 9 else 4 if x <= 15 else 3 if x <= 20 else 2
        if y >= 25: c -= 1
        return str(max(1, c))
    faixa(y, a, b, t)
for y in range(15, 26):
    g[(9, y)] = "6" if y < 24 else "4"           # a costura do painel da esquerda pega luz
    g[(22, y)] = "1"                               # a do painel da direita, na sombra
# os bolsos dos lados, por fora do corpo: a abinha acesa em cima com a beira escura, a costura junto do corpo
BOLSO_E = {18: (3, 5), 19: (2, 5), **{y: (2, 5) for y in range(20, 26)}, 26: (2, 5), 27: (3, 5)}
BOLSO_D = {18: (26, 28), 19: (26, 29), **{y: (26, 29) for y in range(20, 26)}, 26: (26, 29), 27: (26, 28)}
for y in range(18, 28):
    for x in range(BOLSO_E[y][0], BOLSO_E[y][1] + 1):
        g[(x, y)] = "6" if y == 18 else "5" if y == 19 else "2" if y == 20 else ("5" if x < 3 else "4" if x < 4 else "3") if y < 26 else "2"
    g[(6, y)] = "2" if 18 <= y <= 26 else g.get((6, y), "2")
    for x in range(BOLSO_D[y][0], BOLSO_D[y][1] + 1):
        g[(x, y)] = "4" if y == 18 else "3" if y == 19 else "1" if y == 20 else ("2" if x < 28 else "1") if y < 26 else "1"
    g[(25, y)] = "1" if 18 <= y <= 26 else g.get((25, y), "1")
# a aba: a dobra de cima acesa, o corpo dela pela luz, a borda de baixo em U (escura) e a sombra no corpo
FUNDO = {8: 15, 9: 15, 10: 16, 11: 16, 12: 17, **{x: 18 for x in range(13, 19)}, 19: 17, 20: 16, 21: 16, 22: 15, 23: 15}
for x, yb in FUNDO.items():
    for y in range(8, yb + 1):
        c = "7" if y == 8 else ("6" if x <= 11 else "5" if x <= 17 else "4" if x <= 20 else "3")
        if y == 9 and x <= 17: c = "7" if x <= 11 else "6"
        if y == yb: c = "2"
        g[(x, y)] = c
    g[(x, yb + 1)] = "2" if x > 16 else "3"
# a cinta do meio, por cima da aba e do corpo
for y in range(13, 26):
    g[(15, y)] = "3"; g[(16, y)] = "2"
# a fivela vazada (latão): a cinta passa por dentro, o pino no meio
for (x, y, c) in ((13, 18, "z"), (14, 18, "z"), (15, 18, "z"), (16, 18, "y"), (17, 18, "y"), (18, 18, "x"),
                  (13, 19, "z"), (18, 19, "x"), (13, 20, "y"), (18, 20, "x"), (13, 21, "y"), (18, 21, "x"),
                  (13, 22, "y"), (14, 22, "x"), (15, 22, "x"), (16, 22, "x"), (17, 22, "x"), (18, 22, "x"),
                  (14, 19, "1"), (17, 19, "1"), (14, 20, "1"), (17, 20, "1"), (14, 21, "1"), (17, 21, "1"),
                  (15, 20, "z"), (16, 20, "y")):
    g[(x, y)] = c
# o cobertor enrolado em cima, preso por duas tiras de couro; as pontas em espiral
ROLO = {2: (9, 22), 3: (8, 23), 4: (7, 24), 5: (7, 24), 6: (7, 24), 7: (8, 23)}
TOM = {2: "k", 3: "k", 4: "j", 5: "i", 6: "h", 7: "h"}
for y, (a, b) in ROLO.items():
    faixa(y, a, b, TOM[y])
    for x in (a, b): g[(x, y)] = "h" if x == b or y > 4 else "i"
g[(7, 4)] = "j"; g[(8, 4)] = "g"; g[(24, 4)] = "i"; g[(23, 4)] = "g"
for y in range(2, 8):
    for x in (11, 12, 20, 21):
        g[(x, y)] = ("4" if x in (11, 20) else "3") if y <= 4 else ("3" if x in (11, 20) else "2")
salvar(g, 32, "m32h.png")
