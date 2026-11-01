// PROTÓTIPO de campo livre: o desenho do campo, em pixels nativos (o canvas tem o tamanho do campo visível dividido
// pela ampliação inteira; o CSS amplia sem suavizar). Só lê: o mundo (sim.js), os efeitos (efeitos.js) e as opções.
// As áreas (os avisos do campeão, a preparação do herói, a prévia, os cortes) são pintadas pixel a pixel com a mesma
// função `dentro` que decide quem é atingido: o que aparece é exatamente o que acerta.
import { CAMPO, TIPOS } from "./conteudo.js";
import { dentro, formaDaAcao } from "./sim.js";
import { pousarCorpos } from "./efeitos.js";

export const BORDA = 70;   // o chão de fora do campo, que a câmera pode mostrar perto das bordas

export function criarChao(rng) {
  const W = CAMPO.largura + BORDA * 2, H = CAMPO.altura + BORDA * 2;
  const c = document.createElement("canvas");
  c.width = W; c.height = H;
  const g = c.getContext("2d");
  g.fillStyle = "#3f5636";
  g.fillRect(0, 0, W, H);
  g.fillStyle = "#5a7748";
  g.fillRect(BORDA, BORDA, CAMPO.largura, CAMPO.altura);
  // a beira do campo, pontilhada: o gramado de fora começa sem linha dura
  g.fillStyle = "#4d6840";
  for (let x = BORDA - 2; x < BORDA + CAMPO.largura + 2; x++) for (const y of [BORDA - 1, BORDA + CAMPO.altura]) if ((x + y) % 2) g.fillRect(x, y, 1, 1);
  for (let y = BORDA - 2; y < BORDA + CAMPO.altura + 2; y++) for (const x of [BORDA - 1, BORDA + CAMPO.largura]) if ((x + y) % 2) g.fillRect(x, y, 1, 1);
  // manchas grandes e discretas, com a beirada pontilhada (poucas variações: o piso não disputa com as tropas)
  for (let k = 0; k < 16; k++) {
    const cx = BORDA + rng() * CAMPO.largura, cy = BORDA + rng() * CAMPO.altura, r = 22 + rng() * 48;
    const cor = rng() < 0.5 ? "#577449" : "#5c7a49";
    g.fillStyle = cor;
    for (let y = -r; y <= r; y++) for (let x = -r; x <= r; x++) {
      const d = Math.hypot(x, y * 1.4) / r;
      if (d > 1) continue;
      if (d > 0.82 && (x + y) % 2) continue;
      g.fillRect(Math.round(cx + x), Math.round(cy + y), 1, 1);
    }
  }
  // tufos, pedrinhas e algumas flores
  for (let k = 0; k < 520; k++) {
    const x = Math.round(BORDA + rng() * CAMPO.largura), y = Math.round(BORDA + rng() * CAMPO.altura);
    g.fillStyle = rng() < 0.6 ? "#4c6740" : "#6b8a56";
    g.fillRect(x, y, 1, 1); g.fillRect(x + 2, y, 1, 1); g.fillRect(x + 1, y - 1, 1, 1);
  }
  for (let k = 0; k < 40; k++) {
    const x = Math.round(BORDA + rng() * CAMPO.largura), y = Math.round(BORDA + rng() * CAMPO.altura);
    g.fillStyle = "#8c8a7c"; g.fillRect(x, y, 2, 1);
    g.fillStyle = "#6c6a5e"; g.fillRect(x, y + 1, 2, 1);
  }
  for (let k = 0; k < 50; k++) {
    const x = Math.round(BORDA + rng() * CAMPO.largura), y = Math.round(BORDA + rng() * CAMPO.altura);
    g.fillStyle = rng() < 0.5 ? "#e8e2b8" : "#d9c262"; g.fillRect(x, y, 1, 1);
  }
  // fora do campo: moitas escuras
  for (let k = 0; k < 160; k++) {
    let x = rng() * W, y = rng() * H;
    if (x > BORDA - 6 && x < W - BORDA + 6 && y > BORDA - 6 && y < H - BORDA + 6) continue;
    const r = 3 + rng() * 5;
    g.fillStyle = "#344a2d";
    g.beginPath(); g.ellipse(Math.round(x), Math.round(y), r, r * 0.7, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#4a6340"; g.fillRect(Math.round(x - 1), Math.round(y - r * 0.5), 2, 1);
  }
  return c;
}

// Pinta uma forma pixel a pixel (o centro de cada pixel testado com `dentro`); a borda é quem tem um vizinho fora.
function pintarForma(g, f, cx, cy, preenche, borda, tracejado = 0) {
  let x0, y0, x1, y1;
  if (f.tipo === "faixa") {
    x0 = Math.min(f.x1, f.x2) - f.largura - 1; x1 = Math.max(f.x1, f.x2) + f.largura + 1;
    y0 = Math.min(f.y1, f.y2) - f.largura - 1; y1 = Math.max(f.y1, f.y2) + f.largura + 1;
  } else { x0 = f.x - f.raio - 1; x1 = f.x + f.raio + 1; y0 = f.y - f.raio - 1; y1 = f.y + f.raio + 1; }
  x0 = Math.floor(x0); y0 = Math.floor(y0); x1 = Math.ceil(x1); y1 = Math.ceil(y1);
  const w = x1 - x0 + 1, h = y1 - y0 + 1, mapa = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) mapa[y * w + x] = dentro(f, x0 + x + 0.5, y0 + y + 0.5) ? 1 : 0;
  const em = (x, y) => x >= 0 && y >= 0 && x < w && y < h && mapa[y * w + x] === 1;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (!mapa[y * w + x]) continue;
      const beira = !em(x - 1, y) || !em(x + 1, y) || !em(x, y - 1) || !em(x, y + 1);
      if (beira) {
        if (!borda || (tracejado && ((x + y) >> 1) % tracejado)) continue;
        g.fillStyle = borda;
      } else {
        if (!preenche) continue;
        g.fillStyle = preenche;
      }
      g.fillRect(x0 + x - cx, y0 + y - cy, 1, 1);
    }
  }
}

