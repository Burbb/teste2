/* Mapa em pixel art: terreno colorido pelo bioma de cada região conhecida (o resto é névoa),
   estradas pontilhadas, ícones dos lugares e botões clicáveis por cima para viajar. */
"use strict";

const MapaPx = (() => {
  const COR_BIOMA = { floresta: [38, 62, 34], pantano: [30, 58, 56], montanha: [64, 64, 72], planicie: [86, 74, 40],
    ruinas: [60, 42, 72], cidadela: [80, 18, 20], vila: [84, 56, 30] };
  const cache = {};

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

  function terreno(nos, vb, W, H) {
    const chave = nos.map((n) => `${n.id}${n.bioma}${n.tipo}`).join(",") + vb.map((v) => v.toFixed(1)).join(",") + W;
    if (cache[chave]) return cache[chave];
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    const x = c.getContext("2d");
    const img = x.createImageData(W, H);
    const pos = nos.map((n) => [(n.x * 100 - vb[0]) / vb[2] * W, (n.y * 50 - vb[1]) / vb[3] * H, n]);
    const alcance = (W / vb[2]) * 13;
    let s = 12345;
    const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    for (let py = 0; py < H; py++) {
      for (let px = 0; px < W; px++) {
        let melhor = null, d2 = Infinity;
        for (const p of pos) {
          const dx = p[0] - px, dy = p[1] - py, d = dx * dx + dy * dy;
          if (d < d2) { d2 = d; melhor = p; }
        }
        const d = Math.sqrt(d2);
        const base = melhor ? (COR_BIOMA[melhor[2].tipo === "vila" ? "vila" : melhor[2].bioma] || [40, 34, 28]) : [20, 16, 12];
        let t = Math.max(0, 1 - d / alcance);
        // névoa pontilhada nas bordas do conhecido
        if (t > 0 && t < 0.35 && ((px + py) % 2 === 0)) t *= 0.4;
        const ruido = rnd() * 10 - 5;
        const fundo = [18, 14, 11];
        const k = (py * W + px) * 4;
        for (let i = 0; i < 3; i++) img.data[k + i] = Math.max(0, Math.min(255, fundo[i] + (base[i] - fundo[i]) * t * (melhor && melhor[2].visitado ? 1 : 0.6) + ruido));
        img.data[k + 3] = 255;
      }
    }
    x.putImageData(img, 0, 0);
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
    mapa.nos.forEach((n) => {
      const [px, py] = conv(n);
      const esq = (px / W) * 100, topo = (py / H) * 100;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "no-btn" + (n.atual ? " atual" : "") + (clic.has(n.id) ? " clicavel" : "");
      b.style.left = esq + "%"; b.style.top = topo + "%";
      const nv = n.nivel ? ` · inimigos Nv.${n.nivel}` : "";
      b.title = `${n.nome} — ${n.descricao}${nv}${n.distancia ? ` · ${n.distancia} trecho(s) daqui` : ""}${clic.has(n.id) ? "\nClique para viajar" : ""}`;
      if (clic.has(n.id) && opts.aoClicar) b.addEventListener("click", (ev) => { ev.stopPropagation(); opts.aoClicar(n.id); });
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
  return { criar, sprite };
})();
