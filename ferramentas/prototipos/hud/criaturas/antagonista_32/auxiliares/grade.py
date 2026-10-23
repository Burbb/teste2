"""O antagonista do mundo gerado em 32×32 nativos (pedido do Jean, 23/10/2026; protótipo, nada no jogo, sem adaptação para
16), pela direção A de `identidades/LEIA-ME.md`: o humano que a Fenda está apagando. Um rosto humano de traços ambíguos
(sem barba, sem marca de gênero, o cabelo escuro partido ao meio até a gola), magro e cansado, com as sobrancelhas
tristes e um olho humano olhando de frente; uma fissura irregular desce em diagonal da têmpora, abre um buraco no lugar
do outro olho, passa ao lado do nariz e corta o canto da boca até a mandíbula, com o Vazio (o preto e o violeta da Cria
do Vazio) por trás; as bordas lascadas, rachaduras finas e três lascas soltando-se da cabeça. Sem diadema, coroa, mitra,
corda, moscas ou véu: serve aos oito títulos e às cinco origens. A gola alta escura, de quem já teve posto. Sem guia.
Uma letra por pixel; o contorno faz parte do desenho.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "0c0a0e",
          "q": "1c1822", "w": "2e2836", "W": "463e50",  # o cabelo
          "K": "4a3c3c", "s": "7c6c66", "m": "a6968c", "l": "cbbdb0", "L": "e4d9cc",  # a pele
          "j": "d6d0c6", "i": "68727e", "z": "141218", "p": "8c6a68",  # o olho e a boca
          "c": "16121c", "C": "262030", "D": "3a3248",  # a gola
          "v": "060309", "V": "180c28", "u": "3a1e5c", "U": "9a64d8",  # o Vazio e a borda dele
          "f": "f2e8dc"}  # as lascas claras da borda
GRADE_32 = [
    "................................",
    "................................",
    "...........oooooooooo...........",
    ".........ooqqqqqqqqqqoo.........",
    "........oqqqqwqwqwqqqqqo..l.....",
    ".......oqqqqwqWwwqwqqKqqo.......",
    "......oqqwWqmllllllmquwqfo......",
    "......oqwqqmlllLLlllmvKqqo......",
    "......oqwqmllllLLlllKvuwqo......",
    "......oWwmllllsllslfUvKKqm......",
    "......oqqmlsKKlllKUvvVuqqo......",
    "......oqqmllssslfUvVvvuwqo......",
    "......oqwmljizjlKUvvVvKqqo......",
    "......oqwmlsmmsKlfUvvumqqo......",
    "......oqqmllllsLmlUvKsmwqo......",
    "......oWqmmllllLsUvuKmmqqo......",
    "......oqwsmllllLsUKllmsqqo......",
    "......oqqsmlllsKfUvllmswqo......",
    "......oqqsmllllUvuKllmsqqo......",
    "......oqwKsmlpUvKppmlsKqqo......",
    "......oqqqKslUvuKlllsKqwqo......",
    "......oqqqKsKvKllllmsKqqqo......",
    "......oqqqqKumllllmsKqqqqo......",
    "......oqqqqqKssmmssKqqqqqo......",
    "......oqqqqqqsmllmsqqqqqqo......",
    "....ocCDqqqsmlmssmlmsqqqDCco....",
    "..ocCCDDqqqKsmllllmsKqqqDDCCco..",
    ".ocCCDDCqqqcKsmllmsKcqqqCDDCCco.",
    "ocCCDDCCcqqcCKsmmsKCcqqcCCDDCCco",
    "ocCCDCCCccccCcKssKcCccccCCCDCCco",
    "ocCCDCCCcccccCcKKcCcccccCCCDCCco",
    "ocCCDCCCccccccCccCccccccCCCDCCco",
]
# cada desenho: a grade e o lado (só o 32 nesta rodada)
DESENHOS = {"antagonista-n32": (GRADE_32, 32)}
# as camadas, de baixo para cima
ORDEM = ["gola", "cabelo", "rosto", "vazio", "lascas", "contorno"]
# as lascas soltas, fora da cabeça (x, y)
SOLTAS = {(26, 4), (24, 6), (25, 9)}


def camada(x, y, ch, ident):
    if (x, y) in SOLTAS or ch == "f":
        return "lascas"
    if ch == "o":
        return "contorno"
    if ch in "vVuU":
        return "vazio"
    if ch in "qwW":
        return "cabelo"
    if ch in "cCD":
        return "gola"
    return "rosto"


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
