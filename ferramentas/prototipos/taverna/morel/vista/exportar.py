"""Exporta a vista diante de Morel (a fonte `morel/vista/morel-vista.aseprite`) para `camadas/morel-vista/`.

    python ferramentas/prototipos/taverna/morel/vista/exportar.py

A fonte é a autoridade: este script só a lê (o Aseprite em lote achata cada quadro com as camadas de luz, `sombra` em
multiplicar e `brilho` em somar, e exporta as células de cada camada) e recorta as peças que a cena desenha:
- `fundo.png`: o quadro 1 sem as camadas animadas, a mesa e as mãos (a sala, o balcão, a cadeira);
- `chamas.png`: 4 quadros, o fogo da lareira (onde o balcão não o cobre) e a chama da vela (a cena a desenha
  depois da mesa: a base da chama encosta no pavio);
- `taverneiro.png`: as poses do taverneiro ao fundo (só o que o balcão não cobre), recortadas na caixa delas;
- `morel.png`: as poses de Morel, recortadas na caixa delas, em duas faixas: a de cima é o corpo e a cabeça (atrás da
  mesa; o corpo se inclina para a tigela enquanto ele come), a de baixo o braço da colher (por cima da mesa);
- `frente.png`: a mesa com o que está nela e o braço que descansa;
- `rotina.json`: as caixas, as linhas do tempo (um índice por tique de 100 ms; `ROTINA_MOREL`, `ROTINA_TAVERNEIRO`), as
  poses paradas;
- `parada.png`: a vista inteira na pose parada (Morel descansando, o taverneiro na primeira pose), para a inspeção
  ampliada do painel;
- `construcao.png` (inspeção): em cima, as cinco poses do estudo de construção (`morel/estudo-construcao/`, formas
  simples, as juntas da guia); embaixo, as mesmas poses vestidas na vista;
- `trajetorias.png` (inspeção): uma volta da colher sobre a pose parada escurecida, à esquerda a v2 (as juntas
  medidas nela, registradas em `_JUNTAS_V2`), à direita a atual (as juntas da camada `guia` da fonte): o cotovelo em
  verde, o pulso em azul, a ponta da colher em amarelo, um ponto por pose.
A arte não sai daqui: as folhas de inspeção só recortam a fonte e ligam as juntas da guia."""
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
ANIMADAS = ["guia", "fogo", "chamas", "taverneiro", "morel_corpo", "morel_cabeca", "morel_braco", "mesa", "maos"]

# Morel, pose a pose (o quadro da fonte menos 1; os nomes estão nas etiquetas da fonte). As juntas de cada pose vêm do
# estudo de construção (morel/estudo-construcao/): braço 28 e antebraço 22 no espaço, o que muda na tela é o escorço.
# 0 recolhe e 1 recolhe2 (a concha no caldo), 2 sai, 3 sobe1, 4 sobe2, 5 levanta (a colher cheia diante do peito),
# 6 sobe3, 7 sobe4, 8 sobe5 (a cabeça desce ao encontro da colher), 9 boca, 10 desce1, 11 desce2, 12 desce2b,
# 13 desce2c, 14 retorna, 15 desce3, 16 desce4, 17 repousa (a mão na borda da tigela), 18 mastiga, 19 olha (para
# quem está à mesa). De um desenho ao seguinte a mão e o cotovelo andam no máximo 6 px (a v2 saltava 9 a 11 px a
# cada 200 ms). O tempo segue o da curandeira e o do balcão: as poses das pontas de cada trecho (sair da tigela, a
# pausa em `levanta` antes da boca, chegar à boca, pousar) seguram 2 tiques, as passagens do meio 1, a boca 6; a
# última pose (repousa) emenda na primeira (recolhe) com a mão 1 px e o corpo 1 px.
_VOLTA = [(0, 4), (1, 3), (0, 3), (1, 3), (0, 2),
          (2, 2), (3, 1), (4, 1), (5, 2), (6, 1), (7, 1), (8, 2), (9, 6),
          (10, 2), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 2),
          (17, 3), (18, 3), (17, 3), (18, 3), (17, 3), (18, 3), (17, 8)]
