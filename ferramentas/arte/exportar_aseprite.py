"""Exporta os ícones cuja fonte final é um .aseprite (ferramentas/arte/aseprite/<peça>/<peça>-<lado>.aseprite) para os
PNGs do jogo: o 1× pela linha de comando do Aseprite (o composto das camadas visíveis) e o @2x pela duplicação exata
(vizinho mais próximo), como o `salvar` de pixel_comum.py.

    python ferramentas/arte/exportar_aseprite.py varinha                 # grava em rpg/web/static/hud/icones/
    python ferramentas/arte/exportar_aseprite.py varinha <pasta>         # grava numa pasta qualquer (proposta)
    python ferramentas/arte/exportar_aseprite.py varinha --conferir      # exporta numa pasta temporária e compara
                                                                         # com os do jogo, byte a byte e pixel a pixel

O Aseprite vem de ASEPRITE=<executável>; sem a variável, de `aseprite` no PATH ou do lugar de instalação comum (Steam
no Windows, macOS e Linux). O jogo nunca lê nada daqui: só os PNGs exportados.
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[2]
FONTES = RAIZ / "ferramentas" / "arte" / "aseprite"
JOGO = RAIZ / "rpg" / "web" / "static" / "hud" / "icones"
LUGARES = [
    pathlib.Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Steam/steamapps/common/Aseprite/Aseprite.exe",
    pathlib.Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Aseprite/Aseprite.exe",
    pathlib.Path("/Applications/Aseprite.app/Contents/MacOS/aseprite"),
    pathlib.Path.home() / "Library/Application Support/Steam/steamapps/common/Aseprite/Aseprite.app/Contents/MacOS/aseprite",
    pathlib.Path.home() / ".steam/steam/steamapps/common/Aseprite/aseprite",
]


def aseprite():
    if os.environ.get("ASEPRITE"):
        return os.environ["ASEPRITE"]
    achado = shutil.which("aseprite") or next((str(p) for p in LUGARES if p.exists()), None)
    if not achado:
        sys.exit("Não achei o Aseprite: defina ASEPRITE=<executável>.")
    return achado


def fontes(peca):
    lista = sorted(FONTES.joinpath(peca).glob(f"{peca}-*.aseprite"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
    if not lista:
        sys.exit(f"Sem fontes em {FONTES / peca}.")
    return lista


def exportar(peca, pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    exe, feitos = aseprite(), []
    for fonte in fontes(peca):
        png = pasta / f"{fonte.stem}.png"
        r = subprocess.run([exe, "-b", str(fonte), "--save-as", str(png)], capture_output=True, text=True)
        if r.returncode or not png.exists():
            sys.exit(f"O Aseprite não exportou {fonte.name}:\n{r.stdout}{r.stderr}")
        im = Image.open(png).convert("RGBA")
        im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(pasta / f"{fonte.stem}@2x.png")
        feitos += [png.name, f"{fonte.stem}@2x.png"]
    return feitos


def conferir(peca):
    with tempfile.TemporaryDirectory() as tmp:
        diferentes = []
        for nome in exportar(peca, pathlib.Path(tmp)):
            novo, jogo = pathlib.Path(tmp) / nome, JOGO / nome
            if not jogo.exists():
                diferentes.append(f"{nome}: não está no jogo")
                continue
            pixels = list(Image.open(novo).convert("RGBA").getdata()) == list(Image.open(jogo).convert("RGBA").getdata())
            bytes_ = novo.read_bytes() == jogo.read_bytes()
            print(f"{nome}: pixels {'iguais' if pixels else 'DIFERENTES'}, bytes {'iguais' if bytes_ else 'diferentes'}")
            if not pixels:
                diferentes.append(nome)
        return diferentes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    peca = args[0]
    if "--conferir" in sys.argv:
        dif = conferir(peca)
        print("tudo igual ao jogo" if not dif else "DIFERENTE: " + ", ".join(dif))
        sys.exit(1 if dif else 0)
    pasta = pathlib.Path(args[1]) if len(args) > 1 else JOGO
    print("\n".join(str(pasta / n) for n in exportar(peca, pasta)))


if __name__ == "__main__":
    main()
