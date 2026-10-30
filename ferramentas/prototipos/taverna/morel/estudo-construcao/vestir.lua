-- Veste o braço de Morel sobre as juntas do estudo de construção (protótipo). Roda no Aseprite (pela ponte do
-- editor), com a vista aberta: POSES3 vem de `juntas.py --lua`; DESENHA_CABECA é a grade da cabeça feita à mão (na
-- fonte, camada morel_cabeca). O que este arquivo faz na fonte já está salvo em morel/vista/morel-vista.aseprite (a
-- fonte é a autoridade); ele fica aqui para refazer ou adaptar o método.
--
-- O braço é dois volumes de couro (o braço e o antebraço), cada um com a sua luz (a lareira e a vela, à esquerda e na
-- frente). Sem contorno: o antebraço fica um tom abaixo do braço e projeta sombra nele; o vinco de dentro do cotovelo
-- marca a dobra; o punho da manga escurece o fim do antebraço; a mão é uma bolinha de pele fechada no cabo; a colher é
-- rígida e o que afunda no caldo não aparece; o braço faz uma sombra de um pixel no que está embaixo (o peito, a mesa).
local rgba = app.pixelColor.rgba
local pc = app.pixelColor
local function C(h) return rgba(tonumber(h:sub(1,2),16), tonumber(h:sub(3,4),16), tonumber(h:sub(5,6),16), 255) end
local function escurece(v, k)
  return rgba(math.floor(pc.rgbaR(v) * k), math.floor(pc.rgbaG(v) * k), math.floor(pc.rgbaB(v) * k), 255)
end

V4 = {
  j = C("8a5a38"), a = C("6a4a2c"), b = C("4e3420"), c = C("33231a"), l = C("2a1c14"), w = C("1f150e"),
  pele = {C("c09070"), C("9a6c52"), C("6c4a38")}, punho = {C("3a2716"), C("2a1c14")},
  colher = C("9a9ca4"), brilho = C("cfd1d6"), caldo = C("6a2a14"),
}
-- o porte de Morel: braços grossos de couro
R4 = {ombro = 5.6, cotovelo = 4.6, cotoveloPerto = 5.1, antebraco = 4.6, punho = 3.3, maoX = 2.6, maoY = 2.3}
local LUZ = {-0.6, -0.55, 0.58}
do local n = math.sqrt(LUZ[1]^2 + LUZ[2]^2 + LUZ[3]^2); for i = 1, 3 do LUZ[i] = LUZ[i] / n end end

