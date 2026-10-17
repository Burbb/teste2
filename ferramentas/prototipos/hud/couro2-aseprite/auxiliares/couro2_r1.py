"""Rodada 1 do capuz (o desenho "capuz") e da luva com braçadeira (o desenho "luva") da família de couro: as listas de
pixels por camada que o pintar.lua (ferramentas/arte/aseprite/) escreve no Aseprite pelo MCP. O Python só calcula.

    python ferramentas/prototipos/hud/couro2-aseprite/auxiliares/couro2_r1.py <pasta>

O 32 é a fonte: desenhado direto na grade de 32 (as faixas de cada linha e a luz por regras de região). O 64 da prévia
é o 32 ampliado 2× (vizinho mais próximo), não um desenho. Grava <pasta>/<peça>-32/<camada>.lua e .txt, previa.png
(o 32) e previa-64.png (o 2×). As rampas são as do gibão e das botas aprovados (couro_r2.py). Luz de cima e da
esquerda.
"""
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "couro-aseprite" / "auxiliares"))
from couro_r2 import BORDA, BOTA, CORDAO, COURO, FORRO, GASTO, Desenho  # noqa: E402

N = 32


def faixas(d, ext, camada, rampa, tom):
    """Pinta cada linha y de ext {y: (x0, x1)} com tom(x, y) (None deixa vazio)."""
    for y, (x0, x1) in ext.items():
        for x in range(x0, x1 + 1):
            t = tom(x, y)
            if t is not None:
                d.px[(x, y)] = (camada, rampa, max(0, min(len(rampa) - 1, t)))


# --- o capuz -------------------------------------------------------------------------------------------------------
# De frente: a ponta curta no alto, tombada para a direita (a cauda do capuz), a costura do meio do crânio (duas peças de couro), a abertura com a borda virada
# (acesa em cima e à esquerda) e o interior escuro (a parede de dentro da direita pega um pouco de luz: a espessura e
# a fundura), a garganta com o cordão cruzado e a capa de ombro em volta, com dois cortes na barra.
CAPUZ = {1: (17, 18), 2: (15, 19), 3: (13, 20), 4: (11, 21), 5: (10, 21), 6: (9, 22), 7: (9, 22), 8: (8, 23),
         9: (8, 23), 10: (8, 23), 11: (7, 24), 12: (7, 24), 13: (7, 24), 14: (7, 24), 15: (7, 24), 16: (7, 24),
         17: (7, 24), 18: (7, 24), 19: (7, 24), 20: (7, 24)}
ABERTURA = {9: (13, 18), 10: (12, 19), 11: (11, 20), 12: (11, 20), 13: (11, 20), 14: (11, 20), 15: (11, 20),
            16: (12, 19), 17: (12, 19), 18: (13, 18), 19: (14, 17)}
CAPA = {21: (5, 26), 22: (4, 27), 23: (4, 27), 24: (4, 27), 25: (4, 27), 26: (4, 27), 27: (4, 27)}


