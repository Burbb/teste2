// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 8: Harg reconstruído como o confronto principal da batalha, nos
// encontros com `harg8` (o treino e "Harg entra na batalha"; os outros seguem o Harg de antes). Sem DOM. O estudo e as
// razões estão em roadmapIDEIAS/33. Os números estão em conteudo.HARG8.
//
// O repertório é curto: o Talho (a pressão), a Varredura Longa (alcança quem só recua), a Martelada (o golpe final
// comprometido, com a abertura grande), a Investida pela linha (atravessa a infantaria) e o Rodopio (contra a tropa que o
// cerca). Cada golpe tem três tempos que não se misturam:
// - a preparação, com o aviso no chão: ele vira para o alvo só na primeira parte (`rastreia`) e no máximo `giro` rad/s;
//   depois a direção fica marcada. Ele não sabe o que você vai apertar: vira para onde você ESTÁ;
// - a execução, rápida: o avanço curto e o contato no fim, que pega todos os nossos dentro da forma (ele derruba
//   soldados comuns de um golpe e abre caminho);
// - a recuperação, parado; depois da Martelada e da Investida, a abertura (leva +50% e o dobro de postura).
// Entre as sequências, a pressão (anda até o alvo) ou um passo de lado. A escolha de alvo é a do Campo Livre 7
// (campo7.escolherFoco): você, Morel, Odette ou as tropas, com tempo mínimo e inércia.
//
// A postura (a quebra): tudo o que o fere enche a postura (o seu dano inteiro; Morel e Odette 60%; as tropas 25%; o
// contínuo metade; os controles, que nele não atordoam, enchem 20). Cheia, ele quebra: ajoelha 2,2 s levando +50% e
// perde o que fazia. Depois fica firme por 7 s (a postura enche a 35%): não há atordoamento permanente. Acertar sem
// quebrar mostra a reação (o tranco, o brilho, a barra) sem cancelar o golpe dele.
//
// A fase 2 (abaixo de 55% da vida): o Rugido (empurra a nossa tropa em volta), depois sequências de três golpes, pausas
// mais curtas e a Martelada com a onda. As preparações continuam do mesmo tamanho: muda o ritmo, não a leitura.
import { HARG8 } from "./conteudo.js";
import { bloqueado, dentroObstaculo } from "./navegacao.js";
import { escolherFoco, precisaRever } from "./campo7.js";

let S = null;    // as funções de sim.js (ferir, andarPara, registrar)
export function ligar8(h) { S = h; }

const dist2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;
const H = HARG8, G = H.golpes, P = H.postura;
const comum = (v) => !v.def.elite && v.tipo !== "heroi";

/** O estado de Harg no Campo Livre 8 (chamado ao criar o encontro). */
export function prepararHarg8(u) {
  u.vidaMax = u.vida = H.vida;
  u.h8 = { fase: 1, golpe: null, fila: [], pausa: 1, investidaCd: 2, rodopioCd: 2, postura: 0, posturaT: -9, quebrado: 0,
    firmeAte: 0, seq: 0, passo: null };
}

