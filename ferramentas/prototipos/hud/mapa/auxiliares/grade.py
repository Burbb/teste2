"""As peças do primeiro lote da 1E.4 (23/10/2026; protótipo, nada no jogo): as marcas que ficam por cima do mapa e do
minimapa, desenhadas à mão no tamanho em que aparecem (1:1 na tela; o mapa grande e o minimapa têm cada um o seu):

  - posicao (19×17) e posicao-mini (13×12): o "você está aqui", a seta de ouro apontando para o lugar (a direção A);
  - posicao-plaqueta (20×22): a moldura de ouro com a ponta, onde entra a figura de 16 do herói (a direção B; a figura
    é a aprovada, de retratos.js, e não está aqui; no mapa grande, a plaqueta e a figura a 2×);
  - missao (11×14) e missao-mini (9×11): a plaqueta de ouro com o "!" (o objetivo da missão);
  - contrato (11×14) e contrato-mini (9×11): o cartaz do mural, com o lacre vermelho e as linhas (um contrato aceito);
  - cancela (19×11) e cancela-mini (13×9): a barreira de madeira com a faixa vermelha (a saída fechada).
A primeira passada (23/10) tinha as marcas do minimapa no mapa grande e outras ainda menores no minimapa: pequenas
demais ao lado dos ícones de 40 e de 32. Ficaram as maiores no minimapa e as novas, desenhadas para o mapa grande.

O ouro é a rampa da Iniciativa (estado-iniciativa-16), o papel e o vermelho os do Marcado, o contorno o comum da
família (08080a). Uma letra por pixel; o contorno faz parte do desenho.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETA = {"a": "08080a",
          "b": "fff6c8", "c": "f6d86a", "d": "e0b83a", "e": "b08418", "f": "6b4a0e",  # o ouro
          "K": "1a1714",  # o fundo da plaqueta (o carvão)
          "w": "f1e4c4", "v": "cfc6b0", "u": "a89e88", "k": "8a8070",  # o papel e as linhas escritas
          "R": "ec5a4c", "r": "c42a2e", "q": "8a1418",  # o lacre e a faixa
          "p": "b08a58", "P": "8a6a3e", "o": "5a4028"}  # a madeira
DESENHOS = {
    # o mapa grande (a 1:1 ao lado do ícone de 40)
    "posicao": [
        "......aaaaaaa......",
        "......abccdda......",
        "......acccdea......",
        "......acccdea......",
        "......acccdea......",
        "......acccdea......",
        "aaaaaaacccdeaaaaaaa",
        "abcccccccccdddddeea",
        ".acccccccccdddddea.",
        "..accccccccddddea..",
        "...acccccccdddea...",
        "....accccccddea....",
        ".....acccccdea.....",
        "......accccea......",
        ".......accea.......",
        "........aea........",
        ".........a.........",
    ],
    "missao": [
        ".aaaaaaaaa.",
        "abbccccddea",
        "abccaaadeea",
        "acccaaadeea",
        "acccaaadeea",
        "acccaaadeea",
        "accccaddeea",
        "accccaddeea",
        "acccccddeea",
        "acccaaadeea",
        "acccaaadeea",
        "accccdddeea",
        "addeeeeeefa",
        ".aaaaaaaaa.",
    ],
    "contrato": [
        "aaaaaaaaaaa",
        "awwwrRrwwva",
        "awwwqrqwwva",
        "awwwwqwwwva",
        "awkkkkkkwva",
        "awwwwwwwwva",
        "awkkkkkwwva",
        "awwwwwwwwva",
        "awkkkkkkwva",
        "awwwwwwwwva",
        "awkkkkwwwva",
        "awwwwwwwwva",
        "avvvvvvvvua",
        "aaaaaaaaaaa",
    ],
    "cancela": [
        ".aaaa.........aaaa.",
        ".appa.........appa.",
        "aaaaaaaaaaaaaaaaaaa",
        "awwwrrrwwwrrrwwwrra",
        "awwwrrrwwwrrrwwwrra",
        "aaaaaaaaaaaaaaaaaaa",
        ".appa.........appa.",
        ".aPPa.........aPPa.",
        ".aPPa.........aPPa.",
        ".aooa.........aooa.",
        ".aaaa.........aaaa.",
    ],
    # o minimapa (a 1:1 ao lado do ícone de 32)
    "posicao-mini": [
        "....aaaaa....",
        "....abcda....",
        "....accda....",
        "....accda....",
        "aaaaaccdaaaaa",
        "abcccccddddea",
        ".accccccddea.",
        "..acccccdea..",
        "...acccdea...",
        "....accea....",
        ".....aea.....",
        "......a......",
    ],
    "missao-mini": [
        ".aaaaaaa.",
        "abcccddea",
        "abccaddea",
        "acccaddea",
        "acccaddea",
        "acccaddea",
        "acccaddea",
        "acccdddea",
        "acccaddea",
        "adeeeeefa",
        ".aaaaaaa.",
    ],
    "contrato-mini": [
        "aaaaaaaaa",
        "awwrRrvva",
        "awwwrwvva",
        "awkkkkkva",
        "awwwwwwva",
        "awkkkkwva",
        "awwwwwwva",
        "awkkkwwva",
        "awwwwwwva",
        "avvvvvvua",
        "aaaaaaaaa",
    ],
    "cancela-mini": [
        ".aaa.....aaa.",
        ".apa.....apa.",
        "aaaaaaaaaaaaa",
        "awwrrwwrrwwra",
        "aaaaaaaaaaaaa",
        ".apa.....apa.",
        ".aPa.....aPa.",
        ".aoa.....aoa.",
        ".aaa.....aaa.",
    ],
    # a direção B do "você está aqui": a plaqueta (no minimapa a 1:1; no mapa grande a 2×, com a figura também a 2×)
    "posicao-plaqueta": [
        "..aaaaaaaaaaaaaaaa..",
        ".abcccccccccccccdda.",
    ] + ["ac" + "K" * 16 + "ea"] * 16 + [
        ".adeeeeeeeeeeeeeefa.",
        "..aaaaaaadeaaaaaaa..",
        "........adea........",
        ".........aa.........",
    ],
}
# as camadas, de baixo para cima
ORDEM = ["corpo", "marca", "contorno"]


def camada(ch):
    if ch == "a":
        return "contorno"
    if ch in "rRqk":
        return "marca"  # o lacre, a faixa e as linhas
    return "corpo"


def lado(ident):
    g = DESENHOS[ident]
    return len(g[0]), len(g)


def imagem(ident):
    g = DESENHOS[ident]
    w, h = lado(ident)
    im = Image.new("RGBA", (w, h))
    for y, l in enumerate(g):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(PALETA[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ident):
    g = DESENHOS[ident]
    w, h = lado(ident)
    assert all(len(l) == w for l in g), (ident, [len(l) for l in g])
    (base / "grades").mkdir(parents=True, exist_ok=True)
    (base / f"grades/{ident}.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    listas = {c: [] for c in ORDEM}
    for y, l in enumerate(g):
        for x, ch in enumerate(l):
            if ch != ".":
                listas[camada(ch)].append(f"{x},{y},{PALETA[ch]}")
    d = base / f"listas/{ident}"
    d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    (d / "ordem.txt").write_text(",".join(ORDEM) + "\n", encoding="utf-8")
    print(ident, f"{w}×{h}", {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    for ident in sys.argv[2:] or DESENHOS:
        gravar(pathlib.Path(sys.argv[1]), ident)
