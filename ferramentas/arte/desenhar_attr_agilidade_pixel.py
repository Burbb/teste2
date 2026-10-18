"""O ícone de Agilidade (`attr-agilidade`): proposta, nada no jogo. O atual é um placeholder pintado; a proposta chapada
de 18/10/2026 (`desenhar_atributos_pixel.py`, a bota do conjunto de perfil, parada) foi recusada.

O objeto: uma bota de couro em pleno passo, com pose própria (não é a bota do equipamento): inclinada para a frente,
o calcanhar no ar e a ponta indo para a direita, e três rastros de velocidade atrás, curvos, claros junto da bota e
apagando para trás. Volume pela luz da família (pixel_comum.LUZ):
  - o cano como um cilindro (aceso à esquerda, escuro na beira da direita), a dobra de camurça em cima, mais clara;
  - o peito do pé aceso em cima, a ponta arredondada com um brilho; a tira do tornozelo com a fivela de latão;
  - a sola escura com a quina de cima acesa e o salto.
Os papéis: a ficha e o Inventário (24), o selo da festa de atributo permanente (64, o 32 ampliado 2×) e o comando
Fugir da luta (32: `ACAO.fuga` em icones.js usa este desenho).

    python ferramentas/arte/desenhar_attr_agilidade_pixel.py <pasta> [--listas]
"""

import math
import sys

import numpy as np
from PIL import Image

import pixel_comum as pc

COURO = ["#1C120C", "#2E1E13", "#45301E", "#604229", "#7C5634", "#986C42", "#B48752", "#CFA36C"]
CAMURCA = ["#4A3524", "#6E5236", "#957250", "#B8946A", "#D6B88C"]
SOLA = ["#0E0A08", "#211A14", "#352A20", "#4C3E30"]
LATAO = ["#5A3C12", "#9C6E22", "#DDB45C"]
RASTRO = ["#5C5446", "#9C907A", "#D8CCB0", "#F6EEDA"]
RAMPAS = {"k": COURO, "d": CAMURCA, "s": SOLA, "l": LATAO, "r": RASTRO}

NOME = "attr-agilidade"
CAMADAS = ["rastros", "sola", "bota", "dobra", "tira", "contorno"]

# as medidas em unidades do 24; a bota no sistema dela (u para a frente, v para baixo), girada por GIRO em volta do
# tornozelo (o centro da tira)
M = {
    "tornozelo": (12.6, 11.2), "giro": -24.0,   # negativo: o cano inclina para a frente, a ponta desce (o impulso)
    "cano": (-3.0, 2.3, -8.6, 0.0),        # u0, u1, v0, v1
    "dobra": (-3.5, 2.8, -10.2, -7.6),
    "pe": (-3.3, 8.6, -0.6, 4.2),           # do calcanhar à ponta, do peito à sola
    "sola": (4.2, 5.6),                     # o fundo da sola (v; sv1 é a borda de baixo)
    "bico": 2.6,                            # o raio da ponta arredondada (u)
    "peito": 0.42,                          # quanto o peito do pé desce por unidade, do cano à ponta
    "salto": (-3.3, -0.6),                  # o salto (u), mais alto
    "tira": (-2.0, -0.9),                   # a tira (v)
    # os rastros: (y no 24, x do começo junto da bota, comprimento, curva)
    "rastros": ((6.4, 8.2, 6.2, 0.5), (10.6, 7.2, 5.6, 0.4), (14.8, 6.8, 4.6, 0.3)),
}


