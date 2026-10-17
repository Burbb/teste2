"""Monta as pranchas da rodada 1 do peitoral e das botas de couro (couro-aseprite/), a partir dos arquivos e das fotos
de fotografar_couro.mjs (couro-aseprite/capturas/jogo/):
  - comparacao-<janela>-<peça>-<lugar>.png: o atual à esquerda e o candidato à direita, em tamanho real (a ficha e o
    mercado em 32, a dica com a comparação, o cartão do saque em 64, as telas inteiras);
  - prancha-zoom.png: os espaços no jogo (ficha, venda, saque 64) ampliados 3× sem suavizar, só para achar o pixel.
As pranchas sobre o carvão e a silhueta saem de couro-aseprite/auxiliares/fila.py e silhueta.py.

    python ferramentas/prototipos/hud/comparar_couro.py
"""

import pathlib
import sys

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from comparar_varinha import FUNDO, TEXTO, em_colunas  # noqa: E402

PROPOSTA = AQUI / "couro-aseprite"
FOTOS, SAIDA = PROPOSTA / "capturas" / "jogo", PROPOSTA / "capturas"
LUGARES = ("ficha", "mercado-vender", "mercado-dica", "saque-cartao", "tela-mercado", "tela-saque")


def prancha_zoom(z=3):
    linhas = []
    for jan in ("normal", "baixa"):
        for peca in ("gibao", "bota"):
            for versao in ("atual", "proposta"):
                ims = [(n, FOTOS / f"zoom-{jan}-{versao}-{peca}-{n}.png") for n in ("ficha", "vender", "saque-64")]
                ims = [(n, Image.open(p).convert("RGB")) for n, p in ims if p.exists()]
                linhas.append((f"{jan} · {peca} · {versao}", [(n, i.resize((i.width * z, i.height * z), Image.NEAREST))
                                                               for n, i in ims]))
    larg = max(sum(i.width + 16 for _, i in ims) for _, ims in linhas) + 24
    alts = [max(i.height for _, i in ims) + 40 for _, ims in linhas]
    img = Image.new("RGB", (larg, sum(alts) + 10), FUNDO)
    d, y = ImageDraw.Draw(img), 10
    for (titulo, ims), a in zip(linhas, alts):
        d.text((12, y), titulo, fill=TEXTO)
        x = 12
        for n, i in ims:
            img.paste(i, (x, y + 16)); d.text((x, y + 20 + i.height), n, fill=TEXTO); x += i.width + 16
        y += a
    img.save(SAIDA / "prancha-zoom.png")


def main():
    feitas = []
    for jan in ("normal", "baixa"):
        for peca in ("gibao", "bota"):
            for lugar in LUGARES:
                fotos = [FOTOS / f"{jan}-{v}-{peca}-{lugar}.png" for v in ("atual", "proposta")]
                if all(f.exists() for f in fotos):
                    nome = SAIDA / f"comparacao-{jan}-{peca}-{lugar}.png"
                    em_colunas(fotos, [f"{jan} · {peca} · {lugar}: atual (sprite 16x16)", "candidato (rodada 1)"]).save(nome)
                    feitas.append(nome.name)
    prancha_zoom()
    print("\n".join(feitas + ["prancha-zoom.png"]))


if __name__ == "__main__":
    main()
