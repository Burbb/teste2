# A espada e a maça do Guerreiro (o começo do remake do ferro, proposta de 19/10/2026): na diagonal da família (o pomo
# embaixo à esquerda, a ponta em cima à direita), com o ferro do machado aprovado (o cinza neutro), o latão do escudo e
# a madeira do cabo do machado; a luz de cima e da esquerda (a metade de cima de cada peça na luz). As medidas estão num
# sistema que segue a arma: u ao longo do eixo (do pomo à ponta), v através dele (- em cima/à esquerda, + embaixo/à
# direita), no quadro de 32. Primeiro o 32; o 64 é o 32 ampliado 2x (a política da skill); 40 e 48 depois da aprovação.
# Uso: python desenho.py <espada|maca> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas

PECA = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {
    "f": ["#0e0f11", "#1a1c20", "#282b31", "#383c44", "#4c5159", "#646a73", "#848b94", "#b0b6bd", "#e4e8ec"],   # o ferro (o do machado)
    "o": ["#26170a", "#40270c", "#623c12", "#8a571b", "#ae7526", "#cf9737", "#e9bb5c", "#f8dc94"],              # o latão (o do escudo)
    "m": ["#20150c", "#3a2716", "#583c21", "#77532e", "#946b3c", "#ae844e", "#c49d66", "#d8b886"],              # o freixo (o do machado)
    "k": ["#140b09", "#251412", "#3a1f1a", "#522c23", "#6b3b2d", "#86503c"],                                    # o couro (o do arco)
}
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
x32, y32 = X / K, Y / K
O = np.array([4.4, 27.6])                                    # a origem: o centro do pomo
D = np.array([1.0, -1.0]) / np.sqrt(2); Pp = np.array([1.0, 1.0]) / np.sqrt(2)
U = (x32 - O[0]) * D[0] + (y32 - O[1]) * D[1]                # ao longo da arma
V = (x32 - O[0]) * Pp[0] + (y32 - O[1]) * Pp[1]              # através (- em cima, na luz)


def pinta(onde, m, t, c):
    mat[onde] = m; tom[onde] = t if np.isscalar(t) else t[onde]; cam[onde] = c


def poligono_uv(pts):
    """Os pixels dentro do polígono dado em (u, v)."""
    xy = [tuple(O + u * D + v * Pp) for u, v in pts]
    dentro = np.zeros((N, N), bool)
    n = len(xy)
    for i in range(n):
        (xa, ya), (xb, yb) = xy[i], xy[(i + 1) % n]
        cruza = ((ya > y32) != (yb > y32)) & (x32 < (xb - xa) * (y32 - ya) / ((yb - ya) or 1e-9) + xa)
        dentro ^= cruza
    return dentro


def disco(u, v, r):
    c = O + u * D + v * Pp
    return np.hypot(x32 - c[0], y32 - c[1]) * K <= max(r * K, 0.6)


def faixa_uv(u0, u1, meia):
    return (U >= u0) & (U <= u1) & (np.abs(V) * K <= max(meia * K, 0.5))


if PECA == "espada":
    # A espada de uma mão: a lâmina larga de dois gumes, em dois planos (a metade de cima na luz, a de baixo na sombra),
    # com o sulco no plano claro e a ponta afilada; a guarda de latão reta, as pontas curvadas para a lâmina; a empunhadura de
    # couro com as voltas; o pomo de latão.
    def larg(u):
        return np.interp(u, [8.2, 10.0, 22.0, 27.6, 31.2, 32.4], [2.35, 2.3, 2.05, 1.7, 0.6, 0.0])
    us = np.linspace(8.2, 32.4, 50)
    lamina = poligono_uv([(u, -larg(u)) for u in us] + [(u, larg(u)) for u in us[::-1]])
    guarda = poligono_uv([(7.2, -6.6), (6.2, -5.8), (6.4, 0.0), (6.2, 5.8), (7.2, 6.6), (8.8, 6.4), (8.2, 5.2), (8.4, 0.0),
                          (8.2, -5.2), (8.8, -6.4)])
    empunhadura = faixa_uv(1.5, 6.6, 1.05)
    pomo = disco(0.0, 0.0, 1.9)
    if ETAPA == "silhueta":
        pinta(lamina | guarda | empunhadura | pomo, "f", 5, "lamina")
    else:
        # a lâmina: o plano de cima claro, o de baixo escuro; o gume de cima aceso, o de baixo um tom acima da sombra
        lp = larg(np.clip(U, 8.2, 32.4))
        tl = np.where(V < -0.15, 7, 5)
        tl = np.where((V < -0.15) & (V < -lp + 0.85), 8, tl)                    # o gume de cima, na luz
        tl = np.where((V > 0.15) & (V > lp - 0.75), 4, tl)                      # o gume de baixo, na sombra
        tl = np.where((U > 29.4) & (V < 0.15), 8, tl)                           # a ponta, acesa
        pinta(lamina, "f", tl, "lamina")
        sulco = lamina & (U > 9.6) & (U < 23.0) & (np.abs(V + 0.55) * K < max(0.42 * K, 0.5))
        pinta(sulco, "f", 5, "lamina"); fixo[sulco] = True                      # linha diagonal: a limpeza não mexe
        pinta(lamina & (U < 9.4), "f", np.where(V < 0, 6, 5), "lamina")          # o talão, junto da guarda
        # a guarda de latão (o do escudo): a face de cima acesa, a de baixo na sombra, as pontas um tom acima
        pinta(guarda, "o", np.where(U < 7.5, 6, 3), "guarda")
        pinta(guarda & (np.abs(V) > 5.5), "o", np.where(V < 0, 7, 4), "guarda")
        # a empunhadura: o couro com as voltas (as faixas escuras inclinadas)
        volta = ((U * 1.0 + V * 0.6) % 1.6) < 0.55
        pinta(empunhadura, "k", np.where(V < 0, 5, 3), "empunhadura")
        pinta(empunhadura & volta, "k", 2, "empunhadura"); fixo[empunhadura & volta] = True
        # o pomo de latão: a luz em cima à esquerda
        pinta(pomo, "o", np.where(V + U < -0.6, 6, np.where(V + U < 0.8, 5, 3)), "pomo")
        pinta(disco(-0.5, -0.6, 0.55) & pomo, "o", 7, "pomo")
    camadas = ["empunhadura", "pomo", "guarda", "lamina", "contorno"]
