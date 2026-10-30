"""O estudo do tronco de Morel no canto (protótipo): a construção que gerou o rascunho da grade `TRONCO` de `morel.py`.

    python ferramentas/prototipos/taverna/morel/canto/tronco_estudo.py --grade         # imprime o rascunho da grade
    python ferramentas/prototipos/taverna/morel/canto/tronco_estudo.py --guia <png>    # a construção (guia oculta)

A primeira candidata desenhava o tronco como um polígono de 92 px (x 126 a 218, mais largo que as duas juntas dos
ombros) preenchendo tudo entre os braços, e a gola como uma faixa reta de 4 px entre o colete e a barba. Aqui o tronco
sai das formas, nesta ordem (a skill `arte-personagens-fenda`, "O tronco sob os braços"):
- **as medidas pela cabeça:** a cabeça tem 28 de largura com o cabelo e a barba (o crânio, uns 24); um homem grande
  tem a caixa torácica com uns 2,2 a 2,4 crânios de largura na frente: 58 a 62 px. As juntas dos ombros (x 138 e 206)
  ficam a 68 px: o tronco é mais estreito que elas, e os braços saem por fora dele;
- **a caixa torácica** (um ovo de topo mais estreito, inclinado para a frente: a câmera olha de cima, então o peito é
  o que mais se vê), mais larga na altura das costelas de baixo, sem cintura marcada (ele é robusto e está curvado
  para a tigela; a barriga continua o volume até o tampo);
- **o trapézio** desce do pescoço até os ombros por baixo das ombreiras; **a axila** é o ponto em que o contorno de
  dentro do braço encontra o lado do tronco (x 141 e 203, y ~50): abaixo dela, o fundo aparece entre o braço e o
  tronco, onde o braço se afasta (o cotovelo pousa para fora);
- **a roupa sobre esses volumes:** o casaco aberto acompanha o tronco (couro grosso, 1 px além dele); o colete fecha
  alto, até a garganta, e a barba passa por cima dele; a gola do casaco fica em pé atrás da barba, dos dois lados
  (o que a imagem gerada e o Gwent mostram), e as lapelas descem em diagonal até as bordas do colete; as tiras
  acompanham a curva do peito (visto de cima, a frente de um cilindro fica mais baixa: as pontas sobem 1 px).

O rascunho foi gravado como grade (`morel.TRONCO`) e retocado à mão lá; a grade é a autoridade."""
import sys

X0, Y0 = 128, 25          # o canto de cima à esquerda da grade
LARG, ALT = 90, 56        # x 128 a 217, y 25 a 80

# o contorno da barba por linha (x da esquerda e da direita), da cabeça na pose de repouso: o colete e a gola encostam nele
BARBA = {27: (160, 182), 28: (160, 182), 29: (161, 182), 30: (161, 181), 31: (162, 180), 32: (163, 179), 33: (164, 177),
         34: (166, 176), 35: (168, 174)}


def _lados(y):
    """O contorno do casaco, linha a linha (decidido à mão sobre a construção): o trapézio da gola até os ombros, os
    ombros por baixo das ombreiras, a axila, o lado da caixa torácica até o tampo."""
    # o trapézio desce da gola (côncavo), o ombro arredonda por cima do deltoide (convexo) e recolhe até a axila;
    # abaixo dela, o lado da caixa torácica, um pouco mais larga embaixo, até o tampo
    esq = {27: 153, 28: 150, 29: 147, 30: 144, 31: 141, 32: 139, 33: 137, 34: 136, 35: 135, 36: 134, 37: 133, 44: 133,
           45: 134, 46: 135, 47: 136, 48: 138, 49: 139, 50: 140, 51: 141, 55: 140, 65: 141}
    dir_ = {27: 189, 28: 192, 29: 195, 30: 198, 31: 201, 32: 203, 33: 205, 34: 206, 35: 207, 36: 208, 37: 209, 45: 208,
            46: 207, 47: 206, 48: 205, 49: 204, 51: 203, 65: 202}
    if y < 27:
        return None
    return esq[max(k for k in esq if k <= y)], dir_[max(k for k in dir_ if k <= y)]


