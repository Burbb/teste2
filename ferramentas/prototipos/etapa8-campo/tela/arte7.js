// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 7: o cenário nas duas direções do estudo de arte ("sobria" e
// "sombria"; a "atual" continua em desenho.js e desenho6.js). Só desenho: as construções ocupam no chão exatamente o
// retângulo da colisão e sobem `alto` px para o norte, como antes; a luz vem do noroeste (o alto à esquerda), as sombras
// caem para o sudeste. Cada construção e cada árvore é pintada uma vez por direção e guardada; as chamas das tochas e o
// brilho da luz são os únicos que mudam de um quadro para o outro.
//
// O que é desenho à mão e o que é montagem: as texturas do chão (16 × 16), os blocos de pedra, as telhas, as ameias, a
// enxaimel e as copas das árvores são motivos pequenos desenhados em grade; o código só os repete no tamanho de cada
// construção (o kit modular do Slynyrd, Pixelblog 20, 21 e 44). Candidatas para comparar, nada aprovado.
import { CAMPO } from "./conteudo.js";

const C = {
  sobria: {
    fundo: "#3e4a37", campo: "#56664a", textura: ["#4e5d43", "#62735a"], mancha: ["#52623f", "#5a6a4c"], tufo: ["#47573d", "#6b7c5e"],
    flor: ["#d8d2b0", "#c9b25c"], pedra: ["#8a887e", "#67655d"], moita: ["#33402e", "#46573e"],
    estrada: "#7c6c52", estradaEsc: "#6a5c45", estradaClara: "#8e7d61", sulco: "#5f5240", poca: null,
    reboco: ["#c6baa0", "#a59a82", "#8a806b"], madeira: ["#5e4631", "#43311f"], telha: ["#8a5644", "#6e4336", "#a06a54", "#4a2e25"],
    muro: ["#8d8a81", "#6e6b64", "#5a5751", "#a19d93", "#45433e"], musgo: null, janela: "#26262c", luzJanela: null,
    copa: ["#3f5a35", "#4e6b40", "#62804f", "#7a9662"], tronco: ["#5a4330", "#3c2c1f"], sombra: "rgba(14,18,12,0.30)",
  },
  sombria: {
    fundo: "#2a3125", campo: "#3d4635", textura: ["#343d2e", "#4b5340"], mancha: ["#433d30", "#38412f"], tufo: ["#5b5842", "#48543c"],
    flor: null, pedra: ["#6b6a62", "#4a4943"], moita: ["#222a1e", "#323d2b"],
    estrada: "#4d4333", estradaEsc: "#3b3328", estradaClara: "#5c5140", sulco: "#2f2820", poca: ["#2c363b", "#4f5d63"],
    reboco: ["#8e846f", "#706855", "#58513f"], madeira: ["#3d2c1f", "#281c13"], telha: ["#43464f", "#30323a", "#5b5f6a", "#1f2026"],
    muro: ["#615e58", "#4a4843", "#383632", "#75726b", "#2b2926"], musgo: ["#3f4b33", "#4d5b3c"], janela: "#1c1a1e", luzJanela: ["#e3a952", "#ffd27a"],
    copa: ["#232f20", "#2f3d2a", "#3e4f36", "#536646"], tronco: ["#3e2f22", "#271d15"], sombra: "rgba(6,8,6,0.38)",
  },
};

// um número fixo por posição (o mesmo musgo, a mesma telha quebrada a cada quadro)
const h2 = (x, y) => { let n = (x * 374761393 + y * 668265263) | 0; n = (n ^ (n >>> 13)) * 1274126177; return ((n ^ (n >>> 16)) >>> 0) / 4294967296; };

// ------------------------------------------------------------------------------------------------ o chão
// A textura do gramado (16 × 16): '.' o campo, 'a' o tom de baixo, 'b' o de cima. Grupos pequenos que atravessam a borda
// do quadro e não encostam lado a lado (Pixelblog 20); repetida espelhada a cada quadro, para a grade não aparecer.
const TEXTURA = [
  "................",
  "..a.......b.....",
  ".aa.............",
  "........a.......",
  "....b..aa.......",
  "..............a.",
  ".a............aa",
  "......b.........",
  "..........a.....",
  "...a.....aa....b",
  "..aa............",
  "........b.......",
  "............a...",
  ".b..........aa..",
  "......a.........",
  ".....aa.........",
];

