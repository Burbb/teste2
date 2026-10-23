"""A folha compacta da integração da Árvore Desperta e do golem de pedra (integracoes-1189.png), só com as capturas do
jogo com os arquivos de produção, a 1920×945, em tamanho real (criaturas/arvore_golem/capturas-1189): os dois na luta com
o lobo e o javali, o Bestiário (com a faixa do mestre caçador nos dois), os contratos de caça (o cartaz e o rastreador) e
as exceções pelo código real dos eventos (o Espantalho Possuído e o Mímico, que continuam nos traços); embaixo, os
arquivos a 1× e a 3×.
    python prancha_1189.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/arvore_golem/capturas-1189"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
# (título, foto, recorte, ao lado da anterior)
FOTOS = [
    ("1.189.0 — a carta (32): a Árvore desperta e o Golem de pedra com o Lobo e o Javali", "luta-arvore.png",
     (1008, 118, 1438, 232), False),
    ("o Bestiário (48), com a faixa do mestre caçador: o Golem e a Árvore", "bestiario.png", (945, 248, 1296, 514), False),
    ("", "bestiario.png", (945, 690, 1296, 848), True),
    ("os contratos de caça: o cartaz do mural (48) e o rastreador (32), da Árvore e do Golem", "contratos-arvore.png",
     (582, 660, 812, 850), False),
    ("", "contratos-arvore-rastreador.png", (0, 30, 330, 140), True),
    ("", "contratos-golem.png", (582, 660, 812, 850), True),
    ("", "contratos-golem-rastreador.png", (0, 30, 330, 140), True),
    ("as exceções, pelos eventos reais: o Espantalho Possuído e o Mímico continuam nos sprites (planta, construto)",
     "espantalho.png", (1226, 148, 1438, 202), False),
    ("", "mimico.png", (1226, 148, 1438, 202), True),
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
    d.text((16, y), "o arquivo a 1× e a 3× (o retrato 16; o 32 e o 48 são ×2 e ×3)",
           fill=(210, 210, 214, 255), font=f)
    for k, nome in enumerate(("retrato-arvore-desperta", "retrato-golem")):
        ic = Image.open(ICONES / f"{nome}-16.png").convert("RGBA")
        out.alpha_composite(ic, (16 + k * 90, y + 30))
        out.alpha_composite(ic.resize((48, 48), Image.NEAREST), (40 + k * 90, y + 20))
    out = out.crop((0, 0, out.width, y + 76))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1189.png")
    print("integracoes-1189.png", out.size)


if __name__ == "__main__":
    main()
