-- Monta a fonte em camadas da Calça de Couro no Aseprite, pela linha de comando (sem o conector do MCP):
--   Aseprite.exe -b --script-param n=40 --script-param listas=<pasta das listas do tamanho> \
--                --script-param saida=<arquivo .aseprite> --script montar_fontes.lua
-- Cria o sprite RGBA n×n, as camadas de baixo para cima (as CAMADAS de desenhar_calca_couro_pixel.py) e pinta cada uma
-- pelo pintar.lua (ferramentas/arte/aseprite/), com as listas de pixels que o script em Python grava (--listas).
local P = dofile(app.params["pintar"])
local CAMADAS = { "pernas", "remendo", "cos", "barra", "braguilha", "desgaste", "contorno" }

local n = tonumber(app.params["n"])
local listas, saida = app.params["listas"], app.params["saida"]
local s = Sprite(n, n, ColorMode.RGB)
s.layers[1].name = CAMADAS[1]
for i = 2, #CAMADAS do
  local l = s:newLayer(); l.name = CAMADAS[i]
end
local t = {}
for _, c in ipairs(CAMADAS) do t[#t + 1] = P.pintar_arquivo(c, listas .. "/" .. c .. ".lua") end
s:saveAs(saida)
print(table.concat(t, " | "))
