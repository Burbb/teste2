"""Histórico: o candidato de Poder de `35262ca`, não aprovado. O Poder do jogo (1.123.0) vem das fontes em camadas de
ferramentas/arte/aseprite/attr-poder/ (exportar_aseprite.py attr-poder); este script só grava numa pasta.

O ícone de Poder (`attr-poder`): proposta, nada no jogo. O atual é um placeholder pintado (a chama roxa com halo
suave); a proposta de 18/10/2026 (`desenhar_atributos_pixel.py`) foi recusada (lia como cristal ou gota rígida).

O objeto: uma chama violeta viva, a energia mágica. Três línguas que nascem de uma base redonda e ondulam (a do meio
a mais alta, curvando na ponta; a da esquerda abrindo para fora; a da direita curta), e duas faíscas soltas acima. A
luz é da própria chama, em camadas aninhadas, sem desfoque: cada camada é a silhueta da chama encolhida em direção à
base, então as línguas de dentro repetem as de fora:
  - a beira de 1 px roxo escuro, o corpo violeta, o interior lilás, o núcleo quase branco perto da base;
  - o lado de trás de cada camada (à direita) um tom abaixo, para a chama ter volume e não virar um adesivo.
Os papéis: a ficha e o Inventário (24) e o selo da festa de atributo permanente (64, o 32 ampliado 2×).

    python ferramentas/arte/desenhar_attr_poder_pixel.py <pasta> [--listas]
"""

import math
import sys

import numpy as np
from PIL import Image

import pixel_comum as pc

# a rampa com deslocamento de matiz: do índigo da beira ao violeta, ao magenta-lilás e ao núcleo branco rosado (a luz
# da energia sai do contraste entre as camadas, não de desfoque)
ROXO = ["#1A0A4A", "#2E1180", "#5A1FC8", "#8A3CEA", "#BC5CF2", "#EBA0FA", "#FFF2FC"]
RAMPAS = {"r": ROXO, "f": ROXO}

NOME = "attr-poder"
CAMADAS = ["chama", "nucleo", "faiscas", "contorno"]

# as medidas em unidades do 24
M = {
    "ancora": (11.8, 21.6),                     # para onde as camadas de dentro encolhem
    "base": (11.8, 17.2, 6.4, 4.6),             # a base redonda: centro, semieixos
    # as línguas: (x da base, y da base, y da ponta, largura, deslocamento da ponta, ondulação)
    "linguas": ((11.6, 15.0, 1.2, 4.6, 1.8, 0.9), (7.6, 16.0, 5.8, 3.0, -2.4, 0.6), (16.4, 16.4, 8.4, 2.6, 1.4, -0.5)),
    "camadas": ((1.0, 3), (0.78, 4), (0.58, 5), (0.36, 6)),   # (escala para a âncora, tom)
    "faiscas": ((18.6, 4.2), (5.2, 3.6)),
}


def _chama(X, Y):
    """A silhueta da chama nas coordenadas dadas (unidades do 24)."""
    bx, by, rx, ry = M["base"]
    forma = ((X - bx) / rx) ** 2 + ((Y - by) / ry) ** 2 <= 1
    for (x0, y0, yt, larg, desl, onda) in M["linguas"]:
        t = np.clip((y0 - Y) / (y0 - yt), 0, 1)               # 0 na base da língua, 1 na ponta
        centro = x0 + desl * t ** 1.6 + onda * np.sin(t * math.pi * 1.4)
        meia = larg * (1 - t) ** 0.85 * np.sqrt(np.clip(t * 6 + 0.2, 0, 1))
        forma |= (Y <= y0) & (Y >= yt) & (np.abs(X - centro) <= np.maximum(meia, 0.0))
    return forma


def desenhar(lado, partes=False):
    """A imagem do tamanho; com partes=True, também a camada de cada pixel (CAMADAS)."""
    s = lado / 24
    mat, tom, fixo, x, y = pc.grade(lado)
    X, Y = x / s, y / s
    ax, ay = M["ancora"]
    nucleo = np.zeros(X.shape, dtype=bool)
    for (k, t) in M["camadas"]:
        dentro = _chama(ax + (X - ax) / k, ay + (Y - ay) / k)
        mat[dentro] = "r" if t < 6 else "f"
        tom[dentro] = t
        if t >= 5:
            nucleo |= dentro
        # o lado de trás (à direita do centro da camada) um tom abaixo
        lado_tras = dentro & (X > ax + 1.4 * k)
        tom[lado_tras] = t - 1
    fixo[nucleo] = True
    # a beira de 1 px roxo escuro, por dentro do contorno
    forma = mat != ""
    viz = np.zeros_like(forma)
    for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        viz |= ~np.roll(np.roll(forma, oy, 0), ox, 1)
    beira = forma & viz
    tom[beira] = np.where(X[beira] < ax, 2, 1)
    fixo[beira] = True
    # as faíscas: um ponto claro com a beira (no 24, só a de cima à direita)
    for i, (fx, fy) in enumerate(M["faiscas"]):
        if lado < 32 and i > 0:
            continue
        xx, yy = int(fx * s), int(fy * s)
        mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "f", 5, True
        if lado >= 32:
            mat[yy + 1, xx], tom[yy + 1, xx], fixo[yy + 1, xx] = "f", 3, True

    tom = pc.limpar(mat, tom, fixo)
    pc.contornar(mat)
    img = pc.imagem(mat, tom, RAMPAS)
    if not partes:
        return img
    camada = np.full(mat.shape, "", dtype=object)
    camada[mat == "r"] = "chama"
    camada[(mat == "f") | ((mat == "r") & nucleo)] = "nucleo"
    for i, (fx, fy) in enumerate(M["faiscas"]):
        xx, yy = int(fx * s), int(fy * s)
        for dy in (0, 1):
            if 0 <= yy + dy < lado and mat[yy + dy, xx] == "f" and not nucleo[yy + dy, xx]:
                camada[yy + dy, xx] = "faiscas"
    camada[mat == "c"] = "contorno"
    return img, camada


def main():
    pasta = pc.destino(sys.argv)
    if pasta == pc.ICONES:
        sys.exit("Proposta: passe uma pasta (o jogo só recebe o desenho aprovado).")
    print(24, pc.salvar(desenhar(24), pasta, NOME), "cores")
    img32 = desenhar(32)
    print(32, pc.salvar(img32, pasta, NOME), "cores")
    print(64, pc.salvar(img32.resize((64, 64), Image.NEAREST), pasta, NOME), "cores (o 32 ampliado 2×)")
    if "--listas" in sys.argv:
        for lado in (24, 32):
            print("listas", pc.listas_camadas(desenhar(lado, partes=True), pasta / "listas" / f"{NOME}-{lado}", CAMADAS))


if __name__ == "__main__":
    main()
