# o Diário 36 à mão: o livro aberto visto um pouco de cima (as páginas em arco, a dobra do meio funda), a capa de couro
# por baixo, as camadas das folhas nas bordas, poucas anotações, a pena e a fita do marcador
import math
from ver import salvar
from rotulos import Grade
g = Grade()
GX = 17.5                      # a dobra do meio
def topo(x):                   # a borda de cima: funda na dobra, alta no meio de cada página, um pouco mais baixa na beira
    d = min(abs(x + 0.5 - GX) / 14.5, 1)
    return 15.0 - 6.5 * math.sin(d * math.pi * 0.7) + 1.5 * d
def base(x):
    d = min(abs(x + 0.5 - GX) / 14.5, 1)
    return 28.6 - 2.8 * math.sin(d * math.pi * 0.7) + 0.8 * d
g.atual = "capa"
# a capa de couro por baixo: a beira à vista nos lados e embaixo
for x in range(1, 35):
    t, b = topo(x) + 2.0, base(x) + 2.4
    for y in range(int(t), int(b) + 1):
        g[(x, y)] = "n" if x < GX and y < b - 1 else "m" if y < b - 1 else "k"
g.atual = "paginas"
# as páginas: o papel aceso; a curva que entra na dobra escurece (2 px de cada lado)
for x in range(3, 33):
    t, b = topo(x), base(x)
    d = abs(x + 0.5 - GX)
    for y in range(int(math.ceil(t)), int(b) + 1):
        c = "s" if d > 3 else "q" if d > 2 else "p" if d > 1 else "r"
        if x > GX and c == "s": c = "q" if y > b - 2 else "s"
        if y >= b - 1 and c == "s": c = "q"
        g[(x, y)] = c
g.atual = "paginas"
# as camadas das folhas nas beiras (a espessura do bloco)
for x in (3, 4, 31, 32):
    for y in range(int(topo(x)) + 1, int(base(x)) + 2):
        g[(x, y)] = "q" if (y + x) % 2 else "r"
PAGINA = dict(g)
g.atual = "anotacoes"
# as anotações: poucas linhas de tinta, de tamanhos diferentes, acompanhando a curva da página
for (x0, x1, dy) in ((6, 13, 3), (6, 10, 6), (7, 14, 9), (6, 11, 12), (21, 25, 3)):
    for x in range(x0, x1 + 1):
        g[(x, int(topo(x)) + dy)] = "r"
g.atual = "fita"
# a fita do marcador, saindo da dobra por baixo
for y in range(28, 34):
    g[(17, y)] = "S"; g[(18, y)] = "R"
g.atual = "pena"
# a pena: a ponta na página da direita, a pluma afunilada subindo para a direita (acesa do lado de cima)
pts = [(21 + i * 0.58, 25 - i) for i in range(0, 20)]
for i, (fx, fy) in enumerate(pts):
    x, y = int(round(fx)), int(round(fy))
    if y < 2: break
    if i < 3:
        g[(x, y)] = "1" if i == 0 else "t"          # a ponta (o bico com tinta) e o cálamo
        continue
    g[(x, y)] = "w"                                  # a raque
    larg = min(i - 2, 3, 21 - i) if i < 19 else 1
    for k in range(1, larg + 1):
        if k == larg and i % 4 == 0: continue        # os recortes da barba (a pena, não uma lâmina)
        g[(x - k, y)] = "w" if k < larg else "u"     # a barba de cima, acesa (o branco frio contra o papel creme)
    for k in range(1, max(1, larg - 1) + 1):
        if k == max(1, larg - 1) and i % 4 == 2: continue
        g[(x + k, y)] = "u" if k == 1 else "t"       # a de baixo, na sombra
g.atual = "paginas"
# a pena sobre o papel: a sombra dela na página (embaixo, à direita)
pena = {k for k, c in g.items() if c in "swut" and k[0] >= 19 and g[k] != PAGINA.get(k)}
for (x, y) in sorted(pena):
    for q in ((x + 1, y + 1), (x + 2, y + 1)):
        if q in PAGINA and q not in pena and g[q] in "sq": g[q] = "p"
salvar(g, 36, "d36.png")
import json; json.dump({f"{x},{y}": c for (x, y), c in g.cam.items()}, open("d36.cam.json", "w"))
