// PROTÓTIPO de campo livre: o desenho do campo, em pixels nativos (o canvas tem o tamanho do campo visível dividido
// pela ampliação inteira; o CSS amplia sem suavizar). Só lê: o mundo (sim.js), os efeitos (efeitos.js) e as opções.
// As áreas (os avisos do campeão, a preparação do herói, a prévia, os cortes) são pintadas pixel a pixel com a mesma
// função `dentro` que decide quem é atingido: o que aparece é exatamente o que acerta.
import { CAMPO, TIPOS, HARG8 } from "./conteudo.js";
const G8 = HARG8.golpes;
import { dentro, formaDaAcao, alvoAssistido } from "./sim.js";
import { pousarCorpos, NUMEROS } from "./efeitos.js";
import { desenharEstradas, prediosOrdenados, temAtras, desenharPredio, desenharMagias, desenharCargas } from "./desenho6.js";
import { desenharEstradas7, desenharLuzes7, desenharPredio7, cobre } from "./arte7.js";

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

// Os contornos de círculo (auras, presença, alcance de defesa, anéis) se repetem a cada quadro: guardados prontos por
// raio, cor e tracejado, desenhados com o centro arredondado. A forma continua a mesma de `dentro`.
const contornos = new Map();
function contornoCirculo(g, f, cx, cy, borda, tracejado) {
  const r = f.raio, chave = `${r}|${borda}|${tracejado}`;
  let c = contornos.get(chave);
  if (!c) {
    const lado = Math.ceil(r) * 2 + 4;
    c = document.createElement("canvas");
    c.width = c.height = lado;
    pintarForma(c.getContext("2d"), { tipo: "circulo", x: lado / 2, y: lado / 2, raio: r }, 0, 0, null, borda, tracejado, true);
    if (contornos.size > 400) contornos.clear();
    contornos.set(chave, c);
  }
  g.drawImage(c, Math.round(f.x) - c.width / 2 - cx, Math.round(f.y) - c.height / 2 - cy);
}

