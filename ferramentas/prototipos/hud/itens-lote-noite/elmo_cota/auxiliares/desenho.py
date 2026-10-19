# O elmo e a cota do Guerreiro (o remake do ferro, 2; proposta de 19/10/2026), com o ferro do machado e da espada
# aprovados, o latão do escudo e o couro da família; a luz de cima e da esquerda. Primeiro o 32; o 64 é o 32 ampliado 2x
# (a política da skill); o 40 e o 48 depois da aprovação da forma. As medidas no quadro de 32.
# Uso: python desenho.py <elmo|cota> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas, LUZ

PECA = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {
    "f": ["#0e0f11", "#1a1c20", "#282b31", "#383c44", "#4c5159", "#646a73", "#848b94", "#b0b6bd", "#e4e8ec"],   # o ferro
    "o": ["#26170a", "#40270c", "#623c12", "#8a571b", "#ae7526", "#cf9737", "#e9bb5c", "#f8dc94"],              # o latão
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


if PECA == "elmo":
    # O elmo de ferro (uma barbuta) em três quartos, virado um pouco para a esquerda: a calota arredondada com a crista
    # no alto, a faixa da testa de latão com os rebites, a borda de baixo contínua (a nuca mais baixa atrás) e a abertura
    # em T na frente (o vão dos olhos sob a faixa e o vão do rosto descendo), escura: o interior vazio.
    C = (16.4, 13.8); RX, RY = 11.0, 10.6
    calota = elipse(*C, RX, RY) & (y32 < C[1] + 0.5)
    corpo = poligono([(5.4, 13.6), (27.4, 13.6), (28.2, 21.0), (29.0, 27.2), (24.0, 28.0), (16.0, 27.4), (9.0, 27.8),
                      (5.2, 27.2), (5.0, 20.0)])
    elmo = calota | corpo
    CF = 12.0                                                                  # o meio da frente (virada à esquerda)
    olhos = poligono([(6.2, 17.0), (CF + 6.0, 17.0), (CF + 5.6, 19.6), (6.4, 19.6)])
    rosto = poligono([(CF - 2.2, 19.0), (CF + 2.2, 19.0), (CF + 2.0, 28.4), (CF - 2.0, 28.4)])
    abertura = (olhos | rosto) & elmo
    yf = lambda x: 15.2 + 0.09 * (x - CF)                                      # a faixa da testa (sobe para trás)
    faixa = elmo & (np.abs(y32 - yf(x32)) < 1.05)
    if ETAPA == "silhueta":
        pinta(elmo & ~abertura, "f", 5, "calota")
        pinta(abertura, "f", 1, "interior")
    else:
        li = luz_esfera(C[0] - 1.0, C[1] + 3.0, RX + 1.0, RY + 5.0)
        tc = np.select([li > 0.97, li > 0.88, li > 0.7, li > 0.48, li > 0.24], [8, 7, 6, 5, 4], 3)
        tc = np.where(x32 > 24.6, np.minimum(tc, 3), tc)                       # a lateral que vira para trás
        pinta(elmo, "f", tc, "calota")
        # a barra de baixo, um tom abaixo (a espessura da chapa virando para dentro)
        pinta(corpo & (y32 > 26.2), "f", np.maximum(np.where(x32 < 16, 4, 2), 2), "calota")
        # a crista: a linha clara no alto da calota, com a sombra à direita
        crista = elmo & (np.abs(x32 - (CF + 2.6)) < 0.5) & (y32 < yf(x32) - 1.2)
        pinta(crista, "f", 8, "calota"); fixo[crista] = True
        sombra = elmo & (np.abs(x32 - (CF + 3.6)) < 0.5) & (y32 < yf(x32) - 1.2) & (y32 > 4.5)
        pinta(sombra, "f", 5, "calota"); fixo[sombra] = True
        # o interior: escuro; mais claro embaixo à direita (a parede de dentro, do outro lado)
        pinta(abertura, "f", np.where((y32 > 22.0) & (x32 > CF), 1, 0), "interior")
        # a faixa da testa de latão, com os rebites
        pinta(faixa, "o", np.where(x32 < 11.0, 6, np.where(x32 < 21.0, 5, 3)), "faixa")
        for xr in (7.6, 19.6, 24.6):
            rb = (np.hypot(x32 - xr, y32 - yf(xr)) * K <= max(0.6 * K, 0.5)) & faixa
            pinta(rb, "o", 7 if xr < 20 else 5, "faixa"); fixo[rb] = True
    camadas = ["calota", "interior", "faixa", "contorno"]
else:
    # A cota de malha de frente: a gola de couro, os ombros, as mangas curtas abrindo, o corpo até a barra; a malha em
    # fileiras de pequenos anéis (o alto de cada anel claro, a base escura) que seguem o volume (a luz da esquerda pelo
    # corpo, as mangas um tom abaixo); o cinto de couro com a fivela de ferro; as barras de couro nas mangas e embaixo.
    corpo = poligono([(9.6, 5.4), (22.4, 5.4), (24.4, 7.4), (24.0, 27.4), (8.0, 27.4), (7.6, 7.4)])
    manga_e = poligono([(8.6, 6.0), (4.6, 8.4), (2.4, 17.0), (7.6, 17.6), (8.4, 12.0)])
    manga_d = poligono([(23.4, 6.0), (27.4, 8.4), (29.6, 17.0), (24.4, 17.6), (23.6, 12.0)])
    mangas = (manga_e | manga_d) & ~corpo
    gola = poligono([(11.0, 4.4), (21.0, 4.4), (20.2, 8.0), (16.0, 9.6), (11.8, 8.0)])
    pescoco = poligono([(12.8, 4.6), (19.2, 4.6), (18.6, 6.8), (16.0, 7.8), (13.4, 6.8)])
    cinto = corpo & (y32 > 19.2) & (y32 < 21.6)
    fivela = poligono([(14.4, 18.8), (17.8, 18.8), (17.8, 22.0), (14.4, 22.0)])
    barra = corpo & (y32 > 25.6)
    punhos = mangas & (y32 > 15.6)
    if ETAPA == "silhueta":
        pinta(corpo | mangas | gola, "f", 5, "malha")
    else:
        # o volume: a luz da esquerda em faixas largas pelo corpo; as mangas, a esquerda na luz, a direita na sombra
        tv = np.where(x32 < 11.5, 6, np.where(x32 < 17.0, 5, np.where(x32 < 21.5, 4, 3)))
        tv = np.where(mangas, np.where(x32 < 16, 5, 2), tv)
        # a malha: anéis numa grade deslocada (a cada 2 px na fileira, a fileira seguinte meio passo ao lado): o alto de
        # cada anel um tom acima do volume, a base logo abaixo um tom abaixo; entre eles, o tom do volume. Grupos
        # pequenos que seguem o corpo, sem xadrez de pixel a pixel nem faixas inteiras.
        xi = np.floor(x32).astype(int); yi = np.floor(y32).astype(int)
        des = (yi // 2) % 2
        alto = ((yi % 2) == 0) & (((xi + des) % 2) == 0)
        base = ((yi % 2) == 1) & (((xi + des) % 2) == 0)
        anel = np.clip(np.where(alto, tv + 1, np.where(base, tv - 1, tv)), 1, 8)
        pinta(corpo | mangas, "f", anel, "malha")
        fixo[(alto | base) & (corpo | mangas)] = True
        # a sombra embaixo dos braços e dos lados do corpo
        pinta(corpo & ((x32 < 9.0) | (x32 > 23.0)) & (y32 > 9.0), "f", 2, "malha")
        # as barras de couro: punhos e a barra de baixo; a gola de couro com o vão do pescoço escuro
        pinta(punhos, "k", np.where(x32 < 16, 4, 2), "couro")
        pinta(barra, "k", np.where(x32 < 12.0, 5, np.where(x32 < 20.0, 4, 3)), "couro")
        pinta(gola, "k", np.where(x32 < 14.0, 5, np.where(x32 < 18.0, 4, 3)), "couro")
        pinta(pescoco, "k", 0, "couro")
        # o cinto de couro e a fivela de ferro
        pinta(cinto, "k", np.where(x32 < 12.0, 5, np.where(x32 < 20.0, 4, 2)), "couro")
        pinta(fivela, "f", 7, "ferragem")
        pinta(fivela & (x32 > 15.2) & (x32 < 17.0) & (y32 > 19.6) & (y32 < 21.2), "k", 1, "ferragem")
    camadas = ["malha", "couro", "ferragem", "contorno"]

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
