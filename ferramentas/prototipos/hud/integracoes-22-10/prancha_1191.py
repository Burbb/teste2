"""A folha compacta da integração do Golem Primordial (integracoes-1191.png), só com as capturas do jogo com os arquivos de
produção, a 1920×945, em tamanho real (criaturas/chefes_arvore_golem/capturas-1191): o guardião na luta com o golem de
pedra e o esqueleto, e o Mímico pelo código real do evento (no sprite de antes); embaixo, o arquivo a 1× e a 3× (o
guardião só aparece na carta: o 16 e o 32).
    python prancha_1191.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/chefes_arvore_golem/capturas-1191"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
# (título, foto, recorte, ao lado da anterior)
FOTOS = [
    ("1.191.0 — a carta (32): o Golem Primordial (pelo id do guardião) com o Golem de pedra e o Esqueleto",
     "luta-primordial.png", (1225, 88, 1438, 260), False),
    ("o Mímico, pelo evento real, continua no sprite do construto", "mimico.png", (1226, 148, 1438, 202), False),
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
    for k, nome in enumerate(("retrato-golem-primordial",)):
        ic = Image.open(ICONES / f"{nome}-16.png").convert("RGBA")
        out.alpha_composite(ic, (16 + k * 90, y + 30))
        out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40 + k * 90, y + 20))
    out = out.crop((0, 0, out.width, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1191.png")
    print("integracoes-1191.png", out.size)


if __name__ == "__main__":
    main()
