"""O escudo refinado em pixel art (experimento, fora do jogo): o candidato de desenhar_escudo.py (o render do relevo)
continua como referência de forma, construção e luz, e o escudo atual da HUD como referência de presença dos reflexos
e de contraste nos tamanhos pequenos. Aqui o desenho não é a redução do render: cada tamanho final (32, 48 e 64 px) é
construído na própria grade, por regras, com a paleta organizada em rampas e a luz em grupos de pixels deliberados.

A construção, em cada tamanho:
  - a silhueta: dois discos em centro de pixel (a frente, e atrás dela, deslocada para baixo e para a direita, a
    lateral do escudo, que aparece como um crescente); os raios são escolhidos para os degraus do círculo saírem
    regulares, e o contorno escuro tem 1 pixel, só pelos lados (sem engrossar nas diagonais);
  - o aro de latão: um rolo, por regras: o tom pelo ângulo até a luz, a fileira de fora e a de dentro um degrau abaixo
    do lado em que viram, e o brilho mais claro só onde a luz bate de frente (um arco curto em cima à esquerda): um
    reflexo localizado, sem um anel claro em volta do círculo inteiro;
  - o degrau entre a face e o aro: a sombra do aro sobre a face, a volta toda;
  - a face de ferro: oito gomos, cada um num tom só da rampa de ferro, pela direção dele em relação à luz (o gomo de
    cima à esquerda o mais claro, o de baixo à direita o mais escuro); no gomo iluminado, o reflexo é uma mancha
    desenhada em três tons; a emenda entre os gomos aparece como uma linha de pixel em 48 e 64 e só pela troca de tom
    em 32;
  - a peça central: o sulco escuro, a base de latão (um anel, como o aro), a cúpula sombreada por faixas com o brilho
    num grupo pequeno em cima à esquerda, e a sombra da peça sobre a face embaixo à direita;
  - os cravos: oito, nos mesmos ângulos; em 32, um pixel de latão com um pixel de sombra; em 48, dois por dois; em
    64, uma cruz arredondada; o tom de cada um pelo lado em que está;
  - a limpeza: um pixel isolado de um tom no meio de outro do mesmo material vira o tom em volta (fora o que é
    desenhado de propósito: o brilho, os cravos); e as correções feitas olhando cada tamanho (AJUSTES).
O dobro de cada arquivo (para telas densas) é a duplicação exata dos pixels.

    python ferramentas/prototipos/hud/desenhar_escudo_pixel.py
"""

import math
import pathlib

import numpy as np

from pixel_comum import ANG_LUZ, LUZ, ajustar, contornar, imagem, limpar, salvar

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI / "escudo-pixel"

# As rampas: do mais escuro ao brilho (o ferro azulado e o latão do escudo atual, organizados em degraus).
FERRO = ["#0e1117", "#191e28", "#252c3a", "#343e51", "#465269", "#5d6b86", "#8492ab", "#bcc5d4", "#eef1f6"]
LATAO = ["#26170a", "#40270c", "#623c12", "#8a571b", "#ae7526", "#cf9737", "#e9bb5c", "#f8dc94", "#fff5d6"]
# o tom de cada gomo pela distância à luz (o da luz, os vizinhos, os de lado, os de trás, o oposto) fica em MEDIDAS
# (`escada`): na passagem final, os de trás desceram um degrau em 48 e 64
# a luz (de cima e da esquerda) e o contorno são os de pixel_comum.py, comuns aos objetos

