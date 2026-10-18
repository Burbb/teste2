"""As peças derivadas da pintura aprovada ("../Painel vertical em tinta escura.png", de Jean) para o estudo do conjunto
da HUD (em avaliação, nada no jogo). Nenhuma pincelada é esticada nem alargada: só espelhar, recortar, reduzir na
mesma proporção e emendar por espelho.

  python ferramentas/prototipos/hud/direcao/conjunto/derivar_pecas.py

  pecas/pintura-espelhada.png  a pintura inteira espelhada na horizontal: a coluna do mundo (periferia direita), com o
                               desgaste do lado de fora, como a ficha à esquerda
  pecas/carvao.png             um ladrilho do miolo da pintura (a tinta preta com as passadas diagonais), reduzido a
                               0,5 como a ficha e emendado por espelho (2×2), para repetir sem costura: a superfície
                               calma do centro, do topo, da doca e do seletor
  pecas/borda-mascara.png      o alfa da pintura inteira reduzido a 0,25 (o rasgo, os respingos): a máscara de nove
                               partes do mapa (cantos e lados vêm do próprio rasgo, só repetidos ao longo do lado)
"""

import os

import numpy as np
from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, "..", "Painel vertical em tinta escura.png")
PECAS = os.path.join(AQUI, "pecas")


def main():
    os.makedirs(PECAS, exist_ok=True)
    pintura = Image.open(FONTE).convert("RGBA")
    ImageOps.mirror(pintura).save(os.path.join(PECAS, "pintura-espelhada.png"), optimize=True)

    # o miolo: uma área sem respingo nem papel (a área escura sólida vai de x 86 a 723 e de y 127 a 1847)
    miolo = pintura.crop((180, 420, 620, 1300)).convert("RGB")
    miolo = miolo.resize((miolo.width // 2, miolo.height // 2), Image.LANCZOS)          # 0,5, como a ficha
    w, h = miolo.size
    ladrilho = Image.new("RGB", (2 * w, 2 * h))
    ladrilho.paste(miolo, (0, 0))
    ladrilho.paste(ImageOps.mirror(miolo), (w, 0))
    ladrilho.paste(ImageOps.flip(miolo), (0, h))
    ladrilho.paste(ImageOps.flip(ImageOps.mirror(miolo)), (w, h))
    ladrilho.save(os.path.join(PECAS, "carvao.png"), optimize=True)

    alfa = pintura.getchannel("A")
    alfa = alfa.resize((alfa.width // 4, alfa.height // 4), Image.LANCZOS)
    mascara = Image.new("RGBA", alfa.size, (255, 255, 255, 0))
    mascara.putalpha(alfa)
    mascara.save(os.path.join(PECAS, "borda-mascara.png"), optimize=True)

    a = np.asarray(ladrilho, float).mean(2)
    print("ladrilho", ladrilho.size, "luminância média", round(a.mean(), 1), "máx", round(a.max(), 1))
    print("máscara", mascara.size)


if __name__ == "__main__":
    main()
