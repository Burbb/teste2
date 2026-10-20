"""O 40 e o 48 da L7 (20/10/2026), a partir do 32 final (o c7639438: a limpeza e os dois retoques), que é a autoridade.
O mesmo princípio da M5 em 40 e 48 (manopla_perneiras/auxiliares/malha_dcss.lua com N):
  - a forma: cada pixel de N vem do pixel do 32 correspondente (o vizinho mais próximo), o quadro inteiro na mesma
    escala (a composição, a pose, as proporções e as margens ficam);
  - o contorno: o de fora com 1 px (a beira da silhueta de N); as linhas de dentro (os vãos dos dedos, a sobreposição, a
    costura, e a sombra sólida do tom 1, como a linha dos nós da direita) ficam com 1 px: o primeiro pixel de N na direção
    da espessura da linha no 32 (a deitada, a primeira fileira; a em pé, a primeira coluna; o canto, qualquer um); o
    pixel a mais toma o material dos vizinhos (o couro ou a malha, sem preto novo);
  - a malha: refeita na grade de N, com o volume do 32 (a média do xadrez em volta) e o xadrez de um tom acima e um abaixo,
    os anéis do mesmo tamanho em pixels, como a cota em 40 e 48;
  - o couro: o tom do pixel do 32.
Depois, os ajustes à mão de cada grade (AJUSTES), cada um com o porquê. Grava grades/L7-<N>.txt.
    python tamanhos.py <pasta da L7> 40|48
(Hoje vale PURO, logo abaixo: a réplica pelo vizinho mais próximo; o resto fica como histórico das tentativas.)
"""
import pathlib
import sys
from collections import Counter

LINHA = "#1"   # o contorno e a sombra sólida (a linha dos nós da direita, as separações): linhas, não malha
# A revisão (20/10/2026, pedido do Jean: o 40 e o 48 do aeb5ad75 tinham perdido parte da leitura da mão do 32): as linhas
# de dentro passam a vir do 32 pelo vizinho mais próximo (com 1 ou 2 px, na proporção do 32; só o contorno de fora com
# 1 px), e os ajustes à mão corrigem onde o arredondamento engrossou, afinou ou fundiu as formas. A versão anterior (as
# linhas forçadas a 1 px, que no 48 viravam riscos e no 40 apagavam os vãos dos dedos e do polegar) fica em
# anterior_aeb5ad75/.
SO_FORA = True
# A réplica (20/10/2026, pedido do Jean: "precisamos de réplicas idênticas no 40 e no 48", olhando pixel a pixel contra o
# 32): o 40 e o 48 são o 32 pelo vizinho mais próximo, puro: cada pixel de N é o pixel do 32 de que ele vem, sem afinar o
# contorno, sem refazer a malha e sem ajustes (como o 64 é o 32 ×2, numa escala não inteira: cada pixel do 32 vira um
# bloco de 1 ou 2 px). As regras anteriores (o contorno de 1 px, a malha na grade de N, os ajustes) mudavam o desenho:
# o dedo mínimo da direita perdia o vão, o alto dos dedos da esquerda mudava (fd60dd2c, em anterior_fd60dd2c/).
PURO = True
ENGROSSA = "a linha que a escala dobrou (2 px onde o 32 tem 1, fora da proporção): 1 px, o resto no material vizinho"
NOS = "os nós da direita na proporção do 32 (a linha preta, a faixa acesa, a sombra escura, cada uma com a mesma altura)"
PONTA = "a ponta do dedo do meio da esquerda, plana como no 32 (a escala a afinava em 1 px)"
AJUSTES = {   # (y, x0, trecho, porquê); " " no trecho mantém o pixel
    40: [(13, 22, "ccd", ENGROSSA + ": o bloco preto do encontro das luvas, abaixo dos dedos"),
         (16, 23, "4", ENGROSSA + ": a sombra do polegar da direita, ao lado da malha"),
         (17, 23, "6", ENGROSSA + ": a sombra do polegar da direita"), (18, 23, "4", ENGROSSA + ": a sombra do polegar da direita"),
         (24, 23, "3", ENGROSSA + ": a sombra do polegar da direita"),
         (23, 6, "424", ENGROSSA + ": o canto preto da junção da luva da esquerda com o punho"),
         (28, 14, "53", ENGROSSA + ": a beira direita do punho da esquerda")],
    48: [(2, 21, "#ddd#", PONTA), (1, 22, "###", PONTA),
         (5, 26, "de", ENGROSSA + ": o contorno duplo no alto do dedo seguinte"),
         (11, 10, "#e", ENGROSSA + ": o topo do polegar da esquerda"), (11, 13, "#e", ENGROSSA + ": o topo do polegar da esquerda"),
         (14, 30, "deeefffff", NOS), (17, 31, "646464646", NOS),
         (18, 41, "c", ENGROSSA + ": a sombra da beira da malha"),
         (22, 43, "4", ENGROSSA + ": a sombra da beira direita da malha"), (23, 43, "6", ENGROSSA + ": a sombra da beira direita da malha"),
         (37, 43, "6", ENGROSSA + ": a sombra da beira direita do punho"), (38, 43, "4", ENGROSSA + ": a sombra da beira direita do punho"),
         (24, 29, "4", ENGROSSA + ": a sombra do polegar da direita, ao lado da malha"),
         (25, 29, "6", ENGROSSA + ": a sombra do polegar da direita"), (26, 29, "4", ENGROSSA + ": a sombra do polegar da direita"),
         (27, 29, "6", ENGROSSA + ": a sombra do polegar da direita"),
         (35, 28, "3546464646464646", ENGROSSA + ": a costura entre a faixa e o punho da direita (2 linhas pretas inteiras: 1)")]}


