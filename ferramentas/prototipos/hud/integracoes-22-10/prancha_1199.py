"""A folha compacta da integração do Lich Menor (integracoes-1199.png), só com as capturas do jogo com os arquivos de
produção, a 1920×945, em tamanho real (criaturas/lich_32/capturas-1199): as duas fases da mesma luta (na segunda, o Lich
etéreo com o mesmo retrato), cada uma com o servo aliado e, do lado inimigo, o Lich, o Esqueleto e os esqueletos que ele
invoca (o retrato da família); embaixo, o arquivo a 1× e a 3× (o Lich só aparece na carta: o 16 e o 32).
    python prancha_1199.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/lich_32/capturas-1199"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
# (título, foto, recorte, ao lado da anterior)
FOTOS = [
    ("1.199.0 — fase 1: o servo aliado | o Lich Menor (pelo id do guardião), o Esqueleto e o esqueleto que ele invoca",
     "luta-lich-fase1.png", (440, 167, 658, 257), False),
    ("", "luta-lich-fase1.png", (1222, 88, 1440, 262), True),
    ("fase 2 (o Lich etéreo, pelo Combate.checar_fase): o mesmo retrato; os invocados com o da família",
     "luta-lich-fase2.png", (440, 167, 658, 257), False),
    ("", "luta-lich-fase2.png", (1004, 88, 1440, 262), True),
]


def main():
    f = ImageFont.truetype("arial.ttf", 14)
    out = Image.new("RGBA", (1500, 1400), (13, 11, 10, 255))
    d = ImageDraw.Draw(out)
    y, x, alto = 12, 16, 0
    for t, arq, corte, lado in FOTOS:
        im = Image.open(CAP / arq).convert("RGBA")
        im = im.crop(corte) if corte else im
        if lado:
            x += 24
        else:
            y += alto + (8 if alto else 0)
            x, alto = 16, 0
            if t:
                d.text((16, y), t, fill=(210, 210, 214, 255), font=f)
                y += 20
        out.alpha_composite(im, (x, y))
        x += im.width
        alto = max(alto, im.height)
    y += alto + 10
    d.text((16, y), "os arquivos a 1× e a 3× (o retrato 16; o 32 é ×2): o Lich Menor",
           fill=(210, 210, 214, 255), font=f)
    for k, nome in enumerate(("retrato-lich-menor",)):
        ic = Image.open(ICONES / f"{nome}-16.png").convert("RGBA")
        out.alpha_composite(ic, (16 + k * 90, y + 30))
        out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40 + k * 90, y + 20))
    out = out.crop((0, 0, out.width, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1199.png")
    print("integracoes-1199.png", out.size)


if __name__ == "__main__":
    main()
