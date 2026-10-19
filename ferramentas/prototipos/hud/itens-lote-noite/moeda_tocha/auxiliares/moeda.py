# a moeda avulsa (16 e 32): uma moeda só, de frente, com a espessura aparecendo embaixo à direita (a luz vem de cima e
# da esquerda); a mesma família da pilha aprovada (moedas-24): o mesmo ouro, a beira em relevo, o sulco do anel e a face.
# Uso: python moeda.py <16|32> [silhueta]. Grava as listas por camada (moeda_<camada>_<N>.lua) e a prévia.
import sys, math
from PIL import Image
N = int(sys.argv[1]); ETAPA = sys.argv[2] if len(sys.argv) > 2 else "final"
K = N / 16
R = {"1": "3A1C04", "2": "6E3C08", "3": "A86410", "4": "D69018", "5": "F0B828", "6": "FFDC5A", "O": "08080A"}
T = 1 if N == 16 else 2                                       # a espessura, para baixo e para a direita
CX = CY = (N - T) / 2; RAIO = 5.9 * K                         # a face, centrada com a espessura
g, cam = {}, {}
def pinta(x, y, c, k):
    g[(x, y)] = c; cam[(x, y)] = k
def r_de(px, py, ox=0, oy=0):
    return math.hypot(px - CX - ox, py - CY - oy) / RAIO
for y in range(N):                                            # a espessura: a face repetida T px abaixo e à direita
    for x in range(N):
        px, py = x + 0.5, y + 0.5
        if r_de(px, py) <= 1: continue
        if any(r_de(px, py, d, d) <= 1 for d in range(1, T + 1)):
            if ETAPA == "silhueta": pinta(x, y, "3", "espessura"); continue
            ang = math.atan2(py - CY, px - CX)                # a lateral: mais clara embaixo, escura à direita
            pinta(x, y, "3" if ang > math.pi * 0.5 else "2" if ang > -0.3 else "2", "espessura")
ANEL = (0.58, 0.78)                                           # as faixas da moeda da frente da pilha
for y in range(N):
    for x in range(N):
        px, py = x + 0.5, y + 0.5
        r = r_de(px, py)
        if r > 1: continue
        if ETAPA == "silhueta": pinta(x, y, "5", "face"); continue
        luz = -((px - CX) + (py - CY)) / RAIO                # de cima e da esquerda
        if r > ANEL[1]: pinta(x, y, "6" if luz > 0.2 else "5" if luz > -0.5 else "4", "beira")   # em relevo, clara
        elif r > ANEL[0]: pinta(x, y, "2" if luz > -0.2 else "3", "anel")                     # o sulco, fundo
        else: pinta(x, y, "6" if luz > 0.75 else "5" if luz > -0.6 else "4", "face")         # as regras da pilha
forma = set(g)
for y in range(N):
    for x in range(N):
        if (x, y) not in g and any((x + a, y + b) in forma for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            pinta(x, y, "O", "contorno")
im = Image.new("RGBA", (N, N))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(R[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
im.save(f"moeda_{ETAPA}_{N}.png")
for k in sorted(set(cam.values())):
    open(f"moeda_{k}_{N}.lua", "w").write('return "' + ";".join(f"{x},{y},{R[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == k) + '"\n')
print(N, sorted(set(cam.values())), im.getbbox())
print("".join("\n" + "".join(g.get((x, y), ".") for x in range(N)) for y in range(N)))
