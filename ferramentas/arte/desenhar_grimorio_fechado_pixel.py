"""O livro do Mago: o grimório fechado da referência do Jean (aprovado; no jogo desde a 1.108.0; antes, o sprite 16×16
"livro"). Feito do zero; os candidatos anteriores, não aprovados, ficam como histórico (desenhar_livro_pixel.py,
desenhar_grimorio_pixel.py, desenhar_grimorio_aberto_pixel.py, desenhar_grimorio_estudo_pixel.py). Pelo método do
escudo e do machado (pixel_comum.py), cada tamanho (32, 40, 48 e 64) na própria grade: o corpo pelas mesmas regras,
na mesma proporção do quadro, e o emblema simplificado para a leitura de cada um (MEDIDAS); o 64 tem o crescente com
a correção do Jean. Grava com o nome "livro" (é o mesmo papel) nos ícones do jogo, ou numa pasta dada.

O que o jogo diz (rpg/itens.py): o desenho "livro" é o da arma Grimório e o do apoio Tomo do Mago, em todos os
materiais, e o do único Tomo do Nome Esquecido. O mesmo sprite é também o atalho do Diário (com desenho próprio no
Icones), um talento e o livro da capela: esses papéis não mudam (o item se acha só em Icones.ITEM).

A referência (uma imagem do Jean, só referência: nada dela é reduzido nem copiado): um grimório fechado, deitado na
diagonal, visto de cima em três quartos. O que se preserva, reconstruído por regras na grade:
  - a pose: a lombada à esquerda, descendo da cabeça (em cima à esquerda) até o pé (embaixo); a capa de cima larga,
    em perspectiva; o pé do livro de frente para quem olha, mostrando o bloco de páginas;
  - a capa: couro violeta (puxado para o vinho), com espessura (as tábuas aparecem no pé), quinas e planos de luz
    definidos: a face de cima levemente abaulada em três planos (o alto junto da cabeça e da lombada aceso, o meio, a
    descida para o pé e a beira da frente na sombra), o brilho só na aresta da cabeça (mais forte junto da lombada), o
    sulco escuro da dobradiça entre a capa e a lombada, a espessura no pé na sombra;
  - a lombada: um cilindro de couro, um fio mais alto que a capa, com dois reforços de latão em volta (os nervos da
    encadernação), cada um com o lado da luz aceso; o brilho do couro em trechos, no meio de cada gomo entre os
    reforços, sem correr a lombada inteira;
  - o bloco de páginas: papel envelhecido, recuado das capas, com a beira de cima clara e fios de folhas; separado
    das tábuas por uma linha escura;
  - o fecho: uma tira de couro que vem da capa de trás pela beira da frente e uma chapa de latão sobre a capa, com o
    rasgo escuro do pino;
  - as ferragens: cantoneiras de latão envelhecido nos dois cantos soltos, com o rebite;
  - o emblema: um losango de latão aplicado no meio da capa, inclinado para conversar com ela (estilizado: a leitura
    vem antes da projeção exata), com o crescente e um ponto dentro, só como decoração.

A construção: um modelo em três dimensões de polígonos planos (as tábuas, o bloco, as facetas da lombada e dos
reforços), numa projeção paralela; cada pixel acha o plano mais perto da câmera e o ponto 3D dele: o tom vem da
direção da face em relação à luz de pixel_comum, e o que fica sobre a capa (as beiras, o emblema, as cantoneiras, o
fecho) vem das coordenadas da capa, de modo que acompanha a perspectiva. A limpeza, o contorno de 1 pixel e as
correções são as etapas comuns (pixel_comum.py). O dobro do arquivo é a duplicação exata.

    python ferramentas/arte/desenhar_grimorio_fechado_pixel.py [pasta]
"""

import math
import sys

import numpy as np

from pixel_comum import LUZ, ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)

