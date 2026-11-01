// PROTÓTIPO tático por turnos (nada no jogo): as regras, sem DOM (rodam no navegador e no Node). A tela e a IA só
// chamam estas funções; a prévia de uma ação é a própria ação aplicada numa cópia da luta (prever), então o número
// mostrado antes é o que acontece depois.
//
// Geometria: casas quadradas, vizinhança de 4 (na vista em losango, as quatro diagonais da tela); distância em casas
// (|dx| + |dy|), o "losango" de alcance de Dofus. Linha de visão: o segmento entre os centros das casas; bloqueiam os
// pilares, os barris e os combatentes no meio (não quem lança nem o alvo). Quando o segmento passa exatamente por um
// canto, só bloqueia se as duas casas do canto bloquearem (a regra permissiva).
import { REGRAS, ESTADOS, HABILIDADES, TALENTOS, CLASSES, COMPANHEIROS, INIMIGOS, ARENAS, ENCONTROS, MAX_TALENTOS } from "./conteudo.js";

export const VIZ = [[1, 0], [-1, 0], [0, 1], [0, -1]];
const chave = (x, y) => `${x},${y}`;
export const dist = (ax, ay, bx, by) => Math.abs(ax - bx) + Math.abs(ay - by);
const sinal = (v) => (v > 0 ? 1 : v < 0 ? -1 : 0);
const RUINS = Object.entries(ESTADOS).filter(([, e]) => e.ruim).map(([id]) => id);

// ------------------------------------------------------------------------------------------------ criação
/** O kit montado: as habilidades escolhidas, cópias com os números depois dos talentos. */
export function montarKit(dono, ids, talentos = []) {
  const kit = {};
  for (const id of ids) kit[id] = structuredClone({ ...HABILIDADES[dono][id], id, texto: undefined });
  for (const k of Object.values(kit)) {
    k.colisao = REGRAS.colisao * (talentos.includes("impacto") ? 2 : 1);
    k.fogoChao = REGRAS.fogoChao;
    if (k.esp === "armadilha") k.maxArmadilhas = 1;
  }
  for (const t of talentos) { const d = TALENTOS[dono] && TALENTOS[dono][t]; if (d && d.mod) d.mod(kit); }
  return kit;
}

/** A descrição de uma habilidade do kit montado (o texto mora em conteudo.js; os números vêm do kit). */
export function descricao(dono, k) { return HABILIDADES[dono][k.id].texto(k); }

/** Os talentos que valem para um kit: no máximo MAX_TALENTOS, e só os que têm a habilidade pedida. */
export function talentosValidos(classe, kitIds, talentos) {
  return talentos.filter((t) => TALENTOS[classe][t] && (!TALENTOS[classe][t].requer || kitIds.includes(TALENTOS[classe][t].requer))).slice(0, MAX_TALENTOS);
}

function combatente(id, def, lado, x, y, dono, kitIds, talentos = []) {
  return {
    id, nome: def.nome, dono, lado, x, y, modelo: def.modelo, papel: def.papel || null,
    pv: def.pv, pvMax: def.pv, paMax: def.pa, pmMax: def.pm, pa: def.pa, pm: def.pm, ini: def.ini,
    pesado: !!def.pesado, agil: !!def.agil, vivo: true, talentos, kit: montarKit(dono, kitIds, talentos),
    estados: [], cds: {}, usosTurno: {}, usosAlvo: {}, embalo: false, foco: null,
  };
}