// ------------------------------------------------------------------------------------------------ o passo
/** Harg decide e age. Sempre devolve true (cuida do movimento também). */
export function harg8(m, u, dt) {
  const s = u.h8;
  s.investidaCd -= dt; s.rodopioCd -= dt;
  if (m.t - s.posturaT > P.espera && s.postura > 0) s.postura = Math.max(0, s.postura - P.regen * dt);
  u.vx = u.vy = 0;
  if (s.quebrado > 0) {
    s.quebrado -= dt;
    if (s.quebrado <= 0) {
      s.postura = 0; s.firmeAte = m.t + P.firme;
      m.eventos.push({ tipo: "hargLevanta", id: u.id, x: u.x, y: u.y });
    }
    return true;
  }
  // a fase 2: o rugido, uma vez, quando não está no meio de um golpe
  if (s.fase === 1 && u.vida < u.vidaMax * H.fase2 && !s.golpe) { s.fila = []; comecar(m, u, "rugido", u); return true; }
  if (s.golpe) { avancar(m, u, s.golpe, dt); return true; }
  if (precisaRever(m, u, dt)) escolherFoco(m, u);
  const alvo = alvoDe(m, u);
  if (!alvo) return true;
  const d = Math.sqrt(dist2(u, alvo));
  // a sequência em curso continua enquanto o alvo está ao alcance do golpe seguinte; senão, acaba
  if (s.fila.length) {
    const prox = s.fila[0];
    if (d <= alcanceDe(prox) + alvo.raio + 4) { s.fila.shift(); comecar(m, u, prox, alvo); return true; }
    s.fila = [];
  }
  // o passo de lado depois de uma sequência (o reposicionamento)
  if (s.passo) {
    s.passo.t -= dt;
    if (s.passo.t > 0) { S.andarPara(u, s.passo.x, s.passo.y, H.vel); return true; }
    s.passo = null;
  }
  // contra a tropa que o cerca: o Rodopio
  if (s.rodopioCd <= 0) {
    let n = 0;
    for (const v of m.lados[0]) if (!v.morto && comum(v) && dist2(u, v) <= (G.rodopio.raio - 6) ** 2) n++;
    if (n >= G.rodopio.min) { s.rodopioCd = G.rodopio.recarga; comecar(m, u, "rodopio", u); return true; }
  }
  s.pausa -= dt;
  // a Investida pela linha: de longe, com o caminho livre de construções (a tropa no meio ele atravessa)
  const I = G.investida;
  if (s.investidaCd <= 0 && d >= I.min && d <= I.max && !bloqueado(m, u.x, u.y, alvo.x, alvo.y, false, 4)) {
    s.investidaCd = I.recarga; comecar(m, u, "investida", alvo); return true;
  }
  // perto: começa uma sequência (depois da pausa); longe ou na pausa: a pressão, andando até o alvo
  if (s.pausa <= 0 && d <= alcanceDe("talho") + alvo.raio + 6) {
    const lista = H.sequencias[s.fase], seq = lista[s.seq++ % lista.length].slice();
    const primeiro = seq.shift();
    s.fila = seq;
    comecar(m, u, primeiro, alvo);
    return true;
  }
  if (d > 18) S.andarPara(u, alvo.x, alvo.y, d > 60 ? H.velPressao : H.vel);
  u.virado = alvo.x >= u.x ? 1 : -1;
  return true;
}

// o alcance efetivo de um golpe: o raio, mais o avanço, mais a distância da forma à frente
function alcanceDe(id) { const g = G[id]; return (g.raio || 0) + (g.avanco || 0) + (g.distancia || 0); }

// o alvo de agora: o do duelo (você, Morel, Odette) ou, com as tropas, quem está mais perto dele no grupo escolhido
function alvoDe(m, u) {
  if (u.modo !== "tropas" && u.focoU && !u.focoU.morto) return u.focoU;
  const ref = u.grupoAlvo || u;
  let melhor = null, dm = Infinity;
  for (const v of m.lados[0]) {
    if (v.morto) continue;
    const q = dist2(v, ref) + dist2(v, u) * 0.5;
    if (q < dm) { dm = q; melhor = v; }
  }
  return melhor;
}

// ------------------------------------------------------------------------------------------------ os golpes
function forma(u, g, dir) {
  if (g.forma === "arco") return { tipo: "arco", x: u.x, y: u.y, raio: g.raio, ang: dir, abertura: g.abertura };
  if (g.forma === "circulo") return { tipo: "circulo", x: u.x + Math.cos(dir) * g.distancia, y: u.y + Math.sin(dir) * g.distancia, raio: g.raio };
  return { tipo: "faixa", x1: u.x, y1: u.y, x2: u.x + Math.cos(dir) * g.alcance, y2: u.y + Math.sin(dir) * g.alcance, largura: g.largura };
}

