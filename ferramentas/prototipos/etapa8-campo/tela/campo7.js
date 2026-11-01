// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 7: como os heróis inimigos escolhem quem enfrentar, os controles
// (CC) com a proteção contra repetição, as provocações (o Desafio de Morel e o Brado de Harg) e a Investida Curta em
// três tempos. Sem DOM. Vale nos encontros com Morel e Odette (os do Campo Livre 6 em diante); os antigos seguem as
// regras de antes. sim.js e campo6.js chamam estas funções; o dano continua em sim.ferir.
//
// A escolha de alvo dos heróis inimigos (`escolherFoco`) usa só o que está no campo: onde cada um está e o caminho até
// ele (não a linha reta através da muralha), quanto cada um os feriu e feriu as tropas deles há pouco (a memória cai pela
// metade a cada 3 s), quanto cada um curou ou protegeu, quem está ferido ou sozinho, onde as nossas tropas estão juntas e
// o que as habilidades prontas alcançam. Nada do que o jogador vai apertar. Uma escolha dura pelo menos `minimo` s e é
// revista de `revisao` em `revisao` s (sorteado), ou antes quando algo relevante acontece (o alvo caiu ou ficou
// inacessível, um golpe forte de outro, a provocação); quem já é o alvo ganha `inercia` (não troca por um pixel).
import { CONTROLE } from "./conteudo.js";
import { bloqueado, distCaminho, dentroObstaculo, inacessivel } from "./navegacao.js";
import { controleHarg8 } from "./campo8.js";

let S = null;    // as funções de sim.js (ferir, registrar)
export function ligar7(h) { S = h; }

const dist2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;
const num = (v) => (Math.round(v * 10) / 10).toFixed(1).replace(".", ",");
const heroico = (m, v) => v === m.heroi || !!v.def.elite;

// ------------------------------------------------------------------------------------------------ a memória do campo
const MEIA_VIDA = 3;
function lembrar(mapa, id, v, t) {
  const e = mapa.get(id);
  mapa.set(id, { v: (e ? e.v * 0.5 ** ((t - e.t) / MEIA_VIDA) : 0) + v, t });
}
export function lembrado(mapa, id, t) {
  const e = mapa && mapa.get(id);
  return e ? e.v * 0.5 ** ((t - e.t) / MEIA_VIDA) : 0;
}
const valor = (e, t) => (e ? e.v * 0.5 ** ((t - e.t) / MEIA_VIDA) : 0);
const somar = (e, v, t) => ({ v: valor(e, t) + v, t });

/**
 * Um golpe que saiu da vida de `u`: os heróis (e Morel, Odette, os heróis inimigos) lembram de quem apanharam; os heróis
 * inimigos lembram também de quem está derrubando a tropa deles por perto (a até 160 px).
 */
export function registrarGolpe(m, u, fonte, dano) {
  if (!fonte || fonte === u || dano <= 0) return;
  if (heroico(m, u)) {
    lembrar(u.dor ||= new Map(), fonte.id, dano, m.t);
    // um golpe forte de quem não é o alvo de agora: o herói inimigo revê a escolha já
    if (u.def.heroiInimigo && dano >= 18 && u.focoU !== fonte) u.reverFoco = true;
    if (u.def.heroiInimigo && fonte.lado !== u.lado && !heroico(m, fonte)) u.dorTropas = somar(u.dorTropas, dano, m.t);
  }
  if (u.lado === 1 && !u.def.elite && heroico(m, fonte)) {
    for (const e of [m.lider, m.ardis]) {
      if (!e || e.morto || !e.def.focoIA || dist2(e, u) > 160 * 160) continue;
      lembrar(e.nasTropas ||= new Map(), fonte.id, dano, m.t);
    }
  }
}

/** Cura e proteção prestadas (Odette, os magos): quem ajuda vira um alvo que vale mais. */
export function registrarApoio(m, quem, v) { quem.apoioV = somar(quem.apoioV, v, m.t); }

