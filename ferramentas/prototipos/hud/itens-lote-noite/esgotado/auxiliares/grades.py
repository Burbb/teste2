"""O ícone do Esgotado do mercado (22/10/2026, pedido do Jean; proposta, nada no jogo). O suprimento sem estoque no dia
mostra o motivo "Esgotado" no cartão (o mercador reabastece amanhã cedo, na dica), hoje com o cadeado do jogo (o
antigo desenho do Firme, também do Salvar, do bloqueio de vida, do Armadilheiro e dos outros motivos do mercado). Duas
propostas de papel próprio, 16×16 como os estados aprovados (contorno de 1 px, luz de cima e da esquerda), desenhadas
pixel a pixel nas grades abaixo:
  - A, o caixote vazio: a caixa de tábuas aberta, o fundo escuro à vista, a travessa na frente;
  - B, o cesto vazio: o cesto de palha com a alça, a boca aberta e o fundo escuro.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

CORES = {
    "k": "08080a",  # o contorno dos ícones aprovados
    # a madeira do caixote: o fio da luz, o meio, o meio escuro, a sombra; os montantes (o da luz e o da sombra)
    "L": "dcb27a", "M": "b5854c", "m": "936839", "S": "6b4726", "P": "c99a5e", "Q": "7a522c",
    # o vazio de dentro: a parede do fundo e o fundo
    "I": "4f341c", "i": "1d130c", "w": "2f1f12", "W": "7d5730",
    # a palha do cesto, da luz à sombra
    "A": "e2c27e", "B": "c09a55", "C": "94723a", "D": "684f26",
    # a parede de dentro do cesto
    "J": "5c4422",
}

# A, o caixote vazio: visto um pouco de cima, a boca funda (a parede do fundo, as paredes dos lados em cunha, a da
# esquerda na sombra e a da direita na luz, o fundo escuro), a frente de duas tábuas com os montantes e a travessa
CAIXOTE = [
    "................",
    ".kkkkkkkkkkkkkk.",
    ".kLLLLLLLLLLLLk.",
    ".kQIIIIIIIIIImk.",
    ".kQwIIIIIIIIWmk.",
    ".kQwwiiiiiiWWmk.",
    ".kQwwiiiiiiWWmk.",
    ".kLLLLLLLLLLLLk.",
    ".kPMMMMMMMMLLQk.",
    ".kPMMMMMMLLMMQk.",
    ".kPSSSSLLSSSSQk.",
    ".kPMMLLMMMMMMQk.",
    ".kPLLMMMMMMMMQk.",
    ".kPmmmmmmmmmmQk.",
    ".kkkkkkkkkkkkkk.",
    "................",
]
# B, o cesto vazio: a alça em arco, a boca aberta com a parede de dentro e o fundo escuro, a borda e o trançado
CESTO = [
    "................",
    ".....kkkkkk.....",
    "....kAABBBCk....",
    "...kAkkkkkkCk...",
    "..kAk......kCk..",
    ".kAkkkkkkkkkkCk.",
    "kAAJJJJJJJJJJCCk",
    "kAAiiiiiiiiiiCCk",
    "kAAiiiiiiiiiiCDk",
    "kAAAAABBBBBCCCDk",
    ".kAABBAABBCCDDk.",
    ".kBAABBAACCDDCk.",
    "..kAABBAABCCDk..",
    "..kBAABBCCDDCk..",
    "...kkkkkkkkkk...",
    "................",
]

CAMADAS = {
    "esgotado-caixote": (CAIXOTE, ["vazio", "madeira", "contorno"],
                         lambda x, y, ch: "contorno" if ch == "k" else "vazio" if ch in "IiwW" else "madeira"),
    "esgotado-cesto": (CESTO, ["vazio", "palha", "contorno"],
                       lambda x, y, ch: "contorno" if ch == "k" else "vazio" if ch in "Ji" else "palha"),
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
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{CORES[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + "\n", encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
