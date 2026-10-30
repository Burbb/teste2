"""A pose central da queda de braço, terceira proposta: o acabamento desenhado à mão sobre a construção (protótipo).

    python ferramentas/prototipos/taverna/morel/queda3/pose.py --criar     # monta disputa.aseprite (só se não existir)
    python ferramentas/prototipos/taverna/morel/queda3/pose.py             # exporta camadas/morel-vista/queda3*.png

**O estudo de construção e o acabamento são coisas diferentes.** A construção (`juntas.py`, os volumes de
`desenho.py` e `maos.py`, da segunda proposta) verifica o apoio, o alcance, as articulações e o espaço dos derrubes;
ela fica na fonte como guia oculta (`guia`; `guia_vitorias`: o arco da pega e os dois fins). O acabamento não é a
construção iluminada: cada elemento abaixo é uma silhueta e grupos de luz escolhidos à mão, com a vista aprovada de
Morel comendo ao lado (o couro em dois ou três tons em blocos, a aresta acesa do lado da vela; o colete vermelho sobre o
corpo, com a borda clara, a costura e as tiras com fivelas quadradas; a ombreira em cunha deitada no ombro, com a faixa
clara em cima e o pontilhado só nela; as mãos simples, sem dedos). O pontilhado só onde ele diz algo (o halo da vela no
tampo, a ombreira), não em áreas grandes.

As coordenadas são da tela (320×96), tiradas da guia: a pega em (150, 26), o pulso de Morel em (154, 34) e o nosso em
(146, 37), os cotovelos em (172, 70) e (128, 90), o ombro direito de Morel em (187, 21) e o esquerdo em (253, 25).
`--criar` monta a fonte uma vez; depois ela é a autoridade (os retoques no editor), e a exportação lê dela."""
import math
import pathlib
import sys
import tempfile

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.append(str(AQUI.parent / "queda"))  # o fonte_aseprite.py

import fonte_aseprite as fa  # noqa: E402

FONTE = AQUI / "disputa.aseprite"
VISTA = AQUI.parents[1] / "camadas" / "morel-vista"
SAIDA = VISTA / "queda3.png"
CAMADAS = ["fundo", "morel_tronco", "mesa", "objetos", "morel_esquerdo", "morel_braco", "nosso_braco", "maos",
           "guia", "guia_vitorias"]
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)  # noqa: E731

# as paletas da vista aprovada (o couro e a pele do vestir.lua, o colete, o aço e a barba da fonte da vista, a madeira
# do tampo, a tigela, a vela e a caneca); a nossa lã e a nossa pele, as da segunda proposta
COURO = {"j": H("8a5a38"), "a": H("6a4a2c"), "b": H("4e3420"), "c": H("33231a"), "l": H("2a1c14")}
PUNHO_M = H("3a2716")
PELE_M = {"q": H("c09070"), "w": H("9a6c52"), "e": H("6c4a38")}
COLETE = {"a": H("a8443a"), "b": H("8a3428"), "c": H("5e241c"), "d": H("3e1610")}
ACO = {"0": H("c4c6cc"), "1": H("9a9ca4"), "2": H("6e7078"), "3": H("4e4640"), "4": H("34302c"), "5": H("2e3034")}
BARBA = {"a": H("5a3e2a"), "b": H("3e2a1c"), "c": H("2a1c14")}
LA = {"j": H("7c889a"), "a": H("5e6878"), "b": H("474f5d"), "c": H("333a45"), "l": H("262b34")}
PUNHO_N = H("2f3540")
PELE_N = {"1": H("dcb090"), "2": H("b48464"), "3": H("7e5844")}
MADEIRA = {"0": H("7a512f"), "1": H("744d2d"), "2": H("6d492b"), "3": H("654429"), "4": H("5d4027"), "5": H("543a23"),
           "6": H("4a3320"), "junta": H("4c3420"), "aresta": H("b27c44"), "aresta2": H("ae7943"), "face": H("3e2a18")}
BALCAO = {"a": H("3e2a1a"), "b": H("34231a"), "c": H("2a1c14"), "d": H("221710"), "chao": H("1c1511")}
VELA = {"0": H("fff0d0"), "1": H("e6d0ae"), "2": H("d9caab"), "3": H("bfa472"), "pavio": H("2a1c14"),
        "f0": H("fff2c4"), "f1": H("ffcc66"), "f2": H("ffa736"), "f3": H("eb9b45"),
        "prato": H("9c6438"), "prato2": H("7a4a2c"), "prato_luz": H("c4843e")}
