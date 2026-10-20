# A manopla e as perneiras do Guerreiro (o remake do ferro, 3; a nova rodada de 19/10/2026, pelas referências novas do
# Jean), com o ferro da espada, do elmo e da cota aprovados e o couro da família; a luz de cima e da esquerda. Primeiro o
# 32; o 64 é o 32 ampliado 2x (a política da skill); o 40 e o 48 depois da aprovação da forma. Vazias, sem ninguém
# dentro. As propostas recusadas do c5fd33b estão em recusadas_c5fd33b/ (o script delas ao lado).
# Uso: python desenho.py <manopla|perneiras> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas

PECA = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {   # as rampas do elmo e da cota aprovados
    "f": ["#0e0f11", "#1a1c20", "#282b31", "#383c44", "#4c5159", "#646a73", "#848b94", "#b0b6bd", "#e4e8ec"],   # o ferro
    "k": ["#140b09", "#251412", "#3a1f1a", "#522c23", "#6b3b2d", "#86503c"],                                    # o couro
}
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
x32, y32 = X / K, Y / K


def pinta(onde, m, t, c):
    mat[onde] = m; tom[onde] = t if np.isscalar(t) else t[onde]; cam[onde] = c


def dentro(pts, xs, ys):
    """O polígono pts (nas coordenadas xs, ys) como máscara."""
    d = np.zeros((N, N), bool)
    for i in range(len(pts)):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % len(pts)]
        d ^= ((ya > ys) != (yb > ys)) & (xs < (xb - xa) * (ys - ya) / ((yb - ya) or 1e-9) + xa)
    return d


def poligono(pts):
    return dentro(pts, x32, y32)


def faixa(pts, r):
    """Uma faixa de largura 2r ao longo da linha pts (um dedo): a máscara e a posição ao longo dela (0 a 1)."""
    melhor = np.full((N, N), np.inf); pos = np.zeros((N, N)); lado = np.zeros((N, N))
    total = sum(np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])); feito = 0.0
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        L = np.hypot(xb - xa, yb - ya); ux, uy = (xb - xa) / L, (yb - ya) / L
        t = np.clip((x32 - xa) * ux + (y32 - ya) * uy, 0, L)
        d = np.hypot(x32 - (xa + t * ux), y32 - (ya + t * uy))
        m = d < melhor
        melhor = np.where(m, d, melhor); pos = np.where(m, (feito + t) / total, pos)
        lado = np.where(m, (x32 - xa) * -uy + (y32 - ya) * ux, lado)       # >0: o lado de baixo da faixa
        feito += L
    return melhor < r, pos, lado


