/* A forja do Vau, a B refinada (R): a candidata (protótipo, 25/10/2026; nada no jogo). A profundidade da B (a porta à
   esquerda, a fornalha ao fundo, o armazém à direita) com a oficina reconstruída por zonas e o ferreiro trabalhando
   numa espada, sem parar. A e B (forja-arte.js) ficam como histórico.

   O ferreiro: gordo e forte, quase de perfil para a esquerda e um pouco de costas, a barriga e o avental com volume, o
   cabelo à vista e a barba grande recortada contra o fogo. O corpo é uma grade desenhada à mão; o braço do martelo sai
   de juntas por pose (ombro, cotovelo, punho), com o contorno e a luz do fogo de um lado; o martelo e a tenaz em pixels
   inteiros, sem borrão. O ciclo: assentado na lâmina → sobe em dois tempos → segura no alto (2 a 4 quadros, variando)
   → desce num quadro (o rastro do martelo, nítido) → o golpe (o tronco afunda 1 px, faíscas do ponto de contato) → o
   rebote → assenta; depois de quatro golpes, uma pausa em que a tenaz vira a espada. O relógio é o das cenas (o quadro
   da vista, 10 por segundo): sair e entrar não cria outro. Com movimento reduzido: a pose do alto, parada, sem faíscas.

   Exporta window.ForjaArte.r = { base, desenhar, pontos, poseDe, POSES } (o formato das cenas da capela). */
"use strict";

