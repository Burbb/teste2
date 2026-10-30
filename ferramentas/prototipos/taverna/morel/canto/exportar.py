"""Exporta a cena de Morel no canto (a fonte `canto.aseprite`) para `camadas/morel-canto/`.

    python ferramentas/prototipos/taverna/morel/canto/exportar.py             # exporta
    python ferramentas/prototipos/taverna/morel/canto/exportar.py --conferir  # a fonte contra o desenho em código

A fonte é a autoridade: este script só lê as células dela (pelo Aseprite em lote) e monta as peças que a cena desenha,
as mesmas da vista aprovada (`morel/vista/exportar.py`), para a tela e a reação ao pagamento serem as mesmas:
- `fundo.png` (as paredes e os esteios), `frente.png` (o tampo e os objetos), `chamas.png` (a chama da vela, 4 quadros);
- `morel.png`: as 20 poses recortadas na caixa delas, em duas faixas: a de cima, o que fica atrás do tampo (a espada,
  o tronco, a cabeça); a de baixo, o que fica por cima dele (os dois braços, as mãos, a colher, as ombreiras);
- `rotina.json`: a caixa, a linha do tempo (a da vista aprovada: as mesmas poses, na mesma ordem) e a pose parada;
- `moedas.png` (as moedas da vista) e `moedas.json` (o lançamento com o pouso nesta mesa, entre o pão e a tigela, e a
  reação de Morel, pelas mesmas poses);
- as folhas de inspeção: `parada.png` (a cena inteira, repousando), `comparacao.png` (a referência no lugar em que é
  transposta, em cima; a cena, embaixo) e `poses.png` (as 20 poses, recortadas em Morel)."""
import importlib.util
import json
import pathlib
import shutil
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "queda"))

import cena as CE  # noqa: E402
import fonte_aseprite as fa  # noqa: E402

SAIDA = AQUI.parents[1] / "camadas" / "morel-canto"
ATRAS = ["espada", "morel_corpo", "morel_cabeca"]
FRENTE_MOREL = ["morel_esquerdo", "morel_braco"]
PARADA = 17


