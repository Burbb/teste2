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
//
// Campo Livre 9: a mesma máquina serve a quem tem `u.h8.cfg` (Harg frágil, Vesna, o General; campo9.js). O que entrou,
// sem mudar o Harg do 8: os golpes em estágios (`estagios`: os anéis do Terremoto, a cruz, o leque de facas, cada
// estágio com as suas formas, um depois do outro a cada `intervalo` s), o salto no ponto do alvo (`salto`), o puxão
// (`puxa`, com o golpe `seguinte` garantido só quando prende alguém), os controles no contato (`atordoa`, `lento`, pela
// proteção contra repetição), o recuo de quem luta solto (`recuo`) e as variações (campo9: `ritmo9`, `velF`, `inabalavel`).
import { HARG8 } from "./conteudo.js";
import { bloqueado, dentroObstaculo, pontoLivre } from "./navegacao.js";
import { escolherFoco, precisaRever, aplicarControle } from "./campo7.js";

let S = null;    // as funções de sim.js (ferir, andarPara, registrar)
export function ligar8(h) { S = h; }

const dist2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;
const GRAU = Math.PI / 180;
const comum = (v) => !v.def.elite && v.tipo !== "heroi";

/** O estado de Harg no Campo Livre 8 (chamado ao criar o encontro); `cfg`, a tabela de quem usa a máquina. */
export function prepararHarg8(u, cfg = HARG8) {
  u.vidaMax = u.vida = cfg.vida;
  u.h8 = { cfg, fase: 1, golpe: null, fila: [], pausa: 1, investidaCd: 2, rodopioCd: 2, recuoCd: 2, postura: 0, posturaT: -9,
    quebrado: 0, firmeAte: 0, seq: 0, passo: null };
}

// ------------------------------------------------------------------------------------------------ o passo
/** Harg decide e age. Sempre devolve true (cuida do movimento também). */
export function harg8(m, u, dt) {
  const s = u.h8, H = s.cfg, G = H.golpes, P = H.postura, ritmo = u.ritmo9 || 1, vel = (v) => v * (u.velF || 1);
  s.investidaCd -= dt * ritmo; s.rodopioCd -= dt * ritmo; s.recuoCd -= dt * ritmo;
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
  if (s.fase === 1 && H.fase2 && u.vida < u.vidaMax * H.fase2 && !s.golpe) { s.fila = []; comecar(m, u, H.golpeFase2, u); return true; }
  if (s.golpe) { avancar(m, u, s.golpe, dt); return true; }
  if (precisaRever(m, u, dt)) escolherFoco(m, u);
  const alvo = alvoDe(m, u);
  if (!alvo) return true;
  const d = Math.sqrt(dist2(u, alvo));
  // a sequência em curso continua enquanto o alvo está ao alcance do golpe seguinte; senão, acaba
  if (s.fila.length) {
    const prox = s.fila[0];
    if (d <= alcanceDe(G[prox]) + alvo.raio + 4) { s.fila.shift(); comecar(m, u, prox, alvo); return true; }
    s.fila = [];
  }
  // o passo de lado depois de uma sequência (o reposicionamento)
  if (s.passo) {
    s.passo.t -= dt;
    if (s.passo.t > 0) { S.andarPara(u, s.passo.x, s.passo.y, vel(H.vel)); return true; }
    s.passo = null;
  }
  // quem luta solto (Vesna): com o alvo colado, some para longe dele
  if (H.recuo && s.recuoCd <= 0 && !comum(alvo) && d <= H.recuo.perto) { recuar(m, u, alvo, H.recuo); return true; }
  // contra a tropa que o cerca: o Rodopio
  const C = H.cerco && G[H.cerco];
  if (C && s.rodopioCd <= 0) {
    let n = 0;
    for (const v of m.lados[0]) if (!v.morto && comum(v) && dist2(u, v) <= (C.raio - 6) ** 2) n++;
    if (n >= C.min) { s.rodopioCd = C.recarga; comecar(m, u, H.cerco, u); return true; }
  }
  s.pausa -= dt * ritmo;
  // a Investida pela linha: de longe, com o caminho livre de construções (a tropa no meio ele atravessa)
  const I = G[H.aproxima];
  if (I && s.investidaCd <= 0 && d >= I.min && d <= I.max && !bloqueado(m, u.x, u.y, alvo.x, alvo.y, false, 4)) {
    s.investidaCd = I.recarga; comecar(m, u, H.aproxima, alvo); return true;
  }
  // perto: começa uma sequência (depois da pausa); longe ou na pausa: a pressão, andando até o alvo
  const lista = H.sequencias[s.fase];
  if (s.pausa <= 0 && d <= alcanceDe(G[H.inicio || lista[s.seq % lista.length][0]]) + alvo.raio + 6) {
    const seq = lista[s.seq++ % lista.length].slice();
    const primeiro = seq.shift();
    s.fila = seq;
    comecar(m, u, primeiro, alvo);
    return true;
  }
  if (d > 18) S.andarPara(u, alvo.x, alvo.y, vel(d > 60 ? H.velPressao : H.vel));
  u.virado = alvo.x >= u.x ? 1 : -1;
  return true;
}

