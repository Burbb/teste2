"""A taverna no jogo (desde a 1.220.0): copia as camadas aprovadas, exportadas das fontes em Aseprite, para
`rpg/web/static/cenas/` (o que telas/cena-taverna.js lê). Não se editam as cópias: um retoque vai na fonte e se
exporta de novo por aqui.

    python ferramentas/prototipos/taverna/jogo.py              # exporta das fontes e copia para o jogo
    python ferramentas/prototipos/taverna/jogo.py --conferir   # só confere: as cópias do jogo iguais às exportações

As fontes (a autoridade; os scripts que as montaram não as refazem sem `--refazer --sem-os-retoques`):
- o balcão: `g4/aseprite/taverna-g4.aseprite` (g4/fonte.py) → `cenas/taverna/`: fundo, fogo, velas, taverneiro,
  frente e rotina.json;
- Morel no canto: `morel/canto/canto.aseprite` (morel/canto/exportar.py) e a queda de braço:
  `morel/queda-canto/queda-canto.aseprite` (morel/queda-canto/exportar.py) → `cenas/taverna-mesa/`: fundo, chamas,
  morel, frente, rotina.json, moedas.png e moedas.json, queda-canto.png e queda-canto.json.

As folhas de revisão e as comparações ficam no protótipo (camadas/); só o que a cena desenha vai para o jogo."""
import pathlib
import shutil
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
JOGO = RAIZ / "rpg" / "web" / "static" / "cenas"
CAMADAS = AQUI / "camadas"
COPIAS = {
    "taverna": (CAMADAS / "g4", ["fundo.png", "fogo.png", "velas.png", "taverneiro.png", "frente.png", "rotina.json"]),
    "taverna-mesa": (CAMADAS / "morel-canto", ["fundo.png", "chamas.png", "morel.png", "frente.png", "rotina.json",
                                               "moedas.png", "moedas.json", "queda-canto.png", "queda-canto.json"]),
}


def _rodar(arq, *args):
    """Roda um script do protótipo como na linha de comando (cada um num processo: os módulos de mesmo nome das pastas
    não se misturam)."""
    subprocess.run([sys.executable, str(arq), *args], check=True)


def exportar():
    """As três exportações, cada uma lendo a sua fonte (e conferindo que ela é a do desenho aprovado)."""
    _rodar(AQUI / "g4" / "fonte.py", "--conferir")
    _rodar(AQUI / "morel" / "canto" / "exportar.py")
    _rodar(AQUI / "morel" / "canto" / "exportar.py", "--conferir")
    _rodar(AQUI / "morel" / "queda-canto" / "exportar.py")
    _rodar(AQUI / "morel" / "queda-canto" / "exportar.py", "--conferir")


def copiar():
    for pasta, (origem, nomes) in COPIAS.items():
        destino = JOGO / pasta
        destino.mkdir(parents=True, exist_ok=True)
        for n in nomes:
            shutil.copyfile(origem / n, destino / n)
        print(f"cenas/{pasta}: {len(nomes)} arquivos")


def conferir():
    dif = [f"{pasta}/{n}" for pasta, (origem, nomes) in COPIAS.items() for n in nomes
           if not (JOGO / pasta / n).exists() or (JOGO / pasta / n).read_bytes() != (origem / n).read_bytes()]
    print("as cópias do jogo iguais às exportações" if not dif else f"diferem: {', '.join(dif)}")
    return not dif


if __name__ == "__main__":
    if "--conferir" in sys.argv:
        sys.exit(0 if conferir() else 1)
    exportar()
    copiar()
    conferir()
