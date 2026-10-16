"""Monta as comparações do grimório fechado nos quatro tamanhos (fotografar_livro.mjs com
SAIDA=ferramentas/prototipos/hud/capturas-livro-tamanhos VERSOES=atual,tamanhos), em tamanho real:
  - comparacao-<janela>-<lugar>.png: o jogo de hoje (o sprite 16×16) e o grimório, lado a lado, em cada lugar;
  - prancha-zoom.png: os espaços no jogo (a ficha, a venda, o corpo, a mochila, o saque em 48 e 64) ampliados 3× sem
    suavizar, nas duas janelas (julgue pelo tamanho real);
  - prancha-tamanhos.png: os quatro arquivos em 1× sobre o carvão da HUD, com a ampliação 6×;
  - prancha-vizinhos.png: uma linha por tamanho, o livro ao lado do escudo, do cajado e do orbe aprovados, em 1× sobre
    o carvão e ampliados 3× sem suavizar.

    python ferramentas/prototipos/hud/comparar_livro_tamanhos.py
"""

import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = AQUI / "capturas-livro-tamanhos"
PASTA = AQUI / "livro-fechado-tamanhos"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
try:  # uma fonte com acentos (a de bitmap do Pillow não tem o "ó")
    FONTE = ImageFont.truetype("DejaVuSans.ttf", 12)
except OSError:
    FONTE = ImageFont.load_default(size=12)
VERSOES = (("atual", "o jogo hoje"), ("tamanhos", "grimório fechado"))
LUGARES = ("ficha", "inventario", "mercado-vender", "mercado-dica", "saque-cartao", "saque-voo", "tela-mercado",
           "tela-inventario", "tela-saque")
ZOOM = ("ficha-arma", "vender", "corpo", "mochila", "saque-48", "saque-64")


def lado_a_lado(imagens, titulo):
    ims = [(Image.open(p).convert("RGB"), r) for p, r in imagens]
    img = Image.new("RGB", (sum(i.width for i, _ in ims) + 12 * (len(ims) + 1), max(i.height for i, _ in ims) + 30), FUNDO)
    d, x = ImageDraw.Draw(img), 12
    for i, r in ims:
        img.paste(i, (x, 24))
        d.text((x, 6), f"{titulo}: {r}" if x == 12 else r, fill=TEXTO, font=FONTE)
        x += i.width + 12
    return img


def prancha_zoom(z=3):
    linhas = []
    for jan in ("normal", "baixa"):
        for versao, rotulo in VERSOES:
            ims = [(n, FOTOS / f"zoom-{jan}-{versao}-livro-{n}.png") for n in ZOOM]
            linhas.append((f"{jan} · {rotulo}", [(n, Image.open(p).convert("RGB")) for n, p in ims if p.exists()]))
    larg = max(sum(i.width * z + 14 for _, i in ims) for _, ims in linhas) + 190
    alt = sum(max(i.height for _, i in ims) * z + 30 for _, ims in linhas) + 10
    img = Image.new("RGB", (larg, alt), FUNDO)
    d, y = ImageDraw.Draw(img), 10
    for rotulo, ims in linhas:
        d.text((10, y + 12), rotulo, fill=TEXTO, font=FONTE)
        x = 190
        for n, i in ims:
            img.paste(i.resize((i.width * z, i.height * z), Image.NEAREST), (x, y + 16))
            d.text((x, y), n, fill=TEXTO, font=FONTE)
            x += i.width * z + 14
        y += max(i.height for _, i in ims) * z + 30
    img.save(FOTOS / "prancha-zoom.png")


def vizinhos(z=3):
    icones = RAIZ / "rpg/web/static/hud/icones"
    pecas = [("livro", PASTA), ("escudo", icones), ("cajado", icones), ("orbe", icones)]
    linhas = [(lado, [Image.open(pasta / f"{n}-{lado}.png").convert("RGBA") for n, pasta in pecas]) for lado in (32, 40, 48, 64)]
    larg = 70 + 4 * (64 + 12) + 4 * (64 * z + 12)
    img = Image.new("RGB", (larg, sum(64 * z + 30 for _ in linhas) + 10), FUNDO)
    d, y = ImageDraw.Draw(img), 10
    for lado, ims in linhas:
        d.text((10, y + 4), f"{lado} px", fill=TEXTO, font=FONTE)
        x = 70
        for (nome, _), im in zip(pecas, ims):                   # em 1×, num nicho de 64 sobre o carvão
            img.paste((10, 11, 13), (x, y + 18, x + 64, y + 18 + 64))
            img.paste(im, (x + (64 - lado) // 2, y + 18 + (64 - lado) // 2), im)
            x += 64 + 12
        for (nome, _), im in zip(pecas, ims):                   # ampliados, sem suavizar
            g = im.resize((lado * z, lado * z), Image.NEAREST)
            img.paste(g, (x, y + 18), g)
            d.text((x, y + 4), nome, fill=TEXTO, font=FONTE)
            x += 64 * z + 12
        y += 64 * z + 30
    img.save(FOTOS / "prancha-vizinhos.png")


def main():
    for jan in ("normal", "baixa"):
        for lugar in LUGARES:
            par = [(FOTOS / f"{jan}-{v}-livro-{lugar}.png", r) for v, r in VERSOES]
            if all(p.exists() for p, _ in par):
                lado_a_lado(par, f"{jan} · {lugar}").save(FOTOS / f"comparacao-{jan}-{lugar}.png")
    prancha_zoom()
    prancha = [sys.executable, str(RAIZ / "ferramentas/arte/prancha.py")]
    livros = [str(PASTA / f"livro-{l}.png") for l in (32, 40, 48, 64)]
    subprocess.run(prancha + livros + ["-o", str(FOTOS / "prancha-tamanhos.png"), "--zoom", "6"], check=True)
    vizinhos()
    print(f"comparações em {FOTOS}")


if __name__ == "__main__":
    main()
