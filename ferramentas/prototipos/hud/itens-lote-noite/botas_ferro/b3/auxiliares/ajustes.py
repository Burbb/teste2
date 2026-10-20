"""Os ajustes à mão da B3 sobre o rascunho (grades/rascunho.txt, a redução da referência na paleta do conjunto), pixel a
pixel, guiados pela medida das linhas da referência (reducao.linhas): o resultado é grades/B3.txt, a fonte das camadas.
    python ajustes.py <pasta da B3>
"""
import pathlib
import sys

# (x, y): o caractere novo, com o porquê
AJUSTES = {}
def poe(y, x0, s, porque):
    for k, ch in enumerate(s): AJUSTES[(x0 + k, y)] = (ch, porque)

# a bota de trás: a boca (a beira do fundo em aço, o vão escuro, as beiras dos lados)
poe(1, 20, "#34433332", "a beira do fundo da boca de trás, em aço (o rascunho a fazia de couro escuro)")
poe(2, 20, "43biiiib23", "o vão da boca de trás, escuro, entre as beiras")
poe(3, 23, "3", "a beira da frente da boca de trás, aço")
# a bota da frente: a boca
poe(5, 10, "334444433", "a beira do fundo da boca da frente, em aço")
poe(6, 9, "54biiiiib34", "o vão da boca da frente, escuro, entre as beiras acesas")
poe(7, 9, "45777776543", "o lábio da boca da frente, aceso (o rascunho deixava o vão escorrer pela direita)")
# a linha entre as duas botas (o rascunho a fazia de couro escuro e interior)
for x, y in ((20, 7), (21, 7), (20, 8), (21, 8), (20, 9), (10, 10), (19, 10), (22, 11), (22, 12), (22, 13), (22, 14),
             (21, 15), (20, 17), (20, 18), (19, 19), (19, 20)):
    AJUSTES[(x, y)] = ("#", "o contorno entre as botas e nas beiras do cano")
poe(6, 28, "32", "a beira de trás do cano de trás, aço acima da tira")
# as tiras e as fivelas (a fivela dourada da referência em ferro claro, a paleta do conjunto)
poe(13, 23, "efedd7c", "a tira da bota de trás com a fivela à direita")
poe(14, 23, "455443c", "o aço abaixo da tira de trás")
poe(17, 11, "deeeedd76", "a tira da bota da frente inteira, com a fivela à direita")
poe(18, 11, "c", "a tira da frente, embaixo")
poe(18, 19, "6", "a fivela da frente, embaixo")
poe(19, 17, "cd", "o couro do calcanhar da frente")
poe(20, 18, "c", "o couro do calcanhar da frente")
# as junções das placas do pé da frente (as linhas da referência, em diagonal até a biqueira)
for x, y in ((13, 22), (14, 23), (15, 24), (12, 25), (13, 26), (13, 27), (9, 26), (9, 27)):
    AJUSTES[(x, y)] = ("2", "a junção entre as placas do pé da frente")
poe(30, 4, "b", "a sola de baixo, couro")
poe(30, 9, "bb", "a beira de baixo da sola da frente, couro (o rascunho a fazia de interior)")
poe(28, 17, "b", "o fim do calcanhar da frente, couro")
poe(22, 25, "bcc", "a sola da bota de trás, couro")
poe(23, 25, "b", "a sola da bota de trás, couro")


def contorno_1px(g):
    """O contorno com 1 px: a beira escura do desenho (o tom 2 ou o couro escuro b encostando no contorno de fora) vira
    contorno, e o contorno de fora que sobra (sem nada cheio do lado) sai."""
    g = [list(l) for l in g]
    fora = lambda x, y: not (0 <= x < 32 and 0 <= y < 32) or g[y][x] == "."
    externo = lambda x, y: 0 <= x < 32 and 0 <= y < 32 and g[y][x] == "#" and any(
        fora(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    vira = [(x, y) for y in range(32) for x in range(32) if g[y][x] in "2b" and any(
        externo(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in vira: g[y][x] = "#"
    cheio = lambda x, y: 0 <= x < 32 and 0 <= y < 32 and g[y][x] not in ".#"
    sobra = [(x, y) for y in range(32) for x in range(32) if g[y][x] == "#" and not any(
        cheio(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in sobra: g[y][x] = "."
    return ["".join(l) for l in g], len(vira), len(sobra)


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g = [list(l) for l in (base / "grades/rascunho.txt").read_text(encoding="utf-8").split("\n")[:32]]
    for (x, y), (ch, _) in AJUSTES.items(): g[y][x] = ch
    g, v, s = contorno_1px(["".join(l) for l in g])
    (base / "grades/B3.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    print(f"{len(AJUSTES)} ajustes; contorno: {v} beiras viraram contorno, {s} sobras saíram")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(g)))
