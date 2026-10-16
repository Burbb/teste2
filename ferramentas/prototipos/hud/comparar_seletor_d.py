"""Monta as comparações do seletor D (faixas de tinta) a partir de fotografar_seletor_d.mjs (capturas-seletor-d/), em
tamanho real (nada ampliado nem reduzido; as telas inteiras ficam nos arquivos <janela>-<luta>-<versão>-tela.png):
  - <janela>-<luta>-comparacao.png: o seletor de hoje e o D, abertos na mesma luta, lado a lado;
  - <janela>-<luta>-estados.png (1500×950 e 1280×720): os estados do D (o mouse com a dica, a indisponível, o
    pressionado, o foco do teclado ao abrir pela tecla e depois das setas);
  - comportamentos.png: a entrada fotografada aos 40 ms, com movimento e com movimento reduzido, e o pressionado sem
    deslocamento.

    python ferramentas/prototipos/hud/comparar_seletor_d.py [pasta]   (padrão: capturas-seletor-d/)
"""

import pathlib
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comparar_seletor import grade  # noqa: E402  (a mesma montagem das propostas A, B e C)

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "capturas-seletor-d"
LUTAS = ("guerreiro", "arqueiro", "mago", "capacidade")
ESTADOS = (("2-mouse", "mouse (com a dica)"), ("3-indisponivel", "mouse na indisponível"), ("4-pressionado", "pressionado"),
           ("5-teclado", "aberto pela tecla 2"), ("6-setas", "depois das setas (baixo, direita)"))


def abrir(nome):
    p = FOTOS / f"{nome}.png"
    return Image.open(p).convert("RGB") if p.exists() else None


def main():
    feitos = 0
    for jan in ("normal", "grande", "baixa"):
        for luta in LUTAS:
            base = f"{jan}-{luta}"
            if not abrir(f"{base}-d-tela"):
                continue
            rot = lambda r: f"{jan} · {luta} · {r}"
            grade([(abrir(f"{base}-{v}-1-aberto"), rot(r)) for v, r in (("atual", "o jogo hoje"), ("d", "D · faixas de tinta"))], 2).save(FOTOS / f"{base}-comparacao.png")
            if jan != "grande":  # em 1920×1080 os estados são os mesmos, mais largos (ficam nos arquivos)
                cel = [(img, rot(r)) for e, r in ESTADOS if (img := abrir(f"{base}-d-{e}"))]
                grade(cel, 2).save(FOTOS / f"{base}-estados.png")
            feitos += 1
    cel = [(img, r) for n, r in (("comportamento-d-entrada-40ms", "D · a entrada aos 40 ms"), ("comportamento-d-reduzido-40ms", "D · movimento reduzido, 40 ms"),
                                 ("comportamento-d-reduzido-pressionado", "D · movimento reduzido, pressionado")) if (img := abrir(n))]
    if cel:
        grade(cel, 1).save(FOTOS / "comportamentos.png")
    print(f"{feitos} conjuntos de comparações em {FOTOS}")


if __name__ == "__main__":
    main()
