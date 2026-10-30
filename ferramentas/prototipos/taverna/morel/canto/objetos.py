"""Os objetos da mesa de Morel no canto (protótipo): a vela com o castiçal, a caneca, o pão, a tigela com o ensopado,
e a chama da vela (quatro quadros).

Cada objeto é construído na grade da cena (as posições e os tamanhos medidos na referência "Encontro com Morel na
taverna" e somados os 40 px da borda), com as paletas das cenas aprovadas: o ferro do castiçal, a cera da vela, o
estanho da caneca, a casca e o miolo do pão, a madeira da tigela, o ensopado. Três tons por material, a aresta acesa
do lado da vela, o brilho do metal de um pixel, a sombra de contato no tampo. Nada da imagem gerada é copiado: o miolo
do pão, os pedaços do ensopado e as dobras da cera são simplificados para a escala."""
import math

from espaco import h, _px

FERRO = [h("6e7078"), h("45474e"), h("2e3034"), h("24252a"), h("16171a")]
CERA = [h("f4ecd6"), h("e6dec8"), h("c8bea6"), h("958b74")]
ESTANHO = [h("e2e4e8"), h("cfd1d6"), h("9a9ca4"), h("6e7078"), h("45474e"), h("24252a")]
CASCA = [h("d89a52"), h("c4843e"), h("9c6438"), h("76522f"), h("5a3e26")]
MIOLO = [h("f0dcae"), h("d4b67e"), h("b8955e")]
TIGELA = [h("c47a3a"), h("9e5c28"), h("7a4a2c"), h("68381a"), h("4c2c18"), h("2e1a0e")]
ENSOPADO = [h("c8642a"), h("a8582a"), h("8a3a1a"), h("6a2a14"), h("4a1a0c")]
BATATA = [h("e6c27a"), h("c49a52")]
VERDE = h("6a7a2a")
SOMBRA_TAMPO = h("281b10")
CHAMA = [h("fff2c0"), h("ffd060"), h("f09030"), h("c85a1a")]


def _elipse(cx, cy, rx, ry):
    for y in range(math.floor(cy - ry), math.ceil(cy + ry) + 1):
        for x in range(math.floor(cx - rx), math.ceil(cx + rx) + 1):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                yield x, y


def sombra(img, pontos, dx=2, dy=1):
    """A sombra de contato no tampo, do lado oposto à vela (para a direita e para cima)."""
    for x, y in pontos:
        _px(img, x + dx, y + dy, SOMBRA_TAMPO)


def castical(img):
    """O castiçal de ferro: o prato raso (a borda de cima acesa, a de baixo escura), o copinho que segura a vela e a
    alça em argola à esquerda."""
    cx, cy = 57, 83
    prato = list(_elipse(cx, cy, 13, 4.2))
    sombra(img, [(x, y) for x, y in prato if y >= cy], 3, 1)
    for x, y in prato:
        u = (x + 0.5 - cx) / 13
        v = (y + 0.5 - cy) / 4.2
        cor = FERRO[1] if v < -0.3 else FERRO[3] if v > 0.5 else FERRO[2]
        if v < -0.55 and u < 0.2:
            cor = FERRO[0]
        _px(img, x, y, cor)
    for x, y in _elipse(cx, cy - 1, 9, 2.6):  # o fundo do prato, um degrau abaixo
        if (y + 0.5 - (cy - 1)) / 2.6 > -0.4:
            _px(img, x, y, FERRO[3])
    for y in range(74, 82):  # o copinho
        for x in range(cx - 6, cx + 6):
            k = x - (cx - 6)
            _px(img, x, y, FERRO[1] if k <= 1 else FERRO[4] if k >= 10 else FERRO[2] if k < 7 else FERRO[3])
    for x, y in _elipse(cx, 74, 6, 1.6):
        _px(img, x, y, FERRO[1])
    # a alça: uma argola à esquerda, presa ao prato
    for a in range(0, 360, 6):
        t = math.radians(a)
        x, y = 44 + 4.2 * math.cos(t), 76 + 4.6 * math.sin(t)
        if x < 48.5:
            _px(img, round(x), round(y), FERRO[1] if math.sin(t) < 0 else FERRO[3])
    _px(img, 47, 72, FERRO[1])
    _px(img, 47, 80, FERRO[2])


