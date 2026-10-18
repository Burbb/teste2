# o Sair (36): o arco de pedra de uma passagem, de frente e um pouco de lado, e a seta quente saindo dela para a
# direita. A profundidade: o vão escuro, mais fundo em cima; a parede de dentro (a espessura do arco) acesa do lado da
# direita; a soleira embaixo. A seta tem contorno próprio e passa por cima da beira do arco.
import math, sys, json
from ver import contorno, imagem
n = int(sys.argv[1]); k = n / 36
CX, CY = 12.6, 13.0                    # o centro do arco
RE, RI = 10.4, 6.2                     # o raio de fora e o do vão
BASE = 33.0
g = {}; cam = {}
for y in range(n):
    for x in range(n):
        px, py = (x + 0.5) / k, (y + 0.5) / k
        dx, dy = px - CX, py - CY
        fora = (abs(dx) <= RE and py <= BASE) and (py >= CY or math.hypot(dx, dy) <= RE)
        vao = (abs(dx) <= RI and py <= BASE - 1.0) and (py >= CY or math.hypot(dx, dy) <= RI)
        if not fora: continue
        if vao:
            # o vão: a parede de dentro à direita (a espessura do arco, acesa), o fundo escuro, mais fundo em cima
            prof = RI - dx if py >= CY else RI - math.hypot(dx, dy)          # quanto falta até a face do arco
            if dx > 1.5 and prof < 2.2:                                        # a parede de dentro, à direita
                c = "&" if prof < 1.0 else "%"                                 # clara junto da face, mais funda escura
                if py > BASE - 3.0: c = "$"
            else: c = "!" if py < BASE - 3.0 else "#"                          # o fundo escuro; o chão de pedra
            g[(x, y)] = c; cam[(x, y)] = "passagem"
            continue
        # a pedra do arco, em blocos: as aduelas em volta do vão (linhas para o centro), as fiadas nos lados
        if py < CY:
            ang = math.degrees(math.atan2(-dy, dx)) % 180
            junta = min(abs(ang - a) for a in (30, 60, 90, 120, 150)) < 4.5
        else:
            junta = int((py - CY) // 4.0) != int((py - CY + 0.9) // 4.0) or (abs(dx) > RI + 0.2 and abs(abs(dx) - (RI + RE) / 2) < 0.45 and int((py - CY) // 4.0) % 2 == 0)
        luz = -(dx / RE) * 0.7 - (dy / RE) * 0.7
        c = "@" if luz > 0.55 else "&" if luz > 0.1 else "%" if luz > -0.4 else "$"
        if junta: c = "#" if c in "@&" else "!"
        if abs(math.hypot(dx, dy) - RI) < 1.0 and py < CY or (abs(abs(dx) - RI) < 1.0 and py >= CY):
            c = "&" if dx < 0 else c                                          # a quina do vão, acesa à esquerda
        if dx > 0 and (abs(dx) - RI < 0.9 if py >= CY else math.hypot(dx, dy) - RI < 0.9): c = "!"   # a junta da quina com a parede
        if py > BASE - 1.0: c = "$" if dx < 0 else "#"                         # a soleira
        g[(x, y)] = c; cam[(x, y)] = "arco"
base = contorno(dict(g), n)
# a seta: o cabo saindo do vão e a ponta à direita, fora do arco
s = {}
for y in range(n):
    for x in range(n):
        px, py = (x + 0.5) / k, (y + 0.5) / k
        cabo = 15.0 <= px <= 25.0 and abs(py - 22.0) <= 2.4
        ponta = 24.0 <= px <= 33.6 and abs(py - 22.0) <= (33.6 - px) * 0.62
        if cabo or ponta:
            v = py - 22.0
            s[(x, y)] = "9" if v < -1.2 and px < 30 else "8" if v < 0.6 else "7"
seta = contorno(s, n)
h = dict(base)
for p, v in seta.items():
    h[p] = v; cam[p] = "seta" if v != "O" else "contorno"
for p, v in h.items():
    if v == "O" and p not in seta: cam[p] = "contorno"
imagem(h, n, f"x{n}.png")
json.dump({f"{x},{y}": c for (x, y), c in cam.items()}, open(f"x{n}.cam.json", "w"))
