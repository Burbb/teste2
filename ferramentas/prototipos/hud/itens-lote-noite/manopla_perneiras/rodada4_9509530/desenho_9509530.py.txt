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
    # A manopla, rodada 4, pela imagem que o Jean mandou (referencias/Luvas/manopla-jean.webp, feita da principal
    # Luvas/2.webp); a prancha Raven Fantasy (Luvas/1.gif) para a simplificação de ícone. A mão primeiro: vista pelas
    # costas, um pouco de cima e de lado, os dedos para a esquerda; os quatro dedos abertos em leque, levemente dobrados
    # (cada um um pouco mais baixo e o de baixo indo mais longe), separados por um vão; o polegar embaixo, ligado à base
    # da mão; o pulso estreito. Depois as placas: cada dedo em três segmentos (as juntas escuras), a placa das costas da
    # mão em pentágono com a ponta para os dedos, os anéis do pulso, a manchete abrindo para a direita. A manchete menor
    # que na rodada anterior (os dedos com espaço). Sem rebites.
    # no 32, três dedos (o indicador, o médio e o anelar com o mínimo por trás), de 3 px com 1 px de vão: dedos, não
    # hastes; levemente dobrados, o do meio o mais longo
    DEDOS = [[(13.0, 11.0), (9.4, 10.8), (6.4, 11.2), (4.6, 12.4), (4.0, 13.6)],
             [(13.0, 15.0), (9.0, 15.0), (5.6, 15.6), (3.2, 16.8), (2.4, 18.2)],
             [(13.2, 19.0), (10.0, 19.4), (6.8, 20.4), (4.8, 21.8), (4.2, 23.0)]]
    dedos = [faixa(pts, 1.5) for pts in DEDOS]
    polegar, pos_pol, lado_pol = faixa([(16.4, 20.0), (14.0, 22.0), (12.2, 24.0), (11.4, 25.8)], 1.35)
    mao = poligono([(12.0, 13.8), (13.4, 9.6), (19.4, 9.0), (20.4, 11.4), (20.4, 18.4), (19.0, 20.4), (13.6, 20.0)])
    placa = poligono([(13.4, 14.4), (14.4, 10.6), (18.8, 10.2), (19.4, 12.0), (19.4, 17.6), (18.4, 19.0), (14.4, 18.6)])
    pulso = poligono([(20.2, 10.0), (22.6, 9.8), (22.6, 19.4), (20.2, 19.6)])
    manchete = poligono([(22.4, 9.8), (25.4, 8.8), (28.2, 8.0), (29.4, 9.0), (30.0, 12.0), (30.0, 17.4), (29.4, 20.4),
                         (28.2, 21.6), (25.4, 21.0), (22.4, 19.6)])
    boca = manchete & (x32 > 27.8)                                             # a beira da boca, arredondada
    peca = manchete | pulso | mao | polegar
    for d, _, _ in dedos:
        peca |= d
    # os vãos entre os dedos: o pixel mais perto de dois dedos que de um fica vazio (o dedo de cima por cima)
    proprio = []; acima = np.zeros((N, N), bool)
    for d, _, _ in dedos:
        proprio.append(d & ~acima & ~mao); acima |= d
    if ETAPA == "silhueta":
        pinta(peca, "f", 5, "mao")
    else:
        # a manchete: acesa por cima, escurecendo para baixo; a costura no meio; a beira da boca, com a quina acesa
        topo = np.interp(x32, [22.4, 28.2, 30.0], [9.8, 8.0, 12.0]); base = np.interp(x32, [22.4, 28.2, 30.0], [19.6, 21.6, 17.4])
        v = (y32 - topo) / np.maximum(base - topo, 1)
        pinta(manchete, "f", np.select([v < 0.22, v < 0.5, v < 0.78], [8, 6, 5], 4), "punho")
        pinta(manchete & (np.abs(v - 0.5) < 0.05), "f", 3, "punho")
        pinta(boca, "f", np.select([v < 0.3, v < 0.7], [6, 4], 3), "punho")
        pinta(manchete & (x32 > 27.0) & (x32 < 28.0), "f", np.where(v < 0.55, 7, 4), "punho")
        # os anéis do pulso: dois escuros com a beira acesa (a luva entra na manchete)
        vp = (y32 - 9.8) / 9.8
        pinta(pulso, "f", np.where(vp < 0.45, 5, 3), "punho")
        pinta(pulso & ((np.abs(x32 - 21.0) < 0.5) | (np.abs(x32 - 22.4) < 0.4)), "f", 2, "punho")
        # as costas da mão: o pentágono em relevo, aceso no alto e à esquerda; em volta, a base mais escura
        vm = (y32 - 9.0) / 11.4
        pinta(mao, "f", np.where(vm < 0.5, 5, 4), "mao")
        pinta(placa, "f", np.select([vm < 0.25, vm < 0.6], [8, 7], 5), "mao")
        pinta(placa & (x32 > 18.6), "f", np.where(vm < 0.5, 5, 4), "mao")
        pinta(mao & ~placa & (y32 > 18.4), "f", 2, "mao")
        # os dedos: cada um aceso por cima e escuro por baixo; as juntas (duas) atravessando; a ponta arredondada na
        # luz; onde um passa sobre o de baixo, a linha escura
        for k, ((d, pos, lado), meu) in enumerate(zip(dedos, proprio)):
            pinta(meu, "f", np.select([lado < -0.4, lado < 0.5], [8, 6], 4) - (1 if k == 2 else 0), "dedos")
            junta = (np.abs(pos - 0.36) < 0.045) | (np.abs(pos - 0.68) < 0.045)
            pinta(meu & junta, "f", np.where(lado < 0, 5, 3), "dedos")
            pinta(meu & (pos > 0.88), "f", np.where(lado < 0.5, 7, 4), "dedos")
        # o polegar: aceso por cima, uma junta, a ponta na luz; a base sob a mão escura
        pinta(polegar & ~mao, "f", np.where(lado_pol < 0, 7, 5), "dedos")
        pinta(polegar & ~mao & (np.abs(pos_pol - 0.52) < 0.07), "f", 3, "dedos")
        pinta(polegar & ~mao & (pos_pol < 0.2), "f", 3, "dedos")
        fixo[peca & (tom <= 3) & (cam == "dedos")] = True
    camadas = ["punho", "mao", "dedos", "contorno"]
