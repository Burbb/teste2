from ver import salvar
g = {}
# a lâmina em 5 linhas, afinando em ponta: cada linha começa mais abaixo quanto mais longe do centro (p=22)
for p, ini, fim in ((20, 5, 13), (21, 3, 13), (22, 1, 14), (23, 2, 14), (24, 6, 14)):
    for y in range(ini, fim + 1):
        if p == 20: c = "5"
        elif p == 21: c = "7" if y >= 5 else "6"
        elif p == 22: c = "4" if y >= 7 else "6"
        elif p == 23: c = "3"
        else: c = "2"
        g[(p - y, y)] = c
# a guarda: mais curta, o miolo engrossado, as pontas viradas para a lâmina, com a conta de latão
for x in range(5, 12):
    g[(x, x + 6)] = "c"; g[(x, x + 7)] = "b"
for (x, y, c) in ((7, 12, "c"), (8, 13, "d"), (9, 14, "c"), (10, 15, "b"), (7, 15, "a"), (8, 16, "a"),
                  (5, 10, "d"), (4, 10, "c"), (12, 17, "b"), (12, 18, "a")):
    g[(x, y)] = c
# o cabo (couro claro e escuro em faixas) e o pomo redondo
# o cabo: o couro enrolado, a volta acesa (m) do lado da luz e a sombra (l) do outro, com o vão escuro (k) entre voltas
for (x, y, c) in ((6, 16, "m"), (6, 17, "l"), (5, 17, "k"), (5, 18, "k"), (4, 18, "m"), (4, 19, "l")):
    g[(x, y)] = c
for (x, y, c) in ((2, 19, "d"), (3, 19, "c"), (1, 20, "c"), (2, 20, "c"), (3, 20, "b"), (1, 21, "b"), (2, 21, "b"), (3, 21, "a"), (2, 22, "a")):
    g[(x, y)] = c
salvar(g, 24, "e24c.png")
