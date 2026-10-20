-- P5: livre em placas. As perneiras de perfil, num passo (como os ícones de pernas da Dungeon Crawl e do Idylwild, só
-- de estudo): o cinto de couro e as faltas em cima; as duas pernas abrindo em V invertido, viradas para a esquerda, a de
-- trás um tom mais escura; o coxote com a faixa de reflexo na frente e a beira de baixo escura; a joelheira pequena na
-- frente do joelho, integrada ao perfil; a greva com a beira da frente acesa; a beira do tornozelo.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
D.tons = {V, V, V,
l(11, "ffeee76edc"),
l(11, "eedd5443cb"),
l(10, "678887766543"),
l(10, "567776655432"),
l(10, "222222222211"),
l(10, "678765", 17, "566543"),
l(9, "678765", 17, "566543"),
l(9, "578765", 18, "456543"),
l(8, "578765", 18, "456543"),
l(8, "467654", 19, "455432"),
l(7, "222221", 19, "222211"),
l(6, "6887654", 19, "5665432"),
l(6, "5776543", 18, "4665432"),
l(7, "22221", 19, "222211"),
l(7, "78654", 19, "56543"),
l(7, "78654", 20, "56543"),
l(7, "78654", 20, "56543"),
l(7, "68654", 20, "56543"),
l(6, "68654", 20, "56543"),
l(6, "68654", 20, "46543"),
l(6, "57543", 20, "45432"),
l(6, "22221", 20, "22221"),
l(5, "6787654", 19, "5676543"),
l(5, "3444332", 19, "2333221"),
}
D.silhueta = D.tons
D.camadas = {
  {"cinto", function(x, y) return y <= 4 end},
  {"faltas", function(x, y) return y <= 7 end},
  {"perna_de_tras", function(x, y) return x >= 17 end},
  {"perna_da_frente", function() return true end}}
return D
