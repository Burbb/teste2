"""Monta as pranchas da rodada 1 do capuz e da luva com braçadeira de couro (couro2-aseprite/), a partir dos arquivos e
das fotos de fotografar_couro2.mjs (couro2-aseprite/capturas/jogo/), em couro2-aseprite/capturas/:
  - comparacao-<janela>-<peça>-<lugar>.png: o atual à esquerda e o candidato à direita, em tamanho real (a ficha e o
    mercado em 32, a dica, o cartão do saque com o 64 derivado, as telas inteiras);
  - prancha-zoom.png: os espaços no jogo ampliados 3× sem suavizar, só para achar o pixel;
  - carvao-32.png, carvao-64.png: os candidatos em 1× sobre o carvão, ao lado do gibão, das botas e dos aprovados;
  - silhueta.png: os dois numa cor só.

    python ferramentas/prototipos/hud/comparar_couro2.py

A rodada 2 (couro2-aseprite/rodada2/: o capuz de couro refeito, a luva de couro aprovada, o capuz de tecido e a luva de
seda), com as fotos de fotografar_couro2.mjs em rodada2/capturas/jogo (VERSOES=atual,couro,atual_mago,tecido), monta
em rodada2/capturas/: capuz-couro-r1-r2.png (o capuz de couro antes e depois), couro-tecido.png (os dois materiais do
capuz e da luva), carvao-32.png e carvao-64.png (com o gibão e as botas), silhueta.png, as comparações no jogo
(comparacao-<janela>-<arqueiro|mago>-<peça>-<lugar>.png) e prancha-zoom.png:

    python ferramentas/prototipos/hud/comparar_couro2.py rodada2
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


R2 = PROPOSTA / "rodada2"
FOTOS2, SAIDA2 = R2 / "capturas" / "jogo", R2 / "capturas"


def _quadro(pares, saida, z=8):
    """Cada arquivo de 32 em 1× e 2× sobre o carvão, e a ampliação z× ao lado (só para achar o pixel)."""
    from PIL import Image, ImageDraw
    from comparar_varinha import TEXTO, carvao
    col = 32 + 64 + 32 * z + 40
    img = carvao(col * len(pares) + 20, 32 * z + 50)
    d = ImageDraw.Draw(img)
    for k, (r, p) in enumerate(pares):
        a, x = Image.open(p).convert("RGBA"), 10 + k * col
        img.alpha_composite(a, (x, 30)); img.alpha_composite(a.resize((64, 64), Image.NEAREST), (x, 72))
        img.alpha_composite(a.resize((32 * z, 32 * z), Image.NEAREST), (x + 76, 30))
        d.text((x, 8), f"{r}: 1x, 2x (o 64) e {z}x", fill=TEXTO)
    img.convert("RGB").save(saida)


def rodada2():
    from PIL import Image, ImageDraw
    from comparar_varinha import FUNDO, TEXTO
    py, feitas = sys.executable, []
    _quadro([("capuz de couro, rodada 1", R1 / "capuz-32.png"), ("capuz de couro, revisado", R2 / "capuz-32.png")],
            SAIDA2 / "capuz-couro-r1-r2.png")
    _quadro([("capuz de couro", R2 / "capuz-32.png"), ("capuz de tecido", R2 / "capuz_tecido-32.png"),
             ("luva de couro (aprovada)", R2 / "luva-32.png"), ("luva de seda", R2 / "luva_seda-32.png")],
            SAIDA2 / "couro-tecido.png", z=6)
    for n in (32, 64):
        pares = [f"capuz couro={R2 / f'capuz-{n}.png'}", f"capuz tecido={R2 / f'capuz_tecido-{n}.png'}",
                 f"luva couro={R2 / f'luva-{n}.png'}", f"luva seda={R2 / f'luva_seda-{n}.png'}"]
        pares += [f"{r}={ICONES / f'{r}-{n}.png'}" for r in ("gibao", "bota", "elmo", "manopla", "varinha")]
        subprocess.run([py, str(AUX / "fila.py"), str(SAIDA2 / f"carvao-{n}.png"), *pares], check=True)
    subprocess.run([py, str(AUX / "silhueta.py"), str(SAIDA2 / "silhueta.png"),
                    *(str(R2 / f"{p}-32.png") for p in ("capuz", "capuz_tecido", "luva", "luva_seda")),
                    str(R1 / "capuz-32.png")], check=True)
    for jan in ("normal", "baixa"):
        for classe, (antes, depois, rot) in (("arqueiro", ("atual", "couro", "couro")), ("mago", ("atual_mago", "tecido", "tecido"))):
            for peca in ("capuz", "luva"):
                for lugar in LUGARES:
                    fotos = [FOTOS2 / f"{jan}-{v}-{peca}-{lugar}.png" for v in (antes, depois)]
                    if all(f.exists() for f in fotos):
                        nome = SAIDA2 / f"comparacao-{jan}-{classe}-{peca}-{lugar}.png"
                        em_colunas(fotos, [f"{jan} · {classe} · {peca} · {lugar}: atual",
                                           f"candidato de {rot} (rodada 2; o 64 é o 32 ampliado 2x)"]).save(nome)
                        feitas.append(nome.name)
    linhas = []
    for jan in ("normal", "baixa"):
        for v in ("atual", "couro", "atual_mago", "tecido"):
            for peca in ("capuz", "luva"):
                ims = [(n, FOTOS2 / f"zoom-{jan}-{v}-{peca}-{n}.png") for n in ("ficha", "vender", "saque-64")]
                ims = [(n, Image.open(p).convert("RGB")) for n, p in ims if p.exists()]
                linhas.append((f"{jan} · {v} · {peca}", [(n, i.resize((i.width * 3, i.height * 3), Image.NEAREST)) for n, i in ims]))
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
    img.save(SAIDA2 / "prancha-zoom.png")
    print("\n".join(feitas + ["capuz-couro-r1-r2.png", "couro-tecido.png", "carvao-32.png", "carvao-64.png",
                               "silhueta.png", "prancha-zoom.png"]))


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
    rodada2() if sys.argv[1:] == ["rodada2"] else main()
