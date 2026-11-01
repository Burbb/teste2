// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 6: o cenário com construções, os tipos novos de tropa, Morel e
// Odette autônomos e os heróis inimigos. Sem DOM. sim.js chama este módulo pelos ganchos (`ligar` passa as funções de
// lá que estas regras usam) e continua dono do passo, do dano e das ordens.
//
// As regras do cenário, explícitas:
// - Casas, a muralha e as torres bloqueiam a passagem, as flechas, os projéteis e as áreas (uma explosão não atinge
//   quem está do outro lado de uma parede alta). Os muros baixos de pedra bloqueiam a passagem; flechas e magias passam
//   por cima deles.
// - O ponto de uma habilidade do herói (e do salto do Capitão) para na primeira parede alta entre quem lança e o
//   mouse; nenhum ponto cai dentro de uma construção.
// - Quem anda contorna as construções por um grafo dos cantos (calculado uma vez por mapa); com a linha livre, vai reto.
import { CENARIOS, TIPOS, CAMPO } from "./conteudo.js";

let S = null;    // as funções de sim.js (ferir, corpoACorpo, escolherAlvo, registrar...)
let M = null;    // o mundo do passo de agora (andarPara e pontoNoAlcance não recebem o mundo)
export function ligar(h) { S = h; }
export function mundoAtual(m) { M = m; }

const FOLGA = 6;              // quanto os retângulos crescem nas contas de caminho (o maior corpo comum tem raio 6,5)
const dist2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;

// ------------------------------------------------------------------------------------------------ geometria
// O segmento corta o retângulo crescido de `f`? Devolve o t de entrada (0 a 1) ou -1 (Liang-Barsky).
function corte(o, x1, y1, x2, y2, f) {
  const dx = x2 - x1, dy = y2 - y1;
  let t0 = 0, t1 = 1;
  const p = [-dx, dx, -dy, dy], q = [x1 - (o.x - f), o.x + o.w + f - x1, y1 - (o.y - f), o.y + o.h + f - y1];
  for (let i = 0; i < 4; i++) {
    if (Math.abs(p[i]) < 1e-9) { if (q[i] < 0) return -1; continue; }
    const r = q[i] / p[i];
    if (p[i] < 0) { if (r > t1) return -1; if (r > t0) t0 = r; } else { if (r < t0) return -1; if (r < t1) t1 = r; }
  }
  return t0;
}
const obsDe = (m) => (m && m.cenario ? m.cenario.obs : []);

/** A linha entre dois pontos passa por alguma construção? `tiro`: só as altas (as que barram flechas e áreas). */
export function bloqueado(m, x1, y1, x2, y2, tiro = false, f = 0) {
  for (const o of obsDe(m)) { if (tiro && !o.tiro) continue; if (corte(o, x1, y1, x2, y2, f) >= 0) return true; }
  return false;
}

/** O primeiro ponto em que a linha bate numa construção alta (um pouco antes dela), ou null. */
export function primeiroBloqueio(m, x1, y1, x2, y2) {
  let tm = Infinity;
  for (const o of obsDe(m)) { if (!o.tiro) continue; const t = corte(o, x1, y1, x2, y2, 0); if (t >= 0 && t < tm) tm = t; }
  if (tm === Infinity) return null;
  const n = Math.hypot(x2 - x1, y2 - y1) || 1, t = Math.max(0, tm - 4 / n);
  return { x: x1 + (x2 - x1) * t, y: y1 + (y2 - y1) * t };
}

export function dentroObstaculo(m, x, y, f = 0, tiro = false) {
  for (const o of obsDe(m)) {
    if (tiro && !o.tiro) continue;
    if (x > o.x - f && x < o.x + o.w + f && y > o.y - f && y < o.y + o.h + f) return o;
  }
  return null;
}

/** Tira um círculo de dentro das construções (o empurrão para fora pela borda mais perto). */
export function empurrarParaFora(m, u, r = u.raio) {
  for (const o of obsDe(m)) {
    const qx = Math.max(o.x, Math.min(u.x, o.x + o.w)), qy = Math.max(o.y, Math.min(u.y, o.y + o.h));
    let dx = u.x - qx, dy = u.y - qy;
    const d2 = dx * dx + dy * dy;
    if (d2 >= r * r) continue;
    if (d2 > 1e-6) {
      const d = Math.sqrt(d2);
      u.x = qx + (dx / d) * r; u.y = qy + (dy / d) * r;
    } else {
      // o centro dentro do retângulo: sai pela borda mais perto
      const e = [u.x - o.x, o.x + o.w - u.x, u.y - o.y, o.y + o.h - u.y], i = e.indexOf(Math.min(...e));
      if (i === 0) u.x = o.x - r; else if (i === 1) u.x = o.x + o.w + r; else if (i === 2) u.y = o.y - r; else u.y = o.y + o.h + r;
    }
    // quem bate na parede perde o empurrão naquela direção
    if (u.kx !== undefined) { u.kx *= 0.3; u.ky *= 0.3; }
  }
}

/** O ponto livre mais perto de (x, y), para um corpo de raio `r`. */
export function pontoLivre(m, x, y, r = 6) {
  const p = { x, y, kx: 0, ky: 0 };
  for (let i = 0; i < 4; i++) empurrarParaFora(m, p, r);
  const g = CAMPO.margem;
  return { x: Math.max(g, Math.min(CAMPO.largura - g, p.x)), y: Math.max(g, Math.min(CAMPO.altura - g, p.y)) };
}

/** O ponto de uma habilidade: para na primeira parede alta entre (ox, oy) e (x, y) e sai de dentro de construções. */
export function pontoDaHabilidade(ox, oy, x, y) {
  if (!M || !M.cenario) return { x, y };
  const b = primeiroBloqueio(M, ox, oy, x, y);
  return pontoLivre(M, b ? b.x : x, b ? b.y : y, 5);
}

