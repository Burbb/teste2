"""As folhas da P7:
  - p7.png: a referência, a guia e a P7 ampliadas sem suavização (12×, a referência na mesma altura); o elmo, a cota, a
    P4 do jogo, a P6 (52de4445), a P7 e as botas em tamanho real e a 4×;
  - p7-ficha.png: a ficha a 1920×945 com os mesmos dados, P6 × P7 (as capturas de fotografar.mjs perneiras_p7);
  - p7-retoque.png e p7-retoque-ficha.png: o retoque das laterais (retoque.py), antes (anterior_3cb041db/) × depois, em
    tamanho real junto do conjunto, a 4× e a 12× sem suavização, e na ficha (a captura de antes guardada lá).
    python prancha.py <pasta da P7>
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[6]
ICONES = RAIZ / "rpg/web/static/hud/icones"
REF = RAIZ / "ferramentas/arte/referencias/calça/perneiras-gerada-2.webp"
P6 = RAIZ / "ferramentas/prototipos/hud/itens-lote-noite/perneiras_p6/proposta/P6-32.png"
CAIXA = (357, 120, 970, 1057)   # a caixa do desenho na referência (a da guia.py)
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
    p7 = Image.open(base / "proposta/P7-32.png").convert("RGBA")
    guia = Image.open(base / "previa/guia-32.png").convert("RGBA")
    ref = Image.open(REF).convert("RGBA").crop(CAIXA)
    ref = ref.resize((round(ref.width * 30 * Z / ref.height), 30 * Z), Image.LANCZOS)  # a referência só para olhar
    conjunto = [("elmo", Image.open(ICONES / "elmo-32.png")), ("cota", Image.open(ICONES / "cota-32.png")),
                ("P4 (jogo)", Image.open(ICONES / "perneiras-32.png")), ("P6", Image.open(P6)), ("P7", p7),
                ("botas", Image.open(ICONES / "botas-ferro-32.png"))]
    out, d = desenho(max(40 + ref.width + 2 * (32 * Z + 30), 20 + 6 * 150), 32 * Z + 300)
    x = 20
    for rotulo, im, y in (("referência", ref, 30 + Z), ("guia (a média, 32)", guia.resize((32 * Z,) * 2, Image.NEAREST), 30),
                          ("P7 (32, 12×)", p7.resize((32 * Z,) * 2, Image.NEAREST), 30)):
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
    out.save(base / "p7.png")
    fichas = [Image.open(base / f"capturas/{n}-1920x945-ficha.png").convert("RGBA") for n in ("p6", "p7")]
    w, h = fichas[0].size
    out, d = desenho(2 * w + 60, h + 30)
    for k, (rotulo, im) in enumerate(zip(("P6", "P7"), fichas)):
        d.text((20 + k * (w + 20), 8), rotulo, fill=TEXTO)
        out.alpha_composite(im, (20 + k * (w + 20), 26))
    out.save(base / "p7-ficha.png")

    # o retoque das laterais: antes × depois
    antes = Image.open(base / "anterior_3cb041db/proposta/P7-32.png").convert("RGBA")
    conjunto = [("elmo", Image.open(ICONES / "elmo-32.png")), ("cota", Image.open(ICONES / "cota-32.png")),
                ("P7 antes", antes), ("P7 depois", p7), ("botas", Image.open(ICONES / "botas-ferro-32.png"))]
    out, d = desenho(20 + 2 * (32 * Z + 30), 32 * Z + 300)
    for k, (rotulo, im) in enumerate((("antes (3cb041db), 12×", antes), ("depois, 12×", p7))):
        d.text((20 + k * (32 * Z + 30), 8), rotulo, fill=TEXTO)
        out.alpha_composite(im.resize((32 * Z,) * 2, Image.NEAREST), (20 + k * (32 * Z + 30), 26))
    y = 32 * Z + 50
    d.text((20, y - 16), "tamanho real", fill=TEXTO)
    for k, (_, im) in enumerate(conjunto): out.alpha_composite(im.convert("RGBA"), (20 + k * 44, y))
    y += 56
    for k, (rotulo, im) in enumerate(conjunto):
        d.text((20 + k * 150, y), rotulo, fill=TEXTO)
        out.alpha_composite(im.convert("RGBA").resize((128, 128), Image.NEAREST), (20 + k * 150, y + 16))
    out.save(base / "p7-retoque.png")
    fichas = [Image.open(base / "anterior_3cb041db/p7-1920x945-ficha.png").convert("RGBA"),
              Image.open(base / "capturas/p7-1920x945-ficha.png").convert("RGBA")]
    w, h = fichas[0].size
    out, d = desenho(2 * w + 60, h + 30)
    for k, (rotulo, im) in enumerate(zip(("P7 antes", "P7 depois"), fichas)):
        d.text((20 + k * (w + 20), 8), rotulo, fill=TEXTO)
        out.alpha_composite(im, (20 + k * (w + 20), 26))
    out.save(base / "p7-retoque-ficha.png")
