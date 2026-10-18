"""O ícone de Defesa (`attr-defesa`): proposta, nada no jogo. Os ícones atuais de atributo são placeholders pintados;
a proposta chapada de 18/10/2026 (`desenhar_atributos_pixel.py`, o escudo em duas metades lisas) foi recusada por ter
perdido volume e material.

O objeto: um escudo de bico (o de cavaleiro) de frente, abaulado, com volume pela luz da família (pixel_comum.LUZ):
  - a face de aço é uma superfície curva (mais funda nas laterais e embaixo); o tom de cada pixel sai da normal dela
    contra a luz, em faixas da rampa: o lado de cima à esquerda acende, o da direita vira para a sombra; um reflexo
    largo e curto em cima à esquerda, onde a luz bate de frente;
  - a borda de latão é chanfrada: a quina de fora acesa no lado da luz, a de dentro com uma linha de sombra sobre o
    aço (a borda fica por cima da face);
  - a bossa no centro, uma cúpula de latão com o brilho dela, segura a pega por trás.
Não copia o escudo redondo do equipamento: é o símbolo da Defesa, no formato que já se lê como proteção.

Os tamanhos: o 24 é o mais visto (a ficha e o Inventário) e é desenhado na própria grade; o 32 é desenhado também e é
a fonte do 64 (o selo da festa de atributo permanente), que é o 32 ampliado 2×.

    python ferramentas/arte/desenhar_attr_defesa_pixel.py <pasta>
"""

import sys

import numpy as np
from PIL import Image

import pixel_comum as pc

ACO = ["#1A1E25", "#2C333D", "#434C58", "#5D6774", "#7B8693", "#9DA8B4", "#C2CBD4", "#E6ECF0"]
LATAO = ["#2E1E08", "#5C3C12", "#8C621E", "#B98A34", "#DDB45C", "#F6DC96"]
RAMPAS = {"a": ACO, "l": LATAO}

# as medidas em unidades do 24
M = {
    "cx": 12.0, "topo": 1.6, "reto": 9.0, "bico": 22.6, "meia": 9.0,   # a silhueta: reta até `reto`, curva até o bico
    "borda": 1.25,                                                        # a largura da borda de latão
    "bossa": (12.0, 10.4, 2.35),                                          # o centro e o raio da bossa
}


def _meia_largura(Y, meia, reto, bico):
    t = np.clip((Y - reto) / (bico - reto), 0, 1)
    return meia * np.sqrt(np.clip(1 - t ** 1.8, 0, 1))


def desenhar(lado):
    s = lado / 24
    mat, tom, fixo, x, y = pc.grade(lado)
    X, Y = x / s, y / s
    px = 1 / s
    cx, topo, reto, bico, meia = M["cx"], M["topo"], M["reto"], M["bico"], M["meia"]

    larg = _meia_largura(Y, meia, reto, bico)
    # o topo levemente convexo: as quinas um pouco mais baixas que o meio
    topo_y = topo + 0.6 * np.clip(np.abs(X - cx) / meia, 0, 1) ** 2
    forma = (Y >= topo_y) & (Y <= bico) & (np.abs(X - cx) <= larg)
    b = M["borda"]
    larg_in = _meia_largura(Y, meia - b, reto, bico - b * 1.5)
    face = forma & (Y >= topo_y + b) & (Y <= bico - b * 1.5) & (np.abs(X - cx) <= larg_in)
    borda = forma & ~face

    # a face de aço: a normal de uma superfície abaulada. u de -1 (esquerda) a 1 (direita); v de -1 (topo) a 1 (bico).
    u = (X - cx) / np.maximum(larg_in, 0.6)
    v = (Y - (topo + bico) / 2) / ((bico - topo) / 2)
    nx, ny = 0.85 * u, 0.45 * v                       # a inclinação da superfície em cada direção
    nz = np.sqrt(np.clip(1 - nx * nx - ny * ny, 0.05, 1))
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    luz = (nx * pc.LUZ[0] + ny * pc.LUZ[1] + nz * pc.LUZ[2]) / n
    mat[face] = "a"
    # em faixas largas da rampa (2 a 6), pela luz
    tf = np.clip(np.round(1.0 + (luz - 0.15) * 7.2), 1, 6).astype(int)
    tom[face] = tf[face]
    # o reflexo: uma mancha larga e curta em cima à esquerda, onde a normal aponta para a luz
    refl = face & (luz > np.percentile(luz[face], 93))
    tom[refl] = 7
    fixo[refl] = True

    # a borda de latão, chanfrada: acesa por fora do lado da luz, escura do lado da sombra
    mat[borda] = "l"
    lado_luz = ((X - cx) * -0.6 + (Y - 10) * -0.8)     # positivo em cima à esquerda
    tb = np.where(lado_luz > 2.5, 3, np.where(lado_luz > -2.5, 2, 1))
    tom[borda] = tb[borda]
    # a quina de fora: a fileira de fora da borda do lado da luz um tom acima
    fora = borda & ~(np.roll(forma, 1, 0) & np.roll(forma, 1, 1) & np.roll(forma, -1, 0) & np.roll(forma, -1, 1))
    tom[fora & (lado_luz > 0)] = 4
    tom[fora & (lado_luz < -4)] = 1
    fixo[borda] = True
    # a sombra da borda sobre a face: a primeira fileira do aço junto da borda, do lado da luz (em cima e à esquerda)
    junto = face & (np.roll(borda, 1, 0) | np.roll(borda, 1, 1)) & (lado_luz > -1)
    tom[junto] = np.maximum(tom[junto] - 2, 1)
    fixo[junto] = True

    # a bossa: uma cúpula de latão pela luz, com o ponto de brilho
    bx, by, br = M["bossa"]
    dx, dy = (X - bx) / br, (Y - by) / br
    bossa = dx * dx + dy * dy <= 1
    dz = np.sqrt(np.clip(1 - dx * dx - dy * dy, 0, 1))
    lb = dx * pc.LUZ[0] + dy * pc.LUZ[1] + dz * pc.LUZ[2]
    mat[bossa] = "l"
    tom[bossa] = np.clip(np.round(1.2 + lb * 3.4), 1, 4).astype(int)[bossa]
    fixo[bossa] = True
    idx = np.argmax(np.where(bossa, lb, -9))
    yy, xx = np.unravel_index(idx, lb.shape)
    tom[yy, xx] = 5
    # a sombra da bossa sobre o aço, embaixo à direita
    sombra = face & ~bossa & ((X - bx - 0.7 * px) ** 2 + (Y - by - 0.7 * px) ** 2 <= (br + 0.6 * px) ** 2)
    tom[sombra] = np.maximum(tom[sombra] - 2, 1)
    fixo[sombra] = True

    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    print(24, pc.salvar(desenhar(24), pasta, "attr-defesa"), "cores")
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, "attr-defesa"), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, "attr-defesa"), "cores (o 32 ampliado 2×)")


if __name__ == "__main__":
    main()
