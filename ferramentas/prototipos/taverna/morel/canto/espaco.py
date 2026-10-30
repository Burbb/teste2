"""O canto da taverna onde Morel come (protótipo): o espaço sem pessoa nem objetos, na grade da cena (320×96).

    python ferramentas/prototipos/taverna/morel/canto/espaco.py <pasta>     # espaco.png (e ampliado) para conferir

**A câmera** é a dos olhos de quem senta diante de Morel (a referência "Encontro com Morel na taverna", aprovada pelo
Jean): perto, o tampo visto de cima, a borda do nosso lado fora do quadro. A referência tem 2,5 por 1; na altura das
cenas (96) ela ocupa 240 de largura, no tamanho dela (nada esticado, Morel não achata, a câmera não recua), e os 40 px
de cada lado continuam o canto: à esquerda, mais da parede lateral; à direita, outra baia da parede do fundo.

**A perspectiva:** o horizonte na altura dos olhos de Morel (dois adultos sentados frente a frente), em y 22, com o
ponto de fuga no meio dele (x 170): as tábuas do tampo, que correm de nós para ele, convergem para lá; a parede do fundo
fica de frente (as fiadas horizontais). Na imagem gerada, a parede da esquerda tem as fiadas descendo para o canto como
se o olho estivesse abaixo do tampo, o que não fecha com o tampo visto de cima; aqui ela é um pano em ângulo no canto
(não a 90°), com o ponto de fuga dela longe (x 600, no mesmo horizonte): as fiadas ficam suaves como na referência, a
viga de cima sobe para a esquerda como lá, e o conjunto é coerente.

**Os materiais** (as paletas das cenas aprovadas da taverna): a pedra em fiadas regulares com as juntas um tom abaixo e
a aresta de cima de cada bloco acesa só onde a vela alcança; a madeira com a aresta acesa e o lado escuro; a parede da
esquerda, perto da vela, quente; a do fundo, longe dela, escurecendo em degraus pontilhados para a direita."""
import math
import pathlib
import sys

from PIL import Image

W, H = 320, 96
OX = 40                      # a referência (240 de largura) começa aqui
HORIZONTE, FUGA_X = 22, 170  # o ponto de fuga do tampo (e do que corre de nós para o fundo)
FUGA2_X = 600                # o da parede da esquerda, em ângulo
CANTO = (95, 106)            # o esteio do canto (x de um lado ao outro)
ESTEIO_DIR = (270, 280)      # o esteio da direita (o da referência, em x 230 a 240 dela)
TRAVESSA = (9, 17)           # a travessa de madeira na parede do fundo (y)
TAMPO_Y = 72                 # a borda de lá do tampo (Morel apoia os braços logo depois dela)

def h(s):
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)


# a pedra do fundo (a da vista aprovada, escura) e a da esquerda (a mesma, aquecida pela vela)
PEDRA = [h("3d362d"), h("2e2925"), h("29251f"), h("221e1b"), h("1a1714"), h("171412")]
PEDRA_QUENTE = [h("a2784a"), h("8a643c"), h("704e30"), h("5a3e26"), h("44301e"), h("332316"), h("241810")]
MADEIRA = [h("946a3c"), h("76522f"), h("5a3e26"), h("4c3420"), h("3c2918"), h("2e2014"), h("281b10"), h("1c140d")]
TAMPO = [h("c4843e"), h("9c6438"), h("76522f"), h("5a3e26"), h("4c3420"), h("3c2918"), h("2e2014")]


def _px(img, x, y, cor):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), cor)


def luz_vela(x, y):
    """Quanto a vela (em x 58, y 48) alcança o ponto: 1 junto dela, 0 longe (em degraus, para os pontilhados)."""
    d = math.hypot((x - 58) * 0.8, (y - 48) * 1.2)
    return max(0.0, 1 - d / 150)


