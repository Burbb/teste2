/* Os retratos do herói desenhados em código, pelo método das cenas e do mercador: uma grade de letras, cada letra uma
   cor da paleta do desenho, pintada por Sprites.grade (cada pixel da arte, um quadrado inteiro da tela). Icones pede
   aqui o busto da ficha e a cabeça do topo e da carta; a classe que não tem retrato desenhado fica com o que tinha.
   As três classes básicas (o Mago e o Arqueiro desde a 1.91.0, abaixo). O Guerreiro: o capacete fechado de ferro, sem rosto (a calota, a cruz de reforço, a fresta da viseira em
   duas aberturas, um amassado na calota), a gola alta de gibão, a capa de lã nos ombros e a correia da espada. O ferro
   tem as cores do baú e da capela, o gibão as da túnica do mercador; a luz vem da esquerda, em poucos planos.
   Um desenho só de 40×40, sempre a ×2: o busto da ficha é ele inteiro (80 px); o da janela baixa (64 px) e a cabeça
   do topo (48 px) são recortes dele, na mesma escala. A carta da luta (32 px) tem a versão de 16×16, com a mesma
   silhueta e sem o amassado (que lá vira um ponto parecido com um olho). Aprovado no teste de
   ferramentas/prototipos/hud/retrato-teste.html. */
"use strict";

