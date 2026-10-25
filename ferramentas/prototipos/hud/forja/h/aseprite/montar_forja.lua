-- Monta a fonte em camadas da forja F (forja-f.aseprite) pela linha de comando do Aseprite, a partir das camadas que o
-- desenhar_f.py grava (<camada>-<quadro>.png, 320×96, um quadro por estado do ferreiro). Quem chama é o desenhar_f.py:
--   Aseprite.exe -b --script-param pasta=<pngs> --script-param camadas=<a,b,...> --script-param estados=<a,b,...>
--                --script-param saida=<arquivo .aseprite> --script montar_forja.lua
local pasta, saida = app.params["pasta"], app.params["saida"]
local camadas, estados = {}, {}
for c in app.params["camadas"]:gmatch("[^,]+") do camadas[#camadas + 1] = c end
for c in app.params["estados"]:gmatch("[^,]+") do estados[#estados + 1] = c end
local s = Sprite(320, 96, ColorMode.RGB)
local L = {}
s.layers[1].name = camadas[1]; L[camadas[1]] = s.layers[1]
for i = 2, #camadas do local l = s:newLayer(); l.name = camadas[i]; L[camadas[i]] = l end
for f = 2, #estados do s:newEmptyFrame() end
local n = 0
for f = 1, #estados do
  s.frames[f].duration = 0.1
  for _, c in ipairs(camadas) do
    local arq = pasta .. "/" .. c .. "-" .. (f - 1) .. ".png"
    if app.fs.isFile(arq) then
      s:newCel(L[c], s.frames[f], Image{ fromFile = arq }, Point(0, 0)); n = n + 1
    end
  end
  local t = s:newTag(f, f); t.name = estados[f]
end
s:saveAs(saida)
print("celulas " .. n)