/** O chão do campo (com a borda de fora), uma vez por direção. */
export function criarChao7(arte, rng, BORDA) {
  const P = C[arte], W = CAMPO.largura + BORDA * 2, H = CAMPO.altura + BORDA * 2;
  const c = document.createElement("canvas");
  c.width = W; c.height = H;
  const g = c.getContext("2d");
  g.fillStyle = P.fundo; g.fillRect(0, 0, W, H);
  g.fillStyle = P.campo; g.fillRect(BORDA, BORDA, CAMPO.largura, CAMPO.altura);
  for (let ty = 0; ty < CAMPO.altura; ty += 16) for (let tx = 0; tx < CAMPO.largura; tx += 16) {
    const ex = (tx / 16) % 2, ey = (ty / 16) % 2;
    for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) {
      const ch = TEXTURA[ey ? 15 - y : y][ex ? 15 - x : x];
      if (ch === ".") continue;
      g.fillStyle = ch === "a" ? P.textura[0] : P.textura[1];
      g.fillRect(BORDA + tx + x, BORDA + ty + y, 1, 1);
    }
  }
  // manchas grandes (na sombria, terra e lama), com a beirada pontilhada
  for (let k = 0; k < (arte === "sombria" ? 22 : 14); k++) {
    const cx = BORDA + rng() * CAMPO.largura, cy = BORDA + rng() * CAMPO.altura, r = 18 + rng() * 44;
    g.fillStyle = rng() < 0.5 ? P.mancha[0] : P.mancha[1];
    for (let y = -r; y <= r; y++) for (let x = -r; x <= r; x++) {
      const d = Math.hypot(x, y * 1.4) / r;
      if (d > 1 || d > 0.8 && (x + y) % 2) continue;
      g.fillRect(Math.round(cx + x), Math.round(cy + y), 1, 1);
    }
  }
  for (let k = 0; k < (arte === "sombria" ? 380 : 300); k++) {
    const x = Math.round(BORDA + rng() * CAMPO.largura), y = Math.round(BORDA + rng() * CAMPO.altura);
    g.fillStyle = rng() < 0.6 ? P.tufo[0] : P.tufo[1];
    g.fillRect(x, y, 1, 1); g.fillRect(x + 2, y, 1, 1); g.fillRect(x + 1, y - 1, 1, 1);
  }
  for (let k = 0; k < 46; k++) {
    const x = Math.round(BORDA + rng() * CAMPO.largura), y = Math.round(BORDA + rng() * CAMPO.altura);
    g.fillStyle = P.pedra[0]; g.fillRect(x, y, 2, 1);
    g.fillStyle = P.pedra[1]; g.fillRect(x, y + 1, 2, 1);
  }
  if (P.flor) for (let k = 0; k < 28; k++) {
    g.fillStyle = rng() < 0.5 ? P.flor[0] : P.flor[1];
    g.fillRect(Math.round(BORDA + rng() * CAMPO.largura), Math.round(BORDA + rng() * CAMPO.altura), 1, 1);
  }
  for (let k = 0; k < 160; k++) {
    const x = rng() * W, y = rng() * H;
    if (x > BORDA - 6 && x < W - BORDA + 6 && y > BORDA - 6 && y < H - BORDA + 6) continue;
    const r = 3 + rng() * 5;
    g.fillStyle = P.moita[0];
    g.beginPath(); g.ellipse(Math.round(x), Math.round(y), r, r * 0.7, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = P.moita[1]; g.fillRect(Math.round(x - 1), Math.round(y - r * 0.5), 2, 1);
  }
  return c;
}

