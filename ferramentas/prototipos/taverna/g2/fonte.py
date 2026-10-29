"""A fonte em camadas da G refinada (G2), feita a partir da fonte da G, e as camadas que a demonstração lê.

    python ferramentas/prototipos/taverna/g2/fonte.py --criar [--refazer]   # a fonte da G + os retoques (retoques.py)
    python ferramentas/prototipos/taverna/g2/fonte.py [--conferir]           # exporta da fonte para camadas/g2

`--criar` lê as células de `g/aseprite/taverna-g.aseprite` como estão, aplica os retoques seletivos (`retoques.py`) e
grava `g2/aseprite/taverna-g2.aseprite`, com as mesmas camadas da G (fundo, fogo, lampiao, caldeirao, taverneiro,
frente). Depois de criada, ela é a autoridade: os retoques à mão se fazem nela, e `--criar` não a sobrescreve sem
`--refazer`. A exportação grava em `camadas/g2/` o que `tela/cena-taverna-b.js` lê (`estatica("g2")`); `--conferir`
compara com a fonte da G mais os retoques do script (as diferenças, se houver, são os retoques à mão)."""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))

from g import fonte as F  # noqa: E402
from g2 import retoques as R  # noqa: E402

FONTE = AQUI / "aseprite" / "taverna-g2.aseprite"
SAIDA = AQUI.parent / "camadas" / "g2"


def quadros_retocados():
    """{camada: [imagem, ...]}: as células da fonte da G com os retoques da G2."""
    q, feitos = R.aplicar(F.ler_fonte(F.FONTE))
    print("retoques:", ", ".join(f"{k} {v} px" for k, v in feitos.items()))
    return q


if __name__ == "__main__":
    F.principal(FONTE, SAIDA, quadros_retocados)
