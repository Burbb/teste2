"""Monta as fontes e exporta (o Esgotado, 22/10/2026). O conector do Aseprite estava fora nesta sessão: as fontes saem
da linha de comando do Aseprite (ferramentas/arte/aseprite/montar_camadas.lua, o mesmo do montar_fontes.py, com o
pintar.lua: as camadas pintadas pelas listas de grades.py, relidas pixel a pixel). Depois, o Aseprite (-b <fonte>
--save-as) grava proposta/<id>-16.png, o composto das camadas, e o @2x é a duplicação exata. A conferência: 16×16
RGBA, alfa só 0 ou 255, o 1× igual à grade.
    python grades.py ..                      # as grades e as listas (antes)
    python exportar.py [--montar] [<id> ...] # --montar refaz as fontes a partir das listas
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

import grades as gr

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
RAIZ = AQUI.parents[5]
sys.path.insert(0, str(RAIZ / "ferramentas/arte"))
from exportar_aseprite import aseprite  # noqa: E402

LADO = 16


def montar(ident):
    """A fonte pela linha de comando do Aseprite (aseprite/montar_camadas.lua, como o montar_fontes.py: o script
    copiado para uma pasta sem espaço no caminho, o pintar.lua por parâmetro)."""
    ordem = gr.CAMADAS[ident][1]
    fonte = PASTA / f"fontes/{ident}/{ident}-{LADO}.aseprite"
    fonte.parent.mkdir(parents=True, exist_ok=True)
    arte = RAIZ / "ferramentas/arte/aseprite"
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "montar_camadas.lua"
        shutil.copy(arte / "montar_camadas.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"n={LADO}", "--script-param",
                            f"listas={PASTA / 'listas' / ident}", "--script-param", f"camadas={','.join(ordem)}",
                            "--script-param", f"saida={fonte}", "--script-param", f"pintar={arte / 'pintar.lua'}",
                            "--script", str(script)], capture_output=True, text=True)
    pintura = [l for l in r.stdout.splitlines() if "escritos" in l]
    falhas = [c for l in pintura for c in l.split(" | ") if " 0 diferentes" not in c or " 0 fora" not in c]
    assert pintura and not falhas, (ident, r.stdout, r.stderr)
    print(ident, "fonte:", " | ".join(pintura))


def exportar(ident):
    fonte, png = PASTA / f"fontes/{ident}/{ident}-{LADO}.aseprite", PASTA / f"proposta/{ident}-{LADO}.png"
    png.parent.mkdir(exist_ok=True)
    subprocess.run([aseprite(), "-b", str(fonte), "--save-as", str(png)], capture_output=True, text=True)
    um = Image.open(png)
    assert um.size == (LADO, LADO) and um.mode == "RGBA", (ident, um.size, um.mode)
    esperado = gr.imagem(ident)
    difere = [(x, y) for y in range(LADO) for x in range(LADO) if um.getpixel((x, y)) != esperado.getpixel((x, y))
              and not (um.getpixel((x, y))[3] == esperado.getpixel((x, y))[3] == 0)]
    assert not difere, (ident, difere[:6])
    assert all(p[3] in (0, 255) for p in um.getdata()), ident
    um.resize((2 * LADO, 2 * LADO), Image.NEAREST).save(PASTA / f"proposta/{ident}-{LADO}@2x.png")
    print(f"{ident}: exportado = grade, @2x exato")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--montar"]
    for ident in args or list(gr.CAMADAS):
        if "--montar" in sys.argv:
            montar(ident)
        exportar(ident)
