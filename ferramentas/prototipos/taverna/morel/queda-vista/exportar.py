"""Exporta a queda de braço na vista aprovada (a fonte `queda-vista.aseprite`) para `camadas/morel-vista/`.

    python ferramentas/prototipos/taverna/morel/queda-vista/exportar.py             # exporta
    python ferramentas/prototipos/taverna/morel/queda-vista/exportar.py --conferir  # compara a fonte com o desenho

A fonte é a autoridade: este script só a lê (o Aseprite em lote achata cada quadro com a luz, sem a `guia`, as `juntas`,
o fogo e as chamas, que a cena desenha por cima com as da vista aprovada) e grava:
- `queda-vista-fundo.png`: o primeiro quadro inteiro (a sala, a mesa com a tigela deslizada, Morel na pose `firma`);
- `queda-vista.png`: as poses recortadas na caixa em que os quadros diferem, lado a lado;
- `queda-vista.json`: a caixa, os nomes das poses e, para cada desfecho (`nos`, `morel`), a linha do tempo (um índice
  de pose por tique de 100 ms) e a do movimento reduzido;
- as folhas de inspeção: `queda-vista-comparacao.png` (o queda 1, a primeira candidata e a refeita, pose a pose; na
  primeira linha, a vista aprovada no lugar do queda 1),
  `queda-vista-poses.png` (cada pose com a construção em cima e o acabamento embaixo) e `queda-vista-trajetorias.png`
  (a pega, os pulsos e o ombro de Morel, um ponto por pose, nos dois desfechos).
`--conferir` refaz o desenho em código (`poses.py`) e compara, camada a camada, com as células da fonte: diz o que foi
retocado à mão na fonte (ou o que mudou no código desde a montagem)."""
import json
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import geometria as G  # noqa: E402
import poses as PO  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = PO.FONTE
SAIDA = AQUI.parents[1] / "camadas" / "morel-vista"
FORA = ["guia", "juntas", "fogo", "chamas"]
RECORTE = (140, 0, 300, 96)  # a disputa inteira, com Morel, nas folhas


def achatar(tmp):
    cmd = [aseprite(), "-b"]
    for c in FORA:
        cmd += ["--ignore-layer", c]
    subprocess.run(cmd + [str(FONTE), "--save-as", str(tmp / "q{frame}.png")], capture_output=True, text=True)
    qs = sorted(tmp.glob("q*.png"), key=lambda p: int(p.stem[1:]))
    return [Image.open(q).convert("RGBA") for q in qs]


