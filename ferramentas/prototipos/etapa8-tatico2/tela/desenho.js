// PROTÓTIPO tático (nada no jogo): o desenho da arena em losangos, em pixels nativos (a tela amplia por um fator
// inteiro). Casa de 32 × 16 px; o pé do combatente fica no centro do losango. Ordem: o piso e as marcas no chão
// primeiro; depois, por profundidade (x + y), os obstáculos e os combatentes; por último, o contorno da casa sob o
// mouse (por cima de tudo: nunca fica escondida atrás de um corpo). Os pilares e os barris ficam transparentes quando
// há alguém (ou a casa sob o mouse) logo atrás deles.

export const TW = 32, TH = 16, ALTO = 30;   // a casa e a altura do pilar

const COR = {
  piso: ["#5d6c46", "#57663f"], borda: "rgba(28,34,20,0.55)", grade: "rgba(240,236,210,0.10)", gradeForte: "rgba(240,236,210,0.32)",
  alcanc: "rgba(120,200,96,0.42)", caminho: "rgba(246,224,120,0.78)", alcance: "rgba(96,150,240,0.34)",
  semVisao: "rgba(40,44,60,0.42)", area: "rgba(236,96,64,0.55)", areaAliado: "rgba(250,206,80,0.60)", alvo: "rgba(120,170,255,0.55)",
  pedraTopo: "#9a968b", pedraEsq: "#615d56", pedraDir: "#7b776e", rocha: ["#7d776b", "#5a554c", "#6b665c"],
  agua: "#2f5f7c", aguaLuz: "#4f87a8", barril: ["#8f5f30", "#6b4320", "#3a2a1c"],
};

export const proj = (x, y) => [(x - y) * (TW / 2), (x + y) * (TH / 2)];

/** A casa sob o ponto (px, py) da tela nativa, relativo à origem (o vértice de cima da casa 0,0). */
export function casaEm(px, py) {
  const u = px / (TW / 2), v = py / (TH / 2);
  return [Math.floor((v + u) / 2), Math.floor((v - u) / 2)];
}

function losango(g, x, y, cor, contorno) {
  const [sx, sy] = proj(x, y);
  g.beginPath();
  g.moveTo(sx, sy); g.lineTo(sx + TW / 2, sy + TH / 2); g.lineTo(sx, sy + TH); g.lineTo(sx - TW / 2, sy + TH / 2); g.closePath();
  if (cor) { g.fillStyle = cor; g.fill(); }
  if (contorno) { g.strokeStyle = contorno; g.lineWidth = 1; g.stroke(); }
}

// listras diagonais dentro do losango (casas sem visão, golpe preparado)
function listras(g, x, y, cor) {
  const [sx, sy] = proj(x, y);
  g.save();
  g.beginPath();
  g.moveTo(sx, sy); g.lineTo(sx + TW / 2, sy + TH / 2); g.lineTo(sx, sy + TH); g.lineTo(sx - TW / 2, sy + TH / 2); g.closePath();
  g.clip();
  g.strokeStyle = cor; g.lineWidth = 1;
  for (let i = -TW; i < TW; i += 5) { g.beginPath(); g.moveTo(sx + i, sy); g.lineTo(sx + i + TH, sy + TH); g.stroke(); }
  g.restore();
}

function pilar(g, x, y, alfa) {
  const [sx, sy] = proj(x, y);
  g.save();
  g.globalAlpha = alfa;
  const topo = sy - ALTO;
  // a face esquerda, a direita e o topo (o losango levantado)
  g.fillStyle = COR.pedraEsq;
  g.beginPath(); g.moveTo(sx - TW / 2, topo + TH / 2); g.lineTo(sx, topo + TH); g.lineTo(sx, sy + TH); g.lineTo(sx - TW / 2, sy + TH / 2); g.closePath(); g.fill();
  g.fillStyle = COR.pedraDir;
  g.beginPath(); g.moveTo(sx + TW / 2, topo + TH / 2); g.lineTo(sx, topo + TH); g.lineTo(sx, sy + TH); g.lineTo(sx + TW / 2, sy + TH / 2); g.closePath(); g.fill();
  g.fillStyle = COR.pedraTopo;
  g.beginPath(); g.moveTo(sx, topo); g.lineTo(sx + TW / 2, topo + TH / 2); g.lineTo(sx, topo + TH); g.lineTo(sx - TW / 2, topo + TH / 2); g.closePath(); g.fill();
  // juntas das pedras
  g.fillStyle = "rgba(30,26,22,0.35)";
  for (let i = 1; i < 3; i++) {
    g.fillRect(sx - TW / 2 + 2, topo + TH / 2 + i * 10, TW / 2 - 3, 1);
    g.fillRect(sx + 1, topo + TH + i * 10 - 6, TW / 2 - 3, 1);
  }
  g.restore();
}