def parede_fundo(img):
    """A parede do fundo (de frente): da direita do canto até a borda; a travessa no alto; as fiadas de pedra."""
    x0 = CANTO[1]
    for y in range(H):
        for x in range(x0, W):
            _px(img, x, y, PEDRA[3])
    # as fiadas: 10 px de altura, os blocos de 22 a 26 px, desencontrados; a junta um tom abaixo, a aresta de cima um
    # tom acima (só nos blocos que a vela ainda alcança mais)
    fiadas = [(0, TRAVESSA[0])] + [(y, min(y + 10, TAMPO_Y)) for y in range(TRAVESSA[1], TAMPO_Y, 10)]
    for k, (y0, y1) in enumerate(fiadas):
        if y1 <= y0:
            continue
        passo, deslo = 24, (k * 13) % 24
        for y in range(y0, y1):
            for x in range(x0, W):
                bloco = (x - x0 + deslo) // passo
                bx = (x - x0 + deslo) % passo
                tom = 3 if (bloco + k) % 3 else 2  # blocos um pouco diferentes entre si
                cor = PEDRA[tom]
                if y == y1 - 1 or bx == 0:
                    cor = PEDRA[5]                 # a junta
                elif y == y0 and bx > 1:
                    cor = PEDRA[1] if luz_vela(x, y) > 0.25 else PEDRA[2]  # a aresta de cima
                _px(img, x, y, cor)
    # o escuro para a direita, longe da vela: um degrau só, com uma passagem pontilhada estreita (x 228 a 236)
    for y in range(H):
        for x in range(x0, W):
            c = img.getpixel((x, y))
            if (x >= 236 or (x >= 228 and (x + y) % 2 == 0)) and c in (PEDRA[2], PEDRA[3]):
                _px(img, x, y, PEDRA[4])
            elif (x >= 236 or (x >= 228 and (x + y) % 2 == 0)) and c == PEDRA[1]:
                _px(img, x, y, PEDRA[2])
    # a travessa: a madeira com a aresta de cima acesa e a de baixo escura
    for y in range(TRAVESSA[0], TRAVESSA[1]):
        for x in range(x0, W):
            cor = MADEIRA[3] if y == TRAVESSA[0] else MADEIRA[6] if y == TRAVESSA[1] - 1 else \
                MADEIRA[4] if y < TRAVESSA[0] + 3 else MADEIRA[5]
            _px(img, x, y, cor)
    for x in range(x0, W, 37):  # os veios e as emendas curtas
        _px(img, x + 9, TRAVESSA[0] + 4, MADEIRA[6])
        _px(img, x + 10, TRAVESSA[0] + 4, MADEIRA[6])


def _y_lateral(x, y_canto):
    """A linha da parede da esquerda que passa por y_canto no canto, rumo ao ponto de fuga dela."""
    return HORIZONTE + (y_canto - HORIZONTE) * (x - FUGA2_X) / (CANTO[0] - FUGA2_X)


