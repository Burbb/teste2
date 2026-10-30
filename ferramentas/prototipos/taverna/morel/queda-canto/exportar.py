"""Exporta a queda de braço no canto (a fonte `queda-canto.aseprite`) para `camadas/morel-canto/`.

    python ferramentas/prototipos/taverna/morel/queda-canto/exportar.py             # exporta
    python ferramentas/prototipos/taverna/morel/queda-canto/exportar.py --conferir  # a fonte contra o desenho em código

A fonte é a autoridade: este script só lê as células dela e monta o que a tela desenha por cima da cena do canto:
- `queda-canto.png`: cada pose inteira (a parede, Morel, a mesa, os objetos, os braços e as mãos) recortada na caixa do
  que muda; fora dela, a cena do canto como está (`fundo.png`, `frente.png`, a chama da vela);
- `queda-canto.json`: a caixa, os nomes, a preparação, a espera (enquanto o motor não disse o resultado), e para cada
  desfecho (`nos`, `morel`) a linha do tempo e a do movimento reduzido (um índice de pose por tique de 100 ms);
- as folhas: `queda-canto-poses.png` (as poses principais: a pose do meio, uma passagem para cada lado e os dois fins,
  com a construção em cima e o acabamento embaixo) e `queda-canto-sequencia.png` (todas as poses, em ordem)."""
import json
import pathlib
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.append(str(AQUI.parent / "queda"))  # o fonte_aseprite (no fim: o poses.py daqui vence o de lá)

import poses as PO  # noqa: E402
import fonte_aseprite as fa  # noqa: E402

SAIDA = AQUI.parents[1] / "camadas" / "morel-canto"
CAIXA = (70, 0, 262, 96)
PRINCIPAIS = ["disputa", "pende_n2", "pende_m2", "nos_4", "morel_4", "nos_fim", "morel_fim"]


def celulas(tmp):
    cel = fa.celulas(PO.FONTE, pathlib.Path(tmp) / "cel")
    n = len(PO.ROTEIRO)

    def ler(camada, k):
        arq = cel / f"{camada}-{k}.png"
        return Image.open(arq).convert("RGBA") if arq.exists() else Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    return {c: [ler(c, k) for k in range(n)] for c in PO.CAMADAS}


def compor(C, k):
    im = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    for c in PO.CAMADAS:
        if c not in PO.OCULTAS:
            im.alpha_composite(C[c][k])
    return im


def main():
    with tempfile.TemporaryDirectory() as tmp:
        C = celulas(tmp)
    nomes = [n for n, _ in PO.ROTEIRO]
    idx = {n: i for i, n in enumerate(nomes)}
    x0, y0, x1, y1 = CAIXA
    w, h = x1 - x0, y1 - y0
    cenas = [compor(C, k) for k in range(len(nomes))]
    tira = Image.new("RGBA", (w * len(nomes), h))
    for k, im in enumerate(cenas):
        tira.paste(im.crop(CAIXA), (k * w, 0))
    tira.save(SAIDA / "queda-canto.png", optimize=True)

    def linha(lst):
        out = []
        for n, t in lst:
            out += [idx[n]] * t
        return out
    dados = {"caixa": [x0, y0, w, h], "poses": nomes, "preparo": linha(PO.PREPARO), "espera": linha(PO.ESPERA),
             "desfechos": {k: {"tempo": linha(PO.TEMPO[k]), "reduzido": linha(PO.REDUZIDO[k])} for k in PO.TEMPO}}
    (SAIDA / "queda-canto.json").write_text(json.dumps(dados, separators=(",", ":")), encoding="utf-8")
    # as folhas
    R = (96, 8, 256, 96)
    rw, rh = R[2] - R[0], R[3] - R[1]
    esc = 2
    folha = Image.new("RGBA", (len(PRINCIPAIS) * (rw * esc + 4) - 4, 2 * (rh * esc + 4) - 4), (24, 22, 20, 255))
    for j, n in enumerate(PRINCIPAIS):
        k = idx[n]
        g = cenas[k].copy()
        g.alpha_composite(Image.new("RGBA", (320, 96), (0, 0, 0, 120)))
        g.alpha_composite(C["construcao"][k])
        for i, im in enumerate((g, cenas[k])):
            folha.alpha_composite(im.crop(R).resize((rw * esc, rh * esc), Image.NEAREST),
                                  (j * (rw * esc + 4), i * (rh * esc + 4)))
    folha.save(SAIDA / "queda-canto-poses.png", optimize=True)
    cols = 9
    seq = Image.new("RGBA", (cols * (w + 2) - 2, ((len(nomes) + cols - 1) // cols) * (h + 2) - 2), (24, 22, 20, 255))
    for k, im in enumerate(cenas):
        seq.alpha_composite(im.crop(CAIXA), ((k % cols) * (w + 2), (k // cols) * (h + 2)))
    seq.save(SAIDA / "queda-canto-sequencia.png", optimize=True)
    print(f"queda-canto: {len(nomes)} poses, caixa {list(CAIXA)}; nós {len(dados['desfechos']['nos']['tempo'])} "
          f"tiques, Morel {len(dados['desfechos']['morel']['tempo'])}, a preparação {len(dados['preparo'])}; "
          f"folhas {folha.size} {seq.size}")


def conferir():
    with tempfile.TemporaryDirectory() as tmp:
        C = celulas(tmp)
    dif = 0
    for k, (nome, c) in enumerate(PO.quadros()):
        for camada in PO.CAMADAS:
            a = np.array(C[camada][k]).astype(int)
            b = np.array(c[camada]).astype(int)
            a[a[:, :, 3] == 0] = 0
            b[b[:, :, 3] == 0] = 0
            m = int((a != b).any(2).sum())
            if m:
                dif += m
                print(f"  {nome} {camada}: {m} px diferentes")
    print("a fonte é igual ao desenho" if not dif else f"{dif} px diferentes (retoques na fonte ou mudanças no código)")


if __name__ == "__main__":
    conferir() if "--conferir" in sys.argv else main()