def capuz():
    d = Desenho(N)
    dentro = {(x, y) for y, (a, b) in ABERTURA.items() for x in range(a, b + 1)}

    def tom_capuz(x, y):
        if (x, y) in dentro: return None
        t = 5 if x < 12 else 4 if x < 20 else 3
        if x >= 23: t = 2
        if y <= 8 and x < 16: t += 1                                   # o alto do crânio, de frente para a luz
        if 2 <= y <= 8 and x == 16 + (y <= 3): t = 3                   # a costura do meio (curva para a ponta)
        if y >= 16: t -= 1                                             # o capuz vira para baixo, na sombra
        return t
    faixas(d, CAPUZ, "capuz", COURO, tom_capuz)
    # a borda virada em volta da abertura: acesa em cima e à esquerda, escura embaixo e à direita
    for (x, y) in list(d.px):
        if any((x + dx, y + dy) in dentro for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            acesa = y <= 10 or x < 15
            d.px[(x, y)] = ("borda", COURO if acesa else BORDA, 6 if acesa and x < 16 else 5 if acesa else 2)
    # o interior: a faixa do forro logo abaixo da borda de cima, a parede de dentro da direita um pouco clara
    def tom_dentro(x, y):
        if (x, y - 1) not in dentro: return 1                          # o forro, logo abaixo da borda
        x1 = ABERTURA[y][1]
        return 2 if x == x1 else 1 if x == x1 - 1 else 0
    faixas(d, ABERTURA, "interior", FORRO, tom_dentro)
    # a capa de ombro: por baixo do capuz, a sombra dele na primeira linha; dois cortes na barra
    def tom_capa(x, y):
        t = 5 if x < 10 else 4 if x < 16 else 3 if x < 22 else 2
        if y == 21: t -= 2
        if x <= 5 and y >= 23: t += 1                                  # a beira de fora da capa, acesa
        return t
    faixas(d, CAPA, "capa", COURO, tom_capa)
    for x in range(4, 28):
        if (x, 27) in d.px: d.px[(x, 27)] = ("capa", BORDA, 2 if x < 16 else 1)   # a barra
    for x in (10, 21):
        for y in (26, 27): d.px[(x, y)] = ("capa", BORDA, 0)          # os cortes da capa
    # o cordão cruzado na garganta
    d.px[(15, 20)] = ("cordao", CORDAO, 2); d.px[(16, 20)] = ("cordao", CORDAO, 1)
    d.px[(15, 21)] = ("cordao", CORDAO, 1); d.px[(16, 21)] = ("cordao", CORDAO, 2)
    # o couro raspado na capa, do lado da sombra
    d.px[(24, 24)] = ("desgaste", GASTO, 1); d.px[(25, 25)] = ("desgaste", GASTO, 0)
    d.contornar()
    return d


# --- a luva com a braçadeira -------------------------------------------------------------------------------------
# Uma luva da mão direita, de costas: os dedos juntos (só as pontas separadas, por vincos curtos), o polegar à
# esquerda, o nó dos dedos aceso; o cano longo de braçadeira, de couro mais escuro, com a beira de cima virada e a
# amarração em zigue-zague (a do gibão) até a barra.
DEDOS = [((11, 12), 5), ((14, 15), 3), ((17, 18), 4), ((20, 21), 7)]  # (colunas, linha da ponta)
MAO = {y: (11, 21) for y in range(10, 17)} | {17: (12, 21), 18: (12, 20)}
POLEGAR = {10: (8, 9), 11: (7, 10), 12: (7, 10), 13: (8, 10), 14: (9, 10), 15: (10, 10)}
CANO = {19: (11, 21), 20: (11, 21), 21: (10, 22), 22: (10, 22), 23: (10, 22), 24: (10, 22), 25: (10, 22),
        26: (9, 23), 27: (9, 23), 28: (9, 23), 29: (9, 23)}


def luva():
    d = Desenho(N)
    tom_mao = lambda x, y: (5 if x < 14 else 4 if x < 18 else 3 if x < 20 else 2) + (1 if y == 10 and x < 18 else 0)
    faixas(d, MAO, "luva", COURO, tom_mao)
    for (c0, c1), topo in DEDOS:
        tons = {11: (5, 5), 14: (5, 4), 17: (4, 3), 20: (3, 2)}[c0]
        for y in range(topo, 10):
            for x, t in ((c0, tons[0]), (c1, tons[1])):
                d.px[(x, y)] = ("luva", COURO, t + (1 if y == topo else 0))
    for (_, e), topo_e in DEDOS[:-1]:                                   # os vincos entre os dedos, só nas pontas
        x = e + 1
        topo_d = next(t for (c, _), t in DEDOS if c == x + 1)
        for y in range(max(topo_e, topo_d) + 1, 10):
            d.px[(x, y)] = ("luva", COURO, 2)
    faixas(d, POLEGAR, "luva", COURO, lambda x, y: 6 if y == 10 else 5 if x < 9 else 4)
    d.px[(10, 13)] = ("luva", COURO, 2); d.px[(10, 14)] = ("luva", COURO, 2)   # a dobra entre o polegar e a mão
    # a braçadeira
    def tom_cano(x, y):
        if y == 19: return 6 if x < 16 else 4                          # a beira de cima, virada
        t = 5 if x < 13 else 4 if x < 17 else 3 if x < 21 else 2
        return t
    faixas(d, CANO, "bracadeira", BOTA, tom_cano)
    for x in range(9, 24):
        if (x, 29) in d.px: d.px[(x, 29)] = ("bracadeira", BORDA, 2 if x < 16 else 1)   # a barra
    for y in range(21, 29):                                             # a fenda e o cordão em zigue-zague
        d.px[(15, y)] = ("cordao", FORRO, 0); d.px[(16, y)] = ("cordao", FORRO, 0)
    for k, y in enumerate(range(21, 28)):
        d.px[(15 if k % 2 == 0 else 16, y)] = ("cordao", CORDAO, 2 if k % 2 == 0 else 1)
    d.px[(20, 25)] = ("desgaste", GASTO, 0); d.px[(21, 26)] = ("desgaste", GASTO, 1)   # o couro raspado
    d.contornar()
    return d


PECAS = {"capuz": (capuz, ["capa", "capuz", "interior", "borda", "cordao", "desgaste", "contorno"]),
         "luva": (luva, ["bracadeira", "luva", "cordao", "desgaste", "contorno"])}


def gravar(peca, pasta):
    fazer, ordem = PECAS[peca]
    cam = fazer().camadas()
    pasta.mkdir(parents=True, exist_ok=True)
    previa = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    for c in ordem:
        px = cam.get(c, {})
        texto = ";".join(f"{x},{y},{k}" for (x, y), k in sorted(px.items()))
        (pasta / f"{c}.txt").write_text(texto)
        (pasta / f"{c}.lua").write_text(f'return "{texto}"\n')
        for (x, y), k in px.items():
            previa.putpixel((x, y), tuple(int(k[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    previa.save(pasta / "previa.png")
    previa.resize((2 * N, 2 * N), Image.NEAREST).save(pasta / "previa-64.png")
    (pasta / "camadas.txt").write_text(",".join(ordem))
    return previa.getbbox(), sum(len(v) for v in cam.values()), len({k for v in cam.values() for k in v.values()})


if __name__ == "__main__":
    saida = pathlib.Path(sys.argv[1])
    for p in [a for a in sys.argv[2:] if a in PECAS] or list(PECAS):
        print(p, *gravar(p, saida / f"{p}-32"))
