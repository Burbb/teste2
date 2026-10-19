# O anel, rodada 2 (pela prancha de referência do Jean, ferramentas/arte/referencias/aneis/): o aro em pé, de três
# quartos e inclinado, com a abertura elíptica em diagonal. O aro é modelado como um cilindro curto (a faixa de metal):
# a face de fora, a de dentro e as duas bordas, projetadas no quadro; cada pixel fica com a superfície mais perto de
# quem olha (a perspectiva e a espessura saem coerentes em todo tamanho). A luz é a da família (de cima e da esquerda,
# um pouco de frente), em poucos tons do ouro das moedas, com o reflexo agrupado; a face de dentro mais escura. O
# acabamento do sample do Jean (o aro liso de ouro): o chanfro claro nas duas bordas da faixa e o meio mais fundo.
# Sem pedra nem decoração: o anel básico. A mesma construção em 32, 40 e 48 (o 64 é o 32 ampliado 2x).
# Uso: python aro.py <32|40|48> [silhueta] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import math, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, listas_camadas

N = int(sys.argv[1]); ETAPA = "silhueta" if "silhueta" in sys.argv[2:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[2:] if a != "silhueta"), "."))
K = N / 32
RAMPAS = {"o": ["#3A1C04", "#6E3C08", "#A86410", "#D69018", "#F0B828", "#FFDC5A", "#FFF0A8"]}   # o ouro das moedas aprovadas
CX, CY = 15.6, 16.4                                             # o centro do aro no quadro de 32
R, PAREDE, LARG = 11.4, 1.8, 5.4                                # o raio de fora, a parede e a largura da faixa
EIXO = np.array([0.60, -0.20, 0.77]); EIXO /= np.linalg.norm(EIXO)   # para a direita, um pouco para cima e para frente
U = np.cross(EIXO, [0.0, 0.0, 1.0]); U /= np.linalg.norm(U)
V = np.cross(EIXO, U)
LUZ = np.array([-0.58, -0.62, 0.53]); LUZ /= np.linalg.norm(LUZ)
MEIO = (LUZ + np.array([0, 0, 1.0])); MEIO /= np.linalg.norm(MEIO)

prof = np.full((N, N), -1e9); tomz = np.zeros((N, N), int); camz = np.full((N, N), "", dtype=object)


def ponto(p, n, onde, t_faixa=0.0):
    """Projeta um ponto da superfície (com a normal) e fica com ele se estiver na frente do que já há no pixel."""
    x, y = int((CX + p[0]) * K), int((CY + p[1]) * K)
    if not (0 <= x < N and 0 <= y < N) or p[2] <= prof[y, x]:
        return
    prof[y, x] = p[2]
    d = max(0.0, float(n @ LUZ)); s = max(0.0, float(n @ MEIO)) ** 24
    if onde == "dentro":                                         # a face de dentro: na sombra, o laranja quente
        v = 0.25 + 0.5 * d
        t = 3 if v > 0.62 else 2 if v > 0.42 else 1
    else:                                                        # a de fora e as bordas: o ouro claro, contrastado
        v = 0.42 + 0.7 * d + (0.15 if onde == "borda" else 0.0)
        if onde == "fora":                                       # o chanfro claro nas duas bordas, o meio mais fundo
            dist = LARG / 2 - abs(t_faixa)
            v += 0.2 if dist < 0.9 else (-0.1 if dist > 1.7 else 0.0)
        t = 6 if s > 0.5 else (5 if v > 1.02 else 4 if v > 0.82 else 3 if v > 0.6 else 2)
    tomz[y, x] = t; camz[y, x] = "brilho" if t == 6 else onde


passo = 0.22 / K
for th in np.arange(0, 2 * math.pi, passo / R):
    radial = math.cos(th) * U + math.sin(th) * V
    for t in np.arange(-LARG / 2, LARG / 2 + 1e-6, passo):
        ponto(R * radial + t * EIXO, radial, "fora", t)
        ponto((R - PAREDE) * radial + t * EIXO, -radial, "dentro")
    for r in np.arange(R - PAREDE, R + 1e-6, passo):              # as duas bordas da faixa
        ponto(r * radial + LARG / 2 * EIXO, EIXO, "borda")
        ponto(r * radial - LARG / 2 * EIXO, -EIXO, "borda")

mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
cheio = camz != ""
if ETAPA == "silhueta":
    mat[cheio] = "o"; tom[cheio] = 4; cam[cheio] = "fora"
else:
    mat[cheio] = "o"; tom[cheio] = tomz[cheio]; cam[cheio] = camz[cheio]
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"anel_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta, ["dentro", "fora", "borda", "brilho", "contorno"])
print("\n".join("".join("#" if mat[y, x] == "c" else str(tom[y, x]) if mat[y, x] else "." for x in range(N)) for y in range(N)))
