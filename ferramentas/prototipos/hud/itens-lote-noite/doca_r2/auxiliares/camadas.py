# auxiliar: a camada de cada pixel das grades da mochila e do mapa, pelas mesmas medidas dos scripts de desenho
import re
def grade(f):
    return [list(l.replace("O", ".")) for l in open(f).read().split("\n") if l]
def mochila(n, src, txt):
    s = open(src, encoding="utf-8").read(); ns = {}
    exec(s[s.index("FUNDO = {"):s.index("\n", s.index("FUNDO = {"))], ns)
    for nome in ("BOLSO_E", "BOLSO_D"):
        i = s.index(nome + " = {"); exec(s[i:s.index("\n", i)], ns)
    rolo = re.search(r"ROLO = (\{.*?\})", s).group(1); ns["ROLO"] = eval(rolo)
    g = grade(txt); cam = [["." if c == "." else "c" for c in r] for r in g]   # c: corpo
    cinta_x = (17, 18) if n == 36 else (15, 16)
    caixa = (15, 21, 20, 25) if n == 36 else (13, 18, 18, 22)
    for y in range(n):
        for x in range(n):
            if g[y][x] == ".": continue
            if y in ns["ROLO"] and ns["ROLO"][y][0] <= x <= ns["ROLO"][y][1]: cam[y][x] = "r"
            elif y in ns["BOLSO_E"] and x <= ns["BOLSO_E"][y][1]: cam[y][x] = "b"
            elif y in ns["BOLSO_D"] and x >= ns["BOLSO_D"][y][0]: cam[y][x] = "b"
            elif x in ns["FUNDO"] and y <= ns["FUNDO"][x] and y >= (9 if n == 36 else 8): cam[y][x] = "a"
            if x in cinta_x and cam[y][x] in "ca" and y >= (15 if n == 36 else 13) and g[y][x] in "23": cam[y][x] = "t"
            if caixa[0] <= x <= caixa[2] and caixa[1] <= y <= caixa[3] and g[y][x] in "xyz1": cam[y][x] = "f"
    return cam
def mapa(n, txt):
    g = grade(txt); cam = [["." if c == "." else "p" for c in r] for r in g]   # p: papel
    vincos = (13, 23) if n == 36 else (12, 21)
    for y in range(n):
        for x in range(n):
            c = g[y][x]
            if c == ".": continue
            if c in "rst": cam[y][x] = "x" if x >= (26 if n == 36 else 23) and y <= (12 if n == 36 else 11) else "q"
            elif c in "vwlm": cam[y][x] = "e"          # o terreno
            elif c == "A" or (c == "B" and (y + 1 >= n or g[y + 1][x] == ".")): cam[y][x] = "s"   # a espessura
            elif x in vincos and c in "CF": cam[y][x] = "v"
    return cam
import pathlib, sys
B = pathlib.Path(sys.argv[1])
for n, src, txt in ((36, "m36h.py", "m36h.txt"), (32, "m32h.py", "m32h.txt")):
    (B / f"atalho-inventario-{n}.txt").write_text("\n".join("".join(r) for r in grade(txt)) + "\n")
    (B / f"atalho-inventario-{n}-camadas.txt").write_text("\n".join("".join(r) for r in mochila(n, src, txt)) + "\n")
for n, txt in ((36, "mapa36.txt"), (32, "mapa32.txt")):
    (B / f"atalho-mapa-{n}.txt").write_text("\n".join("".join(r) for r in grade(txt)) + "\n")
    (B / f"atalho-mapa-{n}-camadas.txt").write_text("\n".join("".join(r) for r in mapa(n, txt)) + "\n")
print("ok")
