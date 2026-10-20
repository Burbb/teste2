-- O desenho à mão da manopla e das perneiras (a rodada 5, 20/10/2026), pixel a pixel no Aseprite: cada etapa é uma grade
-- de texto (um caractere por pixel) escrita à mão, aplicada numa camada pelo pintar.lua (o fluxo seguro: cel cobrindo a
-- tela, um passo de desfazer, releitura). Nada é calculado por fórmula: a grade é o desenho.
--   "." vazio (não pinta)   "0".."8" o ferro (a rampa da família, do escuro ao claro)   "a".."f" o couro (do escuro ao claro)
--   "A".."I" a malha no tom 0..8 (o xadrez dos anéis, como na cota)
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
-- o estudo da mão (a camada auxiliar estudo_mao, oculta): a mão nua na pose da luva, para conferir a anatomia
G.PELE = {s = "d9a98a", t = "a8755c", u = "6e4636"}

-- a malha (o lote de exploração, 20/10/2026): "A".."I" é a malha no tom 0..8, como na cota aprovada: um xadrez de dois
-- tons vizinhos (o tom e o de baixo), como um pincel de padrão; a área e o tom de cada pixel continuam desenhados à mão
local function cor(ch, x, y)
  local n = tonumber(ch)
  if n then return G.FERRO[n + 1] end
  local b = string.byte(ch)
  if b >= 65 and b <= 73 then
    local t = b - 65
    if (x + y) % 2 == 1 then t = math.max(t - 1, 0) end
    return G.FERRO[t + 1]
  end
  if ch == "s" or ch == "t" or ch == "u" then return G.PELE[ch] end
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
        local c = cor(ch, x - 1, y - 1)
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

-- Um candidato do lote de exploração: o arquivo de grades (lote_exploracao/grades/<id>.lua) devolve
--   { silhueta = {...}, tons = {...}, camadas = { {"nome", filtro(x, y, ch)}, ... } }  (tons e camadas podem faltar)
-- etapa "estudo": só a mão nua (estudo, visível); etapa "silhueta": a camada silhueta numa cor e o contorno; etapa
-- "volumes": as camadas pelos tons (cada pixel vai para a primeira camada cujo filtro aceita) e o contorno. Quando há
-- estudo, ele fica na camada estudo_mao, embaixo e oculta (fora do contorno e da exportação). Grava em <destino>.
function G.candidato(arquivo, destino, etapa)
  local def = dofile(arquivo)
  for _, s in ipairs(app.sprites) do if s.filename == destino then s:close() end end
  if etapa == "estudo" then
    local s = Sprite(32, 32, ColorMode.RGB)
    s.layers[1].name = "estudo_mao"
    local r = G.aplicar("estudo_mao", def.estudo)
    s:saveAs(destino)
    return r
  end
  local grade = etapa == "silhueta" and def.silhueta or def.tons
  for i, l in ipairs(grade) do if #l ~= 32 then error("linha " .. (i - 1) .. " com " .. #l) end end
  if #grade > 32 then error(#grade .. " linhas") end
  while #grade < 32 do grade[#grade + 1] = G.VAZIA end                -- completa embaixo com linhas vazias
  if def.estudo then while #def.estudo < 32 do def.estudo[#def.estudo + 1] = G.VAZIA end end
  local s = Sprite(32, 32, ColorMode.RGB)
  local out = {}
  if etapa == "silhueta" then
    s.layers[1].name = "silhueta"
    local sil = {}
    for i, l in ipairs(def.silhueta) do sil[i] = l:gsub("[^%.]", "5") end
    out[#out + 1] = G.aplicar("silhueta", sil)
  else
    s.layers[1].name = def.camadas[1][1]
    for _, c in ipairs(def.camadas) do camada(c[1]) end
    local dono = function(x, y, ch)
      for _, c in ipairs(def.camadas) do if c[2](x, y, ch) then return c[1] end end
      return def.camadas[#def.camadas][1]
    end
    for _, c in ipairs(def.camadas) do
      out[#out + 1] = G.aplicar(c[1], def.tons, function(x, y)
        local ch = def.tons[y + 1]:sub(x + 1, x + 1)
        return dono(x, y, ch) == c[1]
      end)
    end
  end
  out[#out + 1] = G.contorno("contorno")
  if def.estudo then
    out[#out + 1] = G.aplicar("estudo_mao", def.estudo)
    for _, l in ipairs(s.layers) do
      if l.name == "estudo_mao" then l.stackIndex = 1; l.isVisible = false; l.opacity = 160 end
    end
  end
  s:saveAs(destino)
  return table.concat(out, " | ")
end

-- uma linha de 32 pixels com trechos em posições dadas: G.linha(7, "5555", 20, "666") (o resto vazio)
function G.linha(...)
  local a = {...}
  local t = {}
  for i = 1, 32 do t[i] = "." end
  for i = 1, #a, 2 do
    local x0, s = a[i], a[i + 1]
    for k = 1, #s do t[x0 + k] = s:sub(k, k) end
  end
  return table.concat(t)
end
G.VAZIA = "................................"

-- os filtros por material, para as camadas
function G.ferro(x, y, ch) return ch:match("%d") ~= nil end
function G.malha(x, y, ch) return ch:match("[A-I]") ~= nil end
function G.couro(x, y, ch) return ch:match("[a-f]") ~= nil end

return G
