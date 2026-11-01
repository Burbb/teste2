// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 6: o desenho do cenário (estradas, casas, muros, a muralha com
// as torres), das magias anunciadas, dos dardos, da Corrente Arcana e das silhuetas atrás das construções. Na vista do
// campo (de cima, com os corpos em três quartos), cada construção ocupa no chão exatamente o retângulo da colisão e
// sobe `alto` px para o norte: quem está atrás dela (ao norte) fica coberto; a construção fica translúcida quando há
// alguém atrás. Arte provisória, nas cores do jogo (pedra fria, reboco e madeira, telhado de barro escuro).

const COR = {
  estrada: "rgba(150,124,82,0.42)", estradaBorda: "rgba(110,88,58,0.35)",
  pedra: ["#8e8a80", "#6f6b63", "#55524c", "#3e3b37"], reboco: ["#c9b796", "#a8977a"], madeira: ["#6a4a2c", "#4a321e"],
  telha: ["#8a3f2c", "#6d2f22", "#a65038"], sombra: "rgba(10,14,8,0.32)",
};

export function desenharEstradas(g, m, cx, cy) {
  const c = m.cenario && m.cenario.def;
  if (!c || !c.estradas) return;
  for (const e of c.estradas) {
    g.fillStyle = COR.estrada; g.fillRect(e.x - cx, e.y - cy, e.w, e.h);
    g.fillStyle = COR.estradaBorda;
    if (e.w > e.h) { g.fillRect(e.x - cx, e.y - cy, e.w, 1); g.fillRect(e.x - cx, e.y + e.h - 1 - cy, e.w, 1); }
    else { g.fillRect(e.x - cx, e.y - cy, 1, e.h); g.fillRect(e.x + e.w - 1 - cx, e.y - cy, 1, e.h); }
  }
  // a sombra de cada construção no chão (para o leste e o sul, como a luz do campo)
  for (const o of m.cenario.obs) {
    g.fillStyle = COR.sombra;
    g.fillRect(o.x + 3 - cx, o.y + o.h - cy, o.w, 4);
    g.fillRect(o.x + o.w - cx, o.y + 3 - cy, 4, o.h);
  }
  // a brecha da muralha: entulho no chão
  for (const o of m.cenario.obs) if (o.tipo === "muralha" && o.y > 400 && o.y < 470) {
    g.fillStyle = "#6f6b63";
    for (let i = 0; i < 14; i++) g.fillRect(o.x - 6 + ((i * 7) % 26) - cx, o.y - 44 + ((i * 11) % 40) - cy, 2 + (i % 2), 2);
  }
}

/** As construções em ordem de profundidade (a base, a borda de baixo do retângulo). */
export function prediosOrdenados(m) {
  return (m.cenario ? m.cenario.obs : []).slice().sort((a, b) => a.y + a.h - (b.y + b.h));
}

/** Há alguém atrás desta construção (coberto pelo desenho dela)? */
export function temAtras(m, o) {
  const topo = o.y - o.alto - 12, base = o.y + o.h;
  for (const u of m.unidades) if (!u.morto && u.y < base && u.y > topo && u.x > o.x - 6 && u.x < o.x + o.w + 6) return true;
  return false;
}

export function desenharPredio(g, o, cx, cy, alfa = 1) {
  g.save();
  g.globalAlpha = alfa;
  const x = Math.round(o.x) - cx, y = Math.round(o.y) - cy, w = o.w, h = o.h, a = o.alto;
  if (o.tipo === "casa") {
    // a parede da frente (reboco e madeira) e o telhado por cima, inclinado para o norte
    const paredeA = Math.round(a * 0.55), telhadoA = h + a - paredeA;
    g.fillStyle = COR.reboco[0]; g.fillRect(x, y + h - paredeA, w, paredeA);
    g.fillStyle = COR.madeira[0];
    g.fillRect(x, y + h - paredeA, w, 2); g.fillRect(x, y + h - 2, w, 2);
    for (let i = 0; i <= w; i += Math.max(10, Math.floor(w / 4))) g.fillRect(x + Math.min(i, w - 2), y + h - paredeA, 2, paredeA);
    // a porta e uma janela
    g.fillStyle = COR.madeira[1]; g.fillRect(x + Math.floor(w / 2) - 3, y + h - 9, 6, 9);
    g.fillStyle = "#2a2a30"; g.fillRect(x + 5, y + h - paredeA + 4, 5, 4);
    // o telhado: do topo da parede até a borda de cima do retângulo, subindo `alto`
    const ty = y + h - paredeA - telhadoA;
    g.fillStyle = COR.telha[0]; g.fillRect(x - 2, ty, w + 4, telhadoA);
    g.fillStyle = COR.telha[1];
    for (let j = ty + 3; j < ty + telhadoA; j += 4) g.fillRect(x - 2, j, w + 4, 1);
    g.fillStyle = COR.telha[2]; g.fillRect(x - 2, ty, w + 4, 2);
    g.fillStyle = COR.madeira[1]; g.fillRect(x - 2, ty + telhadoA - 1, w + 4, 1);
  } else if (o.tipo === "muro") {
    // o muro baixo de pedra solta: só o alto dele, com as pedras
    g.fillStyle = COR.pedra[1]; g.fillRect(x, y - a + h, w, a);
    g.fillStyle = COR.pedra[0];
    for (let i = 0; i < w; i += 6) g.fillRect(x + i, y - a + h + ((i / 6) % 2), 5, 2);
    g.fillStyle = COR.pedra[3]; g.fillRect(x, y + h - 1, w, 1);
  } else {
    // a muralha e as torres: o topo (o caminho de ronda com as ameias) e a face sul de cada ponta
    const topo = y - a;
    g.fillStyle = COR.pedra[1]; g.fillRect(x, topo, w, h);
    g.fillStyle = COR.pedra[2]; g.fillRect(x, topo + h, w, a);   // a face sul (a ponta do trecho)
    g.fillStyle = COR.pedra[3];
    for (let j = topo + h + 4; j < topo + h + a; j += 6) g.fillRect(x, j, w, 1);
    // as ameias nas duas bordas do topo
    g.fillStyle = COR.pedra[0];
    for (let j = topo; j < topo + h; j += 6) { g.fillRect(x, j, 3, 4); g.fillRect(x + w - 3, j, 3, 4); }
    if (o.tipo === "torre") {
      g.fillStyle = COR.pedra[0]; g.fillRect(x - 1, topo - 2, w + 2, 3);
      g.fillStyle = "#2a2a30"; g.fillRect(x + Math.floor(w / 2) - 1, topo + h + 8, 3, 5);
    }
  }
  g.restore();
}