/** Uma luta nova. `heroi`: { classe, kit: [ids], talentos: [ids] }. */
export function criarLuta({ heroi, encontro = "aberto" }) {
  const enc = ENCONTROS[encontro], arena = ARENAS[enc.arena];
  const linhas = arena.mapa, h = linhas.length, w = Math.max(...linhas.map((l) => l.length));
  const celulas = [], inicioA = [], inicioE = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    let c = linhas[y][x] || " ";
    if (c === "a") { inicioA.push([x, y]); c = "."; }
    if (c === "e") { inicioE.push([x, y]); c = "."; }
    celulas.push(c);
  }
  const m = { w, h, celulas, unidades: [], ordem: [], vez: 0, rodada: 1, chao: {}, armadilhas: [], preparos: [],
    eventos: [], registro: [], fim: null, encontro, proxId: 1 };
  const cls = CLASSES[heroi.classe];
  const tal = talentosValidos(heroi.classe, heroi.kit, heroi.talentos || []);
  const aliados = [
    combatente("heroi", cls, 0, ...inicioA[0], heroi.classe, heroi.kit, tal),
    combatente("morel", COMPANHEIROS.morel, 0, ...inicioA[1], "morel", COMPANHEIROS.morel.kit),
    combatente("odette", COMPANHEIROS.odette, 0, ...inicioA[2], "odette", COMPANHEIROS.odette.kit),
  ];
  aliados[0].papel = { guerreiro: "perto", mago: "area", arqueiro: "longe" }[heroi.classe];
  aliados[0].nome = cls.nome;
  aliados[1].papel = "pesado"; aliados[2].papel = "apoio";
  const contagem = {};
  const inimigos = enc.inimigos.map((tipo, i) => {
    const def = INIMIGOS[tipo];
    contagem[tipo] = (contagem[tipo] || 0) + 1;
    const u = combatente(`${tipo}${contagem[tipo]}`, def, 1, ...inicioE[i], tipo, def.kit);
    if (enc.inimigos.filter((t) => t === tipo).length > 1) u.nome = `${def.nome} ${contagem[tipo]}`;
    return u;
  });
  m.unidades = [...aliados, ...inimigos];
  // a ordem: cada lado pela iniciativa, alternando aliado e inimigo (como em Dofus); fixa até o fim da luta
  const porIni = (a, b) => b.ini - a.ini || a.id.localeCompare(b.id);
  const A = [...aliados].sort(porIni), E = [...inimigos].sort(porIni);
  const comecaA = A[0].ini >= E[0].ini;
  for (let i = 0; i < Math.max(A.length, E.length); i++) {
    const par = comecaA ? [A[i], E[i]] : [E[i], A[i]];
    for (const u of par) if (u) m.ordem.push(u.id);
  }
  iniciarVez(m);
  return m;
}

// ------------------------------------------------------------------------------------------------ consultas
export const unidade = (m, id) => m.unidades.find((u) => u.id === id);
export const atual = (m) => unidade(m, m.ordem[m.vez]);
export const celula = (m, x, y) => (x < 0 || y < 0 || x >= m.w || y >= m.h ? " " : m.celulas[y * m.w + x]);
export const naArena = (m, x, y) => celula(m, x, y) !== " ";
export const passavel = (m, x, y) => celula(m, x, y) === ".";
export const tapaVisao = (m, x, y) => { const c = celula(m, x, y); return c === "#" || c === "o"; };
export const unidadeEm = (m, x, y) => m.unidades.find((u) => u.vivo && u.x === x && u.y === y) || null;
export const livre = (m, x, y) => passavel(m, x, y) && !unidadeEm(m, x, y);
export const temEstado = (u, e) => u.estados.find((s) => s.e === e) || null;
export const tem = (u, t) => u.talentos.includes(t);
export const inimigosDe = (m, u) => m.unidades.filter((w) => w.vivo && w.lado !== u.lado);
export const aliadosDe = (m, u) => m.unidades.filter((w) => w.vivo && w.lado === u.lado);

/** Linha de visão entre duas casas (a casa de origem e a de destino não bloqueiam). */
export function visao(m, ax, ay, bx, by) {
  if (ax === bx && ay === by) return true;
  const bloqueia = (x, y) => !(x === ax && y === ay) && !(x === bx && y === by) && (tapaVisao(m, x, y) || !!unidadeEm(m, x, y));
  // percorre as casas cortadas pelo segmento entre os centros (Amanatides e Woo)
  const dx = bx - ax, dy = by - ay, sx = sinal(dx), sy = sinal(dy);
  const tdx = dx ? 1 / Math.abs(dx) : Infinity, tdy = dy ? 1 / Math.abs(dy) : Infinity;
  let tx = dx ? tdx / 2 : Infinity, ty = dy ? tdy / 2 : Infinity, x = ax, y = ay;
  while (x !== bx || y !== by) {
    if (Math.abs(tx - ty) < 1e-9) {
      // pelo canto: bloqueia só se as duas casas do canto bloquearem
      if (bloqueia(x + sx, y) && bloqueia(x, y + sy)) return false;
      x += sx; y += sy; tx += tdx; ty += tdy;
    } else if (tx < ty) { x += sx; tx += tdx; } else { y += sy; ty += tdy; }
    if ((x !== bx || y !== by) && bloqueia(x, y)) return false;
  }
  return true;
}

/** Os PM a mais para sair da casa (x, y): 1 por inimigo vizinho (2 se for pesado ou tiver Muralha Viva). */
export function custoSaida(m, u, x, y) {
  if (u.agil || tem(u, "leveza")) return 0;
  let c = 0;
  for (const w of inimigosDe(m, u)) if (dist(w.x, w.y, x, y) === 1) c += w.pesado || tem(w, "muralhaViva") ? 2 : REGRAS.bloqueio;
  return c;
}

