# a ediÃ§Ã£o Ã  mÃ£o da aljava 32 sobre o rascunho do corpo: a boca, as cintas com o latÃ£o, a alÃ§a e as trÃªs flechas

from regioes import mostrar

g = [list(l) for l in open("c32.txt").read().split("\n") if l]

def p(x, y, c): g[y][x] = c

def varios(lst, c=None, m=None):

    for t in lst:

        p(t[0], t[1], (m or {}).get(c or t[2], c or t[2]))

# a boca: o fundo escuro, a parede de trÃ¡s (acesa por dentro), a borda da frente com a luz em cima

for y in range(9, 17):

    for x in range(14, 25):

        if g[y][x] in "i": g[y][x] = "5"

varios([(18, 11), (18, 12), (19, 12), (20, 12), (19, 13), (20, 13), (21, 13), (20, 14), (21, 14), (22, 14), (21, 15), (22, 15)], "i")
BOCA = {"3": "P", "4": "Q", "5": "U", "6": "V", "7": "W"}

varios([(17, 10, "5"), (18, 10, "5"), (19, 11, "5"), (20, 11, "4"), (21, 12, "4"), (22, 13, "4"), (23, 14, "3"), (23, 15, "3")], m=BOCA)

varios([(16, 11, "6"), (17, 11, "7"), (16, 12, "6"), (17, 12, "7"), (17, 13, "6"), (18, 13, "7"), (18, 14, "6"), (19, 14, "7"),

        (19, 15, "6"), (20, 15, "6"), (20, 16, "5"), (21, 16, "5"), (22, 16, "4"), (23, 16, "3")], m=BOCA)

# as cintas: a beira de cima acesa (a que olha para a boca); a argola de latão na de cima, o rebite na de baixo

for y in range(1, 32):

    for x in range(32):

        if g[y][x] == "B" and g[y - 1][x] not in "AB" and g[y + 1][x] in "AB": p(x, y, "C")
        elif g[y][x] == "B" and g[y + 1][x] not in "ABC": p(x, y, "A")

varios([(14, 16, "z"), (15, 17, "y"), (10, 26, "z")])

# a alça, pendurada do lado de fora (direita), da ponta da cinta de cima até perto da de baixo

varios([(20, 21, "4"), (21, 22, "4"), (22, 23, "4"), (22, 24, "3"), (22, 25, "3"), (21, 26, "3"), (20, 27, "2"), (19, 27, "2"),

        (18, 27, "2"), (17, 28, "2")], m={"2": "D", "3": "E", "4": "F"})

# as flechas: a haste (j na sombra perto da boca, l acesa) e as penas largas atrÃ¡s, afinando para a frente

def haste(pts, ate):

    for i, (x, y) in enumerate(pts): p(x, y, "j" if i < ate else "l")

A1 = [(18, 11), (18, 10), (19, 9), (19, 8), (19, 7), (20, 6), (20, 5), (20, 4), (20, 3), (20, 2), (20, 1)]

haste(A1, 4)

varios([(19, 2, "o"), (21, 2, "n"), (19, 3, "o"), (21, 3, "n"), (19, 4, "n"), (21, 4, "m"), (19, 5, "m")])

A2 = [(20, 12), (21, 11), (21, 10), (22, 9), (23, 8), (23, 7), (24, 6), (24, 5), (25, 4), (25, 3)]

haste(A2, 4)

varios([(24, 4, "T"), (26, 4, "S"), (23, 5, "T"), (25, 5, "S"), (23, 6, "S"), (25, 6, "R"), (22, 7, "R")])

A3 = [(22, 14), (23, 13), (24, 12), (25, 11), (26, 10), (27, 9), (28, 8), (29, 7)]

haste(A3, 4)

varios([(26, 9, "o"), (27, 8, "o"), (28, 7, "o"), (27, 10, "n"), (28, 9, "n"), (29, 8, "n"), (25, 10, "m")])

mostrar(g)

open("c32m.txt", "w").write("\n".join("".join(r) for r in g) + "\n")

