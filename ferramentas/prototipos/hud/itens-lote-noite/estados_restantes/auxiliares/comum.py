"""O que as ferramentas do lote dos 14 estados (21/10/2026) dividem: os sprites atuais do jogo (com as variantes de cor
de sprites-dados.js), os três estados finais, a leitura das grades e o carvão das folhas."""
import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
LOTE = AQUI.parent
RAIZ = AQUI.parents[5]
STATIC = RAIZ / "rpg/web/static"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (200, 200, 205, 255), (140, 140, 148, 255)

# os 14 estados do lote, na ordem dos lotes: (id do motor, título, sprite atual)
ESTADOS = [("veneno", "Veneno", "gota_verde"), ("sangramento", "Sangramento", "gota"),
           ("queimadura", "Chamas", "chama"), ("maldito", "Maldição", "gota_roxa"),
           ("atordoado", "Atordoado", "estrela"), ("enfraquecido", "Enfraquecido", "osso"),
           ("marcado", "Marcado", "flecha"), ("furtivo", "Furtivo", "olho"),
           ("barreira", "Barreira", "escudo_azul"), ("provocando", "Provocando", "caveira"),
           ("fortalecido", "Fortalecido", "espada"), ("iniciativa", "Iniciativa", "bota"),
           ("furia", "Fúria", "machado"), ("frenesi", "Frenesi", "raio")]
LOTES = {1: ("veneno", "sangramento"), 2: ("queimadura", "maldito"), 3: ("atordoado", "enfraquecido"),
         4: ("marcado", "furtivo"), 5: ("barreira", "provocando"), 6: ("fortalecido", "iniciativa"),
         7: ("furia", "frenesi")}
TITULO = {k: t for k, t, _ in ESTADOS}
ATUAL = {k: s for k, _, s in ESTADOS}
FINAIS = [("firme", "Firme"), ("guarda", "Em guarda"), ("esquiva", "Esquiva")]


def fonte(tam=13):
    try:
        return ImageFont.truetype("arial.ttf", tam)
    except OSError:
        return ImageFont.load_default()


def _paleta():
    return dict(re.findall(r'(\w): "#([0-9a-f]{6})"', re.search(r"const PALETA = \{(.*?)\};",
                (STATIC / "sprites.js").read_text(encoding="utf-8"), re.S).group(1)))


def _grade(nome, texto):
    m = re.search(rf"\n    {nome}: \[(.*?)\]", texto, re.S) or re.search(rf"\n  S\.{nome} = \[(.*?)\]", texto, re.S)
    if m:
        return re.findall(r'"([^"]+)"', m.group(1))
    m = re.search(rf"S\.{nome} = trocar\(S\.(\w+), \{{(.*?)\}}\)", texto)   # uma variante de cor (gota_verde...)
    troca = dict(re.findall(r'(\w): "(\w)"', m.group(2)))
    return ["".join(troca.get(c, c) for c in l) for l in _grade(m.group(1), texto)]


def sprite(nome):
    """O sprite 16×16 do jogo (sprites-dados.js), como o jogo o pinta (pixel a pixel, sem sombra)."""
    pal, texto = _paleta(), (STATIC / "sprites-dados.js").read_text(encoding="utf-8")
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(_grade(nome, texto)):
        for x, c in enumerate(l):
            if c in pal:
                im.putpixel((x, y), tuple(int(pal[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def abre(arq):
    return Image.open(arq).convert("RGBA")


def final(ident):
    return abre(STATIC / f"hud/icones/estado-{ident}-16.png")


def proposta(ident):
    """O desenho proposto (proposta/<ident>-16.png, ident = "estado-<id>..."), ou None se ainda não existe."""
    arq = LOTE / f"proposta/{ident}-16.png"
    return abre(arq) if arq.exists() else None


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


def grade_px(im, z, cor=(40, 36, 34, 255)):
    """A ampliação z× com a grade de pixels desenhada, para achar o pixel."""
    out = Image.new("RGBA", (im.width * z, im.height * z), (24, 21, 19, 255))
    out.alpha_composite(amplia(im, z))
    d = ImageDraw.Draw(out)
    for i in range(1, im.width):
        d.line([(i * z, 0), (i * z, out.height)], fill=cor)
    for i in range(1, im.height):
        d.line([(0, i * z), (out.width, i * z)], fill=cor)
    return out