/** As casas alcançáveis com os PM de agora: Map chave -> { x, y, custo, caminho } (Dijkstra, com o bloqueio). */
export function alcancaveis(m, u, pm = u.pm) {
  const res = new Map(), fila = [{ x: u.x, y: u.y, custo: 0, caminho: [] }];
  res.set(chave(u.x, u.y), fila[0]);
  while (fila.length) {
    fila.sort((a, b) => a.custo - b.custo);
    const c = fila.shift();
    if (res.get(chave(c.x, c.y)) !== c) continue;
    // as armadilhas inimigas não entram no cálculo (quem anda não as vê); mover() para na primeira
    const sai = custoSaida(m, u, c.x, c.y);
    for (const [dx, dy] of VIZ) {
      const nx = c.x + dx, ny = c.y + dy;
      if (!livre(m, nx, ny)) continue;
      const custo = c.custo + 1 + sai;
      if (custo > pm) continue;
      const k = chave(nx, ny), ant = res.get(k);
      if (ant && ant.custo <= custo) continue;
      const n = { x: nx, y: ny, custo, caminho: [...c.caminho, [nx, ny]] };
      res.set(k, n);
      fila.push(n);
    }
  }
  return res;
}

/** O alcance de agora (Ofuscado tira 2, Olho de Águia soma 2; só nas habilidades de alcance maior que 1). */
export function alcanceDe(u, k) {
  let [a, b] = k.alcance;
  if (b > 1) {
    if (temEstado(u, "olhoAguia")) b += 2;
    if (temEstado(u, "ofuscado")) b = Math.max(a, Math.max(1, b - 2));
  }
  return [a, b];
}

/** Pode lançar agora (PA, recarga, vezes por turno)? { ok, motivo }. */
export function podeLancar(m, u, id) {
  const k = u.kit[id];
  if (!k) return { ok: false, motivo: "Fora do kit" };
  if (m.fim) return { ok: false, motivo: "A luta acabou" };
  if ((u.cds[id] || 0) > 0) return { ok: false, motivo: `Recarga: ${u.cds[id]} ${u.cds[id] === 1 ? "turno" : "turnos"}` };
  if (k.pa > u.pa) return { ok: false, motivo: `Faltam ${k.pa - u.pa} PA` };
  if (k.porTurno && (u.usosTurno[id] || 0) >= k.porTurno) return { ok: false, motivo: `Já usada ${k.porTurno}× neste turno` };
  if (k.esp === "recuo" && !destinoRecuo(m, u, k)) return { ok: false, motivo: "Sem espaço para saltar" };
  return { ok: true };
}

/** As casas de destino válidas de uma habilidade, a partir da posição de agora. */
export function alvosValidos(m, u, id) {
  const k = u.kit[id], res = [];
  if (!podeLancar(m, u, id).ok) return res;
  if (k.alvo === "si") return [[u.x, u.y]];
  const [a, b] = alcanceDe(u, k);
  for (let y = 0; y < m.h; y++) for (let x = 0; x < m.w; x++) {
    if (!naArena(m, x, y)) continue;
    const d = dist(u.x, u.y, x, y);
    if (d < a || d > b) continue;
    if (k.linha && x !== u.x && y !== u.y) continue;
    if (alvoValido(m, u, k, x, y)) res.push([x, y]);
  }
  return res;
}

function alvoValido(m, u, k, x, y) {
  const w = unidadeEm(m, x, y);
  if (k.alvo === "inimigo" && (!w || w.lado === u.lado)) return false;
  if (k.alvo === "aliado" && (!w || w.lado !== u.lado || (k.soOutro && w === u))) return false;
  if (k.alvo === "livre" && (!livre(m, x, y) || m.armadilhas.some((t) => t.x === x && t.y === y))) return false;
  if (k.visao !== false && !visao(m, u.x, u.y, x, y)) return false;
  if (k.porAlvo && w && (u.usosAlvo[`${k.id}:${w.id}`] || 0) >= k.porAlvo) return false;
  if (k.esp === "investida") {
    const sx = sinal(x - u.x), sy = sinal(y - u.y);
    for (let i = 1; i < dist(u.x, u.y, x, y); i++) if (!livre(m, u.x + sx * i, u.y + sy * i)) return false;
  }
  return true;
}

/** As casas atingidas por uma habilidade lançada em (tx, ty). */
export function areaDe(m, u, k, tx, ty) {
  const a = k.area || { f: "alvo" }, cel = [];
  const add = (x, y) => { if (naArena(m, x, y)) cel.push([x, y]); };
  if (a.f === "alvo") add(tx, ty);
  else if (a.f === "cruz") {
    add(tx, ty);
    for (const [dx, dy] of VIZ) for (let i = 1; i <= a.r; i++) add(tx + dx * i, ty + dy * i);
  } else if (a.f === "circulo") {
    for (let y = ty - a.r; y <= ty + a.r; y++) for (let x = tx - a.r; x <= tx + a.r; x++) if (dist(x, y, tx, ty) <= a.r) add(x, y);
  } else if (a.f === "raio") {
    // em linha reta a partir de quem lança, na direção da casa escolhida, até `r` casas; para no pilar
    const sx = sinal(tx - u.x), sy = sinal(ty - u.y);
    for (let i = 1; i <= a.r; i++) {
      const x = u.x + sx * i, y = u.y + sy * i;
      if (!naArena(m, x, y) || tapaVisao(m, x, y)) break;
      add(x, y);
    }
  } else if (a.f === "perp") {
    // atravessada à linha de mira: a casa e `r` casas para cada lado
    const dx = tx - u.x, dy = ty - u.y, horiz = Math.abs(dx) >= Math.abs(dy);
    add(tx, ty);
    for (let i = 1; i <= a.r; i++) {
      if (horiz) { add(tx, ty + i); add(tx, ty - i); } else { add(tx + i, ty); add(tx - i, ty); }
    }
  }
  // quem lança uma área em volta de si não se atinge
  return k.alvo === "si" && a.f !== "alvo" ? cel.filter(([x, y]) => x !== u.x || y !== u.y) : cel;
}

