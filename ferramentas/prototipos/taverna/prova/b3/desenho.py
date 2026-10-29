"""A B3: a B2 com os ombros e os braços dos dois jogadores redesenhados (a mesa, os banquinhos, a escala, as pernas, as
cabeças e as poses gerais continuam os da B2). Só semeia o retoque: `fonte.py --criar` copia a fonte da B2 e troca, nas
camadas verde e ocre, só os pixels em que este desenho difere do da B2.

O problema da B2: os braços liam ambíguos (pareciam sair do ombro oposto; era preciso achar a outra mão para entender a
pose). A correção decide primeiro a orientação do peito e dos ombros e depois separa cada braço por silhueta,
sobreposição e poucos planos de luz e sombra, sem contorno pesado:

- **o de verde:** o peito em três quartos, virado para a câmera e para a mesa; o decote no meio do peito mostra o giro.
  O ombro de cá (o da esquerda) é uma calota redonda acesa por cima; o braço desce **à frente do tronco**, com uma faixa
  das costas à vista atrás dele e a sombra dele no peito; o cotovelo dobra e o antebraço atravessa a barriga até a mão na
  coxa. O ombro de lá aparece atrás da barba; o peito passa **na frente da raiz** do braço da mesa, que sai à direita do
  tronco, mais escuro, com a aresta acesa pela vela; braço e antebraço formam um V aberto (o fundo à vista entre eles),
  com o cotovelo no tampo.
- **o de ocre:** o ombro de cá é uma calota acesa no alto da frente do tronco; a manga sai dela num tom próprio (o alto
  aceso, o meio claro, a dobra de baixo escura) sobre a túnica de tom médio, que fica na sombra do braço logo abaixo
  dele; o cotovelo marca a dobra; o punho dobrado da manga, o antebraço e a mão na peça.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(AQUI)))

from prova import conjunto as C  # noqa: E402
from prova.b2 import desenho as B2  # noqa: E402
from prova.b2.desenho import partes, tom  # noqa: E402

W, H, S = B2.W, B2.H, B2.S


def _verde():
    p = B2.verde_partes()
    # o braço da mesa (o de lá) primeiro: o peito vem por cima da raiz dele
    sup = {25: (36, 40), 26: (36, 40), 27: (37, 41), 28: (37, 41), 29: (38, 41), 30: (38, 41), 31: (39, 42),
           32: (39, 42), 33: (40, 43), 34: (40, 44), 35: (41, 45)}
    braco_la = {y: tom(a, b, "zn", "n", "Z") for y, (a, b) in sup.items()}
    braco_la.update({36: (41, "znZWWZ"), 37: (42, "znZWWZ"), 38: (43, "nnNNZn"), 39: (44, "nnnnn")})
    # o tronco: as costas à esquerda (atrás do braço de cá), o peito de frente (médio), a frente acesa pela vela
    bordas = {23: (26, 33), 24: (23, 35), 25: (21, 36), 26: (19, 37), 27: (18, 37), 28: (17, 38), 29: (16, 38),
              30: (15, 38), 31: (13, 39), 32: (12, 39), 33: (12, 39), 34: (12, 39)}
    bordas.update({y: (12, 40) for y in range(35, 41)})
    bordas.update({41: (12, 39), 42: (12, 39), 43: (12, 39), 44: (12, 37), 45: (12, 34), 46: (12, 30), 47: (12, 26),
                   48: (13, 22)})
    # ao lado do braço da mesa, a frente do peito fica no tom médio (a aresta acesa é a do braço); abaixo dele, acesa
    tronco = {y: [tom(a, b, "zn", "N", "N" if y < 36 else "ZN")] for y, (a, b) in bordas.items()}
    tronco[23] = [(26, "nNNNZZZN")]
    tronco[24] = [(23, "nNNNNNZZZZZZN")]
    tronco[24].append((28, "SssS"))                                 # o decote, no meio do peito
    tronco[25].append((28, "Sss"))
    tronco[26].append((29, "Ss"))
    tronco[27].append((29, "S"))
    for y in range(29, 39):                                         # a sombra do braço de cá no peito
        tronco[y].append((23, "nn"))
    for y in (42, 43):                                              # o cinto
        tronco[y].append((13, "c" + "C" * 13 + "f" + "C" * 11 + "c"))
    tronco[44].append((13, "n"))
    tronco[48].append((13, "zzzzzzzzzz"))
    # o braço de cá: a calota do ombro acesa por cima, a manga à frente das costas, o punho dobrado no cotovelo
    braco_ca = {24: (19, "nZWWZ"), 25: (17, "nNZWWZZN"), 26: (16, "zNNZZZZNn"), 27: (15, "zNNNZZNNNz"),
                28: (15, "zNNNNNNZz"), 29: (15, "zNNNNNNZz")}
    braco_ca.update({y: (15, "zNNNNNZz") for y in range(30, 36)})
    braco_ca.update({36: (15, "nZWWWZNz"), 37: (15, "zNZZZNnz"), 38: (16, "zznnz")})
    mao_coxa = {38: (20, "Ssl"), 39: (19, "Sssssl"), 40: (20, "Sssssl"), 41: (21, "Sssssl"), 42: (22, "Sssssll"),
                43: (22, "SsssslllS"), 44: (23, "SsSsSsS"), 45: (24, "SSsSsS"), 46: (25, "SS")}
    # o antebraço da mesa à direita do braço (o V aberto) e o punho no queixo
    ante = {29: (43, "Ssll"), 30: (44, "Sssl"), 31: (44, "Sssl"), 32: (45, "Sssl"), 33: (45, "Sssl"),
            34: (45, "ZWWZ"), 35: (46, "WWZ")}
    ordem = dict(coxa_la=p["coxa_la"], canela_la=p["canela_la"], bota_la=p["bota_la"], coxa_ca=p["coxa_ca"],
                 canela_ca=p["canela_ca"], bota_ca=p["bota_ca"], braco_la=braco_la, tronco=tronco, cabeca=p["cabeca"],
                 braco_ca=braco_ca, mao_coxa=mao_coxa, ante=ante, punho=p["punho"])
    return partes(*ordem.values())


def _ocre():
    p = B2.ocre_partes()
    tronco = p["tronco"]
    for y, a in ((27, 80), (28, 80), (29, 80), (30, 80), (31, 81), (32, 81), (33, 82), (34, 82)):
        tronco[y] = tronco[y] + [(a, "yyyyyy")]                       # a sombra do braço estendido na túnica
    tronco[35] = tronco[35] + [(83, "Yyy")]
    # o braço estendido: a calota do ombro, a manga num tom próprio (o alto aceso, a dobra de baixo escura), o cotovelo
    braco = {25: (84, "WWWX"), 26: (82, "XWWWWXY"), 27: (79, "WWWWXXXXXY"), 28: (76, "WWWXXXXXXXXXy"),
             29: (73, "WWWXXXXXXXXXXyx"), 30: (71, "WXXXXXXXXXXyyx"), 31: (70, "XXXXXXXyyyyx"),
             32: (70, "yyyyyyyxx"), 33: (71, "xxxx")}
    punho_manga = {29: (69, "WW"), 30: (67, "WWWX"), 31: (67, "XXXy"), 32: (67, "Xyyx"), 33: (68, "xx")}
    ordem = dict(p)
    ordem["tronco"], ordem["braco"], ordem["punho_manga"] = tronco, braco, punho_manga
    return partes(*ordem.values())


VERDE, OCRE = _verde(), _ocre()


def camada(linhas, pal):
    t = B2.D.Tela(W, H)
    C.Pincel(t).trechos(linhas, pal)
    C.luz(t, S)
    return t


def camadas():
    """As duas camadas que a B3 muda, já com a luz da sala: {nome: (B2, B3)}."""
    return {"verde": (camada(B2.VERDE, B2.PAL_VERDE), camada(VERDE, B2.PAL_VERDE)),
            "ocre": (camada(B2.OCRE, B2.PAL_OCRE), camada(OCRE, B2.PAL_OCRE))}
