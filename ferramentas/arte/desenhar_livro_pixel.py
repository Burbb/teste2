"""O livro do Mago em pixel art (proposta; o jogo ainda usa o sprite 16×16 "livro"). Pelo método do escudo e do
machado (pixel_comum.py), cada tamanho desenhado na própria grade.

O que o jogo diz (rpg/itens.py): o desenho "livro" é o da arma Grimório e o do apoio Tomo do Mago, em todos os
materiais (de Enferrujado a Rúnico: as peças de metal do livro), e o do único Tomo do Nome Esquecido ("As páginas
estão em branco até você sangrar nelas."). O mesmo sprite é também o atalho do Diário na doca (que tem desenho
próprio no Icones), um talento e o livro da capela: esses papéis não mudam (o item se acha só em Icones.ITEM). O
desenho atual: um livro aberto de capa violeta. A capa violeta fica.

O tipo: um livro grosso, fechado, de couro violeta, visto de cima e da direita: a capa da frente de frente para quem
olha, a lombada à esquerda (o lado da luz) e o corte de baixo, com a espessura das páginas. Poucos detalhes fortes,
todos da construção: os cantos de latão nas duas pontas da capa, o fecho (uma tira de couro que vem de trás, dá a
volta e prende na frente com uma chapa de latão) e, na lombada, os nervos (as costuras em relevo, em 48 e 64). Nenhum
símbolo nem inscrição na capa.

A construção, em cada tamanho (32, 40, 48 e 64 px):
  - a projeção: a capa da frente é um retângulo; a de trás é a mesma, deslocada para a esquerda e para baixo pela
    espessura do livro; entre as duas, a lombada (a face da esquerda) e o corte de baixo (a face de baixo);
  - a capa: o couro, plano e de frente, com a beira da tábua mais clara em cima e à esquerda (a quina que pega luz) e
    mais escura embaixo e à direita; um degrau de sombra junto da lombada (a capa dobra ali);
  - a lombada: um cilindro achatado, em faixas pela espessura (a do meio a mais acesa), com os nervos como fios
    claros com sombra embaixo;
  - o corte de baixo: as páginas em creme, em fios alternados ao longo da capa (a espessura), entre a beira da tábua da
    frente e a da tábua de trás; as páginas recuam da beira das capas (o "esquadro" do livro);
  - os cantos: triângulos de latão nas pontas da capa do lado do corte, acesos na quina (o de baixo desce pela
    beira da tábua no corte);
  - o fecho: a tira de couro mais escura que sai da beira direita da capa e uma chapa de latão com o pino;
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/arte/desenhar_livro_pixel.py <pasta>    (grava noutra pasta: a proposta)
    python ferramentas/arte/desenhar_livro_pixel.py            (grava em rpg/web/static/hud/icones/: só na integração)
"""

import sys

import numpy as np

from pixel_comum import ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)

# As rampas, do mais escuro ao mais claro: o couro violeta, o papel e o latão (o mesmo do escudo).
COURO = ["#0f0a14", "#1e1229", "#2e1b3f", "#402656", "#55336f", "#6c4489", "#8659a3", "#a578bd"]
PAPEL = ["#2a2117", "#4a3d2b", "#6f5f45", "#968461", "#bba982", "#d9caa2", "#efe3c2"]
LATAO = ["#26170a", "#40270c", "#623c12", "#8a571b", "#ae7526", "#cf9737", "#e9bb5c", "#f8dc94", "#fff5d6"]

