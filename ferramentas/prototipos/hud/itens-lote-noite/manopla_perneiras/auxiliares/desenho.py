# A manopla e as perneiras do Guerreiro (o remake do ferro, 3; proposta de 19/10/2026), com o ferro da espada, do elmo e
# da cota aprovados e o couro da família; a luz de cima e da esquerda. Primeiro o 32; o 64 é o 32 ampliado 2x (a política
# da skill); o 40 e o 48 depois da aprovação da forma. As medidas no quadro de 32. Vazias, sem ninguém dentro.
# Uso: python desenho.py <manopla|perneiras> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas, LUZ

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


def poligono(pts):
    dentro = np.zeros((N, N), bool)
    for i in range(len(pts)):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % len(pts)]
        dentro ^= ((ya > y32) != (yb > y32)) & (x32 < (xb - xa) * (y32 - ya) / ((yb - ya) or 1e-9) + xa)
    return dentro


def elipse(cx, cy, rx, ry):
    return ((x32 - cx) / rx) ** 2 + ((y32 - cy) / ry) ** 2 <= 1


def luz_esfera(cx, cy, rx, ry):
    """A iluminação de um volume arredondado (a normal de um elipsoide) pela luz da família."""
    nx = (x32 - cx) / rx; ny = (y32 - cy) / ry; nz = np.sqrt(np.clip(1 - nx * nx - ny * ny, 0, 1))
    return nx * LUZ[0] + ny * LUZ[1] + nz * LUZ[2]


def cilindro(x0, x1):
    """O tom de uma peça cilíndrica de pé entre x0 e x1 (a luz da esquerda): 0 na beira escura, 1 na faixa acesa."""
    u = np.clip((x32 - x0) / max(x1 - x0, 1e-9), 0, 1) * 2 - 1
    return np.clip(u * LUZ[0] / abs(LUZ[0]) * 0.55 + np.sqrt(np.clip(1 - u * u, 0, 1)) * 0.6, 0, 1)


if PECA == "manopla":
    # A manopla de placas, pela referência principal (ferramentas/arte/referencias/Luvas/tQXl+6.png, o par da caixa
    # (534, 148, 594, 202)), uma só, de pé e vista pelas costas da mão, como a luva de couro e a de seda da família: o
    # punho em duas lâminas que abrem para baixo (a manchete); a placa das costas da mão, abaulada; a placa dos nós
    # atravessando; os quatro dedos separados, cada um em segmentos (as juntas escuras), o do meio mais comprido; o
    # polegar saindo de lado, inclinado, também em segmentos. A forma antes das divisões: sem rebites.
    # as proporções da referência: os dedos em quase metade da altura; a mão curta; o pulso estreito separando a mão do
    # punho, que abre em sino até a barra
    punho = poligono([(10.6, 21.6), (21.4, 21.6), (22.0, 25.0), (23.2, 29.6), (8.8, 29.6), (10.0, 25.0)])
    pulso = (x32 > 11.0) & (x32 < 21.0) & (y32 > 19.4) & (y32 < 21.8)
    mao = poligono([(9.6, 13.6), (22.4, 13.6), (22.2, 17.4), (21.0, 19.8), (11.0, 19.8), (9.8, 17.4)])
    nos = poligono([(9.4, 12.0), (22.6, 12.0), (22.6, 14.0), (9.4, 14.0)])
    # os dedos: (x da esquerda, topo); 2 px de largura e 1 de vão, na grade (no 32); a ponta arredondada
    DEDOS = [(10.0, 4.0), (13.0, 2.0), (16.0, 2.8), (19.0, 5.0)]
    dedos = []
    for xd, topo in DEDOS:
        d = (x32 > xd) & (x32 < xd + 2.0) & (y32 > topo) & (y32 < 12.6)
        dedos.append((d, xd, topo))
    # o polegar: da beira da mão, à esquerda, saindo para fora na altura dos nós, em dois segmentos
    polegar = poligono([(10.4, 19.6), (10.0, 14.0), (7.4, 10.8), (5.0, 9.6), (3.6, 10.8), (4.6, 13.0), (6.8, 16.6), (8.2, 19.6)])
    peca = punho | pulso | mao | nos | polegar
    for d, _, _ in dedos:
        peca |= d
    if ETAPA == "silhueta":
        pinta(peca, "f", 5, "mao")
    else:
        # o punho: duas lâminas que abrem, cada uma um cilindro (a luz da esquerda), a de cima sobre a de baixo
        c = cilindro(8.0, 24.0)
        tp = np.select([c > 0.8, c > 0.55, c > 0.3], [7, 6, 5], 4)
        pinta(punho, "f", tp, "punho")
        pinta(punho & (y32 > 24.6) & (y32 < 25.6), "f", np.where(x32 < 16, 3, 2), "punho")        # a sombra da lâmina de cima
        pinta(punho & (y32 > 25.6) & (y32 < 26.6), "f", np.where(c > 0.55, 8, 6), "punho")       # a beira da de baixo, acesa
        pinta(punho & (y32 > 28.6), "f", np.where(x32 < 16, 4, 3), "punho")                      # a barra, virando
        pinta(punho & (y32 < 22.6), "f", np.where(c > 0.55, 8, 6), "punho")                      # a beira de cima, acesa
        pinta(pulso & ~punho, "f", np.where(x32 < 14, 3, 2), "punho")                            # o pulso, na sombra da mão
        # a mão: a placa abaulada pela luz da esfera; a placa dos nós como uma faixa com a beira de cima acesa
        li = luz_esfera(15.4, 15.8, 7.4, 5.0)
        pinta(mao, "f", np.select([li > 0.86, li > 0.66, li > 0.42], [8, 7, 6], 5), "mao")
        pinta(mao & (y32 > 18.8), "f", np.where(x32 < 16, 4, 3), "mao")
        pinta(nos, "f", np.where(x32 < 13, 7, np.where(x32 < 19, 6, 5)), "mao")
        pinta(nos & (y32 < 13.0), "f", np.where(x32 < 18, 8, 7), "mao")
        pinta(nos & (y32 > 13.4), "f", np.where(x32 < 16, 3, 2), "mao")                          # a sombra sobre a mão
        # os dedos: cada um um cilindro (a beira esquerda acesa, a direita escura), as juntas escuras atravessando
        for d, xd, topo in dedos:
            t = np.where(x32 < xd + 1.0, 7, 5)
            pinta(d, "f", t, "dedos")
            for yj in np.linspace(topo, 12.6, 4)[1:-1]:                                          # duas juntas por dedo
                pinta(d & (np.abs(y32 - yj - 0.4) < 0.5), "f", np.where(x32 < xd + 1.4, 4, 3), "dedos")
            pinta(d & (y32 < topo + 1.2), "f", np.where(x32 < xd + 1.0, 8, 6), "dedos")         # a ponta, na luz
        # o polegar: aceso por cima, a junta no meio, a base na sombra da mão
        pinta(polegar & ~mao & ~nos, "f", np.where(x32 + 0.7 * y32 < 15.6, 7, 5), "dedos")
        pinta(polegar & ~mao & ~nos & (np.abs(y32 + 1.0 * x32 - 20.4) < 0.6), "f", 3, "dedos")
        pinta(polegar & (mao | nos), "f", 4, "dedos")
    camadas = ["punho", "mao", "dedos", "contorno"]
