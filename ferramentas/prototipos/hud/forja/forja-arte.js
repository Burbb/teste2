/* O interior da forja do Vau, duas direções (protótipo, 25/10/2026; nada no jogo). Um quadro de 320×72, o mesmo das
   paisagens e dos ambientes da capela (telas/cenas.js), ampliado pela tela em escala inteira. O ambiente (paredes,
   chão, a luz do fogo caindo nos volumes) é pintado em código, com o pontilhado de Bayer 4×4 do jogo; as figuras e os
   objetos (o ferreiro, a bigorna, a fornalha, as ferramentas) são grades desenhadas à mão, um caractere por pixel.
     A · a bancada de trabalho: perto, o ferreiro e a bigorna conduzindo; a fornalha à esquerda iluminando os volumes;
         as ferramentas na parede e a porta à direita.
     B · o interior da oficina: mais aberto, com profundidade; a fornalha ao fundo, a bigorna no meio, o armazém à
         direita e a porta com a luz fria do dia.
   Uma animação ambiente só: as brasas e as línguas do fogo trocam devagar (com movimento reduzido, o quadro fica
   parado). Exporta window.ForjaArte = { a, b }, cada um { base(W, d), desenhar(c, W, b, est, quadro, destaque),
   pontos } no formato das cenas da capela. */
"use strict";