// ------------------------------------------------------------------------------------------------ navegação
/** Prepara o cenário do mundo: as construções e o grafo dos cantos com todas as distâncias (Floyd-Warshall). */
export function prepararCenario(m, nome) {
  const c = CENARIOS[nome] || CENARIOS.aberto;
  const obs = c.obstaculos.map((o) => ({ ...o, tiro: o.tipo !== "muro" }));
  m.cenario = { nome, def: c, obs, nos: [], D: null, prox: null };
  const R = FOLGA + 3;
  for (const o of obs) {
    for (const [x, y] of [[o.x - R, o.y - R], [o.x + o.w + R, o.y - R], [o.x - R, o.y + o.h + R], [o.x + o.w + R, o.y + o.h + R]]) {
      if (x < 4 || y < 4 || x > CAMPO.largura - 4 || y > CAMPO.altura - 4) continue;
      if (dentroObstaculo(m, x, y, FOLGA)) continue;
      m.cenario.nos.push({ x, y });
    }
  }
  const nos = m.cenario.nos, n = nos.length, D = [], P = [];
  for (let i = 0; i < n; i++) {
    D.push(new Float64Array(n).fill(Infinity)); P.push(new Int32Array(n).fill(-1));
    D[i][i] = 0; P[i][i] = i;
  }
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    if (bloqueado(m, nos[i].x, nos[i].y, nos[j].x, nos[j].y, false, FOLGA - 1)) continue;
    D[i][j] = D[j][i] = Math.hypot(nos[i].x - nos[j].x, nos[i].y - nos[j].y);
    P[i][j] = j; P[j][i] = i;
  }
  for (let k = 0; k < n; k++) for (let i = 0; i < n; i++) {
    const dik = D[i][k];
    if (dik === Infinity) continue;
    for (let j = 0; j < n; j++) if (dik + D[k][j] < D[i][j]) { D[i][j] = dik + D[k][j]; P[i][j] = P[i][k]; }
  }
  m.cenario.D = D; m.cenario.prox = P;
}

/**
 * Para onde andar agora para chegar a (x, y): o próprio ponto, se a linha está livre; senão, o primeiro canto do
 * caminho mais curto pelo grafo. Guardado por unidade por até 0,5 s (ou até chegar ao canto).
 */
export function rumo(u, x, y) {
  const m = M;
  if (!m || !m.cenario || !m.cenario.obs.length) return { x, y };
  if (!bloqueado(m, u.x, u.y, x, y, false, Math.min(FOLGA - 1, u.raio))) { u.nav = null; return { x, y }; }
  const nv = u.nav, { nos, D, prox } = m.cenario;
  // o caminho guardado vale por 1,5 s enquanto o destino não muda muito; ao chegar a um canto, passa ao seguinte do
  // mesmo caminho (sem refazer a conta: no portão cheio, refazê-la a cada passo para centenas travava a simulação)
  if (nv && m.t - nv.t < 1.5 && Math.hypot(nv.tx - x, nv.ty - y) < 24) {
    if (Math.hypot(nv.x - u.x, nv.y - u.y) > 6) return nv;
    if (nv.i === nv.j) return { x, y };
    const i = prox[nv.i][nv.j];
    if (i >= 0) { nv.i = i; nv.x = nos[i].x; nv.y = nos[i].y; return nv; }
  }
  // um recálculo por unidade a cada 0,25 s no máximo, e no máximo 40 por passo no campo todo (uma onda que aparece
  // dentro do castelo pedia centenas no mesmo passo: picos de 20 a 38 ms); quem passa do limite usa o caminho que tinha
  // ou vai reto por um passo
  if (nv && m.t - (nv.calc ?? -9) < 0.25) return nv;
  if (m.navPasso !== m.t) { m.navPasso = m.t; m.navGasto = 0; }
  if (m.navGasto++ >= 40) return nv || { x, y };
  const f = Math.min(FOLGA - 1, u.raio);
  const vis = (px, py) => {
    const r = [];
    for (let i = 0; i < nos.length; i++) if (!bloqueado(m, px, py, nos[i].x, nos[i].y, false, f)) r.push(i);
    return r;
  };
  const a = vis(u.x, u.y), b = vis(x, y);
  let melhor = null, fim = null, custo = Infinity;
  for (const i of a) {
    const di = Math.hypot(nos[i].x - u.x, nos[i].y - u.y);
    for (const j of b) {
      const c = di + D[i][j] + Math.hypot(nos[j].x - x, nos[j].y - y);
      if (c < custo) { custo = c; melhor = i; fim = j; }
    }
  }
  // sem caminho conhecido (preso num canto): vai reto e deixa a colisão resolver
  if (melhor === null) { u.nav = { x, y, tx: x, ty: y, t: m.t, calc: m.t, i: -1, j: -1 }; return { x, y }; }
  u.nav = { x: nos[melhor].x, y: nos[melhor].y, tx: x, ty: y, t: m.t, calc: m.t, i: melhor, j: fim };
  return u.nav;
}

// ------------------------------------------------------------------------------------------------ magias e projéteis
// As áreas dos magos e de Ardis: o círculo aparece no chão por `dur` s e então explode (a regra das paredes vale: quem
// está atrás de uma parede alta, do centro da área, não é atingido).
function novaMagia(m, u, x, y, M2) {
  m.magias.push({ x, y, raio: M2.raio, t: 0, dur: M2.preparo, lado: u.lado, fonte: u, dano: M2.dano, danoHeroi: M2.danoHeroi ?? M2.dano,
    emp: M2.empurrao || 0, atord: M2.atordoa || 0, cor: M2.cor || "fogo", nome: M2.nome });
  m.eventos.push({ tipo: "aviso", id: u.id, forma: { tipo: "circulo", x, y, raio: M2.raio }, preparo: M2.preparo, lider: u.def.heroiInimigo });
}