// ------------------------------------------------------------------------------------------------ os controles
/**
 * Aplica um controle e devolve a duração que pegou (0: não pegou). `tipo`: "atordoado" (nem anda nem age),
 * "imobilizado" (não anda nem usa a mobilidade; ataca e lança no lugar), "interrupcao" (perde a preparação do golpe e
 * segura um instante), "provocacao" (o alvo do ataque principal, num herói; o alvo da escolha, num herói inimigo) e
 * "lento" (`extra.fator`: quanto da velocidade perde). Nos heróis, os fortes passam pela proteção contra repetição
 * (CONTROLE); a lentidão vale a mais forte, sem acumular.
 */
export function aplicarControle(m, alvo, tipo, dura, fonte, extra = {}) {
  if (!alvo || alvo.morto) return 0;
  // Campo Livre 9: o herói inimigo inabalável não fica preso por nada (nem lento, nem provocado)
  if (alvo.inabalavel) { m.eventos.push({ tipo: "firme", id: alvo.id, x: alvo.x, y: alvo.y, cc: tipo, heroi: false }); return 0; }
  // Campo Livre 8: Harg não fica preso; o controle enche a postura dele (a lentidão e a provocação valem como sempre)
  if (alvo.h8 && tipo !== "lento" && tipo !== "provocacao") { controleHarg8(m, alvo); return 0; }
  const C = CONTROLE, t = m.t;
  if (tipo === "lento") {
    const f = extra.fator;
    if (alvo.lentoAte > t && alvo.lentoF > f) return 0;
    alvo.lentoF = f;
    alvo.lentoAte = Math.max(alvo.lentoAte || 0, t + dura);
    m.eventos.push({ tipo: "controle", id: alvo.id, cc: tipo, x: alvo.x, y: alvo.y, dura, fator: 1, heroi: alvo === m.heroi });
    return dura;
  }
  let fator = 1;
  if (heroico(m, alvo)) {
    const r = alvo.resCC ||= { n: 0, ate: 0 };
    if (t >= r.ate) r.n = 0;
    fator = C.fatores[Math.min(r.n, C.fatores.length - 1)];
    if (fator <= 0) {
      m.eventos.push({ tipo: "firme", id: alvo.id, x: alvo.x, y: alvo.y, cc: tipo, heroi: alvo === m.heroi });
      if (alvo === m.heroi) S.registrar(m, `Você está firme: ${C.nomes[tipo].toLowerCase()} não pega.`);
      return 0;
    }
    r.n++;
    r.ate = t + C.janela;
  }
  const d = dura * fator;
  if (tipo === "atordoado") { alvo.atordoado = Math.max(alvo.atordoado || 0, d); interromperPreparo(m, alvo); }
  else if (tipo === "imobilizado") alvo.imobAte = Math.max(alvo.imobAte || 0, t + d);
  else if (tipo === "interrupcao") { interromperPreparo(m, alvo); alvo.atordoado = Math.max(alvo.atordoado || 0, d); }
  else if (tipo === "provocacao") {
    alvo.provocacao = { por: fonte, ate: t + d, total: d };
    if (alvo !== m.heroi) alvo.reverFoco = true;
  }
  alvo.ultimoCC = { tipo, ate: t + d, total: d, fator };
  m.eventos.push({ tipo: "controle", id: alvo.id, cc: tipo, x: alvo.x, y: alvo.y, dura: d, fator, heroi: alvo === m.heroi,
    fonte: fonte ? fonte.id : null });
  m.stats.controles = (m.stats.controles || 0) + 1;
  return d;
}