// ------------------------------------------------------------------------------------------------ as estradas
const estradas = new Map();
// A terra batida (sóbria) ou a lama (sombria): a beira pontilhada, dois sulcos de roda e, na sombria, poças. Pintada uma
// vez por mapa, por cima do chão; as sombras das construções e das árvores vão junto.
function pintarEstradas(arte, m) {
  const P = C[arte], c = document.createElement("canvas");
  c.width = CAMPO.largura; c.height = CAMPO.altura;
  const g = c.getContext("2d"), def = m.cenario.def;
  for (const e of def.estradas || []) {
    for (let y = e.y - 2; y < e.y + e.h + 2; y++) for (let x = e.x - 2; x < e.x + e.w + 2; x++) {
      const borda = x < e.x || y < e.y || x >= e.x + e.w || y >= e.y + e.h;
      if (borda && (x + y) % 2) continue;
      const r = h2(x, y);
      g.fillStyle = borda ? P.estradaEsc : r < 0.08 ? P.estradaEsc : r > 0.95 ? P.estradaClara : P.estrada;
      g.fillRect(x, y, 1, 1);
    }
    // os sulcos: dois traços ao longo, a um terço da largura
    const deitada = e.w > e.h;
    g.fillStyle = P.sulco;
    for (const k of [0.33, 0.67]) {
      if (deitada) { const y = Math.round(e.y + e.h * k); for (let x = e.x; x < e.x + e.w; x++) if (h2(x, y) > 0.18) g.fillRect(x, y, 1, 1); }
      else { const x = Math.round(e.x + e.w * k); for (let y = e.y; y < e.y + e.h; y++) if (h2(x, y) > 0.18) g.fillRect(x, y, 1, 1); }
    }
    if (P.poca) for (let i = 0; i < Math.floor((e.w * e.h) / 1800); i++) {
      const px = e.x + 4 + Math.floor(h2(i, e.x) * (e.w - 12)), py = e.y + 3 + Math.floor(h2(e.y, i) * (e.h - 8)), r = 2 + Math.floor(h2(px, py) * 3);
      g.fillStyle = P.poca[0];
      for (let y = -r; y <= r; y++) for (let x = -r * 2; x <= r * 2; x++) if (Math.hypot(x / 2, y) <= r) g.fillRect(px + x, py + y, 1, 1);
      g.fillStyle = P.poca[1]; g.fillRect(px - r, py - Math.max(1, r - 1), r, 1);   // o reflexo do céu, no alto da poça
    }
  }
  // as sombras no chão (para o sudeste): as construções e a copa das árvores
  for (const o of m.cenario.obs) {
    g.fillStyle = P.sombra;
    if (o.tipo === "arvore") {
      const cx = o.x + o.w / 2 + 4, cy = o.y + o.h + 1, r = o.copa || 12;
      g.beginPath(); g.ellipse(cx, cy, r, r * 0.45, 0, 0, Math.PI * 2); g.fill();
      continue;
    }
    g.fillRect(o.x + 3, o.y + o.h, o.w, 4);
    g.fillRect(o.x + o.w, o.y + 3, 4, o.h);
  }
  return c;
}

export function desenharEstradas7(g, m, cx, cy, arte) {
  const k = arte + "|" + m.cenario.nome;
  let c = estradas.get(k);
  if (!c) { c = pintarEstradas(arte, m); estradas.set(k, c); }
  g.drawImage(c, -cx, -cy);
}

// ------------------------------------------------------------------------------------------------ a luz (sombria)
const luzes = new Map();
/** A luz quente das tochas e da janela (só na sombria): um brilho somado ao chão, com uma oscilação lenta. */
export function desenharLuzes7(g, m, cx, cy, arte, rel) {
  const pontos = m.cenario.def.luzes;
  if (arte !== "sombria" || !pontos) return;
  let c = luzes.get(m.cenario.nome);
  if (!c) {
    c = document.createElement("canvas");
    c.width = CAMPO.largura; c.height = CAMPO.altura;
    const gl = c.getContext("2d");
    for (const p of pontos) {
      const r = p.raio || 46, gr = gl.createRadialGradient(p.x, p.y, 2, p.x, p.y, r);
      gr.addColorStop(0, "rgba(255,170,80,0.34)"); gr.addColorStop(0.5, "rgba(255,140,60,0.12)"); gr.addColorStop(1, "rgba(255,120,40,0)");
      gl.fillStyle = gr; gl.fillRect(p.x - r, p.y - r, r * 2, r * 2);
    }
    luzes.set(m.cenario.nome, c);
  }
  g.save();
  g.globalCompositeOperation = "lighter";
  g.globalAlpha = 0.85 + 0.15 * Math.sin(rel * 7.3) * Math.sin(rel * 2.1);
  g.drawImage(c, -cx, -cy);
  g.restore();
}

