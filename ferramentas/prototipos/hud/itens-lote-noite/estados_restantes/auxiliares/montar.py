"""Monta as fontes em camadas e exporta as propostas dos estados, pela linha de comando do Aseprite (o conector do MCP
não subiu nesta sessão, 21/10/2026; o caminho é o de ferramentas/arte/montar_fontes.py, com o montar_camadas.lua e o
pintar.lua, que relê cada pixel gravado):
  1. icones16.py grava grades/<id>.txt e listas/<id>/<camada>.lua (com ordem.txt);
  2. o Aseprite (-b) monta fontes/<id>/<id>-16.aseprite, uma camada por parte, o contorno por cima;
  3. o Aseprite (-b <fonte> --save-as) exporta proposta/<id>-16.png, o composto das camadas visíveis;
  4. o @2x é a duplicação exata do 1× (vizinho mais próximo);
  5. a conferência: 16×16, RGBA, fundo transparente, o 1× igual pixel a pixel à grade e o @2x igual ao 1× ampliado.
    python montar.py <id> [<id> ...]      (ou: python montar.py lote <n>)
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

import icones16 as ic
from comum import LOTE, LOTES, RAIZ

sys.path.insert(0, str(RAIZ / "ferramentas/arte"))
from exportar_aseprite import aseprite  # noqa: E402

LUA = RAIZ / "ferramentas/arte/aseprite"


def da_grade(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(ic.ICONES[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                c = ic.CORES[ch]
                im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def montar(ident, tmp):
    listas = LOTE / f"listas/{ident}"
    fonte = LOTE / f"fontes/{ident}/{ident}-16.aseprite"
    fonte.parent.mkdir(parents=True, exist_ok=True)
    camadas = (listas / "ordem.txt").read_text(encoding="utf-8").strip()
    r = subprocess.run([aseprite(), "-b", "--script-param", "n=16", "--script-param", f"listas={listas}",
                        "--script-param", f"camadas={camadas}", "--script-param", f"saida={fonte}",
                        "--script-param", f"pintar={LUA / 'pintar.lua'}", "--script", str(tmp / "montar_camadas.lua")],
                       capture_output=True, text=True)
    linhas = [l for l in r.stdout.splitlines() if "escritos" in l]
    if not fonte.exists() or not linhas:
        sys.exit(f"O Aseprite não montou {fonte.name}:\n{r.stdout}{r.stderr}")
    png = LOTE / f"proposta/{ident}-16.png"
    png.parent.mkdir(exist_ok=True)
    r = subprocess.run([aseprite(), "-b", str(fonte), "--save-as", str(png)], capture_output=True, text=True)
    if not png.exists():
        sys.exit(f"O Aseprite não exportou {png.name}:\n{r.stdout}{r.stderr}")
    um = Image.open(png)
    assert um.size == (16, 16) and um.mode == "RGBA", (ident, um.size, um.mode)
    um = um.convert("RGBA")
    dobro = um.resize((32, 32), Image.NEAREST)
    dobro.save(LOTE / f"proposta/{ident}-16@2x.png")
    esperado = da_grade(ident)
    difere = [(x, y) for y in range(16) for x in range(16) if um.getpixel((x, y)) != esperado.getpixel((x, y))
              and not (um.getpixel((x, y))[3] == 0 and esperado.getpixel((x, y))[3] == 0)]
    transparentes = sum(1 for p in um.getdata() if p[3] == 0)
    parciais = sum(1 for p in um.getdata() if 0 < p[3] < 255)
    assert not difere, (ident, difere[:8])
    assert parciais == 0 and transparentes > 0, ident   # só opaco ou transparente, com o fundo transparente
    assert Image.open(LOTE / f"proposta/{ident}-16@2x.png").convert("RGBA").resize((16, 16), Image.NEAREST).tobytes() == um.tobytes()
    print(f"{ident}: {linhas[-1].strip()} | exportado = grade, {transparentes} transparentes, {parciais} parciais, "
          f"{len(set(p for p in um.getdata() if p[3]))} cores")


if __name__ == "__main__":
    args = sys.argv[1:]
    ids = ([k for e in LOTES[int(args[1])] for k in ic.ICONES if k == f"estado-{e}" or k.startswith(f"estado-{e}-")]
           if args[0] == "lote" else args)
    ic.gravar(LOTE, ids)
    with tempfile.TemporaryDirectory() as t:
        tmp = pathlib.Path(t)
        shutil.copy(LUA / "montar_camadas.lua", tmp / "montar_camadas.lua")   # sem espaço no caminho do script
        for ident in ids:
            montar(ident, tmp)