def desenhar(lado, partes=False):
    """A imagem do tamanho; com partes=True, também a camada de cada pixel (CAMADAS)."""
    s = lado / 24
    mat, tom, fixo, x, y = pc.grade(lado)
    X, Y = x / s, y / s
    px = 1 / s
    tx, ty = M["tornozelo"]
    g = math.radians(M["giro"])
    # do quadro para o sistema da bota (girado para a frente: o cano inclina para a direita)
    u = (X - tx) * math.cos(g) - (Y - ty) * math.sin(g)
    v = (X - tx) * math.sin(g) + (Y - ty) * math.cos(g)

    # os rastros de velocidade, atrás (embaixo de tudo): traços de 1 px que curvam um pouco para cima ao se afastar,
    # claros junto da bota, apagando para trás
    for (ry, rx0, comp, curva) in M["rastros"]:
        dist = rx0 - X                                   # para trás, a partir da ponta junto da bota
        yc = ry - curva * (dist / comp) ** 2 * 2
        traco = (dist >= 0) & (dist <= comp) & (np.abs(Y - yc) <= 0.5 * px + 0.05)
        mat[traco] = "r"
        tom[traco] = np.clip(3 - np.floor(dist / comp * 3.2), 0, 3).astype(int)[traco]
        fixo[traco] = True

    # o pé e a sola numa forma só, com o bico arredondado (a frente é meia elipse, o fundo sobe um pouco na ponta: o
    # arrebite); a sola é a faixa de baixo dessa forma, então acompanha a curva até a ponta. Antes o pé e a sola eram
    # retângulos cortados por arcos diferentes, e o giro deixava a ponta com um corte reto.
    pu0, pu1, pv0, pv1 = M["pe"]
    sv0, sv1 = M["sola"]
    rx = M["bico"]
    cu1_ = M["cano"][1]
    # o peito do pé desce do tornozelo até a ponta (a bota afina para o bico)
    topo = lambda uu: pv0 + M["peito"] * np.clip(uu - cu1_, 0, None)
    v_topo_bico = pv0 + M["peito"] * max(0.0, pu1 - rx - cu1_)
    vc, ry = (v_topo_bico + sv1) / 2, (sv1 - v_topo_bico) / 2

    def forma_pe(uu, vv):
        frente = uu > pu1 - rx
        arrebite = 0.55 * np.clip((uu - (pu1 - rx)) / rx, 0, 1) ** 2      # o fundo sobe junto da ponta
        corpo_ = (uu >= pu0) & (vv >= topo(uu)) & (vv < sv1 - arrebite)
        bico = ((uu - (pu1 - rx)) / rx) ** 2 + ((vv - vc) / ry) ** 2 <= 1
        return corpo_ & (~frente | bico)

    pe_todo = forma_pe(u, v)
    hu0, hu1 = M["salto"]
    salto = (u >= hu0) & (u < hu1) & (v >= sv1 - 0.2) & (v < sv1 + 0.9)
    # a sola: o que está a menos de 1,4 da borda de baixo da forma (o ponto 1,4 abaixo já sai dela)
    sola_t = (pe_todo & ~forma_pe(u, v + 1.4)) | salto
    mat[sola_t] = "s"
    tom[sola_t] = 1
    tom[sola_t & forma_pe(u, v - 0.75) & ~forma_pe(u, v - 0.75 + 1.4) & ~salto] = 2   # a quina de cima, um degrau acima

    # o pé: o resto da forma, em couro; o peito aceso em cima, o resto pela luz
    pe = pe_todo & ~sola_t
    # o cano
    cu0, cu1, cv0, cv1 = M["cano"]
    cano = (u >= cu0) & (u < cu1) & (v >= cv0) & (v < cv1 + 0.5)
    bota = pe | cano
    mat[bota] = "k"
    pc_ = (u - cu0) / (cu1 - cu0)                       # de través no cano: 0 à esquerda (luz), 1 à direita
    t_cano = np.where(pc_ < 0.3, 5, np.where(pc_ < 0.7, 4, 3))
    prof = v - topo(u)                                     # a distância até o peito (aceso em cima, escuro embaixo)
    t_pe = np.where(prof < 1.0, 5, np.where(prof < 2.6, 4, 3))
    tom[bota] = np.where(cano & (v < cv1 - 0.4), t_cano, t_pe)[bota]
    # a beira da direita do cano e a parte de trás do calcanhar, na sombra
    beira = cano & (u >= cu1 - 0.9)
    tom[beira] = 3
    # o brilho na ponta: o couro mais polido onde a luz bate
    brilho = pe & (((u - (pu1 - rx)) ** 2 + (v - (v_topo_bico + 0.7)) ** 2) <= 0.95 ** 2)   # no alto do bico
    tom[brilho] = 6
    fixo[brilho] = True

    # a dobra de camurça no alto do cano, mais clara, um pouco mais larga que o cano
    du0, du1, dv0, dv1 = M["dobra"]
    dobra = (u >= du0) & (u < du1) & (v >= dv0) & (v < dv1)
    mat[dobra] = "d"
    tom[dobra] = np.where(v < dv0 + 0.9, 3, np.where((u - du0) / (du1 - du0) < 0.6, 2, 1))[dobra]
    # a sombra que a dobra faz no cano
    sob = cano & ~dobra & (v >= dv1) & (v < dv1 + 0.8)
    tom[sob] = 3

    # a tira do tornozelo com a fivela de latão (do lado da luz)
    ta0, ta1 = M["tira"]
    tira = cano & (v >= ta0) & (v < ta1)
    tom[tira] = 2
    fivela = (np.abs(u - (cu0 + 1.4)) < 0.8) & (v >= ta0 - 0.3) & (v < ta1 + 0.3)
    mat[fivela] = "l"
    tom[fivela] = np.where(v < (ta0 + ta1) / 2, 2, 1)[fivela]
    fixo[tira | fivela] = True

    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    img = pc.imagem(mat, tom, RAMPAS)
    if not partes:
        return img
    camada = np.full(mat.shape, "", dtype=object)
    for m, c in (("r", "rastros"), ("s", "sola"), ("k", "bota"), ("d", "dobra"), ("l", "tira"), ("c", "contorno")):
        camada[mat == m] = c
    camada[tira & (mat == "k")] = "tira"
    return img, camada


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    print(24, pc.salvar(desenhar(24), pasta, NOME), "cores")
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, NOME), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, NOME), "cores (o 32 ampliado 2×)")
    if "--listas" in sys.argv:
        for lado in (24, 32):
            print("listas", pc.listas_camadas(desenhar(lado, partes=True), pasta / "listas" / f"{NOME}-{lado}", CAMADAS))


if __name__ == "__main__":
    main()
