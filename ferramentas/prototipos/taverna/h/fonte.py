"""A fonte em camadas da candidata H e as camadas que a demonstração lê, pelo mesmo caminho da G (`g/fonte.py`).

    python ferramentas/prototipos/taverna/h/fonte.py --criar [--refazer]   # gera a fonte a partir do código
    python ferramentas/prototipos/taverna/h/fonte.py [--conferir]           # exporta da fonte para camadas/h

A fonte é `h/aseprite/taverna-h.aseprite` (320×96, 4 quadros), com as camadas da G: fundo, fogo, lampiao, caldeirao,
taverneiro e frente. Depois de criada, ela é a autoridade: os retoques se fazem nela, e `--criar` não a sobrescreve
sem `--refazer`. A exportação grava em `camadas/h/` o que `tela/cena-taverna-b.js` lê (`estatica("h")`); `--conferir`
compara com o desenho do código."""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))

from g import fonte as F  # noqa: E402
from h import desenho as D, taverneiro as T  # noqa: E402

FONTE = AQUI / "aseprite" / "taverna-h.aseprite"
SAIDA = AQUI.parent / "camadas" / "h"


def quadros_do_codigo():
    """{camada: [imagem, ...]}: o que o código da H desenha, quadro a quadro."""
    return {"fundo": [D.fundo().imagem()], "fogo": [D.fogo(i).imagem() for i in range(4)],
            "lampiao": [D.lampiao_chama(i).imagem() for i in range(4)], "caldeirao": [D.camada_caldeirao().imagem()],
            "taverneiro": [T.camada().imagem()], "frente": [D.frente().imagem()]}


if __name__ == "__main__":
    F.principal(FONTE, SAIDA, quadros_do_codigo)