function sombra(g, x, y, larg) {
  g.fillStyle = "rgba(10,14,8,0.32)";
  const m = Math.floor(larg / 2);
  g.fillRect(x - m, y, larg, 1);
  g.fillRect(x - m + 1, y + 1, larg - 2, 1);
}

const LARGURA_SOMBRA = { soldado: 6, arqueiro: 6, veterano: 7, estandarte: 6, campeao: 11, heroi: 9 };

function poseTropa(u) {
  if (u.atordoado > 0 || u.congelado > 0) return "recuo";
  if (u.mostra > 0) return "golpe";
  if (u.acao) return u.acao.t > 0.08 ? "preparo" : "golpe";
  if (Math.abs(u.vx) + Math.abs(u.vy) > 2) return ["andarA", "parado", "andarB", "parado"][Math.floor(u.passo / 3) % 4];
  return "parado";
}

function poseHeroi(h) {
  if (h.morto) return "caido";
  if (h.atordoado > 0) return "recuo";
  const a = h.acao;
  if (a) {
    if (a.fase === "preparo") return "preparo";
    if (a.fase === "voo") return a.id === "salto" ? "preparo" : "golpe";
    if (a.fase === "rec") {
      const k = h.kit[a.id], decorrido = (a.id === "investida" ? 0.12 : k.rec || 0.1) - a.t;
      if (decorrido < 0.12) return "golpe";
    }
  }
  if (Math.abs(h.vx) + Math.abs(h.vy) > 4) return ["andarA", "parado", "andarB", "parado"][Math.floor(h.passo / 4) % 4];
  return "parado";
}

function barra(g, x, y, larg, frac, cor, alt = 2) {
  g.fillStyle = "#15121a"; g.fillRect(x - 1, y - 1, larg + 2, alt + 2);
  g.fillStyle = "#3a2b2b"; g.fillRect(x, y, larg, alt);
  g.fillStyle = cor; g.fillRect(x, y, Math.max(0, Math.round(larg * frac)), alt);
}