if PECA == "manopla":
    # A manopla, pela referência principal (ferramentas/arte/referencias/Luvas/2.webp, a manopla isolada de perfil: os
    # dedos para a esquerda, o punho à direita), desenhada na grade de 32 pelas proporções dela: os dedos em um terço do
    # comprimento, a mão em um quarto, o pulso uma faixa estreita e a manchete o resto, a parte mais alta; a peça um
    # pouco inclinada (a manchete mais alta, os dedos mais baixos), como na referência. A prancha Raven Fantasy
    # (Luvas/1.gif, a secundária) mostra a simplificação de ícone: os dedos como traços separados por linhas escuras.
    # A construção: a manchete em cone abrindo para a direita, terminando arredondada na beira da boca; a faixa do
    # pulso ligando o punho à mão como uma luva vestível; as costas da mão com a placa em relevo; os quatro dedos como
    # faixas que saem dos nós e curvam para baixo nas pontas (o terceiro o mais longo), cada um por cima do de baixo
    # (a linha escura onde se cruzam), com as juntas atravessando a curva; o polegar saindo de baixo da mão, largo na
    # base, dobrando para a frente. Sem rebites. As medidas encolhidas 7% em volta do meio (uma margem nas beiras).
    x32 = 16.0 + (x32 - 16.0) * 1.07; y32 = 16.0 + (y32 - 16.0) * 1.07
    manchete = poligono([(19.6, 8.6), (23.6, 7.2), (27.4, 5.8), (29.4, 6.4), (30.6, 9.4), (31.0, 13.8), (30.6, 18.4),
                         (29.4, 21.4), (27.4, 22.4), (23.6, 21.6), (19.6, 20.6)])
    boca = manchete & (x32 > 27.8)                                             # a beira da boca, arredondada
    pulso = poligono([(17.0, 9.4), (20.0, 8.6), (20.0, 20.6), (17.0, 20.4)])
    mao = poligono([(10.4, 11.2), (13.6, 10.2), (17.2, 9.2), (17.4, 20.4), (15.0, 21.4), (10.4, 20.8)])
    placa = poligono([(12.0, 11.8), (15.4, 10.8), (16.4, 12.0), (16.4, 18.0), (15.4, 19.4), (12.0, 19.4), (11.2, 18.2), (11.2, 12.8)])
    # os dedos, de cima (o indicador) para baixo (o mínimo): da base nos nós até a ponta, curvando para baixo
    DEDOS = [[(11.0, 12.0), (7.4, 12.2), (5.0, 13.0), (3.8, 14.6), (3.6, 15.8)],
             [(11.0, 14.8), (6.6, 15.0), (3.6, 16.0), (2.2, 17.8), (2.0, 19.2)],
             [(11.0, 17.6), (6.2, 17.8), (3.2, 19.0), (1.8, 21.0), (2.0, 23.0)],
             [(11.0, 20.2), (7.6, 20.6), (5.6, 22.0), (4.8, 24.0), (5.0, 25.4)]]
    dedos = [faixa(pts, 1.25) for pts in DEDOS]
    polegar, pos_pol, lado_pol = faixa([(16.0, 20.0), (14.0, 22.4), (12.4, 24.6), (11.6, 26.6)], 1.45)
    peca = manchete | pulso | mao | polegar
    for d, _, _ in dedos:
        peca |= d
    # cada dedo por cima do de baixo: a parte de um dedo de baixo coberta por um de cima fica do de cima
    proprio = []; acima = np.zeros((N, N), bool)
    for d, _, _ in dedos:
        proprio.append(d & ~acima & ~mao); acima |= d
    if ETAPA == "silhueta":
        pinta(peca, "f", 5, "mao")
    else:
        # a manchete: um cone aceso por cima (a luz de cima e da esquerda), escurecendo para baixo; a beira da boca um
        # tom abaixo, com a quina acesa
        topo = np.interp(x32, [19.6, 27.4, 30.6], [8.6, 5.8, 9.4]); base = np.interp(x32, [19.6, 27.4, 30.6], [20.6, 22.4, 18.4])
        v = (y32 - topo) / np.maximum(base - topo, 1)
        pinta(manchete, "f", np.select([v < 0.2, v < 0.45, v < 0.75], [7, 6, 5], 4), "punho")
        pinta(boca, "f", np.select([v < 0.3, v < 0.7], [5, 4], 3), "punho")
        pinta(manchete & (x32 > 27.0) & (x32 < 28.0), "f", np.where(v < 0.55, 8, 5), "punho")
        # o pulso: escuro (a luva entrando na manchete), com uma tira acesa no meio
        vp = (y32 - 9.0) / 11.6
        pinta(pulso, "f", np.where(vp < 0.4, 4, 3), "punho")
        pinta(pulso & (x32 > 18.0) & (x32 < 19.0), "f", np.where(vp < 0.5, 6, 4), "punho")
        # as costas da mão: a placa em relevo (a quina de cima e da esquerda acesa, a de baixo e da direita escura)
        vm = (y32 - 10.0) / 11.0
        pinta(mao, "f", np.select([vm < 0.3, vm < 0.75], [6, 5], 4), "mao")
        pinta(placa, "f", np.select([vm < 0.35, vm < 0.75], [7, 6], 5), "mao")
        pinta(placa & (y32 < 12.6), "f", 8, "mao")
        pinta(mao & ~placa & ((y32 > 19.4) | (x32 > 16.4)), "f", 3, "mao")
        # os dedos: cada faixa acesa do lado de cima e escura do de baixo; as juntas atravessando nos terços (seguindo a
        # curva); a ponta um tom abaixo; o mínimo um tom abaixo de todos
        for k, ((d, pos, lado), meu) in enumerate(zip(dedos, proprio)):
            t = np.where(lado < 0, 7, 5) - (1 if k == 3 else 0)
            pinta(meu, "f", t, "dedos")
            pinta(meu & (np.abs(pos - 0.42) < 0.06), "f", 4, "dedos")                   # uma junta, no meio
            pinta(meu & (pos > 0.86), "f", np.where(lado < 0, 5, 4), "dedos")
        # a linha escura onde um dedo passa por cima do de baixo
        for k in range(1, 4):
            de_cima = np.zeros((N, N), bool)
            for j in range(k):
                de_cima |= proprio[j]
            viz = np.zeros((N, N), bool)
            viz[1:, :] |= de_cima[:-1, :]; viz[:-1, :] |= de_cima[1:, :]; viz[:, 1:] |= de_cima[:, :-1]; viz[:, :-1] |= de_cima[:, 1:]
            pinta(proprio[k] & viz, "f", 2, "dedos")
        # o polegar: aceso por cima, a dobra escura no meio, a ponta na sombra
        pinta(polegar & ~mao, "f", np.where(lado_pol < 0, 7, 5), "dedos")
        pinta(polegar & ~mao & (np.abs(pos_pol - 0.48) < 0.08), "f", 3, "dedos")
        pinta(polegar & ~mao & (pos_pol > 0.86), "f", 4, "dedos")
        fixo[peca & (tom == 2) & (cam == "dedos")] = True
    camadas = ["punho", "mao", "dedos", "contorno"]
