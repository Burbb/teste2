"""A folha do par Em guarda (G1) e Esquiva (E1), guarda-esquiva.png:
  - a fileira dos estados em tamanho real (16 px) e a 2× sobre o carvão, atual (os sprites "escudo" e "folha" do jogo)
    × proposta, junto do Firme do jogo (a R2) e do Atordoado (a estrela);
  - o atual e a proposta ampliados 12× sem suavização;
  - a carta do Arqueiro na luta a 1920×945, atual × proposta, em tamanho real e a 2× (os mesmos dados:
    flechas_firme/auxiliares/fotografar_luta.mjs com TROCAS=auxiliares/trocas.json).
    python prancha.py <pasta>
"""
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[6]
STATIC = RAIZ / "rpg/web/static"
CARVAO, TEXTO = (13, 11, 10, 255), (200, 200, 205, 255)
Z = 12


def sprite(nome):
    pal = dict(re.findall(r'(\w): "#([0-9a-f]{6})"', re.search(r"const PALETA = \{(.*?)\};",
                          (STATIC / "sprites.js").read_text(encoding="utf-8"), re.S).group(1)))
    texto = (STATIC / "sprites-dados.js").read_text(encoding="utf-8")
    linhas = re.findall(r'"([^"]+)"', re.search(rf"\n    {nome}: \[(.*?)\]", texto, re.S).group(1))
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c in pal: im.putpixel((x, y), tuple(int(pal[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    firme = Image.open(STATIC / "hud/icones/estado-firme-16.png").convert("RGBA")
    estrela = sprite("estrela")
    atual = [sprite("escudo"), sprite("folha")]
    prop = [Image.open(base / f"proposta/estado-{n}-16.png").convert("RGBA") for n in ("guarda", "esquiva")]
    cartas = [Image.open(base / f"capturas/{m}-1920x945-carta.png").convert("RGBA") for m in ("atual", "proposta")]
    cw, ch = cartas[0].size
    out = Image.new("RGBA", (max(40 + 4 * (16 * Z + 20), 40 + 2 * (2 * cw + 20)), 130 + 16 * Z + 60 + 3 * ch + 40), CARVAO)
    d = ImageDraw.Draw(out)
    try: d.font = ImageFont.truetype("arial.ttf", 13)
    except OSError: pass
    for k, (rot, par) in enumerate((("atual", atual), ("proposta", prop))):
        y = 20 + k * 44
        d.text((20, y + 2), rot, fill=TEXTO)
        fila = par + [firme, estrela]   # Em guarda, Esquiva, Firme, Atordoado: a ordem da carta
        for j, im in enumerate(fila):
            out.alpha_composite(im, (100 + j * 22, y))
            out.alpha_composite(im.resize((32, 32), Image.NEAREST), (220 + j * 40, y - 8))
    d.text((420, 22), "em guarda · esquiva · firme · atordoado (tamanho real e 2×)", fill=TEXTO)
    y = 120
    for k, (rot, im) in enumerate(zip(("Em guarda: atual", "Em guarda: G1", "Esquiva: atual", "Esquiva: E1"),
                                      (atual[0], prop[0], atual[1], prop[1]))):
        d.text((20 + k * (16 * Z + 20), y), rot + " (12×)", fill=TEXTO)
        out.alpha_composite(im.resize((16 * Z,) * 2, Image.NEAREST), (20 + k * (16 * Z + 20), y + 18))
    y += 16 * Z + 40
    for k, (rot, im) in enumerate(zip(("atual", "proposta"), cartas)):
        d.text((20 + k * (2 * cw + 20), y), f"{rot}: a carta do Arqueiro a 1920×945 (tamanho real e 2×)", fill=TEXTO)
        out.alpha_composite(im, (20 + k * (2 * cw + 20), y + 18))
        out.alpha_composite(im.resize((2 * cw, 2 * ch), Image.NEAREST), (20 + k * (2 * cw + 20), y + 26 + ch))
    out.save(base / "guarda-esquiva.png")
