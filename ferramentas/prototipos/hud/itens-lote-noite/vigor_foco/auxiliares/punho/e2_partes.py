# etapa 2 (o punho 2 px à esquerda, para o fogo ficar atrás do lado direito): as partes em camadas, com a luz de cima e da esquerda em planos: os dedos dobrados (os nós em degrau, a
# dobra entre eles só em sombra), o polegar deitado na frente, a dobra escura entre os dedos e o polegar, a palma e
# o pulso
import sys; sys.path.insert(0, ".")
from grade import listas
G = [
    "....................",  # 0
    "....................",  # 1
    "....................",  # (o punho desce 2 linhas para o fogo ter espaço em cima)
    "....................",
    "....................",  # 2
    "....................",  # 3
    "....................",  # 4
    ".....ABB............",  # 5  o nó do médio
    "..ABCABCABC.........",  # 6  indicador, médio, anelar
    "..BBCBBCBBCABB......",  # 7  o mínimo, mais baixo
    ".lBBBBBBBBBBBC......",  # 8  os dedos dobrados
    ".lKKKKKKKCCCCC......",  # 9  a dobra sobre o polegar; as pontas dos dedos entrando na palma
    ".QPPPPPPPQKBBC......",  # 10 o polegar deitado na frente (a dobra escura separa a ponta)
    ".QQQQQQQQRKCCC......",  # 11
    "..lmmmmmmmmmss......",  # 12 a palma
    "...lmmmmmmmss.......",  # 13
    "....lmmmmmss........",  # 14 o pulso
    "....lmmmmmss........",  # 15
    "...llmmmmmss........",  # 18
    "...llmmmmmss........",  # 19
]
CORES = {"A": "FFE2A0", "B": "EEB45C", "C": "C2802E", "P": "FFEBB8", "Q": "F2C070", "R": "C8883A",
         "l": "FFDA94", "m": "E6A850", "s": "B87428", "K": "7A3E12", "O": "08080A"}
CAM = {"A": "dedos", "B": "dedos", "C": "dedos", "P": "polegar", "Q": "polegar", "R": "polegar",
       "l": "pulso", "m": "pulso", "s": "pulso", "K": "dobras", "O": "contorno"}
g, por = listas(G, CORES, CAM, saida=".")
print({k: len(v) for k, v in por.items()})