// ------------------------------------------------------------------------------------------------ efeitos
function evento(m, e) { m.eventos.push(e); }
function registrar(m, texto) { m.registro.push({ rodada: m.rodada, texto }); }

function aplicarEstado(m, alvo, e, turnos, v, fonte) {
  const ant = temEstado(alvo, e);
  if (ant) { ant.turnos = Math.max(ant.turnos, turnos); if (v != null) ant.v = Math.max(ant.v || 0, v); ant.fonte = fonte; return; }
  alvo.estados.push({ e, turnos, v: v ?? null, fonte });
  evento(m, { t: "estado", id: alvo.id, e });
}

/** Dano com as regras (Inspirado, Marcado, Emboscada, Estilhaçar, Escudo Erguido, Cobrir, as barreiras). */
export function ferir(m, fonte, alvo, v, el = "fisico", o = {}) {
  if (!alvo.vivo || v <= 0) return 0;
  if (fonte && tem(fonte, "seletivas") && el === "fogo" && fonte.lado === alvo.lado) return 0;
  let dano = v;
  if (!o.bruto) {
    if (fonte && temEstado(fonte, "inspirado")) dano *= 1 + REGRAS.inspirado;
    if (temEstado(alvo, "marcado")) dano *= 1 + REGRAS.marcado;
    if (fonte && tem(fonte, "emboscada") && !aliadosDe(m, alvo).some((w) => w !== alvo && dist(w.x, w.y, alvo.x, alvo.y) === 1)) dano *= 1.25;
  }
  const gelo = temEstado(alvo, "congelado");
  if (gelo && (el === "fogo" || el === "raio") && fonte && tem(fonte, "estilhacar") && !o.bruto) dano += 8;
  if (gelo && el === "fogo") alvo.estados = alvo.estados.filter((s) => s !== gelo);
  else if (gelo && el === "raio" && fonte && tem(fonte, "estilhacar")) alvo.estados = alvo.estados.filter((s) => s !== gelo);
  if (temEstado(alvo, "protegido")) dano *= REGRAS.protegido;
  dano = Math.round(dano);
  const cob = temEstado(alvo, "coberto"), morel = cob && unidade(m, cob.fonte);
  if (cob && morel && morel.vivo && morel !== alvo) {
    const parte = Math.round(dano * REGRAS.coberto);
    dano -= parte;
    ferir(m, fonte, morel, parte, el, { bruto: true, coberto: true });
  }
  for (const id of ["abencoado", "barreira"]) {
    const s = temEstado(alvo, id);
    if (!s || dano <= 0) continue;
    const absorve = Math.min(s.v, dano);
    s.v -= absorve; dano -= absorve;
    if (s.v <= 0) alvo.estados = alvo.estados.filter((x) => x !== s);
  }
  alvo.pv -= dano;
  evento(m, { t: "dano", id: alvo.id, v: dano, el });
  if (alvo.pv <= 0) morrer(m, alvo);
  return dano;
}

function curar(m, alvo, v) {
  const c = Math.min(v, alvo.pvMax - alvo.pv);
  alvo.pv += c;
  evento(m, { t: "cura", id: alvo.id, v: c });
  return c;
}

function morrer(m, u) {
  u.pv = 0; u.vivo = false;
  evento(m, { t: "morre", id: u.id, x: u.x, y: u.y });
  registrar(m, `${u.nome} caiu.`);
  m.preparos = m.preparos.filter((p) => p.dono !== u.id);
  verificarFim(m);
}

function verificarFim(m) {
  if (m.fim) return;
  if (!m.unidades.some((u) => u.vivo && u.lado === 1)) m.fim = "vitoria";
  else if (!m.unidades.some((u) => u.vivo && u.lado === 0)) m.fim = "derrota";
  if (m.fim) registrar(m, m.fim === "vitoria" ? "Vitória." : "Derrota.");
}