/** A preparação em curso se perde (o golpe do herói, a ação de uma unidade, a Investida, o Brado, o Grilhão). */
export function interromperPreparo(m, u) {
  if (u === m.heroi) {
    const a = u.acao;
    if (a && a.fase === "preparo") { u.acao = null; m.eventos.push({ tipo: "interrompe", x: u.x, y: u.y, heroi: true }); }
    return;
  }
  let perdeu = false;
  if (u.dash7 && u.dash7.fase === "preparo") { u.dash7 = null; perdeu = true; }
  if (u.brado7) { u.brado7 = null; perdeu = true; }
  if (u.acaoA) { u.acaoA = null; perdeu = true; }
  if (perdeu && u.def.elite) m.eventos.push({ tipo: "interrompe", x: u.x, y: u.y });
}

/**
 * O que a tela mostra de controle numa unidade (a sua HUD, Morel, Odette, os heróis inimigos): os efeitos ativos e a
 * proteção, cada um com o texto pronto. `[{ id, texto, resta, total }]`.
 */
export function estadoControle(m, u) {
  const t = m.t, l = [];
  if (!u || u.morto) return l;
  if (u.atordoado > 0) l.push({ id: "atordoado", texto: `Atordoado ${num(u.atordoado)} s`, resta: u.atordoado, total: (u.ultimoCC || {}).total || u.atordoado });
  if (u.imobAte > t) l.push({ id: "imobilizado", texto: `Imobilizado ${num(u.imobAte - t)} s: não anda`, resta: u.imobAte - t, total: (u.ultimoCC || {}).total || 1 });
  if (u.lentoAte > t) l.push({ id: "lento", texto: `Lento (−${Math.round(u.lentoF * 100)}%) ${num(u.lentoAte - t)} s`, resta: u.lentoAte - t, total: 2 });
  const p = u.provocacao;
  if (p && p.ate > t && p.por && !p.por.morto) {
    const nome = p.por.def.nome.split(",")[0];
    l.push({ id: "provocacao", texto: u === m.heroi ? `Provocado por ${nome} ${num(p.ate - t)} s: o ataque principal vai nele` :
      `Provocado por ${nome} ${num(p.ate - t)} s`, resta: p.ate - t, total: p.total });
  }
  // Campo Livre 9: o veneno das variações (as doses e o tempo que falta)
  const v = u.veneno9;
  if (v && v.ate > t && v.doses > 0) l.push({ id: "veneno", texto: `Envenenado ×${v.doses} ${num(v.ate - t)} s`, resta: v.ate - t, total: 3 });
  const r = u.resCC;
  if (r && r.ate > t && r.n > 0) {
    const f = CONTROLE.fatores[Math.min(r.n, CONTROLE.fatores.length - 1)];
    l.push({ id: "protecao", texto: f > 0 ? `Proteção: o próximo controle dura ${Math.round(f * 100)}% (${num(r.ate - t)} s)` :
      `Firme: controles não pegam por ${num(r.ate - t)} s`, resta: r.ate - t, total: CONTROLE.janela, firme: f <= 0 });
  }
  return l;
}

// ------------------------------------------------------------------------------------------------ a provocação no herói
/**
 * Com a provocação, o ataque principal mira o provocador: a Varredura vira para ele (a assistência o escolhe) e a Bola cai
 * nele, se ele está ao alcance e à vista; fora do alcance ou sem visão, o golpe sai para onde o mouse aponta, sem
 * assistência (a provocação não puxa o herói nem atravessa paredes); morto o provocador, ela acaba. As outras
 * habilidades seguem a mira de sempre. Devolve o provocador quando ele vale, null quando não, undefined sem provocação.
 */
export function provocadorAoAlcance(m, h, alcance) {
  const p = h.provocacao;
  if (!p || p.ate <= m.t) return undefined;
  if (!p.por || p.por.morto) { h.provocacao = null; return undefined; }
  const e = p.por;
  if (Math.hypot(e.x - h.x, e.y - h.y) > alcance + e.raio) return null;
  if (m.cenario.obs.length && bloqueado(m, h.x, h.y, e.x, e.y, true)) return null;
  return e;
}