export function atualizarMagias(m, dt) {
  if (!m.magias) return;
  const fica = [];
  for (const g of m.magias) {
    g.t += dt;
    if (g.t < g.dur) { fica.push(g); continue; }
    let n = 0;
    for (const v of m.lados[1 - g.lado]) {
      if (v.morto || (v.x - g.x) ** 2 + (v.y - g.y) ** 2 > (g.raio + v.raio * 0.5) ** 2) continue;
      if (bloqueado(m, g.x, g.y, v.x, v.y, true)) continue;
      const dx = v.x - g.x, dy = v.y - g.y, d = Math.hypot(dx, dy) || 1;
      S.ferir(m, v, v === m.heroi ? g.danoHeroi : g.dano, g.fonte, { dx: dx / d, dy: dy / d, emp: g.emp, atord: g.atord, forte: g.emp > 100, hab: g.nome });
      n++;
    }
    m.eventos.push({ tipo: "explosao", x: g.x, y: g.y, raio: g.raio, de: g.cor === "gelo" ? "estilhacar" : "ignicao" });
    m.stats.magias = (m.stats.magias || 0) + n;
  }
  m.magias = fica;
  // os dardos (Ardis) e a luz (Odette): andam em linha, param na parede alta, acertam o primeiro do outro lado
  const resto = [];
  for (const p of m.projE || []) {
    const s = p.vel * dt;
    p.x += p.dx * s; p.y += p.dy * s; p.resta -= s;
    if (dentroObstaculo(m, p.x, p.y, 0, true) || p.resta <= 0) { m.eventos.push({ tipo: "flechaChao", x: p.x, y: p.y, ang: Math.atan2(p.dy, p.dx) }); continue; }
    let acertou = null;
    for (const v of m.lados[1 - p.lado]) if (!v.morto && (v.x - p.x) ** 2 + (v.y - p.y) ** 2 <= (v.raio + 2.5) ** 2) { acertou = v; break; }
    if (acertou) { S.ferir(m, acertou, acertou === m.heroi ? p.danoHeroi : p.dano, p.fonte, { dx: p.dx, dy: p.dy, emp: 30 }); continue; }
    resto.push(p);
  }
  m.projE = resto;
}

function dardo(m, u, alvo, D) {
  const dx = alvo.x - u.x, dy = alvo.y - u.y, d = Math.hypot(dx, dy) || 1;
  (m.projE ||= []).push({ x: u.x, y: u.y - 4, dx: dx / d, dy: dy / d, vel: D.vel, resta: D.alcance + 20, lado: u.lado, dano: D.dano,
    danoHeroi: D.danoHeroi ?? D.dano, fonte: u, cor: D.cor });
  u.virado = dx >= 0 ? 1 : -1;
}

/** O ponto que pega mais inimigos de `u` num círculo de raio `r`, entre os que estão a até `alcance` (com visão). */
function melhorPonto(m, u, alcance, r, pesoHeroi = 3) {
  const cand = m.lados[1 - u.lado].filter((v) => !v.morto && dist2(u, v) <= alcance * alcance && !bloqueado(m, u.x, u.y, v.x, v.y, true));
  let melhor = null;
  for (let i = 0; i < cand.length && i < 40; i++) {
    const c = cand[(i * 7) % cand.length];
    let n = 0;
    for (const v of cand) if (dist2(c, v) <= r * r) n += v === m.heroi ? pesoHeroi : v.def.companheiro ? 2 : 1;
    if (!melhor || n > melhor.n) melhor = { x: c.x, y: c.y, n };
  }
  return melhor;
}

function maisPerto(m, u, lado, filtro = () => true) {
  let melhor = null, dm = Infinity;
  for (const v of m.lados[lado]) { if (v.morto || !filtro(v)) continue; const d = dist2(u, v); if (d < dm) { dm = d; melhor = v; } }
  return melhor ? { v: melhor, d: Math.sqrt(dm) } : null;
}

function andar(u, x, y, vel) { return S.andarPara(u, x, y, vel); }

// ------------------------------------------------------------------------------------------------ o gancho
/** Os tipos novos e os heróis: devolve true quando cuidou da unidade neste passo. */
export function atualizarEspecial(m, u, dt) {
  switch (u.tipo) {
    case "cavaleiro": return cavalaria(m, u, dt);
    case "magoBatalha": return magoDeBatalha(m, u, dt);
    case "morel": return morel(m, u, dt);
    case "odette": return odette(m, u, dt);
    case "ardis": return ardis(m, u, dt);
    default: return false;
  }
}

