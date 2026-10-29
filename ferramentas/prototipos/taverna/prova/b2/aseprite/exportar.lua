-- Exporta cada camada da b2.aseprite como PNG do tamanho do quadro (<camada>.png) e lista as camadas com a
-- visibilidade ("camada <nome> <0|1>"), para o fonte.py compor a imagem sem a guia. Lê o arquivo como está (os
-- retoques feitos no Aseprite inclusive).
--   Aseprite.exe -b --script-param fonte=<b2.aseprite> --script-param pasta=<saída> --script exportar.lua
local s = app.open(app.params["fonte"])
local pasta = app.params["pasta"]
for _, l in ipairs(s.layers) do
  local img = Image(s.width, s.height, s.colorMode)
  local c = l:cel(1)
  if c then img:drawImage(c.image, c.position) end
  img:saveAs(pasta .. "/" .. l.name .. ".png")
  print("camada " .. l.name .. " " .. (l.isVisible and 1 or 0))
end