// ------------------------------------------------------------------------------------------------ a escolha de alvo
function aliadosPerto(m, w, r) {
  for (const o of m.lados[w.lado]) if (o !== w && !o.morto && dist2(o, w) <= r * r) return true;
  return false;
}

function grupoTropas(m, u, alcance) {
  let melhor = null;
  const L = m.lados[1 - u.lado], comp = (o) => o === m.heroi || o.def.companheiro;
  for (let i = 0; i < L.length; i += L.length > 80 ? 2 : 1) {
    const a = L[i];
    if (a.morto || comp(a) || dist2(a, u) > alcance * alcance) continue;
    let n = 0, sx = 0, sy = 0;
    for (const b of L) if (!b.morto && !comp(b) && dist2(a, b) <= 40 * 40) { const w = b.tipo === "arqueiro" || b.tipo === "magoBatalha" ? 1.5 : 1; n += w; sx += b.x * w; sy += b.y * w; }
    if (n >= 4 && (!melhor || n > melhor.n)) melhor = { x: sx / n, y: sy / n, n };
  }
  return melhor;
}

// o que as habilidades prontas alcançam daqui
function oportunidade(m, u, d, grupo) {
  const D = u.def;
  if (u.tipo === "lider") {
    if (grupo) return u.cargaCd <= 0 || u.arremCd <= 0 && d >= D.arremetida.min && d <= D.arremetida.max;
    return u.arremCd <= 0 && d >= D.arremetida.min && d <= D.arremetida.max || u.dashCd <= 0 && d >= D.investida7.min && d <= D.investida7.max;
  }
  if (u.tipo === "ardis") return u.colunaCd <= 0 && d <= D.coluna.alcance || !grupo && u.grilhaoCd <= 0 && d <= D.grilhao.alcance;
  return false;
}

const NOMES = { heroi: "você", morel: "Morel", odette: "Odette", tropas: "as suas tropas" };

/** A escolha de um herói inimigo. Grava `u.modo` ("heroi", "morel", "odette", "tropas"), `u.focoU` e `u.grupoAlvo`. */
export function escolherFoco(m, u) {
  const F = u.def.focoIA, h = m.heroi, t = m.t, vel = u.def.vel;
  u.reverFoco = false;
  const pv = u.provocacao;
  if (pv && pv.ate > t && pv.por && !pv.por.morto && distCaminho(m, u, pv.por.x, pv.por.y) < Infinity) {
    return definirFoco(m, u, pv.por === h ? "heroi" : pv.por.tipo, pv.por, null, "provocado");
  }
  const prot = u.tipo === "lider" && m.ardis && !m.ardis.morto ? m.ardis : null;
  let melhor = null;
  for (const [tipo, w] of [["heroi", h], ["morel", m.morel], ["odette", m.odette]]) {
    if (!w || w.morto || inacessivel(m, u, w.x, w.y, 30)) continue;
    const dc = distCaminho(m, u, w.x, w.y);
    if (dc === Infinity) continue;
    let v = F.base[tipo] - (dc / vel) * F.tempo;
    v += (lembrado(u.dor, w.id, t) + lembrado(u.nasTropas, w.id, t) * 0.35) * F.pressao;
    v += valor(w.apoioV, t) * F.apoio;
    v += (1 - w.vida / w.vidaMax) * F.ferido;
    if (!aliadosPerto(m, w, 40)) v += F.isolado;
    if (oportunidade(m, u, dc, false)) v += F.oportunidade;
    if (prot) v += lembrado(prot.dor, w.id, t) * F.protege + (dist2(w, prot) < 90 * 90 ? 25 : 0);
    if (u.focoU === w && u.modo === tipo) v += F.inercia;
    v += (m.rng() - 0.5) * F.ruido;
    if (!melhor || v > melhor.v) melhor = { tipo, alvo: w, grupo: null, v };
  }
  const g = grupoTropas(m, u, u.tipo === "ardis" ? 240 : 190);
  if (g) {
    const dc = distCaminho(m, u, g.x, g.y);
    if (dc < Infinity) {
      let v = F.base.tropas + g.n * F.concentracao - (dc / vel) * F.tempo + valor(u.dorTropas, t) * F.pressao * 0.5;
      if (oportunidade(m, u, dc, true)) v += F.oportunidade;
      if (u.modo === "tropas") v += F.inercia;
      v += (m.rng() - 0.5) * F.ruido;
      if (!melhor || v > melhor.v) melhor = { tipo: "tropas", alvo: null, grupo: g, v };
    }
  }
  if (!melhor) return definirFoco(m, u, h.morto ? "tropas" : "heroi", h.morto ? null : h, null);
  return definirFoco(m, u, melhor.tipo, melhor.alvo, melhor.grupo);
}

