"""A folha compacta da integração da Harpia e do Xamã Caído (integracoes-1184.png), só com as capturas do jogo com os
arquivos de produção, a 1920×945, em tamanho real (criaturas/rodada_23_10/capturas-1184): a harpia junto do grifo e o
xamã junto dos caídos (o cão infernal no sprite de demônio de sempre), o Bestiário e os contratos de caça (os cartazes e
o rastreador); embaixo, os arquivos a 1× e a 3×.
    python prancha_1184.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/rodada_23_10/capturas-1184"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
# (título, foto, recorte, ao lado da anterior)
FOTOS = [
    ("1.184.0 — a carta (32): a Harpia junto do Grifo | o Xamã caído junto dos Caídos (o Cão infernal no demônio)",
     "luta-harpia.png", (1225, 92, 1437, 258), False),
    ("", "luta-xama.png", (1008, 92, 1437, 258), True),
    ("o Bestiário (48)", "bestiario.png", (585, 248, 1295, 760), False),
    ("os contratos de caça: os cartazes do mural (48) e o rastreador (32)", "contratos.png", (583, 660, 1055, 850), False),
    ("", "contratos-rastreador.png", None, True),
]


def main():
    f = ImageFont.truetype("arial.ttf", 14)
    out = Image.new("RGBA", (1200, 1400), (13, 11, 10, 255))
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
    d.text((16, y), "os arquivos a 1× e a 3× (o retrato 16; o 32 e o 48 são ×2 e ×3): a Harpia, o Xamã caído",
           fill=(210, 210, 214, 255), font=f)
    for k, nome in enumerate(("retrato-harpia", "retrato-xama-caido")):
        ic = Image.open(ICONES / f"{nome}-16.png").convert("RGBA")
        out.alpha_composite(ic, (16 + k * 90, y + 30))
        out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40 + k * 90, y + 20))
    out = out.crop((0, 0, out.width, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1184.png")
    print("integracoes-1184.png", out.size)


if __name__ == "__main__":
    main()