TIGELA = {"aro": H("9c6438"), "aro2": H("7a4a2c"), "caldo": H("6a2a14"), "caldo2": H("4c2c18"), "sombra": H("2e2014"),
          "pontos": [H("c4843e"), H("6a7a2a"), H("d4b67e"), H("c8642a")]}
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


# ------------------------------------------------------------------ as ferramentas (a mão: polígonos, linhas, pontos)
class Camada:
    def __init__(self):
        self.im = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def poly(self, pts, cor):
        self.d.polygon(pts, fill=cor)

    def linha(self, pts, cor):
        self.d.line(pts, fill=cor, width=1)

    def px(self, pts, cor):
        for p in pts:
            self.im.putpixel(p, cor)

    def elipse(self, caixa, cor):
        self.d.ellipse(caixa, fill=cor)

    def pontilhado(self, pts, cor, nivel):
        """Um pontilhado de Bayer só dentro do polígono (nivel de 0 a 16): usado onde ele diz algo."""
        m = Image.new("1", (320, 96), 0)
        ImageDraw.Draw(m).polygon(pts, fill=1)
        for y in range(96):
            for x in range(320):
                if m.getpixel((x, y)) and BAYER[y % 4][x % 4] < nivel:
                    self.im.putpixel((x, y), cor)

    def mascara(self, outra):
        """Só onde esta camada tem pixel (para pintar por dentro de uma forma já desenhada)."""
        return [(x, y) for y in range(96) for x in range(320) if self.im.getpixel((x, y))[3]]

    def pixels(self):
        return {(x, y): self.im.getpixel((x, y)) for y in range(96) for x in range(320) if self.im.getpixel((x, y))[3]}


def _reta(a, b, x):
    return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])


# ------------------------------------------------------------------ o fundo e a mesa
def fundo():
    c = Camada()
    # a frente do balcão atrás de Morel, no escuro; a luz da lareira (a oeste) esquenta a esquerda
    c.poly([(0, 0), (319, 0), (319, 95), (0, 95)], BALCAO["b"])
    c.poly([(0, 0), (120, 0), (90, 40), (0, 40)], BALCAO["a"])
    c.pontilhado([(90, 0), (150, 0), (120, 40), (90, 40)], BALCAO["a"], 6)
    c.poly([(0, 0), (319, 0), (319, 3), (0, 3)], BALCAO["c"])          # a régua de cima, na sombra
    c.linha([(0, 4), (319, 4)], COURO["b"])                              # a aresta dela
    for x in range(10, 320, 15):                                         # as tábuas, de pé
        c.linha([(x, 5), (x, 95)], BALCAO["c"])
    c.poly([(250, 78), (319, 70), (319, 95), (205, 95)], BALCAO["chao"])  # o chão além da ponta da mesa
    return c


