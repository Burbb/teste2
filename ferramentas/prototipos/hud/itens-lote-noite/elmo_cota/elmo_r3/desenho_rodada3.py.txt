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
    # O capacete, rodada 3, pela mesma referência principal (ferramentas/arte/referencias/capacete/5+N9Nb.png, o
    # capacete aberto da caixa (147, 479, 191, 532)), com as medidas tiradas dela: as formas são definidas nas
    # coordenadas da referência (R: x de 5 a 38, y de 6 a 47) e levadas ao quadro de 32 na mesma proporção (a peça mais
    # alta que larga). A peça está um pouco girada: a faixa da testa sobe da esquerda para a direita, com uma leve curva
    # (mais baixa no meio, mais perto); as faces descem inclinadas, a da esquerda entrando para a direita e mais longa, a
    # da direita mais curta; o nariz longo, até cerca de 2/3 da altura. A abertura: uma sombra curta do lado de dentro
    # da calota logo abaixo da faixa, e abaixo dela o vazio entre as faces (o fundo; sem travessa). As tiras e a faixa
    # são o mais claro, separadas da calota por uma emenda escura; a calota em volume um tom abaixo.
    ESC = 0.70
    xr = 21.0 + (x32 - 16.0) / ESC                                              # o quadro de 32 nas coordenadas da referência
    yr = 6.0 + (y32 - 2.2) / ESC
    def poli_r(pts):                                                            # um polígono dado nas coordenadas da referência
        return poligono([(16.0 + (x - 21.0) * ESC, 2.2 + (y - 6.0) * ESC) for x, y in pts])
    def yb(x):                                                                  # o meio da faixa da testa
        return 23.3 - 0.118 * (x - 7.0) + 0.5 * np.clip(1 - ((x - 19.5) / 14.0) ** 2, 0, 1)
    # a calota: uma elipse um pouco girada (como a faixa), até a faixa
    ang = np.deg2rad(-6.0)
    cx, cy = 20.6, 21.6
    u = (xr - cx) * np.cos(ang) + (yr - cy) * np.sin(ang); v = -(xr - cx) * np.sin(ang) + (yr - cy) * np.cos(ang)
    calota = ((u / 14.4) ** 2 + (v / 15.6) ** 2 <= 1) & (yr <= yb(xr) + 1.4)
    faixa = (np.abs(yr - yb(xr)) <= 1.6) & (xr >= 6.0) & (xr <= 34.8)
    fx = lambda y: 18.4 + 0.03 * (y - 6.0)                                      # a borda esquerda da tira e do nariz
    tira = (xr >= fx(yr)) & (xr <= fx(yr) + 3.2) & calota & (yr < yb(xr))
    nariz = poli_r([(18.9, 22.0), (22.2, 22.0), (22.0, 31.0), (21.0, 34.2), (19.8, 34.2), (19.0, 31.0)])
    face_e = poli_r([(5.0, 23.4), (10.6, 24.6), (14.2, 44.6), (12.6, 47.6), (9.2, 47.6), (5.6, 30.0)])
    face_d = poli_r([(31.2, 22.4), (37.2, 22.0), (38.4, 30.0), (38.0, 42.8), (35.0, 44.0), (32.8, 30.0)])
    # a sombra do lado de dentro: logo abaixo da faixa, entre as faces, curta (mais funda junto do nariz e da esquerda)
    fundo = (yr > yb(xr) + 1.0) & (yr < yb(xr) + 4.2 - 0.06 * np.clip(xr - 22.0, 0, 20)) & (xr > 9.0) & (xr < 33.6)
    metal = calota | faixa | tira | nariz | face_e | face_d
    if ETAPA == "silhueta":
        pinta(metal, "f", 5, "calota")
        pinta(fundo & ~metal, "f", 1, "interior")
    else:
        pinta(fundo & ~metal, "f", np.where(yr < yb(xr) + 2.6, 0, 1), "interior")
        # a calota: a luz da família pelo volume, um tom abaixo das tiras; a emenda escura junto da tira e da faixa
        li = luz_esfera(16.0 + (cx - 21.0) * ESC, 2.2 + (cy - 6.0) * ESC, 14.4 * ESC + 0.6, 15.6 * ESC)
        pinta(calota, "f", np.select([li > 0.82, li > 0.6, li > 0.36], [7, 6, 5], 4), "calota")
        emenda = calota & ~tira & ~faixa & ((np.abs(xr - fx(yr)) < 1.2 / ESC * 0.6) | (np.abs(xr - (fx(yr) + 3.2)) < 1.2 / ESC * 0.6) | (yr > yb(xr) - 2.6))
        pinta(emenda, "f", 3, "calota")
        # a tira e o nariz: claros à esquerda, a beira direita um tom abaixo; a ponta do nariz na sombra
        pinta(tira, "f", np.where(xr < fx(yr) + 2.0, 8, 6), "tiras")
        pinta(nariz, "f", np.where(xr < 20.8, 8, 5), "tiras")
        pinta(nariz & (yr > 32.4), "f", 4, "tiras")
        # a faixa da testa: a beira de cima acesa, o meio claro, a de baixo escura (a espessura); mais escura à direita
        tf = np.where(yr < yb(xr) - 0.5, 8, np.where(yr < yb(xr) + 0.7, 7, 3))
        tf = np.where((xr > 27.0) & (tf > 3), tf - 2, tf)
        pinta(faixa, "f", tf, "tiras")
        # as faces: a da esquerda na luz (a beira de dentro clara, a de fora um tom abaixo), a da direita na sombra; as
        # pontas de baixo escurecendo
        pinta(face_e, "f", 5, "faces")
        pinta(face_e & (xr > 7.8 + 0.2 * (yr - 24.0)), "f", 7, "faces")
        pinta(face_d, "f", 4, "faces")
        pinta(face_d & (xr < 35.0), "f", 6, "faces")
        pinta((face_e & (yr > 44.0)) | (face_d & (yr > 40.6)), "f", 3, "faces")
    camadas = ["interior", "calota", "faces", "tiras", "contorno"]
