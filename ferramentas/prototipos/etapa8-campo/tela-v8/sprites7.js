// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 7: o estudo de direção de arte das miniaturas. Candidatas para
// o Jean comparar, nada aprovado. À mão, uma letra por pixel, virados para a direita (a esquerda é o espelho), nos
// mesmos tamanhos e poses do catálogo atual (sprites.js): parado, duas passadas (as pernas trocadas), preparo, golpe,
// recuo; caído é o recuo girado. As letras novas: g G (malha de ferro), n N (couro e pele escuros), o (osso, chifre).
//
// As direções:
// - "atual": a arte do Campo Livre 6, intacta.
// - "sobria": a evolução sóbria do minimalismo atual: as mesmas grades, a paleta menos saturada e com materiais mais
//   separados (aço frio, couro, tecido), as cores das equipes mais fechadas (azul-aço e ferrugem).
// - "sombria": um pouco mais detalhada e sombria: grades redesenhadas para as tropas da amostra (soldado, arqueiro,
//   pesado, cavaleiro) e para Harg (malha, capuz e couro escuros, o tabardo da equipe por cima), paleta escura com
//   contraste guardado nas cabeças, nas armas e nas bordas. Os heróis e quem não está na amostra usam as grades atuais
//   com esta paleta (o catálogo não foi refeito antes da escolha da direção).
// A escala "menor" (só o seu herói: Guerreiro e Mago) tem 1 linha a menos de tronco e 2 colunas a menos: 14 px de
// altura em vez de 15 (o soldado tem 13). Morel, Odette e Harg ficam como estão: a robustez deles é silhueta.

export const ARTES = {
  atual: { nome: "Atual (Campo Livre 6)" },
  sobria: { nome: "Sóbria (o minimalismo, mais contido)" },
  sombria: { nome: "Sombria (mais detalhe, mais escura)" },
};
// Campo Livre 8: a escala virou a escolha dos modelos dos heróis (F9): os novos (a candidata do 8, sprites8.js), os do
// Campo Livre 7 e o herói menor do estudo do 7 (a diferença de 15 para 14 px quase não aparece: não substitui o redesenho)
export const ESCALAS = { novo: { nome: "Modelos novos (candidata)" }, atual: { nome: "Modelos do Campo Livre 7" }, menor: { nome: "Herói menor (estudo do 7)" } };

// As paletas trocam o valor de cada letra (a grade não muda).
export const PALETAS = {
  sobria: {
    k: "#1b1a20", K: "#2f2c35", h: "#c3c6cc", H: "#8a8e98", M: "#565a66", s: "#d6a688", S: "#a67455",
    p: "#4a3d34", P: "#2a221d", b: "#8f6a45", B: "#5e4229", w: "#e9ecef", y: "#d6b866", Y: "#9a7a36",
    c: "#e3dbc6", C: "#b6a888", v: "#ddd5c0", V: "#ada28a", X: "#323b4e", Z: "#4a5670",
    g: "#9a9ca3", G: "#666a73", n: "#5e4a36", N: "#3b2e22", o: "#e3d8bd",
  },
  sombria: {
    k: "#121016", K: "#24202a", h: "#b3b7bf", H: "#757a85", M: "#454852", s: "#c9997a", S: "#8f6249",
    p: "#3b302a", P: "#211a16", b: "#7a5734", B: "#4c331d", w: "#d9dde2", y: "#c9a84f", Y: "#8a6c2c",
    c: "#cfc4a8", C: "#9a8f74", v: "#bdb39b", V: "#857b67", X: "#252b3a", Z: "#38415a",
    f: "#ffd27a", F: "#ff8a30", r: "#a8322a", R: "#6b1f1c", a: "#a986d8", A: "#6c48a8",
    g: "#8d9098", G: "#5a5d66", n: "#5a4632", N: "#3a2c1f", o: "#d8ccb0",
  },
};
export const EQUIPES_ARTE = {
  sobria: [{ t: "#6e95c9", T: "#4b6fa3", u: "#2f4a73" }, { t: "#c45f4f", T: "#963f35", u: "#612a26" }],
  sombria: [{ t: "#7095bd", T: "#4a6a8f", u: "#2e4463" }, { t: "#b8493c", T: "#86302a", u: "#541d1b" }],
};
// Harg e o contorno dele, por direção (o vermelho mais escuro na sombria)
export const CORES_ARTE = { sombria: { lider: { t: "#4e4a56", T: "#35313d", u: "#1d1a22" } } };