// ------------------------------------------------------------------------------------------------ as construções
const predios = new Map();
const MARGEM = 8;   // o espaço em volta do retângulo no desenho guardado (ameias, beiral, copa)

/** Uma construção (ou árvore) na direção `arte`, com a transparência `alfa` (só usada na direção atual). */
export function desenharPredio7(g, o, cx, cy, arte, rel) {
  const k = `${arte}|${o.tipo}|${o.x},${o.y},${o.w},${o.h},${o.alto},${o.copa || 0}`;
  let p = predios.get(k);
  if (!p) { p = pintarPredio(o, arte); predios.set(k, p); }
  g.drawImage(p.c, Math.round(o.x) - p.ox - cx, Math.round(o.y) - p.oy - cy);
  // as tochas das torres, na sombria: a chama muda de quadro
  if (arte === "sombria" && o.tipo === "torre") {
    const x = Math.round(o.x + o.w / 2) - cx, y = Math.round(o.y + o.h - 12) - cy, f = Math.floor(rel * 9) % 3;
    g.fillStyle = "#ff8a30"; g.fillRect(x, y - 2 - (f === 1 ? 1 : 0), 1, 2);
    g.fillStyle = "#ffd27a"; g.fillRect(x, y - 1, 1, 1);
    if (f === 2) { g.fillStyle = "#ff8a30"; g.fillRect(x + 1, y - 2, 1, 1); }
  }
}

function pintarPredio(o, arte) {
  const P = C[arte], arvore = o.tipo === "arvore", alto = arvore ? (o.copa || 12) * 2 + 10 : o.alto;
  const ox = MARGEM + (arvore ? (o.copa || 12) : 0), oy = alto + MARGEM + (arvore ? 4 : 0);
  const c = document.createElement("canvas");
  c.width = o.w + ox * 2; c.height = o.h + oy + MARGEM;
  const g = c.getContext("2d");
  const px = (x, y, cor) => { g.fillStyle = cor; g.fillRect(x, y, 1, 1); };
  const x = ox, y = oy, w = o.w, h = o.h, a = o.alto;
  if (o.tipo === "casa") casa(g, px, P, x, y, w, h, a, arte);
  else if (o.tipo === "muro") {
    for (let i = 0; i < w; i++) for (let j = 0; j < a; j++) {
      const lin = Math.floor(j / 3), col = Math.floor((i + (lin % 2) * 3) / 6);
      const junta = j % 3 === 2 || (i + (lin % 2) * 3) % 6 === 5;
      px(x + i, y + h - a + j, junta ? P.muro[2] : h2(col, lin) < 0.3 ? P.muro[3] : P.muro[1]);
    }
    for (let i = 0; i < w; i++) px(x + i, y + h - a, P.muro[3]);
    for (let i = 0; i < w; i++) px(x + i, y + h, P.muro[4]);
  } else if (arvore) arvoreEm(g, px, P, x + w / 2, y + h, o.copa || 12, arte, o.x * 7 + o.y);
  else pedra(g, px, P, x, y, w, h, a, o.tipo === "torre", arte);
  return { c, ox, oy };
}

