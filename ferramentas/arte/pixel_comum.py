"""As etapas comuns do método de pixel art dos objetos da HUD, usadas pelo escudo (desenhar_escudo_pixel.py) e pelo
unguento (desenhar_unguento_pixel.py). Só o que já se repetiu nos dois objetos: o resto (a forma, os materiais, a luz
de cada parte) é de cada desenho.

O desenho de um objeto é uma grade de lado x lado com duas camadas: `mat` (o material de cada pixel, uma letra; ""
é vazio, "c" é o contorno) e `tom` (o índice do tom na rampa daquele material); `fixo` marca o que foi desenhado de
propósito (um brilho, um cravo) e que a limpeza não pode mexer.
"""

import math
import pathlib

import numpy as np
from PIL import Image

# A direção da luz, a mesma para todos os objetos: de cima e da esquerda, um pouco de frente.
LUZ = np.array([-0.58, -0.62, 0.53]); LUZ = LUZ / np.linalg.norm(LUZ)
ANG_LUZ = math.atan2(LUZ[1], LUZ[0])
# O contorno: quase preto, igual para todos.
CONTORNO = "#08080a"


def grade(lado):
    """As camadas vazias e as coordenadas dos centros dos pixels."""
    y, x = np.mgrid[0:lado, 0:lado] + 0.5
    return (np.full((lado, lado), "", dtype=object), np.zeros((lado, lado), dtype=int),
            np.zeros((lado, lado), dtype=bool), x, y)


def limpar(mat, tom, fixo, voltas=2):
    """Um pixel sozinho num tom, cercado (nos quatro lados) pelo mesmo material com outro tom, vira o tom mais comum
    em volta. O que está em `fixo` fica."""
    lado = mat.shape[0]
    for _ in range(voltas):
        novo = tom.copy()
        for yy in range(1, lado - 1):
            for xx in range(1, lado - 1):
                if not mat[yy, xx] or fixo[yy, xx]:
                    continue
                viz = [(yy - 1, xx), (yy + 1, xx), (yy, xx - 1), (yy, xx + 1)]
                if all(mat[a, b] == mat[yy, xx] and tom[a, b] != tom[yy, xx] for a, b in viz):
                    tons = [tom[a, b] for a, b in viz]
                    novo[yy, xx] = max(set(tons), key=tons.count)
        tom = novo
    return tom


def contornar(mat):
    """O contorno: 1 pixel em volta da silhueta, só pelos lados (sem engrossar nas diagonais)."""
    forma = mat != ""
    viz = np.zeros_like(forma)
    for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        viz |= np.roll(np.roll(forma, oy, 0), ox, 1)
    mat[viz & ~forma] = "c"


def ajustar(mat, tom, ajustes):
    """As correções feitas olhando o tamanho: {(x, y): (material ou None, tom)}."""
    for (xx, yy), (m_, t_) in ajustes.items():
        mat[yy, xx] = "" if m_ is None else m_
        tom[yy, xx] = t_ or 0


def imagem(mat, tom, rampas):
    """A imagem RGBA: cada material pela sua rampa ({"f": [...], "l": [...]}), o contorno pela cor comum."""
    lado = mat.shape[0]
    img = np.zeros((lado, lado, 4), dtype=np.uint8)
    cor = lambda h: [int(h[i:i + 2], 16) for i in (1, 3, 5)] + [255]
    for yy in range(lado):
        for xx in range(lado):
            m_ = mat[yy, xx]
            if m_ == "c":
                img[yy, xx] = cor(CONTORNO)
            elif m_:
                img[yy, xx] = cor(rampas[m_][tom[yy, xx]])
    return Image.fromarray(img, "RGBA")


# Onde os ícones do jogo moram (a família de ferro da HUD, hud/icones/): os desenhos são gravados aqui, prontos.
ICONES = pathlib.Path(__file__).resolve().parents[2] / "rpg" / "web" / "static" / "hud" / "icones"


def destino(argv):
    """A pasta de saída: a dos ícones do jogo, ou a pasta dada na linha de comando (para experimentar sem tocar no
    jogo)."""
    return pathlib.Path(argv[1]).resolve() if len(argv) > 1 else ICONES


def listas_camadas(img_camada, pasta, camadas):
    """As listas de pixels de cada camada ("x,y,RRGGBB;..."), cada uma num .lua que faz return: o que o pintar.lua
    (aseprite/) pinta por dofile para montar a fonte em camadas (montar_fontes.py). img_camada: (a imagem, a camada de
    cada pixel). Devolve a pasta."""
    img, camada = img_camada
    px = np.asarray(img)
    pasta.mkdir(parents=True, exist_ok=True)
    for c in camadas:
        ys, xs = np.where(camada == c)
        texto = ";".join(f"{x},{y},{px[y, x, 0]:02X}{px[y, x, 1]:02X}{px[y, x, 2]:02X}" for y, x in zip(ys, xs))
        (pasta / f"{c}.lua").write_text(f'return "{texto}"\n', encoding="utf-8")
    (pasta / "ordem.txt").write_text(",".join(camadas) + "\n", encoding="utf-8")   # de baixo para cima
    return pasta


def salvar(img, pasta, nome):
    """O arquivo e o dobro (a duplicação exata dos pixels, sem detalhe novo); devolve quantas cores o desenho usa."""
    pasta.mkdir(parents=True, exist_ok=True)
    lado = img.size[0]
    img.save(pasta / f"{nome}-{lado}.png")
    img.resize((2 * lado, 2 * lado), Image.NEAREST).save(pasta / f"{nome}-{lado}@2x.png")
    return len({tuple(p) for p in np.asarray(img).reshape(-1, 4) if p[3]})
