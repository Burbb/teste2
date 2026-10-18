"""Histórico: a direção anterior da aljava (rodadas 1 a 8, recusada em 18/10/2026). A aljava do jogo (1.122.0) vem das
fontes em camadas de ferramentas/arte/aseprite/aljava/ (exportar_aseprite.py aljava); este script só grava numa pasta.

A aljava (o equipamento secundário do Patrulheiro e o ícone das flechas no topo) no método da família: proposta,
nada no jogo. Rodada 6 (a 5 e as anteriores em ferramentas/prototipos/hud/itens-lote-noite/aljava/rodadaN/).

O pedido do Jean na rodada 6: a aljava lembrava uma bolsa de tacos de golfe; as pontas das flechas pareciam cabeças
engrossadas (as penas eram um bloco claro de 2 px). O que se lê agora, primeiro em tamanho real:
  - as hastes: madeira de 1 px, traçadas na grade (Bresenham) da boca até a ponta;
  - as penas: palhetas de 1 px dos dois lados da haste, nas últimas linhas (a haste continua visível pelo meio, em
    madeira); a do meio com penas vermelhas, para as três não virarem uma mancha;
  - o entalhe: no 32, 1 px de madeira escura além das penas;
  - a boca: uma elipse em perspectiva no topo do tubo, com o aro de couro aceso e o fundo escuro, de onde as hastes
    saem (elas começam dentro da abertura).
O tubo é o couro do conjunto aprovado (as rampas de `couro_r2.py`), em pé e inclinado para a direita, com as cintas
de borda e, no 32, a alça do lado da sombra. Sem ornamento.

O 32 (a ficha) e o 24 (o topo) têm cada um as suas medidas, em pixels da própria grade (PERFIL); o 64 é o 32 ampliado
2×. Os 40 e 48 (rodada 8) se derivam da construção aprovada do 32 (`_derivado`).

    python ferramentas/arte/desenhar_aljava_pixel.py <pasta> [--listas]
"""

import math
import sys

import numpy as np
from PIL import Image

import pixel_comum as pc

COURO = ["#1C120C", "#2E1E13", "#45301E", "#604229", "#7C5634", "#986C42", "#B48752"]
BORDA = ["#140C08", "#22150D", "#321F13", "#45301E"]
MADEIRA = ["#4A3424", "#7A5C3C", "#B08A5E", "#D8B888"]          # a haste: do entalhe escuro à madeira acesa
PENA = ["#8A8476", "#C4BEAE", "#ECE6D6"]                           # as penas claras
PENA_V = ["#5E1A12", "#962C1C", "#C8462C"]                         # as penas vermelhas (a flecha do meio)
FUNDO = ["#0C0806"]                                                # o escuro de dentro da boca
RAMPAS = {"k": COURO, "b": BORDA, "m": MADEIRA, "p": PENA, "v": PENA_V, "x": FUNDO}

# as medidas de cada tamanho, em pixels da própria grade
PERFIL = {
    32: {"fundo": (10.8, 26.6), "inclina": 20.0, "tubo": 13.4, "larg": (3.5, 4.1),
         "cintas": ((2.8, 4.0), (8.6, 9.8)), "fundo_borda": 1.8, "aro": 1.0, "boca_k": 0.56,
         "alca": (2.6, 11.6, 2.6),
         # as flechas: (desvio de través na boca, inclinação em graus a partir da vertical, comprimento, penas vermelhas?)
         "flechas": ((-1.6, -10.0, 12.4, False), (2.0, 13.0, 11.4, True)),
         "pena": (0, 1, 2, 2, 1),   # a meia-largura das penas em cada linha a partir do fim (0: o entalhe, só a haste)
         "entalhe": True},
    24: {"fundo": (8.6, 19.0), "inclina": 22.0, "tubo": 9.8, "larg": (3.2, 3.6),
         "cintas": ((4.0, 5.2),), "fundo_borda": 1.6, "aro": 0.9, "boca_k": 0.56,
         "alca": None,
         "flechas": ((-1.4, -10.0, 8.6, False), (1.8, 14.0, 7.8, True)),
         "pena": (1, 1, 1),
         "entalhe": False},
}


