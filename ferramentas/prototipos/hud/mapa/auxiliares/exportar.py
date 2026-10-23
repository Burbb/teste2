"""Monta e exporta as peças do primeiro lote da 1E.4, como o exportar.py dos estudos das criaturas: a fonte sai da
linha de comando do Aseprite (auxiliares/montar.lua, o montar_camadas.lua para peças w×h, com o pintar.lua de
ferramentas/arte/aseprite/: cada camada pintada pela lista de grade.py e relida pixel a pixel); o Aseprite
(-b <fonte> --save-as) grava proposta/<id>.png, o composto; o @2x é a duplicação exata. A conferência: o tamanho, RGBA,
alfa só 0 ou 255, igual à grade, o @2x em blocos inteiros que voltam ao original, a fonte reaberta com as camadas na
ordem. O conector do editor não foi usado (a janela aberta do Aseprite não é tocada).
    python grade.py ..                       # as grades e as listas (antes)
    python exportar.py [--montar] [<id> ...]   # o --montar refaz a fonte
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

import grade
import lugares

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(RAIZ / "ferramentas/arte"))
from exportar_aseprite import aseprite  # noqa: E402


def gr(ident):
    """O módulo do desenho: as marcas (grade.py) ou os símbolos de lugar (lugares.py)."""
    return lugares if ident in lugares.DESENHOS else grade


def ordem(ident):
    m = gr(ident)
    return m.ordem(ident) if hasattr(m, "ordem") else m.ORDEM


def fonte(ident):
    return PASTA / f"fontes/{ident}.aseprite"


def lua(texto, **params):
    """Roda um script curto na linha de comando do Aseprite (numa pasta sem espaço no caminho) e devolve a saída."""
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "s.lua"
        script.write_text(texto, encoding="utf-8")
        args = [a for k, v in params.items() for a in ("--script-param", f"{k}={v}")]
        return subprocess.run([aseprite(), "-b", *args, "--script", str(script)], capture_output=True, text=True).stdout


def montar(ident):
    f = fonte(ident)
    f.parent.mkdir(parents=True, exist_ok=True)
    w, h = gr(ident).lado(ident)
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "montar.lua"
        shutil.copy(AQUI / "montar.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"w={w}", "--script-param", f"h={h}",
                            "--script-param", f"listas={PASTA / 'listas' / ident}",
                            "--script-param", f"camadas={','.join(ordem(ident))}", "--script-param", f"saida={f}",
                            "--script-param", f"pintar={RAIZ / 'ferramentas/arte/aseprite/pintar.lua'}",
                            "--script", str(script)], capture_output=True, text=True)
    pintura = [l for l in r.stdout.splitlines() if "escritos" in l]
    falhas = [c for l in pintura for c in l.split(" | ") if " 0 diferentes" not in c or " 0 fora" not in c]
    assert pintura and not falhas, (ident, r.stdout, r.stderr)
    print(ident, "fonte:", " | ".join(pintura))


def conferir_fonte(ident):
    saida = lua('local s = app.open(app.params["fonte"]); print("@@" .. s.width .. "x" .. s.height); '
                'for _, l in ipairs(s.layers) do print("@@" .. l.name .. "=" .. tostring(l.isVisible)) end', fonte=fonte(ident))
    linhas = [l[2:] for l in saida.splitlines() if l.startswith("@@")]
    w, h = gr(ident).lado(ident)
    assert linhas[0] == f"{w}x{h}", (ident, linhas)
    assert linhas[1:] == [f"{c}=true" for c in ordem(ident)], (ident, linhas)


def exportar(ident):
    w, h = gr(ident).lado(ident)
    png = PASTA / f"proposta/{ident}.png"
    png.parent.mkdir(exist_ok=True)
    subprocess.run([aseprite(), "-b", str(fonte(ident)), "--save-as", str(png)], capture_output=True, text=True)
    um = Image.open(png)
    assert um.size == (w, h) and um.mode == "RGBA", (ident, um.size, um.mode)
    esperado = gr(ident).imagem(ident)
    difere = [(x, y) for y in range(h) for x in range(w) if um.getpixel((x, y)) != esperado.getpixel((x, y))
              and not (um.getpixel((x, y))[3] == esperado.getpixel((x, y))[3] == 0)]
    assert not difere, (ident, difere[:6])
    assert all(p[3] in (0, 255) for p in um.getdata()), ident
    dobro = PASTA / f"proposta/{ident}@2x.png"
    um.resize((w * 2, h * 2), Image.NEAREST).save(dobro)
    volta = Image.open(dobro).convert("RGBA")
    assert volta.resize((w, h), Image.NEAREST).tobytes() == um.tobytes(), ident
    assert all(len({volta.getpixel((2 * x + i, 2 * y + j)) for i in range(2) for j in range(2)}) == 1
               for y in range(h) for x in range(w)), ident
    print(f"{ident} {w}×{h}: fonte reaberta com {','.join(ordem(ident))}; exportado = grade, alfa 0/255, @2x em blocos inteiros")


if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if a != "--montar"] or list(grade.DESENHOS) + list(lugares.DESENHOS)
    for ident in ids:
        if "--montar" in sys.argv:
            montar(ident)
        conferir_fonte(ident)
        exportar(ident)
