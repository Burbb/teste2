/* Mapa em pixel art: terreno colorido pelo bioma de cada região conhecida (o resto é névoa),
   estradas pontilhadas, ícones dos lugares e botões clicáveis por cima para viajar. */
"use strict";

const MapaPx = (() => {
  // Mesma paleta e mesmo pontilhado da vista: três tons por bioma, tingidos pela hora do dia.
  const PALETA = {
    floresta: ["#142618", "#24402a", "#3e6236"], pantano: ["#122624", "#1f3d38", "#3d6052"],
    montanha: ["#2e2f3a", "#4d4f5e", "#858b9c"], planicie: ["#3e3618", "#5e5326", "#8a7c40"],
    ruinas: ["#251d2e", "#3d3046", "#5e5068"], cidadela: ["#240606", "#420c0e", "#7a1c16"],
    vila: ["#33240f", "#523a1e", "#7e6034"],
  };
  const TINTA = [["#c09a80", 0.12], [null, 0], ["#82363e", 0.2], ["#0d1328", 0.5]];  // manhã, tarde, crepúsculo, noite
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const NEVOA = "#0f0c0a";
  let ambiente = { periodo_n: 1, clima_id: "limpo", corrupcao: 0 };
  const cache = {};

  function hex(c) { return [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16)); }
  function mix(a, b, t) {
    const x = hex(a), y = hex(b);
    return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join("");
  }
  function tons(n) {
    const b = n.tipo === "vila" ? "vila" : n.bioma;
    let t = (PALETA[b] || PALETA.planicie).slice();
    const [cor, f] = TINTA[ambiente.periodo_n] || TINTA[1];
    if (cor) t = t.map((c) => mix(c, cor, f));
    if (!n.visitado && !n.atual) t = t.map((c) => mix(c, NEVOA, 0.35));
    return t;
  }
  // Ruído suave (manchas) para o pontilhado ter "relevo", como as faixas do céu da vista.
  function ruido(x, y, sem) {
    const h = (a, b) => { let v = Math.sin(a * 127.1 + b * 311.7 + sem * 74.7) * 43758.5453; return v - Math.floor(v); };
    const xi = Math.floor(x), yi = Math.floor(y), fx = x - xi, fy = y - yi;
    const a = h(xi, yi), b = h(xi + 1, yi), c = h(xi, yi + 1), d = h(xi + 1, yi + 1);
    const ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
    return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
  }

  function sprite(n) {
    if (n.covil === "ativo") return "covil";
    if (n.covil === "vencido") return "vencido";
    if (n.tipo === "vila") return "vila";
    return n.bioma;
  }

  function enquadrar(nos, grande) {
    let vb = [-6, -5, 112, 64];
    if (nos.length) {
      const xs = nos.map((n) => n.x * 100), ys = nos.map((n) => n.y * 50);
      const minW = grande ? 70 : 46, minH = grande ? 40 : 26;
      let w = Math.max(Math.max(...xs) - Math.min(...xs) + 20, minW), h = Math.max(Math.max(...ys) - Math.min(...ys) + 16, minH);
      if (w / h > 1.75) h = w / 1.75; else w = h * 1.75;
      const cx = (Math.max(...xs) + Math.min(...xs)) / 2, cy = (Math.max(...ys) + Math.min(...ys)) / 2;
      vb = [cx - w / 2, cy - h / 2, w, h];
    }
    return vb;
  }

  // Silhuetas miúdas de cada bioma (as mesmas formas da vista, em escala de mapa).
  function enfeite(x, b, px, py, t, r) {
    const p = (dx, dy, w, h, c) => { x.fillStyle = c; x.fillRect(px + dx, py + dy, w, h); };
    if (b === "floresta") { p(0, -4, 1, 1, t[0]); p(-1, -3, 3, 1, t[0]); p(-1, -2, 3, 1, t[0]); p(-2, -1, 5, 1, t[0]); p(0, 0, 1, 1, t[0]); p(0, -3, 1, 1, t[2]); }
    else if (b === "montanha") {
      for (let i = 0; i < 4; i++) p(-i, -3 + i, 1 + i * 2, 1, i < 2 ? "#dfe4ee" : t[0]);
      p(1, -1, 2, 2, t[1]);
    } else if (b === "pantano") { if (r < 0.5) { p(-2, 0, 4, 1, t[2]); p(0, 2, 3, 1, t[2]); } else { p(0, -3, 1, 4, t[0]); p(2, -2, 1, 3, t[0]); p(-1, -1, 1, 2, t[0]); } }
    else if (b === "planicie") { p(0, -1, 1, 1, t[2]); p(-1, -2, 1, 1, t[2]); p(1, -2, 1, 1, t[2]); }
    else if (b === "ruinas") { p(0, -4, 2, 5, t[0]); p(-1, -4, 4, 1, t[0]); if (r < 0.4) { p(2, -3, 3, 1, t[0]); p(4, -3, 1, 4, t[0]); } }
    else if (b === "cidadela") { p(0, -4, 1, 5, "#120303"); p(2, -2, 1, 3, "#120303"); p(1, -1, 1, 1, "#ff3020"); }
    else if (b === "vila") { p(-2, -2, 5, 3, t[0]); p(-1, -3, 3, 1, "#5a1a10"); p(0, -1, 1, 1, ambiente.periodo_n >= 2 ? "#ffc860" : t[1]); }
  }

  function terreno(nos, vb, W, H) {
    const chave = nos.map((n) => `${n.id}${n.bioma}${n.tipo}${n.visitado ? 1 : 0}`).join(",") + vb.map((v) => v.toFixed(1)).join(",") + W +
      ambiente.periodo_n + ambiente.clima_id;
    if (cache[chave]) return cache[chave];
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    const x = c.getContext("2d");
    const img = x.createImageData(W, H);
    const pos = nos.map((n) => [(n.x * 100 - vb[0]) / vb[2] * W, (n.y * 50 - vb[1]) / vb[3] * H, n]);
    const paletas = pos.map((p) => tons(p[2]).map(hex));
    const nevoa = hex(NEVOA);
    const alcance = (W / vb[2]) * 13;
    const escala = W / 14;
    const dono = new Int16Array(W * H).fill(-1);
    for (let py = 0; py < H; py++) {
      for (let px = 0; px < W; px++) {
        let i1 = -1, d1 = Infinity, d2 = Infinity;
        pos.forEach((p, i) => {
          const dx = p[0] - px, dy = p[1] - py, d = dx * dx + dy * dy;
          if (d < d1) { d2 = d1; d1 = d; i1 = i; } else if (d < d2) d2 = d;
        });
        const k = (py * W + px) * 4;
        const bayer = BAYER[(py % 4) * 4 + (px % 4)] / 16;
        let cor = nevoa;
        if (i1 >= 0) {
          // borda recortada (como um litoral), não um círculo
          const t = Math.max(0, 1 - Math.sqrt(d1) / alcance + (ruido(px / escala * 1.6, py / escala * 1.6, 99) - 0.5) * 0.45);
          // névoa pontilhada nas bordas do que você conhece
          if (t * 2.2 > bayer + 0.05) {
            const tom = paletas[i1];
            // manchas grandes em três tons; o pontilhado só aparece na passagem de um tom para o outro
            const n = ruido(px / escala, py / escala, pos[i1][2].id) * 0.8 + ruido(px / (escala / 2.5), py / (escala / 2.5), 7) * 0.2;
            const v = n + (bayer - 0.5) * 0.1;
            cor = v > 0.64 ? tom[2] : v > 0.34 ? tom[1] : tom[0];
            if (Math.sqrt(d2) - Math.sqrt(d1) < 1.2) cor = tom[0];  // fronteira entre regiões
            dono[py * W + px] = t > 0.35 ? i1 : -1;
          }
        }
        img.data[k] = cor[0]; img.data[k + 1] = cor[1]; img.data[k + 2] = cor[2]; img.data[k + 3] = 255;
      }
    }
    x.putImageData(img, 0, 0);
    // enfeites do bioma, só onde a região é visível
    let s = 4242;
    const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const passo = Math.max(6, Math.round(W / 40));
    for (let py = 4; py < H - 1; py += passo) {
      for (let px = 3; px < W - 3; px += passo) {
        const jx = px + Math.floor(rnd() * passo), jy = py + Math.floor(rnd() * passo);
        if (jx >= W || jy >= H) continue;
        const i = dono[jy * W + jx];
        if (i < 0 || rnd() < 0.35) continue;
        const n = pos[i][2];
        if (Math.hypot(pos[i][0] - jx, pos[i][1] - jy) < 9) continue;  // deixa espaço para o ícone do lugar
        enfeite(x, n.tipo === "vila" ? "vila" : n.bioma, jx, jy, tons(n), rnd());
      }
    }
    if (ambiente.clima_id === "neve") {  // neve assentada nos enfeites: alguns pontos claros, sem chiado
      x.fillStyle = "rgba(240,244,255,0.55)";
      for (let i = 0; i < W * H / 260; i++) x.fillRect(Math.floor(rnd() * W), Math.floor(rnd() * H), 1, 1);
    }
    cache[chave] = c;
    return c;
  }

  function linha(x, x0, y0, x1, y1, cor, pontilhada) {
    x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1);
    const dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    let err = dx + dy, i = 0;
    x.fillStyle = cor;
    for (;;) {
      if (!pontilhada || i % 3 !== 2) x.fillRect(x0, y0, 1, 1);
      if (x0 === x1 && y0 === y1) break;
      const e2 = 2 * err;
      if (e2 >= dy) { err += dy; x0 += sx; }
      if (e2 <= dx) { err += dx; y0 += sy; }
      i++;
    }
  }

  /** Cria o mapa. opts: grande, clicaveis (Set de ids), aoClicar(id), nivelHeroi */
  function criar(mapa, opts = {}) {
    const grande = !!opts.grande;
    const W = grande ? 352 : 224, H = Math.round(W / 1.75);
    const vb = enquadrar(mapa.nos, grande);
    const conv = (n) => [(n.x * 100 - vb[0]) / vb[2] * W, (n.y * 50 - vb[1]) / vb[3] * H];
    const caixa = document.createElement("div");
    caixa.className = "mapa-px" + (grande ? " grande" : "");
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    const x = c.getContext("2d");
    x.drawImage(terreno(mapa.nos, vb, W, H), 0, 0);
    const porId = {};
    mapa.nos.forEach((n) => { porId[n.id] = n; });
    mapa.estradas.forEach((e) => {
      const a = porId[e.a], b = porId[e.b];
      if (!a || !b) return;
      const [x0, y0] = conv(a), [x1, y1] = conv(b);
      const cor = e.atual ? "#f2c94c" : e.percorrida ? "#b8a888" : "#5a4f40";
      linha(x, x0 + 1, y0 + 1, x1 + 1, y1 + 1, "#0d0b0a", true);
      linha(x, x0, y0, x1, y1, cor, !e.percorrida && !e.atual);
    });
    const tam = grande ? 16 : 14;
    mapa.nos.forEach((n) => {
      const [px, py] = conv(n);
      const spr = Sprites.canvas(sprite(n));
      x.globalAlpha = n.visitado || n.atual ? 1 : 0.6;
      if (spr) x.drawImage(spr, Math.round(px - tam / 2), Math.round(py - tam / 2), tam, tam);
      x.globalAlpha = 1;
    });
    caixa.appendChild(c);
    const clic = opts.clicaveis || new Set();
    const marcas = opts.marcas || new Set();  // lugares com contrato: ganham um "!" de missão
    mapa.nos.forEach((n) => {
      const [px, py] = conv(n);
      const esq = (px / W) * 100, topo = (py / H) * 100;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "no-btn" + (n.atual ? " atual" : "") + (clic.has(n.id) ? " clicavel" : "") + (marcas.has(n.id) ? " contrato" : "");
      b.dataset.id = n.id;
      b.style.left = esq + "%"; b.style.top = topo + "%";
      const nv = n.nivel ? ` · inimigos Nv.${n.nivel}` : "";
      b.title = `${n.nome} — ${n.descricao}${nv}${n.distancia ? ` · ${n.distancia} trecho(s) daqui` : ""}${clic.has(n.id) ? "\nClique para viajar" : ""}`;
      if (clic.has(n.id) && opts.aoClicar) b.addEventListener("click", (ev) => { ev.stopPropagation(); opts.aoClicar(n.id); });
      if (marcas.has(n.id)) {
        // Elemento próprio (e não ::after, que o anel de "você está aqui" já usa): um selo "!" no canto do lugar.
        const m = document.createElement("span");
        m.className = "marca-contrato";
        m.textContent = "!";
        b.appendChild(m);
        b.title += "\nVocê tem um contrato aqui";
      }
      caixa.appendChild(b);
      if (grande || n.atual || clic.has(n.id)) {
        const r = document.createElement("span");
        const perigo = n.nivel && opts.nivelHeroi && n.nivel >= opts.nivelHeroi + 2;
        r.className = "rotulo-mapa" + (n.atual ? " atual" : "") + (perigo ? " perigo" : "") + (!n.visitado && !n.atual ? " apagado" : "");
        r.textContent = n.nome + (grande && n.nivel ? ` · Nv.${n.nivel}` : "");
        r.style.left = esq + "%";
        r.style.top = `calc(${topo}% + ${grande ? 14 : 11}px)`;
        caixa.appendChild(r);
      }
    });
    return caixa;
  }
  return { criar, sprite, ambiente(m) { if (m) ambiente = m; } };
})();
