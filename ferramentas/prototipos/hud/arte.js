/* Protótipo da ficha: os assets próprios, desenhados em código como os cenários, na paleta indexada do jogo
   (Sprites.PALETA). Experimento: nada daqui é usado pelo jogo.

   Os ícones e o retrato são mapas de MATERIAL, não de cor: cada letra diz do que a parte é feita (aço, ouro, couro,
   pele...), e o pintor decide a luz. A luz vem de cima e da esquerda, como nos painéis do jogo: a borda de cima e a da
   esquerda de cada material ficam no tom claro, a de baixo e a da direita no escuro, e o miolo no médio, com um
   pontilhado (Bayer) que escurece para o canto de baixo. Onde um material encosta no vazio, entra o contorno preto.
   Assim, cada peça tem contorno e volume já na escala de uso (16 texels num espaço de 40 px), e não só ampliada. */
"use strict";

const Arte = (() => {
  const P = Sprites.PALETA;
  const { pontilha } = Sprites;

  // Material: [claro, médio, escuro] (letras da paleta). "fixo" pinta sempre a mesma cor (olhos, brilhos).
  const MATERIAIS = {
    A: ["W", "G", "g"],   // aço polido (lâmina, elmo)
    a: ["G", "g", "d"],   // aço velho (ombreiras, aro)
    T: ["g", "d", "K"],   // ferro escuro (sombra do elmo, malha)
    O: ["Y", "y", "C"],   // ouro (guarda, aro do anel, rebite)
    o: ["y", "c", "C"],   // ouro velho (emblema)
    L: ["n", "b", "B"],   // couro e madeira
    P: ["h", "h", "H"],   // pele
    B: ["n", "b", "B"],   // barba
    R: ["R", "r", "D"],   // pano vermelho, poção
    V: ["U", "u", "v"],   // gema azul
    G: ["G", "T", "t"],   // vidro
    k: "k", w: "w", W: "W", h: "H", r: "D",  // fixos: contorno, brilho, branco, sombra de pele, boca
  };

  /** Pinta um mapa de materiais num canvas: contorno onde o material encosta no vazio, luz em cima e à esquerda,
   *  sombra embaixo e à direita, e o miolo pontilhado para o escuro no canto de baixo. */
  function pintar(mapa, { contorno = true } = {}) {
    const h = mapa.length, w = mapa[0].length;
    mapa.forEach((l, y) => { if (l.length !== w) throw new Error(`linha ${y} com ${l.length} (esperado ${w})`); });
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    const x = c.getContext("2d");
    const em = (i, j) => (j >= 0 && j < h && i >= 0 && i < w ? mapa[j][i] : ".");
    const set = (i, j, letra) => { x.fillStyle = P[letra]; x.fillRect(i, j, 1, 1); };
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const m = em(i, j);
      if (m === ".") {
        if (contorno && [em(i - 1, j), em(i + 1, j), em(i, j - 1), em(i, j + 1)].some((v) => v !== ".")) set(i, j, "k");
        continue;
      }
      const mat = MATERIAIS[m];
      if (!mat) throw new Error(`material desconhecido: ${m}`);
      if (typeof mat === "string") { set(i, j, mat); continue; }
      const outro = (v) => v !== m && !(typeof MATERIAIS[v] === "string");  // brilho e olho não quebram o volume
      const luz = outro(em(i, j - 1)) || outro(em(i - 1, j));
      const sombra = outro(em(i, j + 1)) || outro(em(i + 1, j));
      let tom = 1;
      if (sombra && !luz) tom = 2;
      else if (luz && !sombra) tom = 0;
      else if (!luz && !sombra && pontilha(i, j, Math.max(0, Math.min(6, Math.round((i / w + j / h - 1.1) * 9))))) tom = 2;
      set(i, j, mat[tom]);
    }
    return c;
  }

  // ------------------------------------------------------------ ícones (16×16)
  const ICONES = {
    espada: [
      "................",
      ".............AA.",
      "............AAA.",
      "...........AAA..",
      "..........AAA...",
      ".........AAA....",
      "........AAA.....",
      ".......AAA......",
      "..OO..AAA.......",
      "...OOAAA........",
      "....OOA.........",
      "....LOOO........",
      "...LL..OO.......",
      "..LL............",
      ".OO.............",
      ".OO.............",
    ],
    escudo: [
      "................",
      "..aaaaaaaaaaaa..",
      "..aRRRRRaRRRRa..",
      "..aRRRRRaRRRRa..",
      "..aRRRRRaRRRRa..",
      "..aRRRROOORRRa..",
      "..aaaaaOOOaaaa..",
      "..aRRRROOORRRa..",
      "..aRRRRRaRRRRa..",
      "...aRRRRaRRRa...",
      "...aRRRRaRRRa...",
      "....aRRRaRRa....",
      ".....aRRaRa.....",
      "......aaaa......",
      ".......aa.......",
      "................",
    ],
    anel: [
      "................",
      "......VVVV......",
      ".....VVWVVV.....",
      "......VVVV......",
      ".....OOOOOO.....",
      "....OOOOOOOO....",
      "...OOO....OOO...",
      "...OO......OO...",
      "...OO......OO...",
      "...OO......OO...",
      "...OOO....OOO...",
      "....OOOOOOOO....",
      ".....OOOOOO.....",
      "................",
      "................",
      "................",
    ],
    pocao: [
      "................",
      "......LLLL......",
      "......LLLL......",
      ".......GG.......",
      ".......GG.......",
      "......GGGG......",
      ".....GRRRRG.....",
      "....GRRWRRRG....",
      "....GRWRRRRG....",
      "....GRRRRRRG....",
      "....GRRRRRRG....",
      "....GRRRRRRG....",
      ".....GRRRRG.....",
      "......GGGG......",
      "................",
      "................",
    ],
  };

  // ------------------------------------------------------------ o retrato do Guerreiro (32×32)
  // Elmo de aço com nasal e protetores de face, olhar firme, barba curta, malha no pescoço, ombreiras e o tabardo
  // vermelho com a cruz da ordem em ouro velho.
  const RETRATO_GUERREIRO = [
    "................................",
    "............AAAAAAAA............",
    "..........AAAAAAAAAAAA..........",
    ".........AAAAAAAAAAAAAA.........",
    "........AAAAAAAAAAAAAAAA........",
    "........AAAAAAAAAAAAAAAA........",
    "........AAAAAAAAAAAAAAAA........",
    "........AAAAAAAAAAAAAAAA........",
    ".......aaaaaaaaaaaaaaaaaa.......",
    ".......aOaaaaaaaaaaaaaaOa.......",
    ".......aaaaTTTTAATTTTaaaa.......",
    "........aaTPPPPAAPPPPTaa........",
    "........aaTPkwPAAPwkPTaa........",
    "........aaTPPPPAAPPPPTaa........",
    "........aaTPPPPhhPPPPTaa........",
    "........aaTPPBBhhBBPPTaa........",
    "........aaTPBBBBBBBBPTaa........",
    "........aaTTBBBBBBBBTTaa........",
    ".........aaTTBBBBBBTTaa.........",
    "...........TTTBBBBTTT...........",
    "..........TTTTTTTTTTTT..........",
    "...aaaaaaaTTTTTTTTTTTTaaaaaaa...",
    "..aaaaaaaaaRRRRRRRRRRaaaaaaaaa..",
    ".aaaaaaaaaaRRRRRRRRRRaaaaaaaaaa.",
    ".TTTTTTTTTaRRRRooRRRRaTTTTTTTTT.",
    ".aaaaaaaaaaRRRRooRRRRaaaaaaaaaa.",
    ".TaaaaaaaaTRRooooooRRTaaaaaaaaT.",
    ".TTaaaaaaTTRRooooooRRTTaaaaaaTT.",
    ".TTTTTTTTTTRRRRooRRRRTTTTTTTTTT.",
    ".TTTTTTTTTTRRRRooRRRRTTTTTTTTTT.",
    ".TTTTTTTTTTRRRRRRRRRRTTTTTTTTTT.",
    ".TTTTTTTTTTRRRRRRRRRRTTTTTTTTTT.",
  ];

  // ------------------------------------------------------------ a moldura (nove partes) e o espaço de item
  /** A moldura dos painéis: ferro escurecido com o filete de bronze por dentro, a luz em cima e à esquerda e um
   *  rebite em cada canto (o único ouro dela). É uma imagem de 3·c texels, recortada em nove partes pelo CSS
   *  (border-image): os cantos nunca esticam, e as bordas são lisas no comprimento, então esticar não muda nada. */
  function moldura(c = 6) {
    const n = c * 3, cv = document.createElement("canvas");
    cv.width = cv.height = n;
    const x = cv.getContext("2d");
    const set = (i, j, l) => { x.fillStyle = P[l]; x.fillRect(i, j, 1, 1); };
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      const d = Math.min(i, j, n - 1 - i, n - 1 - j);     // distância até a borda de fora
      const claro = (j <= i && j <= n - 1 - i) || (i < j && i <= n - 1 - j);  // a metade de cima e a da esquerda
      let l = null;
      if (d === 0) l = "k";                               // o contorno
      else if (d === 1) l = claro ? "d" : "K";            // a quina do ferro: acesa em cima e à esquerda
      else if (d === 2 || d === 3) l = claro ? "K" : "s"; // o corpo do ferro
      else if (d === 4) l = claro ? "J" : "j";            // o filete de bronze
      else if (d === 5) l = "k";                          // a sombra para dentro
      if (l) set(i, j, l);
    }
    // os rebites: um ponto de ouro velho com sombra, no meio de cada canto
    for (const [cx, cy] of [[2, 2], [n - 4, 2], [2, n - 4], [n - 4, n - 4]]) {
      set(cx, cy, "a"); set(cx + 1, cy, "c"); set(cx, cy + 1, "c"); set(cx + 1, cy + 1, "C");
    }
    return cv;
  }

  /** O espaço de um item: um nicho fundo na pedra, com a quina de cima e da esquerda na sombra e a de baixo e da
   *  direita acesa (é um buraco, não uma placa), os cantos cortados e o fundo com um grão quase invisível. */
  function espaco(n = 20) {
    const cv = document.createElement("canvas");
    cv.width = cv.height = n;
    const x = cv.getContext("2d");
    const set = (i, j, l) => { x.fillStyle = P[l]; x.fillRect(i, j, 1, 1); };
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      const d = Math.min(i, j, n - 1 - i, n - 1 - j);
      const canto = (i === 0 || i === n - 1) && (j === 0 || j === n - 1);
      if (canto) continue;                                // canto cortado
      const fundoSup = i <= j ? i : j, cima = j <= i && j <= n - 1 - i, esq = i < j && i <= n - 1 - j;
      void fundoSup;
      let l;
      if (d === 0) l = "k";
      else if (d === 1) l = cima || esq ? "N" : "d";      // a beira do nicho: sombra em cima e à esquerda, luz embaixo
      else if (d === 2) l = cima || esq ? "z" : "Q";
      else l = pontilha(i, j, 2) ? "Q" : "q";             // o fundo: escuro, mas acima do contorno preto dos ícones
      set(i, j, l);
    }
    return cv;
  }

  const cache = {};
  const url = (chave, f) => (cache[chave] ||= f().toDataURL());
  return {
    MATERIAIS,
    icone: (nome) => (ICONES[nome] ? url("ic:" + nome, () => pintar(ICONES[nome])) : null),
    temIcone: (nome) => !!ICONES[nome],
    retrato: () => url("retrato", () => pintar(RETRATO_GUERREIRO)),
    moldura: () => url("moldura", () => moldura(6)),
    espaco: () => url("espaco", () => espaco(20)),
    pintar,
  };
})();
