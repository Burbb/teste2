"""Monta e exporta as fontes do Lich Menor (o estudo de 32 e a proposta de 16), como o exportar.py do Senhor da Guerra:
a fonte sai da linha de comando do Aseprite (ferramentas/arte/aseprite/montar_camadas.lua com o pintar.lua: cada camada
pintada pela lista de grade.py e relida pixel a pixel; o Lich não tem guia). O Aseprite (-b <fonte> --save-as)
grava proposta/<id>-<lado>.png, o composto. Os derivados são ampliações
exatas: no N32, o @2x de 64; no N16, o @2x, o 32 da carta (o 16 ×2) e o @2x dele. A conferência: o lado certo, RGBA,
alfa só 0 ou 255, igual à grade, cada derivado em blocos inteiros que voltam ao original, a fonte reaberta com as
camadas na ordem.
    python grade.py ..                      # as grades e as listas (antes)
    python exportar.py [--montar] [<id> ...]  # sem id, os dois; o --montar refaz só as fontes pedidas
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

import grade as gr

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
RAIZ = AQUI.parents[5]
sys.path.insert(0, str(RAIZ / "ferramentas/arte"))
from exportar_aseprite import aseprite  # noqa: E402


def fonte(ident):
    return PASTA / f"fontes/{ident}/{ident}-{gr.DESENHOS[ident][1]}.aseprite"


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
    arte = RAIZ / "ferramentas/arte/aseprite"
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "montar_camadas.lua"
        shutil.copy(arte / "montar_camadas.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"n={gr.DESENHOS[ident][1]}",
                            "--script-param", f"listas={PASTA / 'listas' / ident}",
                            "--script-param", f"camadas={','.join(gr.ORDEM)}", "--script-param", f"saida={f}",
                            "--script-param", f"pintar={arte / 'pintar.lua'}", "--script", str(script)],
                           capture_output=True, text=True)
    pintura = [l for l in r.stdout.splitlines() if "escritos" in l]
    falhas = [c for l in pintura for c in l.split(" | ") if " 0 diferentes" not in c or " 0 fora" not in c]
    assert pintura and not falhas, (ident, r.stdout, r.stderr)
    print(ident, "fonte:", " | ".join(pintura))


def conferir_fonte(ident):
    """Reabre a fonte: o tamanho e as camadas na ordem, todas visíveis."""
    saida = lua('local s = app.open(app.params["fonte"]); print("@@" .. s.width .. "x" .. s.height); '
                'for _, l in ipairs(s.layers) do print("@@" .. l.name .. "=" .. tostring(l.isVisible)) end', fonte=fonte(ident))
    linhas = [l[2:] for l in saida.splitlines() if l.startswith("@@")]  # as extensões do Aseprite também escrevem
    n = gr.DESENHOS[ident][1]
    assert linhas[0] == f"{n}x{n}", (ident, linhas)
    assert linhas[1:] == [f"{c}=true" for c in gr.ORDEM], (ident, linhas)
    print(ident, "fonte reaberta:", " ".join(linhas))


def derivado(um, fator, arquivo):
    """Grava a ampliação exata por vizinho mais próximo e confere os blocos e a volta ao original."""
    lado = um.width * fator
    um.resize((lado, lado), Image.NEAREST).save(arquivo)
    volta = Image.open(arquivo).convert("RGBA")
    assert all(len({volta.getpixel((fator * x + i, fator * y + j)) for i in range(fator) for j in range(fator)}) == 1
               for y in range(um.height) for x in range(um.width)), arquivo
    assert volta.resize(um.size, Image.NEAREST).tobytes() == um.tobytes(), arquivo


def exportar(ident):
    n = gr.DESENHOS[ident][1]
    png = PASTA / f"proposta/{ident}-{n}.png"
    png.parent.mkdir(exist_ok=True)
    subprocess.run([aseprite(), "-b", str(fonte(ident)), "--save-as", str(png)], capture_output=True, text=True)
    um = Image.open(png)
    assert um.size == (n, n) and um.mode == "RGBA", (ident, um.size, um.mode)
    um = um.convert("RGBA")
    esperado = gr.imagem(ident)
    difere = [(x, y) for y in range(n) for x in range(n) if um.getpixel((x, y)) != esperado.getpixel((x, y))
              and not (um.getpixel((x, y))[3] == esperado.getpixel((x, y))[3] == 0)]
    assert not difere, (ident, difere[:6])
    assert all(p[3] in (0, 255) for p in um.getdata()), ident
    derivado(um, 2, PASTA / f"proposta/{ident}-{n}@2x.png")
    if n == 16:  # o 32 da carta e o @2x dele
        derivado(um, 2, PASTA / f"proposta/{ident}-32.png")
        derivado(um, 4, PASTA / f"proposta/{ident}-32@2x.png")
    print(f"{ident}: exportado = grade, alfa 0/255, derivados em blocos inteiros que voltam ao {n}")


if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if a != "--montar"] or list(gr.DESENHOS)
    for ident in ids:
        if "--montar" in sys.argv:
            montar(ident)
        conferir_fonte(ident)
        exportar(ident)
