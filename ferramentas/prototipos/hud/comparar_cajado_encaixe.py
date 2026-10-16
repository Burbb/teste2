"""Antes × depois do encaixe do cristal no cajado (o retorno do Jean: "a base azul do cristal parece ultrapassar o
alojamento de madeira"). Antes: arco-cajado-pixel/ (a proposta de 16/10); depois: cajado-encaixe/. Monta, em
capturas-cajado-encaixe/:
  - prancha-arquivos.png: os arquivos em 1× sobre o carvão com a ampliação (prancha.py), antes e depois por tamanho,
    32 e 40 primeiro;
  - prancha-jogo.png: os espaços no jogo (a ficha, a venda, o corpo, a mochila, o saque em 48 e 64), antes em cima e
    depois embaixo, ampliados 3× (julgue pelo tamanho real: as fotos inteiras estão na mesma pasta).

    python ferramentas/prototipos/hud/comparar_cajado_encaixe.py
"""

import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
ANTES, DEPOIS = AQUI / "arco-cajado-pixel", AQUI / "cajado-encaixe"
FOTOS_ANTES, FOTOS = AQUI / "capturas-arco-cajado", AQUI / "capturas-cajado-encaixe"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
ZOOM = ["ficha-arma", "vender", "corpo", "mochila", "saque-48", "saque-64"]


def main():
    arquivos = [str(p / f"cajado-{l}.png") for l in (32, 40, 48, 64) for p in (ANTES, DEPOIS)]
    subprocess.run([sys.executable, str(RAIZ / "ferramentas/arte/prancha.py"), *arquivos, "-o",
                    str(FOTOS / "prancha-arquivos.png"), "--zoom", "8"], check=True)
    z, linhas = 3, []
    for jan in ("normal", "baixa"):
        for rot, pasta in (("antes", FOTOS_ANTES), ("depois", FOTOS)):
            ims = [(n, pasta / f"zoom-{jan}-proposta-mago-{n}.png") for n in ZOOM]
            linhas.append((f"{jan} · {rot}", [(n, Image.open(p).convert("RGB")) for n, p in ims if p.exists()]))
    larg = max(sum(i.width * z + 14 for _, i in ims) for _, ims in linhas) + 140
    alt = sum(max(i.height for _, i in ims) * z + 30 for _, ims in linhas) + 10
    img = Image.new("RGB", (larg, alt), FUNDO)
    d, y = ImageDraw.Draw(img), 10
    for rotulo, ims in linhas:
        d.text((10, y + 12), rotulo, fill=TEXTO)
        x = 140
        for n, i in ims:
            img.paste(i.resize((i.width * z, i.height * z), Image.NEAREST), (x, y + 16))
            d.text((x, y), n, fill=TEXTO)
            x += i.width * z + 14
        y += max(i.height for _, i in ims) * z + 30
    img.save(FOTOS / "prancha-jogo.png")
    print(f"prancha-arquivos.png e prancha-jogo.png em {FOTOS}")


if __name__ == "__main__":
    main()
