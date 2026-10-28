"""O templo do Vau, candidata B: a composição da referência do Jean (`ferramentas/arte/referencias/cenarios internos/
Interior do Templo da Vila.png`), redesenhada na grade de 320×96 e no acabamento das cenas aprovadas. Da imagem vêm só a
composição, a distância da câmera e a organização do espaço, medidas na escala do jogo com uma grade por cima (a
imagem nunca é reduzida para virar fundo): a nave vista de frente, para o altar; o arco de pedra entre duas colunas,
com o presbitério um degrau acima e a janela alta atrás do altar; os bancos em dois blocos vistos por trás, o corredor
no meio; a entrada com a luz do dia à esquerda; o atendimento à direita (a mesa dos panos, o armário de potes, a porta
lateral, a mesinha do incenso); as silhuetas da frente.

O que não vem da imagem: os estandartes com cruz e a cruz no avental (símbolos gerados, provisórios: o jogo só
estabelece a cruz do campanário), o vidro azul e amarelo (as janelas da igreja na vila são acesas em amarelo quente),
as texturas miúdas e as sombras suaves. O clérigo é desenhado a partir do que o jogo diz dele (figura.py).

A câmera é mais aberta que a da A: o clérigo tem ~31 px (na A, ~42; Marta, 52). As camadas: `fundo()`, `velas(i)` (4),
`fumaca(i)` (8), `frente()`."""
import math

from ..a.desenho import C, Pincel, Tela, pont

QW, QH = 320, 96
P = 70        # a linha do chão da nave
PRESB = 58    # o chão do presbitério (dois degraus acima)
MESA = 56     # o tampo da mesa dos panos
PES = 70      # onde pisa o clérigo

C.update({
    "pedraB": "#45403a", "pedraBLuz": "#5c554c", "pedraBEsc": "#2c2925", "juntaB": "#36322d",
    "fundoArco": "#2a2622", "fundoArcoLuz": "#363029",
    "tapete": "#2e3640", "tapeteLuz": "#3c4652", "tapeteBorda": "#7a6430",
    "brasa": "#c8501a",
})


