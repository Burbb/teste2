-- P4: livre mista (as "Templar Legs" da prancha referencias/calça/1.gif como apoio). A calça de malha com proteções de
-- ferro localizadas: o cinto de couro com a fivela; o quadril de malha; na frente de cada coxa uma placa de ferro, mais
-- estreita que a perna (a malha aparece dos lados), com a faixa de reflexo e a beira de baixo escura; uma joelheira
-- pequena da largura da placa, integrada; a malha descendo até a barra em dentes.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
D.tons = {V, V, V, V,
l(8, "ffffeee77eddddcc"),
l(8, "eeeddd5445cccbbb"),
l(8, "EEEEEEEEDDDDDDDD"),
l(8, "FGHHGGFFFGGFFEED"),
l(7, "EFGHHGGFFGGGFFEED"),
l(7, "E678876DFFE567765D"),
l(7, "E578765D", 17, "E467654D"),
l(7, "E578765D", 17, "E467654D"),
l(7, "E578765D", 17, "E467654D"),
l(7, "E467654D", 17, "E356543D"),
l(7, "E222221D", 17, "E222211D"),
l(7, "EFGHGGFD", 17, "EGGFEEDD"),
l(7, "EF5775FD", 17, "EF4664ED"),
l(7, "EF6886FD", 17, "EF5775ED"),
l(7, "EF3443ED", 17, "EE3332DD"),
l(8, "FGHGGFD", 17, "EGGFEED"),
l(8, "FGHGGFD", 17, "EGGFEED"),
l(8, "FGHGGFD", 17, "EGGFEED"),
l(8, "FGGGFED", 17, "EFGFEED"),
l(8, "FGGGFED", 17, "EFGFEED"),
l(8, "EFGGFED", 17, "EFGFEDD"),
l(8, "EFFFEDD", 17, "DEFFEDC"),
l(8, "E.F.E.D", 17, "D.F.E.C"),
}
D.silhueta = D.tons
D.camadas = {{"malha", G.malha}, {"placas", G.ferro}, {"cinto", G.couro}}
return D
