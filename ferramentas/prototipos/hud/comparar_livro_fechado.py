"""Monta as comparações do grimório fechado (fotografar_livro_fechado.mjs, capturas-livro-fechado/), em tamanho real,
uma por par: "antes-depois" (o 64 aprovado como direção, livro-fechado-ref/, e a revisão de acabamento,
livro-fechado-acabamento/) e "emblema" (a revisão de acabamento e o mesmo corpo com o emblema corrigido,
livro-fechado-emblema/):
  - <par>-<janela>-saque-cartao.png: o cartão do saque com um e com o outro, lado a lado;
  - <par>-zoom.png: os dois arquivos em 1× sobre o carvão da HUD, com a ampliação 8× sem suavizar;
  - <par>-vizinhos.png: os dois ao lado do escudo, do cajado e do orbe aprovados, em 1× e 4×.

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
PASTAS = {"fechado": "livro-fechado-ref", "acabamento": "livro-fechado-acabamento", "emblema": "livro-fechado-emblema"}
PARES = {"antes-depois": (("fechado", "antes (o 64 aprovado como direção)"), ("acabamento", "depois (a revisão de acabamento)")),
         "emblema": (("acabamento", "a revisão de acabamento"), ("emblema", "o mesmo corpo, com o emblema corrigido"))}


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
    prancha = [sys.executable, str(RAIZ / "ferramentas/arte/prancha.py")]
    icones = RAIZ / "rpg/web/static/hud/icones"
    for par, versoes in PARES.items():
        for jan in ("normal", "baixa"):
            lado_a_lado([(FOTOS / f"{jan}-{v}-saque-cartao.png", r) for v, r in versoes],
                        f"{jan} · cartão do saque").save(FOTOS / f"{par}-{jan}-saque-cartao.png")
        a, b = (str(AQUI / PASTAS[v] / "livro-64.png") for v, _ in versoes)
        subprocess.run(prancha + [a, b, "-o", str(FOTOS / f"{par}-zoom.png"), "--zoom", "8"], check=True)
        subprocess.run(prancha + [a, b, *[str(icones / f"{n}-64.png") for n in ("escudo", "cajado", "orbe")],
                                  "-o", str(FOTOS / f"{par}-vizinhos.png"), "--zoom", "4"], check=True)
    print(f"comparações em {FOTOS}")


if __name__ == "__main__":
    main()
