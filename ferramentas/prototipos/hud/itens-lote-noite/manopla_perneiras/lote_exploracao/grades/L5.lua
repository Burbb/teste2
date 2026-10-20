-- L5: livre mista. A mão aberta de pé, pelas costas: a luva de couro com uma placa de ferro nos nós e placas pequenas
-- nas falanges do meio; o punho de malha embaixo, com a barra em dentes.
local G = dofile("C:/Users/Jean Wress/Desktop/packs/teste2/ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/auxiliares/grade.lua")
local l, V = G.linha, G.VAZIA
local D = {}
-- o estudo da mão (a camada estudo_mao, oculta): a palma afunilando até o pulso; os nós em arco; os quatro dedos abrindo
-- um pouco em leque (o indicador para a esquerda, o mínimo para a direita), o médio o mais longo, o anelar e o indicador
-- quase iguais, o mínimo o mais curto; o polegar saindo da lateral perto do pulso, inclinado, com a dobra no meio
D.estudo = {V, V, V,
l(13, "ss"),
l(13, "sss", 18, "ss"),
l(7, "ss", 13, "sss", 18, "sss"),
l(7, "sss", 13, "sss", 18, "sss"),
l(8, "sss", 13, "sss", 17, "sss", 22, "ss"),
l(8, "sss", 13, "sss", 17, "sss", 22, "ss"),
l(9, "sss", 13, "sss", 17, "sss", 21, "ss"),
l(9, "sss", 13, "sss", 17, "sss", 21, "ss"),
l(4, "ss", 9, "sss", 13, "sss", 17, "sss", 21, "ss"),
l(4, "sss", 9, "sss", 13, "sss", 17, "sss", 21, "ss"),
l(5, "sss", 9, "sssssssssss", 21, "ss"),
l(5, "sss", 9, "ssssssssssssss"),
l(6, "sssssssssssssssss"),
l(6, "sssssssssssssssss"),
l(7, "ssssssssssssssss"),
l(8, "ssssssssssssss"),
l(9, "ssssssssssss"),
l(10, "ssssssssss"),
l(10, "ssssssssss"),
V, V, V, V, V, V, V, V, V, V}
-- a luva por cima do estudo: o couro aceso à esquerda e nas pontas; placas de ferro pequenas nas falanges do meio e a
-- placa dos nós atravessando, com a sombra embaixo; a faixa escura do pulso; o punho de malha (o xadrez da cota) abrindo
-- para baixo, com a barra em dentes
D.tons = {V, V, V,
l(13, "fe"),
l(13, "fed", 18, "fe"),
l(7, "fe", 13, "fed", 18, "fed"),
l(7, "fed", 13, "787", 18, "fed"),
l(8, "fed", 13, "565", 17, "676", 22, "ed"),
l(8, "ffe", 13, "ffe", 17, "454", 22, "ed"),
l(9, "676", 13, "fed", 17, "fed", 21, "ed"),
l(9, "454", 13, "fed", 17, "fed", 21, "65"),
l(4, "fe", 9, "ffe", 13, "ffe", 17, "fed", 21, "43"),
l(4, "fed", 9, "677", 13, "787", 17, "776", 21, "65"),
l(5, "edc", 9, "56777766554", 21, "43"),
l(5, "edc", 9, "33333333222222"),
l(6, "edd" .. "fffeeeeeddddcc"),
l(6, "dde" .. "ffeeeeeddddccb"),
l(7, "deffeeeeedddcccb"),
l(8, "deeeeeddddcccb"),
l(9, "dddcccccbbba"),
l(10, "edddcccbba"),
l(9, "GGGFFFEEEDDC"),
l(8, "GHHGGGFFFEEEDD"),
l(8, "GHHGGGFFFEEEDC"),
l(7, "GHHHGGGFFFEEEDDC"),
l(7, "FGHHGGGFFFEEEDDC"),
l(6, "FGGGGGFFFFEEEDDDCC"),
l(6, "F.F.F.F.E.E.E.D.D."),
V, V, V, V}
D.silhueta = D.tons
D.camadas = {{"couro", G.couro}, {"placas", G.ferro}, {"malha", G.malha}}
return D