function definirFoco(m, u, tipo, alvo, grupo, motivo) {
  const F = u.def.focoIA, mudou = tipo !== u.modo || alvo !== u.focoU;
  u.modo = tipo; u.focoU = alvo; u.grupoAlvo = grupo;
  u.focoT = F.revisao[0] + m.rng() * (F.revisao[1] - F.revisao[0]);
  if (!mudou) return;
  u.focoDesde = m.t;
  u.alvo = null;
  u.reavaliar = 0;
  const quem = u.def.nome.split(",")[0];
  const texto = motivo === "provocado" ? `${quem} foi provocado por ${alvo.def.nome.split(",")[0]}.`
    : tipo === "heroi" ? `${quem} vem atrás de você.` : tipo === "tropas" ? `${quem} vai para as suas tropas.` : `${quem} vai atrás de ${NOMES[tipo]}.`;
  m.eventos.push({ tipo: "liderFoco", id: u.id, modo: tipo, texto, x: u.x, y: u.y });
  S.registrar(m, texto);
  m.stats.trocasFoco = (m.stats.trocasFoco || 0) + 1;
}

/** Hora de rever a escolha? (o tempo mínimo e a revisão; antes disso, só uma mudança relevante) */
export function precisaRever(m, u, dt) {
  u.focoT = (u.focoT ?? 0) - dt;
  const f = u.focoU, pv = u.provocacao;
  if (pv && pv.ate > m.t) return u.focoU !== pv.por && !pv.por.morto;
  if (pv && pv.ate <= m.t) { u.provocacao = null; return true; }
  if (u.modo === undefined || u.reverFoco) return true;
  if (f && (f.morto || f.saiu)) return true;
  if (u.modo === "tropas" && !u.grupoAlvo) return u.focoT <= 0;
  return u.focoT <= 0 && m.t - (u.focoDesde ?? -9) >= u.def.focoIA.minimo;
}

// ------------------------------------------------------------------------------------------------ Harg (CL7)
/**
 * A Investida Curta em três tempos e o Brado. Devolve true enquanto uma delas ocupa o Capitão neste passo. `fu`: o alvo
 * do duelo (você, Morel ou Odette), ou null com as tropas.
 */