const Retratos = (() => {
  // R/l/m/s/d/D o ferro, da luz à sombra (o brilho, o plano da luz, a frente, o plano da sombra, a borda, o fundo); v a
  // fresta; W/w/q/Q a capa de lã (ombro na luz, frente, sombra, o fundo junto do capacete); u/t/T o gibão; a/A a correia
  const FERRO_LA = { R: "#b4b6bc", l: "#8c8e96", m: "#6e7078", s: "#53555c", d: "#3c3e44", D: "#26272c", v: "#0d0b0a",
    W: "#5a707a", w: "#405660", q: "#2e3d44", Q: "#20292e", u: "#9a8a66", t: "#7a6c4e", T: "#544a36", a: "#6e4c30", A: "#4a3220" };
  const GUERREIRO = [
      "........................................",
      "........................................",
      "................lllRdmmm................",
      ".............lRRlllRdmmmmms.............",
      "............lRRRlllRdmmmmmss............",
      "...........lRRRRlllRdmmmmmsss...........",
      "..........mlRddlmmmRdsssssdddD..........",
      "..........mlRRRsmmmRdsssssdddD..........",
      "..........mlRlllmmmRdsssssdddD..........",
      "..........lRRRRRlllRdmmmmmmmmm..........",
      "..........mmmmmmmmmRdddddddddd..........",
      "..........mlllllmmmldsssssdddD..........",
      "..........mvvvvvvvvldvvvvvvvvD..........",
      "..........mRRRRRlllldmmmmmmmmD..........",
      "..........mlRlllmmmldsssssdddD..........",
      "..........mlRlllmmmldsssssdddD..........",
      "..........mlRlllmmmldsssssdddD..........",
      "..........mlRlllmmmldsssssdddD..........",
      "..........mlRlllmmmldsssssdddD..........",
      "...........mRlllmmmldsssssddd...........",
      ".........wQmRlllmmmldsssssdddQQ.........",
      "......WWWwQRRRRRlllldmmmmmmmmQQwww......",
      "....WWaaAwQTddddddddDDDDDDDDTQQQqqww....",
      "...WWWWaaAwwTTTTTTTTTTTTTTTTqqQQqqQQw...",
      "..WWWWWWWaaAuuuuttttttttTTTTqqQQqqQQQw..",
      ".WWWWWWWWwaaAuuuttttttttTTTTqqQQqqQQQQw.",
      ".WWWWWWWWwwwaaAuutttttTTTTQqqqqqqqQQQQQ.",
      "WWWWWWWWWwwwwaaAutttttTTTQqqqqqqqqQQQQQw",
      "WWWWWWWWWwwwwwwaaAttttTTQqqqqqqqqqQQQQQQ",
      "WWWWWWWWWwwwwwwwaaAtttTQqqqqqqqqqqQQQQQQ",
      "WWWWWWWWWwwwwwwwwaaAttQqqqqqqqqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwaaAqqqqqqqqqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWaaAqqqqqqqqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWQqaaAqqqqqqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWQqqaaAqqqqqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWQqqqaaAqqqqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWQqqqqqaaAqqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWQqqqqqqaaAqqQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWQqqqqqqqqaaAQqQQQQQQ",
      "WWWWWWWWWwqwwwwwwwwWQqqqqqqqqqaaAqQQQQQQ",
  ];
  const GUERREIRO_CARTA = [
      "....lRlRdmms....",
      "...lRRlRdmmss...",
      "..mlRlmRdsssdD..",
      "..mlRlmRdsssdD..",
      "..lRRRlRdmmmmm..",
      "..mvvvvldvvvvD..",
      "..mRRRlldmmmmD..",
      "..mlRlmldsssdD..",
      "..mlRlmldsssdD..",
      "..mlRlmldsssdD..",
      "...lRlmldsssd...",
      ".WQRRRllldmmmQw.",
      "WaAQdddddDDDDQqw",
      "WWaAuuttTTTqqQQQ",
      "WWWaAuttTqqqqQQQ",
      "WWWWaAtTqqqqqQQQ",
  ];
  // O Mago (1.91.0): capuz alto de pano azul apagado, a ponta mole caída para trás, o manto do capuz nos ombros, em
  // triângulo, e o rosto na sombra (só a metade de baixo, à luz da esquerda). A/a/b/B o pano, da luz à sombra; Z o fundo
  // do capuz; P/p/o o rosto.
  const PANO_AZUL = { A: "#6a7a98", a: "#4e5b76", b: "#384258", B: "#252c3c", Z: "#101218", P: "#b08868", p: "#8a6650", o: "#5c4434" };
  const MAGO = [
    "........................................",
    ".....................aab................",
    "...................aaaabb...............",
    ".................aaaaaabbB..............",
    "................aaaaaaabbbB.............",
    "...............aaaaaaaabbbb.............",
    "..............aaaaAAAAabbbbB............",
    ".............AaaaAZZZZbbbbbB............",
    ".............AaaAZZZZZZbbbbBB...........",
    "............AAaAZZZZZZZZbbbBB...........",
    "............AAAZZZZZZZZZZbbBB...........",
    "...........AAAAZZZZZZZZZZbbBB...........",
    "...........AAAAZZZZZZZZZZbbBB...........",
    "...........AAAAZZZZpoZZZZbbBB...........",
    "...........AAAAZZpPPoooZZbbBB...........",
    "...........AAAAZopPpoooZZbbBB...........",
    "...........AAAAZoppppooZZbbBB...........",
    "...........AAAAZZpooooZZZbbBB...........",
    "...........AAAaAZZpppoZZbbbBB...........",
    "...........AAAaaAZZooZZbbbbBB...........",
    "..........AAAAaaaAZZZZbbbbbBBa..........",
    ".......AAAaAAAaaaaaaaaabbbbBBbaaa.......",
    ".....AAaaaaaaaaaaaaaaabbbbbbbbbbBaa.....",
    "...AAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBaa...",
    "..AAAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBBBa..",
    ".AAAAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBBBBa.",
    ".AAAAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBBBBB.",
    "AAAAAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBBBBBB",
    "AAAAAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBBBBBB",
    "AAAAAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBBBBBB",
    "AAAAAAAaaaaaaaaaaaaaaabbbbbbbbbbBBBBBbbb",
    "aaaAAAAAAAaaaaaaaaaaaabbbbbbbbbbbbbbbBBB",
    "aaaaaaaaaaAAAAAAAaaaaabbbbbbbbBBBBBBBBBB",
    "aaaaaaaaaabbbbbbbAAAbbbBBBBBBBBBBBBBBBBB",
    "aaaaaaaaaabbbbbbbbbBbbBBBBBBBBBBBBBBBBBB",
    "aaaaaaaaaabbbbbbbbbBbbBBBBBBBBBBBBBBBBBB",
    "aaaaaaaaaabbbbbbbbbBbbBBBBBBBBBBBBBBBBBB",
    "aaaaaaaaaabbbbbbbbbBbbBBBBBBBBBBBBBBBBBB",
    "aaaaaaaaaabbbbbbbbbBbbBBBBBBBBBBBBBBBBBB",
    "aaaaaaaaaabbbbbbbbbBbbBBBBBBBBBBBBBBBBBB",
  ];
  const MAGO_CARTA = [
    "........aab.....",
    ".......aaabb....",
    "......Aaaaabb...",
    ".....AAaaaabbB..",
    ".....AZZZZZbbB..",
    "....AAZZZZZZbBB.",
    "....AAZZZZZZbBB.",
    "....AAZpPpoZbBB.",
    "....AAZppooZbBB.",
    "....AAZZooZZbBB.",
    "...AAAAZZZZbbBB.",
    "..AAAaaaaaabbbB.",
    ".AAAaaaaaaabbbBB",
    "AAAaaaaaaaabbbBB",
    "AAaaaaaaaabbbBBB",
    "AAaaaaaBaabbbBBB",
  ];
  // O Arqueiro (1.91.0): capuz curto e redondo de pano verde apagado, rente à cabeça, que acaba numa capinha nos ombros;
  // o rosto à mostra, o gibão de couro, uma correia só e a boca da aljava com duas penas curtas atrás do ombro. G/g/h/H o
  // pano; Z a sombra do capuz; L/l/m/M o couro; P/p/o o rosto e e os olhos; f/F as penas.
  const PANO_VERDE = { G: "#788a5c", g: "#5b6a45", h: "#434e33", H: "#2d3423", Z: "#151710", L: "#7e6044", l: "#5f4630", m: "#46331f", M: "#2f2217", P: "#c09474", p: "#9a7058", o: "#6a4c3a", e: "#22180f", f: "#a89c80", F: "#7c7260" };
  const ARQUEIRO = [
    "........................................",
    "........................................",
    "........................................",
    "................gggggggh................",
    "..............Ggggggggghhh..............",
    ".............GGgggggggghhhH.............",
    "............GGGggGGGGGGhhhHH............",
    "............GGGgGZZZZZZhhhHH............",
    "............GGGGZZZZZZZZhhHH............",
    "............GGGZZZZZZZZZZhHH...f........",
    "............GGGZooooooZZZhHH.f.f........",
    "............GGGZpPPpppoZZhHH.f.F........",
    "............GGGZpePppeoZZhHH.FMF........",
    "............GGGZpPPPpooZZhHHLLLLl.......",
    "............GGGZpPPPooooZhHHlmmmM.......",
    "............GGGZpPppoooZZhHHlmmmM.......",
    "............GGGZZpoooooZZhHHlmmmM.......",
    "............GGGZZppppoZZZhHHlmmmM.......",
    "............GGGGZZppooZZhhHHlmmmM.......",
    "............GGGgGZZZZZZhhhHHlmmmM.......",
    "...........gggggggggggghhhhhhmmmM.......",
    ".........GGgggggggggggghhhhhhhHmM.......",
    "......LGGGGgggggggggggghhhhhhhHHHl......",
    "....LLGGGGGgggggggggggghhhhhhhHHHHll....",
    "..LLLLGGGGGgggggggggggghhhhhhhHHHHMMll..",
    ".LLLLLLGGGGgggggggggggghhhhhhhHHHMMMMMl.",
    ".LLLLLLlGGGGGGGGGGGGhhhhhhhhhhhhmMMMMMM.",
    "LLLLLLLlllllllllllllllmmmmMMmmmmmMMMMMMM",
    "LLLLLLLlllllllllllllllmmmMMmmmmmmMMMMMMM",
    "LLLLLLLllllllllllllmllmMMmmmmmmmmMMMMMMM",
    "LLLLLLLllllllllllllmlmMMmmmmmmmmmMMMMMMM",
    "LLLLLLLllllllllllllmmMMmmmmmmmmmmMMMMMMM",
    "LLLLLLLlllllllllllmMMlmmmmmmmmmmmMMMMMMM",
    "LLLLLLLllllllllllmMMllmmmmmmmmmmmMMMMMMM",
    "LLLLLLLllllllllmMMlmllmmmmmmmmmmmMMMMMMM",
    "LLLLLLLlllllllmMMllmllmmmmmmmmmmmMMMMMMM",
    "LLLLLLLllllllmMMlllmllmmmmmmmmmmmMMMMMMM",
    "LLLLLLLllllmMMlllllmllmmmmmmmmmmmMMMMMMM",
    "LLLLLLLlllmMMllllllmllmmmmmmmmmmmMMMMMMM",
    "LLLLLLLllmMMlllllllmllmmmmmmmmmmmMMMMMMM",
  ];
  const ARQUEIRO_CARTA = [
    "............f.f.",
    ".....Gggggh.f.F.",
    "....GGgggghhFMF.",
    "....GZZZZZZhLLL.",
    "....GZoooooZlmM.",
    "....GZpeppeZlmM.",
    "....GZPPpooZlmM.",
    "....GZpPoooZlmM.",
    "....GZZppoZhlmM.",
    "...GGgZZZZghlmM.",
    "..GGGgggggghhmM.",
    ".LGGGgggggghhHMl",
    "LLLGGGGGGhhhhMMl",
    "LLLllllllmmmMMMM",
    "LLllllMlmmmmMMMM",
    "LLlllMllmmmmMMMM",
  ];
  /** Um recorte quadrado de `lado` pixels de arte, a partir de (x, y): o mesmo desenho, na mesma escala. */
  const recorte = (grade, x, y, lado) => grade.slice(y, y + lado).map((l) => l.slice(x, x + lado));
  // cada classe com retrato: o desenho de cada papel (busto, busto da janela baixa, cabeça do topo, cabeça da carta)
  const DESENHOS = {
    guerreiro: { cores: FERRO_LA, busto: GUERREIRO, bustoBaixo: recorte(GUERREIRO, 4, 1, 32), cabeca: recorte(GUERREIRO, 8, 1, 24),
      carta: GUERREIRO_CARTA },
    mago: { cores: PANO_AZUL, busto: MAGO, bustoBaixo: recorte(MAGO, 4, 1, 32), cabeca: recorte(MAGO, 8, 1, 24), carta: MAGO_CARTA },
    arqueiro: { cores: PANO_VERDE, busto: ARQUEIRO, bustoBaixo: recorte(ARQUEIRO, 4, 1, 32), cabeca: recorte(ARQUEIRO, 8, 1, 24),
      carta: ARQUEIRO_CARTA },
  };

  return {
    tem: (classe) => !!DESENHOS[classe],
    /** O endereço da imagem do papel (busto, bustoBaixo, cabeca, carta), com `escala` pixels de tela por pixel da arte. */
    url(classe, papel, escala) {
      const d = DESENHOS[classe];
      return Sprites.grade(`retrato-${classe}-${papel}`, d[papel], d.cores, escala);
    },
    /** O desenho do papel num canvas (para quem pinta em canvas: a fogueira), `escala` pixels de tela por pixel da arte. */
    canvas(classe, papel, escala = 1) {
      const d = DESENHOS[classe];
      return Sprites.gradeCanvas(`retrato-${classe}-${papel}`, d[papel], d.cores, escala);
    },
    /** O lado, em pixels de arte, do desenho do papel. */
    lado: (classe, papel) => DESENHOS[classe][papel].length,
  };
})();
