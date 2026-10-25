-- Exporta cada célula da forja-f.aseprite como PNG de 320×96 (<camada>-<quadro>.png) para o exportar_f.py montar as
-- tiras do jogo. Lê o que está no arquivo (os retoques feitos no Aseprite inclusive).
--   Aseprite.exe -b --script-param fonte=<forja-f.aseprite> --script-param pasta=<saída> --script exportar_forja.lua
local s = app.open(app.params["fonte"])
local pasta, n = app.params["pasta"], 0
for _, l in ipairs(s.layers) do
  for f = 1, #s.frames do
    local c = l:cel(f)
    if c then
      local img = Image(s.width, s.height, s.colorMode)
      img:drawImage(c.image, c.position)
      img:saveAs(pasta .. "/" .. l.name .. "-" .. (f - 1) .. ".png"); n = n + 1
    end
  end
end
print("celulas " .. n)