// ------------------------------------------------------------------------------------------------ a cavalaria
// Chega rápido, carrega em linha reta (atropela quem está na frente, uma vez cada), passa do ponto e precisa se
// reposicionar antes de carregar de novo. Parada, luta mal (dano 3). A infantaria pesada segura a carga: bater num
// pesado (massa 5 ou mais) encerra a carga e deixa o cavaleiro atordoado. Antes de carregar, empina por 0,35 s (o
// aviso: a nossa tropa e o herói veem a carga vindo).
function cavalaria(m, u, dt) {
  const d = u.def, C = d.carga;
  u.cargaCd = (u.cargaCd ?? m.rng() * 2) - dt;
  if (u.galope) {
    const g = u.galope;
    if (g.prepara > 0) { g.prepara -= dt; u.vx = u.vy = 0; return true; }
    g.t -= dt;
    u.vx = g.dx * C.vel; u.vy = g.dy * C.vel;
    u.virado = g.dx >= 0 ? 1 : -1;
    let parou = dentroObstaculo(m, u.x + g.dx * 8, u.y + g.dy * 8, u.raio);
    for (const v of m.lados[1 - u.lado]) {
      if (v.morto || g.hit.has(v.id) || dist2(u, v) > (u.raio + v.raio + 2) ** 2) continue;
      g.hit.add(v.id);
      const lado = g.dx * (v.y - u.y) - g.dy * (v.x - u.x) >= 0 ? 1 : -1;
      S.ferir(m, v, v === m.heroi ? C.danoHeroi : C.dano, u, { dx: -g.dy * lado * 0.7 + g.dx * 0.5, dy: g.dx * lado * 0.7 + g.dy * 0.5,
        emp: C.empurrao, atord: C.atordoa, forte: v.massa < 3, hab: "carga" });
      m.stats.cargas = (m.stats.cargas || 0) + 1;
      if ((v.massa || 2.5) >= 5 || v === m.heroi && m.heroi.acao && m.heroi.acao.fase === "escudo") {
        parou = true;
        u.atordoado = C.barrado;
        m.eventos.push({ tipo: "bloqueio", x: v.x, y: v.y, dx: -g.dx, dy: -g.dy });
      }
    }
    if (g.t <= 0 || parou) {
      u.galope = null;
      u.cargaCd = C.recarga;
      // reposicionar: sai para o próprio lado, um pouco para o flanco, antes da próxima carga
      const lado = u.lado === 0 ? -1 : 1, fl = (u.id % 2 ? 1 : -1) * 50;
      const p = pontoLivre(m, u.x + lado * C.recua, u.y + fl, u.raio);
      u.reposiciona = { x: p.x, y: p.y, t: C.reposiciona };
    }
    return true;
  }
  if (u.reposiciona) {
    const r = u.reposiciona;
    r.t -= dt;
    if (andar(u, r.x, r.y, d.vel * 1.2) < 6 || r.t <= 0) u.reposiciona = null;
    return true;
  }
  if (u.acao) return false;
  if (!u.alvo || u.alvo.morto || (u.reavaliarCav = (u.reavaliarCav || 0) - dt) <= 0) {
    u.alvo = S.escolherAlvo(m, u);
    u.reavaliarCav = 0.5;
  }
  const a = u.alvo;
  if (!a) return false;
  const dd = Math.sqrt(dist2(u, a));
  if (u.cargaCd <= 0 && dd >= C.min && dd <= C.max && !bloqueado(m, u.x, u.y, a.x, a.y, false, u.raio)) {
    // mira onde o alvo estará; passa `passa` px além dele
    const tx = a.x + (a.vx || 0) * 0.25, ty = a.y + (a.vy || 0) * 0.25, n = Math.hypot(tx - u.x, ty - u.y) || 1;
    u.galope = { dx: (tx - u.x) / n, dy: (ty - u.y) / n, t: (n + C.passa) / C.vel, prepara: C.prepara, hit: new Set() };
    m.eventos.push({ tipo: "contato", x: u.x, y: u.y });
    return true;
  }
  if (dd < C.min) return false;   // perto e sem carga pronta: luta parado, como a infantaria
  // longe ou esperando a carga: mantém a distância de carga, do próprio lado
  if (u.cargaCd > 0 && dd < C.max) {
    const lado = u.lado === 0 ? -1 : 1, p = pontoLivre(m, a.x + lado * (C.min + 30), a.y + ((u.id % 5) - 2) * 14, u.raio);
    andar(u, p.x, p.y, d.vel);
    return true;
  }
  andar(u, a.x, a.y, d.vel);
  return true;
}

// ------------------------------------------------------------------------------------------------ o mago de batalha
// Fica atrás da própria linha, a até `alcance` px do alvo e com visão; lança a Bola de Batalha no ponto que pega mais
// gente (o círculo aparece no chão 0,9 s antes). De `escudo.recarga` em `escudo.recarga` s, se três ou mais dos seus estão
// lutando a até `escudo.raio` px, põe neles um escudo que absorve `escudo.absorve`.
function magoDeBatalha(m, u, dt) {
  const d = u.def;
  u.escudoCd = (u.escudoCd ?? 3 + m.rng() * 3) - dt;
  if (u.lancando > 0) { u.lancando -= dt; u.vx = u.vy = 0; return true; }
  if (u.escudoCd <= 0) {
    const meus = m.lados[u.lado].filter((v) => !v.morto && v !== u && !v.def.elite && v.atacantes > 0 && dist2(u, v) <= d.escudo.raio ** 2);
    if (meus.length >= 3) {
      for (const v of meus.slice(0, 8)) { v.absorve = d.escudo.absorve; v.absorveAte = m.t + d.escudo.dura; }
      u.escudoCd = d.escudo.recarga;
      m.eventos.push({ tipo: "congela", x: u.x, y: u.y - 4 });
      return true;
    }
  }
  if (u.acao) return false;
  const perto = maisPerto(m, u, 1 - u.lado);
  if (!perto) return false;
  if (perto.d < d.perto) {
    const dx = u.x - perto.v.x, dy = u.y - perto.v.y, n = perto.d || 1;
    const p = pontoLivre(m, u.x + (dx / n) * 24, u.y + (dy / n) * 24, u.raio);
    andar(u, p.x, p.y, d.vel);
    return true;
  }
  if (!u.alvo || u.alvo.morto || (u.reav = (u.reav || 0) - dt) <= 0) { u.alvo = S.escolherAlvo(m, u); u.reav = 0.6; }
  const a = u.alvo;
  if (!a) return false;
  const dd = Math.sqrt(dist2(u, a)), visivel = !bloqueado(m, u.x, u.y, a.x, a.y, true);
  if (dd > d.alcance || !visivel) { andar(u, a.x, a.y, d.vel); return true; }
  u.vx = u.vy = 0;
  u.virado = a.x > u.x ? 1 : -1;
  if (u.recarga <= 0) {
    const p = melhorPonto(m, u, d.alcance, d.bola.raio) || { x: a.x, y: a.y };
    novaMagia(m, u, p.x, p.y, d.bola);
    u.recarga = d.recarga;
    u.lancando = 0.3;
  }
  return true;
}

// ------------------------------------------------------------------------------------------------ Morel
// O escudo da comitiva: enfrenta as ameaças (os heróis inimigos perto de você ou de Odette), protege quem está
// cercado, abre espaço com o Golpe de Escudo e provoca a tropa inimiga que cerca você ou Odette. Nunca persegue
// além da coleira (`coleira` px de você, ou do ponto da ordem); ferido (25%), recua para perto de Odette.
function ancoraCompanheiro(m, u) {
  const o = u.ordem || m.ordem, h = m.heroi;
  if (o && o.tipo === "defender") return { x: o.x, y: o.y };
  if (h.morto) return { x: u.x, y: u.y };
  return { x: h.x, y: h.y };
}

