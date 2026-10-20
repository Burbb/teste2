-- O desenho à mão da manopla e das perneiras (a rodada 5, 20/10/2026), pixel a pixel no Aseprite: cada etapa é uma grade
-- de texto (um caractere por pixel) escrita à mão, aplicada numa camada pelo pintar.lua (o fluxo seguro: cel cobrindo a
-- tela, um passo de desfazer, releitura). Nada é calculado por fórmula: a grade é o desenho.
--   "." vazio (não pinta)   "0".."8" o ferro (a rampa da família, do escuro ao claro)   "a".."f" o couro (do escuro ao claro)
-- Uso (execute_script):
--   local G = dofile("<pasta>/auxiliares/grade.lua")
--   G.aplicar("camada", {"....", ...}, filtro)  -- filtro(x, y) opcional: só os pixels em que ele devolve true
--   G.contorno("contorno")                       -- o contorno de 1 px pelos lados, em volta do que as outras camadas têm
--   G.limpar("camada")                           -- apaga a camada (para refazer uma etapa)
local G = {}
local RAIZ = "C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/"
local P = dofile(RAIZ .. "arte/aseprite/pintar.lua")

G.FERRO = {"0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"}
G.COURO = {a = "140b09", b = "251412", c = "3a1f1a", d = "522c23", e = "6b3b2d", f = "86503c"}
G.CONTORNO = "08080a"

local function cor(ch)
  local n = tonumber(ch)
  if n then return G.FERRO[n + 1] end
  return G.COURO[ch]
end

local function camada(nome)
  for _, l in ipairs(app.sprite.layers) do if l.name == nome then return l end end
  local l = app.sprite:newLayer(); l.name = nome; return l
end

function G.aplicar(nome, linhas, filtro)
  camada(nome)
  local lista = {}
  for y, linha in ipairs(linhas) do
    for x = 1, #linha do
      local ch = linha:sub(x, x)
      if ch ~= "." and ch ~= " " and (not filtro or filtro(x - 1, y - 1)) then
        local c = cor(ch)
        if not c then error("caractere sem cor: " .. ch .. " em " .. (x - 1) .. "," .. (y - 1)) end
        lista[#lista + 1] = (x - 1) .. "," .. (y - 1) .. "," .. c
      end
    end
  end
  if #lista == 0 then return nome .. ": nada" end
  return P.pintar(nome, table.concat(lista, ";"))
end

function G.limpar(nome)
  for _, l in ipairs(app.sprite.layers) do
    if l.name == nome then
      for _, cel in ipairs(l.cels) do app.sprite:deleteCel(cel) end
    end
  end
end

-- o que está pintado no composto das outras camadas (visíveis), para o contorno
local function forma(exceto)
  local s = app.sprite
  local img = Image(s.spec); img:clear()
  for _, l in ipairs(s.layers) do
    if l.isVisible and l.name ~= exceto then
      local cel = l:cel(1)
      if cel then img:drawImage(cel.image, cel.position) end
    end
  end
  return img
end

function G.contorno(nome)
  local s = app.sprite
  local img = forma(nome)
  local cheio = function(x, y)
    if x < 0 or y < 0 or x >= s.width or y >= s.height then return false end
    return app.pixelColor.rgbaA(img:getPixel(x, y)) > 0
  end
  local lista = {}
  for y = 0, s.height - 1 do
    for x = 0, s.width - 1 do
      if not cheio(x, y) and (cheio(x - 1, y) or cheio(x + 1, y) or cheio(x, y - 1) or cheio(x, y + 1)) then
        lista[#lista + 1] = x .. "," .. y .. "," .. G.CONTORNO
      end
    end
  end
  G.limpar(nome); camada(nome)
  return P.pintar(nome, table.concat(lista, ";"))
end

return G