# As medidas de cada tamanho, em pixels (os raios em relação ao centro do disco da frente).
MEDIDAS = {
    32: dict(raio=12.45, lado=1, aro=2.0, degrau=1, cupula=3.5, base=0.0, sulco=1.0, cravos=7.9, cravo="1", sombra_peca=1, emendas=False, reflexo=(1.35, 2.0), alcance=0.62, escada=(7, 5, 4, 3, 2)),
    48: dict(raio=18.45, lado=1, aro=2.8, degrau=1, cupula=4.4, base=1.2, sulco=1.0, cravos=12.3, cravo="2", sombra_peca=1, emendas=True, reflexo=(1.0, 1.65), alcance=0.7, escada=(7, 5, 4, 3, 1)),
    64: dict(raio=24.45, lado=1, aro=3.0, degrau=1, cupula=6.0, base=1.6, sulco=1.1, cravos=17.2, cravo="3", sombra_peca=2, emendas=True, reflexo=(1.05, 1.7), alcance=0.72, escada=(7, 5, 4, 2, 1)),
}
# O brilho da cúpula, desenhado por tamanho: {(dx, dy): tom} em volta do ponto de luz.
BRILHO_CUPULA = {32: {(0, 0): 8, (1, 0): 6, (0, 1): 6},
                 48: {(0, 0): 8, (1, 0): 7, (0, 1): 7, (1, 1): 6, (-1, 0): 6, (0, -1): 6},
                 64: {(0, 0): 8, (1, 0): 8, (0, 1): 7, (1, 1): 7, (-1, 0): 6, (0, -1): 6, (2, 0): 6, (0, 2): 6, (-1, 1): 6,
                      (1, -1): 6}}
# Correções feitas olhando cada tamanho: {(x, y): ("f"|"l"|"c", índice)} (ferro, latão, contorno; None apaga).
AJUSTES = {32: {}, 48: {}, 64: {}}


