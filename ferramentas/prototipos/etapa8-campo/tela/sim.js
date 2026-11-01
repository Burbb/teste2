// PROTÓTIPO de campo livre da etapa 8 (nada no jogo): a simulação em tempo real. Sem DOM: roda no navegador (main.js)
// e no Node (testes/sim.test.mjs). Passo fixo de 1/60 s; o sorteio vem de uma semente, então a mesma entrada dá a
// mesma batalha. A tela só lê o mundo e os eventos (m.eventos) que cada passo deixa; não decide regra nenhuma.
//
// O que está aqui: o herói (movimento com aceleração, a mira, as ações com preparo, contato e recuperação, o
// adiantamento de comando), as tropas (alvo com vagas, aproximação, ataque, arqueiros que mantêm distância, ordens
// coletivas), os projéteis, o fogo no chão, os empurrões e a separação dos corpos numa grade espacial.
import { CAMPO, ATRITO_EMPURRAO, SEMENTE, TIPOS, HEROIS, ORDENS, CONTINGENTES, BATALHA, VARIANTES, ENCONTROS } from "./conteudo.js";

export const PASSO = 1 / 60;
const GRAU = Math.PI / 180;
const CELULA = 12;          // a célula da grade de vizinhança (≥ o maior par de raios: campeão 6 + herói 5)
const ADIANTAR = 0.2;       // um comando apertado durante outra ação espera até 0,2 s para sair
const ACELERA = 1000;       // px/s²: o herói chega à velocidade máxima em ~0,07 s
const FREIA = 1400;         // e para em ~0,05 s