# As rampas, do mais escuro ao mais claro: o couro violeta-vinho, o papel envelhecido e o latão (o do escudo).
COURO = ["#14060f", "#230b1c", "#33112a", "#451838", "#582046", "#6c2954", "#833563", "#9c4673", "#b65d86"]
PAPEL = ["#3a2918", "#5d4427", "#85653a", "#a88752", "#c7a76b", "#dcc289", "#ecd9a9", "#f6eac7"]
LATAO = ["#26170a", "#40270c", "#623c12", "#8a571b", "#ae7526", "#cf9737", "#e9bb5c", "#f8dc94", "#fff5d6"]

# O livro deitado, em unidades do comprimento (L = 1, do pé à cabeça): a largura (W), a espessura do bloco (T), a da
# tábua (tab), o quanto as capas passam do bloco (esq), o raio da lombada (fração da espessura toda) e quanto ela passa
# das capas na cabeça e no pé (cabo); os reforços (as posições ao longo da lombada e a largura); a câmera: o giro e a
# altura, em graus.
LIVRO = dict(W=0.74, T=0.22, tab=0.045, esq=0.015, lombada=0.55, cabo=0.0, reforcos=(0.3, 0.68), reforco=0.06,
             giro=-32.0, alt=58.0)
# Por tamanho: a escala (o comprimento do livro na tela, em px; a mesma proporção do quadro em todos) e o centro dele
# na tela; o emblema de cada tamanho, simplificado para a leitura dele.
MEDIDAS = {
    64: dict(esc=38.0, cx=31.5, cy=31.5,
             # o emblema, em pixels da tela a partir do meio da capa (mais emblema_em), estilizado para a leitura: os
             # vértices do losango (o eixo comprido inclinado como a lombada, o curto subindo como a cabeça da capa; os
             # lados em degraus de 2 por 1 e de 1 por 2, as pontas com 2 pixels), o crescente à mão (o da primeira
             # proposta, inclinado com o eixo do losango; "#" o latão, "+" o fio aceso; a linha e a coluna do meio do
             # desenho caem em crescente_em) e o ponto na abertura (None: sem ponto); tudo com 1 pixel de folga ou mais
             emblema_em=(0, 0),
             losango=((-3, -7), (7, -2), (3, 6), (-7, 1)),
             crescente_em=(0, 0),
             crescente=("..+#...",
                        ".+#....",
                        ".+#....",
                        ".+#....",
                        "..+#...",
                        "...+#+."),     # a ponta de baixo volta para a abertura (a correção do Jean)
             ponto=(2, -1)),
    # 48: o losango um passo menor, o crescente de 5 fileiras com a mesma ponta e o ponto
    48: dict(esc=28.5, cx=23.5, cy=23.5, emblema_em=(0, 0),
             losango=((-2, -6), (6, -2), (2, 6), (-6, 2)),
             crescente_em=(0, 0),
             crescente=(".+#..",
                        "+#...",
                        "+#...",
                        ".+#..",
                        "..+#+"),
             ponto=(2, -1)),
    # 40: o losango menor e o crescente de 4 fileiras; o ponto sai (não cabe com folga); um pixel para a lombada,
    # longe do fecho
    40: dict(esc=23.75, cx=19.5, cy=19.5, emblema_em=(-1, 0),
             losango=((-2, -5), (4, -2), (1, 4), (-5, 1)),
             crescente_em=(-1, 0),
             crescente=(".+#",
                        "+#.",
                        "+#.",
                        ".+#"),
             ponto=None),
    # 32: o mesmo losango do 40 e o crescente reduzido a um "C" de 3 fileiras, sem o ponto
    32: dict(esc=19.0, cx=15.5, cy=15.5, emblema_em=(-1, 0),
             losango=((-2, -5), (4, -2), (1, 4), (-5, 1)),
             crescente_em=(-1, 0),
             crescente=(".+#",
                        "+#.",
                        ".+#"),
             ponto=None),
}
# A capa de cima: a largura da beira que arredonda (em fração da largura e do comprimento), a altura da almofada, a
# curvatura do couro inteiro (o alto um pouco para o lado da lombada e da cabeça), o quanto de luz vale um degrau da rampa e até
# onde vai o brilho mais claro da aresta da cabeça, a partir da lombada.
CAPA = dict(borda_u=0.16, borda_v=0.13, altura=0.05, abaulado=1.2, degrau=0.045, quina_luz=0.3)
# A lombada: que parte do comprimento de cada gomo (entre os reforços) leva o fio de luz.
LOMBADA = dict(fio=0.5)
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def camera():
    """Os eixos da tela (direita, cima) e a direção até a câmera (x da lombada para a beira da frente, y para cima,
    z do pé para a cabeça; a câmera fica do lado do pé e da lombada, em cima)."""
    g, a = math.radians(LIVRO["giro"]), math.radians(LIVRO["alt"])
    para_camera = np.array([math.sin(g) * math.cos(a), math.sin(a), -math.cos(g) * math.cos(a)])
    direita = np.cross(para_camera, np.array([0.0, 1.0, 0.0]))
    direita /= np.linalg.norm(direita)
    cima = np.cross(direita, para_camera)
    return direita, cima, para_camera


