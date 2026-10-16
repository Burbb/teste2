"""O livro do Mago, quarto candidato: o grimório de estudo (proposta; o jogo usa o sprite 16×16 "livro"). Os candidatos
anteriores ficam intactos ao lado: o fechado (desenhar_livro_pixel.py), o entreaberto (desenhar_grimorio_pixel.py) e
o aberto de duas páginas (desenhar_grimorio_aberto_pixel.py). Pelo método do escudo e do machado (pixel_comum.py),
cada tamanho desenhado na própria grade. Grava os arquivos com o nome "livro" (é o mesmo papel) e só numa pasta dada.

O que o jogo diz (rpg/itens.py): o desenho "livro" é o da arma Grimório e o do apoio Tomo do Mago, em todos os
materiais, e o do único Tomo do Nome Esquecido. O mesmo sprite é também o atalho do Diário (com desenho próprio no
Icones), um talento e o livro da capela: esses papéis não mudam (o item se acha só em Icones.ITEM).

O pedido (Jean, depois do aberto de duas páginas): voltar à pose do entreaberto, de que ele gostou mais, e se espelhar
na referência que ele mandou (um grimório com a capa levantada, o bloco de folhas, a página com anotações e um
diagrama de anéis, a fita pendurada no pé). O que o desenho faz:
  - a pose do entreaberto: o livro deitado, a capa da frente levantada um pouco além da vertical, apoiada para o lado
    da lombada, visto de cima, da frente e da esquerda;
  - a construção que faltava ao entreaberto: o bloco de folhas com espessura (o corte do pé em fios irregulares de
    papel), apoiado na capa de trás, que passa dele e aparece embaixo; a lombada redonda à vista na dobra, ligando a
    capa levantada ao bloco;
  - a capa: couro violeta apagado, gasto onde o couro gasta (as beiras e os cantos mais claros) e, em 48 e 64, umas
    poucas manchas de uso; nada espalhado pelo meio;
  - a página: pergaminho que escurece para a beira, com a beira de fora e a da cabeça um pouco irregulares em 48 e 64;
  - as marcas, de tinta seca: linhas de anotação na metade de cima da página e o diagrama da referência na de baixo:
    dois anéis com o ponto no centro, a linha que os atravessa com uma cruzinha na ponta de cima e duas cruzinhas dos
    lados (em 48 e 64); em 40, os dois anéis, o ponto e a linha; em 32, um anel, o ponto e a linha;
  - a fita vermelho-escura, larga, sai entre as folhas no pé e cai pela frente do bloco, com a ponta cortada;
  - nenhuma luz, partícula, joia ou texto legível.

A construção: o renderizador do aberto de duas páginas (polígonos planos em 3D; cada pixel acha o plano mais perto da
câmera e o ponto 3D dele, de onde vêm o tom pela luz de pixel_comum e as marcas, nas coordenadas da página). A
limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py). O dobro de cada arquivo é a
duplicação exata.

    python ferramentas/arte/desenhar_grimorio_estudo_pixel.py <pasta>
"""

import math
import sys

import numpy as np

from pixel_comum import LUZ, ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)

# As rampas: o couro violeta apagado (o do entreaberto, com o tom de cima mais quente, do couro gasto), o pergaminho,
# a tinta seca e a fita.
COURO = ["#110b17", "#20152b", "#302041", "#422d57", "#553c6c", "#694e80", "#806596", "#a08aa6"]
PAPEL = ["#2b2318", "#4c3f2c", "#6e5a3e", "#8f7652", "#ad946b", "#c6ad84", "#d9c49c", "#e8d8b4"]
TINTA = ["#1c120c", "#3a291c", "#5b4632"]
FITA = ["#1e0a0c", "#3b1418", "#5c1f24", "#7d2c30", "#9d4040"]