def parede_lateral(img):
    """A parede da esquerda, em ângulo, aquecida pela vela: as fiadas de pedra rumo ao ponto de fuga dela e duas vigas
    (a de cima, na altura da travessa do fundo; a do meio)."""
    xs = range(0, CANTO[0])
    linhas = [-6, 3, 12, 21, 30, 39, 48, 57, 66, 75, 84]  # as fiadas no canto
    for x in xs:
        for y in range(H):
            # em que fiada está (pelas linhas que fogem para o ponto de fuga da parede)
            ys = [_y_lateral(x, yc) for yc in linhas]
            k = sum(1 for v in ys if v <= y) - 1
            if k < 0 or k >= len(ys) - 1:
                continue
            y0, y1 = ys[k], ys[k + 1]
            # o comprimento dos blocos encurta para o canto
            esc = (CANTO[0] - FUGA2_X) / (x - FUGA2_X)
            u = (CANTO[0] - x) * esc
            passo, deslo = 26, (k * 11) % 26
            bx = (u + deslo) % passo
            l = luz_vela(x, y)
            # o halo da vela em degraus (a pedra mais clara e quente perto dela), com a passagem pontilhada
            tom = 1 if l > 0.72 else 2 if l > 0.56 else 3 if l > 0.4 else 4
            if tom > 1 and (x + y) % 2 == 0 and l > (0.72, 0.56, 0.4)[tom - 2] - 0.04:
                tom -= 1
            if (int((u + deslo) // passo) + k) % 3 == 0:
                tom = min(5, tom + 1)
            cor = PEDRA_QUENTE[tom]
            if y >= y1 - 1.0 or bx < 1.0:
                cor = PEDRA_QUENTE[min(6, tom + 2)]
            elif y < y0 + 1.0 and l > 0.4:
                cor = PEDRA_QUENTE[max(0, tom - 1)]
            _px(img, x, y, cor)
    # as vigas: a da travessa (no canto, na mesma altura dela) e a do meio
    for (yc0, yc1) in ((TRAVESSA[0], TRAVESSA[1]), (32, 38)):
        for x in xs:
            a, b = _y_lateral(x, yc0), _y_lateral(x, yc1)
            for y in range(math.floor(a), math.ceil(b)):
                if not 0 <= y < H:
                    continue
                l = luz_vela(x, y)
                base = 1 if l > 0.5 else 2 if l > 0.3 else 3
                cor = MADEIRA[base - 1] if y < a + 1 else MADEIRA[base + 3] if y >= b - 1 else MADEIRA[base]
                _px(img, x, y, cor)


def esteio(img, x0, x1, y1=TAMPO_Y):
    """Um esteio de madeira de frente: a aresta da esquerda acesa (a vela), o meio, o lado escuro, os veios."""
    for y in range(0, y1):
        for x in range(x0, x1):
            k = x - x0
            l = luz_vela(x0, y)
            cor = (MADEIRA[1] if l > 0.4 else MADEIRA[2]) if k == 0 else MADEIRA[6] if k == x1 - x0 - 1 else \
                MADEIRA[5] if k >= x1 - x0 - 3 else (MADEIRA[3] if l > 0.4 else MADEIRA[4])
            _px(img, x, y, cor)
        if y % 17 == 5:
            _px(img, x0 + 3, y, MADEIRA[5])
            _px(img, x0 + 3, y + 1, MADEIRA[5])


def _tom_tampo(x, y):
    """O tom da madeira do tampo pela luz da vela: quente e claro perto dela, escurecendo em degraus para a direita
    (as passagens pontilhadas estreitas)."""
    l = luz_vela(x, y)
    t = 2 if l > 0.55 else 3 if l > 0.38 else 4 if l > 0.18 else 5
    lim = {2: 0.55, 3: 0.38, 4: 0.18}
    if t > 2 and (x + y) % 2 == 0 and l > lim.get(t - 1, 1) - 0.03:
        t -= 1  # a passagem pontilhada entre um degrau e o seguinte
    return t


def tampo(img):
    """O tampo visto de cima: as tábuas correm de nós para Morel e fogem para o ponto de fuga; a borda de lá acesa;
    perto da vela, quente; para a direita, escurecendo. A borda do nosso lado fica fora do quadro. Cada tábua num tom
    (a luz é que muda); as juntas são linhas contínuas, um tom abaixo dois, e uma ou outra emenda curta."""
    for y in range(TAMPO_Y, H):
        for x in range(W):
            t = _tom_tampo(x, y)
            cor = TAMPO[t]
            if y == TAMPO_Y:
                cor = TAMPO[max(0, t - 2)]            # a aresta da borda de lá
            elif y == TAMPO_Y + 1:
                cor = TAMPO[min(6, t + 1)]
            _px(img, x, y, cor)
    juntas_baixo = [-90, -46, -2, 42, 86, 128, 170, 212, 254, 298, 342, 386, 430]  # na borda de baixo (y 96)
    for j in juntas_baixo:
        for y in range(TAMPO_Y + 2, H):
            f = (y - HORIZONTE) / (H - HORIZONTE)
            x = round(FUGA_X + (j - FUGA_X) * f - 0.5)
            if 0 <= x < W:
                _px(img, x, y, TAMPO[min(6, _tom_tampo(x, y) + 2)])
    for (x, y, n) in ((60, 88, 5), (150, 83, 4), (232, 90, 6), (300, 80, 4)):  # as emendas das tábuas
        for k in range(n):
            _px(img, x + k, y, TAMPO[min(6, _tom_tampo(x + k, y) + 2)])


def espaco():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    parede_fundo(img)
    parede_lateral(img)
    esteio(img, *CANTO)
    esteio(img, *ESTEIO_DIR)
    tampo(img)
    return img


if __name__ == "__main__":
    saida = pathlib.Path(sys.argv[1])
    im = espaco()
    im.save(saida / "espaco.png")
    im.resize((W * 4, H * 4), Image.NEAREST).save(saida / "espaco4.png")