/** Entrar numa casa: o chão em chamas ou envenenado fere; a armadilha inimiga dispara (e para o movimento). */
function entrar(m, u, x, y) {
  u.x = x; u.y = y;
  const ch = m.chao[chave(x, y)];
  if (ch) danoDoChao(m, u, ch);
  if (!u.vivo) return true;
  const i = m.armadilhas.findIndex((a) => a.x === x && a.y === y && a.lado !== u.lado);
  if (i >= 0) {
    const a = m.armadilhas[i], dono = unidade(m, a.dono);
    m.armadilhas.splice(i, 1);
    evento(m, { t: "armadilha", x, y });
    registrar(m, `${u.nome} pisou numa armadilha.`);
    for (const e of a.efeitos) aplicarEfeito(m, dono, u, e, { origem: [x, y], k: a.k });
    return true;
  }
  return false;
}

function danoDoChao(m, u, ch) {
  const dono = unidade(m, ch.dono);
  if (ch.e === "fogo") ferir(m, dono, u, REGRAS.fogoChao, "fogo", { bruto: true, chao: true });
  else if (ch.e === "veneno") ferir(m, dono, u, REGRAS.venenoChao, "veneno", { bruto: true, chao: true });
}

/** Andar por um caminho de alcancaveis(): gasta os PM, aplica o chão, para na armadilha. */
export function mover(m, u, x, y) {
  const r = alcancaveis(m, u).get(chave(x, y));
  if (!r || !r.caminho.length) return false;
  const feito = [];
  let gasto = 0, px = u.x, py = u.y;
  for (const [nx, ny] of r.caminho) {
    gasto += 1 + custoSaida(m, u, px, py);
    feito.push([nx, ny]);
    const parou = entrar(m, u, nx, ny);
    px = nx; py = ny;
    if (parou || !u.vivo) break;
  }
  u.pm = Math.max(0, u.pm - gasto);
  evento(m, { t: "andar", id: u.id, caminho: feito });
  return true;
}

/** Empurra `alvo` `n` casas para longe de (ox, oy); bater em algo fere pelas casas que faltaram. */
function empurrar(m, fonte, alvo, n, ox, oy, k) {
  let dx = alvo.x - ox, dy = alvo.y - oy;
  if (!dx && !dy) { dx = alvo.x - fonte.x; dy = alvo.y - fonte.y; }
  let sx = sinal(dx), sy = sinal(dy);
  if (Math.abs(dx) !== Math.abs(dy)) { if (Math.abs(dx) > Math.abs(dy)) sy = 0; else sx = 0; }
  if (!sx && !sy) return;
  const de = [alvo.x, alvo.y];
  for (let i = 0; i < n; i++) {
    const nx = alvo.x + sx, ny = alvo.y + sy;
    if (!livre(m, nx, ny)) {
      const falta = n - i, dano = falta * (k ? k.colisao : REGRAS.colisao);
      const outro = unidadeEm(m, nx, ny);
      evento(m, { t: "empurra", id: alvo.id, de, para: [alvo.x, alvo.y], bateu: [nx, ny] });
      ferir(m, fonte, alvo, dano, "colisao", { bruto: true });
      if (outro) ferir(m, fonte, outro, Math.floor(dano / 2), "colisao", { bruto: true });
      return;
    }
    const parou = entrar(m, alvo, nx, ny);
    if (parou || !alvo.vivo) break;
  }
  evento(m, { t: "empurra", id: alvo.id, de, para: [alvo.x, alvo.y] });
}

/** Puxa `alvo` até `n` casas na direção de quem puxa, parando vizinho dele ou no primeiro obstáculo. */
function puxar(m, fonte, alvo, n) {
  const sx = sinal(fonte.x - alvo.x), sy = sinal(fonte.y - alvo.y);
  if (sx && sy) return;
  const de = [alvo.x, alvo.y];
  for (let i = 0; i < n; i++) {
    const nx = alvo.x + sx, ny = alvo.y + sy;
    if (!livre(m, nx, ny)) break;
    const parou = entrar(m, alvo, nx, ny);
    if (parou || !alvo.vivo) break;
  }
  evento(m, { t: "empurra", id: alvo.id, de, para: [alvo.x, alvo.y] });
}

function porChao(m, fonte, x, y, e, turnos) {
  if (celula(m, x, y) === "o" && e === "fogo") return explodirBarril(m, fonte, x, y);
  if (!passavel(m, x, y)) return;
  m.chao[chave(x, y)] = { e, ate: m.rodada + turnos, dono: fonte.id };
}

