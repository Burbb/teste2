"""O martelo aprovado (1.93.0, a grade de 32 em rpg/web/static/desenhos.js) no 40 e no 48, pela mesma construção (20/10/2026).

O desenho de 32 é todo alinhado às duas diagonais: o cabo corre na diagonal (x + y constante por faixa) e a cabeça
atravessa no alto, perpendicular a ele. Nas coordenadas p = x + y (através do cabo, ao longo da cabeça) e q = x - y (ao
longo do cabo), cada parte é um retângulo e cada material, uma faixa; as medidas abaixo foram lidas pixel a pixel na
grade de 32, e a regra refaz o 32 idêntico ao aprovado (conferido aqui). No 40 e no 48, as mesmas medidas vezes 1,25 e 1,5,
pelo centro de cada pixel, com o contorno de 1 px pelos lados (como no 32): as beiras saem em degraus de 45 graus
limpos, sem os degraus repetidos de uma ampliação. A paleta é a do desenho (CORES_MARTELO), sem cor nova.

A regra dá o rascunho; as grades finais (grades/martelo-40.txt e -48.txt) foram ajustadas à mão: no 40, o cabo com 4 px
(MMmn: com 3 ficava fino para a cabeça) e a ponta de baixo da cabeça; no 40 e no 48, a empunhadura (a volta clara, as
lisas, a volta da beira, como no 32) e o pomo (a beira de latão, a bola, o fim arredondado um pixel para dentro).

    python medidas.py <pasta do martelo>              # confere o 32; das grades, grava listas/ e previa/
    python medidas.py <pasta do martelo> --rascunho   # refaz as grades pela regra (apaga os ajustes à mão)
"""
import pathlib
import re
import sys

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[6]
JS = (RAIZ / "rpg/web/static/desenhos.js").read_text(encoding="utf-8")
CORES = dict(re.findall(r'"?([#A-Za-z])"?: "#([0-9a-f]{6})"', JS[JS.index("const CORES_MARTELO"):].split("\n")[0]))
APROVADO = re.findall(r'"([.#A-Za-z]{32})"', JS[JS.index("const MARTELO = ["):JS.index("// A Pena de Fênix")])
assert len(APROVADO) == 32 and len(CORES) == 13

# as partes, nas coordenadas da grade de 32 (p e q inteiros, inclusive), e o material de cada pixel
def material(p, q):
    """O material do ponto (p, q) da grade de 32 (contínuo: as faixas valem até meio pixel além das bordas)."""
    dentro = lambda v, a, b: a - 0.5 <= v <= b + 0.5
    # a cabeça de ferro: ao longo dela p de 25 a 37, através q de 13 (a beira de trás) a 22 (a beira de bater)
    if dentro(p, 25, 37) and dentro(q, 13, 22):
        if q <= 14.5: return "D"                       # a beira de trás, escura, em todo o comprimento
        if q >= 20.5: return "W" if p <= 34.5 else "S"  # a beira de bater: clara no alto, o tom do topo na ponta de baixo
        if p <= 28.5: return "S"                        # o topo da cabeça, aceso
        if p <= 33.5: return "s"                        # o meio
        return "d"                                      # a ponta de baixo, na sombra
    # o colar de latão em volta do alto do cabo
    if dentro(p, 29, 33) and dentro(q, 9, 12):
        return "Y" if p <= 30.5 else "y"
    # o cabo de madeira (a luz, o meio, a sombra), a empunhadura de couro e o pomo de latão
    if dentro(p, 30, 32) and q <= 8.5:                  # o cabo acaba no colar
        lado = "M" if p <= 30.5 else "m" if p <= 31.5 else "n"
        if q >= -16.5 + (1 if lado == "m" else 0) and q <= 8.5: return lado    # a madeira desce até a empunhadura
        if q >= -23.5:                                                          # a empunhadura: as voltas claras
            volta = p <= 31.5 and (q >= -18.5 or q <= -21.5)
            return "L" if volta else "l"
        if q >= -27.5:
            return "Y" if p <= 31.5 and q >= -26.5 else "y"
    return None


def grade(N):
    k = N / 32
    m = [[None] * N for _ in range(N)]
    for Y in range(N):
        for X in range(N):
            # o centro do pixel de N, na grade de 32 (p e q dos centros: x + y + 1 e x - y)
            p = (X + Y + 1) / k - 1
            q = (X - Y) / k
            m[Y][X] = material(p, q)
    cheio = lambda x, y: 0 <= x < N and 0 <= y < N and m[y][x] is not None
    linhas = []
    for Y in range(N):
        l = ""
        for X in range(N):
            if m[Y][X]: l += m[Y][X]
            elif cheio(X - 1, Y) or cheio(X + 1, Y) or cheio(X, Y - 1) or cheio(X, Y + 1): l += "#"
            else: l += "."
        linhas.append(l)
    return linhas


# as camadas no Aseprite (cada pixel na sua parte)
def camada(ch, x, y, N):
    if ch == "#": return "contorno"
    if ch in "WSsdD": return "cabeca"
    if ch in "Mmn": return "cabo"
    if ch in "Ll": return "empunhadura"
    return "colar" if y < N / 2 else "pomo"


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g32 = grade(32)
    dif = [(x, y) for y in range(32) for x in range(32) if g32[y][x] != APROVADO[y][x]]
    print("o 32 pela regra = o aprovado:", not dif, dif[:10])
    if dif: sys.exit(1)
    # o 32 e o 64 do jogo (a grade aprovada, o 64 a 2×), em imagem só para as pranchas: não mudam
    (base / "previa").mkdir(exist_ok=True)
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    for y, l in enumerate(APROVADO):
        for x, ch in enumerate(l):
            if ch != ".": im.putpixel((x, y), tuple(int(CORES[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    im.save(base / "previa" / "martelo-32-jogo.png"); im.resize((64, 64), Image.NEAREST).save(base / "previa" / "martelo-64-jogo.png")
    for N in (40, 48):
        txt = base / "grades" / f"martelo-{N}.txt"
        if "--rascunho" in sys.argv or not txt.exists():
            # o rascunho pela regra; depois ele é ajustado à mão no .txt (o cabo do 40 com 4 px, a empunhadura e o pomo
            # refeitos pelo ritmo do 32), e o .txt passa a ser a fonte: sem --rascunho, ele é lido, não sobrescrito
            txt.parent.mkdir(exist_ok=True)
            txt.write_text("\n".join(grade(N)) + "\n", encoding="utf-8")
        g = txt.read_text(encoding="utf-8").split("\n")[:N]
        assert len(g) == N and all(len(l) == N for l in g), N
        listas = {}
        for y, l in enumerate(g):
            for x, ch in enumerate(l):
                if ch != ".": listas.setdefault(camada(ch, x, y, N), []).append(f"{x},{y},{CORES[ch]}")
        d = base / "listas" / str(N); d.mkdir(parents=True, exist_ok=True)
        for nome, v in listas.items():
            (d / f"{nome}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        for y, l in enumerate(g):
            for x, ch in enumerate(l):
                if ch != ".": im.putpixel((x, y), tuple(int(CORES[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
        (base / "previa").mkdir(exist_ok=True); im.save(base / "previa" / f"martelo-{N}.png")
        print(N, {k: len(v) for k, v in listas.items()})
        print("\n".join(g))
