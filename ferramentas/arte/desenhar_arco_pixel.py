"""O arco do Arqueiro em pixel art (proposta; o jogo ainda usa o sprite 16×16 "arco"). Pelo método do escudo e do
machado (pixel_comum.py), cada tamanho desenhado na própria grade.

O que o jogo diz (rpg/itens.py): o desenho "arco" é o das três bases de arma do Arqueiro, Arco Curto, Arco Longo e
Arco Recurvo, em todos os materiais, e o dos únicos Ventre da Tempestade (Arco Longo; "a corda foi trançada com cabelo
de uma bruxa afogada") e Sussurro do Vazio (Arco Recurvo). O mesmo sprite é também o Atacar do Arqueiro na roda, o Tiro
Duplo e o ícone do contrato de caça: esses papéis não mudam (o item se acha só em Icones.ITEM). O desenho atual: um
arco de madeira em D, de pé, com a corda clara.

O tipo: um arco de madeira de uma peça, de pontas levemente viradas (serve aos três: curto, longo e recurvo, sem
puxar para um só), com a empunhadura de couro no meio e a corda clara. Sem flecha (a flecha é da aljava).

A construção, em cada tamanho (32, 40, 48 e 64 px):
  - a composição: na diagonal, como as armas da família; a corda vai da ponta de cima, à direita, até a de baixo, à
    esquerda, e o arco abaula para cima e para a esquerda, com as costas viradas para a luz. As medidas são num
    sistema que gira com a corda (u ao longo dela, v para o lado do arco);
  - a madeira (teixo): as costas do arco em alburno claro, a barriga em cerne escuro (as duas madeiras do arco de
    teixo, que é o que mais se reconhece nele), a luz pela posição na curva (o meio, virado para a luz, acende);
  - a empunhadura: couro escuro enrolado, um pouco mais grossa que o arco, com as voltas marcadas em 48 e 64;
  - as pontas: afinam e viram levemente para fora (o arco recurvo); em 48 e 64, a ponta de chifre clara onde a
    corda prende;
  - a corda: um fio claro e reto entre as pontas;
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/arte/desenhar_arco_pixel.py <pasta>    (grava noutra pasta: a proposta)
    python ferramentas/arte/desenhar_arco_pixel.py            (grava em rpg/web/static/hud/icones/: só na integração)
"""

import math
import sys

import numpy as np

from pixel_comum import ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)  # 32: ficha, mercado, dicas; 40: o corpo e a mochila do Inventário; 48 e 64: o saque

# As rampas, do mais escuro ao mais claro: o teixo (cerne e alburno na mesma rampa), o couro da empunhadura, a corda
# (linho encerado) e o chifre das pontas.
TEIXO = ["#1c0f08", "#351a0d", "#522812", "#713819", "#8f4c22", "#ab6631", "#c58449", "#dba56a", "#ecc893"]
COURO = ["#140b09", "#251412", "#3a1f1a", "#522c23", "#6b3b2d", "#86503c"]
CORDA = ["#5f584a", "#8f8670", "#bdb497", "#e1dabe", "#f3eedb"]
CHIFRE = ["#3b3328", "#6e6250", "#a8987c", "#d6c8a8"]

R2 = math.sqrt(2)
# As medidas de cada tamanho, em pixels: o meio da corda (cx, cy, num centro de pixel), a meia corda (L), quanto o
# arco abaula (H) e a forma da curva (forma: maior = mais cheio no meio, o D); a espessura no meio e na ponta (t_meio,
# t_ponta); a empunhadura (emp, a meia altura, e emp_t, a espessura); a virada das pontas (vira, em px, e vira_l, o
# trecho); `det` liga as voltas do couro e as pontas de chifre (48 e 64).
MEDIDAS = {
    32: dict(cx=18.5, cy=18.5, L=15.6, H=8.8, forma=0.75, t_meio=3.1, t_ponta=1.5, emp=2.4, emp_t=4.0, vira=0.8,
             vira_l=2.5, det=0),
}
for _l, _extra in ((40, dict(cx=23.5, cy=23.5)), (48, dict(cx=27.5, cy=27.5, det=1)), (64, dict(cx=36.5, cy=36.5, det=2))):
    _e = _l / 32
    MEDIDAS[_l] = {k: (v * _e if k not in ("forma", "det") else v) for k, v in MEDIDAS[32].items()} | _extra
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    dx, dy = x - M["cx"], y - M["cy"]
    u, v = (dx - dy) / R2, (-dx - dy) / R2   # u ao longo da corda (para a ponta de cima), v para o lado do arco
    L, H = M["L"], M["H"]
    tu = np.clip(np.abs(u) / L, 0, 1)

    # ---- o arco: a linha do meio (o D), a virada das pontas e a espessura que afina para as pontas
    meio = H * np.clip(1 - tu ** 2, 0, 1) ** M["forma"]
    perto = np.clip((np.abs(u) - (L - M["vira_l"])) / M["vira_l"], 0, 1)   # 0 longe da ponta, 1 na ponta
    centro = meio + M["vira"] * perto ** 2
    inclina = np.gradient(centro, axis=1) * R2   # a inclinação da linha (a distância de verdade nas pontas)
    t = M["t_ponta"] + (M["t_meio"] - M["t_ponta"]) * np.clip(1 - tu ** 1.5, 0, 1)
    emp = np.abs(u) <= M["emp"]
    t = np.where(emp, M["emp_t"], t)
    s = (v - centro) / np.sqrt(1 + inclina ** 2) / (t / 2)    # -1 a barriga (para a corda) ... 1 as costas
    arco = (np.abs(s) <= 1) & (np.abs(u) <= L + 0.3)
    # a madeira: o alburno claro nas costas, o cerne escuro na barriga; a luz pela posição na curva (o meio, que vira
    # para a luz, um degrau acima; as pontas, de lado, um abaixo)
    luz = np.select([tu < 0.45, tu < 0.8], [1, 0], -1)
    tom_arco = np.select([s > 0.35, s > -0.3], [6, 4], 2) + luz
    mat[arco], tom[arco] = "m", np.clip(tom_arco, 1, 8)[arco]
    fixo[arco] = True   # as faixas de 1 pixel do alburno e do cerne são de propósito
    # a empunhadura: couro, com a luz das costas e, em 48 e 64, as voltas (uma linha escura a cada 2 px)
    pega = arco & emp
    tom_pega = np.select([s > 0.3, s > -0.4], [4, 3], 1)
    if M["det"]:
        volta = (np.floor((u + M["emp"]) / 2) % 2 == 0) & (np.abs(s) < 0.9)
        tom_pega = np.where(volta, tom_pega - 1, tom_pega)
    mat[pega], tom[pega] = "l", np.clip(tom_pega, 0, 5)[pega]
    # as pontas de chifre (48 e 64), onde a corda prende
    if M["det"]:
        chifre = arco & (np.abs(u) > L - 1.6)
        mat[chifre], tom[chifre] = "h", np.where(s[chifre] > 0, 3, 2)

    # ---- a corda: um fio reto de ponta a ponta, sobre a linha v = centro das pontas
    v_ponta = M["vira"]
    corda = (np.abs(v - v_ponta + 0.2) <= 0.42) & (np.abs(u) <= L - 0.4) & (mat == "")
    mat[corda], tom[corda] = "s", np.where(u[corda] > 0, 3, 2)
    fixo[corda] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"m": TEIXO, "l": COURO, "s": CORDA, "h": CHIFRE})


if __name__ == "__main__":
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"arco-{lado}: {salvar(desenhar(lado), saida, 'arco')} cores")
