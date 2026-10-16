-- Monta um documento da varinha no Aseprite (execute_script do aseprite-mcp-bridge): cria o sprite RGBA n×n, as
-- camadas na ordem de baixo para cima e pinta cada uma pelo pintar.lua com as listas de varinha_r2.py.
--   local M = dofile("<auxiliares>/montar.lua"); return M.montar(64, "<pasta das listas>/64/")
local AUX = debug.getinfo(1, "S").source:match("^@(.*[/\\])")
local P = dofile(AUX .. "pintar.lua")
local M = {}
M.CAMADAS = { "pomo", "empunhadura", "anel", "haste", "taca", "pedra", "garras", "contorno" }

function M.montar(n, pasta)
  local s = Sprite(n, n, ColorMode.RGB)
  s.layers[1].name = M.CAMADAS[1]
  for i = 2, #M.CAMADAS do
    local l = s:newLayer(); l.name = M.CAMADAS[i]
  end
  local t = {}
  for _, c in ipairs(M.CAMADAS) do t[#t + 1] = P.pintar_arquivo(c, pasta .. c .. ".lua") end
  return table.concat(t, " | ") .. " || " .. P.camadas()
end

return M
