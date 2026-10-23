"""A Árvore Desperta e o golem de pedra (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta e o 48 do
Bestiário são o 16 ×2 e ×3. Desenhados à mão, uma letra por pixel; silhueta, volumes e expressão primeiro.
  A Árvore Desperta (`ent_jovem`: "Árvores que acordaram com raiva. Madeira verde queima mal — mas queima."; planta e
  blindada; o Golpe Esmagador e o Regenerar): a casca, os nós e os galhos formando o rosto.
      A1, os galhos nus: de frente, o tronco é a cabeça, os galhos secos subindo em forquilhas com poucas folhas na
          ponta, as sobrancelhas de casca sobre os olhos de nó inclinados (bravos), a fenda da boca com as lascas e as
          raízes se abrindo embaixo;
      A2, a copa pesada: a copa verde redonda caindo sobre os olhos como uma testa, o toco de galho quebrado como
          nariz, a boca de nó com as lascas, o tronco largo.
  O golem de pedra (`golem`: "Pedra e runas. Lento, mas cada golpe é uma avalanche. A magia racha a pedra."; construto
  e blindado; o Golpe Esmagador): peso e construção mineral, blocos e juntas legíveis.
      G1, a cantaria: blocos cortados, a cabeça um bloco só com a laje da testa e as órbitas quadradas, a junta escura
          do pescoço, as ombreiras e o peito em blocos brutos, a rachadura descendo pelo peito;
      G2, o rochedo: pedras brutas e arredondadas, a cabeça pequena e baixa entre dois ombros enormes, a testa saliente
          sobre as órbitas, o musgo num ombro, o punho de pedra embaixo à esquerda.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "arvore": {
        "o": "1a120c", "s": "3a2a1c", "m": "5e4630", "l": "86684a", "h": "a88a62",  # a casca (contorno à luz)
        "k": "0e0a08",  # os ocos: os olhos de nó, a boca
        "G": "2e4a22", "g": "4e7032", "y": "76984a",  # as folhas
    },
    "golem": {
        "o": "1a1816", "s": "3c3832", "m": "5e5950", "l": "847e72", "h": "a8a294",  # a pedra (contorno à luz)
        "k": "0e0c0a",  # as juntas, as órbitas, a rachadura
        "g": "6a7a44",  # o musgo
    },
}

ARVORE_A1 = [
    ".g......g....g..",
    ".go....og...ogy.",
    "..mo..oms..omg..",
    "..oms.oms.omso..",
    "...ommmlmmmmo...",
    "..olllhllmmmso..",
    "..olhhlmlhhmso..",
    "..olkklmlkkmso..",
    "..ollklmlkmsso..",
    "..ollmlhmmmsso..",
    "..olkkkkkkksso..",
    "..olklkkklksso..",
    "..ollkkkkkmsso..",
    ".oolllmlmmmssoo.",
    "ollllmlmmmmsssso",
    "olmlomlmsomssoso",
]
ARVORE_A2 = [
    ".....GggyG......",
    "...GggyygggG....",
    "..GgggyggggyG...",
    ".GgggggggggggGG.",
    ".GgGgggGggggGgG.",
    "..GGoGGGGGoGGG..",
    "...osssssssso...",
    "...oskkmmkkso...",
    ".ohhmlkmlkmso...",
    "..oolmlhmmmso...",
    "...olkkkkkmso...",
    "...olklkklmso...",
    "..ollmkkkmmsso..",
    ".olllmlmmmmssso.",
    "olllmmlmmmmmssso",
    "olmmmmmmmmmmssso",
]
GOLEM_G1 = [
    "................",
    "....oooooooo....",
    "....ohhhlllmo...",
    "....ollllllmo...",
    "....ossssssso...",
    "....okkllmkko...",
    "....olllkmmmo...",
    "....olmkkkmso...",
    ".oooookkkkkoooo.",
    "ohhhlohhllmohllo",
    "ollllolkmmmollmo",
    "olllmollkmmolmso",
    "ollmmollkmmommso",
    "ommmsollmksomsso",
    "osmsoolmmmsoosso",
    "oo.ooolmmmsoo.oo",
]
GOLEM_G2 = [
    "................",
    "......oooo......",
    ".....ohhllo.....",
    "....ohhhhlmo....",
    "..oooskmksoooo..",
    ".ohhlolmmmolhgo.",
    "ohllloommmoollgo",
    "ohllllooooollmmo",
    "olllllmmmmmlmmso",
    "ollllmmlmmmmmmso",
    "oolllmmmmmmmmsso",
    "ohhhomllmmmmssso",
    "ohlllommmmmssso.",
    "ollllommmmmsso..",
    "ollmmoommmsso...",
    ".oooo.oommoo....",
]


def _camada_arvore(x, y, ch):
    if ch in "Ggy":
        return "folhas"
    return "rosto" if ch == "k" else "casca"


def _camada_golem(x, y, ch):
    if ch == "g":
        return "musgo"
    return "juntas" if ch == "k" else "pedra"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "arvore-a1": (ARVORE_A1, "arvore", ["casca", "folhas", "rosto"], _camada_arvore),
    "arvore-a2": (ARVORE_A2, "arvore", ["casca", "folhas", "rosto"], _camada_arvore),
    "golem-g1": (GOLEM_G1, "golem", ["pedra", "juntas"], _camada_golem),
    "golem-g2": (GOLEM_G2, "golem", ["pedra", "musgo", "juntas"], _camada_golem),
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