def caixa(nome, mat_, x0, x1, y0, y1, z0, z1):
    """As seis faces de uma caixa (as que não se veem caem fora pela direção)."""
    P = lambda *v: np.array(v, dtype=float)
    return [
        (f"{nome}_cima", mat_, [P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)]),
        (f"{nome}_pe", mat_, [P(x0, y0, z0), P(x1, y0, z0), P(x1, y1, z0), P(x0, y1, z0)]),
        (f"{nome}_cabeca", mat_, [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]),
        (f"{nome}_frente", mat_, [P(x1, y0, z0), P(x1, y0, z1), P(x1, y1, z1), P(x1, y1, z0)]),
        (f"{nome}_lado", mat_, [P(x0, y0, z0), P(x0, y0, z1), P(x0, y1, z1), P(x0, y1, z0)]),
    ]


def cilindro(nome, mat_, r, rx, yc, z0, z1, n=10):
    """Meio cilindro para a esquerda (a lombada): facetas da base até o topo, e as tampas no pé e na cabeça."""
    P = lambda *v: np.array(v, dtype=float)
    lista = []
    angs = [-math.pi / 2 - math.pi * k / n for k in range(n + 1)]
    pts = [(rx * math.cos(a), yc + r * math.sin(a)) for a in angs]
    for k in range(n):
        (xa, ya), (xb, yb) = pts[k], pts[k + 1]
        lista.append((f"{nome}{k}", mat_, [P(xa, ya, z0), P(xb, yb, z0), P(xb, yb, z1), P(xa, ya, z1)]))
    lista.append((f"{nome}_tampa_pe", mat_, [P(0, yc, z0)] + [P(px, py, z0) for px, py in pts]))
    lista.append((f"{nome}_tampa_cabeca", mat_, [P(0, yc, z1)] + [P(px, py, z1) for px, py in pts]))
    return lista


def faces():
    W, T, tab, e = LIVRO["W"], LIVRO["T"], LIVRO["tab"], LIVRO["esq"]
    Tt = 2 * tab + T
    lista = []
    lista += caixa("tras", "v", 0, W + e, 0, tab, -e, 1 + e)                     # a capa de trás
    lista += caixa("bloco", "p", 0, W, tab, tab + T, 0, 1)                         # o bloco de páginas
    lista += caixa("capa", "v", 0, W + e, tab + T, Tt, -e, 1 + e)                  # a capa de cima
    r = Tt / 2 + 0.006                                                            # a lombada, um fio mais alta que a capa
    c = LIVRO["cabo"]
    lista += cilindro("lombada", "v", r, LIVRO["lombada"] * 2 * r * 0.55, Tt / 2, -e - c, 1 + e + c)
    for i, zr in enumerate(LIVRO["reforcos"]):                                    # os reforços de latão em volta
        h = LIVRO["reforco"] / 2
        lista += cilindro(f"reforco{i}_", "l", r + 0.012, LIVRO["lombada"] * 2 * (r + 0.012) * 0.55, Tt / 2, zr - h, zr + h)
    # o fecho: a chapa de latão, com espessura, sobre a capa e passando da beira da frente
    lista += caixa("chapa", "l", W - 0.08, W + e + 0.035, Tt, Tt + 0.014, 0.43, 0.57)
    return lista