/** O barril de óleo: dano de fogo o explode (8 na cruz em volta, chão em chamas por 2 rodadas); encadeia. */
function explodirBarril(m, fonte, x, y) {
  if (celula(m, x, y) !== "o") return;
  m.celulas[y * m.w + x] = ".";
  evento(m, { t: "explode", x, y });
  registrar(m, "Um barril de óleo explodiu.");
  const cel = [[x, y], ...VIZ.map(([dx, dy]) => [x + dx, y + dy])];
  for (const [cx, cy] of cel) {
    if (celula(m, cx, cy) === "o") { explodirBarril(m, fonte, cx, cy); continue; }
    const w = unidadeEm(m, cx, cy);
    if (w) ferir(m, fonte, w, 8, "fogo", { bruto: true });
    if (passavel(m, cx, cy)) m.chao[chave(cx, cy)] = { e: "fogo", ate: m.rodada + 2, dono: fonte.id };
  }
}

function aplicarEfeito(m, u, alvo, e, ctx) {
  if (!alvo || !alvo.vivo) return;
  if (e.t === "dano") {
    let v = e.v;
    if (ctx.k && ctx.k.esp === "matilha" && aliadosDe(m, u).some((w) => w !== u && dist(w.x, w.y, alvo.x, alvo.y) === 1)) v += 3;
    if (ctx.k && ctx.k.porDistancia) v += Math.max(0, dist(u.x, u.y, alvo.x, alvo.y) - 4) * ctx.k.porDistancia;
    if (ctx.k && ctx.k.id === "golpe" && u.embalo) { v += 6; u.embalo = false; }
    if (ctx.queda) v = Math.max(1, v - ctx.queda);
    ferir(m, u, alvo, v, e.el || "fisico");
  } else if (e.t === "cura") curar(m, alvo, e.v);
  else if (e.t === "empurra") empurrar(m, u, alvo, e.n, ...(ctx.origem || [u.x, u.y]), ctx.k);
  else if (e.t === "puxa") puxar(m, u, alvo, e.n);
  else if (e.t === "estado") {
    if (ctx.k && ctx.k.soAliados && alvo.lado !== u.lado) return;
    aplicarEstado(m, alvo, e.e, e.turnos, e.v, u.id);
    if (ctx.k && ctx.k.marcaLento && e.e === "marcado") aplicarEstado(m, alvo, "lento", 1, 1, u.id);
  }
}

