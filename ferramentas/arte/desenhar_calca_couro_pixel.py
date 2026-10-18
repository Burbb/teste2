"""A Calça de Couro do Arqueiro (`calca_couro`, espaço das pernas) no método da família: proposta, nada no jogo.

Hoje ela não tem desenho da família: o jogo mostra o sprite 16×16 da calça recolorido (sprites-dados.js). O desenho
segue o conjunto de couro aprovado (o gibão, as botas, o capuz e a luva, 1.110.0 e 1.112.0): as mesmas rampas
(`couro_r2.py` em ferramentas/prototipos/hud/couro-aseprite/auxiliares), a luz em faixas chapadas (clara à esquerda,
escura na beira da direita), as emendas como linhas escuras, o cordão em zigue-zague contínuo de duas cores e um
ponto de desgaste.

O objeto: um par de pernas de frente (como a perneira de ferro, que é o vizinho no mesmo espaço), o cós de couro
escuro de borda, a braguilha amarrada com o cordão do gibão, o reforço costurado nos joelhos e o barrado escuro. A
perna da direita fica um tom abaixo (a luz vem da esquerda). Sem tachas, fivela grande nem bolsos: a calça é a peça
mais simples do conjunto.

Medidas no 32 (MEDIDAS); o 64 é o 32 ampliado 2× (como no couro); 40 e 48 saem das mesmas medidas na grade deles,
depois de aprovada a leitura do 32 (a prévia deles ainda pede retoque no remendo do joelho).

    python ferramentas/arte/desenhar_calca_couro_pixel.py <pasta> [--intermediarios]   # grava a proposta numa pasta
"""

import math
import sys

import numpy as np
from PIL import Image

import pixel_comum as pc

# as rampas do conjunto de couro (couro_r2.py), do escuro ao claro
COURO = ["#1C120C", "#2E1E13", "#45301E", "#604229", "#7C5634", "#986C42", "#B48752"]
BORDA = ["#140C08", "#22150D", "#321F13", "#45301E"]
CORDAO = ["#5E472E", "#8E7250", "#BFA27A"]
GASTO = ["#8A6A4C", "#A07E5C"]
RAMPAS = {"k": COURO, "b": BORDA, "o": CORDAO, "g": GASTO}

# A construção, em unidades do 32 (o pixel k do 32 vai de k a k+1). Cada perna é um trapézio de lado reto por dentro
# e um pouco aberto por fora; o cós cobre as duas.
MEDIDAS = {
    "cos": (2.0, 5.0),            # o cós: do topo até a primeira linha das pernas
    "cos_x": (8.0, 24.0),         # largura do cós
    "gancho": 12.0,               # onde as pernas se separam (abaixo, o vão em V)
    "vao": (15.5, 16.5),          # o vão no gancho (1 px no 32); embaixo ele abre (as pernas de dentro)
    "perna_esq": ((8.0, 15.5), (9.0, 14.2)),     # (x de fora, x de dentro) no quadril e na barra
    "perna_dir": ((16.5, 24.0), (17.8, 23.0)),
    "barra": (28.0, 30.0),        # o barrado: as últimas linhas
    "joelho": (17.0, 21.0),       # o remendo do joelho (das costuras de cima e de baixo), dentro da perna
    "bragueta": (5.0, 11.0),      # a amarração da braguilha (abaixo do cós até perto do gancho)
}


