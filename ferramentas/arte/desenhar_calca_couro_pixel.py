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

Medidas no 32 (MEDIDAS); o 64 é o 32 ampliado 2× (como no couro). O 32 foi aprovado (18/10/2026); os 40 e 48 saem
da mesma construção na grade deles: as formas em degraus nas mesmas alturas relativas (o quadril, a fenda do gancho, o
vão que abre), a luz pelas mesmas faixas, as costuras do remendo, o cordão e o contorno com 1 px. O 32 sai igual,
pixel a pixel, ao aprovado.

    python ferramentas/arte/desenhar_calca_couro_pixel.py <pasta> [--intermediarios] [--listas]

--intermediarios grava também os 40 e 48; --listas grava as listas de pixels por camada (CAMADAS) para montar as
fontes em camadas no Aseprite (`montar_fontes.lua` da pasta da proposta).
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
    "gancho": 12.0,               # onde as pernas se separam (a fenda do contorno)
    "quadril": 16.0,              # até aqui o quadril tem a largura do cós; abaixo, a perna recua 1
    "abre": 24.0,                 # daqui à barra o vão entre as pernas abre
    # a luz: cada perna como um cone suave, (x de fora, x de dentro) no quadril e na barra (só para as faixas)
    "luz_esq": ((8.0, 15.5), (9.0, 14.2)),
    "luz_dir": ((16.5, 24.0), (17.8, 23.0)),
    "barra": (28.0, 30.0),        # o barrado: as últimas linhas
    "joelho": (17.0, 21.0),       # o remendo do joelho (das costuras de cima e de baixo), dentro da perna
    "bragueta": (5.0, 11.0),      # a amarração da braguilha (abaixo do cós até perto do gancho)
}


CAMADAS = ["pernas", "remendo", "cos", "barra", "braguilha", "desgaste", "contorno"]   # de baixo para cima


def desenhar(lado, partes=False):
    """A imagem do tamanho; com partes=True, também a camada de cada pixel (CAMADAS), para a fonte do Aseprite."""
    s = lado / 32
    mat, tom, fixo, x, y = pc.grade(lado)
    u, v = x / s, y / s      # o centro de cada pixel em unidades do 32
    M = MEDIDAS
    topo, base = M["cos"][0], M["barra"][1]

    # As pernas em degraus, nas mesmas alturas relativas em todos os tamanhos (as bordas nas linhas e colunas do 32):
    # o quadril até v 16, a perna recuada 1 depois; a fenda do gancho (o contorno, 2 unidades) de v 12 a 24 e o vão
    # aberto (4 unidades) de 24 à barra. Uma afunilada contínua punha o degrau em outra altura em cada grade.
    def limites(lado_esq):
        fora = np.where(v < M["quadril"], M["cos_x"][0], M["cos_x"][0] + 1) if lado_esq else             np.where(v < M["quadril"], M["cos_x"][1], M["cos_x"][1] - 1)
        if lado_esq:
            dentro = np.where(v < M["gancho"], 16, np.where(v < M["abre"], 15, 14))
            return fora, dentro
        dentro = np.where(v < M["gancho"] - 1, 16, np.where(v < M["abre"], 17, 18))
        return dentro, fora

    a_e, b_e = limites(True)
    a_d, b_d = limites(False)
    alto = (v >= topo) & (v < base)
    esq = alto & (u >= a_e) & (u < b_e)
    dir_ = alto & (u >= a_d) & (u < b_d)
    corpo = esq | dir_
    mat[corpo] = "k"

    # a luz em faixas por perna, pela posição de través (0 fora/esquerda, 1 dentro/direita) nas medidas de luz (LUZ:
    # a perna como um cone suave, as faixas do 32 aprovado); a última coluna (a beira) um tom abaixo, pela forma
    def faixas(mask, lims, b_forma, base_tom):
        (fq, dq), (fb, db) = lims
        t = np.clip((v - topo) / (base - topo), 0, 1)
        a, b = fq + (fb - fq) * t, dq + (db - dq) * t
        p = (u - a) / np.maximum(b - a, 1e-6)
        tt = np.where(p < 0.28, base_tom + 1, np.where(p < 0.72, base_tom, base_tom - 1))
        ultima = (u + 1 / s >= b_forma)
        tt = np.where(ultima & (p > 0.5), tt - 1, tt)
        tom[mask] = tt[mask]

    faixas(esq, M["luz_esq"], np.where(v < M["gancho"], 15, b_e), 5)   # acima do gancho a beira é a da braguilha
    faixas(dir_, M["luz_dir"], b_d, 4)
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
    remendo_area = (esq & (u >= a_e + 1.0) & (u < b_e - 1.0)) | (dir_ & (u >= a_d + 1.0) & (u < b_d - 1.0))
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
    camada = np.full(mat.shape, "pernas", dtype=object)
    joelho = remendo_area & (np.floor(y) >= math.floor(j0 * s)) & (np.floor(y) <= math.floor(j1 * s))
    camada[joelho] = "remendo"   # o remendo: as duas costuras e o couro entre elas
    camada[cos] = "cos"
    camada[barra] = "barra"
    # a fenda do gancho fica escura e fechada em todos os tamanhos (no 48 ela tem 3 px e o do meio ficava vazio)
    fenda = (v >= M["gancho"]) & (v < M["abre"]) & (u >= 14.5) & (u < 17.5) & (mat == "")
    mat[fenda] = "c"
    img = pc.imagem(mat, tom, RAMPAS)
    if not partes:
        return img
    camada[mat == "o"] = "braguilha"
    camada[mat == "g"] = "desgaste"
    camada[mat == "c"] = "contorno"
    camada[mat == ""] = ""
    return img, camada


def listas(lado, pasta):
    """As listas de pixels de cada camada ("x,y,RRGGBB;..."), num .lua que faz return (o pintar.lua as lê por dofile:
    o io.open num script do Aseprite pede permissão numa janela)."""
    img, camada = desenhar(lado, partes=True)
    px = np.asarray(img)
    d = pasta / f"calca_couro-{lado}"
    d.mkdir(parents=True, exist_ok=True)
    for c in CAMADAS:
        ys, xs = np.where(camada == c)
        texto = ";".join(f"{x},{y},{px[y, x, 0]:02X}{px[y, x, 1]:02X}{px[y, x, 2]:02X}" for y, x in zip(ys, xs))
        (d / f"{c}.lua").write_text(f'return "{texto}"\n', encoding="utf-8")
    return d


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    # A skill: primeiro a leitura do 32 no jogo; o 64 é o 32 ampliado 2× (como no couro). Os 40 e 48 se derivam das
    # mesmas MEDIDAS depois de o 32 ser aprovado ("--intermediarios" grava a prévia deles, ainda sem retoque).
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, "calca_couro"), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, "calca_couro"), "cores (o 32 ampliado 2×)")
    if "--intermediarios" in sys.argv or "--listas" in sys.argv:
        for lado in (40, 48):
            print(lado, pc.salvar(desenhar(lado), pasta, "calca_couro"), "cores")
    if "--listas" in sys.argv:   # as listas por camada para montar as fontes no Aseprite (montar_fontes.lua)
        for lado in (32, 40, 48):
            print("listas", listas(lado, pasta / "listas"))


if __name__ == "__main__":
    main()
