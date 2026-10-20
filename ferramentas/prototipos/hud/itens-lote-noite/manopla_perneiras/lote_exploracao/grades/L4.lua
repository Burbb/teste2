-- L4: livre em placas. O punho cerrado de frente: os quatro dedos dobrados lado a lado (cada um com a placa da falange
-- e o nó em cima; o mínimo mais estreito e mais baixo, o médio o mais alto), o polegar dobrado atravessando por cima do
-- indicador e do médio, a base da mão embaixo, o pulso e o manguito abrindo para baixo.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
-- o estudo da mão fechada (a camada estudo_mao, oculta): os quatro dedos dobrados, as falanges do meio de frente, os nós
-- em cima em alturas diferentes; o polegar dobrado por cima do indicador e do médio, com a base grossa saindo da lateral
-- esquerda da palma; a base da mão e o pulso embaixo
D.estudo = {V, V, V, V, V, V,
l(14, "ss"),
l(8, "ssss", 13, "ssss", 18, "ssss"),
l(8, "sssstsssstsssst", 23, "ss"),
l(8, "sssstsssstsssstsss"),
l(8, "ttttuttttuttttuttt"),
l(8, "sssstsssstsssstsss"),
l(6, "sssssssssss", 17, "tsssstsss"),
l(5, "ssssssssssss", 17, "tsssstsss"),
l(5, "tttttttttttt", 17, "sssssssss"),
l(6, "sssssssssssssssssss"),
l(7, "sssssssssssssssss"),
l(8, "sssssssssssssss"),
l(10, "sssssssssss"),
l(10, "sssssssssss"),
V, V, V, V, V, V, V, V, V, V, V, V}
-- a manopla por cima do estudo: uma placa por dedo, com o nó aceso em cima e o vinco escuro entre eles; a dobra da
-- junta; as pontas recolhidas em placas menores; o polegar em placa, a beira de cima acesa e a sombra embaixo; a base
-- da mão; a lâmina do pulso na sombra; o manguito curto em sino, com a beira de baixo virando
D.tons = {V, V, V, V, V, V,
l(14, "77"),
l(8, "6776", 13, "7887", 18, "6776"),
l(8, "5665", 12, "2", 13, "6776", 17, "2", 18, "5665", 22, "2", 23, "55"),
l(8, "4554", 12, "1", 13, "5665", 17, "1", 18, "4554", 22, "1", 23, "454"),
l(8, "2222", 12, "1", 13, "2222", 17, "1", 18, "2222", 22, "1", 23, "222"),
l(8, "5665", 12, "2", 13, "6776", 17, "2", 18, "5665", 22, "2", 23, "454"),
l(6, "67777776665", 17, "2", 18, "4554", 22, "2", 23, "343"),
l(5, "566666655543", 17, "2", 18, "4554", 22, "2", 23, "343"),
l(5, "122222222221", 17, "333333322"),
l(6, "4555555444443333322"),
l(7, "34444443333332222"),
l(8, "455555544433322"),
l(10, "22222222221"),
l(10, "56666655443"),
l(9, "4566666554432"),
l(8, "567777666554432"),
l(7, "56788776665544322"),
l(7, "567887766655443322"),
l(6, "7888877766665544332"),
l(6, "3333333222222222111"),
V, V, V, V, V, V}
D.silhueta = D.tons
D.camadas = {
  {"polegar", function(x, y) return y >= 12 and y <= 14 and x <= 16 end},
  {"dedos", function(x, y) return y <= 14 end},
  {"manguito", function(x, y) return y >= 18 end},
  {"mao", function() return true end}}
return D
