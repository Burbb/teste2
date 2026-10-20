-- L1: a luva de malha pela referência nova (referencias/Luvas/luva-malha.png): o punho em cima à direita, com a boca e
-- a tira de couro; a mão pendendo para baixo e à esquerda, relaxada; a faixa de couro no pulso. Cinco dedos (a
-- referência mostra quatro): juntos e relaxados, curvando nas pontas, em comprimentos naturais; o polegar embaixo à
-- direita, ligado à palma.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
-- o estudo da mão (a camada estudo_mao, oculta): o antebraço descendo da direita; a palma inclinada, com a beira dos nós
-- em diagonal; os dedos saindo dela para baixo e à esquerda, juntos na base e soltos nas pontas: o mínimo (o mais curto,
-- em cima), o anelar, o médio (o mais longo) e o indicador; o polegar descendo à direita, separado do indicador
D.estudo = {V, V,
l(23, "ssssss"),
l(22, "ssssssss"),
l(21, "ssssssss"),
l(20, "ssssssss"),
l(19, "ssssssss"),
l(18, "ssssssss"),
l(17, "ssssssss"),
l(15, "sssssssss"),
l(13, "ssssssssss"),
l(10, "sssssssssssss"),
l(8, "sssssssssssssss"),
l(7, "ssssssssssssssss"),
l(6, "sssssssssssssssss"),
l(6, "sssssssssssssssssss"),
l(6, "sssssssssssssss", 22, "sss"),
l(6, "ssstssstssstsss", 22, "sss"),
l(6, "ssstssstssstsss", 22, "sss"),
l(6, "ssstssstssstsss", 22, "sss"),
l(5, "ssstssstssstsss", 21, "sss"),
l(5, "ts", 9, "ssstssstsss", 21, "sss"),
l(9, "ssstssstsss", 21, "ss"),
l(8, "ssstssstsss"),
l(8, "ts", 12, "ssstsss"),
l(11, "ssstsss"),
l(11, "sss", 15, "ts"),
l(11, "ts"),
V, V, V, V}
-- a luva por cima do estudo: a beira de couro na boca do punho e a faixa de couro no pulso (como na referência); a malha
-- (o xadrez da cota) acesa à esquerda; os nós acesos; as divisas entre os dedos um tom abaixo; as pontas na sombra
D.tons = {V, V,
l(23, "ffeedc"),
l(22, "eeedddcb"),
l(21, "HGGFFEED"),
l(20, "HGGFFEED"),
l(19, "GGGFFEED"),
l(18, "GGFFFEED"),
l(17, "ffeeddcc"),
l(15, "eeedddccb"),
l(13, "FGGGFFFEED"),
l(10, "FGHHGGGFFFEED"),
l(8, "FGHHHGGGFFFEEDD"),
l(7, "FGHHHGGGGFFFEEDD"),
l(6, "FGGHHGGGGFFFEEEDD"),
l(6, "FGGGGGGFFFFFEEED", 22, "GFE"),
l(6, "HIH2HIH2HIH2HHG", 22, "GFE"),
l(6, "HGF1HGF1HGF1GGF", 22, "FED"),
l(6, "HGF1HGF1HGF1GGF", 22, "FED"),
l(6, "HGF1HGF1HGF1GGF", 22, "FED"),
l(5, "HGF1HGF1HGF1GFE", 21, "FED"),
l(5, "FE", 9, "HGF1HGF1GFE", 21, "EDC"),
l(9, "GGF1HGF1GFE", 21, "DC"),
l(8, "GFE1HGF1GFE"),
l(8, "FE", 12, "HGF1GFE"),
l(11, "HGF1GFE"),
l(11, "GFE", 15, "FE"),
l(11, "FE"),
V, V, V, V}
D.silhueta = D.tons
D.camadas = {{"malha", G.malha}, {"couro", G.couro}, {"vincos", G.ferro}}
return D
