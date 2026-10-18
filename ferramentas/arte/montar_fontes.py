"""Monta as fontes em camadas (.aseprite) de uma peça a partir das listas por camada que o script de desenho grava
(`desenhar_<peça>_pixel.py <pasta> --listas`, por `pixel_comum.listas_camadas`): uma fonte por tamanho, em
`aseprite/<peça>/<peça>-<lado>.aseprite`, pela linha de comando do Aseprite (`aseprite/montar_camadas.lua`, com o
`pintar.lua`). Depois, `exportar_aseprite.py <peça>` exporta os PNGs e `--conferir` os compara com os do jogo.

    python ferramentas/arte/montar_fontes.py <peça> <pasta das listas> [--fontes=<pasta>]
    (a pasta das listas tem <peça>-<lado>/ com ordem.txt; --fontes=<pasta>: uma proposta, fora de aseprite/)
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

import exportar_aseprite as ex
from exportar_aseprite import aseprite

AQUI = pathlib.Path(__file__).resolve().parent


def montar(peca, listas):
    destino = ex.FONTES / peca
    destino.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "montar_camadas.lua"
        shutil.copy(AQUI / "aseprite" / "montar_camadas.lua", script)
        for pasta in sorted(listas.glob(f"{peca}-*")):
            lado = int(pasta.name.rsplit("-", 1)[1])
            camadas = (pasta / "ordem.txt").read_text(encoding="utf-8").strip()
            saida = destino / f"{peca}-{lado}.aseprite"
            r = subprocess.run([aseprite(), "-b", "--script-param", f"n={lado}", "--script-param", f"listas={pasta}",
                                "--script-param", f"camadas={camadas}", "--script-param", f"saida={saida}",
                                "--script-param", f"pintar={AQUI / 'aseprite' / 'pintar.lua'}", "--script", str(script)],
                               capture_output=True, text=True)
            linhas = [l for l in r.stdout.splitlines() if "escritos" in l]
            if not saida.exists() or not linhas:
                sys.exit(f"O Aseprite não montou {saida.name}:\n{r.stdout}{r.stderr}")
            print(f"{saida.name}: {linhas[-1]}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    montar(args[0], pathlib.Path(args[1]).resolve())
