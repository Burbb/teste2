"""A aljava (o equipamento secundário do Patrulheiro e o ícone das flechas no topo) no método da família: proposta,
nada no jogo.

Hoje é a peça pintada da família de ferro. O desenho novo segue o conjunto de couro aprovado (o gibão, as botas, o
capuz e a luva): as mesmas rampas de couro (`couro_r2.py`), a luz em faixas chapadas pela direção da superfície, as
cintas como bordas escuras e o contorno comum.

O objeto: um tubo de couro em pé, inclinado 22° para a direita (como se carrega nas costas; a 45° ele deitava e
ocupava pouco do quadro), a boca com a borda de couro escuro
acesa em cima, duas cintas costuradas, o fundo arredondado mais escuro e uma alça de couro em arco do lado da sombra;
saindo da boca, três flechas com a pena para cima (como se guardam), a haste de madeira e as penas claras, uma delas
mais escura. Sem fivela grande, tachas ou brilho: o jogo só diz "Aljava".

Medidas no sistema do tubo: `a` ao longo dele (do fundo para a boca), `w` de través (negativo do lado da luz). O 32 é a arte principal; o 64 é o 32 ampliado 2× (como no couro); o 24 (o topo, onde ela também fica parada)
sai das mesmas medidas na grade dele. 40 e 48 depois da aprovação do 32.

    python ferramentas/arte/desenhar_aljava_pixel.py <pasta> [--intermediarios]
"""

import math
import sys

import numpy as np
from PIL import Image

import pixel_comum as pc

COURO = ["#1C120C", "#2E1E13", "#45301E", "#604229", "#7C5634", "#986C42", "#B48752"]
BORDA = ["#140C08", "#22150D", "#321F13", "#45301E"]
MADEIRA = ["#3A2A1C", "#6A5038", "#9C7E58", "#C4A57A"]   # a haste: clara, para ler contra o contorno
PENA = ["#4A4640", "#7C766C", "#B4AE9E", "#E2DCCB"]
PENA_ESCURA = ["#3A2E28", "#5E4A3E", "#86705E"]     # a pena escura (parda), clara o bastante para o carvão
RAMPAS = {"k": COURO, "b": BORDA, "m": MADEIRA, "p": PENA, "q": PENA_ESCURA}

# a origem (o centro do fundo do tubo), a inclinação e as medidas, em unidades do 32
MEDIDAS = {
    "fundo": (10.5, 27.4),         # o centro do fundo do tubo (o fundo não encosta na borda: o contorno cabe)
    "inclina": 22.0,               # graus a partir da vertical, para a direita
    "tubo": 15.5,                  # o comprimento do tubo (a)
    "larg": (3.1, 3.8),            # a meia-largura no fundo e na boca (w)
    "boca": 1.6,                   # a borda da boca (a)
    "cintas": ((3.8, 5.0), (10.2, 11.4)),
    "fundo_borda": 1.8,            # o fundo arredondado, mais escuro
    # as flechas: (desvio de w na boca, inclinação em graus a partir do eixo, comprimento além da boca, pena escura?)
    # (a haste fica à vista entre a boca e a pena, como na aljava pintada original: o pedido do Jean)
    "flechas": ((-2.0, -16.0, 11.0, False), (0.4, -2.0, 12.6, False), (2.6, 13.0, 10.4, True)),
    "pena": 4.4,                   # o comprimento da pena (a partir da ponta de cima)
    "alca": (3.0, 12.6, 3.0),      # a alça: de a=3 até a=12,6, saindo até w = meia-largura + 3
    "claro": 0,                    # degraus a mais na rampa do couro (o 24 do topo fica um degrau mais claro)
}
# O 24 (o ícone das flechas no topo, onde ela fica parada pequena) tem simplificações próprias do mesmo objeto: o tubo
# mais largo e mais inclinado, ocupando o quadro; o couro um degrau mais claro; sem a alça (a 24 ela virava um risco
# escuro solto); a boca e as cintas com a borda de cima acesa; duas cintas viram uma; as penas em blocos.
PERFIL = {
    24: {"fundo": (10.0, 26.4), "inclina": 28.0, "tubo": 14.0, "larg": (4.4, 5.0), "boca": 2.4,
         "cintas": ((6.6, 8.6),), "fundo_borda": 2.4, "alca": None, "claro": 1, "pena": 4.8,
         "flechas": ((-2.6, -16.0, 8.8, False), (0.6, -1.0, 10.0, False), (3.4, 14.0, 8.4, True))},
}