def mesa():
    c = Camada()
    longe, perto, ponta = ((0, 27), (250, 78)), ((0, 60), (98, 96)), ((250, 78), (213, 96))
    tampo = [(0, 27), (250, 78), (213, 96), (98, 96), (0, 60)]
    c.poly(tampo, MADEIRA["3"])
    # a luz da vela (à esquerda): o tampo mais claro em volta dela, o pontilhado só na passagem
    c.poly([(0, 30), (70, 44), (95, 62), (80, 86), (30, 80), (0, 60)], MADEIRA["2"])
    c.pontilhado([(70, 44), (110, 52), (120, 70), (95, 86), (80, 86), (95, 62)], MADEIRA["2"], 8)
    c.poly([(14, 62), (40, 58), (72, 64), (78, 74), (52, 82), (18, 76)], MADEIRA["1"])
    c.pontilhado([(14, 62), (40, 58), (72, 64), (78, 74), (52, 82), (18, 76)], MADEIRA["0"], 4)
    # o lado de Morel e a ponta da mesa, mais escuros (a sombra dele, o lampião longe)
    c.poly([(150, 57), (250, 78), (230, 88), (185, 84), (160, 70)], MADEIRA["4"])
    c.pontilhado([(130, 52), (150, 57), (160, 70), (150, 74), (130, 64)], MADEIRA["4"], 8)
    c.poly([(205, 80), (250, 78), (225, 90)], MADEIRA["5"])
    # as juntas das tábuas, para o ponto de fuga do tampo (de cá para lá), e os riscos de uso
    for xa, xb in ((-14, 64), (16, 92), (44, 118), (73, 145), (102, 172), (128, 197), (156, 222), (180, 245)):
        a, b = (xa, 96), (xb, 30)
        pts = [(x, round(_reta(a, b, x))) for x in range(min(xa, xb), max(xa, xb) + 1)]
        for (x, y) in pts:
            if 0 <= x < 320 and 0 <= y < 96 and y > _reta(*longe, x) + 1 and (x > 98 or y < _reta(*perto, x)) \
                    and (x < 213 or y < _reta(*ponta, x)):
                c.px([(x, y)], MADEIRA["junta"])
    for a, b in (((30, 49), (38, 50)), ((112, 62), (118, 61)), ((60, 70), (66, 72)), ((196, 74), (203, 76))):
        c.linha([a, b], MADEIRA["5"])
    # as arestas: a de lá (acesa pela vela até perto de Morel), a de cá e a ponta, com a espessura
    c.linha([(0, 27), (150, 58)], MADEIRA["aresta"])
    c.linha([(151, 58), (250, 78)], MADEIRA["aresta2"])
    c.linha([(0, 60), (98, 96)], MADEIRA["aresta2"])
    c.poly([(0, 61), (98, 97), (78, 97), (0, 68)], MADEIRA["face"])
    c.poly([(250, 79), (250, 86), (221, 96), (214, 96)], MADEIRA["face"])
    c.linha([(250, 78), (213, 96)], MADEIRA["aresta2"])
    return c


def objetos():
    """A tigela deslizada (atrás), a caneca e a vela com o prato e a chama (na frente, do nosso lado)."""
    c = Camada()
    # a tigela, longe (na metade de lá, além da vela): o aro aceso em cima, o caldo, o bojo na sombra
    c.elipse((52, 38, 98, 51), TIGELA["sombra"])
    c.elipse((52, 37, 98, 49), TIGELA["aro2"])
    c.elipse((53, 37, 97, 46), TIGELA["aro"])
    c.elipse((57, 39, 93, 45), TIGELA["caldo"])
    c.elipse((62, 41, 92, 45), TIGELA["caldo2"])
    c.px([(64, 41), (72, 42), (80, 41), (86, 43), (69, 43)], TIGELA["pontos"][0])
    c.px([(76, 40), (84, 42)], TIGELA["pontos"][1])
    c.px([(70, 41), (89, 42)], TIGELA["pontos"][2])
    c.linha([(56, 38), (66, 37)], VELA["prato_luz"])
    # a caneca de estanho: o corpo, as duas cintas, a asa à esquerda, a boca
    c.elipse((22, 48, 30, 58), ACO["3"])
    c.elipse((24, 50, 28, 56), (0, 0, 0, 0))
    c.poly([(27, 46), (41, 46), (41, 62), (27, 62)], ACO["2"])
    c.poly([(27, 46), (30, 46), (30, 62), (27, 62)], ACO["1"])
    c.linha([(28, 47), (28, 61)], ACO["0"])
    c.poly([(37, 46), (41, 46), (41, 62), (37, 62)], ACO["3"])
    for y in (50, 58):
        c.linha([(27, y), (41, y)], ACO["4"])
    c.elipse((27, 44, 41, 48), ACO["1"])
    c.elipse((29, 45, 39, 47), ACO["5"])
    c.elipse((26, 61, 42, 64), ACO["3"])
    # a vela: o prato de cobre, a cera (a luz da própria chama na esquerda), os pingos, o pavio e a chama
    c.elipse((38, 69, 58, 76), VELA["prato2"])
    c.elipse((39, 69, 57, 74), VELA["prato"])
    c.linha([(41, 70), (49, 69)], VELA["prato_luz"])
    c.poly([(44, 36), (52, 36), (52, 72), (44, 72)], VELA["1"])
    c.poly([(44, 36), (46, 36), (46, 72), (44, 72)], VELA["0"])
    c.poly([(50, 36), (52, 36), (52, 72), (50, 72)], VELA["3"])
    c.elipse((44, 35, 52, 37), VELA["2"])
    c.px([(45, 38), (45, 39), (45, 40), (51, 41), (51, 42)], VELA["0"])
    c.linha([(48, 32), (48, 35)], VELA["pavio"])
    c.poly([(48, 22), (51, 27), (51, 31), (48, 34), (45, 31), (45, 27)], VELA["f3"])
    c.poly([(48, 24), (50, 28), (50, 31), (48, 33), (46, 31), (46, 28)], VELA["f1"])
    c.poly([(48, 27), (49, 29), (49, 31), (48, 32), (47, 31), (47, 29)], VELA["f0"])
    return c


