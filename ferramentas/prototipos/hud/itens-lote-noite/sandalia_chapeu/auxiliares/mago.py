# A Sandália e o Chapéu Pontudo do Mago (proposta de 19/10/2026), no conjunto de tecido aprovado (o capuz de tecido,
# a luva de seda, o manto e a calça de viagem): a lã azul-acinzentada e o linho cru das mesmas rampas, o couro das
# botas aprovadas, a luz de cima e da esquerda. A construção é a mesma em 32, 40 e 48 (as medidas no quadro de 32);
# o 64 é o 32 ampliado 2x (a política da skill).
# Uso: python mago.py <sandalia|chapeu> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas

PECA = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {
    "l": ["#10131C", "#1C2230", "#2A3346", "#3B4760", "#4F5E7C", "#667696", "#8392B0"],   # a lã (a do capuz de tecido)
    "n": ["#5A4A36", "#8A7656", "#BCA67E", "#E2D2AA"],                                  # o linho cru (as faixas da calça)
    "k": ["#1E130C", "#3E2716", "#57381F", "#724B2A", "#8E6236", "#B08C62"],            # o couro (o das botas aprovadas)
}
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
x32, y32 = X / K, Y / K                                         # as coordenadas no quadro de 32


def pinta(onde, m, t, c):
    mat[onde] = m; tom[onde] = t if np.isscalar(t) else t[onde]; cam[onde] = c


def poligono(pts, dx=0.0, dy=0.0):
    """Os pixels (pelo centro) dentro do polígono de pontos no quadro de 32 (deslocado de dx, dy)."""
    dentro = np.zeros((N, N), bool)
    n = len(pts)
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
        xa += dx; xb += dx; ya += dy; yb += dy
        cruza = ((ya > y32) != (yb > y32)) & (x32 < (xb - xa) * (y32 - ya) / ((yb - ya) or 1e-9) + xa)
        dentro ^= cruza
    return dentro


def tira(pts, larg, dx=0.0, dy=0.0):
    """Os pixels perto da linha quebrada (no quadro de 32), com a meia largura `larg` em pixels do quadro de 32 (no
    mínimo meio pixel do tamanho, para a tira não sumir)."""
    meia = max(larg * K, 0.5)
    d = np.full((N, N), np.inf)
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        xa += dx; xb += dx; ya += dy; yb += dy
        ddx, ddy = xb - xa, yb - ya; L2 = ddx * ddx + ddy * ddy or 1e-9
        t = np.clip(((x32 - xa) * ddx + (y32 - ya) * ddy) / L2, 0, 1)
        d = np.minimum(d, np.hypot(x32 - (xa + t * ddx), y32 - (ya + t * ddy)) * K)
    return d <= meia


