"""A prancha da P6 (p6.png): a referência, a guia e a proposta ampliadas sem suavização (12×, a referência na mesma
altura), e o conjunto de ferro final (o elmo, a cota, as perneiras P4 do jogo, a P6 e as botas) em tamanho real e a 4×.
    python prancha.py <pasta da P6>
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[6]
ICONES = RAIZ / "rpg/web/static/hud/icones"
REF = RAIZ / "ferramentas/arte/referencias/calça/perneiras-gerada.webp"
CAIXA = (354, 141, 918, 1098)   # a caixa do desenho na referência (a mesma do transpor.py)
Z = 12
FUNDO, TEXTO = (24, 24, 28, 255), (200, 200, 205, 255)

if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    p6 = Image.open(base / "proposta/P6-32.png").convert("RGBA")
    guia = Image.open(base / "previa/guia-32.png").convert("RGBA")
    ref = Image.open(REF).convert("RGBA").crop(CAIXA)
    ref = ref.resize((round(ref.width * 30 * Z / ref.height), 30 * Z), Image.LANCZOS)  # a referência só para olhar
    conjunto = [("elmo", Image.open(ICONES / "elmo-32.png")), ("cota", Image.open(ICONES / "cota-32.png")),
                ("P4 (jogo)", Image.open(ICONES / "perneiras-32.png")), ("P6", p6),
                ("botas", Image.open(ICONES / "botas-ferro-32.png"))]
    out = Image.new("RGBA", (40 + ref.width + 2 * (32 * Z + 30) + 20, 32 * Z + 300), FUNDO)
    d = ImageDraw.Draw(out)
    try: d.font = ImageFont.truetype("arial.ttf", 13)   # com acentos (a fonte padrão do Pillow não tem)
    except OSError: pass
    x = 20
    for rotulo, im, y in (("referência", ref, 30 + Z), ("guia (a média, 32)", guia.resize((32 * Z,) * 2, Image.NEAREST), 30),
                          ("P6 (32, 12×)", p6.resize((32 * Z,) * 2, Image.NEAREST), 30)):
        d.text((x, 8), rotulo, fill=TEXTO)
        out.alpha_composite(im, (x, y))
        x += im.width + 30
    y = 32 * Z + 50
    d.text((20, y - 16), "tamanho real", fill=TEXTO)
    for k, (_, im) in enumerate(conjunto): out.alpha_composite(im.convert("RGBA"), (20 + k * 44, y))
    y += 56
    for k, (rotulo, im) in enumerate(conjunto):
        d.text((20 + k * 150, y), rotulo, fill=TEXTO)
        out.alpha_composite(im.convert("RGBA").resize((128, 128), Image.NEAREST), (20 + k * 150, y + 16))
    out.save(base / "p6.png")
