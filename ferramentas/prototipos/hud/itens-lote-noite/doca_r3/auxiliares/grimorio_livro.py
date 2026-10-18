# o Grimório, rodada 3: o livro como objeto 3D simples numa projeção só (a da referência principal: girado, a borda de
# cima subindo para a direita; à vista a capa da frente, a lombada à esquerda e as folhas embaixo, entre as capas).
# Coordenadas do livro: u da lombada para a beira, v de cima para baixo, w da capa da frente para a de trás.
#   python livro.py <36|32> [construcao]
import math, sys, json
from grimorio_ver import salvar
n = int(sys.argv[1]); SO_CONSTRUCAO = len(sys.argv) > 2
k = n / 36
A = math.radians(-16)
U = (math.cos(A), math.sin(A)); V = (-math.sin(A), math.cos(A))
D = (-0.50 * k, 0.86 * k)                 # a profundidade (por unidade de w): para baixo e para a esquerda
LARG, ALT, ESP = 19.0 * k, 22.5 * k, 6.0  # a capa (u, v) e a espessura (w, em unidades de D)
CAPA = 1.1                                # a espessura de cada capa (w)
RECUO = 0.9 * k                           # as folhas recuadas das beiras das capas (a "esquadria")
BOJO = 1.8 * k                            # o quanto a lombada redonda sai para a esquerda
O = (9.6 * k, 5.6 * k)
def tela(u, v, w):
    return (O[0] + u * U[0] + v * V[0] + w * D[0], O[1] + u * U[1] + v * V[1] + w * D[1])
def plano(sx, sy, w):                      # (u, v) do ponto da tela num plano de w fixo
    px, py = sx - O[0] - w * D[0], sy - O[1] - w * D[1]
    return px * U[0] + py * U[1], px * V[0] + py * V[1]
def baixo(sx, sy, v):                      # (u, w) do ponto da tela na face de baixo (v fixo)
    # sx = O + uU + vV + wD -> resolve u, w
    px, py = sx - O[0] - v * V[0], sy - O[1] - v * V[1]
    det = U[0] * D[1] - U[1] * D[0]
    return (px * D[1] - py * D[0]) / det, (U[0] * py - U[1] * px) / det
def bojo(w): return BOJO * math.sin(math.pi * min(max(w / ESP, 0), 1))
def lombada(sx, sy):                       # (v, w) na lombada redonda (u = -bojo(w)), ou None
    melhor = None
    for i in range(121):
        w = ESP * i / 120
        u, v = plano(sx, sy, w)
        if abs(u + bojo(w)) < 0.35 and 0 <= v <= ALT and (melhor is None or abs(u + bojo(w)) < melhor[0]):
            melhor = (abs(u + bojo(w)), v, w)
    return melhor and melhor[1:]
def face(sx, sy):
    """A face mais da frente no ponto da tela: (nome, parâmetros)."""
    u, v = plano(sx, sy, 0)
    if 0 <= u <= LARG and 0 <= v <= ALT: return ("frente", u, v)
    # a beira de baixo da capa da frente (a espessura dela)
    u, w = baixo(sx, sy, ALT)
    if 0 <= u <= LARG and 0 <= w <= CAPA: return ("beira_frente", u, w)
    # as folhas: a face de baixo do bloco, recuada (entre as capas)
    u, w = baixo(sx, sy, ALT - RECUO)
    if 0 <= u <= LARG - RECUO and CAPA <= w <= ESP - CAPA: return ("folhas", u, w)
    l = lombada(sx, sy)
    if l: return ("lombada", l[0], l[1])
    # a contracapa: a beira de baixo dela e o que aparece por trás das folhas
    u, w = baixo(sx, sy, ALT)
    if 0 <= u <= LARG and ESP - CAPA <= w <= ESP: return ("beira_tras", u, w)
    u, v = plano(sx, sy, ESP - CAPA)
    if 0 <= u <= LARG and 0 <= v <= ALT: return ("tras", u, v)
    return None
