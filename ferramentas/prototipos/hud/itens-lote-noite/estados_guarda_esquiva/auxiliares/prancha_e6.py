"""A folha da E6, a cópia da figura em movimento (esquiva-e6.png). Cada ícone entra pelo nome e pelo arquivo, nunca pela
posição (o Em guarda e o Firme são os arquivos do jogo):
  - a fileira da carta, Firme · Em guarda · Esquiva, para a folha do jogo, a E3, a E5 (recusada) e a E6, em tamanho real
    e a 2×;
  - a E6 numa cor só (a silhueta, sem contorno nem tons), em tamanho real, a 2× e a 12×, ao lado da referência e da E6
    acabada a 12× (as ampliações só para inspecionar os pixels);
  - a carta do Arqueiro na luta a 1920×945 com os mesmos dados (fotografar_luta.mjs com TROCAS=trocas-r4.json): a folha,
    a E3 e a E6, em tamanho real e a 2×.
    python prancha_e6.py <pasta>
"""
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parents[6]
STATIC = RAIZ / "rpg/web/static"
REF = RAIZ / "ferramentas/arte/referencias/icones/esquiva-figura-movimento.png"
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
    abre = lambda arq: Image.open(arq).convert("RGBA")
    FIRME, GUARDA = abre(STATIC / "hud/icones/estado-firme-16.png"), abre(STATIC / "hud/icones/estado-guarda-16.png")
    e6 = abre(base / "proposta/estado-esquiva-e6-16.png")
    linhas = [l for l in (base / "grades/estado-esquiva-e6.txt").read_text(encoding="utf-8").split("\n")[:16]]
    silhueta = Image.new("RGBA", (16, 16))
    for y, l in enumerate(linhas):
        for x, c in enumerate(l):
            if c not in ".#": silhueta.putpixel((x, y), (176, 182, 189, 255))
    ESQUIVAS = [("jogo (folha)", sprite("folha")), ("E3, a bota", abre(base / "proposta/estado-esquiva-e3-16.png")),
                ("E5, a pose à mão (recusada)", abre(base / "proposta/estado-esquiva-e5-16.png")),
                ("E6, a cópia da referência", e6)]
    cartas = [(rot, abre(base / f"capturas/rodada4/{m}-1920x945-carta.png")) for rot, m in
              (("jogo (folha)", "atual"), ("E3", "e3"), ("E6", "e6"))]
    cw, ch = cartas[0][1].size
    out = Image.new("RGBA", (max(60 + 4 * (16 * Z + 20), 40 + 3 * (cw + 20), 40 + 2 * (2 * cw + 20)),
                             30 + 4 * 40 + 40 + 16 * Z + 50 + ch + 40 + 2 * ch + 40), CARVAO)
    d = ImageDraw.Draw(out)
    try: d.font = ImageFont.truetype("arial.ttf", 13)
    except OSError: pass
    d.text((20, 6), "a fileira da carta: Firme · Em guarda (o G1 do jogo) · Esquiva, em tamanho real e a 2×", fill=TEXTO)
    for k, (rot, esq) in enumerate(ESQUIVAS):
        y = 30 + k * 40
        for j, im in enumerate((FIRME, GUARDA, esq)):
            out.alpha_composite(im, (20 + j * 22, y + 8))
            out.alpha_composite(im.resize((32, 32), Image.NEAREST), (110 + j * 40, y))
        d.text((240, y + 9), "Esquiva: " + rot, fill=TEXTO)
    y = 30 + 4 * 40 + 20
    d.text((20, y), "E6 numa cor só: real, 2×, 12×", fill=TEXTO)
    out.alpha_composite(silhueta, (20, y + 24)); out.alpha_composite(silhueta.resize((32, 32), Image.NEAREST), (44, y + 24))
    out.alpha_composite(silhueta.resize((16 * Z,) * 2, Image.NEAREST), (90, y + 24))
    d.text((90 + 16 * Z + 20, y), "E6 acabada (12×)", fill=TEXTO)
    out.alpha_composite(e6.resize((16 * Z,) * 2, Image.NEAREST), (90 + 16 * Z + 20, y + 24))
    ref = abre(REF); ref = ref.crop((0, 38, 182, 174)).resize((16 * Z, round(136 * 16 * Z / 182)), Image.LANCZOS)
    fundo = Image.new("RGBA", (16 * Z, 16 * Z), (255, 255, 255, 255)); fundo.alpha_composite(ref, (0, (16 * Z - ref.height) // 2))
    d.text((90 + 2 * (16 * Z + 20), y), "referência", fill=TEXTO)
    out.alpha_composite(fundo, (90 + 2 * (16 * Z + 20), y + 24))
    y += 16 * Z + 50
    for k, (rot, im) in enumerate(cartas):
        d.text((20 + k * (cw + 20), y), f"carta a 1920×945: Esquiva {rot}", fill=TEXTO)
        out.alpha_composite(im, (20 + k * (cw + 20), y + 18))
    y += ch + 40
    for k, (rot, im) in enumerate(cartas[1:]):
        d.text((20 + k * (2 * cw + 20), y), f"a 2×: Esquiva {rot}", fill=TEXTO)
        out.alpha_composite(im.resize((2 * cw, 2 * ch), Image.NEAREST), (20 + k * (2 * cw + 20), y + 18))
    out.save(base / "esquiva-e6.png")
