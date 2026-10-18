"""Os ícones dos quatro atributos (Ataque, Defesa, Agilidade, Poder) no método da família: proposta, nada no jogo.

Hoje são peças pintadas da família de ferro (`attr-*-24` e `-32`). Ficam os conceitos que já se leem (a espada, o
escudo, a bota com os riscos de movimento, a chama roxa), redesenhados na grade, como o escudo, o machado e o
conjunto de couro: rampas por material, luz de cima e da esquerda em faixas, contorno comum.

Os lugares: a ficha e o Inventário em 24 (o mais visto); o comando Fugir da luta usa a bota da Agilidade em 32
(`ACAO.fuga` em icones.js: o mesmo desenho em outro papel; trocar a bota troca os dois). Os dois tamanhos são
desenhados nas mesmas medidas (em unidades do 24), cada um na sua grade.

    python ferramentas/arte/desenhar_atributos_pixel.py <pasta>
"""

import math
import sys

import numpy as np

import pixel_comum as pc

ACO = ["#23272E", "#3A414B", "#58616D", "#7C8693", "#A3ADB8", "#CBD3DA", "#EEF2F4"]
LATAO = ["#3A2A10", "#6B4E1C", "#9C7630", "#C9A14A", "#E8C878"]
COURO = ["#1C120C", "#2E1E13", "#45301E", "#604229", "#7C5634", "#986C42", "#B48752"]   # o conjunto de couro
BOTA = ["#1A110B", "#2A1A10", "#3E2716", "#57381F", "#724B2A", "#8E6236", "#AE7E47"]
DOBRA = ["#3F2C1C", "#5C4129", "#7A5838", "#97724C", "#B08C62"]
SOLA = ["#0E0A08", "#1C1510", "#2B221A", "#3D3226"]
ROXO = ["#2A0F45", "#4B1C78", "#7430B0", "#9E57DD", "#C690F2", "#EAD2FF"]
RAMPAS = {"a": ACO, "l": LATAO, "k": COURO, "t": BOTA, "d": DOBRA, "s": SOLA, "r": ROXO}
R2 = math.sqrt(2)


def _base(lado):
    s = lado / 24
    mat, tom, fixo, x, y = pc.grade(lado)
    return s, mat, tom, fixo, x / s, y / s, 1 / s     # coordenadas no 24 e o tamanho de 1 px nelas