function comecar(m, u, id, alvo) {
  const g = G[id], dir = alvo === u ? (u.virado > 0 ? 0 : Math.PI) : Math.atan2(alvo.y - u.y, alvo.x - u.x);
  const golpe = { id, etapa: "preparo", t: g.preparo, total: g.preparo, dir, alvo: alvo === u ? null : alvo, forma: null, atingidos: new Set() };
  golpe.forma = forma(u, g, dir);
  if (id === "martelada" && u.h8.fase === 2) golpe.onda = { tipo: "circulo", x: golpe.forma.x, y: golpe.forma.y, raio: g.onda.raio };
  u.h8.golpe = golpe;
  u.virado = Math.cos(dir) >= 0 ? 1 : -1;
  m.eventos.push({ tipo: "aviso", id: u.id, forma: golpe.forma, preparo: g.preparo, lider: true, h8: id });
  if (id === "rugido") S.registrar(m, `${u.def.nome} ruge: a fase 2 começa (sequências mais longas, a Martelada solta uma onda).`);
}

function avancar(m, u, golpe, dt) {
  const g = G[golpe.id];
  golpe.t -= dt;
  if (golpe.etapa === "preparo") {
    // a mira: só na primeira parte da preparação, e com o giro limitado; depois a direção fica
    const a = golpe.alvo;
    if (a && !a.morto && golpe.total - golpe.t <= golpe.total * g.rastreia) {
      const quer = Math.atan2(a.y - u.y, a.x - u.x);
      let dif = quer - golpe.dir;
      while (dif > Math.PI) dif -= 2 * Math.PI;
      while (dif < -Math.PI) dif += 2 * Math.PI;
      golpe.dir += Math.max(-g.giro * dt, Math.min(g.giro * dt, dif));
      golpe.forma = forma(u, g, golpe.dir);
      if (golpe.onda) { golpe.onda.x = golpe.forma.x; golpe.onda.y = golpe.forma.y; }
      u.virado = Math.cos(golpe.dir) >= 0 ? 1 : -1;
    }
    if (golpe.t > 0) return;
    golpe.etapa = "exec";
    golpe.t = golpe.id === "investida" ? g.alcance / g.vel : g.exec;
    golpe.total = golpe.t;
    m.eventos.push({ tipo: "hargExec", id: u.id, golpe: golpe.id, x: u.x, y: u.y, dir: golpe.dir });
    return;
  }
  if (golpe.etapa === "exec") {
    const ux = Math.cos(golpe.dir), uy = Math.sin(golpe.dir);
    if (golpe.id === "investida") return investir(m, u, golpe, g, ux, uy);
    // o avanço curto, na direção marcada; o contato no fim da execução
    if (g.avanco) { u.vx = (ux * g.avanco) / g.exec; u.vy = (uy * g.avanco) / g.exec; }
    if (golpe.t > 0) return;
    contato(m, u, golpe, g, ux, uy);
    return;
  }
  // a recuperação: parado; na abertura, leva +50%
  if (golpe.t > 0) return;
  u.h8.golpe = null;
  if (!u.h8.fila.length) depoisDaSequencia(m, u);
}

