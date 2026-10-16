"""A Bomba de Fumaça em pixel art (proposta; o jogo ainda usa o sprite 16×16 "caveira"). O quarto objeto do método do
escudo e do unguento (pixel_comum.py), desenhado na grade de 32 px.

O que o jogo diz do item (rpg/itens.py e os usos): "Bomba de Fumaça", 35 de ouro, "Garante a fuga de um combate
(exceto chefes)", usada só na luta; vem de bandidos ("tirou a gente de muita enrascada") e de um ladrão que você
poupa. Nada de mágico: é um recurso de quem foge, feito à mão. O desenho atual é a caveira, que no jogo também é o
retrato dos inimigos, o Bestiário, a derrota, o estado Provocando, a fome e a lixeira do Inventário; o item novo se acha
só pelo id (SO_PELO_ID), e a caveira continua em todos esses papéis.

O conceito (com o retorno do Jean: "mais cara de bomba, mais personalidade; preta já faz grande diferença"): a bomba
redonda e preta dos jogos, feita com o que há na vila. Um pote quase esférico de barro preto vidrado (louça negra de
queima, com o ponto de brilho do esmalte), o pescoço curto tapado por um tufo de pano encerado amarrado com cordão de
cânhamo, uma rede de cordão em volta da barriga (para levar e atirar) e um pavio grosso que sobe e enrola, com a
ponta desfiada. Sem pino, alavanca ou cinta de granada moderna, sem caveira nem símbolo, sem fogo: o pavio está
apagado. A fumaça não aparece (o objeto se reconhece sozinho). A primeira versão (terracota, mais realista) lia como um
pote de barro e ficava parecida com o unguento na bolsa.

A construção (32 px; a bomba só fica parada em 32: a bolsa, a prateleira do mercado, a janelinha de Itens da luta, o
quadro do baú; o voo até a bolsa anima o mesmo arquivo):
  - o pote: uma forma de revolução vista um pouco de cima, como o unguento: a barriga quase esférica, a base cortada
    na elipse de baixo; vidrado escuro: a forma em poucas faixas largas de quase preto, a luz de volta do chão
    embaixo à direita (a silhueta não some no fundo da HUD) e o reflexo do esmalte desenhado, em cima à esquerda;
  - o pano: um tufo sobre a boca, apertado pelo cordão e abrindo numa saia curta com as pregas em pixels alternados;
    linho cru (bege acinzentado), o ponto claro contra o pote preto;
  - o cordão: uma volta no pescoço, com o nó do lado da sombra e as pontas caindo; dois fios que descem até o fundo e
    um anel em volta da barriga, escuros (claros, viravam uma grade de cesto);
  - o pavio: grosso no pé, sobe e enrola para a direita, a ponta desfiada mais clara;
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro do arquivo é a duplicação exata dos pixels.

    python ferramentas/arte/desenhar_bomba_pixel.py <pasta>    (grava noutra pasta: a proposta)
    python ferramentas/arte/desenhar_bomba_pixel.py            (grava em rpg/web/static/hud/icones/: só na integração)
"""

import sys

import numpy as np

from pixel_comum import LUZ, ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32,)

# As rampas, do mais escuro ao mais claro: o barro preto vidrado (um quase preto um pouco quente, e o brilho do
# esmalte), o pano (linho cru encerado) e o cordão (cânhamo; o pavio usa os tons de baixo).
BARRO = ["#09080a", "#121114", "#1b1a1e", "#252429", "#302f35", "#3e3d44", "#56555d", "#8a8992", "#d4d3da"]
PANO = ["#24221d", "#3d3a31", "#5c584b", "#7c7766", "#9a9480", "#b5ae97", "#cdc7ae", "#e0dbc4"]
CORDAO = ["#1c140b", "#33240f", "#4f3816", "#6f5022", "#906b30", "#ad8743", "#c6a25c"]

