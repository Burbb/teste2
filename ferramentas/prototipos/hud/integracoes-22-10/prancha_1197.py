"""A folha compacta da integração da Hidra do Brejo (integracoes-1197.png), só com a captura do jogo com os arquivos de
produção, a 1920×945, em tamanho real (criaturas/hidra_32/capturas-1197): a guardiã na luta com o sapo e a sanguessuga;
embaixo, o arquivo a 1× e a 3× (a guardiã só aparece na carta: o 16 e o 32).
    python prancha_1197.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/hidra_32/capturas-1197"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
# (título, foto, recorte, ao lado da anterior)
FOTOS = [
    ("1.197.0 — a carta (32): a Hidra do Brejo (pelo id da guardiã) com o Sapo-touro e a Sanguessuga", "luta-hidra.png",
     (1220, 86, 1442, 264), False),
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
    d.text((16, y), "o arquivo a 1× e a 3× (o retrato 16; o 32 é ×2)",
           fill=(210, 210, 214, 255), font=f)
    for k, nome in enumerate(("retrato-hidra-do-brejo",)):
        ic = Image.open(ICONES / f"{nome}-16.png").convert("RGBA")
        out.alpha_composite(ic, (16 + k * 90, y + 30))
        out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40 + k * 90, y + 20))
    out = out.crop((0, 0, out.width, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1197.png")
    print("integracoes-1197.png", out.size)


if __name__ == "__main__":
    main()