// o alcance efetivo de um golpe: o raio, mais o avanço, mais a distância da forma à frente (`alcanceIA`, nos golpes em
// estágios: até onde vale começar)
function alcanceDe(g) { return g.alcanceIA ?? (g.raio || 0) + (g.avanco || 0) + (g.distancia || 0); }

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
// a forma de um golpe simples vista de onde ele vai estar no contato: depois do avanço curto da execução (Campo Livre 9:
// antes, o aviso ficava no pé dele e o golpe acertava até 30 px adiante)
function forma(u, g, dir) {
  const a = g.dash ? 0 : g.avanco || 0, x = u.x + Math.cos(dir) * a, y = u.y + Math.sin(dir) * a;
  if (g.forma === "arco") return { tipo: "arco", x, y, raio: g.raio, ang: dir, abertura: g.abertura };
  if (g.forma === "circulo") return { tipo: "circulo", x: x + Math.cos(dir) * g.distancia, y: y + Math.sin(dir) * g.distancia, raio: g.raio };
  return { tipo: "faixa", x1: x, y1: y, x2: x + Math.cos(dir) * g.alcance, y2: y + Math.sin(dir) * g.alcance, largura: g.largura };
}

// as formas de um estágio (Campo Livre 9): em volta dele (ou do ponto do salto); `ang` em graus, somado à direção do
// golpe (o leque) ou fixo no mundo (`fixo`: a cruz)
function formasDoEstagio(u, e, dir, c) {
  const x = c ? c.x : u.x, y = c ? c.y : u.y, out = [];
  for (const f of e.formas) {
    const angs = f.forma === "cruz" ? [0, 90, 180, 270].map((a) => (a + (f.ang || 0)) * GRAU) : [(f.fixo ? 0 : dir) + (f.ang || 0) * GRAU];
    for (const a of angs) {
      if (f.forma === "anel") out.push({ tipo: "anel", x, y, r0: f.r0, raio: f.raio });
      else if (f.forma === "circulo") out.push({ tipo: "circulo", x: x + Math.cos(a) * (f.distancia || 0), y: y + Math.sin(a) * (f.distancia || 0), raio: f.raio });
      else if (f.forma === "arco") out.push({ tipo: "arco", x, y, raio: f.raio, ang: a, abertura: f.abertura });
      else out.push({ tipo: "faixa", x1: x, y1: y, x2: x + Math.cos(a) * f.alcance, y2: y + Math.sin(a) * f.alcance, largura: f.largura });
    }
  }
  return out;
}

// o ponto do salto: onde o alvo está, no máximo a `max` px dele
function pontoDoSalto(m, u, g, alvo) {
  let dx = alvo.x - u.x, dy = alvo.y - u.y;
  const d = Math.hypot(dx, dy) || 1, k = Math.min(1, g.max / d);
  return pontoLivre(m, u.x + dx * k, u.y + dy * k, u.raio);
}

// as formas de agora de um golpe (o aviso no chão): todas as dos estágios, ou a única
function atualizarFormas(u, golpe, g) {
  if (g.salto) golpe.forma = { tipo: "circulo", x: golpe.centro.x, y: golpe.centro.y, raio: g.raio };
  else if (!g.estagios) golpe.forma = forma(u, g, golpe.dir);
  if (g.estagios) {
    golpe.formasEstagio = g.estagios.map((e) => formasDoEstagio(u, e, golpe.dir, g.salto ? golpe.centro : null));
    golpe.formas = golpe.formasEstagio.flat();
    golpe.forma = golpe.formas[0];
  }
}

