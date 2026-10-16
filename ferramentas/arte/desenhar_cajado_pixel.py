"""O cajado do Mago em pixel art (proposta; o jogo ainda usa o sprite 16×16 "cajado"). Pelo método do escudo e do
machado (pixel_comum.py), cada tamanho desenhado na própria grade.

O que o jogo diz (rpg/itens.py): o desenho "cajado" é o da base Cajado do Mago (a arma de Poder), em todos os
materiais, e o do único Cajado da Peste ("pertenceu a um curandeiro..."). O mesmo sprite é também o Atacar do Mago na
roda e o traço Conjurador dos inimigos: esses papéis não mudam (o item se acha só em Icones.ITEM). O desenho atual: um
cajado de madeira com uma pedra azul na ponta; a pedra azul é o que o faz ser o cajado do mago e fica.

O tipo: um cajado de caminhada de madeira escura, com a ponta aberta em garras que seguram um cristal azul lapidado,
a empunhadura de couro e a ponteira de ferro no pé. O cristal é pedra (facetas, reflexo de vidro), sem aura nem
brilho mágico em volta.

A construção, em cada tamanho (32, 40, 48 e 64 px):
  - a composição: na diagonal, do pé embaixo à esquerda até o cristal em cima à direita, como as outras armas; as
    medidas num sistema que gira com a haste (u ao longo dela, v para o lado da luz);
  - a madeira (carvalho escuro): um cilindro em faixas de 1 pixel na diagonal, o lado da luz mais claro; o veio e um
    nó em 48 e 64;
  - o encaixe (retornos do Jean: a pedra parecia solta, encostada na madeira; depois, a base azul passava do
    alojamento): a haste abre num alojamento que engole a parte de baixo da pedra; a borda da frente é uma faixa de
    madeira por cima da pedra, de lado a lado, acesa do lado da luz; as duas garras nascem na borda e sobem pelas faces;
    sombra de contato na pedra acima da borda e junto das garras;
  - o cristal: quatro facetas (a de cima à esquerda a mais clara, a de baixo à direita a mais escura), a aresta do
    meio acesa, um reflexo pequeno e duro na faceta da luz (a regra do vidro) e, embaixo, um degrau mais claro dentro
    da pedra (a luz que atravessa);
  - a empunhadura: couro enrolado no terço de baixo da haste (voltas em 48 e 64); a ponteira: ferro no pé;
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/arte/desenhar_cajado_pixel.py <pasta>    (grava noutra pasta: a proposta)
    python ferramentas/arte/desenhar_cajado_pixel.py            (grava em rpg/web/static/hud/icones/: só na integração)
"""

import math
import sys

import numpy as np

from pixel_comum import ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)

# As rampas, do mais escuro ao mais claro: o carvalho, o couro, o ferro da ponteira e o cristal azul.
CARVALHO = ["#150c07", "#27160c", "#3b2213", "#53311b", "#6c4225", "#875632", "#a26e44", "#bb8a5c"]
COURO = ["#120b0a", "#22140f", "#371f17", "#4d2c20", "#66402c"]
FERRO = ["#101114", "#22252b", "#3a3e46", "#5a606a", "#8c939d", "#c4cad2"]
CRISTAL = ["#0b1530", "#142553", "#1e3a7c", "#2a55a8", "#3d74cf", "#5f98e8", "#90bdf5", "#c8e0ff", "#f2f8ff"]