def desenhar(lado_img):
    M = MEDIDAS[lado_img]
    R, s = M["raio"], M["lado"]
    # o centro da frente num centro de pixel; a lateral deslocada `s` para baixo e para a direita
    cx = cy = lado_img / 2 + 0.5 - s  # um centro de pixel: a frente e a lateral juntas no enquadramento do atual
    y, x = np.mgrid[0:lado_img, 0:lado_img] + 0.5
    dx, dy = x - cx, y - cy
    d = np.hypot(dx, dy)
    ang = np.arctan2(dy, dx)
    frente = d <= R
    # a lateral: o disco de trás deslocado pela diagonal, `s` px no total (com 1 px em x e 1 em y, a diagonal dava
    # 1,4 px e o canto de baixo à direita engordava)
    dsl = s / math.sqrt(2)
    tras = np.hypot(x - cx - dsl, y - cy - dsl) <= R
    mat = np.full(d.shape, "", dtype=object)   # "f" ferro, "l" latão, "c" contorno
    tom = np.zeros(d.shape, dtype=int)
    fixo = np.zeros(d.shape, dtype=bool)       # desenhado de propósito: a limpeza não mexe

    def delta(a):  # o ângulo até a direção da luz, de 0 (de frente para a luz) a pi
        return np.abs((a - ANG_LUZ + np.pi) % (2 * np.pi) - np.pi)

    # ---- a lateral: o crescente embaixo e à direita, latão na sombra
    lat = tras & ~frente
    mat[lat], tom[lat] = "l", 1

    # ---- o aro: um rolo de latão, por regras (a conta pela normal acendia a metade de baixo inteira)
    #   o tom pelo ângulo até a luz; a fileira de fora um degrau abaixo do lado da sombra e a de dentro um degrau
    #   abaixo do lado da luz (o rolo vira para fora ali); o brilho num arco curto do lado da luz
    dl = delta(ang)
    r_aro = R - M["aro"]
    aro = frente & (d > r_aro)
    fileira = np.clip(np.floor(d - r_aro), 0, math.ceil(M["aro"]) - 1).astype(int)  # 0 dentro ... fora
    ultima = math.ceil(M["aro"]) - 1
    base_aro = np.select([dl < 0.7, dl < 1.4, dl < 2.1, dl < 2.6], [4, 4, 3, 2], 2)
    t_aro = base_aro.copy()
    t_aro = np.where((fileira == ultima) & (dl > 1.6) & (t_aro > 2), t_aro - 1, t_aro)
    t_aro = np.where((fileira == 0) & (dl < 1.2), t_aro - 1, t_aro)
    meio_aro = (fileira > 0) & (fileira < ultima) if ultima >= 2 else (fileira == ultima)
    t_aro = np.where(meio_aro & (dl < 0.62), 5, t_aro)
    t_aro = np.where(meio_aro & (dl < 0.4), 6, t_aro)
    t_aro = np.where(meio_aro & (dl < 0.24), 7, t_aro)
    t_aro = np.where(meio_aro & (dl < 0.1), 8, t_aro)
    t_aro = np.clip(t_aro, 1, 8)
    mat[aro], tom[aro] = "l", t_aro[aro]

    # ---- o degrau: a sombra do aro sobre a face, a volta toda (a parede de dentro do aro acesa embaixo à direita
    #   foi tirada: em 32 e 48 engordava o canto, e em 64 virava um risco solto por dentro do aro)
    r_deg = r_aro - M["degrau"]
    deg = frente & (d > r_deg) & ~aro
    mat[deg], tom[deg] = "f", 0

    # ---- a face: oito gomos, cada um num tom pela direção dele
    passo = np.pi / 4
    centro_gomo = np.round(ang / passo) * passo
    r_sulco = M["cupula"] + M["base"] + M["sulco"]
    face = frente & (d <= r_deg) & (d > r_sulco)
    ordem = np.round(delta(centro_gomo) / passo).astype(int)  # 0 o gomo da luz ... 4 o oposto
    escada = np.array(M["escada"])
    tom_gomo = escada[ordem]
    mat[face], tom[face] = "f", tom_gomo[face]
    rf = (d - r_sulco) / (r_deg - r_sulco)  # 0 junto do sulco, 1 junto do degrau
    # a emenda: uma linha de pixel um tom abaixo do mais escuro dos dois gomos
    if M["emendas"]:
        dist_emenda = np.abs(((ang - passo / 2) % passo) - passo / 2) * d
        em = face & (dist_emenda < 0.5) & (rf > 0.05) & (rf < 0.97)
        tom[em] = np.maximum(1, np.minimum(tom_gomo[em], escada[np.minimum(ordem[em] + 1, 4)]) - 1)
    # a sombra junto do sulco (o pé da peça central) e a sombra da peça sobre a face, embaixo à direita
    pe = face & (d <= r_sulco + 1.0)
    tom[pe] = np.maximum(1, tom[pe] - 1)
    sp = M["sombra_peca"]
    sombra_peca = face & (np.hypot(dx - sp, dy - sp) <= M["cupula"] + M["base"] + 0.6) & (d > r_sulco)
    tom[sombra_peca] = np.maximum(0, tom[sombra_peca] - 2)

    # o reflexo no gomo da luz (depois das sombras, por cima delas): uma mancha em três tons, do pé da peça para fora
    lado_g = np.abs((ang - centro_gomo + np.pi) % (2 * np.pi) - np.pi) * d  # distância à linha do meio do gomo, em px
    gomo_luz = face & (ordem == 0)
    largura = (0.3 + 0.9 * rf) * (r_deg - r_sulco) * 0.4
    nucleo = gomo_luz & (rf > 0.0) & (rf < M["alcance"]) & (lado_g < largura * M["reflexo"][0])
    meio = gomo_luz & (rf > -0.1) & (rf < M["alcance"] + 0.18) & (lado_g < largura * M["reflexo"][1]) & ~nucleo
    tom[meio], tom[nucleo] = 7, 8
    tom[gomo_luz & ~meio & ~nucleo] = np.minimum(tom[gomo_luz & ~meio & ~nucleo], 6)
    fixo[nucleo | meio] = True

    # ---- o sulco, a base e a cúpula
    sulco = frente & (d <= r_sulco) & (d > M["cupula"] + M["base"])
    mat[sulco], tom[sulco] = "f", 0
    base = frente & (d <= M["cupula"] + M["base"]) & (d > M["cupula"])
    mat[base], tom[base] = "l", np.where(dl[base] < 0.9, 6, np.where(dl[base] < 1.9, 5, np.where(dl[base] < 2.5, 3, 2)))
    cup = frente & (d <= M["cupula"])
    rc = np.clip(d / M["cupula"], 0, 0.999)
    nc = np.stack([dx / M["cupula"], dy / M["cupula"], np.sqrt(1 - rc ** 2)], -1)
    vc = np.clip(nc @ LUZ, 0, 1)
    tom_cup = np.clip(np.round(1.4 + 4.0 * vc), 2, 5).astype(int)
    mat[cup], tom[cup] = "l", tom_cup[cup]
    # o brilho da cúpula: um grupo desenhado por tamanho, em cima à esquerda do centro (a conta de um disco saía em cruz)
    bx = int(math.floor(cx + 0.42 * M["cupula"] * math.cos(ANG_LUZ)))
    by = int(math.floor(cy + 0.42 * M["cupula"] * math.sin(ANG_LUZ)))
    for (ox, oy), t_ in BRILHO_CUPULA[lado_img].items():
        xx, yy = bx + ox, by + oy
        if cup[yy, xx]:
            tom[yy, xx], fixo[yy, xx] = max(tom[yy, xx], t_), True
    # a borda de baixo da cúpula escurece um degrau (o volume da cúpula contra a base)
    borda_c = cup & (d > M["cupula"] - 1) & (dl > 1.9)
    tom[borda_c] = np.minimum(tom[borda_c], 2)

    # ---- os cravos
    for k in range(8):
        a = -np.pi / 2 + k * passo
        px, py = cx + M["cravos"] * math.cos(a), cy + M["cravos"] * math.sin(a)
        ix, iy = int(math.floor(px)), int(math.floor(py))
        lado_luz = math.cos(a - ANG_LUZ)  # 1 de frente para a luz, -1 do lado oposto
        claro = 7 if lado_luz > 0.5 else 6 if lado_luz > -0.3 else 5
        if M["cravo"] == "1":
            pontos = {(0, 0): ("l", claro - 1)}
        elif M["cravo"] == "2":
            pontos = {(0, 0): ("l", claro), (1, 0): ("l", claro - 1), (0, 1): ("l", claro - 1), (1, 1): ("l", 3),
                      (2, 1): ("f", 0), (1, 2): ("f", 0), (2, 2): ("f", 1)}
        else:
            # uma cabeça redonda de 3 por 3: os cantos seguem a luz (cantos todos escuros pareciam uma cruz)
            pontos = {(-1, -1): ("l", claro - 1), (0, -1): ("l", claro - 1), (1, -1): ("l", claro - 2),
                      (-1, 0): ("l", claro - 1), (0, 0): ("l", claro), (1, 0): ("l", claro - 2),
                      (-1, 1): ("l", claro - 2), (0, 1): ("l", claro - 2), (1, 1): ("l", 2),
                      (2, 0): ("f", 1), (2, 1): ("f", 0), (1, 2): ("f", 0), (0, 2): ("f", 1), (2, 2): ("f", 1)}
        for (ox, oy), (m_, t_) in pontos.items():
            xx, yy = ix + ox, iy + oy
            if 0 <= xx < lado_img and 0 <= yy < lado_img and mat[yy, xx] == "f":
                if m_ == "f":  # a sombra do cravo: a face embaixo dele, dois degraus abaixo
                    t_ = max(0, min(tom[yy, xx] - 2, t_ + 2))
                mat[yy, xx], tom[yy, xx], fixo[yy, xx] = m_, t_, True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado_img])
    return imagem(mat, tom, {"f": FERRO, "l": LATAO})


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    for lado in (32, 48, 64):
        print(f"escudo-{lado}: {salvar(desenhar(lado), SAIDA, 'escudo')} cores")
