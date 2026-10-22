"""O Esqueleto do zero (21/10/2026, pedido do Jean): o inimigo na linguagem dos retratos aprovados (a cabeça com um
pedaço do ombro ou da roupa enchendo o quadro, sem contorno, a paleta contida, os traços pequenos, a luz da
esquerda), sem relação com as tentativas anteriores (A, B, A2, A2n, S1, S2, C, C2). Três direções, 16×16; o osso mais
apagado que antes, para não ser o retrato mais claro da fileira:
  - E1, o guarda morto: o elmo de ferro com o nasal e a ferrugem sobre a caveira, as órbitas na sombra da aba, a
    careta dos dentes, a malha nos ombros (o Esqueleto de Guarda, as ruínas);
  - E2, o encapuzado: a caveira na sombra de um capuz de pano roído, na língua do Bandido;
  - E3, a caveira nua: em três quartos para a esquerda (a órbita de perto maior), a mandíbula entreaberta, a coluna e
    as clavículas.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

CORES = {
    # o osso apagado (a luz, o meio, a sombra, a sombra funda) e as cavidades
    "B": "cbbf9c", "b": "a39776", "d": "776d54", "D": "4d4636", "k": "15120f",
    # o ferro do elmo e da malha, e a ferrugem
    "I": "a4a6a0", "i": "7b7e78", "j": "555853", "J": "363936", "R": "7c4a2a", "r": "a2663a",
    # o pano do capuz
    "H": "6b5c4c", "h": "4d4238", "g": "342c26", "G": "221d19",
}
# E1, o guarda morto
E1 = [
 "......iIIi......",
 "....iIIIiiij....",
 "...iIIiiiiijj...",
 "...iIiiiRiijj...",
 "..JjjjjiijjRjJJ.",
 "...DbbbijbbbD...",
 "...bkkdijdkkb...",
 "...bkkdijdkkd...",
 "...dBbbkkbbdD...",
 "....bBdkkdbD....",
 "....DdbBbbdD....",
 ".....DkkkkD.....",
 ".....dbBbdD.....",
 "..jjjJDddDJjjj..",
 ".iIijjJddJjjiIj.",
 "iIiijjjJJjjjiiIj",
]
# E2, o encapuzado
E2 = [
 ".....hhHHhh.....",
 "....hHHHhhhg....",
 "...hHHhhhhhgg...",
 "..hHHhgggghhgg..",
 "..hHhgDbbDghgg..",
 "..hHgDbBBbDghg..",
 ".hHhgbkkbkkdghg.",
 ".hHhgbkkbkkdghg.",
 ".hHhgdbbkbbDghgG",
 ".hHhggdbkbdgghgG",
 "hHHhggDbDbDgghgG",
 "hHhhgggdkdggghgG",
 "hHhhggggggggghgG",
 "hHhhhgggggggghhG",
 "HHhhhhgggggghhhG",
 "HHhhhhhggghhhhhG",
]
# E3, a caveira nua, em três quartos
E3 = [
 "................",
 "......dbBBbbd...",
 ".....bBBBbbbbd..",
 "....bBBbbbbbddD.",
 "....bBbbbbbbddD.",
 "...dbbbdbbbdddD.",
 "...kkkDbbDkkddD.",
 "...DkkdbbdkkdD..",
 "..bBbbbdbbbddD..",
 "...dbDkbbbdD....",
 "...dbDbDbdD.....",
 "....DkkkkD......",
 "....dbDbdD......",
 ".....dbbdD......",
 "...Dd..bdD..dbD.",
 "dbbBbdDdbbdDbbBd",
]


CAMADAS = {
    "esqueleto-e1": (E1, ["ombros", "cranio", "elmo", "cavidades"],
                     lambda x, y, ch: "cavidades" if ch == "k" else "ombros" if y >= 13
                     else "elmo" if ch in "IijJRr" else "cranio"),
    "esqueleto-e2": (E2, ["capuz", "cranio", "cavidades"],
                     lambda x, y, ch: "cavidades" if ch == "k" else "capuz" if ch in "HhgG" else "cranio"),
    "esqueleto-e3": (E3, ["ombros", "cranio", "cavidades"],
                     lambda x, y, ch: "cavidades" if ch == "k" else "ombros" if y >= 14 else "cranio"),
}


def imagem(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(CAMADAS[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(CORES[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, ordem, camada = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{CORES[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + "\n", encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
