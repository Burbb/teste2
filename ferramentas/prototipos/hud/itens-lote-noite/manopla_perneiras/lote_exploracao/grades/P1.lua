-- P1: a calça de malha pela referência nova (referencias/calça/calca-malha.png; a construção, não o ângulo): de frente,
-- o cinto de couro com a fivela de ferro; o quadril de malha; as duas pernas separadas a partir do gancho, afinando um
-- pouco até a barra em dentes (sem botas); a malha (o xadrez da cota) acompanhando o volume: a frente de cada coxa e
-- canela acesa, os lados e o lado de dentro na sombra; a dobra do gancho; uma liga de couro abaixo de cada joelho.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
D.tons = {V, V, V,
l(8, "ffffeee77eddddcc"),
l(8, "eeeddd5445cccbbb"),
l(8, "EEEEEEEEDDDDDDDD"),
l(8, "FGHHGGFFFGGFFEED"),
l(8, "FGHHGGFFFGGFFEED"),
l(7, "EFGHHGGFFFGGFFEED"),
l(7, "EFGHHGGFFGGGFFEED"),
l(7, "EFGHHGGFFGGGFFEED"),
l(7, "EFGHHGGFEFGGFFEED"),
l(7, "EFGHHGGFDDFGGFFEED"),
l(7, "EFGHHGGE", 17, "FGGFFEED"),
l(7, "EFGHHGGD", 17, "EGGFFEED"),
l(7, "EFGHHGFD", 17, "EGGFFEDD"),
l(7, "EFGHHGFD", 17, "EGGFFEDD"),
l(7, "EFGHGGFD", 17, "EGGFEEDD"),
l(7, "EFGHGGFD", 17, "EGGFEEDD"),
l(8, "FGHGGFD", 17, "EGGFEED"),
l(8, "ffeeddc", 17, "eeddccb"),
l(8, "FGHGGFD", 17, "EGGFEED"),
l(8, "FGGGFED", 17, "EFGFEED"),
l(8, "FGGGFED", 17, "EFGFEED"),
l(8, "EFGGFED", 17, "EFGFEDD"),
l(8, "EFGGFED", 17, "EFGFEDD"),
l(8, "EFFFEDD", 17, "DEFFEDC"),
l(8, "E.F.E.D", 17, "D.F.E.C"),
V, V, V, V}
D.silhueta = D.tons
D.camadas = {{"malha", G.malha}, {"cinto", function(x, y, ch) return ch:match("[a-f]") ~= nil or y <= 4 end}}
return D