else:
    # As perneiras, rodada 4: armadura pesada, pela imagem que o Jean mandou (referencias/calça/perneiras-jean.webp,
    # feita do conjunto prateado da 3.ª linha, última coluna de calça/2.png, a principal). O metal em planos: cada placa
    # com faces retas, o reflexo definido numa faixa clara contra planos escuros, a espessura na beira; a sombra de 1 px
    # onde uma placa cobre a outra. O cinto de couro com a boca escura em cima e a fivela; a placa do meio em ponta, em
    # duas faces; o coxote em duas lâminas (a do quadril e a da coxa), o contorno em degrau; a joelheira em losango com
    # a aresta no meio e quatro faces (a de cima à esquerda acesa, as de baixo escuras), as asas em ponta para os lados,
    # por cima do fim do coxote e de uma lâmina curta que a liga à greva; a greva reta afinando, a tornozeleira por baixo.
    # As correias de couro aparecem no vão entre as coxas. Cada perna inteira, as placas ligadas.
    # u: a distância ao eixo, v: a altura. O contorno de cada perna: (v, u de fora, u de dentro)
    CONTORNO = [(4.6, 7.8, 0.0), (6.6, 7.8, 0.0), (6.7, 8.6, 0.0), (9.4, 8.6, 0.0), (10.6, 8.4, 1.4), (12.6, 8.2, 1.6),
                (13.4, 7.8, 1.8), (15.0, 7.8, 2.0), (20.2, 7.4, 2.2), (21.6, 7.4, 2.2), (27.2, 6.8, 2.4), (27.3, 7.4, 2.0),
                (29.6, 7.4, 2.0)]
    vs = [c[0] for c in CONTORNO]
    u_fora = np.interp(y32, vs, [c[1] for c in CONTORNO]); u_dentro = np.interp(y32, vs, [c[2] for c in CONTORNO])
    de = np.abs(x32 - 16.0)
    lado_x = np.where(x32 < 16.0, -1, 1)
    perna = (y32 > 4.6) & (y32 < 29.6) & (de < u_fora) & (de > u_dentro)
    # a joelheira em losango, com as asas: o meio a UJ do eixo, na altura JK
    UJ, JK, MH = 4.8, 17.2, 3.0
    dxj = (x32 - (16.0 + lado_x * UJ)); dyj = y32 - JK
    def losango(lado, enc=0.0):                                                 # a joelheira, a asa de fora mais comprida
        c = 16.0 + lado * UJ
        return poligono([(c, JK - MH + enc), (c + lado * (4.4 - enc), JK - 0.2), (c, JK + MH - enc), (c - lado * (3.6 - enc), JK - 0.2)])
    joelheira = losango(-1) | losango(+1)
    miolo_j = losango(-1, 0.9) | losango(+1, 0.9)
    cinto = (y32 > 2.0) & (y32 < 4.8) & (de < 8.6)
    meio = poligono([(12.4, 4.6), (19.6, 4.6), (19.0, 8.0), (16.0, 12.2), (13.0, 8.0)])
    peca = cinto | meio | perna | joelheira
    if ETAPA == "silhueta":
        pinta(peca, "f", 5, "coxotes")
    else:
        # a posição na largura da perna (0 na beira da esquerda, 1 na da direita): as faces de cada placa
        esq = np.where(lado_x < 0, 16.0 - u_fora, 16.0 + u_dentro); dir_ = np.where(lado_x < 0, 16.0 - u_dentro, 16.0 + u_fora)
        a = (x32 - esq) / np.maximum(dir_ - esq, 1)
        faces = np.select([a < 0.16, a < 0.42, a < 0.7, a < 0.88], [6, 8, 6, 5], 3)
        # as grevas e a tornozeleira
        greva = perna & (y32 > 19.6)
        pinta(greva, "f", faces, "grevas")
        pinta(greva & (y32 < 20.6), "f", 2, "grevas")                                    # a sombra da lâmina do joelho
        pinta(greva & (y32 > 20.6) & (y32 < 21.6), "f", np.where(a < 0.6, 7, 5), "grevas")  # a lâmina curta, acesa em cima
        pinta(greva & (y32 > 21.6) & (y32 < 22.4), "f", 2, "grevas")                     # a lâmina sobre a greva
        pinta(greva & (y32 > 27.0) & (y32 < 27.8), "f", 1, "grevas")                     # a beira da greva sobre a tornozeleira
        pinta(greva & (y32 > 27.8), "f", np.select([a < 0.42, a < 0.75], [7, 5], 3), "grevas")
        # os coxotes: a lâmina do quadril e a da coxa, cada uma com a beira de cima acesa (a espessura) e a sombra da
        # de cima por cima dela
        coxa = perna & (y32 <= 19.6)
        pinta(coxa, "f", faces, "coxotes")
        pinta(coxa & (y32 < 5.6), "f", 2, "coxotes")                                     # a sombra do cinto
        pinta(coxa & (y32 > 6.6) & (y32 < 7.4), "f", 2, "coxotes")                       # a lâmina do quadril sobre a coxa
        pinta(coxa & (y32 > 7.4) & (y32 < 8.2), "f", np.where(a < 0.7, 7, 5), "coxotes")
        pinta(coxa & (y32 > 12.6) & (y32 < 13.4), "f", 2, "coxotes")                     # a coxa sobre a lâmina de baixo
        pinta(coxa & (y32 > 13.4) & (y32 < 14.2), "f", np.where(a < 0.7, 7, 5), "coxotes")
        # as correias de couro no vão entre as coxas
        correia = perna & (de < u_dentro + 1.0) & (np.abs(y32 - 9.4 - (de - u_dentro) * 1.0) < 0.6)   # uma tira, em diagonal
        pinta(correia, "k", np.where(x32 < 16.0, 4, 2), "cinto")
        # a joelheira: quatro faces pela aresta no meio (a de cima à esquerda acesa, a de cima à direita média, as de
        # baixo escuras), as asas um tom abaixo, a beira escura por cima das placas em volta
        if N != 32:
            f_j = np.where(dyj < -0.2, np.where(dxj < 0, 8, 6), np.where(dxj < 0, 4, 2))
            pinta(joelheira, "f", f_j, "joelhos")
            pinta(joelheira & ~miolo_j, "f", np.where((dyj < -0.2) & (dxj < 0), 6, 1), "joelhos")   # a espessura, a beira
        else:
            # no 32 o losango tem 9 x 7 px e a regra não forma as faces: desenhado à mão. A aresta vertical no meio e a
            # horizontal na altura das asas; a face de cima à esquerda a mais clara, a de cima à direita média, as de
            # baixo escuras; a beira de baixo escura por cima da greva; as asas passando do contorno da perna (2 px do
            # lado de fora, 1 do de dentro). "." deixa a placa de baixo.
            JOELHO = ["....7....",
                      "...876...",
                      "..88766..",
                      "687776554",
                      ".1443221.",
                      "..14321..",
                      "...131..."]
            # a lâmina de baixo do coxote, em volta da joelheira, recolhida atrás dela (escura)
            pinta(coxa & (y32 > 14.0) & (y32 < 17.0), "f", np.where(a < 0.42, 4, 3), "coxotes")
            for x0 in (6, 17):
                for j, linha in enumerate(JOELHO):
                    for i, t in enumerate(linha):
                        if t != ".":
                            pinta((X == x0 + i + 0.5) & (Y == 14 + j + 0.5), "f", int(t), "joelhos")
            joelheira = (cam == "joelhos")
        fixo[joelheira] = True
        # a placa do meio, em duas faces; a beira escura por cima das coxas
        pinta(meio, "f", np.where(x32 < 16.0, 8, 6), "meio")
        borda_meio = meio & ~poligono([(12.4, 4.0), (19.6, 4.0), (18.2, 7.8), (16.0, 11.0), (13.8, 7.8)])
        pinta(borda_meio, "f", 1, "meio"); fixo[borda_meio] = True
        # o cinto: a boca escura em cima (o lado de dentro), o couro e a fivela de ferro
        pinta(cinto, "k", np.where(x32 < 12.0, 5, np.where(x32 < 20.0, 4, 2)), "cinto")
        pinta(cinto & (y32 < 2.9), "f", 1, "cinto")
        pinta(cinto & (y32 > 4.0), "k", np.where(x32 < 16.0, 3, 1), "cinto")
        fivela = (np.abs(x32 - 16.0) < 1.7) & (y32 > 2.9) & (y32 < 5.0)
        pinta(fivela, "f", np.where(x32 < 16.0, 7, 5), "cinto")
        pinta(fivela & (np.abs(x32 - 16.0) < 0.7) & (np.abs(y32 - 3.9) < 0.6), "f", 2, "cinto")
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