else:
    # A maça de aletas: a cabeça de aço em bulbo, simétrica no eixo, dividida em gomos pelas aletas (os vãos escuros, que
    # recortam a ponta de cima em dentes curtos), a luz de cima e da esquerda; a ponta curta no alto; o colar de
    # aço; o cabo de freixo; a empunhadura de couro e o botão de latão no pé.
    botao = disco(0.0, 0.0, 1.45)
    empunhadura = faixa_uv(1.1, 7.4, 1.1)
    cabo = faixa_uv(7.4, 20.0, 0.92)
    colar = faixa_uv(18.8, 20.8, 1.55)
    # a cabeça: um bulbo de aço (o ovo ao longo do eixo) dividido em três gomos pelas aletas (a da frente no meio, as dos
    # lados nas beiras; no 32 não cabem mais); os vãos entre elas, escuros, recortam a ponta de cima em dentes curtos
    CU, RU, RV = 25.6, 5.1, 4.5                                                 # o centro e os raios do bulbo
    BORDAS = [-RV, -1.55, 1.55, RV]
    def topo(v):
        return CU + RU * np.sqrt(np.clip(1 - (v / RV) ** 2, 0, 1))
    def pe(v):
        return CU - RU * np.sqrt(np.clip(1 - (v / RV) ** 2, 0, 1))
    cabeca = ((U - CU) / RU) ** 2 + (V / RV) ** 2 <= 1
    vaos = np.zeros((N, N), bool)
    for b in BORDAS[1:-1]:
        vaos |= np.abs(V - b) * K <= max(0.38 * K, 0.5)
    vaos &= (U > pe(V) + 0.8)                                                   # o pé do bulbo fica inteiro
    recorte = vaos & (U > topo(V) - 0.9)                                        # os dentes da ponta de cima
    cabeca &= ~recorte
    aleta = np.digitize(V, BORDAS[1:-1])                                        # 0..2: o gomo de cima, o da frente, o de baixo
    ponta = poligono_uv([(30.2, -1.0), (32.4, 0.0), (30.2, 1.0)])
    if ETAPA == "silhueta":
        pinta(botao | empunhadura | cabo | colar | cabeca | ponta, "f", 5, "cabeca")
    else:
        pinta(cabo, "m", np.where(V < -0.2, 6, np.where(V < 0.4, 5, 3)), "cabo")
        volta = ((U * 1.0 + V * 0.6) % 1.6) < 0.55
        pinta(empunhadura, "k", np.where(V < 0, 5, 3), "empunhadura")
        pinta(empunhadura & volta, "k", 2, "empunhadura"); fixo[empunhadura & volta] = True
        pinta(botao, "o", np.where(V + U < -0.4, 6, 4), "empunhadura")
        pinta(colar, "f", np.where(V < 0, 6, 3), "cabeca")
        pinta(colar & (np.abs(U - 19.8) < 0.35), "f", 2, "cabeca")
        # as aletas: a de perfil de cima e a de 45 graus de cima na luz, a da frente a mais clara, as de baixo na sombra;
        # a beira de fora de cada aleta um tom acima; os vãos escuros
        # os gomos: a luz de cima e da esquerda, mais forte no da frente; o alto de cada gomo aceso, o pé na sombra
        ta = np.choose(aleta, [6, 8, 4])
        ta = np.where((aleta == 0) & (V < -3.3), 7, ta)                         # a beira de cima, na luz
        ta = np.where((aleta == 2) & (V > 3.3), 3, ta)
        ta = np.where(U > topo(V) - 1.5, np.minimum(ta + 1, 8), ta)
        ta = np.where(U < pe(V) + 1.3, np.maximum(ta - 2, 2), ta)
        pinta(cabeca, "f", ta, "cabeca")
        pinta(cabeca & vaos, "f", 2, "cabeca"); fixo[cabeca & vaos] = True
        pinta(ponta, "f", np.where(V < 0, 7, 4), "cabeca")
    camadas = ["cabo", "empunhadura", "cabeca", "contorno"]

if ETAPA == "final":
    tom = limpar(mat, tom, fixo)
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"{PECA}_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta / "listas", camadas)
