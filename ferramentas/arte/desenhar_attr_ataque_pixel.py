"""O ícone de Ataque (`attr-ataque`): proposta, nada no jogo. Os ícones atuais de atributo são placeholders pintados;
a proposta chapada de 18/10/2026 (`desenhar_atributos_pixel.py`) foi recusada por ter perdido volume e material.

O objeto: uma espada de lâmina larga na diagonal (o pomo embaixo à esquerda, a ponta em cima à direita), com volume
pela luz da família (pixel_comum.LUZ, de cima e da esquerda):
  - a lâmina de aço em dois planos (o bisel): a face voltada para a luz clara, a outra escura, a aresta do meio entre
    elas; o fio da face acesa num tom mais claro e um brilho especular na metade de baixo da lâmina;
  - a guarda de latão como um cilindro de través: a borda de cima acesa, a de baixo na sombra, as pontas arredondadas;
  - a empunhadura de couro enrolada em faixas inclinadas, de dois tons;
  - o pomo de latão como uma esfera, com o ponto de brilho.
Não copia a espada do equipamento: é um símbolo, com a lâmina mais larga e a guarda maior, para ler no 24.

Os tamanhos: o 24 é o mais visto (a ficha e o Inventário) e é desenhado na própria grade; o 32 é desenhado também e é
a fonte do 64 (o selo da festa de atributo permanente), que é o 32 ampliado 2×.

    python ferramentas/arte/desenhar_attr_ataque_pixel.py <pasta>
"""

import math
import sys

import numpy as np
from PIL import Image

import pixel_comum as pc

ACO = ["#1E2229", "#343B45", "#4E5764", "#6B7684", "#8E99A6", "#B6BFC9", "#DCE2E8", "#FFFFFF"]
LATAO = ["#3A2608", "#6A4614", "#9C6E22", "#C99A3A", "#E8C468", "#FFF0B0"]
COURO = ["#1C120C", "#3A2416", "#5A3A22", "#7C5634", "#986C42"]
RAMPAS = {"a": ACO, "l": LATAO, "k": COURO}
R2 = math.sqrt(2)

# as medidas em unidades do 24 (cada tamanho as lê na própria grade): a origem é o centro do pomo
M = {
    "pomo": (3.0, 21.0), "pomo_r": 1.65,
    "cabo": (1.4, 5.6, 0.95),           # a empunhadura: de a=1,4 a 5,6, meia-largura 0,95
    "guarda": (5.6, 7.1, 4.4),          # a guarda: de a=5,6 a 7,1, meia-largura de través 4,4
    "lamina": (7.1, 26.4, 2.05, 20.6),  # a lâmina: de a=7,1 até a ponta em 26,4, meia-largura 2,05, afina a partir de 20,6
}


def desenhar(lado):
    s = lado / 24
    mat, tom, fixo, x, y = pc.grade(lado)
    X, Y = x / s, y / s
    px = 1 / s
    x0, y0 = M["pomo"]
    a = ((X - x0) - (Y - y0)) / R2          # ao longo da espada (para cima e à direita)
    w = ((X - x0) + (Y - y0)) / R2          # de través (negativo: em cima à esquerda, o lado da luz)

    # a lâmina: dois planos pelo bisel; a meia-largura afina no último trecho até a ponta
    a0, a1, meia0, afina = M["lamina"]
    meia = np.where(a < afina, meia0, meia0 * np.clip((a1 - a) / (a1 - afina), 0, 1))
    lamina = (a >= a0) & (a <= a1) & (np.abs(w) <= np.maximum(meia, 0.4 * px))
    mat[lamina] = "a"
    r = w / np.maximum(meia, 0.5)           # -1 no fio da luz, 0 na aresta, 1 no fio da sombra
    # a face da luz em duas faixas (o fio mais claro), a da sombra em duas; perto da guarda a luz cai um pouco
    face = np.where(r < -0.62, 6, np.where(r < -0.08, 5, np.where(r < 0.5, 3, 2)))
    face = face - (a < a0 + 2.2) * 1
    tom[lamina] = face[lamina]
    # a aresta do meio: a linha clara entre os planos (a quina pega a luz), até perto da ponta
    aresta = lamina & (np.abs(w) < 0.5 * px) & (a < a1 - 1.5)
    tom[aresta] = 4
    fixo[aresta] = True
    # o brilho especular: uma mancha curta na face da luz, na metade de baixo da lâmina
    brilho = lamina & (a > a0 + 3.4) & (a < a0 + 7.6) & (r < -0.25) & (r > -0.95)
    tom[brilho] = 7
    fixo[brilho] = True

    # a guarda: um cilindro de través, de latão, com as pontas arredondadas
    g0, g1, gm = M["guarda"]
    meio_g = (g0 + g1) / 2
    guarda = (np.abs(a - meio_g) <= (g1 - g0) / 2) & (np.abs(w) <= gm)
    pontas = ((a - meio_g) ** 2 + (np.abs(w) - gm) ** 2 <= ((g1 - g0) / 2 + 0.35) ** 2)
    guarda = guarda | pontas
    mat[guarda] = "l"
    lado_g = (a - meio_g) / ((g1 - g0) / 2 + 0.35)       # -1 embaixo (o lado do cabo), 1 em cima (o lado da lâmina)
    tg = np.where(lado_g > 0.25, 4, np.where(lado_g > -0.35, 3, 2))
    tg = tg + (w < -gm * 0.55) * 1 - (w > gm * 0.55) * 1  # a ponta da luz um tom acima, a da sombra um abaixo
    tom[guarda] = np.clip(tg, 1, 5)[guarda]

    # a empunhadura: o couro enrolado em faixas inclinadas de dois tons
    c0, c1, cm = M["cabo"]
    cabo = (a >= c0) & (a < c1) & (np.abs(w) <= cm)
    mat[cabo] = "k"
    faixa = np.floor((a - c0 + 0.6 * w) / max(1.2, 1.2 * px)).astype(int) % 2
    tom[cabo] = np.where(faixa == 0, np.where(w < 0, 4, 3), np.where(w < 0, 2, 1))[cabo]
    fixo[cabo] = True

    # o pomo: uma esfera de latão, pela luz da família
    pr = M["pomo_r"]
    dx, dy = (X - x0) / pr, (Y - y0) / pr
    pomo = dx * dx + dy * dy <= 1
    dz = np.sqrt(np.clip(1 - dx * dx - dy * dy, 0, 1))
    luz = dx * pc.LUZ[0] + dy * pc.LUZ[1] + dz * pc.LUZ[2]
    mat[pomo] = "l"
    tom[pomo] = np.clip(np.round(1 + luz * 3.6), 1, 4).astype(int)[pomo]
    # o ponto de brilho: o pixel do pomo mais perto da luz
    idx = np.argmax(np.where(pomo, luz, -9))
    by, bx = np.unravel_index(idx, luz.shape)
    tom[by, bx], fixo[by, bx] = 5, True

    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    print(24, pc.salvar(desenhar(24), pasta, "attr-ataque"), "cores")
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, "attr-ataque"), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, "attr-ataque"), "cores (o 32 ampliado 2×)")


if __name__ == "__main__":
    main()
