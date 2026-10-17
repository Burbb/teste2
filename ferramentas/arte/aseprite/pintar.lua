-- Pintar e ler pixels numa camada pelo execute_script do aseprite-mcp-bridge, no lugar do put_pixels.
--
-- O put_pixels da extensão (1.0.0) tem dois defeitos, medidos em 16/10/2026:
--   1. descarta em silêncio o pixel fora do retângulo da cel (a cel feita pelo lápis ou deslocada é menor que a tela)
--      e mesmo assim responde pixels_set com o total pedido;
--   2. escreve direto na imagem da cel, o que o Aseprite não registra: o undo consome um passo vazio e o pixel fica.
-- Aqui a cel ganha uma imagem nova que cobre a cel antiga e a tela inteira, com o conteúdo antigo no mesmo lugar do
-- documento, os pixels pedidos por cima, e a troca acontece numa transação só (um passo de desfazer).
-- Coordenadas sempre do documento. Pixel fora da tela é recusado e contado, nunca descartado em silêncio.
--
-- Uso (execute_script):  local P = dofile("<caminho>/pintar.lua"); return P.pintar("camada", "x,y,RRGGBB[AA];...")
--                        ou P.pintar_arquivo("camada", "<arquivo .lua que faz return com o mesmo texto>")
-- O arquivo de dados é lido por dofile: o io.open de um script pede permissão numa janela do Aseprite e trava o
-- conector até alguém responder (medido: 60 s sem resposta).
local P = {}

local function camada(nome)
  local function busca(lista)
    for _, l in ipairs(lista) do
      if l.name == nome then return l end
      if l.isGroup then local a = busca(l.layers); if a then return a end end
    end
  end
  return busca(app.sprite.layers)
end

local function cor(hex)
  local r, g, b = tonumber(hex:sub(1, 2), 16), tonumber(hex:sub(3, 4), 16), tonumber(hex:sub(5, 6), 16)
  local a = #hex >= 8 and tonumber(hex:sub(7, 8), 16) or 255
  return app.pixelColor.rgba(r, g, b, a)
end

function P.pintar(nome, texto, rotulo)
  local s = app.sprite
  local l = camada(nome)
  if not l then error("camada não encontrada: " .. nome) end
  local lista, fora = {}, {}
  for x, y, h in texto:gmatch("(-?%d+),(-?%d+),#?(%x+)") do
    x, y = tonumber(x), tonumber(y)
    if x < 0 or y < 0 or x >= s.width or y >= s.height then fora[#fora + 1] = x .. "," .. y
    else lista[#lista + 1] = { x, y, cor(h) } end
  end
  local quadro = app.frame or s.frames[1]
  app.transaction(rotulo or ("Pintar " .. nome), function()
    local c = l:cel(quadro)
    local r = Rectangle(0, 0, s.width, s.height)
    if c then r = c.bounds:union(r) end
    local img = Image(r.width, r.height, s.colorMode)
    img:clear()
    if c then img:drawImage(c.image, Point(c.position.x - r.x, c.position.y - r.y), 255, BlendMode.SRC) end
    for _, p in ipairs(lista) do img:drawPixel(p[1] - r.x, p[2] - r.y, p[3]) end
    if c then c.image = img; c.position = Point(r.x, r.y)
    else s:newCel(l, quadro, img, Point(r.x, r.y)) end
  end)
  -- conferência: relê cada pixel pedido na cel gravada
  local c, erros = l:cel(quadro), 0
  for _, p in ipairs(lista) do
    if c.image:getPixel(p[1] - c.position.x, p[2] - c.position.y) ~= p[3] then erros = erros + 1 end
  end
  return string.format("%s: %d escritos, %d diferentes na releitura, %d fora da tela%s", nome, #lista, erros, #fora,
    #fora > 0 and (" (" .. table.concat(fora, " ") .. ")") or "")
end

function P.pintar_arquivo(nome, caminho, rotulo)
  return P.pintar(nome, dofile(caminho), rotulo)
end

-- Os pixels opacos da camada em coordenadas do documento ("x,y,RRGGBBAA;..."), e a cel.
function P.ler(nome)
  local l = camada(nome)
  if not l then error("camada não encontrada: " .. nome) end
  local c = l:cel(app.frame or app.sprite.frames[1])
  if not c then return nome .. ": sem cel" end
  local t = {}
  for p in c.image:pixels() do
    local v = p()
    local a = app.pixelColor.rgbaA(v)
    if a > 0 then
      t[#t + 1] = string.format("%d,%d,%02X%02X%02X%02X", c.position.x + p.x, c.position.y + p.y,
        app.pixelColor.rgbaR(v), app.pixelColor.rgbaG(v), app.pixelColor.rgbaB(v), a)
    end
  end
  return string.format("%s cel(%d,%d %dx%d) %d px: %s", nome, c.position.x, c.position.y, c.image.width,
    c.image.height, #t, table.concat(t, ";"))
end


-- Resumo das camadas: ordem, nome, visibilidade, cel e quantos pixels opacos.
function P.camadas()
  local t = {}
  local function vai(lista, prefixo)
    for _, l in ipairs(lista) do
      local c, n = l:cel(app.frame or app.sprite.frames[1]), 0
      if c and not l.isGroup then for p in c.image:pixels() do if app.pixelColor.rgbaA(p()) > 0 then n = n + 1 end end end
      t[#t + 1] = string.format("%s%d %s%s%s %dpx", prefixo, l.stackIndex, l.name, l.isGroup and " [grupo]" or "",
        l.isVisible and "" or " [oculta]", n)
      if l.isGroup then vai(l.layers, prefixo .. "  ") end
    end
  end
  vai(app.sprite.layers, "")
  return table.concat(t, " | ")
end

return P
