/* Teste de arte (experimento): duas peças da interface desenhadas em código, pelo mesmo método das cenas (uma grade
   de letras, cada letra uma cor), a partir do que já existe no mundo. Não substituem catálogo nenhum.
     Mercador: o homem da banca (telas/mercado.js, FIGURA), mais perto: um busto de 24×24 pixels de arte. As mesmas
       cores e traços: mais velho, careca com a franja grisalha, sobrancelha pesada e desconfiada, nariz comprido, barba
       grisalha, o capuz verde-acinzentado caído nos ombros, a túnica de lã crua e o avental de couro. A luz vem da
       esquerda, como a lamparina da banca. Usado a 48 px (×2) e ampliado a 96 (×4).
     Baú: o baú de ferro da sacristia (telas/cenas.js, desenharBau), de frente, como ícone de 16×16 para a bolsa: a
       tampa abaulada mais clara em cima, a junta escura, as duas cintas com rebites, o espelho de latão com a fechadura
       e as manchas de ferrugem; o contorno escuro da família de ícones. Usado a 32 px (×2) e ampliado a 64 (×4).
     Guerreiro: o primeiro retrato do herói no estilo do mundo (candidato, só aqui no protótipo). Capacete fechado de
       ferro, sem rosto: a calota, a cruz de reforço, a fresta da viseira em duas aberturas e um amassado na calota; a
       gola alta de gibão, a capa de lã nos ombros e a correia da espada. O ferro com as cores do baú e da capela, o
       gibão com as da túnica do mercador; a luz da esquerda, em poucos planos. Um desenho só, de 40×40: o busto da
       ficha é ele inteiro (80 px, ×2); o de janela baixa (64 px) e a cabeça do topo (48 px) são recortes dele, na
       mesma escala. A carta da luta (32 px) tem a versão de 16×16, mais simples (sem o amassado, que lá vira um
       ponto), com a mesma silhueta.
     Mago e Arqueiro (candidatos do teste das três classes): pelo mesmo método e no mesmo enquadramento do Guerreiro.
       Mago: capuz alto de pano azul apagado, a ponta mole caída para trás, o manto do capuz nos ombros e o rosto na
       sombra (só a metade de baixo, com a luz da esquerda). Arqueiro: capuz curto e redondo de pano verde apagado, rente
       à cabeça, que acaba numa capinha nos ombros; o rosto à mostra, o gibão de couro, uma correia só e a boca da aljava
       com duas penas curtas atrás do ombro (a silhueta fica torta de um lado, a do Mago é um triângulo). A carta de cada
       um tem a versão de 16×16.
   Cada pixel da arte vira um quadrado inteiro de pixels da tela (nada de suavizar). */
"use strict";