R2 = math.sqrt(2)
# As medidas de cada tamanho, em pixels, no sistema da haste: a origem (o pé, x0 e y0), a meia largura (hw), o fim da
# haste (L, onde ela se abre nas garras); o cristal: o centro (uc), a meia altura (h) e a meia largura (w); as garras:
# a espessura (g) e até onde sobem (g_ate, em fração da meia altura acima do centro do cristal); a taça (taca, onde fica
# a borda, em fração da meia altura abaixo do centro), a sombra dela na pedra (sombra), a altura da borda da frente
# (beira) e quanto ela passa da pedra de cada lado (folga); a empunhadura (de e ate, em fração de L);
# a ponteira (pont); `det` liga o veio, o nó e as voltas do couro (48 e 64).
MEDIDAS = {
    32: dict(x0=5.0, y0=29.5, hw=1.1, L=23.0, uc=27.6, h=6.2, w=3.9, g=1.0, g_ate=0.3, taca=0.62, sombra=1.1, beira=1.7, folga=0.4, de=0.18, ate=0.42, pont=1.6, det=0),
}
for _l, _extra in ((40, dict(x0=6.0, y0=37.5)), (48, dict(x0=7.0, y0=44.5, det=1)), (64, dict(x0=9.0, y0=59.5, det=2))):
    _e = _l / 32
    MEDIDAS[_l] = {k: (v * _e if k not in ("de", "ate", "det", "g_ate", "taca", "folga") else v) for k, v in MEDIDAS[32].items()} | _extra
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    dx, dy = x - M["x0"], y - M["y0"]
    u, v = (dx - dy) / R2, (-dx - dy) / R2   # u ao longo da haste (para a ponta), v para cima e para a esquerda
    hw, L, uc, h, w = M["hw"], M["L"], M["uc"], M["h"], M["w"]

    # ---- a haste: carvalho em faixas pela diagonal (o lado da luz mais claro)
    haste = (u >= -0.4) & (u <= L) & (np.abs(v) <= hw)
    tom_haste = np.select([v > 0.6 * hw, v > 0, v > -0.6 * hw], [5, 4, 3], 2)
    if M["det"]:
        veio = (np.abs(v - (-0.35 if M["det"] == 1 else 0.35)) < 0.1) & (np.sin(u * 0.85) + 0.6 * np.sin(u * 0.33 + 1) > 0.5)
        tom_haste = np.where(veio, tom_haste - 1, tom_haste)
        no = np.hypot(u - 0.62 * L, (v - 0.35) * 1.6) < 0.9 * lado / 32   # um nó, do lado da luz
        tom_haste = np.where(no, 2, tom_haste)
    mat[haste], tom[haste] = "m", tom_haste[haste]
    fixo[haste] = True
    # a empunhadura de couro e a ponteira de ferro
    pega = haste & (u > M["de"] * L) & (u < M["ate"] * L)
    tom_pega = np.select([v > 0.4 * hw, v > -0.4 * hw], [4, 3], 1)
    if M["det"]:
        tom_pega = np.where(np.floor(u / 2) % 2 == 0, tom_pega - 1, tom_pega)
    mat[pega], tom[pega] = "l", np.clip(tom_pega, 0, 4)[pega]
    ponteira = (u >= -0.6) & (u < M["pont"]) & (np.abs(v) <= hw + 0.3)
    mat[ponteira], tom[ponteira] = "f", np.select([v > 0.3, v > -0.5], [4, 3], 1)[ponteira]

    # ---- o cristal: um losango alongado ao longo da haste, em quatro facetas
    du = u - uc
    cristal = (np.abs(du) / h + np.abs(v) / w) <= 1
    cima, esq = du > 0, v > 0
    tom_cr = np.select([cima & esq, ~cima & esq, cima & ~esq], [6, 4, 3], 2)
    aresta = cristal & (np.abs(v) < 0.45)                          # a aresta do meio, acesa
    tom_cr = np.where(aresta, np.where(cima, 6, 4), tom_cr)
    dentro = cristal & ~cima & (np.abs(du) / h + np.abs(v) / w < 0.45) & ~aresta   # a luz que atravessa, embaixo
    tom_cr = np.where(dentro, tom_cr + 1, tom_cr)
    mat[cristal], tom[cristal] = "q", tom_cr[cristal]
    fixo[cristal] = True
    # o reflexo duro na faceta da luz: um grupo pequeno, desenhado
    bu, bv = uc + 0.42 * h, 0.4 * w
    bx = int(np.floor(M["x0"] + (bu - bv) / R2)); by_ = int(np.floor(M["y0"] - (bu + bv) / R2))
    for (ox, oy), t_ in ({(0, 0): 8, (1, 0): 7} if lado < 48 else {(0, 0): 8, (1, 0): 7, (0, 1): 7, (1, 1): 6}).items():
        if mat[by_ + oy, bx + ox] == "q":
            tom[by_ + oy, bx + ox] = t_

    # ---- o encaixe (retornos do Jean: a pedra parecia solta na madeira; depois, a base azul passava do alojamento):
    # a haste abre num alojamento que engole a parte de baixo da pedra; a borda da frente é uma faixa de madeira por
    # cima da pedra, de lado a lado (a pedra entra atrás dela); as duas garras nascem na borda e sobem pelas faces;
    # sombra de contato na pedra logo acima da borda e junto de cada garra
    borda = w * np.clip(1 - np.abs(u - uc) / h, 0, 1)              # a meia largura da pedra naquela altura
    ut0, ut1 = L - 0.8, uc - M["taca"] * h                         # do pé do alojamento até a borda
    tt = np.clip((u - ut0) / (ut1 - ut0), 0, 1)
    boca = max(w * M["taca"] + 0.35, w * (1 - M["taca"]) + M["folga"])   # a borda é sempre mais larga que a pedra ali
    larg_taca = hw + (boca - hw) * np.sin(tt * np.pi / 2)
    taca = (u >= ut0) & (u <= ut1) & (np.abs(v) <= larg_taca)
    taca |= (mat == "q") & (u < ut1)                               # a parte de baixo da pedra fica toda dentro
    mat[taca], tom[taca] = "m", np.select([v > 0.35 * larg_taca, v > -0.35 * larg_taca], [5, 4], 2)[taca]
    # a borda da frente, por cima da pedra: acompanha a largura do alojamento (ou a da pedra, um pouco mais)
    beira = (u > ut1 - M["beira"]) & (u <= ut1 + 0.25) & (np.abs(v) <= np.maximum(larg_taca, borda + M["folga"]))
    mat[beira], tom[beira] = "m", np.where(v[beira] > 0.3 * boca, 6, np.where(v[beira] > -0.3 * boca, 5, 3))
    fixo[taca | beira] = True
    sombra = (mat == "q") & (u > ut1) & (u < ut1 + M["sombra"])   # a sombra de contato acima da borda
    tom[sombra] = np.maximum(1, tom[sombra] - 2)
    ug1 = uc + M["g_ate"] * h
    centro_g = np.maximum(borda - M["g"] * 0.5, 0)                 # as garras correm sobre a face, junto da aresta
    garra = (u > ut1) & (u <= ug1) & (np.abs(np.abs(v) - centro_g) <= M["g"] / 2) & (np.abs(v) <= borda + 0.1)
    ponta = garra & (u > ug1 - 1.0)
    mat[garra], tom[garra] = "m", np.where(v[garra] > 0, 6, 3)
    tom[ponta] = np.where(v[ponta] > 0, 7, 4)
    fixo[garra] = True
    junto = (mat == "q") & (np.abs(np.abs(v) - (centro_g - M["g"])) <= 0.5) & (u > ut1) & (u <= ug1)   # a sombra das garras
    tom[junto] = np.maximum(1, tom[junto] - 1)

    # os furos: um pixel vazio preso entre a garra e o alojamento (três vizinhos cheios) vira madeira, senão o contorno
    # fazia um ponto escuro e um degrau na silhueta
    for _ in range(2):
        cheio = mat != ""
        viz = sum(np.roll(np.roll(cheio, oy, 0), ox, 1).astype(int) for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        furo = ~cheio & (viz >= 3) & (u > L - 2)
        mat[furo], tom[furo] = "m", 4

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"m": CARVALHO, "l": COURO, "f": FERRO, "q": CRISTAL})


if __name__ == "__main__":
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"cajado-{lado}: {salvar(desenhar(lado), saida, 'cajado')} cores")