// ---- a direção sombria: as tropas da amostra e Harg, redesenhados
const SOLDADO = {
  largura: 13, pe: 5,
  parado: [
    ".............",
    ".........w...",
    "....HhH..w...",
    "...MHHHM.w...",
    "...MsSk..w...",
    "....gSG.HyH..",
    "..gtTttTGs...",
    ".gGtTYTtG....",
    ".gGtTttTG....",
    "..NnTTTnN....",
  ],
  preparo: [
    "........w....",
    "........w....",
    "...HhH..w....",
    "..MHHHM.w....",
    "..MsSk.HyH...",
    "...gSG.Gs....",
    ".gtTttTG.....",
    "gGtTYTtG.....",
    "gGtTttTG.....",
    ".NnTTTnN.....",
  ],
  golpe: [
    ".............",
    ".............",
    ".....HhH.....",
    "....MHHHM....",
    "....MsSk.....",
    ".....gSG.....",
    "...gtTttTsHww",
    "..gGtTYTtG...",
    "..gGtTttTG...",
    "...NnTTTnN...",
  ],
  recuo: [
    ".............",
    ".............",
    "...HhH.......",
    "..MHHHM......",
    "..MkkS.......",
    "...gSG..w....",
    ".gtTttTsw....",
    "gGtTYTtG.w...",
    "gGtTttTG.....",
    ".NnTTTnN.....",
  ],
};

const ARQUEIRO = {
  largura: 13, pe: 5,
  parado: [
    ".............",
    ".............",
    "....nnn..b...",
    "...nNNNn.Bb..",
    "...nsskN..b..",
    "....sSs...b..",
    "...gtttgsHb..",
    "...NtTtN..b..",
    "...ntttn.b...",
    "...NnNnN.....",
  ],
  preparo: [
    ".............",
    ".............",
    "...nnn....b..",
    "..nNNNn...Bb.",
    "..nsskN..w.b.",
    "...sSs..w..b.",
    "..gtttgsw.Hb.",
    "..NtTtN..w.b.",
    "..ntttn...b..",
    "..NnNnN......",
  ],
  golpe: [
    ".............",
    ".............",
    "....nnn...b..",
    "...nNNNn..Bb.",
    "...nsskN...b.",
    "....sSs....b.",
    "...gtttgggsb.",
    "...NtTtN...b.",
    "...ntttn..b..",
    "...NnNnN.....",
  ],
  recuo: [
    ".............",
    ".............",
    "...nnn.......",
    "..nNNNn..b...",
    "..nkksN..Bb..",
    "...sSs....b..",
    "..gtttgs..b..",
    "..NtTtN...b..",
    "..ntttn..b...",
    "..NnNnN......",
  ],
};

