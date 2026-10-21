"""As folhas da A1 (o acabamento contido das botas B3):
  - a1.png: a B3 do jogo e a A1 ampliadas 12× sem suavização, com a referência de acabamento ao lado; as duas em tamanho
    real e a 4× junto do conjunto atualizado (o capacete C1, a cota, a luva L7, as perneiras P7);
  - a1-ficha.png: a ficha a 1920×945 com os mesmos dados, a B3 do jogo × a A1 (fotografar.mjs botas_a1).
    python prancha.py <pasta da A1>
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[7]
ICONES = RAIZ / "rpg/web/static/hud/icones"
REF = RAIZ / "ferramentas/arte/referencias/botas/Botas de ferro em pixel art.png"
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
    a1 = Image.open(base / "proposta/A1-32.png").convert("RGBA")
    b3 = Image.open(ICONES / "botas-ferro-32.png").convert("RGBA")
    ref = Image.open(REF).convert("RGBA")
    ref = ref.crop(ref.getbbox()).resize((32 * Z * ref.width // ref.height, 32 * Z), Image.LANCZOS)  # só para olhar
    conjunto = [("capacete C1", Image.open(ICONES / "elmo-32.png")), ("cota", Image.open(ICONES / "cota-32.png")),
                ("luva L7", Image.open(ICONES / "manopla-32.png")), ("perneiras P7", Image.open(ICONES / "perneiras-32.png")),
                ("B3 (jogo)", b3), ("A1", a1)]
    out, d = desenho(max(20 + 2 * (32 * Z + 30) + ref.width + 20, 20 + 6 * 150), 32 * Z + 300)
    x = 20
    for rotulo, im in (("B3 do jogo, 12×", b3.resize((32 * Z,) * 2, Image.NEAREST)),
                       ("A1, 12×", a1.resize((32 * Z,) * 2, Image.NEAREST)), ("referência de acabamento", ref)):
        d.text((x, 8), rotulo, fill=TEXTO)
        out.alpha_composite(im, (x, 26))
        x += im.width + 30
    y = 32 * Z + 50
    d.text((20, y - 16), "tamanho real", fill=TEXTO)
    for k, (_, im) in enumerate(conjunto): out.alpha_composite(im.convert("RGBA"), (20 + k * 44, y))
    y += 56
    for k, (rotulo, im) in enumerate(conjunto):
        d.text((20 + k * 150, y), rotulo, fill=TEXTO)
        out.alpha_composite(im.convert("RGBA").resize((128, 128), Image.NEAREST), (20 + k * 150, y + 16))
    out.save(base / "a1.png")
    fichas = [Image.open(base / f"capturas/{n}-1920x945-ficha.png").convert("RGBA") for n in ("atual", "proposta")]
    w, h = fichas[0].size
    out, d = desenho(2 * w + 60, h + 30)
    for k, (rotulo, im) in enumerate(zip(("B3 do jogo", "A1"), fichas)):
        d.text((20 + k * (w + 20), 8), rotulo, fill=TEXTO)
        out.alpha_composite(im, (20 + k * (w + 20), 26))
    out.save(base / "a1-ficha.png")
