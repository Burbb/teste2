-- P2: as perneiras de placas pela prancha de armaduras de pernas (referencias/calça/1.gif, as "Lion Knight Legs", a 2.ª
-- da 2.ª linha; a construção, sem os leões): de frente, o cinto de couro com a fivela; as faltas curtas em duas lâminas
-- (sem placa central); as pernas separadas logo abaixo delas; os coxotes com a faixa de reflexo; a joelheira da largura
-- da perna, a beira de cima acesa e a sombra embaixo (sem inchaço nem asas); as grevas afinando; a beira do tornozelo.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
D.tons = {V, V, V, V,
l(8, "ffffeee76eddddcc"),
l(8, "eeeddd4553cccbbb"),
l(8, "6788776666554433"),
l(8, "5677665555443322"),
l(7, "222222221222222222"),
l(7, "678877665655544332"),
l(7, "57887654", 17, "56776543"),
l(6, "568876543", 17, "567765432"),
l(6, "568876543", 17, "567765432"),
l(6, "457765432", 17, "456654322"),
l(6, "122222221", 17, "122222211"),
l(7, "57876543", 17, "56765432"),
l(7, "46777654", 17, "45666543"),
l(7, "57888765", 17, "56777654"),
l(7, "46777654", 17, "45666543"),
l(8, "344443", 18, "333332"),
l(8, "222221", 18, "222211"),
l(8, "687654", 18, "576543"),
l(8, "587654", 18, "576543"),
l(8, "587654", 18, "576543"),
l(8, "587654", 18, "476543"),
l(8, "476543", 18, "465432"),
l(7, "12222221", 17, "12222211"),
l(7, "67776544", 17, "56665433"),
}
D.silhueta = D.tons
D.camadas = {
  {"cinto", function(x, y) return y <= 5 end},
  {"faltas", function(x, y) return y <= 9 end},
  {"joelhos", function(x, y) return y >= 16 and y <= 20 end},
  {"pernas", function() return true end}}
return D