// a casa: a parede da frente (reboco e madeira; na sombria, enxaimel) e o telhado subindo para o norte
function casa(g, px, P, x, y, w, h, a, arte) {
  const paredeA = Math.round(a * 0.55), telhadoA = h + a - paredeA, py = y + h - paredeA, ty = py - telhadoA;
  // a parede: o reboco, mais escuro à direita (a luz vem da esquerda) e embaixo do beiral
  for (let i = 0; i < w; i++) for (let j = 0; j < paredeA; j++) {
    let cor = P.reboco[0];
    if (j < 2 || i > w - 4) cor = P.reboco[1];
    if (arte === "sombria" && h2(x + i, py + j) < 0.05) cor = P.reboco[2];
    px(x + i, py + j, cor);
  }
  // a base de pedra
  for (let i = 0; i < w; i++) for (let j = paredeA - 3; j < paredeA; j++) px(x + i, py + j, (i + j) % 5 === 0 ? P.muro[2] : P.muro[1]);
  // a madeira: os esteios e as vigas; na sombria, as escoras em diagonal (o enxaimel)
  const passo = Math.max(10, Math.floor(w / 4));
  for (let i = 0; i <= w; i += passo) for (let j = 0; j < paredeA - 3; j++) { const xx = x + Math.min(i, w - 2); px(xx, py + j, P.madeira[0]); px(xx + 1, py + j, P.madeira[1]); }
  for (let i = 0; i < w; i++) { px(x + i, py, P.madeira[1]); px(x + i, py + Math.floor((paredeA - 3) / 2), P.madeira[0]); }
  if (arte === "sombria") for (let i = 0; i + passo <= w; i += passo) {
    const meio = Math.floor((paredeA - 3) / 2);
    for (let t = 0; t < meio; t++) { const k = Math.round((t / meio) * (passo - 2)); px(x + i + 1 + k, py + meio - t, P.madeira[0]); }
  }
  // a porta e a janela (na sombria, acesa por dentro)
  const dx = x + Math.floor(w / 2) - 3;
  for (let j = 0; j < 9; j++) for (let i = 0; i < 6; i++) px(dx + i, y + h - 9 + j, i === 0 || i === 5 || j === 0 ? P.madeira[1] : arte === "sombria" && j === 4 ? "#5a5d66" : P.madeira[0]);
  for (let j = 0; j < 4; j++) for (let i = 0; i < 5; i++) {
    const luz = P.luzJanela, cor = luz ? (i === 2 || j === 2 ? P.madeira[1] : j === 1 && i === 1 ? luz[1] : luz[0]) : P.janela;
    px(x + 5 + i, py + 4 + j, cor);
  }
  for (let i = 0; i < 7; i++) px(x + 4 + i, py + 8, P.reboco[1]);
  // o telhado: as fileiras de telhas (ou de lousa), a cumeeira clara em cima, o lado direito na sombra, o beiral escuro
  for (let j = 0; j < telhadoA; j++) for (let i = -2; i < w + 2; i++) {
    const fil = Math.floor(j / 3), junta = j % 3 === 2 || (i + fil * 2) % 5 === 0 && j % 3 === 1;
    let cor = junta ? P.telha[1] : P.telha[0];
    if (j < 2) cor = P.telha[2];
    if (i > w - 2 && !junta) cor = P.telha[1];
    if (arte === "sombria" && P.musgo && h2(i * 3 + x, j * 5 + y) < 0.06) cor = P.musgo[h2(i, j) < 0.5 ? 0 : 1];
    px(x + i, ty + j, cor);
  }
  for (let i = -2; i < w + 2; i++) px(x + i, ty + telhadoA - 1, P.telha[3]);
  // a chaminé, de pedra, perto da cumeeira
  const ch = x + w - 12;
  for (let j = -5; j < 3; j++) for (let i = 0; i < 4; i++) px(ch + i, ty + j, i === 3 ? P.muro[2] : j === -5 ? P.muro[3] : P.muro[1]);
}

