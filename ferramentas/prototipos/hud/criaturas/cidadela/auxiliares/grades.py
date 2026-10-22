"""A Abominação e o Cavaleiro Sombrio (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta e o 48 do Bestiário
são o 16 ×2 e ×3. Desenhados à mão, uma letra por pixel; silhueta e volumes primeiro.
  A Abominação ("Carne costurada pela corrupção. Ninguém sabe o que ela foi antes."; corrompida e gigante; o Golpe
  Esmagador, o Veneno e o Regenerar): a carne pálida e a roxa de hematoma, unidas por costuras.
      A, a boca costurada: de frente, a cabeça disforme, metade roxa e inchada com o olho fechado, metade pálida com um
          olho pequeno, a costura subindo pela testa, a boca fechada a pontos, os ombros pesados;
      B, o brutamontes curvado: de três quartos, a corcunda costurada com o hematoma subindo à direita, a cabeça pequena
          e baixa à esquerda com a mandíbula torta, o punho enorme na frente (o golpe esmagador).
  O Cavaleiro Sombrio ("Guerreiros que juraram lealdade ao Vazio e não puderam morrer depois."; morto-vivo e blindado; o
  Golpe Esmagador e o Toque Drenante; também o Último Guarda antes do antagonista, "um cavaleiro de armadura negra"): o
  aço escuro com as bordas claras, o elmo fechado sem rosto, a capa vinho rasgada.
      A, o elmo fechado: de frente, a viseira em T (um ponto violeta do Vazio dentro dela), as ombreiras largas, a capa
          entre elas;
      B, a espada e a crista: o elmo com a crista de crina vinho caindo para trás, a espada de ponta para baixo à frente,
          com a guarda e o punho, as ombreiras, a capa.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "abominacao": {
        "p": "c49a8a", "P": "9a6a62", "x": "5e3a3a",  # a carne pálida (luz, meio, sombra)
        "b": "7a5a88", "B": "4a3058",  # o hematoma roxo da corrupção
        "k": "1e1214", "t": "d8c8a8",  # a costura e a linha dela; os vãos escuros
        "m": "3a1a1a", "d": "e8d8c0", "e": "e8e070",  # a boca, os dentes, o olho amarelado
    },
    "cavaleiro": {
        "a": "24242e", "A": "444452", "L": "6e6e80", "W": "aeaec0",  # o aço escuro (do fundo à borda clara)
        "k": "0a080e", "v": "8a5ac8",  # a viseira e o ponto do Vazio dentro dela
        "c": "2a1820", "C": "5e3046",  # a capa e a crista vinho
        "g": "8a7a4a", "r": "5a3a2a",  # o pomo e o punho da espada
    },
}

ABOMINACAO_A = [
    "................",
    "....BBbb.xPPx...",
    "...BbbbbbPppPx..",
    "..BbbbbbbtppppP.",
    "..BbbBBbbkpppPPx",
    "..BbBkkBbtpkePPx",
    "..BbbbbbbkppppPx",
    "..BBbbbbbtppppPx",
    "...BBkkkkkkkkPx.",
    "...BbtbbtPtPPtx.",
    "....BkkkkkkkkPx.",
    ".....BBbbPPPPx..",
    "...xxBBBbPPPxxx.",
    ".xPPPxBBBPPPxPPx",
    "xPppPPxBBBxPPppP",
    "xPPPPPPxxxPPPPPP",
]
ABOMINACAO_B = [
    "................",
    ".........xxPx...",
    ".......xxPpbbx..",
    "......xPppptbbx.",
    ".....xPpppkpbbPx",
    "..xxxPpppptpppPx",
    ".xPPPxppppkppPPx",
    "xPpkepPpppppPPPx",
    "xPpppPPppppPPPx.",
    "xkmmdPPppPPPPx..",
    ".xxxbPPPPPPPx...",
    "..xPPpPPPPPPPx..",
    ".xPppppPxPPPPPx.",
    "xPppppppxPPPPPx.",
    "xPpppppPx.xPPx..",
    ".xxxxxxx........",
]
CAVALEIRO_A = [
    "......aaaa......",
    ".....aALLAa.....",
    "....aALWWLAa....",
    "....aLWLLLLa....",
    "....aLkkvkLa....",
    "....aLLkkLLa....",
    "....aALkkLAa....",
    "....aALkkLAa....",
    ".....aAkkAa.....",
    "..aaAaAAAAaAaa..",
    ".aLLWAaAAaAWLLa.",
    "aLWLLAaLLaALLWLa",
    "aALLAacAAcaALLAa",
    ".aAAacCAACcaAAa.",
    "..aacCcAAcCcaa..",
    "..ccCcCaaCcCcc..",
]
CAVALEIRO_B = [
    ".......cCcc.....",
    "......aAcCccc...",
    ".....aALLAcCcc..",
    "....aALWLLAacCc.",
    "....aLkkkkLAacc.",
    ".g..aLLkLLLAa.c.",
    ".r..aALkLLAa....",
    ".r...aAkLAa.....",
    ".r...aaAAa......",
    "LLL.aAAaAAaaa...",
    ".W.aLWLAaALLLa..",
    ".WaLWLLAaALLWLa.",
    ".WaLLLAcAAaLLLa.",
    ".WaAAAcCcAaAAa..",
    ".WcccCcCcccCcc..",
    ".W.ccCcCcCcc....",
]


def _camada_abominacao(x, y, ch):
    if ch == "e":
        return "olhos"
    if ch in "ktmd":
        return "costura"
    return "hematoma" if ch in "bB" else "carne"


def _camada_cavaleiro_b(x, y, ch):  # a espada da B fica nas colunas 0 a 2 (o pomo, o punho, a guarda e a lâmina)
    return "espada" if x <= 2 and ch in "grLW" else _camada_cavaleiro(x, y, ch)


def _camada_cavaleiro(x, y, ch):
    if ch in "kv":
        return "viseira"
    return "capa" if ch in "cC" else "armadura"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "abominacao-a": (ABOMINACAO_A, "abominacao", ["carne", "hematoma", "costura", "olhos"], _camada_abominacao),
    "abominacao-b": (ABOMINACAO_B, "abominacao", ["carne", "hematoma", "costura", "olhos"], _camada_abominacao),
    "cavaleiro-a": (CAVALEIRO_A, "cavaleiro", ["capa", "armadura", "viseira"], _camada_cavaleiro),
    "cavaleiro-b": (CAVALEIRO_B, "cavaleiro", ["capa", "armadura", "viseira", "espada"], _camada_cavaleiro_b),
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
