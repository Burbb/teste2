"""O templo do Vau, candidata B: a composição da referência do Jean (`ferramentas/arte/referencias/cenarios internos/
Interior do Templo da Vila.png`), redesenhada na grade de 320×96 e no acabamento das cenas aprovadas. Da imagem vêm só a
composição, a distância da câmera e a organização do espaço, medidas na escala do jogo com uma grade por cima (a
imagem nunca é reduzida para virar fundo): a nave vista de frente, para o altar; o arco de pedra entre duas colunas,
com o presbitério dois degraus acima e a janela alta atrás do altar; os bancos em dois blocos vistos por trás, o
corredor no meio; a entrada com a luz do dia à esquerda; o atendimento à direita (a mesa dos panos, o armário de potes,
a porta lateral, a mesinha do incenso); as silhuetas da frente.

O que não vem da imagem: os estandartes com cruz e a cruz no avental (símbolos gerados, provisórios: o jogo só
estabelece a cruz do campanário), o vidro azul e amarelo (as janelas da igreja na vila são acesas em amarelo quente),
as texturas miúdas e as sombras suaves. O clérigo é desenhado a partir do que o jogo diz dele (figura.py).

**O espaço (segunda passada, 28/10/2026).** A primeira passada pôs tudo na linha em que o piso começava, e o piso, em
fiadas desencontradas, lia como um muro baixo: os móveis e o clérigo pareciam grudados na parede. Agora o espaço é
construído antes dos objetos (e conferido sozinho, com eles escondidos: `so_o_espaco()`):
- **um piso contínuo** da entrada ao atendimento, horizontal: as juntas transversais mais juntas no fundo e mais
  abertas na frente, e as longitudinais convergindo para o fundo da nave (o centro, acima do altar);
- **a parede de fundo** encontra o piso em PAREDE (y 58), atrás de tudo; o que se encosta nela (o armário, as portas,
  o banquinho) pisa logo à frente; o que está mais perto pisa mais embaixo (a mesa e o clérigo em PES, as fileiras de
  bancos em 68, 76 e 86), com chão à vista entre eles;
- **a única elevação é o presbitério**, debaixo do arco: o piso de cima e o do degrau claros (horizontais), as frentes
  dos dois degraus escuras (verticais); o altar é um bloco de pedra apoiado nele, com a base mais larga e a sombra no
  pé, a toalha só no alto;
- as sombras de contato, de um pixel, só depois da geometria.

A câmera é mais aberta que a da A: o clérigo tem ~31 px (na A, ~42; Marta, 52). As camadas: `fundo()`, `velas(i)` (4),
`fumaca(i)` (8), `frente()`."""
import math

from ..a.desenho import C, Pincel, Tela, pont

QW, QH = 320, 96
PAREDE = 58   # onde a parede de fundo encontra o piso (dos lados do arco)
FUNDO_P = 50  # onde a parede do fundo do presbitério encontra o piso dele (mais funda)
DEGRAU = 62   # a borda da frente do presbitério, no piso da nave
PES = 70      # onde pisam o clérigo e a mesa dos panos
MESA = 56     # o tampo da mesa dos panos
VP = (134, 18)  # para onde as juntas do piso convergem (o fundo da nave, acima do altar)

C.update({
    "pedraB": "#45403a", "pedraBLuz": "#5c554c", "pedraBEsc": "#2c2925", "juntaB": "#36322d",
    "fundoArco": "#2a2622", "fundoArcoLuz": "#363029",
    "piso": "#4a443c", "pisoLuz": "#575047", "pisoJunta": "#332f2a", "contato": "#1c1a17",
    "degrau": "#5a534a", "degrauFrente": "#33302b",
    "luzDia": "#5d6266", "luzDiaForte": "#727a80",
    "tapete": "#2e3640", "tapeteLuz": "#3c4652", "tapeteBorda": "#7a6430",
    "brasa": "#c8501a", "brasaEsc": "#7a2a10",
})


