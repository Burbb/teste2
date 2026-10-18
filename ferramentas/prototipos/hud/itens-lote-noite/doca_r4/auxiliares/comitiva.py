# a Comitiva (36): três viajantes, um à frente e dois um pouco atrás; cada figura com o próprio contorno, desenhada de
# trás para a frente (o contorno da da frente separa as de trás). As figuras por formas simples nas unidades do 36.
import sys, json
from ver import contorno, imagem
n = int(sys.argv[1]); k = n / 36
def figura(cx, topo, esc, partes):
    """Uma figura: partes é uma lista de (forma, função de tom); devolve {(x, y): letra}."""
    g = {}
    for y in range(n):
        for x in range(n):
            px, py = (x + 0.5 - cx) / (k * esc), (y + 0.5 - topo) / (k * esc)
            for forma, tom in partes:
                if forma(px, py): g[(x, y)] = tom(px, py)
    return g
def elipse(cx, cy, rx, ry): return lambda px, py: ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1
def manto(y0, y1, w0, w1):    # um trapézio: meia-largura w0 em cima, w1 embaixo (a barra reta)
    return lambda px, py: y0 <= py <= y1 and abs(px) <= w0 + (w1 - w0) * (py - y0) / (y1 - y0)
def luz(claro, meio, escuro, eixo=0.0):   # a luz da esquerda: claro, meio e o lado de trás escuro
    return lambda px, py: claro if px < eixo - 1.5 else meio if px < eixo + 1.8 else escuro
def ombros(y0, y1, w0, w1, r):   # o corpo com ombros arredondados (o canto de cima cortado em arco de raio r)
    def f(px, py):
        if not (y0 <= py <= y1): return False
        w = w0 + (w1 - w0) * (py - y0) / (y1 - y0)
        if abs(px) > w: return False
        if py < y0 + r and abs(px) > w - r:
            return ((abs(px) - (w - r)) / r) ** 2 + ((py - (y0 + r)) / r) ** 2 <= 1
        return True
    return f
# 1. o de trás à esquerda: chapéu de copa alta e aba larga, o casaco de couro
esq = figura(9.6, 3.4, 0.88, [
    (ombros(9.0, 22.0, 5.4, 6.6, 2.0), luz("i", "h", "g")),                  # o casaco
    (elipse(0, 6.6, 2.9, 3.0), lambda px, py: "c" if px < 0.5 else "b"),     # o rosto
    (lambda px, py: abs(py - 4.0) <= 0.75 and abs(px) <= 5.4, lambda px, py: "h" if px < 0 else "g"),   # a aba
    (lambda px, py: 0.6 <= py <= 3.6 and abs(px) <= 2.9 - (3.6 - py) * 0.25, lambda px, py: "i" if px < -0.5 else "g"),   # a copa
    (lambda px, py: abs(py - 6.9) < 0.5 and (abs(px + 1.1) < 0.5 or abs(px - 1.1) < 0.5), lambda px, py: "e"),   # os olhos
])
# 2. o de trás à direita: ombreiras de metal e uma capa vermelho-escura
dir_ = figura(26.4, 3.4, 0.88, [
    (ombros(9.0, 22.0, 5.6, 6.8, 2.0), luz("s", "r", "q")),                  # a capa
    (elipse(0, 5.6, 2.9, 3.1), lambda px, py: "c" if px < 0.5 else "b"),     # o rosto
    (lambda px, py: ((px / 3.2) ** 2 + ((py - 3.8) / 2.6) ** 2 <= 1) and py <= 4.4, lambda px, py: "n" if px < 0 else "m"),   # o cabelo
    (elipse(-4.0, 9.8, 2.6, 1.8), lambda px, py: "p" if py < 9.4 and px < -4 else "o"),   # a ombreira da esquerda
    (elipse(4.0, 9.8, 2.6, 1.8), lambda px, py: "o" if py < 9.4 else "n"),               # a da direita
    (lambda px, py: abs(py - 6.0) < 0.5 and (abs(px + 1.1) < 0.5 or abs(px - 1.1) < 0.5), lambda px, py: "e"),   # os olhos
])
# 3. o da frente: capuz emoldurando o rosto, manto verde com ombros, o cajado na mão
fre = figura(18.0, 8.6, 1.0, [
    (ombros(9.6, 26.0, 6.2, 8.4, 2.6), luz("4", "3", "2")),                  # o manto
    (lambda px, py: abs(px - 0.4) < 0.6 and 13.0 <= py <= 26.0, lambda px, py: "2"),   # a abertura do manto
    (elipse(0, 5.0, 4.8, 5.0), lambda px, py: "5" if px < -1.6 else "4" if px < 1.8 else "3"),   # o capuz
    (elipse(0.3, 6.2, 2.7, 2.9), lambda px, py: "d" if px < -0.6 else "c" if px < 1.2 else "b"),   # o rosto
    (lambda px, py: abs(py - 3.9) < 0.6 and abs(px - 0.3) < 2.4, lambda px, py: "a"),   # a sombra do capuz na testa
    (lambda px, py: abs(py - 5.9) < 0.5 and (abs(px + 0.8) < 0.5 or abs(px - 1.4) < 0.5), lambda px, py: "e"),   # os olhos
    (elipse(-2.2, 10.8, 1.0, 1.0), lambda px, py: "z" if px < -2.2 else "y"),   # o broche de latão
])
camadas = {}
h = {}
for nome, g in (("tras_esquerda", esq), ("tras_direita", dir_), ("frente", fre)):
    c = contorno(g, n)
    for p, v in c.items():
        h[p] = v; camadas[p] = nome if v != "O" else "contorno"
imagem(h, n, f"c{n}.png")
json.dump({f"{x},{y}": c for (x, y), c in camadas.items()}, open(f"c{n}.cam.json", "w"))
