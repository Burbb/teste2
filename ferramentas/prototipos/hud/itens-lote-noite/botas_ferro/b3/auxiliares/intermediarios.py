"""O 40 e o 48 da B3 (20/10/2026), pelo mesmo caminho do 32 aprovado (reducao.py: a guia e o rascunho na paleta do
conjunto, com a caixa do desenho em 38 e 45 px, a proporção do 32) e os ajustes à mão de cada grade (AJUSTES abaixo).
O contorno é por dentro, como o do desenho da referência: a silhueta é o que a guia cobre em metade ou mais, e o pixel
dela que encosta no lado de fora vira contorno (no 32, a beira escura virou contorno e o anel de fora saiu: o mesmo
resultado; nos tamanhos maiores, aquela regra deixava sobras). O interior escuro fora das bocas vira o couro escuro (as
solas, os calcanhares).
    python intermediarios.py <pasta da B3> 40|48     # grava grades/B3-<N>.txt
"""
import pathlib
import sys

from PIL import Image

# as bocas (as caixas onde o interior escuro fica), por tamanho: (x0, y0, x1, y1), inclusive
BOCAS = {40: [(28, 0, 37, 4), (13, 4, 24, 9)], 48: [(32, 0, 45, 5), (15, 6, 29, 11)]}
# os ajustes à mão de cada tamanho: {N: [(y, x0, trecho, porquê)]}
BOCA_T = "a boca da bota de trás: a beira do fundo em aço, o vão escuro, o lábio aceso (como no 32)"
BOCA_F = "a boca da bota da frente: a beira do fundo em aço, o vão escuro, o lábio aceso (como no 32)"
FIVELA = "a fivela em ferro claro na ponta direita da tira (como no 32; o ouro da referência na paleta do conjunto)"
AJUSTES = {
    40: [(2, 29, "3444433", BOCA_T), (3, 26, "54biiiiiib3", BOCA_T), (4, 26, "6653biiib33", BOCA_T),
         (6, 16, "344443", BOCA_F), (7, 13, "43biiiiib3", BOCA_F), (8, 12, "75biiiiib4", BOCA_F),
         (9, 12, "6777766666543", BOCA_F),
         (8, 23, "...", "o vão entre os canos (o fundo, como na referência), sem o escuro que a redução deixava"),
         (22, 22, "7", FIVELA), (23, 22, "6", FIVELA), (16, 35, "7", FIVELA), (17, 35, "6", FIVELA)],
    48: [(2, 35, "34444433", BOCA_T), (3, 31, "433biiiiiib34", BOCA_T), (4, 30, "6543biiiiib443", BOCA_T),
         (5, 30, "55776655555443", BOCA_T),
         (7, 18, "344444443", BOCA_F), (8, 15, "43biiiiiiiib3#", BOCA_F), (9, 14, "75biiiiiiiiiib4#", BOCA_F),
         (10, 14, "7776655555554433", BOCA_F),
         (26, 26, "7", FIVELA), (27, 26, "6", FIVELA), (19, 41, "7", FIVELA), (20, 41, "6", FIVELA)]}


def base(pasta, N):
    g = [list(l) for l in (pasta / f"grades/rascunho-{N}.txt").read_text(encoding="utf-8").split("\n")[:N]]
    guia = Image.open(pasta / f"previa/guia-{N}.png").convert("RGBA")
    S = {(x, y) for y in range(N) for x in range(N) if guia.getpixel((x, y))[3] >= 128}
    for y in range(N):
        for x in range(N):
            if (x, y) not in S: g[y][x] = "."
            elif any((x + dx, y + dy) not in S for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = "#"
    boca = lambda x, y: any(a <= x <= c and b <= y <= d for a, b, c, d in BOCAS[N])
    for y in range(N):
        for x in range(N):
            if g[y][x] == "i" and not boca(x, y): g[y][x] = "b"
    return g


if __name__ == "__main__":
    pasta = pathlib.Path(sys.argv[1]); N = int(sys.argv[2])
    g = base(pasta, N)
    for y, x0, trecho, _ in AJUSTES[N]:
        for k, ch in enumerate(trecho):
            if ch != " ": g[y][x0 + k] = ch
    g = ["".join(l) for l in g]
    (pasta / f"grades/B3-{N}.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    print(f"{len(AJUSTES[N])} ajustes")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(g)))
