"""Monta as pranchas da proposta da varinha desenhada no Aseprite pelo MCP (varinha-aseprite/), a partir dos arquivos e
das fotos de fotografar_varinha.mjs (varinha-aseprite/capturas/jogo/):
  - carvao-tamanhos.png: o 32 e o 64 em 1× num nicho de item sobre o carvão da HUD, com a ampliação ao lado
    (ferramentas/arte/prancha.py);
  - familia.png: a varinha ao lado do cajado, do orbe, do grimório e do escudo aprovados, em 32 e em 64, em 1× sobre o
    carvão (e a mesma fila ampliada 3× embaixo, só para achar o pixel);
  - comparacao-<janela>-<lugar>.png: o atual à esquerda e a proposta à direita, em tamanho real (a ficha e o mercado em
    32, a dica com a comparação, o cartão do saque em 64);
  - prancha-zoom.png: os espaços no jogo (ficha, venda, saque em 48 e 64) ampliados 3× sem suavizar, atual em cima e
    proposta embaixo, nas duas janelas.

    python ferramentas/prototipos/hud/comparar_varinha.py
"""

import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
PROPOSTA = AQUI / "varinha-aseprite"
FOTOS = PROPOSTA / "capturas" / "jogo"
SAIDA = PROPOSTA / "capturas"
ICONES = RAIZ / "rpg" / "web" / "static" / "hud" / "icones"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
NICHO, ARESTA = (10, 11, 13), (58, 61, 67)

sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))
from prancha import carvao  # noqa: E402


def lado_a_lado(a, b, titulo):
    ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    img = Image.new("RGB", (ia.width + ib.width + 36, max(ia.height, ib.height) + 30), FUNDO)
    img.paste(ia, (12, 24))
    img.paste(ib, (ia.width + 24, 24))
    d = ImageDraw.Draw(img)
    d.text((12, 6), f"{titulo}: atual (sprite 16x16)", fill=TEXTO)
    d.text((ia.width + 24, 6), "proposta (Aseprite)", fill=TEXTO)
    return img


def familia():
    pecas = [("varinha", PROPOSTA), ("cajado", ICONES), ("orbe", ICONES), ("livro", ICONES), ("escudo", ICONES)]
    nomes = {"varinha": "varinha (proposta)", "cajado": "cajado", "orbe": "orbe", "livro": "livro (grimorio)", "escudo": "escudo"}
    col, z = 150, 3
    alt = [10 + 32 + 24 + 34, 64 + 24 + 34, 32 * z + 30, 64 * z + 30]
    img = carvao(col * len(pecas) + 20, sum(alt) + 20)
    d = ImageDraw.Draw(img)
    y = 10
    for lado, ampliar in ((32, False), (64, False), (32, True), (64, True)):
        for k, (nome, pasta) in enumerate(pecas):
            i = Image.open(pasta / f"{nome}-{lado}.png").convert("RGBA")
            x = 10 + k * col
            if ampliar:
                i = i.resize((lado * z, lado * z), Image.NEAREST)
                img.alpha_composite(i, (x + (col - i.width) // 2, y))
            else:
                n = lado + 24
                d.rectangle((x + (col - n) // 2, y, x + (col - n) // 2 + n - 1, y + n - 1), fill=NICHO, outline=ARESTA)
                img.alpha_composite(i, (x + (col - lado) // 2, y + 12))
                d.text((x + 6, y + n + 6), f"{nomes[nome]} {lado}", fill=TEXTO)
        y += {32: alt[0], 64: alt[1]}[lado] if not ampliar else (lado * z + 30)
    img.convert("RGB").save(SAIDA / "familia.png")


def prancha_zoom(z=3):
    linhas = []
    for jan in ("normal", "baixa"):
        for versao in ("atual", "proposta"):
            ims = [(n, FOTOS / f"zoom-{jan}-{versao}-{n}.png") for n in ("ficha-arma", "vender", "saque-48", "saque-64")]
            ims = [(n, Image.open(p).convert("RGB")) for n, p in ims if p.exists()]
            linhas.append((f"{jan} · {versao}", [(n, i.resize((i.width * z, i.height * z), Image.NEAREST)) for n, i in ims]))
    larg = max(sum(i.width + 16 for _, i in ims) for _, ims in linhas) + 24
    alts = [max(i.height for _, i in ims) + 40 for _, ims in linhas]
    img = Image.new("RGB", (larg, sum(alts) + 10), FUNDO)
    d = ImageDraw.Draw(img)
    y = 10
    for (titulo, ims), a in zip(linhas, alts):
        d.text((12, y), titulo, fill=TEXTO)
        x = 12
        for n, i in ims:
            img.paste(i, (x, y + 16))
            d.text((x, y + 20 + i.height), n, fill=TEXTO)
            x += i.width + 16
        y += a
    img.save(SAIDA / "prancha-zoom.png")


def main():
    subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "arte" / "prancha.py"), str(PROPOSTA / "varinha-32.png"),
                    str(PROPOSTA / "varinha-64.png"), "-o", str(SAIDA / "carvao-tamanhos.png"), "--zoom", "6"], check=True)
    familia()
    for jan in ("normal", "baixa"):
        for lugar in ("ficha", "mercado-vender", "mercado-dica", "saque-cartao", "tela-mercado", "tela-saque"):
            a, b = FOTOS / f"{jan}-atual-{lugar}.png", FOTOS / f"{jan}-proposta-{lugar}.png"
            if a.exists() and b.exists():
                lado_a_lado(a, b, f"{jan} · {lugar}").save(SAIDA / f"comparacao-{jan}-{lugar}.png")
    prancha_zoom()
    print("\n".join(sorted(p.name for p in SAIDA.glob("*.png"))))


if __name__ == "__main__":
    main()
