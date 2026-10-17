-- Monta um documento no Aseprite (execute_script do aseprite-mcp-bridge): cria o sprite RGBA n×n, as camadas na
-- ordem dada (de baixo para cima) e pinta cada uma pelo pintar.lua com as listas de couro_r1.py.
--   local M = dofile("<auxiliares>/montar.lua")
--   return M.montar(64, "<pasta das listas>/gibao-64/", {"forro", "corpo", ..., "contorno"})
local AUX = debug.getinfo(1, "S").source:match("^@(.*[/\\])")
-- o pintar.lua mora em ferramentas/arte/aseprite/ (desta pasta: quatro níveis acima, depois arte/aseprite)
local P = dofile(AUX .. "../../../../arte/aseprite/pintar.lua")
local M = {}

function M.montar(n, pasta, camadas)
  local s = Sprite(n, n, ColorMode.RGB)
  s.layers[1].name = camadas[1]
  for i = 2, #camadas do
    local l = s:newLayer(); l.name = camadas[i]
  end
  local t = {}
  for _, c in ipairs(camadas) do t[#t + 1] = P.pintar_arquivo(c, pasta .. c .. ".lua") end
  return table.concat(t, " | ") .. " || " .. P.camadas()
end

return M