function morel(m, u, dt) {
  const d = u.def, h = m.heroi, od = m.odette;
  u.escudoCd = (u.escudoCd ?? 1) - dt;
  u.provocaCd = (u.provocaCd ?? 3) - dt;
  if (u.acao) return false;
  const anc = ancoraCompanheiro(m, u), longe = Math.hypot(u.x - anc.x, u.y - anc.y);
  const coleira = (u.ordem && u.ordem.tipo === "atacar") ? d.coleira * 1.6 : d.coleira;
  // ferido: recua para perto de Odette (ou de você)
  if (u.vida < u.vidaMax * 0.25 && od && !od.morto && dist2(u, od) > 30 * 30) { andar(u, od.x, od.y, d.vel); u.alvo = null; return true; }
  // longe demais: volta, sem parar para lutar
  if (longe > coleira) { andar(u, anc.x, anc.y, d.vel * 1.1); u.alvo = null; return true; }
  // o Golpe de Escudo: três ou mais inimigos colados na frente dele
  if (u.escudoCd <= 0) {
    const G = d.golpeEscudo, perto = m.lados[1].filter((v) => !v.morto && dist2(u, v) <= (G.raio + v.raio) ** 2);
    if (perto.length >= G.min || perto.some((v) => v.def.heroiInimigo)) {
      const c = perto.reduce((s, v) => ({ x: s.x + v.x / perto.length, y: s.y + v.y / perto.length }), { x: 0, y: 0 });
      const ang = Math.atan2(c.y - u.y, c.x - u.x);
      for (const v of perto) {
        const dx = v.x - u.x, dy = v.y - u.y, n = Math.hypot(dx, dy) || 1;
        if (Math.cos(Math.atan2(dy, dx) - ang) < Math.cos((G.abertura / 2) * Math.PI / 180)) continue;
        S.ferir(m, v, G.dano, u, { dx: dx / n, dy: dy / n, emp: G.empurrao, atord: G.atordoa, forte: true, hab: "golpeEscudo" });
      }
      u.escudoCd = G.recarga;
      u.virado = Math.cos(ang) >= 0 ? 1 : -1;
      m.eventos.push({ tipo: "golpeCampeao", x: u.x, y: u.y, forma: { tipo: "arco", x: u.x, y: u.y, raio: G.raio, ang, abertura: G.abertura }, heroi: false });
      m.stats.morelEscudo = (m.stats.morelEscudo || 0) + 1;
      return true;
    }
  }
  // a provocação: você ou Odette cercados (4 ou mais a 30 px)
  if (u.provocaCd <= 0) {
    const P = d.provocar;
    const cerca = (w) => w && !w.morto && m.lados[1].filter((v) => !v.morto && !v.def.elite && dist2(w, v) <= 30 * 30).length >= (w === h ? 4 : 2);
    if (cerca(h) || cerca(od)) {
      let n = 0;
      for (const v of m.lados[1]) {
        if (v.morto || v.def.elite || dist2(u, v) > P.raio * P.raio) continue;
        v.provocador = u; v.provocadoAte = m.t + P.dura; v.alvo = u; n++;
      }
      if (n) {
        u.provocaCd = P.recarga;
        m.eventos.push({ tipo: "abalo", x: u.x, y: u.y });
        S.registrar(m, `Morel provoca ${n} inimigos.`);
        m.stats.morelProvoca = (m.stats.morelProvoca || 0) + n;
        return true;
      }
    }
  }
  // o alvo: um herói inimigo perto de você ou de Odette; quem bate em Odette; quem está em você; o mais perto
  const ameaca = (w, r) => w && !w.morto && m.lados[1].find((v) => !v.morto && v.def.heroiInimigo && dist2(v, w) <= r * r);
  let alvo = ameaca(h, 160) || ameaca(od, 120);
  if (!alvo && od && !od.morto) alvo = m.lados[1].find((v) => !v.morto && dist2(v, od) <= 40 * 40);
  if (!alvo) alvo = m.lados[1].find((v) => !v.morto && !h.morto && dist2(v, h) <= 50 * 50);
  if (!alvo) { const p = maisPerto(m, u, 1); alvo = p && Math.hypot(p.v.x - anc.x, p.v.y - anc.y) <= coleira ? p.v : null; }
  if (!alvo) {
    // sem nada perto: fica entre você e os inimigos
    const e = m.centros[1], q = e ? { x: anc.x + (e.x - anc.x) * 0.12, y: anc.y + (e.y - anc.y) * 0.12 } : anc;
    andar(u, q.x + 10, q.y + 12, d.vel);
    return true;
  }
  u.alvo = alvo;
  S.corpoACorpo(m, u);
  return true;
}

