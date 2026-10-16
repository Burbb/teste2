"""Monta as comparações da proposta do machado e da Bomba de Fumaça a partir das fotos de fotografar_machado_bomba.mjs
(capturas-machado-bomba/):
  - comparacao-<janela>-<lugar>.png: o atual à esquerda e a proposta à direita, em tamanho real (sem escala);
  - prancha-zoom.png: os recortes pequenos de cada espaço no jogo (o corpo, a mochila, a bolsa, a prateleira, a
    janelinha da luta, o baú, o saque, a lixeira) ampliados 4× sem suavizar, atual em cima e proposta embaixo, nas
    duas janelas, para achar o pixel;
  - prancha-arquivos.png: os arquivos da proposta em 1× sobre o carvão, com o atual e os vizinhos aprovados
    (ferramentas/arte/prancha.py).

    python ferramentas/prototipos/hud/comparar_machado_bomba.py
"""

import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = AQUI / "capturas-machado-bomba"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
ZOOM = ["corpo-machado", "mochila-machado", "vender-machado", "saque-48", "saque-64", "bolsa-bomba",
        "prateleira-bomba", "luta-bomba", "bau-bomba", "lixeira"]


def lado_a_lado(a, b, titulo):
    ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    w, h = ia.width + ib.width + 36, max(ia.height, ib.height) + 34
    img = Image.new("RGB", (w, h), FUNDO)
    img.paste(ia, (12, 28))
    img.paste(ib, (ia.width + 24, 28))
    d = ImageDraw.Draw(img)
    d.text((12, 8), f"{titulo}: atual", fill=TEXTO)
    d.text((ia.width + 24, 8), "proposta", fill=TEXTO)
    return img


def prancha_zoom(z=4):
    linhas = []
    for jan in ("normal", "baixa"):
        for versao in ("atual", "proposta"):
            ims = [(n, FOTOS / f"zoom-{jan}-{versao}-{n}.png") for n in ZOOM]
            linhas.append((f"{jan} · {versao}", [(n, Image.open(p).convert("RGB")) for n, p in ims if p.exists()]))
    larg = max(sum(i.width * z + 14 for _, i in ims) for _, ims in linhas) + 130
    alt = sum(max(i.height for _, i in ims) * z + 30 for _, ims in linhas) + 10
    img = Image.new("RGB", (larg, alt), FUNDO)
    d = ImageDraw.Draw(img)
    y = 10
    for rotulo, ims in linhas:
        d.text((10, y + 12), rotulo, fill=TEXTO)
        x = 130
        for n, i in ims:
            img.paste(i.resize((i.width * z, i.height * z), Image.NEAREST), (x, y + 16))
            d.text((x, y), n, fill=TEXTO)
            x += i.width * z + 14
        y += max(i.height for _, i in ims) * z + 30
    img.save(FOTOS / "prancha-zoom.png")


def main():
    feitas = 0
    for atual in sorted(FOTOS.glob("*-atual-*.png")):
        if atual.name.startswith("zoom-"):
            continue
        jan, lugar = atual.stem.split("-atual-")
        proposta = FOTOS / f"{jan}-proposta-{lugar}.png"
        if proposta.exists():
            lado_a_lado(atual, proposta, f"{jan} · {lugar}").save(FOTOS / f"comparacao-{jan}-{lugar}.png")
            feitas += 1
    prancha_zoom()
    icones, proposta = RAIZ / "rpg/web/static/hud/icones", AQUI / "machado-bomba-pixel"
    subprocess.run([sys.executable, str(RAIZ / "ferramentas/arte/prancha.py"),
                    *[str(proposta / f"machado-{l}.png") for l in (32, 40, 48, 64)], str(icones / "espada-32.png"),
                    str(icones / "maca-32.png"), str(icones / "escudo-40.png"), str(proposta / "bomba-32.png"),
                    str(icones / "unguento-32.png"), str(icones / "pocao-32.png"), "-o", str(FOTOS / "prancha-arquivos.png"),
                    "--zoom", "6"], check=True)
    print(f"{feitas} comparações, prancha-zoom.png e prancha-arquivos.png em {FOTOS}")


if __name__ == "__main__":
    main()
