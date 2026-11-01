// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 7: a geometria das construções e a navegação. Sem DOM. Antes no
// campo6.js (que reexporta daqui o que sim.js e os testes usam).
//
// Quatro problemas diferentes, resolvidos em lugares diferentes:
// 1. Achar a rota pelo cenário (`rumo`): com a linha livre, reto; senão, o caminho mais curto pelo grafo dos cantos
//    das construções, guardado inteiro e seguido canto a canto (pulando os que já se veem).
// 2. Contornar as outras unidades: a separação dos corpos (sim.separar) e, quando alguém não sai do lugar no meio da
//    multidão, um desvio curto para o lado (`vigiar`).
// 3. Alcançar uma posição útil (`posicaoUtil`): quem atira ou ajuda procura um ponto com visão do alvo, no alcance,
//    que se alcança por um caminho curto e longe do perigo; quem luta perto escolhe o alvo pelo caminho, não pela
//    linha reta através de uma parede (`custoAte`).
// 4. Reconhecer o inacessível: destino fechado (sem canto visível), ou dois segundos sem sair do lugar apesar dos
//    recálculos, viram `u.inacessivel` por 2,5 s; quem decide o alvo ou a posição evita aquele ponto.
// Ninguém atravessa construção nem é teleportado: o que faltava era a rota, não um atalho.
import { CENARIOS, CAMPO } from "./conteudo.js";

let M = null;    // o mundo do passo de agora (andarPara e pontoNoAlcance não recebem o mundo)
export function mundoNav(m) { M = m; }
export function mundoDaNav() { return M; }

export const FOLGA = 6;       // quanto os retângulos crescem nas contas de caminho (o maior corpo comum tem raio 6,5)
// A folga de quem está andando: um pouco menor que o corpo. A separação deixa o centro exatamente a `raio` da parede;
// com a folga igual ao raio, a linha que sai dali já "tocava" o retângulo crescido e nenhum canto era visível (era
// isso que prendia Odette na muralha: sem canto visível, ela ia reto contra a pedra).
export const folgaDe = (u) => Math.max(0, Math.min(FOLGA - 1, u.raio) - 1.5);

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

