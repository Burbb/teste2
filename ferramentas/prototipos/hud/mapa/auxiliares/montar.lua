-- Monta uma peça em camadas pela linha de comando do Aseprite (sem o conector), como o montar_camadas.lua de
-- ferramentas/arte/aseprite/, para peças que não são quadradas (w×h). Quem chama é o exportar.py:
--   Aseprite.exe -b --script-param w=<largura> --script-param h=<altura> --script-param listas=<pasta>
--                --script-param camadas=<a,b,...> --script-param saida=<.aseprite> --script-param pintar=<pintar.lua>
--                --script montar.lua
local P = dofile(app.params["pintar"])
local camadas = {}
for c in app.params["camadas"]:gmatch("[^,]+") do camadas[#camadas + 1] = c end
local s = Sprite(tonumber(app.params["w"]), tonumber(app.params["h"]), ColorMode.RGB)
s.layers[1].name = camadas[1]
for i = 2, #camadas do
  local l = s:newLayer(); l.name = camadas[i]
end
local t = {}
for _, c in ipairs(camadas) do t[#t + 1] = P.pintar_arquivo(c, app.params["listas"] .. "/" .. c .. ".lua") end
s:saveAs(app.params["saida"])
print(table.concat(t, " | "))
