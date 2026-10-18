"""Os oito ícones do menu de baixo (a doca: Talentos, Grimório, Inventário, Mapa, Diário, Bestiário, Salvar, Sair) no
método da família: proposta, nada no jogo.

Hoje são peças pintadas da família de ferro (`atalho-*-32` e `-36`). Ficam os conceitos que já se leem, redesenhados
na grade com rampas por material, luz de cima e da esquerda em faixas e o contorno comum:
  Talentos    três nós de latão ligados (a árvore)
  Grimório    o livro roxo de capa dura com a pedra violeta e os cantos de ferro (também o comando Habilidades da luta:
              `ACAO.grimorio` em icones.js; trocar o grimório troca os dois)
  Inventário  a mochila de couro, nas rampas do conjunto de couro aprovado, com a aba, a fivela e as alças
  Mapa        o pergaminho dobrado em três, o caminho tracejado e o X vermelho
  Diário      o livro aberto com a pena
  Bestiário   o crânio de chifres
  Salvar      o baú escuro com a seta descendo
  Sair        o arco de pedra com a seta laranja saindo

Os tamanhos: 36 na doca (o mais visto) e 32 (a doca estreita); os dois nas mesmas medidas (unidades do 36), cada um
na sua grade.

    python ferramentas/arte/desenhar_doca_pixel.py <pasta>
"""

import math
import sys

import numpy as np

import pixel_comum as pc

LATAO = ["#2E200C", "#5A4118", "#8A6828", "#B98E3E", "#DDB860", "#F4DE98"]
ROXO = ["#1E1030", "#352052", "#4E3274", "#6A4896", "#8A66B8"]
VIOLETA = ["#3A1466", "#6A2CB0", "#A060EA", "#E0C8FF"]
FERRO = ["#22252B", "#3A3F47", "#5C636D", "#8A929C", "#B8C0C8"]
COURO = ["#1C120C", "#2E1E13", "#45301E", "#604229", "#7C5634", "#986C42", "#B48752"]
BORDA = ["#140C08", "#22150D", "#321F13", "#45301E"]
PERGAMINHO = ["#6E5A3E", "#9A8260", "#C2AA84", "#DCC8A2", "#EEE0C0"]
TINTA = ["#3A2A1C", "#5C4630"]
VERMELHO = ["#5C1010", "#9A1E1E", "#D03A30"]
PAPEL = ["#7A6E5C", "#A89C86", "#CFC4AE", "#ECE4D2"]
PENA = ["#5E5850", "#9A948A", "#D2CCC0", "#F2EEE6"]
OSSO = ["#4A4236", "#7A6E5C", "#A89A82", "#CFC2A8", "#EAE0CA"]
MADEIRA = ["#1E1A16", "#2E2A26", "#46403A", "#5E5750"]
PEDRA = ["#26282C", "#3C4046", "#585E66", "#7C838C", "#A4ABB2"]
LARANJA = ["#6A2C08", "#B05A14", "#E88C2C", "#FFC060"]
RAMPAS = {"l": LATAO, "r": ROXO, "v": VIOLETA, "f": FERRO, "k": COURO, "b": BORDA, "p": PERGAMINHO, "t": TINTA,
          "e": VERMELHO, "q": PAPEL, "n": PENA, "o": OSSO, "m": MADEIRA, "d": PEDRA, "x": LARANJA}


def _base(lado):
    s = lado / 36
    mat, tom, fixo, x, y = pc.grade(lado)
    return s, mat, tom, fixo, x / s, y / s, 1 / s


def _fim(mat, tom, fixo):
    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    return pc.imagem(mat, tom, RAMPAS)


