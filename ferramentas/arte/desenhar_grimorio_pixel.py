"""O livro do Mago, segundo conceito: o grimório entreaberto (proposta; o jogo usa o sprite 16×16 "livro"; o primeiro
candidato, o livro fechado de desenhar_livro_pixel.py, fica intacto ao lado). Pelo método do escudo e do machado
(pixel_comum.py), cada tamanho desenhado na própria grade. Grava os arquivos com o nome "livro" (é o mesmo papel).

O que o jogo diz (rpg/itens.py): o desenho "livro" é o da arma Grimório e o do apoio Tomo do Mago, em todos os
materiais (de Enferrujado a Rúnico: as ferragens), e o do único Tomo do Nome Esquecido ("As páginas estão em branco
até você sangrar nelas."). O mesmo sprite é também o atalho do Diário (com desenho próprio no Icones), um talento e o
livro da capela: esses papéis não mudam (o item se acha só em Icones.ITEM).

O pedido (o retorno de Jean ao livro fechado: "lembra uma agenda de couro com fecho"; pesado e genérico):
personalidade de equipamento de mago pela composição, pelos materiais e pelos sinais de uso, sem luz, partícula nem
joia. O que o desenho faz:
  - entreaberto, em três quartos: o livro deitado, a capa da frente levantada um pouco além da vertical, apoiada para
    o lado da lombada; de cima, da frente e da esquerda se vê a capa por fora (o couro), a lombada embaixo dela e a
    primeira página inteira;
  - fino (o miolo tem 3/4 da espessura do candidato fechado, sem bloco);
  - couro violeta apagado; a beira solta da capa com uns poucos dentes (em 40 um, em 48 e 64 dois): o gasto fica na
    beira, não espalhado;
  - a página em papel envelhecido, que escurece só na beira e na sombra da capa, com poucos grupos de marcas de tinta
    seca: linhas de anotação (traços curtos, sem letra; um grupo em 32, dois em 40, 48 e 64) e, em 48 e 64, onde cabe,
    um diagrama abstrato (um círculo fino com dois pontos e a reta que os une); um círculo de 4 pixels em 32 e 40
    viraria letra, por isso fica de fora;
  - a fita de tecido vermelho escuro sai do pé do miolo e cai na mesa, para a frente: entra na silhueta;
  - ferragens discretas: cantoneiras de ferro escuro nos cantos soltos da capa, com a quina acesa.

A construção: um modelo do livro em três dimensões (a capa de trás e o miolo deitados, a lombada em meio cilindro à
esquerda, a capa da frente presa na dobra de cima da lombada e aberta num ângulo), visto numa projeção paralela e
rasterizado na grade de cada tamanho: cada face é um paralelogramo com coordenadas próprias (u, v), e o que se desenha
nela (o tom pela direção da face em relação à luz de pixel_comum, as marcas da página, os dentes, as cantoneiras) vem
dessas coordenadas. As faces se pintam pela profundidade. A limpeza, o contorno de 1 pixel e as correções são as
etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/arte/desenhar_grimorio_pixel.py <pasta>    (grava noutra pasta: a proposta)
"""

import math
import sys

import numpy as np

from pixel_comum import LUZ, ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)

# As rampas, do mais escuro ao mais claro: o couro violeta apagado, o papel envelhecido, a fita e o ferro.
COURO = ["#110b17", "#20152b", "#302041", "#422d57", "#553c6c", "#694e80", "#806596", "#9a80ad"]
PAPEL = ["#2b2318", "#4c3f2c", "#6e5e44", "#8f7d5a", "#ad9a73", "#c6b38a", "#d9c9a1", "#e8dcb9"]
TINTA = ["#1c140e", "#3a2c1f", "#5b4a35"]      # as marcas na página: a tinta seca, de escura a desbotada
FITA = ["#1e0a0c", "#3b1418", "#5c1f24", "#7d2c30", "#9d4040"]
FERRO = ["#101114", "#22252b", "#3a3e46", "#5a606a", "#8c939d"]