else:
    # A cota de malha, rodada 2, pela referência principal (ferramentas/arte/referencias/peitoral/etbij8.png, o nº 103 do
    # índice: a camisa de malha de aço de frente): a gola é a própria malha, com a beira clara e o vão escuro do pescoço
    # (vê-se o lado de dentro das costas); os ombros caem nas mangas curtas, que abrem; o corpo abre um pouco para baixo;
    # as mangas e a barra acabam na malha, com a beira em dentes; o cinto de couro com a fivela de ferro quebra a
    # silhueta. O volume primeiro: a luz da esquerda no peito, os lados e as axilas na sombra, as mangas abaixo; a malha
    # em anéis numa grade deslocada por cima, seguindo esse volume.
    corpo = poligono([(10.0, 4.8), (22.0, 4.8), (24.4, 7.2), (24.2, 18.0), (25.0, 27.0), (7.0, 27.0), (7.8, 18.0), (7.6, 7.2)])
    manga_e = poligono([(8.8, 5.6), (4.8, 8.0), (2.2, 16.8), (7.6, 17.6), (8.2, 11.6)])
    manga_d = poligono([(23.2, 5.6), (27.2, 8.0), (29.8, 16.8), (24.4, 17.6), (23.8, 11.6)])
    mangas = (manga_e | manga_d) & ~corpo
    pescoco = poligono([(12.0, 4.2), (20.0, 4.2), (19.6, 6.6), (17.6, 8.6), (14.4, 8.6), (12.4, 6.6)])
    beira_gola = poligono([(10.8, 3.8), (21.2, 3.8), (20.8, 7.0), (18.2, 9.8), (13.8, 9.8), (11.2, 7.0)]) & ~pescoco
    cinto = corpo & (y32 > 19.0) & (y32 < 21.4)
    fivela = poligono([(17.0, 18.6), (20.0, 18.6), (20.0, 21.8), (17.0, 21.8)])
    # a malha e os dentes na grade de pixels de cada tamanho (no 32, o mesmo que o quadro de 32): os anéis ficam do mesmo
    # tamanho em pixels em todos os tamanhos, em vez de esticar com a escala
    xi = np.floor(X).astype(int); yi = np.floor(Y).astype(int)
    dentes = ((xi % 2) == 1)                                                    # a beira da malha em dentes (barra e mangas)
    barra_dente = corpo & (y32 > 26.0) & dentes
    manga_dente = mangas & (y32 > 16.6) & dentes
    peca = (corpo | mangas) & ~barra_dente & ~manga_dente
    if ETAPA == "silhueta":
        pinta(peca, "f", 5, "malha")
        pinta(pescoco, "f", 1, "malha")
    else:
        # o volume: a luz da esquerda no peito em faixas largas; os lados e as axilas na sombra; as mangas, a da
        # esquerda na luz, a da direita na sombra; a parte de baixo (abaixo do cinto) um tom abaixo
        tv = np.where(x32 < 11.0, 6, np.where(x32 < 16.5, 6, np.where(x32 < 21.0, 5, 4)))
        tv = np.where((x32 > 11.0) & (x32 < 16.5) & (y32 < 14.0), 7, tv)          # o alto do peito, o mais claro
        tv = np.where(y32 > 21.4, tv - 1, tv)
        tv = np.where(mangas, np.where(x32 < 16, 5, 3), tv)
        tv = np.where(corpo & ((x32 < 9.2) | (x32 > 22.8)) & (y32 > 8.0), np.minimum(tv, 3), tv)   # os lados e as axilas
        # a malha: anéis numa grade deslocada (o alto de cada anel um tom acima, a base um tom abaixo)
        des = (yi // 2) % 2
        alto = ((yi % 2) == 0) & (((xi + des) % 2) == 0)
        base = ((yi % 2) == 1) & (((xi + des) % 2) == 0)
        anel = np.clip(np.where(alto, tv + 1, np.where(base, tv - 1, tv)), 1, 8)
        if N != 32:   # nos maiores, o alto do peito mais claro só nos topos dos anéis (sem um bloco de borda reta)
            peito = (x32 > 11.0) & (x32 < 16.5) & (y32 < 14.0)
            anel = np.where(peito & ~alto & ~base, 6, anel)
        pinta(peca, "f", anel, "malha")
        fixo[(alto | base) & peca] = True
        # a gola: a beira da malha clara em volta do vão; o vão do pescoço, escuro (o lado de dentro das costas)
        pinta(beira_gola & peca, "f", np.where(x32 < 16, 7, 5), "malha")
        pinta(pescoco, "f", np.where(y32 > 6.6, 2, np.where(y32 > 5.4, 1, 0)), "malha")
        # o cinto de couro e a fivela de ferro
        pinta(cinto, "k", np.where(x32 < 12.0, 5, np.where(x32 < 20.0, 4, 2)), "couro")
        pinta(fivela, "f", 7, "ferragem")
        pinta(fivela & (x32 > 17.8) & (x32 < 19.2) & (y32 > 19.4) & (y32 < 21.0), "k", 1, "ferragem")
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