def lado_losango(a, b):
    """Os pixels de um lado do losango, de um vértice inteiro ao outro, em degraus iguais (2 por 1, 1 por 2...) que
    começam no vértice: as pontas saem iguais, sem o degrau curto que a reta de Bresenham deixa numa delas."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    sx, sy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
    if abs(dx) >= abs(dy):
        r = abs(dx) // max(1, abs(dy))
        return [(x0 + k * sx, y0 + min(k // r, abs(dy)) * sy) for k in range(abs(dx) + 1)]
    r = abs(dy) // max(1, abs(dx))
    return [(x0 + min(k // r, abs(dx)) * sx, y0 + k * sy) for k in range(abs(dy) + 1)]


def dentro_poligono(px, py, poly):
    """Par-ímpar: os pixels (px, py) dentro do polígono [(x, y), ...] na tela."""
    dentro = np.zeros(px.shape, dtype=bool)
    for i in range(len(poly)):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % len(poly)]
        dentro ^= ((y0 > py) != (y1 > py)) & (px < (x1 - x0) * (py - y0) / ((y1 - y0) or 1e-9) + x0)
    return dentro


def desenhar(lado_img):
    M = MEDIDAS[lado_img]
    mat, tom, fixo, x, y = grade(lado_img)
    direita, cima, para_camera = camera()
    W, T, tab, e = LIVRO["W"], LIVRO["T"], LIVRO["tab"], LIVRO["esq"]
    Tt = 2 * tab + T
    meio = np.array([W * 0.42, Tt / 2, 0.5])
    esc = M["esc"]
    tela = lambda p: (M["cx"] + (p - meio) @ direita * esc, M["cy"] - (p - meio) @ cima * esc)
    a_px, b_px = (x - M["cx"]) / esc, -(y - M["cy"]) / esc
    base = meio + a_px[..., None] * direita + b_px[..., None] * cima
    prof = np.full(x.shape, -1e9)
    qual = np.full(x.shape, "", dtype=object)
    pt = np.zeros(x.shape + (3,))
    luz = {}
    for nome, m_, pts in faces():
        nrm = np.cross(pts[1] - pts[0], pts[2] - pts[0])
        if np.linalg.norm(nrm) < 1e-12:
            nrm = np.cross(pts[2] - pts[0], pts[3] - pts[0])
        nrm /= np.linalg.norm(nrm)
        if nrm @ para_camera < 0:
            nrm = -nrm
        if nrm @ para_camera < 0.02:
            continue
        n_tela = np.array([nrm @ direita, -(nrm @ cima), nrm @ para_camera])
        luz[nome] = float(np.clip(n_tela @ LUZ, 0, 1))
        dentro = dentro_poligono(x, y, [tela(p) for p in pts])
        t = ((pts[0] - base) @ nrm) / (para_camera @ nrm)
        ganha = dentro & (t > prof + 1e-6)
        prof[ganha], qual[ganha] = t[ganha], nome
        pt[ganha] = base[ganha] + t[ganha][..., None] * para_camera
        mat[ganha] = m_
    nomes = qual.astype(str)
    X, Y, Z = pt[..., 0], pt[..., 1], pt[..., 2]

    # ---- os tons, um por plano, decididos (a conta pela luz deixava a capa quase toda clara): a capa de cima no meio da
    # rampa, as espessuras na sombra, a lombada pela curva (o lado que olha para a luz mais claro), o latão pela luz
    for nome in set(nomes[nomes != ""]):
        sel = nomes == nome
        m_ = mat[sel][0]
        if m_ == "v":
            if nome.startswith("lombada"):
                tom[sel] = int(np.clip(round(1.5 + 5.0 * luz[nome]), 1, 6))
            elif nome.endswith("_cima"):
                tom[sel] = 4
            else:
                tom[sel] = 2
        elif m_ == "l":
            tom[sel] = int(np.clip(round(2.0 + 5.5 * luz[nome]), 2, 7))

    # ---- a capa de cima: o plano num tom, as beiras do lado da luz acesas, a do pé e a da frente em sombra
    cima_capa = nomes == "capa_cima"
    if cima_capa.any():
        t0 = int(np.median(tom[cima_capa]))
        u = X / (W + e)                                                # 0 na lombada, 1 na beira da frente
        v = (Z + e) / (1 + 2 * e)                                      # 0 no pé, 1 na cabeça
        px = 1.0 / esc
        # o couro levemente abaulado (uma almofada): a altura sobe das beiras para o meio e, de leve, do canto da
        # frente no pé para o da lombada na cabeça; a luz (a de pixel_comum) sobre a normal dessa forma vira poucos
        # planos: o meio no tom da capa, a subida para a cabeça e a lombada um degrau acima, a descida para o pé e a
        # beira da frente um degrau abaixo
        bu = np.clip(u / CAPA["borda_u"], 0, 1)
        bf = np.clip((1 - u) / CAPA["borda_u"], 0, 1)
        bv = np.clip(v / CAPA["borda_v"], 0, 1)
        bc = np.clip((1 - v) / CAPA["borda_v"], 0, 1)
        sobe = lambda b: 1 - (1 - b) ** 2                               # a beira que arredonda
        dsobe = lambda b: 2 * (1 - b)
        hu, hv = sobe(bu) * sobe(bf), sobe(bv) * sobe(bc)
        dh_du = (dsobe(bu) / CAPA["borda_u"] * (bu < 1) * sobe(bf) - dsobe(bf) / CAPA["borda_u"] * (bf < 1) * sobe(bu)) * hv
        dh_dv = (dsobe(bv) / CAPA["borda_v"] * (bv < 1) * sobe(bc) - dsobe(bc) / CAPA["borda_v"] * (bc < 1) * sobe(bv)) * hu
        # e o abaulado do couro inteiro, com o alto um pouco para o lado da lombada e da cabeça
        dh_du = dh_du - 2 * CAPA["abaulado"] * (u - 0.4)
        dh_dv = dh_dv - 2 * CAPA["abaulado"] * (v - 0.6)
        k = CAPA["altura"]
        nx, ny, nz = -k * dh_du / (W + e), np.ones_like(u), -k * dh_dv / (1 + 2 * e)
        nn = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
        n_tela = np.stack([(nx * direita[0] + ny * direita[1] + nz * direita[2]) / nn,
                           -(nx * cima[0] + ny * cima[1] + nz * cima[2]) / nn,
                           (nx * para_camera[0] + ny * para_camera[1] + nz * para_camera[2]) / nn], axis=-1)
        L = n_tela @ LUZ
        plano = np.array([direita[1], -cima[1], para_camera[1]]) @ LUZ
        degrau = np.clip(np.round((L - plano) / CAPA["degrau"]), -1, 1).astype(int)
        tom[cima_capa] = (t0 + degrau)[cima_capa]
        # as arestas: só as voltadas para a luz pegam brilho, e concentrado. A da cabeça num fio, mais claro junto da
        # quina da lombada (a que mais olha para a luz) e apagando para a frente; junto da lombada, o sulco da
        # dobradiça (a sombra de construção entre a lombada e a capa)
        cabeca = cima_capa & (v > 1 - 1.2 * px)
        tom[cabeca] = t0 + 2
        tom[cabeca & (u < CAPA["quina_luz"])] = t0 + 3
        tom[cabeca & (u > 0.72)] = t0 + 1
        da_lombada = np.char.startswith(nomes, "lombada") | np.char.startswith(nomes, "reforco")
        encosta = np.zeros(x.shape, dtype=bool)
        for dy_, dx_ in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            encosta |= np.roll(da_lombada, (dy_, dx_), axis=(0, 1))
        sulco = cima_capa & encosta & (u < 0.2)                           # o sulco: o pixel da capa encostado na lombada
        tom[sulco] = t0 - 2
        tom[sulco & (v > 1 - 1.2 * px)] = t0 + 2
        fixo[sulco | cabeca] = True                                     # traços de 1 pixel: a limpeza não os apaga
        # o emblema aplicado no couro: o losango (os lados entre os vértices), o crescente e o ponto, a partir do meio
        # da capa na tela; as linhas do lado da luz (a da cabeça e a da lombada) acesas, as do
        # outro lado mais baixas, e o sulco escuro embaixo, que assenta a peça no couro
        cx_e, cy_e = tela(np.array([0.52 * (W + e), Tt, 0.5]))
        sx = np.floor(x) - math.floor(cx_e) - M["emblema_em"][0]
        sy = np.floor(y) - math.floor(cy_e) - M["emblema_em"][1]
        vert = M["losango"]
        linha, linha_luz = np.zeros(x.shape, dtype=bool), np.zeros(x.shape, dtype=bool)
        for k in range(4):
            for qx, qy in lado_losango(vert[k], vert[(k + 1) % 4]):
                aqui = (sx == qx) & (sy == qy)
                linha |= aqui
                if k in (0, 3):                                        # a da cabeça e a da lombada
                    linha_luz |= aqui
        linha &= cima_capa
        cres, cres_luz = np.zeros(x.shape, dtype=bool), np.zeros(x.shape, dtype=bool)
        desenho = M["crescente"]
        for j, fila in enumerate(desenho):
            for i, c in enumerate(fila):
                if c in "#+":
                    aqui = cima_capa & (sx == i - len(fila) // 2 + M["crescente_em"][0]) & \
                        (sy == j - len(desenho) // 2 + M["crescente_em"][1])
                    cres |= aqui
                    cres_luz |= aqui & (c == "+")
        ponto = np.zeros(x.shape, dtype=bool)                            # (os tamanhos pequenos ficam sem o ponto)
        if M["ponto"]:
            ponto = cima_capa & (sx == M["ponto"][0]) & (sy == M["ponto"][1])
        grav = linha | cres | ponto
        mat[grav], tom[grav] = "l", 5
        tom[linha & linha_luz] = 6
        tom[cres] = 6
        tom[cres_luz | ponto] = 7
        sombra = cima_capa & ~grav & np.roll(grav, 1, axis=0) & np.roll(grav, 1, axis=1)
        tom[sombra] = np.maximum(1, tom[sombra] - 2)                    # o sulco da gravação, embaixo à direita
        fixo[grav] = True
        # as cantoneiras de latão nos cantos soltos (a beira da frente na cabeça e no pé), com o rebite
        for vc in (0.0, 1.0):
            d_canto = (1 - u) * (W + e) + np.abs(v - vc) * (1 + 2 * e)
            canto = cima_capa & (d_canto < 0.17)
            mat[canto], tom[canto] = "l", 5
            tom[canto & (d_canto > 0.135)] = 3
            rebite = canto & (np.hypot((1 - u) * (W + e) - 0.045, np.abs(v - vc) * (1 + 2 * e) - 0.045) < 1.1 * px)
            tom[rebite] = 8 if vc == 1 else 7
            fixo[canto] = True
        # o fecho: a tira de couro sob a chapa (passa da chapa para dentro da capa, mais escura)
        tira = cima_capa & (u > 0.8) & (u < 0.9) & (np.abs(v - 0.5) < 0.05)
        tom[tira] = t0 - 2
        fixo[tira] = True
    # a chapa: a face de cima acesa na beira da luz, o rasgo escuro do pino; a borda do pé em sombra
    chapa = nomes == "chapa_cima"
    if chapa.any():
        cu2 = (X - (W - 0.08)) / (e + 0.115)
        cv2 = (Z - 0.43) / 0.14
        tom[chapa] = 5
        tom[chapa & ((cu2 < 0.12) | (cv2 > 0.85))] = 7
        tom[chapa & ((cu2 > 0.9) | (cv2 < 0.12))] = 4
        tom[chapa & (np.abs(cu2 - 0.48) < 0.09) & (np.abs(cv2 - 0.5) < 0.25)] = 1
    fixo[np.char.startswith(nomes, "chapa")] = True

    # ---- a espessura das capas no pé e a capa de trás: um degrau abaixo, a quina de cima com um fio
    for nome in ("capa_pe", "tras_pe", "capa_lado"):
        sel = nomes == nome
        tom[sel & (Y > (Tt if "capa" in nome else tab) - 0.012)] = np.minimum(8, tom[sel & (Y > (Tt if "capa" in nome else tab) - 0.012)] + 1)
    # a cantoneira do pé desce pela espessura da capa
    canto_pe = (nomes == "capa_pe") & (X > W + e - 0.1)
    mat[canto_pe], tom[canto_pe] = "l", 4
    fixo[canto_pe] = True

    # ---- a lombada: um fio de brilho ao longo do cilindro (o couro curvo pega a luz numa faixa)
    lomb = np.char.startswith(nomes, "lombada") & ~np.char.endswith(nomes, "tampa_pe")
    rl = Tt / 2 + 0.006
    rx = LIVRO["lombada"] * 2 * rl * 0.55
    ang = np.arctan2((Y - Tt / 2) / rl, X / rx)                         # o ângulo em volta do eixo (na elipse)
    # o brilho não corre a lombada inteira: cada trecho entre os reforços (e as pontas) é um gomo de couro estufado,
    # com o fio de luz só no meio dele; perto dos reforços e das pontas o fio apaga para o tom do lado da luz
    fio = lomb & (np.abs(ang - math.radians(140)) < 0.24)
    cortes = [-e] + [zr for zr in LIVRO["reforcos"]] + [1 + e]
    meio_gomo = np.zeros(x.shape, dtype=bool)
    for z0, z1 in zip(cortes[:-1], cortes[1:]):
        zm, meia = (z0 + z1) / 2, (z1 - z0) / 2
        meio_gomo |= (np.abs(Z - zm) < meia * LOMBADA["fio"])
    tom[fio] = 6
    tom[fio & meio_gomo] = 7
    # o pé da lombada não é maciço: a casca de couro faz a curva por fora e, dentro dela, o maço de folhas dobra
    tampa = nomes == "lombada_tampa_pe"
    dentro = tampa & ((X / rx) ** 2 + ((Y - Tt / 2) / rl) ** 2 < 0.45)
    tom[tampa] = 2
    mat[dentro], tom[dentro] = "p", 3
    # os reforços: o lado da luz aceso, uma sombra no couro logo abaixo de cada um
    for i, zr in enumerate(LIVRO["reforcos"]):
        h = LIVRO["reforco"] / 2
        sob = lomb & (Z < zr - h) & (Z > zr - h - 0.03)
        tom[sob] = np.maximum(1, tom[sob] - 2)
        ref = np.char.startswith(nomes, f"reforco{i}_")
        tom[ref & (np.abs(ang - math.radians(140)) < 0.3)] = 8

    # ---- o bloco de páginas, por coluna de pixels, de cima para baixo: a fresta escura sob a capa, o fio aceso das
    # folhas de cima, as folhas em dois tons alternados (o maço) e a última fileira na sombra da capa de trás
    pag = mat == "p"
    for coluna in range(lado_img):
        fil = np.nonzero(pag[:, coluna])[0]
        if len(fil) == 0:
            continue
        tons = [1, 6] + [5 if k % 2 == 0 else 4 for k in range(len(fil) - 3)] + [3]
        tom[fil, coluna] = tons[:len(fil)] if len(fil) >= 3 else [6, 4][:len(fil)]
    tom[pag & (X > W - 0.03)] = np.minimum(tom[pag & (X > W - 0.03)], 4)   # a quina da frente vira para a sombra
    fixo[pag] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado_img])
    return imagem(mat, tom, {"v": COURO, "p": PAPEL, "l": LATAO})


if __name__ == "__main__":
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"livro-{lado}: {salvar(desenhar(lado), saida, 'livro')} cores")
