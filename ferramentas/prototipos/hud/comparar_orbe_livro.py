"""Monta as comparações da proposta do orbe e do livro a partir de fotografar_orbe_livro.mjs (capturas-orbe-livro/):
  - comparacao-<janela>-<classe>-<lugar>.png: o atual à esquerda e a proposta à direita, em tamanho real;
  - prancha-zoom.png: os espaços no jogo (a ficha, a venda, o corpo, a mochila, o saque em 48 e 64) ampliados 3× sem
    suavizar, atual em cima e proposta embaixo, nas duas janelas, para achar o pixel (julgue pelo tamanho real);
  - prancha-arquivos.png: os arquivos da proposta em 1× sobre o carvão, com os vizinhos aprovados (escudo, machado,
    cajado, unguento, arco).

    python ferramentas/prototipos/hud/comparar_orbe_livro.py
"""

import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = AQUI / "capturas-orbe-livro"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
ZOOM = ["ficha-arma", "vender", "corpo", "mochila", "saque-48", "saque-64"]


def lado_a_lado(a, b, titulo):
    ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    img = Image.new("RGB", (ia.width + ib.width + 36, max(ia.height, ib.height) + 30), FUNDO)
    img.paste(ia, (12, 24))
    img.paste(ib, (ia.width + 24, 24))
    d = ImageDraw.Draw(img)
    d.text((12, 6), f"{titulo}: atual", fill=TEXTO)
    d.text((ia.width + 24, 6), "proposta", fill=TEXTO)
    return img


def prancha_zoom(z=3):
    linhas = []
    for classe in ("orbe", "livro"):
        for jan in ("normal", "baixa"):
            for versao in ("atual", "proposta"):
                ims = [(n, FOTOS / f"zoom-{jan}-{versao}-{classe}-{n}.png") for n in ZOOM]
                linhas.append((f"{classe} · {jan} · {versao}", [(n, Image.open(p).convert("RGB")) for n, p in ims if p.exists()]))
    larg = max(sum(i.width * z + 14 for _, i in ims) for _, ims in linhas) + 170
    alt = sum(max(i.height for _, i in ims) * z + 30 for _, ims in linhas) + 10
    img = Image.new("RGB", (larg, alt), FUNDO)
    d, y = ImageDraw.Draw(img), 10
    for rotulo, ims in linhas:
        d.text((10, y + 12), rotulo, fill=TEXTO)
        x = 170
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
        jan, resto = atual.stem.split("-atual-")
        proposta = FOTOS / f"{jan}-proposta-{resto}.png"
        if proposta.exists():
            lado_a_lado(atual, proposta, f"{jan} · {resto}").save(FOTOS / f"comparacao-{jan}-{resto}.png")
            feitas += 1
    prancha_zoom()
    icones, proposta = RAIZ / "rpg/web/static/hud/icones", AQUI / "orbe-livro-pixel"
    subprocess.run([sys.executable, str(RAIZ / "ferramentas/arte/prancha.py"),
                    *[str(proposta / f"orbe-{l}.png") for l in (32, 40, 48, 64)],
                    *[str(proposta / f"livro-{l}.png") for l in (32, 40, 48, 64)],
                    str(icones / "escudo-32.png"), str(icones / "machado-32.png"), str(icones / "cajado-32.png"),
                    str(icones / "unguento-32.png"), str(icones / "arco-32.png"), str(icones / "escudo-64.png"),
                    "-o", str(FOTOS / "prancha-arquivos.png"), "--zoom", "6"], check=True)
    print(f"{feitas} comparações, prancha-zoom.png e prancha-arquivos.png em {FOTOS}")


if __name__ == "__main__":
    main()