if PECA == "sandalia":
    # A sandália sozinha, de lado e um pouco de cima, com a ponta à esquerda (como as botas de couro): a sola grossa
    # de couro, a palmilha clara aparecendo por cima dela, e as tiras que formam a gaiola do pé, presas nas beiras da
    # sola: a alça dos dedos, a do peito do pé, as duas que sobem até o anel do tornozelo (uma da frente, outra de trás
    # do calcanhar) e o anel. Por dentro das alças e do anel aparece o fundo: o espaço do pé, vazio. Um laço de linho
    # (o das faixas da calça) fecha o anel.
    # a sola: o lado (a espessura) e a palmilha por cima, com a ponta um pouco levantada
    sola_lado = poligono([(3.0, 22.6), (5.0, 22.8), (14.0, 23.4), (27.0, 23.0), (28.6, 23.4), (28.8, 25.2), (27.6, 26.6),
                          (14.0, 26.6), (6.0, 26.2), (3.6, 25.4), (2.6, 24.0)])
    palmilha = poligono([(3.4, 22.6), (5.0, 21.4), (9.0, 20.6), (14.0, 21.0), (19.0, 20.6), (24.0, 20.2), (27.6, 20.4),
                         (28.6, 21.6), (28.2, 23.0), (24.0, 23.4), (14.0, 23.8), (6.0, 23.4)])
    sola_lado &= ~palmilha
    # as alças: cada uma sobe da beira de perto (embaixo), passa por cima do pé e desce na beira de longe (atrás)
    def alca(x0, x1, topo, n=20):
        t = np.linspace(0, np.pi, n)
        xs = x0 + (x1 - x0) * (1 - np.cos(t)) / 2
        base = np.interp(t, [0, np.pi], [23.2, 21.0])                       # perto (embaixo) para longe (em cima)
        return [(x, b - (b - topo) * np.sin(tt)) for x, b, tt in zip(xs, base, t)]
    dedos = alca(5.4, 11.6, 15.6)
    peito = alca(12.6, 19.2, 11.8)
    C = (24.0, 7.4); RX, RY = 4.1, 3.4                                     # o anel do tornozelo
    ang = np.linspace(0, 2 * np.pi, 60)
    aro_longe = [(C[0] + RX * np.cos(a), C[1] + RY * np.sin(a)) for a in ang if np.sin(a) < 0.15]
    aro_perto = [(C[0] + RX * np.cos(a), C[1] + RY * np.sin(a)) for a in ang if np.sin(a) > -0.15]
    subida_frente = [(20.0, 22.8), (19.6, 15.0), (20.0, 9.0)]
    subida_tras = [(28.2, 21.4), (28.6, 15.0), (27.8, 8.6)]
    LT = 0.62
    if ETAPA == "silhueta":
        pinta(sola_lado | palmilha, "k", 3, "sola")
        for pts in (dedos, peito, aro_longe, aro_perto, subida_frente, subida_tras):
            pinta(tira(pts, LT), "k", 3, "tiras")
    else:
        pinta(sola_lado, "k", np.where(x32 < 6.0, 2, 1), "sola")
        pinta(sola_lado & (y32 > 25.4), "k", 0, "sola")                        # a beira de baixo
        pinta(palmilha, "k", np.where(y32 < 21.6, 5, 4), "palmilha")
        pinta(palmilha & (x32 > 23.4) & (y32 > 21.0), "k", 3, "palmilha")      # o gasto do calcanhar
        pinta(palmilha & (x32 > 7.0) & (x32 < 11.0) & (y32 > 21.4), "k", 3, "palmilha")   # o gasto da planta
        # as partes de longe (atrás do espaço do pé), mais escuras: as pernas de trás das alças e o anel de trás
        for pts in (dedos, peito):
            meio = len(pts) // 2
            pinta(tira(pts[meio:], LT), "k", 2, "tiras")
        pinta(tira(aro_longe, LT), "k", 1, "tiras")
        pinta(tira(subida_tras, LT + 0.1), "k", 2, "tiras")
        # as partes de perto: a perna da frente de cada alça e o topo, com a beira de cima clara
        for pts in (dedos, peito):
            meio = len(pts) // 2
            pinta(tira(pts[:meio + 2], LT), "k", 3, "tiras")
            pinta(tira(pts[meio - 3:meio + 3], LT), "k", 4, "tiras")
        pinta(tira(subida_frente, LT + 0.1), "k", 3, "tiras")
        pinta(tira(aro_perto, LT), "k", 3, "tiras")
        pinta(tira([p for p in aro_perto if p[0] < C[0]], LT), "k", 4, "tiras")
        # o laço de linho na frente do anel, com as duas pontas soltas
        no = (C[0] - RX * 0.98, C[1] + 1.0)
        pinta(tira([(no[0] - 0.5, no[1]), (no[0] + 0.3, no[1])], 0.8), "n", 3, "no")
        pinta(tira([(no[0] - 0.8, no[1] + 0.4), (no[0] - 2.4, no[1] + 2.8)], 0.5), "n", 2, "no")
    camadas = ["sola", "palmilha", "tiras", "no", "contorno"]

