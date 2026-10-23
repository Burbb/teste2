"""A Árvore Anciã e o Golem Primordial, os guardiões (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta da
luta é o 16 ×2 (os guardiões só aparecem na carta: não entram no Bestiário nem nos contratos). Desenhados à mão, uma
letra por pixel; a presença de chefe pela composição e pelos volumes, não por detalhe miúdo.
  A Árvore Anciã (`ent_anciao`: "Uma árvore milenar abre olhos de seiva âmbar e fala com voz de terremoto."; planta e
  blindada; o Golpe Esmagador, o Regenerar, o Agarrão e a Varredura): a linguagem e o material da Árvore Desperta T1.
      AA1, o rosto-rei: de frente e de perto, o tronco na largura toda, a copa de galhos grossos subindo como uma coroa,
          as sobrancelhas pesadas na largura do rosto, os olhos de seiva âmbar fundos e afastados, o nariz, a boca
          longa fechada e a barba de raízes caindo em mechas;
      AA2, a árvore imensa: a árvore inteira, a copa larga de galhos secos ocupando o alto, o tronco estreitando e
          abrindo de novo, o rosto mais baixo no tronco (a escala vem do rosto pequeno diante da árvore), as raízes.
  O Golem Primordial (`golem_primordial`: "O que você pensava ser uma parede se levanta: um golem do tamanho de uma
  casa."; construto e blindado; o Golpe Esmagador, a Investida e a Varredura): o peso e a pedra bruta do G2.
      GP1, a parede que se levanta: a cabeça grande de pedra no meio de uma parede de pedras, a laje por cima, três
          pedras de cada lado e o bloco do peito embaixo, com o vão escuro em volta da cabeça;
      GP2, o ídolo: a cabeça grande esculpida num bloco, a laje mais larga que ela por cima (como um dólmen), a testa,
          as órbitas fundas, o nariz e o talho da boca, sobre o corpo de rochedos do G2.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "anciaa": {  # a casca da T1, mais funda; a seiva âmbar dos olhos (do texto do jogo)
        "o": "1a120c", "s": "36281e", "m": "54443a", "l": "7a6656", "h": "9e8a74", "k": "100a06", "e": "b88830",
    },
    "primordial": {  # a pedra do G2, mais escura e mais velha
        "o": "161412", "s": "34302a", "m": "545048", "l": "787268", "h": "9c968a", "k": "0c0a08", "g": "5a6a3a",
    },
}

ANCIAA_AA1 = [
    ".o...o....o...o.",
    ".mo..ms..sm..om.",
    "..ms.mls.lm.sm..",
    "..smmllhhllmms..",
    ".osmllhhhhllmso.",
    "osmhhhhllhhhhmso",
    "ossskeksskeksso.",
    "osmlsmllllmsmlso",
    "osmllmlhhlmllmso",
    "osmllmlhhlmllmso",
    "osmllssmmsslmmso",
    "osmlkkkkkkkklmso",
    "osmllmllllmllmso",
    "osmlsmlsmlsmlsso",
    "osml.mls.ls.ml.o",
    "osm..ml..ls..mso",
]
ANCIAA_AA2 = [
    ".o..o...o...o...",
    "om.om..om..mo.o.",
    ".ms.ms.ms.sm.sm.",
    "..msmlsmlsmlsm..",
    "...smllmllmlms..",
    "....smllmllms...",
    ".....slhhlms....",
    "....oslhhlmso...",
    "...osmhhhhmmso..",
    "...oskekkeksso..",
    "...osmllhlmmso..",
    "..osmlkkkkmmmso.",
    "..osmllmllmmmso.",
    ".osmllmlllmmmsso",
    "osmllmlmllmmmsso",
    "osml.smlsmls.mso",
]
PRIMORDIAL_GP1 = [
    "ohhlohhhhlmmohlm",
    "olmlollllmmsolms",
    "olmkkkkkkkkkklms",
    "olmkohhhhlloklms",
    "olmkolllllmoklmm",
    "kkkkohhhlhhokkkk",
    "ohlkoskklkkokhlm",
    "olmkolllhmmoklms",
    "olmkolkkkkmoklms",
    "olmkolllmmmoklms",
    "osmkoolmmmookmms",
    "kkkkkooooookkkkk",
    "ohlllmllmmmlhllm",
    "ollmllmmmmmmlmms",
    "olmmmmmmmmmsmmss",
    "osmsmmmsssssssso",
]
PRIMORDIAL_GP2 = [
    "..oooooooooooo..",
    "..ohhhhhhhllmo..",
    "..osssssssssso..",
    "...olllllmmmo...",
    "...ohhhlhhhmo...",
    "...oskklskkso...",
    "...ollllhmmmo...",
    "...olkkkkkkmo...",
    "..oolllmmmmmoo..",
    ".ohhooossssoohgo",
    "ohllllooooollmmo",
    "olllllmmmmmlmmso",
    "ollllmmlmmmmmmso",
    "oolllmmmmmmmmsso",
    "ohhhomllmmmmssso",
    "ohlllommmmmssso.",
]


def _camada_anciaa(x, y, ch):
    return "rosto" if ch in "ke" else "casca"


def _camada_primordial(x, y, ch):
    if ch == "g":
        return "musgo"
    return "juntas" if ch == "k" else "pedra"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "anciaa-aa1": (ANCIAA_AA1, "anciaa", ["casca", "rosto"], _camada_anciaa),
    "anciaa-aa2": (ANCIAA_AA2, "anciaa", ["casca", "rosto"], _camada_anciaa),
    "primordial-gp1": (PRIMORDIAL_GP1, "primordial", ["pedra", "juntas"], _camada_primordial),
    "primordial-gp2": (PRIMORDIAL_GP2, "primordial", ["pedra", "musgo", "juntas"], _camada_primordial),
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
