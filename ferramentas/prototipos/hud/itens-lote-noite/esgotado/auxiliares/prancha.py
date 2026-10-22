"""A folha do Esgotado (esgotado.png): por linha, o atual (o cadeado), o caixote e o cesto; em cada uma, o pedaço do
mercado a 1920×945 em tamanho real (um cartão esgotado ao lado de um com "Ouro insuficiente", que continua no cadeado)
e a mesma área a 3× para achar o pixel; embaixo, os dois a 1× e 8× ao lado do Firme, do Atordoado e do Enfraquecido.
    python prancha.py      (depois do fotografar.mjs)
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

PASTA = pathlib.Path(__file__).resolve().parent.parent
RAIZ = PASTA.parents[4]
CARVAO = (24, 21, 19, 255)
TINTA = (226, 214, 190, 255)


def fonte(t):
    try:
        return ImageFont.truetype("arial.ttf", t)
    except OSError:
        return ImageFont.load_default()


def main():
    reg = json.loads((PASTA / "capturas/registro.json").read_text(encoding="utf-8"))
    # o recorte: as duas primeiras linhas de cartões (o Unguento esgotado entre a Bandagem e a Poção sem ouro)
    caixa = (250, 10, 1010, 190)
    linhas = []
    for nome, titulo in (("atual", "Atual: o cadeado (o antigo Firme)"), ("caixote", "A: o caixote vazio"),
                         ("cesto", "B: o cesto vazio")):
        im = Image.open(PASTA / f"capturas/suprimentos-{nome}.png").convert("RGBA").crop(caixa)
        linhas.append((titulo, im))
    w1 = caixa[2] - caixa[0]
    h1 = caixa[3] - caixa[1]
    zoom = (Image.open(PASTA / "capturas/suprimentos-atual.png").convert("RGBA").crop((570, 60, 740, 100)))
    zw, zh = zoom.size[0] * 3, zoom.size[1] * 3
    alto_linha = max(h1, zh) + 34
    W = Image.new("RGBA", (w1 + zw + 48, 40 + 3 * alto_linha + 260), CARVAO)
    d = ImageDraw.Draw(W)
    d.text((16, 10), "Esgotado no mercado, 1920×945 (tamanho real à esquerda; o mesmo motivo a 3× à direita)",
           fill=TINTA, font=fonte(16))
    for n, (titulo, im) in enumerate(linhas):
        y = 40 + n * alto_linha
        d.text((16, y), titulo, fill=TINTA, font=fonte(15))
        W.alpha_composite(im, (16, y + 24))
        nome = ("atual", "caixote", "cesto")[n]
        z = Image.open(PASTA / f"capturas/suprimentos-{nome}.png").convert("RGBA").crop((570, 60, 740, 100))
        W.alpha_composite(z.resize((zw, zh), Image.NEAREST), (w1 + 32, y + 24))
    y = 40 + 3 * alto_linha + 6
    d.text((16, y), "Os dois a 1× e 8×, ao lado do Firme, do Atordoado e do Enfraquecido (os estados aprovados)",
           fill=TINTA, font=fonte(15))
    ims = [Image.open(PASTA / f"proposta/{i}-16.png").convert("RGBA") for i in ("esgotado-caixote", "esgotado-cesto")]
    ims += [Image.open(RAIZ / f"rpg/web/static/hud/icones/estado-{e}-16.png").convert("RGBA")
            for e in ("firme", "atordoado", "enfraquecido")]
    for n, im in enumerate(ims):
        x = 16 + n * 160
        W.alpha_composite(im, (x, y + 30))
        W.alpha_composite(im.resize((128, 128), Image.NEAREST), (x + 24, y + 30))
    W.save(PASTA / "esgotado.png")
    print("esgotado.png", W.size, reg.get("erros"))


if __name__ == "__main__":
    main()
