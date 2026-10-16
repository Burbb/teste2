"""Monta a comparação entre a D atual e a D refinada (bordas das faixas e fundo) a partir de fotografar_seletor_d.mjs
com VERSOES=d,d2 RODADA=1 (capturas-seletor-d2/), tudo em tamanho real (as telas inteiras ficam nos arquivos
<janela>-<luta>-<versão>-tela.png):
  - <janela>-<luta>-fundo.png: o seletor e o registro real por baixo dele, recortados da tela inteira, D atual em cima
    e D refinada embaixo (a integração do fundo e a borda de baixo);
  - <janela>-<luta>-estados.png: o seletor parado, o destaque claro (mouse, com a dica) e o mouse numa indisponível,
    D atual à esquerda e D refinada à direita;
  - reduzido.png: o movimento reduzido (aberto aos 40 ms e o pressionado), as duas.

    python ferramentas/prototipos/hud/comparar_seletor_d2.py [pasta]   (padrão: capturas-seletor-d2/)
"""

import json
import pathlib
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comparar_seletor import grade  # noqa: E402  (a mesma montagem das outras comparações)

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "capturas-seletor-d2"
VERSOES = (("d", "D atual"), ("d2", "D refinada"))
ESTADOS = (("1-aberto", "parado"), ("2-mouse", "destaque claro (mouse, com a dica)"), ("3-indisponivel", "mouse na indisponível"))


def abrir(nome):
    p = FOTOS / f"{nome}.png"
    return Image.open(p).convert("RGB") if p.exists() else None


def main():
    medidas = {r["nome"]: r for r in json.loads((FOTOS / "relatorio.json").read_text())["relatorio"]}
    feitos = 0
    for jan in ("normal", "baixa"):
        for luta in ("guerreiro", "mago", "arqueiro"):
            base = f"{jan}-{luta}"
            if not abrir(f"{base}-d-tela"):
                continue
            rot = lambda r: f"{jan} · {luta} · {r}"
            fundo = []
            for v, r in VERSOES:
                m = medidas[f"{base}-{v}"]
                x, y = (int(n) for n in m["posicao"].split(","))
                w, h = (int(n) for n in m["tamanho"].split("×"))
                tela = abrir(f"{base}-{v}-tela")
                fundo.append((tela.crop((max(0, x - 24), max(0, y - 40), min(tela.width, x + w + 24), min(tela.height, y + h + 190))), rot(f"{r} · o seletor e o registro por baixo")))
            grade(fundo, 1).save(FOTOS / f"{base}-fundo.png")
            grade([(abrir(f"{base}-{v}-{e}"), rot(f"{r} · {er}")) for e, er in ESTADOS for v, r in VERSOES if abrir(f"{base}-{v}-{e}")], 2).save(FOTOS / f"{base}-estados.png")
            feitos += 1
    cel = [(img, f"{r} · {er}") for n, er in (("reduzido-40ms", "movimento reduzido, aberto aos 40 ms"), ("reduzido-pressionado", "movimento reduzido, pressionado"))
           for v, r in VERSOES if (img := abrir(f"comportamento-{v}-{n}"))]
    if cel:
        grade(cel, 2).save(FOTOS / "reduzido.png")
    print(f"{feitos} conjuntos de comparações em {FOTOS}")


if __name__ == "__main__":
    main()