// o pesado: o elmo fechado, o escudo grande na cor da equipe com a borda de ferro
const PESADO = {
  largura: 13, pe: 5,
  parado: [
    "....MHM......",
    "...MhhhM.....",
    "...MkkkM.....",
    "...gHhHg.HH..",
    "..gTTtTTHtTH.",
    ".gGtTtTGHtyH.",
    ".gGtTtTGHtTH.",
    "..gTTTTTHtTH.",
    "..NnTTTn.HH..",
    "..NnTTTnN....",
  ],
  preparo: [
    "...MHM.......",
    "..MhhhM......",
    "..MkkkM......",
    "..gHhHg..HH..",
    ".gTTtTT.HtTH.",
    "gGtTtTG.HtyH.",
    "gGtTtTG.HtTH.",
    ".gTTTTT.HtTH.",
    ".NnTTTn..HH..",
    ".NnTTTnN.....",
  ],
  golpe: [
    ".....MHM.....",
    "....MhhhM....",
    "....MkkkM....",
    "....gHhHgHH..",
    "...gTTtTTHtTH",
    "..gGtTtTGHtyH",
    "..gGtTtTGHtTH",
    "...gTTTTTHtTH",
    "...NnTTTn.HH.",
    "...NnTTTnN...",
  ],
};
PESADO.recuo = PESADO.parado;

// o cavaleiro: o cavalo escuro com a xairel na cor da equipe, o cavaleiro de malha e elmo, a lança
const CAV_CORPO = [
  "..N..NNtTTNNNNNn...",
  ".NnNnuTtTtTtTunNnN.",
  "..N.NuuTTTTTTun.Nnk",
  "....NnnnnnnnnnN..NN",
];
const CAVALEIRO = {
  largura: 19, pe: 9, semPernas: true,
  parado: [
    "........HH.........",
    ".......MHhH....w...",
    ".......gskG...w....",
    "......gtTtTs.b.....",
    "......gtTyT.b......",
    ...CAV_CORPO,
    "....nN......nN.....",
    "....n.N.....n.N....",
    "....N..N....N..N...",
  ],
  preparo: [
    "........HH.....w...",
    ".......MHhH...b....",
    ".......gskG..b.....",
    "......gtTtTsb......",
    "......gtTyT........",
    ...CAV_CORPO,
    "....nN.......N.n...",
    "....n.N......N.....",
    "....N..N...........",
  ],
  golpe: [
    "........HH.........",
    ".......MHhH........",
    ".......gskG........",
    "......gtTtTssbbbbww",
    "......gtTyT........",
    ...CAV_CORPO,
    "..nN..........nN...",
    ".n..N........n..N..",
    ".N...N.......N...N.",
  ],
};
CAVALEIRO.recuo = CAVALEIRO.parado;
CAVALEIRO.andarA = [...CAVALEIRO.parado.slice(0, 9), "...nN........nN....", "..n..N......n..N...", "..N...N.....N...N.."];
CAVALEIRO.andarB = [...CAVALEIRO.parado.slice(0, 9), ".....nN....nN......", ".....nN....nN......", ".....NN....NN......"];

// Harg: os chifres de osso, a malha escura, o manto de pele, a faixa vermelha e o machado
const LIDER = {
  largura: 19, pe: 7, pernasLargura: true, contorno: "#3a0b0b",
  parado: [
    "..o.....o....hh....",
    "..oo...oo...hhHh...",
    "...oMMMo....hHHb...",
    "...MhhhM.....hhb...",
    "...MkhkM.......b...",
    "..nHsSsHn......b...",
    ".nNgGgGgGn.....b...",
    "nNgGgryrgGgGssb....",
    "nNgGgrRrgGgg..b....",
    "nNgGgrRrgGgg.......",
    ".NgGGGGGGGGn.......",
    "..NNGGGGGNN........",
  ],
  preparo: [
    ".............hh....",
    "..o.....o...hhHh...",
    "..oo...oo...hHHb...",
    "...oMMMo.....hb....",
    "...MhhhM....sb.....",
    "...MkhkM...sb......",
    "..nHsSsHn.Gb.......",
    ".nNgGgGgGGG........",
    "nNgGgryrgGgn.......",
    "nNgGgrRrgGgn.......",
    ".NgGGGGGGGGn.......",
    "..NNGGGGGNN........",
  ],
  golpe: [
    "...................",
    "..o.....o..........",
    "..oo...oo..........",
    "...oMMMo...........",
    "...MhhhM...........",
    "...MkhkM...........",
    "..nHsSsHn..........",
    ".nNgGgGgGn.........",
    "nNgGgryrgGgGssbbbhh",
    "nNgGgrRrgGgg...hHHh",
    "nNgGgrRrgGgg....hh.",
    "..NNGGGGGNN........",
  ],
};
LIDER.recuo = LIDER.parado;