// Pinta uma forma pixel a pixel (o centro de cada pixel testado com `dentro`); a borda é quem tem um vizinho fora.
function pintarForma(g, f, cx, cy, preenche, borda, tracejado = 0, direto = false) {
  // só os grandes (auras e alcance de defesa, ≥ 50 px), que não são áreas de golpe: estas seguem exatas, sem arredondar o centro
  if (!direto && !preenche && f.tipo === "circulo" && f.raio >= 50 && Number.isInteger(f.raio)) return contornoCirculo(g, f, cx, cy, borda, tracejado);
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

// Os algarismos dos números de dano, 3 × 5 pixels desenhados à mão (e o "!" do crítico): nítidos em qualquer
// ampliação, com um contorno escuro de 1 px que os separa de qualquer fundo.
const DIGITOS = {
  0: ["111", "101", "101", "101", "111"], 1: ["010", "110", "010", "010", "111"], 2: ["111", "001", "111", "100", "111"],
  3: ["111", "001", "011", "001", "111"], 4: ["101", "101", "111", "001", "001"], 5: ["111", "100", "111", "001", "111"],
  6: ["111", "100", "111", "101", "111"], 7: ["111", "001", "010", "010", "010"], 8: ["111", "101", "111", "101", "111"],
  9: ["111", "101", "111", "001", "111"], "!": ["1", "1", "1", "0", "1"],
};
const COR_NUMERO = { normal: "#ffffff", forte: "#ffd84a", critico: "#ff8a3a", fogo: "#ffa45a", sangue: "#ff6060",
  sofrido: "#ff4040", abertura: "#ffe46a" };

export function numeroPixel(g, texto, x, y, cor, esc = 1) {
  const pts = [];
  let ox = 0;
  for (const ch of texto) {
    const gl = DIGITOS[ch];
    if (!gl) continue;
    for (let r = 0; r < 5; r++) for (let c = 0; c < gl[r].length; c++) if (gl[r][c] === "1") pts.push([ox + c, r]);
    ox += gl[0].length + 1;
  }
  const larg = (ox - 1) * esc, x0 = Math.round(x - larg / 2), y0 = Math.round(y);
  g.fillStyle = "#15121a";
  for (const [px, py] of pts) g.fillRect(x0 + px * esc - 1, y0 + py * esc - 1, esc + 2, esc + 2);
  g.fillStyle = cor;
  for (const [px, py] of pts) g.fillRect(x0 + px * esc, y0 + py * esc, esc, esc);
}

function sombra(g, x, y, larg, cor = "rgba(10,14,8,0.32)") {
  g.fillStyle = cor;
  const m = Math.floor(larg / 2);
  g.fillRect(x - m, y, larg, 1);
  g.fillRect(x - m + 1, y + 1, larg - 2, 1);
}

const LARGURA_SOMBRA = { soldado: 6, arqueiro: 6, veterano: 7, estandarte: 6, campeao: 11, lider: 12, heroi: 9, cavaleiro: 10, pesado: 7, magoBatalha: 6, morel: 9, odette: 8, ardis: 9 };
// a sombra tingida pela cor do lado: no meio do choque, o pé de cada um diz de que lado ele está
const SOMBRA_LADO = ["rgba(20,40,110,0.5)", "rgba(110,16,16,0.5)"];

function poseTropa(u) {
  // Campo Livre 8: Harg pelo tempo do golpe (a preparação, o contato, o machado preso na abertura, de joelhos na quebra)
  const s = u.h8;
  if (s) {
    if (s.quebrado > 0) return "recuo";
    const g = s.golpe;
    if (g) return g.etapa === "preparo" ? "preparo" : g.etapa === "exec" || g.total - g.t < 0.18 ? "golpe" : G8[g.id].abertura === true ? "recuo" : "parado";
  }
  if (u.atordoado > 0 || u.congelado > 0) return "recuo";
  if (u.mostra > 0) return "golpe";
  if (u.acao) return u.acao.t > 0.08 ? "preparo" : "golpe";
  if (Math.abs(u.vx) + Math.abs(u.vy) > 2) return ["andarA", "parado", "andarB", "parado"][Math.floor(u.passo / 3) % 4];
  return "parado";
}

function poseHeroi(h) {
  if (h.morto) return "caido";
  if (h.atordoado > 0 || h.dorAte > h.tAgora) return "recuo";   // a dor do golpe recebido: 0,12 s, só no desenho
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
  const cx = Math.round(cam.x), cy = Math.round(cam.y), arte = s.arte || "atual", nova = arte !== "atual";
  pousarCorpos(E, Q);
  g.imageSmoothingEnabled = false;
  g.drawImage(s.chao, -cx - BORDA, -cy - BORDA);
  const h = m.heroi, rel = s.relogio;
  // Campo Livre 7: nas direções novas do estudo, a estrada vai embaixo das marcas (o sangue fica nela) e a luz das tochas
  // por cima do chão; na atual, como antes
  if (nova) { desenharEstradas7(g, m, cx, cy, arte); g.drawImage(E.marcas, -cx, -cy); desenharLuzes7(g, m, cx, cy, arte, rel); }
  else { g.drawImage(E.marcas, -cx, -cy); desenharEstradas(g, m, cx, cy); }
  // a posição interpolada, com o tranco do acerto (heróis e ameaças: 1 px no golpe fraco, 2 no forte, na direção dele)
  const pos = (u) => {
    const t = u.tranco, o = t ? (t.forte ? 2 : 1) * Math.min(1, t.t / 0.08) : 0;
    return [u.px + (u.x - u.px) * alfa + (t ? Math.round(t.dx * o) : 0), u.py + (u.y - u.py) * alfa + (t ? Math.round(t.dy * o) : 0)];
  };

  // ---- o chão: fogo, aura do estandarte, ordem, avisos, prévias
  for (const z of m.zonas) {
    const fim = Math.min(1, z.t / 0.4);
    if (z.tipo === "gelo") {
      // o Campo de Gelo: o círculo exato (a mesma regra de quem fica lento), claro por dentro, e cristais que piscam
      pintarForma(g, { tipo: "circulo", x: z.x, y: z.y, raio: z.raio }, cx, cy, `rgba(190,230,255,${0.16 * fim})`, `rgba(220,245,255,${0.75 * fim})`, 2);
      const n = Math.round(z.raio * 0.9 * fim);
      for (let i = 0; i < n; i++) {
        const a = i * 2.399, r = Math.sqrt((i * 0.618) % 1) * (z.raio - 2);
        if ((i + Math.floor(rel * 4)) % 5 === 0) continue;
        g.fillStyle = i % 3 ? "#cfeeff" : "#ffffff";
        g.fillRect(Math.round(z.x + Math.cos(a) * r) - cx, Math.round(z.y + Math.sin(a) * r) - cy, 1, 1);
      }
      continue;
    }
    if (z.tipo === "chao") {
      const n = Math.round(z.raio * z.raio * 0.12 * fim);
      for (let i = 0; i < n; i++) {
        const a = (i * 2.399 + Math.floor(rel * 9) * 0.7) % (Math.PI * 2), r = Math.sqrt(((i * 0.618 + Math.floor(rel * 7) * 0.13) % 1)) * z.raio;
        const x = Math.round(z.x + Math.cos(a) * r) - cx, y = Math.round(z.y + Math.sin(a) * r) - cy;
        g.fillStyle = i % 3 ? "#ff8a30" : "#ffe08a";
        g.fillRect(x, y - (i % 2), 1, 1 + (i % 2));
      }
    } else if (z.tipo === "vortice") {
      // o Vórtice: braços em espiral girando para dentro
      const k = 1 - z.t / z.dur;
      pintarForma(g, { tipo: "circulo", x: z.x, y: z.y, raio: z.raio }, cx, cy, null, "rgba(190,150,255,0.5)", 3);
      for (let b = 0; b < 4; b++) for (let i = 0; i < 14; i++) {
        const r = z.raio * (1 - i / 14), a = b * Math.PI / 2 + i * 0.35 + rel * 5;
        g.fillStyle = i % 3 ? "#9a6cff" : "#e0d0ff";
        g.fillRect(Math.round(z.x + Math.cos(a) * r) - cx, Math.round(z.y + Math.sin(a) * r * 0.8) - cy, 1, 1);
      }
      void k;
    } else if (z.tipo === "rachado") {
      // o chão rachado do Tremor Residual: fendas escuras com pó subindo
      pintarForma(g, { tipo: "circulo", x: z.x, y: z.y, raio: z.raio }, cx, cy, "rgba(60,40,20,0.12)", "rgba(120,90,50,0.5)", 3);
      for (let i = 0; i < 18; i++) {
        const a = i * 2.399, r = Math.sqrt((i * 0.618) % 1) * z.raio;
        if ((i + Math.floor(rel * 6)) % 4 === 0) { g.fillStyle = "#b8a27a"; g.fillRect(Math.round(z.x + Math.cos(a) * r) - cx, Math.round(z.y + Math.sin(a) * r) - cy - 1, 1, 1); }
      }
    } else if (z.tipo === "anel") {
      const n = Math.floor((2 * Math.PI * z.raio) / 3);
      for (let i = 0; i < n; i++) {
        const an = (i / n) * Math.PI * 2, x = Math.round(z.x + Math.cos(an) * z.raio) - cx, y = Math.round(z.y + Math.sin(an) * z.raio) - cy;
        const alt = Math.round((2 + ((i * 7 + Math.floor(rel * 10)) % 4)) * fim);
        g.fillStyle = "#a8361f"; g.fillRect(x - 1, y, 3, 1);
        g.fillStyle = "#ff8a30"; g.fillRect(x, y - alt, 1, alt);
        g.fillStyle = "#ffe08a"; g.fillRect(x, y - Math.max(1, alt - 2), 1, 1);
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
  // uma bandeira por ponto de defesa ainda em uso; o círculo do alcance aparece pausado, logo depois da ordem e
  // quando alguém daquele grupo está selecionado
  const pontos = new Map();
  for (const u of m.lados[0]) {
    const o = u.ordem;
    if (!o || o.tipo !== "defender") continue;
    const k = `${Math.round(o.x)}:${Math.round(o.y)}`;
    const p = pontos.get(k) || { x: o.x, y: o.y, sel: false };
    if (m.selecao && m.selecao.has(u.id)) p.sel = true;
    pontos.set(k, p);
  }
  for (const p of pontos.values()) {
    const x = Math.round(p.x) - cx, y = Math.round(p.y) - cy;
    const recente = E.ordem && E.ordem.tipo === "defender" && E.ordem.t < 3 && Math.hypot(E.ordem.x - p.x, E.ordem.y - p.y) < 1;
    if (s.pausado || p.sel || recente) pintarForma(g, { tipo: "circulo", x: p.x, y: p.y, raio: 85 }, cx, cy, null, "rgba(140,190,255,0.4)", 3);
    g.fillStyle = "#6a4521"; g.fillRect(x, y - 12, 1, 12);
    g.fillStyle = p.sel ? "#bff4ff" : "#76a8ea"; g.fillRect(x + 1, y - 12, 5, 3);
    g.fillStyle = "#4778c2"; g.fillRect(x + 1, y - 9, 4, 1);
  }
  if (E.ordem && E.ordem.tipo !== "defender" && E.ordem.t < 0.6) {
    const r = 8 + E.ordem.t * 90;
    pintarForma(g, { tipo: "circulo", x: h.x, y: h.y, raio: r }, cx, cy, null, `rgba(140,190,255,${0.6 - E.ordem.t})`, 2);
  }
  // os avisos do campeão: o arco que o machado vai varrer, enchendo até o golpe
  const avisos = [];
  for (const u of m.lados[1]) {
    if (!u.acao || !u.acao.forma) continue;
    if (u.tipo !== "campeao" && u.tipo !== "lider") continue;
    let k;
    if (u.acao.tipo === "reunir") k = 1 - Math.max(0, u.acao.t) / u.def.carga.reunir;
    else if (u.acao.tipo === "carga") k = 1;
    else if (u.acao.tipo === "arremetida") k = u.acao.fase === "voo" ? 1 : 1 - Math.max(0, u.acao.t) / u.def.arremetida.preparo;
    else if (u.acao.tipo === "rodopio") k = 1 - Math.max(0, u.acao.t) / u.def.rodopio.preparo;
    else k = 1 - Math.max(0, u.acao.t) / (u.acao.preparo || u.def.preparo);
    avisos.push(u.acao.forma);
    pintarForma(g, u.acao.forma, cx, cy, `rgba(220,40,30,${0.12 + 0.3 * k})`, "rgba(255,90,70,0.95)");
  }
  // Campo Livre 8: os golpes de Harg reconstruído: a forma do golpe enchendo na preparação (a onda da fase 2, tracejada,
  // em volta), por baixo e de novo por cima dos corpos; na fase 2, o anel vermelho pulsando no chão; a abertura, dourada
  for (const u of m.lados[1]) {
    const h8 = u.h8;
    if (!h8 || u.morto) continue;
    const gp = h8.golpe;
    if (gp && gp.etapa === "preparo") {
      const k = 1 - Math.max(0, gp.t) / G8[gp.id].preparo;
      if (gp.onda) pintarForma(g, gp.onda, cx, cy, null, "rgba(255,150,110,0.7)", 3);
      avisos.push(gp.forma);
      pintarForma(g, gp.forma, cx, cy, `rgba(220,40,30,${0.1 + 0.36 * k})`, "rgba(255,90,70,0.95)");
    }
    if (h8.fase === 2 && !h8.quebrado) pintarForma(g, { tipo: "circulo", x: Math.round(u.x), y: Math.round(u.y), raio: 11 + (Math.floor(rel * 6) % 2) }, cx, cy, null, "rgba(255,70,50,0.7)", 0);
    if (h8.quebrado > 0 || m.t < (h8.abertoAte || 0)) pintarForma(g, { tipo: "circulo", x: Math.round(u.x), y: Math.round(u.y), raio: 13 }, cx, cy, "rgba(255,220,100,0.14)", "rgba(255,226,120,0.95)", 0);
  }
  // Campo Livre 7: a Investida Curta (a faixa enchendo na preparação), o Brado (o anel) e o Grilhão (as mãos de Ardis)
  for (const u of m.lados[1]) {
    if (u.morto) continue;
    const D = u.dash7;
    if (D && D.fase === "preparo") {
      const k = 1 - Math.max(0, D.t) / u.def.investida7.preparo;
      const f = { tipo: "faixa", x1: u.x, y1: u.y, x2: u.x + D.dx * D.comp, y2: u.y + D.dy * D.comp, largura: u.def.investida7.largura };
      avisos.push(f);
      pintarForma(g, f, cx, cy, `rgba(220,40,30,${0.12 + 0.35 * k})`, "rgba(255,90,70,0.95)");
    }
    if (u.brado7) {
      const k = 1 - Math.max(0, u.brado7.t) / u.def.brado.preparo, f = { tipo: "circulo", x: u.x, y: u.y, raio: u.def.brado.raio };
      pintarForma(g, f, cx, cy, `rgba(255,170,60,${0.05 + 0.12 * k})`, "rgba(255,190,90,0.9)", 3);
    }
    if (u.acaoA && u.acaoA.tipo === "grilhao") {
      pintarForma(g, { tipo: "circulo", x: u.x, y: u.y - 4, raio: 4 + Math.floor(rel * 12) % 2 }, cx, cy, "rgba(170,120,255,0.35)", "rgba(220,200,255,0.95)");
    }
  }
  // Campo Livre 6: as magias anunciadas (magos de batalha, Ardis) e as cargas da cavalaria
  desenharMagias(g, m, cx, cy, pintarForma, rel);
  desenharCargas(g, m, cx, cy, rel);
  // o anel do líder inimigo, vermelho, como o dourado do herói
  if (m.lider && !m.lider.morto) {
    const [lx, ly] = pos(m.lider);
    // firme (logo depois de ser interrompido): o anel fica claro, sinal de que agora o golpe forte não o segura
    const firme = m.lider.firmeAte > m.t;
    pintarForma(g, { tipo: "circulo", x: Math.round(lx), y: Math.round(ly), raio: 9 }, cx, cy, null, firme ? "rgba(255,220,200,0.9)" : "rgba(255,70,50,0.8)", 0);
    pintarForma(g, { tipo: "circulo", x: Math.round(lx), y: Math.round(ly), raio: m.lider.def.presenca }, cx, cy, null, "rgba(230,80,60,0.16)", 5);
  }
  // os alvos das ordens de atacar um alvo: uma mira vermelha em volta de cada um
  const focos = new Set();
  for (const u of m.lados[0]) if (u.ordem && u.ordem.alvoU && !u.ordem.encerrada && !u.ordem.alvoU.morto) focos.add(u.ordem.alvoU);
  for (const a of focos) {
    const [fx, fy] = pos(a), r = Math.round(a.raio + 5 + (Math.floor(rel * 4) % 2)), x = Math.round(fx) - cx, y = Math.round(fy) - 3 - cy;
    g.fillStyle = "#15121a";
    for (const [sx, sy] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { g.fillRect(x + sx * r - 1, y + sy * r - 1, 3, 3); }
    g.fillStyle = "#ff4a3a";
    for (const [sx, sy] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
      g.fillRect(x + sx * r - (sx > 0 ? 2 : 0), y + sy * r, 3, 1);
      g.fillRect(x + sx * r, y + sy * r - (sy > 0 ? 2 : 0), 1, 3);
    }
  }
  // o alvo do ataque básico (a assistência): dois cantos claros no pé de quem o golpe vai pegar
  if (s.alvoBasico && !h.morto && s.mouse) {
    const a = alvoAssistido(m, h, s.mouse.x, s.mouse.y);
    if (a) {
      const [ax, ay] = pos(a), x = Math.round(ax) - cx, y = Math.round(ay) - cy, r = Math.round(a.raio) + 2;
      g.fillStyle = "#fff6dc";
      g.fillRect(x - r, y + 1, 2, 1); g.fillRect(x - r, y, 1, 1);
      g.fillRect(x + r - 1, y + 1, 2, 1); g.fillRect(x + r, y, 1, 1);
    }
  }
  // a preparação do herói e os pontos de chegada
  const a = h.acao;
  if (a && !h.morto) {
    if (a.fase === "preparo" && a.id !== "basico" && a.forma) {
      const f = a.forma.fixa || a.forma.tipo === "faixa" ? a.forma : { ...a.forma, x: h.x, y: h.y };
      // o Turbilhão: o alcance do puxão, tracejado, em volta do círculo do golpe
      if (f.puxa) pintarForma(g, { tipo: "circulo", x: f.x, y: f.y, raio: f.puxa }, cx, cy, null, "rgba(255,245,210,0.6)", 3);
      pintarForma(g, f, cx, cy, "rgba(255,245,210,0.12)", "rgba(255,245,210,0.85)");
    }
    if (a.fase === "escudo" && a.forma) {
      // o Avanço de Escudo: o arco do escudo (barra flechas e empurra) e, tracejado, quem fica protegido
      pintarForma(g, { tipo: "circulo", x: h.x, y: h.y, raio: h.kit.escudo.protege }, cx, cy, null, "rgba(170,210,255,0.45)", 3);
      pintarForma(g, a.forma, cx, cy, "rgba(170,210,255,0.16)", "rgba(200,230,255,0.9)");
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
  for (const u of lista) {
    const [x, y] = pos(u), sx = Math.round(x) - cx, sy = Math.round(y) - cy;
    sombra(g, sx, sy, LARGURA_SOMBRA[u.tipo], SOMBRA_LADO[u.lado]);
    if (m.selecao && m.selecao.has(u.id)) {
      // selecionado: um colchete claro em volta do pé
      g.fillStyle = "#bff4ff";
      g.fillRect(sx - 4, sy - 1, 1, 3); g.fillRect(sx + 4, sy - 1, 1, 3);
      g.fillRect(sx - 3, sy + 2, 2, 1); g.fillRect(sx + 2, sy + 2, 2, 1);
    }
  }
  for (const v of voadores) sombra(g, Math.round(v.x) - cx, Math.round(v.y) - cy, Math.max(3, 6 - Math.round(v.z / 8)));
  let iv = 0;
  // as construções entram na mesma ordem de profundidade (pela base); translúcidas quando há alguém atrás delas
  // (nas direções novas, opacas: quem está atrás aparece em silhueta, depois)
  const predios = prediosOrdenados(m), translucido = nova ? null : new Map(predios.map((o) => [o, temAtras(m, o)]));
  const predio = (o) => (nova ? desenharPredio7(g, o, cx, cy, arte, rel) : desenharPredio(g, o, cx, cy, translucido.get(o) ? 0.62 : 1));
  let ip = 0;
  for (const u of lista) {
    while (iv < voadores.length && voadores[iv].y < u.y) desenharVoador(g, Q, voadores[iv++], cx, cy);
    while (ip < predios.length && predios[ip].y + predios[ip].h < u.y) predio(predios[ip++]);
    const [x, y] = pos(u);
    const sp = Q[tipoDe(u)][u.lado][poseTropa(u)];
    const img = u.flash > 0.03 ? (u.virado > 0 ? sp.bd : sp.be) : u.virado > 0 ? sp.d : sp.e;
    g.drawImage(img, Math.round(x - (u.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - (u.z || 0)) - cy);
    // a vida só das ameaças (sempre) e do veterano (por 1,5 s depois de apanhar): os soldados comuns caem de uma vez
    // a vida: sempre nas ameaças; no veterano, só por 0,8 s depois de apanhar, curta, para o choque não virar barras
    if (u.def.elite || u.tipo === "veterano" && m.t - (u.ferido ?? -9) < 0.8) {
      const grande = u.tipo === "campeao" || u.tipo === "lider" || u.def.heroiInimigo || u.def.companheiro, larg = u.tipo === "lider" || u.tipo === "ardis" ? 18 : grande ? 14 : 5;
      barra(g, Math.round(x - larg / 2) - cx, Math.round(y - sp.ay) - cy - 4, larg, u.vida / u.vidaMax, u.lado === 0 ? "#6fbf5d" : "#e05a48", grande ? 2 : 1);
    }
    const topo = Math.round(y - sp.ay) - cy;
    // o Sangramento: uma gota por acúmulo (até 5), descendo
    if (u.sangra) {
      g.fillStyle = "#c8282a";
      for (let i = 0; i < u.sangra.acum; i++) g.fillRect(Math.round(x + 2 - i * 1.5) - cx, topo + 3 + ((Math.floor(rel * 6) + u.id + i * 2) % 4), 1, 1);
    }
    // congelado: a silhueta coberta de gelo; enregelado: dois pontos azuis
    if (u.gelo > m.t) {
      g.fillStyle = "rgba(190,230,255,0.75)";
      g.fillRect(Math.round(x - 3) - cx, topo + 1, 7, Math.round(sp.ay - 2));
      g.fillStyle = "#ffffff"; g.fillRect(Math.round(x - 2) - cx, topo + 2, 1, 1); g.fillRect(Math.round(x + 2) - cx, topo + 5, 1, 1);
    } else if (u.enregelado > m.t) { g.fillStyle = "#9fd8ff"; g.fillRect(Math.round(x - 3) - cx, topo + 2, 1, 1); g.fillRect(Math.round(x + 3) - cx, topo + 4, 1, 1); }
    // a Brasa da Ignição: um ponto laranja piscando em cima
    if (u.brasa > m.t) { g.fillStyle = Math.floor(rel * 8 + u.id) % 2 ? "#ffb15a" : "#fff1c4"; g.fillRect(Math.round(x) - cx, topo - 2, 1, 1); }
    if (u.inspirado > 0 && Math.floor(rel * 5 + u.id) % 3 === 0) { g.fillStyle = "#ffe08a"; g.fillRect(Math.round(x - 2) - cx, topo + 1, 1, 1); }
    if (u.reuniao) { g.fillStyle = "#ff5a48"; g.fillRect(Math.round(x) - cx, topo - 4, 1, 2); g.fillRect(Math.round(x) - cx, topo - 1, 1, 1); }
    if ((u.atordoado > 0.15 || u.ofegante > 0) && (u.def.elite || u.tipo === "veterano")) {
      const t = rel * 8, top = Math.round(y - sp.ay) - cy - 2;
      g.fillStyle = "#f0cb62";
      g.fillRect(Math.round(x + Math.cos(t) * 4) - cx, top + Math.round(Math.sin(t) * 1), 1, 1);
      g.fillRect(Math.round(x - Math.cos(t) * 4) - cx, top - Math.round(Math.sin(t) * 1), 1, 1);
    }
    if (u.abalado > 0) { g.fillStyle = "#ffffff"; g.fillRect(Math.round(x) - cx, Math.round(y - sp.ay) - cy - 4, 1, 2); }
    if (u.h8 && !u.h8.quebrado && u.h8.postura / HARG8.postura.max >= 0.7 && Math.floor(rel * 10 + u.id) % 3 === 0) {
      g.fillStyle = "#ffe08a";
      g.fillRect(Math.round(x - 4 + ((Math.floor(rel * 13) * 5) % 9)) - cx, Math.round(y - sp.ay + 2 + ((Math.floor(rel * 11) * 3) % 7)) - cy, 1, 1);
    }
    if (u.gelado > 0) { g.fillStyle = "#cfeeff"; g.fillRect(Math.round(x + 2) - cx, topo + 2, 1, 1); g.fillRect(Math.round(x - 3) - cx, topo + 5, 1, 1); }
  }
  while (iv < voadores.length) desenharVoador(g, Q, voadores[iv++], cx, cy);
  while (ip < predios.length) predio(predios[ip++]);
  // Campo Livre 7: quem está atrás de uma construção alta ou debaixo de uma copa aparece em silhueta (azul os nossos,
  // vermelho os inimigos) por cima dela; a construção continua inteira
  const coberto = (u) => nova && predios.some((o) => o.alto > 8 && cobre(o, u) && u.y < o.y + o.h);
  if (nova) {
    g.globalAlpha = 0.55;
    for (const u of lista) {
      if (u === m.lider || !coberto(u)) continue;
      const [x, y] = pos(u), sp = Q[tipoDe(u)][u.lado][poseTropa(u)];
      g.drawImage(u.virado > 0 ? sp.sd : sp.se, Math.round(x - (u.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - (u.z || 0)) - cy);
    }
    g.globalAlpha = 1;
  }
  // as peças que voam de quem morre (a arma, o elmo, às vezes um pedaço), até pousarem nas marcas
  for (const p of E.pecas || []) {
    g.fillStyle = p.forma === "cabeca" || p.forma === "braco" ? "#c99a7a" : "#b8bcc4";
    g.fillRect(Math.round(p.x) - cx, Math.round(p.y - p.z) - cy, 2, p.giro % 2 ? 1 : 2);
  }

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
    } else if (p.tipo === "lanca") {
      // a Lança de Gelo: um estilhaço comprido na direção dela
      const x = Math.round(p.x) - cx, y = Math.round(p.y) - cy - 6;
      g.fillStyle = "#4f8fd8";
      for (let i = 2; i <= 7; i++) g.fillRect(Math.round(x - p.dx * i), Math.round(y - p.dy * i), 1, 1);
      g.fillStyle = "#cfeeff";
      for (let i = 0; i <= 3; i++) g.fillRect(Math.round(x - p.dx * i), Math.round(y - p.dy * i), 1, 1);
      g.fillStyle = "#ffffff"; g.fillRect(x, y, 1, 1);
    } else if (p.tipo === "onda") {
      // a onda do Golpe Sísmico: o chão levantando numa frente perpendicular à direção
      const x = Math.round(p.x) - cx, y = Math.round(p.y) - cy;
      for (let i = -p.k.largura; i <= p.k.largura; i += 2) {
        const qx = Math.round(x - p.dy * i), qy = Math.round(y + p.dx * i), alt = 1 + ((i * 7 + Math.floor(rel * 20)) & 3);
        g.fillStyle = "#6c5a40"; g.fillRect(qx, qy, 2, 1);
        g.fillStyle = "#b8a27a"; g.fillRect(qx, qy - alt, 1, alt);
      }
    } else if (p.tipo === "meteoro") {
      // o meteoro: o círculo marcado enchendo e a pedra caindo do alto
      const k = p.t / p.dur;
      pintarForma(g, { tipo: "circulo", x: p.x, y: p.y, raio: p.k.raio }, cx, cy, `rgba(255,120,40,${0.08 + 0.2 * k})`, "rgba(255,150,70,0.9)");
      const x = Math.round(p.x) - cx, y = Math.round(p.y - (1 - k) * 90) - cy;
      g.fillStyle = "#5a2a14"; g.fillRect(x - 2, y - 2, 5, 5);
      g.fillStyle = "#ff8a30"; g.fillRect(x - 1, y - 1, 3, 3);
      g.fillStyle = "#ffe08a"; g.fillRect(x, y + 3, 1, 2); g.fillRect(x - 1, y + 5, 1, 1);
    } else if (p.tipo === "bola") {
      const x = Math.round(p.x) - cx, y = Math.round(p.y - (p.z || 0)) - cy - 6;
      g.fillStyle = "#c63b2b"; g.fillRect(x - 2, y - 1, 5, 3); g.fillRect(x - 1, y - 2, 3, 5);
      g.fillStyle = "#ff8a30"; g.fillRect(x - 1, y - 1, 3, 3);
      g.fillStyle = "#ffe08a"; g.fillRect(x, y, 1, 1);
    }
  }

  const liderCoberto = m.lider && !m.lider.morto && coberto(m.lider);
  if (m.lider && !m.lider.morto) {
    const l = m.lider, [x, y] = pos(l), sp = Q.lider[1][poseTropa(l)], z = Math.round(l.z || 0);
    const img = liderCoberto ? (l.virado > 0 ? sp.sd : sp.se) : l.flash > 0.03 ? (l.virado > 0 ? sp.bd : sp.be) : l.virado > 0 ? sp.d : sp.e;
    if (liderCoberto) g.globalAlpha = 0.7;
    g.drawImage(img, Math.round(x - (l.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - z) - cy);
    g.globalAlpha = 1;
    barra(g, Math.round(x - 9) - cx, Math.round(y - sp.ay - z) - cy - 4, 18, l.vida / l.vidaMax, "#e05a48", 2);
  }
  // os avisos de novo, só a borda, por cima dos corpos: o golpe preparado não se esconde atrás da multidão
  for (const f of avisos) pintarForma(g, f, cx, cy, null, "rgba(255,110,90,0.55)", 2);

  // ---- o herói por cima de todos (nunca some no meio da multidão)
  {
    const [x, y] = pos(h);
    const sp = Q[h.nomeHeroi][0][poseHeroi(h)];
    const z = Math.round(h.z || 0);
    if (!h.morto) sombra(g, Math.round(x) - cx, Math.round(y) - cy, 9);
    // o golpe que o herói levou: um arco vermelho no chão, do lado de quem bateu, mais longo e grosso quanto mais pesou
    const gh = E.golpeHeroi;
    if (gh && !h.morto && !gh.sem) {
      const k = 1 - gh.t / gh.dur, meia = 0.45 + 0.7 * gh.forca, n = 10 + Math.round(10 * gh.forca);
      g.fillStyle = `rgba(255,${Math.round(70 - 40 * gh.forca)},50,${(0.5 + 0.5 * gh.forca) * k})`;
      for (let i = 0; i <= n; i++) {
        const a = gh.ang - meia + (2 * meia * i) / n;
        for (let r = 0; r < (gh.forca > 0.5 ? 2 : 1); r++) {
          g.fillRect(Math.round(x + Math.cos(a) * (10 + r)) - cx, Math.round(y + Math.sin(a) * (10 + r) * 0.8) - cy, 1, 1);
        }
      }
    }
    let img = h.virado > 0 ? sp.d : sp.e;
    if (h.flash > 0.03 && !h.morto) img = h.virado > 0 ? sp.bd : sp.be;
    if (h.invul > 0 && h.acao && h.acao.id === "investida") {
      // os rastros da investida
      g.globalAlpha = 0.35;
      for (let i = 1; i <= 3; i++) g.drawImage(img, Math.round(x - h.vx * 0.012 * i - (h.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - h.vy * 0.012 * i - sp.ay) - cy);
      g.globalAlpha = 1;
    }
    g.drawImage(img, Math.round(x - (h.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - z) - cy);
    if (!h.morto) {
      const tx = Math.round(x) - cx, ty = Math.round(y - sp.ay - z) - cy - 4;
      barra(g, tx - 7, ty, 14, h.vida / h.vidaMax, "#7fd36a");
      // a seta dourada em cima: o herói se acha mesmo no meio do choque
      g.fillStyle = "#15121a"; g.fillRect(tx - 3, ty - 6, 7, 4);
      g.fillStyle = "#f0cb62"; g.fillRect(tx - 2, ty - 5, 5, 1); g.fillRect(tx - 1, ty - 4, 3, 1); g.fillRect(tx, ty - 3, 1, 1);
    }
  }

  // Campo Livre 6: o herói atrás de uma construção: ela por cima dele, translúcida (ele não some e a ordem se lê).
  // Campo Livre 7, nas direções novas: ela por cima, inteira, e a silhueta clara dele por cima dela
  let heroiCoberto = false;
  if (!h.morto && !nova) for (const o of predios) if (h.y < o.y + o.h && h.y > o.y - o.alto - 14 && h.x > o.x - 8 && h.x < o.x + o.w + 8) desenharPredio(g, o, cx, cy, 0.45);
  if (!h.morto && nova) for (const o of predios) if (o.alto > 8 && cobre(o, h) && h.y < o.y + o.h) { desenharPredio7(g, o, cx, cy, arte, rel); heroiCoberto = true; }
  if (heroiCoberto) {
    const [x, y] = pos(h), sp = Q[h.nomeHeroi][0][poseHeroi(h)];
    g.globalAlpha = 0.8;
    g.drawImage(h.virado > 0 ? sp.bd : sp.be, Math.round(x - (h.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - Math.round(h.z || 0)) - cy);
    g.globalAlpha = 1;
  }
  marcasDeControle(g, m, pos, Q, tipoDe, cx, cy, rel);

  // ---- os efeitos por cima
  for (const c of E.cortes) {
    const k = c.t / c.dur, f = c.forma;
    const cor = c.inimigo ? `rgba(255,120,90,${0.55 * (1 - k)})` : `rgba(255,250,230,${(c.forte ? 0.55 : 0.4) * (1 - k)})`;
    // o corte varre o arco: a borda de fora inteira, e o preenchimento só na faixa que o golpe já passou
    const varrido = { ...f, abertura: f.abertura * Math.min(1, 0.35 + k * 2) };
    pintarForma(g, varrido, cx, cy, cor, c.inimigo ? "rgba(255,150,120,0.9)" : `rgba(255,255,255,${0.95 * (1 - k * 0.6)})`);
  }
  // as explosões: fogo (a Bola, os meteoros, a Brasa), gelo (o Estilhaçar, a Lança Estilhaçante), sangue, arcano
  const CORES_EXPLOSAO = { gelo: [[220, 245, 255], [120, 190, 255]], sangue: [[255, 160, 150], [200, 30, 30]],
    arcano: [[230, 210, 255], [160, 100, 255]] };
  for (const ex of E.explosoes) {
    const k = ex.t / ex.dur, c = CORES_EXPLOSAO[ex.cor];
    if (k < 0.18) pintarForma(g, { tipo: "circulo", x: ex.x, y: ex.y, raio: ex.raio }, cx, cy, c ? `rgba(${c[0]},0.7)` : "rgba(255,236,170,0.75)", "#ffffff");
    else {
      const r = ex.raio * (0.6 + 0.4 * k);
      pintarForma(g, { tipo: "circulo", x: ex.x, y: ex.y, raio: r * 0.55 }, cx, cy, c ? `rgba(${c[1]},${0.45 * (1 - k)})` : `rgba(255,140,50,${0.45 * (1 - k)})`, null);
      pintarForma(g, { tipo: "circulo", x: ex.x, y: ex.y, raio: r }, cx, cy, null, c ? `rgba(${c[1]},${1 - k})` : `rgba(255,${Math.round(200 - 120 * k)},60,${1 - k})`);
    }
  }
  for (const r of E.raios) {
    // a Corrente de Raios: segmentos em zigue-zague entre os alvos, que mudam a cada 0,05 s e somem
    const k = r.t / r.dur, quadro = Math.floor(r.t / 0.05);
    g.globalAlpha = k < 0.5 ? 1 : (1 - k) * 2;
    for (let i = 1; i < r.pontos.length; i++) {
      const a = r.pontos[i - 1], b = r.pontos[i], dx = b.x - a.x, dy = b.y - a.y, n = Math.max(1, Math.round(Math.hypot(dx, dy) / 3));
      for (let j = 0; j <= n; j++) {
        const t = j / n, des = j === 0 || j === n ? 0 : (((r.semente + i * 31 + j * 17 + quadro * 7) % 5) - 2) * 0.8;
        const px = Math.round(a.x + dx * t - (dy / (Math.hypot(dx, dy) || 1)) * des) - cx;
        const py = Math.round(a.y + dy * t + (dx / (Math.hypot(dx, dy) || 1)) * des) - cy;
        g.fillStyle = "#6fb8ff"; g.fillRect(px - 1, py, 3, 1); g.fillRect(px, py - 1, 1, 3);
        g.fillStyle = "#ffffff"; g.fillRect(px, py, 1, 1);
      }
    }
    g.globalAlpha = 1;
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
  // ---- os números de dano do herói (por cima dos efeitos; o líder e o herói são redesenhados depois, para nunca sumirem atrás deles)
  for (const n of E.numeros) {
    const k = n.t / NUMEROS.vida, sobe = 10 * (1 - (1 - Math.min(1, k * 1.6)) ** 2);
    g.globalAlpha = k > 0.72 ? Math.max(0, (1 - k) / 0.28) : 1;
    const cor = n.t < 0.05 && (n.tipo === "critico" || n.tipo === "forte") ? "#ffffff" : COR_NUMERO[n.tipo];
    numeroPixel(g, String(Math.round(n.valor)) + (n.tipo === "critico" ? "!" : ""), n.x + n.dx * 4 * k - cx, n.y - sobe - cy,
      cor, n.tipo === "critico" || n.tipo === "abertura" ? 2 : 1);
  }
  g.globalAlpha = 1;
  if (m.lider && !m.lider.morto && !liderCoberto) {
    const l = m.lider, [x, y] = pos(l), sp = Q.lider[1][poseTropa(l)];
    g.drawImage(l.virado > 0 ? sp.d : sp.e, Math.round(x - (l.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - (l.z || 0)) - cy);
  }
  if (!h.morto && !heroiCoberto) {
    const [x, y] = pos(h), sp = Q[h.nomeHeroi][0][poseHeroi(h)];
    g.drawImage(h.virado > 0 ? sp.d : sp.e, Math.round(x - (h.virado > 0 ? sp.ax : sp.w - sp.ax)) - cx, Math.round(y - sp.ay - Math.round(h.z || 0)) - cy);
  }
  for (const msg of E.mensagens) texto(g, msg.texto, msg.x - cx, msg.y - cy - msg.t * 10, "#ffe08a");

  // ---- quem importa e está fora da tela: setas na borda
  for (const u of m.lados[1]) {
    if (!u.def.elite) continue;
    const x = u.x - cx, y = u.y - cy;
    if (x >= 0 && y >= 0 && x < W && y < H) continue;
    seta(g, x, y, W, H, u.tipo === "lider" ? "#ff2a2a" : u.tipo === "campeao" ? "#ff5a48" : "#f0cb62");
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

// Campo Livre 7: os controles à vista. A provocação: uma linha tracejada de quem está provocado até quem provocou e um
// "!" em cima, com o tempo que falta numa barrinha; imobilizado: correntes em volta dos pés; lento: dois traços azuis
// atrás dos pés; Morel com o escudo erguido (o Desafio): um arco claro na frente dele.
function marcasDeControle(g, m, pos, Q, tipoDe, cx, cy, rel) {
  for (const u of m.unidades) {
    if (u.morto || !(u === m.heroi || u.def.elite)) continue;
    const [x, y] = pos(u), sx = Math.round(x) - cx, sy = Math.round(y) - cy;
    const sp = Q[tipoDe(u)][u.lado].parado, topo = Math.round(y - sp.ay) - cy;
    const p = u.provocacao;
    if (p && p.ate > m.t && p.por && !p.por.morto) {
      const [px, py] = pos(p.por), n = Math.max(1, Math.floor(Math.hypot(px - x, py - y) / 4)), cor = u === m.heroi ? "#ff6a4a" : "#bcd8ff";
      g.fillStyle = cor;
      for (let i = 1; i < n; i++) if ((i + Math.floor(rel * 8)) % 2) g.fillRect(Math.round(x + ((px - x) * i) / n) - cx, Math.round(y - 4 + ((py - y) * i) / n) - cy, 1, 1);
      g.fillStyle = "#15121a"; g.fillRect(sx - 2, topo - 15, 5, 8);
      g.fillStyle = cor; g.fillRect(sx, topo - 14, 1, 4); g.fillRect(sx, topo - 9, 1, 1);
      const k = Math.max(0, (p.ate - m.t) / (p.total || 1));
      g.fillStyle = "#15121a"; g.fillRect(sx - 5, topo - 6, 11, 2);
      g.fillStyle = cor; g.fillRect(sx - 4, topo - 6 + 0, Math.max(1, Math.round(9 * k)), 1);
    }
    if (u.imobAte > m.t) {
      g.fillStyle = Math.floor(rel * 6) % 2 ? "#e0d0ff" : "#9a6cff";
      for (let i = 0; i < 10; i++) { const a = (i / 10) * Math.PI * 2; if (i % 2) g.fillRect(Math.round(sx + Math.cos(a) * 6), Math.round(sy + Math.sin(a) * 3), 1, 1); }
    }
    if (u.lentoAte > m.t) { g.fillStyle = "#8fc8ff"; g.fillRect(sx - 6, sy - 1, 2, 1); g.fillRect(sx - 7, sy + 1, 2, 1); }
    if (u.posturaAte > m.t) {
      g.fillStyle = "#e9f2ff";
      const v = u.virado || 1;
      for (let j = -5; j <= 2; j++) g.fillRect(sx + v * (7 - Math.abs(j + 1) * 0.3 | 0), sy - 4 + j, 1, 1);
    }
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
