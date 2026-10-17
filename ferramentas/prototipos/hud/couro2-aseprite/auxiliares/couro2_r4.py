"""Os tamanhos 40 e 48 dos quatro desenhos aprovados (o capuz de couro da rodada 2, a luva de couro da rodada 1, a luva
de seda da rodada 2, o capuz de tecido da rodada 3): a mesma construção de cada peça, escrita para qualquer grade. As
listas de pixels por camada que o pintar.lua (ferramentas/arte/aseprite/) escreve no Aseprite pelo MCP; o Python só
calcula.

    python ferramentas/prototipos/hud/couro2-aseprite/auxiliares/couro2_r4.py <pasta> [capuz|luva|luva_seda|capuz_tecido] [32,40,48]

Como cada tamanho sai (nada é ampliação por fator não inteiro):
- as formas (a cabeça, a abertura, a capa, a mão, o cano...) são as faixas de cada linha do 32 lidas como bordas
  contínuas: a borda esquerda e a direita de cada parte passam pelos centros das linhas do 32 e, entre elas, seguem em
  reta; cada tamanho preenche os pixels cujo centro cai dentro, na grade dele (a diagonal continua diagonal, sem os
  degraus repetidos de uma ampliação);
- a luz de cada parte é a mesma regra do 32, nas coordenadas do 32 (as faixas de tom ficam proporcionais);
- os detalhes finos ficam finos: a costura do crânio, os vincos da capa, a fenda e o cordão da braçadeira, o vão dos
  dedos e o contorno continuam com 1 px; o cordão cruzado do capuz continua um 2×2; o desgaste, dois pixels;
- a borda da abertura, o forro e a parede de dentro saem da abertura de cada tamanho (o anel de 1 px em volta).
Conferido: no 32, cada peça sai igual, pixel a pixel, ao aprovado (`conferir_32`); os retoques de grade de cada
tamanho, quando precisos, vão em AJUSTES com o porquê.
"""
import math
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parents[1] / "couro-aseprite" / "auxiliares"))
from couro2_r1 import ABERTURA, CANO, DEDOS, MAO, POLEGAR  # noqa: E402
from couro2_r2 import (CABECA, CABECA_T, CAPA_LARG, DEDOS_S, FORRO_TECIDO, MAO_S, POLEGAR_S, PUNHO_S, SEDA,  # noqa: E402
                       TECIDO)
from couro2_r3 import CX, CY, DOBRAS, PALA  # noqa: E402
from couro_r2 import BORDA, BOTA, CORDAO, COURO, FORRO, GASTO, Desenho  # noqa: E402

PROPOSTA = AQUI.parent  # couro2-aseprite/


class Grade:
    """Um tamanho n: a ponte entre os pixels dele e as coordenadas do 32."""

    def __init__(self, n):
        self.n, self.s = n, n / 32

    def c(self, X):
        """O centro do pixel X do tamanho, em coordenadas do 32 (o pixel k do 32 vai de k a k+1)."""
        return (X + 0.5) / self.s

    def k(self, X):
        """O pixel do 32 que contém o centro do pixel X."""
        return math.floor(self.c(X))

    def alvo(self, k):
        """O pixel do tamanho que contém o centro do pixel k do 32."""
        return math.floor((k + 0.5) * self.s)

    def regiao(self, faixas32):
        """As faixas {y: (x0, x1)} de uma parte do 32, lidas como bordas contínuas, na grade do tamanho: {Y: (X0, X1)}."""
        ys = sorted(faixas32)
        py = [y + 0.5 for y in ys]
        esq = [faixas32[y][0] for y in ys]
        dir_ = [faixas32[y][1] + 1 for y in ys]
        out = {}
        for Y in range(self.n):
            yc = self.c(Y)
            if not ys[0] <= yc < ys[-1] + 1:
                continue
            a, b = _interp(yc, py, esq), _interp(yc, py, dir_)
            xs = [X for X in range(self.n) if a <= self.c(X) < b]
            if xs:
                out[Y] = (xs[0], xs[-1])
        return out

    def linha(self, p0, p1):
        """A reta de 1 px entre dois pixels do 32 (levados ao tamanho), sem buracos."""
        (x0, y0), (x1, y1) = (self.alvo(p0[0]), self.alvo(p0[1])), (self.alvo(p1[0]), self.alvo(p1[1]))
        pts, dx, dy = [], abs(x1 - x0), -abs(y1 - y0)
        sx, sy, err = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1), dx + dy
        while True:
            pts.append((x0, y0))
            if (x0, y0) == (x1, y1):
                return pts
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy


def _interp(v, xs, ys):
    if v <= xs[0]: return ys[0]
    if v >= xs[-1]: return ys[-1]
    for i in range(1, len(xs)):
        if v <= xs[i]:
            t = (v - xs[i - 1]) / (xs[i] - xs[i - 1])
            return ys[i - 1] + t * (ys[i] - ys[i - 1])


def preencher(d, reg, camada, rampa, tom):
    """Pinta cada linha Y de reg {Y: (X0, X1)} com tom(X, Y) (None deixa vazio)."""
    for Y, (a, b) in reg.items():
        for X in range(a, b + 1):
            t = tom(X, Y)
            if t is not None:
                d.px[(X, Y)] = (camada, rampa, max(0, min(len(rampa) - 1, t)))


def conjunto(reg):
    return {(X, Y) for Y, (a, b) in reg.items() for X in range(a, b + 1)}


def _abertura_e_borda(g, d, dentro, rampa_luz, tons, rampa_sombra, forro):
    """A borda em volta da abertura (acesa em cima e à esquerda) e o interior (o forro logo abaixo da borda de cima, a
    parede de dentro da direita um pouco clara): as regras das rodadas 1 a 3, em coordenadas do 32."""
    for (X, Y) in list(d.px):
        if any((X + dx, Y + dy) in dentro for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            acesa = g.c(Y) < 11 or g.c(X) < 15
            d.px[(X, Y)] = ("borda", rampa_luz if acesa else rampa_sombra,
                            tons[0] if acesa and g.c(X) < 16 else tons[1] if acesa else tons[2])
    direita = {}
    for (X, Y) in dentro:
        direita[Y] = max(direita.get(Y, X), X)

    def tom_dentro(X, Y):
        if (X, Y - 1) not in dentro: return 1
        x1 = direita[Y]
        return 2 if X == x1 else 1 if X == x1 - 1 else 0
    reg = {}
    for (X, Y) in dentro:
        a, b = reg.get(Y, (X, X)); reg[Y] = (min(a, X), max(b, X))
    preencher(d, reg, "interior", forro, tom_dentro)


def _barra(g, x_meio, meio, lados, expoente):
    """A barra de baixo de uma capa: a linha de baixo de cada coluna, a curva do 32 (round) lida contínua. Devolve a
    função "o pixel (X, Y) está acima da barra"."""
    def dentro(X, Y):
        xs = g.c(X) - 0.5
        v = meio + ((abs(xs - x_meio) / 12.5) ** expoente) * (lados - meio)
        return g.c(Y) - 0.5 <= v + 0.5 - 1e-9
    return dentro


# --- o capuz de couro (rodada 2) ----------------------------------------------------------------------------------
def capuz(n):
    g, d = Grade(n), Desenho(n)
    dentro = conjunto(g.regiao(ABERTURA))
    costura = {(g.alvo(16 + (yr <= 3)), Y) for Y in range(n) for yr in [g.k(Y)] if 2 <= yr <= 8}

    def tom_cabeca(X, Y):
        if (X, Y) in dentro: return None
        x, y = g.c(X), g.c(Y)
        t = 5 if x < 12 else 4 if x < 20 else 3
        if x >= 23: t = 2
        if y < 9 and x < 16: t += 1                                     # o alto do crânio, de frente para a luz
        if (X, Y) in costura: t = 3                                     # a costura do meio
        if y >= 16: t -= 1                                              # o capuz vira para baixo, na sombra
        return t
    preencher(d, g.regiao(CABECA), "capuz", COURO, tom_cabeca)
    _abertura_e_borda(g, d, dentro, COURO, (6, 5, 2), BORDA, FORRO)

    acima = _barra(g, 15.5, 23, 27, 1.3)
    vinco_e = set(g.linha((11, 21), (6, 26)))                           # desce para a esquerda
    vinco_d = set(g.linha((20, 21), (25, 26)))                          # desce para a direita
    capa = g.regiao(CAPA_LARG)

    def tom_capa(X, Y):
        if not acima(X, Y): return None
        x = g.c(X)
        t = 5 if x < 9 else 4 if x < 16 else 3 if x < 23 else 2
        if (X, Y) in vinco_e: return 2
        if (X + 1, Y) in vinco_e: return 6                              # a crista acesa do vinco da esquerda
        if (X, Y) in vinco_d: return 1
        if (X - 1, Y) in vinco_d: return 3
        if not acima(X, Y + 1) and x >= 16: t -= 1                      # a beira de baixo vira para dentro, na sombra
        return t
    preencher(d, capa, "capa", COURO, tom_capa)
    for (X, Y), (cam, _, _) in list(d.px.items()):                      # a sombra do capuz logo abaixo dele
        if cam == "capa" and g.k(Y) == 21 and 7 <= g.k(X) <= 24:
            d.px[(X, Y)] = ("capa", COURO, 2)
    x0, y0 = round(16 * g.s) - 1, round(21 * g.s) - 1                   # o cordão cruzado: um 2×2 em volta do meio
    d.px[(x0, y0)] = ("cordao", CORDAO, 2); d.px[(x0 + 1, y0)] = ("cordao", CORDAO, 1)
    d.px[(x0, y0 + 1)] = ("cordao", CORDAO, 1); d.px[(x0 + 1, y0 + 1)] = ("cordao", CORDAO, 2)
    gx, gy = g.alvo(25), g.alvo(24)                                     # o couro raspado na capa, do lado da sombra
    d.px[(gx, gy)] = ("desgaste", GASTO, 1); d.px[(gx + 1, gy + 1)] = ("desgaste", GASTO, 0)
    d.ajustar(AJUSTES.get(("capuz", n), {}))
    d.contornar()
    return d


# --- o capuz de tecido (rodada 3) ---------------------------------------------------------------------------------
def capuz_tecido(n):
    g, d = Grade(n), Desenho(n)
    dentro = conjunto(g.regiao(ABERTURA))
    cabeca = g.regiao({y: v for y, v in CABECA_T.items() if y <= 18})
    pala = g.regiao(PALA)
    tudo = cabeca | pala
    acima = _barra(g, CX, 26, 28, 1.6)

    def tom_pala(X, Y):
        if not acima(X, Y) or (X, Y) in dentro: return None
        x, y = g.c(X) - 0.5, g.c(Y) - 0.5                               # como as contas da rodada 3 (pixel inteiro no 32)
        r = (x - CX) / (y - CY)
        t = 4 if r < -0.75 else 3 if r < 0.15 else 2 if r < 0.7 else 1
        if 18.5 <= y < 20.5 and abs(x - CX) < 4 - (y - 19) * 1.5: t = min(t, 2)   # a sombra curta do queixo
        a = tudo[Y][0]
        if 19.5 <= y < 23.5 and X - a <= 1 and r < -1.3: t += 1         # o alto dos ombros, um tom acima
        for v in DOBRAS:
            dv = r - v
            if y >= 20.5 and -0.09 <= dv < 0.09: t -= 1
            elif y >= 20.5 and -0.26 <= dv < -0.09: t += 1
        if not acima(X, Y + 1) and x >= 17: t -= 1                      # a beira de baixo vira, só do lado da sombra
        return t

    def tom_cabeca(X, Y):
        if (X, Y) in dentro: return None
        x, y = g.c(X), g.c(Y)
        t = 4 if x < 12 else 3 if x < 20 else 2
        if x >= 23: t = 1
        if y < 9 and x < 16: t += 1
        if y >= 16: return tom_pala(X, Y)                               # os lados do capuz já descem para os ombros
        return t
    preencher(d, cabeca, "capuz", TECIDO, tom_cabeca)
    preencher(d, pala, "capa", TECIDO, tom_pala)
    _abertura_e_borda(g, d, dentro, TECIDO, (6, 5, 3), TECIDO, FORRO_TECIDO)
    d.ajustar(AJUSTES.get(("capuz_tecido", n), {}))
    d.contornar()
    return d


# --- as mãos -------------------------------------------------------------------------------------------------------
def _dedos(g, dedos, ate):
    """Os quatro dedos na grade do tamanho: as colunas de cada um (o vão entre eles fica com 1 px), a ponta (a linha do
    32 lida contínua) e a coluna do vão à direita. Devolve [(colunas, topo, coluna do vão ou None, (c0 do 32))]."""
    a = min(g.alvo(c0) for (c0, _), _ in dedos)
    b = max(g.alvo(c1) for (_, c1), _ in dedos)
    largura = b - a + 1 - (len(dedos) - 1)                              # sem os vãos de 1 px
    base, sobra = divmod(largura, len(dedos))
    larg = [base + (1 if i in _ordem_sobra(len(dedos))[:sobra] else 0) for i in range(len(dedos))]
    out, x = [], a
    for i, ((c0, c1), topo) in enumerate(dedos):
        cols = list(range(x, x + larg[i]))
        topo_t = min(Y for Y in range(g.n) if g.c(Y) >= topo)
        out.append((cols, topo_t, x + larg[i] if i < len(dedos) - 1 else None, c0))
        x += larg[i] + 1
    return out


def _ordem_sobra(n):
    """Quem ganha o pixel que sobra quando a mão não divide igual: os do meio primeiro (o médio e o anelar)."""
    return [1, 2, 0, 3][:n]


def luva(n):
    """A luva de couro com braçadeira (rodada 1)."""
    g, d = Grade(n), Desenho(n)
    fim_dedos = min(Y for Y in range(n) if g.c(Y) >= 10)                # a linha do nó dos dedos (y 10 do 32)
    mao = g.regiao(MAO)

    def tom_mao(X, Y):
        x = g.c(X)
        return (5 if x < 14 else 4 if x < 18 else 3 if x < 20 else 2) + (1 if g.k(Y) == 10 and x < 18 else 0)
    preencher(d, mao, "luva", COURO, tom_mao)
    dedos = _dedos(g, DEDOS, fim_dedos)
    tons = {11: (5, 5), 14: (5, 4), 17: (4, 3), 20: (3, 2)}
    for cols, topo, _, c0 in dedos:
        meio = len(cols) // 2 if len(cols) > 2 else 1                   # as colunas da esquerda com o tom aceso
        for Y in range(topo, fim_dedos):
            for i, X in enumerate(cols):
                t = tons[c0][0] if i < meio else tons[c0][1]
                d.px[(X, Y)] = ("luva", COURO, t + (1 if Y == topo else 0))
    for i, (cols, topo, vao, _) in enumerate(dedos[:-1]):              # o vão entre os dedos, preenchido abaixo das pontas
        topo_d = dedos[i + 1][1]
        for Y in range(max(topo, topo_d) + 1, fim_dedos):
            d.px[(vao, Y)] = ("luva", COURO, 2)
    preencher(d, g.regiao(POLEGAR), "luva", COURO, lambda X, Y: 6 if g.k(Y) == 10 else 5 if g.c(X) < 9 else 4)
    for Y in range(n):                                                 # a dobra entre o polegar e a mão
        if 13 <= g.k(Y) <= 14:
            d.px[(g.alvo(10), Y)] = ("luva", COURO, 2)
    cano = g.regiao(CANO)

    def tom_cano(X, Y):
        x = g.c(X)
        if g.k(Y) == 19: return 6 if x < 16 else 4                      # a beira de cima, virada
        return 5 if x < 13 else 4 if x < 17 else 3 if x < 21 else 2
    preencher(d, cano, "bracadeira", BOTA, tom_cano)
    ultima = max(cano)
    for X in range(n):                                                  # a barra
        if (X, ultima) in d.px: d.px[(X, ultima)] = ("bracadeira", BORDA, 2 if g.c(X) < 16 else 1)
    fenda = [Y for Y in range(n) if 21 <= g.k(Y) <= 28 and Y != ultima]
    xa, xb = g.alvo(15), g.alvo(15) + 1                                 # a fenda: duas colunas, como no 32
    for Y in fenda:
        d.px[(xa, Y)] = ("cordao", FORRO, 0); d.px[(xb, Y)] = ("cordao", FORRO, 0)
    for j, Y in enumerate(Y for Y in fenda if g.k(Y) <= 27):           # o cordão: um pixel por linha, alternando
        d.px[(xa if j % 2 == 0 else xb, Y)] = ("cordao", CORDAO, 2 if j % 2 == 0 else 1)
    gx, gy = g.alvo(20), g.alvo(25)                                     # o couro raspado
    d.px[(gx, gy)] = ("desgaste", GASTO, 0); d.px[(gx + 1, gy + 1)] = ("desgaste", GASTO, 1)
    d.ajustar(AJUSTES.get(("luva", n), {}))
    d.contornar()
    return d


def luva_seda(n):
    """A luva de seda (rodada 2): justa, os dedos separados até a mão, o punho curto, o brilho numa faixa."""
    g, d = Grade(n), Desenho(n)
    fim_dedos = min(Y for Y in range(n) if g.c(Y) >= 13)
    preencher(d, g.regiao(MAO_S), "luva", SEDA, lambda X, Y: (lambda x: 5 if x < 14 else 4 if x < 18 else 3 if x < 20 else 2)(g.c(X)))
    tons = {11: (5, 4), 14: (5, 4), 17: (4, 3), 20: (3, 2)}
    for cols, topo, _, c0 in _dedos(g, DEDOS_S, fim_dedos):
        meio = len(cols) // 2 if len(cols) > 2 else 1
        for Y in range(topo, fim_dedos):
            for i, X in enumerate(cols):
                t = tons[c0][0] + (1 if Y == topo else 0) if i < meio else tons[c0][1]
                d.px[(X, Y)] = ("luva", SEDA, t)
    preencher(d, g.regiao(POLEGAR_S), "luva", SEDA, lambda X, Y: 6 if g.k(Y) == 11 else 5 if g.c(X) < 10 else 4)
    # o brilho da seda: a faixa diagonal nas costas da mão (do nó dos dedos ao punho) e os dois toques nos dedos
    faixa = g.linha((13, 13), (15, 18))
    brilho = {p: (6 if i < len(faixa) / 2 else 5) for i, p in enumerate(faixa)}
    for Y in range(n):
        if 6 <= g.k(Y) <= 7: brilho[(g.alvo(14), Y)] = 6
    brilho[(g.alvo(11), g.alvo(8))] = 6
    for p, t in brilho.items():
        if p in d.px: d.px[p] = ("brilho", SEDA, t)
    punho = g.regiao(PUNHO_S)
    primeira, ultima = min(punho), max(punho)

    def tom_punho(X, Y):
        x = g.c(X)
        if Y == primeira: return 5 if x < 16 else 3
        t = 4 if x < 14 else 3 if x < 18 else 2
        return t - (1 if Y == ultima else 0)
    preencher(d, punho, "punho", SEDA, tom_punho)
    d.ajustar(AJUSTES.get(("luva_seda", n), {}))
    d.contornar()
    return d


# Os retoques de grade de cada tamanho (o porquê ao lado). {(peça, n): {(x, y): (camada, rampa, tom) ou None}}
# No capuz de tecido, a crista da dobra da esquerda cruza a fronteira do ombro aceso (tom 4) num ponto em que, no 32,
# ela não cruza: sobrava um pixel de tom 5 sozinho no meio do 4 (um brilho que o pano não tem). Volta ao tom do plano.
AJUSTES = {("capuz_tecido", 40): {(10, 29): ("capa", TECIDO, 4), (7, 33): ("capa", TECIDO, 4)},
           ("capuz_tecido", 48): {(15, 31): ("capa", TECIDO, 4), (12, 35): ("capa", TECIDO, 4), (9, 39): ("capa", TECIDO, 4)}}

PECAS = {"capuz": (capuz, ["capa", "capuz", "interior", "borda", "cordao", "desgaste", "contorno"]),
         "luva": (luva, ["bracadeira", "luva", "cordao", "desgaste", "contorno"]),
         "luva_seda": (luva_seda, ["punho", "luva", "brilho", "contorno"]),
         "capuz_tecido": (capuz_tecido, ["capa", "capuz", "interior", "borda", "contorno"])}
APROVADO_32 = {"capuz": "rodada2/capuz-32.png", "luva": "rodada1/luva-32.png", "luva_seda": "rodada2/luva_seda-32.png",
               "capuz_tecido": "rodada3/capuz_tecido-32.png"}


def imagem(peca, n):
    cam = PECAS[peca][0](n).camadas()
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    for c in PECAS[peca][1]:
        for (x, y), k in cam.get(c, {}).items():
            im.putpixel((x, y), tuple(int(k[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im, cam


def conferir_32():
    """O 32 de cada peça, refeito por esta construção, tem de sair igual ao aprovado, pixel a pixel."""
    res = {}
    for p, arq in APROVADO_32.items():
        feito = imagem(p, 32)[0]
        aprovado = Image.open(PROPOSTA / arq).convert("RGBA")
        dif = [(x, y) for y in range(32) for x in range(32) if feito.getpixel((x, y)) != aprovado.getpixel((x, y))]
        res[p] = dif
    return res


def gravar(peca, n, pasta):
    im, cam = imagem(peca, n)
    pasta.mkdir(parents=True, exist_ok=True)
    for c in PECAS[peca][1]:
        px = cam.get(c, {})
        texto = ";".join(f"{x},{y},{k}" for (x, y), k in sorted(px.items()))
        (pasta / f"{c}.txt").write_text(texto)
        (pasta / f"{c}.lua").write_text(f'return "{texto}"\n')
    im.save(pasta / "previa.png")
    (pasta / "camadas.txt").write_text(",".join(PECAS[peca][1]))
    return im.getbbox(), sum(len(v) for v in cam.values()), len({k for v in cam.values() for k in v.values()})


if __name__ == "__main__":
    if sys.argv[1:2] == ["--conferir"]:
        for p, dif in conferir_32().items():
            print(p, "32 igual ao aprovado" if not dif else f"32 DIFERENTE em {len(dif)} pixels: {dif[:12]}")
        sys.exit()
    saida = pathlib.Path(sys.argv[1])
    pecas = [a for a in sys.argv[2:] if a in PECAS] or list(PECAS)
    tamanhos = next((list(map(int, a.split(","))) for a in sys.argv[2:] if a[0].isdigit()), [40, 48])
    for p in pecas:
        for n in tamanhos:
            print(p, n, *gravar(p, n, saida / f"{p}-{n}"))
