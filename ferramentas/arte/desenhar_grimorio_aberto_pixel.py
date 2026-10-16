"""O livro do Mago, terceiro conceito: o grimório aberto, com duas páginas (proposta; o jogo usa o sprite 16×16 "livro").
Os candidatos anteriores ficam intactos ao lado: o fechado (desenhar_livro_pixel.py) e o entreaberto
(desenhar_grimorio_pixel.py). Pelo método do escudo e do machado (pixel_comum.py), cada tamanho desenhado na própria
grade. Grava os arquivos com o nome "livro" (é o mesmo papel) e só numa pasta dada.

O que o jogo diz (rpg/itens.py): o desenho "livro" é o da arma Grimório e o do apoio Tomo do Mago, em todos os
materiais, e o do único Tomo do Nome Esquecido. O mesmo sprite é também o atalho do Diário (com desenho próprio no
Icones), um talento e o livro da capela: esses papéis não mudam (o item se acha só em Icones.ITEM).

O pedido (o retorno de Jean ao entreaberto: a pose lembrava uma folha apoiada numa capa levantada, a página plana, sem
ligação convincente entre capa, lombada e miolo): um livro físico aberto, em diagonal, com duas páginas num "V" suave
ligadas pela dobra, apoiadas sobre a capa; os materiais e a linguagem do entreaberto. O que o desenho faz:
  - as páginas: cada uma é uma curva que mergulha na dobra e se assenta para a borda, feita de poucos planos (a luz
    muda de plano em plano: a faixa que desce para a dobra fica na sombra, a de fora pega a luz); as duas sobem num
    "V" suave a partir da lombada e não são iguais (a da esquerda um pouco mais curva, a fita só de um lado);
  - a dobra: a linha escura no fundo do "V", que desce pelo corte do pé até a lombada;
  - o bloco de folhas: fino, embaixo das páginas, visto no pé e nas bordas de fora, em fios de papel;
  - a capa: couro violeta apagado, aparecendo em volta do bloco (as capas passam um pouco das folhas) e na beira das
    tábuas; a lombada, um meio cilindro de couro embaixo da dobra, aparece no pé;
  - as marcas, de tinta seca: na página da esquerda, grupos de anotação (traços curtos, sem letra); na da direita, um
    diagrama (um anel com o ponto no centro, que forma uma marca também em 32 e 40; em 48 e 64, mais dois pontos
    marcados no anel);
  - a fita vermelho-escura: deitada na dobra, sai pelo pé entre as folhas e cai na mesa, para a frente;
  - nenhuma luz, partícula, joia, texto legível ou símbolo.

A construção: um modelo em três dimensões feito de polígonos planos (cada faixa de página, as faces do bloco, as
capas, a lombada), numa projeção paralela vista de cima e da frente, girada em diagonal. Cada pixel acha o plano mais
perto da câmera e o ponto 3D dele: o tom vem da direção da face em relação à luz de pixel_comum, e o que se desenha na
página (as marcas, os fios do bloco) vem das coordenadas desse ponto, igual em todos os tamanhos. A limpeza, o contorno
de 1 pixel e as correções são as etapas comuns (pixel_comum.py). O dobro de cada arquivo é a duplicação exata.

    python ferramentas/arte/desenhar_grimorio_aberto_pixel.py <pasta>
"""

import math
import sys

import numpy as np

from pixel_comum import LUZ, ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)

# As rampas (as do entreaberto), do mais escuro ao mais claro.
COURO = ["#110b17", "#20152b", "#302041", "#422d57", "#553c6c", "#694e80", "#806596", "#9a80ad"]
PAPEL = ["#2b2318", "#4c3f2c", "#6e5e44", "#8f7d5a", "#ad9a73", "#c6b38a", "#d9c9a1", "#e8dcb9"]
TINTA = ["#1c140e", "#3a2c1f", "#5b4a35"]
FITA = ["#1e0a0c", "#3b1418", "#5c1f24", "#7d2c30", "#9d4040"]

