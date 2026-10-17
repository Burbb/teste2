"""Monta as pranchas da rodada 1 do peitoral e das botas de couro (couro-aseprite/), a partir dos arquivos e das fotos
de fotografar_couro.mjs (couro-aseprite/capturas/jogo/):
  - comparacao-<janela>-<peça>-<lugar>.png: o atual à esquerda e o candidato à direita, em tamanho real (a ficha e o
    mercado em 32, a dica com a comparação, o cartão do saque em 64, as telas inteiras);
  - prancha-zoom.png: os espaços no jogo (ficha, venda, saque 64) ampliados 3× sem suavizar, só para achar o pixel.
As pranchas sobre o carvão e a silhueta saem de couro-aseprite/auxiliares/fila.py e silhueta.py.

    python ferramentas/prototipos/hud/comparar_couro.py

A rodada 2 (couro-aseprite/rodada2/: o fechamento novo do gibão de 32, o 40 e o 48), com as fotos de
fotografar_couro.mjs em rodada2/capturas/jogo (VERSOES=atual,rodada2), monta em rodada2/capturas/ as mesmas
comparações (com o Inventário em 40, o "você usa" em 48 e o voo), a prancha ampliada, as pranchas sobre o carvão dos
quatro tamanhos, a silhueta e o antes e depois do fechamento do gibão de 32:

    python ferramentas/prototipos/hud/comparar_couro.py rodada2

A comparação "64 trabalhado" × "32 ampliado 2×" (o *-32@2x.png no lugar do 64, vizinho mais próximo, sem retoque), com
as fotos de fotografar_couro.mjs em rodada2/capturas/jogo-x2 (VERSOES=rodada2,x2 LUGARES=saque), em
rodada2/capturas/x2-<peça>.png: o cartão do saque com os mesmos dados nas duas janelas e as duas artes em 1× e 3×:

    python ferramentas/prototipos/hud/comparar_couro.py x2
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


def prancha_zoom(z=3, fotos=FOTOS, saida=SAIDA, versoes=("atual", "proposta"), lugares=("ficha", "vender", "saque-64")):
    linhas = []
    for jan in ("normal", "baixa"):
        for peca in ("gibao", "bota"):
            for versao in versoes:
                ims = [(n, fotos / f"zoom-{jan}-{versao}-{peca}-{n}.png") for n in lugares]
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
    img.save(saida / "prancha-zoom.png")


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


R2 = PROPOSTA / "rodada2"
FOTOS2, SAIDA2 = R2 / "capturas" / "jogo", R2 / "capturas"
LUGARES2 = ("ficha", "mercado-vender", "mercado-dica", "inventario", "saque-cartao", "saque-voo", "tela-mercado",
            "tela-inventario", "tela-saque")


def fecho32(z=14):
    """O fechamento do gibão de 32, antes (rodada 1, pontos soltos) e depois (o cordão em zigue-zague): 1×, 2× e o peito
    ampliado, sobre o carvão."""
    from comparar_varinha import carvao
    a = Image.open(PROPOSTA / "rodada1" / "gibao-32.png").convert("RGBA")
    b = Image.open(R2 / "gibao-32.png").convert("RGBA")
    img = carvao(2 * (64 + 20 + 16 * z) + 40, 16 * z + 40)
    d, x = ImageDraw.Draw(img), 10
    for nome, i in (("antes (rodada 1)", a), ("depois (rodada 2)", b)):
        img.alpha_composite(i, (x, 24)); img.alpha_composite(i.resize((64, 64), Image.NEAREST), (x, 64))
        img.alpha_composite(i.crop((8, 4, 24, 20)).resize((16 * z, 16 * z), Image.NEAREST), (x + 84, 24))
        d.text((x, 6), f"{nome}: 1x, 2x e o peito ampliado", fill=TEXTO); x += 64 + 20 + 16 * z + 20
    img.convert("RGB").save(SAIDA2 / "fecho-gibao-32.png")


def rodada2():
    import subprocess
    aux, icones = PROPOSTA / "auxiliares", AQUI.parents[2] / "rpg" / "web" / "static" / "hud" / "icones"
    feitas = []
    for jan in ("normal", "baixa"):
        for peca in ("gibao", "bota"):
            for lugar in LUGARES2:
                fotos = [FOTOS2 / f"{jan}-{v}-{peca}-{lugar}.png" for v in ("atual", "rodada2")]
                if all(f.exists() for f in fotos):
                    nome = SAIDA2 / f"comparacao-{jan}-{peca}-{lugar}.png"
                    em_colunas(fotos, [f"{jan} · {peca} · {lugar}: atual (sprite 16x16)", "candidato (rodada 2)"]).save(nome)
                    feitas.append(nome.name)
    prancha_zoom(fotos=FOTOS2, saida=SAIDA2, versoes=("atual", "rodada2"),
                 lugares=("ficha", "vender", "corpo", "mochila", "saque-48", "saque-64"))
    fecho32()
    py = sys.executable
    for n, refs in ((32, ("cota", "botas-ferro", "escudo", "machado", "varinha")), (40, ("cota", "botas-ferro", "escudo", "varinha")),
                    (48, ("cota", "botas-ferro", "escudo", "varinha")), (64, ("cota", "botas-ferro", "escudo", "machado", "varinha"))):
        # o sprite atual só em 32 e 64 (os tamanhos em que ele é duplicação exata do 16×16)
        pares = [f"gibao atual={PROPOSTA / 'atual' / f'gibao-sprite-{n}.png'}"] if n in (32, 64) else []
        pares += [f"gibao={R2 / f'gibao-{n}.png'}", f"botas={R2 / f'bota-{n}.png'}"] + [f"{r}={icones / f'{r}-{n}.png'}" for r in refs]
        subprocess.run([py, str(aux / "fila.py"), str(SAIDA2 / f"carvao-{n}.png"), *pares], check=True)
    subprocess.run([py, str(aux / "silhueta.py"), str(SAIDA2 / "silhueta.png"),
                    *(str(R2 / f"{p}-{n}.png") for p in ("gibao", "bota") for n in (32, 40, 48, 64))], check=True)
    print("\n".join(feitas + ["prancha-zoom.png", "fecho-gibao-32.png", "carvao-32/40/48/64.png", "silhueta.png"]))


def x2(z=3):
    from comparar_varinha import carvao
    fotos = R2 / "capturas" / "jogo-x2"
    rot = {"rodada2": "64 trabalhado", "x2": "32 ampliado 2x (vizinho mais proximo, sem retoque)"}
    for peca in ("gibao", "bota"):
        linhas = []
        for jan in ("normal", "baixa"):
            linhas.append(em_colunas([fotos / f"{jan}-{v}-{peca}-saque-cartao.png" for v in rot],
                                     [f"{jan} · cartao do saque · {r}" for r in rot.values()]))
        arte = [("64 trabalhado", Image.open(R2 / f"{peca}-64.png").convert("RGBA")),
                ("32 ampliado 2x", Image.open(R2 / f"{peca}-32@2x.png").convert("RGBA")),
                ("32 final (1x)", Image.open(R2 / f"{peca}-32.png").convert("RGBA"))]
        larg = max(max(l.width for l in linhas), 3 * (64 * z + 100) + 20)
        alt_arte = 64 * z + 40
        img = Image.new("RGB", (larg, sum(l.height for l in linhas) + alt_arte + 20), FUNDO)
        y = 0
        for l in linhas:
            img.paste(l, (0, y)); y += l.height
        fundo = carvao(larg, alt_arte + 20)
        d = ImageDraw.Draw(fundo)
        for k, (r, a) in enumerate(arte):
            x = 10 + k * (64 * z + 100)
            fundo.alpha_composite(a, (x, 24))
            fundo.alpha_composite(a.resize((a.width * z, a.height * z), Image.NEAREST), (x + 80, 24))
            d.text((x, 6), f"{r}: 1x e ampliado {z}x", fill=TEXTO)
        img.paste(fundo.convert("RGB"), (0, y))
        img.save(SAIDA2 / f"x2-{peca}.png")
        print(f"x2-{peca}.png")


if __name__ == "__main__":
    {"rodada2": rodada2, "x2": x2}.get(sys.argv[1] if sys.argv[1:] else "", main)()
