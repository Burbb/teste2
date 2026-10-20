"""A grade de 32 da P7 (20/10/2026), montada à mão sobre a guia (previa/guia-32.png, a segunda imagem gerada do Jean
reduzida pela média, sem esticar: 20 × 30 px, de x 6 a 25 e da linha 1 à 30). A silhueta vem primeiro, linha a linha
pela cobertura da guia, com as mudanças de largura da referência:
  - o cinto (linhas 1 a 4) mais estreito que as coxas (x 8 a 23), o quadril abrindo (5 e 6: x 7 a 24) até as coxas
    (7 a 14: x 6 a 25); as pernas se encostam na linha 11 e se separam a partir da 12 (o vão de 2 px, abrindo para baixo);
  - a faixa do joelho (15) na largura do fim da coxa; a joelheira (16 a 22) mais estreita (5 px por dentro);
  - o alto da canela (23 e 24) abrindo de novo, a asa da caneleira; a canela (25 a 27) de 5 px; o fim da canela (28)
    afinando, e o punho de couro (29) um pouco mais largo, como na referência.
Depois o volume de cada parte (o tom pela luminosidade média da guia, a luz do conjunto de cima e da esquerda) e por
último a textura: a malha é a da cota (o tom do volume e o de baixo, alternando), só nas áreas de malha.
As duas pernas têm a mesma construção; a da direita é a da esquerda deslocada 11 px (a luz é a mesma, não espelhada),
menos nas coxas, que se encontram no meio (a costura de aço é da perna da esquerda).
Grava grades/P7.txt e as listas por camada para o pintar.lua (listas/<camada>.lua: a malha, o aço, o couro, o contorno
e a guia, que fica escondida na fonte).
    python grade.py <pasta da P7>
"""
import pathlib
import sys

from PIL import Image

FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
COURO = {"a": "140b09", "b": "251412", "c": "3a1f1a", "d": "522c23", "e": "6b3b2d", "f": "86503c"}
CONTORNO = "08080a"
DIREITA = 11    # a perna da direita: a da esquerda deslocada 11 px (do joelho para baixo)
g = [["."] * 32 for _ in range(32)]
MALHA = set()   # os pixels escritos pela malha() (a camada da malha; os outros tons de ferro são o aço)


def poe(y, x0, s):
    """Escreve o trecho s na linha y a partir da coluna x0; " " mantém o pixel."""
    for k, ch in enumerate(s):
        if ch != " ": g[y][x0 + k] = ch


def malha(y, x0, volumes):
    """A malha da cota: o tom do volume onde (x + y) é par, o de baixo onde é ímpar."""
    for k, t in enumerate(volumes):
        x = x0 + k
        g[y][x] = str(t if (x + y) % 2 == 0 else max(t - 1, 2))
        MALHA.add((x, y))


def perna(y, x0, s, vol=None, xm=None):
    """Uma linha das duas pernas (do joelho para baixo): o trecho s na da esquerda e na da direita, e a malha."""
    for d in (0, DIREITA):
        poe(y, x0 + d, s)
        if vol: malha(y, xm + d, vol)


# o cinto (1 a 4, de x 8 a 23): a borda de cima; as pontas do cinto sobem um pouco nos lados (linha 2), no meio fica
# o cós escuro acima dele; a fivela simples de aço (3 × 3, x 15 a 17) com o couro aparecendo no vão; nas pontas, o alto
# das placas de aço dos lados (x 9 e x 22)
poe(1, 8, "################")
poe(2, 8, "#5ee33378722ed4#")
poe(3, 8, "#5ffeee7c5eeed4#")
poe(4, 8, "#4ddddc654cddc3#")

# as coxas: o quadril (5 e 6, x 7 a 24) e as coxas (7 a 14, x 6 a 25). Por fora, as placas de aço dos lados (a de cima até
# a linha 10, a junta escura na 11, a de baixo de 12 a 14); a malha; no meio, a costura de aço da perna da esquerda (x 15,
# com a linha escura em x 16) até a linha 10; na 11 os dois contornos se encostam; da 12 em diante, o vão
COXA_E = [6, 6, 5, 5, 4, 3]       # x 9 a 14 (a luz de fora para dentro)
COXA_D = [5, 6, 6, 5, 4, 3]       # x 17 a 22
for y in range(5, 15):
    sombra = 1 if y in (5, 14) else 0          # a sombra do cinto e a de cima da faixa do joelho
    e = [t - sombra for t in COXA_E]
    d = [t - sombra for t in COXA_D]
    if y <= 6:                                  # o quadril, 1 px mais estreito de cada lado: a placa só por dentro
        poe(y, 7, "#5" if y == 5 else "#6")
        poe(y, 23, "3#" if y == 5 else "4#")
    else:
        placa_e, placa_d = ("32", "23") if y == 11 else ("73", "36")   # a placa acesa e a junta escura com a malha
        poe(y, 6, "#" + placa_e)
        poe(y, 23, placa_d + "#")
    if y <= 10:
        malha(y, 9, e)
        poe(y, 15, ("5" if y == 5 else "6") + "2")
        malha(y, 17, d)
    elif y == 11:
        malha(y, 9, e)
        poe(y, 15, "##")
        malha(y, 17, d)
    else:                                       # as pernas separadas: o contorno de dentro de cada uma, o vão no meio
        malha(y, 9, e[:5])
        poe(y, 14, "#..#")
        malha(y, 18, d[1:])

# a faixa do joelho (15): acesa, na largura do fim da coxa (x 7 a 13 por dentro), o brilho em x 9 e 10
perna(15, 6, "#5788653#")
# a joelheira (16 a 22, x 8 a 12 por dentro): a junta escura com a faixa (16), a cúpula com o brilho em cima à esquerda
# (17 a 21) e a junta de baixo (22)
JOELHEIRA = ["32221", "56643", "78654", "78653", "56543", "45432", "33221"]
for k, linha in enumerate(JOELHEIRA):
    perna(16 + k, 7, "#" + linha + "#")
# o alto da canela (23 e 24, x 7 a 13 por dentro): a asa da caneleira, acesa por fora, com a faixa de aço em cima e a
# malha começando embaixo, entre as tiras
perna(23, 6, "#7665546#")
perna(24, 6, "#67   54#", [5, 5, 4], 9)
# a canela (25 a 27): a tira de aço de fora (x 8), a malha (x 9 a 11), a tira de dentro (x 12)
for y in range(25, 28):
    perna(y, 7, "#7   5#", [5, 5, 4], 9)
# o fim da canela (28), afinando, na sombra; o punho de couro (29) e o contorno de baixo (30)
perna(28, 8, "#   #", [4, 4, 3], 9)
perna(29, 7, "#ffeed#")
perna(30, 8, "#####")

if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    linhas = ["".join(l) for l in g]
    (base / "grades").mkdir(exist_ok=True)
    (base / "grades/P7.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
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
