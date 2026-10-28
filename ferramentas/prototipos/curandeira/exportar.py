"""Exporta as camadas da candidata para a demonstração (`camadas/`) e, com --ver, uma composição ampliada de cada estado
para conferir o desenho (`conferencia/`, fora do que se entrega).

    python ferramentas/prototipos/curandeira/exportar.py [--ver]

As tiras de quadros vão lado a lado, 320 px cada (como as da forja): fogo (4), vapor e vapor-forte (4), pita e marta
(um quadro por desenho diferente da rotina). `rotina.json` diz, para cada uma, qual quadro vale em cada tique de
100 ms (`tempo`) e qual é a pose parada do movimento reduzido (`parada`): a linha do tempo sai de `figuras.py`, não é
repetida na tela.

Só escreve em `camadas/` (e em `conferencia/` com --ver). As passadas anteriores, guardadas para comparação em
`anterior/` (a segunda em `camadas/`, a moagem da terceira em `terceira/`), nunca são escritas por script."""
import json
import os
import sys

from PIL import Image

import desenho as D
import figuras as F

AQUI = os.path.dirname(os.path.abspath(__file__))
CAMADAS = os.path.join(AQUI, "camadas")


def tira(quadros):
    im = Image.new("RGBA", (D.QW * len(quadros), D.QH))
    for i, q in enumerate(quadros):
        im.paste(q.imagem(), (i * D.QW, 0))
    return im


def exportar():
    os.makedirs(CAMADAS, exist_ok=True)
    D.fundo().imagem().save(os.path.join(CAMADAS, "fundo.png"))
    D.frente().imagem().save(os.path.join(CAMADAS, "frente.png"))
    D.baldes().imagem().save(os.path.join(CAMADAS, "baldes.png"))
    tira([D.fogo(i) for i in range(4)]).save(os.path.join(CAMADAS, "fogo.png"))
    tira([D.vapor(i) for i in range(4)]).save(os.path.join(CAMADAS, "vapor.png"))
    tira([D.vapor(i, forte=True) for i in range(4)]).save(os.path.join(CAMADAS, "vapor-forte.png"))
    rotina = {}
    for quem in F.FIG:
        tira(F.todas(quem)).save(os.path.join(CAMADAS, f"{quem}.png"))
        _, tempo, parada = F.quadros(quem)
        rotina[quem] = {"tempo": tempo, "parada": parada}
    with open(os.path.join(CAMADAS, "rotina.json"), "w", encoding="utf-8") as f:
        json.dump(rotina, f, separators=(",", ":"))


def composicao(quem, item=F.PARADA, escura=False, f=0):
    im = D.fundo().imagem()
    fig = F.figura(quem, F.pose_de(quem, item))
    for camada in ([D.baldes()] if escura else []) + [D.fogo(f), D.vapor(f, escura), fig, D.frente()]:
        im.alpha_composite(camada.imagem())
    return im


def ver():
    pasta = os.path.join(AQUI, "conferencia")
    os.makedirs(pasta, exist_ok=True)
    for nome, quem, escura in (("pita", "pita", False), ("pita-agua-escura", "pita", True), ("marta", "marta", False)):
        im = composicao(quem, escura=escura)
        im.resize((D.QW * 4, D.QH * 4), Image.NEAREST).save(os.path.join(pasta, f"{nome}-4x.png"))
        im.crop((120, 20, 200, 90)).resize((80 * 8, 70 * 8), Image.NEAREST).save(os.path.join(pasta, f"{nome}-figura-8x.png"))
    # os desenhos da rotina lado a lado, recortados na figura (4×), na ordem em que aparecem
    for quem in F.FIG:
        unicos, _, _ = F.quadros(quem)
        quadros = [composicao(quem, it).crop((134, 24, 178, 84)) for it in unicos]
        col = 8
        folha = Image.new("RGBA", (44 * 4 * col, 60 * 4 * ((len(quadros) + col - 1) // col)))
        for i, q in enumerate(quadros):
            folha.paste(q.resize((44 * 4, 60 * 4), Image.NEAREST), ((i % col) * 44 * 4, (i // col) * 60 * 4))
        folha.save(os.path.join(pasta, f"{quem}-rotina-4x.png"))


if __name__ == "__main__":
    exportar()
    if "--ver" in sys.argv:
        ver()
    print("ok")