export function sorteio(semente) {
  let a = semente >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function entradaVazia() {
  return { mx: 0, my: 0, cima: false, baixo: false, esq: false, dir: false, atacar: false, apertos: [] };
}

// ------------------------------------------------------------------------------------------------ o mundo
export function criarMundo({ heroi = "guerreiro", quantidade = "normal", semente = SEMENTE, encontro = "original",
  kit = {} } = {}) {
  const enc = ENCONTROS[encontro] || ENCONTROS.original;
  if (!enc.original) return criarEncontro(enc, encontro, heroi, quantidade, semente, kit);
  const m = {
    t: 0, rng: sorteio(semente), campo: CAMPO, proximoId: 1, unidades: [], lados: [[], []], centros: [null, null],
    proj: [], zonas: [], eventos: [], registro: [], fase: "formacao", resultado: null, fimEm: 0,
    ordem: { tipo: "acompanhar", x: 0, y: 0 }, quantidade, nomeHeroi: heroi,
    stats: novasEstatisticas(), grupos: {}, selecao: new Set(), lider: null, encontro: "original",
  };
  const c = CONTINGENTES[quantidade] || CONTINGENTES.normal;
  const cy = CAMPO.altura / 2;
  // os aliados à esquerda, virados para a direita; os inimigos à direita
  bloco(m, 0, "soldado", c.aliados.soldado, 262, cy, quantidade === "maior" ? 6 : 4, -1);
  bloco(m, 0, "arqueiro", c.aliados.arqueiro, quantidade === "maior" ? 180 : 200, cy, quantidade === "maior" ? 3 : 2, -1);
  const grande = quantidade === "maior";
  bloco(m, 1, "veterano", c.inimigos.veterano, 646, cy, grande ? 3 : 2, 1);
  bloco(m, 1, "soldado", c.inimigos.soldado, grande ? 684 : 674, cy, grande ? 5 : 4, 1);
  bloco(m, 1, "arqueiro", c.inimigos.arqueiro, grande ? 760 : 738, cy, grande ? 3 : 2, 1);
  for (let i = 0; i < c.inimigos.estandarte; i++) novaUnidade(m, 1, "estandarte", grande ? 800 : 772, cy + (i - (c.inimigos.estandarte - 1) / 2) * 110);
  m.reforco = { comp: c.reforco, chegou: false };
  prepararHeroi(m, heroi, 300, cy, kit);
  limpar(m);
  m.stats.inimigos = m.lados[1].length + Object.values(c.reforco).reduce((x, y) => x + y, 0);
  m.stats.primeira = m.lados[1].length;
  m.stats.aliados = m.lados[0].length - 1;
  return m;
}

function novasEstatisticas() {
  return { abatesHeroi: 0, abatesAliados: 0, perdas: 0, danoSofrido: 0, usos: {}, maiorGolpe: 0, fugiram: 0, inimigos: 0,
    aliados: 0, danoTropas: 0, ocupados: 0, flechasTropas: 0, flechasHeroi: 0 };
}

/** O kit com as versões escolhidas (as que não existem caem na original). */
export function montarKit(heroi, escolha = {}) {
  const kit = { ...HEROIS[heroi].kit };
  for (const [slot, v] of Object.entries(escolha)) {
    const def = VARIANTES[heroi] && VARIANTES[heroi][slot] && VARIANTES[heroi][slot][v];
    if (def) kit[slot] = { ...def, variante: v };
  }
  return kit;
}

function prepararHeroi(m, heroi, x, y, escolha) {
  const h = novaUnidade(m, 0, "heroi", x, y);
  m.heroi = h;
  const d = HEROIS[heroi];
  Object.assign(h, { nomeHeroi: heroi, kit: montarKit(heroi, escolha), cds: {}, recurso: d.recurso.inicial,
    recursoMax: d.recurso.max, mira: 0, acao: null, buffer: null, invul: 0, combo: 0, comboT: 0, z: 0, contato: 0 });
  for (const id in h.kit) h.cds[id] = 0;
  m.ordem = { tipo: "acompanhar", x: h.x, y: h.y };
  for (const u of m.unidades) if (u.lado === 0 && u !== h) u.ordem = { tipo: "acompanhar", x: h.x, y: h.y };
}

// Os encontros novos: blocos fixos (tipo, quantos, onde, colunas, grupo), grupos que acordam no tempo deles e levas.
function criarEncontro(enc, nome, heroi, quantidade, semente, kit) {
  const grande = quantidade === "maior";
  const m = {
    t: 0, rng: sorteio(semente), campo: CAMPO, proximoId: 1, unidades: [], lados: [[], []], centros: [null, null],
    proj: [], zonas: [], eventos: [], registro: [], fase: "formacao", resultado: null, fimEm: 0,
    ordem: { tipo: "acompanhar", x: 0, y: 0 }, quantidade, nomeHeroi: heroi, stats: novasEstatisticas(),
    grupos: {}, selecao: new Set(), lider: null, encontro: nome, levas: [],
  };
  const qtd = (b) => (grande && !["lider", "campeao", "estandarte"].includes(b[0]) ? b[1] * 2 : b[1]);
  for (const b of enc.aliados) bloco(m, 0, b[0], qtd(b), b[2], b[3], (b[4] || 3) * (grande ? 2 : 1), -1);
  for (const [g, def] of Object.entries(enc.grupos)) m.grupos[g] = { ativo: false, ativa: def.ativa ?? 0, posto: !!def.posto };
  const porLeva = { 0: [] };
  for (const b of enc.inimigos) {
    const leva = b[6] || 0;
    if (leva) { (porLeva[leva] ||= []).push(b); continue; }
    criarBlocoInimigo(m, b, qtd(b), grande);
  }
  for (const lv of enc.levas || []) m.levas.push({ ...lv, chegou: false, blocos: porLeva[lv.id] || [] });
  m.reforco = { chegou: m.levas.length === 0, comp: {} };
  prepararHeroi(m, heroi, enc.heroi[0], enc.heroi[1], kit);
  limpar(m);
  m.stats.primeira = m.lados[1].length;
  m.stats.inimigos = m.lados[1].length + m.levas.reduce((n, lv) => n + lv.blocos.reduce((k, b) => k + qtd(b), 0), 0);
  m.stats.aliados = m.lados[0].length - 1;
  return m;
}

function criarBlocoInimigo(m, b, n, grande) {
  const antes = m.unidades.length;
  bloco(m, 1, b[0], n, b[2], b[3], (b[4] || 3) * (grande && n > 2 ? 2 : 1), 1);
  const g = m.grupos[b[5]];
  for (const u of m.unidades.slice(antes)) {
    u.grupo = b[5];
    if (g && g.posto) u.posto = { x: u.x, y: u.y };
    if (u.tipo === "lider") m.lider = u;
  }
}

function chegarLevas(m) {
  for (const lv of m.levas) {
    if (lv.chegou) continue;
    if (m.t < lv.t && m.lados[1].length > m.stats.primeira * (lv.quando ?? 0)) continue;
    lv.chegou = true;
    const antes = m.unidades.length, grande = m.quantidade === "maior";
    for (const b of lv.blocos) {
      const n = grande && !["lider", "campeao", "estandarte"].includes(b[0]) ? b[1] * 2 : b[1];
      criarBlocoInimigo(m, b, n, grande);
    }
    for (const u of m.unidades.slice(antes)) {
      u.x = Math.max(CAMPO.margem, Math.min(CAMPO.largura - CAMPO.margem, u.x));
      u.y = Math.max(CAMPO.margem, Math.min(CAMPO.altura - CAMPO.margem, u.y));
      u.px = u.x; u.py = u.y;
      if (u.grupo) m.grupos[u.grupo].ativo = true;
    }
    m.eventos.push({ tipo: "reforco", x: lv.x ?? CAMPO.largura - 14, y: lv.y ?? CAMPO.altura / 2, texto: lv.aviso });
    registrar(m, lv.aviso);
  }
  m.reforco.chegou = m.levas.every((lv) => lv.chegou);
}

function bloco(m, lado, tipo, n, x0, cy, colunas, sentido) {
  const esp = 12, linhas = Math.ceil(n / colunas);
  for (let i = 0; i < n; i++) {
    const col = i % colunas, lin = Math.floor(i / colunas);
    const x = x0 + col * esp * sentido + (m.rng() - 0.5) * 3;
    const y = cy + (lin - (linhas - 1) / 2) * esp + (m.rng() - 0.5) * 3;
    novaUnidade(m, lado, tipo, x, y);
  }
}

// a segunda leva entra pela borda direita, em coluna, já marchando
function chegarReforco(m) {
  const c = m.reforco.comp, cy = CAMPO.altura / 2, x = CAMPO.largura - 14, grande = m.quantidade === "maior";
  const antes = m.unidades.length;
  bloco(m, 1, "veterano", c.veterano, x - 12, cy, grande ? 2 : 1, 1);
  bloco(m, 1, "soldado", c.soldado, x, cy, grande ? 4 : 2, 1);
  bloco(m, 1, "arqueiro", c.arqueiro, x + 6, cy - 70, grande ? 2 : 1, 1);
  for (let i = 0; i < c.campeao; i++) novaUnidade(m, 1, "campeao", x - 26, cy + (i - (c.campeao - 1) / 2) * 120);
  for (const u of m.unidades.slice(antes)) {
    u.x = Math.min(u.x, CAMPO.largura - CAMPO.margem);
    u.px = u.x;
  }
  m.reforco.chegou = true;
  m.eventos.push({ tipo: "reforco", x, y: cy });
  registrar(m, `A segunda leva chega pela direita (${m.unidades.length - antes}, com ${c.campeao === 1 ? "o campeão" : "os campeões"}).`);
}

function novaUnidade(m, lado, tipo, x, y) {
  const d = tipo === "heroi" ? HEROIS[m.nomeHeroi] : TIPOS[tipo];
  const u = {
    id: m.proximoId++, lado, tipo, def: d, x, y, px: x, py: y, vx: 0, vy: 0, kx: 0, ky: 0, raio: d.raio,
    massa: d.massa, vida: lado === 0 && d.vidaAliado || d.vida, vidaMax: lado === 0 && d.vidaAliado || d.vida, alvo: null, reavaliar: m.rng() * 0.3, acao: null,
    recarga: m.rng() * 0.6, atordoado: 0, congelado: 0, flash: 0, virado: lado === 0 ? 1 : -1, passo: m.rng() * 10,
    abalado: 0, mostra: 0, fugindo: false, saiu: false, morto: false, atacantes: 0, aura: false, slot: 0,
  };
  m.unidades.push(u);
  return u;
}

function registrar(m, texto) {
  m.registro.push({ t: m.t, texto });
  if (m.registro.length > 200) m.registro.shift();
}

// ------------------------------------------------------------------------------------------------ o passo
export function passo(m, ent) {
  const dt = PASSO;
  if (m.fase === "fim") return;
  m.t += dt;
  if (m.fase === "formacao" && m.t >= BATALHA.formacao) {
    m.fase = "luta";
    m.eventos.push({ tipo: "avanco" });
  }
  if (m.levas) { if (!m.reforco.chegou) chegarLevas(m); }
  else if (!m.reforco.chegou && m.fase === "luta" &&
      (m.t >= BATALHA.reforcoT || m.lados[1].length <= m.stats.primeira * BATALHA.reforcoQuando)) chegarReforco(m);
  contarAtacantes(m);
  marcarAuras(m);
  atualizarHeroi(m, m.heroi, ent || entradaVazia(), dt);
  for (const u of m.unidades) if (u !== m.heroi && !u.morto) atualizarUnidade(m, u, dt);
  atualizarProjeteis(m, dt);
  atualizarZonas(m, dt);
  mover(m, dt);
  separar(m);
  limpar(m);
  verificarFim(m);
}

function contarAtacantes(m) {
  for (const u of m.unidades) u.atacantes = 0;
  for (const u of m.unidades) {
    if (!u.alvo || u.alvo.morto) continue;
    u.alvo.atacantes++;
    // a contribuição das tropas além das mortes: inimigos ocupados com elas (inimigo × segundo)
    if (u.lado === 1 && u.alvo !== m.heroi) m.stats.ocupados += PASSO;
  }
}

function marcarAuras(m) {
  for (const u of m.lados[1]) { u.aura = false; u.firme = false; }
  const l = m.lider;
  if (l && !l.morto) {
    const r2 = l.def.presenca * l.def.presenca;
    for (const u of m.lados[1]) if (u !== l && !u.def.elite && dist2(u, l) <= r2) u.firme = true;
  }
  for (const e of m.lados[1]) {
    if (e.tipo !== "estandarte" || e.morto) continue;
    const r2 = e.def.aura * e.def.aura;
    for (const u of m.lados[1]) if (u !== e && dist2(u, e) <= r2) u.aura = true;
  }
}

// ------------------------------------------------------------------------------------------------ geometria
const dist2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;
function difAngulo(a, b) {
  let d = (a - b) % (2 * Math.PI);
  if (d > Math.PI) d -= 2 * Math.PI;
  if (d < -Math.PI) d += 2 * Math.PI;
  return Math.abs(d);
}
function distSegmento(px, py, x1, y1, x2, y2) {
  const vx = x2 - x1, vy = y2 - y1, l2 = vx * vx + vy * vy;
  const k = l2 ? Math.max(0, Math.min(1, ((px - x1) * vx + (py - y1) * vy) / l2)) : 0;
  const qx = x1 + vx * k, qy = y1 + vy * k;
  return { d: Math.hypot(px - qx, py - qy), qx, qy };
}

/** O que a área de uma ação cobre. A mesma forma desenha a prévia e o efeito e decide quem é atingido. */
export function dentro(f, x, y) {
  if (f.tipo === "circulo") return (x - f.x) ** 2 + (y - f.y) ** 2 <= f.raio * f.raio;
  if (f.tipo === "arco") {
    const dx = x - f.x, dy = y - f.y, d = Math.hypot(dx, dy);
    if (d > f.raio) return false;
    if (d < 4) return true;      // quem está colado ao herói é atingido de qualquer lado
    return difAngulo(Math.atan2(dy, dx), f.ang) <= (f.abertura * GRAU) / 2;
  }
  if (f.tipo === "faixa") return distSegmento(x, y, f.x1, f.y1, f.x2, f.y2).d <= f.largura;
  return false;
}

export function pontoNoAlcance(h, mx, my, alcance) {
  const dx = mx - h.x, dy = my - h.y, d = Math.hypot(dx, dy);
  let x = mx, y = my;
  if (d > alcance) { x = h.x + (dx / d) * alcance; y = h.y + (dy / d) * alcance; }
  return limitarAoCampo(x, y);
}
function limitarAoCampo(x, y) {
  const g = CAMPO.margem;
  return { x: Math.max(g, Math.min(CAMPO.largura - g, x)), y: Math.max(g, Math.min(CAMPO.altura - g, y)) };
}

/** A área que a ação `id` cobriria agora, com o mouse em (mx, my): a prévia na tela e o contato usam esta forma. */
export function formaDaAcao(h, id, mx, my) {
  const k = h.kit[id], ang = Math.atan2(my - h.y, mx - h.x);
  if (id === "basico" && k.arremate) {
    const fim = h.comboT > 0 && h.combo + 1 >= k.arremate.cada;
    const r = fim ? k.arremate : k;
    return { tipo: "arco", x: h.x, y: h.y, raio: r.raio, ang, abertura: r.abertura || k.abertura, arremate: fim };
  }
  if (id === "basico") return { tipo: "linha", x: h.x, y: h.y, ang, alcance: k.alcance };
  if (id === "varredura") return { tipo: "arco", x: h.x, y: h.y, raio: k.raio, ang, abertura: k.abertura };
  if (id === "investida" && k.inspira) return { tipo: "circulo", x: h.x, y: h.y, raio: k.raio };
  if (id === "muralha" && k.variante === "anel") {
    const p = pontoNoAlcance(h, mx, my, k.alcance);
    return { tipo: "circulo", x: p.x, y: p.y, raio: k.raio, anel: true };
  }
  if (id === "investida") {
    const p = limitarAoCampo(h.x + Math.cos(ang) * k.distancia, h.y + Math.sin(ang) * k.distancia);
    return { tipo: "faixa", x1: h.x, y1: h.y, x2: p.x, y2: p.y, largura: k.largura };
  }
  if (id === "salto" || id === "bola") {
    const p = pontoNoAlcance(h, mx, my, k.alcance);
    return { tipo: "circulo", x: p.x, y: p.y, raio: k.raio };
  }
  if (id === "piscar") {
    const d = Math.min(k.distancia, Math.max(30, Math.hypot(mx - h.x, my - h.y)));
    const p = limitarAoCampo(h.x + Math.cos(ang) * d, h.y + Math.sin(ang) * d);
    return { tipo: "circulo", x: h.x, y: h.y, raio: k.raio, destino: p };
  }
  if (id === "muralha") {
    const c = pontoNoAlcance(h, mx, my, k.alcance);
    const a = Math.atan2(c.y - h.y, c.x - h.x) + Math.PI / 2, l = k.comprimento / 2;
    const p1 = limitarAoCampo(c.x + Math.cos(a) * l, c.y + Math.sin(a) * l);
    const p2 = limitarAoCampo(c.x - Math.cos(a) * l, c.y - Math.sin(a) * l);
    return { tipo: "faixa", x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y, largura: 4 };
  }
  return null;
}

// ------------------------------------------------------------------------------------------------ dano
/**
 * Um acerto: tira vida, empurra (vivo) ou derruba (morto). `forte`: o golpe arremessa quem morre e interrompe até a
 * preparação das ameaças. `sutil`: dano contínuo (fogo), sem pausa no alvo. Devolve 0 (nada), 1 (acertou), 2 (matou).
 */
export function ferir(m, u, dano, fonte, o = {}) {
  if (u.morto || u.saiu) return 0;
  const h = m.heroi;
  if (u === h && h.invul > 0) return 0;
  const dx = o.dx || 0, dy = o.dy || 0, emp = o.emp || 0;
  if (u.lado === 1) acordar(m, u);
  if (u.vulneravel > 0) dano = Math.round(dano * u.def.carga.vulneravel);   // o líder ofegante depois da carga
  const antes = u.vida;
  u.vida -= dano;
  u.flash = o.sutil ? 0.04 : o.forte ? 0.09 : 0.06;
  u.ferido = m.t;
  if (u === h) m.stats.danoSofrido += dano;
  else if (u.lado === 0) m.stats.danoTropas += dano;
  // o número na tela é o dano que saiu da vida: o mesmo valor, uma vez por acerto (o contínuo também, por tique)
  if (fonte === h && u.lado === 1 && dano > 0) m.eventos.push({ tipo: "dano", id: u.id, x: u.x, y: u.y, valor: dano, dx, dy,
    forte: !!o.forte, critico: !!o.critico, sutil: !!o.sutil, elemento: o.elemento || null, morte: u.vida <= 0, antes });
  if (fonte === h && u.lado === 1) ganharRecurso(m, h.def.recurso.porAcerto || 0);
  if (u.vida <= 0) {
    morrer(m, u, fonte, dx, dy, emp, o.forte);
    return 2;
  }
  const k = (emp / Math.pow(u.massa, 0.8)) * (u.firme ? TIPOS.lider.presencaFirmeza : 1);
  u.kx += dx * k;
  u.ky += dy * k;
  if (!o.sutil && u !== h) u.congelado = Math.max(u.congelado, o.forte ? 0.07 : 0.045);
  let at = o.atord || 0;
  if (u.def.elite || u === h) at *= 0.4;
  // golpe fraco só faz recuar e estremecer; atordoar e interromper uma preparação é coisa de golpe forte
  if (at > 0 && (o.forte || !u.acao)) {
    u.atordoado = Math.max(u.atordoado, at);
    if (u.acao && u !== h && u.acao.tipo !== "carga") {
      if (u.def.elite) m.eventos.push({ tipo: "interrompe", x: u.x, y: u.y });
      if (u.acao.tipo === "reunir") soltarReunidos(m, u);
      u.acao = null;
    }
  }
  if (!o.sutil) m.eventos.push({ tipo: "acerto", x: u.x, y: u.y, dx, dy, forte: !!o.forte, lado: u.lado, alvo: u.tipo });
  return 1;
}

function ganharRecurso(m, n) {
  const h = m.heroi;
  if (!n || h.def.recurso.regen) return;
  h.recurso = Math.min(h.recursoMax, h.recurso + n);
}

function morrer(m, u, fonte, dx, dy, emp, forte) {
  u.morto = true;
  u.vida = 0;
  u.acao = null;
  const voa = !!forte && u.massa < 3;
  // o arremesso é efeito: voa uns 20 a 45 px na direção do golpe (mais longe que isso, o corpo parecia outro soldado)
  const vel = voa ? emp * 0.3 + 25 * m.rng() : 14 + 8 * m.rng();
  m.eventos.push({ tipo: "morte", id: u.id, unidade: u.tipo, lado: u.lado, x: u.x, y: u.y, dx, dy, vel,
    sobe: voa ? 55 + 35 * m.rng() : 18, voa, virado: u.virado });
  const h = m.heroi;
  if (u === h) {
    m.fimEm = m.t + BATALHA.derrotaDura;
    m.resultado = "derrota";
    registrar(m, "O herói caiu.");
    return;
  }
  if (u.lado === 0) m.stats.perdas++;
  if (fonte === h) {
    m.stats.abatesHeroi++;
    ganharRecurso(m, h.def.recurso.porAbate || 0);
    if (h.def.curaPorAbate) h.vida = Math.min(h.vidaMax, h.vida + h.def.curaPorAbate);
  } else if (u.lado === 1) m.stats.abatesAliados++;
  if (u.tipo === "estandarte") {
    const r2 = u.def.abala * u.def.abala;
    for (const e of m.lados[1]) if (!e.morto && dist2(e, u) <= r2) { e.abalado = u.def.abalaTempo; e.acao = null; }
    m.eventos.push({ tipo: "abalo", x: u.x, y: u.y, raio: u.def.abala });
    registrar(m, "O porta-estandarte caiu: os inimigos em volta recuam.");
  }
  if (u.tipo === "campeao") registrar(m, "O campeão caiu.");
  if (u.tipo === "lider") {
    // a consequência anunciada no encontro: a tropa perto dele foge; o resto se abala
    if (u.acao && u.acao.tipo === "reunir") soltarReunidos(m, u);
    const d = u.def.derrota;
    let fogem = 0;
    for (const e of m.lados[1]) {
      if (e.morto || e === u) continue;
      if (dist2(e, u) <= d.foge * d.foge) { e.fugindo = true; e.acao = null; fogem++; }
      else { e.abalado = Math.max(e.abalado, d.abala); e.acao = null; }
    }
    m.lider = null;
    m.eventos.push({ tipo: "liderCaiu", x: u.x, y: u.y, raio: d.foge, fogem });
    registrar(m, `${u.def.nome} caiu: ${fogem} inimigos perto dele fogem; os outros se abalam por ${d.abala} s.`);
  }
}

/** O crítico do herói: 10% de chance de 1,5× (arredondado), sorteado por acerto. */
function golpeDoHeroi(m, h, base) {
  const c = h.def.critico;
  if (c && m.rng() < c.chance) return { dano: Math.round(base * c.mult), critico: true };
  return { dano: base, critico: false };
}

/** Aplica um golpe do herói a todos os inimigos dentro da forma; uma vez cada um. */
function atingirArea(m, h, f, k, opts = {}) {
  let acertos = 0, abates = 0;
  for (const u of m.lados[1]) {
    if (u.morto || !dentro(f, u.x, u.y)) continue;
    let dx = u.x - (f.x ?? h.x), dy = u.y - (f.y ?? h.y);
    const d = Math.hypot(dx, dy);
    if (d < 0.5) { dx = Math.cos(h.mira); dy = Math.sin(h.mira); } else { dx /= d; dy /= d; }
    const g = golpeDoHeroi(m, h, opts.dano ?? k.dano);
    const r = ferir(m, u, g.dano, h, { dx, dy, emp: opts.emp ?? k.empurrao, atord: opts.atord ?? k.atordoa,
      forte: opts.forte !== false, critico: g.critico, elemento: k.elemento });
    if (r === 1 && k.sangra) u.sangra = { n: Math.round(k.sangra.duracao / 0.5), tick: 0.5, tique: k.sangra.tique };
    if (r) acertos++;
    if (r === 2) abates++;
  }
  return { acertos, abates };
}

// ------------------------------------------------------------------------------------------------ o herói
function podeIniciar(h, id) {
  const k = h.kit[id];
  if (!k) return false;
  if ((h.cds[id] || 0) > 0) return false;
  if (k.custo && h.recurso < k.custo) return false;
  const a = h.acao;
  if (!a) return true;
  if (id === "basico") return false;
  // uma habilidade corta o ataque básico a qualquer momento e a recuperação de qualquer golpe depois do contato;
  // a preparação de um golpe forte não se cancela (é o compromisso dele)
  return a.id === "basico" || (a.fase === "rec" && a.cancelavel);
}

function iniciar(m, h, id, ent) {
  const k = h.kit[id];
  if (k.custo) h.recurso -= k.custo;
  if (k.recarga) h.cds[id] = k.recarga;
  const u = (m.stats.usos[id] ||= { usos: 0, acertos: 0, abates: 0 });
  u.usos++;
  const ang = h.mira;
  const a = { id, fase: "preparo", t: k.preparo || 0, dir: ang, mover: 0, cancelavel: false, mx: ent.mx, my: ent.my,
    forma: formaDaAcao(h, id, ent.mx, ent.my) };
  if (id === "basico") {
    a.mover = k.mover;
    if (k.arremate) {
      h.combo = h.comboT > 0 ? h.combo + 1 : 1;
      h.comboT = k.arremate.janela;
      a.arremate = h.combo >= k.arremate.cada;
      if (a.arremate) h.combo = 0;
    }
  }
  if (id === "investida" && !k.inspira) {
    a.fase = "voo";
    a.t = k.duracao;
    a.vx = (Math.cos(ang) * k.distancia) / k.duracao;
    a.vy = (Math.sin(ang) * k.distancia) / k.duracao;
    a.atingidos = new Set();
    h.invul = k.duracao + 0.05;
  }
  h.acao = a;
  m.eventos.push({ tipo: "inicio", id, heroi: h.nomeHeroi, forma: a.forma, preparo: a.t, arremate: a.arremate });
  if (id === "piscar") contato(m, h, a);   // instantâneo
}

function atualizarHeroi(m, h, ent, dt) {
  if (h.morto) return;
  for (const id in h.cds) if (h.cds[id] > 0) h.cds[id] = Math.max(0, h.cds[id] - dt);
  if (h.invul > 0) h.invul = Math.max(0, h.invul - dt);
  if (h.flash > 0) h.flash = Math.max(0, h.flash - dt);
  if (h.comboT > 0) h.comboT -= dt;
  const rec = h.def.recurso;
  if (rec.regen) h.recurso = Math.min(h.recursoMax, h.recurso + rec.regen * dt);
  const mdx = ent.mx - h.x, mdy = ent.my - h.y;
  if (mdx * mdx + mdy * mdy > 0.25) h.mira = Math.atan2(mdy, mdx);
  if (m.fase === "fim" || m.resultado === "derrota") return;

  for (const id of ent.apertos) if (h.kit[id]) h.buffer = { id, t: ADIANTAR };
  if (h.buffer) {
    h.buffer.t -= dt;
    if (h.buffer.t <= 0) h.buffer = null;
  }
  const preso = h.atordoado > 0;
  if (preso) h.atordoado -= dt;
  if (!preso && h.buffer && podeIniciar(h, h.buffer.id)) {
    const id = h.buffer.id;
    h.buffer = null;
    iniciar(m, h, id, ent);
  }
  if (!preso && !h.acao && ent.atacar && podeIniciar(h, "basico")) iniciar(m, h, "basico", ent);

  let ix = (ent.dir ? 1 : 0) - (ent.esq ? 1 : 0), iy = (ent.baixo ? 1 : 0) - (ent.cima ? 1 : 0);
  if (ix && iy) { ix *= Math.SQRT1_2; iy *= Math.SQRT1_2; }
  const a = h.acao;
  // andar corta a recuperação de um golpe forte depois do contato (o mesmo vale para todos: é a regra do compromisso)
  if (a && a.fase === "rec" && a.cancelavel && a.id !== "basico" && (ix || iy)) h.acao = null;
  if (h.acao && h.acao.fase === "voo") {
    avancarAcao(m, h, h.acao, dt);
  } else {
    let fator = preso ? 0 : h.acao ? h.acao.mover : 1;
    fator *= Math.max(0.45, 1 / (1 + 0.3 * h.contato));
    const qx = ix * h.def.vel * fator, qy = iy * h.def.vel * fator;
    const taxa = (ix || iy) && fator > 0 ? ACELERA : FREIA;
    const dvx = qx - h.vx, dvy = qy - h.vy, dv = Math.hypot(dvx, dvy), lim = taxa * dt;
    if (dv <= lim) { h.vx = qx; h.vy = qy; } else { h.vx += (dvx / dv) * lim; h.vy += (dvy / dv) * lim; }
    if (h.acao) avancarAcao(m, h, h.acao, dt);
  }
  const olhar = h.acao ? h.acao.dir : h.mira;
  const c = Math.cos(olhar);
  if (Math.abs(c) > 0.05) h.virado = c > 0 ? 1 : -1;
}

function avancarAcao(m, h, a, dt) {
  a.t -= dt;
  const k = h.kit[a.id];
  if (a.fase === "preparo") {
    if (a.t <= 0) contato(m, h, a);
    return;
  }
  if (a.fase === "voo" && a.id === "investida") {
    h.vx = a.vx;
    h.vy = a.vy;
    h.kx = h.ky = 0;
    const ux = Math.cos(a.dir), uy = Math.sin(a.dir);
    for (const e of m.lados[1]) {
      if (e.morto || a.atingidos.has(e.id)) continue;
      const rx = e.x - h.x, ry = e.y - h.y;
      if (rx * rx + ry * ry > (k.largura + e.raio) ** 2) continue;
      a.atingidos.add(e.id);
      if (e.massa >= 6) {
        // o campeão segura a investida: os dois sentem o choque
        const g = golpeDoHeroi(m, h, k.dano);
        ferir(m, e, g.dano, h, { dx: ux, dy: uy, emp: k.empurrao, atord: k.atordoa, forte: true, critico: g.critico });
        a.t = 0;
        h.vx = -ux * 40;
        h.vy = -uy * 40;
        m.eventos.push({ tipo: "choque", x: e.x, y: e.y });
        break;
      }
      // os soldados no caminho são jogados para os lados (e um pouco para a frente)
      const lado = ux * ry - uy * rx >= 0 ? 1 : -1;
      let px = -uy * lado * 0.85 + ux * 0.5, py = ux * lado * 0.85 + uy * 0.5;
      const n = Math.hypot(px, py);
      px /= n; py /= n;
      const g = golpeDoHeroi(m, h, k.dano);
      ferir(m, e, g.dano, h, { dx: px, dy: py, emp: k.empurrao, atord: k.atordoa, forte: true, critico: g.critico });
    }
    if (a.t <= 0) {
      // a chegada empurra quem ficou perto (sem dano: o dano da investida é um por inimigo)
      const f = { tipo: "circulo", x: h.x, y: h.y, raio: k.fimRaio };
      for (const e of m.lados[1]) {
        if (e.morto || a.atingidos.has(e.id) || !dentro(f, e.x, e.y)) continue;
        const dx = e.x - h.x, dy = e.y - h.y, d = Math.hypot(dx, dy) || 1;
        ferir(m, e, 0, h, { dx: dx / d, dy: dy / d, emp: k.fimEmpurrao, atord: 0.25, forte: false });
      }
      const s = m.stats.usos.investida;
      s.acertos += a.atingidos.size;
      m.eventos.push({ tipo: "contato", id: "investida", x: h.x, y: h.y, dir: a.dir, acertos: a.atingidos.size,
        tremor: k.tremor, raio: k.fimRaio });
      if (a.atingidos.size) registrar(m, `Investida: ${a.atingidos.size} atingidos.`);
      a.fase = "rec";
      a.t = 0.12;
      a.cancelavel = true;
      a.mover = 0.5;
      h.vx *= 0.25;
      h.vy *= 0.25;
    }
    return;
  }
  if (a.fase === "voo" && a.id === "salto") {
    const p = 1 - Math.max(0, a.t) / k.voo, e = p < 0.5 ? 2 * p * p : 1 - (-2 * p + 2) ** 2 / 2;
    h.x = a.ox + (a.tx - a.ox) * e;
    h.y = a.oy + (a.ty - a.oy) * e;
    h.vx = h.vy = h.kx = h.ky = 0;
    h.z = Math.sin(Math.PI * p) * 22;
    if (a.t <= 0) {
      h.z = 0;
      h.x = a.tx;
      h.y = a.ty;
      const f = { tipo: "circulo", x: h.x, y: h.y, raio: k.raio };
      const r = atingirArea(m, h, f, k);
      golpeConcluido(m, h, a, r, k, { x: h.x, y: h.y, raio: k.raio });
      a.fase = "rec";
      a.t = k.rec;
      a.cancelavel = true;
    }
    return;
  }
  if (a.fase === "rec" && a.t <= 0) h.acao = null;
}

function golpeConcluido(m, h, a, r, k, extra) {
  const s = m.stats.usos[a.id];
  s.acertos += r.acertos;
  s.abates += r.abates;
  m.stats.maiorGolpe = Math.max(m.stats.maiorGolpe, r.abates);
  const pausa = k.pausa ? Math.min(k.pausaMax || k.pausa, k.pausa + (k.pausaPorAbate || 0) * Math.max(0, r.abates - 1)) : 0;
  const tremor = k.tremor ? Math.min(k.tremorMax || k.tremor, k.tremor + (k.tremorPorAbate || 0) * r.abates) : 0;
  m.eventos.push({ tipo: "contato", id: a.id, dir: a.dir, acertos: r.acertos, abates: r.abates,
    pausa: r.acertos ? pausa : 0, tremor: r.acertos ? tremor : tremor * 0.4, ...extra });
  if (a.id !== "basico" && (r.acertos || a.id === "salto")) {
    registrar(m, `${k.nome}: ${r.acertos} atingido${r.acertos === 1 ? "" : "s"}, ${r.abates} derrubado${r.abates === 1 ? "" : "s"}.`);
  }
}

function contato(m, h, a) {
  const k = h.kit[a.id];
  a.cancelavel = true;
  if (a.id === "basico" && k.arremate) {
    const r0 = a.arremate ? k.arremate : k;
    const f = { tipo: "arco", x: h.x, y: h.y, raio: r0.raio, ang: a.dir, abertura: r0.abertura || k.abertura };
    const r = atingirArea(m, h, f, k, { dano: r0.dano, emp: r0.empurrao, atord: r0.atordoa, forte: !!a.arremate });
    golpeConcluido(m, h, a, r, a.arremate ? { ...k, ...k.arremate } : k, { forma: f, arremate: a.arremate });
    a.fase = "rec"; a.t = k.rec; a.mover = k.mover;
    return;
  }
  if (a.id === "basico") {
    m.proj.push({ tipo: "faisca", x: h.x + Math.cos(a.dir) * 5, y: h.y + Math.sin(a.dir) * 5 - 0,
      dx: Math.cos(a.dir), dy: Math.sin(a.dir), vel: k.vel, resta: k.alcance, k });
    m.eventos.push({ tipo: "disparo", id: "basico", x: h.x, y: h.y, dir: a.dir });
    a.fase = "rec"; a.t = k.rec; a.mover = k.mover;
    return;
  }
  if (a.id === "varredura") {
    const f = { tipo: "arco", x: h.x, y: h.y, raio: k.raio, ang: a.dir, abertura: k.abertura };
    const r = atingirArea(m, h, f, k);
    golpeConcluido(m, h, a, r, k, { forma: f });
    a.fase = "rec"; a.t = k.rec;
    return;
  }
  if (a.id === "salto") {
    const p = pontoNoAlcance(h, a.mx, a.my, k.alcance);
    Object.assign(a, { fase: "voo", t: k.voo, ox: h.x, oy: h.y, tx: p.x, ty: p.y });
    h.invul = k.voo + 0.05;
    m.eventos.push({ tipo: "decolagem", x: h.x, y: h.y, tx: p.x, ty: p.y, raio: k.raio, voo: k.voo });
    return;
  }
  if (a.id === "bola") {
    const p = pontoNoAlcance(h, a.mx, a.my, k.alcance);
    const d = Math.hypot(p.x - h.x, p.y - h.y);
    m.proj.push({ tipo: "bola", x0: h.x, y0: h.y, x1: p.x, y1: p.y, t: 0, dur: Math.max(0.08, d / k.vel), k,
      x: h.x, y: h.y });
    m.eventos.push({ tipo: "disparo", id: "bola", x: h.x, y: h.y, tx: p.x, ty: p.y, raio: k.raio });
    a.fase = "rec"; a.t = k.rec;
    return;
  }
  if (a.id === "piscar") {
    const f = { tipo: "circulo", x: h.x, y: h.y, raio: k.raio };
    const r = atingirArea(m, h, f, k);
    const fd = formaDaAcao(h, "piscar", a.mx, a.my);
    const x0 = h.x, y0 = h.y;
    h.x = h.px = fd.destino.x;
    h.y = h.py = fd.destino.y;
    h.vx *= 0.3; h.vy *= 0.3;
    h.invul = Math.max(h.invul, k.invul);
    golpeConcluido(m, h, a, r, k, { x: x0, y: y0, raio: k.raio, x1: h.x, y1: h.y });
    a.fase = "rec"; a.t = 0.1; a.mover = 1;
    return;
  }
  if (a.id === "investida" && k.inspira) {
    // o Grito: inspira as tropas perto (atacam mais rápido e se curam) e abala os inimigos colados ao herói
    let n = 0, ab = 0;
    for (const u of m.lados[0]) {
      if (u === h || dist2(u, h) > k.raio * k.raio) continue;
      u.inspirado = k.inspira; u.inspiraRitmo = 1 / k.ritmo; u.inspiraCura = k.cura; n++;
    }
    for (const e of m.lados[1]) {
      if (e.def.elite || e.firme || dist2(e, h) > k.raioAbala * k.raioAbala) continue;
      e.abalado = Math.max(e.abalado, k.abala); e.acao = null; ab++;
    }
    m.stats.usos.investida.acertos += n;
    m.eventos.push({ tipo: "contato", id: "grito", x: h.x, y: h.y, raio: k.raio, tremor: k.tremor, acertos: n, abates: 0 });
    registrar(m, `Grito de Guerra: ${n} aliados inspirados, ${ab} inimigos abalados.`);
    a.fase = "rec"; a.t = k.rec;
    return;
  }
  if (a.id === "muralha" && k.variante === "anel") {
    const f = formaDaAcao(h, "muralha", a.mx, a.my);
    m.zonas.push({ tipo: "anel", x: f.x, y: f.y, raio: f.raio, t: k.duracao, dur: k.duracao, tique: k.tique, tick: 0.5, k });
    m.eventos.push({ tipo: "contato", id: "anel", forma: f, tremor: k.tremor, acertos: 0, abates: 0 });
    registrar(m, "Anel de Fogo erguido.");
    a.fase = "rec"; a.t = k.rec;
    return;
  }
  if (a.id === "muralha") {
    const f = formaDaAcao(h, "muralha", a.mx, a.my);
    m.zonas.push({ tipo: "muralha", ...f, t: k.duracao, dur: k.duracao, tique: k.tique, tick: 0.5, k });
    m.eventos.push({ tipo: "contato", id: "muralha", forma: f, tremor: k.tremor, acertos: 0, abates: 0 });
    registrar(m, "Muralha de Fogo erguida.");
    a.fase = "rec"; a.t = k.rec;
  }
}

// ------------------------------------------------------------------------------------------------ as tropas
function atualizarUnidade(m, u, dt) {
  if (u.flash > 0) u.flash = Math.max(0, u.flash - dt);
  if (u.mostra > 0) u.mostra -= dt;
  estados(m, u, dt);
  if (u.morto) return;
  let ritmo = 1;
  if (u.aura) ritmo /= TIPOS.estandarte.auraRitmo;
  if (u.firme) ritmo /= TIPOS.lider.presencaRitmo;
  if (u.inspirado > 0) ritmo /= u.inspiraRitmo || 1;
  if (u.recarga > 0) u.recarga -= dt * ritmo;
  if (u.congelado > 0) { u.congelado -= dt; u.vx = u.vy = 0; return; }
  if (u.atordoado > 0) { u.atordoado -= dt; u.vx = u.vy = 0; return; }
  if (u.ofegante > 0) { u.ofegante -= dt; u.vx = u.vy = 0; return; }
  const d = u.def;
  // a carga do líder: quem foi reunido espera parado, virado para a faixa; depois corre junto
  if (u.reuniao) { u.vx = u.vy = 0; u.virado = Math.cos(u.reuniao.acao ? u.reuniao.acao.dir : 0) >= 0 ? 1 : -1; return; }
  if (u.carga) {
    u.carga.t -= dt;
    u.vx = u.carga.dx * TIPOS.lider.carga.vel;
    u.vy = u.carga.dy * TIPOS.lider.carga.vel;
    u.virado = u.vx >= 0 ? 1 : -1;
    if (u.carga.t <= 0) { u.carga = null; u.impeto = TIPOS.lider.carga.impeto; u.reavaliar = 0; }
    return;
  }
  if (u.fugindo) {
    u.alvo = null;
    u.acao = null;
    andarPara(u, u.lado === 1 ? CAMPO.largura + 40 : -40, u.y, d.vel * 1.15);
    if (u.x > CAMPO.largura - 2 || u.x < 2) { u.saiu = true; m.stats.fugiram++; }
    return;
  }
  if (u.abalado > 0 && u.firme) u.abalado = 0;   // a presença do líder segura a tropa
  if (u.abalado > 0) {
    u.abalado -= dt;
    const h = m.heroi, dx = u.x - h.x, dy = u.y - h.y, n = Math.hypot(dx, dy) || 1;
    u.vx = (dx / n) * d.vel * 0.6;
    u.vy = (dy / n) * d.vel * 0.6;
    u.virado = u.vx >= 0 ? 1 : -1;
    return;
  }
  if (u.acao) { progredirAtaque(m, u, dt); return; }
  if (u.lado === 1) {
    if (u.grupo) {
      // os grupos dos encontros acordam no tempo deles, quando alguém chega perto ou quando um deles apanha
      const g = m.grupos[u.grupo];
      if (!g.ativo) {
        if (m.t >= g.ativa || ameacaPerto(m, u, 80)) acordar(m, u);
        else { u.vx = u.vy = 0; return; }
      }
    } else if (m.fase === "formacao" && !ameacaPerto(m, u, 70)) { u.vx = u.vy = 0; return; }
  }
  if (u.tipo === "lider" && m.fase !== "fuga" && tentarCarga(m, u, dt)) return;
  u.reavaliar -= dt;
  if (u.reavaliar <= 0 || !u.alvo || u.alvo.morto || u.alvo.saiu || !alvoValido(m, u, u.alvo)) {
    u.alvo = escolherAlvo(m, u);
    u.reavaliar = BATALHA.reavaliar[0] + m.rng() * (BATALHA.reavaliar[1] - BATALHA.reavaliar[0]);
  }
  if (d.papel === "apoio" && apoio(m, u)) return;
  if (!u.alvo) { semAlvo(m, u); return; }
  if (d.papel === "longe") arqueiro(m, u);
  else corpoACorpo(m, u);
}

function estados(m, u, dt) {
  if (u.sangra) {
    // o sangramento conta tiques (n), não segundos: são exatamente duração ÷ 0,5 tiques, sem erro de arredondamento
    u.sangra.tick -= dt;
    if (u.sangra.tick <= 1e-9) {
      u.sangra.tick += 0.5;
      u.sangra.n--;
      const s = u.sangra;
      if (s.n <= 0) u.sangra = null;
      ferir(m, u, s.tique, m.heroi, { sutil: true, elemento: "sangue" });
    }
  }
  if (u.inspirado > 0) {
    u.inspirado -= dt;
    u.vida = Math.min(u.vidaMax, u.vida + (u.inspiraCura || 0) * dt);
  }
  if (u.vulneravel > 0) u.vulneravel -= dt;
  if (u.impeto > 0) u.impeto -= dt;
}

/** Acorda o grupo da unidade (e desfaz a formação da batalha original). */
function acordar(m, u) {
  if (m.fase === "formacao" && !u.grupo) {
    // atacada, a primeira leva desfaz a formação e avança (não espera parada a próxima explosão)
    m.fase = "luta";
    m.eventos.push({ tipo: "avanco" });
  }
  if (u.grupo && !m.grupos[u.grupo].ativo) {
    m.grupos[u.grupo].ativo = true;
    m.eventos.push({ tipo: "acorda", grupo: u.grupo, x: u.x, y: u.y });
  }
}

// O líder tenta a Carga a cada 0,4 s, quando a recarga deixa: escolhe o grupo nosso mais denso entre 50 e 170 px
// (o herói conta como três), reúne até 10 soldados dele por perto e marca a faixa no chão.
function tentarCarga(m, u, dt) {
  const c = u.def.carga;
  if (u.cargaCd === undefined) u.cargaCd = c.primeira;
  if (u.cargaCd > 0) { u.cargaCd -= dt; return false; }
  u.tentaCarga = (u.tentaCarga || 0) - dt;
  if (u.tentaCarga > 0) return false;
  u.tentaCarga = 0.4;
  let melhor = null, nMelhor = 0;
  for (const a of m.lados[0]) {
    const d2 = dist2(a, u);
    if (d2 < 50 * 50 || d2 > 170 * 170) continue;
    let n = 0;
    for (const b of m.lados[0]) if (dist2(a, b) <= 30 * 30) n += b === m.heroi ? 3 : 1;
    if (n > nMelhor) { nMelhor = n; melhor = a; }
  }
  if (!melhor || nMelhor < 4) return false;
  const ang = Math.atan2(melhor.y - u.y, melhor.x - u.x);
  const p = limitarAoCampo(u.x + Math.cos(ang) * c.distancia, u.y + Math.sin(ang) * c.distancia);
  const forma = { tipo: "faixa", x1: u.x, y1: u.y, x2: p.x, y2: p.y, largura: c.largura };
  const perto = m.lados[1].filter((e) => e !== u && !e.def.elite && !e.fugindo && e.def.papel === "perto" &&
    dist2(e, u) <= c.raioReunir ** 2).sort((a, b) => dist2(a, u) - dist2(b, u)).slice(0, c.max);
  for (const s2 of perto) { s2.reuniao = u; s2.acao = null; s2.alvo = null; }
  u.acao = { tipo: "reunir", t: c.reunir, dir: ang, forma, reunidos: perto };
  u.vx = u.vy = 0;
  u.virado = Math.cos(ang) >= 0 ? 1 : -1;
  u.cargaCd = c.recarga;
  m.eventos.push({ tipo: "aviso", id: u.id, forma, preparo: c.reunir, lider: true, reunidos: perto.length });
  registrar(m, `${u.def.nome} reúne ${perto.length} soldados para a carga.`);
  return true;
}

function soltarReunidos(m, u) {
  for (const s2 of u.acao.reunidos) if (s2.reuniao === u) s2.reuniao = null;
}

function ameacaPerto(m, u, r) {
  const r2 = r * r;
  for (const o of m.lados[1 - u.lado]) if (!o.morto && dist2(o, u) <= r2) return true;
  return false;
}

function andarPara(u, x, y, vel) {
  const dx = x - u.x, dy = y - u.y, d = Math.hypot(dx, dy);
  if (d < 1.5) { u.vx = u.vy = 0; return d; }
  const v = Math.min(vel, d * 8);
  u.vx = (dx / d) * v;
  u.vy = (dy / d) * v;
  if (Math.abs(dx) > 0.3) u.virado = dx > 0 ? 1 : -1;
  return d;
}

// as restrições da ordem: quem segue o herói só se afasta para lutar perto dele; quem defende, perto do ponto
function alvoValido(m, u, c) {
  if (u.lado !== 0) {
    // a retaguarda de arqueiros fica no posto: só mira quem está ao alcance de lá
    if (u.posto) return (c.x - u.posto.x) ** 2 + (c.y - u.posto.y) ** 2 <= (u.def.alcance + 30) ** 2;
    return true;
  }
  const o = u.ordem || m.ordem, ord = ORDENS[o.tipo];
  if (o.tipo === "acompanhar") {
    const h = m.heroi;
    if (h.morto) return true;
    return dist2(u, c) <= ord.engaja ** 2 || dist2(h, c) <= ord.engajaHeroi ** 2;
  }
  if (o.tipo === "defender") return (c.x - o.x) ** 2 + (c.y - o.y) ** 2 <= ord.coleira ** 2;
  return true;
}

function escolherAlvo(m, u) {
  const o = u.ordem || m.ordem;
  let melhor = null, custoMin = Infinity;
  for (const c of m.lados[1 - u.lado]) {
    if (c.morto || c.saiu || c.fugindo && u.def.papel !== "longe" && dist2(u, c) > 900) continue;
    if (u.lado === 0 && o.tipo === "defender") {
      if ((c.x - o.x) ** 2 + (c.y - o.y) ** 2 > ORDENS.defender.engaja ** 2) continue;
    } else if (!alvoValido(m, u, c)) continue;
    const d = Math.sqrt(dist2(u, c));
    if (u.def.papel === "longe" && d > 300) continue;
    const fila = c.atacantes - (u.alvo === c ? 1 : 0);
    let custo = d + BATALHA.custoFila * Math.max(0, fila);
    if (fila >= c.def.vagas) custo += 400;
    if (u.tipo === "campeao" && c.tipo === "heroi") custo -= 120;
    if (u.tipo === "lider" && c.tipo === "heroi") custo -= 60;
    if (u.posto && !alvoValido(m, u, c)) continue;
    if (u.lado === 1 && c.tipo === "heroi") custo -= u.def.papel === "longe" ? 30 : 15;   // o herói atrai
    if (custo < custoMin) { custoMin = custo; melhor = c; }
  }
  return melhor;
}

function semAlvo(m, u) {
  if (u.lado === 1) {
    const c = m.centros[0];
    if (u.posto) { andarPara(u, u.posto.x, u.posto.y, u.def.vel); return; }
    if (m.fase !== "luta" || !c) { u.vx = u.vy = 0; return; }
    andarPara(u, c.x, c.y, u.def.vel * 0.8);
    return;
  }
  // a posição em volta do ponto da ordem: um anel solto, os arqueiros por fora
  const o = u.ordem || m.ordem;
  let ax, ay;
  if (o.tipo === "acompanhar" && !m.heroi.morto) { ax = m.heroi.x; ay = m.heroi.y; }
  else if (o.tipo === "defender") { ax = o.x; ay = o.y; }
  else {
    const c = m.centros[1];
    if (!c) { u.vx = u.vy = 0; return; }
    andarPara(u, c.x, c.y, u.def.vel);
    return;
  }
  const base = u.def.papel === "longe" ? 34 : 12, ang = u.slot * 2.39996, r = base + 5.2 * Math.sqrt(u.slot);
  let sx = ax + Math.cos(ang) * r, sy = ay + Math.sin(ang) * r;
  if (o.tipo === "acompanhar" && u.def.papel === "longe") sx -= 18;   // os arqueiros um pouco atrás do herói
  const p = limitarAoCampo(sx, sy);
  const d = Math.hypot(p.x - u.x, p.y - u.y);
  if (d < 3) { u.vx = u.vy = 0; return; }
  andarPara(u, p.x, p.y, u.def.vel * (d > 40 ? 1.15 : 1));
}

function corpoACorpo(m, u) {
  const a = u.alvo, d = u.def;
  const dx = a.x - u.x, dy = a.y - u.y, dist = Math.hypot(dx, dy) || 0.001;
  const folga = dist - u.raio - a.raio;
  if (Math.abs(dx) > 0.3) u.virado = dx > 0 ? 1 : -1;
  if (folga > d.alcance) {
    // chegando perto, cada um abre um pouco para o seu lado: o grupo envolve o alvo em vez de fazer fila
    let ux = dx / dist, uy = dy / dist;
    if (dist < 30) {
      const s = (u.id % 2 ? 1 : -1) * 0.35;
      ux += -uy * s; uy += (dx / dist) * s;
      const n = Math.hypot(ux, uy); ux /= n; uy /= n;
    }
    u.vx = ux * d.vel;
    u.vy = uy * d.vel;
    return;
  }
  u.vx = u.vy = 0;
  if (u.recarga > 0) return;
  const ang = Math.atan2(dy, dx);
  u.acao = { t: d.preparo, alvo: a, dir: ang };
  if (u.tipo === "campeao" || u.tipo === "lider") {
    u.acao.forma = { tipo: "arco", x: u.x, y: u.y, raio: d.alcance + u.raio + 4, ang, abertura: d.abertura };
    m.eventos.push({ tipo: "aviso", id: u.id, forma: u.acao.forma, preparo: d.preparo });
  }
}

function progredirAtaque(m, u, dt) {
  u.vx = u.vy = 0;
  const a = u.acao, d = u.def;
  a.t -= dt;
  if (a.tipo === "reunir") {
    a.forma.x1 = u.x; a.forma.y1 = u.y;
    if (a.t > 0) return;
    // a carga: o líder corre a faixa atropelando quem está nela; os reunidos correm junto, lado a lado
    const c = d.carga, ux = Math.cos(a.dir), uy = Math.sin(a.dir), dur = c.distancia / c.vel;
    for (const s2 of a.reunidos) {
      if (s2.reuniao !== u || s2.morto) continue;
      s2.reuniao = null;
      s2.carga = { dx: ux, dy: uy, t: dur };
    }
    u.acao = { tipo: "carga", t: dur, dir: a.dir, forma: a.forma, atingidos: new Set() };
    m.eventos.push({ tipo: "carga", x: u.x, y: u.y, dir: a.dir, forma: a.forma });
    return;
  }
  if (a.tipo === "carga") {
    const c = d.carga, ux = Math.cos(a.dir), uy = Math.sin(a.dir);
    u.vx = ux * c.vel; u.vy = uy * c.vel;
    for (const o of m.lados[1 - u.lado]) {
      if (o.morto || a.atingidos.has(o.id)) continue;
      if ((o.x - u.x) ** 2 + (o.y - u.y) ** 2 > (c.largura + o.raio) ** 2) continue;
      a.atingidos.add(o.id);
      const lado = ux * (o.y - u.y) - uy * (o.x - u.x) >= 0 ? 1 : -1;
      const px = -uy * lado * 0.8 + ux * 0.6, py = ux * lado * 0.8 + uy * 0.6, n = Math.hypot(px, py);
      ferir(m, o, o === m.heroi ? c.danoHeroi : c.dano, u, { dx: px / n, dy: py / n, emp: c.empurrao, atord: 0.4, forte: true });
    }
    if (a.t > 0) return;
    u.acao = null;
    u.vx = u.vy = 0;
    u.ofegante = c.ofegante;
    u.vulneravel = c.ofegante;
    m.eventos.push({ tipo: "fimCarga", x: u.x, y: u.y, acertos: a.atingidos.size });
    registrar(m, `A carga atropelou ${a.atingidos.size}; ${d.nome} fica ofegante (leva +50% de dano por ${c.ofegante} s).`);
    return;
  }
  if ((u.tipo === "campeao" || u.tipo === "lider") && a.forma) { a.forma.x = u.x; a.forma.y = u.y; }
  if (a.t > 0) return;
  u.acao = null;
  u.mostra = 0.15;   // a pose do golpe fica um instante depois do contato
  u.recarga = d.recarga * (0.85 + 0.3 * m.rng());
  if (d.papel === "longe") {
    const alvo = a.alvo;
    if (alvo.morto) return;
    const dist = Math.hypot(alvo.x - u.x, alvo.y - u.y), dur = dist / d.flecha;
    const x1 = alvo.x + alvo.vx * dur * 0.5 + (m.rng() - 0.5) * 8, y1 = alvo.y + alvo.vy * dur * 0.5 + (m.rng() - 0.5) * 8;
    m.proj.push({ tipo: "flecha", lado: u.lado, x0: u.x, y0: u.y - 4, x1, y1, t: 0, dur, dano: d.dano, fonte: u, x: u.x, y: u.y });
    return;
  }
  if (u.tipo === "campeao" || u.tipo === "lider") {
    let n = 0;
    for (const c of m.lados[1 - u.lado]) {
      if (c.morto || !dentro(a.forma, c.x, c.y)) continue;
      const dx = c.x - u.x, dy = c.y - u.y, dd = Math.hypot(dx, dy) || 1;
      ferir(m, c, c === m.heroi ? d.danoHeroi : d.dano, u, { dx: dx / dd, dy: dy / dd, emp: d.empurrao,
        atord: c === m.heroi ? 0.35 : 0.4, forte: true });
      n++;
    }
    m.eventos.push({ tipo: "golpeCampeao", x: u.x, y: u.y, forma: a.forma, acertos: n,
      heroi: dentro(a.forma, m.heroi.x, m.heroi.y) });
    return;
  }
  const alvo = a.alvo;
  if (alvo.morto) return;
  const folga = Math.hypot(alvo.x - u.x, alvo.y - u.y) - u.raio - alvo.raio;
  if (folga > d.alcance + 4) return;   // o alvo saiu do alcance durante a preparação: golpe no vazio
  const dx = alvo.x - u.x, dy = alvo.y - u.y, dd = Math.hypot(dx, dy) || 1;
  const mult = (u.aura ? TIPOS.estandarte.auraDano : 1) * (alvo === m.heroi ? BATALHA.danoNoHeroi : 1) *
    (u.impeto > 0 ? 2 : 1);
  ferir(m, alvo, (u.lado === 0 && d.danoAliado || d.dano) * mult, u, { dx: dx / dd, dy: dy / dd, emp: 30 });
}

// o porta-estandarte fica uns 40 px atrás do meio do próprio exército; só luta com quem chega encostado
function apoio(m, u) {
  if (u.alvo && Math.hypot(u.alvo.x - u.x, u.alvo.y - u.y) - u.raio - u.alvo.raio <= 6) return false;
  const c = m.centros[u.lado], o = m.centros[1 - u.lado];
  if (!c || !o || m.fase !== "luta") { u.vx = u.vy = 0; return true; }
  const dx = c.x - o.x, dy = c.y - o.y, n = Math.hypot(dx, dy) || 1;
  const p = limitarAoCampo(c.x + (dx / n) * 40, c.y + (dy / n) * 40);
  if (andarPara(u, p.x, p.y, u.def.vel) < 3) u.virado = o.x > u.x ? 1 : -1;
  return true;
}

function arqueiro(m, u) {
  const d = u.def, a = u.alvo;
  // o mais perto dos inimigos: se chegou perto demais, o arqueiro recua antes de atirar
  let perto = null, dp = Infinity;
  for (const c of m.lados[1 - u.lado]) {
    if (c.morto) continue;
    const q = dist2(u, c);
    if (q < dp) { dp = q; perto = c; }
  }
  dp = Math.sqrt(dp);
  if (perto && dp < d.perto) {
    const dx = u.x - perto.x, dy = u.y - perto.y, n = dp || 1;
    const p = limitarAoCampo(u.x + (dx / n) * 20, u.y + (dy / n) * 20);
    andarPara(u, p.x, p.y, d.vel);
    u.virado = perto.x > u.x ? 1 : -1;
    return;
  }
  const dist = Math.hypot(a.x - u.x, a.y - u.y);
  if (dist > d.alcance) {
    // o arqueiro não se adianta ao próprio exército para alcançar alguém: volta para trás da linha
    const c = m.centros[u.lado], o = m.centros[1 - u.lado];
    if (c && o && u.lado === 1 && Math.hypot(u.x - c.x, u.y - c.y) > 70 && Math.hypot(a.x - c.x, a.y - c.y) > d.alcance) {
      const dx = c.x - o.x, dy = c.y - o.y, n = Math.hypot(dx, dy) || 1;
      andarPara(u, c.x + (dx / n) * 30, c.y + (dy / n) * 30, d.vel);
      return;
    }
    andarPara(u, a.x, a.y, d.vel);
    return;
  }
  u.vx = u.vy = 0;
  u.virado = a.x > u.x ? 1 : -1;
  if (u.recarga <= 0) u.acao = { t: d.preparo, alvo: a, dir: Math.atan2(a.y - u.y, a.x - u.x) };
}

// ------------------------------------------------------------------------------------------------ projéteis e chão
function atualizarProjeteis(m, dt) {
  const fica = [];
  for (const p of m.proj) {
    if (p.tipo === "flecha") {
      p.t += dt;
      const k = Math.min(1, p.t / p.dur);
      p.x = p.x0 + (p.x1 - p.x0) * k;
      p.y = p.y0 + (p.y1 - p.y0) * k;
      if (k < 1) { fica.push(p); continue; }
      let acertou = null, melhor = Infinity;
      for (const c of m.lados[1 - p.lado]) {
        if (c.morto) continue;
        const q = (c.x - p.x1) ** 2 + (c.y - p.y1) ** 2;
        if (q < melhor && q <= (c.raio + 2.5) ** 2) { melhor = q; acertou = c; }
      }
      const dl = Math.hypot(p.x1 - p.x0, p.y1 - p.y0) || 1;
      if (acertou && p.lado === 1) acertou === m.heroi ? m.stats.flechasHeroi++ : m.stats.flechasTropas++;
      if (acertou) ferir(m, acertou, p.dano * (acertou === m.heroi ? BATALHA.danoNoHeroi : 1), p.fonte, { dx: (p.x1 - p.x0) / dl, dy: (p.y1 - p.y0) / dl, emp: 10 });
      else m.eventos.push({ tipo: "flechaChao", x: p.x1, y: p.y1, ang: Math.atan2(p.y1 - p.y0, p.x1 - p.x0) });
      continue;
    }
    if (p.tipo === "faisca") {
      const passos = Math.ceil((p.vel * dt) / 3);
      let fim = false;
      for (let i = 0; i < passos && !fim; i++) {
        const s = (p.vel * dt) / passos;
        p.x += p.dx * s; p.y += p.dy * s; p.resta -= s;
        for (const c of m.lados[1]) {
          if (c.morto || (c.x - p.x) ** 2 + (c.y - p.y) ** 2 > (c.raio + 1.5) ** 2) continue;
          const g = golpeDoHeroi(m, m.heroi, p.k.dano);
          const r = ferir(m, c, g.dano, m.heroi, { dx: p.dx, dy: p.dy, emp: p.k.empurrao, atord: p.k.atordoa, critico: g.critico });
          const s2 = m.stats.usos.basico;
          if (s2) { s2.acertos++; if (r === 2) s2.abates++; }
          m.eventos.push({ tipo: "faiscaAcerto", x: p.x, y: p.y });
          fim = true;
          break;
        }
        if (p.resta <= 0 || p.x < 0 || p.y < 0 || p.x > CAMPO.largura || p.y > CAMPO.altura) {
          if (!fim) m.eventos.push({ tipo: "faiscaFim", x: p.x, y: p.y });
          fim = true;
        }
      }
      if (!fim) fica.push(p);
      continue;
    }
    if (p.tipo === "bola") {
      p.t += dt;
      const k = Math.min(1, p.t / p.dur);
      p.x = p.x0 + (p.x1 - p.x0) * k;
      p.y = p.y0 + (p.y1 - p.y0) * k;
      p.z = Math.sin(Math.PI * k) * Math.min(16, p.dur * 40);
      if (k < 1) { fica.push(p); continue; }
      const h = m.heroi, f = { tipo: "circulo", x: p.x1, y: p.y1, raio: p.k.raio };
      const r = atingirArea(m, h, f, p.k);
      golpeConcluido(m, h, { id: "bola", dir: Math.atan2(p.y1 - p.y0, p.x1 - p.x0) }, r, p.k, { x: p.x1, y: p.y1, raio: p.k.raio, forma: f });
      const ch = p.k.chao;
      m.zonas.push({ tipo: "chao", x: p.x1, y: p.y1, raio: ch.raio || p.k.raio * 0.8, t: ch.duracao, dur: ch.duracao,
        tique: ch.tique, repele: !!ch.repele, tick: 0.5 });   // o chão começa a queimar depois da explosão, não junto
    }
  }
  m.proj = fica;
}

function atualizarZonas(m, dt) {
  const fica = [];
  for (const z of m.zonas) {
    z.t -= dt;
    z.tick -= dt;
    const tique = z.tick <= 0;
    if (tique) z.tick += 0.5;   // o fogo queima de meio em meio segundo, um valor inteiro por tique
    for (const u of m.lados[1]) {
      if (u.morto) continue;
      if (z.tipo === "chao") {
        const d = Math.hypot(u.x - z.x, u.y - z.y);
        if (tique && d <= z.raio) ferir(m, u, z.tique, m.heroi, { sutil: true, elemento: "fogo" });
        // o chão da Bola Incendiária: quem está de fora contorna; quem está dentro sai pelo lado mais perto
        if (z.repele && !u.morto && d < z.raio + 4 && d > 0.01) {
          const f = Math.min(1.2, (z.raio + 4 - d) * 0.08);
          u.x += ((u.x - z.x) / d) * f; u.y += ((u.y - z.y) / d) * f;
        }
        continue;
      }
      if (z.tipo === "anel") {
        // o Anel: a linha de fogo queima e ninguém a atravessa (quem está dentro fica dentro, quem está fora, fora)
        const d = Math.hypot(u.x - z.x, u.y - z.y), borda = Math.abs(d - z.raio);
        if (tique && borda <= 4) ferir(m, u, z.tique, m.heroi, { sutil: true, elemento: "fogo" });
        if (!u.morto && borda < 7 && d > 0.01) {
          const lado = d < z.raio ? -1 : 1, f = (7 - borda) * 0.3;
          u.x += ((u.x - z.x) / d) * f * lado; u.y += ((u.y - z.y) / d) * f * lado;
        }
        continue;
      }
      // a muralha é um obstáculo macio: quem chega perto escorrega para fora; quem está dentro queima
      const s = distSegmento(u.x, u.y, z.x1, z.y1, z.x2, z.y2);
      if (s.d >= 10) continue;
      if (tique && s.d <= 5) ferir(m, u, z.tique, m.heroi, { sutil: true, elemento: "fogo" });
      let nx = u.x - s.qx, ny = u.y - s.qy, n = Math.hypot(nx, ny);
      if (n < 0.01) { nx = -(z.y2 - z.y1); ny = z.x2 - z.x1; n = Math.hypot(nx, ny); if (u.id % 2) { nx = -nx; ny = -ny; } }
      const f = (10 - s.d) * 0.22;
      u.x += (nx / n) * f;
      u.y += (ny / n) * f;
    }
    if (z.t > 0) fica.push(z);
  }
  m.zonas = fica;
}

// ------------------------------------------------------------------------------------------------ movimento e corpos
function mover(m, dt) {
  const atrito = Math.exp(-ATRITO_EMPURRAO * dt), h = m.heroi;
  for (const u of m.unidades) {
    if (u.morto) continue;
    u.px = u.x; u.py = u.y;
    if (u !== h && u.congelado > 0) continue;
    u.x += (u.vx + u.kx) * dt;
    u.y += (u.vy + u.ky) * dt;
    u.kx *= atrito; u.ky *= atrito;
    if (Math.abs(u.kx) < 0.5) u.kx = 0;
    if (Math.abs(u.ky) < 0.5) u.ky = 0;
    u.passo += Math.hypot(u.vx, u.vy) * dt;
  }
}

// A separação dos corpos. A regra deliberada do herói: os aliados abrem caminho (ele não perde velocidade por eles);
// os inimigos são corpo sólido (o herói empurra, mas pesa como 2,5 soldados, e anda mais devagar a cada um encostado:
// atravessa uma linha fina devagar, apanhando, mas não a multidão inteira; para isso existe a Investida).
let cabeca = new Int32Array(0), proximo = new Int32Array(0);
function separar(m) {
  const us = m.unidades, n = us.length, h = m.heroi;
  const cols = Math.ceil(CAMPO.largura / CELULA) + 2, lins = Math.ceil(CAMPO.altura / CELULA) + 2;
  if (cabeca.length !== cols * lins) cabeca = new Int32Array(cols * lins);
  if (proximo.length < n) proximo = new Int32Array(n * 2);
  cabeca.fill(-1);
  const celula = (u) => (Math.max(0, Math.min(lins - 1, Math.floor(u.y / CELULA) + 1)) * cols) +
    Math.max(0, Math.min(cols - 1, Math.floor(u.x / CELULA) + 1));
  for (let i = 0; i < n; i++) {
    if (us[i].morto) continue;
    const c = celula(us[i]);
    proximo[i] = cabeca[c];
    cabeca[c] = i;
  }
  h.contato = 0;
  const heroiSolto = h.acao && h.acao.fase === "voo";   // no ar ou na investida, o herói passa
  for (let i = 0; i < n; i++) {
    const u = us[i];
    if (u.morto) continue;
    const cx = Math.max(0, Math.min(cols - 1, Math.floor(u.x / CELULA) + 1));
    const cy = Math.max(0, Math.min(lins - 1, Math.floor(u.y / CELULA) + 1));
    for (let oy = -1; oy <= 1; oy++) {
      const yy = cy + oy;
      if (yy < 0 || yy >= lins) continue;
      for (let ox = -1; ox <= 1; ox++) {
        const xx = cx + ox;
        if (xx < 0 || xx >= cols) continue;
        for (let j = cabeca[yy * cols + xx]; j !== -1; j = proximo[j]) {
          if (j <= i) continue;
          const v = us[j];
          if (v.morto) continue;
          const comHeroi = u === h || v === h;
          if (comHeroi && heroiSolto) continue;
          let dx = v.x - u.x, dy = v.y - u.y;
          // um vão maior entre lados diferentes: as duas linhas se encostam sem se misturar
          const min = u.raio + v.raio + (u.lado === v.lado ? 0.4 : 1.6);
          let d2 = dx * dx + dy * dy;
          if (d2 >= min * min) continue;
          let d = Math.sqrt(d2);
          if (d < 0.01) { const a = ((u.id * 7 + v.id * 13) % 360) * GRAU; dx = Math.cos(a); dy = Math.sin(a); d = 1; d2 = 1; }
          const nx = dx / d, ny = dy / d, ov = min - Math.min(d, min);
          let wu, wv;
          if (comHeroi && u.lado === v.lado) { wu = u === h ? 0 : 1; wv = 1 - wu; }
          else {
            const mu = u === h ? 2.5 : u.massa, mv = v === h ? 2.5 : v.massa;
            wu = mv / (mu + mv); wv = mu / (mu + mv);
            if (comHeroi) h.contato++;
          }
          u.x -= nx * ov * wu; u.y -= ny * ov * wu;
          v.x += nx * ov * wv; v.y += ny * ov * wv;
        }
      }
    }
  }
  const g = CAMPO.margem;
  for (const u of us) {
    if (u.morto || u.fugindo) continue;
    u.x = Math.max(g, Math.min(CAMPO.largura - g, u.x));
    u.y = Math.max(g, Math.min(CAMPO.altura - g, u.y));
  }
}

function limpar(m) {
  m.unidades = m.unidades.filter((u) => !u.morto && !u.saiu || u === m.heroi && !u.saiu);
  const l0 = [], l1 = [], slots = {};
  let s0x = 0, s0y = 0, s1x = 0, s1y = 0, k0 = 0, k1 = 0;
  for (const u of m.unidades) {
    if (u.morto) continue;
    if (u.lado === 0) {
      l0.push(u);
      if (u !== m.heroi) {
        // a posição de cada um no anel é contada dentro do grupo que tem a mesma ordem
        const o = u.ordem || m.ordem, chave = `${o.tipo}:${Math.round(o.x)}:${Math.round(o.y)}:${u.def.papel}`;
        u.slot = slots[chave] = (slots[chave] ?? -1) + 1;
        s0x += u.x; s0y += u.y; k0++;
      }
    } else { l1.push(u); s1x += u.x; s1y += u.y; k1++; }
  }
  if (m.selecao) for (const id of m.selecao) if (!l0.some((u) => u.id === id)) m.selecao.delete(id);
  m.lados = [l0, l1];
  m.centros = [k0 ? { x: s0x / k0, y: s0y / k0 } : m.heroi.morto ? null : { x: m.heroi.x, y: m.heroi.y },
    k1 ? { x: s1x / k1, y: s1y / k1 } : null];
}

function verificarFim(m) {
  if (m.fimEm) {
    if (m.t >= m.fimEm || m.fase === "fuga" && !m.lados[1].length) {
      m.fase = "fim";
      m.eventos.push({ tipo: "fim", resultado: m.resultado });
      registrar(m, m.resultado === "vitoria" ? "Vitória." : "Derrota.");
    }
    return;
  }
  if (m.fase !== "luta" || !m.reforco.chegou) return;
  if (m.lider && !m.lider.morto) return;   // enquanto o líder estiver de pé, a tropa dele não foge
  if (m.lados[1].length <= Math.floor(m.stats.inimigos * BATALHA.fugaQuando)) {
    m.fase = "fuga";
    m.resultado = "vitoria";
    m.fimEm = m.t + BATALHA.fugaDura;
    for (const u of m.lados[1]) { u.fugindo = true; u.acao = null; }
    m.eventos.push({ tipo: "fuga" });
    registrar(m, "Os inimigos que restam fogem.");
  }
}

// ------------------------------------------------------------------------------------------------ ordens
/**
 * Uma ordem: vale para a seleção, se houver alguém selecionado; sem seleção, para o exército inteiro. Quem não recebeu
 * a ordem mantém a sua. Devolve quantos a receberam.
 */
export function ordenar(m, tipo, x, y) {
  if (!ORDENS[tipo]) return 0;
  const o = { tipo, x: x ?? m.heroi.x, y: y ?? m.heroi.y };
  const sel = m.selecao && m.selecao.size;
  const alvos = m.lados[0].filter((u) => u !== m.heroi && (!sel || m.selecao.has(u.id)));
  for (const u of alvos) {
    u.ordem = o;
    u.reavaliar = 0;
    if (u.alvo && !alvoValido(m, u, u.alvo)) u.alvo = null;
  }
  if (!sel) m.ordem = o;
  m.eventos.push({ tipo: "ordem", ordem: tipo, x: o.x, y: o.y, n: alvos.length, selecao: !!sel, ids: alvos.map((u) => u.id) });
  registrar(m, `Ordem: ${ORDENS[tipo].nome} (${sel ? `${alvos.length} selecionados` : "todo o exército"}).`);
  return alvos.length;
}

/** Seleciona tropas aliadas (nunca o herói). `ids` vazio limpa; `somar` acrescenta à seleção atual. */
export function selecionar(m, ids, somar = false) {
  if (!somar) m.selecao.clear();
  const vivos = new Set(m.lados[0].filter((u) => u !== m.heroi).map((u) => u.id));
  for (const id of ids) if (vivos.has(id)) m.selecao.add(id);
  return m.selecao.size;
}

/** As tropas aliadas de um tipo ("soldado", "arqueiro"), ou todas com `null`. */
export function tropasDoTipo(m, tipo) {
  return m.lados[0].filter((u) => u !== m.heroi && (!tipo || u.tipo === tipo)).map((u) => u.id);
}

/** O resumo de agora, para a tela e o registro. */
export function resumo(m) {
  const h = m.heroi;
  const inimigosVivos = m.lados[1].length;
  return { ...m.stats, t: m.t, fase: m.fase, resultado: m.resultado, aliadosVivos: m.lados[0].length - (h.morto ? 0 : 1),
    inimigosVivos, vida: Math.max(0, h.vida), recurso: h.recurso, encontro: m.encontro,
    inimigosPorVir: Math.max(0, m.stats.inimigos - inimigosVivos - m.stats.abatesHeroi - m.stats.abatesAliados - m.stats.fugiram) };
}