const ArteTeste = (() => {
  const MERCADOR = {
    cores: { L: "#d09a70", s: "#b07a56", d: "#7e5236", n: "#7e5236", k: "#8a8478", K: "#5e5a52", h: "#a8a296", w: "#4a463e",
      e: "#120c08", B: "#7a7266", b: "#5a544a", H: "#9a9488", M: "#3a2418", c: "#4e5640", C: "#363c2c", g: "#5e6850",
      u: "#8a7a5a", t: "#6e6046", T: "#4a402e", a: "#5a3e28", A: "#3e2a1a", x: "#4a3220", y: "#704c2e" },
    // L/s/d pele (luz, meio, sombra), n nariz, h/k/K franja grisalha, w sobrancelha, e olho, H/B/b barba, M boca,
    // g/c/C capuz caído, u/t/T túnica, a/A avental, y a alça do avental, x mancha no couro
    grade: [
      "........................",
      "..........LLLsd.........",
      "........LLLLLssdd.......",
      ".......LLLLsssssdd......",
      ".......LLssssssssd......",
      "......hLsssddssddsdK....",
      "......kLsssssssssdK.....",
      "......kwwwLssssLwwwK....",
      ".....dkLweesssseewdKd...",
      ".....dkLsssLsnsssddKd...",
      "......kLssssLnnssddK....",
      "......kKsssLsnnsddKK....",
      "......KBBsdLnnndBbbK....",
      ".......BHBBdMMMdBbb.....",
      ".......BHBBBBBBBbbb.....",
      "........BHBBBBBbbb......",
      ".........BBBBBbbb.......",
      ".......ccgBBBbbCCC......",
      ".....ccgcccdddCCCCCC....",
      "...uuuuccgcccCCCCCttTT..",
      "..uuuuttayaaaaaaAAttTTT.",
      "..uuuttaayaaaaaaAAtttTT.",
      ".uuuuttaaaaaxaaaAAtttTTT",
      ".uuuuttaaaaaaaaaAAtttTTT",
    ],
  };
  const BAU = {
    cores: { o: "#0d0b0a", l: "#6e7078", f: "#45474e", j: "#1c1d21", m: "#38393f", e: "#2a2b30", s: "#53555c", S: "#62646c",
      r: "#9a9ca4", p: "#7a6438", P: "#a8904c", h: "#120f0c", R: "#6a3e24" },
    // o contorno, l/f a tampa (luz e ferro), j a junta, m/e o corpo (meio e sombra), s/S as cintas, r os rebites,
    // p/P o espelho de latão, h a fechadura, R a ferrugem
    grade: [
      "................",
      "...ooooooooooo..",
      "..olSlllllllSlo.",
      ".ollSlllllllSllo",
      ".offsfffRfffsffo",
      ".offsfPPPPffsffo",
      ".ojjsjppppjjsjjo",
      ".olmsmphhpmmsmeo",
      ".olmrmphhpmmrmeo",
      ".olmsmmppmmmsmeo",
      ".olmsmmmmmmmsmeo",
      ".olRsmmmmmmmsmeo",
      ".olmrmmmmmmRrmeo",
      ".oeeeeeeeeeeeeeo",
      ".oooooooooooooo.",
      "................",
    ],
  };
  // R/l/m/s/d/D o ferro, da luz à sombra (o brilho, o plano da luz, a frente, o plano da sombra, a borda, o fundo); v a
  // fresta; W/w/q/Q a capa de lã (ombro na luz, frente, sombra, o fundo junto do capacete); u/t/T o gibão; a/A a correia
  const FERRO_LA = { R: "#b4b6bc", l: "#8c8e96", m: "#6e7078", s: "#53555c", d: "#3c3e44", D: "#26272c", v: "#0d0b0a",
    W: "#5a707a", w: "#405660", q: "#2e3d44", Q: "#20292e", u: "#9a8a66", t: "#7a6c4e", T: "#544a36", a: "#6e4c30", A: "#4a3220" };
  const GUERREIRO = {
    cores: FERRO_LA,
    grade: [
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
    ],
  };
  const GUERREIRO_CARTA = {
    cores: FERRO_LA,
    grade: [
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
    ],
  };
  // Mago e Arqueiro (candidatos, só aqui): o mesmo método e o mesmo enquadramento do Guerreiro (a cabeça na mesma
  // região, para os recortes de 64 e 48 px servirem aos três); a carta, uma versão de 16×16 de cada um.
  // Mago: A/a/b/B o pano azul apagado, da luz à sombra; Z o fundo do capuz; P/p/o o rosto (luz, meio, sombra)
  const PANO_AZUL = { A: "#6a7a98", a: "#4e5b76", b: "#384258", B: "#252c3c", Z: "#101218", P: "#b08868", p: "#8a6650", o: "#5c4434" };
  const MAGO = { cores: PANO_AZUL, grade: [
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
  ] };
  const MAGO_CARTA = { cores: PANO_AZUL, grade: [
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
  ] };
  // Arqueiro: G/g/h/H o pano verde apagado; Z a sombra do capuz; L/l/m/M o couro; P/p/o o rosto, e os olhos; f/F as penas
  const PANO_VERDE = { G: "#788a5c", g: "#5b6a45", h: "#434e33", H: "#2d3423", Z: "#151710", L: "#7e6044", l: "#5f4630", m: "#46331f", M: "#2f2217", P: "#c09474", p: "#9a7058", o: "#6a4c3a", e: "#22180f", f: "#a89c80", F: "#7c7260" };
  const ARQUEIRO = { cores: PANO_VERDE, grade: [
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
  ] };
  const ARQUEIRO_CARTA = { cores: PANO_VERDE, grade: [
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
  ] };
  /** Um recorte quadrado de `lado` pixels de arte, a partir de (x, y): o mesmo desenho, na mesma escala. */
  const recorte = (peca, x, y, lado) => ({ cores: peca.cores, grade: peca.grade.slice(y, y + lado).map((l) => l.slice(x, x + lado)) });
  const PECAS = { mercador: MERCADOR, bau: BAU, guerreiro: GUERREIRO, "guerreiro-busto-baixo": recorte(GUERREIRO, 4, 1, 32),
    "guerreiro-cabeca": recorte(GUERREIRO, 8, 1, 24), "guerreiro-carta": GUERREIRO_CARTA,
    mago: MAGO, "mago-busto-baixo": recorte(MAGO, 4, 1, 32), "mago-cabeca": recorte(MAGO, 8, 1, 24), "mago-carta": MAGO_CARTA,
    arqueiro: ARQUEIRO, "arqueiro-busto-baixo": recorte(ARQUEIRO, 4, 1, 32), "arqueiro-cabeca": recorte(ARQUEIRO, 8, 1, 24),
    "arqueiro-carta": ARQUEIRO_CARTA };

  const cache = {};
  /** A peça desenhada num canvas, cada pixel da arte em `escala` × `escala` pixels. */
  function canvas(nome, escala = 1) {
    const { grade, cores } = PECAS[nome];
    const c = document.createElement("canvas");
    c.width = grade[0].length * escala; c.height = grade.length * escala;
    const ctx = c.getContext("2d");
    grade.forEach((linha, y) => [...linha].forEach((ch, x) => {
      if (ch === ".") return;
      ctx.fillStyle = cores[ch]; ctx.fillRect(x * escala, y * escala, escala, escala);
    }));
    return c;
  }
  /** A peça como endereço de imagem (data URL), já na escala. */
  function url(nome, escala = 1) {
    const chave = `${nome}@${escala}`;
    return cache[chave] || (cache[chave] = canvas(nome, escala).toDataURL());
  }
  /** Uma <img> no tamanho de uso: `escala` pixels de tela por pixel da arte (e o dobro para telas densas). */
  function img(nome, escala, classe = "", alt = "") {
    const { grade } = PECAS[nome], w = grade[0].length * escala, h = grade.length * escala;
    return `<img class="arte-teste ${classe}" src="${url(nome, escala)}" srcset="${url(nome, escala * 2)} 2x" width="${w}" height="${h}" alt="${alt}" draggable="false">`;
  }
  return { canvas, url, img, PECAS };
})();