def desenhar(lado):
    M = {**MEDIDAS, **PERFIL.get(lado, {})}
    s = lado / 32
    mat, tom, fixo, x, y = pc.grade(lado)
    X, Y = x / s, y / s                          # o centro do pixel em unidades do 32
    x0, y0 = M["fundo"]
    th = math.radians(M["inclina"])
    a = (X - x0) * math.sin(th) - (Y - y0) * math.cos(th)    # ao longo do tubo (para cima, inclinado à direita)
    w = (X - x0) * math.cos(th) + (Y - y0) * math.sin(th)    # de través (negativo: à esquerda, o lado da luz)
    L = M["tubo"]
    meia = M["larg"][0] + (M["larg"][1] - M["larg"][0]) * np.clip(a / L, 0, 1)

    # as flechas primeiro (o tubo fica por cima do que estiver dentro dele)
    px = 1.0 / s
    for (dw, ang, comp, escura) in M["flechas"]:
        th = math.radians(ang)
        ca, sa = math.cos(th), math.sin(th)
        # a reta da flecha no sistema (a, w): começa em (L - 1, dw) e segue a direção girada
        da, dw_ = a - (L - 1), w - dw
        t = da * ca + dw_ * sa                    # ao longo da flecha
        d = -da * sa + dw_ * ca                   # distância de través
        haste = (t >= 0) & (t <= comp) & (np.abs(d) <= 0.5 * max(px, 0.75))
        mat[haste] = "m"
        tom[haste] = np.where(d[haste] < 0, 3, 2)
        fixo[haste] = True
        pena0 = comp - M["pena"]
        larg_pena = np.clip((t - pena0) / M["pena"], 0, 1) * 0.7 + 1.0   # a pena quase reta, ~2 px: um bloco claro
        pena = (t >= pena0) & (t <= comp) & (np.abs(d) <= larg_pena)
        mat[pena] = "q" if escura else "p"
        r = PENA_ESCURA if escura else PENA
        tt = np.where(d < -0.3, len(r) - 1, np.where(d < 0.5, len(r) - 2, len(r) - 3))
        tom[pena] = tt[pena]
        # a nervura da pena: a haste continua por dentro, um tom abaixo
        nerv = pena & (np.abs(d) <= 0.5 * max(px, 0.75))
        mat[nerv] = "m"
        tom[nerv] = 2

    # o tubo
    tubo = (a >= 0) & (a <= L) & (np.abs(w) <= meia)
    # o fundo arredondado: um semicírculo abaixo de a = 0
    fundo = (a < 0) & (a * a + w * w <= M["larg"][0] ** 2)
    corpo = tubo | fundo
    mat[corpo] = "k"
    p = w / meia
    k = M["claro"]
    tom[corpo] = np.where(p < -0.45, 5 + k, np.where(p < 0.15, 4 + k, np.where(p < 0.6, 3 + k, 2 + k)))[corpo]
    borda_fundo = corpo & (a < M["fundo_borda"])
    mat[borda_fundo] = "b"
    tom[borda_fundo] = np.where(p < 0, 2, 1)[borda_fundo]
    for (c0, c1) in M["cintas"]:
        cinta = corpo & (a >= c0) & (a < c1)
        mat[cinta] = "b"
        tom[cinta] = np.where(p < -0.3, 3, np.where(p < 0.4, 2, 1))[cinta]
        if k:   # a borda de cima da cinta acesa: o couro do lado da luz (mostra que a cinta é uma tira por cima)
            topo_c = cinta & (a >= c1 - 1 / s) & (p < 0.2)
            mat[topo_c], tom[topo_c] = "k", 4
    # a boca: a borda (acesa do lado da luz) e o escuro de dentro na ponta
    boca = (a > L - M["boca"]) & (a <= L) & (np.abs(w) <= meia)
    mat[boca] = "b"
    tom[boca] = np.where(p < 0, 3, 2)[boca]
    if k:   # a borda da boca acesa no lado da luz (o couro dobrado), o resto na sombra
        aro = boca & (a > L - 1 / s) & (p < 0.3)
        mat[aro], tom[aro] = "k", 5

    # a alça: um arco de couro escuro do lado da sombra, fora do tubo
    if M["alca"] is None:
        tom = pc.limpar(mat, tom, fixo)
        pc.contornar(mat)
        return pc.imagem(mat, tom, RAMPAS)
    a0, a1, sai = M["alca"]
    meio = (a0 + a1) / 2
    k = np.clip(1 - ((a - meio) / ((a1 - a0) / 2)) ** 2, 0, 1)
    w_alca = meia + 0.2 + sai * k
    alca = (a >= a0) & (a <= a1) & (np.abs(w - w_alca) <= 0.5 * max(px, 0.8)) & (mat == "")
    mat[alca] = "b"
    tom[alca] = 2
    fixo[alca] = True

    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, "aljava"), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, "aljava"), "cores (o 32 ampliado 2×)")
    print(24, pc.salvar(desenhar(24), pasta, "aljava"), "cores (o topo)")
    if "--intermediarios" in sys.argv:
        for lado in (40, 48):
            print(lado, pc.salvar(desenhar(lado), pasta, "aljava"), "cores (prévia)")


if __name__ == "__main__":
    main()