g = {}; cam = {}
SS = 4
for y in range(n):
    for x in range(n):
        votos = {}
        for i in range(SS):
            for j in range(SS):
                f = face(x + (i + 0.5) / SS, y + (j + 0.5) / SS)
                nome = f[0] if f else None
                votos[nome] = votos.get(nome, 0) + 1
        nome = max(votos, key=votos.get)
        if nome is None: continue
        f = face(x + 0.5, y + 0.5) or next(face(x + (i + .5) / SS, y + (j + .5) / SS) for i in range(SS) for j in range(SS) if face(x + (i + .5) / SS, y + (j + .5) / SS) and face(x + (i + .5) / SS, y + (j + .5) / SS)[0] == nome)
        if f[0] != nome:
            f = next(ff for ff in (face(x + (i + .5) / SS, y + (j + .5) / SS) for i in range(SS) for j in range(SS)) if ff and ff[0] == nome)
        _, p1, p2 = f
        if nome == "frente":     # poucos planos: o alto e o lado da lombada claros, a beira oposta na sombra
            t = p1 / LARG * 0.8 + p2 / ALT * 0.7
            c = "5" if t < 0.45 else "4" if t < 1.05 else "3"
            if p1 < 0.9 * k: c = "2"                                  # o sulco entre a lombada e a capa
            elif p1 < 2.0 * k: c = "6"                                # a quina da capa junto do sulco, acesa
            if p1 > LARG - 1.0 * k or p2 > ALT - 1.0 * k: c = "2"     # a beira oposta
        elif nome == "beira_frente": c = "4" if p1 < LARG * 0.5 else "3"   # a espessura da capa, acesa embaixo
        elif nome == "folhas":   # as linhas das folhas correm ao longo da lombada (u)
            c = "s" if int(p2 * 1.6) % 2 == 0 else "q"
            if p1 > LARG - RECUO - 1.2 * k: c = "p"
        elif nome == "lombada":  # o dorso redondo: a luz no meio de cima
            t = p2 / ESP
            c = "3" if t < 0.15 else "4" if t < 0.45 else "2" if t < 0.8 else "1"
        elif nome == "beira_tras": c = "2"
        else: c = "2"
        camada = None
        if not SO_CONSTRUCAO:
            if nome == "lombada":   # as nervuras: faixas em relevo atravessando o dorso (acesas em cima, sombra embaixo)
                for vb in (ALT * 0.24, ALT * 0.72):
                    if 0 <= p1 - vb < 0.9 * k: c = "5"
                    elif 0.9 * k <= p1 - vb < 1.7 * k: c = "1"
            if nome == "frente":
                cu, cv = (2.0 * k + LARG) / 2 + 0.2 * k, ALT * 0.47       # o centro do plano útil da capa
                du, dv = p1 - cu, p2 - cv; r = math.hypot(du, dv)
                # a moldura em baixo relevo, a 2,4 das beiras (o sulco escuro e a beira acesa por dentro)
                m = min(p1 - 2.6 * k, LARG - 1.6 * k - p1, p2 - 1.8 * k, ALT - 1.8 * k - p2)
                if -0.45 < m <= 0.35: c = "2"
                elif 0.35 < m <= 0.9 and (p1 - 2.6 * k < 1.0 * k or p2 - 1.8 * k < 1.0 * k): c = "6"
                # o emblema: o halo violeta, o anel de latão, a estrela de quatro pontas luminosa
                R = 5.0 * k
                astro = (abs(du) / R) ** 0.62 + (abs(dv) / R) ** 0.62    # a estrela de quatro pontas (astroide)
                if r < R * 0.9 and c != "2": c = "6"; camada = "emblema"   # o halo: o couro aceso em volta
                if astro < 1.0:
                    c = "e" if astro < 0.5 else "d" if (du + dv) < 0.6 * k else "c"; camada = "emblema"
                # os cravos de latão nos cantos da moldura
                for (su, sv) in ((3.6 * k, 2.8 * k), (LARG - 2.6 * k, 2.8 * k), (3.6 * k, ALT - 2.8 * k), (LARG - 2.6 * k, ALT - 2.8 * k)):
                    if math.hypot(p1 - su, p2 - sv) < 0.75 * k: c = "d"; camada = "cravos"
        g[(x, y)] = c; cam[(x, y)] = camada or {"frente": "capa", "beira_frente": "capa", "folhas": "folhas", "lombada": "lombada",
                                     "beira_tras": "contracapa", "tras": "contracapa"}[nome]
if not SO_CONSTRUCAO:
    # a fita do marcador: sai das folhas, perto da beira da direita, e cai um pouco abaixo do livro
    fx, fy = tela(LARG * 0.66, ALT - RECUO, ESP * 0.55)
    x0 = int(fx)
    for dy in range(0, int(4 * k) + 3):
        for dx, c in ((0, "T"), (1, "S")):
            p = (x0 + dx, int(fy) + dy)
            if dy == int(4 * k) + 2 and dx == 1: continue           # a ponta em V
            g[p] = c if dy > 0 else "R"; cam[p] = "fita"
salvar(g, n, f"l{n}{'c' if SO_CONSTRUCAO else ''}.png")
json.dump({f"{x},{y}": c for (x, y), c in cam.items()}, open(f"l{n}.cam.json", "w"))