else:
    # As perneiras de placas, rodada 2, pela orientação do Jean (19/10/2026, uma imagem de perneiras de placas mandada
    # na conversa): armadura de ferro, não uma calça. Sem o corpo de pano, o cinto e a cintura inteira: uma placa no
    # meio, em cima, ligando as duas pernas; cada perna uma cadeia de placas abauladas, uma sobre a outra (o coxote com a
    # ponta do quadril saindo para cima e para fora, a joelheira, a mais saliente, a greva até o tornozelo, que abre um
    # pouco); entre elas, os entalhes na silhueta. O vão entre as pernas aberto desde o alto: o arco. Vazias.
    def placa(lado, u, v, ru, rv):                                             # uma placa abaulada, pela distância ao eixo
        return elipse(16.0 + lado * u, v, ru, rv)
    PLACAS = {   # (u, v, ru, rv): o meio de cada placa e os raios, no quadro de 32
        "coxote": (7.2, 8.8, 3.8, 6.0),
        "joelheira": (7.0, 17.4, 3.9, 3.0),
        "greva": (6.8, 24.0, 2.8, 5.8),
    }
    def ponta(lado):                                                            # a ponta do quadril, para cima e para fora
        return poligono([(16.0 + lado * u, v) for u, v in [(7.6, 4.8), (12.8, 1.4), (11.0, 7.4)]])
    def pe(lado):                                                               # o tornozelo, abrindo um pouco
        return poligono([(16.0 + lado * u, v) for u, v in [(3.4, 27.8), (9.8, 27.8), (10.2, 29.6), (3.0, 29.6)]])
    centro = poligono([(11.4, 2.4), (20.6, 2.4), (19.4, 5.6), (17.0, 8.4), (15.0, 8.4), (12.6, 5.6)])
    partes = {}
    for lado in (-1, +1):
        for nome, (u, v, ru, rv) in PLACAS.items():
            partes[(nome, lado)] = placa(lado, u, v, ru, rv)
        partes[("ponta", lado)] = ponta(lado)
        partes[("pe", lado)] = pe(lado)
    peca = centro.copy()
    for m in partes.values():
        peca |= m
    peca &= (y32 > 1.0) & (y32 < 29.8)
    if ETAPA == "silhueta":
        pinta(peca, "f", 5, "coxotes")
    else:
        # de baixo para cima, cada placa por cima da seguinte: a greva, a joelheira, o coxote; cada uma pela luz da
        # esfera (o especular no alto à esquerda), a beira de baixo escura sobre a de baixo; a perna da direita um tom
        # abaixo. Por último a placa do meio, por cima dos coxotes.
        for lado in (-1, +1):
            menos = 0 if lado < 0 else 1
            cam_de = {"pe": "grevas", "greva": "grevas", "joelheira": "joelhos", "coxote": "coxotes", "ponta": "coxotes"}
            for nome in ("pe", "greva", "joelheira", "ponta", "coxote"):
                m = partes[(nome, lado)]
                if nome in PLACAS:
                    u, v, ru, rv = PLACAS[nome]
                    li = luz_esfera(16.0 + lado * u, v, ru, rv)
                    t = np.select([li > 0.92, li > 0.74, li > 0.5, li > 0.26], [8, 7, 6, 5], 4) - menos
                    pinta(m, "f", t, cam_de[nome])
                    beira = m & ~elipse(16.0 + lado * u, v - 0.6, ru, rv) & (y32 > v)      # a beira de baixo, virando
                    pinta(beira, "f", 3 - menos, cam_de[nome])
                elif nome == "pe":
                    pinta(m, "f", np.where(x32 < 16.0 + lado * 6.6, 5, 3) - menos, "grevas")
                else:
                    pinta(m, "f", np.where(y32 < 4.4, 7, 5) - menos, "coxotes")
        li = luz_esfera(16.0, 3.6, 3.6, 5.2)
        pinta(centro, "f", np.select([li > 0.8, li > 0.55], [7, 6], 4), "centro")
        pinta(centro & (y32 > 7.0), "f", 3, "centro")
    camadas = ["grevas", "joelhos", "coxotes", "centro", "contorno"]

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