// ------------------------------------------------------------------------------------------------ lançar
/** Lança uma habilidade em (tx, ty). Retorna false se não puder (nada muda). */
export function lancar(m, u, id, tx, ty) {
  const k = u.kit[id];
  if (!k || u !== atual(m) || !alvosValidos(m, u, id).some(([x, y]) => x === tx && y === ty)) return false;
  u.pa -= k.pa;
  u.usosTurno[id] = (u.usosTurno[id] || 0) + 1;
  if (k.recarga) u.cds[id] = k.recarga;
  const alvoU = unidadeEm(m, tx, ty);
  if (alvoU && k.porAlvo) u.usosAlvo[`${id}:${alvoU.id}`] = (u.usosAlvo[`${id}:${alvoU.id}`] || 0) + 1;
  evento(m, { t: "lanca", id: u.id, hab: id, x: tx, y: ty });
  registrar(m, `${u.nome}: ${k.nome}.`);
  if (alvoU && alvoU.lado !== u.lado) u.foco = alvoU.id;
  const ctx = { k };

  switch (k.esp) {
    case "investida": {
      const sx = sinal(tx - u.x), sy = sinal(ty - u.y), d = dist(u.x, u.y, tx, ty);
      const de = [u.x, u.y];
      for (let i = 1; i < d; i++) { if (entrar(m, u, de[0] + sx * i, de[1] + sy * i) || !u.vivo) break; }
      evento(m, { t: "salto", id: u.id, de, para: [u.x, u.y] });
      if (u.vivo && dist(u.x, u.y, tx, ty) === 1) for (const e of k.efeitos) aplicarEfeito(m, u, alvoU, e, ctx);
      if (tem(u, "embalo")) u.embalo = true;
      break;
    }
    case "piscar": {
      evento(m, { t: "salto", id: u.id, de: [u.x, u.y], para: [tx, ty], piscar: true });
      entrar(m, u, tx, ty);
      break;
    }
    case "recuo": {
      const [x, y] = destinoRecuo(m, u, k);
      evento(m, { t: "salto", id: u.id, de: [u.x, u.y], para: [x, y] });
      entrar(m, u, x, y);
      break;
    }
    case "raios": {
      let alvo = alvoU, queda = 0;
      const atingidos = new Set();
      for (let i = 0; i <= k.saltos && alvo; i++) {
        atingidos.add(alvo.id);
        evento(m, { t: "raio", de: i ? null : [u.x, u.y], para: [alvo.x, alvo.y] });
        aplicarEfeito(m, u, alvo, k.efeitos[0], { ...ctx, queda });
        queda += 2;
        const de = alvo;
        alvo = inimigosDe(m, u).filter((w) => !atingidos.has(w.id) && dist(w.x, w.y, de.x, de.y) <= k.salto)
          .sort((a, b) => dist(a.x, a.y, de.x, de.y) - dist(b.x, b.y, de.x, de.y) || a.id.localeCompare(b.id))[0];
      }
      break;
    }
    case "perfurante": {
      const sx = sinal(tx - u.x), sy = sinal(ty - u.y), [, max] = alcanceDe(u, k);
      let n = 0;
      for (let i = 1; i <= max && n < k.atravessa; i++) {
        const x = u.x + sx * i, y = u.y + sy * i;
        if (!naArena(m, x, y) || tapaVisao(m, x, y)) break;
        const w = unidadeEm(m, x, y);
        if (w) { aplicarEfeito(m, u, w, k.efeitos[0], ctx); n++; }
      }
      evento(m, { t: "flecha", de: [u.x, u.y], para: [tx, ty] });
      break;
    }
    case "combustao": {
      for (const [x, y] of areaDe(m, u, k, tx, ty)) {
        const ch = m.chao[chave(x, y)];
        if (!ch || ch.e !== "fogo") continue;
        delete m.chao[chave(x, y)];
        evento(m, { t: "explode", x, y, pequeno: true });
        const w = unidadeEm(m, x, y);
        if (w) aplicarEfeito(m, u, w, k.efeitos[0], ctx);
      }
      break;
    }
    case "armadilha": {
      const minhas = m.armadilhas.filter((a) => a.dono === u.id);
      if (minhas.length >= k.maxArmadilhas) m.armadilhas.splice(m.armadilhas.indexOf(minhas[0]), 1);
      m.armadilhas.push({ x: tx, y: ty, dono: u.id, lado: u.lado, efeitos: k.efeitos, k });
      break;
    }
    case "provocar": {
      for (const [x, y] of areaDe(m, u, k, tx, ty)) {
        const w = unidadeEm(m, x, y);
        if (w && w.lado !== u.lado) aplicarEstado(m, w, "provocado", 1, null, u.id);
      }
      break;
    }
    case "escudo": {
      aplicarEstado(m, u, "protegido", 1, null, u.id);
      if (k.raioProtege) for (const w of aliadosDe(m, u)) if (w !== u && dist(w.x, w.y, u.x, u.y) <= k.raioProtege) aplicarEstado(m, w, "protegido", 1, null, u.id);
      break;
    }
    case "preparar": {
      m.preparos.push({ dono: u.id, celulas: areaDe(m, u, k, tx, ty), efeitos: k.efeitos, origem: [u.x, u.y], k });
      registrar(m, `${u.nome} prepara o ${k.nome}.`);
      break;
    }
    case "purificar": {
      alvoU.estados = alvoU.estados.filter((s) => !RUINS.includes(s.e));
      for (const e of k.efeitos) aplicarEfeito(m, u, alvoU, e, ctx);
      break;
    }
    default: {
      const cel = areaDe(m, u, k, tx, ty);
      const centro = k.alvo === "si" ? [u.x, u.y] : [tx, ty];
      const atingidos = cel.map(([x, y]) => unidadeEm(m, x, y)).filter(Boolean)
        .filter((w) => !(k.soInimigos && w.lado === u.lado))
        // quem está mais longe do centro primeiro: os empurrões não batem em quem ainda vai sair
        .sort((a, b) => dist(b.x, b.y, ...centro) - dist(a.x, a.y, ...centro) || a.id.localeCompare(b.id));
      let porAlvo = 0;
      for (const w of atingidos) {
        const origem = k.area && k.alvo !== "si" && (w.x !== tx || w.y !== ty) ? [tx, ty] : [u.x, u.y];
        for (const e of k.efeitos) if (e.t !== "chao") aplicarEfeito(m, u, w, e, { ...ctx, origem });
        if (w.lado !== u.lado) porAlvo++;
      }
      if (k.curaPorAlvo && porAlvo) curar(m, u, k.curaPorAlvo * porAlvo);
      for (const e of k.efeitos) if (e.t === "chao") for (const [x, y] of cel) porChao(m, u, x, y, e.e, e.turnos);
      // o fogo direto numa área também acende os barris dentro dela
      if (k.efeitos.some((e) => e.el === "fogo")) for (const [x, y] of cel) if (celula(m, x, y) === "o") explodirBarril(m, u, x, y);
    }
  }
  verificarFim(m);
  return true;
}

function destinoRecuo(m, u, k) {
  const ins = inimigosDe(m, u);
  if (!ins.length) return null;
  const perto = ins.sort((a, b) => dist(a.x, a.y, u.x, u.y) - dist(b.x, b.y, u.x, u.y))[0];
  let dx = u.x - perto.x, dy = u.y - perto.y;
  const opcoes = Math.abs(dx) >= Math.abs(dy) ? [[sinal(dx) || 1, 0], [0, sinal(dy) || 1], [0, -(sinal(dy) || 1)]] : [[0, sinal(dy) || 1], [sinal(dx) || 1, 0], [-(sinal(dx) || 1), 0]];
  for (const [sx, sy] of opcoes) {
    let x = u.x, y = u.y;
    for (let i = 0; i < k.distancia && livre(m, x + sx, y + sy); i++) { x += sx; y += sy; }
    if (x !== u.x || y !== u.y) return [x, y];
  }
  return null;
}

