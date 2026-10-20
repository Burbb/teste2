-- P4 em 40 (20/10/2026): a P4 aprovada em 32 (lote_exploracao/grades/P4.lua) na grade de 40, à mão, com a mesma
-- construção: o cinto de couro com a fivela no meio; a faixa escura e o quadril de malha; em cada coxa a placa de ferro
-- com a coluna de malha dos dois lados, a faixa de reflexo à esquerda e a beira de baixo escura (1 px); uma linha de
-- malha; a joelheira com uma coluna de malha de cada lado e a sombra embaixo; a malha descendo, mais estreita, até a barra
-- em dentes (1 px, alternados). O vão entre as pernas fica com 2 px (os dois contornos encostados, como no 32).
-- As medidas do 32 vezes 1,25, arredondadas: as pernas de 8 para 10 px, as placas de 6 para 8, a joelheira de 4 para 6.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l = G.linha_de(40)
local V = string.rep(".", 40)
local D = {lado = 40}
D.tons = {V, V, V, V, V, V,
-- o cinto (x 10..29) e a fivela no meio
l(10, "fffffeeee77eddddddcc"),
l(10, "eeeedddd5445ccccbbbb"),
-- o quadril
l(10, "EEEEEEEEEEDDDDDDDDDD"),
l(10, "FGHHHGGFFFFGGGFFEEED"),
l(10, "FGHHHGGFFFFGGGFFEEED"),
l(9, "EFGHHHGGFFFGGGGFFEEED"),
-- as placas das coxas
l(9, "E67788776DFFE56677665D"),
l(9, "E57887655D", 21, "E46776544D"),
l(9, "E57887655D", 21, "E46776544D"),
l(9, "E57887655D", 21, "E46776544D"),
l(9, "E57887655D", 21, "E46776544D"),
l(9, "E46776544D", 21, "E35665433D"),
l(9, "E22222221D", 21, "E22222111D"),
-- a malha e a joelheira
l(9, "EFGHHGGFFD", 21, "EGGGFEEEDD"),
l(9, "EF567765FD", 21, "EF456654ED"),
l(9, "EF678876FD", 21, "EF567765ED"),
l(9, "EF678876FD", 21, "EF567765ED"),
l(9, "EF334433ED", 21, "EE333322DD"),
-- a malha das canelas e a barra em dentes
l(10, "FGHHGGFFD", 21, "EGGGFFEED"),
l(10, "FGHHGGFFD", 21, "EGGGFFEED"),
l(10, "FGHHGGFFD", 21, "EGGGFFEED"),
l(10, "FGHHGGFFD", 21, "EGGGFFEED"),
l(10, "FGGGGFFED", 21, "EFGGFFEED"),
l(10, "FGGGGFFED", 21, "EFGGFFEED"),
l(10, "EFGGGFEED", 21, "EFGGFEEDD"),
l(10, "EFGGGFEED", 21, "EFGGFEEDD"),
l(10, "EFFFFEEDD", 21, "DEFFFEEDC"),
l(10, "E.F.F.E.D", 21, "D.F.F.E.C"),
}
D.silhueta = D.tons
D.camadas = {{"malha", G.malha}, {"placas", G.ferro}, {"cinto", G.couro}}
return D
