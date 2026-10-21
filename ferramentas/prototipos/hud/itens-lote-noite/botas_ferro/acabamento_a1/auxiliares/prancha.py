"""As folhas da A1 (o acabamento contido das botas B3):
  - a1.png: a B3 do jogo e a A1 ampliadas 12× sem suavização, com a referência de acabamento ao lado; as duas em tamanho
    real e a 4× junto do conjunto atualizado (o capacete C1, a cota, a luva L7, as perneiras P7);
  - a1-ficha.png: a ficha a 1920×945 com os mesmos dados, a B3 do jogo × a A1 (fotografar.mjs botas_a1);
  - a1-tamanhos.png: os quatro tamanhos, B3 do jogo × A1, em tamanho real e ampliados 4× (o 32, o 40, o 48 e o 64 sem
    ampliar), junto do C1, da cota, da L7 e da P7 (o 32 deles e o 40 do Inventário); a1-tamanhos-no-jogo.png: o
    Inventário (40) e o saque (64 e o "você usa" em 48), atual × A1 (fotografar.mjs botas_a1_tamanhos).
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

    # os quatro tamanhos
    linhas = [("B3 (jogo)", {n: Image.open(ICONES / f"botas-ferro-{n}.png").convert("RGBA") for n in (32, 40, 48, 64)}),
              ("A1", {n: Image.open(base / f"proposta/A1-{n}.png").convert("RGBA") for n in (32, 40, 48, 64)})]
    vizinhos = {n: [Image.open(ICONES / f"{p}-{n}.png").convert("RGBA") for p in ("elmo", "cota", "manopla", "perneiras")]
                for n in (32, 40)}
    out, d = desenho(1300, 2 * 230 + 140)
    y = 10
    for rotulo, ims in linhas:
        d.text((20, y), rotulo, fill=TEXTO)
        x = 20
        for n in (32, 40, 48, 64):
            out.alpha_composite(ims[n], (x, y + 20))
            x += n + 16
        for n in (32, 40, 48):
            out.alpha_composite(ims[n].resize((4 * n, 4 * n), Image.NEAREST), (x, y + 20))
            x += 4 * n + 16
        y += 230
    d.text((20, y), "o conjunto (C1, cota, L7, P7) no 32 e no 40, com a A1", fill=TEXTO)
    x = 20
    for n in (32, 40):
        for im in vizinhos[n] + [linhas[1][1][n]]:
            out.alpha_composite(im, (x, y + 20))
            x += n + 8
        x += 30
    out.save(base / "a1-tamanhos.png")
    cap = base / "capturas/tamanhos"
    fotos = [[Image.open(cap / f"{m}-1920x945-{f}.png").convert("RGBA") for m in ("atual", "proposta")]
             for f in ("inventario", "saque")]
    w = max(im.width for par in fotos for im in par)
    h = sum(max(im.height for im in par) + 30 for par in fotos)
    out, d = desenho(2 * w + 60, h + 10)
    y = 0
    for par in fotos:
        for k, (rotulo, im) in enumerate(zip(("B3 do jogo", "A1"), par)):
            d.text((20 + k * (w + 20), y + 8), rotulo, fill=TEXTO)
            out.alpha_composite(im, (20 + k * (w + 20), y + 26))
        y += max(im.height for im in par) + 30
    out.save(base / "a1-tamanhos-no-jogo.png")
