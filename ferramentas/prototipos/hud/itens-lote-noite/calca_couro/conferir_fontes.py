"""Confere as fontes em camadas da Calça de Couro: exporta cada .aseprite pela linha de comando do Aseprite (o composto
das camadas visíveis, como o exportar_aseprite.py) e compara, pixel a pixel, com os PNGs da proposta; confere também
que o 64 é o 32 ampliado 2× exatamente.

    python ferramentas/prototipos/hud/itens-lote-noite/calca_couro/conferir_fontes.py
"""
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[4] / "ferramentas" / "arte"))
from exportar_aseprite import aseprite  # noqa: E402

ok = True
with tempfile.TemporaryDirectory() as tmp:
    for n in (32, 40, 48):
        png = pathlib.Path(tmp) / f"calca_couro-{n}.png"
        subprocess.run([aseprite(), "-b", str(AQUI / "fontes" / f"calca_couro-{n}.aseprite"), "--save-as", str(png)],
                       capture_output=True)
        a = np.asarray(Image.open(png).convert("RGBA"))
        b = np.asarray(Image.open(AQUI / "proposta" / f"calca_couro-{n}.png").convert("RGBA"))
        igual = a.shape == b.shape and (a == b).all()
        ok &= igual
        print(f"{n}: o composto do .aseprite {'=' if igual else '≠'} a proposta")
p32 = Image.open(AQUI / "proposta" / "calca_couro-32.png").convert("RGBA")
p64 = Image.open(AQUI / "proposta" / "calca_couro-64.png").convert("RGBA")
dobro = (np.asarray(p32.resize((64, 64), Image.NEAREST)) == np.asarray(p64)).all()
ok &= dobro
print(f"64: {'=' if dobro else '≠'} o 32 ampliado 2×")
sys.exit(0 if ok else 1)
