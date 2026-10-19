# Os acessórios (anel e amuleto): no latão do aro do escudo aprovado (a mesma rampa), com a luz de cima e da esquerda.
# A construção é a mesma em 32, 40 e 48 (as medidas em frações do quadro de 32); o 64 é o 32 ampliado 2x.
#   o anel: o aro visto de três quartos, um pouco de cima; a abertura vazada (o fundo aparece), a parede de dentro do
#     lado de trás (mais escura: a espessura), o lado de fora em poucos planos de luz e o engaste com a granada no alto;
#   o amuleto (rodada 2): a gema violeta alongada (um cabochão) no engaste de latão, a argola no alto e o cordão de
#     couro que passa pela argola e fecha o laço do colar (o medalhão da rodada 1 em rodada1/joias_rodada1.py).
# Uso: python joias.py <anel|amuleto> <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import math, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, listas_camadas

PECA = sys.argv[1]; N = int(sys.argv[2]); ETAPA = "silhueta" if "silhueta" in sys.argv[3:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[3:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {
    "o": ["#40270C", "#623C12", "#8A571B", "#AE7526", "#CF9737", "#E9BB5C", "#F8DC94", "#FFF5D6"],   # o latão do escudo
    "g": ["#3E0812", "#6E1020", "#A41C30", "#D63E48", "#FF9C94"],                                     # a granada
    "u": ["#2A1A0E", "#46301C", "#6A4A2C", "#8E6A44"],                                                 # o cordão de couro
    "v": ["#22043E", "#3A0C68", "#541890", "#7028B8", "#9450D6", "#C08EEC", "#F4DEFF"],                 # a gema violeta
}
mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
x32, y32 = X / K, Y / K


def elipse(cx, cy, rx, ry):
    return ((x32 - cx) / rx) ** 2 + ((y32 - cy) / ry) ** 2 <= 1


def pinta(onde, m, t, c):
    mat[onde] = m; tom[onde] = t if np.isscalar(t) else t[onde]; cam[onde] = c


def luz_ang(cx, cy):
    """O quanto o ponto, em volta de (cx, cy), está do lado da luz (de cima e da esquerda): de -1 a 1."""
    a = np.arctan2(y32 - cy, x32 - cx)
    return np.cos(a - math.atan2(-0.72, -0.69))


if PECA == "anel":
    CX, CY, RX, RY = 16.0, 18.6, 12.6, 9.6                       # o lado de fora do aro
    HX, HY, HRX, HRY = 16.0, 19.7, 9.4, 6.5                      # a abertura (um pouco abaixo: o lado de trás mais alto)
    fora = elipse(CX, CY, RX, RY)
    furo = elipse(HX, HY, HRX, HRY)
    aro = fora & ~furo
    bezel = elipse(16.0, 9.2, 3.9, 2.9)
    pedra = elipse(16.0, 8.9, 2.5, 1.8)
    if ETAPA == "silhueta":
        pinta(aro | bezel, "o", 4, "aro")
    else:
        la = luz_ang(CX, CY)
        t = np.where(la > 0.55, 6, np.where(la > 0.1, 5, np.where(la > -0.35, 4, np.where(la > -0.75, 3, 2))))
        pinta(aro, "o", t, "aro")
        # a parede de dentro, do lado de trás: a faixa do aro logo acima da abertura, mais escura (a direita pega luz)
        parede = aro & elipse(HX, HY - 1.6, HRX + 0.4, HRY + 0.9) & (y32 < HY)
        tp = np.where(x32 > HX + HRX * 0.35, 3, np.where(x32 > HX - HRX * 0.2, 2, 1))
        pinta(parede, "o", tp, "parede")
        # a beira de dentro, na frente: uma linha clara de 1 px onde o aro vira para dentro, embaixo da abertura
        beira = aro & elipse(HX, HY + 0.9, HRX + 0.8, HRY + 0.9) & (y32 > HY + HRY * 0.4)
        pinta(beira, "o", np.where(x32 < HX, 4, 3), "aro")
        # o brilho agrupado em cima à esquerda do lado de fora
        brilho = aro & elipse(CX - RX * 0.62, CY - RY * 0.42, 1.6, 1.1)
        pinta(brilho, "o", 7, "brilho")
        # o engaste e a granada
        tb = np.where(luz_ang(16.0, 9.2) > 0.2, 6, np.where(luz_ang(16.0, 9.2) > -0.4, 4, 2))
        pinta(bezel & ~pedra, "o", tb, "engaste")
        tg = np.where(luz_ang(16.0, 8.9) > 0.5, 3, np.where(luz_ang(16.0, 8.9) > -0.3, 2, 1))
        pinta(pedra, "g", tg, "pedra")
        pinta(pedra & elipse(15.2, 8.4, 0.7, 0.5), "g", 4, "pedra")
    camadas = ["aro", "parede", "brilho", "engaste", "pedra", "contorno"]
else:
    # rodada 2: a gema violeta alongada num engaste de latão contido (o medalhão da rodada 1 lembrava uma moeda)
    GX, GY, GRX, GRY = 16.0, 21.4, 3.9, 6.3                      # a gema (um cabochão alongado)
    pedra = elipse(GX, GY, GRX, GRY)
    engaste = elipse(GX, GY, GRX + 1.4, GRY + 1.4) & ~pedra
    argola = elipse(16.0, 12.4, 1.9, 2.2) & ~elipse(16.0, 12.4, 0.8, 1.0)
    disco = pedra | engaste
    # o cordão: o colar deitado, um laço em gota (redondo em cima, estreitando até a argola, onde ele passa)
    cordao = np.zeros((N, N), bool)
    for k in range(2400):
        t = 2 * math.pi * k / 2400
        cx_ = 16.0 + 12.6 * math.sin(t) * math.sin(t / 2) ** 1.15
        cy_ = 6.2 + 5.0 * math.cos(t)
        x, y = int(cx_ * K), int(cy_ * K)
        if 0 <= x < N and 0 <= y < N:
            cordao[y, x] = True
    cordao &= ~elipse(16.0, 12.0, 2.0, 2.3)
    if ETAPA == "silhueta":
        pinta(cordao, "u", 2, "cordao"); pinta(argola, "o", 4, "argola"); pinta(disco, "o", 4, "engaste")
    else:
        tc = np.where((x32 < 16.0) & (y32 < 6.2), 3, np.where(y32 < 6.2, 2, 1))      # o couro: a luz em cima à esquerda
        pinta(cordao, "u", tc, "cordao")
        ta = np.where(luz_ang(16.0, 12.4) > 0.2, 6, np.where(luz_ang(16.0, 12.4) > -0.4, 4, 2))
        pinta(argola, "o", ta, "argola")
        le = luz_ang(GX, GY)                                     # o engaste: claro do lado da luz, escuro do outro
        pinta(engaste, "o", np.where(le > 0.35, 6, np.where(le > -0.35, 4, 2)), "engaste")
        # a gema: um domo (cabochão) iluminado de cima e da esquerda, em poucos planos; a beira mais funda
        nx_ = (x32 - GX) / GRX; ny_ = (y32 - GY) / GRY; nz_ = np.sqrt(np.clip(1 - nx_ ** 2 - ny_ ** 2, 0, 1))
        d = -0.58 * nx_ - 0.62 * ny_ + 0.53 * nz_
        tg = np.where(d > 0.78, 4, np.where(d > 0.5, 3, np.where(d > 0.15, 2, 1)))   # violeta fundo, como a pedra de hoje
        tg = np.where(nx_ ** 2 + ny_ ** 2 > 0.78, np.maximum(tg - 1, 0), tg)
        pinta(pedra, "v", tg, "pedra")
        pinta(pedra & elipse(GX - GRX * 0.4, GY - GRY * 0.45, 0.9, 1.3), "v", 6, "brilho")     # o reflexo agrupado
        pinta(pedra & elipse(GX + GRX * 0.35, GY + GRY * 0.5, 0.7, 0.8), "v", 4, "brilho")      # o brilho de dentro
    camadas = ["cordao", "argola", "engaste", "pedra", "brilho", "contorno"]

mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"{PECA}_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta, camadas)
print("\n".join("".join("#" if mat[y, x] == "c" else (mat[y, x] + str(tom[y, x])) if mat[y, x] else ".." for x in range(N)) for y in range(N)))