# O livro aberto, em unidades do comprimento da página (L = 1, da cabeça ao pé): a largura de cada página (W), o "V"
# (graus de cada metade acima do horizontal), a espessura do bloco de folhas na borda (bloco), a da tábua (tab), o
# quanto a capa passa das folhas (esq), o perfil de cada página (a altura acima do bloco, em fração de `bloco`, nos
# pontos S, da dobra à borda; a da esquerda um pouco mais curva); a câmera: o giro e a altura, em graus.
LIVRO = dict(W=0.68, V=15.0, bloco=0.07, tab=0.04, esq=0.06, giro=-50.0, alt=56.0)
S = [0.0, 0.05, 0.14, 0.32, 0.62, 1.0]
PERFIL = {-1: [0.0, 0.85, 1.3, 1.55, 1.5, 1.25], 1: [0.0, 0.7, 1.15, 1.4, 1.42, 1.25]}
# Por tamanho: a escala (o comprimento da página na tela, em px), o centro do livro na tela, quantas linhas de
# anotação, o diagrama inteiro (48 e 64) ou simplificado, e a largura da fita (px).
MEDIDAS = {
    32: dict(esc=15.6, cx=16.0, cy=16.2, linhas=3, diagrama=0, fita=1.4),
    40: dict(esc=19.6, cx=20.0, cy=20.4, linhas=3, diagrama=0, fita=1.7),
    48: dict(esc=23.6, cx=24.0, cy=24.5, linhas=4, diagrama=1, fita=2.0),
    64: dict(esc=31.6, cx=32.0, cy=32.6, linhas=5, diagrama=1, fita=2.6),
}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def camera():
    """Os eixos da tela (direita, cima) e a direção até a câmera (x à direita, y para cima, z da cabeça ao pé... o pé
    em z = 0, perto de quem olha)."""
    g, a = math.radians(LIVRO["giro"]), math.radians(LIVRO["alt"])
    para_camera = np.array([math.sin(g) * math.cos(a), math.sin(a), -math.cos(g) * math.cos(a)])
    direita = np.cross(para_camera, np.array([0.0, 1.0, 0.0]))
    direita /= np.linalg.norm(direita)
    cima = np.cross(direita, para_camera)
    return direita, cima, para_camera


def capa_y(s):
    """A altura da face de cima da tábua a `s` (0 na lombada, 1 na borda da página), no "V"."""
    return s * LIVRO["W"] * math.tan(math.radians(LIVRO["V"]))


def pagina_y(lado, s):
    """A altura da página de cima a `s`: a tábua, a tábua e o bloco, e a curva da página."""
    return capa_y(s) + LIVRO["tab"] * 0.2 + LIVRO["bloco"] * float(np.interp(s, S, PERFIL[lado]))


def faces():
    """Os polígonos planos do livro: (nome, material, [pontos 3D]). lado -1 é a página da esquerda, 1 a da direita."""
    W, tab, e = LIVRO["W"], LIVRO["tab"], LIVRO["esq"]
    P = lambda *v: np.array(v, dtype=float)
    lista = []
    for lado in (-1, 1):
        X = lambda s: lado * s * W
        # a capa: a face de cima (passa das folhas na borda, na cabeça e no pé), a beira de fora e a do pé
        se = 1 + e / W
        lista.append((f"capa_cima{lado}", "v", [P(0, capa_y(0), -e), P(X(se), capa_y(se), -e), P(X(se), capa_y(se), 1 + e), P(0, capa_y(0), 1 + e)]))
        lista.append((f"capa_fora{lado}", "v", [P(X(se), capa_y(se), -e), P(X(se), capa_y(se) - tab, -e), P(X(se), capa_y(se) - tab, 1 + e), P(X(se), capa_y(se), 1 + e)]))
        lista.append((f"capa_pe{lado}", "v", [P(0, capa_y(0), -e), P(X(se), capa_y(se), -e), P(X(se), capa_y(se) - tab, -e), P(0, capa_y(0) - tab, -e)]))
        # as faixas da página: entre dois pontos do perfil, da cabeça ao pé
        for k in range(len(S) - 1):
            s0, s1 = S[k], S[k + 1]
            p0, p1 = P(X(s0), pagina_y(lado, s0), 0), P(X(s1), pagina_y(lado, s1), 0)
            lista.append((f"pagina{lado}_{k}", "p", [p0, p1, p1 + P(0, 0, 1), p0 + P(0, 0, 1)]))
        # o bloco de folhas: o corte do pé (do perfil até a tábua) e o corte de fora (na borda)
        sp = np.linspace(0, 1, 13)
        pe = [P(X(s), pagina_y(lado, s), 0) for s in sp] + [P(X(1), capa_y(1), 0), P(0, capa_y(0), 0)]
        lista.append((f"bloco_pe{lado}", "b", pe))
        lista.append((f"bloco_fora{lado}", "b", [P(X(1), pagina_y(lado, 1), 0), P(X(1), capa_y(1), 0), P(X(1), capa_y(1), 1), P(X(1), pagina_y(lado, 1), 1)]))
    # a lombada: o meio cilindro de couro embaixo da dobra, visto no pé
    r = 0.045
    arco = [P(r * math.cos(t), capa_y(0) - tab + 0.004 - 0.75 * r * math.sin(t), -e) for t in np.linspace(0, math.pi, 9)]
    lista.append(("lombada_pe", "v", arco))
    return lista