# As medidas (32 px): o eixo (cx) e o achatamento das voltas (K); a barriga: o centro (by), a meia largura (a), a meia
# altura (b), o expoente (exp) e o fundo (yf); o pescoço (rn); o pano: o topo do tufo (yt), a meia largura dele (rt), a
# linha do cordão (yc) e a saia (rs, até ys); as alças (alca: onde passam, em fração do raio) e o anel da barriga
# (anel: a altura, a partir do centro da barriga); o pavio e o nó: os
# pixels, com o tom.
MEDIDAS = {
    32: dict(cx=16.0, K=0.4, by=19.6, a=11.6, b=10.8, exp=2.0, yf=28.2, rn=3.0, yt=5.4, rt=3.9, yc=9.0, rs=4.8, ys=10.6,
             alca=0.5, anel=-2.4,
             # o pavio: grosso no pé, sobe e enrola para a direita, a ponta desfiada mais clara
             pavio=[((15, 5), 4), ((16, 5), 2), ((15, 4), 5), ((16, 4), 3), ((16, 3), 4), ((17, 2), 5), ((18, 2), 4),
                    ((19, 2), 3), ((19, 3), 4), ((20, 3), 6), ((20, 4), 6), ((21, 3), 5)],
             nos=[((19, 9), 4), ((20, 9), 2), ((20, 10), 3), ((21, 11), 2), ((19, 11), 3), ((19, 12), 2)],
             # o brilho do esmalte: uma mancha pequena em cima à esquerda da barriga, em volta do ponto de luz
             brilho={(0, 0): 8, (1, 0): 8, (0, 1): 7, (1, 1): 7, (-1, 1): 6, (2, 0): 7, (-1, 2): 6, (3, -1): 6, (2, -1): 7,
                     (0, 2): 6, (4, -1): 6}),
}
# Correções feitas olhando o tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}}


def faixas(v):
    """O tom pela luz recebida, em poucas faixas largas (fosco)."""
    return np.select([v > 0.66, v > 0.4, v > 0.14], [6, 5, 4], 3) - (v < 0.03)


