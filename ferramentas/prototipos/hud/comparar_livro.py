"""Monta as comparações do livro (fotografar_livro.mjs, capturas-livro/): o jogo de hoje, o candidato fechado, o
grimório entreaberto, o grimório aberto de duas páginas e o grimório de estudo (a pose do entreaberto pela referência
do Jean), em tamanho real:
  - comparacao-<janela>-livro-<lugar>.png: as versões lado a lado;
  - par-<janela>-<lugar>.png: só o entreaberto e o de estudo (a pose e a revisão dela);
  - prancha-zoom.png: os espaços no jogo (a ficha, a venda, o corpo, a mochila, o saque em 48 e 64) ampliados 3× sem
    suavizar, para achar o pixel (julgue pelo tamanho real);
  - prancha-arquivos.png: os arquivos dos candidatos em 1× sobre o carvão, com os vizinhos aprovados (o orbe, o
    cajado, o escudo, o machado).

    python ferramentas/prototipos/hud/comparar_livro.py
"""

import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = AQUI / "capturas-livro"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
try:  # uma fonte com acentos (a de bitmap do Pillow não tem o "ó")
    FONTE = ImageFont.truetype("DejaVuSans.ttf", 12)
except OSError:
    FONTE = ImageFont.load_default(size=12)
VERSOES = (("atual", "o jogo hoje"), ("fechado", "candidato fechado"), ("entreaberto", "grimório entreaberto"),
           ("aberto", "grimório aberto"), ("estudo", "grimório de estudo"))
ZOOM = ["ficha-arma", "vender", "corpo", "mochila", "saque-48", "saque-64"]


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
    linhas = [ln for ln in linhas if ln[1]]
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


def main():
    feitas = 0
    for atual in sorted(FOTOS.glob("*-atual-livro-*.png")):
        if atual.name.startswith("zoom-"):
            continue
        jan, resto = atual.stem.split("-atual-livro-")
        versoes = [(FOTOS / f"{jan}-{v}-livro-{resto}.png", r) for v, r in VERSOES]
        if all(p.exists() for p, _ in versoes):
            lado_a_lado(versoes, f"{jan} · {resto}").save(FOTOS / f"comparacao-{jan}-livro-{resto}.png")
            feitas += 1
    for jan in ("normal", "baixa"):  # os pares: o entreaberto (o preferido do Jean) e o de estudo
        for lugar in ("inventario", "saque-cartao", "tela-mercado", "ficha", "mercado-dica"):
            par = [(FOTOS / f"{jan}-{v}-livro-{lugar}.png", r) for v, r in (("entreaberto", "entreaberto"), ("estudo", "grimório de estudo"))]
            if all(p.exists() for p, _ in par):
                lado_a_lado(par, f"{jan} · {lugar}").save(FOTOS / f"par-{jan}-{lugar}.png")
    prancha_zoom()
    icones = RAIZ / "rpg/web/static/hud/icones"
    subprocess.run([sys.executable, str(RAIZ / "ferramentas/arte/prancha.py"),
                    *[str(AQUI / "orbe-livro-pixel" / f"livro-{l}.png") for l in (32, 40, 48, 64)],
                    *[str(AQUI / "livro-entreaberto" / f"livro-{l}.png") for l in (32, 40, 48, 64)],
                    *[str(AQUI / "livro-aberto" / f"livro-{l}.png") for l in (32, 40, 48, 64)],
                    *[str(AQUI / "livro-estudo" / f"livro-{l}.png") for l in (32, 40, 48, 64)],
                    str(icones / "orbe-32.png"), str(icones / "cajado-32.png"), str(icones / "escudo-32.png"),
                    str(icones / "machado-32.png"), str(icones / "orbe-64.png"),
                    "-o", str(FOTOS / "prancha-arquivos.png"), "--zoom", "6"], check=True)
    print(f"{feitas} comparações, prancha-zoom.png e prancha-arquivos.png em {FOTOS}")


if __name__ == "__main__":
    main()
