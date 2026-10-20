-- L6: a forma de mão pedida pelo Jean (20/10/2026), a partir de uma imagem de banco que ele mostrou na conversa (só a
-- forma de uma mão enluvada; nem os detalhes, nem as cores, nem o arranjo das placas dela): a luva de pé, o punho em
-- cima com o topo arredondado, quase metade da altura; as costas da mão da largura do punho; os quatro dedos curtos (2
-- px), juntos, separados pela linha do contorno, as pontas em arco (os dois do meio mais longos); o polegar pequeno no
-- canto de baixo do lado oposto ao mínimo, dobrando para baixo, separado do indicador por um entalhe.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
-- o estudo da mão (oculto na fonte): o antebraço, as costas da mão, os quatro dedos e o polegar na mesma pose
D.estudo = {V, V, V,
l(12, "ssssssss"),
l(11, "ssssssssss"),
l(11, "ssssssssss"),
l(11, "ssssssssss"),
l(11, "ssssssssss"),
l(11, "ssssssssss"),
l(11, "ssssssssss"),
l(11, "ssssssssss"),
l(11, "ssssssssss"),
l(10, "ssssssssssss"),
l(10, "ssssssssssss"),
l(10, "ssssssssssss"),
l(10, "ssssssssssss"),
l(10, "ssssssssssss"),
l(10, "ssssssssssss", 22, "s"),
l(10, "ssssssssssss", 22, "ss"),
l(10, "ssssssssssss", 22, "ss"),
l(9, "st.st.st.st", 21, "ss"),
l(9, "st", 12, "st", 15, "st", 18, "st", 21, "ss"),
l(9, "st", 12, "st", 15, "st", 18, "st", 21, "s"),
l(9, "st", 12, "st", 15, "st", 18, "st"),
l(12, "st", 15, "st", 18, "t"),
l(12, "t", 15, "t"),
}
-- a luva por cima: o ferro aceso à esquerda; o punho com o topo arredondado e a beira de baixo virando; a lâmina sobre
-- as costas da mão; a linha dos nós; os dedos acesos à esquerda, as pontas na sombra; o polegar
D.tons = {V, V,
l(13, "677765"),
l(11, "6788776554"),
l(10, "567887765543"),
l(9, "45678877655432"),
l(9, "56788776655432"),
l(9, "56788776655432"),
l(9, "56787766554432"),
l(9, "56787766554432"),
l(9, "45677665544322"),
l(9, "67888877766554"),
l(9, "22222222222111"),
l(9, "56788776654432"),
l(9, "56788776654432"),
l(9, "56787766554432"),
l(9, "45677665544322"),
l(9, "45666655443322"),
l(9, "67777777766543"),
l(9, "45666666554432", 23, "5"),
l(9, "34555555443322", 23, "54"),
l(9, "23333333222211", 23, "54"),
l(9, "76", 12, "76", 15, "76", 18, "65", 21, "654"),
l(9, "65", 12, "76", 15, "76", 18, "65", 21, "543"),
l(9, "65", 12, "65", 15, "65", 18, "54", 21, "43"),
l(9, "54", 12, "65", 15, "65", 18, "43"),
l(9, "43", 12, "54", 15, "54", 18, "32"),
l(12, "43", 15, "43", 18, "32"),
l(12, "32", 15, "32"),
}
D.silhueta = D.tons
D.camadas = {
  {"punho", function(x, y) return y <= 12 end},
  {"polegar", function(x, y) return x >= 21 and y >= 19 end},
  {"dedos", function(x, y) return y >= 22 end},
  {"mao", function() return true end}}
return D
