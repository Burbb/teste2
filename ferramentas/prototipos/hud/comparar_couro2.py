"""Monta as pranchas da rodada 1 do capuz e da luva com braçadeira de couro (couro2-aseprite/), a partir dos arquivos e
das fotos de fotografar_couro2.mjs (couro2-aseprite/capturas/jogo/), em couro2-aseprite/capturas/:
  - comparacao-<janela>-<peça>-<lugar>.png: o atual à esquerda e o candidato à direita, em tamanho real (a ficha e o
    mercado em 32, a dica, o cartão do saque com o 64 derivado, as telas inteiras);
  - prancha-zoom.png: os espaços no jogo ampliados 3× sem suavizar, só para achar o pixel;
  - carvao-32.png, carvao-64.png: os candidatos em 1× sobre o carvão, ao lado do gibão, das botas e dos aprovados;
  - silhueta.png: os dois numa cor só.

    python ferramentas/prototipos/hud/comparar_couro2.py
"""

import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from comparar_varinha import em_colunas  # noqa: E402

PROPOSTA = AQUI / "couro2-aseprite"
R1, FOTOS, SAIDA = PROPOSTA / "rodada1", PROPOSTA / "capturas" / "jogo", PROPOSTA / "capturas"
LUGARES = ("ficha", "mercado-vender", "mercado-dica", "saque-cartao", "tela-mercado", "tela-saque")
ICONES = AQUI.parents[2] / "rpg" / "web" / "static" / "hud" / "icones"
AUX = AQUI / "couro-aseprite" / "auxiliares"


def main():
    feitas = []
    for jan in ("normal", "baixa"):
        for peca in ("capuz", "luva"):
            for lugar in LUGARES:
                fotos = [FOTOS / f"{jan}-{v}-{peca}-{lugar}.png" for v in ("atual", "proposta")]
                if all(f.exists() for f in fotos):
                    nome = SAIDA / f"comparacao-{jan}-{peca}-{lugar}.png"
                    em_colunas(fotos, [f"{jan} · {peca} · {lugar}: atual (sprite 16x16)",
                                       "candidato (rodada 1; o 64 é o 32 ampliado 2x)"]).save(nome)
                    feitas.append(nome.name)
    _zoom_pecas(("capuz", "luva"))
    py = sys.executable
    for n in (32, 64):
        atual = PROPOSTA / "atual"
        pares = [f"capuz atual={atual / f'capuz-sprite-{n}.png'}", f"capuz={R1 / f'capuz-{n}.png'}",
                 f"luva atual={atual / f'luva-sprite-{n}.png'}", f"luva={R1 / f'luva-{n}.png'}"]
        pares += [f"{r}={ICONES / f'{r}-{n}.png'}" for r in ("gibao", "bota", "elmo", "manopla", "escudo", "varinha")]
        subprocess.run([py, str(AUX / "fila.py"), str(SAIDA / f"carvao-{n}.png"), *pares], check=True)
    subprocess.run([py, str(AUX / "silhueta.py"), str(SAIDA / "silhueta.png"), str(R1 / "capuz-32.png"),
                    str(R1 / "luva-32.png"), str(ICONES / "gibao-32.png"), str(ICONES / "bota-32.png")], check=True)
    print("\n".join(feitas + ["prancha-zoom.png", "carvao-32.png", "carvao-64.png", "silhueta.png"]))


def _zoom_pecas(pecas, z=3):
    """A prancha ampliada dos espaços no jogo (ficha, venda, saque 64), atual e candidato, das duas janelas."""
    from PIL import Image, ImageDraw
    from comparar_varinha import FUNDO, TEXTO
    linhas = []
    for jan in ("normal", "baixa"):
        for peca in pecas:
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


if __name__ == "__main__":
    main()
