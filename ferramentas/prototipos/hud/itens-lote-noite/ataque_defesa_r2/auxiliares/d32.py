# o escudo 24 à mão: por linha, a face (xl..xr) e a espessura à direita (até xs); o aro de latão na beira da face
from ver import salvar
L = {2: (6, 21, 22), 3: (4, 23, 24), 4: (4, 23, 25), **{y: (4, 23, 26) for y in range(5, 16)}, 16: (5, 23, 26),
     17: (5, 22, 25), 18: (6, 22, 25), 19: (6, 21, 24), 20: (7, 21, 24), 21: (8, 20, 23), 22: (9, 20, 22), 23: (10, 19, 21),
     24: (11, 18, 20), 25: (12, 18, 19), 26: (13, 17, 18), 27: (14, 16, 17), 28: (15, 15, 16)}
g = {}
ultimo = max(L)
for y, (xl, xr, xs) in L.items():
    for x in range(xl, xs + 1):
        if x > xr:                                        # a espessura (o lado do escudo), na sombra
            g[(x, y)] = ("b" if y <= 3 else "a") if x == xr + 1 else "z"   # a beira do lado acesa, o resto escuro
            continue
        aro = x == xl or x == xr or y == 2 or y == ultimo or (y == 3 and (x < 6 or x > 21)) or (y + 1 in L and (x < L[y + 1][0] or x > L[y + 1][1]))
        if aro:
            u = (x - xl) / max(1, xr - xl)
            g[(x, y)] = "d" if (y <= 3 and u < 0.5) or (x == xl and y < 12) else ("c" if (u < 0.6 and y < 17) or (x == xl) else "b")
            continue
        # a face de aço convexa: a luz numa faixa à esquerda do meio, escurecendo para a direita e para a ponta
        u = (x - xl - 1) / max(1, xr - xl - 2)
        c = 5 if u < 0.14 else 6 if u < 0.34 else 5 if u < 0.5 else 4 if u < 0.7 else 3 if u < 0.88 else 2
        if 0.14 <= u < 0.34 and 4 <= y <= 8: c = 7                    # o brilho, só no alto da faixa de luz
        if y >= 19: c -= 1
        if y >= 24: c -= 1
        g[(x, y)] = str(max(2, c))
# a bossa: o domo de latão, aceso em cima à esquerda, com a sombra no aço embaixo à direita
for (x, y, c) in ((12, 9, "d"), (13, 9, "c"), (14, 9, "b"), (11, 10, "c"), (12, 10, "d"), (13, 10, "c"), (14, 10, "b"), (15, 10, "a"),
                  (11, 11, "c"), (12, 11, "c"), (13, 11, "b"), (14, 11, "b"), (15, 11, "a"), (11, 12, "b"), (12, 12, "b"), (13, 12, "a"),
                  (14, 12, "a"), (15, 12, "a"), (12, 13, "a"), (13, 13, "a"), (14, 13, "a"),
                  (16, 11, "3"), (16, 12, "3"), (15, 13, "3"), (14, 14, "3")):
    g[(x, y)] = c
salvar(g, 32, "d32.png")
