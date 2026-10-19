# O código de conferência de uma imagem (o mesmo que soma.lua calcula no editor sobre o composto das camadas): para
# comparar o composto do Aseprite com o PNG exportado e com a prévia, sem trazer a imagem.
# Uso: python soma.py <png> [<png>...]
import sys
from PIL import Image
def soma(caminho):
    im = Image.open(caminho).convert("RGBA"); h = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            if a == 0: r = g = b = 0
            h = (h * 31 + ((r * 256 + g) * 256 + b) * 2 + (1 if a > 0 else 0)) % 2147483647
    return h
if __name__ == "__main__":
    for c in sys.argv[1:]: print(c, soma(c))
