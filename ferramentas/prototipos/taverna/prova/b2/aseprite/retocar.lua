-- Retoca a b2.aseprite pela linha de comando: pinta pixels numa camada e salva o arquivo (o retoque fica na fonte; a
-- exportação o lê dali). A lista vem num arquivo de texto, uma linha por pixel: "x y #rrggbb".
--   Aseprite.exe -b --script-param fonte=<b2.aseprite> --script-param camada=<nome> --script-param lista=<txt>
--                --script retocar.lua
local s = app.open(app.params["fonte"])
local alvo
for _, l in ipairs(s.layers) do if l.name == app.params["camada"] then alvo = l end end
assert(alvo, "camada não encontrada: " .. app.params["camada"])
local c = alvo:cel(1)
local img = Image(s.width, s.height, s.colorMode)
if c then img:drawImage(c.image, c.position) end
local n = 0
for linha in io.lines(app.params["lista"]) do
  local x, y, cor = linha:match("^(%d+) (%d+) #(%x+)$")
  if x then
    local v = tonumber(cor, 16)
    img:drawPixel(tonumber(x), tonumber(y), app.pixelColor.rgba((v >> 16) & 255, (v >> 8) & 255, v & 255, 255))
    n = n + 1
  end
end
s:newCel(alvo, 1, img, Point(0, 0))
s:saveAs(app.params["fonte"])
print("pintados " .. n)
