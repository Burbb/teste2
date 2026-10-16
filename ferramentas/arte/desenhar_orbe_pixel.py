"""O orbe do Mago em pixel art (no jogo desde a 1.107.0; antes, o sprite 16×16 "orbe"). Pelo método do escudo e do
machado (pixel_comum.py), cada tamanho desenhado na própria grade.

O que o jogo diz (rpg/itens.py): o desenho "orbe" é o da arma Orbe e o do apoio Foco Arcano do Mago, em todos os
materiais (de Enferrujado a Rúnico: o suporte é de metal), e o do único Olho do Abismo ("Ele olha de volta. Sempre
olhou."). Nenhum outro papel usa o desenho "orbe" (os orbes de luz, sombra e arcano dos projéteis são outros sprites).
O desenho atual: uma esfera violeta num pé de latão. A esfera violeta no pé de latão é o que o faz ser este objeto e
fica.

O tipo: uma esfera de vidro violeta presa num suporte de latão: uma taça que engole o terço de baixo da esfera, três
garras que nascem da borda da taça e sobem pela esfera (as dos lados pelo contorno, a da frente pelo meio), um
pescoço curto e um pé largo. O suporte segura de fato a esfera: a borda da frente passa por cima dela, as garras se
fecham sobre a superfície e deixam sombra nela.

A luz, com a reflexão separada da luz de dentro:
  - a superfície (reflexão): o corpo do vidro pela direção da superfície (o lado da luz um pouco mais claro), a borda
    mais escura em volta e um reflexo pequeno e duro em cima à esquerda, quase branco: a janela que o vidro reflete;
  - a luz de dentro (o vidro que deixa a luz passar): um miolo lavanda macio, do lado oposto ao da luz, embaixo à
    direita, em três degraus, sempre dentro da esfera. Nenhuma aura fora do contorno.

A construção, em cada tamanho (32, 40, 48 e 64 px):
  - a esfera: um disco em centro de pixel; o latão é o rolo do escudo (o mesmo LATAO), com o tom pela posição na
    peça cilíndrica (o lado da luz à esquerda) e um fio de brilho;
  - a taça: a borda é uma faixa curva (a frente desce no meio: vista um pouco de cima), por cima da esfera; abaixo
    dela, o bojo estreita até o pescoço; sombra de contato na esfera logo acima da borda;
  - as garras: três, da espessura de 1 pixel em 32 e 40 e 2 em 48 e 64, com a ponta mais clara curvada para dentro;
    em 48 e 64, um anel no pé de cada garra (onde ela nasce da borda);
  - o pé: a face de cima (uma elipse, acesa) e a lateral (a faixa de baixo, em sombra), com o pescoço entre a taça e o
    pé;
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/arte/desenhar_orbe_pixel.py <pasta>    (grava noutra pasta: a proposta)
    python ferramentas/arte/desenhar_orbe_pixel.py            (grava em rpg/web/static/hud/icones/: só na integração)
"""

import sys

import numpy as np

from pixel_comum import LUZ, ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)

# As rampas, do mais escuro ao mais claro: o vidro violeta e o latão (o mesmo do escudo).
VIDRO = ["#100a1c", "#1d1236", "#2b1a52", "#3c2473", "#503196", "#6844b6", "#835fd0", "#a283e3", "#c6b0f4", "#f4eeff"]
LATAO = ["#26170a", "#40270c", "#623c12", "#8a571b", "#ae7526", "#cf9737", "#e9bb5c", "#f8dc94", "#fff5d6"]