# O livro, deitado, em unidades do comprimento (1): a largura (W), a espessura do miolo (T), a da tábua (tab), o quanto
# as capas passam do miolo (esq), o ângulo da capa da frente (graus a partir da página: passa da vertical e se apoia
# para trás, do lado da lombada); a câmera: o giro (para a esquerda, negativo) e a altura (alt), em graus.
LIVRO = dict(W=0.72, T=0.075, tab=0.02, esq=0.022, abre=100.0, giro=-42.0, alt=56.0)
# Por tamanho: a escala (o comprimento do livro na tela, em px), o centro do livro na tela (cx, cy) e o que liga ou
# desliga: quantas linhas de anotação, os dentes na beira da capa (48 e 64; em 40 um só) e a largura da fita.
MEDIDAS = {
    32: dict(esc=21.0, cx=15.0, cy=17.4, linhas=2, dentes=0, fita=1.4),
    40: dict(esc=26.5, cx=18.9, cy=21.8, linhas=3, dentes=0, fita=1.8),
    48: dict(esc=32.0, cx=22.8, cy=26.2, linhas=3, dentes=1, fita=2.1),
    64: dict(esc=42.5, cx=30.4, cy=35.0, linhas=4, dentes=1, fita=2.8),
}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def camera():
    """Os eixos da tela (direita, cima) e a direção até a câmera, numa projeção paralela (x à direita, y para cima,
    z para o fundo: a câmera fica na frente, z negativo)."""
    g, a = math.radians(LIVRO["giro"]), math.radians(LIVRO["alt"])
    para_camera = np.array([math.sin(g) * math.cos(a), math.sin(a), -math.cos(g) * math.cos(a)])
    direita = np.cross(para_camera, np.array([0.0, 1.0, 0.0]))
    direita /= np.linalg.norm(direita)
    cima = np.cross(direita, para_camera)
    return direita, cima, para_camera