window.ForjaArte = (() => {
  const QW = 320, QH = 72;
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const pont = (x, y, n) => BAYER[(y & 3) * 4 + (x & 3)] < n;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const camada = (W) => { const k = document.createElement("canvas"); k.width = W; k.height = QH; return k; };
  const pincel = (c) => (x, y, w = 1, h = 1, cor) => { if (!cor) return; c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, h); };
  /** Uma grade desenhada à mão: cada caractere um pixel, `.` transparente, as cores pela paleta. `espelho`: vira. */
  function grade(px, x0, y0, linhas, pal, espelho = false) {
    const w = Math.max(...linhas.map((l) => l.length));
    linhas.forEach((l, y) => [...l].forEach((ch, x) => { if (ch !== "." && ch !== " " && pal[ch]) px(x0 + (espelho ? w - 1 - x : x), y0 + y, 1, 1, pal[ch]); }));
  }
  /** A luz do fogo: de 0 (frio) a 1 (perto da boca), caindo com a distância; o pontilhado escolhe o tom. */
  function luz(x, y, fx, fy, raio, achatar = 1) {
    const d = Math.hypot(x - fx, (y - fy) * achatar);
    return Math.max(0, 1 - d / raio);
  }
  /** Entre duas cores pelo pontilhado: t de 0 a 1. */
  const entre = (x, y, fria, quente, t) => (pont(x, y, Math.round(t * 16)) ? quente : fria);
  /** Entre três (o frio, o meio, o quente): o degradê em dois passos curtos, sem a faixa larga de xadrez. */
  const entre3 = (x, y, fria, meio, quente, t) => (t < 0.5 ? entre(x, y, fria, meio, t * 2) : entre(x, y, meio, quente, (t - 0.5) * 2));

  // ---------------------------------------------------------------- as cores
  const K = "#0a090b";
  const PAL = {
    k: K,
    // o ferro: escuro, meio, luz, brilho
    f: "#1d1f24", F: "#383b43", G: "#5c606a", H: "#9a9ea8", I: "#d4d8de",
    // a madeira
    m: "#231811", M: "#3e2b1c", n: "#5a3f28", N: "#7a5836",
    // a pele (o fogo de lado), o cabelo e a barba
    s: "#4e2c1e", S: "#84492e", L: "#b86e44", T: "#e2a06a", b: "#1c1310", B: "#3a2518",
    // o avental de couro, a camisa
    a: "#24170f", A: "#43291a", Z: "#63402a", c: "#1f2027", C: "#35343b",
    // o fogo e o ferro em brasa
    o: "#4a1208", O: "#962a0c", r: "#d8541a", R: "#ff9430", y: "#ffcf6a", Y: "#fff0bc",
    // a pedra e o tijolo da fornalha
    p: "#1a1a1f", P: "#2a2a31", q: "#3b3a41", t: "#3a1e16", u: "#5a2e1e", v: "#7a4026",
    // a água da tina, a luz fria do dia
    w: "#0e1820", W: "#24384a", d: "#3e566a", D: "#7c96a8", e: "#b6c8d2",
  };

  // ---------------------------------------------------------------- o ferreiro (à mão)
  // A: perto, de frente para a bigorna (à esquerda dele), o martelo erguido na mão direita (à direita da tela), a tenaz
  // na esquerda segurando a barra em brasa. Ombros largos, braços grossos, a careca e a barba curta, o avental de couro
  // até os joelhos. O fogo vem da esquerda: o lado esquerdo do corpo aceso (L, T), o direito na sombra (s, S).
  const FERREIRO_A = [
    "............................kkkkkkkkkk..",
    "...........................kFGGHHHGGFk..",
    "...........................kFGGGGGGGFk..",
    "...........................kFFGGGGGFFk..",
    "............................kkkkMkkkk...",
    "...............................kMk......",
    "...............................kMk......",
    "...............................kMk......",
    "..............kkkkkkk..........kMk......",
    ".............kbbbbbbbk........kSSk......",
    "............kbbbbBbbbbk......kSLSSk.....",
    "............kbTLLSSSbbk......kSLSSk.....",
    "............kTLLLSSSSSk......kSSSk......",
    "............kTkkLSkkSSk.....kSSSk.......",
    "............kTLLLSSSSSk.....kSSk........",
    "............kLTLLLSSSSk....kSSSk........",
    "............kLBLLLSSBSk....kSSk.........",
    ".............kBBLLSBBk....kSSSk.........",
    ".............kBBBBBBBk...kSSSk..........",
    "..............kBBBBBk...kSSSk...........",
    "...........kkkkLSSSkkkkkSSSk............",
    ".........kkTTLLaLSSSSSSaSSk.............",
    "........kTTTLLZAAAAAAASaSSk.............",
    ".......kTTLLLkZAAAAAAAAaSSk.............",
    ".......kTLLLkZAAAAAAAAAASSk.............",
    "......kTTLLkZAAAAAAAAAAAASk.............",
    "......kTLLk.kZAAAAAAAAAAAk..............",
    ".....kTTLLk.kZAAAAAAAAAAAk..............",
    ".....kTLLk..kZAAAAAAAAAAAk..............",
    "....kTTLk...kZAAAAAAAAAAAk..............",
    "....kTLLk...kaaaaaGGaaaaak..............",
    "...kTTLk....kZAAAAAAAAAAAk..............",
    "..kTTLLk....kZAAAAAAAAAAAk..............",
    ".kTTLLk.....kZAAAaAAAaAAAk..............",
    "kTTLLk......kZAAAaAAAaAAAk..............",
    "kLLLk.......kZAAAaAAAaAAAk..............",
    "kLLSk.......kZAAAaAAAaAAAk..............",
    ".kkk........kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kZAAAaAAAaAAAk..............",
    "............kkZAAAAAAAAAkk..............",
    ".............kcCCkkkcCCCk...............",
    ".............kcCCk.kcCCCk...............",
    ".............kcCCk.kcCCCk...............",
    ".............kcCCk.kcCCCk...............",
    ".............kcCCk.kcCCCk...............",
    ".............kcCCk.kcCCCk...............",
    "............kMMMMk.kMMMMk...............",
    "............kkkkkk.kkkkkk...............",
  ];

  // a bigorna de frente-lado: a mesa larga, o chifre para a esquerda, a cintura e o pé; o tronco de madeira embaixo
  const BIGORNA_A = [
    "..............kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk...",
    "kkkkkkkkkkkkkkkIIIHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHGk..",
    ".kHHHHHHHHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFk.",
    "..kkHGGGGGGGGGGGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFk.",
    "....kkkGGGGGGGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfk.",
    ".......kkkkkkkkkFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfkk.",
    "................kkfFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfkk...",
    "..................kkfFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfkk.....",
    "....................kfFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfk.......",
    "....................kfFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfk.......",
    "...................kfFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfk......",
    ".................kkfGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfkk....",
    "...............kkGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfkk..",
    "...............kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
    "................kNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNk...",
    "................knMMMnMMMMMMnMMMMMMMnMMMMMMMnMMMMMMMnMMMMk...",
    "................knMMMnMMMMMMnMMMMMMMnMMMMMMMnMMMMMMMnMMMMk...",
    "................knMMMnMMMMMMnMMMMMMMnMMMMMMMnMMMMMMMnMMMMk...",
    "................knMMMnMMMMMMnMMMMMMMnMMMMMMMnMMMMMMMnMMMMk...",
    "................knMMMnMMMMMMnMMMMMMMnMMMMMMMnMMMMMMMnMMMMk...",
    "................knMMMnMMMMMMnMMMMMMMnMMMMMMMnMMMMMMMnMMMMk...",
    "................kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmk...",
  ];

  // a fornalha de tijolo, a boca com as brasas (o fogo anima por cima) e a coifa que sobe para a chaminé
  function fornalhaA(px, x0, piso) {
    // a coifa: um tronco de pirâmide de ferro batido, saindo pelo alto do quadro
    for (let y = 0; y < 22; y++) {
      const meia = 14 + Math.round(y * 0.95);
      for (let x = -meia; x <= meia; x++) {
        const borda = Math.abs(x) >= meia - 1;
        const cor = borda ? K : x < -meia + 4 ? PAL.G : x < 0 ? PAL.F : PAL.f;
        px(x0 + 37 + x, y, 1, 1, cor);
      }
      if (y % 5 === 2) for (let x = -meia + 2; x <= meia - 2; x += 6) px(x0 + 37 + x, y, 1, 1, PAL.H);  // os rebites
    }
    // a aba da coifa
    px(x0 + 1, 22, 74, 2, K); px(x0 + 2, 22, 72, 1, PAL.G);
    // o corpo de tijolo
    for (let y = 24; y < piso; y++) {
      for (let x = 2; x < 72; x++) {
        const fiada = Math.floor((y - 24) / 3), deslo = fiada % 2 ? 3 : 0;
        const junta = (y - 24) % 3 === 2 || (x + deslo) % 7 === 0;
        px(x0 + x, y, 1, 1, junta ? PAL.t : x < 8 ? PAL.v : PAL.u);
      }
    }
    px(x0 + 1, 24, 1, piso - 24, K); px(x0 + 72, 24, 1, piso - 24, K);
    // a boca: o arco escuro e o leito de brasas
    for (let y = 32; y < 50; y++) {
      const meia = y < 36 ? 20 - (36 - y) * 2 : 22;
      for (let x = -meia; x <= meia; x++) px(x0 + 37 + x, y, 1, 1, Math.abs(x) >= meia - 1 ? K : PAL.o);
    }
    for (let x = 16; x < 59; x++) px(x0 + x, 50, 1, 1, K);
    // a borda de pedra da boca (a soleira)
    px(x0 + 12, 50, 51, 3, PAL.q); px(x0 + 12, 50, 51, 1, PAL.G); px(x0 + 12, 53, 51, 1, K);
  }
  /** As brasas e as línguas: o que muda de quadro em quadro (k de 0 a 2). */
  function fogoA(px, x0, k) {
    const leito = 46;
    for (let x = 17; x < 58; x++) {
      const v = (x * 7 + k * 5) % 9;
      px(x0 + x, leito + 2, 1, 2, v < 3 ? PAL.R : PAL.r);
      px(x0 + x, leito + 1, 1, 1, v < 2 ? PAL.y : PAL.R);
    }
    // as línguas: três chamas altas, trocando de altura
    [[24, 9], [35, 13], [47, 10], [53, 6]].forEach(([cx, alt], i) => {
      const h = alt - ((k + i) % 3) * 2;
      for (let y = 0; y < h; y++) {
        const largura = Math.max(1, Math.round((1 - y / h) * 4));
        const cor = y < h * 0.35 ? PAL.y : y < h * 0.7 ? PAL.R : PAL.r;
        px(x0 + cx - Math.floor(largura / 2) + ((y + k + i) % 2), leito - y, largura, 1, cor);
      }
      px(x0 + cx, leito - 1, 1, 1, PAL.Y);
    });
  }

  // as ferramentas penduradas: a tenaz, dois martelos e a lima, no quadro de madeira (A)
  const FERRAMENTAS = [
    "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
    "kNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNk",
    "knMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMnk",
    "kkkGkkkkkkkkGkkkkkkkkkkGkkkkkkGkkk",
    "...G........G..........G......G...",
    "..kHk.....kkGkk.....kkkGkk....G...",
    "..kGk....kHHHHHk...kHHHHHHk...G...",
    "..kGk....kGGGGGk...kGGGGGGk..kHk..",
    ".kG.Gk....kkMkk.....kkMMkk...kGk..",
    ".kG.Gk......M.........MM.....kGk..",
    ".kG.Gk......M.........MM.....kGk..",
    "kG...Gk.....M.........MM.....kFk..",
    "kG...Gk.....M.........MM.....kFk..",
    "kF...Fk.....k.........kk......k...",
    ".k...k............................",
  ];

  const TINA = [
    ".kkkkkkkkkkkkkkkkkk.",
    "kNNNNNNNNNNNNNNNNNNk",
    "kWdDWWWdWWWWWdWWWWnk",
    "knwwwwwwwwwwwwwwwwnk",
    "kGGGGGGGGGGGGGGGGGGk",
    "knMMMnMMMMMnMMMMnMMk",
    "knMMMnMMMMMnMMMMnMMk",
    "kFFFFFFFFFFFFFFFFFFk",
    "knMMMnMMMMMnMMMMnMMk",
    "knMMMnMMMMMnMMMMnMMk",
    "knMMMnMMMMMnMMMMnMMk",
    "kGGGGGGGGGGGGGGGGGGk",
    "kmmmmmmmmmmmmmmmmmmk",
    ".kkkkkkkkkkkkkkkkkk.",
  ];

  // o fole de couro, de lado, encostado na fornalha
  const FOLE = [
    "..kkkkkkkkkkk.....",
    ".kNNNNNNNNNNNkk...",
    "kAZAAZAAZAAZAAAkkk",
    "kAAAAAAAAAAAAAAAFk",
    "kAZAAZAAZAAZAAAkkk",
    ".kNNNNNNNNNNNkk...",
    "..kkkkkkkkkkk.....",
  ];

  // ================================================================ A · a bancada de trabalho
  const A = { piso: 62, fx: 13, fy: 42, forno: -24, bigorna: 70, ferreiro: 128, quadro: 214, bancada: 212, porta: 288 };

  function baseA(W, d) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2), P = A.piso;
    // a parede de tábuas grossas e o madeiramento: fria longe do fogo, quente perto dele
    for (let y = 0; y < P; y++) for (let x = 0; x < W; x++) {
      const t = luz(x - ox, y, A.fx, A.fy, 175, 1.4);
      const tab = (x - ox + 400) % 23 === 0, veio = (x - ox + y * 3 + 400) % 31 === 0;
      const fria = tab ? PAL.p : veio ? "#211d1d" : "#26211f", quente = tab ? "#2c1810" : veio ? "#4a2c1c" : "#55331f";
      const meio = tab ? "#231713" : veio ? "#33241c" : "#3c2a1f";
      px(x, y, 1, 1, entre3(x, y, fria, meio, quente, Math.min(1, t * 1.3)));
    }
    // a viga de cima e os esteios
    for (let x = 0; x < W; x++) { const t = luz(x - ox, 8, A.fx, A.fy, 190, 1.4); px(x, 6, 1, 1, K); px(x, 7, 1, 3, entre(x, 7, PAL.M, PAL.N, t)); px(x, 10, 1, 1, K); }
    [196, 272].forEach((sx) => { for (let y = 10; y < P; y++) { const t = luz(sx, y, A.fx, A.fy, 190, 1.4); px(ox + sx, y, 1, 1, K); px(ox + sx + 1, y, 5, 1, entre(ox + sx, y, PAL.m, PAL.n, t)); px(ox + sx + 6, y, 1, 1, K); } });
    // o chão de terra batida, com a luz do fogo espalhada na frente da fornalha
    for (let y = P; y < QH; y++) for (let x = 0; x < W; x++) {
      const t = luz(x - ox, y, A.fx, A.fy + 6, 150, 2.2);
      px(x, y, 1, 1, entre3(x, y, (x + y * 2) % 13 === 0 ? "#100e0c" : "#191511", "#2c1f15", (x + y) % 11 === 0 ? "#3a2416" : "#4a2e1a", Math.min(1, t * 1.4)));
    }
    px(0, P, W, 1, K);
    // a fornalha, o fole e o carvão no chão
    fornalhaA(px, ox + A.forno, P);
    grade(px, ox + 50, 50, FOLE, PAL);
    // as ferramentas na parede, a bancada com o elmo e a espada, a tina de têmpera
    grade(px, ox + A.quadro, 16, FERRAMENTAS, PAL);
    bancadaA(px, ox + A.bancada, P);
    portaA(px, ox + A.porta, P);
    return { canvas: k, ox, d };
  }

  function bancadaA(px, x0, P) {
    // o tampo grosso e as pernas
    px(x0 - 1, 41, 62, 1, K); px(x0, 42, 60, 2, PAL.N); px(x0, 44, 60, 1, PAL.M); px(x0 - 1, 45, 62, 1, K);
    [[2, 4], [52, 4]].forEach(([dx, w]) => { px(x0 + dx, 46, w, P - 46, PAL.m); px(x0 + dx - 1, 46, 1, P - 46, K); px(x0 + dx + w, 46, 1, P - 46, K); });
    // a espada sem cabo, deitada, e o elmo em conserto
    px(x0 + 6, 39, 30, 1, K); px(x0 + 6, 40, 30, 1, PAL.H); px(x0 + 36, 40, 2, 1, PAL.G); px(x0 + 6, 41, 30, 1, PAL.F);
    grade(px, x0 + 40, 30, [
      "...kkkkkkk...",
      "..kGHHHHGGk..",
      ".kGHIHHGGGFk.",
      ".kGHHGGGGFFk.",
      "kGHHGkkkkGFFk",
      "kGHGk.....kFk",
      "kGGGkkkkkkFFk",
      "kGGFFFFFFFFFk",
      ".kkkkkkkkkkk.",
      "..kFFFFFFFk..",
      "..kkkkkkkkk..",
    ], PAL);
  }

  function portaA(px, x0, P) {
    // o batente e a porta entreaberta: a fresta com a luz fria do dia
    px(x0 - 2, 12, 34, 2, K); px(x0 - 1, 13, 32, 2, PAL.n);
    px(x0 - 2, 14, 2, P - 14, K); px(x0, 14, 3, P - 14, PAL.M);
    for (let y = 15; y < P; y++) for (let x = 3; x < 12; x++) px(x0 + x, y, 1, 1, entre(x0 + x, y, PAL.d, PAL.D, (12 - x) / 12));
    for (let y = 15; y < P; y++) for (let x = 12; x < 30; x++) {
      const tab = (x - 12) % 6 === 0;
      px(x0 + x, y, 1, 1, tab ? PAL.m : PAL.M);
    }
    px(x0 + 12, 15, 1, P - 15, K); px(x0 + 13, 22, 16, 2, PAL.F); px(x0 + 13, 46, 16, 2, PAL.F);  // as dobradiças
    px(x0 + 15, 34, 2, 3, PAL.G);  // o puxador
    // a luz fria entrando pelo chão
    for (let y = P; y < QH; y++) for (let x = -6; x < 14; x++) if (pont(x0 + x, y, 6 - Math.floor((y - P) / 2))) px(x0 + x, y, 1, 1, PAL.W);
  }

  function desenharA(c, W, b, est, quadro, destaque) {
    const px = pincel(c), ox = b.ox, P = A.piso, quieto = reduzido(), k = quieto ? 1 : Math.floor(quadro / 3) % 3;
    c.drawImage(b.canvas, 0, 0);
    fogoA(px, ox + A.forno, k);
    // o brilho na boca da fornalha (a luz pulsando devagar)
    const brilho = quieto ? 0 : (k === 1 ? 1 : 0);
    for (let y = 26; y < 31; y++) for (let x = 14; x < 62; x++) if (pont(ox + x, y, 3 + brilho * 2)) px(ox + A.forno + x, y, 1, 1, PAL.r);
    // a bigorna, a barra em brasa e o ferreiro atrás dela
    grade(px, ox + A.ferreiro, P - 57, FERREIRO_A, PAL);
    grade(px, ox + A.bigorna, P - 22, BIGORNA_A, PAL);
    // a barra em brasa deitada na mesa e a tenaz, da mão esquerda dele até ela
    const by = P - 23, bx = ox + A.bigorna + 26;
    px(bx - 1, by - 1, 24, 1, K); px(bx, by, 22, 1, PAL.y); px(bx - 1, by, 1, 1, PAL.R); px(bx + 22, by, 2, 1, PAL.R);
    px(bx + 20, by - 3, 14, 1, K); px(bx + 21, by - 2, 13, 1, PAL.G);
    px(bx + 20, by + 1, 14, 1, K); px(bx + 22, by + 1, 12, 1, PAL.F);
    // o contorno dos pontos acesos (mouse, foco do teclado)
    if (destaque) cantos(px, A_PONTOS[destaque].area);
  }

  // ================================================================ B · o interior da oficina
  const B = { piso: 46, fx: 160, fy: 34, forno: 130, porta: 14, armazem: 214 };
  function baseB(W, d) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2), P = B.piso;
    // a parede do fundo, de pedra: a luz quente perto da fornalha e da bigorna, o frio do resto
    for (let y = 0; y < P; y++) for (let x = 0; x < W; x++) {
      const t = luz(x - ox, y, B.fx, B.fy, 130, 1.2);
      const fiada = Math.floor(y / 5), junta = y % 5 === 4 || (x - ox + (fiada % 2) * 6 + 400) % 12 === 0;
      px(x, y, 1, 1, entre3(x, y, junta ? PAL.p : PAL.P, junta ? "#241814" : "#3a2a26", junta ? "#2e1a14" : "#4a2a1c", Math.min(1, t * 1.25)));
    }
    // o telhado: os caibros inclinados e a linha da cumeeira
    for (let x = 0; x < W; x++) { px(x, 0, 1, 3, K); px(x, 3, 1, 1, PAL.M); }
    for (let r = -2; r < 12; r++) { const x0 = ox + r * 32; for (let y = 0; y < 10; y++) { px(x0 + y * 2, y, 3, 1, K); px(x0 + y * 2 + 1, y, 1, 1, PAL.M); } }
    // o chão em perspectiva: tábuas que fogem para o fundo
    for (let y = P; y < QH; y++) for (let x = 0; x < W; x++) {
      const prof = (y - P) / (QH - P), cx = x - ox - 160, linha = Math.round(cx / (8 + prof * 10));
      const borda = Math.abs(cx - linha * (8 + prof * 10)) < 0.6;
      const t = luz(x - ox, y, B.fx, P + 4, 120, 2.6);
      px(x, y, 1, 1, borda ? K : entre3(x, y, prof > 0.5 ? "#1a1612" : "#14110e", prof > 0.5 ? "#33241a" : "#2a1e15", prof > 0.5 ? "#4e321e" : "#3e2818", Math.min(1, t * 1.3)));
    }
    px(0, P, W, 1, K);
    fornalhaB(px, ox + B.forno, P);
    grade(px, ox + B.forno + 60, P - 9, FOLE, PAL, true);
    armazemB(px, ox + B.armazem, P);
    portaB(px, ox + B.porta, P);
    // a tina de têmpera na frente, cortada pela borda de baixo
    grade(px, ox + 66, QH - 9, TINA.slice(0, 9), PAL);
    return { canvas: k, ox, d };
  }

  function fornalhaB(px, x0, P) {
    // a chaminé de pedra subindo ao telhado, a coifa e a boca
    for (let y = 0; y < 22; y++) for (let x = 12; x < 48; x++) px(x0 + x, y, 1, 1, x === 12 || x === 47 ? K : (x + Math.floor(y / 4) * 3) % 9 === 0 || y % 4 === 3 ? PAL.p : x < 18 ? PAL.q : PAL.P);
    for (let y = 22; y < 28; y++) { const meia = 18 + (y - 22) * 3; for (let x = -meia; x <= meia; x++) px(x0 + 30 + x, y, 1, 1, Math.abs(x) >= meia - 1 ? K : x < -meia + 3 ? PAL.G : PAL.F); }
    for (let y = 28; y < P; y++) for (let x = 2; x < 58; x++) {
      const junta = (y - 28) % 3 === 2 || (x + ((y - 28) / 3 % 2 ? 3 : 0)) % 7 === 0;
      px(x0 + x, y, 1, 1, junta ? PAL.t : x < 6 ? PAL.v : PAL.u);
    }
    px(x0 + 1, 28, 1, P - 28, K); px(x0 + 58, 28, 1, P - 28, K);
    for (let y = 31; y < 42; y++) { const meia = y < 33 ? 14 - (33 - y) * 2 : 16; for (let x = -meia; x <= meia; x++) px(x0 + 30 + x, y, 1, 1, Math.abs(x) >= meia - 1 ? K : PAL.o); }
    px(x0 + 10, 42, 41, 2, PAL.q); px(x0 + 10, 42, 41, 1, PAL.G);
  }
  function fogoB(px, x0, k) {
    const leito = 39;
    for (let x = 16; x < 45; x++) { const v = (x * 7 + k * 5) % 9; px(x0 + x, leito + 1, 1, 2, v < 3 ? PAL.R : PAL.r); px(x0 + x, leito, 1, 1, v < 2 ? PAL.y : PAL.R); }
    [[22, 6], [30, 8], [38, 6]].forEach(([cx, alt], i) => {
      const h = alt - ((k + i) % 3);
      for (let y = 0; y < h; y++) { const w = Math.max(1, Math.round((1 - y / h) * 3)); px(x0 + cx - Math.floor(w / 2) + ((y + k) % 2), leito - y, w, 1, y < h * 0.4 ? PAL.y : PAL.R); }
    });
  }

  // o ferreiro de B: menor (o meio da sala), de perfil para a esquerda, o martelo descendo na bigorna
  const FERREIRO_B = [
    ".......kkkkk........",
    "......kbbbbbk.......",
    ".....kbbbBbbbk......",
    ".....kTLSSSSbk......",
    ".....kLkLSSSSk......",
    "....kTLLSSSSk.......",
    ".....kLBSSSSk.......",
    ".....kBBBBSk........",
    "......kBBBk.........",
    "....kkkLSSkkkk......",
    "...kTLLSSSSSSSk.....",
    "..kTLZAAAAASSSSk....",
    ".kTLkZAAAAAASSSk....",
    ".kLk.kZAAAAAAASk....",
    "kTLk.kZAAAAAAASk....",
    "kLLk.kZAAAAAAAk.....",
    "kLSk.kZAAAAAAAk.....",
    "kkkk.kZAAAAAAAk.....",
    ".....kZAAAAAAAk.....",
    ".....kZAAAAAAAk.....",
    ".....kZAAAAAAAk.....",
    ".....kZAAAAAAAk.....",
    ".....kZAAAAAAAk.....",
    ".....kZAAAAAAAk.....",
    ".....kZAAAAAAAk.....",
    ".....kkZAAAAAkk.....",
    "......kcCkcCCk......",
    "......kcCkcCCk......",
    "......kcCkcCCk......",
    "......kcCkcCCk......",
    "......kcCkcCCk......",
    ".....kMMMkMMMMk.....",
    ".....kkkkkkkkkk.....",
  ];

  const BIGORNA_B = [
    "......kkkkkkkkkkkkkkkkkkkkkkk..",
    "kkkkkkkIIHHHHHHHHHHHHHHHHHHHGk.",
    ".kHHHHHGGGGGGGGGGGGGGGGGGGGGFk.",
    "..kkkGGGGFFFFFFFFFFFFFFFFFFFFk.",
    ".....kkkkkFFFFFFFFFFFFFFFFFfkk.",
    "..........kfFFFFFFFFFFFFFfk....",
    "..........kfFFFFFFFFFFFFFfk....",
    ".........kfGGFFFFFFFFFFFFFfk...",
    "........kkkkkkkkkkkkkkkkkkkkk..",
    ".........kNNNNNNNNNNNNNNNNNNk..",
    ".........knMMnMMMMMnMMMMMnMMk..",
    ".........knMMnMMMMMnMMMMMnMMk..",
    ".........kmmmmmmmmmmmmmmmmmmk..",
  ];

  function armazemB(px, x0, P) {
    // o suporte de armas encostado na parede: as lâminas e as lanças em pé
    px(x0, 20, 46, 2, K); px(x0 + 1, 20, 44, 1, PAL.n);
    px(x0, 40, 46, 3, K); px(x0 + 1, 41, 44, 1, PAL.n);
    for (let i = 0; i < 6; i++) {
      const x = x0 + 4 + i * 7, topo = 10 + (i % 3) * 3;
      px(x - 1, topo, 3, 31 - (topo - 10), K); px(x, topo + 1, 1, 29 - (topo - 10), i % 2 ? PAL.H : PAL.G);
      if (i % 2) { px(x - 2, 30, 5, 1, K); px(x - 1, 30, 3, 1, PAL.N); }  // a guarda das espadas
      else { px(x - 1, topo - 2, 3, 3, K); px(x, topo - 2, 1, 2, PAL.H); }  // a ponta das lanças
    }
    // o peitoral num cavalete, ao lado
    grade(px, x0 + 50, 18, [
      "..kkkkkkkkk..",
      ".kGHHGGGGFFk.",
      "kGHIHGGGGFFFk",
      "kGHHGGGGGFFFk",
      "kGHGGGGGGGFFk",
      ".kGGGGGGGGFk.",
      ".kGGGGGGGFFk.",
      "..kGGGGGFFk..",
      "..kkkkkkkkk..",
      ".....kNk.....",
      ".....kNk.....",
      ".....kNk.....",
      ".....kNk.....",
      ".....kNk.....",
      ".....kNk.....",
      ".....kNk.....",
      "...kkkNkkk...",
      "...kNNNNNk...",
    ], PAL);
    // os barris e os caixotes na frente, no chão
    for (const [dx, dy] of [[2, P + 2], [16, P + 4]]) {
      grade(px, x0 + dx, dy, [
        ".kkkkkkkkkk.",
        "kMNNNNNNNNMk",
        "kFFFFFFFFFFk",
        "kMnMMnMMnMMk",
        "kMnMMnMMnMMk",
        "kFFFFFFFFFFk",
        "kMnMMnMMnMMk",
        "kMnMMnMMnMMk",
        "kFFFFFFFFFFk",
        "kmmmmmmmmmmk",
        ".kkkkkkkkkk.",
      ], PAL);
    }
  }
  function portaB(px, x0, P) {
    // a porta do fundo aberta para a rua: o dia frio e claro, o batente de madeira
    px(x0 - 2, 14, 30, 2, K); px(x0 - 1, 15, 28, 1, PAL.n);
    for (let y = 16; y < P; y++) for (let x = 0; x < 26; x++) px(x0 + x, y, 1, 1, x < 2 || x > 23 ? PAL.M : entre(x0 + x, y, PAL.D, PAL.e, (P - y) / (P - 16) * 0.6));
    px(x0 - 2, 16, 2, P - 16, K); px(x0 + 26, 16, 2, P - 16, K);
    // a folha aberta, para dentro, à direita do batente
    for (let y = 18; y < P; y++) px(x0 + 28, y, 6, 1, y % 7 === 0 ? PAL.m : PAL.M);
    px(x0 + 34, 18, 1, P - 18, K);
    // o rastro de luz fria no chão, entrando
    for (let y = P; y < QH; y++) for (let x = -4; x < 60; x++) {
      const t = 1 - (y - P) / (QH - P);
      if (x > -2 + (y - P) * 0.3 && x < 26 + (y - P) * 1.2 && pont(x0 + x, y, Math.round(t * 7))) px(x0 + x, y, 1, 1, PAL.d);
    }
  }

  function desenharB(c, W, b, est, quadro, destaque) {
    const px = pincel(c), ox = b.ox, P = B.piso, quieto = reduzido(), k = quieto ? 1 : Math.floor(quadro / 3) % 3;
    c.drawImage(b.canvas, 0, 0);
    fogoB(px, ox + B.forno, k);
    // a bigorna no meio da sala e o ferreiro à direita dela, o martelo descendo
    const bx = 112, fx = 144;
    grade(px, ox + bx, P + 3, BIGORNA_B, PAL);
    grade(px, ox + fx, P - 18, FERREIRO_B, PAL);
    // a barra em brasa na mesa e o martelo descendo nela, do punho dele
    px(ox + bx + 10, P + 2, 14, 1, PAL.y); px(ox + bx + 9, P + 2, 1, 1, PAL.R); px(ox + bx + 24, P + 2, 1, 1, PAL.R);
    px(ox + fx - 8, P - 2, 9, 1, K); px(ox + fx - 8, P - 1, 9, 1, PAL.M); px(ox + fx - 8, P, 9, 1, K);
    px(ox + fx - 14, P - 4, 7, 6, K); px(ox + fx - 13, P - 3, 5, 4, PAL.G); px(ox + fx - 13, P - 3, 5, 1, PAL.H);
    if (destaque) cantos(px, B_PONTOS[destaque].area);
  }

  // ---------------------------------------------------------------- os pontos e o contorno aceso
  const OURO = "#ffd070";
  function cantos(px, [x, y, w, h]) {
    const L = 4, x1 = x + w - 1, y1 = Math.min(QH - 1, y + h - 1);
    [[K, 1], [OURO, 0]].forEach(([cor, d]) => {
      [[x, y, 1, 1], [x1, y, -1, 1], [x, y1, 1, -1], [x1, y1, -1, -1]].forEach(([cx, cy, sx, sy]) => {
        for (let i = 0; i < L; i++) { px(cx + sx * i + d * sx, cy + d * sy, 1, 1, cor); px(cx + d * sx, cy + sy * i + d * sy, 1, 1, cor); }
      });
    });
  }
  const A_PONTOS = {
    ferreiro: { area: [74, 2, 96, 60], balao: [176, 24], foco: [138, 34] },
    saida: { area: [286, 12, 32, 52], balao: [302, 26], foco: [300, 38] },
  };
  const B_PONTOS = {
    ferreiro: { area: [108, 26, 62, 36], balao: [151, 27], foco: [144, 46] },
    saida: { area: [10, 14, 38, 34], balao: [27, 28], foco: [27, 32] },
  };

  return {
    a: { base: baseA, desenhar: desenharA, pontos: A_PONTOS },
    b: { base: baseB, desenhar: desenharB, pontos: B_PONTOS },
    QW, QH,
  };
})();
