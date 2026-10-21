"""As folhas da flecha da carta (F1) e do Firme (R1):
  - flechas-firme.png: o atual (os sprites "flecha" e "cadeado" do jogo, lidos de sprites-dados.js com a paleta de
    sprites.js) × a proposta, em tamanho real (16 px) sobre o carvão da HUD, ao lado de um número como o da carta, e
    ampliados 12× sem suavização; as referências reduzidas só para olhar; o Firme ao lado dos outros estados da carta
    (escudo, folha, estrela, como no jogo);
  - flechas-firme-luta.png: a carta do Arqueiro e a luta a 1920×945, atual × proposta, com os mesmos dados
    (auxiliares/fotografar_luta.mjs).
    python prancha.py <pasta>
"""
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[6]
STATIC = RAIZ / "rpg/web/static"
REFS = RAIZ / "ferramentas/arte/referencias/icones"
CARVAO, TEXTO = (23, 18, 15, 255), (200, 200, 205, 255)
Z = 12


def paleta():
    bloco = re.search(r"const PALETA = \{(.*?)\};", (STATIC / "sprites.js").read_text(encoding="utf-8"), re.S).group(1)
    return dict(re.findall(r'(\w): "#([0-9a-f]{6})"', bloco))


def sprite(nome, pal):
    texto = (STATIC / "sprites-dados.js").read_text(encoding="utf-8")
    bloco = re.search(rf"\n    {nome}: \[(.*?)\]", texto, re.S).group(1)
    linhas = re.findall(r'"([^"]+)"', bloco)
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c in pal: im.putpixel((x, y), tuple(int(pal[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def desenho(w, h):
    out = Image.new("RGBA", (w, h), CARVAO)
    d = ImageDraw.Draw(out)
    try:
        d.font = ImageFont.truetype("arial.ttf", 13)
        grande = ImageFont.truetype("arialbd.ttf", 17)
    except OSError:
        grande = None
    return out, d, grande


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    pal = paleta()
    pares = [("flecha da carta", sprite("flecha", pal), Image.open(base / "proposta/flecha_contador-16.png").convert("RGBA"),
              Image.open(REFS / "iconeflechaarqueiro.png").convert("RGBA")),
             ("Firme", sprite("cadeado", pal), Image.open(base / "proposta/firme-16.png").convert("RGBA"),
              Image.open(REFS / "iconefirme.png").convert("RGBA"))]
    outros = [sprite(n, pal) for n in ("escudo", "folha", "estrela")]   # Em guarda, Esquiva, Atordoado
    out, d, grande = desenho(20 + 2 * (16 * Z + 30) + 220 + 20, 2 * (16 * Z + 120) + 20)
    y = 10
    for rotulo, atual, prop, ref in pares:
        d.text((20, y), f"{rotulo}: atual × proposta (tamanho real, 2× e 12×)", fill=TEXTO)
        x = 20
        for im in (atual, prop):
            out.alpha_composite(im, (x, y + 24))
            if rotulo.startswith("flecha"): d.text((x + 19, y + 22), "20", fill=(235, 225, 205, 255), font=grande)
            out.alpha_composite(im.resize((32, 32), Image.NEAREST), (x, y + 48))
            x += 90
        if rotulo == "Firme":   # a fileira dos estados, como na carta: atual e proposta ao lado dos outros
            for k, fila in enumerate(([atual] + outros, [prop] + outros)):
                for j, im in enumerate(fila): out.alpha_composite(im, (210 + j * 22, y + 24 + k * 22))
        x = 20
        for im in (atual, prop):
            out.alpha_composite(im.resize((16 * Z,) * 2, Image.NEAREST), (x, y + 90))
            x += 16 * Z + 30
        r = ref.crop(ref.getbbox()); r.thumbnail((200, 16 * Z))
        out.alpha_composite(r, (x, y + 90))
        y += 16 * Z + 120
    out.save(base / "flechas-firme.png")
    cap = base / "capturas"
    cartas = [Image.open(cap / f"{m}-1920x945-carta.png").convert("RGBA") for m in ("atual", "proposta")]
    lutas = [Image.open(cap / f"{m}-1920x945-luta.png").convert("RGBA") for m in ("atual", "proposta")]
    w, h = lutas[0].size
    cw, ch = cartas[0].size
    out, d, _ = desenho(2 * w + 60, h + 3 * ch + 80)
    for k, rotulo in enumerate(("atual", "proposta")):
        d.text((20 + k * (w + 20), 8), f"{rotulo}: a carta do Arqueiro (tamanho real e 2×)", fill=TEXTO)
        out.alpha_composite(cartas[k], (20 + k * (w + 20), 26))
        out.alpha_composite(cartas[k].resize((2 * cw, 2 * ch), Image.NEAREST), (40 + cw + k * (w + 20), 26))
        d.text((20 + k * (w + 20), 2 * ch + 40), f"{rotulo}: a luta a 1920×945", fill=TEXTO)
        out.alpha_composite(lutas[k], (20 + k * (w + 20), 2 * ch + 58))
    out.save(base / "flechas-firme-luta.png")
