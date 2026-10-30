"""Exporta a vista diante de Morel (a fonte `morel/vista/morel-vista.aseprite`) para `camadas/morel-vista/`.

    python ferramentas/prototipos/taverna/morel/vista/exportar.py

A fonte é a autoridade: este script só a lê (o Aseprite em lote achata cada quadro com as camadas de luz, `sombra` em
multiplicar e `brilho` em somar, e exporta as células de cada camada) e recorta as peças que a cena desenha:
- `fundo.png`: o quadro 1 sem as camadas animadas, a mesa e as mãos (a sala, o balcão, a cadeira, o corpo de Morel);
- `chamas.png`: 4 quadros, o fogo da lareira (onde o balcão não o cobre) e a chama da vela (a cena a desenha
  depois da mesa: a base da chama encosta no pavio);
- `taverneiro.png`: as poses do taverneiro ao fundo (só o que o balcão não cobre), recortadas na caixa delas;
- `morel.png`: as poses de Morel (a cabeça e o braço da colher), recortadas na caixa delas, em duas faixas: a de cima é a
  cabeça (atrás da mesa), a de baixo o braço (por cima da mesa);
- `frente.png`: a mesa com o que está nela e o braço que descansa;
- `rotina.json`: as caixas, as linhas do tempo (um índice por tique de 100 ms; `ROTINA_MOREL`, `ROTINA_TAVERNEIRO`), as
  poses paradas;
- `parada.png`: a vista inteira na pose parada (Morel descansando, o taverneiro na primeira pose), para a inspeção
  ampliada do painel.
Nada aqui desenha."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "morel-vista.aseprite"
SAIDA = AQUI.parents[1] / "camadas" / "morel-vista"
LUA = RAIZ / "ferramentas" / "prototipos" / "hud" / "forja" / "h2" / "aseprite" / "exportar_forja.lua"
ANIMADAS = ["guia", "fogo", "chamas", "taverneiro", "morel_cabeca", "morel_braco", "mesa", "maos"]

# Morel, pose a pose (o quadro da fonte menos 1): 0 recolhe, 1 recolhe (a colher no fundo da tigela), 7 a mão saindo
# da tigela (o cotovelo ainda no tampo), 2 a mão no meio do caminho, 8 a mão no peito (o cotovelo sai do tampo), 3 a
# colher na boca (a cabeça desce 1 px ao encontro dela), 9/10/11 a volta com a colher vazia, 4 descansa, 5 mastiga (o
# queixo 1 px abaixo), 6 ergue os olhos (a cabeça sobe 1 px). Uma volta sem olhar e outra que termina olhando para quem
# está à mesa; a última pose (descansa) emenda na primeira (recolhe) com a mão 1 px.
_VOLTA = [(0, 4), (1, 3), (0, 3), (1, 3), (0, 2), (7, 2), (2, 2), (8, 2), (3, 7), (9, 2), (10, 2), (11, 2), (4, 3),
          (5, 3), (4, 3), (5, 3), (4, 3), (5, 3), (4, 10)]
ROTINA_MOREL = _VOLTA + _VOLTA + [(6, 20), (4, 4)]
PARADA_MOREL = 4  # descansando, os olhos na tigela: ele come sem levantar os olhos do prato
# o taverneiro ao fundo: duas poses (esfrega), a pausa longa
ROTINA_TAVERNEIRO = [(0, 5), (1, 4), (0, 4), (1, 4), (0, 3), (1, 3), (0, 14)]


def _linha(rotina):
    t = []
    for i, n in rotina:
        t += [i] * n
    return t


def _caixa(ims):
    caixas = [im.getbbox() for im in ims if im.getbbox()]
    x0, y0 = min(c[0] for c in caixas), min(c[1] for c in caixas)
    x1, y1 = max(c[2] for c in caixas), max(c[3] for c in caixas)
    return x0, y0, x1 - x0, y1 - y0


def _mascara(im, alfa):
    a = np.array(im.convert("RGBA"))
    a[~alfa] = 0
    return Image.fromarray(a, "RGBA")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        ase = aseprite()
        # cada quadro achatado, com a luz (sem a guia)
        subprocess.run([ase, "-b", "--ignore-layer", "guia", str(FONTE), "--save-as", str(tmp / "q{frame1}.png")],
                       capture_output=True, text=True)
        # o fundo: o quadro 1 sem as camadas animadas, a mesa e as mãos
        cmd = [ase, "-b"]
        for n in ANIMADAS:
            cmd += ["--ignore-layer", n]
        subprocess.run(cmd + [str(FONTE), "--frame-range", "0,0", "--save-as", str(tmp / "fundo.png")],
                       capture_output=True, text=True)
        # a frente: o quadro 1 sem o braço da colher e as chamas (a mesa e as mãos sem nada por cima)
        subprocess.run([ase, "-b", "--ignore-layer", "guia", "--ignore-layer", "morel_braco", "--ignore-layer", "chamas",
                        str(FONTE), "--frame-range", "0,0", "--save-as", str(tmp / "mesa.png")], capture_output=True,
                       text=True)
        # as células de cada camada, quadro a quadro (as máscaras)
        script = tmp / "exportar.lua"
        shutil.copy(LUA, script)
        celulas = tmp / "cel"
        celulas.mkdir()
        r = subprocess.run([ase, "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={celulas}",
                            "--script", str(script)], capture_output=True, text=True)
        if "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não exportou as células:\n{r.stdout}{r.stderr}")
        quadros = sorted(tmp.glob("q*.png"), key=lambda p: int(p.stem[1:]))
        Q = [Image.open(p).convert("RGBA") for p in quadros]
        fundo = Image.open(next(tmp.glob("fundo*.png"))).convert("RGBA")
        mesa = Image.open(next(tmp.glob("mesa*.png"))).convert("RGBA")

        def alfa(camada, q):
            p = celulas / f"{camada}-{q}.png"
            if not p.exists():
                return np.zeros((Q[0].height, Q[0].width), bool)
            return np.array(Image.open(p).convert("RGBA"))[:, :, 3] > 0

        balcao = alfa("balcao", 0)
        SAIDA.mkdir(parents=True, exist_ok=True)
        fundo.save(SAIDA / "fundo.png", optimize=True)
        frente = _mascara(mesa, alfa("mesa", 0) | alfa("maos", 0))
        frente.save(SAIDA / "frente.png", optimize=True)
        # as chamas: 4 quadros
        tira = Image.new("RGBA", (320 * 4, 96))
        for i in range(4):
            tira.paste(_mascara(Q[i], (alfa("fogo", i) & ~balcao) | alfa("chamas", i)), (320 * i, 0))
        tira.save(SAIDA / "chamas.png", optimize=True)
        # o taverneiro: as duas poses (quadros 1 e 2), só o que o balcão não cobre
        tav = [_mascara(Q[j], alfa("taverneiro", j) & ~balcao) for j in range(2)]
        x, y, w, h = _caixa(tav)
        t = Image.new("RGBA", (w * 2, h))
        for j, im in enumerate(tav):
            t.paste(im.crop((x, y, x + w, y + h)), (w * j, 0))
        t.save(SAIDA / "taverneiro.png", optimize=True)
        caixa_tav = [x, y, w, h]
        # Morel: a cabeça e o braço da colher, pose a pose (um quadro da fonte por pose)
        n = len(Q)
        cab = [_mascara(Q[k], alfa("morel_cabeca", k)) for k in range(n)]
        bra = [_mascara(Q[k], alfa("morel_braco", k)) for k in range(n)]
        x, y, w, h = _caixa(cab + bra)
        m = Image.new("RGBA", (w * n, h * 2))
        for k in range(n):
            m.paste(cab[k].crop((x, y, x + w, y + h)), (w * k, 0))
            m.paste(bra[k].crop((x, y, x + w, y + h)), (w * k, h))
        m.save(SAIDA / "morel.png", optimize=True)
        rotina = {
            "morel": {"caixa": [x, y, w, h], "tempo": _linha(ROTINA_MOREL), "parada": PARADA_MOREL, "faixas": 2},
            "taverneiro": {"caixa": caixa_tav, "tempo": _linha(ROTINA_TAVERNEIRO), "parada": 0},
        }
        parada = fundo.copy()
        parada.alpha_composite(tav[0])
        parada.alpha_composite(cab[PARADA_MOREL])
        parada.alpha_composite(frente)
        parada.alpha_composite(tira.crop((320, 0, 640, 96)))
        parada.alpha_composite(bra[PARADA_MOREL])
        parada.save(SAIDA / "parada.png", optimize=True)
        with open(SAIDA / "rotina.json", "w", encoding="utf-8") as f:
            json.dump(rotina, f, separators=(",", ":"))
        print("camadas/morel-vista: fundo, chamas, taverneiro, morel, frente, parada, rotina.json;",
              f"Morel {len(rotina['morel']['tempo'])} tiques, taverneiro {len(rotina['taverneiro']['tempo'])}")


if __name__ == "__main__":
    main()
