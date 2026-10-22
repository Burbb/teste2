"""A folha compacta da integração do Caído (integracoes-1182.png), só com as capturas do jogo com os arquivos de
produção, a 1920×945, em tamanho real (criaturas/caidos/capturas-1182): o bando (três caídos com o retrato novo; o
xamã e o cão infernal no sprite de demônio de sempre), o Bestiário e o contrato de caça (o cartaz e o rastreador);
embaixo, o arquivo a 1× e a 3×.
    python prancha_1182.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/caidos/capturas-1182"
ICONE = HUD.parents[2] / "rpg/web/static/hud/icones/retrato-caido-16.png"
FOTOS = [
    ("1.182.0 — o bando na carta (32): três caídos com o retrato do CA; o Xamã caído e o Cão infernal no demônio de "
     "sempre", "luta.png", (1005, 88, 1440, 262)),
    ("o Bestiário (48)", "bestiario.png", (585, 245, 1295, 600)),
    ("o contrato de caça: o cartaz do mural (48) e o rastreador (32)", "contratos.png", (580, 640, 830, 800)),
    ("", "contratos-rastreador.png", None),
]


def main():
    f = ImageFont.truetype("arial.ttf", 14)
    ims = [(t, Image.open(CAP / a).convert("RGBA").crop(c) if c else Image.open(CAP / a).convert("RGBA")) for t, a, c in FOTOS]
    w = max(im.width for _, im in ims) + 400
    h = sum(im.height + 30 for _, im in ims) + 90
    out = Image.new("RGBA", (w, h), (13, 11, 10, 255))
    d = ImageDraw.Draw(out)
    y = 12
    for n, (t, im) in enumerate(ims):
        x = 16
        if n == 3:  # o rastreador ao lado do cartaz
            y -= ims[2][1].height + 8
            x = 16 + ims[2][1].width + 24
        if t:
            d.text((16, y), t, fill=(210, 210, 214, 255), font=f)
            y += 20
        out.alpha_composite(im, (x, y))
        y += im.height + 8
    d.text((16, y), "o arquivo a 1× e a 3× (o retrato 16; o 32 e o 48 são ×2 e ×3)", fill=(210, 210, 214, 255), font=f)
    ic = Image.open(ICONE).convert("RGBA")
    out.alpha_composite(ic, (16, y + 30))
    out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40, y + 20))
    out = out.crop((0, 0, w, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1182.png")
    print("integracoes-1182.png", out.size)


if __name__ == "__main__":
    main()
