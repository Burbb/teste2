"""A terceira rodada (22/10/2026, pedido do Jean; propostas, nada no jogo): o carniçal A2 com a bochecha direita
recolhida, o javali A2 com as presas em arco e o espectro no retrato do manto inflado (a referência nova). 16×16 na
linguagem dos retratos aprovados, vistas a 2× na carta e a 3× no Bestiário. As fontes no Aseprite pelo conector.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

# as paletas da segunda rodada (segunda_rodada/auxiliares/grades.py), sem tons novos
CORES_CARNE_NEVOA = {
    "L": "a89a96",
    "l": "7a6c6c",
    "d": "4e4246",
    "D": "2e262a",
    "Y": "d0c060",
    "R": "8a1e1e",
    "T": "d8d0bc",
    "k": "120c0c",
    "t": "b0a690",
    "C": "aeb6c4",
    "c": "7a8698",
    "s": "4c5468",
    "S": "343a4a",
    "V": "0c0e14",
    "E": "b8eef0",
    "G": "5a2a2e",
}
CORES_JAVALI = {
    "J": "1e1612",
    "j": "3a2a20",
    "b": "5a4232",
    "B": "7a5c44",
    "n": "9a7462",
    "N": "c0988a",
    "o": "2a1814",
    "T": "e6dcc4",
    "E": "b0381e",
    "K": "1e1a18",
    "r": "443a34",
    "R": "6a5e56",
    "g": "928678",
    "p": "c4908a",
    "P": "8a5a58",
    "Y": "d8c070",
    "e": "d0302a",
    "t": "b4aa90",
    "Q": "8e8670",
}

# Carniçal A3: o A2 (a boca e os dentes aprovados) com a bochecha direita recolhida: a coluna 13 sai nas linhas 8 e 9, e
# a sombra passa à coluna 12; o resto igual
CARN_A3 = [
    "................",
    ".....dlllld.....",
    "....dlLLLlld....",
    "...dlLLLLllld...",
    "...lLdkLLkdld...",
    "...lLkYlLYkdd...",
    "...dLlllllldD...",
    "...dLlGGGGldD...",
    "...dlTtTTtTlD...",
    "...dlTkkkkTlD...",
    "...dlkkkkkkld...",
    "...dltkkkktld...",
    "....dTRTTtGd....",
    "..ddDdlRllDDdd..",
    ".dlLldDllDdlLld.",
    "dlLlldttttdllLld",
]
# Javali A3: o rosto do A com as presas do A2 (o tamanho e a grossura) refeitas em arco: a base grossa sai da boca ao
# lado do focinho, abre para fora, sobe e afina na ponta, que volta para dentro; as presas curtas do A saem
JAV_A3 = [
    "................",
    "..J..........J..",
    "..jJ.J.JJ.J.Jj..",
    "..jbJjJjjJjJbj..",
    ".jbbBbbjjbbBbbj.",
    ".TbEbBbbbbBbEbT.",
    "TjbbBBbbbbBBbbjT",
    "tTjbBBnnnnBBbjTt",
    "tTjbBnNNNNnBbjTt",
    ".tTbnNoNNoNnbTt.",
    "..tTnNNNNNNnTt..",
    "...QTnnnnnnTQ...",
    "...jjbbbbbbjj...",
    "..jbbjbbbbjbbj..",
    ".jbbBbJJJJbBbbj.",
    "JjjjjJJJJJJjjjjJ",
]
# Espectro M, o manto inflado (a referência "Espectro do Manto Inflado.png"; a guia oculta, guias/espectro-guia-16.png):
# o capuz pequeno no alto com a cavidade escura e o olho único em fenda, a sombra na base do capuz, o pano que incha nos
# ombros e desce até a borda de baixo (o corpo continua fora do quadro), a luz à esquerda, os rasgos escuros
ESP_M = [
    "......sc........",
    ".....scCc.......",
    "....scCCCc......",
    "....cCSVVSc.....",
    "....cSVEVVSs....",
    "....cSVEVVSs....",
    "....scSVVSss....",
    "..sssccSSccsss..",
    ".scCCcsssscCcss.",
    "scCCCCcssccccsss",
    "cCCCcccVcccccsSs",
    "cCCccVcccccsVcsS",
    "cCcccVcsccccVssS",
    "cCccccsccccccssS",
    "cCcVcccccscccssS",
    "cccVcccccscccssS",
]

# Espectro AP (22/10/2026, pedido do Jean; o M não foi escolhido): o espectro-a dos quatro pares, igual nas linhas 0 a
# 10 (a cabeça, o capuz, a cavidade, o olho, a paleta, a posição), com o pano continuando até a borda de baixo: os vãos
# das linhas 11 a 15 fechados, abrindo um pouco, com as dobras em sombra (o corpo grande fica para a arte de cenário)
ESP_AP = [
    "................",
    "......cccc......",
    ".....cCCCcs.....",
    "....cCcSSccs....",
    "...cCcSVVScss...",
    "...cCSVEVVScs...",
    "...cCSVVEVScs...",
    "...cCSVVVVScss..",
    "...cCcSVVScsss..",
    "..ccCccSScccss..",
    "..cCccccccccss..",
    ".cCcccccccccss..",
    ".cCccsccccccsss.",
    "cCCccsccccscsss.",
    "cCcccsccccscssss",
    "cCcccsccccscssss",
]


CAMADAS = {
    "carnical-a3": (CARN_A3, ["corpo", "rosto", "boca"],
                    lambda x, y, ch: "boca" if ch in "RTktG" and 7 <= y <= 13 else "rosto" if y <= 11 else "corpo",
                    CORES_CARNE_NEVOA),
    "javali-a3": (JAV_A3, ["corpo", "focinho", "presas", "olhos"],
                  lambda x, y, ch: "olhos" if ch == "E" else "presas" if ch in "TtQ" else "focinho" if ch in "nNo" else "corpo",
                  CORES_JAVALI),
    "espectro-m": (ESP_M, ["manto", "rasgos", "cavidade", "olho"],
                   lambda x, y, ch: "olho" if ch == "E" else "cavidade" if ch in "VS" and y <= 6 else "rasgos" if ch == "V" else "manto",
                   CORES_CARNE_NEVOA),
    "espectro-ap": (ESP_AP, ["nevoa", "vazio"], lambda x, y, ch: "vazio" if ch in "VE" else "nevoa", CORES_CARNE_NEVOA),
}


def imagem(ident):
    grade, _, _, cores = CAMADAS[ident]
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(cores[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, ordem, camada, cores = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text(chr(10).join(grade) + chr(10), encoding="utf-8")
        listas = {k: [] for k in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{cores[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text('return "' + ";".join(v) + '"' + chr(10), encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + chr(10), encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
