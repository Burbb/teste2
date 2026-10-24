"""As folhas da etapa 2 a partir das capturas de fotografar.mjs (23/10/2026):

    folha-estados.png   cada momento, atual × proposta, em 1× (o recorte do meio da tela, 900 ms depois de aparecer)
    folha-ritmo.png     cada momento nos cinco instantes (60, 250, 500, 900, 1600 ms), atual em cima, proposta embaixo
    folha-apertados.png a proposta a 1280×720 e com movimento reduzido (900 ms), ao lado do atual nas mesmas condições

    python folhas.py <pasta das capturas>
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

CAP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parents[1] / "capturas")
MOMENTOS = [("nivel", "nivel", "Nível 2 (guerreiro)"), ("dois-niveis", "nivel2", "Dois níveis: o 2 (mago)"),
            ("dois-niveis", "nivel3", "Dois níveis: o 3"), ("nivel", "espolio", "Espólio (sem mudança)"),
            ("raridades", "comum", "Comum"), ("raridades", "magico", "Mágico"),
            ("raridades", "raro", "Raro"), ("raridades", "lendario", "Lendário")]
INSTANTES = ["0060", "0250", "0500", "0900", "1600"]
FUNDO, TINTA, APAGADO = (14, 13, 12), (232, 220, 190), (150, 140, 120)
try:
    FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
except OSError:
    FONTE = ImageFont.load_default()


def recorte(pasta, sit, foto, ms, caixa=None):
    arq = CAP / pasta / f"{sit}-{foto}-{ms}.png"
    if not arq.exists():
        return None
    im = Image.open(arq).convert("RGB")
    w, h = im.size
    caixa = caixa or (w // 2 - 420, 120, w // 2 + 420, h - 120)  # o modal e um pouco em volta
    return im.crop(caixa)


def folha(linhas, saida):
    """linhas: [(rótulo, [imagem ou None, ...])]; cada linha com as imagens lado a lado."""
    gap, topo = 12, 30
    larg = max(sum((i.width if i else 300) + gap for i in ims) for _, ims in linhas) + gap
    alt = sum(topo + max((i.height if i else 40) for i in ims) + gap for _, ims in linhas) + gap
    f = Image.new("RGB", (larg, alt), FUNDO)
    d = ImageDraw.Draw(f)
    y = gap
    for rotulo, ims in linhas:
        d.text((gap, y + 4), rotulo, fill=TINTA, font=FONTE)
        y += topo
        x = gap
        for i in ims:
            if i:
                f.paste(i, (x, y))
            else:
                d.text((x, y + 10), "(sem captura nesta condição)", fill=APAGADO, font=FONTE)
            x += (i.width if i else 300) + gap
        y += max((i.height if i else 40) for i in ims) + gap
    f.save(saida, optimize=True)
    print(saida, f.size)


def main():
    folha([(f"{rot}: atual | proposta (1×, 900 ms)",
            [recorte("atual", s, foto, "0900"), recorte("proposta", s, foto, "0900")]) for s, foto, rot in MOMENTOS],
          CAP / "folha-estados.png")
    linhas = []
    for s, foto, rot in MOMENTOS:
        for lado in ("atual", "proposta"):
            ims = [recorte(lado, s, foto, ms) for ms in INSTANTES]
            ims = [i.resize((i.width * 2 // 5, i.height * 2 // 5), Image.LANCZOS) if i else None for i in ims]
            linhas.append((f"{rot}, {lado}: 60 · 250 · 500 · 900 · 1600 ms (reduzida a 40%)", ims))
    folha(linhas, CAP / "folha-ritmo.png")
    apertados = []
    for s, foto, rot in MOMENTOS:
        um = [recorte(p, s, foto, "0900", (240, 60, 1040, 660)) for p in ("atual-1280", "proposta-1280")]
        red = [recorte(p, s, foto, "0900") for p in ("atual-reduzido", "proposta-reduzido")]
        red = [i.resize((i.width * 3 // 4, i.height * 3 // 4), Image.LANCZOS) if i else None for i in red]
        apertados.append((f"{rot}: 1280×720 atual | proposta (1×) · movimento reduzido atual | proposta (75%)", um + red))
    folha(apertados, CAP / "folha-apertados.png")


if __name__ == "__main__":
    main()
