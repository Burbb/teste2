-- Troca as células de UMA camada da fonte da forja (forja-h2.aseprite) pelas imagens <camada>-<quadro>.png de uma pasta
-- (320×96, um quadro por estado), e salva. As outras camadas, as tags e as durações não mudam. Quem chama é o
-- consolidar_gesto.py:
--   Aseprite.exe -b --script-param fonte=<arquivo> --script-param pasta=<pngs> --script-param camada=<nome>
--                --script trocar_camada.lua
local s = app.open(app.params["fonte"])
local pasta, nome, n = app.params["pasta"], app.params["camada"], 0
local camada
for _, l in ipairs(s.layers) do if l.name == nome then camada = l end end
if not camada then print("sem camada " .. nome); return end
for f = 1, #s.frames do
  local arq = pasta .. "/" .. nome .. "-" .. (f - 1) .. ".png"
  if app.fs.isFile(arq) then
    if camada:cel(f) then s:deleteCel(camada, f) end
    s:newCel(camada, s.frames[f], Image{ fromFile = arq }, Point(0, 0)); n = n + 1
  end
end
s:saveAs(app.params["fonte"])
print("celulas " .. n)