// o contato: todos os nossos na forma (vista de onde ele está agora) levam o golpe; os comuns caem de uma vez
function contato(m, u, golpe, g, ux, uy) {
  const f = forma(u, g, golpe.dir);
  let n = 0, mortos = 0, heroi = false;
  for (const v of m.lados[1 - u.lado]) {
    if (v.morto || !S.dentro(f, v.x, v.y)) continue;
    const dx = v.x - u.x, dy = v.y - u.y, d = Math.hypot(dx, dy) || 1;
    const comumV = comum(v);
    if (S.ferir(m, v, comumV ? g.dano : g.danoHeroi, u, { dx: dx / d, dy: dy / d, emp: g.empurrao, forte: true, hab: "harg-" + golpe.id }) === 2) mortos++;
    n++;
    if (v === m.heroi) heroi = true;
  }
  // a onda da Martelada (fase 2): o anel em volta do ponto do golpe
  if (golpe.onda) {
    const o = g.onda, c = { tipo: "circulo", x: f.x, y: f.y, raio: o.raio };
    for (const v of m.lados[1 - u.lado]) {
      if (v.morto || S.dentro(f, v.x, v.y) || !S.dentro(c, v.x, v.y) || bloqueado(m, f.x, f.y, v.x, v.y, true)) continue;
      const dx = v.x - f.x, dy = v.y - f.y, d = Math.hypot(dx, dy) || 1;
      if (S.ferir(m, v, comum(v) ? o.dano : o.danoHeroi, u, { dx: dx / d, dy: dy / d, emp: o.empurrao, forte: true, hab: "harg-onda" }) === 2) mortos++;
      if (v === m.heroi) heroi = true;
      n++;
    }
  }
  if (golpe.id === "rugido") { u.h8.fase = 2; m.eventos.push({ tipo: "hargFase", id: u.id, x: u.x, y: u.y, fase: 2 }); }
  m.eventos.push({ tipo: "hargContato", id: u.id, golpe: golpe.id, x: u.x, y: u.y, forma: f, onda: golpe.onda || null, acertos: n, mortos, heroi });
  m.stats.hargAcertos = (m.stats.hargAcertos || 0) + n;
  m.stats.hargMortos = (m.stats.hargMortos || 0) + mortos;
  if (heroi) m.stats.hargNoHeroi = (m.stats.hargNoHeroi || 0) + 1;
  irParaRecuperacao(m, u, golpe, g);
}

// a Investida: corre a faixa marcada; derruba e empurra a infantaria nela (cada um uma vez) e para no primeiro herói (você,
// Morel, Odette), num pesado, numa parede ou no fim do alcance
function investir(m, u, golpe, g, ux, uy) {
  u.vx = ux * g.vel; u.vy = uy * g.vel;
  u.virado = ux >= 0 ? 1 : -1;
  let para = golpe.t <= 0 || !!dentroObstaculo(m, u.x + ux * (u.raio + 4), u.y + uy * (u.raio + 4), 0);
  for (const v of m.lados[1 - u.lado]) {
    if (para) break;
    if (v.morto || golpe.atingidos.has(v.id) || dist2(u, v) > (u.raio + v.raio + 3) ** 2 || (v.x - u.x) * ux + (v.y - u.y) * uy < -2) continue;
    golpe.atingidos.add(v.id);
    const lado = ux * (v.y - u.y) - uy * (v.x - u.x) >= 0 ? 1 : -1, heroico = !comum(v);
    S.ferir(m, v, heroico ? g.danoHeroi : g.dano, u, { dx: -uy * lado * 0.8 + ux * 0.6, dy: ux * lado * 0.8 + uy * 0.6, emp: g.empurrao, forte: true, hab: "harg-investida" });
    if (heroico || (v.massa || 1) >= 5) para = true;
  }
  if (!para) return;
  u.vx = u.vy = 0;
  m.eventos.push({ tipo: "hargContato", id: u.id, golpe: "investida", x: u.x, y: u.y, acertos: golpe.atingidos.size, heroi: golpe.atingidos.has(m.heroi.id) });
  irParaRecuperacao(m, u, golpe, g);
}

function irParaRecuperacao(m, u, golpe, g) {
  golpe.etapa = "rec";
  golpe.t = g.recupera; golpe.total = g.recupera;
  u.vx = u.vy = 0;
  if (g.abertura === true) {
    u.vulneravel = g.recupera;   // ferir: +50% (a regra do líder, def.carga.vulneravel)
    u.h8.abertoAte = m.t + g.recupera;
    m.eventos.push({ tipo: "hargAbertura", id: u.id, x: u.x, y: u.y, dura: g.recupera, golpe: golpe.id });
  }
}