def luz(dx, raio, dr):
    """A luz de uma forma de revolução: a normal pela posição na volta (dx/raio) e pela inclinação do perfil (dr)."""
    u = np.clip(dx / np.maximum(raio, 0.5), -1, 1)
    nz = np.sqrt(1 - u ** 2)
    n = np.stack([u, -np.clip(dr, -2.5, 2.5) * nz, nz + 0.1], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return np.clip(n @ LUZ, 0, 1), u


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    cx, K = M["cx"], M["K"]
    dx = x - cx

    # ---- o pote: a barriga (superelipse girada) e o fundo cortado na elipse de baixo
    def raio_barriga(yy):
        t = np.clip((yy - M["by"]) / M["b"], -1, 1)
        return M["a"] * np.clip(1 - np.abs(t) ** M["exp"], 0, 1) ** (1 / M["exp"])
    rbar = np.maximum(raio_barriga(y), np.where(y < M["by"], M["rn"], 0))
    rf = float(raio_barriga(np.array(M["yf"])))
    chao = M["yf"] + rf * K * np.sqrt(np.clip(1 - (dx / rf) ** 2, 0, 1))
    corpo = (np.abs(dx) <= rbar) & (y >= M["yc"]) & ((y <= M["yf"]) | ((np.abs(dx) <= rf) & (y <= chao)))
    dr = (raio_barriga(y + 0.5) - raio_barriga(y)) / 0.5
    dr = np.where(y > M["yf"], (raio_barriga(np.array(M["yf"] + 0.5)) - rf) / 0.5, dr)
    v, u = luz(dx, np.where(y > M["yf"], rf, rbar), dr)
    # vidrado: a forma em faixas escuras (o barro é preto), a borda da sombra quase sem luz e um reflexo de volta
    # embaixo à direita (o chão), um degrau acima, para a silhueta não se perder no fundo escuro
    tom_corpo = np.select([v > 0.7, v > 0.45, v > 0.2], [5, 4, 3], 2) - (np.abs(u) > 0.95)
    volta = (dx > 0.35 * rbar) & (y > M["by"] + 0.35 * M["b"]) & (np.hypot(dx / M["a"], (y - M["by"]) / M["b"]) > 0.82)
    tom_corpo = np.where(volta, 3, tom_corpo)
    mat[corpo], tom[corpo] = "b", tom_corpo[corpo]
    pe = corpo & (y > chao - 1.0) & (y > M["yf"] - 0.5)
    tom[pe] = np.maximum(1, tom[pe] - 1)

    # ---- o pano: a saia sobre o ombro (abre do cordão para baixo, em pregas) e o tufo sobre a boca
    ys, yc = M["ys"], M["yc"]
    t_saia = np.clip((y - yc) / (ys - yc), 0, 1)
    r_saia = M["rn"] + (M["rs"] - M["rn"]) * t_saia ** 0.7
    saia = (np.abs(dx) <= r_saia) & (y > yc) & (y <= ys + K * np.sqrt(np.clip(1 - (dx / M["rs"]) ** 2, 0, 1)))
    vs, us = luz(dx, r_saia, np.full_like(dx, 0.9))
    prega = (np.floor(x) % 2 == 1) & (y > yc + 1)   # as pregas: o pano franzido, uma coluna sim, outra não
    tom_saia = np.clip(faixas(vs) - prega, 1, 6)
    mat[saia], tom[saia] = "p", tom_saia[saia]
    fixo[saia & prega] = True
    # o tufo: um bulbo em cima da boca, apertado embaixo pelo cordão
    tb = np.clip((y - M["yt"]) / (yc - M["yt"]), 0, 1)
    r_tufo = M["rt"] * np.sqrt(np.clip(np.sin(np.pi * (0.12 + 0.8 * tb)), 0, 1))
    tufo = (np.abs(dx) <= r_tufo) & (y >= M["yt"]) & (y <= yc)
    dr_t = np.gradient(r_tufo, axis=0)
    vt, ut = luz(dx, r_tufo, dr_t)
    mat[tufo], tom[tufo] = "p", np.clip(faixas(vt), 1, 7)[tufo]

    # ---- o cordão: a volta no pescoço (acesa à esquerda), o nó e as pontas
    volta = (np.abs(dx) <= M["rn"] + 0.6) & (np.floor(y) == np.floor(yc))
    mat[volta], tom[volta] = "r", np.select([dx < -1.5, dx < 1.5], [5, 4], 2)[volta]
    fixo[volta] = True
    for (xx, yy), t_ in M["nos"]:
        mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "r", t_, True

    # ---- as alças do cordão: dois fios do nó até o fundo, abraçando a barriga (o pote amarrado para levar e atirar),
    # curvados pela forma; o tom pela luz da barriga, um degrau acima do barro em volta
    for lado_ in (-1, 1):
        for yy in range(int(M["ys"]) + 1, int(M["yf"]) + 1):
            r_ = float(raio_barriga(np.array(yy + 0.5)))
            xx = int(np.floor(cx + lado_ * r_ * M["alca"]))
            if mat[yy, xx] == "b":
                mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "r", int(np.clip(tom[yy, xx] - 2, 1, 2)), True

    # a volta da barriga: um anel do cordão em volta do pote, que cruza as alças (a frente do anel, vista um pouco de
    # cima, desce no meio)
    ya = M["by"] + M["anel"]
    ra = float(raio_barriga(np.array(ya)))
    for xx in range(int(np.floor(cx - ra)), int(np.ceil(cx + ra))):
        yy = int(np.floor(ya + ra * K * np.sqrt(max(0.0, 1 - ((xx + 0.5 - cx) / ra) ** 2))))
        if mat[yy, xx] in ("b", "r"):
            mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "r", int(np.clip(tom[yy, xx] - 2, 1, 2)), True

    # o brilho do esmalte, desenhado (por cima do cordão, como num pote vidrado)
    bx, by_ = int(np.floor(cx - 0.33 * M["a"])), int(np.floor(M["by"] - 0.5 * M["b"]))
    for (ox, oy), t_ in M["brilho"].items():
        if mat[by_ + oy, bx + ox] in ("b", "r"):
            mat[by_ + oy, bx + ox], tom[by_ + oy, bx + ox], fixo[by_ + oy, bx + ox] = "b", t_, True

    # ---- o pavio: um cordão escuro e torcido, a ponta desfiada mais clara
    for (xx, yy), t_ in M["pavio"]:
        mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "r", t_, True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"b": BARRO, "p": PANO, "r": CORDAO})


if __name__ == "__main__":
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"bomba-{lado}: {salvar(desenhar(lado), saida, 'bomba')} cores")