function rocha(g, x, y) {
  const [sx, sy] = proj(x, y), cy = sy + TH / 2;
  g.fillStyle = "rgba(0,0,0,0.25)"; g.beginPath(); g.ellipse(sx, cy + 2, 11, 4, 0, 0, Math.PI * 2); g.fill();
  g.fillStyle = COR.rocha[1]; g.beginPath(); g.ellipse(sx, cy - 1, 10, 6, 0, 0, Math.PI * 2); g.fill();
  g.fillStyle = COR.rocha[0]; g.beginPath(); g.ellipse(sx - 2, cy - 3, 7, 4, 0, 0, Math.PI * 2); g.fill();
  g.fillStyle = COR.rocha[2]; g.fillRect(sx + 2, cy - 2, 5, 2);
}

function agua(g, x, y, t) {
  losango(g, x, y, COR.agua);
  const [sx, sy] = proj(x, y), f = Math.floor((t * 2 + x * 0.7 + y * 0.4) % 3);
  g.fillStyle = COR.aguaLuz;
  g.fillRect(sx - 6 + f * 2, sy + 6, 5, 1);
  g.fillRect(sx + 1 - f, sy + 10, 4, 1);
}

function barril(g, x, y, alfa) {
  const [sx, sy] = proj(x, y), base = sy + TH / 2 + 2;
  g.save(); g.globalAlpha = alfa;
  g.fillStyle = "rgba(0,0,0,0.3)"; g.beginPath(); g.ellipse(sx, base, 8, 3, 0, 0, Math.PI * 2); g.fill();
  g.fillStyle = COR.barril[1]; g.fillRect(sx - 7, base - 16, 14, 16);
  g.fillStyle = COR.barril[0]; g.fillRect(sx - 5, base - 16, 9, 16);
  g.fillStyle = COR.barril[2]; g.fillRect(sx - 7, base - 13, 14, 2); g.fillRect(sx - 7, base - 5, 14, 2);
  g.fillStyle = "#4a3320"; g.beginPath(); g.ellipse(sx, base - 16, 7, 3, 0, 0, Math.PI * 2); g.fill();
  g.fillStyle = "#e0b040"; g.fillRect(sx - 1, base - 11, 3, 3);   // a marca do óleo
  g.restore();
}

function chamas(g, x, y, t, veneno) {
  const [sx, sy] = proj(x, y);
  losango(g, x, y, veneno ? "rgba(90,160,60,0.38)" : "rgba(220,100,30,0.36)");
  const f = Math.floor(t * 8 + x * 3 + y * 5) % 3;
  g.fillStyle = veneno ? "#8fd060" : "#ffb040";
  for (let i = 0; i < 3; i++) {
    const px = sx - 8 + i * 7 + ((f + i) % 2), py = sy + 6 + ((i + f) % 3);
    g.fillRect(px, py - 3, 2, 3);
    g.fillStyle = veneno ? "#d8f0a0" : "#ffe08a"; g.fillRect(px, py - 4 - ((f + i) % 2), 1, 2);
    g.fillStyle = veneno ? "#8fd060" : "#ffb040";
  }
}

/**
 * Desenha a arena. `v`: { m, disp (posições e vida mostradas), Q (sprites), hl: { alcanc, caminho, alcance, semVisao,
 * area, areaAliado, alvos }, hover, atual, prev (prévia), t, efeitos, preparosVisiveis }.
 */
