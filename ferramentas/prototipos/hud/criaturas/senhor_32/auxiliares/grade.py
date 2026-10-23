"""O Senhor da Guerra construído em 32×32 nativos e adaptado à mão para 16 (pedido do Jean, 23/10/2026; protótipo, nada
no jogo), o caminho do Dragão de Gelo e do Espantalho: primeiro o estudo nativo de 32, pela referência
`Senhor da guerra caolho-3.png` (o veterano de cabeça raspada em três quartos, a testa pesada sobre o olho visível
semicerrado, a venda com a tira subindo pela testa até a orelha, a cicatriz atravessando, o nariz, o bigode, a boca e a
barba separados, a expressão severa); depois a proposta de 16, redesenhada à mão com o 32 como mapa. Os retratos
aprovados (o Mercenário) dão a pele e a luz de cima e da esquerda. As guias (a referência reduzida por média, o
recorte de 880 px a partir de (230, 190): o alto da cabeça sai do quadro) mediram as posições e ficam ocultas nas fontes.
Uma letra por pixel; o contorno faz parte do desenho.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "1a120c", "k": "120c08", "K": "2c2622", "L": "4a423c", "P": "dcac84", "p": "c09070",
          "q": "9a6c52", "g": "6e4a38", "G": "4e3024", "r": "8a2e2e", "e": "b8ac98", "m": "7a5236",
          "n": "5a3a24", "N": "3a2418", "F": "4a3428", "f": "6a4c36"}
GRADE_32 = [
    ".......oqppPPppppqqqgo..........",
    "......oqpPPPppppqqqqggo.........",
    ".....okKpPPPpppqqqqqggo.........",
    ".....oqkKPPpppqqqqqqgggo........",
    "....oqpPkKqqqppqqrqqggggo.......",
    "....oqpPPkKPpppqqrqqqggggo......",
    "....oqppqqkKqqpqqgrqqqgggo......",
    "....oqpPPppkKppqqgrqqqgggo......",
    "....ogPPPppqkKqggGrgqqgggo......",
    "....ogpPppqqgkKkkkkkGqqggo......",
    "....oNNnppqggGkKLKKKkkqggo......",
    "....ogNNNnGqgkKLLKKKKkkkgpqo....",
    "....oGkkkGgpqkKLKKKKKkggGgpo....",
    "....oGekgGqPgkKKKKKKKkqqgqpo....",
    "....oqggqgpPqgkKKKKKKkpqgGpo....",
    "....opPPpqpPpggkKKKKkqpqgqqo....",
    "....oqppqpPPpgqgkkkkgppqgqo.....",
    "....ogpqgPPpgqppqrppqqqggo......",
    "....ogqgGgGGgqgqpqrqqggno.......",
    "....ongnmnmnNgqgqqgqgnNno.......",
    "....oNnmnmnmnNgqggqgnmnNo.......",
    "....onNNkkkkkNNnnmnNnmnNo.......",
    "....onNgqpPpqgNnmnNnnNnNooo.....",
    "....omnNGggGNnmnNnmnNnmooFfFo...",
    ".oooonmmnNnmmnNnmnNnmnNoFfFFfo..",
    "oFfFoNnmnNNnmnNNnmnNnnNoFFfFFfo.",
    "FfFfooNnnNmnnNnmnNNmnNooFfFFfFfF",
    "FFfFFooNnNnmnNNnmnNnnooFfFFfFFfF",
    "fFFfFFooNNnmnNnnNNnNooFFfFFfFFfF",
    "FfFFfFFooNNnNNnmNnNooFfFFfFFfFFF",
    "FFfFFFfFooNNnNNnNNooFFfFFFfFFfFF",
    "FfFFfFFFFooNNNnNNooFFFfFFFFfFFFF",
]
GRADE_16 = [
    "...oqpPppqqgo...",
    "..okPPppqqqggo..",
    "..oqkPqpqrqggo..",
    "..oppkpqqrqggo..",
    "..oPPpgkkkGqgo..",
    "..oNNGkKLKkkgqo.",
    "..oekPkKKKkggpo.",
    "..opqPgkkkgpgqo.",
    "..oqPpgpqrpqgo..",
    "..ogGGgqqqgnno..",
    "..onmnmNggnmNo..",
    "..oNkkkNnmnNoFfo",
    "oFonqpqNmnNoFfFo",
    "FfoNnmnNmnNoFfFF",
    "FFfoNnmNnNoFfFFf",
    "fFFFoNnNNoFFfFFF",
]
# cada desenho: a grade, o lado e a guia
DESENHOS = {"senhor-n32": (GRADE_32, 32, "guias/senhor-guia-32.png"),
            "senhor-n16": (GRADE_16, 16, "guias/senhor-guia-16.png")}
# o preto do olho e da boca (o resto do preto é a venda e a tira): as linhas do olho, até que coluna, e a linha da boca
TRACOS = {"senhor-n32": ((12, 13), 8, 21), "senhor-n16": ((6,), 4, 11)}
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "manto", "pele", "barba", "cicatriz", "tracos", "venda", "contorno"]


def camada(x, y, ch, ident):
    olho, ate, boca = TRACOS[ident]
    if ch == "o":
        return "contorno"
    if ch == "k":
        return "tracos" if (y in olho and x <= ate) or y == boca else "venda"
    if ch in "KL":
        return "venda"
    if ch == "e":
        return "tracos"
    if ch == "r":
        return "cicatriz"
    if ch in "mnN":
        return "barba"
    if ch in "Ff":
        return "manto"
    return "pele"


def imagem(ident):
    grade, n, _ = DESENHOS[ident]
    im = Image.new("RGBA", (n, n))
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(PALETA[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ident):
    grade, n, guia = DESENHOS[ident]
    assert len(grade) == n and all(len(l) == n for l in grade), (ident, [len(l) for l in grade])
    (base / "grades").mkdir(parents=True, exist_ok=True)
    (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
    g = Image.open(base / guia).convert("RGBA")
    listas = {c: [] for c in ORDEM}
    listas["guia"] = [f"{x},{y},{''.join(f'{v:02x}' for v in g.getpixel((x, y)))}" for y in range(n) for x in range(n)
                      if g.getpixel((x, y))[3]]
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
