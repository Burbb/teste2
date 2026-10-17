"""O teste do pen.dev (experimento): monta, por janela e estado, a comparação em tamanho real (sem escala) das fotos
de capturas/: o jogo de hoje, o fluxo A (CSS direto), o fluxo B (o canvas do pen.dev levado ao CSS) e o próprio canvas
do pen.dev; e a importação crua do pen.dev ao lado do jogo. Grava capturas/comparacao-<janela>-<estado>.png.

    python ferramentas/prototipos/hud/pen-composicao/comparar.py
"""
import os

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(AQUI, "capturas")
FAIXA = 22


def montar(nome, pecas):
    imgs = [(r, Image.open(os.path.join(CAP, f)).convert("RGB")) for r, f in pecas if os.path.exists(os.path.join(CAP, f))]
    w = max(i.width for _, i in imgs) + 24
    h = sum(i.height + FAIXA + 12 for _, i in imgs) + 12
    tela = Image.new("RGB", (w, h), (24, 24, 26))
    d = ImageDraw.Draw(tela)
    y = 12
    for rotulo, i in imgs:
        d.text((12, y + 4), rotulo, fill=(190, 180, 160))
        tela.paste(i, (12, y + FAIXA))
        y += i.height + FAIXA + 12
    tela.save(os.path.join(CAP, nome))


for jan in ("1280x720", "1500x950"):
    for est in ("parado", "destaque", "indisponivel"):
        montar(f"comparacao-{jan}-{est}.png", [
            ("o jogo hoje", f"{jan}-{est}-atual.png"),
            ("A: ajuste direto no CSS", f"{jan}-{est}-a.png"),
            ("B: canvas do pen.dev levado ao CSS", f"{jan}-{est}-b.png"),
            ("o canvas do pen.dev (export PNG 1x)", f"{jan}-{est}-pen-canvas.png"),
        ])
montar("comparacao-importacao.png", [
    ("o jogo hoje (1500x950, destacada)", "1500x950-destaque-atual.png"),
    ("pen.dev: importacao direta do localhost", "1500x950-destaque-pen-importacao.png"),
    ("pen.dev: reconstrucao com as pecas do jogo (antes do ajuste)", "1500x950-destaque-pen-reconstrucao.png"),
])
print("ok")
