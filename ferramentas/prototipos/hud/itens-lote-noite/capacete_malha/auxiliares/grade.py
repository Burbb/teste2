"""A grade de 32 do C1, o capacete com malha (20/10/2026), montada à mão sobre a guia (previa/guia-32.png, a imagem
gerada do Jean reduzida pela média, sem esticar: 24 × 30 px, de x 4 a 27 e da linha 1 à 30). Primeiro a silhueta,
simétrica em torno do meio do quadro (entre x 15 e 16), pela cobertura da guia (EXTENSAO); depois as partes, cada uma com
o seu volume (a luz do conjunto, de cima e da esquerda):
  - a calota (linhas 1 a 9), arredondada, com o brilho em cima à esquerda e a crista de aço no meio (x 15 e 16, acesa, com
    as juntas escuras dos lados);
  - a faixa da testa (10 a 12): a junta com a calota (10), a faixa acesa (11) e a beira de baixo (12), um pouco mais larga
    que a calota, como na referência;
  - a nasal (x 15 e 16), que desce da crista, cruza a faixa e termina na linha 17;
  - a abertura do rosto (13 a 23), vazia: o escuro do interior, sem pessoa, mais estreita embaixo;
  - as tiras de couro (13 a 15, x 7 e 8 e x 23 e 24) presas embaixo da faixa, com o rebite;
  - a malha (16 a 30) envolvendo os lados e a nuca, no xadrez da cota (o tom do volume e o de baixo), acesa do lado
    esquerdo, mais escura do lado direito, embaixo e na beira de dentro, onde ela vira para o interior.
O contorno sai da silhueta (o pixel cheio com um vizinho de fora). Grava grades/C1.txt e as listas por camada para o
pintar.lua (listas/<camada>.lua: aco, malha, couro, interior, contorno e a guia, que fica escondida na fonte).
    python grade.py <pasta do C1>
"""
import pathlib
import sys

from PIL import Image

FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
COURO = {"a": "140b09", "b": "251412", "c": "3a1f1a", "d": "522c23", "e": "6b3b2d", "f": "86503c"}
CONTORNO = "08080a"
INTERIOR = "i"   # o escuro da abertura (o ferro 0): camada própria, para não se misturar com o aço
# a silhueta, linha a linha (x de começo e de fim, com o contorno): a cobertura de metade ou mais na guia, simétrica; a
# calota um pouco mais cheia em cima (a referência tem o topo plano de ~6 px) e embaixo, a ponta da malha também
EXTENSAO = {1: (13, 18), 2: (11, 20), 3: (10, 21), 4: (9, 22), 5: (8, 23), 6: (8, 23), 7: (7, 24), 8: (7, 24),
            9: (7, 24), 10: (6, 25), 11: (6, 25), 12: (6, 25), 13: (6, 25), 14: (6, 25), 15: (7, 24),
            16: (6, 25), 17: (6, 25), 18: (6, 25), 19: (6, 25), 20: (6, 25), 21: (6, 25), 22: (5, 26), 23: (5, 26),
            24: (4, 27), 25: (4, 27), 26: (5, 26), 27: (6, 25), 28: (8, 23), 29: (11, 20), 30: (13, 18)}
# a abertura do rosto: as colunas do vazio em cada linha (da guia: o escuro de x 10 a 21, estreitando embaixo)
ABERTURA = {13: (9, 22), 14: (9, 22), 15: (9, 22), 16: (10, 21), 17: (10, 21), 18: (10, 21), 19: (10, 21),
            20: (10, 21), 21: (10, 21), 22: (11, 20), 23: (12, 19)}
NASAL = (15, 16)
g = [["."] * 32 for _ in range(32)]
MALHA = set()


def dentro(x, y):
    return y in EXTENSAO and EXTENSAO[y][0] <= x <= EXTENSAO[y][1]


def calota(x, y):
    """O tom da calota: o brilho em cima à esquerda (em x 11, linha 4), escurecendo para a direita e para baixo."""
    if (x, y) in ((11, 4), (12, 4), (11, 5)): return 8                    # o reflexo
    d = ((x - 11) ** 2 + (y - 4) ** 2) ** 0.5
    return max(3, min(7, round(7.2 - 0.33 * d)))


def malha_tom(x, y):
    """O volume da malha: acesa do lado de fora da esquerda, média na frente, escura à direita e embaixo; um tom abaixo
    na beira de dentro (vira para o interior) e logo abaixo das tiras."""
    t = 7 if x <= 8 else 5 if x >= 23 else 6   # no nível da cota (um tom abaixo saía chapado)
    if y >= 28: t -= 1
    if y == 16: t -= 1
    if any((x + dx, y + dy) in VAZIO for dx in (-1, 0, 1) for dy in (-1, 0, 1)): t -= 1
    return max(t, 3)


VAZIO = {(x, y) for y, (a, b) in ABERTURA.items() for x in range(a, b + 1)
         if not (x in NASAL and y <= 17)}

for y in range(32):
    for x in range(32):
        if not dentro(x, y): continue
        if y <= 9:                                              # a calota e a crista
            if x in NASAL: ch = "7" if x == 15 else "8"
            elif x in (14, 17): ch = "4" if x == 14 else "3"
            else: ch = str(calota(x, y))
        elif y == 10:                                           # a junta da calota com a faixa
            ch = "7" if x == 15 else "8" if x == 16 else "3" if x < 20 else "2"
        elif y == 11:                                           # a faixa acesa
            ch = "7" if x == 15 else "8" if x == 16 else "7" if x <= 13 else "6" if x <= 19 else "5" if x <= 22 else "4"
        elif y == 12:                                           # a beira de baixo da faixa
            ch = "6" if x == 15 else "7" if x == 16 else "5" if x <= 13 else "4" if x <= 21 else "3"
        elif (x, y) in VAZIO:
            ch = INTERIOR
        elif x in NASAL and y <= 17:                            # a nasal, com a ponta escurecendo
            ch = {15: "6", 16: "7"}[x] if y <= 15 else {15: "5", 16: "6"}[x] if y == 16 else {15: "4", 16: "4"}[x]
        elif y <= 15:                                           # as tiras de couro com o rebite
            ch = {(7, 13): "f", (8, 13): "e", (7, 14): "6", (8, 14): "d", (8, 15): "c",
                  (23, 13): "e", (24, 13): "d", (23, 14): "d", (24, 14): "5", (23, 15): "c"}.get((x, y), "#")
        else:
            t = malha_tom(x, y)
            ch = str(t if (x + y) % 2 == 0 else max(t - 1, 2))
            MALHA.add((x, y))
        g[y][x] = ch

# o contorno: o pixel cheio que encosta (pelos lados) em fora vira contorno
fora = lambda x, y: not dentro(x, y)
borda = [(x, y) for y in range(32) for x in range(32) if dentro(x, y) and g[y][x] != INTERIOR
         and any(fora(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
for x, y in borda:
    g[y][x] = "#"
    MALHA.discard((x, y))

if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    linhas = ["".join(l) for l in g]
    (base / "grades").mkdir(exist_ok=True)
    (base / "grades/C1.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    listas = {"malha": [], "aco": [], "couro": [], "interior": [], "contorno": []}
    for y in range(32):
        for x in range(32):
            ch = g[y][x]
            if ch == ".": continue
            if ch == "#": listas["contorno"].append(f"{x},{y},{CONTORNO}")
            elif ch == INTERIOR: listas["interior"].append(f"{x},{y},{FERRO[0]}")
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