export function desenharArena(g, v) {
  const { m, t } = v;
  // o piso
  for (let y = 0; y < m.h; y++) for (let x = 0; x < m.w; x++) {
    const c = m.celulas[y * m.w + x];
    if (c === " ") continue;
    if (c === "~") agua(g, x, y, t);
    else losango(g, x, y, COR.piso[(x + y) % 2], COR.borda);
  }
  // a grade: discreta em repouso, mais forte ao andar ou mirar
  const forte = v.hl.alcance || v.hl.alcanc;
  for (let y = 0; y < m.h; y++) for (let x = 0; x < m.w; x++) if (m.celulas[y * m.w + x] === "." ) losango(g, x, y, null, forte ? COR.gradeForte : COR.grade);
  // o chão em chamas ou envenenado
  for (const [k, ch] of Object.entries(m.chao)) { const [x, y] = k.split(",").map(Number); chamas(g, x, y, t, ch.e === "veneno"); }
  // as marcas
  const pinta = (lista, cor) => { if (lista) for (const [x, y] of lista) losango(g, x, y, cor); };
  pinta(v.hl.alcanc, COR.alcanc);
  pinta(v.hl.alcance, COR.alcance);
  if (v.hl.semVisao) for (const [x, y] of v.hl.semVisao) { losango(g, x, y, COR.semVisao); listras(g, x, y, "rgba(200,200,220,0.25)"); }
  pinta(v.hl.alvos, COR.alvo);
  pinta(v.hl.caminho, COR.caminho);
  // os golpes preparados (de quem está vivo): listras vermelhas
  for (const p of m.preparos) for (const [x, y] of p.celulas) { losango(g, x, y, "rgba(200,40,30,0.30)"); listras(g, x, y, "rgba(255,110,90,0.75)"); }
  pinta(v.hl.area, COR.area);
  pinta(v.hl.areaAliado, COR.areaAliado);
  if (v.prev && v.prev.preparo) for (const [x, y] of v.prev.preparo) listras(g, x, y, "rgba(255,140,110,0.9)");
  // as armadilhas do jogador (o inimigo não as vê)
  for (const a of m.armadilhas) if (a.lado === 0) {
    const [sx, sy] = proj(a.x, a.y);
    g.strokeStyle = "#e8d070"; g.lineWidth = 1;
    g.beginPath(); g.moveTo(sx - 6, sy + 8); g.lineTo(sx + 6, sy + 8); g.moveTo(sx, sy + 5); g.lineTo(sx, sy + 11); g.stroke();
    g.fillStyle = "#e8d070"; g.fillRect(sx - 1, sy + 7, 3, 3);
  }
  // a casa do combatente da vez
  if (v.atual) {
    const d = v.disp[v.atual.id];
    if (d) losango(g, Math.round(d.x), Math.round(d.y), null, "#ffe27a");
  }

  // os objetos e os combatentes, por profundidade
  const itens = [];
  for (let y = 0; y < m.h; y++) for (let x = 0; x < m.w; x++) {
    const c = m.celulas[y * m.w + x];
    if (c === "#" || c === "o" || c === "r") itens.push({ z: x + y, o: 0, x, y, c });
  }
  for (const u of m.unidades) {
    const d = v.disp[u.id];
    if (!d || !d.mostrar) continue;
    itens.push({ z: d.x + d.y + 0.01, o: 1, u, d });
  }
  itens.sort((a, b) => a.z - b.z || a.o - b.o);
  const atras = (x, y) => {
    // alguém (ou a casa sob o mouse) numa das casas logo atrás deste objeto, na tela
    const perto = (px, py) => { const dz = x + y - (px + py), dl = Math.abs(x - y - (px - py)); return dz >= 1 && dz <= 3 && dl <= 2; };
    if (v.hover && perto(...v.hover)) return true;
    return m.unidades.some((u) => { const d = v.disp[u.id]; return d && d.mostrar && perto(d.x, d.y); });
  };
  for (const it of itens) {
    if (it.o === 0) {
      if (it.c === "#") pilar(g, it.x, it.y, atras(it.x, it.y) ? 0.42 : 1);
      else if (it.c === "o") barril(g, it.x, it.y, atras(it.x, it.y) ? 0.55 : 1);
      else rocha(g, it.x, it.y);
    } else desenharCombatente(g, v, it.u, it.d);
  }
  // por cima: a casa sob o mouse e os efeitos
  if (v.hover && m.celulas[v.hover[1] * m.w + v.hover[0]] && m.celulas[v.hover[1] * m.w + v.hover[0]] !== " ") losango(g, v.hover[0], v.hover[1], null, "#fffbe8");
  for (const e of v.efeitos) desenharEfeito(g, e, t);
}

