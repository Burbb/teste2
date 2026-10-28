"""Exporta as camadas das duas candidatas do templo para a demonstração (`camadas/a/`, `camadas/b/`) e a rotina do
clérigo de cada uma (`camadas/rotina.json`: o quadro de cada tique de 100 ms e a pose parada).

    python ferramentas/prototipos/templo/exportar.py

As tiras vão lado a lado, 320 px cada: velas (4 quadros), fumaca (8), poeira (8, só na A) e clerigo (um quadro por
desenho da rotina). Só escreve em `camadas/`."""
import json
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

from templo.a import desenho as DA, figura as FA  # noqa: E402
from templo.b import desenho as DB, figura as FB  # noqa: E402

CAMADAS = os.path.join(AQUI, "camadas")


def tira(telas):
    im = Image.new("RGBA", (320 * len(telas), 96))
    for i, t in enumerate(telas):
        im.paste(t.imagem(), (320 * i, 0))
    return im


def exportar():
    rotina = {}
    for nome, D, F, desenhos in (("a", DA, FA, lambda: FA.todas()), ("b", DB, FB, lambda: FB.todas())):
        pasta = os.path.join(CAMADAS, nome)
        os.makedirs(pasta, exist_ok=True)
        D.fundo().imagem().save(os.path.join(pasta, "fundo.png"))
        D.frente().imagem().save(os.path.join(pasta, "frente.png"))
        tira([D.velas(i) for i in range(4)]).save(os.path.join(pasta, "velas.png"))
        tira([D.fumaca(i) for i in range(8)]).save(os.path.join(pasta, "fumaca.png"))
        if hasattr(D, "poeira"):
            tira([D.poeira(i) for i in range(8)]).save(os.path.join(pasta, "poeira.png"))
        tira(desenhos()).save(os.path.join(pasta, "clerigo.png"))
        _, tempo, parada = F.quadros()
        rotina[nome] = {"tempo": tempo, "parada": parada}
    with open(os.path.join(CAMADAS, "rotina.json"), "w", encoding="utf-8") as f:
        json.dump(rotina, f, separators=(",", ":"))


if __name__ == "__main__":
    exportar()
    print("ok")
