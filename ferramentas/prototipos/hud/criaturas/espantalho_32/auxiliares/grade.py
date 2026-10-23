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
          "r": "c03020", "R": "f07830", "y": "d8b048", "Y": "a07c30", "g": "5a4c42", "G": "75665a",
          "x": "8a2414"}
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
# O refino (23/10/2026, o N32 e o N16 preservados): o quadro mais perto, pela sugestão do Jean (a ponta da copa e as
# pontas da aba saem pelas bordas, o rosto cresce de ~14 para ~17 px no 32); o chapéu reto, levemente inclinado, sem a aba
# caída; o rosto afunilando para o queixo, a testa e as órbitas oblíquas fazendo a ameaça, as brasas contidas, a boca
# numa costura torta sobre a estopa e a palha em dois tufos com o vão da corda no meio. O 16 redesenhado à mão com o 32R
# como mapa (no 16, a brasa é o vermelho escuro: o laranja num pixel de 2×2 virava um ponto aceso).
GRADE_32R = [
    "...........ojHHHhhhhhto.........",
    "..........ojJHHHhhhhthho........",
    ".........ojJjHHHhhhhthhho.......",
    "........ojJjHHHHhhhhhthho.......",
    "........ojjHHHtHhhhhhhthho......",
    ".......ojjHHHHthHhhhhhhhto......",
    ".oohHjogGGggdgggdddgddgdto......",
    "ohHjjJjttdtddtdttdtddtddthhoo...",
    "hjJJjjjHHjHHHHHhHHHhHhhhhhhhhoo.",
    "tHjjjjjHHHHHHHHHHHHHhhhhhhhhhhht",
    "othHHHHHhhhhhhhhhhhhhhhhhhhhhhhh",
    ".ottttttttottttttttttttthhhhhhht",
    ".oo.occCCCCCCCCCCCCCCCottotttto.",
    "....oBccCcCCCCCCCCCCCCo.........",
    "....obbbBBBbBBcBBcccCCo.........",
    "....obbCCtBBBcBBBcccCCo.........",
    "....obCtttkBBcBBBcccCCo.........",
    "....obCCkkRktBcccCttCCo.........",
    "...obbbcCkkCtBcttkkcCCo.........",
    "...obbwbbBcBtkRkCcccCCo.........",
    "...obbwbbBBbBcCccBccCCo.........",
    "....obbbBbBBBcCcBBcccCo.........",
    ".....obbbBbBBBcBBBccCo..........",
    "......obbbBcBBBcBBctCo..........",
    ".......obbBcttbcBttCCo..........",
    "........otttBbtttBcCCo..........",
    "......oodoBcBBBcBcCCCodoo.......",
    "..ooddddyYoBBBBccCCoyYdddooo....",
    "odddddyYdyYocBcCCoyYddyYddddoo..",
    "dddddyYdyYhHHtHHhtdyYdddyYdddddo",
    "dddyYddyYDDDDhtDDDDdyYddddyYdddd",
    "ddYdddyYDDDDDDhDDDDDDyYdddddYddd",
]
GRADE_16R = [
    ".....ojHHhhto...",
    "....ojJHHhhtho..",
    "ohHgGgdggdgddto.",
    "jJjjHjHHHHhhhhhh",
    "otttttttthhhhhhh",
    "..oBcCCCCCCCtttt",
    "..obbBBBcBcCo...",
    "..obCtBBccCCo...",
    "..obkrtBcttCo...",
    ".obwbcBkrkCCo...",
    ".obwbcbcCctCo...",
    "..obttBtttco....",
    "...obBcBcCCo....",
    "..yyoBccCoyyo...",
    ".yYyhHtHhdYyyo..",
    "yYdYDDhDDDdYdyYd",
]
# A passagem local no rosto do N16R (23/10/2026, o N16R preservado): só as linhas 7 a 10, com o N32R como referência de
# expressão. Os olhos na mesma linha (no 16 a inclinação fica na aba; a linha de diferença lia como erro), as sobrancelhas
# descendo até se encontrar sobre o nariz, as brasas no canto de dentro de fendas escuras (a do lado da sombra num vermelho
# apagado, "x"), a sombra marrom embaixo em vez do preto (o preto fazia órbitas de caveira), as bochechas com volume e o
# canto da costura subindo.
GRADE_16R2 = list(GRADE_16R)
GRADE_16R2[7:11] = [
    "..otCcBcCtCCo...",
    "..oCkrttxkCCo...",
    ".obbcCBcCCcCo...",
    ".obwbBbCcBtCo...",
]
# cada desenho: a grade, o lado e a guia
DESENHOS = {"espantalho-n32": (GRADE_32, 32, "guias/espantalho-guia-32.png"),
            "espantalho-n16": (GRADE_16, 16, "guias/espantalho-guia-16.png"),
            "espantalho-n32r": (GRADE_32R, 32, "guias/espantalho-r-guia-32.png"),
            "espantalho-n16r": (GRADE_16R, 16, "guias/espantalho-r-guia-16.png"),
            "espantalho-n16r2": (GRADE_16R2, 16, "guias/espantalho-r-guia-16.png")}
# onde cada desenho separa a aba, o pescoço e a aba caída (o "t" e os marrons mudam de camada por posição)
CORTES = {"espantalho-n32": (12, 26, 23), "espantalho-n16": (6, 13, 13),
          "espantalho-n32r": (12, 27, 99), "espantalho-n16r": (5, 13, 99),
          "espantalho-n16r2": (5, 13, 99)}
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "casaco", "estopa", "chapeu", "palha", "costura", "olhos", "contorno"]


def camada(x, y, ch, ident):
    aba, pescoco, lado = CORTES[ident]
    if ch == "o":
        return "contorno"
    if ch in "kRrx":
        return "olhos"
    if ch in "hHjJ":  # o chapéu, ou a corda na gola
        return "palha" if y >= pescoco else "chapeu"
    if ch in "gG":  # a faixa do chapéu
        return "chapeu"
    if ch == "t":  # o escuro da faixa e da aba, a corda do pescoço, ou a costura (a boca e as sobrancelhas)
        return "chapeu" if y <= aba or x >= lado else ("palha" if y >= pescoco else "costura")
    if ch in "yY":
        return "palha"
    if ch in "dD":  # o casaco, ou o escuro da faixa
        return "chapeu" if y <= aba else "casaco"
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
