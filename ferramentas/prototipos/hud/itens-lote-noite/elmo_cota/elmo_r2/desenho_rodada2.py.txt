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
    # O capacete, rodada 2, pela referência principal (ferramentas/arte/referencias/capacete/5+N9Nb.png, o nº 62 do
    # índice: o elmo aberto de frente, um pouco de cima): a calota arredondada com a tira vertical no meio, a faixa da
    # testa contornando a peça em curva (mais baixa no meio, que está mais perto), a tira que desce da calota e vira o
    # protetor do nariz, as duas faces laterais descendo até embaixo, e entre elas o fundo escuro do interior até cerca de
    # 3/4 da altura, com o vazio abaixo (a profundidade da abertura). As tiras e as faces com a beira clara (a espessura da
    # chapa) e a beira de dentro escura. Ferro do machado e da espada; sem latão, sem crista.
    # o ângulo da referência: de frente, um pouco virado (vê-se mais o lado direito): a frente (a tira e o nariz) fica à
    # esquerda do meio, a face da esquerda aparece estreita, quase de perfil, e a da direita larga
    CX, CY, RX, RY = 16.2, 13.4, 12.6, 10.8
    FX = 13.6                                                                   # a linha da frente (a tira e o nariz)
    calota = elipse(CX, CY, RX, RY) & (y32 <= CY + 0.6)
    def yb(x):                                                                  # o meio da faixa da testa: mais baixa na frente
        return CY - 0.4 + 2.4 * np.clip(1 - ((x - FX) / (RX + 2.6)) ** 2, 0, 1)
    faixa = (np.abs(y32 - yb(x32)) <= 1.3) & (np.abs(x32 - CX) <= RX)
    face_e = poligono([(3.6, CY - 0.2), (6.6, CY + 1.2), (6.4, 26.0), (5.8, 30.0), (4.0, 29.8), (3.6, 22.0)])
    face_d = poligono([(28.8, CY - 0.2), (22.6, CY + 1.4), (23.2, 25.0), (24.6, 30.0), (28.0, 29.8), (28.6, 22.0)])
    tira = (np.abs(x32 - FX) <= 1.3) & (y32 <= yb(x32)) & (elipse(CX, CY, RX, RY) | (y32 > CY))
    nariz = poligono([(FX - 1.3, 14.6), (FX + 1.3, 14.6), (FX + 1.15, 20.6), (FX + 0.6, 21.8), (FX - 0.6, 21.8), (FX - 1.15, 20.6)])
    # o fundo do interior: a parede de trás vista pela abertura, entre as faces, até a borda de trás (a 3/4 da altura);
    # abaixo dela, entre as faces, o vazio
    def yfundo(x):
        return 23.8 + 1.4 * np.sqrt(np.clip(1 - ((x - 15.0) / 8.6) ** 2, 0, 1))
    interior = (x32 > 6.2) & (x32 < 23.4) & (y32 > yb(x32)) & (y32 < yfundo(x32))
    metal = calota | faixa | face_e | face_d | tira | nariz
    if ETAPA == "silhueta":
        pinta(metal, "f", 5, "calota")
        pinta(interior & ~metal, "f", 1, "interior")
    else:
        # o interior: escuro no alto (a sombra da calota), um pouco mais claro embaixo, junto da borda de trás
        pinta(interior, "f", np.where(y32 > yfundo(x32) - 1.6, 2, np.where(y32 > 19.0, 1, 0)), "interior")
        # a calota em volume: a luz da família em faixas largas, o brilho agrupado em cima à esquerda
        li = luz_esfera(CX - 0.5, CY + 1.5, RX + 0.6, RY + 3.0)
        pinta(calota, "f", np.select([li > 0.93, li > 0.74, li > 0.5], [7, 6, 5], 4), "calota")   # as tiras, o mais claro
        pinta(calota & (x32 > CX + 9.0), "f", 3, "calota")                      # a curva que vira para o lado de trás
        # as faces laterais: a da esquerda na luz, a da direita na sombra; a beira de fora clara, a de dentro escura
        pinta(face_e, "f", 6, "faces"); pinta(face_d, "f", 4, "faces")
        pinta(face_e & (x32 < 4.6), "f", 7, "faces"); pinta(face_e & (x32 > 5.6), "f", 3, "faces")
        pinta(face_d & (x32 > 27.4), "f", 5, "faces"); pinta(face_d & (x32 < 24.0), "f", 2, "faces")
        pinta((face_e | face_d) & (y32 > 27.6), "f", 2, "faces")                # a barra, virando para dentro
        # a faixa da testa: a beira de cima clara, a de baixo escura (a espessura); a direita na sombra
        tf = np.where(y32 < yb(x32) - 0.35, np.where(x32 < CX + 5, 8, 6), np.where(y32 < yb(x32) + 0.55, np.where(x32 < CX + 5, 7, 5), 2))
        pinta(faixa, "f", tf, "tiras")
        # a tira da calota e o nariz: clara à esquerda, escura à direita
        pinta(tira, "f", np.where(x32 < FX, 8, 6), "tiras")
        pinta(nariz, "f", np.where(x32 < FX - 0.2, 8, 5), "tiras")
        pinta(nariz & (y32 > 20.8), "f", 3, "tiras")
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
    xi = np.floor(x32).astype(int); yi = np.floor(y32).astype(int)
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
