"""O Lich Menor construído em 32×32 nativos e adaptado à mão para 16 (pedido do Jean, 23/10/2026; protótipo, nada no
jogo), o caminho do Dragão de Gelo, com a identidade da L1b (`chefes_e_especiais/`): a coroa antiga, o crânio exposto, os
olhos verdes sobrenaturais e o manto violeta; um feiticeiro morto antigo, severo e consciente. Em close: a coroa pesada
encaixada sobre a testa, o crânio com volume (a testa larga, as têmporas recolhidas, as maçãs salientes, a face
estreitando até a mandíbula fina e o queixo), as órbitas fundas descendo para o nariz com o verde contido, a cavidade do
nariz separada, a mordida fechada numa linha escura com os dentes em grupos e a gola alta do manto sustentando o busto,
com o fecho de ouro. Sem livro nem acessórios. Sem guia: o desenho parte da L1b, não de uma referência externa. Uma letra
por pixel; o contorno faz parte do desenho.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "100c0e", "W": "e2d8b8", "b": "cbbf9c", "B": "a39776", "c": "776d54", "d": "4d4636",
          "k": "0a0808", "R": "2a1e30", "r": "4a3450", "s": "6a4e7a", "S": "8a6aa0", "Z": "e8c860",
          "y": "c8a040", "Y": "8a6a28", "f": "60e080", "F": "c0ffc8", "g": "1e3a26"}
GRADE_32 = [
    "...............oZo..............",
    ".........oZo..oyZyo..oyo........",
    "........oyZyooyyZyYooyyYo.......",
    ".......oyyyyyyyyZyyyyyyyYo......",
    ".......oYyysyyYyfyYyysyyYo......",
    ".......oYYYYYYYYYYYYYYYYYo......",
    ".......odbWWbbbbbbbBBBBcdo......",
    ".......odbWbbbbbbbbbBBBcdo......",
    "........odbbbbbBBbbbbBBco.......",
    "........obWbbcBbBbcbbBBco.......",
    "........obcdddcBbBcdddcco.......",
    ".........odkkkdBbBdkkkdo........",
    ".........okkgFkcBckFgkko........",
    ".........odkkfdcBcdfkkdo........",
    "........oWbdddcBdBcdddBBo.......",
    "oRo.....obWbBccdkdccBBBco....oRo",
    "oRRoRRRRRocBcdckkdcdcBcoRRRRoRRo",
    "orRRoRRRRRodcBbBbBbBcdoRRRRoRRro",
    "osrRRoRRRRodcbBdbbdBbcoRRRoRRrso",
    "oSsrRRoRRRodkkkkkkkkkdoRRoRRrsSo",
    "oSsrRRRoRRRokBbdbBdbkoRRoRRRrsSo",
    "oSsrRRRoRRRocBbbbbBcdoRRoRRRrsSo",
    "oSsrRRRRoRRRocBbBBcdoRRoRRRRrsSo",
    "oSsrRRRRoRRRRodcccdoRRRoRRRRrsSo",
    "oSsrRRRRRRRRRRoooooRRRRRRRRRrsSo",
    "oSsrRRRRRRRRRRRRRRRRRRRRRRRRrsSo",
    "oSsrRRRRRRRRRRRRRRRRRRRRRRRRrsSo",
    "oSsrRRRRRRRRRRRRRRRRRRRRRRRRrsSo",
    "oSsrRRRRRRRRRRRoyoRRRRRRRRRRrsSo",
    "oSsrRRRRRRRRRRoyZyoRRRRRRRRRrsSo",
    "oSsrRRRRRRRRRRRoyoRRRRRRRRRRrsSo",
    "oSsrRRRRRRRRRRRRRRRRRRRRRRRRrsSo",
]
GRADE_16 = [
    "....y...Z...y...",
    "...oyyyyZyyyyo..",
    "...oYysyfysyYo..",
    "....obWbbbBco...",
    "....oddcBcddo...",
    "....okfkBkfko...",
    "oRo.obcdkdcBooRo",
    "osRoRocBbBcooRso",
    "oSsRoobBdBboRsSo",
    "oSsRRodkkkdoRsSo",
    "oSsRRRocBcoRRsSo",
    "oSsRRRRoooRRRsSo",
    "oSsRRRRRRRRRRsSo",
    "oSsRRRRRyRRRRsSo",
    "oSsRRRRRRRRRRsSo",
    "oSsRRRRRRRRRRsSo",
]
# cada desenho: a grade e o lado
DESENHOS = {"lich-n32": (GRADE_32, 32), "lich-n16": (GRADE_16, 16)}
# a última linha da coroa em cada desenho (o "s" e o "f" acima dela são as pedras da coroa)
COROA = {"lich-n32": 5, "lich-n16": 2}
# as camadas, de baixo para cima
ORDEM = ["manto", "cranio", "coroa", "olhos", "contorno"]


def camada(x, y, ch, ident):
    if ch == "o":
        return "contorno"
    if y <= COROA[ident] and ch in "yYZsf":
        return "coroa"
    if ch in "fFg":
        return "olhos"
    if ch in "RrsS" or (ch in "yZ" and y > COROA[ident]):  # o manto e o fecho de ouro
        return "manto"
    if ch in "yYZ":
        return "coroa"
    return "cranio"


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