def _gola(y):
    """As duas bandas da gola em pé e das lapelas: (x da banda esquerda, x da direita, largura). A gola fica atrás da
    barba no alto (y 26 a 33) e desce em diagonal até as bordas do colete (x 157 e 184) em y 41."""
    if y < 26:
        return None
    if y <= 33:
        return 153, 186, 5
    if y <= 41:
        t = (y - 33) / 8
        return round(153 + 3 * t), round(186 - 2 * t), round(5 - 2 * t)
    return 156, 184, 3


def grade():
    linhas = []
    for gy in range(ALT):
        y = Y0 + gy
        lin = ["."] * LARG
        lados = _lados(y)
        gola = _gola(y)
        if lados:
            e, d = lados
            for x in range(e, d + 1):
                # o casaco: o lado da vela (esquerda) aceso, a frente, o lado de lá à sombra
                if x <= e and y >= 47:
                    ch = "j"
                elif x < 158:
                    ch = "a"
                elif x < 196:
                    ch = "b"
                elif x < d - 1:
                    ch = "c"
                else:
                    ch = "l"
                if y <= 35 and (y == lados[0] or x in (e, e + 1)):
                    ch = "j" if x < 171 else "a"  # o alto do trapézio pega a luz
                lin[x - X0] = ch
        # o colete: das lapelas para dentro, até a barba (a barba passa por cima dele)
        if gola and y >= 27:
            ge, gd, gl = gola
            for x in range(ge + gl, gd):
                k = x - 171
                ch = "1" if -13 <= k <= -11 else "2" if k < 0 else "3" if k < 10 else "4"
                if k == 0:
                    ch = "4"   # a costura do meio
                lin[x - X0] = ch
            # as bandas da gola e das lapelas: a da esquerda acesa na borda de dentro, a da direita à sombra
            for i in range(gl):
                lin[ge + i - X0] = "j" if i == gl - 1 else "a" if i >= gl - 2 or y <= 27 else "b"
                lin[gd + i - X0] = "l" if i == 0 else "c" if y > 27 else "b"
            if y <= 27:   # o alto da gola em pé: a aresta
                for i in range(gl):
                    lin[ge + i - X0] = "j"
                    lin[gd + i - X0] = "b"
        linhas.append("".join(lin))
    return linhas


def guia(caminho):
    """A construção em formas simples (para a camada oculta da fonte e as folhas): o pescoço, as clavículas, as juntas
    dos ombros, a caixa torácica (o ovo), as axilas, o eixo do meio."""
    import math
    from PIL import Image
    im = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    px = im.load()

    def p(x, y, c):
        if 0 <= x < 320 and 0 <= y < 96:
            px[x, y] = c
    caixa, osso, junta, eixo = (90, 200, 255, 255), (255, 200, 60, 255), (255, 70, 70, 255), (160, 255, 160, 255)
    for a in range(360):   # a caixa torácica: o ovo, mais estreito em cima
        t = math.radians(a)
        rx = 31 if math.sin(t) > 0 else 27
        p(round(171.5 + rx * math.cos(t)), round(58 + 20 * math.sin(t)), caixa)
    for y in range(22, 40):   # o pescoço: um cilindro grosso atrás da barba
        p(162, y, caixa)
        p(181, y, caixa)
    for x0, y0, x1, y1 in ((171, 37, 140, 35), (171, 37, 204, 37)):   # as clavículas, da fúrcula aos ombros
        for i in range(41):
            t = i / 40
            p(round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t), osso)
    for x, y in ((138, 44), (206, 46), (141, 50), (203, 50)):  # as juntas dos ombros e as axilas
        for d in range(-2, 3):
            p(x + d, y, junta)
            p(x, y + d, junta)
    for y in range(26, 80):
        p(171, y, eixo)
    im.save(caminho)


if __name__ == "__main__":
    if "--grade" in sys.argv:
        for lin in grade():
            print(f'    "{lin}",')
    elif "--guia" in sys.argv:
        guia(sys.argv[-1])