// ------------------------------------------------------------------------------------------------ Odette
// Sustenta e responde ao perigo: cura quem perdeu vida de verdade (nunca a vida cheia; a Prece só com `prece.min` ou
// mais faltando), cura em área os soldados feridos juntos, cega e atordoa quem chega nela (Clarão) e, no resto do
// tempo, atira a luz. Fica atrás de você e de Morel, do lado oposto aos inimigos; não persegue.
function odette(m, u, dt) {
  const d = u.def, h = m.heroi, mo = m.morel;
  u.preceCd = (u.preceCd ?? 1) - dt; u.bencaoCd = (u.bencaoCd ?? 4) - dt; u.claraoCd = (u.claraoCd ?? 2) - dt;
  if (u.rezando > 0) { u.rezando -= dt; u.vx = u.vy = 0; return true; }
  // perigo: o Clarão quando dois ou mais estão colados nela
  const colados = m.lados[1].filter((v) => !v.morto && dist2(u, v) <= d.clarao.raio * d.clarao.raio);
  if (u.claraoCd <= 0 && colados.length >= d.clarao.min) {
    for (const v of colados) {
      const dx = v.x - u.x, dy = v.y - u.y, n = Math.hypot(dx, dy) || 1;
      S.ferir(m, v, d.clarao.dano, u, { dx: dx / n, dy: dy / n, emp: 90, atord: v.def.elite ? d.clarao.atordoa * 0.4 : d.clarao.atordoa, forte: true, hab: "clarao" });
    }
    u.claraoCd = d.clarao.recarga;
    m.eventos.push({ tipo: "explosao", x: u.x, y: u.y, raio: d.clarao.raio, de: "estilhacar" });
    m.stats.odetteClarao = (m.stats.odetteClarao || 0) + 1;
    return true;
  }
  // a Prece: o mais ferido entre você, Morel e ela (só quem perdeu `min` ou mais), ao alcance e com visão
  if (u.preceCd <= 0) {
    const cands = [h, mo, u].filter((w) => w && !w.morto && w.vidaMax - w.vida >= d.prece.min && dist2(u, w) <= d.prece.alcance ** 2 &&
      !bloqueado(m, u.x, u.y, w.x, w.y, true));
    cands.sort((a, b) => a.vida / a.vidaMax - b.vida / b.vidaMax);
    const w = cands[0];
    if (w) {
      const c = Math.min(d.prece.cura, w.vidaMax - w.vida);
      w.vida += c;
      if (w === h) m.eventos.push({ tipo: "cura", x: h.x, y: h.y, v: c });
      u.preceCd = d.prece.recarga; u.rezando = 0.35;
      m.eventos.push({ tipo: "congela", x: w.x, y: w.y - 6 });
      m.stats.odetteCura = (m.stats.odetteCura || 0) + c;
      S.registrar(m, `Odette cura ${w === h ? "você" : w.def.nome} (${Math.round(c)}).`);
      return true;
    }
  }
  // a Bênção: cinco ou mais dos nossos feridos juntos
  if (u.bencaoCd <= 0) {
    const B = d.bencao, feridos = m.lados[0].filter((w) => !w.morto && w !== h && w.vidaMax - w.vida >= B.minFalta && dist2(u, w) <= 140 * 140);
    let melhor = null;
    for (const c of feridos) {
      const n = feridos.filter((w) => dist2(c, w) <= B.raio * B.raio).length;
      if (n >= B.min && (!melhor || n > melhor.n)) melhor = { c, n };
    }
    if (melhor) {
      let total = 0;
      for (const w of feridos) if (dist2(melhor.c, w) <= B.raio * B.raio) { const c = Math.min(B.cura, w.vidaMax - w.vida); w.vida += c; total += c; }
      u.bencaoCd = B.recarga; u.rezando = 0.4;
      m.eventos.push({ tipo: "explosao", x: melhor.c.x, y: melhor.c.y, raio: B.raio, de: "estilhacar" });
      m.stats.odetteCura = (m.stats.odetteCura || 0) + total;
      return true;
    }
  }
  // a posição: atrás de você (ou de Morel), do lado oposto ao centro dos inimigos
  const anc = ancoraCompanheiro(m, u), e = m.centros[1];
  let px = anc.x - 30, py = anc.y;
  if (e) { const dx = anc.x - e.x, dy = anc.y - e.y, n = Math.hypot(dx, dy) || 1; px = anc.x + (dx / n) * d.atras; py = anc.y + (dy / n) * d.atras; }
  const perto = maisPerto(m, u, 1);
  if (perto && perto.d < 30) {
    const dx = u.x - perto.v.x, dy = u.y - perto.v.y, n = perto.d || 1;
    const p = pontoLivre(m, u.x + (dx / n) * 30, u.y + (dy / n) * 30, u.raio);
    andar(u, p.x, p.y, d.vel);
    return true;
  }
  const p = pontoLivre(m, px, py, u.raio);
  const ainda = Math.hypot(p.x - u.x, p.y - u.y) > 14 ? andar(u, p.x, p.y, d.vel) : (u.vx = u.vy = 0);
  void ainda;
  // a luz: o inimigo mais perto ao alcance, com visão
  u.luzCd = (u.luzCd ?? 0.5) - dt;
  if (u.luzCd <= 0 && perto && perto.d <= d.luz.alcance && !bloqueado(m, u.x, u.y, perto.v.x, perto.v.y, true)) {
    dardo(m, u, perto.v, d.luz);
    u.luzCd = d.luz.recarga;
  }
  return true;
}

