# a aljava 24 (o topo): a mesma construção do 32, simplificada; sem a alça (não cabe com fundo entre ela e o corpo)
from regioes import mostrar
g = [list(l) for l in open("c24.txt", encoding="utf-8").read().split("\n") if l]
def p(x, y, c): g[y][x] = c
def varios(lst, c=None, m=None):
    for t in lst: p(t[0], t[1], (m or {}).get(c or t[2], c or t[2]))
# a boca
varios([(12, 8, "5"), (13, 8, "5"), (14, 8, "4"), (12, 9, "6"), (13, 9, "i"), (14, 9, "i"), (15, 9, "4"),
        (11, 10, "6"), (12, 10, "7"), (13, 10, "7"), (14, 10, "i"), (15, 10, "i"), (16, 10, "3"),
        (11, 11, "5"), (12, 11, "6"), (13, 11, "6"), (14, 11, "7"), (15, 11, "6"), (16, 11, "i"), (17, 11, "3")], m={"3": "P", "4": "Q", "5": "U", "6": "V", "7": "W"})
for y in range(1, 23):
    for x in range(24):
        if g[y][x] == "B" and g[y - 1][x] not in "AB" and g[y + 1][x] in "AB": p(x, y, "C")
        elif g[y][x] == "B" and g[y + 1][x] not in "ABC": p(x, y, "A")
varios([(11, 12, "z"), (7, 19, "z")])
def haste(pts, ate):
    for i, (x, y) in enumerate(pts): p(x, y, "j" if i < ate else "l")
haste([(13, 9), (13, 8), (13, 7), (14, 6), (14, 5), (14, 4), (14, 3), (14, 2), (14, 1)], 3)
varios([(13, 2, "o"), (15, 2, "n"), (13, 3, "o"), (15, 3, "m"), (13, 4, "m")])
haste([(15, 10), (15, 9), (16, 8), (16, 7), (17, 6), (17, 5), (18, 4), (18, 3)], 3)
varios([(17, 4, "T"), (19, 4, "S"), (16, 5, "T"), (18, 5, "S"), (16, 6, "R")])
haste([(16, 11), (17, 10), (18, 9), (19, 8), (20, 7), (21, 6)], 3)
varios([(19, 7, "o"), (20, 6, "o"), (20, 8, "n"), (21, 7, "n"), (18, 8, "m")])
mostrar(g)
open("c24m.txt", "w").write("\n".join("".join(r) for r in g) + "\n")