-- um volume (cápsula de ra a rb) num mapa: para cada pixel, a parte, o tom pela luz e o parâmetro t ao longo do eixo
local function volume0(mapa, parte, ax, ay, bx, by, ra, rb, realce)
  local dx, dy = bx - ax, by - ay; local L2 = math.max(dx*dx + dy*dy, 1)
  local r = math.max(ra, rb)
  for y = math.floor(math.min(ay, by) - r) - 1, math.ceil(math.max(ay, by) + r) + 1 do
    for x = math.floor(math.min(ax, bx) - r) - 1, math.ceil(math.max(ax, bx) + r) + 1 do
      local px, py = x + 0.5, y + 0.5
      local t = math.max(0, math.min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
      local rr = ra + (rb - ra) * t
      local ox, oy = px - (ax + t * dx), py - (ay + t * dy)
      if ox*ox + oy*oy <= rr * rr then
        local nx, ny = ox / rr, oy / rr; local nz = math.sqrt(math.max(0, 1 - nx*nx - ny*ny))
        local s = nx * LUZ[1] + ny * LUZ[2] + nz * LUZ[3]
        local tom = s > 0.78 and (realce and "j" or "a") or s > 0.5 and "a" or s > 0.12 and "b" or s > -0.25 and "c" or "l"
        mapa[y * 1000 + x] = {parte = parte, tom = tom, t = t}
      end
    end
  end
end
-- o antebraço um tom abaixo do braço: os dois segmentos se separam pelo valor (e do tampo da mesa, que tem o tom do
-- braço); a aresta que pega a luz continua clara
local DESCE = {j = "a", a = "b", b = "c", c = "l", l = "w"}
function V4.volume(mapa, parte, ax, ay, bx, by, ra, rb, realce)
  local tmp = {}
  volume0(tmp, parte, ax, ay, bx, by, ra, rb, realce or parte == "ante")
  if parte == "ante" then for _, v in pairs(tmp) do v.tom = DESCE[v.tom] end end
  for k, v in pairs(tmp) do mapa[k] = v end
end
function V4.dentro(mapa, x, y, parte)
  local p = mapa[y * 1000 + x]; return p and (parte == nil or p.parte == parte)
end
function V4.pinta(img, mapa)
  for k, v in pairs(mapa) do
    local x, y = k % 1000, math.floor(k / 1000)
    local cor = V4[v.tom]
    if v.punho then cor = (v.tom == "j" or v.tom == "a" or v.tom == "b") and V4.punho[1] or V4.punho[2] end
    if x >= 0 and y >= 0 and x < img.width and y < img.height then img:drawPixel(x, y, cor) end
  end
end

-- a sombra de um pixel, do lado oposto à luz, no que está embaixo (sob(x, y) dá a cor de lá, ou nil)
local function sombra_embaixo(img, ocupado, sob)
  local feitas = {}
  for k in pairs(ocupado) do
    local x, y = k % 1000, math.floor(k / 1000)
    for _, d in ipairs({{1, 0}, {0, 1}, {1, 1}}) do
      local qx, qy = x + d[1], y + d[2]; local kk = qy * 1000 + qx
      if not ocupado[kk] and not feitas[kk] and img:getPixel(qx, qy) == 0 then
        local c = sob(qx, qy)
        if c then img:drawPixel(qx, qy, escurece(c, 0.68)); feitas[kk] = true end
      end
    end
  end
end
local function mao(img, cx, cy, rx, ry, ocupado)
  for y = math.floor(cy) - 3, math.floor(cy) + 3 do for x = math.floor(cx) - 3, math.floor(cx) + 3 do
    local ox, oy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
    if ox*ox + oy*oy <= 1 then
      local s = -ox * 0.7 - oy * 0.7
      img:drawPixel(x, y, s > 0.35 and V4.pele[1] or s > -0.45 and V4.pele[2] or V4.pele[3])
      ocupado[y * 1000 + x] = true
    end
  end end
end

-- o braço da colher num quadro (P: uma linha de POSES3)
function BRACO4(img, P, sob)
  local S, E, W, T = P.S, P.E, P.W, P.T
  local mapa = {}
  local dSE = math.sqrt((S[1]-E[1])^2 + (S[2]-E[2])^2)
  -- em escorço (o braço apontando para quem olha) a ponta do cotovelo, mais perto, fica mais larga
  V4.volume(mapa, "braco", S[1], S[2], E[1], E[2], R4.ombro, dSE < 22 and R4.cotoveloPerto or R4.cotovelo, true)
  local fo = {}
  V4.volume(fo, "ante", E[1], E[2], W[1], W[2], R4.antebraco, R4.punho, false)
  for k, v in pairs(fo) do mapa[k] = v end  -- o antebraço passa na frente do braço
  -- a sombra do antebraço no braço
  local sombra = {}
  for k, v in pairs(mapa) do
    if v.parte == "braco" then
      local x, y = k % 1000, math.floor(k / 1000)
      if V4.dentro(mapa, x - 1, y, "ante") or V4.dentro(mapa, x, y - 1, "ante") or V4.dentro(mapa, x - 1, y - 1, "ante") then
        sombra[k] = true
      end
    end
  end
  for k in pairs(sombra) do mapa[k].tom = "l" end
  -- o vinco de dentro do cotovelo, quando o braço dobra mais que 120°
  local ux, uy = S[1] - E[1], S[2] - E[2]; local nu = math.sqrt(ux*ux + uy*uy); ux, uy = ux/nu, uy/nu
  local vx, vy = W[1] - E[1], W[2] - E[2]; local nv = math.sqrt(vx*vx + vy*vy); vx, vy = vx/nv, vy/nv
  if ux*vx + uy*vy > -0.5 then
    local bx, by = ux + vx, uy + vy; local nb = math.sqrt(bx*bx + by*by)
    if nb > 0.01 then
      bx, by = bx/nb, by/nb
      for k = 1, 4 do
        local p = mapa[math.floor(E[2] + by * k + 0.5) * 1000 + math.floor(E[1] + bx * k + 0.5)]
        if p then p.tom = "l" end
      end
    end
  end
  for _, v in pairs(mapa) do if v.parte == "ante" and v.t > 0.86 then v.punho = true end end
  V4.pinta(img, mapa)
  -- a colher: do punho fechado à concha; o que afunda no caldo não aparece
  local tx, ty = T[1] - W[1], T[2] - W[2]; local nt = math.sqrt(tx*tx + ty*ty); tx, ty = tx/nt, ty/nt
  local G = {W[1] + tx * 2.8, W[2] + ty * 2.8}
  local function afundado(x, y) return ((x + 0.5 - 216.5) / 13.5)^2 + ((y + 0.5 - 69.5) / 3.6)^2 <= 1 end
  local n = math.max(math.abs(T[1] - G[1]), math.abs(T[2] - G[2]))
  local ultima
  for k = 0, math.ceil(n) do
    local x = math.floor(G[1] + (T[1] - G[1]) * k / n + 0.5); local y = math.floor(G[2] + (T[2] - G[2]) * k / n + 0.5)
    if afundado(x, y) then break end
    img:drawPixel(x, y, V4.colher); ultima = {x, y}
  end
  if ultima and ultima[1] == T[1] and ultima[2] == T[2] then
    img:drawPixel(T[1], T[2], V4.brilho); img:drawPixel(T[1] + 1, T[2], V4.colher)
    img:drawPixel(T[1], T[2] + 1, V4.colher); img:drawPixel(T[1] + 1, T[2] + 1, V4.colher)
    if P.cheia then img:drawPixel(T[1] + 1, T[2], V4.caldo); img:drawPixel(T[1], T[2] + 1, V4.caldo) end
  end
  local ocupado = {}
  mao(img, G[1], G[2], R4.maoX, R4.maoY, ocupado)
  for k in pairs(mapa) do ocupado[k] = true end
  sombra_embaixo(img, ocupado, sob)
end

-- o braço de apoio no tampo: o cotovelo, o antebraço deitado para a tigela, o punho fechado (mesa(x, y): o tampo)
function MAOS4(mesa)
  local img = Image(320, 96, ColorMode.RGB)
  local mapa = {}
  V4.volume(mapa, "ante", 247, 61, 236, 72, R4.antebraco, R4.punho + 0.2, false)
  for _, v in pairs(mapa) do if v.t > 0.86 then v.punho = true end end
  V4.pinta(img, mapa)
  local ocupado = {}
  mao(img, 233.0, 73.8, 3.0, 2.6, ocupado)
  for k in pairs(mapa) do ocupado[k] = true end
  sombra_embaixo(img, ocupado, mesa)
  return img
end

-- o braço de cima do apoio, parado, no tronco (o casaco e o colete em `base`), com a ombreira de aço da v2 por cima
-- (`omb`, só os pixels de aço) e a sombra dela na fileira de baixo
function TRONCO4(base, omb)
  local tronco = base:clone()
  local mapa = {}
  V4.volume(mapa, "braco", 238, 35, 247, 61, R4.ombro, R4.cotovelo, true)
  for k in pairs(mapa) do
    local x, y = k % 1000, math.floor(k / 1000)
    for _, d in ipairs({{1,0},{0,1},{1,1}}) do
      local qx, qy = x + d[1], y + d[2]
      if not mapa[qy * 1000 + qx] then
        local v = tronco:getPixel(qx, qy)
        if pc.rgbaA(v) > 0 then tronco:drawPixel(qx, qy, escurece(v, 0.68)) end
      end
    end
  end
  V4.pinta(tronco, mapa)
  for y = 0, 94 do for x = 220, 255 do
    if pc.rgbaA(omb:getPixel(x, y)) > 0 and pc.rgbaA(omb:getPixel(x, y + 1)) == 0 and mapa[(y + 1) * 1000 + x] then
      tronco:drawPixel(x, y + 1, V4.l)
    end
  end end
  tronco:drawImage(omb, Point(0, 0))
  return tronco
end
