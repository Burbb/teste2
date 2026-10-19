# a tocha (24 e 32): a tocha simples de aventureiro. O cabo de madeira em diagonal (de baixo à esquerda para cima à
# direita), a cabeça de pano enrolado e encerado na ponta (as voltas do pano em faixas) e a chama subindo reta, em
# línguas, mais quente no miolo. A mesma construção nos dois tamanhos (as medidas em frações do quadro).
# Rodada 2 (a chama refinada; o cabo e o pano aprovados não mudam; a rodada 1 em tocha_r1/): o calor segue o eixo
# curvo de cada língua, em vez de anéis em volta de um ponto (sem a faixa larga e sem o miolo quadrado), e as línguas
# têm alturas e curvas desiguais.
# O 16 (o chip, o aviso, o risco da escolha) é a mesma construção na grade de 16. A apagada (16 do risco "Sem luz" e
# 24 do topo sem tochas): o mesmo cabo e o mesmo pano, sem chama; a ponta de cima do pano queimada e um fio de fumaça
# subindo em dois trechos, sem contorno (o significado do sprite do jogo, a tocha que se apagou).
# Uso: python tocha.py <16|24|32> [silhueta|apagada]. Grava as listas por camada (tocha_<camada>_<N>.lua, ou
# tocha_apagada_<camada>_<N>.lua) e a prévia.
import sys, math
from PIL import Image
N = int(sys.argv[1]); ETAPA = sys.argv[2] if len(sys.argv) > 2 else "final"
R = {"m1": "3A2414", "m2": "5C3A20", "m3": "7E5430", "m4": "A07444",                  # a madeira
     "p1": "2A1E16", "p2": "45342A", "p3": "66503C", "p4": "8A7052",                  # o pano encerado
     "f1": "9A2408", "f2": "D4420E", "f3": "F47A16", "f4": "FFB22A", "f5": "FFE070", "f6": "FFF6C8",  # a chama
     "q1": "17120E", "q2": "2A1E16",                                                   # o pano queimado (apagada)
     "s1": "5E5A56", "s2": "8C8782", "s3": "B4AFA8",                                   # a fumaça (apagada)
     "O": "08080A"}
APAGADA = ETAPA == "apagada"
F = lambda v: v * N / 24
A = (F(4.2), F(21.8)); B = (F(15.6), F(10.4))                # o eixo: do pé do cabo ao alto da cabeça
L = math.hypot(B[0] - A[0], B[1] - A[1]); ux, uy = (B[0] - A[0]) / L, (B[1] - A[1]) / L
vx, vy = -uy, ux                                             # v < 0: o lado de cima e da esquerda (a luz)
CABO_W, CABEC_W, CABEC_U0 = F(1.05), F(2.9), 0.62            # meias-larguras; onde a cabeça começa (fração do eixo)
g, cam = {}, {}
def pinta(x, y, c, k):
    g[(x, y)] = c; cam[(x, y)] = k
for y in range(N):
    for x in range(N):
        px, py = x + 0.5, y + 0.5
        dx, dy = px - A[0], py - A[1]
        u, v = (dx * ux + dy * uy) / L, dx * vx + dy * vy
        if u < 0 or u > 1: continue
        if u >= CABEC_U0:                                     # a cabeça: o pano enrolado, as voltas em faixas
            w = CABEC_W * (0.86 if u < CABEC_U0 + 0.04 or u > 0.97 else 1)
            if abs(v) > w: continue
            if ETAPA == "silhueta": pinta(x, y, "p3", "pano"); continue
            volta = int((u - CABEC_U0) * L / F(1.6) + v / F(2.6) * 0.6) % 2      # as voltas, um pouco inclinadas
            lado = v / w                                       # -1 na luz, +1 na sombra
            t = "p4" if lado < -0.45 else "p3" if lado < 0.3 else "p2"
            if volta: t = {"p4": "p3", "p3": "p2", "p2": "p1"}[t]
            pinta(x, y, t, "pano")
        else:                                                  # o cabo
            if abs(v) > CABO_W: continue
            if ETAPA == "silhueta": pinta(x, y, "m3", "cabo"); continue
            pinta(x, y, "m4" if v < -0.35 * CABO_W else "m3" if v < 0.45 * CABO_W else "m2", "cabo")
# a chama: uma gota que sobe do alto da cabeça (a base redonda, a ponta em S) e duas línguas soltas, a da esquerda alta
# e curvada para fora, a da direita curta; o calor é mais forte perto do eixo de cada língua e embaixo, perto do pano
BX, BY = F(15.7), F(8.9)                                      # o meio da base redonda
def gota(px, py, bx, by, r, alto, ondula, voltas):
    """(distância normalizada ao eixo, altura de 0 na base a 1 na ponta) ou None fora."""
    if py >= by:
        d = math.hypot((px - bx) / r, (py - by) / (r * 0.9))
        return (d, 0.0) if d <= 1 else None
    t = (by - py) / alto
    if t > 1: return None
    cx = bx + ondula * math.sin(t * math.pi * voltas)
    meia = r * (1 - t) ** 1.05
    d = abs(px - cx) / meia if meia > 0 else 9
    return (d, t) if d <= 1 else None