// a muralha e as torres: o caminho de ronda em cima (com as ameias nas bordas) e a face sul de cada ponta, em blocos de
// pedra com as juntas desencontradas; na sombria, o musgo na base e a seteira escura
function pedra(g, px, P, x, y, w, h, a, torre, arte) {
  const topo = y - a;
  for (let i = 0; i < w; i++) for (let j = 0; j < h; j++) {
    const lin = Math.floor(j / 4), junta = j % 4 === 3 || (i + (lin % 2) * 3) % 7 === 6;
    px(x + i, topo + j, junta ? P.muro[2] : P.muro[0]);
  }
  for (let i = 0; i < w; i++) for (let j = 0; j < a; j++) {
    const lin = Math.floor(j / 4), col = Math.floor((i + (lin % 2) * 3) / 6);
    const junta = j % 4 === 3 || (i + (lin % 2) * 3) % 6 === 5;
    let cor = junta ? P.muro[2] : h2(col + x, lin + y) < 0.22 ? P.muro[3] : P.muro[1];
    if (i > w - 3 && !junta) cor = P.muro[2];   // a quina da direita, na sombra
    if (P.musgo && j > a - 5 && h2(i + x, j + y) < 0.35 - (a - j) * 0.06) cor = P.musgo[(i + j) % 2];
    px(x + i, topo + h + j, cor);
  }
  for (let i = 0; i < w; i++) px(x + i, topo + h + a - 1, P.muro[4]);
  // as ameias, nas duas bordas do topo
  for (let j = 0; j < h; j += 6) for (let dj = 0; dj < 4; dj++) for (const i of [0, 1, 2, w - 3, w - 2, w - 1]) px(x + i, topo + j + dj, dj === 0 ? P.muro[3] : P.muro[1]);
  if (torre) {
    for (let i = -1; i <= w; i++) for (let j = -3; j < 0; j++) px(x + i, topo + j, j === -3 ? P.muro[3] : P.muro[1]);
    for (let j = 0; j < 6; j++) px(x + Math.floor(w / 2), topo + h + 6 + j, P.muro[4]);
    if (arte === "sombria") {
      // o suporte da tocha e o estandarte do inimigo pendurado na face
      px(x + Math.floor(w / 2), y + h - 11, P.madeira[0]);
      for (let j = 0; j < 9; j++) for (let i = 0; i < 4; i++) px(x + 3 + i, topo + h + 3 + j, j === 8 && i % 2 ? "rgba(0,0,0,0)" : i === 0 ? "#541d1b" : "#86302a");
    }
  }
}

// a árvore: o tronco (cilindro com casca listrada) e a copa em feixes de folhas sombreados como esferas (o claro em cima
// à esquerda, o crescente escuro embaixo à direita), na ordem da luz (Pixelblog 44)
const FEIXES = [[0, 0, 1], [-0.55, 0.15, 0.7], [0.55, 0.2, 0.72], [-0.2, -0.45, 0.68], [0.3, -0.4, 0.62], [0, 0.45, 0.6]];
function arvoreEm(g, px, P, bx, by, r, arte, semente) {
  const tx = Math.round(bx), topoTronco = by - 9;
  for (let j = topoTronco; j < by; j++) for (let i = -2; i <= 1; i++) px(tx + i, j, i === 1 ? P.tronco[1] : (j + i * 2) % 4 === 0 ? P.tronco[1] : P.tronco[0]);
  const ccx = bx, ccy = topoTronco - r * 0.55;
  const ordem = FEIXES.map((f, i) => ({ f, i })).sort((p, q) => p.f[1] - q.f[1]);
  for (const { f, i } of ordem) {
    const fx = ccx + f[0] * r, fy = ccy + f[1] * r, fr = r * 0.62 * f[2] + 2;
    for (let y = -fr; y <= fr; y++) for (let x = -fr; x <= fr; x++) {
      const d = Math.hypot(x, y * 1.1);
      if (d > fr) continue;
      // a borda recortada em folhas: pula pixels da beira por um padrão fixo
      if (d > fr - 1.5 && h2(Math.round(fx + x) + semente, Math.round(fy + y) + i) < 0.4) continue;
      const luz = (-x - y) / fr;
      let cor = P.copa[1];
      if (luz > 0.55) cor = P.copa[3]; else if (luz > 0.15) cor = P.copa[2];
      else if (luz < -0.55 && d > fr * 0.45) cor = P.copa[0];
      if (h2(Math.round(fx + x) * 3 + semente, Math.round(fy + y)) < 0.07) cor = P.copa[0];
      px(Math.round(fx + x), Math.round(fy + y), cor);
    }
  }
  if (arte === "sombria") {
    // um galho seco saindo da copa
    for (let t = 0; t < 5; t++) px(Math.round(ccx + r * 0.7 + t), Math.round(ccy - r * 0.2 - t * 0.6), P.tronco[0]);
  }
}

/** Quem está atrás desta construção (ou debaixo da copa): a tela desenha a silhueta por cima dela. */
export function cobre(o, u) {
  if (o.tipo === "arvore") {
    const r = o.copa || 12, cx = o.x + o.w / 2, base = o.y + o.h;
    return u.y < base - 1 && u.y > base - 9 - r * 2 && Math.abs(u.x - cx) < r + 3;
  }
  const topo = o.y - o.alto - 12, base = o.y + o.h;
  return u.y < base && u.y > topo && u.x > o.x - 6 && u.x < o.x + o.w + 6;
}
