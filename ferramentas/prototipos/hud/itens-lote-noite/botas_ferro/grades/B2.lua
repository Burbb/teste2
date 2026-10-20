-- B2, as botas de ferro (20/10/2026), à mão, pela referência nova do Jean (o par em pixel art à direita da imagem; a
-- pintura à esquerda para os volumes): armadura pesada, peças rígidas moldadas e articuladas, no ferro e na luz do
-- conjunto. O par lado a lado, as duas inteiras, os bicos para a esquerda como na referência, distintas pela posição e
-- pelo ângulo: a da frente mais baixa, à esquerda, de perfil; a de trás mais alta, à direita, um tom abaixo, mais de
-- frente (o pé encurtado, a biqueira para quem olha). Em cada uma: a borda de cima com espessura (a beira do fundo, o vão escuro, o lábio aceso e a sombra dele sobre o
-- cano); a grevas com a aresta vertical (a face da luz, a aresta clara, a face da sombra, a beira escura), a canela reta
-- na frente e a panturrilha estreitando atrás até o tornozelo; a tira de couro de fechamento; a lâmina do tornozelo mais larga que o cano, com a sombra embaixo; a lâmina do peito do pé e a
-- biqueira; a sola de couro.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
D.tons = {
-- linha a linha, de cima para baixo: a de trás (à direita, 2 px mais alta no topo e 3 na sola) começa na linha 6; a da
-- frente, na 8. Em cada uma: o corte de cima inclinado (a ponta da canela, a beira da frente acesa, o vão, a beira do
-- fundo acesa: a espessura); a grevas (a face da canela até a aresta, a queda para a face do lado, a beira de trás); a
-- tira; a borda de baixo da grevas com a sombra sobre a lâmina do tornozelo; a sombra dessa lâmina sobre a do peito do
-- pé; a biqueira separada por uma linha escura; a sola de couro. A de trás tem o pé encurtado (mais de frente) e uma
-- coluna livre entre os dois pés, para o contorno separá-los
V,
V,
V,
V,
V,
l(19, "56"),
l(18, "56744"),
l(9, "67", 18, "5676004"),
l(8, "67855", 18, "56766004"),
l(8, "6787005", 18, "45674221"),
l(8, "67877015", 18, "45674221"),
l(8, "56785332", 18, "dd6dccba"),
l(8, "56785332", 18, "45674221"),
l(8, "ed7dddcb", 18, "45674221"),
l(8, "56785332", 18, "45674221"),
l(8, "56785332", 19, "4564221"),
l(8, "56785332", 19, "4564210"),
l(9, "6785332", 19, "1222110"),
l(9, "5675321", 18, "45666521"),
l(9, "2333221", 17, "233553321"),
l(8, "56777632", 17, "467776532"),
l(7, "233553321", 17, "567235532"),
l(6, "5677776532", 17, "346633221"),
l(5, "67823553321", 17, "dddddddcb"),
l(4, "567882355321"),
l(3, "3567763333221"),
l(3, "ddddddddddccb"),
V,
}
D.silhueta = D.tons
-- as camadas: o couro (as tiras, as solas), a bota de trás (x >= 17), a bota da frente
D.camadas = {{"couro", G.couro},
  {"bota_tras", function(x) return x >= 17 end},
  {"bota_frente", function() return true end}}
return D
