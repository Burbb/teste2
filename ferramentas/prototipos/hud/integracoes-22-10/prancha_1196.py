"""A folha compacta da integração do servo esquelético (integracoes-1196.png), só com a captura do jogo com os arquivos de
produção, a 1920×945, em tamanho real (criaturas/servo_32/capturas-1196): na mesma luta, a coluna aliada (o herói, o
"Esqueleto (Invocado)" do Erguer Servo com o crânio nu e o lobo erguido pelo Rei dos Mortos com o retrato do lobo) e a
inimiga (o esqueleto, com o dele); embaixo, os arquivos a 1× e a 3× (o servo só aparece na carta: o 16 e o 32).
    python prancha_1196.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/servo_32/capturas-1196"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
# (título, foto, recorte, ao lado da anterior)
FOTOS = [
    ("1.196.0 — a mesma luta: os aliados (o Esqueleto invocado com o crânio nu, o lobo erguido com o do lobo) e o esqueleto "
     "inimigo", "luta-servos.png", (428, 78, 670, 302), False),
    ("", "luta-servos.png", (1222, 133, 1440, 249), True),
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
    d.text((16, y), "os arquivos a 1× e a 3× (o retrato 16; o 32 é ×2): o servo do Erguer Servo, o lobo e o esqueleto inimigo",
           fill=(210, 210, 214, 255), font=f)
    for k, nome in enumerate(("retrato-servo-esqueletico", "retrato-lobo", "retrato-esqueleto")):
        ic = Image.open(ICONES / f"{nome}-16.png").convert("RGBA")
        out.alpha_composite(ic, (16 + k * 90, y + 30))
        out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40 + k * 90, y + 20))
    out = out.crop((0, 0, out.width, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1196.png")
    print("integracoes-1196.png", out.size)


if __name__ == "__main__":
    main()
