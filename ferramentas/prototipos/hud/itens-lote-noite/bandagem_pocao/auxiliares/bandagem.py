# A Bandagem (16, 24, 32): um rolo de linho deitado, a face da ponta virada para a luz (de cima e da esquerda) com uma
# espiral só, solta, em tons de pano (não anéis escuros: não pode parecer rosca); no corpo, as bordas das voltas em
# diagonal e desencontradas, cada uma com a sombra e a beira clara da espessura; a ponta solta descendo para a direita,
# com uma dobra e o corte desfiado. A mesma construção nos três tamanhos (as medidas em frações do quadro).
# Uso: python bandagem.py <16|24|32> [silhueta] [<pasta>]. Grava a prévia e as listas por camada em <pasta>/<N>/.
import math, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, listas_camadas

N = int(sys.argv[1]); ETAPA = "silhueta" if "silhueta" in sys.argv[2:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[2:] if a != "silhueta"), "."))
K = N / 32
RAMPA = {"p": ["#4E4438", "#7E715E", "#AC9F86", "#D2C7AE", "#EDE6D6"]}   # o linho, do escuro ao claro
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
def pinta(m, t, c, onde):
    mat[onde] = m; tom[onde] = t; cam[onde] = c
# o rolo: a face da ponta (uma elipse um pouco estreita: o rolo visto de três quartos) e o corpo indo para trás e para
# a direita (a mesma elipse arrastada ao longo do eixo)
FX, FY, RX, RY = 8.6 * K, 14.0 * K, 4.4 * K, 7.0 * K
EX, EY = 14.6 * K, -1.0 * K                                     # o eixo: da face até a outra ponta
corpo = np.zeros((N, N), bool)
for k in range(0, 61):
    corpo |= ((X - FX - EX * k / 60) / RX) ** 2 + ((Y - FY - EY * k / 60) / RY) ** 2 <= 1
face = ((X - FX) / RX) ** 2 + ((Y - FY) / RY) ** 2 <= 1
# a ponta solta: sai de baixo do corpo e desce para a direita até o corte desfiado
A0 = np.array([FX + EX * 0.62, FY + EY * 0.62 + RY * 0.7]); A1 = np.array([29.4 * K, 26.4 * K])
d = A1 - A0; L = np.hypot(*d); u_ = d / L; v_ = np.array([-u_[1], u_[0]])
LARG = 3.3 * K
pu = ((X - A0[0]) * u_[0] + (Y - A0[1]) * u_[1]) / L
pv = (X - A0[0]) * v_[0] + (Y - A0[1]) * v_[1]
dente = max(1, round(1.5 * K))
franja = (np.floor((pv + 9) / dente) % 2) * (1.2 / L) * (N >= 32)   # o desfiado: dentes no fim (só no 32)
tira = (pu >= 0) & (pu <= 1 - franja) & (np.abs(pv) <= LARG) & ~corpo
if ETAPA == "silhueta":
    pinta("p", 2, "tira", tira); pinta("p", 3, "corpo", corpo & ~face); pinta("p", 4, "face", face)
else:
    # a tira: o lado de cima claro, o de baixo na sombra; uma dobra atravessada no meio
    t = np.where(pv < -LARG * 0.35, 4, np.where(pv < LARG * 0.45, 3, 2))   # a face larga da tira, deitada
    dobra = (pu > 0.58) & (pu < 0.58 + 1.0 / L)
    t = np.where(dobra & (N >= 32), t - 1, t)
    pinta("p", 0, "tira", tira); tom[tira] = t[tira]
    # o corpo: iluminado de cima, em faixas largas; duas bordas de volta inclinadas, com a sombra e a beira clara
    so = corpo & ~face
    cy = FY + EY * np.clip((X - FX) / EX, 0, 1)
    h = (Y - cy) / RY
    tb = np.where(h < -0.5, 4, np.where(h < 0.1, 3, np.where(h < 0.62, 2, 1)))
    for f in ((0.3, 0.68) if N >= 24 else (0.5,)):
        xb = FX + RX * 0.2 + EX * f + (Y - cy) * 0.22
        borda = (X >= xb) & (X < xb + 1) & so
        tb = np.where(borda, np.maximum(tb - 1, 0), tb)
        beira = (X >= xb + 1) & (X < xb + 2) & so & (h < 0.25)
        tb = np.where(beira, np.minimum(tb + 1, 4), tb)
    pinta("p", 0, "corpo", so); tom[so] = tb[so]
    # a face: clara (de frente para a luz), a beira de baixo e da direita mais escura, a espiral numa linha só
    lz = -((X - FX) / RX * 0.75 + (Y - FY) / RY)
    tf = np.where(lz > 0.25, 4, 3)
    tf = np.where((((X - FX) / RX) ** 2 + ((Y - FY) / RY) ** 2 > 0.72) & (lz < -0.25), 2, tf)
    pinta("p", 0, "face", face); tom[face] = tf[face]
    voltas = 1.25 if N >= 24 else 0.8
    r0 = 0.16
    for k in range(1200):
        a = k / 1200 * voltas * 2 * math.pi
        r = r0 + (0.86 - r0) * a / (voltas * 2 * math.pi)
        x = int(FX + r * RX * math.cos(a + 2.4)); y = int(FY + r * RY * math.sin(a + 2.4))
        if 0 <= x < N and 0 <= y < N and face[y, x]:
            tom[y, x] = 2 if N < 24 else 3 if tom[y, x] >= 4 else 2
    mx, my = int(FX), int(FY)                                   # o miolo
    tom[my, mx] = 1
# sem pixel solto: o que não encosta (pelos lados) em nada do desenho sai antes do contorno
for y in range(N):
    for x in range(N):
        if mat[y, x] and not any(0 <= y + b < N and 0 <= x + a < N and mat[y + b, x + a]
                                 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            mat[y, x] = ""; cam[y, x] = ""
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""   # 1 px de margem: o contorno cabe
contornar(mat)
cam[(mat == "c") & (cam == "")] = "contorno"
img = imagem(mat, tom, RAMPA)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"bandagem_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta, ["tira", "corpo", "face", "contorno"])
sim = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5"}
print("\n".join("".join("#" if mat[y, x] == "c" else sim[tom[y, x]] if mat[y, x] else "." for x in range(N)) for y in range(N)))
