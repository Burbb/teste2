"""O livro do Mago, quinto candidato: o grimório fechado da referência do Jean (proposta; o jogo usa o sprite 16×16
"livro"). Feito do zero; os candidatos anteriores ficam como histórico (desenhar_livro_pixel.py,
desenhar_grimorio_pixel.py, desenhar_grimorio_aberto_pixel.py, desenhar_grimorio_estudo_pixel.py). Pelo método do
escudo e do machado (pixel_comum.py), na própria grade. Nesta rodada, só o 64 (o desenho se acerta no tamanho grande
antes de ir para 32, 40 e 48). Grava com o nome "livro" (é o mesmo papel) e só numa pasta dada.

O que o jogo diz (rpg/itens.py): o desenho "livro" é o da arma Grimório e o do apoio Tomo do Mago, em todos os
materiais, e o do único Tomo do Nome Esquecido. O mesmo sprite é também o atalho do Diário (com desenho próprio no
Icones), um talento e o livro da capela: esses papéis não mudam (o item se acha só em Icones.ITEM).

A referência (uma imagem do Jean, só referência: nada dela é reduzido nem copiado): um grimório fechado, deitado na
diagonal, visto de cima em três quartos. O que se preserva, reconstruído por regras na grade:
  - a pose: a lombada à esquerda, descendo da cabeça (em cima à esquerda) até o pé (embaixo); a capa de cima larga,
    em perspectiva; o pé do livro de frente para quem olha, mostrando o bloco de páginas;
  - a capa: couro violeta (puxado para o vinho), com espessura (as tábuas aparecem no pé), quinas e planos de luz
    definidos: a face de cima num tom, as beiras do lado da luz (a cabeça e a da frente) num fio mais claro, a beira
    do pé (a espessura) na sombra;
  - a lombada: um cilindro de couro, mais alto que a capa, com um fio de brilho ao longo e dois reforços de latão em
    volta (os nervos da encadernação), cada um com o lado da luz aceso;
  - o bloco de páginas: papel envelhecido, recuado das capas, com a beira de cima clara e fios de folhas; separado
    das tábuas por uma linha escura;
  - o fecho: uma tira de couro que vem da capa de trás pela beira da frente e uma chapa de latão sobre a capa, com o
    rasgo escuro do pino;
  - as ferragens: cantoneiras de latão envelhecido nos dois cantos soltos, com o rebite;
  - o emblema: um losango gravado em latão no meio da capa, com o crescente e um ponto dentro, só como decoração.

A construção: um modelo em três dimensões de polígonos planos (as tábuas, o bloco, as facetas da lombada e dos
reforços), numa projeção paralela; cada pixel acha o plano mais perto da câmera e o ponto 3D dele: o tom vem da
direção da face em relação à luz de pixel_comum, e o que fica sobre a capa (as beiras, o emblema, as cantoneiras, o
fecho) vem das coordenadas da capa, de modo que acompanha a perspectiva. A limpeza, o contorno de 1 pixel e as
correções são as etapas comuns (pixel_comum.py). O dobro do arquivo é a duplicação exata.

    python ferramentas/arte/desenhar_grimorio_fechado_pixel.py <pasta>
"""

import math
import sys

import numpy as np

from pixel_comum import LUZ, ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (64,)

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
# Por tamanho: a escala (o comprimento do livro na tela, em px) e o centro dele na tela; o emblema em pixels da tela:
# o raio do losango, o ponto e o crescente (em relação ao centro do losango; a linha do meio do desenho é a do centro).
MEDIDAS = {64: dict(esc=38.0, cx=31.5, cy=31.5, losango=7, ponto=(2, 0),
                   # o crescente à mão (a conta com dois círculos virava um "L" nesta grade): "#" o latão, "+" o fio aceso
                   crescente=(" .+#",
                              ".+#.",
                              "+#..",
                              "+#..",
                              "+#..",
                              ".+#.",
                              " .+#"))}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {64: {}}


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
        tom[cima_capa] = t0
        # o chanfro da tábua: uma faixa acesa junto da lombada e da cabeça (as beiras do lado da luz)
        tom[cima_capa & ((u < 0.045) | (v > 1 - 3.2 * px))] = t0 + 1
        beira_luz = cima_capa & ((v > 1 - 1.4 * px) | (u < 0.03))
        tom[beira_luz] = min(8, t0 + 3)
        # o chanfro do lado da sombra: uma faixa mais escura junto do pé e da beira da frente
        tom[cima_capa & ((u > 1 - 2.6 * px / W) | (v < 2.6 * px))] = t0 - 1
        tom[cima_capa & (u > 1 - 1.0 * px / W) & (v > 2.6 * px)] = min(8, t0 + 2)   # a quina da frente pega um fio
        # o emblema gravado: o losango, com o crescente e o ponto dentro. Desenhado em pixels da tela, centrado no
        # meio da capa (onde o meio cai na tela): a linha a 45 graus fica limpa, sem os degraus da perspectiva
        cx_e, cy_e = tela(np.array([0.52 * (W + e), Tt, 0.5]))
        sx, sy = np.floor(x) - math.floor(cx_e), np.floor(y) - math.floor(cy_e)
        R = M["losango"]
        linha = cima_capa & (np.abs(sx) + np.abs(sy) == R)
        cres, cres_luz = np.zeros(x.shape, dtype=bool), np.zeros(x.shape, dtype=bool)
        desenho = M["crescente"]
        for j, fila in enumerate(desenho):
            for i, c in enumerate(fila):
                if c in "#+":
                    aqui = cima_capa & (sx == i - 2) & (sy == j - len(desenho) // 2)
                    cres |= aqui
                    cres_luz |= aqui & (c == "+")
        ponto = cima_capa & (sx == M["ponto"][0]) & (sy == M["ponto"][1])
        grav = linha | cres | ponto
        mat[grav], tom[grav] = "l", 6
        tom[ponto] = 7
        tom[cres_luz] = 7                                                # a borda do crescente do lado da luz
        tom[linha & ((sx < 0) & (sy < 0))] = 7                            # o fio do losango do lado da luz
        tom[linha & ((sx > 0) & (sy > 0))] = 5
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
    tom[lomb & (np.abs(ang - math.radians(140)) < 0.22)] = 7
    tom[lomb & (np.abs(ang - math.radians(140)) < 0.1)] = 8
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
    if len(sys.argv) < 2:
        sys.exit("proposta: diga a pasta (python ferramentas/arte/desenhar_grimorio_fechado_pixel.py <pasta>)")
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"livro-{lado}: {salvar(desenhar(lado), saida, 'livro')} cores")
