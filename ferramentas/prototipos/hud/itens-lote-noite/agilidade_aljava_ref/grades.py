"""As grades desenhadas à mão (rodada das referências): cada pixel é uma letra da paleta da peça, e a letra diz também
a camada. Este script não desenha nada: lê a grade, acrescenta o contorno de 1 px por fora (só pelos lados) e grava
as listas de cada camada para o pintar.lua montar a fonte no Aseprite, mais uma prévia para conferir a fonte.

    python grades.py <peça> <lado> [--pasta=<dir>]   # grava listas/<peça>-<lado>/ e previa/<peça>-<lado>.png

--pasta: a pasta da rodada (com grades/), quando não é esta (o Poder: ../poder_r2).

Quando as cores se repetem entre partes (o couro da mochila no corpo, na aba e nos bolsos), a camada vem de um segundo
mapa, grades/<peça>-<lado>-camadas.txt (um caractere por pixel, pela "legenda" da peça), e a letra da grade fica só
com a cor.

A fonte final é o .aseprite em fontes/<peça>/ (pintado no editor pelo MCP a partir dessas listas, e refinado lá); os
PNGs da proposta saem dele por exportar_aseprite.py --fontes=fontes.
"""

import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
for _a in sys.argv:
    if _a.startswith("--pasta="):
        AQUI = pathlib.Path(_a.split("=", 1)[1]).resolve()
CONTORNO = "08080A"

# couro da bota: 1 (sombra) a 7 (brilho); a dobra usa as mesmas cores com letras próprias (A a G), para ir à camada dela
_COURO = ["2E140A", "4E2210", "6E3317", "8F4620", "B0602C", "CF8040", "EAAA62"]
# o Poder (rodada 2): a rampa violeta com deslocamento de matiz, do índigo da beira ao miolo creme; a chama (1 a 4), o
# miolo (5 a 8) e a faísca solta em camadas próprias
_VIOLETA = ["1E0B4A", "3A1488", "5E22C8", "8A3AE6", "B85CF0", "E08CF4", "F8C8F0", "FFF4DC"]
# a doca (rodada 2, doca_r2/): a mochila no couro do conjunto aprovado, o latão, o pano do cobertor; o mapa de papel
_COURO_DOCA = ["1E130C", "2E1E13", "45301E", "604229", "7C5634", "986C42", "B48752", "CFA36C"]
_LATAO_DOCA = {"x": "5A3C12", "y": "9C6E22", "z": "DDB45C"}
_PANO = {"g": "262B1A", "h": "3E4628", "i": "5C663C", "j": "7E8A56", "k": "A0AC74"}
_PAPEL = {"A": "3E2E1A", "B": "6E5634", "C": "9C8052", "D": "C4A874", "E": "E2CC98", "F": "F4E6C0"}
# Ataque e Defesa (rodada 2, ataque_defesa_r2/): o aço (1 a 7), o latão (a a d) e o couro do cabo
_ACO = ["1C2230", "3A4458", "6A768C", "8C98AC", "B8C2D0", "DDE4EC", "FFFFFF"]
_LATAO = {"a": "5A3A10", "b": "9A6A1C", "c": "D8A438", "d": "F6DC80"}
_COURO_ALJAVA = ["2A100A", "4A1E12", "6E2E1A", "8E4024", "AE5A32", "C87A46", "E29C62"]
PECAS = {
    "attr-agilidade": {
        "camadas": ["rastros", "sola", "bota", "dobra", "tira", "fivela", "contorno"],
        "sem_contorno": "rtu",   # os riscos de velocidade ficam soltos, sem contorno
        "letras": {
            **{str(i + 1): (c, "bota") for i, c in enumerate(_COURO)},
            **{"ABCDEFG"[i]: (c, "dobra") for i, c in enumerate(_COURO)}, "I": ("1A0904", "dobra"),
            "J": (_COURO[0], "tira"), "K": (_COURO[1], "tira"), "L": (_COURO[2], "tira"), "M": (_COURO[3], "tira"),
            "q": ("2E2016", "sola"), "w": ("4A3628", "sola"), "e": ("6E5442", "sola"),   # marrons profundos, não quase preto
            "x": ("6A4A14", "fivela"), "y": ("B48A30", "fivela"), "z": ("F0D070", "fivela"),
            "r": ("7A5228", "rastros"), "t": ("C08A48", "rastros"), "u": ("F2C47A", "rastros"),
        },
    },
    # a aljava: o couro avermelhado da referência (1 a 7), a boca (bordas acesas e o fundo), as cintas escuras com a beira
    # acesa, o latão, a alça, as hastes claras e as penas (claras e vermelhas)
    "aljava": {
        "camadas": ["alca", "couro", "cintas", "latao", "boca", "hastes", "penas", "contorno"],
        "sem_contorno": "hjl",   # as hastes ficam sem contorno: com ele, o fundo entre as flechas vira uma mancha escura
        "letras": {
            **{str(i + 1): (c, "couro") for i, c in enumerate(_COURO_ALJAVA)},
            "P": (_COURO_ALJAVA[2], "boca"), "Q": (_COURO_ALJAVA[3], "boca"), "U": (_COURO_ALJAVA[4], "boca"),
            "V": (_COURO_ALJAVA[5], "boca"), "W": (_COURO_ALJAVA[6], "boca"), "i": ("1A0805", "boca"),
            "D": (_COURO_ALJAVA[1], "alca"), "E": (_COURO_ALJAVA[2], "alca"), "F": (_COURO_ALJAVA[3], "alca"),
            "A": ("2A1A16", "cintas"), "B": ("3E2A22", "cintas"), "C": ("5A4034", "cintas"),
            "x": ("6A4A14", "latao"), "y": ("B48A30", "latao"), "z": ("F0D070", "latao"),
            "h": ("7A5530", "hastes"), "j": ("B08A58", "hastes"), "l": ("DCBC86", "hastes"),
            "m": ("8A8070", "penas"), "n": ("CFC6B0", "penas"), "o": ("F4EEDC", "penas"),
            "R": ("5A1410", "penas"), "S": ("9A2A1C", "penas"), "T": ("D04A2C", "penas"),
        },
    },
    "attr-ataque": {
        "camadas": ["lamina", "guarda", "cabo", "pomo", "contorno"],
        "sem_contorno": "",
        "letras": {
            **{str(i + 1): (c, "lamina") for i, c in enumerate(_ACO)},
            **{k: (c, "guarda") for k, c in _LATAO.items()}, **{k.upper(): (c, "pomo") for k, c in _LATAO.items()},
            "k": ("3A2010", "cabo"), "l": ("6A4024", "cabo"), "m": ("9A6438", "cabo"),
        },
    },
    "attr-defesa": {
        "camadas": ["face", "aro", "lado", "bossa", "contorno"],
        "sem_contorno": "",
        "letras": {
            **{str(i + 1): (c, "face") for i, c in enumerate(_ACO)},
            **{k: (c, "aro") for k, c in _LATAO.items()}, **{k.upper(): (c, "bossa") for k, c in _LATAO.items()},
            "Y": (_LATAO["a"], "lado"), "X": (_LATAO["b"], "lado"), "Z": ("3A240C", "lado"),
        },
    },
    "atalho-inventario": {
        "camadas": ["rolo", "bolsos", "corpo", "aba", "cinta", "fivela", "contorno"],
        "sem_contorno": "",
        "legenda": {"r": "rolo", "b": "bolsos", "c": "corpo", "a": "aba", "t": "cinta", "f": "fivela"},
        "letras": {**{str(i + 1): (c, "") for i, c in enumerate(_COURO_DOCA)},
                   **{k: (c, "") for k, c in _LATAO_DOCA.items()}, **{k: (c, "") for k, c in _PANO.items()}},
    },
    "atalho-mapa": {
        "camadas": ["espessura", "papel", "vincos", "terreno", "percurso", "destino", "contorno"],
        "sem_contorno": "",
        "legenda": {"s": "espessura", "p": "papel", "v": "vincos", "e": "terreno", "q": "percurso", "x": "destino"},
        "letras": {**{k: (c, "") for k, c in _PAPEL.items()},
                   "v": ("7E8A52", ""), "w": ("A4AC72", ""), "l": ("6E8C9C", ""), "m": ("9CB4BC", ""),
                   "r": ("6A1C12", ""), "s": ("B23A24", ""), "t": ("E0603A", "")},
    },
    "attr-poder": {
        "camadas": ["chama", "miolo", "faisca", "contorno"],
        "sem_contorno": "",
        "letras": {
            **{str(i + 1): (c, "chama" if i < 4 else "miolo") for i, c in enumerate(_VIOLETA)},
            "F": (_VIOLETA[4], "faisca"), "G": (_VIOLETA[5], "faisca"),
        },
    },
}


