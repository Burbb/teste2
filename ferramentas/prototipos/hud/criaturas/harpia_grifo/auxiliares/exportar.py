"""Monta, exporta e confere as fontes. O conector do Aseprite estava fora nesta sessão (22/10/2026; a Harpia e o Grifo): com --montar, as
fontes saem da linha de comando do Aseprite (ferramentas/arte/aseprite/montar_camadas.lua, o mesmo do montar_fontes.py,
com o pintar.lua: cada camada pintada pela lista de grades.py e relida pixel a pixel). Depois, o Aseprite (-b <fonte>
--save-as) grava proposta/<id>-16.png, o composto das camadas; o @2x é a duplicação exata; o 32 (a carta) e o 48 (o
Bestiário) são o 16 ×2 e ×3, cada um com o @2x. A conferência: 16×16 RGBA, alfa só 0 ou 255, o 1× igual à grade, os
derivados em blocos inteiros.
    python grades.py ..                       # as grades e as listas (antes)
    python exportar.py [--montar] [<id> ...]
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
sys.path.insert(0, str(AQUI.parents[5] / "ferramentas/arte"))
from exportar_aseprite import aseprite  # noqa: E402

def montar(ident):
    """A fonte pela linha de comando do Aseprite (aseprite/montar_camadas.lua, como o montar_fontes.py: o script
    copiado para uma pasta sem espaço no caminho, o pintar.lua por parâmetro)."""
    ordem = gr.CAMADAS[ident][2]
    fonte = PASTA / f"fontes/{ident}/{ident}-{16}.aseprite"
    fonte.parent.mkdir(parents=True, exist_ok=True)
    arte = RAIZ / "ferramentas/arte/aseprite"
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "montar_camadas.lua"
        shutil.copy(arte / "montar_camadas.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"n={16}", "--script-param",
                            f"listas={PASTA / 'listas' / ident}", "--script-param", f"camadas={','.join(ordem)}",
                            "--script-param", f"saida={fonte}", "--script-param", f"pintar={arte / 'pintar.lua'}",
                            "--script", str(script)], capture_output=True, text=True)
    pintura = [l for l in r.stdout.splitlines() if "escritos" in l]
    falhas = [c for l in pintura for c in l.split(" | ") if " 0 diferentes" not in c or " 0 fora" not in c]
    assert pintura and not falhas, (ident, r.stdout, r.stderr)
    print(ident, "fonte:", " | ".join(pintura))


if __name__ == "__main__":
    for ident in [a for a in sys.argv[1:] if a != "--montar"] or list(gr.CAMADAS):
        if "--montar" in sys.argv:
            montar(ident)
        fonte, png = PASTA / f"fontes/{ident}/{ident}-16.aseprite", PASTA / f"proposta/{ident}-16.png"
        png.parent.mkdir(exist_ok=True)
        subprocess.run([aseprite(), "-b", str(fonte), "--save-as", str(png)], capture_output=True, text=True)
        um = Image.open(png)
        assert um.size == (16, 16) and um.mode == "RGBA", (ident, um.size, um.mode)
        um = um.convert("RGBA")
        esperado = gr.imagem(ident)
        difere = [(x, y) for y in range(16) for x in range(16) if um.getpixel((x, y)) != esperado.getpixel((x, y))
                  and not (um.getpixel((x, y))[3] == esperado.getpixel((x, y))[3] == 0)]
        assert not difere, (ident, difere[:6])
        assert all(p[3] in (0, 255) for p in um.getdata()), ident
        um.resize((32, 32), Image.NEAREST).save(PASTA / f"proposta/{ident}-16@2x.png")
        for lado, f in ((32, 2), (48, 3)):
            der = um.resize((lado, lado), Image.NEAREST)
            der.save(PASTA / f"proposta/{ident}-{lado}.png")
            der.resize((2 * lado, 2 * lado), Image.NEAREST).save(PASTA / f"proposta/{ident}-{lado}@2x.png")
            volta = Image.open(PASTA / f"proposta/{ident}-{lado}.png").convert("RGBA")
            assert volta.resize((16, 16), Image.NEAREST).tobytes() == um.tobytes(), (ident, lado)
            assert all(len({volta.getpixel((x * f + i, y * f + j)) for i in range(f) for j in range(f)}) == 1
                       for y in range(16) for x in range(16)), (ident, lado)
        print(f"{ident}: exportado = grade, @2x exato, 32 e 48 em blocos inteiros")