# ------------------------------------------------------------------ Morel
def morel_tronco():
    """O peito: o couro aberto, o colete vermelho sobre o corpo (a borda clara do lado da vela, a costura, as tiras com
    as fivelas quadradas), a gola, o pescoço e a borda da barba no alto, o punho da espada atrás do ombro direito, a
    ombreira em cunha no ombro esquerdo."""
    c = Camada()
    # o couro: a forma do tronco (embaixo, a mesa cobre), o meio-tom; atrás do braço direito, a sombra dele; a
    # lapela acesa junto do colete; o lado da ombreira na sombra
    corpo = [(188, 12), (210, 5), (238, 5), (256, 14), (262, 40), (262, 90), (186, 90), (184, 40)]
    c.poly(corpo, COURO["a"])
    c.poly([(188, 12), (198, 9), (200, 90), (186, 90), (184, 40)], COURO["b"])
    c.poly([(198, 9), (201, 8), (203, 90), (200, 90)], COURO["c"])          # a sombra do braço no peito
    c.poly([(202, 10), (207, 9), (205, 90), (203, 90)], COURO["j"])         # a lapela acesa
    c.poly([(242, 10), (256, 14), (262, 40), (262, 90), (243, 90)], COURO["b"])
    c.linha([(248, 26), (251, 70)], COURO["c"])                              # a dobra do couro na sombra
    # o colete sobre o peito: a borda acesa do lado da vela, o meio, o lado da sombra que se curva, a costura; as
    # bordas se abrem um pouco embaixo (o peito)
    c.poly([(208, 10), (235, 10), (238, 90), (206, 90)], COLETE["b"])
    c.poly([(208, 10), (212, 10), (211, 90), (206, 90)], COLETE["a"])
    c.linha([(212, 12), (212, 60)], COLETE["a"])
    c.poly([(228, 10), (235, 10), (238, 90), (231, 90)], COLETE["c"])
    c.linha([(234, 10), (237, 90)], COLETE["d"])
    c.linha([(221, 16), (222, 90)], COLETE["d"])                             # a costura do meio
    c.linha([(207, 10), (205, 90)], COURO["c"])                              # a sombra da lapela no colete
    c.poly([(213, 10), (230, 10), (222, 18)], COURO["l"])                    # o decote: a camisa escura no V
    # as tiras com as fivelas quadradas, curvas com o peito (descem nos lados)
    for y in (31, 48):
        pts = [(206, y + 1), (214, y), (230, y), (238, y + 2)]
        for k in range(3):
            c.linha([(x, yy + k) for x, yy in pts], ACO["4"] if k else ACO["3"])
        c.poly([(219, y - 2), (225, y - 2), (225, y + 4), (219, y + 4)], ACO["2"])
        c.linha([(219, y - 2), (224, y - 2)], ACO["0"])
        c.linha([(219, y - 1), (219, y + 3)], ACO["1"])
        c.poly([(221, y), (223, y), (223, y + 2), (221, y + 2)], ACO["5"])
    # a gola do couro, o pescoço e a borda da barba (o rosto fica acima do quadro)
    c.poly([(204, 9), (212, 3), (232, 3), (242, 9), (236, 11), (222, 6), (208, 11)], COURO["c"])
    c.poly([(213, 0), (233, 0), (230, 4), (216, 4)], PELE_M["e"])
    c.poly([(210, 0), (236, 0), (234, 3), (228, 5), (222, 6), (216, 5), (212, 3)], BARBA["b"])
    c.linha([(211, 0), (216, 4)], BARBA["a"])
    c.px([(220, 5), (224, 5), (229, 4)], BARBA["c"])
    # o punho da espada atrás do ombro direito: o cabo de couro na diagonal, a guarda, o pomo de aço
    c.linha([(193, 0), (198, 10)], COURO["b"])
    c.linha([(194, 0), (199, 10)], COURO["a"])
    c.linha([(192, 10), (203, 8)], ACO["2"])
    c.linha([(192, 9), (202, 7)], ACO["1"])
    # a ombreira: a cunha de aço deitada no ombro esquerdo (como na vista: estreita, na diagonal, escura), a aresta clara
    # em cima, o pontilhado das lâminas só nela, a sombra embaixo dela no braço
    omb = [(238, 9), (248, 7), (258, 11), (266, 20), (271, 31), (270, 38), (264, 36), (257, 27), (248, 18), (240, 14)]
    c.poly(omb, ACO["3"])
    c.poly([(238, 9), (248, 7), (258, 11), (266, 20), (269, 27), (261, 19), (250, 12), (241, 12)], ACO["2"])
    c.linha([(239, 9), (248, 7), (257, 10), (264, 17)], ACO["1"])
    c.px([(247, 8), (248, 8)], ACO["0"])
    c.pontilhado([(246, 13), (256, 14), (264, 24), (267, 32), (262, 30), (254, 21)], ACO["1"], 5)
    c.poly([(257, 27), (264, 36), (270, 38), (269, 41), (263, 40), (255, 30)], COURO["l"])
    return c


