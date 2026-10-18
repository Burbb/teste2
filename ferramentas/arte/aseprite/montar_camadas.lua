-- Monta uma fonte em camadas no Aseprite pela linha de comando (sem o conector do MCP), a partir das listas de pixels
-- por camada que os scripts de desenho gravam (pixel_comum.listas_camadas). Quem chama é o montar_fontes.py:
--   Aseprite.exe -b --script-param n=<lado> --script-param listas=<pasta> --script-param camadas=<a,b,...>
--                --script-param saida=<arquivo .aseprite> --script-param pintar=<pintar.lua> --script montar_camadas.lua
-- Cria o sprite RGBA n×n com as camadas de baixo para cima e pinta cada uma pelo pintar.lua (a releitura de cada
-- pixel vai na saída). Com um espaço no caminho do script, o Aseprite não o executa e não avisa: o montar_fontes.py o
-- copia para uma pasta temporária antes, e por isso o pintar.lua vem por parâmetro.
local P = dofile(app.params["pintar"])
local camadas = {}
for c in app.params["camadas"]:gmatch("[^,]+") do camadas[#camadas + 1] = c end
local n = tonumber(app.params["n"])
local s = Sprite(n, n, ColorMode.RGB)
s.layers[1].name = camadas[1]
for i = 2, #camadas do
  local l = s:newLayer(); l.name = camadas[i]
end
local t = {}
for _, c in ipairs(camadas) do t[#t + 1] = P.pintar_arquivo(c, app.params["listas"] .. "/" .. c .. ".lua") end
s:saveAs(app.params["saida"])
print(table.concat(t, " | "))
