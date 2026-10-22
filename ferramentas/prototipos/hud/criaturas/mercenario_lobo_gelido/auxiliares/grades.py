"""O Mercenário e o Lobo Gélido (22/10/2026, pedido do Jean; propostas, nada no jogo). Dois retratos por criatura, na
linguagem dos aprovados (a cabeça com um pedaço do ombro ou do pescoço enchendo o quadro, sem contorno, a paleta
contida, os traços do rosto de 1 ou 2 px, a luz da esquerda), 16×16; o 32 da carta e o 48 do Bestiário são o 16 ×2 e
×3 (DERIVADOS), como os integrados.
  - O Mercenário (`mercenario`: "Armadura boa, moral flexível. Lutam pelo maior lance."; humano, blindado; Preparar
    Golpe, Golpe Sujo, Grito de Guerra; na planície, nos duelos de ponte, nos guardas de um nobre, na escolta do
    cultista e no Theodore dos Cães de Ferro): um soldado de ofício, de metal e de pano grosso, sem o capuz e a faca do
    Bandido, sem o manto do Cultista e com a cabeça coberta (o Morel, mercenário da comitiva, anda de cabeça
    descoberta).
      MA, o chapéu de ferro: o elmo de aba larga dos soldados a soldo, os olhos na sombra da aba, a barba por fazer, o
          gibão acolchoado no pescoço e a malha nos ombros;
      MB, a coifa de malha: o rosto fechado na malha, a barba cheia, o ombro de placa e a correia da bainha.
  - O Lobo Gélido (`lobo_gelido`: "O frio da montanha mora dentro deles. Odeiam fogo mais que qualquer coisa."; fera;
    Mordida Gélida e Uivo; resiste ao gelo, sofre mais com o fogo; nas montanhas): a construção do Lobo aprovado (a
    cabeça de frente, as orelhas, o focinho claro, o começo do pescoço), com o rosto sempre à vista.
      LA, o lobo da geada: a pelagem clara azulada, os olhos de gelo, a juba de pontas brancas que alarga a cara;
      LB, o lobo da nevasca: a pelagem escura de ardósia, as orelhas para trás e o rosnado com as presas, a geada na
          testa e os olhos acesos.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

# as cores de cada desenho (a mesma letra pode ter cor diferente em outro desenho)
PALETAS = {
    "mercenario": {
        # o aço (a luz, o meio, a sombra, a sombra funda) e o brilho
        "W": "d6d9dd", "S": "a9adb4", "s": "7f838b", "t": "585c63", "T": "35383d",
        # a pele (luz, sombra, sombra funda), os olhos e a boca
        "p": "c09070", "P": "9a6c52", "x": "6e4a38", "i": "1a120c", "m": "5a3328",
        # a barba e o cabelo
        "z": "2e2620", "Z": "4a3c30",
        # o gibão acolchoado (ocre) e o couro
        "o": "9c7c46", "O": "735a30", "q": "4a391d", "l": "6a4a30", "L": "3e2a1a",
    },
    "lobo_a": {
        "a": "263445", "c": "46607a", "b": "8aa3b8", "d": "c3d5e3", "h": "eef4f7", "e": "34445a",
        "f": "8fe3f5", "g": "0d1217", "w": "e2eef6",
    },
    "lobo_b": {
        "a": "1b2430", "c": "34465a", "b": "5d7790", "d": "93adc2", "h": "d6e4ee", "e": "2a3646",
        "f": "6ff0ff", "g": "0b0f14", "t": "f1eee4", "m": "3a1418", "r": "7a3038",
    },
}

MA = [
    "................",
    "......tSSs......",
    ".....tSWSsT.....",
    "....tSWSssst....",
    "...tSSSsssstT...",
    ".TsSSSssssssttT.",
    "..TTTTTTTTTTTT..",
    "...zxPPPPPPxz...",
    "...zpippppiPz...",
    "...zpppxpppPz...",
    "...zZpPmmPPZz...",
    "....zZZZZZZz....",
    "..sSOooooOOqst..",
    ".sStqooooOOqtSs.",
    "sStSqOooOOOqStst",
    "StsTqOOOOOOqTsts",
]
MB = [
    "................",
    ".....tsSSst.....",
    "....tSsSsstT....",
    "...tSsSsStstT...",
    "...SsSssststT...",
    "..tSsxPPPPxstT..",
    "..sSzzzPPzzztT..",
    "..tSxipppPixstT.",
    "..sSpppxpppPtsT.",
    "..tSzppppppztsT.",
    "..sSzZmmmmZztsT.",
    "..tszzZZZZzztsT.",
    ".WSstzzzzzztsTT.",
    "WSSsTtzzzztTsllT",
    "SSsstTTttTTlLssT",
    "SsssstTTTTlLsssT",
]
LA = [
    "...w........w...",
    "..wbc......cbw..",
    "..deba....aeba..",
    "..debcaccacebc..",
    "..ddbbbbbbbbbc..",
    ".cddbwbbbbwbbaa.",
    ".cddfgbbbbgfbca.",
    "dcdddbbhhbbbbcac",
    "wdddbhhhhhhbbcaw",
    "wwddbhhhhhhbccww",
    ".wwdbhhgghhbcww.",
    "..wwdbhhhhbcww..",
    "...wwcbbbbccw...",
    "....cdbbbccaac..",
    "....cdbbbcccaac.",
    "...cdbbbccccaaac",
]
LB = [
    "................",
    ".ab..........ba.",
    ".deb........bea.",
    "..debcaccacebc..",
    "..ddbbhbbhbbbc..",
    ".cddhbabbabhbaa.",
    ".cddfgbbbbgfbca.",
    ".cdddbbhhbbbbca.",
    ".cddbhchhchbbca.",
    "..cdhhhgghhhca..",
    "..cdrmtmmtmrca..",
    "..cdbtmmmmtbca..",
    "...cdbhhhhbca...",
    "....ccbhbbcca...",
    "....cdhbbccaac..",
    "...cdbbhccccaaac",
]

CAMADAS = {
    "mercenario-ma": (MA, "mercenario", ["roupa", "rosto", "elmo"],
                      lambda x, y, ch: "elmo" if y <= 6 else "roupa" if y >= 12 else "rosto"),
    "mercenario-mb": (MB, "mercenario", ["roupa", "coifa", "rosto"],
                      lambda x, y, ch: "rosto" if ch in "pPxizZm" and 5 <= y <= 12 else "roupa" if y >= 12 else "coifa"),
    "lobo-gelido-la": (LA, "lobo_a", ["pelagem", "focinho", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch in "fgw" else "focinho" if ch == "h" else "pelagem"),
    "lobo-gelido-lb": (LB, "lobo_b", ["pelagem", "focinho", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch in "fgtmr" else "focinho" if ch == "h" else "pelagem"),
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
