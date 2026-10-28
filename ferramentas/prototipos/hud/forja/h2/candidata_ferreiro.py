"""Candidata de três retoques locais no ferreiro (para o Jean avaliar; o jogo e a fonte aseprite/forja-h2.aseprite não
mudam). Parte do desenho em código (ferreiro_h2.figura, igual ao quadro do jogo pixel a pixel) e grava a tira candidata
em candidata/ferreiro.png, mais a folha de comparação candidata/folha-ferreiro.png (as nove poses, hoje × candidata,
sobre as mesmas camadas do jogo).

1. A mão do martelo no sobe2: o cabo inclina um pouco para trás (a cabeça do martelo vai de x 150,2 para 152) e a
   ponta do cabo sai por baixo do punho, na frente do pulso. O cabo atravessando a mão desfaz a leitura de punho de
   guidão (o T do cabo curto em cima do punho).
2. A nuca: o volume da parte de trás do crânio e do pescoço, do occipital até o trapézio, no tom de sombra da pele
   (o meio da pele, com a borda de trás na sombra; só onde hoje aparece o fundo entre a cabeça e o ombro: nada do
   rosto, da barba ou da alça muda).
3. O calcanhar da bigorna na frente da barriga: o ferreiro está atrás e à direita da bigorna, então a ponta de trás
   dela cobre o avental (some o pixel do ferreiro onde a bigorna existe, da linha 61 para baixo); as garras da tenaz e
   a tenaz, que prendem a espiga em cima da bigorna, continuam por cima.

    python ferramentas/prototipos/hud/forja/h2/candidata_ferreiro.py
"""
import pathlib
import sys

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import ferreiro_h2 as F  # noqa: E402
from desenhar_h2 import ESTADOS  # noqa: E402

SAIDA = AQUI / "candidata"
CAMADAS = AQUI / "camadas"

# 1. a pose do sobe2 com o cabo inclinado (o resto da pose igual)
SOBE2 = dict(F.POSES["sobe2"], cabo=(150, 40), cabeca_m=(152, 25.2))
# a ponta do cabo abaixo do punho (na frente do pulso), em x e y da tela
PONTA_CABO = [(150, 37, "madeiraLuz"), (150, 38, "madeiraLuz")]

# 2. a nuca, à mão, a partir da origem da cabeça (o alto da testa): "s" o meio da pele, "d" a borda de trás na sombra;
# só entra onde a figura está vazia (fica atrás da cabeça, da alça e do ombro)
NUCA = [
    ".sd...",
    "sssd..",
    "sssssd",
    "ssssss",
    "ssssss",
]
NUCA_ORIGEM = (11, 5)
PAL_NUCA = {"d": "peleSombra", "s": "pele"}

# 3. o calcanhar da bigorna: as linhas e colunas onde a bigorna passa à frente (as garras da tenaz, em x 148-149, não)
CALCANHAR = (150, 161, 61, 67)


def figura(estado):
    pose = "ajuste" if estado == "ajuste_virada" else estado
    guardada = F.POSES["sobe2"]
    if pose == "sobe2":
        F.POSES["sobe2"] = SOBE2
    try:
        t = F.figura(pose, virada=estado == "ajuste_virada")
    finally:
        F.POSES["sobe2"] = guardada
    p = SOBE2 if pose == "sobe2" else F.POSES[pose]
    if pose == "sobe2":
        for x, y, cor in PONTA_CABO:
            t.px(x, y, F.COR[cor])
    sx, sy = p["ombro"]
    cx_, cy_ = p["cabeca"]
    hx, hy = 159 + sx + cx_, 31 + sy + cy_
    for dy, linha in enumerate(NUCA):
        for dx, ch in enumerate(linha):
            x, y = hx + NUCA_ORIGEM[0] + dx, hy + NUCA_ORIGEM[1] + dy
            if ch in PAL_NUCA and t.get(x, y)[3] == 0:
                t.px(x, y, F.COR[PAL_NUCA[ch]])
    return t.imagem()


def tira():
    bigorna = Image.open(CAMADAS / "bigorna.png").convert("RGBA")
    x0, x1, y0, y1 = CALCANHAR
    saida = Image.new("RGBA", (320 * len(ESTADOS), 96))
    for i, e in enumerate(ESTADOS):
        q = figura(e)
        for y in range(y0, y1):
            for x in range(x0, x1):
                if bigorna.getpixel((x, y))[3]:
                    q.putpixel((x, y), (0, 0, 0, 0))
        saida.paste(q, (320 * i, 0))
    return saida


def montar(ferreiro, i):
    c = Image.open(CAMADAS / "fundo.png").convert("RGBA")
    c.alpha_composite(Image.open(CAMADAS / "fogo.png").convert("RGBA").crop((0, 0, 320, 96)))
    c.alpha_composite(Image.open(CAMADAS / "bigorna.png").convert("RGBA"))
    c.alpha_composite(Image.open(CAMADAS / "espada.png").convert("RGBA").crop((320 * i, 0, 320 * i + 320, 96)))
    c.alpha_composite(ferreiro.crop((320 * i, 0, 320 * i + 320, 96)))
    c.alpha_composite(Image.open(CAMADAS / "frente.png").convert("RGBA"))
    return c


def folha(nova):
    hoje = Image.open(CAMADAS / "ferreiro.png").convert("RGBA")
    z, (bx0, by0, bx1, by1) = 5, (128, 12, 200, 92)
    w, h = (bx1 - bx0) * z, (by1 - by0) * z
    f = Image.new("RGB", (len(ESTADOS) * (w + 8) + 8, 2 * (h + 24) + 8), (16, 17, 20))
    d = ImageDraw.Draw(f)
    for i, e in enumerate(ESTADOS):
        for j, (rot, camada) in enumerate((("hoje", hoje), ("candidata", nova))):
            q = montar(camada, i).crop((bx0, by0, bx1, by1)).resize((w, h), Image.NEAREST)
            x, y = 8 + i * (w + 8), 8 + j * (h + 24)
            d.text((x, y), f"{e} - {rot}", fill=(220, 210, 180))
            f.paste(q.convert("RGB"), (x, y + 16))
    return f


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    nova = tira()
    nova.save(SAIDA / "ferreiro.png", optimize=True)
    folha(nova).save(SAIDA / "folha-ferreiro.png", optimize=True)
    print("candidata:", SAIDA / "ferreiro.png")