function desenharCombatente(g, v, u, d) {
  const [sx, sy] = proj(d.x, d.y), px = Math.round(sx), py = Math.round(sy + TH / 2);
  const Q = v.Q[u.modelo];
  if (!Q) return;
  const poses = Q[u.lado === 0 ? 0 : 1];
  let pose = d.pose || "parado";
  if (!d.vivo) pose = "caido";
  const img = poses[pose] || poses.parado;
  const lado = d.dir === "e" ? img.e : img.d;
  g.save();
  if (d.alfa != null) g.globalAlpha = d.alfa;
  // a sombra e o anel da equipe no chão (losango pequeno, não um retrato)
  g.fillStyle = "rgba(0,0,0,0.32)"; g.beginPath(); g.ellipse(px, py + 1, 8, 3, 0, 0, Math.PI * 2); g.fill();
  if (d.vivo) {
    g.strokeStyle = u.lado === 0 ? "#7fb2f0" : "#e8705e"; g.lineWidth = 1;
    g.beginPath(); g.moveTo(px - 9, py); g.lineTo(px, py - 4); g.lineTo(px + 9, py); g.lineTo(px, py + 4); g.closePath(); g.stroke();
  }
  g.drawImage(lado, px - Math.round(img.ax), py - Math.round(img.ay) + (d.salto || 0));
  if (d.clarao > 0) { g.globalAlpha = Math.min(1, d.clarao * 4); g.drawImage(d.dir === "e" ? img.be : img.bd, px - Math.round(img.ax), py - Math.round(img.ay)); }
  g.restore();
  if (!d.vivo) return;
  // a vida, curta, acima da cabeça
  const w = 16, topo = py - Math.round(img.ay) - 5;
  g.fillStyle = "#14101a"; g.fillRect(px - w / 2 - 1, topo - 1, w + 2, 4);
  g.fillStyle = "#3a2626"; g.fillRect(px - w / 2, topo, w, 2);
  g.fillStyle = u.lado === 0 ? "#6fbf5d" : "#d65a48";
  g.fillRect(px - w / 2, topo, Math.max(0, Math.round((w * d.pv) / u.pvMax)), 2);
  if (v.prev) {
    const mud = v.prev.mud.find((x) => x.id === u.id);
    if (mud && mud.dPv < 0) {
      // a vida que vai sair, piscando
      const fica = Math.max(0, d.pv + mud.dPv);
      g.fillStyle = Math.floor(v.t * 4) % 2 ? "#ffe08a" : "#ffffff";
      g.fillRect(px - w / 2 + Math.round((w * fica) / u.pvMax), topo, Math.round((w * (d.pv - fica)) / u.pvMax), 2);
    }
  }
  if (v.atual && v.atual.id === u.id) {
    const b = Math.floor(v.t * 3) % 2;
    g.fillStyle = "#ffe27a";
    g.fillRect(px - 2, topo - 6 + b, 5, 1); g.fillRect(px - 1, topo - 5 + b, 3, 1); g.fillRect(px, topo - 4 + b, 1, 1);
  }
}

// os fantasmas da prévia: onde cada um vai parar depois de um empurrão ou de um salto
export function desenharFantasmas(g, v) {
  if (!v.prev) return;
  for (const d of v.prev.mud) {
    if (d.de[0] === d.para[0] && d.de[1] === d.para[1]) continue;
    const u = v.m.unidades.find((x) => x.id === d.id), Q = v.Q[u.modelo];
    const [ax, ay] = proj(...d.de), [bx, by] = proj(...d.para);
    g.strokeStyle = "rgba(255,240,180,0.9)"; g.lineWidth = 1;
    g.beginPath(); g.moveTo(ax, ay + TH / 2); g.lineTo(bx, by + TH / 2); g.stroke();
    const img = Q[u.lado][d.morre ? "caido" : "parado"];
    g.save(); g.globalAlpha = 0.5;
    g.drawImage(img.d, Math.round(bx - img.ax), Math.round(by + TH / 2 - img.ay));
    g.restore();
  }
}

function desenharEfeito(g, e, t) {
  const k = Math.min(1, (t - e.t0) / e.dur);
  if (e.tipo === "linha") {
    const [ax, ay] = proj(...e.de), [bx, by] = proj(...e.para);
    const x = ax + (bx - ax) * k, y = ay + (by - ay) * k;
    g.fillStyle = e.cor;
    g.fillRect(Math.round(x) - 1, Math.round(y + TH / 2 - 10) - 1, 3, 3);
  } else if (e.tipo === "raio") {
    const [ax, ay] = proj(...e.de), [bx, by] = proj(...e.para);
    g.strokeStyle = k < 0.5 ? "#ffffff" : "#9fd0ff"; g.lineWidth = 1;
    g.beginPath(); g.moveTo(ax, ay + TH / 2 - 8);
    for (let i = 1; i < 6; i++) g.lineTo(ax + ((bx - ax) * i) / 6 + ((i * 7) % 5) - 2, ay + ((by - ay) * i) / 6 + TH / 2 - 8 + ((i * 3) % 4) - 2);
    g.lineTo(bx, by + TH / 2 - 8); g.stroke();
  } else if (e.tipo === "estouro") {
    const [sx, sy] = proj(...e.c), r = 4 + k * (e.r || 14);
    g.fillStyle = e.cor; g.globalAlpha = 1 - k;
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2 + e.t0;
      g.fillRect(Math.round(sx + Math.cos(a) * r), Math.round(sy + TH / 2 + Math.sin(a) * r * 0.5 - 4), 2, 2);
    }
    g.globalAlpha = 1;
  } else if (e.tipo === "casas") {
    g.globalAlpha = 1 - k;
    for (const [x, y] of e.celulas) losango(g, x, y, e.cor);
    g.globalAlpha = 1;
  }
}
