# As peças de tecido do Mago (lote 3 da noite de 19/10): a Calça de Viagem (calca_tecido) e o Manto (manto), na lã
# azul-acinzentada do capuz de tecido aprovado (a mesma rampa) e com a luz de cima e da esquerda. A construção é a
# mesma em 32, 40 e 48 (as medidas em frações do quadro de 32); o 64 é o 32 ampliado 2x (a política da skill).
# Uso: python tecido.py <calca|manto> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, listas_camadas

PECA = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {
    "l": ["#10131C", "#1C2230", "#2A3346", "#3B4760", "#4F5E7C", "#667696", "#8392B0"],   # a lã (a do capuz de tecido)
    "n": ["#5A4A36", "#8A7656", "#BCA67E", "#E2D2AA"],                                  # o cordão e as faixas (linho cru; "c" é o contorno)
    "d": ["#3A4864", "#6476A0", "#8494BE", "#B4C2E0"],                                  # o debrum (a seda da luva)
    "b": ["#5E3E14", "#946422", "#C89434", "#EED070"],                                  # o latão do broche
}
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
x32, y32 = X / K, Y / K                                         # as coordenadas no quadro de 32


def poligono(pts):
    """Os pixels (pelo centro) dentro do polígono de pontos no quadro de 32."""
    dentro = np.zeros((N, N), bool)
    n = len(pts)
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
        cruza = ((ya > y32) != (yb > y32)) & (x32 < (xb - xa) * (y32 - ya) / ((yb - ya) or 1e-9) + xa)
        dentro ^= cruza
    return dentro


def pinta(onde, m, t, c):
    mat[onde] = m; tom[onde] = t if np.isscalar(t) else t[onde]; cam[onde] = c


def segmento(xa, ya, xb, yb, larg=0.75):
    """Os pixels perto do segmento (no quadro de 32): um vinco, um cordão."""
    dx, dy = xb - xa, yb - ya; L2 = dx * dx + dy * dy
    t = np.clip(((x32 - xa) * dx + (y32 - ya) * dy) / L2, 0, 1)
    return np.hypot(x32 - (xa + t * dx), y32 - (ya + t * dy)) * K <= larg


if PECA == "calca":
    cintura = poligono([(8.6, 3.6), (23.4, 3.6), (23.6, 7.6), (8.4, 7.6)])
    esq = poligono([(8.4, 7.4), (16.2, 7.4), (16.0, 13.0), (15.0, 22.0), (14.6, 27.6), (8.0, 27.6), (7.0, 22.0)])
    dir_ = poligono([(15.8, 7.4), (23.6, 7.4), (25.0, 22.0), (24.0, 27.6), (17.4, 27.6), (17.0, 22.0), (16.0, 13.0)])
    barra_e = poligono([(7.8, 23.4), (14.8, 23.4), (14.6, 28.2), (8.2, 28.2)])
    barra_d = poligono([(17.2, 23.4), (24.2, 23.4), (23.8, 28.2), (17.4, 28.2)])
    pernas = (esq | dir_) & ~cintura
    if ETAPA == "silhueta":
        pinta(pernas | cintura | barra_e | barra_d, "l", 4, "pernas")
    else:
        # as pernas: a luz da esquerda em faixas largas por perna; a do meio um pouco na sombra
        t = np.where(esq, np.where(x32 < 10.6, 5, np.where(x32 < 13.6, 4, 3)),
                     np.where(x32 < 19.0, 4, np.where(x32 < 22.2, 3, 2)))
        t = np.where((y32 > 20.4) & (y32 < 23.4), t - 1, t)                     # o franzido sobre a faixa
        pinta(pernas, "l", t, "pernas")
        # os vincos: diagonais da coxa e o franzido no joelho, cada um com a beira clara embaixo
        dobras = np.zeros((N, N), bool); claros = np.zeros((N, N), bool)
        for xa, ya, xb, yb in ((14.6, 10.0, 12.0, 13.0), (13.4, 17.0, 10.8, 19.0), (17.6, 10.0, 20.2, 12.8), (18.6, 17.2, 21.4, 19.2)):
            dobras |= segmento(xa, ya, xb, yb, 0.5)
            claros |= segmento(xa, ya + 1.0, xb, yb + 1.0, 0.45)
        pinta(dobras & pernas, "l", np.maximum(t - 1, 0), "dobras")
        pinta(claros & pernas & ~dobras, "l", np.minimum(t + 1, 6), "dobras")
        # a cintura dobrada e o cordão com o laço
        tc = np.where(y32 < 4.8, 5, np.where(x32 < 16, 4, 3))
        pinta(cintura, "l", tc, "cintura")
        cordao = cintura & (np.abs(y32 - 5.9) < 0.6)
        cordao |= segmento(15.6, 6.2, 14.4, 10.2, 0.5) | segmento(16.4, 6.2, 17.4, 10.6, 0.5)
        pinta(cordao, "n", np.where(x32 < 16, 3, 2), "cordao")
        # as faixas dos tornozelos: o linho enrolado em voltas inclinadas
        barras = (barra_e | barra_d) & ~cordao
        volta = (np.floor((y32 - x32 * 0.35) / 1.6) % 2).astype(int)
        pinta(barras, "n", np.where(volta == 1, 1, np.where(x32 % 16 < 11.5, 3, 2)), "barra")
    camadas = ["pernas", "dobras", "barra", "cintura", "cordao", "contorno"]