def _derivado(n):
    """Os intermediários (40 e 48, rodada 8): a construção aprovada do 32 (rodada 7) nas medidas da grade deles (as
    posições e os comprimentos multiplicados por n/32); o que é de 1 px (a haste, a palheta das penas, a alça, o
    entalhe, o contorno) continua de 1 px; as penas ganham uma linha a mais por tamanho."""
    b, k = PERFIL[32], n / 32
    return {"fundo": (b["fundo"][0] * k, b["fundo"][1] * k), "inclina": b["inclina"], "tubo": b["tubo"] * k,
            "larg": (b["larg"][0] * k, b["larg"][1] * k),
            "cintas": tuple((c0 * k, c1 * k) for c0, c1 in b["cintas"]), "fundo_borda": b["fundo_borda"] * k,
            "aro": b["aro"] * k, "boca_k": b["boca_k"], "alca": (b["alca"][0] * k, b["alca"][1] * k, b["alca"][2] * k),
            "flechas": tuple((dw * k, ang, comp * k, verm) for dw, ang, comp, verm in b["flechas"]),
            "pena": {40: (0, 1, 2, 2, 2, 1), 48: (0, 1, 2, 3, 3, 2, 1)}[n], "entalhe": True}


PERFIL[40] = _derivado(40)
PERFIL[48] = _derivado(48)
CAMADAS = ["couro", "borda", "boca", "hastes", "penas", "contorno"]   # de baixo para cima (as fontes em camadas)


def _reta(x0, y0, x1, y1):
    """Os pixels da reta (Bresenham) de (x0, y0) a (x1, y1), na ordem."""
    x0, y0, x1, y1 = (int(round(v)) for v in (x0, y0, x1, y1))
    pts, dx, dy = [], abs(x1 - x0), -abs(y1 - y0)
    sx, sy, err = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1), dx + dy
    while True:
        pts.append((x0, y0))
        if (x0, y0) == (x1, y1):
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy


