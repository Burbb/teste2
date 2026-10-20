-- A troca de material das bases B4 e B5 (as luvas glove_03 e glove_04 da Dungeon Crawl Stone Soup, CC0, via a coleção
-- CC0 Hand Wear Icons; 20/10/2026), de armadura pesada para malha de ferro, sobre uma cópia do sprite original. Nenhum
-- pixel muda de lugar: a silhueta, o contorno, a pose, os dedos, o polegar e o punho são os do original.
--   * o contorno de fora e as linhas pretas entre os dedos ficam (na cor do contorno da família);
--   * cada pixel de dentro vira um tom da rampa de ferro pela luminosidade do original (a luz e a sombra seguem o volume
--     que o artista desenhou; o ouro vira o ferro do mesmo valor);
--   * na mão e no punho, a malha como na cota: o xadrez de dois tons vizinhos (o tom do volume e o de baixo); os vincos
--     pretos de dentro das placas viram malha escura;
--   * nos dedos (e no polegar), o tom liso, sem o xadrez, para não apagar a separação nem as juntas;
--   * os rebites, os pontos brancos e o ouro (ornamento, não volume) viram a malha no tom dos vizinhos (nos dedos, um tom
--     acima: o brilho do nó).
-- Uso (execute_script): local C = dofile("<pasta>/auxiliares/malha_dcss.lua"); return C.converter(<png original>, <destino .aseprite>)
local C = {}
C.FERRO = {"0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"}
C.CONTORNO = "08080a"

local function cor(h) return app.pixelColor.rgba(tonumber(h:sub(1, 2), 16), tonumber(h:sub(3, 4), 16), tonumber(h:sub(5, 6), 16), 255) end

-- os dedos e o polegar, nas duas bases (a mesma mão): acima da linha dos nós
function C.dedo(x, y)
  if y <= 9 then return true end
  if y <= 12 then return x >= 19 end
  return false
end

C.COURO = {"251412", "3a1f1a", "522c23", "6b3b2d", "86503c"}   -- do escuro ao claro (a rampa da família)

-- tira(x, y, r, g, b): opcional, os pixels da divisa entre o punho e a mão (onde o original tinha a faixa ou a borda da
-- placa), que viram uma tira de couro discreta
function C.converter(png, destino, tira)
  local orig = app.open(png)
  local img = Image(orig.width, orig.height, ColorMode.RGB); img:clear(); img:drawSprite(orig, 1)
  orig:close()
  local W, H = img.width, img.height
  local function px(x, y)
    if x < 0 or y < 0 or x >= W or y >= H then return nil end
    local p = img:getPixel(x, y)
    if app.pixelColor.rgbaA(p) == 0 then return nil end
    return app.pixelColor.rgbaR(p), app.pixelColor.rgbaG(p), app.pixelColor.rgbaB(p)
  end
  local function lum(r, g, b) return 0.3 * r + 0.59 * g + 0.11 * b end
  local function preto(r, g, b) return r + g + b < 12 end
  local function branco(r, g, b) return r > 235 and g > 235 and b > 220 end
  local function ouro(r, g, b) return r - b > 40 end                    -- os acabamentos dourados (a B4)
  -- o tom do volume pela luminosidade, na faixa da cota
  local NIVEIS = {{18, 2}, {27, 3}, {38, 4}, {58, 5}, {88, 6}, {999, 7}}
  local function tom(l) for _, n in ipairs(NIVEIS) do if l < n[1] then return n[2] end end end
  local tons = {}
  for y = 0, H - 1 do tons[y] = {} for x = 0, W - 1 do
    local r, g, b = px(x, y)
    if r and not preto(r, g, b) and not branco(r, g, b) and not ouro(r, g, b) then tons[y][x] = tom(lum(r, g, b)) end
  end end
  local function vizinhos(x, y)
    local s, n = 0, 0
    for _, d in ipairs({{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}}) do
      local t = tons[y + d[2]] and tons[y + d[2]][x + d[1]]
      if t then s = s + t; n = n + 1 end
    end
    return n > 0 and math.floor(s / n + 0.5) or 4
  end
  local copia = Image(W, H, ColorMode.RGB); copia:clear()
  local nova = Image(W, H, ColorMode.RGB); nova:clear()
  local couro = Image(W, H, ColorMode.RGB); couro:clear()
  local conta = {contorno = 0, malha = 0, dedo = 0, rebite = 0, vinco = 0, couro = 0}
  for y = 0, H - 1 do for x = 0, W - 1 do
    local r, g, b = px(x, y)
    if r then
      copia:drawPixel(x, y, app.pixelColor.rgba(r, g, b, 255))
      local fora = not px(x + 1, y) or not px(x - 1, y) or not px(x, y + 1) or not px(x, y - 1)
      local h
      if preto(r, g, b) then
        if fora or C.dedo(x, y) then h = C.CONTORNO; conta.contorno = conta.contorno + 1
        else h = C.FERRO[((x + y) % 2 == 0 and 3 or 2) + 1]; conta.vinco = conta.vinco + 1 end
      else
        local t = tons[y][x]
        if not t then t = math.min(8, vizinhos(x, y) + (C.dedo(x, y) and 1 or 0)); conta.rebite = conta.rebite + 1 end
        if C.dedo(x, y) then h = C.FERRO[t + 1]; conta.dedo = conta.dedo + 1
        elseif tira and not fora and tira(x, y, r, g, b) then
          couro:drawPixel(x, y, cor(C.COURO[math.max(1, math.min(5, t - 1))])); conta.couro = conta.couro + 1
        else
          -- a malha: um tom acima e um abaixo do volume, alternando (a média é o volume)
          t = (x + y) % 2 == 0 and math.min(t + 1, 8) or math.max(t - 1, 1)
          h = C.FERRO[t + 1]; conta.malha = conta.malha + 1
        end
      end
      if h then nova:drawPixel(x, y, cor(h)) end
    end
  end end
  local s = Sprite(W, H, ColorMode.RGB)
  s.layers[1].name = "original"
  app.transaction(function()
    s:newCel(s.layers[1], 1, copia, Point(0, 0))
    local l = s:newLayer(); l.name = "malha"
    s:newCel(l, 1, nova, Point(0, 0))
    if conta.couro > 0 then local c = s:newLayer(); c.name = "couro"; s:newCel(c, 1, couro, Point(0, 0)) end
    s.layers[1].isVisible = false
  end)
  s:saveAs(destino)
  return string.format("contorno %d, malha %d, dedos %d, rebites %d, vincos %d, couro %d", conta.contorno, conta.malha, conta.dedo, conta.rebite, conta.vinco, conta.couro)
end

return C
