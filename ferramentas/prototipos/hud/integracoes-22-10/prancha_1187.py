"""A folha compacta da integração do Cavaleiro Sombrio (integracoes-1187.png), só com as capturas do jogo com os arquivos
de produção, a 1920×945, em tamanho real (criaturas/cidadela/capturas-1187): o cavaleiro na luta com o esqueleto e o
mercenário, o Último Guarda (o cavaleiro de nome próprio), o Bestiário (com a faixa do mestre caçador) e o contrato de
caça (o cartaz e o rastreador); embaixo, o arquivo a 1× e a 3×.
    python prancha_1187.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/cidadela/capturas-1187"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
# (título, foto, recorte, ao lado da anterior)
FOTOS = [
    ("1.187.0 — a carta (32): o Cavaleiro sombrio com o Esqueleto e o Mercenário; ao lado, o Último Guarda",
     "luta-cavaleiro.png", (1225, 88, 1438, 260), False),
    ("", "luta-guarda.png", (1225, 145, 1438, 205), True),
    ("o Bestiário (48), com a faixa do mestre caçador no Cavaleiro sombrio", "bestiario.png", (585, 245, 1298, 516), False),
    ("o contrato de caça: o cartaz do mural (48) e o rastreador (32)", "contratos.png", (582, 660, 812, 850), False),
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
    d.text((16, y), "o arquivo a 1× e a 3× (o retrato 16; o 32 e o 48 são ×2 e ×3)",
           fill=(210, 210, 214, 255), font=f)
    for k, nome in enumerate(("retrato-cavaleiro-sombrio",)):
        ic = Image.open(ICONES / f"{nome}-16.png").convert("RGBA")
        out.alpha_composite(ic, (16 + k * 90, y + 30))
        out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40 + k * 90, y + 20))
    out = out.crop((0, 0, out.width, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1187.png")
    print("integracoes-1187.png", out.size)


if __name__ == "__main__":
    main()
