"""O roteiro Lua para montar uma fonte pelo conector do Aseprite (MCP, execute_script), a partir das listas por camada
(icones16.gravar): cria o documento 16×16 com as camadas de baixo para cima, pinta cada uma pelo pintar.lua (que relê
cada pixel), salva o .aseprite em fontes/<id>/ e fecha. Imprime o código para colar no execute_script.
    python montar_mcp.py <id>
"""
import sys

import icones16 as ic
from comum import LOTE, RAIZ

if __name__ == "__main__":
    ident = sys.argv[1]
    ic.gravar(LOTE, [ident])
    listas = (LOTE / f"listas/{ident}").as_posix()
    ordem = (LOTE / f"listas/{ident}/ordem.txt").read_text(encoding="utf-8").strip().split(",")
    fonte = LOTE / f"fontes/{ident}/{ident}-16.aseprite"
    fonte.parent.mkdir(parents=True, exist_ok=True)
    pintar = (RAIZ / "ferramentas/arte/aseprite/pintar.lua").as_posix()
    nomes = ", ".join(f'"{c}"' for c in ordem)
    print(f'''local P = dofile("{pintar}")
local camadas = {{{nomes}}}
local s = Sprite(16, 16, ColorMode.RGB)
s.layers[1].name = camadas[1]
for i = 2, #camadas do local l = s:newLayer(); l.name = camadas[i] end
local t = {{}}
for _, c in ipairs(camadas) do t[#t + 1] = P.pintar_arquivo(c, "{listas}/" .. c .. ".lua") end
s:saveAs("{fonte.as_posix()}")
s:close()
return table.concat(t, " | ")''')