GOTAS = [(BX, BY, F(4.1), F(8.6), F(-1.3), 1.15),             # a principal, a ponta em S virando à esquerda
         (BX - F(3.1), BY - F(1.5), F(1.4), F(5.0), F(-1.2), 0.6),   # a língua da esquerda: alta, abrindo para fora
         (BX + F(2.8), BY - F(2.2), F(1.15), F(2.6), F(0.7), 0.5)]   # a da direita: curta
for y in range(N):
    for x in range(N):
        px, py = x + 0.5, y + 0.5
        dentro = [(i, r) for i, gt in enumerate(GOTAS) if (r := gota(px, py, *gt))]
        if not dentro: continue
        if (x, y) in g and cam[(x, y)] == "pano":
            dx, dy = px - A[0], py - A[1]
            if (dx * ux + dy * uy) / L < 0.88: continue          # o pano fica na frente; só a beira de cima queima
        if ETAPA == "silhueta": pinta(x, y, "f3", "chama"); continue
        i, (d, t) = dentro[0]                                 # a principal prevalece onde as línguas a cruzam
        if i == 0:                                            # o calor pelo eixo da língua, mais forte embaixo
            h = (1 - d) ** 0.9 * (1.05 - 0.95 * t)
            c = "f6" if h > 0.66 else "f5" if h > 0.47 else "f4" if h > 0.3 else "f3" if h > 0.16 else "f2" if h > 0.06 else "f1"
        else:
            h = (1 - d) * (1 - t)
            c = "f4" if h > 0.5 else "f3" if h > 0.22 else "f2"
        pinta(x, y, c, "chama")
if APAGADA:                                                   # sem chama: a ponta de cima do pano queimada
    for (x, y) in [k for k, v in cam.items() if v == "chama"]:
        del g[(x, y)], cam[(x, y)]
    for (x, y) in [k for k, v in cam.items() if v == "pano"]:
        dx, dy = x + 0.5 - A[0], y + 0.5 - A[1]
        u = (dx * ux + dy * uy) / L
        if u > 0.8: pinta(x, y, "q1" if u > 0.9 else "q2", "queimado")
chama = {k for k, v in cam.items() if v == "chama"}
for (x, y) in list(chama):                                    # a beira de cima e dos lados: um tom mais escuro
    if ETAPA != "silhueta" and y < BY and any((x + a, y + b) not in g for a, b in ((1, 0), (-1, 0), (0, -1))):
        g[(x, y)] = {"f6": "f5", "f5": "f4", "f4": "f3", "f3": "f2", "f2": "f2", "f1": "f1"}[g[(x, y)]]
forma = set(g)
for y in range(N):
    for x in range(N):
        if (x, y) not in g and any((x + a, y + b) in forma for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            pinta(x, y, "O", "contorno")
if APAGADA:                                                   # a fumaça: dois fios curtos e curvos, com um vão entre
    for t0, t1, tom in ((0.0, 0.36, ("s3", "s2")), (0.6, 0.92, ("s2", "s1"))):   # eles, mais fracos em cima; sem contorno
        for k in range(40):
            t = t0 + (t1 - t0) * k / 39
            x = int(B[0] + F(0.6) + F(1.2) * math.sin(t * math.pi * 2.6))
            y = int(B[1] - F(2.6) - t * F(8.2))
            if 0 <= x < N and 0 <= y < N and (x, y) not in g:
                pinta(x, y, tom[0] if t - t0 < (t1 - t0) / 2 else tom[1], "fumaca")
im = Image.new("RGBA", (N, N))
for (x, y), c in g.items(): im.putpixel((x, y), tuple(int(R[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
nome = "tocha_apagada" if APAGADA else "tocha"
im.save(f"{nome}_{'final' if APAGADA else ETAPA}_{N}.png")
for k in sorted(set(cam.values())):
    open(f"{nome}_{k}_{N}.lua", "w").write('return "' + ";".join(f"{x},{y},{R[g[(x, y)]]}" for (x, y) in sorted(g) if cam[(x, y)] == k) + '"\n')
print(N, sorted(set(cam.values())), im.getbbox())
sim = {"m1": "a", "m2": "b", "m3": "c", "m4": "d", "p1": "1", "p2": "2", "p3": "3", "p4": "4", "f1": "R", "f2": "r", "f3": "o", "f4": "y", "f5": "Y", "f6": "W", "q1": "Q", "q2": "q", "s1": ":", "s2": "+", "s3": "*", "O": "#"}
print("".join("\n" + "".join(sim[g[(x, y)]] if (x, y) in g else "." for x in range(N)) for y in range(N)))