else:
    # As perneiras, pela referência principal (ferramentas/arte/referencias/calça/2.png, a prancha de calças e perneiras:
    # o conjunto de placas prateadas da 3.ª linha, última coluna); a prancha de armaduras (calça/1.gif) de apoio. De
    # frente e em pé. Uma peça só, com as placas ligadas e sobrepostas: o cinto de couro com a fivela segurando tudo; a
    # placa do meio em ponta, por cima do alto das coxas; cada coxote descendo do cinto, largo e abaulado; a joelheira
    # larga, presa por cima do fim do coxote e do começo da greva (com a asa do lado de fora), sem virar uma bola; a
    # greva descendo e afinando até o tornozelo, com a beira de baixo virando. Cada perna é contínua (sem entalhes
    # separando coxa, joelho e canela); o vão entre as pernas abre debaixo da placa do meio. Vazias.
    # u: a distância ao eixo, v: a altura. O contorno de fora em degraus, onde uma placa passa por cima da outra: o
    # coxote sai além do cinto, a lâmina de baixo dele entra, a asa da joelheira sai, a greva entra e afina, a beira do
    # tornozelo sai um pouco. O vão abre debaixo da placa do meio e alarga até o joelho
    PERNA = [(9.4, 4.6), (10.8, 5.6), (10.8, 11.4), (9.8, 11.8), (9.8, 14.0),
             (9.4, 20.0), (8.8, 23.0), (8.4, 27.4), (9.2, 27.8), (9.2, 29.6),
             (2.8, 29.6), (2.8, 27.8), (3.4, 27.4), (3.4, 23.0), (3.2, 20.0), (2.8, 15.0), (2.0, 12.6), (0.6, 10.4), (0.0, 4.6)]
    def perna(lado):                                                           # lado: -1 a da esquerda, +1 a da direita
        return poligono([(16.0 + lado * u, v) for u, v in PERNA])
    def joelheira(lado):                                                       # a joelheira, mais larga que a perna
        return poligono([(16.0 + lado * u, v) for u, v in
                         [(2.2, 14.6), (6.0, 13.6), (10.0, 14.0), (11.8, 15.4), (11.8, 17.8), (10.2, 19.8), (6.0, 20.6), (2.6, 20.0), (2.0, 17.6)]])
    cinto = poligono([(6.6, 2.6), (25.4, 2.6), (25.4, 4.8), (6.6, 4.8)])
    meio = poligono([(11.4, 4.6), (20.6, 4.6), (19.8, 7.0), (16.0, 11.4), (12.2, 7.0)])          # a placa do meio, em ponta
    perna_e, perna_d = perna(-1), perna(+1)
    joe, jod = joelheira(-1), joelheira(+1)
    pernas = perna_e | perna_d
    peca = cinto | meio | pernas | joe | jod
    if ETAPA == "silhueta":
        pinta(peca, "f", 5, "coxotes")
    else:
        de = np.abs(x32 - 16.0)
        for pr, jo, lado in ((perna_e, joe, -1), (perna_d, jod, +1)):
            menos = 0 if lado < 0 else 1
            # cada perna um cilindro aceso à esquerda (a faixa clara no terço da esquerda, como na referência)
            fora, dentro_ = 16.0 + lado * 10.2, 16.0 + lado * 2.4
            u = (x32 - min(fora, dentro_)) / abs(fora - dentro_)                # 0 na beira esquerda da perna, 1 na direita
            tc = np.select([u < 0.12, u < 0.32, u < 0.55, u < 0.8], [6, 8, 7, 6], 5) - menos
            # as grevas (abaixo da joelheira) e o tornozelo, que sai por baixo dela
            greva = pr & (y32 > 19.4)
            pinta(greva, "f", tc - 1, "grevas")
            pinta(greva & (y32 < 20.6), "f", 4 - menos, "grevas")                      # a sombra da joelheira, 1 px
            pinta(greva & (y32 > 27.4) & (y32 < 28.2), "f", 3 - menos, "grevas")        # a beira do tornozelo
            pinta(greva & (y32 > 28.2), "f", np.where(u < 0.5, 6, 4) - menos, "grevas")
            # os coxotes: o de cima, abaulado; a lâmina de baixo entra por baixo dele (a sombra na beira de cima)
            coxa = pr & (y32 <= 19.4)
            pinta(coxa, "f", tc, "coxotes")
            pinta(coxa & (y32 > 11.2) & (y32 < 12.2), "f", np.where(u < 0.55, 5, 4) - menos, "coxotes")
            pinta(coxa & (y32 > 12.2), "f", tc - 1, "coxotes")
            pinta(coxa & (y32 < 5.8), "f", 3 - menos, "coxotes")                        # a sombra do cinto
            # a joelheira: uma placa larga por cima do fim do coxote e do começo da greva: a beira de cima acesa, a
            # quina no meio, a de baixo escura; a asa de fora um tom abaixo
            uj = (x32 - (16.0 + lado * 2.2)) * lado / 9.6                            # 0 do lado de dentro, 1 na asa
            tj = np.where(x32 < 16.0 + lado * 6.0, 7, 5) if lado < 0 else np.where(x32 < 16.0 + lado * 6.0, 6, 4)
            # a joelheira abaulada pela luz da esquerda: o reflexo curto no alto à esquerda, o lado de fora e a beira
            # de baixo escurecendo, a asa um tom abaixo (sem barras atravessando)
            uk = (x32 - (16.0 + lado * 2.2 if lado < 0 else 16.0 + 2.2)) / 9.6 if lado > 0 else (x32 - (16.0 - 11.8)) / 9.6
            pinta(jo, "f", np.select([uk < 0.18, uk < 0.55, uk < 0.8], [6, 7, 6], 5) - menos, "joelhos")
            pinta(jo & (uk > 0.18) & (uk < 0.45) & (y32 > 14.6) & (y32 < 16.6), "f", 8 - menos, "joelhos")
            pinta(jo & (y32 > 19.0), "f", 4 - menos, "joelhos")
            pinta(jo & ((uk > 0.86) if lado > 0 else (uk < 0.12)), "f", 4 - menos, "joelhos")
            fixo[jo & (y32 > 14.6) & (y32 < 16.6)] = True
        # a placa do meio, em ponta, por cima do alto das coxas: acesa à esquerda, a beira de baixo escura
        pinta(meio, "f", np.where(x32 < 16.0, 8, 6), "meio")
        borda_meio = meio & ~poligono([(11.4, 4.0), (20.6, 4.0), (19.2, 6.6), (16.0, 10.2), (12.8, 6.6)])
        pinta(borda_meio, "f", 1, "meio"); fixo[borda_meio] = True                    # a beira, por cima das coxas
        # o cinto de couro com a fivela de ferro
        pinta(cinto, "k", np.where(x32 < 12.0, 5, np.where(x32 < 20.0, 4, 2)), "cinto")
        pinta(cinto & (y32 > 4.2), "k", np.where(x32 < 16.0, 3, 1), "cinto")
        fivela = poligono([(14.4, 2.2), (17.6, 2.2), (17.6, 5.2), (14.4, 5.2)])
        pinta(fivela, "f", np.where(x32 < 16.0, 7, 5), "cinto")
        pinta(fivela & (np.abs(x32 - 16.0) < 0.7) & (np.abs(y32 - 3.7) < 0.7), "k", 1, "cinto")
    camadas = ["grevas", "coxotes", "joelhos", "meio", "cinto", "contorno"]

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
