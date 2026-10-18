"""O recorte da pintura horizontal de Jean ("../topo.png", 2172×724) para a barra do topo (em avaliação, nada no jogo).

A barra não cresce (46 px). A pintura entra em escala uniforme, com a largura dela ocupando a tela (1920 px:
×0,896), e só a faixa de baixo é usada:
  - dentro da barra, o carvão sólido e o começo do rasgo (as linhas 419 a 470 da pintura, 46 px na tela);
  - abaixo da barra, só as pontas do rasgo (470 a 495, ~22 px na tela), apagando nas últimas linhas, para o desgaste
    ligar o topo às colunas sem cobrir o que está embaixo.
Nada é esticado: o recorte tira as margens transparentes (x 15 a 2158) e as linhas de cima, que não cabem na barra.

  python ferramentas/prototipos/hud/direcao/topo/derivar_topo.py
"""

import os

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, "..", "topo.png")
X0, X1 = 15, 2159          # sem as margens transparentes
Y0, Y_BARRA, Y1 = 419, 470, 495   # o topo da faixa, onde a barra acaba, o fim das pontas
APAGA = 12                 # as últimas linhas das pontas somem aos poucos (sem um corte reto)


def main():
    os.makedirs(os.path.join(AQUI, "pecas"), exist_ok=True)
    faixa = np.asarray(Image.open(FONTE).convert("RGBA").crop((X0, Y0, X1, Y1))).copy()
    alt = faixa.shape[0]
    fator = np.ones(alt)
    fator[alt - APAGA:] = np.linspace(1, 0, APAGA)
    faixa[..., 3] = (faixa[..., 3] * fator[:, None]).astype(np.uint8)
    # As manchas claras das pontas: dentro da barra elas ficam atrás do logotipo (à esquerda) e de "Fonte" e "Som" (à
    # direita) e disputam com o texto. Só ali (as pontas, na altura da barra) o claro escurece até o tom do carvão,
    # com transição suave; abaixo da barra as pontas do rasgo continuam bege (a ligação com as colunas), a da esquerda
    # pela metade, para não somar com a mancha do canto de cima da ficha.
    rgb = faixa[..., :3].astype(float)
    lum = rgb.mean(2)
    larg = faixa.shape[1]
    xs = np.arange(larg)[None, :]
    ys = np.arange(alt)[:, None]
    ponta = np.clip(1 - (xs - 120) / 260, 0, 1) + np.clip((xs - (larg - 380)) / 260, 0, 1)   # 1 nas pontas, 0 no meio
    barra = np.clip((Y_BARRA - Y0 + 4 - ys) / 8, 0, 1)                                      # 1 na barra, 0 abaixo
    esquerda = (xs < larg / 2) * np.clip((ys - (Y_BARRA - Y0)) / 6, 0, 1) * 0.5              # as pontas da esquerda
    claro = np.clip((lum - 45) / 60, 0, 1)                                                  # só o que é claro
    forca = np.clip(ponta * np.maximum(barra, esquerda), 0, 1) * claro
    alvo = np.array([22.0, 21.0, 22.0])
    rgb = rgb * (1 - forca[..., None]) + alvo * forca[..., None]
    faixa[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    Image.fromarray(faixa, "RGBA").save(os.path.join(AQUI, "pecas", "topo-faixa.png"), optimize=True)
    print("faixa", faixa.shape[1], "×", alt, "· a barra até a linha", Y_BARRA - Y0, f"(proporção {faixa.shape[1]}/{alt})")


if __name__ == "__main__":
    main()
