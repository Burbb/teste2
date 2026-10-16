"""Monta o antes × depois do grimório fechado (fotografar_livro_fechado.mjs, capturas-livro-fechado/): o 64 aprovado
como direção (livro-fechado-ref/) e a revisão de acabamento (livro-fechado-acabamento/), em tamanho real:
  - antes-depois-<janela>-saque-cartao.png: o cartão do saque com um e com o outro, lado a lado;
  - antes-depois-zoom.png: os dois arquivos em 1× sobre o carvão da HUD, com a ampliação 8× sem suavizar;
  - antes-depois-vizinhos.png: os dois ao lado do escudo, do cajado e do orbe aprovados, em 1× e 4×.

    python ferramentas/prototipos/hud/comparar_livro_fechado.py
"""

import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = AQUI / "capturas-livro-fechado"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
try:  # uma fonte com acentos (a de bitmap do Pillow não tem o "ó")
    FONTE = ImageFont.truetype("DejaVuSans.ttf", 12)
except OSError:
    FONTE = ImageFont.load_default(size=12)
VERSOES = (("fechado", "antes (o 64 aprovado como direção)"), ("acabamento", "depois (a revisão de acabamento)"))


def lado_a_lado(imagens, titulo):
    ims = [(Image.open(p).convert("RGB"), r) for p, r in imagens]
    img = Image.new("RGB", (sum(i.width for i, _ in ims) + 12 * (len(ims) + 1), max(i.height for i, _ in ims) + 30), FUNDO)
    d, x = ImageDraw.Draw(img), 12
    for i, r in ims:
        img.paste(i, (x, 24))
        d.text((x, 6), f"{titulo}: {r}" if x == 12 else r, fill=TEXTO, font=FONTE)
        x += i.width + 12
    return img


def main():
    for jan in ("normal", "baixa"):
        lado_a_lado([(FOTOS / f"{jan}-{v}-saque-cartao.png", r) for v, r in VERSOES],
                    f"{jan} · cartão do saque").save(FOTOS / f"antes-depois-{jan}-saque-cartao.png")
    antes, depois = AQUI / "livro-fechado-ref" / "livro-64.png", AQUI / "livro-fechado-acabamento" / "livro-64.png"
    prancha = [sys.executable, str(RAIZ / "ferramentas/arte/prancha.py")]
    subprocess.run(prancha + [str(antes), str(depois), "-o", str(FOTOS / "antes-depois-zoom.png"), "--zoom", "8"], check=True)
    icones = RAIZ / "rpg/web/static/hud/icones"
    subprocess.run(prancha + [str(antes), str(depois), *[str(icones / f"{n}-64.png") for n in ("escudo", "cajado", "orbe")],
                              "-o", str(FOTOS / "antes-depois-vizinhos.png"), "--zoom", "4"], check=True)
    print(f"antes × depois em {FOTOS}")


if __name__ == "__main__":
    main()