export function hargCL7(m, u, dt) {
  const d = u.def, D = d.investida7, B = d.brado, h = m.heroi;
  u.bradoCd = (u.bradoCd ?? 4) - dt;
  if (u.dash7) return investida(m, u, dt);
  if (u.brado7) {
    u.brado7.t -= dt; u.vx = u.vy = 0;
    if (u.brado7.t > 0) return true;
    u.brado7 = null;
    if (!h.morto && dist2(h, u) <= B.raio * B.raio && !bloqueado(m, u.x, u.y, h.x, h.y, true)) {
      const ok = aplicarControle(m, h, "provocacao", B.dura, u);
      S.registrar(m, ok ? `${d.nome} brada: você está provocado por ${num(ok)} s (o ataque principal vai nele).` : `${d.nome} brada, mas você está firme.`);
      definirFoco(m, u, "heroi", h, null);
    }
    m.eventos.push({ tipo: "brado", id: u.id, x: u.x, y: u.y, raio: B.raio });
    return true;
  }
  if (u.acao || u.voando) return false;
  // o Brado: você está derrubando a tropa dele por perto (ou batendo em Ardis), à vista e ao alcance; ele quer você
  if (u.bradoCd <= 0 && !h.morto && dist2(u, h) <= (B.raio - 12) ** 2 && !bloqueado(m, u.x, u.y, h.x, h.y, true) &&
      !(h.provocacao && h.provocacao.ate > m.t)) {
    const ocupado = lembrado(u.nasTropas, h.id, m.t) + (m.ardis ? lembrado(m.ardis.dor, h.id, m.t) : 0);
    if (ocupado >= 14 && lembrado(u.dor, h.id, m.t) < 20) {
      u.brado7 = { t: B.preparo };
      u.bradoCd = B.recarga;
      m.eventos.push({ tipo: "aviso", id: u.id, forma: { tipo: "circulo", x: u.x, y: u.y, raio: B.raio }, preparo: B.preparo, lider: true, brado: true });
      S.registrar(m, `${d.nome} prepara o Brado de Desafio.`);
      return true;
    }
  }
  // a Investida Curta: no alvo do duelo, entre `min` e `max` px, com a linha livre
  const fu = u.modo !== "tropas" ? u.focoU : null;
  if (fu && !fu.morto && u.dashCd <= 0) {
    const dd = Math.sqrt(dist2(u, fu));
    if (dd >= D.min && dd <= D.max && !bloqueado(m, u.x, u.y, fu.x, fu.y, false, 3) && (u.arremCd > 0 || dd > d.arremetida.max * 0.8)) {
      // mira onde o alvo está, com um adiantamento curto; a direção fica marcada (sem corrigir na execução)
      const tx = fu.x + (fu.vx || 0) * 0.15, ty = fu.y + (fu.vy || 0) * 0.15, n = Math.hypot(tx - u.x, ty - u.y) || 1;
      const comp = Math.min(D.alcance, n + 16), dx = (tx - u.x) / n, dy = (ty - u.y) / n;
      u.dash7 = { fase: "preparo", t: D.preparo, dx, dy, comp };
      u.dashCd = D.recarga;
      u.virado = dx >= 0 ? 1 : -1;
      m.eventos.push({ tipo: "aviso", id: u.id, forma: { tipo: "faixa", x1: u.x, y1: u.y, x2: u.x + dx * comp, y2: u.y + dy * comp, largura: D.largura },
        preparo: D.preparo, lider: true, investida: true });
      return true;
    }
  }
  return false;
}

function investida(m, u, dt) {
  const D = u.def.investida7, g = u.dash7;
  g.t -= dt;
  u.vx = u.vy = 0;
  if (g.fase === "preparo") {
    if (g.t > 0) return true;
    g.fase = "exec"; g.t = g.comp / D.vel;
    m.eventos.push({ tipo: "investidaSai", id: u.id, x: u.x, y: u.y, dx: g.dx, dy: g.dy });
    return true;
  }
  if (g.fase === "exec") {
    u.vx = g.dx * D.vel; u.vy = g.dy * D.vel;
    u.virado = g.dx >= 0 ? 1 : -1;
    let fim = g.t <= 0 || !!dentroObstaculo(m, u.x + g.dx * (u.raio + 4), u.y + g.dy * (u.raio + 4), 0);
    if (!fim) {
      for (const v of m.lados[1 - u.lado]) {
        if (v.morto || dist2(u, v) > (u.raio + v.raio + 3) ** 2 || (v.x - u.x) * g.dx + (v.y - u.y) * g.dy < 0) continue;
        S.ferir(m, v, v === m.heroi ? D.danoHeroi : D.dano, u, { dx: g.dx, dy: g.dy, emp: D.empurrao, forte: true, hab: "investidaCurta" });
        if (heroico(m, v)) aplicarControle(m, v, "interrupcao", CONTROLE.interrompe, u);
        m.eventos.push({ tipo: "investidaAcerta", x: v.x, y: v.y, dx: g.dx, dy: g.dy, heroi: v === m.heroi });
        m.stats.investidas = (m.stats.investidas || 0) + 1;
        fim = true;
        break;
      }
    }
    if (fim) { g.fase = "rec"; g.t = D.recupera; u.vx = u.vy = 0; u.vulneravel = D.recupera; u.cravado = D.recupera; }
    return true;
  }
  // a recuperação: parado, levando +50% (a abertura para responder)
  if (g.t <= 0) { u.dash7 = null; u.reavaliar = 0; }
  return true;
}