ROTINA_MOREL = _VOLTA + _VOLTA + [(19, 20), (17, 4)]
PARADA_MOREL = 17  # repousando, os olhos na tigela: ele come sem levantar os olhos do prato
# o estudo de construção e as poses dele na vista (o quadro da fonte menos 1): recolher, levantar, boca, retornar,
# repousar
ESTUDO = AQUI.parent / "estudo-construcao" / "morel-construcao.aseprite"
CHAVES = [0, 5, 9, 14, 17]
RECORTE = (172, 0, 268, 96)  # Morel inteiro, 96×96
# a v2 (morel/vista-v2), medida nos quadros dela: (cotovelo, pulso) por pose, na ordem de uma volta (cada pose 2 tiques)
_JUNTAS_V2 = [((183, 65), (199, 69)), ((184, 65), (199, 58)), ((191, 58), (200, 49)), ((199, 52), (202, 40)),
              ((206, 47), (202, 31)), ((199, 52), (202, 40)), ((191, 58), (200, 49)), ((184, 65), (199, 58)),
              ((183, 65), (199, 70))]
_COR_JUNTA = {(48, 255, 96): "cotovelo", (48, 128, 255): "pulso", (255, 224, 48): "ponta"}
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
        cab = [_mascara(Q[k], alfa("morel_corpo", k) | alfa("morel_cabeca", k)) for k in range(n)]
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
        # as folhas de inspeção
        subprocess.run([ase, "-b", str(ESTUDO), "--save-as", str(tmp / "e{frame1}.png")], capture_output=True, text=True)
        est = sorted(tmp.glob("e*.png"), key=lambda p: int(p.stem[1:]))
        folha = Image.new("RGBA", (96 * len(CHAVES), 192))
        for i, k in enumerate(CHAVES):
            folha.paste(Image.open(est[i]).convert("RGBA").crop(RECORTE), (96 * i, 0))
            folha.paste(Q[k].crop(RECORTE), (96 * i, 96))
        folha.save(SAIDA / "construcao.png", optimize=True)
        juntas = []
        for k in range(n):
            g = np.array(Image.open(celulas / f"guia-{k}.png").convert("RGB")) if (celulas / f"guia-{k}.png").exists() else None
            j = {}
            if g is not None:
                for cor, nome in _COR_JUNTA.items():
                    ys, xs = np.nonzero((g == cor).all(2))
                    if len(xs):
                        j[nome] = (int(xs[0]), int(ys[0]))
            juntas.append(j)
        volta = [k for k, _ in _VOLTA if k in range(2, 18)]
        trilhas_v3 = {nome: [juntas[k][nome] for k in [17] + volta if nome in juntas[k]] for nome in _COR_JUNTA.values()}
        trilhas_v2 = {"cotovelo": [e for e, _ in _JUNTAS_V2], "pulso": [w for _, w in _JUNTAS_V2]}
        v2 = Image.open(SAIDA.parent / "morel-vista-v2" / "parada.png").convert("RGBA")
        traj = Image.new("RGBA", (192, 96))
        for i, (base, trilhas) in enumerate([(v2, trilhas_v2), (parada, trilhas_v3)]):
            b = np.array(base.crop(RECORTE).convert("RGB")).astype(float) * 0.35
            for nome, pts in trilhas.items():
                cor = [c for c, nn in _COR_JUNTA.items() if nn == nome][0]
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):  # a linha entre duas poses seguidas, mais apagada
                    m = max(abs(x1 - x0), abs(y1 - y0), 1)
                    for t in range(m + 1):
                        x, y = round(x0 + (x1 - x0) * t / m) - RECORTE[0], round(y0 + (y1 - y0) * t / m)
                        if 0 <= x < 96 and 0 <= y < 96:
                            b[y, x] = np.array(cor) * 0.55
                for x, y in pts:  # o ponto de cada pose
                    if 0 <= x - RECORTE[0] < 96 and 0 <= y < 96:
                        b[y, x - RECORTE[0]] = cor
            traj.paste(Image.fromarray(b.astype(np.uint8), "RGB").convert("RGBA"), (96 * i, 0))
        traj.save(SAIDA / "trajetorias.png", optimize=True)
        print("camadas/morel-vista: fundo, chamas, taverneiro, morel, frente, parada, rotina.json, construcao e trajetorias;",
              f"Morel {len(rotina['morel']['tempo'])} tiques, taverneiro {len(rotina['taverneiro']['tempo'])}")


if __name__ == "__main__":
    main()