def desenhar(lado, partes=False):
    """A imagem do tamanho; com partes=True, também a camada de cada pixel (CAMADAS)."""
    M = PERFIL[lado]
    mat, tom, fixo, X, Y = pc.grade(lado)
    x0, y0 = M["fundo"]
    th = math.radians(M["inclina"])
    ax, ay = math.sin(th), -math.cos(th)            # o eixo do tubo (para cima, inclinado à direita)
    px_, py_ = math.cos(th), math.sin(th)           # de través (positivo: à direita, o lado da sombra)
    a = (X - x0) * ax + (Y - y0) * ay
    w = (X - x0) * px_ + (Y - y0) * py_
    L = M["tubo"]
    meia = M["larg"][0] + (M["larg"][1] - M["larg"][0]) * np.clip(a / L, 0, 1)

    # o tubo de couro: o cilindro em faixas pela direção da superfície, o fundo arredondado mais escuro
    tubo = (a >= 0) & (a <= L) & (np.abs(w) <= meia)
    fundo = (a < 0) & (a * a + w * w <= M["larg"][0] ** 2)
    corpo = tubo | fundo
    mat[corpo] = "k"
    p = w / meia
    tom[corpo] = np.where(p < -0.5, 6, np.where(p < -0.05, 5, np.where(p < 0.45, 4, 3)))[corpo]
    borda_fundo = corpo & (a < M["fundo_borda"])
    mat[borda_fundo] = "b"
    tom[borda_fundo] = np.where(p < 0, 3, 2)[borda_fundo]
    for (c0, c1) in M["cintas"]:   # as cintas: borda escura, a linha de cima acesa do lado da luz
        cinta = corpo & (a >= c0) & (a < c1)
        mat[cinta] = "b"
        tom[cinta] = np.where(p < 0.3, 2, 1)[cinta]
        topo_c = cinta & (a >= c1 - 1.0) & (p < 0.1)
        tom[topo_c] = 3
    # a boca em perspectiva: a elipse do topo (semieixo de través = a largura, ao longo do eixo = boca_k × largura);
    # o anel de fora é o aro de couro dobrado (aceso do lado da luz), o miolo é o escuro de dentro
    R = M["larg"][1] + 0.35
    da = a - L
    elipse = (w / R) ** 2 + (da / (R * M["boca_k"])) ** 2
    aro = (elipse <= 1.0)
    dentro = (w / (R - M["aro"])) ** 2 + (da / ((R - M["aro"]) * M["boca_k"])) ** 2 <= 1.0
    mat[aro] = "k"
    tom[aro] = np.where(w < -0.3 * R, 6, np.where(w < 0.4 * R, 5, 3))[aro]
    # o lábio da frente (a metade de baixo do aro) um tom abaixo: a espessura do couro
    labio = aro & ~dentro & (da > 0.15)
    tom[labio] = np.where(w[labio] < 0.4 * R, 6, 4)
    mat[dentro] = "x"
    tom[dentro] = 0
    fixo[aro] = True

    # as flechas (rodada 7): a haste de 1 px da boca até o fim, à vista entre as penas e a boca; as penas como dois
    # paralelogramos contínuos presos à haste, um de cada lado, inclinados para trás (a parte de fora mais perto do
    # fim da flecha); no 32, o entalhe é só 1 px de haste escura além das penas (sem o U)
    centro_boca = (x0 + ax * L, y0 + ay * L)
    for (dw, ang, comp, vermelha) in M["flechas"]:
        sx = centro_boca[0] + px_ * dw
        sy = centro_boca[1] + py_ * dw
        t = math.radians(ang)
        dx, dy = math.sin(t), -math.cos(t)          # do pé (na boca) para o fim da flecha
        ex, ey = sx + dx * comp, sy + dy * comp       # o fim (o entalhe)
        # a haste
        for i, (hx, hy) in enumerate(_reta(sx, sy, ex, ey)):
            if not (0 <= hx < lado and 0 <= hy < lado):
                continue
            mat[hy, hx] = "m"
            tom[hy, hx] = 0 if (mat[hy, hx] == "x" and i < 2) else 2
            fixo[hy, hx] = True
        # as penas, linha a linha a partir do fim da haste: em cada linha, a meia-largura de PENA (a primeira linha é a
        # do entalhe, quando há), centrada no pixel da haste daquela linha; o lado da luz (à esquerda) mais claro
        linhas = {}
        for (hx, hy) in reversed(_reta(sx, sy, ex, ey)):
            linhas.setdefault(hy, hx)
        ordem = sorted(linhas, key=lambda yy: (yy - ey) * (1 if dy > 0 else -1), reverse=True)
        for k, larg in enumerate(M["pena"]):
            if k >= len(ordem) or larg == 0:
                continue
            hy = ordem[k]
            hx = linhas[hy]
            for off in range(1, larg + 1):
                for lado_s in (-1, 1):
                    qx = hx + lado_s * off
                    if 0 <= qx < lado and 0 <= hy < lado and mat[hy, qx] in ("", "x", "k", "b"):
                        mat[hy, qx] = "v" if vermelha else "p"
                        tom[hy, qx] = 2 if lado_s < 0 else 1
                        fixo[hy, qx] = True
        if M["entalhe"]:                              # o fim da haste além das penas, escuro (sem o U)
            nx, ny = int(round(ex)), int(round(ey))
            if 0 <= nx < lado and 0 <= ny < lado:
                mat[ny, nx], tom[ny, nx], fixo[ny, nx] = "m", 0, True

    # a alça: um arco de couro escuro do lado da sombra, fora do tubo (só no 32)
    if M["alca"]:
        a0, a1, sai = M["alca"]
        meio = (a0 + a1) / 2
        k = np.clip(1 - ((a - meio) / ((a1 - a0) / 2)) ** 2, 0, 1)
        w_alca = meia + 0.3 + sai * k
        alca = (a >= a0) & (a <= a1) & (np.abs(w - w_alca) <= 0.55) & (mat == "")
        mat[alca], tom[alca], fixo[alca] = "b", 2, True

    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    img = pc.imagem(mat, tom, RAMPAS)
    if not partes:
        return img
    camada = np.full(mat.shape, "", dtype=object)
    for m, c in (("k", "couro"), ("b", "borda"), ("x", "boca"), ("m", "hastes"), ("p", "penas"), ("v", "penas"), ("c", "contorno")):
        camada[mat == m] = c
    return img, camada


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, "aljava"), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, "aljava"), "cores (o 32 ampliado 2×)")
    print(24, pc.salvar(desenhar(24), pasta, "aljava"), "cores (o topo)")
    for lado in (40, 48):
        print(lado, pc.salvar(desenhar(lado), pasta, "aljava"), "cores (intermediário)")
    if "--listas" in sys.argv:   # as listas por camada para as fontes em camadas (montar_fontes.py)
        for lado in (24, 32, 40, 48):
            print("listas", pc.listas_camadas(desenhar(lado, partes=True), pasta / "listas" / f"aljava-{lado}", CAMADAS))


if __name__ == "__main__":
    main()
