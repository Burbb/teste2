"""Exporta as camadas da taverna para a demonstração (`camadas/`):

- `fundo.png` (parado, com a luz), `fogo.png` (a lareira, 4 quadros lado a lado), `frente.png` (as mesas e o balcão,
  por cima dos corpos), `velas.png` (4 quadros, por cima de tudo);
- `gente/<nome>.png`: a tira de cada pessoa, recortada na caixa que cobre todas as poses dela, um desenho por coluna;
  a linha de cima é o corpo (atrás dos móveis), a de baixo as mãos com o que seguram (na frente);
- `taverna.json`: para cada pessoa, onde a caixa cai no quadro (`x`, `y`, `w`, `h`), a rotina (`tempo`: o desenho de
  cada passo de 200 ms), a pose parada (`parada`), o passo em que ela começa (`fase`, para ninguém andar em sincronia)
  e `so_com` ("morel": só aparece quando o motor diz que Morel está no canto).

    python ferramentas/prototipos/taverna/exportar.py

Também as candidatas B a F (os estudos estáticos, `b/` a `f/`) em `camadas/<b|c|d|e|f>/`: `fundo.png` (a sala com as pessoas e a luz, com
Morel no canto), `fundo-sem-morel.png` (o canto vazio, quando ele foi recrutado), `fogo.png` e `velas.png` (4 quadros
cada, lado a lado). As pessoas dos estudos estáticos ainda não têm ciclos: ficam no fundo.

Só escreve em `camadas/`."""
import json
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import desenho as D  # noqa: E402
import gente as G  # noqa: E402

CAMADAS = os.path.join(AQUI, "camadas")
# o passo em que cada um começa a rotina: espalhados, para as mesas não mudarem de pose juntas. Os dois jogadores têm a
# mesma fase, porque as rotinas deles (64 passos cada) já se revezam: um mexe a peça enquanto o outro pensa; os da
# conversa também (56 passos): um responde enquanto o outro escuta
FASES = {"esq_a": 0, "esq_b": 23, "meio_a": 9, "meio_b": 9, "dir_a": 5, "dir_b": 5, "fogo": 17, "taverneiro": 11,
         "morel": 3}


def tira(telas):
    im = Image.new("RGBA", (D.QW * len(telas), D.QH))
    for i, t in enumerate(telas):
        im.paste(t.imagem(), (D.QW * i, 0))
    return im


def exportar():
    os.makedirs(os.path.join(CAMADAS, "gente"), exist_ok=True)
    D.fundo().imagem().save(os.path.join(CAMADAS, "fundo.png"))
    tira([D.fogo(i) for i in range(4)]).save(os.path.join(CAMADAS, "fogo.png"))
    D.frente_moveis().imagem().save(os.path.join(CAMADAS, "frente.png"))
    tira([D.velas(i) for i in range(4)]).save(os.path.join(CAMADAS, "velas.png"))
    dados = {}
    for item in G.ELENCO:
        nome = item["fig"].nome
        unicos, tempo, parada = G.quadros(item)
        pares = [[c.imagem() for c in item["fig"].camadas(item["poses"][p])] for p in unicos]
        caixas = [im.getbbox() for par in pares for im in par if im.getbbox()]
        x0, y0 = min(c[0] for c in caixas), min(c[1] for c in caixas)
        x1, y1 = max(c[2] for c in caixas), max(c[3] for c in caixas)
        w, h = x1 - x0, y1 - y0
        im = Image.new("RGBA", (w * len(pares), h * 2))
        for i, (corpo, maos) in enumerate(pares):
            im.paste(corpo.crop((x0, y0, x1, y1)), (i * w, 0))
            im.paste(maos.crop((x0, y0, x1, y1)), (i * w, h))
        im.save(os.path.join(CAMADAS, "gente", f"{nome}.png"))
        dados[nome] = {"x": x0, "y": y0, "w": w, "h": h, "tempo": tempo, "parada": parada, "fase": FASES.get(nome, 0),
                       **({"so_com": "morel"} if nome == "morel" else {})}
    with open(os.path.join(CAMADAS, "taverna.json"), "w", encoding="utf-8") as f:
        json.dump({"gente": dados}, f, separators=(",", ":"))


def exportar_estatica(cand):
    """As camadas de um estudo estático (a B, a C) em camadas/<cand>/."""
    import importlib
    DB = importlib.import_module(f"{cand}.desenho")
    GB = importlib.import_module(f"{cand}.gente")
    pasta = os.path.join(CAMADAS, cand)
    os.makedirs(pasta, exist_ok=True)
    for nome, morel in (("fundo", True), ("fundo-sem-morel", False)):
        t = DB.Tela(DB.QW, DB.QH)
        px = DB.Pincel(t)
        r = DB.sala(px)
        GB.desenhar(px, r, morel=morel)
        if cand in ("e", "f"):                               # a E e a F devolvem as chamas e a boca da lareira com a sala
            DB.luz(t, r["chamas"], r["boca"])
        else:
            DB.luz(t, DB.chamas_velas())
        t.imagem().save(os.path.join(pasta, f"{nome}.png"))
    tira([DB.fogo(i) for i in range(4)]).save(os.path.join(pasta, "fogo.png"))
    tira([DB.velas(i) for i in range(4)]).save(os.path.join(pasta, "velas.png"))


if __name__ == "__main__":
    exportar()
    exportar_estatica("b")
    exportar_estatica("c")
    exportar_estatica("d")
    exportar_estatica("e")
    exportar_estatica("f")
    print("ok")
