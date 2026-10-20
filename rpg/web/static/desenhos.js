/* Os itens desenhados em código, pelo método das cenas e dos retratos (uma grade de letras com a paleta do desenho,
   pintada por Sprites.grade, cada pixel da arte um quadrado inteiro da tela). Icones pede aqui o desenho de um papel
   quando ele existe; o resto continua com os desenhos da HUD (hud/icones/). Cada item é desenhado em 32×32, o tamanho
   em que vive (a bolsa, a mochila, o mercado, o espólio); em 64 px aparece a 2×, pixel a pixel; em 48 px (o item que
   voa para o corpo, o cartão compacto do saque), a versão a 2× reduzida pelo navegador, como os outros ícones da HUD.
   Aprovados no experimento de resolução (ferramentas/prototipos/hud/resolucao-teste.html), desde a 1.93.0. O martelo
   tem, desde a 1.149.0, o 40 e o 48 em arquivo (hud/icones/martelo-40.png e -48, a mesma construção na grade de cada
   tamanho), que o Icones usa nesses tamanhos; a grade daqui continua sendo o 32 e o 64. */
"use strict";

const Desenhos = (() => {
  // O martelo de guerra (o equipamento "Martelo" do Guerreiro): o cabo de madeira na diagonal, como a maça e a espada,
  // a cabeça de ferro atravessada no alto, o colar e o pomo de latão, a empunhadura de couro; a luz de cima-esquerda.
  const CORES_MARTELO = { "#": "#121316", D: "#33373e", L: "#6a4430", M: "#9a6438", S: "#b0b6c0", W: "#e4e8ee", Y: "#e0b850", d: "#4e545e", l: "#43281a", m: "#6e4426", n: "#4a2c18", s: "#7c838e", y: "#a87c2c" };
  const MARTELO = [
    "................................",
    ".......................##.......",
    "......................#WW#......",
    ".....................#SSWW#.....",
    "....................#SSSSWW#....",
    "...................#SSSSssWW#...",
    "..................#DDSSssssWW#..",
    "...................#DDsssssdSS#.",
    "....................#DDsssdddS#.",
    "...................#YYDDsdddd#..",
    "..................#YYyyDDddd#...",
    "..................#Myyy#DDd#....",
    ".................#Mmny#.#D#.....",
    "................#Mmn##...#......",
    "...............#Mmn#............",
    "..............#Mmn#.............",
    ".............#Mmn#..............",
    "............#Mmn#...............",
    "...........#Mmn#................",
    "..........#Mmn#.................",
    ".........#Mmn#..................",
    "........#Mmn#...................",
    ".......#Mmn#....................",
    "......#Mmn#.....................",
    ".....#LLn#......................",
    "....#lll#.......................",
    "...#Lll#........................",
    "..#YLl#.........................",
    ".#YYy#..........................",
    ".#yy#...........................",
    "..##............................",
    "................................",
  ];
  // A Pena de Fênix: uma pena de voo curva, o cálamo marfim, do vermelho fundo da base ao dourado da ponta, a cor
  // correndo pelas barbas.
  const CORES_PENA = { "#": "#1c0d0a", C: "#f4e2b0", G: "#f6c24a", O: "#e86a1c", R: "#a8281c", c: "#c8a868", g: "#d08c24", o: "#b8461a", r: "#74180f" };
  const PENA = [
    "................................",
    "................................",
    "................................",
    "...........................#....",
    "..........................#G#...",
    "........................##GC#...",
    ".......................#GGC#....",
    ".....................##GGCC#....",
    "....................#OOGGCg#....",
    "...................#OOOGCg#.....",
    "..................#OOOGCC#......",
    ".................#OOOOGC#o#.....",
    "................#ROOOOCoo#......",
    "...............##ROOOCooo#......",
    "..............#R#ROOCCoo#.......",
    ".............#RR#OOCCooo#.......",
    "............#RRRROOCooo#........",
    "............#RRRROCoorr#........",
    "...........#RRRRRCrrrr#.........",
    "...........#RRRCCrrrr#..........",
    "...........#RRCCrrrr#...........",
    "..........#RRCCrrr##............",
    "..........#RCCrr##..............",
    "........##CCr###................",
    ".......#CCC##...................",
    ".....##CCc#.....................",
    "....#CCCc#......................",
    "...#CCc##.......................",
    "..#CC##.........................",
    "...##...........................",
    "................................",
    "................................",
  ];

  const DESENHOS = { martelo: { cores: CORES_MARTELO, grade: MARTELO }, pena: { cores: CORES_PENA, grade: PENA } };
  return {
    tem: (nome) => !!DESENHOS[nome],
    /** O lado do desenho, em pixels de arte. */
    lado: (nome) => DESENHOS[nome].grade.length,
    /** O endereço da imagem, com `escala` pixels de tela por pixel da arte. */
    url: (nome, escala) => Sprites.grade(`desenho-${nome}`, DESENHOS[nome].grade, DESENHOS[nome].cores, escala),
  };
})();
