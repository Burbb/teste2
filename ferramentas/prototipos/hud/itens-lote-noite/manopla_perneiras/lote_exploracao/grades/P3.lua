-- P3: livre em malha. As meias de malha (chausses) separadas, presas ao cinto de couro por correias: o vão aberto entre
-- as pernas desde o cinto; cada perna com a beira de couro em cima, a malha (o xadrez da cota) acesa na frente e na
-- sombra dos lados, afinando até a barra em dentes; uma dobra leve na altura do joelho.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
D.tons = {V, V, V, V,
l(6, "fffffeeee76edddddccb"),
l(6, "eeeedddd4553ccccbbba"),
l(8, "e", 12, "d", 19, "d", 23, "c"),
l(8, "e", 12, "d", 19, "d", 23, "c"),
l(7, "feeeedd", 18, "eeddccb"),
l(7, "FGHHGFE", 18, "FGGFEED"),
l(7, "FGHHGFE", 18, "FGGFEED"),
l(6, "EFGHHGFE", 18, "FGGFEEDC"),
l(6, "EFGHHGFE", 18, "FGGFEEDC"),
l(6, "EFGHHGFD", 18, "EGGFEEDC"),
l(6, "EFGHHGFD", 18, "EGGFEEDC"),
l(6, "EFGHGGFD", 18, "EGGFEEDC"),
l(7, "FGHGGFD", 18, "EGGFEDC"),
l(7, "EFFFEED", 18, "DEFEDDC"),
l(7, "FGHGGFD", 18, "EGGFEDC"),
l(7, "FGHGGFD", 18, "EGGFEDC"),
l(7, "FGGGFED", 18, "EFGFEDC"),
l(8, "GGGFED", 18, "FGFEDC"),
l(8, "GGGFED", 18, "FGFEDC"),
l(8, "FGGFED", 18, "FGFEDC"),
l(8, "FGGFED", 18, "EFFEDC"),
l(8, "EFFEDD", 18, "EFEDDC"),
l(8, "E.F.E.", 18, "E.E.D."),
}
D.silhueta = D.tons
D.camadas = {{"malha", G.malha}, {"couro", G.couro}, {"fivela", G.ferro}}
return D
