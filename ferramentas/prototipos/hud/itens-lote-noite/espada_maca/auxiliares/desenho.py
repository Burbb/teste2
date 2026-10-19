# A espada e a maça do Guerreiro (o começo do remake do ferro, proposta de 19/10/2026): na diagonal da família (o pomo
# embaixo à esquerda, a ponta em cima à direita), com o ferro do machado aprovado (o cinza neutro), o latão do escudo e
# a madeira do cabo do machado; a luz de cima e da esquerda (a metade de cima de cada peça na luz). Rodada 2 (a 1 está
# em rodada1/). As medidas estão num
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
    # A espada, rodada 2, pela referência principal (ferramentas/arte/referencias/espada/espadasample.png, a espada de aço
    # da direita): a lâmina comprida de largura constante, os gumes paralelos e contínuos até a ponta, que se forma num
    # trecho curto (os dois gumes convergindo); dois planos do aço (o de cima na luz, com o gume aceso; o de baixo um tom
    # abaixo) e a aresta no meio; a guarda curta de latão, a empunhadura de couro com as voltas e o pomo de aço. As
    # proporções da referência: a lâmina em 2/3 do comprimento, a ponta no último quarto dela, a guarda com 1,6 vez a
    # largura da lâmina; a lâmina um pouco mais larga que a da referência, para ter presença no 32.
    # o começo da lâmina e o vértice: o vértice ajustado por grade (uma fração de pixel), para a ponta terminar num pixel
    # sobre o eixo e as larguras descerem sem degrau em cada tamanho (32: 1, 2, 4, 4, 5; 40 e 48: 1, 2, 4, 5, 6, 6, 7);
    # o 32 é o aprovado (0fcfe18)
    U0, U1 = 10.8, {32: 36.2, 40: 36.3, 48: 36.05}.get(N, 36.2)
    ML = 1.75                                                                   # a meia largura da lâmina
    LT = 4.6                                                                    # o comprimento do fechamento
    # a ponta (a quarta forma, 19/10/2026): como na espada de aço da referência, os dois gumes convergem juntos, em linha
    # reta, até o vértice no eixo da lâmina, num fechamento de cerca de duas vezes a meia largura; sem um gume reto e o
    # outro avançando (que deslocava o vértice para um lado e fazia uma curva brusca no fim)
    def larg(u):
        return ML * np.clip((U1 - np.asarray(u, float)) / LT, 0, 1)
    def gumes(u):
        m = larg(u)
        return -m, m                                                            # o de cima, o de baixo
    us = np.concatenate([np.linspace(U0, U1 - LT, 20), np.linspace(U1 - LT, U1, 40)])
    lamina = poligono_uv([(u, gumes(u)[0]) for u in us] + [(u, gumes(u)[1]) for u in us[::-1]])
    guarda = poligono_uv([(8.6, -4.2), (10.6, -4.2), (10.6, 4.2), (8.6, 4.2)])
    empunhadura = faixa_uv(2.0, 8.8, 0.95)
    pomo = disco(1.0, 0.0, 1.45)
    if ETAPA == "silhueta":
        pinta(lamina | guarda | empunhadura | pomo, "f", 5, "lamina")
    else:
        # os planos: o de cima (v < 0) claro, o gume de cima aceso; a aresta no meio; o de baixo um tom abaixo, o gume de
        # baixo na sombra; na ponta, os dois gumes acesos até o vértice
        # os planos e o fio seguem o fechamento: a posição através da lâmina, normalizada pela largura local (VS), recebe
        # as mesmas regras do corpo (o fio de cima aceso, o plano médio, o de baixo na sombra); o vértice, aceso
        VS = V * ML / np.maximum(larg(np.clip(U, U0, U1)), 1e-3)
        tl = np.where(VS < -0.05, 6, 4)
        tl = np.where(VS < -ML + 0.75, 8, tl)                                   # o gume de cima
        tl = np.where(VS > ML - 0.7, 3, tl)                                     # o gume de baixo
        tl = np.where(U > U1 - 1.1, 8, tl)                                      # o vértice, aceso
        pinta(lamina, "f", tl, "lamina")
        aresta = lamina & (np.abs(V - 0.05) * K < max(0.4 * K, 0.5)) & (U > U0 + 1.2) & (U < U1 - LT)
        pinta(aresta, "f", 5, "lamina"); fixo[aresta] = True                    # linha diagonal: a limpeza não mexe
        # no fechamento (e, nos tamanhos maiores, em toda a lâmina), os tons pela posição de cada pixel na sua linha (a lâmina é diagonal: cada linha da grade é um
        # corte dela, como o 8 8 5 3 3 do corpo): o fio claro junto do gume de cima até o vértice, o plano escuro junto do
        # de baixo até a linha antes do vértice, o médio no meio quando cabe; o vértice, aceso
        fecho = lamina & (U > U1 - LT - 0.4)
        if N != 32:   # nos maiores, a mesma proporção do corte do 32 (8 8 5 3 3) em toda a lâmina, não só no fechamento
            fecho = lamina.copy()
        for yy in np.unique(np.nonzero(fecho)[0]):
            xs = np.nonzero(lamina[yy])[0]
            w = len(xs)
            for i, xx in enumerate(xs):
                if not fecho[yy, xx]:
                    continue
                q = (i + 0.5) / w
                t = 8 if (w == 1 or q < 0.4) else (3 if q >= 0.6 else 5)
                mat[yy, xx] = "f"; tom[yy, xx] = t; fixo[yy, xx] = True
        # a guarda de latão: a face de cima acesa, a de baixo na sombra; as pontas um tom acima
        pinta(guarda, "o", np.where(U < 9.6, 6, 3), "guarda")
        pinta(guarda & (np.abs(V) > 3.3), "o", np.where(V < 0, 7, 4), "guarda")
        # a empunhadura: o couro com as voltas
        volta = ((U * 1.0 + V * 0.6) % 1.6) < 0.55
        pinta(empunhadura, "k", np.where(V < 0, 5, 3), "empunhadura")
        pinta(empunhadura & volta, "k", 2, "empunhadura"); fixo[empunhadura & volta] = True
        # o pomo de aço: a luz em cima à esquerda
        pinta(pomo, "f", np.where(V + (U - 1.0) < -0.5, 7, np.where(V + (U - 1.0) < 0.8, 5, 3)), "pomo")
    camadas = ["empunhadura", "pomo", "guarda", "lamina", "contorno"]