function texto(g, s, x, y, cor) {
  g.font = "8px 'Pixeloid Sans', monospace";
  g.textAlign = "center";
  g.textBaseline = "alphabetic";
  g.fillStyle = "#15121a";
  for (const [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) g.fillText(s, Math.round(x) + dx, Math.round(y) + dy);
  g.fillStyle = cor;
  g.fillText(s, Math.round(x), Math.round(y));
}

/** Desenha um quadro. `s`: { m, E, Q, chao, cam: {x, y}, W, H, alfa, opcoes, mouse: {x, y}, relogio, pausado } */
export function desenhar(g, s) {
  const { m, E, Q, cam, W, H, alfa, opcoes } = s;
  const cx = Math.round(cam.x), cy = Math.round(cam.y);
  pousarCorpos(E, Q);
  g.imageSmoothingEnabled = false;
  g.drawImage(s.chao, -cx - BORDA, -cy - BORDA);
  g.drawImage(E.marcas, -cx, -cy);
  const h = m.heroi, rel = s.relogio;
  const pos = (u) => [u.px + (u.x - u.px) * alfa, u.py + (u.y - u.py) * alfa];

  // ---- o chão: fogo, aura do estandarte, ordem, avisos, prévias
  for (const z of m.zonas) {
    const fim = Math.min(1, z.t / 0.4);
    if (z.tipo === "chao") {
      const n = Math.round(z.raio * z.raio * 0.12 * fim);
      for (let i = 0; i < n; i++) {
        const a = (i * 2.399 + Math.floor(rel * 9) * 0.7) % (Math.PI * 2), r = Math.sqrt(((i * 0.618 + Math.floor(rel * 7) * 0.13) % 1)) * z.raio;
        const x = Math.round(z.x + Math.cos(a) * r) - cx, y = Math.round(z.y + Math.sin(a) * r) - cy;
        g.fillStyle = i % 3 ? "#ff8a30" : "#ffe08a";
        g.fillRect(x, y - (i % 2), 1, 1 + (i % 2));
      }
    } else {
      const comp = Math.hypot(z.x2 - z.x1, z.y2 - z.y1), n = Math.floor(comp / 3);
      for (let i = 0; i <= n; i++) {
        const k = i / n, x = Math.round(z.x1 + (z.x2 - z.x1) * k) - cx, y = Math.round(z.y1 + (z.y2 - z.y1) * k) - cy;
        const alt = Math.round((3 + ((i * 7 + Math.floor(rel * 10)) % 4)) * fim);
        g.fillStyle = "#a8361f"; g.fillRect(x - 1, y, 3, 1);
        g.fillStyle = "#ff8a30"; g.fillRect(x, y - alt, 1, alt);
        g.fillStyle = "#ffe08a"; g.fillRect(x, y - Math.max(1, alt - 2), 1, 1);
      }
    }
  }
  for (const u of m.lados[1]) {
    if (u.tipo !== "estandarte") continue;
    pintarForma(g, { tipo: "circulo", x: u.x, y: u.y, raio: u.def.aura }, cx, cy, null, "rgba(230,120,90,0.22)", 4);
  }
  if (E.ordem && E.ordem.tipo === "defender") {
    const o = E.ordem, x = Math.round(o.x) - cx, y = Math.round(o.y) - cy;
    if (s.pausado || o.t < 3) pintarForma(g, { tipo: "circulo", x: o.x, y: o.y, raio: 85 }, cx, cy, null, "rgba(140,190,255,0.4)", 3);
    g.fillStyle = "#6a4521"; g.fillRect(x, y - 12, 1, 12);
    g.fillStyle = "#76a8ea"; g.fillRect(x + 1, y - 12, 5, 3);
    g.fillStyle = "#4778c2"; g.fillRect(x + 1, y - 9, 4, 1);
  } else if (E.ordem && E.ordem.t < 0.6) {
    const r = 8 + E.ordem.t * 90;
    pintarForma(g, { tipo: "circulo", x: h.x, y: h.y, raio: r }, cx, cy, null, `rgba(140,190,255,${0.6 - E.ordem.t})`, 2);
  }
  // os avisos do campeão: o arco que o machado vai varrer, enchendo até o golpe
  for (const u of m.lados[1]) {
    if (u.tipo !== "campeao" || !u.acao || !u.acao.forma) continue;
    const k = 1 - Math.max(0, u.acao.t) / u.def.preparo;
    pintarForma(g, u.acao.forma, cx, cy, `rgba(220,40,30,${0.12 + 0.3 * k})`, "rgba(255,90,70,0.95)");
  }
  // a preparação do herói e os pontos de chegada
  const a = h.acao;
  if (a && !h.morto) {
    if (a.fase === "preparo" && a.id !== "basico" && a.forma) {
      const f = a.id === "salto" || a.id === "bola" || a.id === "muralha" ? a.forma : { ...a.forma, x: h.x, y: h.y };
      pintarForma(g, f, cx, cy, "rgba(255,245,210,0.12)", "rgba(255,245,210,0.85)");
    }
    if (a.fase === "voo" && a.id === "salto") {
      pintarForma(g, { tipo: "circulo", x: a.tx, y: a.ty, raio: h.kit.salto.raio }, cx, cy, "rgba(255,245,210,0.14)", "rgba(255,245,210,0.9)");
    }
  }
  for (const p of m.proj) {
    if (p.tipo !== "bola") continue;
    const k = p.t / p.dur;
    pintarForma(g, { tipo: "circulo", x: p.x1, y: p.y1, raio: p.k.raio }, cx, cy, `rgba(255,140,50,${0.08 + 0.14 * k})`, "rgba(255,170,80,0.9)");
  }
  // a prévia da habilidade do botão direito no mouse (opção "Mostrar áreas")
  if (opcoes.areas && !h.morto && !a && m.fase !== "fim") {
    const id = h.nomeHeroi === "guerreiro" ? "varredura" : "bola";
    const pronto = h.cds[id] <= 0 && (!h.kit[id].custo || h.recurso >= h.kit[id].custo);
    if (pronto) pintarForma(g, formaDaAcao(h, id, s.mouse.x, s.mouse.y), cx, cy, null, "rgba(255,245,210,0.38)", 2);
  }
  // o anel do herói
  if (!h.morto) {
    const [hx, hy] = pos(h);
    pintarForma(g, { tipo: "circulo", x: Math.round(hx), y: Math.round(hy), raio: 7 }, cx, cy, null, "rgba(240,203,98,0.75)", 0);
  }

  // ---- os corpos, em ordem de profundidade
  const lista = [];
  for (const u of m.unidades) if (!u.morto && u !== h) lista.push(u);
  lista.sort((p, q) => p.y - q.y);
  const voadores = E.voadores.slice().sort((p, q) => p.y - q.y);
  const tipoDe = (u) => (u.tipo === "heroi" ? u.nomeHeroi : u.tipo);
  // sombras primeiro
  for (const u of lista) { const [x, y] = pos(u); sombra(g, Math.round(x) - cx, Math.round(y) - cy, LARGURA_SOMBRA[u.tipo]); }
  for (const v of voadores) sombra(g, Math.round(v.x) - cx, Math.round(v.y) - cy, Math.max(3, 6 - Math.round(v.z / 8)));
  let iv = 0;
  for (const u of lista) {
    while (iv < voadores.length && voadores[iv].y < u.y) desenharVoador(g, Q, voadores[iv++], cx, cy);
    const [x, y] = pos(u);
    const sp = Q[tipoDe(u)][u.lado][poseTropa(u)];
    const img = u.flash > 0.03 ? (u.virado > 0 ? sp.bd : sp.be) : u.virado > 0 ? sp.d : sp.e;
    g.drawImage(img, Math.round(x - (u.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay) - cy);
    // a vida só das ameaças (sempre) e do veterano (por 1,5 s depois de apanhar): os soldados comuns caem de uma vez
    if (u.def.elite || u.tipo === "veterano" && m.t - (u.ferido ?? -9) < 1.5) {
      const larg = u.tipo === "campeao" ? 16 : 6;
      barra(g, Math.round(x - larg / 2) - cx, Math.round(y - sp.ay) - cy - 4, larg, u.vida / u.vidaMax, "#e05a48", u.tipo === "campeao" ? 2 : 1);
    }
    if (u.atordoado > 0.15 && (u.def.elite || u.tipo === "veterano")) {
      const t = rel * 8, top = Math.round(y - sp.ay) - cy - 2;
      g.fillStyle = "#f0cb62";
      g.fillRect(Math.round(x + Math.cos(t) * 4) - cx, top + Math.round(Math.sin(t) * 1), 1, 1);
      g.fillRect(Math.round(x - Math.cos(t) * 4) - cx, top - Math.round(Math.sin(t) * 1), 1, 1);
    }
    if (u.abalado > 0) { g.fillStyle = "#ffffff"; g.fillRect(Math.round(x) - cx, Math.round(y - sp.ay) - cy - 4, 1, 2); }
  }
  while (iv < voadores.length) desenharVoador(g, Q, voadores[iv++], cx, cy);

  // ---- projéteis
  for (const p of m.proj) {
    if (p.tipo === "flecha") {
      const k = p.t / p.dur, z = Math.sin(Math.PI * k) * Math.min(14, p.dur * 22);
      const dx = p.x1 - p.x0, dy = p.y1 - p.y0, n = Math.hypot(dx, dy) || 1;
      const x = Math.round(p.x) - cx, y = Math.round(p.y - z) - cy;
      g.fillStyle = "#e9e2cc";
      g.fillRect(x, y, 1, 1);
      g.fillStyle = "#8a6a40";
      g.fillRect(Math.round(x - (dx / n) * 2), Math.round(y - (dy / n) * 2 + (k < 0.5 ? 1 : -1)), 1, 1);
      g.fillRect(Math.round(x - dx / n), Math.round(y - dy / n), 1, 1);
    } else if (p.tipo === "faisca") {
      const x = Math.round(p.x) - cx, y = Math.round(p.y) - cy - 6;
      g.fillStyle = "#ff8a30"; g.fillRect(Math.round(x - p.dx * 3), Math.round(y - p.dy * 3), 1, 1);
      g.fillStyle = "#ffe08a"; g.fillRect(x - 1, y - 1, 2, 2);
      g.fillStyle = "#ffffff"; g.fillRect(x, y - 1, 1, 1);
    } else if (p.tipo === "bola") {
      const x = Math.round(p.x) - cx, y = Math.round(p.y - (p.z || 0)) - cy - 6;
      g.fillStyle = "#c63b2b"; g.fillRect(x - 2, y - 1, 5, 3); g.fillRect(x - 1, y - 2, 3, 5);
      g.fillStyle = "#ff8a30"; g.fillRect(x - 1, y - 1, 3, 3);
      g.fillStyle = "#ffe08a"; g.fillRect(x, y, 1, 1);
    }
  }

  // ---- o herói por cima de todos (nunca some no meio da multidão)
  {
    const [x, y] = pos(h);
    const sp = Q[h.nomeHeroi][0][poseHeroi(h)];
    const z = Math.round(h.z || 0);
    if (!h.morto) sombra(g, Math.round(x) - cx, Math.round(y) - cy, 9);
    let img = h.virado > 0 ? sp.d : sp.e;
    if (h.flash > 0.03 && !h.morto) img = h.virado > 0 ? sp.bd : sp.be;
    if (h.invul > 0 && h.acao && h.acao.id === "investida") {
      // os rastros da investida
      g.globalAlpha = 0.35;
      for (let i = 1; i <= 3; i++) g.drawImage(img, Math.round(x - h.vx * 0.012 * i - (h.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - h.vy * 0.012 * i - sp.ay) - cy);
      g.globalAlpha = 1;
    }
    g.drawImage(img, Math.round(x - (h.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - z) - cy);
    if (!h.morto) barra(g, Math.round(x - 7) - cx, Math.round(y - sp.ay - z) - cy - 4, 14, h.vida / h.vidaMax, "#7fd36a");
  }

  // ---- os efeitos por cima
  for (const c of E.cortes) {
    const k = c.t / c.dur, f = c.forma;
    const cor = c.inimigo ? `rgba(255,120,90,${0.55 * (1 - k)})` : `rgba(255,250,230,${(c.forte ? 0.55 : 0.4) * (1 - k)})`;
    // o corte varre o arco: a borda de fora inteira, e o preenchimento só na faixa que o golpe já passou
    const varrido = { ...f, abertura: f.abertura * Math.min(1, 0.35 + k * 2) };
    pintarForma(g, varrido, cx, cy, cor, c.inimigo ? "rgba(255,150,120,0.9)" : `rgba(255,255,255,${0.95 * (1 - k * 0.6)})`);
  }
  for (const ex of E.explosoes) {
    const k = ex.t / ex.dur;
    if (k < 0.18) pintarForma(g, { tipo: "circulo", x: ex.x, y: ex.y, raio: ex.raio }, cx, cy, "rgba(255,236,170,0.75)", "#ffffff");
    else {
      const r = ex.raio * (0.6 + 0.4 * k);
      pintarForma(g, { tipo: "circulo", x: ex.x, y: ex.y, raio: r * 0.55 }, cx, cy, `rgba(255,140,50,${0.45 * (1 - k)})`, null);
      pintarForma(g, { tipo: "circulo", x: ex.x, y: ex.y, raio: r }, cx, cy, null, `rgba(255,${Math.round(200 - 120 * k)},60,${1 - k})`);
    }
  }
  for (const r of E.aneis) {
    const k = r.t / r.dur;
    pintarForma(g, { tipo: "circulo", x: r.x, y: r.y, raio: Math.max(1, r.r0 + (r.r1 - r.r0) * k) }, cx, cy, null, hexAlfa(r.cor, 1 - k));
  }
  for (const p of E.particulas) {
    const k = p.vida / p.max;
    g.globalAlpha = p.fumaca ? 0.32 * (1 - k) : k > 0.7 ? (1 - k) / 0.3 : 1;
    g.fillStyle = p.cor;
    const t = p.fumaca ? Math.round(p.tam + k * 2) : p.tam;
    g.fillRect(Math.round(p.x - t / 2) - cx, Math.round(p.y - p.z - t / 2) - cy, t, t);
  }
  g.globalAlpha = 1;
  for (const msg of E.mensagens) texto(g, msg.texto, msg.x - cx, msg.y - cy - msg.t * 10, "#ffe08a");

  // ---- quem importa e está fora da tela: setas na borda
  for (const u of m.lados[1]) {
    if (!u.def.elite) continue;
    const x = u.x - cx, y = u.y - cy;
    if (x >= 0 && y >= 0 && x < W && y < H) continue;
    seta(g, x, y, W, H, u.tipo === "campeao" ? "#ff5a48" : "#f0cb62");
  }
  // o mouse: uma mira de pixel
  if (s.mouse && !s.semMira) {
    const x = Math.round(s.mouse.x) - cx, y = Math.round(s.mouse.y) - cy;
    g.fillStyle = "#15121a";
    g.fillRect(x - 4, y - 1, 9, 3); g.fillRect(x - 1, y - 4, 3, 9);
    g.fillStyle = "#fff6dc";
    g.fillRect(x - 3, y, 2, 1); g.fillRect(x + 2, y, 2, 1); g.fillRect(x, y - 3, 1, 2); g.fillRect(x, y + 2, 1, 2);
  }
}

function desenharVoador(g, Q, v, cx, cy) {
  const tipo = v.tipo;
  if (!Q[tipo]) return;
  const P = Q[tipo][v.eq];
  let sp;
  if (v.girando && (v.z > 0 || v.vz > 0)) sp = P["giro" + ((Math.floor(v.t * 14) * v.giroDir % 4 + 4) % 4)];
  else sp = P.caido;
  const img = v.giroDir > 0 ? sp.d : sp.e;
  g.drawImage(img, Math.round(v.x - sp.ax) - cx, Math.round(v.y - v.z - sp.ay) - cy);
}

function seta(g, x, y, W, H, cor) {
  const mx = W / 2, my = H / 2, dx = x - mx, dy = y - my;
  const k = Math.min((W / 2 - 8) / Math.abs(dx || 1e-6), (H / 2 - 8) / Math.abs(dy || 1e-6));
  const px = Math.round(mx + dx * k), py = Math.round(my + dy * k), a = Math.atan2(dy, dx);
  g.fillStyle = "#15121a";
  g.fillRect(px - 3, py - 3, 7, 7);
  g.fillStyle = cor;
  for (let i = 0; i < 4; i++) for (let j = -i; j <= i; j++) {
    const ox = Math.round(Math.cos(a) * (2 - i) - Math.sin(a) * j), oy = Math.round(Math.sin(a) * (2 - i) + Math.cos(a) * j);
    g.fillRect(px + ox, py + oy, 1, 1);
  }
}

function hexAlfa(hex, a) {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${Math.max(0, a).toFixed(3)})`;
}

export { TIPOS };