def dentro_poligono(px, py, poly):
    """Par-ímpar: os pixels (px, py) dentro do polígono [(x, y), ...] na tela."""
    dentro = np.zeros(px.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        cruza = ((y0 > py) != (y1 > py)) & (px < (x1 - x0) * (py - y0) / ((y1 - y0) or 1e-9) + x0)
        dentro ^= cruza
    return dentro


def desenhar(lado_img):
    M = MEDIDAS[lado_img]
    mat, tom, fixo, x, y = grade(lado_img)
    direita, cima, para_camera = camera()
    W = LIVRO["W"]
    meio = np.array([0.0, 0.05, 0.5])
    esc = M["esc"]
    tela = lambda p: (M["cx"] + (p - meio) @ direita * esc, M["cy"] - (p - meio) @ cima * esc)
    # o ponto 3D de cada pixel num plano: p = meio + a*direita + b*cima + t*para_camera
    a_px, b_px = (x - M["cx"]) / esc, -(y - M["cy"]) / esc
    prof = np.full(x.shape, -1e9)
    qual = np.full(x.shape, "", dtype=object)
    pt = np.zeros(x.shape + (3,))
    tons = {}
    for nome, m_, pts in faces():
        nrm = np.cross(pts[1] - pts[0], pts[2] - pts[0])
        if np.linalg.norm(nrm) < 1e-9:
            nrm = np.cross(pts[2] - pts[0], pts[3] - pts[0])
        nrm /= np.linalg.norm(nrm)
        if nrm @ para_camera < 0:
            nrm = -nrm
        if nrm @ para_camera < 0.02:
            continue
        n_tela = np.array([nrm @ direita, -(nrm @ cima), nrm @ para_camera])
        tons[nome] = float(np.clip(n_tela @ LUZ, 0, 1))
        poly = [tela(p) for p in pts]
        dentro = dentro_poligono(x, y, poly)
        # o t do plano: nrm · (meio + a d + b c + t pc - p0) = 0
        base = meio + a_px[..., None] * direita + b_px[..., None] * cima
        t = ((pts[0] - base) @ nrm) / (para_camera @ nrm)
        ganha = dentro & (t > prof + 1e-5)
        prof[ganha], qual[ganha] = t[ganha], nome
        pt[ganha] = base[ganha] + t[ganha][..., None] * para_camera
        mat[ganha] = m_

    luz = lambda nome: tons.get(nome, 0.3)
    # ---- o couro: o tom pela direção da face
    for nome in set(qual[qual != ""]):
        sel = qual == nome
        if mat[sel][0] == "v":
            tom[sel] = int(np.clip(round(1.5 + 5.5 * luz(nome)), 1, 7))
    # ---- as páginas: o tom pela direção de cada faixa (os planos de luz); a dobra escura no fundo do "V"
    for nome in set(qual[qual != ""]):
        sel = qual == nome
        if nome.startswith("pagina"):
            k = int(nome.split("_")[1])
            t_ = int(np.clip(round(2.5 + 5.0 * luz(nome)), 2, 7))
            if k == 0:
                t_ = min(t_, 3)                                    # a faixa que mergulha na dobra
            elif k == 1:
                t_ = min(t_, 5)                                    # a que começa a descer
            tom[sel] = t_
    pag = np.char.startswith(qual.astype(str), "pagina")
    sx = np.abs(pt[..., 0]) / W                                    # 0 na dobra, 1 na borda
    sz = pt[..., 2]                                                # 0 no pé, 1 na cabeça
    dobra = pag & (sx < 0.022 + 0.6 / (esc * W))
    tom[dobra] = 1
    # o papel envelhecido: só a beira (de fora, da cabeça e do pé) escurece um degrau
    beira = pag & ((sx > 0.94) | (sz < 0.035) | (sz > 0.965))
    tom[beira] = np.maximum(2, tom[beira] - 1)
    # ---- o bloco de folhas: fios de papel ao longo da espessura, a dobra descendo até a lombada
    bloco = mat == "b"
    yc = np.array([capa_y(v) for v in sx.ravel()]).reshape(sx.shape)
    frac = np.clip((pt[..., 1] - yc) / LIVRO["bloco"], 0, 1)
    fio = (np.floor(frac * LIVRO["bloco"] * esc * 1.9) % 2) == 0
    tom[bloco] = np.where(fio, 4, 3)[bloco]
    tom[bloco & (qual != "") & np.char.startswith(qual.astype(str), "bloco_fora")] -= 1
    desce = bloco & (sx < 0.03 + 0.7 / (esc * W))
    tom[desce] = 1
    mat[bloco] = "p"
    # ---- as marcas, de tinta seca, nas coordenadas da página
    passo = 1.0 / esc
    esq, dirp = pag & (pt[..., 0] < 0), pag & (pt[..., 0] > 0)
    marca = np.zeros(x.shape, dtype=bool)
    # a página da esquerda: grupos de anotação (linhas ao longo da largura, empilhadas da cabeça ao pé)
    for k in range(M["linhas"]):
        zl = 0.74 - k * (2.0 if lado_img < 48 else 2.3) * passo * 1.25 - (0.06 if k >= 3 else 0)
        comp = 0.72 - 0.16 * (k % 2) - (0.12 if k == M["linhas"] - 1 else 0)
        linha = esq & (np.abs(sz - zl) < 0.55 * passo) & (sx > 0.2) & (sx < 0.2 + comp * 0.72)
        if lado_img >= 48:
            linha &= (np.floor(sx * W * esc + k * 2) % 6) != 0
        marca |= linha
    # a página da direita: o diagrama, um anel com o ponto no centro (uma órbita, um alvo: não é letra nem emblema) e,
    # em 48 e 64, dois pontos marcados no anel
    cu, cz, raio = 0.5, 0.52, max(0.15, 3.3 * passo)
    rr = np.hypot((sx - cu) * W, sz - cz)
    anel = dirp & (np.abs(rr - raio) < 0.62 * passo)
    ponto = np.zeros(x.shape, dtype=bool)                         # o centro: um pixel só (dois viravam um traço)
    if (dirp & (rr < 1.5 * passo)).any():
        ponto[np.unravel_index(np.argmin(np.where(dirp, rr, 9)), rr.shape)] = True
    marca |= anel | ponto
    if M["diagrama"]:  # em 48 e 64, dois pontos marcados no anel (posições numa órbita), em lados diferentes
        for ang in (math.radians(25), math.radians(250)):
            marca |= dirp & (np.hypot((sx - cu) * W - raio * math.cos(ang), (sz - cz) - raio * math.sin(ang)) < 1.15 * passo)
    mat[marca], tom[marca] = "t", 1
    tom[marca & ~(anel | ponto)] = 1
    tom[anel | ponto] = 0
    fixo[marca] = True

    # ---- a fita: deitada na dobra da página da direita, sai pelo pé entre as folhas e cai na mesa, para a frente
    yt = capa_y(0) - LIVRO["tab"] - 0.04                           # a mesa
    caminho = [np.array([0.02, pagina_y(1, 0.03) + 0.004, 0.26]), np.array([0.025, pagina_y(1, 0.04) + 0.004, 0.0]),
               np.array([0.03, yt + 0.02, -0.05]), np.array([0.07, yt, -0.12]), np.array([0.05, yt, -0.16])]
    pts2 = [tela(p) for p in caminho]
    for i in range(len(pts2) - 1):
        (ax, ay), (bx, by_) = pts2[i], pts2[i + 1]
        sx_, sy_ = bx - ax, by_ - ay
        comp = math.hypot(sx_, sy_) or 1
        tt = np.clip(((x - ax) * sx_ + (y - ay) * sy_) / comp ** 2, 0, 1)
        qx, qy = ax + tt * sx_, ay + tt * sy_
        seg = np.hypot(x - qx, y - qy) <= M["fita"] / 2
        mat[seg], tom[seg] = "r", (3 if i == 0 else 2 if i == 1 else 3)
        claro = seg & ((((x - qx) * -sy_ + (y - qy) * sx_) / comp) < -(M["fita"] / 2 - 0.8))
        tom[claro] = 4 if i != 1 else 3
        fixo[seg] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado_img])
    return imagem(mat, tom, {"v": COURO, "p": PAPEL, "t": TINTA, "r": FITA})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("proposta: diga a pasta (python ferramentas/arte/desenhar_grimorio_aberto_pixel.py <pasta>)")
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"livro-{lado}: {salvar(desenhar(lado), saida, 'livro')} cores")