def morel_esquerdo():
    """O braço esquerdo de Morel: o braço de cima saindo da ombreira, o cotovelo para fora, o antebraço voltando para a
    mão que agarra a borda de lá da mesa."""
    c = Camada()
    c.poly([(256, 36), (270, 42), (286, 68), (282, 78), (272, 78), (258, 50)], COURO["a"])
    c.poly([(256, 36), (262, 39), (276, 70), (272, 78), (258, 50)], COURO["j"])
    c.poly([(278, 50), (286, 68), (282, 78), (279, 76)], COURO["b"])
    c.poly([(282, 66), (280, 78), (244, 76), (236, 66), (246, 64)], COURO["b"])  # o antebraço, um tom abaixo
    c.linha([(246, 64), (282, 66)], COURO["a"])
    c.poly([(240, 64), (246, 64), (248, 75), (241, 75)], PUNHO_M)
    c.poly([(228, 66), (236, 63), (241, 66), (240, 74), (232, 75), (227, 71)], PELE_M["w"])  # a mão na borda
    c.poly([(229, 66), (235, 64), (237, 66), (232, 68)], PELE_M["q"])
    c.linha([(228, 73), (239, 75)], PELE_M["e"])
    c.linha([(244, 79), (282, 80)], MADEIRA["6"])                                          # a sombra no tampo
    return c


def morel_braco():
    """O braço direito de Morel: o braço de cima com a manga de couro (a aresta acesa na esquerda, a sombra na direita,
    a costura do ombro, a dobra de dentro do cotovelo), o cotovelo no tampo, o antebraço um tom abaixo subindo até o
    punho escuro da manga."""
    c = Camada()
    braco = [(176, 9), (193, 7), (198, 19), (191, 50), (185, 70), (178, 76), (168, 74), (167, 56), (171, 28)]
    c.poly(braco, COURO["a"])
    c.poly([(176, 9), (183, 8), (177, 30), (172, 56), (169, 74), (167, 56), (171, 28)], COURO["j"])
    c.poly([(190, 9), (198, 19), (191, 50), (186, 66), (184, 50)], COURO["b"])
    c.linha([(178, 11), (195, 12)], COURO["b"])                                   # a costura do ombro
    c.linha([(183, 54), (180, 62)], COURO["c"])                                   # a dobra de dentro do cotovelo
    c.linha([(186, 57), (183, 64)], COURO["c"])
    # o antebraço, do cotovelo ao punho, por cima do braço de cima (vem para a frente)
    ante = [(166, 75), (180, 71), (168, 46), (161, 32), (150, 34), (153, 45), (159, 60)]
    c.poly(ante, COURO["b"])
    c.poly([(166, 75), (171, 73), (161, 52), (154, 38), (150, 34), (153, 45), (159, 60)], COURO["a"])
    c.linha([(167, 74), (152, 40)], COURO["j"])
    c.poly([(174, 60), (180, 71), (176, 72), (170, 62)], COURO["c"])
    c.poly([(150, 33), (161, 31), (163, 36), (152, 38)], PUNHO_M)                 # o punho da manga
    c.poly([(167, 76), (179, 72), (184, 75), (172, 79)], MADEIRA["6"])            # a sombra do cotovelo no tampo
    return c


