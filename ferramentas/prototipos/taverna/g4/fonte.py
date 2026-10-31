"""A fonte da G4 (o balcão aprovado, animado) e as camadas que a demonstração lê.

    python ferramentas/prototipos/taverna/g4/fonte.py --criar [--refazer]   # a fonte da G3 + o garrafão + as poses
    python ferramentas/prototipos/taverna/g4/fonte.py [--conferir]           # exporta da fonte para camadas/g4

`--criar` lê as células de `g3/aseprite/taverna-g3.aseprite` como estão, corrige o garrafão empalhado na camada
`fundo` (`garrafao`) e troca a camada `taverneiro` pelas poses da rotina (`g4/taverneiro.py`, um quadro por pose, na
ordem de `ORDEM`), e grava `g4/aseprite/taverna-g4.aseprite` (8 quadros: o fogo e o lampião usam os 4 primeiros; o
taverneiro, um por pose; o fundo, o caldeirão e a frente, só o primeiro). Depois de criada, ela é a autoridade: os
retoques à mão se fazem nela, e `--criar` não a sobrescreve sem `--refazer`.

Exportar lê a fonte como está e grava em `camadas/g4/`: `fundo.png` (o fundo com o caldeirão), `fogo.png` e `velas.png`
(as tiras das chamas, cortadas pelo que fica na frente delas), `taverneiro.png` (a tira das poses, recortada na caixa
que cobre todas), `frente.png` (o balcão e os fregueses, por cima dele) e `rotina.json` (a caixa, a linha do tempo de
`taverneiro.tempo()` a 100 ms e a pose parada). `--conferir` compara com o que o código desenha."""
import json
import pathlib
import sys

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))

from g import desenho as G, fonte as F  # noqa: E402
from g3 import fonte as F3, retoques as R3  # noqa: E402
from g4 import taverneiro as T  # noqa: E402
from tela_h2 import Tela  # noqa: E402

FONTE = AQUI / "aseprite" / "taverna-g4.aseprite"
SAIDA = AQUI.parent / "camadas" / "g4"


def _garrafao_novo(px):
    """O garrafão empalhado no eixo x 207: o bojo simétrico de vime (larguras ímpares), a base reta apoiada na tábua,
    o gargalo de vidro de 3 px no meio, o anel da boca, a rolha."""
    y0 = G.PR
    larguras = (5, 7, 9, 11, 11, 11, 11, 11, 11, 9, 9)
    for k, w in enumerate(larguras):
        y = y0 - len(larguras) + k
        a = 207 - w // 2
        for x in range(a, a + w):
            cor = "vimeLuz" if x - a < 2 else "vimeEsc" if a + w - x <= 1 else "vime"
            if (x + y) % 3 == 0 and cor == "vime":
                cor = "vimeEsc"
            px.p(x, y, cor)
    px(202, y0 - 1, 11, 1, "vimeEsc")             # a base, apoiada
    px(206, y0 - 15, 3, 4, "vidro")               # o gargalo
    px(206, y0 - 15, 1, 4, "vidroLuz")
    px(205, y0 - 16, 5, 1, "vidroLuz")            # o anel da boca
    px(206, y0 - 17, 3, 1, "rolha")


def garrafao(fundo):
    """A garrafa bojuda amarelada que o Jean marcou: o garrafão empalhado tinha o bojo torto e o gargalo fora do eixo.
    Onde ele estava volta a parede da G; por cima, o novo, com a luz da G."""
    parede = Tela(G.QW, G.QH)
    G.sala(G.Pincel(parede))
    G.luz(parede)
    x0, y0, x1, y1 = 199, 8, 215, G.PR
    fundo[y0:y1, x0:x1] = parede.a[y0:y1, x0:x1]
    novo = Tela(G.QW, G.QH)
    _garrafao_novo(G.Pincel(novo))
    G.luz(novo)
    return R3._colar(fundo, novo)


def quadros_animados():
    """{camada: [imagem, ...]}: as células da fonte da G3 com o garrafão corrigido e as poses do taverneiro."""
    q = F.ler_fonte(F3.FONTE)
    fundo = np.array(q["fundo"][0].convert("RGBA"))
    n = garrafao(fundo)
    print(f"garrafão: {n} px; poses: {len(T.ORDEM)}")
    novo = dict(q)
    novo["fundo"] = [Image.fromarray(fundo, "RGBA")]
    novo["taverneiro"] = [Image.fromarray(T.quadro(nome), "RGBA") for nome in T.ORDEM]
    return novo


def montar(q):
    """As imagens da demonstração animada."""
    fundo = q["fundo"][0].copy()
    fundo.alpha_composite(q["caldeirao"][0])
    frente = q["frente"][0]
    cobre = Image.new("RGBA", fundo.size)
    cobre.alpha_composite(q["caldeirao"][0])
    cobre.alpha_composite(frente)
    mascara = cobre.getchannel("A").point(lambda a: 255 if a else 0)
    tiras = {}
    for nome, arq in (("fogo", "fogo"), ("lampiao", "velas")):
        tira = Image.new("RGBA", (G.QW * len(q[nome]), G.QH))
        for i, im in enumerate(q[nome]):
            livre = im.copy()
            livre.paste((0, 0, 0, 0), mask=mascara)
            tira.paste(livre, (G.QW * i, 0))
        tiras[arq] = tira
    poses = q["taverneiro"]
    caixas = [im.getbbox() for im in poses if im.getbbox()]
    x0, y0 = min(c[0] for c in caixas), min(c[1] for c in caixas)
    x1, y1 = max(c[2] for c in caixas), max(c[3] for c in caixas)
    w, h = x1 - x0, y1 - y0
    tira = Image.new("RGBA", (w * len(poses), h))
    for i, im in enumerate(poses):
        tira.paste(im.crop((x0, y0, x1, y1)), (w * i, 0))
    rotina = {"caixa": [x0, y0, w, h], "n": len(poses), "tempo": T.tempo(), "parada": T.ORDEM.index(T.PARADA),
              "poses": T.ORDEM}
    return {"fundo": fundo, "frente": frente, "taverneiro": tira, **tiras}, rotina


def exportar():
    imagens, rotina = montar(F.ler_fonte(FONTE))
    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, im in imagens.items():
        im.save(SAIDA / f"{nome}.png", optimize=True)
    with open(SAIDA / "rotina.json", "w", encoding="utf-8") as f:
        json.dump(rotina, f, separators=(",", ":"))
    print("camadas/g4:", ", ".join(sorted(f"{n}.png" for n in imagens)), "+ rotina.json")
    return imagens


def conferir(saida):
    codigo, _ = montar(quadros_animados())
    dif = [n for n in saida if saida[n].tobytes() != codigo[n].tobytes()]
    print(f"conferido: {len(saida) - len(dif)} de {len(saida)} imagens iguais ao código"
          + (f" (diferem: {', '.join(dif)}: os retoques da fonte)" if dif else ""))
    return not dif


if __name__ == "__main__":
    if "--refazer" in sys.argv and "--sem-os-retoques" not in sys.argv:
        sys.exit("A fonte está no jogo desde a 1.220.0 (taverna/jogo.py): refazê-la do código descarta o que foi "
                 "retocado nela. Para isso mesmo, junte --sem-os-retoques.")
    if "--criar" in sys.argv:
        F.criar(FONTE, quadros_animados)
        sys.exit(0)
    s = exportar()
    if "--conferir" in sys.argv and not conferir(s):
        sys.exit(1)
