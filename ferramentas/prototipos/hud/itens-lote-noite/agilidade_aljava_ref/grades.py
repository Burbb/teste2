"""As grades desenhadas à mão (rodada das referências): cada pixel é uma letra da paleta da peça, e a letra diz também
a camada. Este script não desenha nada: lê a grade, acrescenta o contorno de 1 px por fora (só pelos lados) e grava
as listas de cada camada para o pintar.lua montar a fonte no Aseprite, mais uma prévia para conferir a fonte.

    python grades.py <peça> <lado>      # grava listas/<peça>-<lado>/ e previa/<peça>-<lado>.png

A fonte final é o .aseprite em fontes/<peça>/ (pintado no editor pelo MCP a partir dessas listas, e refinado lá); os
PNGs da proposta saem dele por exportar_aseprite.py --fontes=fontes.
"""

import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
CONTORNO = "08080A"

# couro da bota: 1 (sombra) a 7 (brilho); a dobra usa as mesmas cores com letras próprias (A a G), para ir à camada dela
_COURO = ["2E140A", "4E2210", "6E3317", "8F4620", "B0602C", "CF8040", "EAAA62"]
_COURO_ALJAVA = ["2A100A", "4A1E12", "6E2E1A", "8E4024", "AE5A32", "C87A46", "E29C62"]
PECAS = {
    "attr-agilidade": {
        "camadas": ["rastros", "sola", "bota", "dobra", "tira", "fivela", "contorno"],
        "sem_contorno": "rtu",   # os riscos de velocidade ficam soltos, sem contorno
        "letras": {
            **{str(i + 1): (c, "bota") for i, c in enumerate(_COURO)},
            **{"ABCDEFG"[i]: (c, "dobra") for i, c in enumerate(_COURO)}, "I": ("1A0904", "dobra"),
            "J": (_COURO[0], "tira"), "K": (_COURO[1], "tira"), "L": (_COURO[2], "tira"), "M": (_COURO[3], "tira"),
            "q": ("21160F", "sola"), "w": ("382A20", "sola"), "e": ("57453A", "sola"),
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
}


def ler(peca, lado):
    """A grade com o contorno: {(x, y): (cor, camada)}."""
    P = PECAS[peca]
    linhas = [l for l in (AQUI / "grades" / f"{peca}-{lado}.txt").read_text(encoding="utf-8").splitlines() if l]
    assert len(linhas) == lado and all(len(l) == lado for l in linhas), "a grade não é quadrada do lado"
    px = {}
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c != ".":
                px[(x, y)] = P["letras"][c]
    forma = {(x, y) for (x, y), (_, cam) in px.items() if linhas[y][x] not in P["sem_contorno"]}
    for y in range(lado):
        for x in range(lado):
            if (x, y) not in px and any((x + dx, y + dy) in forma for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[(x, y)] = (CONTORNO, "contorno")
    return px


def main():
    peca, lado = sys.argv[1], int(sys.argv[2])
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