def vela(img):
    """A vela de cera: o corpo com o lado da chama aceso, o alto com a borda derretida e um pingo, o pavio."""
    x0, x1, y0, y1 = 52, 62, 56, 74
    for y in range(y0, y1):
        for x in range(x0, x1):
            k = x - x0
            cor = CERA[0] if k in (2, 3) else CERA[1] if k < 6 else CERA[2] if k < 8 else CERA[3]
            _px(img, x, y, cor)
    for x in range(x0, x1):  # o alto: a borda derretida, mais clara, e a concavidade
        _px(img, x, y0, CERA[0] if x < x0 + 7 else CERA[2])
    for x in range(x0 + 2, x1 - 2):
        _px(img, x, y0 + 1, CERA[2])
    for y in range(y0 + 1, y0 + 6):  # um pingo descendo do lado da luz
        _px(img, x0, y, CERA[0])
    _px(img, x0 + 1, y0 + 6, CERA[0])
    _px(img, x0 + 5, y0 - 1, FERRO[4])  # o pavio
    _px(img, x0 + 5, y0 - 2, FERRO[3])


def chama(img, q):
    """A chama da vela, quadro q (0 a 3): uma língua que afina para cima, o miolo claro embaixo, a ponta tremendo."""
    cx = 57 + (0, 0, 1, 0)[q]
    alto = (13, 12, 14, 12)[q]
    base = 54
    for y in range(base - alto, base + 1):
        t = (base - y) / alto
        larg = 2.6 * math.sin(math.pi * min(1.0, 0.25 + t * 0.9)) * (1 - t * 0.55)
        dx = (0, 0.4, -0.3, 0.2)[q] * t * 3
        for x in range(math.floor(cx - larg + dx), math.ceil(cx + larg + dx)):
            d = abs(x + 0.5 - cx - dx) / max(larg, 0.6)
            cor = CHAMA[0] if d < 0.4 and t < 0.55 else CHAMA[1] if d < 0.75 and t < 0.8 else CHAMA[2] if t < 0.9 else \
                CHAMA[3]
            _px(img, x, y, cor)


def caneca(img):
    """A caneca de estanho: o corpo em faixas verticais (o realce do lado da vela, o meio, o escuro à direita), a boca
    em elipse com a borda acesa e o fundo escuro, os dois aros, a alça à esquerda."""
    x0, x1, y0, y1 = 78, 99, 60, 83   # 4 px mais perto da vela: o cotovelo pousa ao lado dela, sem encostar
    sombra(img, [(x, y1 - 1) for x in range(x0, x1)], 2, 1)
    sombra(img, [(x, y1) for x in range(x0 + 2, x1 + 1)], 0, 0)
    for y in range(y0, y1):
        for x in range(x0, x1):
            k = (x - x0) / (x1 - x0)
            cor = ESTANHO[2] if k < 0.08 else ESTANHO[0] if k < 0.2 else ESTANHO[1] if k < 0.42 else \
                ESTANHO[2] if k < 0.7 else ESTANHO[3] if k < 0.9 else ESTANHO[4]
            _px(img, x, y, cor)
    for y in (y0 + 4, y1 - 4):  # os aros
        for x in range(x0, x1):
            _px(img, x, y, ESTANHO[3] if x < x0 + 14 else ESTANHO[4])
    for x in range(x0, x1):
        _px(img, x, y1 - 1, ESTANHO[4])
    for x, y in _elipse((x0 + x1) / 2, y0, (x1 - x0) / 2, 2.4):  # a boca
        v = (y + 0.5 - y0) / 2.4
        _px(img, x, y, ESTANHO[1] if v < -0.4 or x < x0 + 2 else ESTANHO[5] if v < 0.5 else ESTANHO[3])
    for a in range(-90, 91, 5):  # a alça
        t = math.radians(a)
        x, y = x0 - 4.5 * math.cos(t) + 0.5, 70 + 7.5 * math.sin(t)
        _px(img, round(x), round(y), ESTANHO[2])
        _px(img, round(x) + 1, round(y), ESTANHO[4] if a > 30 else ESTANHO[3])


