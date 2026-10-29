-- Monta a fonte em camadas da B2 (b2.aseprite) pela linha de comando do Aseprite, a partir dos PNGs que o fonte.py
-- grava (<camada>.png, do tamanho do quadro). A camada "guia" (a referência na grade) entra oculta e meio transparente:
-- serve para desenhar por cima e fica fora da exportação. Quem chama é o fonte.py:
--   Aseprite.exe -b --script-param pasta=<pngs> --script-param camadas=<a,b,...> --script-param largura=<w>
--                --script-param altura=<h> --script-param saida=<arquivo .aseprite> --script montar.lua
local pasta, saida = app.params["pasta"], app.params["saida"]
local camadas = {}
for c in app.params["camadas"]:gmatch("[^,]+") do camadas[#camadas + 1] = c end
local s = Sprite(tonumber(app.params["largura"]), tonumber(app.params["altura"]), ColorMode.RGB)
local n = 0
for i, c in ipairs(camadas) do
  local l = (i == 1) and s.layers[1] or s:newLayer()
  l.name = c
  s:newCel(l, s.frames[1], Image{ fromFile = pasta .. "/" .. c .. ".png" }, Point(0, 0)); n = n + 1
  if c == "guia" then l.isVisible = false; l.opacity = 128 end
end
s:saveAs(saida)
print("celulas " .. n)