// depois de uma sequência: a pausa (pressão) e, às vezes, um passo de lado
function depoisDaSequencia(m, u) {
  const s = u.h8, [a, b] = H.pausa[s.fase];
  s.pausa = a + m.rng() * (b - a);
  if (m.rng() < (s.fase === 1 ? 0.5 : 0.3)) {
    const alvo = alvoDe(m, u), lado = m.rng() < 0.5 ? 1 : -1;
    if (alvo) {
      const dx = alvo.x - u.x, dy = alvo.y - u.y, n = Math.hypot(dx, dy) || 1;
      s.passo = { x: u.x - (dy / n) * 28 * lado - (dx / n) * 6, y: u.y + (dx / n) * 28 * lado - (dy / n) * 6, t: 0.45 };
    }
  }
}

// ------------------------------------------------------------------------------------------------ a postura
/** O que um golpe faz na postura de Harg (sim.ferir chama, depois do dano). */
export function posturaHarg8(m, u, fonte, dano, o) {
  const s = u.h8;
  if (!s || s.quebrado > 0 || dano <= 0) return;
  const h = m.heroi, F = P.fontes;
  let p = dano * (fonte === h ? F.heroi : fonte && fonte.def && fonte.def.companheiro ? F.companheiro : F.tropa);
  if (o.sutil) p *= P.continuo;
  if (o.forte) p += P.forte;
  ganhar(m, u, p);
}

/** Um controle em Harg (atordoar, imobilizar, interromper, congelar) não o prende: enche a postura. */
export function controleHarg8(m, u) { if (u.h8 && u.h8.quebrado <= 0) ganhar(m, u, P.controle); }

function ganhar(m, u, p) {
  const s = u.h8;
  if (m.t < (s.abertoAte || 0)) p *= P.aberto;
  if (m.t < s.firmeAte) p *= P.firmeFator;
  s.postura += p;
  s.posturaT = m.t;
  // firme (logo depois de uma quebra), a postura enche devagar e não quebra de novo: no máximo 2,2 s de joelhos a cada
  // 9,2 s, mesmo apanhando sem parar
  if (m.t < s.firmeAte) { s.postura = Math.min(s.postura, P.max - 1); return; }
  if (s.postura < P.max) return;
  s.postura = P.max;
  s.quebrado = P.quebra;
  s.golpe = null; s.fila = []; s.passo = null;
  u.vulneravel = P.quebra;
  m.stats.hargQuebras = (m.stats.hargQuebras || 0) + 1;
  m.eventos.push({ tipo: "hargQuebra", id: u.id, x: u.x, y: u.y, dura: P.quebra });
  S.registrar(m, `A postura de ${u.def.nome} quebrou: ${String(P.quebra).replace(".", ",")} s de joelhos, levando +50%.`);
}

/** Antes do passo de Harg: os controles que prenderiam outra unidade viram postura (e o gelo, lentidão curta). */
export function converterControles8(m, u) {
  if (u.atordoado > 0) { u.atordoado = 0; controleHarg8(m, u); }
  if (u.gelo > m.t) { u.gelo = 0; controleHarg8(m, u); u.lentoAte = m.t + 1.5; u.lentoF = 0.4; }
  if (u.imobAte > m.t) { u.imobAte = 0; controleHarg8(m, u); }
}

/** O que a tela mostra de Harg: o golpe em curso, a postura, a fase, a abertura (o texto pronto). */
export function estadoHarg8(m, u) {
  const s = u.h8;
  if (!s) return null;
  const g = s.golpe, nome = g ? G[g.id].nome : null;
  const texto = s.quebrado > 0 ? `Postura quebrada: de joelhos, leva +50% (${s.quebrado.toFixed(1).replace(".", ",")} s)`
    : g && g.etapa === "preparo" ? `Prepara: ${nome}` : g && g.etapa === "exec" ? `${nome}!`
    : g && m.t < (s.abertoAte || 0) ? `Aberto depois da ${nome}: leva +50%` : g && g.etapa === "rec" ? "Recupera"
    : m.t < s.firmeAte ? "Firme: a postura enche devagar" : s.fase === 2 ? "Fúria: sequências mais longas" : "Pressiona";
  return { texto, postura: s.postura / P.max, fase: s.fase, quebrado: s.quebrado > 0, aberto: m.t < (s.abertoAte || 0), firme: m.t < s.firmeAte };
}
