# O anel, rodadas 2 e 3 (pelas referências do Jean, ferramentas/arte/referencias/aneis/): o aro em pé, de três
# quartos e inclinado, com a abertura elíptica em diagonal. O aro é modelado como um cilindro curto (a faixa de metal):
# a face de fora, a de dentro e as duas bordas, projetadas no quadro; cada pixel fica com a superfície mais perto de
# quem olha (a perspectiva e a espessura saem coerentes em todo tamanho). A luz é a da família (de cima e da esquerda,
# um pouco de frente), em poucos tons do ouro das moedas, com o reflexo agrupado; a face de dentro mais escura. O
# acabamento do sample do Jean (o aro liso de ouro): o chanfro claro nas duas bordas da faixa e o meio mais fundo.
# Sem pedra nem decoração: o anel básico. A mesma construção em 32, 40 e 48 (o 64 é o 32 ampliado 2x).
# Rodada 3 (pedido do Jean durante o trabalho): um ornamento leve, o ziguezague gravado no meio da face de fora; com
# "liso", a versão sem ele.
# Uso: python aro.py <32|40|48> [silhueta] [liso] [<pasta>]. Grava a prévia e as listas em <pasta>/<N>/.
import math, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6] / "ferramentas" / "arte"))
from pixel_comum import grade, contornar, imagem, limpar, listas_camadas

N = int(sys.argv[1]); ETAPA = "silhueta" if "silhueta" in sys.argv[2:] else "final"
SAIDA = pathlib.Path(next((a for a in sys.argv[2:] if a not in ("silhueta", "liso")), "."))
K = N / 32
OURO = ["#3A1C04", "#6E3C08", "#A86410", "#D69018", "#F0B828", "#FFDC5A", "#FFF0A8"]           # o ouro das moedas aprovadas
RAMPAS = {"o": OURO, "i": OURO, "b": OURO}                       # uma letra por face (a limpeza não mistura as faces)
# rodada 3: o ângulo e as proporções da referência principal (sample (2).png), achados pelo ajuste_aro.py (a silhueta e
# o vão reduzidos a 32 sobrepõem 0,93 e 0,97): o eixo para baixo, à direita e para frente; a face de fora larga em cima e
# à esquerda, o vão na diagonal de baixo à esquerda para cima à direita, a face de dentro embaixo à direita
CX, CY = 16.72, 16.83                                           # o centro do aro no quadro de 32
R, PAREDE, LARG = 13.64, 1.4, 8.09                              # o raio de fora, a parede (fina: a borda é uma linha) e a largura
EIXO = np.array([0.707, 0.381, 0.596]); EIXO /= np.linalg.norm(EIXO)
U = np.cross(EIXO, [0.0, 0.0, 1.0]); U /= np.linalg.norm(U)
V = np.cross(EIXO, U)
LUZ = np.array([-0.58, -0.62, 0.53]); LUZ /= np.linalg.norm(LUZ)
MEIO = (LUZ + np.array([0, 0, 1.0])); MEIO /= np.linalg.norm(MEIO)

prof = np.full((N, N), -1e9); tomz = np.zeros((N, N), int); camz = np.full((N, N), "", dtype=object)


GRAVA = "liso" not in sys.argv[2:]                              # o ornamento leve (sem ele: a versão lisa)
ZIG, ZIG_A, ZIG_W = 7, LARG * 0.2, 0.6                          # o ziguezague gravado: as voltas, a amplitude e a largura


