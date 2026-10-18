# o Bestiário (36): o crânio de uma criatura com chifres, de frente, um pouco de cima. Não é caveira humana: as maçãs
# largas, as têmporas afundadas, o focinho que afina para baixo, as presas, os chifres grossos em C. A luz de cima e da
# esquerda no osso, em poucos planos; as cavidades (órbitas, narinas) fundas e bem separadas.
import math, sys, json
from ver import contorno, imagem
n = int(sys.argv[1]); k = n / 36
CX = 18.0
def meia_cabeca(y):        # a meia-largura do crânio em cada altura (unidades do 36)
    if y < 8.0: return None
    if y < 11.5: return 4.6 + (y - 8.0) * 1.15          # o alto da cabeça, arredondado
    if y < 16.0: return 8.6                             # a testa e as órbitas
    if y < 17.5: return 8.6 - (y - 16.0) * 0.5          # as têmporas, afundadas
    if y < 20.5: return 8.0 + (y - 17.5) * 0.85         # as maçãs, que abrem
    if y < 22.0: return 10.5 - (y - 20.5) * 2.0         # e fecham no focinho
    if y <= 25.6: return 7.4 - (y - 22.0) * 0.3         # o focinho, afinando até a boca
    if y <= 28.4: return 5.6                            # a arcada de cima (os dentes), um degrau para dentro
    if y <= 30.6: return 5.1                            # os dentes de baixo
    if y <= 33.6: return 5.1 - ((y - 30.6) / 3.0) ** 2 * 2.8   # o queixo, arredondado
    return None
def chifre(px, py, lado):
    melhor = None
    for i in range(61):
        t = i / 60
        cx = CX + lado * (7.0 + 8.6 * math.sin(min(t * 1.6, math.pi / 2)) - 2.4 * t ** 3)
        cy = 11.0 - 10.2 * t ** 1.5
        esp = 3.0 * (1 - t) ** 0.8 + 0.4
        d = math.hypot(px - cx, py - cy)
        if d <= esp and (melhor is None or d / esp < melhor[0]): melhor = (d / esp, t, (px - cx) / esp, (py - cy) / esp)
    return melhor
g = {}; cam = {}
for y in range(n):
    for x in range(n):
        px, py = (x + 0.5) / k, (y + 0.5) / k
        dx = px - CX
        w = meia_cabeca(py)
        if w is not None and abs(dx) <= w:
            u = dx / w
            # os planos: a testa acesa em cima à esquerda, o meio, o lado de trás escuro; o focinho na frente aceso
            if py < 16: c = "V" if u < -0.3 else "U" if u < 0.25 else "T" if u < 0.7 else "S"
            elif py < 21.5: c = "U" if u < -0.25 else "T" if u < 0.45 else "S"
            else: c = "U" if u < -0.15 else "T" if u < 0.4 else "S"
            if 24.8 < py < 25.6: c = {"V": "U", "U": "T", "T": "S", "S": "R"}[c]
            if abs(u) > 0.86: c = "S" if u < 0 else "R"                         # a volta do osso
            if 16.0 <= py < 18.0 and abs(u) > 0.7: c = "R"                       # a têmpora afundada
            if abs(dx + 0.3) < 0.55 and 8.5 < py < 13.0: c = "V"                # a crista da testa
            for lado in (-1, 1):
                ox, oy = CX + lado * 4.5, 15.2
                rx, ry = 3.2, 2.3
                incl = (px - ox) * lado * -0.48                                  # o canto de fora sobe
                e = ((px - ox) / rx) ** 2 + ((py - oy - incl) / ry) ** 2
                if e <= 1: c = "W" if (e < 0.6 or py > oy + incl - 0.3) else "Q"
                elif e <= 1.7 and py < oy + incl: c = "V" if lado < 0 else "U"   # o sobrolho, aceso por cima
            # a cavidade do nariz: um V invertido
            if 21.8 < py < 25.6 and abs(dx + 0.2) < (py - 21.8) * 0.55 + 0.4: c = "W" if py > 22.6 else "Q"
            # a boca: os dentes de cima e os de baixo, separados por fendas escuras, e a linha escura entre as arcadas
            if 25.6 < py < 30.6:
                # os dentes na grade do tamanho: 2 px de dente, 1 de fenda, simétricos em volta do meio
                col = x - int(CX * k)
                dente = col % 3 != 1
                if 28.4 <= py < 29.4: c = "W"                                   # a linha da boca
                elif not dente or abs(u) > 0.88: c = "Q"
                else: c = ("V" if u < 0 else "U") if py < 27.6 else ("U" if u < 0 else "T") if py < 28.4 else ("U" if u < 0 else "T")
            if py >= 30.6: c = "T" if u < -0.1 else "S" if u < 0.55 else "R"   # o queixo
            g[(x, y)] = c; cam[(x, y)] = "cranio"
        for lado in (-1, 1):
            r = chifre(px, py, lado)
            if r and (x, y) not in g:
                d, t, ox, oy = r
                luz = -(ox * 0.72 + oy * 0.69)
                c = "k" if luz > 0.3 else "Z" if luz > -0.25 else "Y"
                if int(t * 10) % 2 == 1 and t < 0.7: c = {"k": "Z", "Z": "Y", "Y": "X"}[c]   # os anéis
                if t > 0.88: c = "Z" if luz > 0 else "Y"
                g[(x, y)] = c; cam[(x, y)] = "chifres"
h = contorno(g, n)
for p, v in h.items():
    if v == "O": cam[p] = "contorno"
imagem(h, n, f"b{n}.png")
json.dump({f"{x},{y}": c for (x, y), c in cam.items()}, open(f"b{n}.cam.json", "w"))