else:
    # O Chapéu Pontudo, de frente e um pouco de cima: a aba larga em perspectiva (a elipse, com a beira da frente
    # caindo um pouco e a espessura embaixo), a copa de lã em cone com volume, que sobe inclinada e tomba a ponta para
    # a direita, com o vinco onde o pano dobra; a fita de linho cru na base da copa. Sem estrela nem brilho: é um
    # chapéu de viagem gasto.
    def poli_linha(c, w):                                                    # o polígono de uma faixa em volta da linha c
        c = np.asarray(c); t = np.gradient(c, axis=0); t /= np.linalg.norm(t, axis=1)[:, None]
        nn = np.stack([t[:, 1], -t[:, 0]], 1)                                 # a normal (para a esquerda da subida)
        return [tuple(p) for p in c + nn * w[:, None]] + [tuple(p) for p in (c - nn * w[:, None])[::-1]], nn
    # a aba
    CA = np.array([15.8, 24.2]); RXA = 14.4
    ang = np.linspace(0, 2 * np.pi, 120)
    rya = 4.4 + 0.5 * np.sin(ang - 0.4) * (np.sin(ang) > 0)                 # a beira da frente cai um pouco à direita
    aba_pts = [(CA[0] + RXA * np.cos(a), CA[1] + r * np.sin(a)) for a, r in zip(ang, rya)]
    aba = poligono(aba_pts)
    aba_lado = poligono(aba_pts, 0, 1.3) & ~aba                              # a espessura da beira, embaixo
    # a copa: a linha do meio sobe da aba e tomba a ponta para a direita
    ts = np.linspace(0, 1, 70)
    cx = np.interp(ts, [0, 0.3, 0.55, 0.72, 0.86, 1.0], [15.8, 16.4, 17.6, 19.6, 22.6, 25.6])
    cy = np.interp(ts, [0, 0.3, 0.55, 0.72, 0.86, 1.0], [23.2, 15.6, 10.2, 6.8, 5.4, 8.4])
    w = np.interp(ts, [0, 0.12, 0.35, 0.6, 0.8, 0.92, 1.0], [6.8, 6.0, 4.4, 2.8, 1.7, 0.8, 0.15])
    copa_pts, nn = poli_linha(np.stack([cx, cy], 1), w)
    copa = poligono(copa_pts)
    # a base da copa é a elipse que senta na aba (a frente curva para baixo)
    base = poligono([(15.8 + 6.8 * np.cos(a), 23.2 + 2.2 * np.sin(a)) for a in ang])
    copa |= base & (y32 > 21.0)
    if ETAPA == "silhueta":
        pinta(aba | aba_lado, "l", 4, "aba")
        pinta(copa, "l", 4, "copa")
    else:
        # a aba: a luz da esquerda em faixas, a parte de trás (acima da copa) mais escura, a espessura embaixo
        ta = np.where(x32 < 8.0, 5, np.where(x32 < 18.0, 4, np.where(x32 < 25.0, 3, 2)))
        ta = np.where(y32 < CA[1] - 1.0, ta - 1, ta)
        pinta(aba, "l", ta, "aba")
        pinta(aba & ~poligono(aba_pts, 0, -0.9) & (y32 > CA[1]), "l", np.maximum(ta - 1, 1), "aba")   # a beira da frente
        pinta(aba_lado, "l", np.where(x32 < 14.0, 1, 0), "aba")
        # a sombra da copa na aba, à direita
        pinta(aba & poligono([(15.8 + 7.4 * np.cos(a) + 2.2, 23.6 + 2.6 * np.sin(a)) for a in ang]) & (x32 > 18.0), "l", 2, "aba")
        # a copa: cada pixel pela posição através da faixa (da esquerda, na luz, à direita, na sombra)
        dist = np.full((N, N), np.inf); lado = np.zeros((N, N)); tpos = np.zeros((N, N))
        for i in range(len(ts)):
            dd = np.hypot(x32 - cx[i], y32 - cy[i])
            melhor = dd < dist
            dist = np.where(melhor, dd, dist)
            s_ = ((x32 - cx[i]) * -nn[i, 0] + (y32 - cy[i]) * -nn[i, 1]) / max(w[i], 0.5)   # -1 à esquerda, +1 à direita
            lado = np.where(melhor, s_, lado); tpos = np.where(melhor, ts[i], tpos)
        tc = np.where(lado < -0.4, 5, np.where(lado < 0.15, 4, np.where(lado < 0.6, 3, 2)))
        tc = np.where((tpos > 0.62) & (lado < 0.0), np.minimum(tc + 1, 6), tc)       # o tombo da ponta, virado para cima
        pinta(copa, "l", tc, "copa")
        # o vinco do tombo: a dobra escura atravessando a copa, com a beira clara em cima
        pinta(copa & tira([(17.6, 8.4), (19.6, 10.4), (21.2, 10.0)], 0.55), "l", 2, "dobras")
        pinta(copa & tira([(17.2, 7.6), (19.4, 9.4)], 0.45), "l", 6, "dobras")
        # duas dobras do pano descendo na copa
        pinta(copa & tira([(13.2, 16.6), (12.0, 20.0)], 0.5), "l", 3, "dobras")
        pinta(copa & tira([(19.0, 14.6), (20.0, 19.4)], 0.5), "l", 2, "dobras")
        # a fita de linho na base da copa, curvando com a elipse
        frente = 23.2 + 2.2 * np.sqrt(np.clip(1 - ((x32 - 15.8) / 6.8) ** 2, 0, 1))   # a beira de baixo da copa
        fita = copa & (y32 > frente - 2.0) & (y32 < frente - 0.4)
        pinta(fita, "n", np.where(x32 < 12.0, 2, np.where(x32 < 19.0, 1, 0)), "fita")
    camadas = ["aba", "copa", "dobras", "fita", "contorno"]

if ETAPA == "final":
    tom = limpar(mat, tom, fixo)                                # sem pixel solto de um tom no meio de outro
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"{PECA}_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta / "listas", camadas)