// ------------------------------------------------------------------------------------------------ Morel: o Desafio
/**
 * O Desafio: um herói inimigo pressionando você ou Odette (a até 80 px dele, ou que feriu há pouco, ou com o protegido
 * abaixo da metade da vida), à vista e a até `alcance` px de Morel, e Morel com vida para aguentar. Devolve true se usou.
 */
export function desafioMorel(m, u) {
  const D = u.def.desafio, h = m.heroi, od = m.odette;
  if (u.desafioCd > 0 || u.vida < u.vidaMax * D.vidaMin) return false;
  for (const e of [m.lider, m.ardis]) {
    if (!e || e.morto || !e.def.focoIA) continue;
    const w = e.focoU;
    if (!w || w.morto || (w !== h && w !== od) || e.provocacao && e.provocacao.ate > m.t) continue;
    const pressiona = dist2(e, w) < 80 * 80 || lembrado(w.dor, e.id, m.t) >= 15 || w.vida < w.vidaMax * 0.5;
    if (!pressiona || dist2(u, e) > D.alcance * D.alcance || bloqueado(m, u.x, u.y, e.x, e.y, true)) continue;
    const ok = aplicarControle(m, e, "provocacao", D.dura, u);
    u.desafioCd = D.recarga;
    if (!ok) continue;
    u.posturaAte = m.t + ok;
    u.alvo = e;
    m.eventos.push({ tipo: "desafio", id: u.id, alvo: e.id, x: u.x, y: u.y, dura: ok });
    S.registrar(m, `Morel desafia ${e.def.nome.split(",")[0]} para proteger ${w === h ? "você" : "Odette"} (${num(ok)} s).`);
    m.stats.desafios = (m.stats.desafios || 0) + 1;
    return true;
  }
  return false;
}

// ------------------------------------------------------------------------------------------------ a Escudada
/** A infantaria pesada empurra e deixa lento um herói (ou uma ameaça) colado na frente dela. */
export function escudada(m, u, dt) {
  const E = u.def.escudada;
  u.escudadaCd = (u.escudadaCd ?? 2 + (u.id % 4)) - dt;
  if (u.escudadaCd > 0 || u.acao) return false;
  for (const v of m.lados[1 - u.lado]) {
    if (v.morto || !heroico(m, v) || dist2(u, v) > (u.raio + v.raio + E.alcance) ** 2 || (Math.sign(v.x - u.x) || 1) !== u.virado) continue;
    const dx = v.x - u.x, dy = v.y - u.y, n = Math.hypot(dx, dy) || 1;
    S.ferir(m, v, E.dano, u, { dx: dx / n, dy: dy / n, emp: E.empurrao, hab: "escudada" });
    aplicarControle(m, v, "lento", E.lento.dura, u, { fator: E.lento.fator });
    u.escudadaCd = E.recarga;
    m.eventos.push({ tipo: "escudada", x: v.x, y: v.y, dx: dx / n, dy: dy / n });
    return true;
  }
  return false;
}