// ------------------------------------------------------------------------------------------------ Ardis
// A feiticeira de guerra: o segundo arquétipo de herói inimigo. Fica de longe (100 a 150 px do herói no duelo),
// sempre em movimento; Dardo Arcano a cada 1,1 s; a Coluna de Fogo (anunciada 0,9 s) no grupo mais denso das nossas
// tropas, ou em você se você para; a Corrente Arcana (preparada 0,5 s: as mãos brilham) quando quatro ou mais dos nossos
// estão encadeados; o Passo Sombrio (some e reaparece a ~130 px, com visão de você) quando você ou Morel chegam a 60 px,
// depois de perceber (0,3 s); a Barreira (absorve 60 por 4 s) abaixo da metade da vida, com você perto. Atordoada,
// perde o que preparava. Duela com você quando você está a até 180 px ou acabou de feri-la; senão, vai nas tropas.
function ardis(m, u, dt) {
  const d = u.def, h = m.heroi;
  // sozinha (Harg caído e quase ninguém da tropa dela de pé), ela foge pelo portão: a batalha não fica presa nela
  const restam = m.lados[1].filter((v) => !v.morto && v !== u).length;
  if ((!m.lider || m.lider.morto) && restam <= Math.max(2, Math.round(m.stats.inimigos * 0.05))) {
    u.fugindo = true; u.acaoA = null;
    S.registrar(m, "Sozinha, Ardis foge.");
    m.eventos.push({ tipo: "fuga" });
    return true;
  }
  for (const k of ["dardoCd", "colunaCd", "passoCd", "correnteCd", "barreiraCd"]) u[k] = (u[k] ?? d.primeiras[k] ?? 0) - dt;
  if (u.acaoA) {
    const a = u.acaoA;
    a.t -= dt; u.vx = u.vy = 0;
    if (a.t > 0) return true;
    u.acaoA = null;
    if (a.tipo === "corrente") correnteArcana(m, u, a);
    return true;
  }
  const dh = h.morto ? Infinity : Math.sqrt(dist2(u, h));
  // o perigo: você ou Morel colados; ela percebe em 0,3 s e some
  const ameaca = dh <= 60 || (m.morel && !m.morel.morto && dist2(u, m.morel) <= 45 * 45);
  if (ameaca) u.perigoDesde ??= m.t; else u.perigoDesde = null;
  if (u.perigoDesde != null && m.t - u.perigoDesde >= d.reacao && u.passoCd <= 0) return passoSombrio(m, u);
  if (u.barreiraCd <= 0 && u.vida < u.vidaMax * 0.5 && dh <= 160) {
    u.absorve = d.barreira.absorve; u.absorveAte = m.t + d.barreira.dura; u.barreiraCd = d.barreira.recarga;
    m.eventos.push({ tipo: "congela", x: u.x, y: u.y - 6 });
    S.registrar(m, "Ardis ergue uma barreira.");
    return true;
  }
  // a escolha: duelo (perto ou ferida há pouco) ou tropas; revista a cada 2 s
  u.modoT = (u.modoT ?? 0) - dt;
  if (u.modoT <= 0) {
    const ferida = m.t - (u.feridaPeloHeroi ?? -9) < 3;
    const g = grupoDenso(m, u, 240);
    const modo = !h.morto && (dh <= 180 || ferida || !g) ? "heroi" : "tropas";
    if (modo !== u.modo) { u.modo = modo; S.registrar(m, modo === "heroi" ? "Ardis vem duelar com você." : "Ardis mira as suas tropas."); }
    u.grupoAlvo = g; u.modoT = 2;
  }
  // a Corrente Arcana: quatro ou mais dos nossos encadeados a até 160 px
  if (u.correnteCd <= 0) {
    const cadeia = cadeiaDe(m, u, 160, d.corrente.salto, d.corrente.alvos);
    if (cadeia.length >= 4) { u.acaoA = { tipo: "corrente", t: d.corrente.preparo, cadeia }; u.correnteCd = d.corrente.recarga; m.eventos.push({ tipo: "aviso", id: u.id, forma: { tipo: "circulo", x: u.x, y: u.y, raio: 8 }, preparo: d.corrente.preparo, lider: true }); return true; }
  }
  // a Coluna de Fogo: no grupo (ou em você, parado ou no duelo)
  if (u.colunaCd <= 0) {
    let p = null;
    if (u.modo === "tropas" && u.grupoAlvo) p = u.grupoAlvo;
    else if (!h.morto && dh <= d.coluna.alcance && !bloqueado(m, u.x, u.y, h.x, h.y, true)) p = { x: h.x + (h.vx || 0) * 0.4, y: h.y + (h.vy || 0) * 0.4 };
    if (p) {
      const q = pontoDaHabilidade(u.x, u.y, p.x, p.y);
      novaMagia(m, u, q.x, q.y, d.coluna);
      u.colunaCd = d.coluna.recarga;
      u.acaoA = { tipo: "gesto", t: 0.25 };
      S.registrar(m, `Ardis chama a Coluna de Fogo ${u.modo === "tropas" ? "nas suas tropas" : "em você"}.`);
      return true;
    }
  }
  // o Dardo Arcano: no herói (duelo) ou na tropa mais perto, com visão
  const alvo = u.modo === "heroi" && !h.morto ? h : (maisPerto(m, u, 0, (v) => v !== h) || {}).v || (h.morto ? null : h);
  if (alvo && u.dardoCd <= 0 && dist2(u, alvo) <= d.dardo.alcance ** 2 && !bloqueado(m, u.x, u.y, alvo.x, alvo.y, true)) {
    dardo(m, u, alvo, d.dardo);
    u.dardoCd = d.dardo.recarga;
  }
  // o movimento: no duelo, a 100-150 px de você, de lado (nunca parada); nas tropas, a ~150 px do grupo
  const ref = u.modo === "tropas" && u.grupoAlvo ? u.grupoAlvo : alvo;
  if (!ref) { u.vx = u.vy = 0; return true; }
  const rx = u.x - ref.x, ry = u.y - ref.y, rd = Math.hypot(rx, ry) || 1;
  const ideal = u.modo === "heroi" ? 125 : 150, lado = (Math.floor(m.t / 3) + u.id) % 2 ? 1 : -1;
  let tx = ref.x + (rx / rd) * ideal - (ry / rd) * 40 * lado, ty = ref.y + (ry / rd) * ideal + (rx / rd) * 40 * lado;
  // sem visão do alvo, chega mais perto pelo caminho
  if (bloqueado(m, u.x, u.y, ref.x, ref.y, true)) { tx = ref.x; ty = ref.y; }
  const p = pontoLivre(m, tx, ty, u.raio);
  andar(u, p.x, p.y, d.vel);
  return true;
}

function passoSombrio(m, u) {
  const h = m.heroi, d = u.def, ameaca = h.morto ? m.morel : h;
  let melhor = null;
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2, x = ameaca.x + Math.cos(a) * d.passo.distancia, y = ameaca.y + Math.sin(a) * d.passo.distancia;
    if (x < 20 || y < 20 || x > CAMPO.largura - 20 || y > CAMPO.altura - 20 || dentroObstaculo(m, x, y, u.raio)) continue;
    // prefere longe dos nossos e perto dos dela, com visão de quem a ameaçava
    let v = bloqueado(m, x, y, ameaca.x, ameaca.y, true) ? -50 : 0;
    for (const o of m.lados[0]) if (!o.morto && (o.x - x) ** 2 + (o.y - y) ** 2 < 60 * 60) v -= 5;
    for (const o of m.lados[1]) if (!o.morto && (o.x - x) ** 2 + (o.y - y) ** 2 < 80 * 80) v += 1;
    if (!melhor || v > melhor.v) melhor = { x, y, v };
  }
  if (!melhor) return false;
  m.eventos.push({ tipo: "explosao", x: u.x, y: u.y, raio: 14, de: "estilhacar" });
  u.x = u.px = melhor.x; u.y = u.py = melhor.y;
  u.passoCd = d.passo.recarga; u.perigoDesde = null;
  u.acaoA = { tipo: "gesto", t: 0.2 };
  m.eventos.push({ tipo: "explosao", x: u.x, y: u.y, raio: 14, de: "estilhacar" });
  S.registrar(m, "Ardis some e reaparece longe.");
  m.stats.ardisPassos = (m.stats.ardisPassos || 0) + 1;
  return true;
}

