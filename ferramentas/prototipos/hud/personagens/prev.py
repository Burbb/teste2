"""Prévia rápida dos candidatos ao lado dos atuais (estudo; a avaliação é no jogo, fotografar_personagens.mjs):
    python prev.py <saida.png> morel-carta:1 morel-carta-c:2 guerreiro-carta:2 ...
Os nomes são os de atuais.json (gerar.py) e os candidatos com -c (morel-carta-c, morel-cabeca-c, mago-figura-c); o
número é a escala em que o jogo os mostra."""
import json, pathlib, sys
import candidatos
from ver import folha

AQUI = pathlib.Path(__file__).resolve().parent
d = json.loads((AQUI / "atuais.json").read_text())
cm, pm = d["morel-carta"]["cores"], d["mago-carta"]["cores"]
d["morel-carta-c"] = {"grade": candidatos.MOREL_CARTA, "cores": cm}
d["morel-cabeca-c"] = {"grade": candidatos.MOREL_CABECA, "cores": cm}
d["mago-figura-c"] = {"grade": candidatos.MAGO_FIGURA, "cores": pm}
folha(d, [(a.split(":")[0], int(a.split(":")[1])) for a in sys.argv[2:]], sys.argv[1])