def pao(img):
    """O pão: a casca dourada, mais clara em cima, com dois cortes; o miolo no lado cortado, à direita; migalhas."""
    cx, cy = 104, 84
    casca = list(_elipse(cx, cy, 13, 6))
    sombra(img, [(x, y) for x, y in casca if y >= cy + 3], 2, 1)
    for x, y in casca:
        v = (y + 0.5 - cy) / 6
        u = (x + 0.5 - cx) / 13
        cor = CASCA[0] if v < -0.55 and u < 0.3 else CASCA[1] if v < -0.1 else CASCA[2] if v < 0.5 else CASCA[3]
        _px(img, x, y, cor)
    for (x, y) in ((97, 80), (98, 79), (103, 79), (104, 78)):  # os cortes da casca
        _px(img, x, y, CASCA[3])
    for x, y in _elipse(115, 84, 3.4, 5.2):  # o miolo no lado cortado
        v = (y + 0.5 - 84) / 5.2
        _px(img, x, y, MIOLO[0] if v < -0.2 else MIOLO[1] if v < 0.5 else MIOLO[2])
    for x, y in ((117, 81), (116, 86), (114, 83)):
        _px(img, x, y, MIOLO[2])
    for x, y in ((121, 89), (124, 90), (119, 91)):  # migalhas
        _px(img, x, y, CASCA[1])


TIGELA_C = (170, 72)          # o centro da boca da tigela
TIGELA_R = (22.5, 5.0)        # os raios da boca


def tigela(img, so_frente=False):
    """A tigela de madeira com o ensopado: a boca em elipse (a borda de lá acesa), o caldo com os pedaços (carne,
    cenoura, batata, um verde), o bojo embaixo da borda da frente, a sombra no tampo. `so_frente`: só a borda da frente
    e o bojo (o que fica na frente da colher quando ela está no caldo)."""
    cx, cy = TIGELA_C
    rx, ry = TIGELA_R
    pts = []
    for y in range(cy, cy + 12):  # o bojo: a meia elipse de baixo, afinando para o pé
        t = (y - cy) / 11
        larg = rx * math.sqrt(max(0.0, 1 - t * t * 0.75))
        for x in range(math.floor(cx - larg), math.ceil(cx + larg)):
            u = (x + 0.5 - cx) / larg
            cor = TIGELA[1] if u < -0.45 else TIGELA[2] if u < 0.25 else TIGELA[3] if u < 0.7 else TIGELA[4]
            if y >= cy + 10:
                cor = TIGELA[4]
            pts.append((x, y, cor))
    if not so_frente:
        sombra(img, [(x, y) for x, y, _ in pts if y >= cy + 8], 3, 1)
    for x, y, cor in pts:
        _px(img, x, y, cor)
    for x, y in _elipse(cx, cy, rx, ry):  # a boca: a borda e o caldo
        v = (y + 0.5 - cy) / ry
        d = ((x + 0.5 - cx) / rx) ** 2 + v ** 2
        if d > 0.62:
            if so_frente and v < 0:
                continue
            cor = TIGELA[0] if v < -0.2 and x < cx + 6 else TIGELA[1] if v < 0.3 else TIGELA[2]
            _px(img, x, y, cor)
        elif not so_frente:
            u = (x + 0.5 - cx) / rx
            _px(img, x, y, ENSOPADO[3] if v < -0.2 else ENSOPADO[2] if u < 0.4 else ENSOPADO[3])
    if so_frente:
        return
    for (x, y, cor) in ((160, 71, ENSOPADO[0]), (161, 71, ENSOPADO[0]), (166, 73, ENSOPADO[1]), (167, 73, ENSOPADO[1]),
                        (172, 70, BATATA[0]), (173, 70, BATATA[0]), (173, 71, BATATA[1]), (178, 72, ENSOPADO[0]),
                        (179, 72, ENSOPADO[1]), (163, 69, ENSOPADO[4]), (176, 69, VERDE), (169, 74, ENSOPADO[4]),
                        (183, 71, BATATA[1]), (157, 73, ENSOPADO[1])):
        _px(img, x, y, cor)


def objetos(img):
    castical(img)
    vela(img)
    caneca(img)
    pao(img)
    tigela(img)
