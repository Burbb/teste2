"""As folhas do C1:
  - c1.png: a referência, a guia e o C1 ampliados sem suavização (12×, a referência na mesma altura); o elmo do jogo e o
    C1 em tamanho real e a 4×, junto da cota, da luva L7, das perneiras e das botas do jogo;
  - c1-ficha.png: a ficha a 1920×945 com os mesmos dados, o elmo do jogo × o C1 (fotografar.mjs capacete_c1).
    python prancha.py <pasta do C1>
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[6]
ICONES = RAIZ / "rpg/web/static/hud/icones"
REF = RAIZ / "ferramentas/arte/referencias/capacete/capacete-malha-gerada.webp"
CAIXA = (191, 90, 1065, 1180)   # a caixa do desenho na referência (a da guia.py)
Z = 12
FUNDO, TEXTO = (24, 24, 28, 255), (200, 200, 205, 255)


def desenho(w, h):
    out = Image.new("RGBA", (w, h), FUNDO)
    d = ImageDraw.Draw(out)
    try: d.font = ImageFont.truetype("arial.ttf", 13)   # com acentos (a fonte padrão do Pillow não tem)
    except OSError: pass
    return out, d


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    c1 = Image.open(base / "proposta/C1-32.png").convert("RGBA")
    guia = Image.open(base / "previa/guia-32.png").convert("RGBA")
    ref = Image.open(REF).convert("RGBA").crop(CAIXA)
    ref = ref.resize((round(ref.width * 30 * Z / ref.height), 30 * Z), Image.LANCZOS)  # a referência só para olhar
    conjunto = [("elmo (jogo)", Image.open(ICONES / "elmo-32.png")), ("C1", c1), ("cota", Image.open(ICONES / "cota-32.png")),
                ("luva L7", Image.open(ICONES / "manopla-32.png")), ("perneiras", Image.open(ICONES / "perneiras-32.png")),
                ("botas", Image.open(ICONES / "botas-ferro-32.png"))]
    out, d = desenho(max(40 + ref.width + 2 * (32 * Z + 30), 20 + 6 * 150), 32 * Z + 300)
    x = 20
    for rotulo, im, y in (("referência", ref, 30 + Z), ("guia (a média, 32)", guia.resize((32 * Z,) * 2, Image.NEAREST), 30),
                          ("C1 (32, 12×)", c1.resize((32 * Z,) * 2, Image.NEAREST), 30)):
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
    out.save(base / "c1.png")
    fichas = [Image.open(base / f"capturas/{n}-1920x945-ficha.png").convert("RGBA") for n in ("atual", "proposta")]
    w, h = fichas[0].size
    out, d = desenho(2 * w + 60, h + 30)
    for k, (rotulo, im) in enumerate(zip(("elmo do jogo", "C1"), fichas)):
        d.text((20 + k * (w + 20), 8), rotulo, fill=TEXTO)
        out.alpha_composite(im, (20 + k * (w + 20), 26))
    out.save(base / "c1-ficha.png")
