"""A Hidra do Brejo construída em 32×32 nativos e adaptada à mão para 16 (pedido do Jean, 23/10/2026; protótipo, nada no
jogo), o caminho do Dragão de Gelo: as três cabeças de réptil olhando para a ESQUERDA (a orientação corrigida pelo Jean;
a referência `Hidra do pântano de três cabeças-1.png` dá o material, a anatomia e a expressão, não a direção), com
focinho, testa e mandíbula de verdade e pescoços grossos ligados ao corpo. A cabeça principal na frente, embaixo e à
esquerda, a boca entreaberta com as presas; a segunda no alto, atrás; a terceira à direita, no meio, atrás e em parte
escondida. As tentativas recusadas (a H1, a H2 e a `hidra-t`: cabecinhas na ponta de pescoços finos) não foram usadas. A
guia (a referência reduzida por média) fica oculta na fonte. Cada desenho foi pintado em três partes, da cabeça de trás
para a da frente (`pintar`): a de trás é coberta pela da frente onde se sobrepõem.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "101810", "s": "24382a", "m": "3a5a3e", "l": "5a7e52", "h": "82a06a", "k": "0a0c08",
          "e": "d8c040", "d": "e0d8b8", "r": "8a2e2e", "R": "4a1414"}


def pintar(partes, n):
    """Cada parte é uma lista de (linha, x, pixels); '.' não pinta. As de depois cobrem as de antes."""
    g = [["."] * n for _ in range(n)]
    for parte in partes:
        for y, x, s in parte:
            for i, ch in enumerate(s):
                if ch != "." and 0 <= x + i < n:
                    g[y][x + i] = ch
    return ["".join(l) for l in g]


# o estudo de 32: a cabeça de cima (B), a da direita (C) e a principal (A), nessa ordem
B = [
    (0, 14, "ooooooooo"),
    (1, 11, "ooohhhsshhhhoo"),
    (2, 10, "olklllmseksmmso"),
    (3, 10, "olllllmmssmmmso"),
    (4, 10, "ommmmmmmmmmmmso"),
    (5, 10, "oooooooooommsso"),
    (6, 11, "ollmmmmmmmssso"),
    (7, 12, "oossmmmmmmssso"),
    (8, 15, "ossmmmmmmsssso"),
    (9, 17, "osmmmmmmssssso"),
    (10, 18, "osmmmmmmssssss"),
    (11, 19, "osmmmmmsssssss"),
]
# a cabeça da direita, atrás (C): o focinho para a esquerda, escondido em parte atrás da A
C = [
    (11, 23, "ooooooooo"),
    (12, 20, "ooohhhsshhhh"),
    (13, 19, "olklllmseksmm"),
    (14, 19, "ollllmmmssmmm"),
    (15, 19, "ommmmmmmmmmmm"),
    (16, 19, "oooooooooommm"),
    (17, 20, "ollmmmmmmsmm"),
    (18, 21, "oossssmmmmm"),
    (19, 24, "smmmmmmmm"),
    (20, 24, "smmmmmmmm"),
    (21, 24, "smmmlmmmm"),
    (22, 24, "smmmlmmmm"),
    (23, 24, "smmmlmmmm"),
    (24, 24, "smmmlmmmm"),
    (25, 24, "smmlmmmmm"),
    (26, 23, "osmmlmmmmm"),
    (27, 23, "osmmlmmmmm"),
    (28, 23, "osmllmmmmm"),
    (29, 23, "osmllmmmmm"),
    (30, 22, "ossmllmmmmm"),
    (31, 22, "ossmllmmmmm"),
]
# a cabeça principal (A), na frente: o focinho longo e chato, a crista da testa sobre o olho de fenda, o lábio com as
# presas, a boca em cunha (alta na frente, fechando para trás), a mandíbula forte e o pescoço grosso
A = [
    (10, 8, "ooooooo"),
    (11, 3, "ooooohhhhhhhoooo"),
    (12, 1, "oollllhhhssshlllmmo"),
    (13, 0, "olkllllmmseksmllmmmmo"),
    (14, 0, "ollllllmmssssmmlmmmmo"),
    (15, 0, "ommmmmmmmmmmmmmllmmso"),
    (16, 0, "oooooooooooooommlmmso"),
    (17, 0, "..dRRRRdRRRRRomllmmso"),
    (18, 0, "..oRrrRRRRooommlmmsso"),
    (19, 0, "..odRRoooooommmlmmmsso"),
    (20, 0, "..ollllllmmmmmlmmmsso"),
    (21, 0, "...ossmmmmmmmmmmmsso"),
    (22, 0, "....oooosssmmmmmmssso"),
    (23, 5, "ooolllmmmmmmssso"),
    (24, 8, "olllmmmmmmssso"),
    (25, 8, "olhllmmmmmsssso"),
    (26, 8, "olhllmmmmmssssso"),
    (27, 9, "olhllmmmmmsssso"),
    (28, 9, "olhllmmmmmssssso"),
    (29, 10, "olhllmmmmmssssso"),
    (30, 10, "olhllmmmmmsssssso"),
    (31, 11, "olhllmmmmmsssssso"),
]
GRADE_32 = pintar([B, C, A], 32)

# a proposta de 16, redesenhada à mão com o 32 como mapa
B16 = [
    (0, 6, "oooooo"),
    (1, 4, "oohhhsso"),
    (2, 3, "olllmsekso"),
    (3, 3, "oooooommsso"),
    (4, 5, "ollmmmssso"),
    (5, 9, "osmmssso"),
    (6, 11, "smssss"),
]
C16 = [
    (5, 12, "oooo"),
    (6, 10, "oohhsso"),
    (7, 9, "olllseks"),
    (8, 9, "oooooomm"),
    (9, 11, "osssmm"),
    (10, 12, "smlm"),
    (11, 12, "smlm"),
    (12, 12, "smlmm"),
    (13, 11, "osmlmm"),
    (14, 11, "osmlmm"),
    (15, 11, "osmlmm"),
]
A16 = [
    (5, 2, "oohhhhoo"),
    (6, 0, "olllhsslmo"),
    (7, 0, "oklllekmmmo"),
    (8, 0, "ooooooomlmso"),
    (9, 0, ".dRrRRomlmso"),
    (10, 0, ".ollllmmmmso"),
    (11, 0, "..oossmmmsso"),
    (12, 4, "olhmmmsso"),
    (13, 4, "olhlmmmsso"),
    (14, 5, "olhlmmmsso"),
    (15, 5, "olhlmmmssso"),
]
GRADE_16 = pintar([B16, C16, A16], 16)
# cada desenho: a grade, o lado e a guia
DESENHOS = {"hidra-n32": (GRADE_32, 32, "guias/hidra-guia-32.png"),
            "hidra-n16": (GRADE_16, 16, "guias/hidra-guia-16.png")}
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "escamas", "boca", "olhos", "contorno"]


def camada(x, y, ch, ident):
    if ch == "o":
        return "contorno"
    if ch in "ek":  # o olho (âmbar com a pupila) e a narina
        return "olhos"
    if ch in "drR":
        return "boca"
    return "escamas"


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