def main():
    nomes = [p[0] for p in G.POSES]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        qs = achatar(tmp)
        cel = PO.fa.celulas(FONTE, tmp / "cel")
        guias = [Image.open(cel / f"guia-{i}.png").convert("RGBA") for i in range(len(qs))]
    if len(qs) != len(nomes):
        sys.exit(f"a fonte tem {len(qs)} quadros e geometria.POSES {len(nomes)}")
    base = np.array(qs[0])
    caixa = None
    for q in qs[1:]:
        d = np.nonzero((np.array(q) != base).any(2))
        if len(d[0]):
            c = (d[1].min(), d[0].min(), d[1].max() + 1, d[0].max() + 1)
            caixa = c if caixa is None else (min(caixa[0], c[0]), min(caixa[1], c[1]), max(caixa[2], c[2]),
                                             max(caixa[3], c[3]))
    x0, y0, x1, y1 = (int(v) for v in caixa)
    w, h = x1 - x0, y1 - y0
    qs[0].save(SAIDA / "queda-vista-fundo.png", optimize=True)
    tira = Image.new("RGBA", (w * len(qs), h))
    for i, q in enumerate(qs):
        tira.paste(q.crop((x0, y0, x1, y1)), (w * i, 0))
    tira.save(SAIDA / "queda-vista.png", optimize=True)
    idx = {n: i for i, n in enumerate(nomes)}
    linha = lambda r: [idx[n] for n, k in r for _ in range(k)]  # noqa: E731
    dados = {"caixa": [x0, y0, w, h], "poses": nomes,
             "desfechos": {k: {"tempo": linha(G.CICLO[k]), "reduzido": linha(G.REDUZIDO[k]),
                               "parada": idx["disputa"]} for k in G.CICLO}}
    (SAIDA / "queda-vista.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    folhas(qs, guias, nomes)
    print(f"queda-vista: {len(qs)} poses, caixa {dados['caixa']}, "
          + ", ".join(f"{k} {len(v['tempo'])} tiques" for k, v in dados["desfechos"].items()))


def folhas(qs, guias, nomes):
    idx = {n: i for i, n in enumerate(nomes)}
    cam = SAIDA
    aprovada = Image.open(cam / "parada.png").convert("RGBA")
    q1 = Image.open(cam / "queda.png").convert("RGBA")
    q1p = [q1.crop((320 * i, 0, 320 * i + 320, 96)) for i in range(3)]
    # a primeira candidata (Morel na postura da conversa), camadas/morel-vista-qv1
    v1 = cam.parent / "morel-vista-qv1"
    d1 = json.loads((v1 / "queda-vista.json").read_text(encoding="utf-8"))
    f1, t1 = Image.open(v1 / "queda-vista-fundo.png").convert("RGBA"), Image.open(v1 / "queda-vista.png").convert("RGBA")
    x, y, w1, h1 = d1["caixa"]

    def antiga(nome):
        im = f1.copy()
        i = d1["poses"].index(nome)
        im.alpha_composite(t1.crop((i * w1, 0, i * w1 + w1, h1)), (x, y))
        return im
    R = RECORTE
    w = R[2] - R[0]
    # a comparação: em cada linha, o queda 1 (na primeira, a vista aprovada), a primeira candidata e a refeita
    linhas = [(aprovada, antiga("firma"), qs[idx["firma"]]), (q1p[0], antiga("disputa"), qs[idx["disputa"]]),
              (q1p[1], antiga("nos_fim"), qs[idx["nos_fim"]]), (q1p[2], antiga("morel_fim"), qs[idx["morel_fim"]])]
    comp = Image.new("RGBA", (3 * w + 8, 4 * 96 + 6), (24, 22, 20, 255))
    for i, trio in enumerate(linhas):
        for k, im in enumerate(trio):
            comp.alpha_composite(im.crop(R), (k * (w + 4), i * 98))
    comp.save(cam / "queda-vista-comparacao.png", optimize=True)
    # as poses: em cima a construção sobre o quadro escurecido, embaixo o acabamento (recorte de 100×96)
    Rp = (160, 0, 260, 96)
    wp, col = Rp[2] - Rp[0], 12
    lin = (len(qs) + col - 1) // col
    pos = Image.new("RGBA", (col * (wp + 2), lin * 2 * 98), (24, 22, 20, 255))
    for i, q in enumerate(qs):
        x, y = (i % col) * (wp + 2), (i // col) * 196
        esc = Image.blend(q, Image.new("RGBA", q.size, (0, 0, 0, 255)), 0.55)
        esc.alpha_composite(guias[i])
        pos.alpha_composite(esc.crop(Rp), (x, y))
        pos.alpha_composite(q.crop(Rp), (x, y + 98))
    pos.save(cam / "queda-vista-poses.png", optimize=True)
    # as trajetórias: a pega (amarelo), o pulso dele (laranja), o nosso (azul), o ombro dele (vermelho), um ponto por
    # pose na ordem do desfecho, sobre a disputa escurecida
    P = G.todas()
    tr = Image.new("RGBA", (2 * w + 4, 96), (24, 22, 20, 255))
    for k, lado in enumerate(("nos", "morel")):
        esc = Image.blend(qs[idx["disputa"]], Image.new("RGBA", (320, 96), (0, 0, 0, 255)), 0.6)
        d = ImageDraw.Draw(esc)
        vistos = []
        for n, _ in G.CICLO[lado]:
            if n not in vistos:
                vistos.append(n)
        for chave, cor in (("S", (255, 70, 60)), ("W", (255, 160, 60)), ("Wn", (90, 150, 255)), ("P", (255, 230, 60))):
            pts = [tuple(int(v) for v in P[n]["tela"][chave]) for n in vistos]
            d.line(pts, fill=cor[:3] + (110,), width=1)
            for p in pts:
                esc.putpixel(p, cor + (255,))
        tr.alpha_composite(esc.crop(R), (k * (w + 4), 0))
    tr.save(cam / "queda-vista-trajetorias.png", optimize=True)


def conferir():
    """O desenho em código (poses.py) contra as células da fonte: quantos pixels diferem por camada e quadro."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        cel = PO.fa.celulas(FONTE, tmp / "cel")
        vcel = PO.fa.celulas(PO.VISTA, tmp / "vcel")
        dif = 0
        for i, (nome, c) in enumerate(PO.poses(vcel)):
            for camada in PO.CAMADAS:
                arq = cel / f"{camada}-{i}.png"
                a = np.array(Image.open(arq).convert("RGBA")) if arq.exists() else np.zeros((96, 320, 4), np.uint8)
                b = np.zeros((96, 320, 4), np.uint8)
                for (x, y), cor in (c.get(camada) or {}).items():
                    if 0 <= x < 320 and 0 <= y < 96:
                        b[y, x] = cor if len(cor) == 4 else tuple(cor) + (255,)
                a[a[:, :, 3] == 0] = 0
                n = int((a != b).any(2).sum())
                if n:
                    dif += n
                    print(f"  {nome} {camada}: {n} px diferentes")
    print("a fonte é igual ao desenho" if not dif else f"{dif} px diferentes (retoques na fonte ou mudanças no código)")


if __name__ == "__main__":
    conferir() if "--conferir" in sys.argv else main()
