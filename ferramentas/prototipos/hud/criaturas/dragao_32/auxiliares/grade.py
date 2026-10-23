"""O teste do Dragão de Gelo em 32×32 nativos (pedido do Jean, 23/10/2026; protótipo, nada no jogo). Uma proposta só,
desenhada à mão na grade de 32 (não o 16 ampliado): a guia (a referência `Cabeça ancestral de dragão de gelo-2.png`
reduzida a 32 por média) mediu as posições; os planos e o acabamento são à mão. Uma letra por pixel; o contorno faz parte
do desenho.
    python grade.py ..      # grava grades/dragao-n32.txt e listas/dragao-n32/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "0e1420", "S": "16243a", "s": "223450", "m": "3a5a80", "L": "5276a4", "l": "6a90b8", "h": "a8cce0",
          "w": "e8f4ff", "e": "e0a838", "E": "a06a20", "d": "e0e8f0", "D": "a8b0b8", "k": "080a10"}
GRADE = [
    "....................oo........oo",
    ".................ooolso....oools",
    "...............ooLlhlmo..ooLlhls",
    ".............ooLlhwhlmoooLlhhlso",
    "............oLlhhhlmsooLlhhlmso.",
    "...........oLlhhhlmsooLlhhlmso..",
    "..........oLlhhlmmsooLlhhlmso...",
    ".........oLlhllmmsSSlhhhlmso....",
    ".........oLhhlmmsmlmlhhhlmso....",
    "........oLllmmlhhlllhhllLmso....",
    "........oLLLlhwhlLLsLlLLmso.....",
    "......oomLLlhhhhhlLssLLmmSo.....",
    ".....oLhhlhhhhhllmSSmsLmmSooo...",
    "....olhhlhhhhhlLLsSmLLmmsmllho..",
    "....ohhlhhhhlLmsSsSmLLmmsmmllho.",
    "....ollLLllLmsSSmLLssLLmssmmmlho",
    "....oSmLsSSSSeeSsllLsLLmmsSllllh",
    "...oomhhLssSeeESlhhhLsLmmmmmmlls",
    ".ooLhhwhhlmsSsLslhhlLsmLmmsmmsoo",
    "oLhhhhlllLLLmmmmslhllLsmsmSsooo.",
    "olhlSSLllllLLLmsSLLLmmSsssSsmlho",
    "omlmmSlhhhlLskkkkSLmmssSsSSllllh",
    "oLmmmmmskkkkkLLLmsSmmmsSsssmmlls",
    "omskkkkkddLdLmmsSmmSsmmsssSmmsoo",
    "okkLlllLdDmLmmmsSmmmSsmmSsSsooo.",
    "oLLlLLmmDmmmmssSSsmmSssmssSsmlho",
    "omLLLmmmmmmssSSSsmmmmSsmsSSllllh",
    ".osmmLLmmssSooSSSmmLmmSssssmmlls",
    "..osmmLmsSoo..oSsmLLmmmSssSmmsoo",
    "...osmmsSo.....oSmLllmmsSsSsooo.",
    "....oSSoo.......oSmLlhlmssSsmlho",
    ".....oo.........oSsmLllmmSSllllh",
]
ID = "dragao-n32"
GUIA = "guias/dragao-guia-32.png"  # a referência reduzida, oculta na fonte
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "cabeca", "chifres", "crista", "boca", "dentes", "olho", "contorno"]


def camada(x, y, ch):
    if ch == "o":
        return "contorno"
    if ch in "eE":
        return "olho"
    if ch in "dD":
        return "dentes"
    if ch == "k":
        return "boca"
    if y <= 9:
        return "chifres"
    if x >= 26 and y >= 13:
        return "crista"
    return "cabeca"


def imagem():
    im = Image.new("RGBA", (32, 32))
    for y, l in enumerate(GRADE):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(PALETA[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base):
    assert len(GRADE) == 32 and all(len(l) == 32 for l in GRADE), [len(l) for l in GRADE]
    (base / "grades").mkdir(parents=True, exist_ok=True)
    (base / f"grades/{ID}.txt").write_text("\n".join(GRADE) + "\n", encoding="utf-8")
    g = Image.open(base / GUIA).convert("RGBA")
    listas = {c: [] for c in ORDEM}
    listas["guia"] = [f"{x},{y},{''.join(f'{v:02x}' for v in g.getpixel((x, y)))}" for y in range(32) for x in range(32)
                      if g.getpixel((x, y))[3]]
    for y, l in enumerate(GRADE):
        for x, ch in enumerate(l):
            if ch != ".":
                listas[camada(x, y, ch)].append(f"{x},{y},{PALETA[ch]}")
    d = base / f"listas/{ID}"
    d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    (d / "ordem.txt").write_text(",".join(ORDEM) + "\n", encoding="utf-8")
    print(ID, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]))
