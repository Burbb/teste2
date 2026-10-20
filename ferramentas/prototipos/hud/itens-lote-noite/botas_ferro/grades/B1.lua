-- B1, as botas de ferro (20/10/2026), à mão, pela construção da bota de couro aprovada (o par de perfil, o bico para a
-- esquerda, a bota de trás deslocada para a direita e para cima, mais escura, separada da da frente por uma linha escura)
-- e pelo material do conjunto de ferro (a rampa da família, a luz da esquerda, as beiras escuras de 1 px, o couro da
-- tira e da sola). A bota da frente: a boca aberta (a beira do fundo, o vão escuro, a beira da frente dobrada: a bota
-- vazia); o cano de aço com a barriga da panturrilha do lado de trás, a faixa clara à esquerda e o reflexo só no alto da
-- panturrilha, escurecendo até o tornozelo (um tubo reto e claro, a primeira passada, lia como cano de chaminé com
-- tampa); a tira de couro com a fivela na canela; duas lâminas articuladas sobre o
-- tornozelo, cada uma mais larga que a de cima, acesa em cima e escura embaixo; o pé de placas com a biqueira separada
-- por uma linha que curva até o bico; a sola de couro com o arco aberto e o salto.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
D.tons = {V, V, V,
-- a beira da bota de trás
l(16, "245554321"),
-- a boca da bota da frente (a beira do fundo, o vão escuro, a beira da frente dobrada e a sombra dela) | a linha entre as
-- duas | a bota de trás
l(12, "3455543", 19, "022221"),
l(11, "510000014", 20, "0321"),
l(11, "578887654", 20, "0321"),
l(11, "234444321", 20, "0321"),
-- o cano: a barriga da panturrilha do lado de trás, o reflexo só no alto dela, escurecendo até o tornozelo; a tira de
-- couro com a fivela no meio da canela
l(12, "4676543", 19, "04321"),
l(12, "46876543", 20, "0321"),
l(12, "46876543", 20, "0321"),
l(12, "46876543", 20, "0321"),
l(12, "4676543", 19, "0cbba"),
l(12, "e56ddcb", 19, "04321"),
l(12, "4676543", 19, "04321"),
l(12, "4565432", 19, "04321"),
l(12, "4565432", 19, "04321"),
l(12, "3454321", 19, "04321"),
-- as lâminas do tornozelo
l(11, "467776542", 20, "04321"),
l(11, "245554321", 20, "04321"),
l(9, "36777765421", 20, "02110"),
l(8, "234555544321", 20, "03321"),
-- o pé: a biqueira à esquerda da linha que curva, as lâminas do peito do pé à direita
l(6, "46778736766543", 20, "03221"),
l(5, "357787256655432", 20, "02211"),
l(4, "3466762455444321", 20, "02211"),
l(3, "23455413343332211", 20, "0dccb"),
-- a sola e o salto
l(3, "dddddddddddddccbb", 20, "0cbba"),
l(13, "cccbbaa"),
}
D.silhueta = D.tons
-- as camadas: o couro (a tira, a sola, o salto), a bota de trás, a bota da frente (com a linha entre as duas)
local function tras(x, y) return y == 3 or x >= 21 or (x == 20 and ((y >= 8 and y <= 17) or y == 4)) end
D.camadas = {{"couro", G.couro},
  {"bota_tras", function(x, y, ch) return tras(x, y) and ch ~= "0" end},
  {"bota_frente", function() return true end}}
return D
