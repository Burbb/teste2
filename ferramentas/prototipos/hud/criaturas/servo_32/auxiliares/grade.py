"""O servo esquelético do Necromante (o "Esqueleto (Invocado)" do Erguer Servo) construído em 32×32 nativos e adaptado à
mão para 16 (pedido do Jean, 23/10/2026; protótipo, nada no jogo), sem elmo, capuz ou armadura, com desenho próprio (não
o Esqueleto inimigo, que tem elmo, com os olhos recoloridos): o crânio descoberto, com o alto saindo do quadro, as órbitas
fundas de tamanhos diferentes e inclinadas para o nariz (o canto de dentro coberto pela testa: sem cara de óculos), a
cavidade do nariz como buraco, a mordida fechada em grupos irregulares de dentes (sem xadrez nem sorriso de foto), a
mandíbula ligada ao crânio, as vértebras sustentando a cabeça e as clavículas com o começo das costelas. O sinal da
necromancia é contido: um violeta fundo em cada órbita (no 16, o violeta escuro: o claro virava lâmpada). A referência
`Caveira esquelética sombria em pixel art.png` dá a anatomia e o material do osso; a guia (ela reduzida por média) fica
oculta nas fontes. Uma letra por pixel; o contorno faz parte do desenho.
    python grade.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETA = {"o": "15120f", "k": "0c0a08", "W": "e2d8b8", "B": "cbbf9c", "b": "a39776", "d": "776d54",
          "D": "4d4636", "v": "b48ae8", "V": "5e3a8a"}
GRADE_32 = [
    "........oWWWWBBBBBbbbbbo........",
    ".......oWWWBBBBBBBBbbbbbbo......",
    "......oWWBBBBBBBBBBbbbbbbo......",
    ".....oBWBBBBBBBBBBbbbbbbddo.....",
    ".....oBBBBBBBBBBBbbbbbbbddo.....",
    ".....obBBBBBBBBBbbbbbbbbddo.....",
    ".....obbWWBBBbbbWWBbbbbbddo.....",
    ".....obdDDDDdbBdDDDDDdbbddo.....",
    ".....obDkkkDDbBDDkkkkDbbddo.....",
    ".....odDkkVkDbbDkkVkkDbdddo.....",
    ".....odDkkvkDbbDkkvkkDbdDDo.....",
    ".....oddDkkDdbbdDkkkDdbdDo......",
    "......odbDDdbBbbdDDdbBbdDo......",
    "......odBBbbdDdbbbBBBbdDDo......",
    "......oDbBbdDkDdbBbbbdDkDo......",
    ".......odbbdkkkdbbbddDkdo.......",
    "........oDWBDWBBDBWDBDdo........",
    "........oDkDkkDkkkDkkDbo........",
    ".........oBbDBBDbBDBDDbo........",
    ".........odbbbbbbbbddDdo........",
    "..........oDdbBBbbddDDo.........",
    "...........ooDdddDDDoo..........",
    "............oodBBdoo............",
    ".............oDddDDo............",
    "............odbBBbdo............",
    ".............oDddDDo............",
    ".oobBBo.....oodbBbdoo....oBBboo.",
    "obBBBbbBBo..oDdBBdDooBBbbBBBbo..",
    ".....oobbddDooDbBbDoooDddbboo...",
    "...ob....oobddoBBodddboo...bo...",
    "....odbbo...oDdBBdDo..obbdo.....",
    "..obdo...obbdoDbBbDodbbo..odbo..",
]
GRADE_16 = [
    "...oWWBBBBbbo...",
    "..oWBBBBBbbbdo..",
    "..obBBBBBbbbdo..",
    "..obWBbbWBbbdo..",
    "..obDkDbDkkDdo..",
    "..odkVDbDVkDdo..",
    "..odDDbBdDDbDo..",
    "...oBbDkbBbDo...",
    "...odbkkbbdko...",
    "....oWDWBDBdo...",
    "....okkDkkDo....",
    "....obBDBbdo....",
    ".....odbbDo.....",
    "......oBdo......",
    "oBBbboodDoobBBbo",
    "..obdodBbdodbo..",
]
# cada desenho: a grade, o lado e a guia
DESENHOS = {"servo-n32": (GRADE_32, 32, "guias/servo-guia-32.png"),
            "servo-n16": (GRADE_16, 16, "guias/servo-guia-16.png")}
# as camadas, de baixo para cima (a guia por baixo de tudo)
ORDEM = ["guia", "ossos", "sombras", "feitico", "contorno"]


def camada(x, y, ch, ident):
    if ch == "o":
        return "contorno"
    if ch in "vV":
        return "feitico"
    if ch in "kD":  # o fundo das órbitas, do nariz e da mordida, e as sombras fundas do osso
        return "sombras"
    return "ossos"


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
