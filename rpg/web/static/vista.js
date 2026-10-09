/* Vista: uma paisagem em pixel art (320x72) gerada para cada lugar, com céu do período do dia, clima, silhuetas do
   bioma e partículas (chuva, neve, névoa, fumaça, estrelas, corvos). Minimalista e melancólica: silhuetas em poucas
   camadas, o céu em faixas pontilhadas (Bayer), o sol morno com um halo só e fiapos de nuvem atravessando. */
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
  let nuvens = [], particulas = [], fumacas = [], estrelas = [], aves = [], relampago = 0, corDaNevoa = "#c8ccd4";

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
    // O sol (ou a lua): um disco morno, a metade de baixo um tom abaixo, e um halo de um anel só, pontilhado.
    if (["limpo", "neve"].includes(clima) || p === 3) {
      const [sx, sy, raio, cor, baixo] = ASTROS[p], halo = mix(bandas[bandas.length - 2], cor, 0.45);
      for (let y = sy - raio - 6; y <= sy + raio + 6; y++) for (let x = sx - raio - 6; x <= sx + raio + 6; x++) {
        const d = Math.hypot(x - sx, y - sy);
        if (d <= raio) px(c, x, y, 1, 1, y > sy + raio / 3 && pont(x, y, 8) ? baixo : cor);
        else if (d < raio + 5 && pont(x, y, Math.round(9 - (d - raio) * 1.6))) px(c, x, y, 1, 1, halo);
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
    const LUZ_JANELA = "#e8a050";
    fumacas = []; aves = [];
    const corvos = (n, y0, y1) => { for (let i = 0; i < n; i++) aves.push({ x: r() * W, y: y0 + r() * (y1 - y0), v: 0.15 + r() * 0.2, f: Math.floor(r() * 8) }); };
    corDaNevoa = mix(horizonte, "#c8ccd4", 0.3);
    // A névoa rasteira de cada bioma, um tom acima da camada de trás (com o clima de névoa, a do clima já basta).
    const bruma = mix(longe, horizonte, 0.5), forcaBruma = e.mundo.clima_id === "nevoa" ? 0 : 1;
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
      nevoa(c, 42, 52, bruma, 4 * forcaBruma);
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
      nevoa(c, 47, 55, bruma, 4 * forcaBruma);
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
      nevoa(c, 48, 56, bruma, 3 * forcaBruma);
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
    } else {  // vila: casas de telhados variados, a igreja, a forca da praça, a cerca e a fumaça das chaminés
      silhueta(c, perfil(r, 42, 4, 0.5), longe);
      const telha = mix(meio, "#5a1a10", 0.35), janela = (k) => (acesa && k % 3 !== 2 ? LUZ_JANELA : null);
      [[8, 58, 14, 10, false], [34, 57, 11, 8, true], [78, 58, 16, 11, false], [124, 57, 12, 8, true],
        [194, 58, 15, 10, false], [232, 57, 11, 7, true], [264, 58, 18, 11, false], [298, 57, 13, 9, true]]
        .forEach(([x, base, w, h, alto], k) => {
          const ch = casa(c, x, base, w, h, alto, meio, telha, janela(k));
          if (r() < 0.6) fumacas.push({ x: ch[0], y: ch[1], t: r() * 20 });
        });
      px(c, 150, 40, 24, 18, meio);
      for (let i = 0; i < 9; i++) px(c, 149 + i, 39 - i, 26 - i * 2, 1, telha);
      px(c, 166, 18, 8, 22, meio); for (let i = 0; i < 5; i++) px(c, 165 + i, 18 - i * 2, 10 - i * 2, 2, telha);
      px(c, 169, 4, 1, 6, meio); px(c, 167, 6, 5, 1, meio);
      px(c, 169, 24, 2, 3, "#0d0b0a"); px(c, 161, 51, 4, 7, "#0d0b0a");
      if (acesa) { px(c, 156, 45, 2, 4, LUZ_JANELA); px(c, 166, 45, 2, 4, LUZ_JANELA); }
      px(c, 104, 40, 2, 18, perto); px(c, 104, 40, 12, 2, perto);  // a forca
      px(c, 113, 42, 1, 3, mix(perto, "#8a7a6a", 0.4)); px(c, 112, 45, 3, 5, perto); px(c, 112, 50, 1, 3, perto); px(c, 114, 50, 1, 3, perto);
      px(c, 0, 58, W, H - 58, chao);
      for (let x = 0; x < W; x += 5) px(c, x, 55, 1, 4, perto);
      px(c, 0, 56, W, 1, perto);
    }
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
    const n = fechado ? 8 : clima === "limpo" && r() < 0.4 ? 0 : 4;
    for (let i = 0; i < n; i++) nuvens.push({ x: r() * (W + 80), y: 5 + r() * 36, w: 40 + r() * 80, v: 0.04 + r() * 0.08, esp: fechado && r() < 0.5 ? 3 : 2, cor: corNuvem });
    bioma(frente.getContext("2d"), e, r, bandas);
    estrelas = [];
    if (p === 3 && !["chuva", "tempestade", "nublado", "nevoa"].includes(clima)) {
      for (let i = 0; i < 40; i++) estrelas.push({ x: Math.floor(r() * W), y: Math.floor(r() * 34), f: r() * 10 });
    }
    particulas = [];
    const qtd = { chuva: 70, tempestade: 120, neve: 60 }[clima] || 0;
    for (let i = 0; i < qtd; i++) particulas.push({ x: r() * W, y: r() * H, v: clima === "neve" ? 0.3 + r() * 0.4 : 3 + r() * 2 });
  }

  function desenhar() {
    if (!estado || !ctx) return;
    quadro++;
    ctx.drawImage(fundo, 0, 0);
    const clima = estado.mundo.clima_id;
    estrelas.forEach((s) => { if ((quadro + s.f) % 14 > 2) px(ctx, s.x, s.y, 1, 1, (quadro + s.f) % 30 < 4 ? "#ffffff" : "#9aa4c0"); });
    nuvens.forEach((n) => {
      n.x = (n.x + n.v) % (W + n.w);
      const x = Math.floor(n.x - n.w);
      px(ctx, x, n.y, n.w, 1, n.cor); px(ctx, x + 6, n.y - 1, n.w - 18, 1, n.cor);
      if (n.esp === 3) px(ctx, x + n.w / 4, n.y - 2, n.w / 3, 1, n.cor);
    });
    ctx.drawImage(frente, 0, 0);
    aves.forEach((a, k) => {  // corvos, devagar, batendo as asas
      a.x = (a.x + a.v) % (W + 20);
      const x = Math.floor(a.x) - 10, y = Math.round(a.y + Math.sin((quadro + k * 9) / 12)), asa = (Math.floor(quadro / 4) + a.f) % 2, cor = "#0c0606";
      px(ctx, x, y, 1, 1, cor); px(ctx, x - 2, y - asa, 2, 1, cor); px(ctx, x + 1, y - asa, 2, 1, cor);
    });
    fumacas.forEach((f) => {  // fumaça pontilhada, rareando enquanto sobe
      for (let i = 0; i < 6; i++) {
        const t = (quadro * 0.5 + f.t + i * 3) % 18, x = f.x + Math.round(Math.sin((t + i) / 3) * 2 + t * 0.3), y = Math.round(f.y - t);
        if (pont(x, y, Math.round(12 - t * 0.6))) px(ctx, x, y, 2, 2, "#8a8288");
      }
    });
    if (clima === "nevoa") {
      for (let i = 0; i < 3; i++) nevoa(ctx, 30 + i * 12, 38 + i * 12, corDaNevoa, 4, 0, W, quadro * (0.3 + i * 0.1));
    }
    particulas.forEach((p) => {
      if (clima === "neve") { p.y += p.v; p.x += Math.sin((quadro + p.y) / 9) * 0.3; px(ctx, p.x, p.y, 1, 1, "#f0f4ff"); }
      else { p.y += p.v; p.x -= p.v * 0.4; px(ctx, p.x, p.y, 1, 3, "rgba(170,190,220,0.7)"); }
      if (p.y > H) { p.y = -3; p.x = Math.random() * (W + 30); }
    });
    if (clima === "tempestade") {
      if (relampago > 0) { ctx.fillStyle = `rgba(230,235,255,${relampago / 6})`; ctx.fillRect(0, 0, W, H); relampago--; }
      else if (Math.random() < 0.006) relampago = 5;
    }
    if (estado.mundo.escuro) { ctx.fillStyle = "rgba(0,0,0,0.55)"; ctx.fillRect(0, 0, W, H); }
    if (aurora) pintarAurora();
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
    if (k !== chave) { chave = k; preparar(e); }
    if (!timer) timer = setInterval(() => { if (!document.hidden) desenhar(); }, 100);
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

  return { atualizar, titulo, corDoCeu, amanhecer };
})();