else:
    # A maça, rodada 2: a cabeça pesada e redonda (a proporção entre cabeça e cabo e a massa arredondada vêm do
    # placeholder antigo, sem a pintura dele), com cinco aletas curtas e bem separadas saindo do bulbo (a da ponta, duas
    # nos lados, duas embaixo, junto do cabo); a luz acompanha o volume (o bulbo como uma esfera, a luz de cima e da
    # esquerda, o brilho agrupado), sem a faixa clara atravessando a cabeça; o colar de aço, o cabo de freixo, a
    # empunhadura de couro e o botão de latão.
    from pixel_comum import LUZ
    CU, R = 25.0, 4.25                                                          # o centro do bulbo (no eixo) e o raio
    C = O + CU * D
    botao = disco(1.0, 0.0, 1.4)
    empunhadura = faixa_uv(2.0, 8.4, 1.05)
    cabo = faixa_uv(8.4, 21.4, 0.95)
    colar = faixa_uv(19.8, 21.6, 1.55)
    bulbo = np.hypot(x32 - C[0], y32 - C[1]) <= R
    ALETAS = [(1.0, 0.0), (0.42, -0.91), (0.42, 0.91), (-0.55, -0.83), (-0.55, 0.83)]   # as direções em (u, v)
    aletas = np.zeros((N, N), bool); qual = np.full((N, N), -1)
    for k, (du, dv) in enumerate(ALETAS):
        n = np.hypot(du, dv); du, dv = du / n, dv / n
        if N == 32:   # o 32 aprovado (87c12eb): o polígono que, na grade de 32, sai como um botão rombudo de ~2 px
            a = poligono_uv([(CU + du * (R - 0.6) - dv * 1.25, dv * (R - 0.6) + du * 1.25),
                             (CU + du * (R + 1.75) - dv * 0.95, dv * (R + 1.75) + du * 0.95),
                             (CU + du * (R + 1.75) + dv * 0.95, dv * (R + 1.75) - du * 0.95),
                             (CU + du * (R - 0.6) + dv * 1.25, dv * (R - 0.6) - du * 1.25)])
        else:         # nos maiores, o mesmo botão rombudo (retangular, sem afilar), para manter o formato do 32
            a = poligono_uv([(CU + du * (R - 0.6) - dv * 1.3, dv * (R - 0.6) + du * 1.3),
                             (CU + du * (R + 2.0) - dv * 1.3, dv * (R + 2.0) + du * 1.3),
                             (CU + du * (R + 2.0) + dv * 1.3, dv * (R + 2.0) - du * 1.3),
                             (CU + du * (R - 0.6) + dv * 1.3, dv * (R - 0.6) - du * 1.3)])
        qual = np.where(a & ~bulbo, k, qual); aletas |= a
    aletas &= ~bulbo
    cabeca = bulbo | aletas
    if ETAPA == "silhueta":
        pinta(botao | empunhadura | cabo | colar | cabeca, "f", 5, "cabeca")
    else:
        pinta(cabo, "m", np.where(V < -0.2, 6, np.where(V < 0.4, 5, 3)), "cabo")
        volta = ((U * 1.0 + V * 0.6) % 1.6) < 0.55
        pinta(empunhadura, "k", np.where(V < 0, 5, 3), "empunhadura")
        pinta(empunhadura & volta, "k", 2, "empunhadura"); fixo[empunhadura & volta] = True
        pinta(botao, "o", np.where(V + (U - 1.0) < -0.4, 6, 4), "empunhadura")
        pinta(colar, "f", np.where(V < 0, 6, 3), "cabeca")
        # o bulbo como esfera: o tom pela normal e pela luz, em faixas largas; o brilho agrupado em cima à esquerda
        nx = (x32 - C[0]) / R; ny = (y32 - C[1]) / R; nz = np.sqrt(np.clip(1 - nx * nx - ny * ny, 0, 1))
        li = nx * LUZ[0] + ny * LUZ[1] + nz * LUZ[2]
        tb = np.select([li > 0.86, li > 0.62, li > 0.32, li > 0.0], [8, 6, 5, 4], 2)
        pinta(bulbo, "f", tb, "cabeca")
        # as aletas: cada uma no tom da direção para onde aponta (as de cima e da esquerda na luz), a beira de fora acesa
        # nas de cima; a junção com o bulbo, uma linha escura
        for k, (du, dv) in enumerate(ALETAS):
            n = np.hypot(du, dv); dxy = (du * D + dv * Pp) / n
            luz_a = dxy[0] * LUZ[0] + dxy[1] * LUZ[1]
            ta = 7 if luz_a > 0.3 else (5 if luz_a > -0.2 else 3)
            pinta(aletas & (qual == k), "f", ta, "cabeca")
        juncao = aletas & (np.hypot(x32 - C[0], y32 - C[1]) <= R + (0.75 if N == 32 else 0.6 + 0.5 / K))   # 1 px escuro na base
        pinta(juncao, "f", 2, "cabeca")
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