# As medidas de cada tamanho, em pixels: o centro (cx, cy) e o raio (R) da esfera; a borda da taça (taca, a altura em
# fração de R abaixo do centro; curva, quanto a frente desce no meio; beira, a altura da faixa); a taça abraça a
# esfera até embaixo e passa dela (folga); o pescoço (pesc, a meia largura; y_pe, o centro da face de cima do pé); o
# pé (pe_w e pe_h, os semieixos da face de cima; pe_lado, a altura da lateral); as garras (g, a espessura; g_ate, até
# onde sobem, em fração de R acima do centro); `det` liga os anéis das garras (48 e 64).
MEDIDAS = {
    32: dict(cx=16.0, cy=12.0, R=9.4, taca=0.6, curva=1.0, beira=1.6, folga=0.7, pesc=1.5, y_pe=25.6, pe_w=6.3, pe_h=1.4, pe_lado=2.0, g=1.0, g_ate=0.22, det=0),
    40: dict(cx=20.0, cy=15.0, R=11.7, taca=0.6, curva=1.3, beira=2.0, folga=0.8, pesc=1.9, y_pe=32.0, pe_w=7.9, pe_h=1.8, pe_lado=2.5, g=1.0, g_ate=0.24, det=0),
    48: dict(cx=24.0, cy=18.0, R=14.0, taca=0.6, curva=1.6, beira=2.4, folga=0.9, pesc=2.3, y_pe=38.4, pe_w=9.5, pe_h=2.1, pe_lado=3.0, g=2.0, g_ate=0.26, det=1),
    64: dict(cx=32.0, cy=24.0, R=18.7, taca=0.6, curva=2.1, beira=3.0, folga=1.1, pesc=3.0, y_pe=51.2, pe_w=12.6, pe_h=2.8, pe_lado=3.9, g=2.0, g_ate=0.28, det=2),
}
# O reflexo da janela no vidro, desenhado por tamanho: {(dx, dy): tom} a partir do ponto de luz.
REFLEXO = {32: {(0, 0): 9, (1, 0): 8, (0, 1): 8},
           40: {(0, 0): 9, (1, 0): 9, (0, 1): 8, (2, 0): 7, (0, 2): 7},
           48: {(0, 0): 9, (1, 0): 9, (0, 1): 9, (1, 1): 8, (2, 0): 8, (0, 2): 7, (3, 0): 7},
           64: {(0, 0): 9, (1, 0): 9, (2, 0): 9, (0, 1): 9, (1, 1): 9, (2, 1): 8, (0, 2): 8, (3, 0): 8, (1, 2): 7,
                (4, 0): 7, (0, 3): 7}}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def cilindro(dx, meia, base=4):
    """O tom de uma peça de latão redonda vista de lado: o lado da luz (à esquerda) mais claro, um fio de brilho perto
    da borda da luz, o lado oposto em sombra."""
    nx = np.clip(dx / np.maximum(meia, 0.5), -1, 1)
    t = np.round(base - 0.4 - 2.4 * nx).astype(int)
    t = np.where((nx > -0.6) & (nx < -0.4), base + 2, np.minimum(t, base + 1))
    return np.clip(t, 1, 7)


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    cx, cy, R = M["cx"], M["cy"], M["R"]
    dx, dy = x - cx, y - cy
    d = np.hypot(dx, dy)

    # ---- a esfera de vidro: o corpo pela direção da superfície, a borda mais escura, a luz de dentro embaixo à direita
    esfera = d <= R
    r = np.clip(d / R, 0, 0.999)
    n = np.stack([dx / R, dy / R, np.sqrt(1 - r ** 2)], -1)
    nl = np.clip(n @ LUZ, 0, 1)
    t_vidro = np.select([nl > 0.8, nl > 0.5, nl > 0.2], [6, 5, 4], 3)
    t_vidro = np.where(r > 0.86, np.maximum(1, t_vidro - 1), t_vidro)          # a borda escurece (o vidro de lado)
    gx, gy = cx + 0.22 * R, cy + 0.26 * R                                       # a luz de dentro: oposta à da janela
    rg = np.hypot(x - gx, (y - gy) * 1.15) / R
    t_vidro = np.where(rg < 0.44, np.maximum(t_vidro, 5), t_vidro)
    t_vidro = np.where(rg < 0.3, np.maximum(t_vidro, 6), t_vidro)
    t_vidro = np.where(rg < 0.15, np.maximum(t_vidro, 7), t_vidro)
    mat[esfera], tom[esfera] = "q", t_vidro[esfera]
    fixo[esfera] = True

    # ---- a taça: a borda (uma faixa curva, a frente descendo no meio) e o bojo, que abraça a esfera até embaixo
    W = R * np.sqrt(1 - M["taca"] ** 2) + 0.5                                     # a meia largura da boca da taça
    curva = M["curva"] * np.sqrt(np.clip(1 - (dx / W) ** 2, 0, 1))
    y_borda = cy + M["taca"] * R + curva                                         # o pé da borda da frente
    borda = (np.abs(dx) <= W) & (y <= y_borda) & (y > y_borda - M["beira"])
    bojo = (y > y_borda) & (d <= R + M["folga"])
    larg = np.sqrt(np.clip((R + M["folga"]) ** 2 - dy ** 2, 0.25, None))       # a meia largura do bojo naquela altura
    mat[bojo], tom[bojo] = "l", np.maximum(1, cilindro(dx, larg) - np.where(dy > 0.9 * R, 1, 0))[bojo]
    mat[borda], tom[borda] = "l", cilindro(dx, W, base=5)[borda]
    lab = borda & (y > y_borda - 1)                                               # o lábio de baixo da borda, um degrau
    tom[lab] = np.maximum(1, tom[lab] - 1)
    fixo[borda | bojo] = True
    # a sombra de contato: o vidro logo acima da borda
    sombra = (mat == "q") & (y > y_borda - M["beira"] - 1.1)
    tom[sombra] = np.maximum(1, tom[sombra] - 2)

    # ---- as garras: as dos lados por dentro do contorno da esfera, a da frente pelo meio; sobem da borda e a ponta,
    # mais clara, se fecha para dentro
    topo_g = cy - M["g_ate"] * R
    g = M["g"]
    pe_g = y_borda - M["beira"] + 0.5
    for lado_g in (-1, 1):
        rr = R - 0.5 * g + 0.05                                                    # na beira da esfera: fazem o contorno
        ang_y = np.clip((y - cy) / rr, -1, 1)
        x_garra = cx + lado_g * rr * np.sqrt(1 - ang_y ** 2)
        garra = esfera & (y <= pe_g) & (y >= topo_g) & (np.abs(x - x_garra) <= g / 2 + 0.05)
        t_g = 6 if lado_g < 0 else 3
        mat[garra], tom[garra] = "l", t_g
        alto = garra & (y < topo_g + 1.2)
        tom[alto] = t_g + 1
        ys = np.where(alto.any(axis=1))[0]
        if len(ys):  # a ponta se fecha: um pixel para dentro, na altura do topo
            yy = ys[0]; xs = np.where(alto[yy])[0]
            xx = xs.max() + 1 if lado_g < 0 else xs.min() - 1
            mat[yy, xx], tom[yy, xx] = "l", t_g + 1
            fixo[yy, xx] = True
        # a sombra da garra no vidro, à direita dela (o lado oposto ao da luz)
        sg = (mat == "q") & (np.abs(x - (x_garra + g / 2 + 0.55)) <= 0.5) & (y >= topo_g) & (y <= pe_g)
        tom[sg] = np.maximum(1, tom[sg] - 2)
        fixo[garra] = True
    # a da frente: sobe pelo meio da esfera vista de frente
    xf = cx - 0.5
    frente = esfera & (np.abs(x - xf) <= g / 2 + 0.05) & (y >= topo_g + 0.8) & (y <= pe_g)
    mat[frente], tom[frente] = "l", 5
    tom[frente & (y < topo_g + 2.0)] = 7
    sf = (mat == "q") & (x > xf + g / 2) & (x < xf + g / 2 + 1.05) & (y >= topo_g + 0.8) & (y <= pe_g)
    tom[sf] = np.maximum(1, tom[sf] - 2)
    fixo[frente] = True
    if M["det"]:  # o anel no pé de cada garra, onde ela nasce da borda
        ya = cy + M["taca"] * R - M["beira"] + 0.2                                # logo acima da borda, nos lados
        xl = (R - 0.5 * g - 0.6) * np.sqrt(1 - ((ya - cy) / R) ** 2)
        for xa, yy in ((cx - xl, ya), (xf, ya + M["curva"]), (cx + xl, ya)):
            anel = (np.abs(x - xa) <= g / 2 + 0.6) & (np.abs(y - yy) <= 0.55) & (mat != "")
            mat[anel], tom[anel] = "l", np.where(x[anel] < xa, 7, 4)

    # ---- o reflexo da janela: um grupo duro em cima à esquerda (a regra do vidro)
    bx = int(np.floor(cx - 0.5 * R)); by_ = int(np.floor(cy - 0.52 * R))
    for (ox, oy), t_ in REFLEXO[lado].items():
        if mat[by_ + oy, bx + ox] == "q":
            tom[by_ + oy, bx + ox] = t_

    # ---- o pescoço e o pé (um disco: a face de cima acesa, a lateral em sombra)
    y_baixo = cy + R + M["folga"]
    pesc = (y > y_baixo - 0.5) & (y <= M["y_pe"]) & (np.abs(dx) <= M["pesc"])
    mat[pesc], tom[pesc] = "l", np.maximum(1, cilindro(dx, M["pesc"], base=3))[pesc]
    em = lambda y0: (dx / M["pe_w"]) ** 2 + ((y - y0) / M["pe_h"]) ** 2 <= 1
    face = em(M["y_pe"])
    disco = face.copy()
    for k in np.arange(0, M["pe_lado"] + 0.01, 0.5):
        disco |= em(M["y_pe"] + k)
    lateral = disco & ~face
    mat[lateral], tom[lateral] = "l", np.maximum(1, cilindro(dx, M["pe_w"], base=3) - 1)[lateral]
    t_face = np.where(dx < -0.35 * M["pe_w"], 6, np.where(dx < 0.3 * M["pe_w"], 5, 4))
    mat[face], tom[face] = "l", t_face[face]
    sombra_p = face & (np.abs(dx + 0.7) <= M["pesc"] + 1.0) & (y < M["y_pe"] + 0.6)   # o pescoço deixa sombra na face
    tom[sombra_p] = 3
    fixo[pesc | disco] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"q": VIDRO, "l": LATAO})


if __name__ == "__main__":
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"orbe-{lado}: {salvar(desenhar(lado), saida, 'orbe')} cores")
