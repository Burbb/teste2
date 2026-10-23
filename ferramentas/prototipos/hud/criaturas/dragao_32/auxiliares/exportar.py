"""Monta e exporta a fonte do teste do Dragão em 32 nativos (como o exportar.py de chefes_e_especiais, com n=32): a fonte
sai da linha de comando do Aseprite (ferramentas/arte/aseprite/montar_camadas.lua com o pintar.lua: cada camada pintada
pela lista de grade.py e relida pixel a pixel), a guia escondida depois (o --save-as só leva as camadas visíveis). O
Aseprite (-b <fonte> --save-as) grava proposta/dragao-n32-32.png, o composto; o @2x (64) é a duplicação exata. A
conferência: 32×32 RGBA, alfa só 0 ou 255, igual à grade, o @2x em blocos 2×2 que voltam ao 32, a guia oculta na fonte.
    python grade.py ..        # a grade e as listas (antes)
    python exportar.py [--montar]
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

FONTE = PASTA / f"fontes/{gr.ID}/{gr.ID}-32.aseprite"


def lua(texto, **params):
    """Roda um script curto na linha de comando do Aseprite (numa pasta sem espaço no caminho) e devolve a saída."""
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "s.lua"
        script.write_text(texto, encoding="utf-8")
        args = [a for k, v in params.items() for a in ("--script-param", f"{k}={v}")]
        return subprocess.run([aseprite(), "-b", *args, "--script", str(script)], capture_output=True, text=True).stdout


def montar():
    FONTE.parent.mkdir(parents=True, exist_ok=True)
    arte = RAIZ / "ferramentas/arte/aseprite"
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / "montar_camadas.lua"
        shutil.copy(arte / "montar_camadas.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", "n=32", "--script-param", f"listas={PASTA / 'listas' / gr.ID}",
                            "--script-param", f"camadas={','.join(gr.ORDEM)}", "--script-param", f"saida={FONTE}",
                            "--script-param", f"pintar={arte / 'pintar.lua'}", "--script", str(script)],
                           capture_output=True, text=True)
    pintura = [l for l in r.stdout.splitlines() if "escritos" in l]
    falhas = [c for l in pintura for c in l.split(" | ") if " 0 diferentes" not in c or " 0 fora" not in c]
    assert pintura and not falhas, (r.stdout, r.stderr)
    lua('local s = app.open(app.params["fonte"]); for _, l in ipairs(s.layers) do '
        'if l.name == "guia" then l.isVisible = false end end; s:saveAs(s.filename)', fonte=FONTE)
    print("fonte:", " | ".join(pintura))


def conferir_fonte():
    """Reabre a fonte: o tamanho, as camadas na ordem e a guia oculta."""
    saida = lua('local s = app.open(app.params["fonte"]); print("@@" .. s.width .. "x" .. s.height); '
                'for _, l in ipairs(s.layers) do print("@@" .. l.name .. "=" .. tostring(l.isVisible)) end', fonte=FONTE)
    linhas = [l[2:] for l in saida.splitlines() if l.startswith("@@")]  # as extensões do Aseprite também escrevem
    assert linhas[0] == "32x32", linhas
    assert linhas[1:] == [f"{c}={'false' if c == 'guia' else 'true'}" for c in gr.ORDEM], linhas
    print("fonte reaberta:", " ".join(linhas))


if __name__ == "__main__":
    if "--montar" in sys.argv:
        montar()
    conferir_fonte()
    png = PASTA / f"proposta/{gr.ID}-32.png"
    png.parent.mkdir(exist_ok=True)
    subprocess.run([aseprite(), "-b", str(FONTE), "--save-as", str(png)], capture_output=True, text=True)
    um = Image.open(png)
    assert um.size == (32, 32) and um.mode == "RGBA", (um.size, um.mode)
    esperado = gr.imagem()
    difere = [(x, y) for y in range(32) for x in range(32) if um.getpixel((x, y)) != esperado.getpixel((x, y))
              and not (um.getpixel((x, y))[3] == esperado.getpixel((x, y))[3] == 0)]
    assert not difere, difere[:6]
    assert all(p[3] in (0, 255) for p in um.getdata())
    dois = um.resize((64, 64), Image.NEAREST)
    dois.save(PASTA / f"proposta/{gr.ID}-32@2x.png")
    volta = Image.open(PASTA / f"proposta/{gr.ID}-32@2x.png").convert("RGBA")
    assert all(len({volta.getpixel((2 * x + i, 2 * y + j)) for i in range(2) for j in range(2)}) == 1
               for y in range(32) for x in range(32))
    assert volta.resize((32, 32), Image.NEAREST).tobytes() == um.tobytes()
    print(f"{gr.ID}: exportado = grade, alfa 0/255, @2x (64) em blocos 2×2 que voltam ao 32")