def paredes(px):
    """A parede de pedra da nave (blocos regulares, as juntas um tom abaixo, quase sem textura), o vigamento de madeira
    no alto dos dois lados e o chão de lajes."""
    px(0, 0, QW, P, "pedraB")
    for y in range(4, P, 6):
        for x in range(((y // 6) % 2) * 8 - 16, QW, 16):
            px(x, y, 16, 1, "juntaB")
            px(x, y, 1, 6, "juntaB")
    for x, y in [(20, 16), (50, 40), (210, 22), (250, 46), (300, 28), (36, 58), (226, 34)]:
        px(x + 1, y + 1, 14, 1, "pedraBLuz")
    # o vigamento: a viga alta e as escoras, dos dois lados do arco
    for x0, x1 in ((0, 76), (190, QW)):
        px(x0, 0, x1 - x0, 4, "madeiraEsc")
        px(x0, 4, x1 - x0, 2, "madeira")
        px(x0, 4, x1 - x0, 1, "madeiraLuz")
    for x0 in (8, 60, 204, 268, 312):
        px(x0, 0, 4, P, "madeira")
        px(x0, 0, 1, P, "madeiraLuz")
        px(x0 + 3, 0, 1, P, "madeiraEsc")
    for x0 in (8, 268):  # as escoras em diagonal
        px.linha(x0 + 4, 14, x0 + 16, 4, "madeira")
        px.linha(x0 + 4, 15, x0 + 16, 5, "madeiraEsc")
    # o chão de lajes
    px(0, P, QW, QH - P, "chao")
    px(0, P, QW, 1, "chaoLuz")
    y, i = P + 4, 0
    while y < QH:
        px(0, y, QW, 1, "chaoJunta")
        if y + 1 < QH:
            px(0, y + 1, QW, 1, "chaoLuz")
        passo = 22 + i * 6
        for x in range((i * 9) % passo, QW, passo):
            px(x, y - (4 + i), 1, 4 + i, "chaoJunta")
        y += 5 + i
        i += 1


ARCO = (82, 184)   # o vão do arco, entre as colunas
JANELA = (128, 3, 12, 30)  # x, y, largura, altura do vão de vidro


def presbiterio(px):
    """O presbitério atrás do arco: a parede do fundo (mais funda e mais escura), a janela alta de arco redondo com o
    vidro aceso em amarelo quente (como as da fachada na vila) e os losangos de chumbo, o chão dois degraus acima, o
    altar com a toalha de linho, os castiçais e o livro, o castiçal de chão de muitos braços."""
    a0, a1 = ARCO
    px(a0, 0, a1 - a0, PRESB, "fundoArco")
    for y in range(6, PRESB, 6):
        for x in range(a0 + ((y // 6) % 2) * 6, a1, 12):
            px(x, y, 12, 1, "pedraBEsc")
            px(x, y, 1, 6, "pedraBEsc")
    # a janela: o derrame claro em volta, o arco, o vidro, os chumbos
    x, y, w, h = JANELA
    px(x - 2, y - 1, w + 4, h + 3, "fundoArcoLuz")
    px(x - 2, y + h + 1, w + 4, 2, "pedraBLuz")
    px(x + 2, y - 2, w - 4, 1, "fundoArcoLuz")
    px(x + 1, y, w - 2, 1, "janela")
    px(x, y + 1, w, h, "janela")
    for yy in range(y + 1, y + h + 1):
        px(x + 3, yy, w - 6, 1, "janelaLuz" if (yy - y) % 6 < 4 else "janela")
    px(x + w // 2, y + 1, 1, h, "chumbo")         # o montante e as barras de chumbo
    for yy in range(y + 6, y + h, 6):
        px(x, yy, w, 1, "chumbo")
    px(x, y + h, w, 1, "janelaEsc")
    # os dois degraus do presbitério, entre as colunas
    px(a0, PRESB, a1 - a0, 4, "pedraBLuz")
    px(a0, PRESB, a1 - a0, 1, "calLuz")
    px(a0 - 4, PRESB + 4, a1 - a0 + 8, 4, "pedraB")
    px(a0 - 4, PRESB + 4, a1 - a0 + 8, 1, "pedraBLuz")
    px(a0 - 4, PRESB + 8, a1 - a0 + 8, P - PRESB - 8, "pedraBEsc")
    # o altar: a pedra, a toalha caindo pela frente, a faixa do meio, os castiçais, o livro
    l0, l1, lt = 116, 152, 44
    px(l0 + 2, lt + 2, l1 - l0 - 4, PRESB - lt - 2, "pedraB")
    px(l0 + 2, lt + 2, 1, PRESB - lt - 2, "pedraBLuz")
    px(l0, lt, l1 - l0, 9, "linho")
    px(l0, lt, l1 - l0, 1, "linhoLuz")
    px(l0, lt + 8, l1 - l0, 1, "linhoSombra")
    for xx in range(l0 + 3, l1, 6):
        px(xx, lt + 2, 1, 7, "linhoSombra")
    px((l0 + l1) // 2 - 3, lt + 1, 6, 8, "linhoSombra")
    px((l0 + l1) // 2 - 2, lt + 1, 4, 8, "linho")
    for cx in (l0 + 4, l1 - 6):
        px(cx - 1, lt - 1, 4, 1, "latao")
        px(cx, lt - 3, 2, 2, "latao")
        px(cx, lt - 3, 1, 2, "lataoLuz")
        px(cx, lt - 10, 2, 7, "cera")
        px(cx + 1, lt - 10, 1, 7, "ceraEsc")
    px((l0 + l1) // 2 - 4, lt - 2, 8, 2, "madeira")   # o livro fechado sobre a toalha
    px((l0 + l1) // 2 - 4, lt - 2, 8, 1, "madeiraLuz")
    # o castiçal de chão, de muitos braços, à esquerda do altar
    cx = 92
    px(cx, 38, 2, PRESB - 38, "ferro")
    px(cx - 3, PRESB - 1, 8, 1, "ferroLuz")
    px(cx - 5, 38, 12, 1, "ferroLuz")
    for xx in (cx - 5, cx - 2, cx + 1, cx + 4, cx + 6):
        px(xx, 34 + (xx % 3), 1, 4 - (xx % 3), "cera")


VELAS = [(120, 33), (146, 33), (87, 33), (90, 32), (93, 33), (96, 32), (98, 33), (40, 34), (196, 34), (306, 43), (250, 31)]


def colunas(px):
    """As duas colunas de pedra que seguram o arco, em blocos, com a base e o capitel; o arco de aduelas por cima,
    cortado pelo alto do quadro (a nave é mais alta que o que se vê)."""
    for x0, x1 in ((72, 82), (184, 194)):
        px(x0, 12, x1 - x0, P - 12, "pedraBLuz")
        px(x0, 12, 2, P - 12, "calLuz")
        px(x1 - 2, 12, 2, P - 12, "pedraB")
        for y in range(18, P, 7):
            px(x0, y, x1 - x0, 1, "pedraB")
        px(x0 - 2, 10, x1 - x0 + 4, 3, "pedraBLuz")   # o capitel
        px(x0 - 2, 12, x1 - x0 + 4, 1, "pedraB")
        px(x0 - 2, P - 4, x1 - x0 + 4, 4, "pedraBLuz")  # a base
        px(x0 - 2, P - 4, x1 - x0 + 4, 1, "calLuz")
    # o arco: a faixa de aduelas que sai de cada capitel e se curva para dentro até o alto do quadro (o resto dele está
    # acima: a nave é mais alta que o que se vê). O vão é o círculo pela borda de dentro das colunas; por fora da
    # faixa, a parede da nave.
    cx, cy, r = 133, 54.2, 66.2
    for y in range(0, 12):
        for x in range(70, 197):
            d = math.hypot(x - cx, y - cy)
            if d < r:
                continue
            if d < r + 7:
                px.p(x, y, "calLuz" if d < r + 1 else "pedraBEsc" if int(math.degrees(math.atan2(cy - y, x - cx))) % 9 == 0
                     else "pedraBLuz" if d < r + 5 else "pedraB")
            else:
                px.p(x, y, "juntaB" if y % 6 == 4 else "pedraB")


def entrada(px):
    """A porta da rua, à esquerda: o vão com a luz do dia (frio), a folha de tábuas aberta para dentro, o batente de
    madeira; a arandela com a vela na parede; o banquinho de esperar junto da parede."""
    x0, x1, y0 = 16, 30, 30
    for y in range(y0, P):
        t = (y - y0) / (P - y0)
        for x in range(x0, x1):
            px.p(x, y, "ceu" if pont(x, y, int(t * 26)) else "ceuAlto")
    px(x0, 56, x1 - x0, 2, "longe")
    px(x0, 58, x1 - x0, P - 58, "neve")
    for xx in (x0 - 3, x1):
        px(xx, y0 - 3, 3, P - y0 + 3, "madeira")
        px(xx, y0 - 3, 1, P - y0 + 3, "madeiraLuz")
    px(x0 - 4, y0 - 5, x1 - x0 + 8, 3, "madeira")
    px(x0 - 4, y0 - 5, x1 - x0 + 8, 1, "madeiraLuz")
    px(x1 + 3, y0 + 1, 6, P - y0 - 1, "madeiraMeio")   # a folha aberta
    px(x1 + 3, y0 + 1, 1, P - y0 - 1, "madeiraLuz")
    px(x1 + 8, y0 + 1, 1, P - y0 - 1, "madeiraEsc")
    for yy in (y0 + 6, P - 9):
        px(x1 + 3, yy, 6, 2, "ferro")
    # a luz do dia no chão, entrando pela porta
    for y in range(P, P + 8):
        for x in range(x0 - 2 + (y - P), x1 + 6 + (y - P) * 2):
            if pont(x, y, 7 - (y - P)):
                px.p(x, y, "neveSombra")
    # a arandela de ferro com a vela
    px(39, 40, 3, 1, "ferro")
    px(40, 38, 1, 4, "ferroLuz")
    px(39, 36, 2, 3, "cera")
    # o banquinho de esperar
    px(40, 62, 18, 2, "madeiraMeio")
    px(40, 62, 18, 1, "madeiraLuz")
    for xx in (41, 55):
        px(xx, 64, 2, P - 64, "madeira")


def bancos(px):
    """Os bancos vistos por trás, em dois blocos (três fileiras cada), o corredor no meio com a passadeira: cada fileira
    é o encosto (a tábua de cima acesa) e as cabeceiras nas pontas; as da frente, maiores e mais baixas."""
    for i, (y, cresce) in enumerate([(62, 0), (68, 2), (76, 4)]):
        for x0, x1 in ((58 - cresce, 116 + cresce // 2), (152 - cresce // 2, 214 + cresce)):
            h = 4 + i
            px(x0, y, x1 - x0, h, "madeira")
            px(x0, y, x1 - x0, 1, "madeiraLuz")
            px(x0, y + h - 1, x1 - x0, 1, "madeiraEsc")
            for xx in (x0, x1 - 3):  # as cabeceiras, um pouco mais altas
                px(xx, y - 2, 3, h + 6, "madeiraMeio")
                px(xx, y - 2, 3, 1, "madeiraLuz")
                px(xx + 2, y - 1, 1, h + 5, "madeiraEsc")


def corredor(px):
    """A passadeira do corredor, alargando para a frente (a perspectiva), com a barra de cor velha nas bordas e o claro
    da janela batendo nela."""
    for y in range(P, QH):
        k = (y - P) / (QH - P)
        a, b = round(124 - k * 8), round(144 + k * 8)
        px(a, y, b - a, 1, "tapete")
        px(a, y, 1, 1, "tapeteBorda")
        px(b - 1, y, 1, 1, "tapeteBorda")
        if 74 <= y <= 82:
            for x in range(a + 3, b - 3):
                if pont(x, y, 6):
                    px.p(x, y, "tapeteLuz")


def atendimento(px):
    """O atendimento, à direita do arco: a mesa dos panos (a jarra e a bacia de barro; o monte de panos, a pilha dos
    dobrados e o pano nas mãos vêm na figura), a caixa no chão; o armário de potes e unguentos, com a toalha pendurada; a porta
    lateral com o batente de pedra; a mesinha do incenso com o fogareiro e a vela."""
    m0, m1 = 198, 222
    px(m0, MESA, m1 - m0, 3, "madeiraMeio")
    px(m0, MESA, m1 - m0, 1, "madeiraLuz")
    px(m0, MESA + 2, m1 - m0, 1, "madeiraEsc")
    for xx in (m0 + 1, m1 - 3):
        px(xx, MESA + 3, 2, PES - MESA - 3, "madeira")
        px(xx + 1, MESA + 3, 1, PES - MESA - 3, "madeiraEsc")
    px(m0 + 1, MESA - 5, 4, 5, "barro")           # a jarra
    px(m0 + 1, MESA - 5, 1, 5, "barroLuz")
    px(m0 + 5, MESA - 4, 2, 2, "barroEsc")        # a asa
    px(m0 + 7, MESA - 2, 6, 2, "barro")           # a bacia
    px(m0 + 7, MESA - 2, 6, 1, "barroLuz")
    px(m0 + 2, 64, 9, 6, "madeira")               # a caixa no chão
    px(m0 + 2, 64, 9, 1, "madeiraLuz")
    # o armário de potes
    a0, a1 = 236, 264
    px(a0, 34, a1 - a0, P - 34, "madeiraEsc")
    for xx in (a0, a1 - 2):
        px(xx, 32, 2, P - 32, "madeira")
        px(xx, 32, 1, P - 32, "madeiraLuz")
    for y in (34, 44, 54):
        px(a0, y, a1 - a0, 2, "madeira")
        px(a0, y, a1 - a0, 1, "madeiraLuz")
    px(a0 + 2, 56, a1 - a0 - 4, P - 56, "madeira")  # as portas de baixo
    px(a0 + 13, 56, 1, P - 56, "madeiraEsc")
    for x, y, w, h, cor in [(238, 39, 4, 5, "linho"), (243, 40, 4, 4, "linho"), (249, 39, 3, 5, "barro"), (254, 40, 4, 4, "barroEsc"),
                            (238, 49, 3, 5, "barro"), (243, 50, 5, 4, "linhoSombra"), (250, 49, 3, 5, "barroLuz"),
                            (240, 28, 4, 4, "barro"), (252, 29, 5, 3, "madeiraMeio")]:
        px(x, y, w, h, cor)
        px(x, y, w, 1, cor + "Luz" if cor + "Luz" in C else cor)
    px(258, 44, 4, 10, "linho")                   # a toalha pendurada no lado
    px(258, 44, 4, 1, "linhoLuz")
    px(261, 45, 1, 9, "linhoSombra")
    # a porta lateral, de tábuas, no batente de pedra
    d0, d1 = 284, 300
    px(d0 - 3, 28, d1 - d0 + 6, P - 28, "pedraBLuz")
    px(d0 - 3, 28, d1 - d0 + 6, 2, "calLuz")
    px(d0, 31, d1 - d0, P - 31, "madeira")
    for xx in range(d0 + 3, d1, 4):
        px(xx, 31, 1, P - 31, "madeiraEsc")
    px(d1 - 4, 50, 2, 3, "ferro")
    # a mesinha do incenso, com o fogareiro e a vela
    px(302, 54, 16, 2, "madeiraMeio")
    px(302, 54, 16, 1, "madeiraLuz")
    for xx in (303, 315):
        px(xx, 56, 2, P - 56, "madeira")
    px(303, 50, 7, 4, "ferro")
    px(303, 50, 7, 1, "ferroLuz")
    px.p(305, 50, "brasa")
    px.p(307, 50, "brasa")
    px(306, 44, 2, 10, "cera")


INCENSO = (306, 49)


# ---------------------------------------------------------------- a luz
LUZES = [(134, 40, 30, 0.9), (92, 34, 14, 0.5), (40, 36, 12, 0.5), (210, 44, 18, 0.55), (306, 44, 14, 0.5), (250, 31, 10, 0.4)]


def luz(t):
    """Longe das velas, a nave escurece em degraus pontilhados (os cantos e o alto); perto, o halo quente; da porta, o
    frio no chão; a janela clareia o presbitério."""
    jx, jy, jw, jh = JANELA
    for y in range(QH):
        for x in range(QW):
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.4)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.6)))
            frio = max(0.0, 1 - math.hypot(x - 24, (y - 74) * 2.0) / 40) if y > P - 30 else 0.0
            escuro = max(0.0, 0.55 - perto * 1.1 - frio * 0.8)
            f5 = escuro / 0.55 * 4
            n = int(f5) + (1 if pont(x, y, int((f5 % 1) * 16)) else 0)
            if n:
                t.mistura(x, y, (4, 4, 6), 0.55 * n / 4)
            for lx, ly, r, f in LUZES:
                d2 = ((x - lx) ** 2 + ((y - ly) * 1.4) ** 2) / (r * r)
                if d2 < 1:
                    al = 0.18 if d2 < 0.08 else 0.11 if d2 < 0.3 else 0.06 if d2 < 0.65 else 0.03
                    t.mistura(x, y, (255, 170, 90), al * f)
            if frio > 0 and y >= P and pont(x, y, int(frio * 8)):
                t.mistura(x, y, (190, 210, 228), 0.12)


def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    presbiterio(px)
    colunas(px)
    entrada(px)
    atendimento(px)
    corredor(px)
    bancos(px)
    luz(t)
    return t


def velas(i):
    """As chamas (4 quadros), cada uma piscando no seu passo, pouco."""
    t = Tela(QW, QH)
    px = Pincel(t)
    for k, (x, y) in enumerate(VELAS):
        f = (i + k * 3) % 4
        alto = 3 if f in (0, 2) else 2 if f == 1 else 4
        px(x, y - alto + 2, 1, alto, "chamaFora")
        px.p(x, y + 1, "chama")
        if alto >= 3:
            px.p(x, y, "chamaMiolo" if f == 3 else "chama")
    return t


def fumaca(i):
    """O incenso da mesinha (8 quadros): dois fiapos de 1 px subindo devagar, ondulando, apagando no alto."""
    t = Tela(QW, QH)
    ix, iy = INCENSO
    for k in range(2):
        cabeca = iy - 3 - (i * 2 + k * 8) % 16
        for s in range(6):
            y = cabeca + s
            if y >= iy - 2 or y < iy - 24:
                continue
            x = ix + (1 if ((y + k * 2) // 3) % 2 else 0) - k
            a = 1 - (iy - y) / 24
            t.px(x, y, (int(170 * a + 60), int(166 * a + 58), int(156 * a + 56)))
    return t


def frente():
    """As silhuetas da frente: os potes à esquerda, a caixa no meio, a jarra grande à direita."""
    t = Tela(QW, QH)
    px = Pincel(t)
    v = "vulto"
    for y in range(84, QH):  # o pote grande à esquerda
        meia = 7 * math.sqrt(max(0.0, 1 - ((y - 91) / 8) ** 2))
        px(round(12 - meia), y, round(meia * 2), 1, v)
    px(9, 82, 6, 3, v)
    px(22, 90, 10, QH - 90, v)
    px(170, 88, 40, QH - 88, v)       # a caixa
    px(170, 88, 40, 1, "vultoLuz")
    for y in range(80, QH):  # a jarra à direita
        meia = 8 * math.sqrt(max(0.0, 1 - ((y - 89) / 10) ** 2))
        px(round(300 - meia), y, round(meia * 2), 1, v)
    px(296, 77, 8, 4, v)
    return t
