"""A grade de 32 da P6 (20/10/2026), montada à mão sobre a guia (previa/guia-32.png, a referência reduzida pela média,
sem esticar: 18 × 30 px, de x 7 a 24 e da linha 1 à 30). O rascunho automático (grades/rascunho.txt, a cor mais perto
da paleta) saiu um mosaico: com cada perna de 7 a 8 px, a malha, as tiras de aço e as joelheiras viravam tons soltos.
Aqui cada parte da referência ocupa as linhas e as colunas que a redução dá a ela (as medidas abaixo, tiradas da guia e da
referência na mesma escala), e o desenho de cada uma é decidido por parte:
  - o contorno com 1 px por fora e entre as pernas;
  - o cinto de couro (linhas 2 e 3) com a fivela de aço no meio, um pouco à direita do centro, como na referência;
  - as coxas de malha (linhas 4 a 13) com as tiras de aço de fora (2 px) e a costura de aço no meio, até onde as pernas
    se separam (linha 11);
  - a tira de couro em diagonal na coxa direita, com a argola em cima e a fivela embaixo;
  - a faixa de aço do joelho com os rebites (linhas 14 e 15) e a joelheira em cúpula (16 a 21), com o brilho em cima à
    esquerda;
  - as canelas de malha (22 a 28) com as tiras de aço dos dois lados;
  - o punho de couro no tornozelo (29).
A malha é a da cota: o tom do volume e o de baixo, alternando ((x + y) par fica com o tom do volume), o volume pela luz do
conjunto (de cima e da esquerda): a metade de fora mais clara, a de dentro mais escura.
Grava grades/P6.txt e as listas por camada para o pintar.lua (listas/<camada>.lua: a malha, o aço das placas, o couro,
o contorno e a guia, que fica escondida na fonte).
    python grade.py <pasta da P6>
"""
import pathlib
import sys

from PIL import Image

FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
COURO = {"a": "140b09", "b": "251412", "c": "3a1f1a", "d": "522c23", "e": "6b3b2d", "f": "86503c"}
CONTORNO = "08080a"

X0 = 7          # a primeira coluna do desenho (c = 0); a última é X0 + 17 = 24
g = [["."] * 32 for _ in range(32)]
MALHA = set()   # os pixels escritos pela malha() (a camada da malha; os outros tons de ferro são o aço)


def poe(y, c0, s):
    """Escreve o trecho s na linha y a partir da coluna c0 do desenho; " " mantém o pixel."""
    for k, ch in enumerate(s):
        if ch != " ": g[y][X0 + c0 + k] = ch


def malha(y, c0, volumes):
    """A malha da cota: o tom do volume onde (x + y) é par, o de baixo onde é ímpar."""
    for k, t in enumerate(volumes):
        x = X0 + c0 + k
        g[y][x] = str(t if (x + y) % 2 == 0 else max(t - 1, 2))
        MALHA.add((x, y))


# o contorno de cima e o cinto (a referência: o cinto de y 25 a 90, 2 linhas; a fivela de c 7,4 a 10,1); nas pontas, o
# alto das tiras de aço, que entram por baixo do cinto (mais escuro que a tira aberta)
poe(1, 1, "################")
poe(2, 0, "#54fece776eeece43#")
poe(3, 0, "#54dddd6d4ddddc43#")

# as coxas (linhas 4 a 13): tira de aço de fora (c 1 e 2), malha, costura de aço (c 8, até a linha 10), malha da direita,
# tira de aço de fora (c 15 e 16, do lado da sombra); a perna da esquerda vai de c 0 a 8, a da direita de c 9 a 17.
# Os volumes pela luminosidade média da guia (a malha da referência, reduzida, dá o tom do volume)
COXA_E = [6, 5, 5, 4, 3]          # c 3 a 7: a luz de fora para dentro
COXA_D = [4, 6, 5, 5, 4, 3]       # c 9 a 14 (a primeira, ao lado da costura, na sombra dela)
for y in range(4, 14):
    sombra = 1 if y in (4, 13) else 0   # a sombra do cinto e a da faixa do joelho
    poe(y, 0, "#75")
    malha(y, 3, [t - sombra for t in COXA_E])
    if y <= 10:
        poe(y, 8, "5" if y == 4 else "6")
        malha(y, 9, [t - sombra for t in COXA_D])
    else:                          # as pernas se separam: o contorno das duas, encostados
        poe(y, 8, "##")
        malha(y, 10, [t - sombra for t in COXA_D[1:]])
    poe(y, 15, "53#")

# a tira de couro da coxa direita (de c 10,9 na linha 4,7 a c 17 na linha 10,9: uma linha por coluna), 2 px de largura,
# a argola de aço em cima e a fivela embaixo
poe(4, 11, "dc")
poe(5, 11, "7e")
poe(6, 12, "ed")
poe(7, 13, "ed")
poe(8, 14, "ed")
poe(9, 15, "7d")
poe(10, 16, "e")

# a faixa do joelho: a junta escura com a coxa (linha 14, como na guia) e a faixa acesa com os rebites (linha 15), de c 1
# a 7 e de c 10 a 16; o contorno de dentro em c 8 e c 9
poe(14, 0, "#2333332##2333221#")
poe(15, 0, "#6477746##6477643#")

# a joelheira em cúpula (linhas 16 a 21, de c 1 a 6 e de c 11 a 16): o brilho em cima à esquerda do centro (a guia: o 7
# nas linhas 18 e 19, nas duas primeiras colunas de dentro)
CUPULA = ["345532",
          "577643",
          "687643",
          "676532",
          "455432",
          "234321"]
for k, linha in enumerate(CUPULA):
    poe(16 + k, 0, "#" + linha + "#..#" + linha + "#")

# as canelas (linhas 22 a 28): a tira de aço de fora e a de dentro, a malha no meio
for y in range(22, 29):
    sombra = 1 if y in (22, 28) else 0   # embaixo da joelheira e em cima do punho
    poe(y, 0, "#7    5#..#6    4#")
    malha(y, 2, [t - sombra for t in (5, 5, 4, 3)])
    malha(y, 12, [t - sombra for t in (5, 5, 4, 3)])

# o punho de couro (linha 29) e o contorno de baixo
poe(29, 0, "#feeedd#..#feeedd#")
poe(30, 1, "######....######")

if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    linhas = ["".join(l) for l in g]
    (base / "grades").mkdir(exist_ok=True)
    (base / "grades/P6.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    listas = {"malha": [], "aco": [], "couro": [], "contorno": []}
    for y in range(32):
        for x in range(32):
            ch = g[y][x]
            if ch == ".": continue
            if ch == "#": listas["contorno"].append(f"{x},{y},{CONTORNO}")
            elif ch in COURO: listas["couro"].append(f"{x},{y},{COURO[ch]}")
            else: listas["malha" if (x, y) in MALHA else "aco"].append(f"{x},{y},{FERRO[int(ch)]}")
    guia = Image.open(base / "previa/guia-32.png").convert("RGBA")
    listas["guia"] = [f"{x},{y},{r:02x}{g_:02x}{b:02x}{a:02x}" for y in range(32) for x in range(32)
                      for r, g_, b, a in [guia.getpixel((x, y))] if a]
    (base / "listas").mkdir(exist_ok=True)
    for k, v in listas.items():
        (base / f"listas/{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(linhas)))
    print({k: len(v) for k, v in listas.items()})
