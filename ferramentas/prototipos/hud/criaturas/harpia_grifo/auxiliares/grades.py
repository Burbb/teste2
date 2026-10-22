"""A Harpia e o Grifo (22/10/2026, pedido do Jean; propostas, nada no jogo). Dois retratos por criatura, 16×16, na
linguagem dos aprovados (a cabeça com um pedaço do ombro enchendo o quadro, sem contorno, a paleta contida, a luz da
esquerda); o 32 da carta e o 48 do Bestiário são o 16 ×2 e ×3.
  - Harpia (`harpia`: "Metade mulher, metade abutre, inteira cruel. Difíceis de acertar com uma espada."; voadora;
    Grito de Terror e Mordida Sangrenta; nas montanhas, nível 2+, em bando de até três):
      HA, a que grita: de frente, o rosto de mulher magro e cinzento, o cabelo em penas desgrenhadas, a boca aberta no
          grito, o pescoço nu e vermelho de abutre dentro da gola de penas, as asas nos ombros;
      HB, a de perfil: virada para a esquerda, o nariz em gancho, o cabelo virando pena, o pescoço nu de abutre, a asa
          erguida atrás dela.
  - Grifo (`grifo`: "Rei dos céus das montanhas. Protege o ninho até a morte."; voador e fera; Investida e Mordida
    Sangrenta; nas montanhas, nível 4+, sozinho; a mãe do ninho do evento):
      GA, a águia-leão: em três quartos para a direita (o contrário do Falcão), a cabeça branca e dourada com os tufos,
          o bico pesado em gancho, o olho feroz e o peito de leão;
      GB, o de asas abertas: de frente, as asas erguidas atrás da cabeça, a cabeça dourada mais estreita, as
          sobrancelhas fechadas, o bico longo descendo até o queixo, o pelo de leão.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "harpia": {
        "h": "2c2228", "H": "4a3a40",  # o cabelo
        "s": "aca69c", "S": "7e7872", "x": "57504c",  # a pele cinzenta (luz, sombra, sombra funda)
        "r": "b0584c", "R": "7a3430",  # o pescoço nu de abutre (luz, sombra)
        "e": "d23a2a", "k": "120e0e", "m": "3a1416", "t": "e8e0cc",  # os olhos, o escuro, a boca, os dentes
        "f": "d8cfbb", "F": "9c8c78", "G": "5e5044", "B": "6e4a32", "W": "8c6a4a",  # as penas e as asas
    },
    "grifo": {
        "W": "ece4cc", "w": "c8bc9c",  # a cabeça branca
        "o": "d0a048", "O": "a0742c", "q": "6a4a20",  # as penas douradas
        "y": "eab232", "Y": "b07a18", "d": "4a3010", "m": "8a2a20",  # o bico, a ponta, a boca
        "e": "e06020", "k": "100c08",  # o olho
        "L": "c08a44", "l": "8e6230", "D": "5e3e1c",  # o pelo de leão
        "B": "5a4028", "b": "84603a",  # as asas
    },
}

HA = [
    "...h..hh..h.....",
    "..hHhhHHhhHh.h..",
    ".hHHHhHHhHHHhHh.",
    ".hHHhsssssshHHh.",
    "hHHsssssssSShHh.",
    "hHhskesssekSxhH.",
    "hHhsssSxssSSxhH.",
    "hHhsSmtttmSxhH..",
    "hHhsSmmmmmSxhH..",
    "hhHxsSSSSSxxhHh.",
    "B.hhFfrrRRfFhh.B",
    "BBhFffFrRFffFhBB",
    "WBBFfFffffFfFBBW",
    "WWBBFfFffFfFBBWW",
    "BWWBGFfFFfFGBWWB",
    "BBWWBGGFFGGBWWBB",
]
HB = [
    "...........B....",
    "....hhh...BWB...",
    "...hHHHh..BWWB..",
    "..hHsssHhBWWWB..",
    "..hsssssHBWBWWB.",
    ".hskesssSHBWBWB.",
    ".xsssSsSSHBWBWWB",
    "xxsmtmSSShBWBWB.",
    ".smmmSSSxhBWBWWB",
    "..sSSSSxxhBWBWB.",
    "...SrRRFFhBWBBB.",
    "...RRFfffFBBWB..",
    "..FfffFffFFBBB..",
    ".FfffFfffFFFBG..",
    "FffFfffFfFFBGG..",
    "fFfffFfFfffFBGG.",
]
GA = [
    "..O.....O.......",
    "..OoO..OoO......",
    "..qOoooooOq.....",
    ".qOowwwwwoOq....",
    ".OowWWWWWwoO....",
    ".OwWWWWkeWwYY...",
    ".OwWWWWWWyyyYY..",
    ".OwwWWWWyyyyYYd.",
    ".qOwwWWWwyyYYdd.",
    "..qOwwwwwYYddd..",
    "..lqOwwwwOq.d...",
    ".LlqOOwwOOql....",
    "LLLlqOOOOqlLL...",
    "LLLLllqqqlLLLl..",
    "LLLLLLlllLLLLLl.",
    "DLLLLLLLLLLLLLlD",
]
GB = [
    "b..............b",
    "Bb............bB",
    "BBb...oOOo...bBB",
    ".BBb.oOooOO.bBB.",
    ".BBboOooooOObBB.",
    "..BOkkoooOkkqB..",
    "..BOoeoYYoeOqB..",
    "..BqOoYyyYoOqB..",
    ".BBqOoYyyYoOqBB.",
    ".BbqOOoYyYOOqbB.",
    "BbBqqOOYyYOqqBbB",
    "BbbBqqOOYdOqqBbB",
    ".BbbBLqqdqqLBbB.",
    "..BBLLLLLLLLBB..",
    ".DLLLlLLLLlLLLD.",
    "DLLLLlLLLLlLLLLD",
]

CAMADAS = {
    "harpia-ha": (HA, "harpia", ["penas", "cabelo", "rosto"],
                  lambda x, y, ch: "rosto" if ch in "sSxekmtrR" and y < 12 else "cabelo" if ch in "hH" else "penas"),
    "harpia-hb": (HB, "harpia", ["penas", "asa", "cabelo", "rosto"],
                  lambda x, y, ch: "rosto" if ch in "sSxekmtrR" and y < 12 else "cabelo" if ch in "hH"
                  else "asa" if ch in "BWG" and x >= 9 else "penas"),
    "grifo-ga": (GA, "grifo", ["pelo", "cabeca", "bico", "olho"],
                 lambda x, y, ch: "olho" if ch in "ek" else "bico" if ch in "yYdm" else "pelo" if ch in "LlD" else "cabeca"),
    "grifo-gb": (GB, "grifo", ["asas", "pelo", "cabeca", "bico", "olho"],
                 lambda x, y, ch: "olho" if ch in "ek" else "bico" if ch in "yYdm" else "pelo" if ch in "LlD"
                 else "asas" if ch in "Bb" else "cabeca"),
}


def cor(ident, ch):
    return PALETAS[CAMADAS[ident][1]][ch]


def imagem(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(CAMADAS[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(cor(ident, ch)[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, _, ordem, camada = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{cor(ident, ch)}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + "\n", encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
