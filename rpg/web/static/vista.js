/* Vista: uma paisagem em pixel art (320x72) gerada para cada lugar, com céu do período do dia, clima, silhuetas do
   bioma e partículas (chuva, neve, névoa, fumaça, estrelas, corvos). Minimalista e melancólica: silhuetas em poucas
   camadas, o céu em faixas pontilhadas (Bayer), o sol morno com um halo só (a lua, sem halo) e fiapos de nuvem. */
"use strict";

const Vista = (() => {
  const W = 320, H = 72;
  const CEUS = [
    ["#2c4470", "#45648f", "#7a90b0", "#c09a80", "#e8b88a"],
    ["#24508c", "#33649e", "#4f80b6", "#79a4c8", "#a8c4d6"],
    ["#22163a", "#43264a", "#82363e", "#bc5630", "#ec8c3c"],
    ["#04050c", "#080b1a", "#0d1328", "#121a33", "#18223f"],
  ];
  // O sol (ou a lua) de cada período: posição, raio, cor do disco e cor da metade de baixo.
  const ASTROS = [[60, 30, 7, "#ffe8a0", "#f0c890"], [210, 12, 6, "#fff6c8", "#ece2b4"], [248, 40, 10, "#e8784a", "#d8603a"], [70, 14, 5, "#e8ecf4", "#c8ccd8"]];
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const pont = (x, y, nivel) => BAYER[(y & 3) * 4 + (x & 3)] < nivel;  // nivel de 0 a 16
  let canvas, ctx, fundo, frente, chave = "", estado = null, quadro = 0, timer = null;
  let nuvens = [], neblinas = [], particulas = [], fumacas = [], estrelas = [], aves = [], relampago = 0;
  const LUZ_JANELA = "#e8a050";
  // A vila como lugar: os prédios clicáveis (área, luzes, ponto do balão), o que está sob o mouse e a câmera (foco).
  // A câmera não desliza (escala quebrada faz o pixel tremer): ela troca de enquadramento num pontilhado que se fecha,
  // do enquadramento de antes (`de`) para o novo, sempre em pixel inteiro.
  let predios = [], destaque = null, quadroBuf = null, mascara = null;
  const camera = { x: 0, y: 0, s: 1, de: null, inicio: 0, ms: 380 };
  const tramas = [];

  function rng(semente) {
    let s = (semente * 9301 + 49297) % 233280 || 1;
    return () => (s = (s * 16807) % 2147483647) / 2147483647;
  }
  function hex(c) { return [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16)); }
  function mix(a, b, t) {
    const x = hex(a), y = hex(b);
    return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join("");
  }
  function px(c, x, y, w = 1, h = 1, cor) { c.fillStyle = cor; c.fillRect(x | 0, y | 0, w, h); }

  /** O céu em faixas; a passagem de uma para a outra é pontilhada pelo Bayer, sem degrau duro. */
  function ceu(c, e) {
    const p = e.mundo.periodo_n;
    let bandas = CEUS[p].slice();
    const clima = e.mundo.clima_id;
    if (["chuva", "tempestade", "nublado"].includes(clima)) bandas = bandas.map((b) => mix(b, "#3a3f48", clima === "tempestade" ? 0.75 : 0.55));
    if (clima === "nevoa") bandas = bandas.map((b) => mix(b, "#8a9098", 0.5));
    if (clima === "neve") bandas = bandas.map((b) => mix(b, "#a8b0bc", 0.45));
    if (e.local.bioma === "cidadela") bandas = bandas.map((b, i) => mix(b, i > 2 ? "#a01818" : "#2a0508", 0.7));
    const altura = 50;
    for (let y = 0; y < H; y++) {
      const f = (Math.min(y, altura) / altura) * (bandas.length - 1), i = Math.floor(f), resto = Math.floor((f - i) * 16);
      const a = bandas[i], b = bandas[Math.min(i + 1, bandas.length - 1)];
      for (let x = 0; x < W; x++) px(c, x, y, 1, 1, pont(x, y, resto) ? b : a);
    }
    // O sol (ou a lua): um disco morno, a metade de baixo um tom abaixo; o sol tem um halo de um anel só, pontilhado,
    // e a lua em quarto fica limpa no escuro.
    if (["limpo", "neve"].includes(clima) || p === 3) {
      const [sx, sy, raio, cor, baixo] = ASTROS[p], halo = mix(bandas[bandas.length - 2], cor, 0.45);
      for (let y = sy - raio - 6; y <= sy + raio + 6; y++) for (let x = sx - raio - 6; x <= sx + raio + 6; x++) {
        const d = Math.hypot(x - sx, y - sy);
        if (d <= raio) px(c, x, y, 1, 1, y > sy + raio / 3 && pont(x, y, 8) ? baixo : cor);
        else if (p !== 3 && d < raio + 5 && pont(x, y, Math.round(9 - (d - raio) * 1.6))) px(c, x, y, 1, 1, halo);
      }
      if (p === 3) for (let y = -raio; y <= raio; y++) for (let x = -raio; x <= raio; x++) {  // a lua em quarto
        if ((x - 3) * (x - 3) + (y + 1) * (y + 1) <= raio * raio * 0.8) px(c, sx + x, sy + y, 1, 1, bandas[0]);
      }
    }
    return bandas;
  }

  function perfil(r, base, amp, rugosidade) {
    const ys = [];
    let y = base, v = 0;
    for (let x = 0; x < W; x++) {
      v += (r() - 0.5) * rugosidade;
      v = Math.max(-1.5, Math.min(1.5, v * 0.92));
      y += v;
      y = Math.max(base - amp, Math.min(base + amp * 0.4, y));
      ys.push(Math.round(y));
    }
    return ys;
  }
  function silhueta(c, ys, cor) { ys.forEach((y, x) => px(c, x, y, 1, H - y, cor)); }
  /** A crista de uma camada, tocada pela luz do lado em que está o sol. */
  function crista(c, ys, cor, ladoX) { ys.forEach((y, x) => { if (Math.abs(x - ladoX) < 120 && (ys[x - 1] ?? y) > y) px(c, x, y, 1, 1, cor); }); }
  /** Névoa pontilhada numa faixa (as bordas mais ralas). */
  function nevoa(c, y0, y1, cor, forca, x0 = 0, x1 = W, fase = 0) {
    const meio = (y0 + y1) / 2, meia = (y1 - y0) / 2;
    for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
      const n = Math.round(forca * (1 - Math.abs(y - meio) / meia) + Math.sin((x + fase) / 11) * 1.5);
      if (n > 0 && pont(x, y, n)) px(c, x, y, 1, 1, cor);
    }
  }

  /** Pinheiro: ponta fina e a copa em degraus (cada terceira linha um pouco mais larga). */
  function pinheiro(c, x, y, h, cor) {
    for (let i = 0; i < h; i++) {
      const larg = Math.floor((i / h) * (h / 2.2)) + (i % 3 === 0 && i > 2 ? 1 : 0);
      px(c, x - larg, y - h + i, larg * 2 + 1, 1, cor);
    }
    px(c, x, y, 1, 2, cor);
  }
  /** Árvore seca: tronco e galhos tortos em diagonal, alternando os lados, mais curtos no alto. */
  function arvoreSeca(c, x, y, h, cor, lado = 1) {
    px(c, x, y - h, 1, h, cor);
    for (let i = 0; i < Math.floor(h / 4); i++) {
      const yy = y - h + 2 + i * 4, dir = (i + (lado > 0 ? 0 : 1)) % 2 ? 1 : -1, comp = Math.max(2, 5 - i + ((x + i) % 2));
      for (let k = 0; k < comp; k++) px(c, x + (dir > 0 ? 1 + k : -1 - k), yy - Math.floor(k / 2), 1, 1, cor);
    }
  }
  /** Casinha do fundo da vila: paredes, telhado em ponta e, à noite, às vezes uma janelinha de um pixel. */
  function casinha(c, x, base, w, h, cor, telha, luz) {
    px(c, x, base - h, w, h, cor);
    for (let i = 0; i < Math.ceil(w / 2); i++) px(c, x - 1 + i, base - h - 1 - i, w + 2 - i * 2, 1, telha);
    if (luz) px(c, x + Math.floor(w / 2) - 1, base - h + 2, 1, 1, luz);
  }
  function casa(c, x, base, w, h, alto, cor, telha, janela) {
    px(c, x, base - h, w, h, cor);
    const t2 = alto ? Math.ceil(w / 2) + 2 : Math.ceil(w / 2);
    for (let i = 0; i < t2; i++) { const recuo = alto ? Math.floor((i * w) / (2 * t2)) : i; px(c, x - 1 + recuo, base - h - 1 - i, w + 2 - recuo * 2, 1, telha); }
    px(c, x + w - 3, base - h - t2 + 1, 2, 4, cor);
    if (janela) px(c, x + 2, base - h + 3, 2, 2, janela);
    if (w > 12) px(c, x + w - 5, base - 4, 2, 4, "#0d0b0a");
    return [x + w - 2, base - h - t2 - 3];
  }

  function bioma(c, e, r, bandas) {
    const p = e.mundo.periodo_n, noite = p === 3, acesa = p >= 2;
    const horizonte = bandas[bandas.length - 1];
    const escuro = (t) => mix(horizonte, "#050404", t);
    const b = e.local.tipo === "vila" ? "vila" : e.local.bioma;
    const longe = escuro(0.45), meio = escuro(0.65), perto = escuro(0.82), chao = escuro(0.9);
    const sol = ASTROS[p], ladoSol = noite ? -999 : sol[0], luz = mix(longe, sol[3], noite ? 0 : 0.4);
    fumacas = []; aves = []; predios = [];
    const corvos = (n, y0, y1) => { for (let i = 0; i < n; i++) aves.push({ x: r() * W, y: y0 + r() * (y1 - y0), v: 0.15 + r() * 0.2, f: Math.floor(r() * 8) }); };
    // A névoa rasteira de cada bioma, um tom acima da camada de trás.
    const bruma = mix(longe, horizonte, 0.5);
    if (b === "montanha") {
      // duas cordilheiras: a de trás alta, de neve pontilhada no topo; a da frente baixa, com pinheiros miúdos
      const picos = perfil(r, 28, 18, 2.6);
      silhueta(c, picos, longe);
      const neve = mix(longe, "#e8ecf4", noite ? 0.35 : 0.75);
      picos.forEach((y, x) => { for (let k = 0; k < 8; k++) if (y + k < 26 && pont(x, y + k, 16 - k * 2)) px(c, x, y + k, 1, 1, neve); });
      const meioYs = perfil(r, 46, 10, 1.6);
      silhueta(c, meioYs, meio);
      crista(c, meioYs, luz, ladoSol);
      silhueta(c, perfil(r, 62, 4, 0.8), chao);
      corvos(2, 6, 20);
    } else if (b === "floresta") {
      silhueta(c, perfil(r, 40, 6, 0.8), longe);
      for (let x = -4; x < W; x += 4 + Math.floor(r() * 4)) pinheiro(c, x, 46 + Math.floor(r() * 4), 8 + Math.floor(r() * 6), mix(longe, meio, 0.5));
      nevoa(c, 42, 52, bruma, 4);
      for (let x = -4; x < W; x += 5 + Math.floor(r() * 4)) pinheiro(c, x, 54 + Math.floor(r() * 4), 10 + Math.floor(r() * 8), meio);
      silhueta(c, perfil(r, 60, 3, 0.6), chao);
      for (let x = 0; x < W; x += 11 + Math.floor(r() * 14)) pinheiro(c, x, 70, 16 + Math.floor(r() * 10), perto);
      arvoreSeca(c, 120 + Math.floor(r() * 80), 66, 16, perto, 1);
    } else if (b === "pantano") {
      // a água espelha o céu em riscos; árvores mortas, juncos e névoa rasteira
      silhueta(c, perfil(r, 44, 3, 0.5), longe);
      const agua = mix(horizonte, "#0a1a18", 0.6), brilho = mix(horizonte, "#5a7a78", 0.4);
      px(c, 0, 52, W, H - 52, agua);
      for (let y = 53; y < H; y += 2) for (let x = (y * 7) % 13; x < W; x += 13 + (y % 5)) px(c, x, y, 3 + (x % 4), 1, brilho);
      for (let x = 8; x < W; x += 26 + Math.floor(r() * 30)) {
        const h = 12 + Math.floor(r() * 12);
        arvoreSeca(c, x, 54, h, perto, r() < 0.5 ? 1 : -1);
        for (let k = 0; k < h / 2; k += 2) if (pont(x, 55 + k, 8)) px(c, x, 55 + k, 1, 1, mix(agua, perto, 0.5));  // reflexo
      }
      for (let x = 0; x < W; x += 3) if (r() < 0.45) px(c, x, 49 + Math.floor(r() * 4), 1, 4 + Math.floor(r() * 3), meio);
      nevoa(c, 47, 55, bruma, 4);
      corvos(2, 10, 26);
    } else if (b === "planicie") {
      // morros suaves, um moinho ao longe, um carvalho sozinho e uma cerca
      const longeYs = perfil(r, 42, 5, 0.6);
      silhueta(c, longeYs, longe);
      crista(c, longeYs, luz, ladoSol);
      const mx = 220 + Math.floor(r() * 50), my = longeYs[mx] + 1;
      px(c, mx, my - 9, 4, 9, mix(longe, meio, 0.6)); px(c, mx + 1, my - 11, 2, 2, mix(longe, meio, 0.6));
      const pa = Math.floor(r() * 2);
      for (let k = -5; k <= 5; k++) px(c, mx + 2 + k, my - 10 + (pa ? k : -k), 1, 1, mix(longe, meio, 0.6));
      silhueta(c, perfil(r, 52, 4, 0.5), meio);
      for (let x = 0; x < W; x += 2) if (r() < 0.55) px(c, x, 55 + Math.floor(r() * 10), 1, 2, mix(meio, "#8a9a4a", noite ? 0.15 : 0.4));
      const ax = 40 + Math.floor(r() * 80);
      px(c, ax, 42, 2, 12, perto);
      [[-6, 34, 14, 3], [-8, 37, 18, 3], [-7, 40, 16, 2], [-4, 32, 9, 2]].forEach(([dx, y, w, h]) => px(c, ax + dx, y, w, h, perto));
      silhueta(c, perfil(r, 64, 2, 0.4), chao);
      for (let x = 150; x < W; x += 6) px(c, x, 60, 1, 4, chao);
      px(c, 150, 61, W - 150, 1, chao);
      corvos(3, 8, 24);
    } else if (b === "ruinas") {
      // colunas quebradas, um arco ainda de pé e blocos caídos
      silhueta(c, perfil(r, 44, 5, 0.6), longe);
      for (let x = 10; x < W; x += 24 + Math.floor(r() * 18)) {
        const h = 8 + Math.floor(r() * 18);
        px(c, x, 54 - h, 4, h, meio); px(c, x - 1, 54 - h, 6, 2, meio);
        if (r() < 0.4) px(c, x + 6, 52, 5, 2, meio);
      }
      // o arco entre duas colunas, com a pedra do meio caída aos pés dele
      const ax = 130 + Math.floor(r() * 50);
      px(c, ax, 30, 4, 24, meio); px(c, ax + 24, 30, 4, 24, meio);
      for (let k = 0; k <= 26; k++) if (k < 11 || k > 15) px(c, ax + 1 + k, 30 - Math.round(Math.sin((k / 26) * Math.PI) * 9), 1, 3, meio);
      px(c, ax + 10, 51, 5, 3, meio); px(c, ax + 16, 52, 3, 2, meio);
      nevoa(c, 48, 56, bruma, 3);
      silhueta(c, perfil(r, 58, 3, 0.5), chao);
      corvos(3, 8, 22);
    } else if (b === "cidadela") {
      // o castelo em bloco da arte original, em silhueta; só duas janelas e o portão em brasa fraca
      const longeYs = perfil(r, 46, 6, 0.9);
      silhueta(c, longeYs, longe);
      crista(c, longeYs, luz, ladoSol);
      silhueta(c, perfil(r, 54, 3, 0.5), meio);
      const cx = 160;
      px(c, cx - 40, 30, 80, 30, perto);
      [[-44, 16, 10], [-14, 8, 12], [16, 12, 10], [36, 20, 10]].forEach(([dx, topo, larg], i) => {
        px(c, cx + dx, topo, larg, 44, perto);
        for (let k = 0; k < larg; k += 3) px(c, cx + dx + k, topo - 2, 2, 2, perto);
        if (i === 1 || i === 3) px(c, cx + dx + Math.floor(larg / 2) - 1, topo + 8, 2, 3, "#c8301c");
      });
      px(c, cx - 4, 47, 8, 13, "#7a1a12"); px(c, cx - 2, 49, 4, 11, "#b83a1a");
      silhueta(c, perfil(r, 60, 2, 0.4), chao);
      for (let y = 60; y < H; y++) { const x = Math.round(cx + Math.sin((y - 60) / 3.5) * (y - 59) * 1.4); px(c, x - 1, y, 2 + Math.floor((y - 60) / 4), 1, mix(chao, "#5a1414", 0.35)); }
      arvoreSeca(c, 36, 64, 20, chao, 1);
      corvos(4, 8, 22);
    } else {
      vila(c, r, { longe, meio, perto, chao, acesa, horizonte });
    }
  }

  /** A vila: cada serviço tem o seu prédio (a forja, as barracas do mercado, o mural da praça, a taverna, o templo, a
   *  curandeira e a estrada com a placa), entre casas comuns, a forca e a cerca; atrás, duas fileiras de casas dão o
   *  fundo. Cada prédio se registra em `predios`: a área de clique, o ponto onde o balão do nome aponta (`balao`), as
   *  luzes que acendem no hover e o que se mexe nele. */
  function vila(c, r, { longe, meio, perto, chao, acesa, horizonte }) {
    silhueta(c, perfil(r, 42, 4, 0.5), longe);
    const telha = mix(meio, "#5a1a10", 0.35), escuro = "#0d0b0a", JANELA = acesa ? LUZ_JANELA : mix(meio, "#7a5a30", 0.5);
    const madeira = mix(meio, "#7a5a3a", 0.4), papel = mix(meio, "#c8b898", 0.45);
    const fundoCasa = mix(longe, meio, 0.45), casaLonge = mix(longe, meio, 0.18);
    // a fileira de longe, no morro: telhados miúdos aparecendo entre os prédios e por cima deles
    const luzLonge = acesa ? mix(LUZ_JANELA, longe, 0.45) : null;
    [[-2, 51, 8, 5], [33, 52, 7, 4], [50, 49, 9, 5], [66, 50, 7, 4], [75, 52, 6, 4], [99, 51, 7, 5], [140, 49, 8, 4],
      [177, 52, 6, 4], [193, 50, 9, 5], [212, 51, 7, 4], [224, 49, 10, 6], [238, 51, 7, 4], [255, 50, 8, 5],
      [270, 52, 6, 4], [298, 50, 9, 5], [312, 52, 8, 4]]
      .forEach(([x, b, w, h], i) => casinha(c, x, b, w, h, casaLonge, mix(casaLonge, "#5a1a10", 0.2), i % 3 === 1 ? luzLonge : null));
    [[204, 58, 12, 8], [218, 58, 9, 6], [229, 58, 12, 9], [246, 58, 10, 7], [262, 58, 9, 6]]
      .forEach(([x, b, w, h], i) => casa(c, x, b, w, h, i === 2, fundoCasa, mix(fundoCasa, "#5a1a10", 0.3), null));
    for (let x = 0; x < W; x += 5) px(c, x, 55, 1, 4, perto);
    px(c, 0, 56, W, 1, perto);
    const reg = (id, nome, area, extra = {}) => predios.push({ id, nome, ...area, luzes: [], ...extra });
    // a forja do ferreiro: chaminé larga, porta em brasa e a bigorna do lado de fora
    px(c, 6, 47, 22, 11, meio);
    for (let i = 0; i < 6; i++) px(c, 5 + i, 46 - i, 24 - i * 2, 1, telha);
    px(c, 23, 35, 6, 1, meio); px(c, 24, 36, 4, 11, meio);
    px(c, 9, 51, 5, 7, "#5a1e0c"); px(c, 10, 52, 3, 6, "#a8401a");
    px(c, 31, 54, 7, 1, perto); px(c, 32, 55, 5, 1, perto); px(c, 33, 56, 3, 2, perto);
    reg("ferreiro", "Ferreiro", { x: 4, y: 33, w: 36, h: 25 }, { balao: [16, 40], luzes: [[10, 52, 3, 6, "#ffa040"]], fagulha: [25, 34] });
    // as barracas do mercado: toldo listrado, balcão e mercadoria
    const listra = [mix(meio, "#7a2a22", 0.5), mix(meio, "#9a7a4a", 0.5)];
    [44, 58].forEach((x) => {
      px(c, x, 46, 1, 12, meio); px(c, x + 11, 46, 1, 12, meio);
      for (let k = 0; k < 13; k++) { px(c, x - 1 + k, 44, 1, 3, listra[Math.floor(k / 2) % 2]); if (k % 2 === 0) px(c, x - 1 + k, 47, 1, 1, listra[Math.floor(k / 2) % 2]); }
      px(c, x, 52, 12, 6, meio); px(c, x + 2, 50, 3, 2, perto); px(c, x + 7, 50, 2, 2, perto);
    });
    reg("mercado", "Mercado", { x: 42, y: 41, w: 31, h: 17 }, { balao: [57, 43], luzes: [[49, 51, 1, 1, "#ffd860"], [63, 51, 1, 1, "#ffd860"]] });
    // o mural de avisos, na praça
    px(c, 84, 46, 1, 12, meio); px(c, 95, 46, 1, 12, meio);
    px(c, 82, 43, 16, 1, telha); px(c, 83, 44, 14, 8, mix(meio, "#5a4030", 0.3));
    [[85, 45, 3, 3], [89, 46, 2, 3], [92, 45, 3, 4]].forEach(([x, y, w, h]) => px(c, x, y, w, h, papel));
    reg("mural", "Mural", { x: 80, y: 40, w: 20, h: 18 }, { balao: [90, 42], luzes: [[85, 45, 3, 3, "#e8dcc0"], [89, 46, 2, 3, "#e8dcc0"], [92, 45, 3, 4, "#e8dcc0"]] });
    // a forca da praça
    px(c, 104, 40, 2, 18, perto); px(c, 104, 40, 12, 2, perto);
    px(c, 113, 42, 1, 3, mix(perto, "#8a7a6a", 0.4)); px(c, 112, 45, 3, 5, perto); px(c, 112, 50, 1, 3, perto); px(c, 114, 50, 1, 3, perto);
    // a taverna: dois andares, placa pendurada, janelas acesas e a chaminé fumando
    px(c, 120, 42, 24, 16, meio);
    for (let i = 0; i < 9; i++) px(c, 119 + i, 41 - i, 26 - i * 2, 1, telha);
    px(c, 137, 30, 3, 6, meio);
    const janelasTaverna = [[123, 45, 3, 3], [137, 45, 3, 3], [124, 51, 4, 3]];
    janelasTaverna.forEach(([x, y, w, h]) => px(c, x, y, w, h, JANELA));
    px(c, 133, 51, 4, 7, escuro);
    px(c, 115, 44, 6, 1, perto); px(c, 115, 45, 4, 3, madeira); px(c, 116, 46, 2, 1, perto);
    fumacas.push({ x: 137, y: 27, t: r() * 20 });
    reg("taverna", "Taverna", { x: 112, y: 29, w: 34, h: 29 }, { balao: [127, 32], luzes: janelasTaverna.map((j) => [...j, "#ffd070"]) });
    // o templo: a igreja com o sino no campanário
    px(c, 150, 40, 24, 18, meio);
    for (let i = 0; i < 9; i++) px(c, 149 + i, 39 - i, 26 - i * 2, 1, telha);
    px(c, 166, 18, 8, 22, meio); for (let i = 0; i < 5; i++) px(c, 165 + i, 18 - i * 2, 10 - i * 2, 2, telha);
    px(c, 169, 4, 1, 6, meio); px(c, 167, 6, 5, 1, meio);
    px(c, 168, 23, 4, 4, escuro); px(c, 169, 24, 2, 2, mix(meio, "#8a7a50", 0.5));
    px(c, 161, 51, 4, 7, escuro);
    const vitrais = [[156, 45, 2, 4], [166, 45, 2, 4]];
    vitrais.forEach(([x, y, w, h]) => px(c, x, y, w, h, JANELA));
    reg("templo", "Templo", { x: 148, y: 2, w: 28, h: 56 }, { balao: [156, 30], foco: [166, 20], luzes: vitrais.map((j) => [...j, "#ffd070"]) });
    // a cabana da curandeira: teto de palha, ervas penduradas e uma janela esverdeada
    px(c, 184, 50, 14, 8, meio);
    [[183, 49, 16], [184, 48, 14], [186, 47, 10], [188, 46, 6]].forEach(([x, y, w]) => px(c, x, y, w, 1, telha));
    [185, 189, 195].forEach((x) => px(c, x, 50, 1, 2, mix(meio, "#4a7a3a", 0.5)));
    px(c, 191, 52, 2, 2, acesa ? "#a8d080" : mix(meio, "#4a6a3a", 0.5)); px(c, 186, 53, 3, 5, escuro);
    reg("curandeiro", "Curandeira", { x: 182, y: 44, w: 18, h: 14 }, { balao: [191, 45], luzes: [[191, 52, 2, 2, "#c8f0a0"]] });
    // a estrada saindo da vila pela direita, a placa de encruzilhada com a lanterna e um marco de pedra
    const terra = mix(chao, "#6a5a48", 0.3);
    for (let y = 58; y < H; y++) { const x0 = Math.round(292 + (71 - y) * 1.3); px(c, x0, y, W - x0, 1, terra); }
    px(c, 284, 42, 2, 16, perto);
    px(c, 277, 43, 9, 2, madeira); px(c, 276, 44, 1, 1, madeira);
    px(c, 286, 47, 10, 2, madeira); px(c, 296, 48, 1, 1, madeira);
    px(c, 286, 41, 4, 1, perto); px(c, 289, 42, 2, 3, perto); px(c, 289, 43, 2, 1, acesa ? LUZ_JANELA : mix(perto, "#5a4028", 0.6));
    px(c, 306, 54, 4, 4, meio); px(c, 307, 53, 2, 1, meio);
    reg("estrada", "Estrada", { x: 272, y: 38, w: 48, h: 20 }, { balao: [285, 40], luzes: [[289, 43, 2, 1, "#ffd070"]], lanterna: [289, 43] });
    px(c, 0, 58, 292, H - 58, chao);
    for (let y = 58; y < H; y++) { const x0 = Math.round(292 + (71 - y) * 1.3); px(c, 290, y, Math.max(0, x0 - 290), 1, chao); }
  }

  /** Duas camadas guardadas: o céu (com o sol) atrás e as silhuetas na frente; nuvens e estrelas passam entre elas. */
  function preparar(e) {
    fundo = document.createElement("canvas"); frente = document.createElement("canvas");
    fundo.width = frente.width = W; fundo.height = frente.height = H;
    const c = fundo.getContext("2d");
    const r = rng(e.local.id * 97 + 13);
    const bandas = ceu(c, e);
    const clima = e.mundo.clima_id, p = e.mundo.periodo_n;
    // fiapos de nuvem: longos e finos, escuros por cima; mais e mais grossos com o tempo fechado
    nuvens = [];
    const fechado = ["chuva", "tempestade", "nublado", "nevoa", "neve"].includes(clima);
    const corNuvem = p === 2 ? mix(bandas[1], "#000000", 0.3) : p === 3 ? mix(bandas[1], "#2a3048", 0.5)
      : mix(bandas[1], fechado ? "#3a3f48" : "#e8ecf4", fechado ? 0.4 : 0.3);
    const n = clima === "nevoa" ? 3 : fechado ? 8 : clima === "limpo" && r() < 0.4 ? 0 : 4;
    for (let i = 0; i < n; i++) nuvens.push({ x: r() * (W + 80), y: 5 + r() * 36, w: 40 + r() * 80, v: 0.04 + r() * 0.08, esp: fechado && r() < 0.5 ? 3 : 2, cor: corNuvem });
    // Névoa: bancos compridos e baixos, do traço das nuvens, passando devagar atrás das silhuetas (a vila e os prédios
    // ficam limpos na frente); os de cima mais ralos, os de perto do morro mais cheios.
    neblinas = [];
    if (clima === "nevoa") {
      const clara = mix(bandas[3], "#dfe2e8", p === 3 ? 0.16 : 0.42), rala = mix(bandas[2], clara, 0.55);
      for (let i = 0; i < 9; i++) {
        const y = 12 + Math.round((i / 8) * 30 + r() * 4);
        neblinas.push({ x: r() * (W + 160), y, w: 90 + r() * 130, v: 0.03 + r() * 0.05, cor: y > 30 ? clara : rala, alta: y <= 30 });
      }
    }
    bioma(frente.getContext("2d"), e, r, bandas);
    pintarChao();
    estrelas = [];
    if (p === 3 && !["chuva", "tempestade", "nublado", "nevoa"].includes(clima)) {
      for (let i = 0; i < 40; i++) estrelas.push({ x: Math.floor(r() * W), y: Math.floor(r() * 34), f: r() * 10 });
    }
    particulas = [];
    const qtd = { chuva: 70, tempestade: 120, neve: 60 }[clima] || 0;
    for (let i = 0; i < qtd; i++) particulas.push({ x: r() * W, y: r() * H, v: clima === "neve" ? 0.3 + r() * 0.4 : 3 + r() * 2 });
  }

  /** O chão da paisagem continua para fora dela: uma rampa pontilhada na cor da última linha, que a cena usa embaixo
   *  da arte (--chao-rampa), para a página parecer começar no chão. Vai no corpo da página: fora da luta a arte está
   *  na cena, na luta ela é o fundo da arena, e o chão continua nos dois casos. */
  function pintarChao() {
    const cena = document.body;
    if (!canvas || !cena) return;
    const [r, g, b] = frente.getContext("2d").getImageData(W >> 1, H - 1, 1, 1).data;
    const t = document.createElement("canvas"), n = 12;
    t.width = 4; t.height = n;
    const x = t.getContext("2d");
    x.fillStyle = `rgb(${r}, ${g}, ${b})`;
    for (let i = 0; i < n; i++) { const k = Math.round(16 * (1 - (i + 0.5) / n)); for (let j = 0; j < 4; j++) if (pont(j, i, k)) x.fillRect(j, i, 1, 1); }
    cena.style.setProperty("--chao-rampa", `url(${t.toDataURL()})`);
    cena.style.setProperty("--chao", `rgb(${r}, ${g}, ${b})`);
  }
  /** O prédio sob o mouse: as luzes dele acendem (só os pixels da janela, sem clarão em volta); a lanterna da estrada
   *  tremula. */
  function pintarDestaque(b) {
    const p = predios.find((x) => x.id === destaque);
    if (!p) return;
    const tremula = [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1][quadro % 14];
    p.luzes.forEach(([x, y, w, h, cor]) => px(b, x, y, w, h, !p.lanterna || tremula ? cor : LUZ_JANELA));
  }
  /** Fagulhas da forja: sempre umas poucas; com o mouse em cima, um punhado. */
  function pintarFagulhas(b) {
    predios.filter((p) => p.fagulha).forEach((p) => {
      const n = destaque === p.id ? 6 : 2;
      for (let i = 0; i < n; i++) {
        const t = (quadro * 0.7 + i * 7) % 16, x = p.fagulha[0] + Math.round(Math.sin(i * 2 + t / 3) * 2), y = p.fagulha[1] - Math.round(t);
        if (t < 12) px(b, x, y, 1, 1, t < 5 ? "#ffd070" : "#e8783a");
      }
    });
  }

  /** Um passo do relógio da paisagem (dez por segundo): nuvens, corvos, chuva e relâmpago andam só aqui, para que
   *  redesenhar (o hover, a troca de câmera, o amanhecer) não apresse nada. */
  function andar() {
    quadro++;
    nuvens.forEach((n) => { n.x = (n.x + n.v) % (W + n.w); });
    neblinas.forEach((n) => { n.x = (n.x + n.v) % (W + n.w); });
    aves.forEach((a) => { a.x = (a.x + a.v) % (W + 20); });
    const neve = estado.mundo.clima_id === "neve";
    particulas.forEach((p) => {
      p.y += p.v;
      p.x += neve ? Math.sin((quadro + p.y) / 9) * 0.3 : -p.v * 0.4;
      if (p.y > H) { p.y = -3; p.x = Math.random() * (W + 30); }
    });
    if (relampago > 0) relampago--;
    else if (estado.mundo.clima_id === "tempestade" && Math.random() < 0.006) relampago = 5;
  }

  /** Uma trama de Bayer com `n` de 16 pixels cheios: a máscara do pontilhado da troca de câmera. */
  function trama(n) {
    if (!tramas[n]) {
      const t = document.createElement("canvas"); t.width = t.height = 4;
      const c = t.getContext("2d"); c.fillStyle = "#000";
      for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) if (pont(x, y, n)) c.fillRect(x, y, 1, 1);
      tramas[n] = ctx.createPattern(t, "repeat");
    }
    return tramas[n];
  }
  /** O quadro pela câmera: a vila inteira, ou o recorte do prédio em dobro. Sempre pixel inteiro. */
  function enquadrar(c, cam) {
    c.imageSmoothingEnabled = false;
    c.drawImage(quadroBuf, cam.x, cam.y, W / cam.s, H / cam.s, 0, 0, W, H);
  }

  function desenhar() {
    if (!estado || !ctx) return;
    if (!quadroBuf) { quadroBuf = document.createElement("canvas"); quadroBuf.width = W; quadroBuf.height = H; }
    desenharEm(quadroBuf.getContext("2d"));
    ctx.clearRect(0, 0, W, H);
    const t = camera.de ? (performance.now() - camera.inicio) / camera.ms : 1;
    if (t >= 1) { camera.de = null; enquadrar(ctx, camera); }
    else {
      // a troca de câmera: o enquadramento de antes embaixo, o novo por cima numa trama que vai fechando
      if (!mascara) { mascara = document.createElement("canvas"); mascara.width = W; mascara.height = H; }
      const m = mascara.getContext("2d");
      enquadrar(ctx, camera.de);
      m.globalCompositeOperation = "source-over"; m.clearRect(0, 0, W, H); enquadrar(m, camera);
      m.globalCompositeOperation = "destination-in"; m.fillStyle = trama(Math.max(1, Math.ceil(t * 16))); m.fillRect(0, 0, W, H);
      ctx.drawImage(mascara, 0, 0);
    }
    if (aurora) pintarAurora();
  }

  function desenharEm(ctx) {
    ctx.drawImage(fundo, 0, 0);
    const clima = estado.mundo.clima_id;
    estrelas.forEach((s) => { if ((quadro + s.f) % 14 > 2) px(ctx, s.x, s.y, 1, 1, (quadro + s.f) % 30 < 4 ? "#ffffff" : "#9aa4c0"); });
    nuvens.forEach((n) => {
      const x = Math.floor(n.x - n.w);
      px(ctx, x, n.y, n.w, 1, n.cor); px(ctx, x + 6, n.y - 1, n.w - 18, 1, n.cor);
      if (n.esp === 3) px(ctx, x + n.w / 4, n.y - 2, n.w / 3, 1, n.cor);
    });
    neblinas.forEach((n) => {  // um banco: o corpo de duas linhas, a crista mais curta e a barra rala embaixo
      const x = Math.floor(n.x - n.w), w = Math.round(n.w);
      px(ctx, x, n.y, w, n.alta ? 1 : 2, n.cor);
      px(ctx, x + 10, n.y - 1, w - 26, 1, n.cor);
      px(ctx, x + 22, n.y - 2, Math.round(w * 0.35), 1, n.cor);
      px(ctx, x + 6, n.y + (n.alta ? 1 : 2), w - 30, 1, n.cor);
    });
    ctx.drawImage(frente, 0, 0);
    pintarFagulhas(ctx);
    if (destaque) pintarDestaque(ctx);
    aves.forEach((a, k) => {  // corvos, devagar, batendo as asas
      const x = Math.floor(a.x) - 10, y = Math.round(a.y + Math.sin((quadro + k * 9) / 12)), asa = (Math.floor(quadro / 4) + a.f) % 2, cor = "#0c0606";
      px(ctx, x, y, 1, 1, cor); px(ctx, x - 2, y - asa, 2, 1, cor); px(ctx, x + 1, y - asa, 2, 1, cor);
    });
    fumacas.forEach((f) => {  // fumaça pontilhada, rareando enquanto sobe
      for (let i = 0; i < 6; i++) {
        const t = (quadro * 0.5 + f.t + i * 3) % 18, x = f.x + Math.round(Math.sin((t + i) / 3) * 2 + t * 0.3), y = Math.round(f.y - t);
        if (pont(x, y, Math.round(12 - t * 0.6))) px(ctx, x, y, 2, 2, "#8a8288");
      }
    });
    particulas.forEach((p) => {
      if (clima === "neve") px(ctx, p.x, p.y, 1, 1, "#f0f4ff");
      else px(ctx, p.x, p.y, 1, 3, "rgba(170,190,220,0.7)");
    });
    if (relampago > 0) { ctx.fillStyle = `rgba(230,235,255,${relampago / 6})`; ctx.fillRect(0, 0, W, H); }
    if (estado.mundo.escuro) { ctx.fillStyle = "rgba(0,0,0,0.55)"; ctx.fillRect(0, 0, W, H); }
  }

  /** O amanhecer: a paisagem já é a da manhã; por cima, a noite se desfaz e um clarão quente sobe do horizonte. */
  let aurora = null;
  function pintarAurora() {
    const t = (performance.now() - aurora.inicio) / aurora.ms;
    if (t >= 1) { aurora = null; return; }
    ctx.fillStyle = `rgba(8, 10, 30, ${0.9 * Math.pow(1 - t, 1.6)})`;
    ctx.fillRect(0, 0, W, H);
    const g = ctx.createRadialGradient(W / 2, H * (1.1 - 0.5 * t), 4, W / 2, H * (1.1 - 0.5 * t), W * 0.6);
    g.addColorStop(0, `rgba(255, 190, 110, ${0.55 * Math.sin(Math.PI * t)})`);
    g.addColorStop(1, "rgba(255, 140, 80, 0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
  }
  function amanhecer(ms = 1800) {
    aurora = { inicio: performance.now(), ms };
    const passo = () => { if (!aurora) { desenhar(); return; } desenhar(); requestAnimationFrame(passo); };
    requestAnimationFrame(passo);
  }

  function atualizar(e) {
    canvas = canvas || document.getElementById("vista");
    if (!canvas || !e) return;
    ctx = ctx || canvas.getContext("2d");
    estado = e;
    const k = [e.local.id, e.local.tipo, e.mundo.periodo_n, e.mundo.clima_id, e.local.bioma].join("|");
    if (k !== chave) {
      if (chave.split("|")[0] !== String(e.local.id)) { camera.x = camera.y = 0; camera.s = 1; camera.de = null; destaque = null; }
      chave = k; preparar(e);
    }
    if (!timer) timer = setInterval(() => { if (!document.hidden) { andar(); desenhar(); } }, 100);
    desenhar();
  }
  // Tela de título: uma das paisagens favoritas, sorteada a cada abertura.
  const TITULOS = [
    { local: { id: 3, tipo: "selvagem", bioma: "montanha" }, mundo: { periodo_n: 3, clima_id: "neve" } },
    { local: { id: 8, tipo: "selvagem", bioma: "floresta" }, mundo: { periodo_n: 2, clima_id: "chuva" } },
    { local: { id: 5, tipo: "selvagem", bioma: "cidadela" }, mundo: { periodo_n: 2, clima_id: "limpo" } },
    { local: { id: 12, tipo: "vila", bioma: "planicie" }, mundo: { periodo_n: 3, clima_id: "neve" } },
  ];
  /** Cor do alto do céu da paisagem atual: na tela de título ela pinta a página inteira acima da vista. */
  function corDoCeu() { return fundo ? fundo.getContext("2d").getImageData(0, 0, 1, 1).data.slice(0, 3) : [4, 5, 12]; }
  function titulo() {
    const t = TITULOS[Math.floor(Math.random() * TITULOS.length)];
    atualizar({ local: t.local, mundo: Object.assign({ escuro: false }, t.mundo) });
    return corDoCeu();
  }

  /** A câmera vai até o prédio (em dobro, centrada nele ou no ponto `foco` dele: no templo, a cruz no alto) ou volta
   *  à vila inteira (id nulo), num pontilhado. */
  function focar(id) {
    const p = id && predios.find((x) => x.id === id);
    const [fx, fy] = p ? p.foco || [p.x + p.w / 2, p.y + p.h / 2] : [0, 0];
    const para = p ? { s: 2, x: Math.max(0, Math.min(W / 2, Math.round(fx - W / 4))), y: Math.max(0, Math.min(H / 2, Math.round(fy - H / 4))) } : { s: 1, x: 0, y: 0 };
    if (camera.s === para.s && camera.x === para.x && camera.y === para.y) return;
    camera.de = { x: camera.x, y: camera.y, s: camera.s }; camera.inicio = performance.now();
    Object.assign(camera, para);
    if (!ctx || !estado) { camera.de = null; return; }
    const passo = () => { desenhar(); if (camera.de) requestAnimationFrame(passo); };
    requestAnimationFrame(passo);
  }
  function destacar(id) { if (destaque !== id) { destaque = id; desenhar(); } }
  /** Os prédios clicáveis da paisagem atual (só na vila), em pixels da arte (320x72). */
  function listaPredios() { return predios.map(({ id, nome, x, y, w, h, balao }) => ({ id, nome, x, y, w, h, balao })); }

  return { atualizar, titulo, corDoCeu, amanhecer, predios: listaPredios, destacar, focar, LARGURA: W, ALTURA: H };
})();
