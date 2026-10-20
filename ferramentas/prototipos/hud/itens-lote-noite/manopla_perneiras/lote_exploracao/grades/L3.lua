-- L3: livre em malha. A mão aberta na diagonal (o punho embaixo à esquerda, os dedos para cima e à direita), como os
-- ícones de luva da Dungeon Crawl Stone Soup que o Jean apontou (os de cima; estudo de construção, nada copiado).
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
-- o estudo da mão (a camada estudo_mao, oculta): a palma larga e inclinada; os quatro dedos saindo da linha dos nós em
-- diagonal, com um vão entre eles: o médio o mais longo, o indicador e o anelar quase iguais, o mínimo o mais curto; o
-- polegar saindo da lateral da palma perto do pulso, subindo quase na vertical, com a membrana (o V) até o indicador
D.estudo = {V, V,
l(23, "ss"),
l(22, "sss"),
l(19, "ss", 22, "sss"),
l(18, "sss", 22, "sss", 26, "ss"),
l(17, "sss", 21, "sss", 25, "sss"),
l(17, "sss", 21, "sss", 25, "sss"),
l(16, "sss", 20, "sss", 24, "sss"),
l(8, "ss", 16, "sss", 20, "sss", 24, "sss", 28, "ss"),
l(8, "sss", 15, "sss", 19, "sss", 23, "sss", 27, "sss"),
l(8, "sss", 15, "sss", 19, "sss", 23, "sss", 27, "ss"),
l(9, "sss", 14, "sssssss", 22, "sss", 26, "sss"),
l(9, "sss", 13, "sssssssssss", 25, "sss"),
l(10, "ssssssssssssssssss"),
l(10, "sssssssssssssssss"),
l(10, "ssssssssssssssss"),
l(10, "sssssssssssssss"),
l(10, "sssssssssssss"),
l(10, "sssssssssss"),
l(10, "sssssssss"),
l(9, "ssssssss"),
l(8, "ssssssss"),
l(7, "ssssssss"),
l(6, "ssssssss"),
V, V, V, V, V, V, V}
-- a luva por cima do estudo: os dedos com a espessura da malha (o vão de 1 px entre eles vira o contorno), acesos na
-- beira de cima e à esquerda, os nós claros; a tira de couro atravessando o pulso na diagonal; o punho de malha abrindo
-- para baixo e à esquerda, escurecendo para a direita, com a barra em dentes como a cota
D.tons = {V, V,
l(23, "HG"),
l(22, "HGF"),
l(19, "HG", 22, "GGF"),
l(18, "HGF", 22, "GGE", 26, "GF"),
l(17, "HGF", 21, "GGE", 25, "GFE"),
l(17, "GGE", 21, "GFE", 25, "GFE"),
l(16, "GGE", 20, "GFE", 24, "FFD"),
l(8, "HG", 16, "GFE", 20, "GFE", 24, "FED", 28, "FE"),
l(8, "HGF", 15, "GFE", 19, "GFE", 23, "FED", 27, "FED"),
l(8, "HGF", 15, "FFE", 19, "FFE", 23, "FED", 27, "ED"),
l(9, "GGE", 14, "HHGHGGF", 22, "FED", 26, "EDC"),
l(9, "GFE", 13, "GHHGGHGGFFE", 25, "EDC"),
l(10, "FFGHHGGGGFFFFEEDDC"),
l(10, "FGHHGGGGFFFFEEDDC"),
l(10, "FGHGGGGFFFFEEDDC"),
l(10, "FGGGGFFFFEEEDDC"),
l(9, "EEedFFFEEEDDC"),
l(8, "FEEEfeFFEEDDC"),
l(7, "FFEEEDfeEEDDC"),
l(6, "FFFEEEDDedDDC"),
l(5, "GFFFEEEDDDedC"),
l(4, "GGFFFEEEDDDCd"),
l(3, "GGFFFEEEEDDCC"),
l(3, "FGFFEEEEDDCC"),
l(2, "FFFEEEEDDDCC"),
l(2, "E.E.E.D.D.C"),
V, V, V, V}
D.silhueta = D.tons
D.camadas = {{"malha", G.malha}, {"couro", G.couro}}
return D
