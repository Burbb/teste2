"""A folha compacta das integrações de 22/10/2026 (integracoes.png), só com as capturas do jogo já registradas em cada
integração, a 1920×945: o Esqueleto E1r (1.175.0) na luta do Lich com os invocados (o palco, o alto das cartas); o urso
e o falcão na fogueira (1.176.0) ao lado do lobo; o cajado no Atacar do Mago (1.177.0). Tamanho real, sem ampliação.
    python prancha.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
FOTOS = [
    ("1.175.0 — o Esqueleto E1r pela família: o Lich Menor com dois invocados (o Lich continua na caveira)",
     HUD / "criaturas/esqueleto_novo/capturas-1175/lich-atual-palco.png", (0, 0, 1088, 230)),
    ("1.176.0 — a fogueira pelo tipo do animal: o lobo c2 (1.170.0), o urso r4 e o falcão",
     HUD / "acampamento_atacar/capturas-1176/fogueira-lobo.png", None),
    ("", HUD / "acampamento_atacar/capturas-1176/fogueira-urso.png", None),
    ("", HUD / "acampamento_atacar/capturas-1176/fogueira-falcao.png", None),
    ("1.177.0 — o Atacar do Mago com o cajado de equipamento", HUD / "acampamento_atacar/capturas-1177/roda-mago.png", None),
]


def main():
    f = ImageFont.truetype("arial.ttf", 14)
    ims = [(t, Image.open(p).convert("RGBA").crop(c) if c else Image.open(p).convert("RGBA")) for t, p, c in FOTOS]
    w = max(im.width for _, im in ims) + 32
    h = sum(im.height + (26 if t else 8) for t, im in ims) + 24
    out = Image.new("RGBA", (w, h), (13, 11, 10, 255))
    d = ImageDraw.Draw(out)
    y = 12
    for t, im in ims:
        if t:
            d.text((16, y), t, fill=(210, 210, 214, 255), font=f)
            y += 20
        out.alpha_composite(im, (16, y))
        y += im.height + 8
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes.png")
    print("integracoes.png", out.size)


if __name__ == "__main__":
    main()
