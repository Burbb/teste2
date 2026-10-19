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
    # O capacete, rodada 4, pela nova referência principal do Jean (ferramentas/arte/referencias/capacete/
    # elmo-frente-jean.webp, a coluna da direita): em pé e de frente, com o eixo vertical. A calota arredondada com a
    # tira vertical no centro; a faixa da testa horizontal, um pouco mais larga que a calota (a aba), com espessura; o
    # protetor do nariz centralizado; uma sombra curta do lado de dentro logo abaixo da faixa e, abaixo dela, o vazio
    # entre as faces; as duas faces simétricas, abrindo um pouco para fora e voltando embaixo, separadas do nariz. A
    # construção alinhada e simétrica; a luz da família (de cima e da esquerda) assimétrica: a calota em facetas, clara à
    # esquerda; as faces com o lado de dentro aceso e a beira de fora escura; o nariz claro à esquerda.
    CX = 16.0
    calota = elipse(CX, 13.4, 10.4, 10.8) & (y32 <= 13.4)
    faixa = (y32 > 12.6) & (y32 < 14.8) & (np.abs(x32 - CX) <= 11.6)
    tira = (np.abs(x32 - CX) <= 1.05) & calota
    nariz = poligono([(CX - 1.05, 14.0), (CX + 1.05, 14.0), (CX + 1.05, 19.6), (CX + 0.5, 20.8), (CX - 0.5, 20.8), (CX - 1.05, 19.6)])
    # uma face, pela distância ao eixo (u) e pela altura (v): a beira de dentro quase reta (7,2 a 7,6 do eixo); a de fora
    # larga sob a faixa e entrando para baixo (de 12 até 10,4), a ponta arredondada: a face afina como na referência
    # embaixo a face vira para dentro, fechando sobre o rosto (o pé de cada face aponta para o nariz)
    FACE = [(12.0, 14.6), (7.2, 14.6), (7.4, 18.0), (7.6, 25.2), (6.8, 26.8), (5.8, 28.2), (5.8, 29.4), (9.8, 29.4),
            (10.6, 27.4), (11.4, 20.0), (12.0, 16.4)]
    fora = lambda v: np.interp(v, [14.6, 16.4, 20.0, 27.4, 29.4], [12.0, 12.0, 11.4, 10.6, 9.8])
    def face(lado):                                                             # lado: -1 a da esquerda, +1 a da direita
        return poligono([(CX + lado * u, v) for u, v in FACE])
    face_e = face(-1); face_d = face(+1)
    fundo = (y32 > 14.6) & (y32 < 16.6) & (np.abs(x32 - CX) < 7.6)          # a sombra do lado de dentro, curta
    metal = calota | faixa | tira | nariz | face_e | face_d
    if ETAPA == "silhueta":
        pinta(metal, "f", 5, "calota")
        pinta(fundo & ~metal, "f", 1, "interior")
    else:
        pinta(fundo & ~metal, "f", np.where(y32 < 15.6, 0, 1), "interior")
        # a calota em facetas: clara à esquerda da tira (mais clara no alto), escura à direita, a beira de baixo um tom
        # abaixo; a emenda escura junto da tira (do lado da sombra)
        tc = np.where(x32 < CX, np.where((y32 < 8.4) & (x32 > 8.6), 7, 6), np.where(x32 < CX + 5.0, 5, 4))
        tc = np.where((x32 < CX) & (x32 < 9.0), 5, tc)
        tc = np.where(y32 > 11.4, tc - 1, tc)
        pinta(calota, "f", tc, "calota")
        pinta(calota & (x32 > CX + 1.05) & (x32 < CX + 2.1), "f", 3, "calota")
        # a tira e o nariz: o mais claro, a beira direita um tom abaixo; a ponta do nariz na sombra
        pinta(tira, "f", np.where(x32 < CX, 8, 7), "tiras")
        pinta(nariz, "f", np.where(x32 < CX, 8, 5), "tiras")
        pinta(nariz & (y32 > 19.6), "f", 4, "tiras")
        # a faixa: a beira de cima acesa, a de baixo escura (a espessura), mais escura à direita
        pinta(faixa, "f", np.where(y32 < 13.6, 8, np.where(x32 < CX + 3, 6, 4)), "tiras")
        pinta(faixa & (y32 > 14.0), "f", np.where(x32 < CX, 3, 2), "tiras")
        # as faces: o lado de dentro aceso, o de fora escuro; a da esquerda mais clara; as pontas de baixo escurecendo
        de = np.abs(x32 - CX); borda = de > fora(y32) - 1.05                    # a beira de fora, 1 px
        pinta(face_e, "f", np.where(borda, 3, np.where(de < 9.0, 7, 5)), "faces")
        pinta(face_d, "f", np.where(borda, 2, np.where(de < 9.0, 5, 4)), "faces")
        # o pé que vira para dentro: o alto dele aceso (pega a luz de cima), a ponta de baixo escurecendo
        pe = (face_e | face_d) & (de < 7.4) & (y32 > 25.6)
        pinta(pe, "f", np.where(x32 < CX, 6, 4), "faces")
        pinta((face_e | face_d) & (y32 > 28.2), "f", np.where(x32 < CX, 4, 2), "faces")
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
