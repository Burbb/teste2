# o Vigor (20): o punho cerrado na frente de uma chama (a ideia da referência do Jean, sem o coração; a construção
# do punho pelas referências de punho dele: em três quartos, os três dedos com as pontas em alturas diferentes, o
# polegar dobrado por cima à direita, o pulso mais estreito). O punho é desenhado pixel a pixel, com o contorno
# dentro da grade (os entalhes entre os nós); a chama, laranja e funda, fica atrás, nas cores do vigor.
import math
from PIL import Image
RAMPA = {"c2": "9A2C0A", "c3": "D24A12", "c4": "F57A20", "c5": "FFA838", "c6": "FFD266",
         "K": "6A3410", "s": "C2802E", "m": "EEB45C", "l": "FFE2A0", "O": "08080A"}
PUNHO = [  # 20 colunas, linhas 5 a 19
    ".......OO.OO........",   # 5  os nós do meio, os mais altos
    "....OOOllOlmOOO.....",   # 6
    "...OllKlmKlmKllO....",   # 7  os quatro dedos, separados por linhas verticais
    "...OlmKlmKlmKlmO....",   # 8
    "...OmmKmmKmmKmsO....",   # 9
    "...OKKKKKKKKKmsO....",   # 10 o polegar atravessado, por cima dos três primeiros dedos
    "...OllllllllKmsO....",   # 11
    "...OmmmmmmmmmmsO....",   # 12
    "...OlmmmmmmmmssO....",   # 13
    "....OlmmmmmmmsO.....",   # 14
    ".....OlmmmmmssO.....",   # 15 o pulso
    "......OlmmmmsO......",   # 16
    "......OlmmmmmsO.....",   # 17 o antebraço abre para baixo
    ".....OllmmmmmsO.....",   # 18
    ".....OlmmmmmmmsO....",   # 19
]
g, cam = {}, {}
for j, linha in enumerate(PUNHO):
    for x, ch in enumerate(linha):
        if ch != ".": g[(x, 5 + j)] = ch; cam[(x, 5 + j)] = "contorno" if ch == "O" else "punho"
dentro_punho = {(x, y) for (x, y) in g}
for y in range(5, 20):   # o vão entre o contorno do punho e a beira (por dentro dele) não é chama
    xs = [x for x in range(20) if (x, y) in g]
    for x in range(min(xs), max(xs) + 1): dentro_punho.add((x, y))
# a chama atrás: um corpo em volta da parte de cima do punho e três línguas (a do meio mais alta, curvando)
def chama(px, py):          # as línguas saem de cima dos nós (o punho em chamas), sem envolver os lados
    if py > 7.5: return False
    for cx, topo, larg, curva in ((5.2, 1.8, 1.7, -1.0), (9.6, 0.0, 2.1, 0.8), (14.0, 1.2, 1.7, 1.2)):
        if topo <= py:
            t = min((py - topo) / (6.5 - topo), 1)
            if abs(px - cx - curva * (1 - t) ** 2) <= larg * t ** 0.7: return True
    return False
for y in range(20):
    for x in range(20):
        if (x, y) in dentro_punho or not chama(x + 0.5, y + 0.5): continue
        c = "c5" if y >= 5 else "c4" if y >= 3 else "c3"     # mais quente junto dos nós
        if y >= 3 and abs(x + 0.5 - (5.2, 9.6, 14.0)[min(range(3), key=lambda k: abs(x + 0.5 - (5.2, 9.6, 14.0)[k]))]) < 0.8: c = "c6" if y >= 4 else "c5"   # o miolo de cada língua
        g[(x, y)] = c; cam[(x, y)] = "chama"
forma = {k for k, v in g.items() if v != "O"}
for y in range(20):
    for x in range(20):
        if (x, y) not in g and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            g[(x, y)] = "O"; cam[(x, y)] = "contorno"
im = Image.new("RGBA", (20, 20))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(RAMPA[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save("vigor20.png")
for camada in ("chama", "punho", "contorno"):
    txt = ";".join(f"{x},{y},{RAMPA[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == camada)
    open(f"vigor_{camada}.lua", "w").write(f'return "{txt}"\n')
leg = {"c2": "2", "c3": "3", "c4": "4", "c5": "5", "c6": "6"}
print("".join("\n" + "".join(leg.get(g.get((x, y), "."), g.get((x, y), ".")) for x in range(20)) for y in range(20)))