else:
    # o manto em partes: a gola, o tronco que afina até a cintura, a saia que abre até a barra e as mangas largas, que
    # saem dos ombros para fora (separadas do corpo por uma costura escura); a frente aberta da cintura à barra
    gola = poligono([(11.6, 3.6), (20.4, 3.6), (21.4, 7.0), (10.6, 7.0)])
    tronco = poligono([(9.8, 6.4), (22.2, 6.4), (21.2, 16.4), (10.8, 16.4)])
    saia = poligono([(10.8, 15.6), (21.2, 15.6), (25.0, 29.2), (7.0, 29.2)])
    manga_e = poligono([(10.4, 6.6), (7.2, 7.8), (3.0, 18.0), (3.4, 20.4), (9.0, 20.4), (10.8, 12.4)])
    manga_d = poligono([(21.6, 6.6), (24.8, 7.8), (29.0, 18.0), (28.6, 20.4), (23.0, 20.4), (21.2, 12.4)])
    corpo = (tronco | saia) & ~gola
    mangas = (manga_e | manga_d) & ~corpo & ~gola
    abertura = poligono([(16.0, 17.2), (19.6, 29.2), (12.4, 29.2)])
    if ETAPA == "silhueta":
        pinta(corpo | mangas | gola, "l", 4, "corpo")
    else:
        tb = np.where(x32 < 12.0, 5, np.where(x32 < 16.0, 4, np.where(x32 < 20.0, 3, 2)))
        pinta(corpo & ~abertura, "l", tb, "corpo")
        for xp in (11.0, 21.0):                                                # as pregas da saia
            prega = saia & ~abertura & (np.abs(x32 - (xp + (y32 - 20) * (-0.16 if xp < 16 else 0.16))) < 0.5) & (y32 > 19.4)
            pinta(prega, "l", np.maximum(tb - 1, 0), "corpo")
        tm = np.where(x32 < 16, np.where(x32 < 6.0, 5, 4), np.where(x32 < 26.0, 2, 1))
        pinta(mangas, "l", tm, "mangas")
        pinta(mangas & (y32 > 18.8), "l", 0, "mangas")                         # a boca da manga: o vão escuro
        costura = np.zeros((N, N), bool)                                       # a manga encostada no corpo
        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            costura |= np.roll(np.roll(corpo, b, 0), a, 1)
        pinta(mangas & costura, "l", 1, "mangas")
        pinta(abertura, "l", np.where(x32 < 15.0, 1, 0), "forro")
        borda = (segmento(16.0, 17.2, 12.4, 29.2, 0.55) | segmento(16.0, 17.2, 19.6, 29.2, 0.55)) & saia
        pinta(borda, "d", np.where(x32 < 16, 3, 1), "debrum")
        pinta(gola, "l", np.where(x32 < 14.0, 5, np.where(x32 < 18.0, 4, 3)), "gola")
        pinta(gola & (y32 > 6.2), "d", np.where(x32 < 16, 2, 1), "debrum")
        faixa = corpo & (np.abs(y32 - 16.4) < 1.0)
        pinta(faixa, "n", np.where(x32 < 13.0, 2, np.where(x32 < 19.0, 1, 0)), "faixa")
        pinta(segmento(16.8, 17.2, 17.8, 20.6, 0.5) & corpo, "n", 1, "faixa")
        broche = (np.abs(x32 - 16.0) < 1.1) & (np.abs(y32 - 7.2) < 1.1)
        pinta(broche, "b", np.where((x32 < 16) & (y32 < 7.2), 3, 2), "fecho")
    camadas = ["mangas", "corpo", "forro", "gola", "debrum", "faixa", "fecho", "contorno"]

mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
nome = "calca_tecido" if PECA == "calca" else "manto"
img.save(pasta / f"{nome}_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta, camadas)
print("\n".join("".join("#" if mat[y, x] == "c" else (mat[y, x] + str(tom[y, x])) if mat[y, x] else ".." for x in range(N)) for y in range(N)))
