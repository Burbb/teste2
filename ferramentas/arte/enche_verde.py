"""O preenchimento verde das barras de Foco (rpg/web/static/hud/enche-verde.png): o azul da Mana com o tom e a
saturação levados ao verde do Foco do jogo (#62b86e, o meio da barra de antes da HUD de ferro), sem mexer na luz nem
no pontilhado, para ficar da mesma família das outras (vermelha, laranja, azul, roxa).

    python ferramentas/arte/enche_verde.py [saida.png]   # sem a saída, grava no jogo
"""
import colorsys
import pathlib
import sys

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[2]
HUD = RAIZ / "rpg" / "web" / "static" / "hud"


def hsv(cor):
    return colorsys.rgb_to_hsv(*(int(cor[i:i + 2], 16) / 255 for i in (1, 3, 5)))


def main():
    azul = Image.open(HUD / "enche-azul.png").convert("RGBA")
    (h_az, s_az, _), (h_vd, s_vd, _) = hsv("#4d74e0"), hsv("#62b86e")  # o meio da Mana e o do Foco
    verde = Image.new("RGBA", azul.size)
    for y in range(azul.height):
        for x in range(azul.width):
            r, g, b, a = azul.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            rr, gg, bb = colorsys.hsv_to_rgb((h + h_vd - h_az) % 1, min(1, s * s_vd / s_az), v)
            verde.putpixel((x, y), (round(rr * 255), round(gg * 255), round(bb * 255), a))
    saida = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HUD / "enche-verde.png"
    verde.save(saida)
    print(saida)


if __name__ == "__main__":
    main()