def ler(peca, lado):
    """A grade com o contorno: {(x, y): (cor, camada)}."""
    P = PECAS[peca]
    linhas = [l for l in (AQUI / "grades" / f"{peca}-{lado}.txt").read_text(encoding="utf-8").splitlines() if l]
    assert len(linhas) == lado and all(len(l) == lado for l in linhas), "a grade não é quadrada do lado"
    mapa = AQUI / "grades" / f"{peca}-{lado}-camadas.txt"
    cam = [l for l in mapa.read_text(encoding="utf-8").splitlines() if l] if mapa.exists() else None
    px = {}
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c != ".":
                cor, camada = P["letras"][c]
                px[(x, y)] = (cor, P["legenda"][cam[y][x]] if cam else camada)
    forma = {(x, y) for (x, y), (_, cam) in px.items() if linhas[y][x] not in P["sem_contorno"]}
    for y in range(lado):
        for x in range(lado):
            if (x, y) not in px and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[(x, y)] = (CONTORNO, "contorno")
    return px


def main():
    peca, lado = [a for a in sys.argv[1:] if not a.startswith("--")][:2]
    lado = int(lado)
    px = ler(peca, lado)
    pasta = AQUI / "listas" / f"{peca}-{lado}"
    pasta.mkdir(parents=True, exist_ok=True)
    camadas = PECAS[peca]["camadas"]
    for cam in camadas:
        texto = ";".join(f"{x},{y},{cor}" for (x, y), (cor, c) in sorted(px.items(), key=lambda i: (i[0][1], i[0][0])) if c == cam)
        (pasta / f"{cam}.lua").write_text(f'return "{texto}"\n', encoding="utf-8")
    (pasta / "ordem.txt").write_text(",".join(camadas) + "\n", encoding="utf-8")
    img = Image.new("RGBA", (lado, lado))
    for (x, y), (cor, _) in px.items():
        img.putpixel((x, y), tuple(int(cor[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    (AQUI / "previa").mkdir(exist_ok=True)
    img.save(AQUI / "previa" / f"{peca}-{lado}.png")
    print(peca, lado, {c: sum(1 for v in px.values() if v[1] == c) for c in camadas})


if __name__ == "__main__":
    main()
