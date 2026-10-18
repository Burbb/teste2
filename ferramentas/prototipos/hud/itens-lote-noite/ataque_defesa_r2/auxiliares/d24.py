# o escudo 24 à mão: por linha, a face (xl..xr) e a espessura à direita (até xs); o aro de latão na beira da face
from ver import salvar
L = {2: (5, 16, 17), 3: (3, 17, 18), 4: (3, 17, 19), 5: (3, 17, 19), 6: (3, 17, 19), 7: (3, 17, 19), 8: (3, 17, 19),
     9: (3, 17, 19), 10: (3, 17, 19), 11: (3, 17, 19), 12: (4, 17, 19), 13: (4, 16, 18), 14: (5, 16, 18), 15: (5, 15, 17),
     16: (6, 15, 17), 17: (7, 14, 16), 18: (8, 14, 15), 19: (9, 13, 14), 20: (10, 12, 13), 21: (11, 11, 12)}
g = {}
ultimo = max(L)
for y, (xl, xr, xs) in L.items():
    for x in range(xl, xs + 1):
        if x > xr:                                        # a espessura (o lado do escudo), na sombra
            g[(x, y)] = ("b" if y <= 3 else "a") if x == xr + 1 else "z"   # a beira do lado acesa, o resto escuro
            continue
        aro = x == xl or x == xr or y == 2 or y == ultimo or (y == 3 and (x < 5 or x > 15)) or (y + 1 in L and (x < L[y + 1][0] or x > L[y + 1][1]))
        if aro:
            u = (x - xl) / max(1, xr - xl)
            g[(x, y)] = "d" if (y <= 3 and u < 0.5) or (x == xl and y < 9) else ("c" if (u < 0.6 and y < 13) or (x == xl) else "b")
            continue
        # a face de aço convexa: a luz numa faixa à esquerda do meio, escurecendo para a direita e para a ponta
        u = (x - xl - 1) / max(1, xr - xl - 2)
        c = 5 if u < 0.14 else 6 if u < 0.34 else 5 if u < 0.5 else 4 if u < 0.7 else 3 if u < 0.88 else 2
        if 0.14 <= u < 0.34 and 4 <= y <= 6: c = 7                    # o brilho, só no alto da faixa de luz
        if y >= 14: c -= 1
        if y >= 18: c -= 1
        g[(x, y)] = str(max(2, c))
# a bossa: um domo de latão, aceso em cima à esquerda, com a sombra no aço embaixo à direita
for (x, y, c) in ((9, 7, "d"), (10, 7, "c"), (11, 7, "b"), (8, 8, "c"), (9, 8, "d"), (10, 8, "c"), (11, 8, "b"), (12, 8, "a"),
                  (8, 9, "b"), (9, 9, "c"), (10, 9, "b"), (11, 9, "a"), (12, 9, "a"), (9, 10, "a"), (10, 10, "a"), (11, 10, "a"),
                  (12, 10, "3"), (11, 11, "3"), (13, 9, "3")):
    g[(x, y)] = c
salvar(g, 24, "d24.png")