# O livro deitado, em unidades do comprimento (L = 1): a largura da página (W), a espessura do bloco de folhas (T),
# a da tábua (tab), o quanto as capas passam do bloco (esq), o raio da lombada (fração da espessura toda), o ângulo
# da capa da frente (graus a partir da página); a câmera (a do entreaberto): o giro e a altura, em graus.
LIVRO = dict(W=0.7, T=0.13, tab=0.026, esq=0.035, lombada=0.62, abre=100.0, giro=-42.0, alt=56.0)
# Por tamanho: a escala (o comprimento do livro na tela, em px), o centro do livro na tela, quantas linhas de
# anotação, o diagrama (1 um anel, 2 dois anéis, 3 com as cruzinhas) e o raio do anel (px), as manchas da capa e a
# beira irregular do papel, e a largura da fita (px).
MEDIDAS = {
    32: dict(esc=21.5, cx=15.4, cy=16.6, linhas=3, diagrama=1, raio=2.4, gasto=0, fita=2.0),
    40: dict(esc=27.0, cx=19.3, cy=20.8, linhas=4, diagrama=1, raio=2.9, gasto=0, fita=2.5),
    48: dict(esc=32.5, cx=23.2, cy=25.0, linhas=5, diagrama=2, raio=3.8, gasto=1, fita=3.0),
    64: dict(esc=43.5, cx=31.0, cy=33.4, linhas=6, diagrama=3, raio=5.0, gasto=1, fita=4.0),
}
# O anel do diagrama em 32 e 40, pixel a pixel (o centro é o meio da grade; o ponto central e o eixo vêm à parte).
DIAGRAMA = {
    32: ["..###..", ".#...#.", "#.....#", "#.....#", "#.....#", ".#...#.", "..###.."],
    40: ["...###...", ".##...##.", ".#.....#.", "#.......#", "#.......#", "#.......#", ".#.....#.", ".##...##.", "...###..."],
}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def camera():
    """Os eixos da tela (direita, cima) e a direção até a câmera (x à direita, y para cima, z da cabeça ao pé: o pé
    em z = 0, perto de quem olha)."""
    g, a = math.radians(LIVRO["giro"]), math.radians(LIVRO["alt"])
    para_camera = np.array([math.sin(g) * math.cos(a), math.sin(a), -math.cos(g) * math.cos(a)])
    direita = np.cross(para_camera, np.array([0.0, 1.0, 0.0]))
    direita /= np.linalg.norm(direita)
    cima = np.cross(direita, para_camera)
    return direita, cima, para_camera


