from ver import salvar
g = {}
# a lâmina em 6 linhas: o bisel aceso, dois planos claros, o sulco, o plano escuro, o bisel escuro; afina em ponta
for p, ini, fim in ((27, 6, 18), (28, 3, 18), (29, 1, 18), (30, 2, 19), (31, 4, 19), (32, 6, 19), (33, 10, 19)):
    for y in range(ini, fim + 1):
        if p == 27: c = "5"
        elif p == 28: c = "7" if y >= 6 else "6"
        elif p == 29: c = "6"
        elif p == 30: c = "4" if y >= 9 else "5"
        elif p in (31, 32): c = "3"
        else: c = "2"
        g[(p - y, y)] = c
# a guarda: as duas linhas de través, o miolo engrossado e as pontas viradas para a lâmina
for x in range(7, 16):
    g[(x, x + 8)] = "c"; g[(x, x + 9)] = "b"
for x in range(8, 15):
    g[(x, x + 10)] = "a"          # a face de baixo da guarda, na sombra
for (x, y, c) in ((9, 16, "c"), (10, 17, "d"), (11, 18, "c"), (12, 19, "c"), (13, 22, "b"), (10, 20, "a"), (11, 21, "a"), (12, 22, "a"),
                  (7, 14, "d"), (6, 14, "c"), (16, 23, "b"), (16, 24, "a")):
    g[(x, y)] = c
# o cabo: as voltas do couro (acesa, sombra) e o vão escuro entre elas
for (x, y, c) in ((9, 20, "m"), (9, 21, "l"), (8, 21, "k"), (8, 22, "k"), (7, 22, "m"), (7, 23, "l"), (6, 23, "k"), (6, 24, "k")):
    g[(x, y)] = c
# o pomo redondo
for (x, y, c) in ((3, 24, "d"), (4, 24, "c"), (5, 24, "c"), (2, 25, "c"), (3, 25, "d"), (4, 25, "c"), (5, 25, "b"),
                  (2, 26, "b"), (3, 26, "c"), (4, 26, "b"), (5, 26, "a"), (3, 27, "a"), (4, 27, "a")):
    g[(x, y)] = c
salvar(g, 32, "e32.png")
