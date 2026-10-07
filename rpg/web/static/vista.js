/* Vista: uma paisagem em pixel art (320x72) gerada para cada lugar, com céu do período do dia,
   clima, silhuetas do bioma e partículas (chuva, neve, fumaça, estrelas). */
"use strict";

const Vista = (() => {
  const W = 320, H = 72;
  const CEUS = [
    ["#2c4470", "#45648f", "#7a90b0", "#c09a80", "#e8b88a"],
    ["#24508c", "#33649e", "#4f80b6", "#79a4c8", "#a8c4d6"],
    ["#22163a", "#43264a", "#82363e", "#bc5630", "#ec8c3c"],
    ["#04050c", "#080b1a", "#0d1328", "#121a33", "#18223f"],
  ];
  let canvas, ctx, fundo, chave = "", estado = null, quadro = 0, timer = null;
  let nuvens = [], particulas = [], fumacas = [], estrelas = [], relampago = 0;

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

  function ceu(c, e, r) {
    const p = e.mundo.periodo_n;
    let bandas = CEUS[p].slice();
    const clima = e.mundo.clima_id;
    if (["chuva", "tempestade", "nublado"].includes(clima)) bandas = bandas.map((b) => mix(b, "#3a3f48", clima === "tempestade" ? 0.75 : 0.55));
    if (clima === "nevoa") bandas = bandas.map((b) => mix(b, "#8a9098", 0.5));
    if (clima === "neve") bandas = bandas.map((b) => mix(b, "#a8b0bc", 0.45));
    if (e.local.bioma === "cidadela") bandas = bandas.map((b, i) => mix(b, i > 2 ? "#a01818" : "#2a0508", 0.7));
    const altura = 46, faixa = altura / bandas.length;
    bandas.forEach((cor, i) => {
      const y0 = Math.round(i * faixa), y1 = Math.round((i + 1) * faixa);
      px(c, 0, y0, W, y1 - y0, cor);
      if (i < bandas.length - 1) {  // pontilhado entre faixas (dithering)
        for (let x = 0; x < W; x += 2) px(c, x + (y1 % 2), y1 - 1, 1, 1, bandas[i + 1]);
        for (let x = 1; x < W; x += 4) px(c, x, y1 - 2, 1, 1, bandas[i + 1]);
      }
    });
    px(c, 0, altura, W, H - altura, bandas[bandas.length - 1]);
    // Sol ou lua
    if (["limpo", "neve"].includes(clima) || p === 3) {
      const [sx, sy, cor, raio] = [[60, 30, "#ffe8a0", 7], [210, 12, "#fff6c8", 6], [250, 36, "#ff9a4a", 10], [70, 14, "#e8ecf4", 5]][p];
      for (let y = -raio; y <= raio; y++) for (let x = -raio; x <= raio; x++) {
        if (x * x + y * y <= raio * raio) px(c, sx + x, sy + y, 1, 1, cor);
      }
      if (p === 3) for (let y = -raio; y <= raio; y++) for (let x = -raio; x <= raio; x++) {
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

  function pinheiro(c, x, y, h, cor) {
    for (let i = 0; i < h; i++) {
      const larg = Math.max(1, Math.floor((i / h) * (h / 2.2))) + (i % 3 === 0 ? 1 : 0);
      px(c, x - larg, y - h + i, larg * 2 + 1, 1, cor);
    }
    px(c, x, y, 1, 2, cor);
  }
  function arvoreSeca(c, x, y, h, cor) {
    px(c, x, y - h, 1, h, cor);
    px(c, x - 2, y - h + 2, 2, 1, cor); px(c, x - 3, y - h + 1, 1, 1, cor);
    px(c, x + 1, y - h + 4, 3, 1, cor); px(c, x + 4, y - h + 3, 1, 1, cor);
  }
  function casa(c, x, y, cor, telhado, janela, acesa) {
    px(c, x, y - 7, 10, 7, cor);
    for (let i = 0; i < 5; i++) px(c, x - 1 + i, y - 8 - i, 12 - i * 2, 1, telhado);
    px(c, x + 2, y - 5, 2, 2, acesa ? janela : "#0d0b0a");
    px(c, x + 6, y - 4, 2, 4, "#0d0b0a");
    px(c, x + 7, y - 13, 2, 4, cor);
    return [x + 8, y - 14];
  }

  function bioma(c, e, r, bandas) {
    const p = e.mundo.periodo_n, noite = p === 3;
    const horizonte = bandas[bandas.length - 1];
    const escuro = (t) => mix(horizonte, "#050404", t);
    const b = e.local.tipo === "vila" ? "vila" : e.local.bioma;
    const longe = escuro(0.45), meio = escuro(0.65), perto = escuro(0.82), chao = escuro(0.9);
    fumacas = [];
    if (b === "montanha") {
      const picos = perfil(r, 26, 18, 2.6);
      silhueta(c, picos, longe);
      picos.forEach((y, x) => { if (y < 22) px(c, x, y, 1, Math.max(1, 22 - y) * 0.6 + 1, mix(longe, "#e8ecf4", noite ? 0.35 : 0.75)); });
      silhueta(c, perfil(r, 46, 10, 1.6), meio);
      silhueta(c, perfil(r, 60, 4, 0.8), chao);
    } else if (b === "floresta") {
      silhueta(c, perfil(r, 40, 6, 0.8), longe);
      for (let x = -4; x < W; x += 5 + Math.floor(r() * 4)) pinheiro(c, x, 50 + Math.floor(r() * 4), 10 + Math.floor(r() * 8), meio);
      silhueta(c, perfil(r, 58, 3, 0.6), chao);
      for (let x = 0; x < W; x += 9 + Math.floor(r() * 10)) pinheiro(c, x, 66, 16 + Math.floor(r() * 10), perto);
    } else if (b === "pantano") {
      silhueta(c, perfil(r, 44, 3, 0.5), longe);
      px(c, 0, 52, W, H - 52, mix(horizonte, "#0a1a18", 0.6));
      for (let y = 53; y < H; y += 3) for (let x = (y * 7) % 11; x < W; x += 11) px(c, x, y, 4, 1, mix(horizonte, "#5a7a78", 0.4));
      for (let x = 5; x < W; x += 18 + Math.floor(r() * 24)) arvoreSeca(c, x, 54, 12 + Math.floor(r() * 10), perto);
      for (let x = 0; x < W; x += 3) if (r() < 0.5) px(c, x, 49 + Math.floor(r() * 4), 1, 4 + Math.floor(r() * 3), meio);
    } else if (b === "planicie") {
      silhueta(c, perfil(r, 42, 5, 0.6), longe);
      silhueta(c, perfil(r, 52, 4, 0.5), meio);
      for (let x = 0; x < W; x += 2) if (r() < 0.6) px(c, x, 55 + Math.floor(r() * 10), 1, 2, mix(meio, "#8a9a4a", noite ? 0.15 : 0.4));
      for (let x = 20; x < W; x += 60 + Math.floor(r() * 60)) { px(c, x, 44, 1, 8, perto); px(c, x - 3, 40, 7, 4, perto); px(c, x - 2, 38, 5, 2, perto); }
      silhueta(c, perfil(r, 64, 2, 0.4), chao);
    } else if (b === "ruinas") {
      silhueta(c, perfil(r, 44, 5, 0.6), longe);
      for (let x = 10; x < W; x += 22 + Math.floor(r() * 18)) {
        const h = 8 + Math.floor(r() * 18);
        px(c, x, 54 - h, 4, h, meio); px(c, x - 1, 54 - h, 6, 2, meio);
        if (r() < 0.4) { px(c, x + 4, 54 - h + 2, 12, 2, meio); px(c, x + 14, 54 - h + 2, 4, h - 2, meio); }
      }
      silhueta(c, perfil(r, 58, 3, 0.5), chao);
    } else if (b === "cidadela") {
      silhueta(c, perfil(r, 46, 4, 0.5), longe);
      const cx = 160;
      px(c, cx - 40, 30, 80, 30, perto);
      [[-44, 16, 10], [-14, 8, 12], [16, 12, 10], [36, 20, 10]].forEach(([dx, topo, larg]) => {
        px(c, cx + dx, topo, larg, 40, perto);
        for (let i = 0; i < larg; i += 3) px(c, cx + dx + i, topo - 2, 2, 2, perto);
        px(c, cx + dx + Math.floor(larg / 2) - 1, topo + 8, 2, 3, "#ff3020");
      });
      px(c, cx - 4, 46, 8, 14, "#ff4020");
      silhueta(c, perfil(r, 60, 2, 0.4), chao);
    } else {  // vila
      silhueta(c, perfil(r, 42, 4, 0.5), longe);
      const acesa = p >= 2;
      for (let x = 8; x < W - 10; x += 22 + Math.floor(r() * 16)) {
        const base = 56 + Math.floor(r() * 3);
        const chamine = casa(c, x, base, meio, mix(meio, "#5a1a10", 0.35), "#ffc860", acesa);
        if (r() < 0.6) fumacas.push({ x: chamine[0], y: chamine[1], t: r() * 20 });
      }
      px(c, 0, 58, W, H - 58, chao);
      for (let x = 0; x < W; x += 6) px(c, x, 57, 1, 4, perto);
    }
  }

  function preparar(e) {
    fundo = document.createElement("canvas");
    fundo.width = W; fundo.height = H;
    const c = fundo.getContext("2d");
    const r = rng(e.local.id * 97 + 13);
    const bandas = ceu(c, e, r);
    bioma(c, e, r, bandas);
    const clima = e.mundo.clima_id;
    nuvens = [];
    if (clima !== "limpo" || r() < 0.6) {
      const n = clima === "limpo" ? 3 : 7;
      for (let i = 0; i < n; i++) nuvens.push({ x: r() * W, y: 4 + r() * 22, w: 14 + r() * 30, v: 0.08 + r() * 0.15,
        cor: mix(bandas[1], e.mundo.periodo_n === 3 ? "#2a3048" : "#e8ecf4", clima === "limpo" ? 0.5 : 0.25) });
    }
    estrelas = [];
    if (e.mundo.periodo_n === 3 && !["chuva", "tempestade", "nublado", "nevoa"].includes(clima)) {
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
      px(ctx, x, n.y, n.w, 3, n.cor); px(ctx, x + 3, n.y - 2, n.w - 8, 2, n.cor); px(ctx, x + 6, n.y - 3, n.w / 3, 1, n.cor);
    });
    fumacas.forEach((f) => {
      for (let i = 0; i < 6; i++) {
        const t = (quadro * 0.5 + f.t + i * 3) % 18;
        px(ctx, f.x + Math.round(Math.sin((t + i) / 3) * 2), f.y - t, 2, 2, `rgba(160,150,140,${0.5 - t / 40})`);
      }
    });
    if (clima === "nevoa") {
      for (let i = 0; i < 4; i++) {
        const y = 30 + i * 10, desl = (quadro * (0.3 + i * 0.1)) % 40;
        ctx.fillStyle = "rgba(200,205,215,0.18)";
        for (let x = -40; x < W; x += 40) ctx.fillRect(Math.floor(x + desl), y, 26, 3);
      }
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
    { local: { id: 5, tipo: "selvagem", bioma: "cidadela" }, mundo: { periodo_n: 3, clima_id: "limpo" } },
    { local: { id: 12, tipo: "vila", bioma: "planicie" }, mundo: { periodo_n: 3, clima_id: "neve" } },
  ];
  /** Cor do alto do céu da paisagem atual: na tela de título ela pinta a página inteira acima da vista. */
  function corDoCeu() { return fundo ? fundo.getContext("2d").getImageData(0, 0, 1, 1).data.slice(0, 3) : [4, 5, 12]; }
  function titulo() {
    const t = TITULOS[Math.floor(Math.random() * TITULOS.length)];
    atualizar({ local: t.local, mundo: Object.assign({ escuro: false }, t.mundo) });
    return corDoCeu();
  }

  return { atualizar, titulo, corDoCeu };
})();
