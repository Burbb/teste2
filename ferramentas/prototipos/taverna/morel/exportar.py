"""Exporta o estudo de Morel (a fonte em camadas `morel/aseprite/morel-mesa.aseprite`) para `camadas/morel/estudo.png`.

    python ferramentas/prototipos/taverna/morel/exportar.py

A fonte é a autoridade: este script só a lê, pelo Aseprite em lote, e achata as camadas visíveis com os modos de
mistura delas (a `sombra` multiplica, o `brilho` soma), sem a camada `guia` (a referência reduzida, oculta). Nada aqui
desenha: o estudo foi construído no editor."""
import pathlib
import subprocess
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "aseprite" / "morel-mesa.aseprite"
SAIDA = AQUI.parent / "camadas" / "morel" / "estudo.png"


if __name__ == "__main__":
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([aseprite(), "-b", "--ignore-layer", "guia", str(FONTE), "--save-as", str(SAIDA)],
                       capture_output=True, text=True)
    if not SAIDA.exists():
        sys.exit(f"O Aseprite não exportou:\n{r.stdout}{r.stderr}")
    im = Image.open(SAIDA)
    print(f"{SAIDA.relative_to(RAIZ)}: {im.size[0]}×{im.size[1]}")