/** As magias anunciadas (o círculo enchendo até cair), os dardos, a luz e a Corrente Arcana. */
export function desenharMagias(g, m, cx, cy, pintarForma, rel) {
  for (const z of m.magias || []) {
    const k = Math.min(1, z.t / z.dur), fogo = z.cor === "fogo";
    pintarForma(g, { tipo: "circulo", x: z.x, y: z.y, raio: z.raio }, cx, cy,
      fogo ? `rgba(255,110,40,${0.08 + 0.22 * k})` : `rgba(170,130,255,${0.08 + 0.22 * k})`, fogo ? "rgba(255,150,70,0.95)" : "rgba(200,170,255,0.95)");
    // o círculo de dentro cresce até a borda: quando encosta, cai
    pintarForma(g, { tipo: "circulo", x: z.x, y: z.y, raio: Math.max(1, z.raio * k) }, cx, cy, null, fogo ? "rgba(255,220,140,0.8)" : "rgba(230,210,255,0.8)", 0);
  }
  for (const p of m.projE || []) {
    const x = Math.round(p.x) - cx, y = Math.round(p.y) - cy - 6;
    const c1 = p.cor === "luz" ? "#fff2b0" : "#c9a0ff", c2 = p.cor === "luz" ? "#ffe08a" : "#8a5ad8";
    g.fillStyle = c2; g.fillRect(Math.round(x - p.dx * 3), Math.round(y - p.dy * 3), 2, 2);
    g.fillStyle = c1; g.fillRect(x - 1, y - 1, 3, 3);
  }
  for (const l of m.linhas || []) {
    if (l.ate < m.t) continue;
    g.fillStyle = Math.floor(rel * 20) % 2 ? "#e0d0ff" : "#9a6cff";
    const n = Math.max(2, Math.floor(Math.hypot(l.x2 - l.x1, l.y2 - l.y1) / 3));
    for (let i = 0; i <= n; i++) {
      const k = i / n, j = i % 2 ? 1 : -1;
      g.fillRect(Math.round(l.x1 + (l.x2 - l.x1) * k + j) - cx, Math.round(l.y1 + (l.y2 - l.y1) * k - j) - cy, 1, 1);
    }
  }
  if (m.linhas && m.linhas.length > 40) m.linhas = m.linhas.filter((l) => l.ate >= m.t);
}

/** A carga da cavalaria: a poeira atrás de quem galopa e o aviso de quem empina (prestes a carregar). */
export function desenharCargas(g, m, cx, cy, rel) {
  for (const u of m.unidades) {
    if (u.morto || u.tipo !== "cavaleiro" || !u.galope) continue;
    const gl = u.galope;
    if (gl.prepara > 0) {
      // empinando: a linha da carga no chão, curta, na direção dela
      g.fillStyle = u.lado === 1 ? "rgba(255,120,90,0.8)" : "rgba(150,200,255,0.8)";
      for (let i = 6; i < 40; i += 3) g.fillRect(Math.round(u.x + gl.dx * i) - cx, Math.round(u.y + gl.dy * i) - cy, 1, 1);
    } else {
      g.fillStyle = "rgba(190,170,130,0.55)";
      for (let i = 1; i < 4; i++) g.fillRect(Math.round(u.x - gl.dx * (6 + i * 4) + ((i + Math.floor(rel * 10)) % 3) - 1) - cx, Math.round(u.y - gl.dy * (6 + i * 4)) - cy, 2, 1);
    }
  }
}
