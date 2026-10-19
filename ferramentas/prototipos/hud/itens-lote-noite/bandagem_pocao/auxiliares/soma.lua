-- O código de conferência do composto de cada sprite aberto (as camadas achatadas), igual ao de soma.py.
-- Uso (execute_script): return dofile("<caminho>/soma.lua")
local out = {}
for _, s in ipairs(app.sprites) do
  local img = Image(s.spec); img:clear(); img:drawSprite(s, 1)
  local h = 0
  for y = 0, s.height - 1 do for x = 0, s.width - 1 do
    local p = img:getPixel(x, y)
    local r, g, b, a = app.pixelColor.rgbaR(p), app.pixelColor.rgbaG(p), app.pixelColor.rgbaB(p), app.pixelColor.rgbaA(p)
    if a == 0 then r, g, b = 0, 0, 0 end
    h = (h * 31 + ((r * 256 + g) * 256 + b) * 2 + (a > 0 and 1 or 0)) % 2147483647
  end end
  local barra = string.char(92)  -- a barra invertida dos caminhos do Windows
  out[#out+1] = s.filename:match("[^/" .. barra .. barra .. "]+$") .. "=" .. h
end
return table.concat(out, " ")