function comecar(m, u, id, alvo) {
  const s = u.h8, H = s.cfg, g = H.golpes[id], dir = alvo === u ? (u.virado > 0 ? 0 : Math.PI) : Math.atan2(alvo.y - u.y, alvo.x - u.x);
  const golpe = { id, etapa: "preparo", t: g.preparo, total: g.preparo, preparo: g.preparo, dir, alvo: alvo === u ? null : alvo, forma: null,
    atingidos: new Set(), estagio: 0 };
  if (g.salto) golpe.centro = pontoDoSalto(m, u, g, alvo);
  atualizarFormas(u, golpe, g);
  if (g.onda && s.fase === 2) golpe.onda = { tipo: "circulo", x: golpe.forma.x, y: golpe.forma.y, raio: g.onda.raio };
  s.golpe = golpe;
  u.virado = Math.cos(dir) >= 0 ? 1 : -1;
  m.eventos.push({ tipo: "aviso", id: u.id, forma: golpe.forma, formas: golpe.formas, preparo: g.preparo, lider: true, h8: id, quem: u.tipo });
  if (g.fase2) S.registrar(m, `${u.def.nome} ${H.registroFase2}.`);
}

function avancar(m, u, golpe, dt) {
  const g = u.h8.cfg.golpes[golpe.id];
  golpe.t -= dt;
  if (golpe.etapa === "preparo") {
    // a mira: só na primeira parte da preparação, e com o giro limitado; depois a direção fica. O aviso acompanha
    // onde ele está a cada passo (um empurrão o tira do lugar) e fica fixo na execução: o contato usa o que foi mostrado
    const a = golpe.alvo;
    if (a && !a.morto && golpe.total - golpe.t <= golpe.total * g.rastreia) {
      if (g.salto) golpe.centro = pontoDoSalto(m, u, g, a);
      else {
        const quer = Math.atan2(a.y - u.y, a.x - u.x);
        let dif = quer - golpe.dir;
        while (dif > Math.PI) dif -= 2 * Math.PI;
        while (dif < -Math.PI) dif += 2 * Math.PI;
        golpe.dir += Math.max(-g.giro * dt, Math.min(g.giro * dt, dif));
      }
      u.virado = Math.cos(golpe.dir) >= 0 ? 1 : -1;
    }
    atualizarFormas(u, golpe, g);
    if (golpe.onda) { golpe.onda.x = golpe.forma.x; golpe.onda.y = golpe.forma.y; }
    if (golpe.t > 0) return;
    golpe.etapa = "exec";
    golpe.t = g.dash ? g.alcance / g.vel : g.estagios && !g.salto ? 0 : g.exec;
    golpe.total = golpe.t;
    if (g.salto) { golpe.de = { x: u.x, y: u.y }; u.voando = true; }
    m.eventos.push({ tipo: "hargExec", id: u.id, golpe: golpe.id, x: u.x, y: u.y, dir: golpe.dir, quem: u.tipo });
    return;
  }
  if (golpe.etapa === "exec") {
    const ux = Math.cos(golpe.dir), uy = Math.sin(golpe.dir);
    if (g.dash) return investir(m, u, golpe, g, ux, uy);
    // o salto: voa até o ponto marcado; o contato na queda
    if (g.salto && golpe.estagio === 0) {
      const k = golpe.total > 0 ? Math.max(0, golpe.t) / golpe.total : 0;
      u.x = golpe.centro.x + (golpe.de.x - golpe.centro.x) * k; u.y = golpe.centro.y + (golpe.de.y - golpe.centro.y) * k;
      if (golpe.t > 0) return;
      u.voando = false;
    }
    // o avanço curto, na direção marcada; o contato no fim da execução
    // (a velocidade cobre o avanço inteiro nos passos que andam antes do contato: o corpo chega aonde o aviso mostrou)
    if (g.avanco && !g.estagios) {
      const k = g.avanco / (Math.max(1, Math.ceil(g.exec / dt - 1e-6) - 1) * dt);
      u.vx = ux * k; u.vy = uy * k;
    }
    if (golpe.t > 0) return;
    if (g.estagios) return estagio(m, u, golpe, g);
    contato(m, u, golpe, g, ux, uy);
    return;
  }
  // a recuperação: parado; na abertura, leva +50%
  if (golpe.t > 0) return;
  u.h8.golpe = null;
  // o puxão que prendeu alguém garante o golpe seguinte (com a preparação inteira: dá para sair dele)
  if (g.seguinte && golpe.puxou) u.h8.fila.unshift(g.seguinte);
  if (!u.h8.fila.length) depoisDaSequencia(m, u);
}