def _modulo(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def celulas(tmp):
    cel = fa.celulas(CE.FONTE, pathlib.Path(tmp) / "cel")
    n = len(CE.J.ROTEIRO)

    def ler(camada, k):
        arq = cel / f"{camada}-{k}.png"
        return Image.open(arq).convert("RGBA") if arq.exists() else Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    return {c: [ler(c, k) for k in range(n)] for c in CE.CAMADAS}


def _junta(ims):
    out = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    for im in ims:
        out.alpha_composite(im)
    return out


def moedas(saida):
    """O lançamento das moedas nesta mesa (o pouso entre o pão e a tigela, na frente), pelas funções da vista."""
    M = _modulo("moedas_vista", AQUI.parent / "moedas" / "moedas.py")
    M.MOEDAS = [
        dict(fim=(128, 84), sai=(140, 106), t0=0, voo=5, escorrega=(-1, 0)),
        dict(fim=(135, 87), sai=(146, 106), t0=0, voo=4, escorrega=(1, 0)),
        dict(fim=(140, 82), sai=(148, 106), t0=1, voo=5, escorrega=(0, 0)),
        dict(fim=(132, 80), sai=(150, 106), t0=1, voo=4, escorrega=(1, 0)),
        dict(fim=(145, 86), sai=(152, 106), t0=2, voo=5, rola=(3, -1)),
    ]
    M.TAMPO = (73, 95)
    quadros = M.lancamento()
    dados = {"celula": M.CELULA,
             "desenhos": {n: [i, len(M.DESENHOS[n][0]), len(M.DESENHOS[n])] for i, n in enumerate(M.ORDEM)},
             "quadros": quadros, "reacao": M.reacao(quadros)}
    (saida / "moedas.json").write_text(json.dumps(dados, separators=(",", ":")), encoding="utf-8")
    shutil.copy(AQUI.parents[1] / "camadas" / "morel-vista" / "moedas.png", saida / "moedas.png")


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        C = celulas(tmp)
    n = len(CE.J.ROTEIRO)
    C["parede"][0].save(SAIDA / "fundo.png", optimize=True)
    _junta([C["mesa"][0], C["objetos"][0]]).save(SAIDA / "frente.png", optimize=True)
    tira = Image.new("RGBA", (320 * 4, 96))
    for q in range(4):
        tira.paste(C["chamas"][q], (320 * q, 0))
    tira.save(SAIDA / "chamas.png", optimize=True)
    atras = [_junta([C[c][k] for c in ATRAS]) for k in range(n)]
    frente = [_junta([C[c][k] for c in FRENTE_MOREL]) for k in range(n)]
    caixas = [im.getbbox() for im in atras + frente if im.getbbox()]
    x0, y0 = min(b[0] for b in caixas), min(b[1] for b in caixas)
    x1, y1 = max(b[2] for b in caixas), max(b[3] for b in caixas)
    w, h = x1 - x0, y1 - y0
    folha = Image.new("RGBA", (w * n, 2 * h))
    for k in range(n):
        folha.paste(atras[k].crop((x0, y0, x1, y1)), (k * w, 0))
        folha.paste(frente[k].crop((x0, y0, x1, y1)), (k * w, h))
    folha.save(SAIDA / "morel.png", optimize=True)
    vista = _modulo("exportar_vista", AQUI.parent / "vista" / "exportar.py")
    tempo = []
    for i, k in vista.ROTINA_MOREL:
        tempo += [i] * k
    (SAIDA / "rotina.json").write_text(json.dumps({"morel": {"caixa": [x0, y0, w, h], "tempo": tempo,
                                                             "parada": PARADA}}), encoding="utf-8")
    moedas(SAIDA)
    # as folhas de inspeção
    cena = [_junta([C["parede"][0], atras[k], C["mesa"][0], C["objetos"][0], C["chamas"][1], frente[k]])
            for k in range(n)]
    cena[PARADA].save(SAIDA / "parada.png", optimize=True)
    ref = C["guia"][0]
    comp = Image.new("RGBA", (320, 194), (24, 22, 20, 255))
    comp.alpha_composite(ref, (0, 0))
    comp.alpha_composite(cena[0], (0, 98))
    comp.save(SAIDA / "comparacao.png", optimize=True)
    R = (100, 0, 230, 96)
    poses = Image.new("RGBA", (10 * 132, 2 * 98), (24, 22, 20, 255))
    for k in range(n):
        poses.alpha_composite(cena[k].crop(R), ((k % 10) * 132, (k // 10) * 98))
    poses.save(SAIDA / "poses.png", optimize=True)
    revisao(C)
    print(f"morel-canto: {n} poses, caixa {[x0, y0, w, h]}, {len(tempo)} tiques")


def _folha(linhas, esc, fundo=(24, 22, 20, 255), vao=4):
    """Uma folha de inspeção: as linhas (listas de imagens do mesmo tamanho) ampliadas sem suavização."""
    w, h = linhas[0][0].size
    cols = max(len(lin) for lin in linhas)
    out = Image.new("RGBA", (cols * (w * esc + vao) - vao, len(linhas) * (h * esc + vao) - vao), fundo)
    for i, lin in enumerate(linhas):
        for j, im in enumerate(lin):
            out.alpha_composite(im.resize((w * esc, h * esc), Image.NEAREST), (j * (w * esc + vao), i * (h * esc + vao)))
    return out


def revisao(C):
    """As folhas da revisão (antes, a primeira candidata em `morel/canto-v1/`, em cima; depois, embaixo):
    - `revisao-mastigacao.png`: a cabeça em repouso, mastigando (as três poses de mastigar), com a colher na boca e
      olhando para quem pagou;
    - `revisao-tronco.png`: o tronco com os braços, as ombreiras e os objetos ocultos; e tudo à vista em repouso, com
      a colher na boca e olhando;
    - `revisao-parede.png`: o espaço sozinho, o espaço com as guias da sala (o horizonte, o ponto de fuga, as fugas da
      parede da esquerda e da mesa) e a cena inteira."""
    with tempfile.TemporaryDirectory() as tmp:
        V = fa.celulas(AQUI.parent / "canto-v1" / "canto.aseprite", pathlib.Path(tmp) / "v1")
        V1 = {}
        for c in CE.CAMADAS:
            V1[c] = []
            for k in range(len(CE.J.ROTEIRO)):
                arq = V / f"{c}-{k}.png"
                V1[c].append(Image.open(arq).convert("RGBA") if arq.exists() else Image.new("RGBA", (320, 96)))
    tudo = [c for c in CE.CAMADAS if c not in CE.OCULTAS]

    def cena(D, k, tirar=(), mais=()):
        return _junta([Image.new("RGBA", (320, 96), (24, 22, 20, 255))] +
                      [D[c][k if c not in ("chamas",) else 1] for c in tudo if c not in tirar] + list(mais))
    mast = [17, 18, 16, 13, 9, 19]
    _folha([[cena(D, k).crop((150, 0, 192, 50)) for k in mast] for D in (V1, C)], 4).save(
        SAIDA / "revisao-mastigacao.png", optimize=True)
    so = ("morel_esquerdo", "morel_braco", "objetos", "chamas")
    R = (110, 0, 232, 80)
    _folha([[cena(D, 17, so).crop(R)] + [cena(D, k).crop(R) for k in (17, 9, 19)] for D in (V1, C)], 3).save(
        SAIDA / "revisao-tronco.png", optimize=True)
    espaco = ("espada", "morel_corpo", "morel_cabeca", "objetos", "morel_esquerdo", "morel_braco", "chamas")
    guia = CE.ES.guia_perspectiva()
    guia.putalpha(guia.getchannel("A").point(lambda a: 170 if a else 0))
    P = (0, 0, 180, 96)
    _folha([[cena(D, 17, espaco).crop(P), cena(D, 17, espaco, [guia]).crop(P), cena(D, 17).crop(P)] for D in (V1, C)],
           2).save(SAIDA / "revisao-parede.png", optimize=True)


def conferir():
    """As células da fonte contra o desenho em código (cena.py): o que foi retocado à mão na fonte, por camada."""
    with tempfile.TemporaryDirectory() as tmp:
        C = celulas(tmp)
    dif = 0
    for k, (nome, c) in enumerate(CE.quadros()):
        for camada in CE.CAMADAS:
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
