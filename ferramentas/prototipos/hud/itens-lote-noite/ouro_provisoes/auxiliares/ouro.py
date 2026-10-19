# o Ouro (24): uma pilha de moedas vista um pouco de cima (a de cima de face, as laterais empilhadas) e uma moeda
# apoiada na frente, à esquerda. Etapas: python ouro.py silhueta | final. Grava as listas por camada e a prévia.
import sys, math
from PIL import Image
N = 24
ETAPA = sys.argv[1] if len(sys.argv) > 1 else "final"
R = {"1": "3A1C04", "2": "6E3C08", "3": "A86410", "4": "D69018", "5": "F0B828", "6": "FFDC5A", "7": "FFF0A8", "O": "08080A"}
g, cam = {}, {}
def pinta(x, y, c, camada):
    if 0 <= x < N and 0 <= y < N: g[(x, y)] = c; cam[(x, y)] = camada
# a pilha: quatro moedas (cilindros de raio 6,5 e 2 px de altura), centro em x 13,5; a face de cima em y 7
CX, RX, RY, TOPO, MOEDAS, ALT = 13.5, 6.6, 2.6, 7.0, 4, 2
base = TOPO + MOEDAS * ALT
for y in range(N):
    for x in range(N):
        px, py = x + 0.5, y + 0.5
        dx = (px - CX) / RX
        if abs(dx) > 1: continue
        meia = RY * math.sqrt(1 - dx * dx)
        if TOPO - meia <= py <= TOPO + meia:                        # a face de cima
            if ETAPA == "silhueta": pinta(x, y, "4", "topo"); continue
            u = (px - CX) / RX + (py - TOPO) / RY * 0.6
            pinta(x, y, "6" if u < -0.5 else "5" if u < 0.45 else "4", "topo")
        elif TOPO + meia < py <= base + meia:                       # as laterais
            if ETAPA == "silhueta": pinta(x, y, "4", "pilha"); continue
            k = (py - meia - TOPO)                                  # quanto desceu desde a beira de cima
            sep = (k % ALT) < 1 and k > 0.5                         # a junta entre duas moedas
            c = "5" if dx < -0.45 else "4" if dx < 0.25 else "3" if dx < 0.75 else "2"
            if sep: c = {"5": "3", "4": "3", "3": "2", "2": "1"}[c]
            pinta(x, y, c, "pilha")
# a moeda apoiada na frente, à esquerda: de pé e um pouco virada (uma elipse alta), com a beira e a face
MX, MY, MRX, MRY = 7.2, 15.6, 4.7, 5.0
for y in range(N):
    for x in range(N):
        px, py = x + 0.5, y + 0.5
        r = math.hypot((px - MX) / MRX, (py - MY) / MRY)
        if r > 1: continue
        if ETAPA == "silhueta": pinta(x, y, "5", "moeda"); continue
        luz = -((px - MX) / MRX + (py - MY) / MRY)
        if r > 0.78: c = "6" if luz > 0.2 else "5" if luz > -0.5 else "4"       # a beira em relevo, clara
        elif r > 0.58: c = "2" if luz > -0.2 else "3"                             # o sulco do anel, fundo
        else: c = "6" if luz > 0.75 else "5" if luz > -0.6 else "4"               # a face
        pinta(x, y, c, "moeda")
forma = set(g)
for y in range(N):
    for x in range(N):
        if (x, y) not in g and any((x + a, y + b) in forma for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            pinta(x, y, "O", "contorno")
# o contorno também entre a moeda da frente e a pilha (a moeda na frente se separa)
for (x, y) in list(forma):
    if cam[(x, y)] != "moeda" and any(cam.get((x + a, y + b)) == "moeda" for a, b in ((1, 0), (0, 1), (-1, 0), (0, -1))) and x >= 6:
        pinta(x, y, "O", "contorno")
im = Image.new("RGBA", (N, N))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(R[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save(f"ouro_{ETAPA}.png")
for camada in set(cam.values()):
    open(f"ouro_{camada}.lua", "w").write('return "' + ";".join(f"{x},{y},{R[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == camada) + '"\n')
print(sorted(set(cam.values())))
print("".join("\n" + "".join(g.get((x, y), ".") for x in range(N)) for y in range(N)))