def faces():
    """Os polígonos planos do livro: (nome, material, [pontos 3D]). A lombada em x = 0, o pé em z = 0, a cabeça em
    z = 1; a capa de trás embaixo, o bloco de folhas, e a capa da frente presa na dobra de cima da lombada."""
    W, T, tab, e = LIVRO["W"], LIVRO["T"], LIVRO["tab"], LIVRO["esq"]
    th = math.radians(LIVRO["abre"])
    P = lambda *v: np.array(v, dtype=float)
    Tt = 2 * tab + T
    q = lambda a, b, c, d: [a, b, c, d]
    lista = []
    # a capa de trás: a face de cima (passa do bloco), a beira do pé e a de fora
    lista.append(("tras_cima", "v", q(P(0, tab, -e), P(W + e, tab, -e), P(W + e, tab, 1 + e), P(0, tab, 1 + e))))
    lista.append(("tras_pe", "v", q(P(0, 0, -e), P(W + e, 0, -e), P(W + e, tab, -e), P(0, tab, -e))))
    lista.append(("tras_fora", "v", q(P(W + e, 0, -e), P(W + e, 0, 1 + e), P(W + e, tab, 1 + e), P(W + e, tab, -e))))
    # o bloco de folhas: o corte do pé, o de fora e a primeira página
    lista.append(("bloco_pe", "b", q(P(0, tab, 0), P(W, tab, 0), P(W, tab + T, 0), P(0, tab + T, 0))))
    lista.append(("bloco_fora", "b", q(P(W, tab, 0), P(W, tab, 1), P(W, tab + T, 1), P(W, tab + T, 0))))
    lista.append(("pagina", "p", q(P(0, tab + T, 0), P(W, tab + T, 0), P(W, tab + T, 1), P(0, tab + T, 1))))
    # a lombada: um meio cilindro de couro, da capa de trás até a dobra da capa da frente, para a esquerda; o pé dela
    r, n = Tt / 2, 8
    for k in range(n):
        a0, a1 = -math.pi / 2 - math.pi * k / n, -math.pi / 2 - math.pi * (k + 1) / n
        p0 = P(LIVRO["lombada"] * 2 * r * math.cos(a0) * 0.5, r + r * math.sin(a0), -e)
        p1 = P(LIVRO["lombada"] * 2 * r * math.cos(a1) * 0.5, r + r * math.sin(a1), -e)
        lista.append((f"lombada{k}", "v", q(p0, p1, p1 + P(0, 0, 1 + 2 * e), p0 + P(0, 0, 1 + 2 * e))))
        lista.append((f"lombada_pe{k}", "v", [P(0, r, -e), p0, p1]))
    # a capa da frente: gira na dobra de cima da lombada (x = 0, y = Tt), aberta `abre` graus a partir da página
    dobra = P(0, Tt, -e)
    u = P(math.cos(th), math.sin(th), 0) * (W + e)
    fora = P(-math.sin(th), math.cos(th), 0) * tab
    comp = P(0, 0, 1 + 2 * e)
    lista.append(("capa_fora", "v", q(dobra, dobra + u, dobra + u + comp, dobra + comp)))
    lista.append(("capa_dentro", "v", q(dobra - fora, dobra - fora + u, dobra - fora + u + comp, dobra - fora + comp)))
    lista.append(("capa_beira", "v", q(dobra + u, dobra + u - fora, dobra + u - fora + comp, dobra + u + comp)))
    lista.append(("capa_pe", "v", q(dobra, dobra + u, dobra + u - fora, dobra - fora)))
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
    meio = np.array([W * 0.32, 0.2, 0.5])
    esc = M["esc"]
    tela = lambda p: (M["cx"] + (p - meio) @ direita * esc, M["cy"] - (p - meio) @ cima * esc)
    a_px, b_px = (x - M["cx"]) / esc, -(y - M["cy"]) / esc
    base = meio + a_px[..., None] * direita + b_px[..., None] * cima
    prof = np.full(x.shape, -1e9)
    qual = np.full(x.shape, "", dtype=object)
    pt = np.zeros(x.shape + (3,))
    tons = {}
    for nome, m_, pts in faces():
        nrm = np.cross(pts[1] - pts[0], pts[2] - pts[0])
        nrm /= np.linalg.norm(nrm)
        if nrm @ para_camera < 0:
            nrm = -nrm
        if nrm @ para_camera < 0.02:
            continue
        n_tela = np.array([nrm @ direita, -(nrm @ cima), nrm @ para_camera])
        tons[nome] = float(np.clip(n_tela @ LUZ, 0, 1))
        dentro = dentro_poligono(x, y, [tela(p) for p in pts])
        t = ((pts[0] - base) @ nrm) / (para_camera @ nrm)
        ganha = dentro & (t > prof + 1e-5)
        prof[ganha], qual[ganha] = t[ganha], nome
        pt[ganha] = base[ganha] + t[ganha][..., None] * para_camera
        mat[ganha] = m_
    nomes = qual.astype(str)

    # ---- o couro: o tom pela direção da face; a lombada em faixas (o cilindro), a beira da capa levantada mais clara
    for nome in set(qual[qual != ""]):
        sel = qual == nome
        if mat[sel][0] == "v":
            t_ = int(round(1.8 + 5.2 * tons[nome]))
            if nome == "capa_beira":
                t_ += 1
            tom[sel] = np.clip(t_, 1, 7)
    # a capa de fora: as coordenadas dela (cu, da dobra à beira solta; cv, do pé à cabeça)
    th = math.radians(LIVRO["abre"])
    capa = qual == "capa_fora"
    cu = (pt[..., 0] * math.cos(th) + (pt[..., 1] - (2 * tab + T)) * math.sin(th)) / (W + e)
    cv = (pt[..., 2] + e) / (1 + 2 * e)
    if capa.any():
        t_capa = int(np.median(tom[capa]))
        gasto = capa & ((cu > 0.95) | (cv < 0.035) | (cv > 0.965))   # o couro gasta nas beiras
        tom[gasto] = min(7, t_capa + 1)
        cantos = capa & (cu > 0.86) & ((cv < 0.1) | (cv > 0.9))          # e mais nos cantos soltos
        tom[cantos & ((1 - cu) * 3 + np.minimum(cv, 1 - cv) * 2 < 0.22)] = min(7, t_capa + 2)
        if M["gasto"]:  # umas poucas manchas de uso, longe do meio
            for mu, mv, ra in ((0.78, 0.3, 0.07), (0.62, 0.74, 0.05)):
                mancha = capa & (np.hypot((cu - mu) * W, (cv - mv)) < ra)
                tom[mancha] = np.minimum(7, tom[mancha] + 1)
    # a capa de trás e a lombada, embaixo: a beira do pé um degrau mais escura (vira para baixo)
    tom[(qual == "tras_pe")] = np.maximum(1, tom[(qual == "tras_pe")] - 1)

    # ---- o pergaminho: a página escurece para a beira; o bloco em fios irregulares
    pag = qual == "pagina"
    pu, pv = pt[..., 0] / W, pt[..., 2]                               # pu da lombada à beira; pv do pé à cabeça
    borda = np.minimum.reduce([pu * 1.3, 1 - pu, pv * 1.2, 1 - pv])
    tom[pag] = 6
    tom[pag & (borda < 0.13)] = 5
    tom[pag & (borda < 0.06)] = 4
    tom[pag & (borda < 0.025)] = 3
    tom[pag & (pu < 0.1)] = np.minimum(tom[pag & (pu < 0.1)], 4)        # a sombra da capa levantada e da dobra
    tom[pag & (pu < 0.04)] = 2
    if M["gasto"]:  # a beira de fora e a da cabeça um pouco irregulares (o pergaminho gasto)
        dente = pag & (((pu > 0.985) & (np.sin(pv * 47) > 0.3)) | ((pv > 0.985) & (np.sin(pu * 39 + 1) > 0.4)))
        mat[dente] = ""
    bloco = mat == "b"
    hy = (pt[..., 1] - tab) / T                                       # 0 embaixo, 1 em cima
    onda = 0.35 * np.sin((pu + pv) * 23.0)                           # as folhas não são retas
    fio = (np.floor(hy * T * esc * 1.9 + onda) % 2) == 0
    tom[bloco] = np.where(fio, 4, 3)[bloco]
    tom[bloco & (nomes == "bloco_fora")] -= 1
    tom[bloco & (hy > 0.86)] = 5                                     # a beira de cima do bloco, junto da página
    mat[bloco] = "p"

    # ---- as marcas, de tinta seca, nas coordenadas da página (pu, pv)
    marca = np.zeros(x.shape, dtype=bool)
    # o diagrama: na metade de baixo, para o lado de fora da página. Desenhado redondo na tela (a perspectiva da
    # página achatava o anel numa elipse, que lia como um olho): a posição é a da página, a forma é a de quem olha
    # de frente, como se faz em pixel art pequeno
    sx0, sy0 = tela(np.array([0.7 * W, tab + T, 0.3]))
    sx0, sy0 = math.floor(sx0) + 0.5, math.floor(sy0) + 0.5        # o centro num centro de pixel: o anel simétrico
    raio = M["raio"]
    rr = np.hypot(x - sx0, y - sy0)
    ix, iy = np.floor(x - sx0 + 0.5).astype(int), np.floor(y - sy0 + 0.5).astype(int)   # a posição em relação ao centro
    if lado_img in DIAGRAMA:  # 32 e 40: o anel desenhado pixel a pixel (a conta pelo raio saía dentado, como uma mira)
        desenho = DIAGRAMA[lado_img]
        h = len(desenho) // 2
        anel = np.zeros(x.shape, dtype=bool)
        for yy, linha_d in enumerate(desenho):
            for xx, ch in enumerate(linha_d):
                if ch == "#":
                    anel |= (ix == xx - h) & (iy == yy - h)
        anel &= pag
        centro = pag & (ix == 0) & (iy == 0)
        eixo = pag & (ix == 0) & (iy < -h) & (iy >= -h - 2)
    else:
        anel = pag & (np.abs(rr - raio) < 0.62)
        if M["diagrama"] >= 2:
            anel |= pag & (np.abs(rr - raio * 0.5) < 0.55)
        centro = pag & (rr < 0.5)
        # o eixo atravessa os anéis (fora deles e do centro)
        sai = (np.abs(rr - raio * 0.5) > 0.9) & (rr > 1.2)
        eixo = pag & (np.abs(x - sx0) < 0.5) & (y > sy0 - raio * 1.9) & (y < sy0 + raio * 1.5) & sai
    # as anotações: linhas horizontais na tela (como na referência; as linhas da página, com este ângulo, viravam
    # risquinhos de contagem), de comprimentos variados, perto da cabeça, recortadas pela página
    nx0, ny0 = tela(np.array([0.5 * W, tab + T, 0.8]))
    nx0, ny0 = math.floor(nx0), math.floor(ny0)
    esp = 2 if lado_img < 48 else 2
    for k in range(M["linhas"]):
        comp = (5, 3, 4, 2, 5, 3)[k] * (1 if lado_img < 40 else 1.4 if lado_img < 64 else 1.8)
        yl, xa = ny0 + k * esp, nx0 + k * (1 if lado_img < 48 else 1.5)
        linha = pag & (np.floor(y) == yl) & (x >= xa) & (x < xa + comp) & (x < sx0 - raio - 1.5)
        if lado_img >= 48:
            linha &= ~((np.floor(x) - xa) % 6 == 4)
        marca |= linha
    marca |= anel | centro | eixo
    if M["diagrama"] >= 3:  # as cruzinhas: na ponta de cima do eixo e dos dois lados do anel
        for dx_, dy_ in ((0, -raio * 2.1), (-raio * 1.7, raio * 0.6), (raio * 1.7, raio * 0.6)):
            cx_, cy_ = math.floor(sx0 + dx_) + 0.5, math.floor(sy0 + dy_) + 0.5
            marca |= pag & (((np.abs(x - cx_) < 0.5) & (np.abs(y - cy_) < 1.6)) | ((np.abs(y - cy_) < 0.5) & (np.abs(x - cx_) < 1.6)))
    mat[marca], tom[marca] = "t", 1 if lado_img >= 48 else 2      # as anotações em tinta mais desbotada nos pequenos
    tom[anel | centro] = 0
    fixo[marca] = True

    # ---- a fita: sai entre as folhas no pé, cai pela frente do bloco e pende para fora, com a ponta cortada
    fu = 0.6
    caminho = [np.array([fu * W, tab + T - 0.01, 0.06]), np.array([fu * W, tab + T * 0.7, -0.003]),
               np.array([fu * W + 0.01, tab * 0.3, -0.01]), np.array([fu * W + 0.03, 0.0, -0.13]),
               np.array([fu * W + 0.02, 0.0, -0.2])]
    pts = [tela(p) for p in caminho]
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by_) = pts[i], pts[i + 1]
        sx_, sy_ = bx - ax, by_ - ay
        cl = math.hypot(sx_, sy_) or 1
        tt = np.clip(((x - ax) * sx_ + (y - ay) * sy_) / cl ** 2, 0, 1)
        qx, qy = ax + tt * sx_, ay + tt * sy_
        seg = np.hypot(x - qx, y - qy) <= M["fita"] / 2
        if i == len(pts) - 2:  # a ponta cortada em diagonal
            seg &= ((x - bx) * sx_ + (y - by_) * sy_) / cl < -((x - qx) * -sy_ + (y - qy) * sx_) / cl * 0.9
        mat[seg], tom[seg] = "r", 2 if i in (1, 2) else 3
        claro = seg & ((((x - qx) * -sy_ + (y - qy) * sx_) / cl) < -(M["fita"] / 2 - 0.8))
        tom[claro] = 3 if i in (1, 2) else 4
        fixo[seg] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado_img])
    return imagem(mat, tom, {"v": COURO, "p": PAPEL, "t": TINTA, "r": FITA})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("proposta: diga a pasta (python ferramentas/arte/desenhar_grimorio_estudo_pixel.py <pasta>)")
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"livro-{lado}: {salvar(desenhar(lado), saida, 'livro')} cores")