// ------------------------------------------------------------------------------------------------ a prévia
/**
 * A prévia de uma ação: a mesma ação numa cópia. Retorna, por combatente que muda, { id, dPv, de, para, morre,
 * estados (novos) }, e as casas que pegam fogo ou veneno.
 */
export function prever(m, id, hab, tx, ty, de = null) {
  const c = structuredClone(m);
  c.eventos = [];
  const u = unidade(c, id);
  if (de) { u.x = de[0]; u.y = de[1]; }
  if (!lancar(c, u, hab, tx, ty)) return null;
  const mud = [];
  for (const a of m.unidades) {
    const b = unidade(c, a.id);
    const novos = b.estados.filter((s) => !temEstado(a, s.e)).map((s) => s.e);
    const ax = a === unidade(m, id) && de ? de : [a.x, a.y];
    if (b.pv !== a.pv || b.x !== ax[0] || b.y !== ax[1] || novos.length || (a.vivo && !b.vivo))
      mud.push({ id: a.id, dPv: b.pv - a.pv, de: ax, para: [b.x, b.y], morre: a.vivo && !b.vivo, estados: novos });
  }
  const chao = Object.keys(c.chao).filter((key) => !m.chao[key]).map((key) => key.split(",").map(Number));
  const preparo = c.preparos.length > m.preparos.length ? c.preparos[c.preparos.length - 1].celulas : null;
  return { mud, chao, preparo, luta: c };
}

// ------------------------------------------------------------------------------------------------ a vez
/** O começo da vez de quem está na ordem: estados, recargas, golpes preparados, chão, PA e PM. */
export function iniciarVez(m) {
  const u = atual(m);
  u.usosTurno = {}; u.usosAlvo = {}; u.embalo = false;
  // os estados que contam no começo da vez de quem os carrega; o Coberto conta na vez de quem cobre (Morel)
  for (const s of u.estados) if (ESTADOS[s.e].ate === "inicio" && s.e !== "coberto") s.turnos--;
  u.estados = u.estados.filter((s) => s.turnos > 0);
  for (const w of m.unidades) {
    for (const s of w.estados) if (s.e === "coberto" && s.fonte === u.id) s.turnos--;
    w.estados = w.estados.filter((s) => s.turnos > 0);
  }
  for (const id of Object.keys(u.cds)) u.cds[id] = Math.max(0, u.cds[id] - 1);
  // o golpe preparado sai no começo da vez de quem preparou
  for (const p of m.preparos.filter((p) => p.dono === u.id)) {
    m.preparos.splice(m.preparos.indexOf(p), 1);
    evento(m, { t: "esmaga", id: u.id, celulas: p.celulas });
    registrar(m, `${u.nome}: o ${p.k.nome} cai.`);
    for (const [x, y] of p.celulas) {
      const w = unidadeEm(m, x, y);
      if (w && w !== u) for (const e of p.efeitos) aplicarEfeito(m, u, w, e, { k: p.k, origem: p.origem });
    }
  }
  u.pa = u.paMax;
  let pm = u.pmMax;
  const lento = temEstado(u, "lento");
  if (lento) pm -= lento.v || 1;
  if (temEstado(u, "desequilibrado")) pm -= 2;
  if (temEstado(u, "congelado")) pm -= 2;
  if (temEstado(u, "imobilizado")) pm = 0;
  u.pm = Math.max(0, pm);
  const ch = m.chao[chave(u.x, u.y)];
  if (ch && u.vivo) danoDoChao(m, u, ch);
  evento(m, { t: "vez", id: u.id });
  if (!u.vivo && !m.fim) encerrarVez(m);
}

/** Encerra a vez: os estados que contam no fim; passa para o próximo vivo. */
export function encerrarVez(m) {
  if (m.fim) return;
  const u = atual(m);
  if (u.vivo) {
    for (const s of u.estados) if (ESTADOS[s.e].ate === "fim") s.turnos--;
    u.estados = u.estados.filter((s) => s.turnos > 0);
  }
  for (let i = 0; i < m.ordem.length; i++) {
    m.vez = (m.vez + 1) % m.ordem.length;
    if (m.vez === 0) {
      m.rodada++;
      for (const [key, ch] of Object.entries(m.chao)) if (m.rodada >= ch.ate) delete m.chao[key];
    }
    if (atual(m).vivo) break;
  }
  iniciarVez(m);
}