def ataque(lado):
    """A espada na diagonal (o pomo embaixo à esquerda, a ponta em cima à direita): a lâmina de aço com o fio aceso do
    lado da luz, a guarda e o pomo de latão, a empunhadura de couro."""
    s, mat, tom, fixo, X, Y, px = _base(lado)
    x0, y0 = 2.9, 21.1                                # o centro do pomo
    a = ((X - x0) - (Y - y0)) / R2                   # ao longo da espada
    w = ((X - x0) + (Y - y0)) / R2                   # de través (negativo: em cima à esquerda, o lado da luz)
    # a lâmina: de a=6,6 até a ponta em a=21,4, a meia-largura afinando no último terço
    meia = np.where(a < 19.0, 2.15, 2.15 * np.clip((25.0 - a) / 6.0, 0, 1))
    lamina = (a >= 6.6) & (a <= 25.0) & (np.abs(w) <= np.maximum(meia, 0.45 * px))
    mat[lamina] = "a"
    tom[lamina] = np.where(w < -0.8, 6, np.where(w < 0.0, 5, np.where(w < 0.9, 3, 2)))[lamina]
    # o sulco do meio, um tom abaixo, só onde a lâmina é larga
    sulco = lamina & (np.abs(w) < 0.5 * px) & (a > 7.6) & (a < 0)
    tom[sulco] = 3
    # a guarda: a barra de través, de latão
    guarda = (a >= 5.0) & (a < 6.8) & (np.abs(w) <= 4.4)
    mat[guarda] = "l"
    tom[guarda] = np.where(w < -1.2, 4, np.where(w < 1.2, 3, 2))[guarda]
    # a empunhadura: couro, com uma faixa escura (o cordão enrolado)
    cabo = (a >= 2.2) & (a < 5.0) & (np.abs(w) <= 1.05)
    mat[cabo] = "k"
    tom[cabo] = np.where(w < 0, 4, 2)[cabo]
    tom[cabo & (np.abs(a - 3.8) < 0.45 * px + 0.2)] = 1
    # o pomo: um disco de latão com o brilho em cima à esquerda
    pomo = (a - 1.2) ** 2 + w ** 2 <= 1.9 ** 2
    mat[pomo] = "l"
    tom[pomo] = np.where((a - 1.2) - w > 0.8, 4, np.where((a - 1.2) - w > -0.8, 3, 1))[pomo]
    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def defesa(lado):
    """O escudo de bico (o de cavaleiro, que a ficha já usa): a face de aço em duas metades pela aresta do meio (a
    esquerda acesa, a direita na sombra), a borda de latão e dois cravos em cima."""
    s, mat, tom, fixo, X, Y, px = _base(lado)
    cx, topo, reto, bico, meia = 12.0, 1.8, 10.0, 22.4, 8.4
    # a meia-largura por altura: reta até `reto`, depois fechando em curva até o bico
    t = np.clip((Y - reto) / (bico - reto), 0, 1)
    largura = meia * np.sqrt(np.clip(1 - t ** 1.7, 0, 1))
    forma = (Y >= topo) & (Y <= bico) & (np.abs(X - cx) <= largura)
    # o topo levemente curvo para dentro no meio (a borda de cima do escudo de bico)
    forma &= Y >= topo + 0.55 * (1 - np.clip(np.abs(X - cx) / meia, 0, 1))
    mat[forma] = "l"
    tom[forma] = 2
    # a face de aço: a forma recuada de 1 px (no 24)
    t_in = np.clip((Y - reto) / (bico - 1.3 - reto), 0, 1)
    larg_in = (meia - 1.15) * np.sqrt(np.clip(1 - t_in ** 1.7, 0, 1))
    face = forma & (Y >= topo + 1.5) & (Y <= bico - 1.3) & (np.abs(X - cx) <= larg_in)
    mat[face] = "a"
    esq = X < cx
    tom[face] = np.where(esq, np.where(Y < 7, 6, np.where(Y < 14, 5, 4)), np.where(Y < 7, 3, np.where(Y < 14, 2, 1)))[face]
    # a aresta do meio: a linha que separa as metades (a luz pega a de cá)
    aresta = face & (np.abs(X - cx) < 0.5 * px)
    tom[aresta] = 4
    # a borda de latão: acesa em cima à esquerda, escura embaixo à direita
    borda = forma & ~face
    tom[borda] = np.where((X - cx) + (Y - 8) * 0.6 < -2, 4, np.where((X - cx) + (Y - 8) * 0.6 < 3, 3, 1))[borda]
    for (rx, ry) in ((cx - 4.6, topo + 2.6), (cx + 4.6, topo + 2.6)):
        xx, yy = int(rx * s), int(ry * s)
        mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "l", 4 if rx < cx else 3, True
    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def agilidade(lado):
    """A bota de couro do conjunto (de perfil, a ponta para a direita: o cano com a dobra de camurça, o peito do pé e
    a sola) e três riscos de movimento de latão atrás dela. A mesma bota é o comando Fugir."""
    s, mat, tom, fixo, X, Y, px = _base(lado)
    # o cano: de x 9,5 a 15,5; a dobra em cima
    cano = (X >= 8.6) & (X < 15.6) & (Y >= 2.6) & (Y < 16.0)
    # o pé: o calcanhar reto embaixo do cano e o peito do pé descendo em curva até a ponta redonda (x 21,5)
    peito = ((X - 15.2) / 7.6) ** 2 + ((Y - 20.0) / 7.4) ** 2 <= 1
    pe = (Y >= 12.5) & (Y < 19.6) & (X >= 8.6) & ((X < 15.2) | peito)
    corpo = cano | pe
    mat[corpo] = "t"
    tom[corpo] = np.where(X < 10.6, 5, np.where(X < 13.8, 4, 3))[corpo]
    tom[pe & (Y < 15.5) & (X >= 15.5)] = 5                      # o peito do pé, aceso em cima
    tom[pe & (Y >= 16.6) & (X >= 15.5)] = 3
    dobra = (X >= 8.0) & (X < 16.2) & (Y >= 2.6) & (Y < 5.8)
    mat[dobra] = "d"
    tom[dobra] = np.where(Y < 3.7, 4, np.where(X < 12.0, 3, 2))[dobra]
    sola = (Y >= 19.6) & (Y < 21.4) & (X >= 8.2) & (X < 22.6)
    mat[sola] = "s"
    tom[sola] = np.where(Y < 20.5, 3, 1)[sola]
    # a tira do tornozelo com a fivela (como a bota do conjunto)
    tira = (X >= 8.6) & (X < 15.6) & (np.abs(Y - 12.6) < 0.5 * px + 0.15)
    mat[tira] = "t"
    tom[tira] = 2
    fivela = (np.abs(X - 10.6) < 0.8) & (np.abs(Y - 12.6) < 0.8)
    mat[fivela], tom[fivela], fixo[fivela] = "l", 3, True
    # os riscos de movimento: três traços de latão, o do meio mais longo, afinando para trás
    for (yy0, x_a, x_b) in ((6.8, 2.6, 6.8), (10.4, 1.2, 6.8), (14.0, 3.0, 6.8)):
        risco = (np.abs(Y - yy0) < 0.5 * px + 0.12) & (X >= x_a) & (X < x_b)
        mat[risco] = "l"
        tom[risco] = np.where(X > x_b - 2.2, 4, 3)[risco]
        fixo[risco] = True
    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def poder(lado):
    """A chama roxa (a magia e a fé): três línguas que nascem de uma base redonda (a do meio a mais alta, a da esquerda
    média, a da direita curta, curvando para dentro), o roxo escuro por fora, o violeta no corpo e o miolo claro
    embaixo, onde ela é mais quente."""
    s, mat, tom, fixo, X, Y, px = _base(lado)

    def lingua(cx, base_y, topo, larg, curva):
        """Uma gota de fogo: redonda embaixo, afinando até a ponta, que se curva (curva > 0: para a direita)."""
        h = base_y - topo
        t = np.clip((base_y - Y) / h, 0, 1)
        meia = larg * np.sqrt(np.clip(t * 2.6, 0, 1)) * (1 - t) ** 0.85
        centro = cx + curva * t ** 2
        return (Y >= topo) & (Y <= base_y) & (np.abs(X - centro) <= meia), (X - centro) / np.maximum(meia, 0.8), t

    meio, rel, t = lingua(12.2, 22.6, 1.0, 6.2, 1.4)
    esq, rel_e, _ = lingua(7.4, 21.4, 5.4, 4.0, -1.4)     # a da esquerda abre para fora e sobe
    dir_, rel_d, _ = lingua(17.0, 21.8, 8.6, 3.4, 1.6)    # a da direita, curta, abre para fora
    corpo = meio | esq | dir_
    mat[corpo] = "r"
    # a luz pela posição de través na língua de que o pixel faz parte (a do meio manda)
    r = np.where(meio, rel, np.where(esq, rel_e, rel_d))
    tom[corpo] = np.where(r < -0.4, 3, np.where(r < 0.35, 2, 1))[corpo]
    tom[corpo & (t > 0.75) & meio] = np.minimum(tom[corpo & (t > 0.75) & meio], 2)   # a ponta, mais fria
    # o miolo: uma gota clara, baixa, dentro da do meio; o núcleo quase branco no pé dela
    m2, rel2, _ = lingua(11.6, 21.4, 10.0, 4.4, 0.6)
    miolo = m2 & corpo
    tom[miolo] = 4
    nucleo = miolo & (np.abs(rel2) <= 0.55) & (Y > 15.0)
    tom[nucleo] = 5
    fixo[miolo] = True
    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


DESENHOS = {"attr-ataque": ataque, "attr-defesa": defesa, "attr-agilidade": agilidade, "attr-poder": poder}


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    for nome, f in DESENHOS.items():
        for lado in (24, 32):
            print(nome, lado, pc.salvar(f(lado), pasta, nome), "cores")


if __name__ == "__main__":
    main()
