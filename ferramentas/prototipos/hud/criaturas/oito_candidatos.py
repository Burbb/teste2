"""A folha compacta dos oito candidatos de 22/10/2026 (oito_candidatos.png): por criatura, o atual (o desenho do traço,
recortado da carta da luta) e as duas propostas, a 32 (a carta) e a 48 (o Bestiário) em tamanho real e a 3× sem
suavização. Nada no jogo.
    python oito_candidatos.py
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
LINHAS = [  # (criatura, pasta, nome na carta, A, B)
    ("Harpia", "harpia_grifo", "Harpia", "harpia-ha", "harpia-hb"),
    ("Grifo", "harpia_grifo", "Grifo", "grifo-ga", "grifo-gb"),
    ("Caído", "caidos", "Caído", "caido-ca", "caido-cb"),
    ("Xamã Caído", "caidos", "Xamã caído", "xama-caido-xa", "xama-caido-xb"),
]


def atual(pasta, nome):
    """O retrato de hoje: o ícone de 32 da carta inimiga na foto da luta do modo atual."""
    reg = json.loads((AQUI / pasta / "capturas/registro.json").read_text(encoding="utf-8"))
    x0, y0, _, _ = next(c["caixa"] for c in reg["luta/atual"]["caixas"] if c["nome"] == nome)
    foto = Image.open(AQUI / pasta / "capturas/luta-atual.png").convert("RGBA")
    return foto.crop((x0 + 8, y0 + 8, x0 + 8 + 32, y0 + 8 + 32))


def main():
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    larg_col = 32 + 48 + 96 + 30
    out = Image.new("RGBA", (150 + 3 * larg_col, 40 + len(LINHAS) * 175), (13, 11, 10, 255))
    d = ImageDraw.Draw(out)
    d.text((16, 10), "Os oito candidatos (22/10/2026) — atual × A × B; a 32 (carta) e a 48 (Bestiário) em tamanho real, a 3×",
           fill=(210, 210, 214, 255), font=f)
    for n, (nome, pasta, carta, a, b) in enumerate(LINHAS):
        y = 40 + n * 175
        d.text((16, y + 60), nome, fill=(210, 210, 214, 255), font=f)
        for c, (rot, im32) in enumerate((("atual", atual(pasta, carta)),
                                         (a, Image.open(AQUI / pasta / "proposta" / f"{a}-32.png").convert("RGBA")),
                                         (b, Image.open(AQUI / pasta / "proposta" / f"{b}-32.png").convert("RGBA")))):
            x = 150 + c * larg_col
            d.text((x, y), rot, fill=(140, 140, 148, 255), font=f2)
            out.alpha_composite(im32, (x, y + 20))
            im48 = im32.resize((48, 48), Image.NEAREST) if rot == "atual" else \
                Image.open(AQUI / pasta / "proposta" / f"{rot}-48.png").convert("RGBA")
            out.alpha_composite(im48, (x + 40, y + 20))
            out.alpha_composite(im32.resize((96, 96), Image.NEAREST), (x + 100, y + 20))
    out.save(AQUI / "oito_candidatos.png")
    print("oito_candidatos.png", out.size)


if __name__ == "__main__":
    main()
