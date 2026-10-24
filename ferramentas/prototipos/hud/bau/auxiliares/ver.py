"""Rascunho: as grades num PNG (1×) e ampliadas, sobre o carvão da HUD, para conferir cada rodada."""
import importlib.util, sys, pathlib
from PIL import Image
def carregar(arq):
    spec = importlib.util.spec_from_file_location("g", arq); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def imagem(grade, paleta):
    n = len(grade); assert all(len(l) == n for l in grade), [len(l) for l in grade]
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    for y, l in enumerate(grade):
        for x, c in enumerate(l):
            if c != ".": im.putpixel((x, y), tuple(int(paleta[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im
if __name__ == "__main__":
    m = carregar(sys.argv[1]); saida = pathlib.Path(sys.argv[2]); nome = sys.argv[3] if len(sys.argv) > 3 else "G32"
    im = imagem(getattr(m, nome), m.PALETA); n = im.size[0]
    fundo = Image.new("RGB", (n * 10 + n + 40, n * 10 + 20), (24, 22, 21))
    fundo.paste(im, (10, 10), im); fundo.paste(im.resize((n * 10, n * 10), Image.NEAREST), (n + 30, 10), im.resize((n * 10, n * 10), Image.NEAREST))
    fundo.save(saida); im.save(saida.with_name(saida.stem + "-1x.png")); print(saida)