# ------------------------------------------------------------------ o nosso braço e as mãos
def nosso_braco():
    """O nosso braço: o ombro e o braço de cima no primeiro plano, na sombra (o tronco fica fora do quadro), o cotovelo
    no tampo, o antebraço de lã subindo até a pega (a aresta acesa na esquerda, as dobras de dentro do cotovelo, o
    punho escuro)."""
    c = Camada()
    c.poly([(56, 84), (80, 80), (104, 83), (126, 86), (136, 91), (136, 96), (50, 96)], LA["c"])
    c.linha([(80, 80), (104, 83), (124, 86)], LA["b"])
    c.poly([(0, 90), (24, 84), (60, 84), (52, 96), (0, 96)], LA["l"])            # o ombro, na beirada
    ante = [(121, 92), (139, 95), (155, 44), (154, 37), (142, 36), (133, 52), (123, 80)]
    c.poly(ante, LA["a"])
    c.poly([(121, 92), (126, 92), (130, 70), (140, 44), (142, 36), (133, 52), (123, 80)], LA["j"])
    c.poly([(134, 94), (139, 95), (155, 44), (150, 44), (140, 72)], LA["b"])
    c.linha([(138, 94), (154, 46)], LA["c"])
    c.linha([(131, 82), (135, 76)], LA["b"])                                      # as dobras da lã perto do cotovelo
    c.linha([(129, 76), (133, 70)], LA["b"])
    c.poly([(141, 36), (154, 37), (154, 42), (140, 41)], PUNHO_N)                 # o punho da manga
    c.poly([(139, 94), (150, 92), (148, 96), (140, 96)], MADEIRA["6"])            # a sombra do cotovelo no tampo
    return c


def maos():
    """A pega: duas formas simples. A mão de Morel atrás, mais escura e quente, com o nó do polegar em cima; a nossa
    na frente, mais clara, o nosso polegar por cima do dele; os dedos dele numa faixa só, dobrados sobre a borda do
    nosso punho; um pixel de sombra onde uma passa na frente da outra."""
    c = Camada()
    c.poly([(150, 20), (156, 16), (162, 21), (163, 30), (159, 35), (152, 35), (149, 28)], PELE_M["w"])
    c.poly([(151, 20), (156, 17), (159, 19), (154, 21)], PELE_M["q"])
    c.poly([(159, 23), (162, 21), (163, 30), (159, 35), (157, 33), (160, 28)], PELE_M["e"])
    c.poly([(140, 25), (146, 20), (152, 21), (155, 29), (152, 38), (144, 39), (139, 33)], PELE_N["2"])
    c.poly([(140, 25), (146, 20), (149, 21), (144, 27), (141, 34), (139, 33)], PELE_N["1"])
    c.poly([(152, 23), (155, 29), (152, 38), (149, 37), (152, 30)], PELE_N["3"])
    c.linha([(146, 20), (152, 19), (155, 21)], PELE_N["1"])                        # o nosso polegar por cima
    c.linha([(147, 21), (154, 22)], PELE_N["3"])
    c.linha([(156, 22), (156, 37)], PELE_M["e"])                                   # a sombra da nossa na dele
    # os dedos de Morel dobrados sobre a borda do nosso punho (a pega fechada dos dois lados), uma faixa só
    c.poly([(150, 25), (155, 23), (156, 34), (151, 35)], PELE_M["w"])
    c.linha([(150, 25), (154, 23)], PELE_M["q"])
    c.linha([(149, 26), (150, 35)], PELE_N["3"])                                   # a sombra dos dedos dele na nossa
    return c