def ponto(p, n, onde, t_faixa=0.0, th=0.0):
    """Projeta um ponto da superfície (com a normal) e fica com ele se estiver na frente do que já há no pixel."""
    x, y = int((CX + p[0]) * K), int((CY + p[1]) * K)
    if not (0 <= x < N and 0 <= y < N) or p[2] <= prof[y, x]:
        return
    prof[y, x] = p[2]
    d = max(0.0, float(n @ LUZ)); s = max(0.0, float(n @ MEIO)) ** 24
    if onde == "dentro":                                         # a face de dentro: escura e quente em cima (a sombra
        v = 0.1 + 0.85 * d                                       # do próprio aro), clareando embaixo, onde pega luz
        v -= 0.25 if p[1] < -R * 0.25 else 0.0
        t = 5 if v > 0.95 else 4 if v > 0.78 else 3 if v > 0.58 else 2 if v > 0.38 else 1
    elif onde == "borda":                                        # a borda da faixa: uma linha clara do lado da luz
        t = 6 if s > 0.5 else 5 if d > 0.45 else 3 if d > 0.15 else 2
    else:                                                        # a de fora: o ouro em três planos largos
        t = 6 if s > 0.75 else 5 if d > 0.86 else 4 if d > 0.55 else 3 if d > 0.22 else 2
        if LARG / 2 - abs(t_faixa) < 0.55 and t < 6:             # o chanfro: a beira da faixa um tom acima
            t += 1
    tomz[y, x] = t; camz[y, x] = "brilho" if t == 6 else onde


passo = 0.22 / K
for th in np.arange(0, 2 * math.pi, passo / R):
    radial = math.cos(th) * U + math.sin(th) * V
    for t in np.arange(-LARG / 2, LARG / 2 + 1e-6, passo):
        ponto(R * radial + t * EIXO, radial, "fora", t, th)
        ponto((R - PAREDE) * radial + t * EIXO, -radial, "dentro")
    for r in np.arange(R - PAREDE, R + 1e-6, passo):              # as duas bordas da faixa
        ponto(r * radial + LARG / 2 * EIXO, EIXO, "borda")
        ponto(r * radial - LARG / 2 * EIXO, -EIXO, "borda")

# a gravação, numa segunda passada: com a frente decidida, o pixel da face de fora fica gravado se uma amostra da
# superfície visível nele (a mesma profundidade) cai no sulco do ziguezague; assim a linha sai contínua
if GRAVA:
    gravado = np.zeros((N, N), bool)
    for th in np.arange(0, 2 * math.pi, passo / R):
        onda = 2 * abs((th * ZIG / (2 * math.pi)) % 1 - 0.5) * 2 - 1
        radial = math.cos(th) * U + math.sin(th) * V
        for t in np.arange(-LARG / 2, LARG / 2 + 1e-6, passo):
            if abs(t - onda * ZIG_A) >= ZIG_W:
                continue
            q = R * radial + t * EIXO
            x, y = int((CX + q[0]) * K), int((CY + q[1]) * K)
            if 0 <= x < N and 0 <= y < N and camz[y, x] in ("fora", "brilho") and q[2] >= prof[y, x] - 0.35:
                gravado[y, x] = True
    tomz[gravado] = np.maximum(tomz[gravado] - 2, 1); camz[gravado] = "gravacao"

mat, tom, fixo, X, Y = grade(N)
cam = np.full((N, N), "", dtype=object)
cheio = camz != ""
if ETAPA == "silhueta":
    mat[cheio] = "o"; tom[cheio] = 4; cam[cheio] = "fora"
else:
    letra = {"fora": "o", "dentro": "i", "borda": "b", "brilho": "o", "gravacao": "o"}
    for k in range(N):
        for j in range(N):
            if cheio[k, j]:
                mat[k, j] = letra[camz[k, j]]; tom[k, j] = tomz[k, j]; cam[k, j] = camz[k, j]
    fixo[:] = (camz == "brilho") | (camz == "gravacao")
    tom = limpar(mat, tom, fixo)                                 # sem pixel solto de um tom no meio de outro
mat[:, -1] = ""; mat[-1, :] = ""; mat[:, 0] = ""; mat[0, :] = ""
contornar(mat)
cam[mat == "c"] = "contorno"
img = imagem(mat, tom, RAMPAS)
pasta = SAIDA / str(N); pasta.mkdir(parents=True, exist_ok=True)
img.save(pasta / f"anel_{ETAPA}_{N}.png")
if ETAPA == "final":
    listas_camadas((img, cam), pasta, ["dentro", "fora", "gravacao", "borda", "brilho", "contorno"])
print("\n".join("".join("#" if mat[y, x] == "c" else str(tom[y, x]) if mat[y, x] else "." for x in range(N)) for y in range(N)))