# As medidas de cada tamanho, em pixels: a capa da frente (x0, x1, y0, y1, os lados do retângulo), a espessura (e, o
# deslocamento da capa de trás para a esquerda e para baixo), a tábua (tab, a espessura de cada capa no corte), o recuo
# das páginas (rec), o canto de latão (canto, o cateto), o fecho (f_y, a altura do meio; f_h, a meia altura da tira;
# f_w, até onde ela entra na capa; ch, o lado da chapa), o painel rebaixado (painel, o recuo do sulco) e os nervos da lombada (nervos, quantos; 0 em 32 e 40, que
# ficam só com as faixas do cilindro).
MEDIDAS = {
    32: dict(x0=10, x1=28, y0=3, y1=25, e=5, tab=1, rec=1, canto=4, painel=2, f_y=14, f_h=1.5, f_w=5, ch=3, nervos=2),
    40: dict(x0=12, x1=35, y0=4, y1=31, e=6, tab=1, rec=1, canto=5, painel=3, f_y=17.5, f_h=2.0, f_w=6, ch=4, nervos=3),
    48: dict(x0=14, x1=42, y0=5, y1=37, e=7, tab=1, rec=1, canto=6, painel=3, f_y=21, f_h=2.5, f_w=7, ch=4, nervos=3),
    64: dict(x0=19, x1=56, y0=6, y1=49, e=9, tab=2, rec=2, canto=8, painel=4, f_y=27.5, f_h=3.0, f_w=10, ch=6, nervos=4),
}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    x0, x1, y0, y1, e = M["x0"], M["x1"], M["y0"], M["y1"], M["e"]
    px, py = np.floor(x).astype(int), np.floor(y).astype(int)   # o pixel inteiro (as faces são de pixel em pixel)

    # ---- a projeção: k é a profundidade (0 a capa da frente, e a de trás) de cada pixel das faces de lado
    # a lombada: à esquerda da capa, entre x0-e e x0, numa faixa que desce com a profundidade (um paralelogramo)
    k_lomb = x0 - px                                             # 1..e
    lomb = (k_lomb >= 1) & (k_lomb <= e) & (py >= y0 + k_lomb) & (py <= y1 + k_lomb)
    # o corte de baixo: abaixo da capa, entre y1 e y1+e, deslocado para a esquerda com a profundidade
    k_corte = py - y1                                            # 1..e
    corte = (k_corte >= 1) & (k_corte <= e) & (px <= x1 - k_corte) & (px >= x0 - k_corte) & ~lomb
    capa = (px >= x0) & (px <= x1) & (py >= y0) & (py <= y1)

    # ---- a lombada: um cilindro achatado em faixas pela profundidade (a do meio a mais acesa)
    fr = (k_lomb - 0.5) / e                                       # 0 junto da capa da frente, 1 junto da de trás
    t_lomb = np.select([fr < 0.18, fr < 0.42, fr < 0.7, fr < 0.88], [5, 6, 5, 4], 3)
    if M["nervos"]:  # os nervos: fios claros com sombra embaixo, a espaços iguais
        alt = y1 - y0
        for j in range(M["nervos"]):
            yn = y0 + alt * (j + 1) / (M["nervos"] + 1)
            linha = py - k_lomb == int(round(yn))
            sob = py - k_lomb == int(round(yn)) + 1
            t_lomb = np.where(linha, np.minimum(t_lomb + 1, 7), np.where(sob & (lado >= 48), t_lomb - 2, t_lomb))
    # as pontas da lombada (a cabeça em cima, o pé embaixo) um degrau abaixo: a quina vira
    pontas = (py == y0 + k_lomb) | (py == y1 + k_lomb)
    t_lomb = np.where(pontas, t_lomb - 1, t_lomb)
    mat[lomb], tom[lomb] = "v", np.clip(t_lomb, 1, 7)[lomb]

    # ---- o corte de baixo: a tábua da frente, as páginas em fios, a tábua de trás
    tab, rec = M["tab"], M["rec"]
    tabua_f = corte & (k_corte <= tab)
    tabua_t = corte & (k_corte > e - tab)
    pag = corte & ~tabua_f & ~tabua_t
    mat[tabua_f | tabua_t], tom[tabua_f | tabua_t] = "v", 2
    # as páginas recuam da beira das capas: o recuo fica na sombra, em couro escuro (o vão entre as tábuas)
    vao = pag & ((px > x1 - k_corte - rec) | (px < x0 - k_corte + rec))
    folhas = pag & ~vao
    t_folha = np.where((k_corte % 2) == 0, 4, 3)                 # os fios das folhas, ao longo da capa
    t_folha = np.where(px < x0 - k_corte + rec + 2, t_folha + 1, t_folha)   # perto da lombada, a luz que entra
    mat[folhas], tom[folhas] = "p", t_folha[folhas]
    mat[vao], tom[vao] = "v", 1

    # ---- a capa: couro de frente, a beira da tábua clara em cima e à esquerda, escura embaixo e à direita
    t_capa = np.full(x.shape, 5)
    t_capa = np.where((px >= x0) & (px <= x0 + 1) & (lado >= 48) | (px == x0), 3, t_capa)   # a dobra junto da lombada
    t_capa = np.where((py == y0) & (px > x0), 7, t_capa)
    t_capa = np.where((px == x0 + (2 if lado >= 48 else 1)) & (py > y0), 6, t_capa)
    t_capa = np.where(py == y1, 3, t_capa)
    t_capa = np.where((px == x1) & (py > y0), 4, t_capa)
    # o painel rebaixado da tábua (um sulco em volta, sem desenho dentro): o sulco escuro e, em 48 e 64, a borda dele
    # que pega a luz (o lado de baixo e o da direita do sulco, que viram para cima e para a esquerda)
    m = M["painel"]
    xa, xb, ya, yb = x0 + m + (1 if lado >= 48 else 0), x1 - m, y0 + m, y1 - m
    sulco = ((((px == xa) | (px == xb)) & (py >= ya) & (py <= yb)) | (((py == ya) | (py == yb)) & (px >= xa) & (px <= xb)))
    t_capa = np.where(sulco, 4, t_capa)
    if lado >= 48:
        luz_s = (((px == xa + 1) & (py > ya) & (py < yb)) | ((py == ya + 1) & (px > xa) & (px < xb)))
        t_capa = np.where(luz_s, 6, t_capa)
    mat[capa], tom[capa] = "v", t_capa[capa]
    fixo[capa | lomb | corte] = True

    # ---- os cantos de latão: nas pontas da capa do lado do corte (em cima à direita e embaixo à direita)
    c = M["canto"]
    sup = capa & ((x1 - px) + (py - y0) < c)
    inf = capa & ((x1 - px) + (y1 - py) < c)
    mat[sup | inf], tom[sup], tom[inf] = "l", 5, 4
    tom[sup & (py == y0)] = 7                                     # a quina de cima pega a luz
    tom[inf & (py == y1)] = 3
    tom[(sup | inf) & (px == x1) & (py > y0)] = 3
    tom[inf & ((x1 - px) + (y1 - py) == c - 1) & (px < x1)] = 6   # a beira de dentro do canto de baixo, acesa
    tom[sup & ((x1 - px) + (py - y0) == c - 1) & (py > y0)] = 4   # a de dentro do de cima, a sombra da peça na capa
    # o canto de baixo desce pelo corte: a tábua da frente também leva latão na ponta
    inf_c = corte & (k_corte <= tab) & (px > x1 - c + 1 - k_corte)
    mat[inf_c], tom[inf_c] = "l", 2
    fixo[sup | inf | inf_c] = True

    # ---- o fecho: a tira de couro mais escura saindo da beira direita e a chapa de latão com o pino
    fy, fh, fw, ch = M["f_y"], M["f_h"], M["f_w"], M["ch"]
    tira = (np.abs(y - fy) <= fh) & (px > x1 - fw) & (px <= x1 + 1)
    tira &= capa | (px == x1 + 1)                                 # a tira dá a volta: um pixel por fora da beira
    t_tira = np.where(np.abs(y - fy) > fh - 1, 2, 3)
    t_tira = np.where(y < fy - fh + 1, 4, t_tira)
    mat[tira], tom[tira] = "v", t_tira[tira]
    sombra_tira = capa & (np.floor(y) == np.floor(fy + fh) + 1) & (px > x1 - fw) & ~tira   # a sombra da tira na capa
    tom[sombra_tira] = 2
    xc = x1 - fw + 1
    chapa = (px >= xc - ch // 2) & (px < xc - ch // 2 + ch) & (np.abs(y - fy) <= fh + (0.6 if lado >= 48 else 0.1))
    mat[chapa], tom[chapa] = "l", 5
    tom[chapa & (px == xc - ch // 2)] = 6
    tom[chapa & (py == np.floor(fy - fh - (0.6 if lado >= 48 else 0.1)) + 1)] = 7
    tom[chapa & (px == xc - ch // 2 + ch - 1)] = 3
    pino = (px == xc - (0 if ch % 2 else 1) + (ch // 2 if ch % 2 == 0 else 0) - (1 if ch >= 4 else 0)) & (py == int(np.floor(fy)))
    if lado >= 48:
        mat[chapa & pino], tom[chapa & pino] = "l", 2
    fixo[tira | chapa] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"v": COURO, "p": PAPEL, "l": LATAO})


if __name__ == "__main__":
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"livro-{lado}: {salvar(desenhar(lado), saida, 'livro')} cores")