def _linha(X, Y, p0, p1, larg):
    """Os pixels a até larg/2 do segmento p0–p1 (em unidades do 36)."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    t = np.clip(((X - x0) * dx + (Y - y0) * dy) / (dx * dx + dy * dy), 0, 1)
    return np.hypot(X - (x0 + t * dx), Y - (y0 + t * dy)) <= larg / 2


def _disco(mat, tom, X, Y, cx, cy, r, m, rampa_n):
    d = (X - cx) ** 2 + (Y - cy) ** 2 <= r * r
    mat[d] = m
    # a luz de uma esfera: clara em cima à esquerda, escura embaixo à direita
    k = ((X - cx) * -0.6 + (Y - cy) * -0.75) / max(r, 1)
    tom[d] = np.clip(np.round(2.2 + 2.6 * k), 0, rampa_n - 1).astype(int)[d]
    return d


def talentos(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    nos = [(18.0, 7.6), (7.6, 27.4), (28.4, 27.4)]
    centro = (18.0, 20.0)
    for (nx, ny) in nos:
        haste = _linha(X, Y, centro, (nx, ny), max(2.0, 1.6 * px))
        mat[haste] = "l"
        tom[haste] = 2
    for (nx, ny) in nos:
        _disco(mat, tom, X, Y, nx, ny, 5.4, "l", len(LATAO))
    _disco(mat, tom, X, Y, centro[0], centro[1], 2.0, "l", len(LATAO))
    # o brilho de cada nó, um ponto claro desenhado
    for (nx, ny) in nos:
        xx, yy = int((nx - 2.0) * s), int((ny - 2.2) * s)
        mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "l", 5, True
    return _fim(mat, tom, fixo)


def grimorio(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    x0, x1, y0, y1 = 7.0, 29.0, 3.0, 33.0
    capa = (X >= x0) & (X < x1) & (Y >= y0) & (Y < y1)
    mat[capa] = "r"
    tom[capa] = np.where(X < x0 + 3.0, 4, np.where(X < 18, 3, 2))[capa]
    # a lombada à esquerda, mais escura, com duas nervuras
    lomb = capa & (X < x0 + 2.4)
    tom[lomb] = 1
    for ny in (9.0, 27.0):
        nerv = lomb & (np.abs(Y - ny) < 0.5 * px + 0.3)
        tom[nerv], fixo[nerv] = 3, True
    # as folhas aparecendo à direita (o miolo do livro)
    folhas = (X >= x1 - 1.6) & (X < x1) & (Y >= y0 + 1.6) & (Y < y1 - 1.6)
    mat[folhas], tom[folhas] = "q", 2
    # os cantos de ferro (em cima e embaixo, à direita)
    for (cy0, cy1) in ((y0, y0 + 4.0), (y1 - 4.0, y1)):
        canto = (X >= x1 - 4.0) & (X < x1) & (Y >= cy0) & (Y < cy1)
        tri = canto & (((X - (x1 - 4.0)) + (np.abs(Y - (cy0 if cy0 == y0 else cy1)))) <= 4.6)
        mat[tri], tom[tri] = "f", 3
        fixo[tri] = True
    # o fecho de ferro na borda direita, no meio
    fecho = (X >= x1 - 2.6) & (X < x1 + 1.4) & (np.abs(Y - 18.0) < 2.2)
    mat[fecho], tom[fecho] = "f", np.where(Y[fecho] < 18, 3, 2)
    # o losango de latão em volta da pedra e a pedra violeta
    cx, cy = 19.0, 18.0
    los = np.abs(X - cx) / 6.2 + np.abs(Y - cy) / 7.4 <= 1
    mat[los] = "l"
    tom[los] = np.where((X - cx) + (Y - cy) < 0, 4, 2)[los]
    pedra = np.abs(X - cx) / 3.6 + np.abs(Y - cy) / 4.6 <= 1
    mat[pedra] = "v"
    tom[pedra] = np.where((X - cx) + (Y - cy) * 0.8 < -1.2, 3, np.where((X - cx) + (Y - cy) * 0.8 < 1.2, 2, 1))[pedra]
    fixo[los] = True
    return _fim(mat, tom, fixo)


def inventario(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    # o corpo: um retângulo de cantos redondos, mais largo embaixo
    def ret_redondo(x0, x1, y0, y1, r):
        cxr = np.clip(X, x0 + r, x1 - r)
        cyr = np.clip(Y, y0 + r, y1 - r)
        return (X >= x0) & (X < x1) & (Y >= y0) & (Y < y1) & ((X - cxr) ** 2 + (Y - cyr) ** 2 <= r * r)
    # a alça de cima: um arco de couro escuro
    alca = (np.abs(np.hypot(X - 18.0, Y - 8.6) - 4.2) <= 0.95) & (Y < 8.6)
    mat[alca], tom[alca] = "b", 2
    corpo = ret_redondo(5.0, 31.0, 7.0, 33.0, 4.0)
    mat[corpo] = "k"
    tom[corpo] = np.where(X < 10.0, 5, np.where(X < 23.0, 4, 3))[corpo]
    # os bolsos dos lados, um tom abaixo, com a borda
    for (bx0, bx1) in ((3.0, 8.0), (28.0, 33.0)):
        bolso = ret_redondo(bx0, bx1, 16.0, 30.0, 2.0)
        mat[bolso] = "k"
        tom[bolso] = 4 if bx0 < 18 else 2
    # a aba: a parte de cima, mais clara, terminando em curva
    aba = corpo & (Y < 17.5 + 2.5 * np.cos(np.clip((X - 18.0) / 13.0, -1, 1) * math.pi / 2) - 2.5)
    tom[aba] = np.where(X[aba] < 12.0, 6, 5)
    borda_aba = corpo & ~aba & (Y < 19.6 + 2.5 * np.cos(np.clip((X - 18.0) / 13.0, -1, 1) * math.pi / 2) - 2.5)
    mat[borda_aba], tom[borda_aba] = "b", 2
    # a tira com a fivela de latão, no meio
    tira = (np.abs(X - 18.0) < 1.6) & (Y >= 12.0) & (Y < 25.0)
    mat[tira], tom[tira] = "b", 3
    fivela = (np.abs(X - 18.0) < 2.6) & (np.abs(Y - 20.5) < 2.0)
    mat[fivela] = "l"
    tom[fivela] = np.where(np.abs(X - 18.0) < 1.2, 1, 3)[fivela]
    tom[fivela & (Y < 19.4)] = 4
    for ax in (9.6, 26.4):   # as alças de carregar, de couro escuro, descendo pela frente
        al = (np.abs(X - ax) < 0.5 * px + 0.25) & (Y >= 9.0) & (Y < 31.0) & corpo & ~aba
        mat[al], tom[al] = "b", 2
        fixo[al] = True
    fixo[tira | fivela | borda_aba] = True
    return _fim(mat, tom, fixo)


def mapa(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    x0, x1, y0, y1 = 3.0, 33.0, 7.0, 29.0
    papel = (X >= x0) & (X < x1) & (Y >= y0 - 1.0 * np.isin(np.floor((X - x0) / 10), [1])) & (Y < y1 + 1.0 * np.isin(np.floor((X - x0) / 10), [1]))
    papel &= (X >= x0) & (X < x1)
    mat[papel] = "p"
    painel = np.floor((X - x0) / 10).astype(int)
    tom[papel] = np.select([painel == 0, painel == 1, painel == 2], [3, 4, 2], 3)[papel]
    # as dobras: o fim de cada painel um tom abaixo
    dobra = papel & (np.abs(((X - x0) % 10) - 9.5) < 0.5 * px + 0.1)
    tom[dobra] = np.maximum(tom[dobra] - 2, 0)
    # o caminho tracejado: uma curva de x 6 a 26
    for i in range(14):
        t = i / 13
        cx = 6.0 + 20.0 * t
        cy = 23.0 - 9.0 * t + 4.0 * math.sin(t * math.pi * 1.6)
        if i % 2 == 0:
            ponto = papel & (np.abs(X - cx) < max(0.9, 0.6 * px)) & (np.abs(Y - cy) < max(0.9, 0.6 * px))
            mat[ponto], tom[ponto], fixo[ponto] = "t", 0, True
    # o X vermelho no fim do caminho
    for (p0, p1) in (((24.6, 9.4), (29.4, 14.2)), ((29.4, 9.4), (24.6, 14.2))):
        risco = _linha(X, Y, p0, p1, max(1.7, 1.0 * px))
        mat[risco], tom[risco], fixo[risco] = "e", 2, True
    return _fim(mat, tom, fixo)


def diario(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    # a capa embaixo (couro escuro) e as duas páginas abertas, curvando na lombada
    capa = (X >= 2.0) & (X < 34.0) & (Y >= 15.0) & (Y < 31.0)
    mat[capa], tom[capa] = "k", 2
    for (a, b, tom_p) in ((3.0, 18.0, 3), (18.0, 33.0, 2)):
        curva = 1.6 * np.cos((X - (a + b) / 2) / (b - a) * math.pi)
        pag = (X >= a) & (X < b) & (Y >= 14.0 - curva) & (Y < 29.0 - curva * 0.4)
        mat[pag] = "q"
        tom[pag] = tom_p
    lomb = (np.abs(X - 18.0) < 0.5 * px + 0.2) & (Y >= 13.0) & (Y < 29.0)
    mat[lomb], tom[lomb], fixo[lomb] = "q", 0, True
    # as linhas de texto, curtas e claras de tinta
    for ly in (18.0, 21.0, 24.0):
        for (a, b) in ((5.5, 15.5), (20.5, 30.5)):
            ln = (mat == "q") & (np.abs(Y - ly) < 0.5 * px) & (X >= a) & (X < b)
            tom[ln], fixo[ln] = 1, True
    # a pena: na diagonal, a ponta na página da direita, a pluma saindo para cima à direita
    haste = _linha(X, Y, (22.0, 24.0), (32.6, 3.0), max(1.2, 0.9 * px))
    pluma = np.zeros_like(haste)
    a0, a1 = np.array([25.0, 18.0]), np.array([32.6, 3.0])
    v = a1 - a0
    t = ((X - a0[0]) * v[0] + (Y - a0[1]) * v[1]) / (v @ v)
    d = ((X - a0[0]) * v[1] - (Y - a0[1]) * v[0]) / np.linalg.norm(v)
    pluma = (t >= 0) & (t <= 1) & (np.abs(d) <= 2.8 * np.sin(np.clip(t, 0, 1) * math.pi) ** 0.7)
    mat[pluma] = "n"
    tom[pluma] = np.where(d[pluma] > 0.5, 3, np.where(d[pluma] > -0.6, 2, 1))
    mat[haste], tom[haste] = "n", 1
    fixo[haste] = True
    return _fim(mat, tom, fixo)


def bestiario(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    # o crânio: a calota larga em cima, afinando no focinho
    cran = ((X - 18.0) / 8.4) ** 2 + ((Y - 17.0) / 7.0) ** 2 <= 1
    foc = (np.abs(X - 18.0) <= 5.0 - np.clip(Y - 23.0, 0, 9) * 0.3) & (Y >= 17.0) & (Y < 33.0)
    corpo = cran | foc
    mat[corpo] = "o"
    tom[corpo] = np.where(X < 15.0, 4, np.where(X < 21.0, 3, 2))[corpo]
    # os chifres: grossos na raiz, saindo dos lados da calota, abrindo para fora e subindo até as pontas
    for lado_s in (-1, 1):
        for i in range(40):
            t = i / 39
            hx = 18.0 + lado_s * (6.4 + 10.0 * math.sin(t * math.pi * 0.55))
            hy = 12.6 - 10.4 * t ** 1.35
            r = 2.7 * (1 - t) + 0.55
            ch = (X - hx) ** 2 + (Y - hy) ** 2 <= r * r
            mat[ch] = "o"
            tom[ch] = 3 if lado_s < 0 else 2
    # os olhos: dois buracos escuros e o nariz
    for ex in (14.2, 21.8):
        olho = ((X - ex) / 2.4) ** 2 + ((Y - 18.0) / 2.2) ** 2 <= 1
        mat[olho], tom[olho], fixo[olho] = "m", 0, True
    nariz = (np.abs(X - 18.0) < 1.2) & (Y >= 22.6) & (Y < 25.6)
    mat[nariz], tom[nariz], fixo[nariz] = "m", 0, True
    # os dentes embaixo
    for dx in (-3.0, -1.0, 1.0, 3.0):
        dente = (np.abs(X - (18.0 + dx)) < 0.5 * px + 0.15) & (Y >= 28.4) & (Y < 31.4)
        mat[dente], tom[dente], fixo[dente] = "m", 1, True
    return _fim(mat, tom, fixo)


def salvar(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    # o baú escuro de madeira com a borda de latão (embaixo) e a seta de ferro descendo (em cima)
    bau = (X >= 5.0) & (X < 31.0) & (Y >= 19.0) & (Y < 33.0)
    mat[bau] = "m"
    tom[bau] = np.where(X < 12, 3, np.where(X < 24, 2, 1))[bau]
    tampa = bau & (Y < 23.0)
    tom[tampa] = np.minimum(tom[tampa] + 1, 3)
    for (bx0, bx1, by0, by1) in ((5.0, 31.0, 23.0, 24.2), (5.0, 7.2, 19.0, 33.0), (28.8, 31.0, 19.0, 33.0)):
        aro = bau & (X >= bx0) & (X < bx1) & (Y >= by0) & (Y < by1)
        mat[aro], tom[aro] = "l", 2
    fech = (np.abs(X - 18.0) < 3.4) & (Y >= 25.4) & (Y < 29.4)
    mat[fech], tom[fech] = "l", np.where(Y[fech] < 26.6, 4, 3)
    fixo[fech] = True
    # a seta: a haste e a ponta, de ferro, descendo para a tampa
    haste = (np.abs(X - 18.0) < 3.4) & (Y >= 1.2) & (Y < 9.4)
    ponta = (Y >= 9.4) & (Y < 18.2) & (np.abs(X - 18.0) <= (18.2 - Y) * 1.05)
    seta = haste | ponta
    mat[seta] = "f"
    tom[seta] = np.where(X < 18.0, 4, 2)[seta]
    return _fim(mat, tom, fixo)


def sair(lado):
    s, mat, tom, fixo, X, Y, px = _base(lado)
    # o arco de pedra: os batentes e a volta em cima, com a passagem escura no meio
    fora = ((X >= 4.0) & (X < 24.0) & (Y >= 11.0) & (Y < 33.0)) | (((X - 14.0) / 10.0) ** 2 + ((Y - 11.0) / 9.0) ** 2 <= 1)
    dentro = ((X >= 8.0) & (X < 20.0) & (Y >= 11.0) & (Y < 33.0)) | (((X - 14.0) / 6.0) ** 2 + ((Y - 11.0) / 5.4) ** 2 <= 1)
    pedra = fora & ~dentro
    mat[pedra] = "d"
    tom[pedra] = np.where(X < 9, 3, np.where(X < 19, 2, 1))[pedra]
    # as juntas das pedras: linhas escuras a cada 4 de altura nos batentes
    junta = pedra & (Y >= 12.0) & (((Y - 12.0) % 4.6) < 0.5 * px + 0.1)
    tom[junta], fixo[junta] = 0, True
    mat[dentro] = "m"
    tom[dentro] = 0
    # o chão claro saindo pela porta (a luz de fora)
    luz = dentro & (Y >= 27.0)
    tom[luz] = 2
    # a seta laranja saindo para a direita, por cima do batente
    haste = (X >= 16.0) & (X < 26.0) & (np.abs(Y - 21.0) < 2.4)
    ponta = (X >= 26.0) & (X < 34.0) & (np.abs(Y - 21.0) <= (34.0 - X) * 0.9)
    seta = haste | ponta
    mat[seta] = "x"
    tom[seta] = np.where(Y < 20.0, 3, np.where(Y < 22.0, 2, 1))[seta]
    fixo[seta] = True
    return _fim(mat, tom, fixo)


DESENHOS = {"atalho-talentos": talentos, "atalho-grimorio": grimorio, "atalho-inventario": inventario,
            "atalho-mapa": mapa, "atalho-diario": diario, "atalho-bestiario": bestiario, "atalho-salvar": salvar,
            "atalho-sair": sair}


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    so = [a for a in sys.argv[2:] if not a.startswith("-")]
    for nome, f in DESENHOS.items():
        if so and nome.replace("atalho-", "") not in so:
            continue
        for lado in (36, 32):
            print(nome, lado, pc.salvar(f(lado), pasta, nome), "cores")


if __name__ == "__main__":
    main()
