"""Exporta e confere as fontes dos animais (montadas no editor pelo conector, com o pintar.lua): o Aseprite (-b <fonte>
--save-as) grava proposta/<id>-16.png, o composto das camadas; o @2x é a duplicação exata. A conferência: 16×16 RGBA,
alfa só 0 ou 255, o 1× igual pixel a pixel à grade, o @2x igual ao 1× ampliado. A cena desenha o 16 na escala dela.
    python exportar.py [<id> ...]
"""
import pathlib
import subprocess
import sys

from PIL import Image

import grades as gr

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
sys.path.insert(0, str(AQUI.parents[4] / "ferramentas/arte"))
from exportar_aseprite import aseprite  # noqa: E402

if __name__ == "__main__":
    for ident in sys.argv[1:] or list(gr.CAMADAS):
        fonte, png = PASTA / f"fontes/{ident}/{ident}-16.aseprite", PASTA / f"proposta/{ident}-16.png"
        png.parent.mkdir(exist_ok=True)
        subprocess.run([aseprite(), "-b", str(fonte), "--save-as", str(png)], capture_output=True, text=True)
        um = Image.open(png)
        assert um.size == (16, 16) and um.mode == "RGBA", (ident, um.size, um.mode)
        um = um.convert("RGBA")
        um.resize((32, 32), Image.NEAREST).save(PASTA / f"proposta/{ident}-16@2x.png")
        esperado = gr.imagem(ident)
        difere = [(x, y) for y in range(16) for x in range(16) if um.getpixel((x, y)) != esperado.getpixel((x, y))
                  and not (um.getpixel((x, y))[3] == esperado.getpixel((x, y))[3] == 0)]
        assert not difere, (ident, difere[:6])
        assert all(p[3] in (0, 255) for p in um.getdata()), ident
        dobro = Image.open(PASTA / f"proposta/{ident}-16@2x.png").convert("RGBA")
        assert dobro.tobytes() == um.resize((32, 32), Image.NEAREST).tobytes(), ident
        print(f"{ident}: exportado = grade, @2x exato, {sum(1 for p in um.getdata() if p[3])} opacos")