def ler(base):
    return [l for l in (base / "grades/L7.txt").read_text(encoding="utf-8").split("\n")[:32]]


def volume_malha(g):
    """O tom do volume de cada pixel de malha do 32: a média dele com os vizinhos de malha (o xadrez vira o volume)."""
    v = {}
    for y in range(32):
        for x in range(32):
            if not g[y][x].isdigit() or g[y][x] in LINHA: continue
            viz = [int(g[y + dy][x + dx]) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                   if 0 <= x + dx < 32 and 0 <= y + dy < 32 and g[y + dy][x + dx].isdigit() and g[y + dy][x + dx] not in LINHA]
            v[(x, y)] = sum(viz) / len(viz)
    return v


def tamanho(g, N, so_fora=False):
    fonte = lambda X: int((X + 0.5) * 32 / N)
    primeiro = lambda X: X == 0 or fonte(X) != fonte(X - 1)
    vol = volume_malha(g)
    m = [[g[fonte(Y)][fonte(X)] for X in range(N)] for Y in range(N)]
    cheio = lambda X, Y: 0 <= X < N and 0 <= Y < N and m[Y][X] != "."
    fora = lambda X, Y: any(not cheio(X + dx, Y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    out = [row[:] for row in m]
    # o contorno: de fora com 1 px; as linhas de dentro só no primeiro pixel de cada pixel do 32
    dobra = []
    linha = lambda ch: ch in LINHA
    for Y in range(N):
        for X in range(N):
            if not linha(m[Y][X]): continue
            if m[Y][X] == "#" and fora(X, Y): continue
            sx, sy = fonte(X), fonte(Y)
            g_ = lambda dx, dy: g[sy + dy][sx + dx] if 0 <= sx + dx < 32 and 0 <= sy + dy < 32 else "."
            borda_fonte = m[Y][X] == "#" and any(g_(dx, dy) == "." for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            # a direção da linha no 32: deitada (vizinhos da mesma linha dos lados), em pé (em cima e embaixo), ou as duas;
            # a sombra do tom 1 segue só a própria linha (encostar no contorno não a engrossa)
            mesma = (lambda c: c == "1") if m[Y][X] == "1" else (lambda c: c == "#")
            deitada = mesma(g_(1, 0)) or mesma(g_(-1, 0))
            em_pe = mesma(g_(0, 1)) or mesma(g_(0, -1))
            if deitada and not em_pe: fica = primeiro(Y)              # a espessura é vertical
            elif em_pe and not deitada: fica = primeiro(X)            # a espessura é horizontal
            elif deitada and em_pe: fica = primeiro(X) or primeiro(Y)  # o canto, o cruzamento
            else: fica = primeiro(X) and primeiro(Y)                   # o ponto solto: 1 px
            if so_fora: fica = True                                    # a forma do 32 pelo vizinho (as linhas de dentro com 1 ou 2 px)
            if borda_fonte or not fica: dobra.append((X, Y))
    for X, Y in dobra:
        viz = [m[Y + dy][X + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
               if 0 <= X + dx < N and 0 <= Y + dy < N and m[Y + dy][X + dx] not in "." + LINHA]
        out[Y][X] = Counter(viz).most_common(1)[0][0] if viz else "#"
    # a malha na grade de N
    for Y in range(N):
        for X in range(N):
            if not out[Y][X].isdigit() or out[Y][X] in LINHA: continue
            sx, sy = fonte(X), fonte(Y)
            t = round(vol.get((sx, sy), int(out[Y][X])))
            out[Y][X] = str(min(t + 1, 7) if (X + Y) % 2 == 0 else max(t - 1, 2))
    return ["".join(l) for l in out], len(dobra)


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1]); N = int(sys.argv[2])
    if PURO:
        g32 = ler(base); fonte = lambda X: int((X + 0.5) * 32 / N)
        g = [[g32[fonte(Y)][fonte(X)] for X in range(N)] for Y in range(N)]; d = 0
        AJUSTES[N] = []
    else:
        g, d = tamanho(ler(base), N, so_fora=SO_FORA)
        g = [list(l) for l in g]
    for y, x0, trecho, _ in AJUSTES[N]:
        for k, ch in enumerate(trecho):
            if ch != " ": g[y][x0 + k] = ch
    g = ["".join(l) for l in g]
    (base / f"grades/L7-{N}.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    print(f"{N}: {d} pixels de linha dobrada no material vizinho; {len(AJUSTES[N])} ajustes à mão")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(g)))