# ---------------------------------------------------------------- o espaço: paredes e piso
def paredes(px):
    """A parede de pedra da nave (blocos regulares, as juntas um tom abaixo, quase sem textura) até o piso, e o
    vigamento de madeira no alto dos dois lados."""
    px(0, 0, QW, PAREDE, "pedraB")
    for y in range(4, PAREDE, 6):
        for x in range(((y // 6) % 2) * 8 - 16, QW, 16):
            px(x, y, 16, 1, "juntaB")
            px(x, y, 1, 6, "juntaB")
    for x, y in [(20, 16), (50, 40), (210, 22), (250, 46), (300, 28), (226, 34)]:
        px(x + 1, y + 1, 14, 1, "pedraBLuz")
    px(0, PAREDE - 2, QW, 2, "pedraBEsc")   # o rodapé: a última fiada, mais escura, no encontro com o piso
    # a madeira do telhado: o frechal (a viga que corre no alto da parede e recebe o telhado), apoiado em mísulas de
    # pedra saindo da parede, no mesmo espaçamento. Cada viga termina antes do arco, com o topo da madeira à vista,
    # em cima de uma mísula: entre a ponta e o arco, parede (a viga não entra no desenho do arco)
    for x0, x1, topo in VIGAS:
        px(x0, 0, x1 - x0, 4, "madeiraEsc")
        px(x0, 4, x1 - x0, 3, "madeira")
        px(x0, 4, x1 - x0, 1, "madeiraLuz")
        px(x0, 7, x1 - x0, 1, "madeiraEsc")
        px(topo, 4, 1, 4, "madeiraLuz")      # o topo da viga (o corte da madeira), aceso
        px(topo + (1 if topo == x1 - 1 else -1), 4, 1, 4, "pedraBEsc")  # a sombra dela na parede, logo depois
    for x in MISULAS:
        px(x, 8, 6, 2, "pedraBLuz")       # a mísula: duas pedras em degrau, a de cima mais larga
        px(x, 8, 6, 1, "calLuz")
        px(x + 1, 10, 4, 2, "pedraBLuz")
        px(x + 1, 11, 4, 1, "pedraB")
        px(x + 1, 12, 4, 1, "pedraBEsc")


VIGAS = [(0, 66, 65), (200, QW, 200)]       # cada viga: de x0 a x1 e onde fica o topo (a ponta junto do arco)
MISULAS = [2, 32, 60, 200, 230, 260, 290]  # o x de cada mísula (a primeira e a última de cada lado, sob as pontas)


def arandela(px, x, base):
    """A arandela de ferro chumbada na pedra: a chapa, o braço, o copo e a vela (a chama vem na camada velas, em
    (x, base - 7))."""
    px(x + 2, base - 1, 2, 4, "ferro")           # a chapa na parede
    px(x + 2, base - 1, 1, 4, "ferroLuz")
    px(x - 1, base, 4, 1, "ferroLuz")            # o copo
    px(x - 1, base + 1, 4, 1, "ferro")
    px(x, base - 5, 2, 5, "cera")                # a vela
    px(x + 1, base - 5, 1, 5, "ceraEsc")
    px.p(x - 1, base - 2, "ceraEsc")             # o pingo de cera


FILAS = [PAREDE, 60, 63, 67, 72, 78, 85, 93]  # as juntas transversais do piso: mais juntas no fundo


def piso(px):
    """O piso de lajes, contínuo da parede de fundo até a borda de baixo: as juntas transversais (FILAS) e as
    longitudinais convergindo para VP. Cada laje tem a borda de trás acesa (a luz vem do fundo, das velas e da janela)."""
    px(0, PAREDE, QW, QH - PAREDE, "piso")
    for i, y in enumerate(FILAS[1:], 1):
        px(0, y, QW, 1, "pisoJunta")
        if y + 1 < QH:
            px(0, y + 1, QW, 1, "pisoLuz")
    for xb in range(-150, QW + 160, 30):  # o pé de cada junta longitudinal, na borda de baixo
        for y in range(PAREDE, QH):
            x = VP[0] + (xb - VP[0]) * (y - VP[1]) / (QH - VP[1])
            if 0 <= x < QW and y not in FILAS:
                px.p(round(x), y, "pisoJunta")


ARCO = (82, 184)   # o vão do arco, entre as colunas
JANELA = (128, 3, 12, 30)  # x, y, largura, altura do vão de vidro


def presbiterio(px):
    """O presbitério atrás do arco: a parede do fundo (mais funda e mais escura), a janela alta de arco redondo com o
    vidro aceso em amarelo quente (como as da fachada na vila), o piso dele, os dois degraus (o piso claro, a frente
    escura), o altar de pedra apoiado no piso dele e o castiçal de chão de muitos braços."""
    a0, a1 = ARCO
    px(a0, 0, a1 - a0, FUNDO_P, "fundoArco")
    for y in range(6, FUNDO_P, 6):
        for x in range(a0 + ((y // 6) % 2) * 6, a1, 12):
            px(x, y, 12, 1, "pedraBEsc")
            px(x, y, 1, 6, "pedraBEsc")
    px(a0, FUNDO_P - 1, a1 - a0, 1, "pedraBEsc")
    # a janela: o derrame claro em volta, o arco, o vidro, o montante e as barras
    x, y, w, h = JANELA
    px(x - 2, y - 1, w + 4, h + 3, "fundoArcoLuz")
    px(x - 2, y + h + 1, w + 4, 2, "pedraBLuz")
    px(x + 2, y - 2, w - 4, 1, "fundoArcoLuz")
    px(x + 1, y, w - 2, 1, "janela")
    px(x, y + 1, w, h, "janela")
    for yy in range(y + 1, y + h + 1):
        px(x + 3, yy, w - 6, 1, "janelaLuz" if (yy - y) % 6 < 4 else "janela")
    px(x + w // 2, y + 1, 1, h, "chumbo")
    for yy in range(y + 6, y + h, 6):
        px(x, yy, w, 1, "chumbo")
    px(x, y + h, w, 1, "janelaEsc")
    # o piso do presbitério (horizontal, claro, com as juntas recuando) e os dois degraus até o piso da nave: cada
    # degrau é o piso dele (claro) e a frente (escura); o de baixo é um pouco mais largo que o de cima
    topo, meio = FUNDO_P, 56  # o piso de cima vai de FUNDO_P a 54; a frente de cima, 54 a 56; o piso do degrau, 56 a 58
    px(a0, topo, a1 - a0, 4, "degrau")
    px(a0, topo, a1 - a0, 1, "pisoLuz")
    for xx in range(a0 + 6, a1, 14):
        px(xx, topo + 1, 1, 3, "pisoJunta")
    px(a0, topo + 4, a1 - a0, 2, "degrauFrente")
    px(a0 - 2, meio, a1 - a0 + 4, 2, "degrau")
    px(a0 - 2, meio, a1 - a0 + 4, 1, "pisoLuz")
    px(a0 - 2, meio + 2, a1 - a0 + 4, DEGRAU - meio - 2, "degrauFrente")
    px(a0 - 2, DEGRAU - 1, a1 - a0 + 4, 1, "contato")
    # o altar: um bloco de pedra com a base mais larga, apoiado no piso de cima; a laje do tampo um pouco saliente; a
    # toalha de linho só no alto, caindo um palmo pela frente; os castiçais e o livro em cima
    l0, l1, lt, pe = 118, 150, 40, topo + 3  # o tampo em lt; o pé do altar em pe (no piso de cima)
    px(l0 - 1, pe - 2, l1 - l0 + 2, 2, "pedraBLuz")       # a base, mais larga
    px(l0 - 1, pe - 2, l1 - l0 + 2, 1, "calLuz")
    px(l0 - 2, pe, l1 - l0 + 4, 1, "contato")             # a sombra no pé
    px(l0 + 1, lt + 2, l1 - l0 - 2, pe - 2 - lt - 2, "pedraB")  # o bloco
    px(l0 + 1, lt + 2, 2, pe - 2 - lt - 2, "pedraBLuz")
    px(l1 - 3, lt + 2, 2, pe - 2 - lt - 2, "pedraBEsc")
    px(l0 + 1, pe - 5, l1 - l0 - 2, 1, "pedraBEsc")        # a junta do embasamento
    px(l0, lt, l1 - l0, 2, "pedraBLuz")                    # a laje do tampo
    px(l0 + 1, lt - 1, l1 - l0 - 2, 2, "linhoLuz")         # a toalha: em cima, e caindo pela frente
    px(l0 + 2, lt + 1, l1 - l0 - 4, 4, "linho")
    px(l0 + 2, lt + 4, l1 - l0 - 4, 1, "linhoSombra")
    for xx in range(l0 + 5, l1 - 3, 6):
        px(xx, lt + 2, 1, 2, "linhoSombra")
    for cx in (l0 + 4, l1 - 6):
        px(cx - 1, lt - 2, 4, 1, "latao")
        px(cx, lt - 4, 2, 2, "latao")
        px(cx, lt - 4, 1, 2, "lataoLuz")
        px(cx, lt - 11, 2, 7, "cera")
        px(cx + 1, lt - 11, 1, 7, "ceraEsc")
    px((l0 + l1) // 2 - 4, lt - 3, 8, 2, "madeira")       # o livro fechado
    px((l0 + l1) // 2 - 4, lt - 3, 8, 1, "madeiraLuz")
    # o castiçal de chão, de muitos braços, apoiado no piso de cima, à esquerda do altar
    cx = 92
    px(cx, 38, 2, pe - 1 - 38, "ferro")
    px(cx - 3, pe - 1, 8, 1, "ferroLuz")
    px(cx - 3, pe, 8, 1, "contato")
    px(cx - 5, 39, 13, 1, "ferro")                       # a barra dos braços
    for xx in (cx - 5, cx - 2, cx + 1, cx + 4, cx + 7):  # cada vela no seu copo, em cima da barra
        px(xx - 1, 38, 3, 1, "ferroLuz")
        px(xx, 35, 1, 3, "cera")


VELAS = [(122, 27), (144, 27), (87, 33), (90, 33), (93, 33), (96, 33), (99, 33), (54, 33), (202, 33), (249, 23)]


def colunas(px):
    """As duas colunas de pedra que seguram o arco, em blocos, com o capitel e a base, de pé no piso da nave, logo à
    frente dos degraus; o arco de aduelas por cima, cortado pelo alto do quadro (a nave é mais alta que o que se vê)."""
    for x0, x1 in ((72, 82), (184, 194)):
        dentro = x1 if x0 < 133 else x0 - 3      # o lado de dentro do pilar: a espessura da parede, mais escura
        px(x0, 12, x1 - x0, DEGRAU + 2 - 12, "pedraBLuz")   # a face do pilar
        px(x0, 12, 1, DEGRAU + 2 - 12, "calLuz")
        for y in range(18, DEGRAU, 7):
            px(x0, y, x1 - x0, 1, "pedraB")
        px(dentro, 12, 3, DEGRAU + 2 - 12, "pedraB")        # o intradorso (o lado de dentro), descendo até o piso
        px(dentro + (0 if x0 < 133 else 2), 12, 1, DEGRAU + 2 - 12, "pedraBEsc")
        px(min(x0, dentro) - 1, 9, x1 - x0 + 5, 3, "pedraBLuz")   # a imposta: a pedra saliente onde o arco nasce
        px(min(x0, dentro) - 1, 9, x1 - x0 + 5, 1, "calLuz")
        px(min(x0, dentro) - 1, 11, x1 - x0 + 5, 1, "pedraB")
        px(x0 - 2, DEGRAU, x1 - x0 + 4, 4, "pedraBLuz")  # a base, no piso da nave
        px(x0 - 2, DEGRAU, x1 - x0 + 4, 1, "calLuz")
        px(x0 - 3, DEGRAU + 4, x1 - x0 + 6, 1, "contato")
    # o arco, acima da imposta: a face (a mesma largura do pilar, em pedra clara, com as juntas das aduelas em raio) e,
    # por dentro dela, o intradorso (a espessura, mais escuro); cortado pelo alto do quadro. Por fora, a parede que
    # paredes() já desenhou.
    # o círculo passa pela borda de dentro da face do pilar (x 82) na altura da imposta (y 9): a curva nasce ali,
    # em cima do pilar, e sobe para dentro (um arco abatido, como o da referência; o alto fica acima do quadro)
    cx, cy, face, esp = 133, 54.0, 10, 3
    r = math.hypot(cx - 82, cy - 9)
    for y in range(0, 9):
        for x in range(70, 197):
            d = math.hypot(x + 0.5 - cx, (y + 0.5 - cy))
            if r - esp <= d < r:
                px.p(x, y, "pedraBEsc" if d < r - esp + 1 else "pedraB")
            elif r <= d < r + face:
                ang = math.degrees(math.atan2(cy - y - 0.5, x + 0.5 - cx))
                junta = abs((ang + 3) % 12 - 6) < 0.9
                px.p(x, y, "pedraB" if junta else "calLuz" if d < r + 1 else "pedraBLuz")
            elif r + face <= d < r + face + 1:
                px.p(x, y, "pedraB")


def entrada(px):
    """A porta da rua, na parede da esquerda: o vão de pedra em arco (como a porta lateral), com o lado de fora em
    faixas chapadas (o céu de inverno, o muro ao longe, a neve), a soleira saindo um pouco para dentro, a folha de
    tábuas aberta para dentro; a luz do dia deitada no piso à frente da porta; a arandela com a vela; o banquinho de
    esperar encostado na parede."""
    x0, x1, y0 = 16, 30, 30
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    for y in range(y0 - round(r), PAREDE):     # o vão: o arco no alto, os lados retos
        for x in range(x0, x1):
            if y < y0 and math.hypot(x + 0.5 - cx, (y0 - y - 0.5)) > r:
                continue
            px.p(x, y, "ceuAlto" if y < 46 else "longe" if y < 48 else "neve")
    px(x0, 48, x1 - x0, 1, "neveSombra")
    # o batente de pedra: as ombreiras e as aduelas do arco (como o da porta lateral)
    for xx in (x0 - 3, x1):
        px(xx, y0, 3, PAREDE - y0, "pedraBLuz")
        px(xx, y0, 1, PAREDE - y0, "calLuz")
        px(xx + 2, y0, 1, PAREDE - y0, "pedraB")
    for y in range(y0 - round(r) - 3, y0):
        for x in range(x0 - 3, x1 + 3):
            d = math.hypot(x + 0.5 - cx, (y0 - y - 0.5))
            if r <= d < r + 3:
                px.p(x, y, "calLuz" if d < r + 1 else "pedraBLuz")
    # a soleira de pedra, no chão do vão, saindo para dentro (o piso dela claro, a frente escura)
    px(x0 - 3, PAREDE, x1 - x0 + 6, 1, "pedraBLuz")
    px(x0 - 3, PAREDE + 1, x1 - x0 + 6, 1, "pedraBEsc")
    # a folha da porta, aberta para dentro, girando nas dobradiças do batente: a ponta livre vem para perto de quem
    # olha (mais alta e mais baixa que o lado das dobradiças); as tábuas, as duas ferragens e a argola
    h0, h1 = x1 + 3, x1 + 12
    for x in range(h0, h1 + 1):
        k = (x - h0) / (h1 - h0)
        topo, pe = round(y0 + 1 - 2 * k), round(PAREDE + 2 * k)
        px(x, topo, 1, pe - topo + 1, "madeiraEsc" if (x - h0) % 3 == 2 else "madeiraMeio")
        px.p(x, topo, "madeiraLuz")
        for yy in (y0 + 6, PAREDE - 7):  # as ferragens, seguindo a inclinação da folha
            px.p(x, round(yy + (yy - (y0 + PAREDE) / 2) * 0.12 * k), "ferro")
        px.p(x, pe + 1, "contato")
    px(h0, y0 + 1, 1, PAREDE - y0, "madeiraLuz")
    px.p(h1 - 2, (y0 + PAREDE) // 2, "ferroLuz")  # a argola
    px.p(h1 - 2, (y0 + PAREDE) // 2 + 1, "ferro")
    # a luz do dia deitada no piso: uma mancha chapada, de borda firme, abrindo para a frente e para a direita (a
    # perspectiva do piso); mais clara junto da soleira
    for y in range(PAREDE + 2, PAREDE + 12):
        k = y - PAREDE - 2
        a_, b_ = x0 - 1 + k // 3, x1 + 2 + round(k * 1.6)
        px(a_, y, b_ - a_, 1, "luzDiaForte" if k < 3 else "luzDia")
    arandela(px, 54, 40)  # a arandela da entrada, acima do banquinho
    # o banquinho de esperar, encostado na parede, os pés no piso logo à frente dela
    px(46, 53, 14, 2, "madeiraMeio")
    px(46, 53, 14, 1, "madeiraLuz")
    for xx in (47, 57):
        px(xx, 55, 2, PAREDE + 2 - 55, "madeira")
        px(xx + 1, 55, 1, PAREDE + 2 - 55, "madeiraEsc")
    px(46, PAREDE + 2, 14, 1, "contato")


BANCOS = [72, 80, 90]            # onde cada fileira pisa (do fundo para a frente): longe o bastante do presbitério
                                 # para os degraus aparecerem pelo corredor
METRO = 28.2                     # 1 m em pixels na borda de baixo (k = 1): o clérigo, ~1,70 m, tem 32 px pisando em y 70
BANCO_ALTO, ASSENTO = 0.90, 0.45  # um banco de igreja: o alto do encosto e o assento, em metros
BLOCOS = [(20, 116), (152, 200)]  # cada bloco na borda de baixo (y = QH): as pontas seguem as linhas até VP; o da
                                  # direita acaba antes do pé da mesa dos panos


def pela_distancia(y_pe):
    """Quanto a fileira que pisa em y_pe encolhe (1 na borda de baixo), pela mesma conta do piso."""
    return (y_pe - VP[1]) / (QH - VP[1])


def bancos(px):
    """Os bancos vistos por trás, em dois blocos de três fileiras, desenhados pela perspectiva do piso: as pontas de
    cada bloco seguem duas linhas que vão a VP, e a altura de cada banco encolhe com a distância. De cada banco se vê o
    encosto, o vão até o piso, as duas
    cabeceiras (a tábua da ponta, até o chão) e um pé no meio; a sombra de contato embaixo de cada pé. O encosto é um
    painel de duas tábuas retas; a altura dele e a do banco saem da mesma conta da distância, nas três fileiras."""
    for pe in BANCOS:
        k = pela_distancia(pe)
        alto = round(BANCO_ALTO * METRO * k)     # do alto do encosto ao chão, na escala do clérigo
        topo = pe - alto
        for xb0, xb1 in BLOCOS:
            x0 = round(VP[0] + (xb0 - VP[0]) * k)
            x1 = round(VP[0] + (xb1 - VP[0]) * k)
            h = alto - round(ASSENTO * METRO * k)    # o encosto, do alto até o assento: duas tábuas
            px(x0, topo, x1 - x0, h, "madeira")
            px(x0, topo, x1 - x0, 1, "madeiraLuz")
            px(x0, topo + h // 2, x1 - x0, 1, "madeiraEsc")    # a junta entre as duas tábuas
            px(x0, topo + h - 1, x1 - x0, 1, "madeiraEsc")
            px(x0 + 2, topo + h + 1, x1 - x0 - 4, 1, "madeiraEsc")  # a borda do assento, atrás, um tom abaixo
            for xx in (x0, x1 - 2):                 # as cabeceiras, do alto do encosto ao chão
                px(xx, topo - 1, 2, alto + 1, "madeiraMeio")
                px(xx, topo - 1, 1, alto + 1, "madeiraLuz")
                px(xx - 1, pe, 4, 1, "contato")
            meio = (x0 + x1) // 2                   # o pé do meio
            px(meio, topo + h, 1, alto - h, "madeira")
            px(meio - 1, pe, 3, 1, "contato")


def corredor(px):
    """A passadeira do corredor, deitada no piso da nave do degrau até a frente, alargando (a perspectiva), com a barra
    de cor velha nas bordas e o claro da janela batendo nela."""
    for y in range(DEGRAU, QH):
        k = pela_distancia(y)                      # as bordas seguem as linhas do piso até VP
        a, b = round(VP[0] - 15 * k), round(VP[0] + 15 * k)
        px(a, y, b - a, 1, "tapete")
        px(a, y, 1, 1, "tapeteBorda")
        px(b - 1, y, 1, 1, "tapeteBorda")
        if 66 <= y <= 74:
            for x in range(a + 3, b - 3):
                if pont(x, y, 6):
                    px.p(x, y, "tapeteLuz")


MESA_X = (196, 219)  # a mesa acaba antes do clérigo: entre o pé dela e a barra do hábito, 2 px de chão


def atendimento(px):
    """O atendimento, à direita do arco, cada coisa pisando no piso: o armário de potes encostado na parede (a base no
    piso logo à frente dela), a porta lateral com a soleira, a mesinha do incenso; mais à frente, a mesa dos panos (o
    tampo com a espessura, as pernas até o piso, a travessa), com a jarra e a bacia de barro (o monte de panos, a pilha
    dos dobrados e o pano nas mãos vêm na figura); a caixa no chão, embaixo da mesa."""
    # o armário de potes, encostado na parede
    a0, a1, ab = 236, 264, PAREDE + 3
    px(a0, 34, a1 - a0, ab - 34, "madeiraEsc")
    for xx in (a0, a1 - 2):
        px(xx, 32, 2, ab - 32, "madeira")
        px(xx, 32, 1, ab - 32, "madeiraLuz")
    px(a0 - 1, 31, a1 - a0 + 2, 2, "madeiraMeio")          # a cornija
    px(a0 - 1, 31, a1 - a0 + 2, 1, "madeiraLuz")
    for y in (40, 48):
        px(a0, y, a1 - a0, 2, "madeira")
        px(a0, y, a1 - a0, 1, "madeiraLuz")
    px(a0 + 2, 50, a1 - a0 - 4, ab - 2 - 50, "madeira")     # as portas de baixo
    px(a0 + 13, 50, 1, ab - 2 - 50, "madeiraEsc")
    px(a0 - 1, ab - 2, a1 - a0 + 2, 2, "madeiraMeio")      # o rodapé do armário, no piso
    px(a0 - 1, ab - 2, a1 - a0 + 2, 1, "madeiraLuz")
    px(a0 - 2, ab, a1 - a0 + 4, 1, "contato")
    for x, y, w, h, cor in [(238, 35, 4, 5, "linho"), (243, 36, 4, 4, "linho"), (249, 35, 3, 5, "barro"), (254, 36, 4, 4, "barroEsc"),
                            (238, 43, 3, 5, "barro"), (243, 44, 5, 4, "linhoSombra"), (250, 43, 3, 5, "barroLuz"),
                            (240, 27, 4, 4, "barro")]:
        px(x, y, w, h, cor)
        px(x, y, w, 1, cor + "Luz" if cor + "Luz" in C else cor)
    px(248, 30, 4, 1, "latao")                             # a vela no pires de latão, em cima do armário
    px(248, 30, 1, 1, "lataoLuz")
    px(249, 25, 2, 5, "cera")
    px(250, 25, 1, 5, "ceraEsc")
    arandela(px, 202, 40)                                  # a arandela da parede, junto da coluna
    # a porta lateral, de tábuas, no batente de pedra, com a soleira saindo um pouco para dentro
    d0, d1 = 284, 300
    px(d0 - 3, 26, d1 - d0 + 6, PAREDE - 26, "pedraBLuz")
    px(d0 - 3, 26, d1 - d0 + 6, 2, "calLuz")
    px(d0, 29, d1 - d0, PAREDE - 29, "madeira")
    for xx in range(d0 + 3, d1, 4):
        px(xx, 29, 1, PAREDE - 29, "madeiraEsc")
    for yy in (33, 50):                                     # as dobradiças de ferro, do lado das dobras
        px(d0, yy, 9, 1, "ferroLuz")
        px(d0, yy + 1, 9, 1, "ferro")
    px(d1 - 4, 42, 2, 2, "ferroLuz")                        # a argola
    px(d1 - 4, 44, 2, 1, "ferro")
    px(d0 - 3, PAREDE, d1 - d0 + 6, 1, "pedraBLuz")
    px(d0 - 3, PAREDE + 1, d1 - d0 + 6, 1, "pedraBEsc")
    # a mesinha do incenso, no piso à frente da parede, com o fogareiro e a vela
    mb = PAREDE + 6
    px(302, 50, 16, 2, "madeiraMeio")
    px(302, 50, 16, 1, "madeiraLuz")
    px(302, 52, 16, 1, "madeiraEsc")
    for xx in (303, 315):
        px(xx, 53, 2, mb - 53, "madeira")
        px(xx + 1, 53, 1, mb - 53, "madeiraEsc")
        px(xx - 1, mb, 4, 1, "contato")
    px(304, 44, 1, 1, "brasa")                              # o fogareiro: as brasas, a borda, a tigela, o pé
    px(306, 44, 1, 1, "brasaEsc")
    px(308, 44, 1, 1, "brasa")
    px(302, 45, 9, 1, "ferroLuz")
    px(303, 46, 7, 2, "ferro")
    px(304, 48, 5, 1, "ferroEsc")
    px(305, 49, 3, 1, "ferro")
    # a mesa dos panos, mais à frente: o tampo (o piso de cima claro, a espessura escura), as pernas até o piso, a
    # travessa de baixo; a caixa embaixo; a jarra e a bacia em cima
    m0, m1 = MESA_X
    px(m0, MESA, m1 - m0, 1, "madeiraLuz")
    px(m0, MESA + 1, m1 - m0, 2, "madeiraMeio")
    px(m0, MESA + 3, m1 - m0, 1, "madeiraEsc")
    for xx in (m0 + 1, m1 - 3):
        px(xx, MESA + 4, 2, PES - MESA - 4, "madeira")
        px(xx, MESA + 4, 1, PES - MESA - 4, "madeiraLuz")
        px(xx - 1, PES, 4, 1, "contato")
    px(m0 + 3, 64, m1 - m0 - 6, 1, "madeiraEsc")            # a travessa
    px(m0 + 5, 65, 10, 5, "madeira")                        # a caixa no chão, embaixo da mesa
    px(m0 + 5, 65, 10, 1, "madeiraLuz")
    px(m0 + 4, PES, 12, 1, "contato")
    px(m0 + 1, MESA - 5, 4, 5, "barro")                     # a jarra
    px(m0 + 1, MESA - 5, 1, 5, "barroLuz")
    px(m0 + 5, MESA - 4, 2, 2, "barroEsc")
    px(m0 + 7, MESA - 2, 5, 2, "barro")                     # a bacia
    px(m0 + 7, MESA - 2, 5, 1, "barroLuz")


INCENSO = (306, 43)


# ---------------------------------------------------------------- a luz
LUZES = [(134, 38, 30, 0.9), (92, 34, 14, 0.5), (40, 36, 12, 0.5), (212, 46, 18, 0.55), (306, 42, 14, 0.5), (250, 29, 10, 0.4)]


def luz(t):
    """Longe das velas, a nave escurece em degraus pontilhados (os cantos e o alto); perto, o halo quente; da porta, o
    frio no chão; a janela clareia o presbitério."""
    for y in range(QH):
        for x in range(QW):
            if 16 <= x < 30 and 23 <= y < PAREDE:  # o lado de fora, no vão da porta: a luz do dia, sem o escuro da sala
                continue
            perto = 0.0
            for lx, ly, r, f in LUZES:
                d = math.hypot(x - lx, (y - ly) * 1.4)
                perto = max(perto, f * max(0.0, 1 - d / (r * 2.6)))
            frio = max(0.0, 1 - math.hypot(x - 28, (y - 62) * 2.0) / 40) if y > PAREDE - 30 else 0.0
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



def so_o_espaco():
    """O espaço sozinho (as paredes, o piso, o presbitério e os degraus, as colunas e o arco, a porta), sem os
    móveis nem o clérigo: a conferência do piso e dos planos antes dos objetos."""
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    piso(px)
    presbiterio(px)
    colunas(px)
    return t


def fundo():
    t = Tela(QW, QH)
    px = Pincel(t)
    paredes(px)
    piso(px)
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
    """Sem primeiro plano: as silhuetas dos cantos não tinham motivo (pontas de banco fora dos dois blocos), e o piso
    fica todo à vista. A camada continua (vazia) para a tela não mudar."""
    return Tela(QW, QH)