(() => {
  const QW = 320, QH = 72;
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const pont = (x, y, n) => BAYER[(y & 3) * 4 + (x & 3)] < n;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const camada = (W) => { const k = document.createElement("canvas"); k.width = W; k.height = QH; return k; };
  const pincel = (c) => (x, y, w = 1, h = 1, cor) => { if (!cor) return; c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, h); };
  function grade(px, x0, y0, linhas, pal) {
    linhas.forEach((l, y) => [...l].forEach((ch, x) => { if (pal[ch]) px(x0 + x, y0 + y, 1, 1, pal[ch]); }));
  }
  const luz = (x, y, fx, fy, raio, ach = 1) => Math.max(0, 1 - Math.hypot(x - fx, (y - fy) * ach) / raio);
  const entre = (x, y, a, b, t) => (pont(x, y, Math.round(t * 16)) ? b : a);
  const entre3 = (x, y, a, m, b, t) => (t < 0.5 ? entre(x, y, a, m, t * 2) : entre(x, y, m, b, (t - 0.5) * 2));

  const K = "#0a090b";
  const C = {
    // ferro
    f: "#1d1f24", F: "#383b43", G: "#5c606a", H: "#9a9ea8", I: "#d4d8de",
    // madeira
    m: "#231811", M: "#3e2b1c", n: "#5a3f28", N: "#7a5836",
    // fogo e brasa
    o: "#4a1208", O: "#962a0c", r: "#d8541a", R: "#ff9430", y: "#ffcf6a", Y: "#fff0bc",
    // pedra, tijolo, fuligem
    p: "#17171b", P: "#25252c", q: "#34343c", Q: "#45444c", t: "#3a1e16", u: "#5a2e1e", v: "#7a4026", z: "#0f0e10",
    // água e o dia
    w: "#0b141b", W: "#1d3040", d: "#3e566a", D: "#7c96a8", e: "#b6c8d2",
  };
  // o ferreiro: o cabelo, a barba, a pele, a camisa, o avental, a calça e as botas (a luz do fogo vem de trás e da
  // esquerda: o contorno da frente aceso; as costas, viradas para quem olha, na sombra)
  const PF = {
    k: K,
    "1": "#3a3634", "2": "#6a625c", "3": "#3e2010", "4": "#6e3a1c", "5": "#a8642e", "6": "#d08a4c",
    s: "#5a3222", S: "#8a5034", L: "#c07a4c", T: "#e8a874",
    c: "#2a2622", C: "#3e3730", D: "#6a5a46",
    a: "#22150d", A: "#3a2414", B: "#54341c", Z: "#8a5a30", x: "#140c08",
    j: "#1c1b22", J: "#2c2b34",
    b: "#140e0b", g: "#2e221a",
  };

  // ---------------------------------------------------------------- o corpo do ferreiro (à mão)
  // Quase de perfil para a esquerda, um pouco de costas: a cabeça com o cabelo grisalho atrás, a orelha, a bochecha
  // acesa e a barba grande descendo pelo peito; os ombros largos curvados, as costas da camisa, a barriga projetada com
  // o avental (o contorno aceso pelo fogo) e o laço dele nas costas; as pernas abertas, firmes no chão.
  // A cabeça e a barba (CABECA, linhas 0–17) e o tronco (TRONCO) mexem separados das pernas (PERNAS), que não saem do
  // lugar. O braço do martelo é desenhado por pose, por cima; o braço da tenaz sai da frente da barriga.
  const CABECA = [
    "......kkkkk.....",
    "....kk22212kk...",
    "...k2221111111k.",
    "..k21111111111k.",
    "..kSSL11111111k.",
    ".kSLLTs1111111k.",
    "kSLkTLS1s11111k.",
    "kTLLLLSssS1111k.",
    "kkTLLLSsSs111k..",
    ".kTLLSSs1111k...",
    "k55LSSs11kk.....",
    "k6655Ss1k.......",
    "k66555s4k.......",
    "k665554443k.....",
    "k66555444k......",
    ".k6655444k......",
    ".k6655443k......",
    "..k665443k......",
    "..k66544k.......",
    "...k6544k.......",
    "....k54k........",
    ".....kk.........",
  ];
  const TRONCO = [
    "..............kccCCkkk......",
    "............kcccCCCCCCkk....",
    "..........kkccccCCCCCCCDk...",
    ".........kBxcccccCCCCCCCDk..",
    "........kZBxccccccccCCCCCDk.",
    ".......kZBBAxccccccccCCCCCk.",
    "......kZBBAAxcccccccccCCCCk.",
    ".....kZBBAAAAxccccccccCCCCk.",
    "....kZBBAAaAAxccccccccCCCk..",
    "...kZBBAAAaAAAxcccccccCCCk..",
    "..kZBBAAAAaAAAAxccccccCCCk..",
    ".kZBBAAAAAaAAAAxxxxxxxxxxk..",
    ".kZBBAAAAaAAAAAAkjjjjjjJJk..",
    "kZBBAAAAAaAAAAAAkjjjjjjJJk..",
    "kZBBAAAAAAaAAAAAkjjjjjjJJk..",
    "kZBBAAAAAAaAAAAkjjjjjjjJk...",
    ".kZBBAAAAAAAAAkjjjjjjjjJk...",
    "..kZBBAAAAAAAkjjjjjjjjJJk...",
    "...kkZBAAAAkkjjjjjjjjJJk....",
  ];
  const PERNAS = [
    ".....kkkkkkkkjjjjkjjjjJJk...",
    ".........kjjjjjjk..kjjjJJk..",
    "........kjjjjjjk...kjjjJJk..",
    ".......kjjjjjjk.....kjjJJk..",
    "......kjjjjjjk......kjjJJk..",
    ".....kjjjjjjk.......kjjJJk..",
    ".....kjjjjjk........kjjJJk..",
    "....kbbbbbbk........kbbbggk.",
    "...kbbbbbbbk.......kbbbbbggk",
    "...kkkkkkkkk.......kkkkkkkkk",
  ];
  const Y_TRONCO = 13, Y_PERNAS = 31;  // onde começam, na figura (a cabeça de 0 a 19, sobreposta ao alto do tronco)
  const OMBRO = [20, 15];             // o ombro do braço do martelo, na figura
  const MAO_TENAZ = [-2, 23];          // a mão da tenaz, saindo da frente da barriga

  // ---------------------------------------------------------------- as poses do braço e do martelo
  // Em coordenadas da figura: o cotovelo e o punho; o martelo pelo ângulo do cabo (graus; 0 aponta para a direita,
  // 90 para baixo) e o comprimento. `tronco`/`cabeca`/`barba`: quanto descem (o peso do golpe). O ponto de contato
  // (a face de baixo do martelo encostando na lâmina) é o mesmo no golpe e no repouso.
  const POSES = {
    repouso: { cotovelo: [10, 22], punho: [-1, 25], angulo: 186, tronco: 0, cabeca: 0 },
    sobe1: { cotovelo: [19, 22], punho: [20, 17], angulo: 300, tronco: 0, cabeca: 0 },
    sobe2: { cotovelo: [22, 14], punho: [18, 8], angulo: 290, tronco: 0, cabeca: 0 },
    alto: { cotovelo: [24, 11], punho: [20, 3], angulo: 322, tronco: -1, cabeca: -1 },
    desce: { cotovelo: [15, 15], punho: [5, 19], angulo: 208, tronco: 0, cabeca: 0, rastro: true },
    golpe: { cotovelo: [10, 22], punho: [-1, 25], angulo: 186, tronco: 1, cabeca: 1, golpe: true },
    volta: { cotovelo: [10, 20], punho: [-1, 22], angulo: 190, tronco: 1, cabeca: 0 },
    ajuste: { cotovelo: [11, 21], punho: [1, 24], angulo: 182, tronco: 0, cabeca: 0, vira: true },
  };
  const CONTATO = [-10, 26];  // onde a face do martelo encosta na lâmina, na figura
  // A linha do tempo, em quadros de 100 ms: quatro golpes com o alto e o repouso variando, e a pausa da tenaz. O último
  // quadro (repouso) emenda no primeiro sem salto.
  const GOLPE = (alto, repouso) => [["sobe1", 1], ["sobe2", 1], ["alto", alto], ["desce", 1], ["golpe", 1], ["volta", 1], ["repouso", repouso]];
  const CICLO = [
    ["repouso", 3],
    ...GOLPE(3, 2), ...GOLPE(2, 2), ...GOLPE(3, 1), ...GOLPE(4, 3),
    ["ajuste", 6], ["repouso", 4],
  ];
  const DURACAO = CICLO.reduce((n, [, d]) => n + d, 0);
  /** A pose no quadro q: { nome, t (o quadro dentro dela), golpe (o índice do golpe, para as faíscas variarem) }. */
  function poseDe(q) {
    let r = ((q % DURACAO) + DURACAO) % DURACAO, golpes = 0;
    for (const [nome, d] of CICLO) {
      if (r < d) return { nome, t: r, golpe: golpes, volta: Math.floor(q / DURACAO) };
      if (nome === "golpe") golpes++;
      r -= d;
    }
    return { nome: "repouso", t: 0, golpe: 0, volta: 0 };
  }

  /** Um segmento grosso (o braço): os pixels a até `raio` da linha, com o contorno de 1 px, o lado de cima e de trás
   *  (a luz do fogo) aceso e o de baixo na sombra. Tudo em pixels inteiros. */
  function membro(px, a, b, raio, cores) {
    const [ax, ay] = a, [bx, by] = b, dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1;
    const x0 = Math.floor(Math.min(ax, bx) - raio - 2), x1 = Math.ceil(Math.max(ax, bx) + raio + 2);
    const y0 = Math.floor(Math.min(ay, by) - raio - 2), y1 = Math.ceil(Math.max(ay, by) + raio + 2);
    const nx = -dy / Math.sqrt(l2), ny = dx / Math.sqrt(l2);  // a normal: um lado aceso, o outro na sombra
    const lado = nx * -1 + ny * -0.6 > 0 ? 1 : -1;            // o lado virado para a luz (alto e esquerda)
    const pinta = [];
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
      const t = Math.max(0, Math.min(1, ((x - ax) * dx + (y - ay) * dy) / l2));
      const qx = ax + t * dx, qy = ay + t * dy, d = Math.hypot(x - qx, y - qy);
      if (d <= raio) {
        const s = ((x - qx) * nx + (y - qy) * ny) * lado;
        pinta.push([x, y, s > raio * 0.35 ? cores.luz : s < -raio * 0.35 ? cores.sombra : cores.meio]);
      } else if (d <= raio + 1) pinta.push([x, y, K]);
    }
    pinta.filter((p) => p[2] === K).forEach(([x, y, c]) => px(x, y, 1, 1, c));
    pinta.filter((p) => p[2] !== K).forEach(([x, y, c]) => px(x, y, 1, 1, c));
  }
  /** O martelo: o cabo do punho até a cabeça, pixel a pixel, e a cabeça atravessada (5 × 3), a face de bater embaixo. */
  function martelo(px, mao, angulo) {
    const rad = (angulo * Math.PI) / 180, ux = Math.cos(rad), uy = Math.sin(rad);
    const fim = [mao[0] + ux * 8, mao[1] + uy * 8];
    // o cabo: o contorno e a madeira
    const passos = 9;
    for (let i = -1; i <= passos; i++) { const x = Math.round(mao[0] + ux * i), y = Math.round(mao[1] + uy * i); px(x - 1, y, 3, 1, K); px(x, y - 1, 1, 3, K); }
    for (let i = 0; i <= passos - 1; i++) { const x = Math.round(mao[0] + ux * i), y = Math.round(mao[1] + uy * i); px(x, y, 1, 1, i < 3 ? C.n : C.N); }
    // a cabeça: perpendicular ao cabo, no fim dele
    const vx = -uy, vy = ux, cx = fim[0] + ux * 1.5, cy = fim[1] + uy * 1.5;
    const cel = [];
    for (let a = -2.5; a <= 2.5; a += 0.5) for (let b = -1.5; b <= 1.5; b += 0.5) cel.push([Math.round(cx + vx * a + ux * b), Math.round(cy + vy * a + uy * b), a, b]);
    const vistos = new Set(cel.map(([x, y]) => `${x},${y}`));
    cel.forEach(([x, y]) => { for (const [ox, oy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) if (!vistos.has(`${x + ox},${y + oy}`)) px(x + ox, y + oy, 1, 1, K); });
    cel.forEach(([x, y, a, b]) => px(x, y, 1, 1, b < -0.6 ? C.H : a > 1.8 || a < -1.8 ? C.F : C.G));
    return { cabeca: [cx, cy], u: [ux, uy], v: [vx, vy] };
  }
  /** A tenaz: as duas hastes da mão até a espiga da espada, presas nela. */
  function tenaz(px, mao, ponta, aberto = 0) {
    const passos = Math.max(Math.abs(ponta[0] - mao[0]), Math.abs(ponta[1] - mao[1]));
    for (const off of [-1, 1]) for (let i = 0; i <= passos; i++) {
      const t = i / passos, x = Math.round(mao[0] + (ponta[0] - mao[0]) * t), y = Math.round(mao[1] + (ponta[1] - mao[1]) * t + off * (t > 0.7 ? 1 + aberto : 0));
      px(x, y, 1, 1, off < 0 ? C.G : C.F);
    }
  }

  // ---------------------------------------------------------------- a espada na bigorna
  /** A lâmina em fabricação: a ponta afinando à esquerda, o fio de cima com a luz, o sulco no meio, a espiga estreita
   *  à direita (sem guarda nem cabo ainda); o trecho batido em brasa, mais vivo logo depois do golpe. `virada`: na
   *  pausa, a tenaz a vira de lado (vê-se o fio, mais fino). */
  function espada(px, x0, y, comp, brasa, virada) {
    const quente = (x) => { const d = Math.abs(x - brasa.x); return d < 4 ? (brasa.forte ? C.Y : C.y) : d < 7 ? C.R : d < 10 ? C.r : d < 13 ? C.O : null; };
    for (let i = 0; i < comp; i++) {
      const x = x0 + i, ponta = i < 4, espiga = i > comp - 7;
      const alto = virada ? 1 : ponta ? (i < 2 ? 1 : 2) : espiga ? 1 : 3;
      px(x, y - alto, 1, 1, K);
      for (let k = 0; k < alto; k++) {
        const q = quente(x);
        const base = virada ? C.G : k === 0 ? C.H : k === 1 && !espiga ? C.F : C.G;
        px(x, y - alto + 1 + k, 1, 1, q && !espiga ? (k === 0 ? q : q === C.Y ? C.y : q === C.y ? C.R : q === C.R ? C.r : C.O) : base);
      }
      px(x, y + 1, 1, 1, K);
    }
    px(x0 - 1, y, 1, 1, K);
  }

  // ---------------------------------------------------------------- o ambiente
  const L = { piso: 46, fx: 176, fy: 34, porta: 10, forno: 146, bigorna: 108, ferreiro: 146, figY: 22 };

  function base(W, d) {
    const k = camada(W), c = k.getContext("2d"), px = pincel(c), ox = Math.round((W - QW) / 2), P = L.piso;
    // a parede do fundo: em cima, taipa e madeira (calma, escura); embaixo, pedra irregular; a luz quente da fornalha e
    // o frio que entra pela porta separam os planos
    for (let y = 0; y < P; y++) for (let x = 0; x < W; x++) {
      const lx = x - ox, t = luz(lx, y, L.fx, L.fy, 135, 1.15), fria = luz(lx, y, 24, 34, 70, 1.4);
      let cor;
      if (y < 21) cor = entre3(x, y, "#19171a", "#2a1f1b", "#43281b", Math.min(1, t * 1.1));
      else {
        // as pedras: fiadas de alturas diferentes e juntas desencontradas
        const fiada = y < 28 ? 0 : y < 36 ? 1 : 2, alt = [21, 28, 36][fiada], larg = [17, 13, 19][fiada];
        const junta = y === alt || (lx + fiada * 7 + 400 + ((Math.floor((lx + 400) / larg) * 5) % 3)) % larg === 0;
        cor = junta ? C.p : entre3(x, y, C.P, "#382a26", "#55301f", Math.min(1, t * 1.2));
      }
      if (fria > 0.25 && pont(x, y, Math.round(fria * 6))) cor = "#2a3644";
      px(x, y, 1, 1, cor);
    }
    // as vigas: a do alto e os dois esteios, de madeira escura, quebrando a parede
    for (let x = 0; x < W; x++) { px(x, 0, 1, 2, K); px(x, 2, 1, 1, C.m); px(x, 19, 1, 1, K); px(x, 20, 1, 1, entre(x, 20, C.m, C.n, luz(x - ox, 20, L.fx, L.fy, 140))); }
    [[96, 4], [236, 5]].forEach(([sx, w]) => { for (let y = 3; y < P; y++) { px(ox + sx - 1, y, 1, 1, K); px(ox + sx, y, w, 1, entre(ox + sx, y, C.m, C.M, luz(sx, y, L.fx, L.fy, 150))); px(ox + sx + w, y, 1, 1, K); } });
    // o chão de terra batida (sem tábuas): mais claro na luz da fornalha, com as lajes da boca do fogo e a cinza
    for (let y = P; y < QH; y++) for (let x = 0; x < W; x++) {
      const lx = x - ox, t = luz(lx, y, L.fx - 20, P + 6, 120, 2.2), fria = luz(lx, y, 26, P + 8, 60, 2);
      let cor = entre3(x, y, "#141110", "#261c15", "#43291a", Math.min(1, t * 1.25));
      if ((lx * 7 + y * 13) % 29 === 0) cor = "#0e0c0b";
      if (fria > 0.2 && pont(x, y, Math.round(fria * 7))) cor = C.W;
      px(x, y, 1, 1, cor);
    }
    px(0, P, W, 1, K);
    lajes(px, ox, P);
    porta(px, ox + L.porta, P);
    fornalha(px, ox + L.forno, P);
    zonaQuente(px, ox, P);
    armazem(px, ox, P);
    resfriamento(px, ox, P);
    restos(px, ox, P);
    return { canvas: k, ox, d };
  }

  function lajes(px, ox, P) {
    // as lajes de pedra na frente da fornalha, desiguais
    [[138, 48, 18, 3], [158, 47, 22, 3], [182, 48, 16, 3], [150, 52, 14, 2]].forEach(([x, y, w, h]) => {
      px(ox + x, y, w, h, "#2a2420"); px(ox + x, y, w, 1, "#4a3a2c"); px(ox + x, y + h, w, 1, K);
    });
  }

  function porta(px, x0, P) {
    px(x0 - 2, 12, 32, 2, K); px(x0 - 1, 13, 30, 1, C.n);
    for (let y = 14; y < P; y++) for (let x = 0; x < 26; x++) px(x0 + x, y, 1, 1, x < 2 || x > 23 ? C.M : entre(x0 + x, y, C.D, C.e, (P - y) / (P - 14) * 0.55));
    // a rua lá fora: a beira de uma casa e o chão claro
    px(x0 + 3, 20, 7, 18, "#5a6a76"); px(x0 + 3, 20, 7, 1, "#8a9aa6"); px(x0 + 4, 26, 2, 3, "#3e4a54");
    px(x0 + 2, P - 4, 22, 4, "#9aaab4");
    px(x0 - 2, 14, 2, P - 14, K); px(x0 + 26, 14, 2, P - 14, K);
    for (let y = 16; y < P; y++) px(x0 + 28, y, 5, 1, y % 6 === 0 ? C.m : C.M);
    px(x0 + 33, 16, 1, P - 16, K); px(x0 + 29, 24, 3, 2, C.F); px(x0 + 29, 38, 3, 2, C.F);
    // a luz fria entrando, um leque pelo chão
    for (let y = P; y < QH; y++) for (let x = -2; x < 64; x++) {
      const t = 1 - (y - P) / (QH - P);
      if (x > (y - P) * 0.2 && x < 26 + (y - P) * 1.3 && pont(x0 + x, y, Math.round(t * 8))) px(x0 + x, y, 1, 1, C.d);
    }
  }

  function fornalha(px, x0, P) {
    // a chaminé de pedra subindo ao telhado, com a fuligem escorrendo; a coifa de ferro; a boca e a soleira
    for (let y = 0; y < 22; y++) for (let x = 18; x < 44; x++) {
      const borda = x === 18 || x === 43, junta = (x + Math.floor(y / 4) * 3) % 8 === 0 || y % 4 === 3;
      const fuligem = pont(x0 + x, y, Math.max(0, 14 - Math.abs(x - 31) - Math.floor(y / 3)));
      px(x0 + x, y, 1, 1, borda ? K : fuligem ? C.z : junta ? C.p : x < 23 ? C.q : C.P);
    }
    for (let y = 20; y < 27; y++) { const meia = 15 + (y - 20) * 3; for (let x = -meia; x <= meia; x++) px(x0 + 31 + x, y, 1, 1, Math.abs(x) >= meia - 1 ? K : y === 26 ? C.G : x < -meia + 3 ? C.G : C.F); }
    for (let y = 27; y < P; y++) for (let x = 2; x < 62; x++) {
      const junta = (y - 27) % 3 === 2 || (x + ((y - 27) / 3 % 2 ? 3 : 0)) % 7 === 0;
      px(x0 + x, y, 1, 1, junta ? C.t : x < 6 ? C.v : C.u);
    }
    px(x0 + 1, 27, 1, P - 27, K); px(x0 + 62, 27, 1, P - 27, K);
    // a fuligem em volta da boca, no tijolo
    for (let y = 27; y < 31; y++) for (let x = 12; x < 52; x++) if (pont(x0 + x, y, 9 - (y - 27) * 2)) px(x0 + x, y, 1, 1, C.t);
    for (let y = 30; y < 42; y++) { const meia = y < 32 ? 15 - (32 - y) * 2 : 17; for (let x = -meia; x <= meia; x++) px(x0 + 32 + x, y, 1, 1, Math.abs(x) >= meia - 1 ? K : C.o); }
    px(x0 + 11, 42, 43, 2, C.Q); px(x0 + 11, 42, 43, 1, C.G);
  }
  function fogo(px, x0, k) {
    const leito = 39;
    for (let x = 17; x < 48; x++) { const v = (x * 7 + k * 5) % 9; px(x0 + x, leito + 1, 1, 2, v < 3 ? C.R : C.r); px(x0 + x, leito, 1, 1, v < 2 ? C.y : C.R); }
    [[22, 6], [29, 9], [36, 7], [43, 5]].forEach(([cx, alt], i) => {
      const h = alt - ((k + i) % 3);
      for (let y = 0; y < h; y++) { const w = Math.max(1, Math.round((1 - y / h) * 3)); px(x0 + cx - Math.floor(w / 2) + ((y + k + i) % 2), leito - y, w, 1, y < h * 0.4 ? C.y : C.R); }
    });
  }

  function zonaQuente(px, ox, P) {
    // o monte de carvão no chão, à direita da fornalha, com umas brasas
    const cx = ox + 214;
    for (let y = 0; y < 8; y++) { const meia = 12 - y; for (let x = -meia; x <= meia; x++) px(cx + x, P - 1 - y, 1, 1, Math.abs(x) === meia ? K : (x * 3 + y * 5) % 7 === 0 ? "#2e2e34" : "#141418"); }
    px(cx - 5, P - 3, 1, 1, C.r); px(cx + 4, P - 2, 1, 1, C.O); px(cx - 1, P - 6, 1, 1, C.O);
    // as duas tenazes penduradas no lado da fornalha: a de bico longo e a de bico chato, de tamanhos diferentes
    const tx = ox + 211;
    px(tx - 1, 20, 18, 1, K); px(tx, 21, 16, 1, C.n); px(tx - 1, 22, 18, 1, K);
    grade(px, tx, 23, [
      ".kk......kk.....",
      "kGFk....kGFk....",
      "kGFk....kGFk....",
      "kGFk....kGFk....",
      "kGFk....kGFk....",
      "kGFk...kGkGFk...",
      ".kGFk.kGk.kGFk..",
      ".kGFkkGk...kGk..",
      "..kGGGk....kGk..",
      "..kGFGk...kGGGk.",
      ".kGk.kGk..kFkFk.",
      "kGk...kGk.kFkFk.",
      "kk.....kk.kkkkk.",
    ], { k: K, G: C.G, F: C.F });
  }

  function armazem(px, ox, P) {
    const pal = { k: K, f: C.f, F: C.F, G: C.G, H: C.H, I: C.I, m: C.m, M: C.M, n: C.n, N: C.N, r: C.O };
    // o cabideiro de madeira na parede, com os ganchos; pendurados: a espada pronta, a lâmina por terminar (sem
    // guarda, mais escura), o machado e o martelo grande, cada um de um tamanho
    const x0 = ox + 244;
    px(x0 - 1, 9, 60, 1, K); px(x0, 10, 58, 2, C.n); px(x0, 12, 58, 1, C.m); px(x0 - 1, 13, 60, 1, K);
    [4, 16, 30, 44].forEach((g) => { px(x0 + g, 13, 1, 2, C.G); });
    grade(px, x0 + 2, 14, [
      "..kk..",
      ".kNNk.",
      ".kmNk.",
      ".kNNk.",
      "kkkkkk",
      "kGHHGk",
      ".kHGk.",
      ".kIGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      ".kHGk.",
      "..kk..",
    ], pal);
    grade(px, x0 + 14, 15, [
      ".kk.",
      ".kk.",
      "kFFk",
      "kGFk",
      "kGFk",
      "kGFk",
      "kGFk",
      "kGFk",
      "kGFk",
      "kGFk",
      "kGFk",
      "kGFk",
      ".kk.",
    ], pal);
    grade(px, x0 + 26, 14, [
      "...kk....",
      "..kNNk...",
      "kkkNNkkk.",
      "kHGkkGGFk",
      "kHGGGGFFk",
      "kGGkkFFFk",
      ".kk.kNk.k",
      "....kNk..",
      "....kNk..",
      "....kNk..",
      "....kNk..",
      "....kmk..",
      "....kkk..",
    ], pal);
    grade(px, x0 + 40, 14, [
      "..kk...",
      "kkkkkkk",
      "kGHHGFk",
      "kGGGFFk",
      "kkkNkkk",
      "...Nk..",
      "...Nk..",
      "...Nk..",
      "...mk..",
      "...kk..",
    ], pal);
    // a prateleira baixa com os lingotes (dois tamanhos)
    px(x0 + 30, 33, 28, 1, K); px(x0 + 30, 34, 28, 1, C.n); px(x0 + 30, 35, 28, 1, K);
    [[32, 6], [40, 8], [50, 5]].forEach(([dx, w]) => { px(x0 + dx, 30, w, 3, K); px(x0 + dx + 1, 31, w - 2, 1, C.G); px(x0 + dx + 1, 32, w - 2, 1, C.F); });
    // no chão: o feixe de barras (grossuras e comprimentos diferentes, as pontas quadradas à vista)
    const fx = ox + 240;
    [[0, 26, 3], [3, 22, 2], [1, 18, 4], [6, 24, 2], [2, 15, 3]].forEach(([dx, w, h], i) => {
      const y = P - 2 - i * 2 - Math.floor(h / 2);
      px(fx + dx - 1, y - 1, w + 2, h + 2, K); px(fx + dx, y, w, h, i % 2 ? C.F : C.G); px(fx + dx, y, w, 1, C.H);
      px(fx + dx + w - 2, y, 2, h, C.f);  // a ponta cortada
    });
    // o barril com um elmo por consertar em cima, as duas lâminas encostadas na parede (inclinadas diferente) e o escudo
    grade(px, ox + 272, P - 11, [
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
    ], pal);
    grade(px, ox + 273, P - 19, [
      "...kkkkk...",
      "..kGHHHGk..",
      ".kGHIHGGFk.",
      ".kGHHGGGFk.",
      "kGHGkkkkGFk",
      "kGGk...kFFk",
      "kGGFFFFFFFk",
      ".kkkkkkkkk.",
    ], pal);
    [[288, 0.35, 20], [295, 0.55, 17]].forEach(([bx, inc, n]) => {
      for (let i = 0; i < n; i++) { const x = ox + bx + Math.floor(i * inc), y = P - 1 - i; px(x - 1, y, 4, 1, K); px(x, y, 1, 1, C.G); px(x + 1, y, 1, 1, i > n - 4 ? C.F : C.H); }
    });
    grade(px, ox + 302, P - 15, [
      "....kkkkk....",
      "..kkMNNNMkk..",
      ".kMNMMMMMNMk.",
      ".kNMMFFFMMNk.",
      "kMNMFGGGFMNMk",
      "kMNMFGHGFMNMk",
      "kMNMFGGGFMNMk",
      ".kNMMFFFMMNk.",
      ".kMNMMMMMNMk.",
      "..kkMNNNMkk..",
      "....kkkkk....",
    ], pal);
  }

  function resfriamento(px, ox, P) {
    // a tina de têmpera (meio barril) com a água escura e o reflexo do fogo, perto da bigorna; o balde ao lado
    grade(px, ox + 66, P + 8, [
      "kkkkkkkkkkkkkkkkkkkk",
      "kNNNNNNNNNNNNNNNNNNk",
      "kWwwwwwwRwwwwwwwwWnk",
      "knwwwwwwwwwwwwwwwwnk",
      "kFFFFFFFFFFFFFFFFFFk",
      "knMMMnMMMMMnMMMMnMMk",
      "knMMMnMMMMMnMMMMnMMk",
      "knMMMnMMMMMnMMMMnMMk",
      "kFFFFFFFFFFFFFFFFFFk",
      "knMMMnMMMMMnMMMMnMMk",
      "knMMMnMMMMMnMMMMnMMk",
      "kmmmmmmmmmmmmmmmmmmk",
      ".kkkkkkkkkkkkkkkkkk.",
    ], { k: K, N: C.N, W: C.W, w: C.w, R: C.r, n: C.n, M: C.M, F: C.F, m: C.m });
    grade(px, ox + 52, P + 13, [
      ".kkkkkk.",
      "kGHHGGFk",
      "kFFFFFFk",
      "kFGFFGFk",
      "kFFFFFFk",
      ".kkkkkk.",
    ], { k: K, G: C.G, H: C.H, F: C.F });
  }

  function restos(px, ox, P) {
    // as sobras de ferro no chão perto da bigorna (umas lascas), a cinza na boca da fornalha
    [[100, 66], [104, 68], [134, 69], [92, 63]].forEach(([x, y]) => { px(ox + x, y, 2, 1, C.F); px(ox + x, y - 1, 1, 1, C.G); });
    for (let y = P + 1; y < P + 5; y++) for (let x = 150; x < 196; x++) if (pont(ox + x, y, 3)) px(ox + x, y, 1, 1, "#3a3634");
  }

  // a bigorna larga de perfil (o chifre para a esquerda), no toco; e os dois martelos encostados no toco (diferentes)
  const BIGORNA = [
    ".......kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
    "kkkkkkkIIHHHHHHHHHHHHHHHHHHHHHHHHHHHGk.",
    ".kHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFk.",
    "..kkkHGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFk.",
    ".....kkkkFFFFFFFFFFFFFFFFFFFFFFFFFFfkk.",
    "..........kfFFFFFFFFFFFFFFFFFFFFFfk....",
    "...........kfFFFFFFFFFFFFFFFFFFFfk.....",
    "...........kfFFFFFFFFFFFFFFFFFFFfk.....",
    "..........kfGGFFFFFFFFFFFFFFFFFFFfk....",
    ".........kkkkkkkkkkkkkkkkkkkkkkkkkkk...",
    "..........kNNNNNNNNNNNNNNNNNNNNNNNk....",
    "..........knMMMnMMMMMMMnMMMMMMMnMMk....",
    "..........knMMMnMMMMMMMnMMMMMMMnMMk....",
    "..........knMMMnMMMMMMMnMMMMMMMnMMk....",
    "..........kmmmmmmmmmmmmmmmmmmmmmmmk....",
  ];
  const MARTELOS = [
    "kkkkk.....",
    "kGHGk.kkk.",
    "kFGFk.kGk.",
    "kkMkk.kHk.",
    "..Mk..kMk.",
    "..Mk...Mk.",
    "..Mk...Mk.",
    "..Mk...Mk.",
    "..mk...mk.",
    "..kk...kk.",
  ];

  // ---------------------------------------------------------------- desenhar (a cada quadro)
  function desenhar(c, W, b, est, quadro, destaque) {
    const px = pincel(c), ox = b.ox, P = L.piso, quieto = reduzido();
    c.drawImage(b.canvas, 0, 0);
    const k = quieto ? 1 : Math.floor(quadro / 3) % 3;
    fogo(px, ox + L.forno, k);
    const pose = quieto ? { nome: "alto", t: 0, golpe: 0, volta: 0 } : poseDe(quadro);
    figura(px, ox, P, pose, quadro, quieto);
    if (destaque) cantos(px, PONTOS[destaque].area);
  }

  /** A bigorna, a espada, o ferreiro e as faíscas, na pose da vez. */
  function figura(px, ox, P, pose, quadro, quieto) {
    const p = POSES[pose.nome], fx = ox + L.ferreiro, fy = L.figY;
    const bx = fx - 44, topo = fy + 27;                        // a mesa da bigorna (a lâmina deita nela)
    grade(px, bx - 9, P + 12, MARTELOS, { k: K, G: C.G, H: C.H, F: C.F, M: C.N, m: C.m });
    grade(px, bx, topo, BIGORNA, { k: K, I: C.I, H: C.H, G: C.G, F: C.F, f: C.f, N: C.N, n: C.n, M: C.M, m: C.m });
    // a espada: o trecho batido perto do ponto de contato; mais vivo logo depois do golpe
    const contato = [fx + CONTATO[0], fy + CONTATO[1]];
    const forte = !quieto && (pose.nome === "golpe" || pose.nome === "volta");
    espada(px, fx - 46, topo - 1, 45, { x: contato[0] - 1, forte }, p.vira && pose.t >= 1 && pose.t < 5);
    // a tenaz: da mão da frente da barriga até a espiga, à direita
    const tr = p.tronco || 0;
    // o ferreiro: as pernas paradas no chão, o tronco e a cabeça descendo com o peso (a barba um quadro depois)
    grade(px, fx, fy + Y_PERNAS, PERNAS, PF);
    // na pausa (o ajuste), a mão da tenaz sobe 1 px e a lâmina vira de lado: ela gira a peça para o próximo golpe
    const virando = p.vira && pose.t >= 1 && pose.t < 5;
    const maoT = [fx + MAO_TENAZ[0], fy + MAO_TENAZ[1] + tr - (virando ? 1 : 0)];
    membro(px, [fx + 6, fy + 20 + tr], maoT, 2.0, { luz: PF.L, meio: PF.S, sombra: PF.s });
    tenaz(px, [maoT[0] - 1, maoT[1] + 1], [fx - 6, topo - 2 - (virando ? 1 : 0)], virando ? 1 : 0);
    grade(px, fx, fy + Y_TRONCO + tr, TRONCO, PF);
    const atras = pose.nome === "volta" ? 1 : p.cabeca || 0;
    grade(px, fx + 5, fy + atras, CABECA, PF);
    // o braço do martelo: o ombro, o cotovelo e o punho da pose
    const ombro = [fx + OMBRO[0], fy + OMBRO[1] + tr], cot = [fx + p.cotovelo[0], fy + p.cotovelo[1] + tr], pun = [fx + p.punho[0], fy + p.punho[1] + tr];
    if (p.rastro && !quieto) rastro(px, fx, fy);
    membro(px, ombro, cot, 2.9, { luz: PF.L, meio: PF.S, sombra: PF.s });
    membro(px, cot, pun, 2.4, { luz: PF.T, meio: PF.L, sombra: PF.S });
    // o martelo: na pose de contato, a face encosta na lâmina (calculado para não atravessar)
    const m = martelo(px, pun, p.angulo);
    px(pun[0] - 2, pun[1] - 2, 5, 5, K); px(pun[0] - 1, pun[1] - 1, 3, 3, PF.S); px(pun[0] - 1, pun[1] - 1, 3, 1, PF.T);  // o punho fechado no cabo
    if (p.golpe && !quieto) faiscas(px, contato, pose.golpe + pose.volta * 4, 0);
    if (pose.nome === "volta" && !quieto) faiscas(px, contato, pose.golpe - 1 + pose.volta * 4, 1);
    if (pose.nome === "repouso" && pose.t === 0 && !quieto) faiscas(px, contato, pose.golpe - 1 + pose.volta * 4, 2);
    return m;
  }

  /** O rastro da descida: dois arcos nítidos de 1 px no caminho da cabeça do martelo, do alto até o golpe. */
  function rastro(px, fx, fy) {
    const pts = [[26, -4], [21, -4], [15, -2], [9, 2], [3, 7], [-2, 12], [-6, 17], [-9, 21]];
    pts.forEach(([x, y], i) => { px(fx + x, fy + y, 2, 1, i < 3 ? "#5a5e68" : "#8a8e98"); });
  }
  /** As faíscas: nascem do ponto de contato no golpe e se abrem por dois quadros (riscos curtos, do branco ao laranja).
   *  As direções variam de golpe para golpe, sempre as mesmas para o mesmo golpe. */
  function faiscas(px, [x, y], semente, idade) {
    let s = (semente * 9301 + 49297) % 233280 || 7;
    const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const n = 9;
    for (let i = 0; i < n; i++) {
      const ang = Math.PI * (1.05 + rnd() * 0.9), vel = 2.5 + rnd() * 4.5, sobe = -1.2 - rnd() * 1.5;
      const d = idade * vel + 1.5, qx = x + Math.cos(ang) * d * (rnd() < 0.5 ? 1 : -0.6), qy = y + Math.sin(ang) * d * 0.55 + (idade * idade) * 0.8 + sobe * (idade > 0 ? 0.5 : 0);
      if (idade === 2 && i % 2) continue;
      const cor = idade === 0 ? C.Y : idade === 1 ? C.y : C.R;
      px(qx, qy, 1, 1, cor);
      if (idade > 0) px(qx + (qx > x ? -1 : 1), qy + 0.5, 1, 1, idade === 1 ? C.R : C.r);
    }
    if (idade === 0) { px(x - 1, y - 1, 3, 1, C.Y); px(x, y - 2, 1, 1, C.Y); }  // o clarão no ponto do golpe
  }

  // ---------------------------------------------------------------- os pontos
  const OURO = "#ffd070";
  function cantos(px, [x, y, w, h]) {
    const Lc = 4, x1 = x + w - 1, y1 = Math.min(QH - 1, y + h - 1);
    [[K, 1], [OURO, 0]].forEach(([cor, d]) => {
      [[x, y, 1, 1], [x1, y, -1, 1], [x, y1, 1, -1], [x1, y1, -1, -1]].forEach(([cx, cy, sx, sy]) => {
        for (let i = 0; i < Lc; i++) { px(cx + sx * i + d * sx, cy + d * sy, 1, 1, cor); px(cx + d * sx, cy + sy * i + d * sy, 1, 1, cor); }
      });
    });
  }
  // o nome do Ferreiro à esquerda da bigorna, sobre a parede (não cobre o rosto, o martelo nem a espada)
  const PONTOS = {
    ferreiro: { area: [104, 14, 80, 58], balao: [118, 36], foco: [150, 46] },
    saida: { area: [8, 12, 34, 34], balao: [23, 26], foco: [23, 30] },
  };

  window.ForjaArte = window.ForjaArte || {};
  window.ForjaArte.r = { base, desenhar, pontos: PONTOS, poseDe, POSES, CICLO, DURACAO, figura, L, QW, QH };
})();
