"""Exporta as camadas da candidata para a demonstração (`camadas/`) e, com --ver, uma composição ampliada de cada estado
para conferir o desenho (`conferencia/`, fora do que se entrega).

    python ferramentas/prototipos/curandeira/exportar.py [--ver]

As tiras de quadros vão lado a lado, 320 px cada (como as da forja): fogo (4), vapor e vapor-forte (4), pita e marta
(um quadro por pose do GIRO)."""
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
    for quem in F.FIG:
        tira([F.figura(quem, i) for i in range(F.QUADROS)]).save(os.path.join(CAMADAS, f"{quem}.png"))


def composicao(quem, i=F.REPOUSO, escura=False, f=0):
    im = D.fundo().imagem()
    for camada in ([D.baldes()] if escura else []) + [D.fogo(f), D.vapor(f, escura), F.figura(quem, i), D.frente()]:
        im.alpha_composite(camada.imagem())
    return im


def ver():
    pasta = os.path.join(AQUI, "conferencia")
    os.makedirs(pasta, exist_ok=True)
    for nome, quem, escura in (("pita", "pita", False), ("pita-agua-escura", "pita", True), ("marta", "marta", False)):
        im = composicao(quem, escura=escura)
        im.resize((D.QW * 4, D.QH * 4), Image.NEAREST).save(os.path.join(pasta, f"{nome}-4x.png"))
        im.crop((120, 20, 200, 90)).resize((80 * 8, 70 * 8), Image.NEAREST).save(os.path.join(pasta, f"{nome}-figura-8x.png"))
    # as poses do giro lado a lado, recortadas na figura (8×)
    for quem in F.FIG:
        quadros = [composicao(quem, i).crop((134, 26, 178, 62)) for i in range(F.QUADROS)]
        folha = Image.new("RGBA", (44 * 8 * 4, 36 * 8 * 2))
        for i, q in enumerate(quadros):
            folha.paste(q.resize((44 * 8, 36 * 8), Image.NEAREST), ((i % 4) * 44 * 8, (i // 4) * 36 * 8))
        folha.save(os.path.join(pasta, f"{quem}-giro-8x.png"))


if __name__ == "__main__":
    exportar()
    if "--ver" in sys.argv:
        ver()
    print("ok")
