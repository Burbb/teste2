"""Monta uma fonte .aseprite em camadas e quadros pelo Aseprite em lote (o `pintar.lua`, um passo por camada), a partir
de listas de pixels, e lê de volta as células. Serve ao estudo e às poses da queda de braço (`estudo.py`, `poses.py`).

Uma fonte só é criada se não existir: depois, ela é a autoridade (retoques no editor) e a exportação lê dela."""
import pathlib
import shutil
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

from exportar_aseprite import aseprite  # noqa: E402

PINTAR = RAIZ / "ferramentas" / "arte" / "aseprite" / "pintar.lua"
CELULAS = RAIZ / "ferramentas" / "prototipos" / "hud" / "forja" / "h2" / "aseprite" / "exportar_forja.lua"

_MONTAR = r'''
local P = dofile(app.params["pintar"])
local D = dofile(app.params["dados"])
local s = Sprite(D.w, D.h, ColorMode.RGB)
s.layers[1].name = D.camadas[1]
for i = 2, #D.camadas do local l = s:newLayer(); l.name = D.camadas[i] end
for i = 2, #D.quadros do s:newEmptyFrame() end
for i, nome in ipairs(D.quadros) do local t = s:newTag(i, i); t.name = nome end
local saida = {}
for i = 1, #D.quadros do
  app.frame = s.frames[i]
  for _, c in ipairs(D.camadas) do
    local px = D.pixels[i][c]
    if px and #px > 0 then saida[#saida + 1] = P.pintar(c, px) end
  end
end
for _, l in ipairs(s.layers) do
  if D.ocultas[l.name] then l.isVisible = false end
  if D.opacidade[l.name] then l.opacity = D.opacidade[l.name] end
  if D.modos[l.name] then l.blendMode = D.modos[l.name] end
end
s:saveAs(app.params["saida"])
print("montada: " .. #saida .. " células")
'''


def _hex(c):
    return "%02x%02x%02x%02x" % (c[0], c[1], c[2], c[3] if len(c) > 3 else 255)


def montar(caminho, w, h, camadas, quadros, pixels, ocultas=(), opacidade=None, modos=None, refazer=False):
    """`pixels[i][camada]` = {(x, y): (r, g, b[, a])} no quadro i (0..); `modos`: o modo de mistura de uma camada (o
    número do Aseprite: 14 multiplicar, 29 somar). Recusa sobrescrever sem `refazer`."""
    caminho = pathlib.Path(caminho)
    if caminho.exists() and not refazer:
        sys.exit(f"{caminho.name} já existe e é a autoridade; use --refazer para descartar os retoques e montar de novo.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        linhas = ["return {", f"w={w}, h={h},",
                  "camadas={" + ",".join(f'"{c}"' for c in camadas) + "},",
                  "quadros={" + ",".join(f'"{q}"' for q in quadros) + "},",
                  "ocultas={" + ",".join(f'["{c}"]=true' for c in ocultas) + "},",
                  "opacidade={" + ",".join(f'["{c}"]={v}' for c, v in (opacidade or {}).items()) + "},",
                  "modos={" + ",".join(f'["{c}"]={v}' for c, v in (modos or {}).items()) + "},",
                  "pixels={"]
        for q in range(len(quadros)):
            partes = []
            for c in camadas:
                px = pixels[q].get(c) or {}
                txt = ";".join(f"{x},{y},{_hex(cor)}" for (x, y), cor in sorted(px.items()) if 0 <= x < w and 0 <= y < h)
                partes.append(f'["{c}"]="{txt}"')
            linhas.append("{" + ",".join(partes) + "},")
        linhas += ["}", "}"]
        dados = tmp / "dados.lua"
        dados.write_text("\n".join(linhas), encoding="utf-8")
        lua = tmp / "montar.lua"
        lua.write_text(_MONTAR, encoding="utf-8")
        r = subprocess.run([aseprite(), "-b", "--script-param", f"pintar={PINTAR}", "--script-param", f"dados={dados}",
                            "--script-param", f"saida={caminho}", "--script", str(lua)], capture_output=True, text=True)
        ok = [x for x in r.stdout.splitlines() if x.startswith("montada")]
        if not ok or not caminho.exists():
            sys.exit(f"o Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
        return ok[0]


def quadros(fonte, pasta, ignorar=()):
    """Cada quadro achatado (as camadas visíveis, menos `ignorar`), em <pasta>/q<n>.png (n a partir de 1)."""
    cmd = [aseprite(), "-b"]
    for c in ignorar:
        cmd += ["--ignore-layer", c]
    subprocess.run(cmd + [str(fonte), "--save-as", str(pathlib.Path(pasta) / "q{frame1}.png")], capture_output=True, text=True)
    return sorted(pathlib.Path(pasta).glob("q*.png"), key=lambda p: int(p.stem[1:]))


def celulas(fonte, pasta):
    """As células de cada camada, quadro a quadro, em <pasta>/<camada>-<quadro>.png (quadro a partir de 0)."""
    pasta = pathlib.Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    script = pasta.parent / "celulas.lua"
    shutil.copy(CELULAS, script)
    subprocess.run([aseprite(), "-b", "--script-param", f"fonte={fonte}", "--script-param", f"pasta={pasta}",
                    "--script", str(script)], capture_output=True, text=True)
    return pasta
