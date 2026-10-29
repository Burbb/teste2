"""A fonte em camadas da G3 (a G2 aprovada com as correções locais), feita a partir da fonte da G2.

    python ferramentas/prototipos/taverna/g3/fonte.py --criar [--refazer]   # a fonte da G2 + as correções (retoques.py)
    python ferramentas/prototipos/taverna/g3/fonte.py [--conferir]           # exporta da fonte para camadas/g3

`--criar` lê as células de `g2/aseprite/taverna-g2.aseprite` como estão, aplica `retoques.py` e grava
`g3/aseprite/taverna-g3.aseprite` (as camadas da G). Depois de criada, ela é a autoridade: os retoques à mão se fazem
nela, e `--criar` não a sobrescreve sem `--refazer`. A exportação grava em `camadas/g3/`; `--conferir` compara com a
fonte da G2 mais as correções do script."""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))

from g import fonte as F  # noqa: E402
from g2 import fonte as F2  # noqa: E402
from g3 import retoques as R  # noqa: E402

FONTE = AQUI / "aseprite" / "taverna-g3.aseprite"
SAIDA = AQUI.parent / "camadas" / "g3"


def quadros_corrigidos():
    """{camada: [imagem, ...]}: as células da fonte da G2 com as correções da G3."""
    q, feitos = R.aplicar(F.ler_fonte(F2.FONTE))
    print("correções:", ", ".join(f"{k} {v} px" for k, v in feitos.items()))
    return q


if __name__ == "__main__":
    F.principal(FONTE, SAIDA, quadros_corrigidos)
