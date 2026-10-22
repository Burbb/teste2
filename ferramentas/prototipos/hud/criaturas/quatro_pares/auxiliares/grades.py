"""Os quatro pares da madrugada de 22/10/2026 (1E.3, pedido do Jean; propostas, nada no jogo): duas direções para cada
criatura, cabeças/bustos de 16×16 na linguagem dos retratos aprovados (sem contorno, a paleta contida, a luz da
esquerda), vistas a 2× na carta (32 px) e a 3× no Bestiário e no mural (48 px). As grades à mão; as fontes no Aseprite
pelo conector (o pintar.lua), em fontes/<id>/<id>-16.aseprite.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

CORES = {}

# Par 1, o pântano: o sapo-touro gigante e a sanguessuga gigante (os dois hoje no "fera", o rosto de lobo)
CORES.update({
    # o sapo: o lodo escuro, o oliva, o oliva claro, a barriga, a barriga na sombra, o olho, a pupila, a boca, o veneno
    "K": "1c1a10", "G": "3d3a1f", "g": "5f5a2e", "h": "85803f", "c": "b8a77a", "C": "8f805a", "Y": "d0a030", "k": "100e0a",
    "M": "2a1612", "O": "c06a2a",
    # a sanguessuga: o escuro, o corpo, o brilho úmido, a faixa avermelhada, o lábio, os dentes, a água
    "S": "1e1a17", "s": "211c16", "t": "3e3628", "w": "6a604a", "r": "7a3a28", "R": "a3433a", "P": "d9b5a0", "A": "1d2e2c",
    "a": "2e4440",
})
# Sapo A, de frente: a cabeçorra larga enchendo a carta, os olhos saltados sob a sobrancelha pesada (a pupila
# horizontal), a boca de ponta a ponta caindo nos cantos, as manchas do veneno, a papada clara
SAPO_A = [
    "................",
    "................",
    "..GGG......GGG..",
    ".GgGGG....GGGgG.",
    ".GYkkG....GkkYG.",
    ".GYYYGGggGGYYYG.",
    "GgGGgghhhhggGGgG",
    "GghgOgghhggOghgG",
    "GgggghhhhhhggggG",
    "KMMMMMMMMMMMMMMK",
    "GMCcccccccccccMG",
    "GgCcCcccccCcCCgG",
    "KGgCccccccccCgGK",
    "KKGGCCccccCCGGKK",
    ".KKGGGGGGGGGGKK.",
    "..KKKKKKKKKKKK..",
]
# Sapo B, de perfil para a esquerda: o papo inchado (o coaxar), o olho alto, a boca comprida, a pata da frente
SAPO_B = [
    "................",
    "................",
    "................",
    "....GGG.........",
    "...GYkYG........",
    "..GgYYgGGGGG....",
    ".GhhgggghhgGG...",
    "GhhgOghhgggOgG..",
    "MMMMMMMghhgggGG.",
    "MCcccCMggghhggG.",
    ".CccccCCgggOggGK",
    ".CCcccCCGggggGGK",
    "..CCCCGgGGgggGK.",
    "....GhgGKGGGGK..",
    "...GhhG.KKKKK...",
    "..KKKK..........",
]
# Sanguessuga A, empinada de frente: a ventosa redonda com o anel de dentes, o corpo gordo em anéis com a faixa, a água
SANG_A = [
    "................",
    "...ssttttts.....",
    "..sRRRRRRRRs....",
    ".sRrPrPrPrPRs...",
    ".sRPkkkkkkPRs...",
    ".sRrkkkkkkrRs...",
    ".sRPkkkkkkPRs...",
    ".sRrPrPrPrPRs...",
    ".stRRRRRRRRts...",
    ".swttrttrttws...",
    ".ssssssssssss...",
    ".stwtrttrtwts...",
    ".ssssssssssss...",
    "..stwrttrwts....",
    "AaAstrttrtsAaAaA",
    "aAaAasssssaAaAaA",
]
# Sanguessuga B, o corpo em curva saindo da água, a cabeça com a boca de dentes para a esquerda
SANG_B = [
    "................",
    "................",
    "..sRRRs.........",
    ".sRPkPRs........",
    ".sRkkkRws.......",
    "..sRPRwtws......",
    "...stwtrtws.....",
    "....stwrtwts....",
    ".....stwrtwts...",
    "......stwrtwts..",
    ".......stwrtws..",
    "......stwrtwts..",
    ".....stwrtwts...",
    "....stwrtwts....",
    "AaAstwrtwtsAaAaA",
    "aAaAasssssaAaAaA",
]

CAMADAS = {
    "sapo-a": (SAPO_A, ["corpo", "barriga", "olhos", "manchas"],
               lambda x, y, ch: "olhos" if ch in "Yk" else "manchas" if ch == "O" else "barriga" if ch in "cCM" else "corpo"),
    "sapo-b": (SAPO_B, ["corpo", "barriga", "olhos", "manchas"],
               lambda x, y, ch: "olhos" if ch in "Yk" else "manchas" if ch == "O" else "barriga" if ch in "cCM" else "corpo"),
    "sanguessuga-a": (SANG_A, ["agua", "corpo", "boca"],
                      lambda x, y, ch: "agua" if ch in "Aa" else "boca" if ch in "RPkr" and y <= 8 else "corpo"),
    "sanguessuga-b": (SANG_B, ["agua", "corpo", "boca"],
                      lambda x, y, ch: "agua" if ch in "Aa" else "boca" if ch in "RPk" and y <= 5 else "corpo"),
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
        (base / f"grades/{ident}.txt").write_text(chr(10).join(grade) + chr(10), encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{CORES[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text('return "' + ";".join(v) + '"' + chr(10), encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + chr(10), encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
