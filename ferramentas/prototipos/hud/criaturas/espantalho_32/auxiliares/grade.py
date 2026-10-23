"""O Espantalho Possuído construído em 32×32 nativos e adaptado à mão para 16 (pedido do Jean, 23/10/2026; protótipo,
nada no jogo), o caminho do Dragão de Gelo: primeiro o estudo nativo de 32, pela referência
`Espantalho possuído em pixel art-5.png` (o chapéu velho e deformado, a cabeça de estopa com volume e dobras, os olhos
fundos com brasas, a boca costurada cruel, a palha saindo da gola); depois a proposta de 16, redesenhada à mão com o 32
como mapa de anatomia e volumes (não uma redução automática). As guias (a referência reduzida por média) mediram as
posições e ficam ocultas nas fontes. Uma letra por pixel; o contorno faz parte do desenho.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "1a120a", "D": "241c14", "d": "3a3028", "t": "3a2a18", "h": "5a3a22", "H": "7a5232", "j": "9a6a40",
          "J": "b48452", "C": "46361f", "c": "5e4a2c", "B": "8a7044", "b": "b89860", "w": "d8c088", "k": "120c06",
          "r": "c03020", "R": "f07830", "y": "d8b048", "Y": "a07c30"}
GRADE_32 = [
    "................ojhoo...........",
    "...............ojHHhhoo.........",
    "..............ojJHHHhhhoo.......",
    ".............ojJjHHHHhhhhoo.....",
    "............ojJjHHHHhHHhhhto....",
    "...........ojJjjHHHhthHhhhto....",
    "..........ojJjjHHHhHthhhhtto....",
    ".........ojJjjHHHHhHhhhtooo.....",
    "...ooooooHhhtthtttthtttthooo....",
    ".oohHjjjHtthttthtttthttttHHhoo..",
    "ohjjJJJjjjjjjHHHHHHHHHHhhhhhhto.",
    "othHHHHHHHhhhhhhhhhhhhhhhhhhhhto",
    ".ottooooCCCCCCCCCCCCCCCthHHhhhto",
    "..oo...oCcBBBBBcBBBBcccCthHHhhto",
    "......oCcbbbbbBcBBBBBccCthHHhhto",
    "......oCcbtttbbcBBBBBccCthHjHhto",
    "......oCcbkktttcBBBBtttCthHHhhto",
    "......oCcbkrRkbcBtttkkcCthHHhhto",
    "......oCcbbkkkkcBBkRrkcCthHhhhto",
    "......oCcbbbBBbcBkkkcccCothHhhht",
    "......oCcbbcbbbcBBBcctcCoothhhht",
    ".......oCbbbctbctBBttcCo..oothht",
    ".......oCcbBttttttttBcco....oooo",
    "........oCctBtBBtBBccCo.........",
    ".........oCCcbBBBBcCCCo.........",
    "......oooooCCBBBBcCcCoo.oo......",
    "ooooooYyYytcttctcttctyYoyYoooooo",
    "ddccccYydyYdyyDyYDYyyYDyYDdddddd",
    "ddddYyddyYddyYDyyDDyyyYDDyYDDDDD",
    "ddYydddyYddyYdDyYDDYyDyYDDDyYDDD",
    "YyddddyddddYddDDYDDDDDDyYDDDDyYD",
    "ddddddddddddddDDDDDDDDDDYDDDDDDD",
]
GRADE_16 = [
    ".......ojho.....",
    "......ojHHhoo...",
    ".....ojJHHhhho..",
    "....ojJHHHhthto.",
    "ooooHhtthttthooo",
    "hjJJjjjHHHHHhhht",
    "thHHhhhhhhhhhhht",
    "oooCcbbBcBBcCtHh",
    "..oCttbcBcttCtHh",
    "..oCbRkbBkRcCthh",
    "..oCbbkbBktcCoth",
    "...oCttttBcCo.oo",
    "...ooCbtBcCoo...",
    "oooYytcttctyYooo",
    "ddyYdydyDyDDDyYD",
    "yYddyddyDDyDDDDy",
]
# cada desenho: a grade, o lado e a guia
DESENHOS = {"espantalho-n32": (GRADE_32, 32, "guias/espantalho-guia-32.png"),
            "espantalho-n16": (GRADE_16, 16, "guias/espantalho-guia-16.png")}
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "casaco", "estopa", "chapeu", "palha", "costura", "olhos", "contorno"]


def camada(x, y, ch, n=32):
    aba, pescoco, lado = (12, 26, 23) if n == 32 else (6, 13, 13)
    if ch == "o":
        return "contorno"
    if ch in "kRr":
        return "olhos"
    if ch in "hHjJ":
        return "chapeu"
    if ch == "t":  # o escuro da faixa e da aba, a corda do pescoço, ou a costura (a boca e as sobrancelhas)
        return "chapeu" if y <= aba or x >= lado else ("palha" if y >= pescoco else "costura")
    if ch in "yY":
        return "palha"
    if ch in "dD":
        return "casaco"
    return "estopa"


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
                listas[camada(x, y, ch, n)].append(f"{x},{y},{PALETA[ch]}")
    d = base / f"listas/{ident}"
    d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    (d / "ordem.txt").write_text(",".join(ORDEM) + "\n", encoding="utf-8")
    print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    for ident in sys.argv[2:] or DESENHOS:
        gravar(pathlib.Path(sys.argv[1]), ident)