// o contato: todos os nossos na forma mostrada no aviso levam o golpe; os comuns caem de uma vez
function contato(m, u, golpe, g, ux, uy) {
  const f = golpe.forma;
  let n = 0, mortos = 0, heroi = false;
  for (const v of m.lados[1 - u.lado]) {
    if (v.morto || !S.dentro(f, v.x, v.y)) continue;
    const dx = v.x - u.x, dy = v.y - u.y, d = Math.hypot(dx, dy) || 1;
    const comumV = comum(v);
    if (S.ferir(m, v, comumV ? g.dano : g.danoHeroi, u, { dx: dx / d, dy: dy / d, emp: g.empurrao, forte: true, hab: "harg-" + golpe.id }) === 2) mortos++;
    else controles(m, u, v, g, golpe);
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
  if (g.fase2) { u.h8.fase = 2; m.eventos.push({ tipo: "hargFase", id: u.id, x: u.x, y: u.y, fase: 2, quem: u.tipo }); }
  m.eventos.push({ tipo: "hargContato", id: u.id, golpe: golpe.id, x: u.x, y: u.y, forma: f, onda: golpe.onda || null, acertos: n, mortos, heroi, quem: u.tipo });
  contar(m, u, n, mortos, heroi);
  irParaRecuperacao(m, u, golpe, g);
}

// um estágio dos golpes em estágios: as formas dele, as do aviso; quem já levou um estágio não leva outro
function estagio(m, u, golpe, g) {
  const formas = golpe.formasEstagio[golpe.estagio];
  let n = 0, mortos = 0, heroi = false;
  for (const v of m.lados[1 - u.lado]) {
    if (v.morto || golpe.atingidos.has(v.id) || !formas.some((f) => S.dentro(f, v.x, v.y))) continue;
    golpe.atingidos.add(v.id);
    const dx = v.x - u.x, dy = v.y - u.y, d = Math.hypot(dx, dy) || 1;
    if (S.ferir(m, v, comum(v) ? g.dano : g.danoHeroi, u, { dx: dx / d, dy: dy / d, emp: g.empurrao, forte: true, hab: "harg-" + golpe.id }) === 2) mortos++;
    else controles(m, u, v, g, golpe);
    n++;
    if (v === m.heroi) heroi = true;
  }
  const ultimo = golpe.estagio === g.estagios.length - 1;
  if (g.fase2 && ultimo) { u.h8.fase = 2; m.eventos.push({ tipo: "hargFase", id: u.id, x: u.x, y: u.y, fase: 2, quem: u.tipo }); }
  m.eventos.push({ tipo: "hargContato", id: u.id, golpe: golpe.id, x: u.x, y: u.y, formas, estagio: golpe.estagio, ultimo, acertos: n, mortos, heroi, quem: u.tipo });
  contar(m, u, n, mortos, heroi);
  golpe.estagio++;
  if (!ultimo) { golpe.t = g.intervalo; return; }
  irParaRecuperacao(m, u, golpe, g);
}

// os controles do contato em quem sobreviveu (nos heróis, pela proteção contra repetição; nas tropas, direto) e o puxão
function controles(m, u, v, g, golpe) {
  if (v.morto) return;
  const heroico = !comum(v);
  if (g.puxa) {
    const ux = Math.cos(golpe.dir), uy = Math.sin(golpe.dir), p = pontoLivre(m, u.x + ux * (u.raio + v.raio + g.puxa.para), u.y + uy * (u.raio + v.raio + g.puxa.para), v.raio);
    m.eventos.push({ tipo: "puxao", de: { x: v.x, y: v.y }, para: p, id: v.id, fonte: u.id });
    v.x = v.px = p.x; v.y = v.py = p.y; v.kx = v.ky = 0;
    if (heroico) { if (aplicarControle(m, v, "imobilizado", g.puxa.imob, u) > 0 || v === m.heroi) golpe.puxou = true; }
    else v.imobAte = m.t + g.puxa.imob;
  }
  if (g.atordoa) { if (heroico) aplicarControle(m, v, "atordoado", g.atordoa, u); else v.atordoado = Math.max(v.atordoado || 0, g.atordoa); }
  if (g.lento) aplicarControle(m, v, "lento", g.lento.dura, u, { fator: g.lento.fator });
}

function contar(m, u, n, mortos, heroi) {
  const pre = u.h8.cfg.stats || "harg";
  m.stats[pre + "Acertos"] = (m.stats[pre + "Acertos"] || 0) + n;
  m.stats[pre + "Mortos"] = (m.stats[pre + "Mortos"] || 0) + mortos;
  if (heroi) m.stats[pre + "NoHeroi"] = (m.stats[pre + "NoHeroi"] || 0) + 1;
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
  m.eventos.push({ tipo: "hargContato", id: u.id, golpe: golpe.id, x: u.x, y: u.y, acertos: golpe.atingidos.size, heroi: golpe.atingidos.has(m.heroi.id), quem: u.tipo });
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

// o recuo (Vesna): some do lado do alvo e reaparece a `dist` px, longe dele, num ponto livre
function recuar(m, u, alvo, R) {
  const s = u.h8, dx = u.x - alvo.x, dy = u.y - alvo.y, a0 = Math.atan2(dy, dx);
  let melhor = null;
  for (const da of [0, 0.5, -0.5, 1, -1]) {
    const p = pontoLivre(m, alvo.x + Math.cos(a0 + da) * R.dist, alvo.y + Math.sin(a0 + da) * R.dist, u.raio);
    const d = Math.hypot(p.x - alvo.x, p.y - alvo.y);
    if (!melhor || d > melhor.d + 4) melhor = { ...p, d };
  }
  m.eventos.push({ tipo: "recuo9", id: u.id, de: { x: u.x, y: u.y }, para: { x: melhor.x, y: melhor.y } });
  u.x = melhor.x; u.y = melhor.y;
  s.recuoCd = R.recarga; s.pausa = Math.min(s.pausa, 0.2);
}

// depois de uma sequência: a pausa (pressão) e, às vezes, um passo de lado
function depoisDaSequencia(m, u) {
  const s = u.h8, [a, b] = s.cfg.pausa[s.fase];
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
  if (!s || s.quebrado > 0 || dano <= 0 || u.inabalavel) return;
  const h = m.heroi, P = s.cfg.postura, F = P.fontes;
  let p = dano * (fonte === h ? F.heroi : fonte && fonte.def && fonte.def.companheiro ? F.companheiro : F.tropa);
  if (o.sutil) p *= P.continuo;
  if (o.forte) p += P.forte;
  ganhar(m, u, p);
}

/** Um controle em Harg (atordoar, imobilizar, interromper, congelar) não o prende: enche a postura. */
export function controleHarg8(m, u) { if (u.h8 && u.h8.quebrado <= 0 && !u.inabalavel) ganhar(m, u, u.h8.cfg.postura.controle); }

function ganhar(m, u, p) {
  const s = u.h8, P = s.cfg.postura;
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
  if (s.golpe && s.golpe.etapa === "exec" && u.voando) u.voando = false;
  s.golpe = null; s.fila = []; s.passo = null;
  u.vulneravel = P.quebra;
  const pre = s.cfg.stats || "harg";
  m.stats[pre + "Quebras"] = (m.stats[pre + "Quebras"] || 0) + 1;
  m.eventos.push({ tipo: "hargQuebra", id: u.id, x: u.x, y: u.y, dura: P.quebra, nome: u.def.nome });
  S.registrar(m, `A postura ${u.def.nome.startsWith("O ") ? "do " + u.def.nome.slice(2) : "de " + u.def.nome} quebrou: ${String(P.quebra).replace(".", ",")} s de joelhos, levando +50%.`);
}

/** Antes do passo de Harg: os controles que prenderiam outra unidade viram postura (e o gelo, lentidão curta). */
export function converterControles8(m, u) {
  if (u.atordoado > 0) { u.atordoado = 0; controleHarg8(m, u); }
  if (u.gelo > m.t) { u.gelo = 0; controleHarg8(m, u); if (!u.inabalavel) { u.lentoAte = m.t + 1.5; u.lentoF = 0.4; } }
  if (u.imobAte > m.t) { u.imobAte = 0; controleHarg8(m, u); }
}

/** O que a tela mostra de Harg: o golpe em curso, a postura, a fase, a abertura (o texto pronto). */
export function estadoHarg8(m, u) {
  const s = u.h8;
  if (!s) return null;
  const H = s.cfg, g = s.golpe, gd = g ? H.golpes[g.id] : null, nome = gd ? gd.nome : null;
  const texto = s.quebrado > 0 ? `Postura quebrada: de joelhos, leva +50% (${s.quebrado.toFixed(1).replace(".", ",")} s)`
    : g && g.etapa === "preparo" ? `Prepara: ${nome}` : g && g.etapa === "exec" ? `${nome}!`
    : g && m.t < (s.abertoAte || 0) ? `Aberto depois ${gd.apos || `da ${nome}`}: leva +50%` : g && g.etapa === "rec" ? "Recupera"
    : m.t < s.firmeAte ? "Firme: a postura enche devagar" : s.fase === 2 ? H.estadoFase2 : "Pressiona";
  return { texto, postura: u.inabalavel ? 0 : s.postura / H.postura.max, fase: s.fase, quebrado: s.quebrado > 0, aberto: m.t < (s.abertoAte || 0),
    firme: m.t < s.firmeAte, inabalavel: !!u.inabalavel };
}