function grupoDenso(m, u, alcance) {
  let melhor = null;
  for (const a of m.lados[0]) {
    if (a === m.heroi || a.morto || dist2(a, u) > alcance * alcance) continue;
    let n = 0, sx = 0, sy = 0;
    for (const b of m.lados[0]) if (!b.morto && b !== m.heroi && dist2(a, b) <= 36 * 36) { n++; sx += b.x; sy += b.y; }
    if (n >= 5 && (!melhor || n > melhor.n)) melhor = { x: sx / n, y: sy / n, n };
  }
  return melhor;
}

function cadeiaDe(m, u, alcance, salto, max) {
  const primeiro = maisPerto(m, u, 0, (v) => !bloqueado(m, u.x, u.y, v.x, v.y, true));
  if (!primeiro || primeiro.d > alcance) return [];
  const cadeia = [primeiro.v], usados = new Set([primeiro.v.id]);
  while (cadeia.length < max) {
    const ult = cadeia[cadeia.length - 1];
    let prox = null, dm = salto * salto;
    for (const v of m.lados[0]) if (!v.morto && !usados.has(v.id) && dist2(ult, v) <= dm) { dm = dist2(ult, v); prox = v; }
    if (!prox) break;
    cadeia.push(prox); usados.add(prox.id);
  }
  return cadeia;
}

function correnteArcana(m, u, a) {
  const C = u.def.corrente;
  let de = u;
  for (const v of a.cadeia) {
    if (v.morto) continue;
    (m.linhas ||= []).push({ x1: de.x, y1: de.y - 4, x2: v.x, y2: v.y - 4, ate: m.t + 0.3 });
    S.ferir(m, v, v === m.heroi ? C.danoHeroi : C.dano, u, { dx: 0, dy: 0, emp: 40, atord: 0.25, hab: "corrente" });
    de = v;
  }
  S.registrar(m, `A Corrente Arcana salta por ${a.cadeia.length}.`);
}

// ------------------------------------------------------------------------------------------------ Harg, evoluído
// O que o Capitão ganhou (Campo Livre 6): a Investida Curta (sem a Arremetida e sem a Carga prontas, com você a 120-220
// px, avança ~85 px em 0,28 s, a cada 7 s: não fica esperando recarga), o golpe em sequência (ao cair da Arremetida com três ou mais
// dos nossos em volta, o Rodopio sai na hora), a Fúria (abaixo de 35% de vida, uma vez: ataca 40% mais rápido por 8 s)
// e, com Ardis, a proteção (você a menos de 90 px dela: ele vem atrás de você, mesmo no meio das tropas).
export function ajustarLider(m, u, dh, dt) {
  const d = u.def, h = m.heroi;
  u.dashCd = (u.dashCd ?? 2) - dt;
  if (u.dash) {
    u.dash.t -= dt;
    u.vx = u.dash.dx * d.dash.vel; u.vy = u.dash.dy * d.dash.vel;
    if (u.dash.t <= 0) { u.dash = null; u.reavaliar = 0; }
    return true;
  }
  if (!u.furiaFeita && u.vida < u.vidaMax * d.furia.vida) {
    u.furiaFeita = true; u.furiaAte = m.t + d.furia.dura;
    m.eventos.push({ tipo: "abalo", x: u.x, y: u.y });
    S.registrar(m, `${d.nome} entra em fúria.`);
  }
  if (d.combo && u.cravado > 0 && !u.comboFeito) {
    u.comboFeito = true;
    let n = 0;
    for (const o of m.lados[0]) if (!o.morto && dist2(o, u) <= (d.rodopio.raio - 6) ** 2) n += o === h ? 2 : 1;
    if (n >= d.rodopio.min) { u.rodopioCd = 0; u.habIntervalo = 0; }
  }
  if (u.acao && u.acao.tipo === "arremetida") u.comboFeito = false;
  const ar = m.ardis;
  if (ar && !ar.morto && !h.morto && dist2(h, ar) <= 90 * 90 && u.modo !== "heroi") {
    u.modo = "heroi"; u.modoT = d.foco.minimo; u.alvo = null; u.reavaliar = 0;
    S.registrar(m, `${d.nome} vem proteger Ardis.`);
  }
  if (u.modo === "heroi" && !h.morto && !u.acao && u.dashCd <= 0 && dh >= d.dash.min && dh <= d.dash.max && u.arremCd > 0 && u.cargaCd > 0) {
    const n = dh || 1;
    u.dash = { dx: (h.x - u.x) / n, dy: (h.y - u.y) / n, t: d.dash.dura };
    u.dashCd = d.dash.recarga;
    u.virado = h.x >= u.x ? 1 : -1;
    m.eventos.push({ tipo: "contato", x: u.x, y: u.y });
    return true;
  }
  return false;
}

// ------------------------------------------------------------------------------------------------ companheiros e composições
/** Cria Morel e Odette perto do herói (encontros com `companheiros`). */
export function criarCompanheiros(m, x, y) {
  const mo = S.novaUnidade(m, 0, "morel", x + 22, y + 14), od = S.novaUnidade(m, 0, "odette", x - 26, y - 10);
  m.morel = mo; m.odette = od;
  // cada um numa casa livre: nenhum começa em cima de um soldado (nas escalas maiores, as alas ocupam mais lugar)
  for (const c of [mo, od]) {
    for (let i = 0; i < 30 && m.unidades.some((v) => v !== c && (v.x - c.x) ** 2 + (v.y - c.y) ** 2 < (c.raio + v.raio + 1) ** 2); i++) {
      c.y += i % 2 ? -(i + 1) * 4 : (i + 1) * 4;
    }
    c.px = c.x; c.py = c.y;
    c.ordem = { tipo: "acompanhar", x, y };   // como as tropas: acompanham você até receberem outra ordem
  }
  return [mo, od];
}

/** Os blocos de uma composição, em volta de (x, y): `sentido` -1 para os aliados (o fundo é o oeste), 1 para os inimigos. */
export function blocosDaComposicao(lista, x, y, sentido) {
  return lista.map(([tipo, n, prof, dy, cols]) => [tipo, n, x + sentido * prof, y + dy, cols]);
}

export { TIPOS };
