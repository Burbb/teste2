-- P4 em 48 (20/10/2026): a P4 aprovada em 32 (lote_exploracao/grades/P4.lua) na grade de 48, à mão, com a mesma
-- construção do 32 e do 40 (ver P4-40.lua): o cinto com a fivela, o quadril de malha, as placas das coxas com a coluna de
-- malha dos dois lados e a beira escura de 1 px, a joelheira com a malha dos dois lados, as canelas de malha e a
-- barra em dentes de 1 px. O vão entre as pernas fica com 2 px (os dois contornos encostados), como no 32 e no 40.
-- As medidas do 32 vezes 1,5, arredondadas: as pernas de 8 para 12 px, as placas de 6 para 10, a joelheira de 4 para 6
-- (com duas colunas de malha de cada lado: com 8 ficava larga demais para a perna), o cinto e a fivela com três linhas
-- (a fivela estreita em cima e mais larga embaixo, como no 32; com seis colunas iguais virava um bloco).
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l = G.linha_de(48)
local V = string.rep(".", 48)
local D = {lado = 48}
D.tons = {V, V, V, V, V, V, V,
-- o cinto (x 12..35) e a fivela no meio
l(12, "ffffffeeeee77eddddddcccc"),
l(12, "eeeeeddddd5775ccccccbbbb"),
l(12, "ddddddccc544445bbbbbbaaa"),
-- o quadril
l(12, "EEEEEEEEEEEEDDDDDDDDDDDD"),
l(12, "FGGHHHGGGFFFFGGGFFFEEEDD"),
l(12, "FGGHHHGGGFFFFGGGFFFEEEDD"),
l(11, "EFGGHHHGGGFFFFGGGFFFEEEDD"),
-- as placas das coxas
l(11, "E6778888776DFFE5667777665D"),
l(11, "E5778876655D", 25, "E4667766544D"),
l(11, "E5778876655D", 25, "E4667766544D"),
l(11, "E5778876655D", 25, "E4667766544D"),
l(11, "E5778876655D", 25, "E4667766544D"),
l(11, "E5778876655D", 25, "E4667766544D"),
l(11, "E4667766544D", 25, "E3556655433D"),
l(11, "E4667766544D", 25, "E3556655433D"),
l(11, "E2222222211D", 25, "E2222222111D"),
-- a malha e a joelheira
l(11, "EFGGHHGGGFFD", 25, "EGGGGFFEEEDD"),
l(11, "EFGGHHGGGFFD", 25, "EGGGGFFEEEDD"),
l(11, "EFF567765FFD", 25, "EFF456654EED"),
l(11, "EFF678876FFD", 25, "EFF567765EED"),
l(11, "EFF678876FFD", 25, "EFF567765EED"),
l(11, "EFF334433EED", 25, "EEE333322DDD"),
-- a malha das canelas e a barra em dentes
l(12, "FGGHHGGGFFD", 25, "EGGGGFFEEED"),
l(12, "FGGHHGGGFFD", 25, "EGGGGFFEEED"),
l(12, "FGGHHGGGFFD", 25, "EGGGGFFEEED"),
l(12, "FGGHHGGGFFD", 25, "EGGGGFFEEED"),
l(12, "FGGGGGGFEED", 25, "EFGGGFFEEED"),
l(12, "FGGGGGGFEED", 25, "EFGGGFFEEED"),
l(12, "FGGGGGGFEED", 25, "EFGGGFFEEED"),
l(12, "EFFGGGGFEED", 25, "EFGGFFEEDDD"),
l(12, "EFFGGGGFEED", 25, "EFGGFFEEDDD"),
l(12, "EFFFFFFEEDD", 25, "DEEFFFEEDDC"),
l(12, "EFFFFFFEEDD", 25, "DEEFFFEEDDC"),
l(12, "E.F.F.E.E.D", 25, "D.F.F.E.D.C"),
}
D.silhueta = D.tons
D.camadas = {{"malha", G.malha}, {"placas", G.ferro}, {"cinto", G.couro}}
return D
