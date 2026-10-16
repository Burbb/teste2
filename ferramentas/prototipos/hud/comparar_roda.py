"""Monta as comparações da roda de ações a partir das fotos de fotografar_roda.mjs (capturas-roda/): para cada janela e
estado, o atual à esquerda e a alternativa à direita, em tamanho real (comparacao-<janela>-<estado>.png); e uma prancha
por janela com todos os estados empilhados (prancha-<janela>.png), também em tamanho real.

    python ferramentas/prototipos/hud/comparar_roda.py
"""

import pathlib

from PIL import Image, ImageDraw

FOTOS = pathlib.Path(__file__).resolve().parent / "capturas-roda"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)


def par(estado, jan):
    a, b = FOTOS / f"{jan}-atual-{estado}.png", FOTOS / f"{jan}-alternativa-{estado}.png"
    if not (a.exists() and b.exists()):
        return None
    ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    img = Image.new("RGB", (ia.width + ib.width + 36, max(ia.height, ib.height) + 30), FUNDO)
    img.paste(ia, (12, 24))
    img.paste(ib, (ia.width + 24, 24))
    d = ImageDraw.Draw(img)
    d.text((12, 6), f"{jan} · {estado} · atual", fill=TEXTO)
    d.text((ia.width + 24, 6), "alternativa", fill=TEXTO)
    return img


def main():
    estados = sorted({p.stem.split("-atual-")[1] for p in FOTOS.glob("*-atual-*.png")})
    for jan in ("normal", "baixa"):
        pares = []
        for e in estados:
            img = par(e, jan)
            if img:
                img.save(FOTOS / f"comparacao-{jan}-{e}.png")
                if not e.startswith("tela"):
                    pares.append(img)
        w = max(i.width for i in pares)
        prancha = Image.new("RGB", (w, sum(i.height for i in pares)), FUNDO)
        y = 0
        for i in pares:
            prancha.paste(i, (0, y))
            y += i.height
        prancha.save(FOTOS / f"prancha-{jan}.png")
    print(f"{len(estados)} estados em {FOTOS}")


if __name__ == "__main__":
    main()