def desenhar(lado):
    s = lado / 32
    mat, tom, fixo, x, y = pc.grade(lado)
    u, v = x / s, y / s      # o centro de cada pixel em unidades do 32
    M = MEDIDAS
    topo, base = M["cos"][0], M["barra"][1]

    def perna(lims, uu, vv):
        (fq, dq), (fb, db) = lims
        t = np.clip((vv - topo) / (base - topo), 0, 1)
        return (uu >= fq + (fb - fq) * t) & (uu < dq + (db - dq) * t)

    esq = perna(M["perna_esq"], u, v) & (v >= topo) & (v < base)
    dir_ = perna(M["perna_dir"], u, v) & (v >= topo) & (v < base)
    meio = (u >= M["vao"][0]) & (u < M["vao"][1]) & (v >= topo) & (v < M["gancho"])   # acima do gancho, o vão é tecido
    corpo = esq | dir_ | meio
    mat[corpo] = "k"

    # a luz em faixas por perna: pela posição de través (0 fora/esquerda, 1 dentro/direita)
    def faixas(mask, lims, base_tom):
        (fq, dq), (fb, db) = lims
        t = np.clip((v - topo) / (base - topo), 0, 1)
        a, b = fq + (fb - fq) * t, dq + (db - dq) * t
        p = (u - a) / np.maximum(b - a, 1e-6)
        tt = np.where(p < 0.28, base_tom + 1, np.where(p < 0.72, base_tom, base_tom - 1))
        ultima = (u + 1 / s >= b)            # a última coluna da perna (a beira), um tom abaixo
        tt = np.where(ultima & (p > 0.5), tt - 1, tt)
        tom[mask] = tt[mask]

    faixas(esq | (meio & (u < 16)), M["perna_esq"], 5)
    faixas(dir_ | (meio & (u >= 16)), M["perna_dir"], 4)
    # o gancho na sombra: as colunas junto do vão, logo abaixo do cós, escurecem
    sombra = corpo & (v >= M["gancho"] - 3) & (v < M["gancho"] + 2) & (np.abs(u - 16) < 2.2)
    tom[sombra] = np.minimum(tom[sombra], 3)

    # o cós: couro de borda, a linha de cima acesa, a de baixo na sombra
    cos = (v >= M["cos"][0]) & (v < M["cos"][1]) & (u >= M["cos_x"][0]) & (u < M["cos_x"][1])
    mat[cos] = "b"
    tom[cos] = np.where(v[cos] < M["cos"][0] + 1, 3, np.where(v[cos] < M["cos"][1] - 1, 2, 1))
    tom[cos & (u >= 20)] = np.maximum(tom[cos & (u >= 20)] - 1, 0)

    # o barrado: a borda escura, a linha de cima acesa à esquerda
    barra = corpo & (v >= M["barra"][0])
    mat[barra] = "b"
    tom[barra] = np.where(v[barra] < M["barra"][0] + 1, 2, 1)
    tom[barra & (u >= 16.5)] = np.maximum(tom[barra & (u >= 16.5)] - 1, 0)

    # o reforço do joelho: as costuras de cima e de baixo (linhas de borda) e o meio um tom acima
    j0, j1 = M["joelho"]
    # o remendo fica dentro de cada perna: 1 px (no 32) longe das duas beiras
    def dentro_da_perna(lims, mask):
        (fq, dq), (fb, db) = lims
        t = np.clip((v - topo) / (base - topo), 0, 1)
        return mask & (u >= fq + (fb - fq) * t + 1.0) & (u < dq + (db - dq) * t - 1.0)
    remendo_area = (dentro_da_perna(M["perna_esq"], esq) | dentro_da_perna(M["perna_dir"], dir_))
    for vv in (j0, j1):   # a costura tem 1 px em todos os tamanhos: a linha do pixel onde ela cai
        linha = remendo_area & (np.floor(y) == math.floor(vv * s))
        tom[linha] = np.where(u[linha] < 16, 2, 1)
        fixo[linha] = True
    reforco = remendo_area & (v >= j0 + 1) & (v < j1)
    tom[reforco] = np.minimum(tom[reforco] + 1, len(COURO) - 1)
    fixo[reforco] = True

    # a braguilha: o cordão em zigue-zague contínuo de duas cores na fenda (como o gibão), 2 colunas no centro
    b0, b1 = M["bragueta"]
    for yy in range(lado):
        vc = (yy + 0.5) / s
        if not b0 <= vc < b1:
            continue
        k = int(math.floor(vc - b0))
        xs = [xx for xx in range(lado) if 15.0 <= (xx + 0.5) / s < 17.0]
        for i, xx in enumerate(xs):
            mat[yy, xx] = "o"
            tom[yy, xx] = 2 if (i + k) % 2 == 0 else 0
            fixo[yy, xx] = True

    # o desgaste: um ponto raspado no reforço do joelho de fora
    for (gu, gv, gt) in ((11.5, 19.5, 1),):
        xx, yy = int(gu * s), int(gv * s)
        if mat[yy, xx] == "k":
            mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "g", gt, True

    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    # A skill: primeiro a leitura do 32 no jogo; o 64 é o 32 ampliado 2× (como no couro). Os 40 e 48 se derivam das
    # mesmas MEDIDAS depois de o 32 ser aprovado ("--intermediarios" grava a prévia deles, ainda sem retoque).
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, "calca_couro"), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, "calca_couro"), "cores (o 32 ampliado 2×)")
    if "--intermediarios" in sys.argv:
        for lado in (40, 48):
            print(lado, pc.salvar(desenhar(lado), pasta, "calca_couro"), "cores (prévia)")


if __name__ == "__main__":
    main()