export const MODELOS_SOMBRIOS = { soldado: SOLDADO, arqueiro: ARQUEIRO, pesado: PESADO, cavaleiro: CAVALEIRO, lider: LIDER };

// ---- a escala "menor": o seu herói com 1 linha de tronco e 2 colunas a menos (o mesmo desenho, refeito à mão)
const GUERREIRO_MENOR = {
  largura: 15, pe: 5, heroi: true,
  parado: [
    ".....yy........",
    "....yYy....w...",
    "...hhhh....w...",
    "..hhwhhh...w...",
    "..hsskhh...w...",
    "..csSsh..yYy...",
    ".cChhhhhhss....",
    "cChhwhhhh......",
    "cChYyyYhh......",
    ".CMhhhhM.......",
    "..MMhhMM.......",
  ],
  preparo: [
    "........w......",
    "....yy..w......",
    "...yYy..w......",
    "..hhhh..w......",
    ".hhwhhhyYy.....",
    ".hsskhh.s......",
    ".csSsh.hs......",
    "cChhhhhh.......",
    "cChhwhhh.......",
    "cChYyyYh.......",
    ".CMhhhhM.......",
  ],
  golpe: [
    "...............",
    "......yy.......",
    ".....yYy.......",
    ".....hhhh......",
    "....hhwhhh.....",
    "....hsskhh.....",
    "...ccsSsh......",
    "..cChhhhhssyYww",
    ".cChhwhhh..y...",
    ".cChYyyYh......",
    "..CMhhhhM......",
  ],
  recuo: [
    "...............",
    "...yy..........",
    "..yYy..........",
    ".hhhh..........",
    "hhwhhh....w....",
    "hkkkhh...w.....",
    "csSsh...w......",
    "cChhhhhsw......",
    "cChhwhh.y......",
    "cChYyyY........",
    ".CMhhhM........",
  ],
};

const MAGO_MENOR = {
  largura: 15, pe: 5, heroi: true,
  parado: [
    ".....X......f..",
    "....XZ.....fFf.",
    "....XZX.....f..",
    "...XXZXX....b..",
    ".yYYYYYYy...b..",
    "...vsskv....b..",
    "...vsSsv....b..",
    "..VvvvvvV..sb..",
    ".VvvyvvvvVs.b..",
    ".VvvyvvvvV..b..",
    ".XVvvvvvVX..b..",
  ],
  preparo: [
    "......X...fFf..",
    ".....XZ..fFfFf.",
    ".....XZX..fFf..",
    "....XXZXX..b...",
    "..yYYYYYYy.b...",
    "....vsskv.sb...",
    "....vsSsvs.....",
    "...VvvvvvV.....",
    "..VvvyvvvvV....",
    "..VvvyvvvvV....",
    "..XVvvvvvVX....",
  ],
  golpe: [
    "...............",
    "......X........",
    ".....XZ........",
    ".....XZX.......",
    "....XXZXX......",
    "..yYYYYYYy.....",
    "....vsskv......",
    "....vsSsv......",
    "...VvvvvvVssbfF",
    "..VvvyvvvvV..ff",
    "..XVvvvvvVX....",
  ],
  recuo: [
    "...............",
    "...X...........",
    "..XZ...........",
    "..XZX..........",
    ".XXZXX.........",
    "yYYYYYYy...f...",
    ".vkksv....fFf..",
    ".vsSsv...sb....",
    "VvvvvvV.s..b...",
    "VvvyvvvV...b...",
    "XVvvvvVX.......",
  ],
};

export const MODELOS_MENORES = { guerreiro: GUERREIRO_MENOR, mago: MAGO_MENOR };
