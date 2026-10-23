"""O Barqueiro do Charco em 32×32 nativos (pedido do Jean, 23/10/2026; protótipo, nada no jogo, sem adaptação para 16):
o barqueiro morto que continua atravessando os afogados, os passageiros dele (`identidades/LEIA-ME.md`). Um velho
encharcado, de rosto afundado e pele cinza-esverdeada, em close (a cabeça e o começo dos ombros): o gorro molhado (a
silhueta redonda e a barra dobrada, sem aba), a testa com rugas, as sobrancelhas brancas, os olhos fundos com o brilho
verde, o nariz comprido, as bochechas fundas, o bigode branco ralo sobre a boca fechada e o queixo; a luz verde da
lanterna vem de baixo (o queixo, o lábio, a ponta do nariz e as pálpebras de baixo acesos; a testa e o gorro no escuro).
A rede fica no pescoço e nos ombros, sobre o casaco escuro, sem cobrir o rosto; a lanterna, o barco e a vara ficam fora
do quadro. Sem guia: o desenho parte do conceito, não de uma referência externa. Uma letra por pixel; o contorno faz
parte do desenho.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "0b100e",
          "a": "1a242c", "A": "28384a", "Q": "3a5464",  # o gorro molhado (a barra dobrada com o brilho de baixo)
          "k": "1f2a24", "s": "3c4a42", "m": "5e6e62", "l": "82977f", "L": "a9c8a2", "G": "cdeec0",  # a pele; a luz de baixo
          "E": "e4ffe8", "e": "7ee6a6", "z": "0e1612",  # os olhos
          "h": "8e9a92", "H": "c4ccc4",  # o cabelo, as sobrancelhas e o bigode, brancos e ralos
          "p": "4a5866",  # o lábio
          "n": "4e4430", "N": "7a6a44", "x": "a8a46a",  # a rede (os nós claros perto da luz)
          "c": "111816", "C": "1d2824", "D": "2c3c34"}  # o casaco
GRADE_32 = [
    "................................",
    "............oooooooo............",
    "..........ooaaaaaaaaoo..........",
    ".........oaaaaaaaaaaaao.........",
    "........oaaaaaaaaaaaaaao........",
    ".......oaaaaaaaaaaaaaaaao.......",
    "......oAAAAAAAAAAAAAAAAAAo......",
    "......oQAQQAQQQQQQQQAQQAQo......",
    "......ohksssssssssssssskho......",
    "......ohsmkkkssmmsskkkmsho......",
    "......ohshhhhksmmskhhhhsho......",
    "......omskkkkksmmskkkkksmo......",
    "......olskzeEksmmskEezkslo......",
    "......omsmllmksmmskmllmsmo......",
    "......oksmmmmmsmmsmmmmmsko......",
    "......oklmmmssmmmmssmmmlko......",
    ".......osmsssmkLLkmsssmso.......",
    ".......osskssmkGLkmssksso.......",
    ".......osskmmlkLLklmmksso.......",
    "........ossmlhhHHhhlmsso........",
    "........okshHkkkkkkHhsko........",
    "........okshslLLLLlshsko........",
    ".........okshmlLLlmhsko.........",
    "..........okhslGGlshko..........",
    "...........oksmLLmsko...........",
    "...........onsmllmsno...........",
    "......ooNnxnNsmLLmsNnxnNoo......",
    "....ocCDnxNnNxNllNxNnNxnDCco....",
    "..ocCDccncccxcNNNNcxcccnccDCco..",
    ".ocCDcncncccNcNccNcNcccncncDCco.",
    "ocCDcnccncNcccxNNxcccNcnccncDCco",
    "ocCDnccncccNcNcNNcNcNcccnccnDCco",
]
# cada desenho: a grade e o lado (só o 32 nesta rodada)
DESENHOS = {"barqueiro-n32": (GRADE_32, 32)}
# as camadas, de baixo para cima
ORDEM = ["casaco", "rede", "pele", "gorro", "olhos", "contorno"]


def camada(x, y, ch, ident):
    if ch == "o":
        return "contorno"
    if ch in "aAQ":
        return "gorro"
    if ch in "cCD":
        return "casaco"
    if ch in "nNx":
        return "rede"
    if ch in "Eez":
        return "olhos"
    return "pele"  # a pele, o cabelo branco e o lábio


def imagem(ident):
    grade, n = DESENHOS[ident]
    im = Image.new("RGBA", (n, n))
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(PALETA[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ident):
    grade, n = DESENHOS[ident]
    assert len(grade) == n and all(len(l) == n for l in grade), (ident, [len(l) for l in grade])
    (base / "grades").mkdir(parents=True, exist_ok=True)
    (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
    listas = {c: [] for c in ORDEM}
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                listas[camada(x, y, ch, ident)].append(f"{x},{y},{PALETA[ch]}")
    d = base / f"listas/{ident}"
    d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    (d / "ordem.txt").write_text(",".join(ORDEM) + "\n", encoding="utf-8")
    print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    for ident in sys.argv[2:] or DESENHOS:
        gravar(pathlib.Path(sys.argv[1]), ident)