# ------------------------------------------------------------------ as guias (ocultas)
def guias():
    """A construção da disputa (`desenho.py` e `maos.py` na câmera desta proposta) e o espaço dos dois derrubes (o
    arco da pega e os fins, com os antebraços de quem perde deitados), em cores lisas."""
    import juntas as J
    import desenho as D
    import maos as M
    g, gv = {}, {}
    t = D.Tela()
    p = J.poses()["disputa"]
    cor = {"mb": (205, 62, 52), "ma": (238, 132, 52), "nb": (40, 70, 165), "na": (72, 132, 232)}
    for S, E, W, b, a in (("ombro_m", "cotovelo_m", "pulso_m", "mb", "ma"), ("ombro_n", "cotovelo_n", "pulso_n", "nb", "na")):
        D.capsula(t, b, p[S], p[E], 5.6, 5.0, lambda n, tt, q, b=b: cor[b] + (120,))
        D.capsula(t, a, p[E], p[W], 4.8, 3.6, lambda n, tt, q, a=a: cor[a] + (120,))
    M.construir(t, "disputa", lambda parte, n: ((240, 200, 120) if parte.startswith("nos") else (200, 120, 60)) + (120,))
    g.update(t.cor)
    alto, r = J.pega(0)
    A, B = J.COTOVELO_NOSSO, J.COTOVELO_MOREL
    u = J._un(J._sub(B, A))
    centro = J._sub(alto, (0.0, r, 0.0))
    lado = J._un((-u[2], 0.0, u[0]))
    for k in range(-90, 91, 2):
        a = math.radians(k)
        q = J._add(centro, J._add(J._mul((0.0, 1.0, 0.0), r * math.cos(a)), J._mul(lado, r * math.sin(a))))
        if q[1] >= J.TAMPO_MAO - 0.01:
            x, y, _ = J.tela(q)
            if 0 <= x < 320 and 0 <= y < 96:
                gv[(int(x), int(y))] = (255, 240, 120, 255)
    for nome in ("vitoria_jogador", "vitoria_morel"):  # os fins: os antebraços em linha, a pega marcada
        pv = J.poses()[nome]
        for E, W in (("cotovelo_m", "pulso_m"), ("cotovelo_n", "pulso_n")):
            a, b = J.tela(pv[E]), J.tela(pv["pega"])
            n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
            for k in range(n + 1):
                x, y = a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n
                if 0 <= x < 320 and 0 <= y < 96:
                    gv[(int(x), int(y))] = (255, 120, 220, 255)
        x, y = J.tela(pv["pega"])[:2]
        for d in range(-2, 3):
            for q in ((int(x) + d, int(y)), (int(x), int(y) + d)):
                if 0 <= q[0] < 320 and 0 <= q[1] < 96:
                    gv[q] = (255, 255, 255, 255)
    return g, gv


def camadas():
    out = {"fundo": fundo().pixels(), "morel_tronco": morel_tronco().pixels(), "mesa": mesa().pixels(),
           "objetos": objetos().pixels(), "morel_esquerdo": morel_esquerdo().pixels(),
           "morel_braco": morel_braco().pixels(), "nosso_braco": nosso_braco().pixels(), "maos": maos().pixels()}
    out["guia"], out["guia_vitorias"] = guias()
    return out


def plano(c, guias_=False):
    im = Image.new("RGBA", (320, 96), (0, 0, 0, 255))
    for cam in CAMADAS:
        if cam.startswith("guia") and not guias_:
            continue
        lay = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
        for q, cor in c.get(cam, {}).items():
            lay.putpixel(q, cor)
        im.alpha_composite(lay)
    return im


def criar(refazer=False):
    print(fa.montar(FONTE, 320, 96, CAMADAS, ["disputa"], [camadas()], ocultas=("guia", "guia_vitorias"),
                    opacidade={"guia": 150}, refazer=refazer))


def exportar():
    with tempfile.TemporaryDirectory() as tmp:
        q = fa.quadros(FONTE, tmp, ignorar=("guia", "guia_vitorias"))[0]
        im = Image.open(q).convert("RGBA")
    im.save(SAIDA, optimize=True)
    # a folha de comparação: a vista aprovada de Morel comendo (a referência) e a pose, lado a lado, e a pose com as guias
    ref = Image.open(VISTA / "parada.png").convert("RGBA")
    folha = Image.new("RGBA", (640, 192), (24, 22, 20, 255))
    folha.alpha_composite(ref, (0, 0))
    folha.alpha_composite(im, (320, 0))
    folha.alpha_composite(plano(camadas(), guias_=True), (320, 96))
    folha.alpha_composite(ref.crop((160, 0, 320, 96)), (0, 96))
    folha.alpha_composite(im.crop((160, 0, 320, 96)), (160, 96))
    folha.save(SAIDA.with_name("queda3-comparacao.png"), optimize=True)
    print(f"{SAIDA.name} e queda3-comparacao.png")


if __name__ == "__main__":
    if "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
    elif "--previa" in sys.argv:
        S = pathlib.Path(sys.argv[-1])
        c = camadas()
        plano(c).save(S / "q3.png")
        plano(c, guias_=True).save(S / "q3-guias.png")
    else:
        exportar()