def faces():
    """As faces do livro deitado: (nome, material, origem, eixo u, eixo v), paralelogramos em 3D. A lombada em x = 0,
    o pé em z = 0 (perto de quem olha), a cabeça em z = 1; a capa de trás embaixo, o miolo, e a capa da frente presa na
    dobra de cima da lombada, aberta."""
    W, T, tab, e = LIVRO["W"], LIVRO["T"], LIVRO["tab"], LIVRO["esq"]
    th = math.radians(LIVRO["abre"])
    P = lambda *v: np.array(v, dtype=float)
    Tt = 2 * tab + T
    lista = []
    # a capa de trás: as beiras (do pé e da frente) passam um pouco do miolo
    lista.append(("tabua_tras_pe", "v", P(0, 0, 0), P(W + e, 0, 0), P(0, tab, 0)))
    lista.append(("tabua_tras_frente", "v", P(W + e, 0, 0), P(0, 0, 1), P(0, tab, 0)))
    lista.append(("tabua_tras_cima", "v", P(0, tab, 0), P(W + e, 0, 0), P(0, 0, 1)))
    # o miolo: o corte do pé (a espessura, em fios) e a primeira página, de cima
    lista.append(("corte_pe", "p", P(0, tab, e), P(W, 0, 0), P(0, T, 0)))
    lista.append(("corte_frente", "p", P(W, tab, e), P(0, 0, 1 - 2 * e), P(0, T, 0)))
    lista.append(("pagina", "p", P(0, tab + T, e), P(W, 0, 0), P(0, 0, 1 - 2 * e)))
    # a lombada: um meio cilindro (achatado) em facetas, para a esquerda, de baixo até a dobra da capa da frente
    r = Tt / 2
    n = 6
    for k in range(n):
        a0, a1 = -math.pi / 2 - math.pi * k / n, -math.pi / 2 - math.pi * (k + 1) / n
        p0 = P(0.7 * r * math.cos(a0), r + r * math.sin(a0), 0)
        p1 = P(0.7 * r * math.cos(a1), r + r * math.sin(a1), 0)
        lista.append((f"lombada{k}", "v", p0, P(0, 0, 1), p1 - p0))
        lista.append((f"lombada_pe{k}", "v", P(0, r, 0), p0 - P(0, r, 0), p1 - p0))
    # a capa da frente: gira na dobra de cima da lombada (x = 0, y = Tt), aberta `abre` graus a partir da página
    dobra = P(0, Tt, 0)
    u_capa = P(math.cos(th), math.sin(th), 0) * (W + e)
    fora = P(-math.sin(th), math.cos(th), 0) * tab
    lista.append(("capa_dentro", "v", dobra - fora, u_capa, P(0, 0, 1)))
    lista.append(("capa_fora", "v", dobra, u_capa, P(0, 0, 1)))
    lista.append(("capa_beira", "v", dobra - fora + u_capa, fora, P(0, 0, 1)))
    lista.append(("capa_pe", "v", dobra - fora, u_capa, fora))
    return lista


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    direita, cima, para_camera = camera()
    prof = np.full(x.shape, -1e9)
    qual = np.full(x.shape, "", dtype=object)
    uu, vv = np.zeros(x.shape), np.zeros(x.shape)
    W, T, tab, e = LIVRO["W"], LIVRO["T"], LIVRO["tab"], LIVRO["esq"]
    meio = np.array([W * 0.3, 0.2, 0.5])
    tela = lambda p: (M["cx"] + (p - meio) @ direita * M["esc"], M["cy"] - (p - meio) @ cima * M["esc"])
    tons = {}
    for nome, m_, o, eu, ev in faces():
        nrm = np.cross(eu, ev)
        nrm /= np.linalg.norm(nrm)
        if nrm @ para_camera < 0:
            nrm = -nrm
        # a luz é a de pixel_comum (na tela: x à direita, y para baixo, z para quem olha)
        n_tela = np.array([nrm @ direita, -(nrm @ cima), nrm @ para_camera])
        tons[nome] = float(np.clip(n_tela @ LUZ, 0, 1))
        ox, oy = tela(o)
        ux, uy = tela(o + eu)[0] - ox, tela(o + eu)[1] - oy
        vx, vy = tela(o + ev)[0] - ox, tela(o + ev)[1] - oy
        det = ux * vy - uy * vx
        if abs(det) < 1e-3:
            continue
        dx, dy = x - ox, y - oy
        u = (dx * vy - dy * vx) / det
        v = (ux * dy - uy * dx) / det
        dentro = (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1)
        z_cam = (u[..., None] * eu + v[..., None] * ev + o) @ para_camera
        ganha = dentro & (z_cam > prof + 1e-4)
        prof[ganha], qual[ganha], uu[ganha], vv[ganha] = z_cam[ganha], nome, u[ganha], v[ganha]
        mat[ganha] = m_

    # ---- o couro (capa, lombada, tábuas): o tom pela direção da face
    for nome in set(qual[qual != ""]):
        sel = qual == nome
        if mat[sel][0] == "v":
            t_ = int(round(2.0 + 5.5 * tons[nome]))
            if "beira" in nome:
                t_ = min(7, t_ + 1)                                # a beira solta da capa pega a luz
            tom[sel] = np.clip(t_, 1, 7)
    # a capa de fora: plana, com a beira solta um degrau mais clara e (em 48 e 64) uns poucos dentes na beira solta
    capa = qual == "capa_fora"
    if capa.any():
        t_capa = int(np.median(tom[capa]))
        tom[capa & (uu > 0.94)] = min(7, t_capa + 1)
        tom[capa & ((vv < 0.03) | (vv > 0.97))] = min(7, t_capa + 1)
        # a beira solta um pouco irregular: uns poucos dentes (couro gasto na beira, não no meio)
        if M["dentes"] or lado >= 40:
            for v_d in ((0.3, 0.71) if lado >= 48 else (0.55,)):
                dente = capa & (uu > 1 - 1.2 / (LIVRO["W"] * M["esc"])) & (np.abs(vv - v_d) < 1.1 / M["esc"])
                mat[dente] = ""
        # as cantoneiras de ferro escuro nos dois cantos soltos
        for v0 in (0.0, 1.0):
            canto = capa & ((1 - uu) * 5.0 + np.abs(vv - v0) * 3.4 < 0.62)
            mat[canto], tom[canto] = "f", 3
            tom[canto & ((1 - uu) * 5.0 + np.abs(vv - v0) * 3.4 > 0.42)] = 2
            tom[canto & (uu > 0.97)] = 4                           # a quina pega a luz
            fixo[canto] = True
    # ---- o papel: a página de frente (clara, escurecendo só na beira) e o corte da cabeça em fios
    pag = qual == "pagina"
    borda = np.minimum.reduce([uu * 1.4, 1 - uu, vv * 1.6, 1 - vv])
    tom[pag] = 6
    tom[pag & (borda < 0.12)] = 5
    tom[pag & (borda < 0.05)] = 4
    # a sombra da capa aberta na página, junto da lombada (u pequeno)
    tom[pag & (uu < 0.12)] = np.minimum(tom[pag & (uu < 0.12)], 3)
    corte = (qual == "corte_pe") | (qual == "corte_frente")
    tom[corte] = np.where((np.floor(vv * T * M["esc"] * 2.2) % 2) == 0, 5, 4)[corte]
    # as marcas: linhas de anotação (traços curtos, com falhas em 48 e 64; sem letra)
    marca = np.zeros(x.shape, dtype=bool)
    passo = 1.0 / M["esc"]
    for k in range(M["linhas"]):
        v_l = 0.82 - k * max(0.08, 2.4 * passo)
        linha = pag & (np.abs(vv - v_l) < 0.6 * passo) & (uu > 0.3) & (uu < 0.84 - 0.18 * (k % 2))
        falha = ((np.floor(uu * W * M["esc"] + k * 2) % 5) == 0) if lado >= 48 else (np.abs(uu - (0.52 + 0.08 * k)) < 0.5 * passo / W)
        marca |= linha & ~falha
    # o diagrama (só em 48 e 64, onde cabe): um círculo fino com dois pontos marcados nele e a reta que os une, um
    # estudo de geometria; em 32 e 40 ficam só as anotações (um círculo de 4 pixels viraria letra)
    arco = np.zeros(x.shape, dtype=bool)
    if lado >= 48:
        cxu, cyv, raio = 0.55, 0.3, 0.13
        rr = np.hypot((uu - cxu) * W, (vv - cyv))
        arco = pag & (np.abs(rr - raio) < 0.55 * passo)
        a1, a2 = math.radians(200), math.radians(320)
        p1 = (cxu + raio * math.cos(a1) / W, cyv + raio * math.sin(a1))
        p2 = (cxu + raio * math.cos(a2) / W, cyv + raio * math.sin(a2))
        su, sv = (p2[0] - p1[0]) * W, p2[1] - p1[1]
        tt = np.clip(((uu - p1[0]) * W * su + (vv - p1[1]) * sv) / (su * su + sv * sv), 0, 1)
        corda = pag & (np.hypot((uu - p1[0]) * W - tt * su, (vv - p1[1]) - tt * sv) < 0.5 * passo)
        pontos = pag & ((np.hypot((uu - p1[0]) * W, vv - p1[1]) < 1.1 * passo) | (np.hypot((uu - p2[0]) * W, vv - p2[1]) < 1.1 * passo))
        arco |= corda | pontos
    elif lado >= 40:  # o segundo grupo de anotações, mais curto, embaixo (em 32 fica um grupo só)
        for k in range(2):
            v_l = 0.4 - k * max(0.12, 3.4 * passo)
            arco |= pag & (np.abs(vv - v_l) < 0.6 * passo) & (uu > 0.42) & (uu < 0.78 - 0.12 * k)
    marca |= arco
    mat[marca], tom[marca] = "t", 2 if lado < 48 else 1
    fixo[marca] = True

    # ---- a fita: sai do pé do miolo, perto do meio, desce pelo corte e cai na mesa, para a frente e para a direita
    base = np.array([0.5 * W, tab + T, e + 0.02]) - meio
    caminho = [base, base + np.array([0.01, 0.0, -0.05]), base + np.array([0.03, -T - tab, -0.07]),
               base + np.array([0.1, -T - tab, -0.17]), base + np.array([0.15, -T - tab, -0.21])]
    pts = [(M["cx"] + p @ direita * M["esc"], M["cy"] - p @ cima * M["esc"]) for p in caminho]
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by_) = pts[i], pts[i + 1]
        sx, sy = bx - ax, by_ - ay
        comp = math.hypot(sx, sy) or 1
        t_ = np.clip(((x - ax) * sx + (y - ay) * sy) / comp ** 2, 0, 1)
        px_, py_ = ax + t_ * sx, ay + t_ * sy
        seg = np.hypot(x - px_, y - py_) <= M["fita"] / 2
        mat[seg], tom[seg] = "r", 2 if i == 1 else 3
        lado_luz = seg & ((((x - px_) * -sy + (y - py_) * sx) / comp) < -(M["fita"] / 2 - 0.8))
        tom[lado_luz] = 3 if i == 1 else 4
        fixo[seg] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"v": COURO, "p": PAPEL, "t": TINTA, "r": FITA, "f": FERRO})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("proposta: diga a pasta (python ferramentas/arte/desenhar_grimorio_pixel.py <pasta>)")
    saida = destino(sys.argv)
    for lado in LADOS:
        print(f"livro-{lado}: {salvar(desenhar(lado), saida, 'livro')} cores")
