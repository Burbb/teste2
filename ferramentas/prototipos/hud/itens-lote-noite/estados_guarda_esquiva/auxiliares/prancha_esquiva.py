"""A folha das alternativas da Esquiva (esquiva-alternativas.png): a bota dando um passo (E3) e a figura que sai do lugar
(E4), com a E1 e a E2 recusadas como histórico.

Cada ícone entra pelo nome e pelo arquivo, nunca pela posição: o Em guarda é sempre o arquivo do jogo
(rpg/web/static/hud/icones/estado-guarda-16.png, o G1 integrado na 1.156.0), o Firme também (estado-firme-16.png), e cada
Esquiva vem do arquivo dela em proposta/. (Na rodada 2, um visualizador de rascunho fora do repositório punha as propostas
por posição nas casas do escudo e da Esquiva; com as duas variantes de curva passadas a ele, a fileira mostrou duas
curvas onde deviam estar o escudo e a Esquiva. Era só a montagem: o jogo mapeia só `firme` e `guarda` em `ESTADO`.)

  - a fileira dos chips em tamanho real (16 px) e a 2× sobre o carvão: Firme, Em guarda e a Esquiva de cada
    alternativa, na ordem da carta, com o rótulo de cada uma;
  - as alternativas ampliadas 12× sem suavização, só para inspecionar os pixels;
  - a carta do Arqueiro na luta a 1920×945 com os mesmos dados (fotografar_luta.mjs com TROCAS=trocas-r3.json): o jogo
    (a folha), a E1, a E3 e a E4, em tamanho real e a 2×.
    python prancha_esquiva.py <pasta>
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
    abre = lambda arq: Image.open(arq).convert("RGBA")
    FIRME = abre(STATIC / "hud/icones/estado-firme-16.png")
    GUARDA = abre(STATIC / "hud/icones/estado-guarda-16.png")
    ESQUIVAS = [("jogo (folha)", sprite("folha")),
                ("E1, vento (recusada)", abre(base / "proposta/estado-esquiva-16.png")),
                ("E2, crescentes (recusada)", abre(base / "proposta/estado-esquiva-e2-16.png")),
                ("E3, bota dando um passo", abre(base / "proposta/estado-esquiva-e3-16.png")),
                ("E4, figura saindo do lugar", abre(base / "proposta/estado-esquiva-e4-16.png"))]
    cap = base / "capturas/rodada3"
    cartas = [(rot, abre(cap / f"{m}-1920x945-carta.png")) for rot, m in
              (("jogo (folha)", "atual"), ("E1", "e1"), ("E3", "e3"), ("E4", "e4"))]
    cw, ch = cartas[0][1].size
    alt = 30 + len(ESQUIVAS) * 40 + 30 + 16 * Z + 50 + 3 * ch + 40
    out = Image.new("RGBA", (max(40 + 4 * (16 * Z + 20), 40 + 4 * (cw + 20), 900), alt), CARVAO)
    d = ImageDraw.Draw(out)
    try: d.font = ImageFont.truetype("arial.ttf", 13)
    except OSError: pass
    d.text((20, 6), "a fileira da carta: Firme · Em guarda (o G1 do jogo) · Esquiva — em tamanho real e a 2×", fill=TEXTO)
    for k, (rot, esq) in enumerate(ESQUIVAS):
        y = 30 + k * 40
        for j, im in enumerate((FIRME, GUARDA, esq)):
            out.alpha_composite(im, (20 + j * 22, y + 8))
            out.alpha_composite(im.resize((32, 32), Image.NEAREST), (110 + j * 40, y))
        d.text((240, y + 9), "Esquiva: " + rot, fill=TEXTO)
    y = 30 + len(ESQUIVAS) * 40 + 20
    for k, (rot, im) in enumerate(ESQUIVAS[3:] + ESQUIVAS[1:3]):
        x = 20 + k * (16 * Z + 20)
        d.text((x, y), rot + " (12×)", fill=TEXTO)
        out.alpha_composite(im.resize((16 * Z,) * 2, Image.NEAREST), (x, y + 18))
    y += 16 * Z + 50
    for k, (rot, im) in enumerate(cartas):
        x = 20 + k * (cw + 20)
        d.text((x, y), f"carta a 1920×945: Esquiva {rot}", fill=TEXTO)
        out.alpha_composite(im, (x, y + 18))
    y += ch + 30
    for k, (rot, im) in enumerate(cartas[2:]):
        x = 20 + k * (2 * cw + 20)
        d.text((x, y), f"a 2×: Esquiva {rot}", fill=TEXTO)
        out.alpha_composite(im.resize((2 * cw, 2 * ch), Image.NEAREST), (x, y + 18))
    out.save(base / "esquiva-alternativas.png")
