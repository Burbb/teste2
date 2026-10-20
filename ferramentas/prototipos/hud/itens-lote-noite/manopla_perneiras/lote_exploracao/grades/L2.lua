-- L2: a manopla de placas pela prancha Raven Fantasy (referencias/Luvas/1.gif, a manopla de aço da 2.ª linha, 3.ª
-- coluna: a caixa (630, 410, 790, 580)): o punho em sino no alto à esquerda, com a boca; a mão descendo para baixo e à
-- direita; os dedos abertos apontando para baixo, em segmentos; o polegar à esquerda.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
-- o estudo da mão (a camada estudo_mao, oculta): o antebraço descendo da esquerda; a palma alargando para baixo e à
-- direita; a linha dos nós; os dedos abertos em leque para baixo (o indicador junto do polegar, o médio o mais longo, o
-- anelar quase do tamanho do indicador, o mínimo o mais curto, abrindo para a direita); o polegar com a base na palma,
-- descendo à esquerda, separado do indicador
D.estudo = {V, V,
l(4, "sssssss"),
l(5, "sssssss"),
l(6, "sssssss"),
l(7, "sssssss"),
l(8, "sssssss"),
l(9, "sssssss"),
l(10, "sssssss"),
l(10, "ssssssss"),
l(9, "ssssssssss"),
l(9, "sssssssssss"),
l(9, "ssssssssssss"),
l(7, "sssssssssssssss"),
l(6, "ssssssssssssssss"),
l(5, "sss", 9, "sssssssssssss"),
l(4, "sss", 10, "ssssssssssss"),
l(4, "sss", 10, "sssssssssssssss"),
l(4, "ss", 10, "sss", 14, "sss", 18, "sss", 22, "sss"),
l(10, "sss", 14, "sss", 18, "sss", 23, "sss"),
l(9, "sss", 14, "sss", 19, "sss", 23, "sss"),
l(9, "sss", 14, "sss", 19, "sss", 23, "ss"),
l(9, "sss", 14, "sss", 19, "sss"),
l(9, "ss", 14, "sss", 19, "sss"),
l(14, "sss", 19, "ss"),
l(14, "ss"),
V, V, V, V, V, V}
-- a manopla por cima do estudo: o sino com a boca à mostra (a beira de trás acesa, o vazio escuro dentro, a beira da
-- frente clara); a lâmina do pulso na sombra; a placa da mão abaulada; a placa dos nós, larga, com as raízes dos dedos
-- juntas embaixo dela; os dedos separados só por 1 px, cada um aceso em cima, com as juntas em alturas diferentes;
-- o polegar à esquerda, em dois segmentos
D.tons = {V,
l(2, "56777765"),
l(1, "62111111254"),
l(1, "788877766554"),
l(2, "678866655443"),
l(4, "67886655443"),
l(6, "6788665443"),
l(8, "567866543"),
l(9, "456665432"),
l(10, "233333221"),
l(9, "5677665432"),
l(9, "56788766543"),
l(9, "567887766543"),
l(7, "56" .. "5678877665432"),
l(6, "675" .. "45677666554322"),
l(5, "675", 9, "34555554443322"),
l(4, "564", 10, "67777766655443"),
l(4, "453", 10, "566666555443322"),
l(4, "43", 10, "342234223421231"),
l(10, "675", 14, "786", 18, "675", 22, "564"),
l(9, "342", 14, "453", 19, "342", 23, "342"),
l(9, "675", 14, "786", 19, "675", 23, "43"),
l(9, "564", 14, "675", 19, "564"),
l(9, "43", 14, "453", 19, "43"),
l(14, "675"),
l(14, "54"),
V, V, V, V, V, V}
-- o desenho 1 px para dentro do quadro (a manchete encostava no canto): o deslocamento de toda a grade, sem redesenho
local function para_dentro(g)
  local n = {G.VAZIA}
  for i = 1, #g - 1 do n[#n + 1] = "." .. g[i]:sub(1, 31) end
  return n
end
D.tons = para_dentro(D.tons)
D.estudo = para_dentro(D.estudo)
D.silhueta = D.tons
D.camadas = {
  {"manchete", function(x, y) return y <= 9 end},
  {"pulso", function(x, y) return y == 10 end},
  {"polegar", function(x, y) return y >= 14 and x <= 9 end},
  {"dedos", function(x, y) return y >= 19 end},
  {"mao", function() return true end}}
return D
