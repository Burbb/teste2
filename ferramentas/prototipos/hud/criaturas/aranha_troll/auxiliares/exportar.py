"""Exporta e confere as fontes (montadas no editor pelo MCP, com o pintar.lua): o Aseprite (-b <fonte> --save-as) grava
proposta/<id>-16.png, o composto das camadas; o @2x é a duplicação exata; a conferência: 16×16 RGBA, alfa só 0 ou 255,
o 1× igual pixel a pixel à grade e o @2x igual ao 1× ampliado; o 32 e o 48 (os derivados ×2 e ×3) em blocos inteiros. Também grava o 48 (o 3× do Bestiário e do mural), só
para as folhas.
    python exportar.py [<id> ...]
"""
import pathlib
import subprocess
import sys

from PIL import Image

import grades as gr
from previa import imagem

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
RAIZ = AQUI.parents[5]
sys.path.insert(0, str(RAIZ / "ferramentas/arte"))
from exportar_aseprite import aseprite  # noqa: E402

if __name__ == "__main__":
    for ident in sys.argv[1:] or list(gr.CAMADAS):
        fonte = PASTA / f"fontes/{ident}/{ident}-16.aseprite"
        png = PASTA / f"proposta/{ident}-16.png"
        png.parent.mkdir(exist_ok=True)
        subprocess.run([aseprite(), "-b", str(fonte), "--save-as", str(png)], capture_output=True, text=True)
        um = Image.open(png)
        assert um.size == (16, 16) and um.mode == "RGBA", (ident, um.size, um.mode)
        um = um.convert("RGBA")
        um.resize((32, 32), Image.NEAREST).save(PASTA / f"proposta/{ident}-16@2x.png")
        esperado = imagem(ident)
        difere = [(x, y) for y in range(16) for x in range(16)
                  if um.getpixel((x, y)) != esperado.getpixel((x, y)) and not (um.getpixel((x, y))[3] == esperado.getpixel((x, y))[3] == 0)]
        assert not difere, (ident, difere[:6])
        assert all(p[3] in (0, 255) for p in um.getdata()), ident
        dobro = Image.open(PASTA / f"proposta/{ident}-16@2x.png").convert("RGBA")
        assert dobro.resize((16, 16), Image.NEAREST).tobytes() == um.tobytes(), ident
        # os derivados inteiros que a produção usaria: o 32 (a carta) e o 48 (o Bestiário), cada um com o @2x
        for lado, f in ((32, 2), (48, 3)):
            der = um.resize((lado, lado), Image.NEAREST)
            der.save(PASTA / f"proposta/{ident}-{lado}.png")
            der.resize((2 * lado, 2 * lado), Image.NEAREST).save(PASTA / f"proposta/{ident}-{lado}@2x.png")
            volta = Image.open(PASTA / f"proposta/{ident}-{lado}.png").convert("RGBA")
            assert volta.resize((16, 16), Image.NEAREST).tobytes() == um.tobytes(), (ident, lado)
            assert all(len({volta.getpixel((x * f + i, y * f + j)) for i in range(f) for j in range(f)}) == 1
                       for y in range(16) for x in range(16)), (ident, lado)
        print(f"{ident}: exportado = grade, @2x exato, 32 e 48 por blocos inteiros, {sum(1 for p in um.getdata() if p[3] == 0)} transparentes, "
              f"{len(set(p for p in um.getdata() if p[3]))} cores")
