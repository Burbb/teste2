"""O teste do Dragão de Gelo em 32×32 nativos (pedido do Jean, 23/10/2026; protótipo, nada no jogo). Uma proposta só,
desenhada à mão na grade de 32 (não o 16 ampliado): a guia (a referência `Cabeça ancestral de dragão de gelo-2.png`
reduzida a 32 por média) mediu as posições; os planos e o acabamento são à mão. Uma letra por pixel; o contorno faz parte
do desenho.
Depois da aprovação da direção (23/10/2026), dois desenhos a mais, também só no protótipo: o N32R, uma cópia do N32 com
um refino leve (os planos da bochecha e do pescoço agrupados, os brilhos concentrados no alto da testa, o olho um pouco
mais estreito sob a testa); e o N16, um teste do Jean, o mesmo dragão redesenhado à mão em 16 a partir do N32R (o N32R
reduzido a 2:1 serviu de mapa). O N32 fica como estava.
    python grade.py ..      # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
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
GRADE_R = [
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
    ".....oLhhhhhhhlllmSSmsLmmSooo...",
    "....olhhhhhhllLLLsSmLLmmsmllho..",
    "....ollllllLLLmsSsSmLLmmsmmllho.",
    "....ollLLLLLmsSSmLLLsLLmmsmmmlho",
    "....oSmLsSSSSSeSslllsLLmmsSllllh",
    "...oomhhLssSeeESlhhhlsLmmmmmmlls",
    ".ooLhhwhhlmsSsLslhhllsmmmmsmmsoo",
    "oLhhhhlllLLLmmmmslllLLsmmmSsooo.",
    "olllSSLllllLLLmsSLLLLmSmssSsmlho",
    "ommmmSlhhhlLskkkkSLLmmmSsSSllllh",
    "oLmmmmmskkkkkLLLmSmLLmmsSssmmlls",
    "omskkkkkddLdLmmsSmmLLmmsssSmmsoo",
    "okkLlllLdDmmmmmsSmmmLmmsssSsooo.",
    "oLLLLLmmDmmmmssSSmmmmmmsssSsmlho",
    "omLLLmmmmmmssSSSsmmmmmmsmSSllllh",
    ".osmmLLmmssSooSSsmLLLmmssssmmlls",
    "..osmmLmsSoo..oSssmmmmssssSmmsoo",
    "...osmmsSo.....oSmLllLmsssSsooo.",
    "....oSSoo.......oSmmLllmssSsmlho",
    ".....oo.........oSssmLLmmSSllllh",
]
GRADE_16 = [
    ".........olo..ol",
    "........ohso.ohs",
    ".......ohlsoohls",
    "....ooohlmsohlso",
    "...oLlhlmsShmso.",
    "..oLhhhhlLLLmso.",
    ".olhhhllLSLmmslo",
    ".ollLLSSSLLmsmlh",
    "oLhhLSeEllsLmsml",
    "LhhllLmsllLsmsoo",
    "lSlllLskSLmSsslh",
    "mkkkdkLLSmLmsmms",
    "LlLmDmmsSmmmsSoo",
    "LLmmsSoSsmmmsSll",
    "osmSoooSmLmssSoo",
    ".ooo...oSmLmsSlh",
]
ID = "dragao-n32"
# cada desenho: a grade, o lado e a guia (a referência reduzida por média ao lado do desenho, oculta na fonte)
DESENHOS = {"dragao-n32": (GRADE, 32, "guias/dragao-guia-32.png"), "dragao-n32r": (GRADE_R, 32, "guias/dragao-guia-32.png"),
            "dragao-n16": (GRADE_16, 16, "guias/dragao-guia-16.png")}
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "cabeca", "chifres", "crista", "boca", "dentes", "olho", "contorno"]


def camada(x, y, ch, n=32):
    if ch == "o":
        return "contorno"
    if ch in "eE":
        return "olho"
    if ch in "dD":
        return "dentes"
    if ch == "k":
        return "boca"
    if y <= (9 if n == 32 else 4):
        return "chifres"
    if (x >= 26 and y >= 13) if n == 32 else (x >= 13 and y >= 7):
        return "crista"
    return "cabeca"


def imagem(ident=ID):
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