// ------------------------------------------------------------------------------------------------ o grafo
/** Prepara o cenário do mundo: as construções e o grafo dos cantos com todas as distâncias (Floyd-Warshall). */
export function prepararCenario(m, nome) {
  const c = CENARIOS[nome] || CENARIOS.aberto;
  // o muro baixo e o tronco das árvores barram a passagem; flechas, magias e áreas passam por cima (a copa é alta)
  const obs = c.obstaculos.map((o) => ({ ...o, tiro: o.tipo !== "muro" && o.tipo !== "arvore" }));
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

function nosVisiveis(m, x, y, f) {
  const r = [], nos = m.cenario.nos;
  for (let i = 0; i < nos.length; i++) if (!bloqueado(m, x, y, nos[i].x, nos[i].y, false, f)) r.push(i);
  return r;
}
// os cantos que uma unidade vê, guardados enquanto ela não anda 6 px (nem passa 0,3 s)
function visDe(m, u, f) {
  const v = u.visNos;
  if (v && m.t - v.t < 0.3 && Math.abs(v.x - u.x) + Math.abs(v.y - u.y) < 6) return v.l;
  u.visNos = { t: m.t, x: u.x, y: u.y, l: nosVisiveis(m, u.x, u.y, f) };
  return u.visNos.l;
}

// O menor caminho entre os cantos vistos daqui e os vistos do destino: { i, j, custo } ou null.
function melhorPar(m, A, B, ox, oy, x, y) {
  const { nos, D } = m.cenario;
  let melhor = null;
  for (const i of A) {
    const di = Math.hypot(nos[i].x - ox, nos[i].y - oy);
    for (const j of B) {
      if (D[i][j] === Infinity) continue;   // cantos sem ligação (um lugar fechado)
      const c = di + D[i][j] + Math.hypot(nos[j].x - x, nos[j].y - y);
      if (!melhor || c < melhor.custo) melhor = { i, j, custo: c };
    }
  }
  return melhor;
}

/** O comprimento do caminho de `u` até (x, y) (a linha, se livre; o grafo, senão); Infinity se não há caminho. */
export function distCaminho(m, u, x, y) {
  const f = folgaDe(u);
  if (!m.cenario.obs.length || !bloqueado(m, u.x, u.y, x, y, false, f)) return Math.hypot(x - u.x, y - u.y);
  const p = melhorPar(m, visDe(m, u, f), nosVisiveis(m, x, y, f), u.x, u.y, x, y);
  return p ? p.custo : Infinity;
}

/**
 * O custo extra de ir até `c` pelo caminho em vez da linha reta (0 com a linha livre). Para a escolha de alvo das
 * tropas: até 2 contas de caminho por unidade por escolha (`u.contas`, zerado por quem escolhe); depois, um desvio
 * presumido de 160 px.
 */
export function desvioAte(m, u, c) {
  if (!m.cenario.obs.length || !bloqueado(m, u.x, u.y, c.x, c.y, false, folgaDe(u))) return 0;
  if ((u.contas = (u.contas || 0) + 1) > 2) return 160;
  const d = distCaminho(m, u, c.x, c.y);
  return d === Infinity ? 1e6 : d - Math.hypot(c.x - u.x, c.y - u.y);
}

/** O ponto (x, y) foi marcado inacessível por esta unidade há pouco? */
export function inacessivel(m, u, x, y, r = 20) {
  const i = u.inacessivel;
  return !!i && i.ate > m.t && (i.x - x) ** 2 + (i.y - y) ** 2 <= r * r;
}

// ------------------------------------------------------------------------------------------------ a rota
/**
 * Para onde andar agora para chegar a (x, y). Com a linha livre, o próprio ponto. Senão, o caminho pelo grafo: guardado
 * inteiro (vale 2 s enquanto o destino não anda 24 px) e seguido canto a canto; de 0,2 em 0,2 s confere se o canto
 * seguinte (ou o destino) já se vê e pula o atual. Um destino dentro de uma construção vira o ponto livre mais perto.
 * Quem não sai do lugar recebe um desvio (`vigiar`).
 */
export function rumo(u, x, y) {
  const m = M;
  if (!m || !m.cenario) return { x, y };
  const obs = m.cenario.obs.length, f = folgaDe(u);
  if (obs && dentroObstaculo(m, x, y, u.raio)) ({ x, y } = pontoLivre(m, x, y, u.raio + 1));
  const desvio = vigiar(m, u, x, y);
  if (desvio) return desvio;
  if (!obs || !bloqueado(m, u.x, u.y, x, y, false, f)) { u.nav = null; return { x, y }; }
  const { nos, prox } = m.cenario;
  const nv = u.nav;
  if (nv && nv.caminho && m.t - nv.t < 2 && Math.hypot(nv.tx - x, nv.ty - y) < 24) {
    if (nv.k < nv.caminho.length && Math.hypot(nos[nv.caminho[nv.k]].x - u.x, nos[nv.caminho[nv.k]].y - u.y) < 6) nv.k++;
    if (m.t - nv.olhou >= 0.2) {
      nv.olhou = m.t;
      // o atalho: o próximo canto (ou o destino) já se vê daqui
      if (nv.k + 1 < nv.caminho.length) { const s = nos[nv.caminho[nv.k + 1]]; if (!bloqueado(m, u.x, u.y, s.x, s.y, false, f)) nv.k++; }
    }
    if (nv.k >= nv.caminho.length) return { x, y };
    return nos[nv.caminho[nv.k]];
  }
  // um recálculo por unidade a cada 0,25 s no máximo, e no máximo 40 por passo no campo todo (uma onda que aparece
  // dentro do castelo pedia centenas no mesmo passo); quem passa do limite segue o caminho que tinha por mais um passo
  if (nv && m.t - (nv.calc ?? -9) < 0.25) return nv.caminho && nv.k < nv.caminho.length ? nos[nv.caminho[nv.k]] : nv.fuga || { x, y };
  if (m.navPasso !== m.t) { m.navPasso = m.t; m.navGasto = 0; }
  if (m.navGasto++ >= 40) return nv && nv.caminho && nv.k < nv.caminho.length ? nos[nv.caminho[nv.k]] : { x, y };
  const A = visDe(m, u, f), B = nosVisiveis(m, x, y, f);
  const par = A.length && B.length ? melhorPar(m, A, B, u.x, u.y, x, y) : null;
  if (!B.length || A.length && !par) {
    // o destino está num lugar fechado (nenhum canto à vista dele, ou nenhum ligado aos daqui): inacessível, fica parado
    u.inacessivel = { x, y, ate: m.t + 2.5 };
    u.nav = { t: m.t, calc: m.t, tx: x, ty: y, caminho: null, k: 0, fuga: { x: u.x, y: u.y } };
    return u.nav.fuga;
  }
  if (!A.length) {
    // nenhum canto à vista (encaixado num vão): sai da parede mais perto pela normal dela e tenta de novo
    const o = dentroObstaculo(m, u.x, u.y, u.raio + 2);
    let fx = u.x, fy = u.y;
    if (o) {
      const qx = Math.max(o.x, Math.min(u.x, o.x + o.w)), qy = Math.max(o.y, Math.min(u.y, o.y + o.h)), n = Math.hypot(u.x - qx, u.y - qy) || 1;
      fx = u.x + ((u.x - qx) / n) * 8; fy = u.y + ((u.y - qy) / n) * 8;
    }
    u.nav = { t: m.t, calc: m.t, tx: x, ty: y, caminho: null, k: 0, fuga: { x: fx, y: fy } };
    return u.nav.fuga;
  }
  const caminho = [par.i];
  for (let i = par.i, n = 0; i !== par.j && n < nos.length; n++) { i = prox[i][par.j]; if (i < 0) break; caminho.push(i); }
  u.nav = { t: m.t, calc: m.t, olhou: m.t, tx: x, ty: y, caminho, k: 0 };
  return nos[caminho[0]];
}

// Quem quer andar e não sai do lugar: a cada 0,5 s compara o quanto andou com o quanto devia. Travado contra uma
// construção, refaz a rota já (u.nav = null); travado na multidão, desvia 0,4 s para o lado (o lado da parede, nunca).
// Dois segundos travado (quatro janelas seguidas): o destino fica inacessível por 2,5 s para essa unidade.
function vigiar(m, u, x, y) {
  // só nos cenários com construções: no campo aberto a multidão já se resolvia pela separação (e as tropas de posto
  // não saem da coleira por um desvio)
  if (!m.cenario.obs.length) return null;
  if (u.desvio) { if (u.desvio.ate > m.t) return u.desvio; u.desvio = null; }
  const g = u.prog;
  if (!g || m.t - g.t > 1) { u.prog = { t: m.t, x: u.x, y: u.y, n: 0 }; return null; }
  if (m.t - g.t < 0.5) return null;
  const andou = Math.hypot(u.x - g.x, u.y - g.y), devia = (u.def.vel || 40) * (m.t - g.t), longe = Math.hypot(x - u.x, y - u.y);
  // perto do destino, ou empurrado de volta por golpe, não é estar travado
  const travado = longe > 12 && andou < devia * 0.2 && !(Math.abs(u.kx || 0) + Math.abs(u.ky || 0) > 20);
  g.t = m.t; g.x = u.x; g.y = u.y;
  if (!travado) { g.n = 0; return null; }
  g.n++;
  if (g.n >= 4) { u.inacessivel = { x, y, ate: m.t + 2.5 }; g.n = 0; m.stats.inacessiveis = (m.stats.inacessiveis || 0) + 1; }
  const parede = dentroObstaculo(m, u.x, u.y, u.raio + 1.5);
  m.stats.travados = (m.stats.travados || 0) + 1;
  if (parede) { u.nav = null; u.visNos = null; return null; }
  const dx = x - u.x, dy = y - u.y, n = longe || 1;
  let s = u.id % 2 ? 1 : -1;
  const lado = (k) => ({ x: u.x - (dy / n) * 14 * k + (dx / n) * 4, y: u.y + (dx / n) * 14 * k + (dy / n) * 4 });
  if (dentroObstaculo(m, lado(s).x, lado(s).y, u.raio)) s = -s;
  u.desvio = { ...lado(s), ate: m.t + 0.4 };
  m.stats.desvios = (m.stats.desvios || 0) + 1;
  return u.desvio;
}

// ------------------------------------------------------------------------------------------------ a posição útil
/**
 * Um ponto de onde `u` alcança `alvo` com visão (para atirar, curar, lançar): a até [`min`, `max`] px dele, fora das
 * construções, que se alcança pelo caminho mais curto, longe dos inimigos de `u` (`perigo` px) e, com `fundo` (o centro
 * dos inimigos), do lado de lá do alvo em relação a eles. Guardado (u.posUtil) por `dura` s enquanto continua valendo.
 * No máximo 6 escolhas novas por passo no campo todo; sem nenhum ponto bom, null.
 */
export function posicaoUtil(m, u, alvo, { min = 30, max = 100, perigo = 40, fundo = null, dura = 0.8, visaoDe = null } = {}) {
  const P = u.posUtil;
  if (P && P.alvo === alvo.id && m.t - P.t < dura && Math.hypot(P.ax - alvo.x, P.ay - alvo.y) < 20 &&
      !bloqueado(m, P.x, P.y, alvo.x, alvo.y, true)) return P;
  if (m.posPasso !== m.t) { m.posPasso = m.t; m.posGasto = 0; }
  if (m.posGasto++ >= 6) return P && P.alvo === alvo.id ? P : null;
  const inimigos = m.lados[1 - u.lado], base = Math.atan2(u.y - alvo.y, u.x - alvo.x);
  let melhor = null;
  for (const r of [max * 0.85, (min + max) / 2, min]) {
    for (let k = 0; k < 12; k++) {
      // começa pela direção de quem procura e alterna para os dois lados
      const a = base + (k % 2 ? 1 : -1) * Math.ceil(k / 2) * (Math.PI / 6);
      const x = alvo.x + Math.cos(a) * r, y = alvo.y + Math.sin(a) * r, g = CAMPO.margem + 4;
      if (x < g || y < g || x > CAMPO.largura - g || y > CAMPO.altura - g) continue;
      if (m.cenario.obs.length && (dentroObstaculo(m, x, y, u.raio + 2) || bloqueado(m, x, y, alvo.x, alvo.y, true))) continue;
      if (visaoDe && bloqueado(m, x, y, visaoDe.x, visaoDe.y, true)) continue;
      if (inacessivel(m, u, x, y)) continue;
      let custo = Math.hypot(x - u.x, y - u.y);
      if (melhor && custo > melhor.custo + 60) continue;
      for (const v of inimigos) if (!v.morto && (v.x - x) ** 2 + (v.y - y) ** 2 < perigo * perigo) custo += 70;
      if (fundo) {
        const fx = alvo.x - fundo.x, fy = alvo.y - fundo.y, fn = Math.hypot(fx, fy) || 1;
        custo -= (((x - alvo.x) * fx + (y - alvo.y) * fy) / (fn * r)) * 40;
      }
      if (melhor && custo >= melhor.custo) continue;
      const dc = distCaminho(m, u, x, y);
      if (dc === Infinity) continue;
      custo += dc - Math.hypot(x - u.x, y - u.y);
      if (!melhor || custo < melhor.custo) melhor = { x, y, custo };
    }
  }
  if (!melhor) { u.posUtil = null; return null; }
  u.posUtil = { x: melhor.x, y: melhor.y, t: m.t, alvo: alvo.id, ax: alvo.x, ay: alvo.y };
  m.stats.posicoes = (m.stats.posicoes || 0) + 1;
  return u.posUtil;
}

