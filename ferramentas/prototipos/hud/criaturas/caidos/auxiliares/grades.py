"""O Caído e o Xamã Caído (22/10/2026, pedido do Jean; propostas, nada no jogo). Dois retratos por criatura, 16×16,
na linguagem dos aprovados; o 32 da carta e o 48 do Bestiário são o 16 ×2 e ×3.
No jogo, os caídos são diabretes (o traço `demonio`, "cria do Inferno"): "Diabretes covardes que atacam em bando,
rindo. Mate o xamã primeiro, ou eles voltam." O xamã é o "pequeno feiticeiro dos caídos. Cospe fogo e ergue os
irmãos mortos do chão." A identidade comum: a pele vermelha, os chifres curtos, as orelhas pontudas para fora, os
olhos amarelos e o riso. O xamã se distingue pela construção (o que ele veste) e pelo fogo, não pela cor do olho.
  - Caído:
      CA, o que ri: de frente, a cabeça redonda com os chifres curtos, as orelhas abertas, os olhos apertados de riso e
          a boca aberta cheia de dentes, os ombros curvados;
      CB, o que se esgueira: em três quartos para a esquerda, mais escuro, os chifres longos para trás, o olhar de
          lado e o sorriso torto com uma presa.
  - Xamã Caído (o par de cada caído: a mesma cabeça):
      XA, o do crânio: o CA com o crânio de uma fera por cima da cabeça (os chifres dele, as órbitas, o focinho), o
          fogo na boca aberta e a capa de couro com contas de osso;
      XB, o do capuz: o CB num capuz de couro com o chifre furando, a gola de contas de osso e a chama alta na mão erguida.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

_COMUM = {
    "h": "e0d0a8", "H": "9a8660",  # os chifres
    "y": "f2d24a", "k": "1a0a08",  # os olhos e o escuro
    "t": "efe6cc", "m": "2e0c0a",  # os dentes e a boca
    "f": "f0a030", "F": "d85020", "Y": "fff0a0",  # o fogo
    "w": "e8dcc0", "W": "c4b490", "n": "3a2a20",  # o osso do crânio
    "c": "5a4430", "C": "36281c", "b": "e0d0a8",  # o couro e as contas
}
PALETAS = {
    "a": {**_COMUM, "a": "d86a4a", "r": "b8442e", "R": "862a20", "D": "521814"},  # o vermelho do CA e do XA
    "b": {**_COMUM, "a": "b0563e", "r": "8a3a2a", "R": "5e2219", "D": "3a1410"},  # o mais escuro do CB e do XB
}

CA = [
    "................",
    "...h........h...",
    "...hH......Hh...",
    "....hRrrrrRh....",
    "...arrrrrrrrR...",
    "aa.arrrrrrrrR.RR",
    ".aaakkrrrrkkRRR.",
    "..aryyrrrryyrR..",
    "..arrrrRrrrrRR..",
    "..akttttttttkR..",
    "...rkmmmmmmkRR..",
    "...rrkttttkRR...",
    "....RrrrrrRR....",
    "..DRRRrrrRRRD...",
    ".DRRrrRRRrrRRD..",
    "DRRrrRRDRRrrRRDD",
]
CB = [
    "..........hhH...",
    "........hhH.....",
    "......hhHrr.....",
    ".....hHrrrrR....",
    "...arrrrrrrRR...",
    "..arkkrrkkrRRRRR",
    ".aryyrrryrRRRRR.",
    "aarrrrRrrrRRRDD.",
    ".rrrRRrrrrRRDD..",
    "..kttkmmkRRRD...",
    "...kmmmtkRRD....",
    "....RRRRRRD.....",
    "....DRrrRRDD....",
    "..DRRrrrRRRRD...",
    ".DRrrrRRRRrrRD..",
    "DRRrrRRRRRrrRRDD",
]
XA = [
    "..h..........h..",
    "..hh.wwwwww.hh..",
    "...hwWWWWWWwh...",
    "...wWkWWWWkWw...",
    "..awWWWnnWWWwR..",
    "aa.awwwwwwwwR.RR",
    ".aaakkrrrrkkRRR.",
    "..aryyrrrryyrR..",
    "..arrrrRrrrrRR..",
    "..akFfYYffFkR...",
    "...rkFfYYfFkRR..",
    "...rrkFffFkRR...",
    "....RrrrrrRR....",
    "..CcRRrrrRRcC...",
    ".CccbcRRRcbccC..",
    "CccCcbcccbcCccCC",
]
XB = [
    "..........hhH...",
    "......CCcchH....",
    ".....CccccCH....",
    "....CccccccCC...",
    "...CcarrrrrrCC..",
    "..CarkkrrkkrRCC.",
    ".CaryyrrryrRRCC.",
    "aarrrrRrrrRRRCC.",
    ".rrrRRrrrrRRCC..",
    "Y.kttkmmkRRRCc..",
    "fY.kmmmtkRRCcc..",
    "FfY.RRRRRRCccC..",
    "FffYCbRRbRCcccC.",
    ".FfFCcbbCccccCC.",
    "aaFaCccccccCccCC",
    "aaaacCcccCcccCCC",
]


def _camada_caido(x, y, ch):
    return "olhos" if ch in "yk" and y < 9 else "boca" if ch in "tmk" else "chifres" if ch in "hH" else "pele"


def _camada_xama(x, y, ch):
    if ch in "fFY":
        return "fogo"
    if ch in "wWn":
        return "cranio"
    if ch in "cCb":
        return "couro"
    return "olhos" if ch in "yk" and y < 9 else "boca" if ch in "tmk" else "chifres" if ch in "hH" else "pele"


CAMADAS = {
    "caido-ca": (CA, "a", ["pele", "chifres", "olhos", "boca"], _camada_caido),
    "caido-cb": (CB, "b", ["pele", "chifres", "olhos", "boca"], _camada_caido),
    "xama-caido-xa": (XA, "a", ["pele", "couro", "chifres", "cranio", "olhos", "boca", "fogo"], _camada_xama),
    "xama-caido-xb": (XB, "b", ["pele", "couro", "chifres", "olhos", "boca", "fogo"], _camada_xama),
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
