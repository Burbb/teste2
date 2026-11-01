// PROTÓTIPO de campo livre (nada no jogo), Campo Livre 9: a guerra nova. Sem DOM. As razões estão em roadmapIDEIAS/34;
// os números, em conteudo.js (HARG9, ARDIS9, VESNA9, GENERAL9, VARIACOES, PELOTOES).
//
// - As ondas: cada uma sorteia um pelotão (soldados e lanceiros, furiosos e cães, besteiros atrás dos pesados,
//   sapadores no meio da infantaria, a matilha, cavalaria, infantaria e arqueiros) e entra por um lado.
// - Os heróis inimigos (Harg, Ardis, Vesna) entram em tempos marcados, na ordem sorteada, cada um com variações
//   sorteadas (gélido, inabalável, venenoso, rastro explosivo, vampírico, implacável). São frágeis e letais.
// - O General: só quando as ondas acabaram, os três heróis caíram e não sobrou ninguém do lado inimigo. A guerra acaba
//   quando ele cai (ou você). Ninguém foge (`m.semFuga`).
// - O sapador: leva o barril até os nossos, acende o pavio e explode; derrubado, o barril cai e explode ferindo qualquer
//   lado (as cargas ficam em `m.g9.cargas`, junto com as do rastro explosivo).
// O sorteio da guerra (as ondas, a ordem dos heróis, as variações) usa um gerador próprio (`m.g9.r`): a mesma luta com
// o mesmo sorteio e a mesma semente sai igual.
import { TIPOS, VARIACOES, PELOTOES, HEROIS9, HARG9, ARDIS9, VESNA9, GENERAL9, CAMPO, HORDA } from "./conteudo.js";
import { prepararHarg8 } from "./campo8.js";
import { aplicarControle } from "./campo7.js";
import { pontoLivre, bloqueado } from "./navegacao.js";

let S = null;    // as funções de sim.js (ferir, novaUnidade, registrar, andarPara, sorteio)
export function ligar9(h) { S = h; }

const dist2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;
const num = (v) => String(Math.round(v * 10) / 10).replace(".", ",");
const CFG = { lider: HARG9, vesna: VESNA9, general: GENERAL9 };

// ------------------------------------------------------------------------------------------------ a preparação
/** Ao criar o encontro: o sorteio das ondas, da ordem dos heróis e das variações. */
export function prepararGuerra9(m, enc, numero) {
  const r = S.sorteio(numero), ids = Object.keys(HEROIS9);
  // a ordem dos heróis e as variações de cada um (sem repetir variação no mesmo herói)
  for (let i = ids.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [ids[i], ids[j]] = [ids[j], ids[i]]; }
  const H = enc.herois9 || { entradas: [] };
  const herois = H.entradas.map((e, i) => {
    const vs = Object.keys(VARIACOES);
    const variacoes = [];
    for (let k = 0; k < e.variacoes; k++) variacoes.push(vs.splice(Math.floor(r() * vs.length), 1)[0]);
    return { ...e, id: ids[i % ids.length], variacoes, entrou: false, u: null, caiuT: null };
  });
  m.semFuga = !!enc.semFuga;
  m.g9 = { r, sorteio: numero, ondas: enc.ondas9 ? { ...enc.ondas9, proxima: enc.ondas9.primeira ?? enc.ondas9.cada, i: 0 } : null,
    herois, heroisCfg: H, general: enc.general ? { ...enc.general, estado: "espera", vazioT: null, u: null } : null,
    cargas: [], envenenados: new Set(), pelotoes: [] };
  m.stats.pelotoes = {};
}

// ------------------------------------------------------------------------------------------------ o passo
/** Uma vez por passo do mundo (depois das levas). */
export function passo9(m, dt) {
  const g9 = m.g9;
  if (m.fase === "luta" && !m.fimEm) {
    if (g9.ondas) chegarOnda(m, g9.ondas);
    entrarHerois(m, g9);
    if (g9.general) chamarGeneral(m, g9);
  }
  for (const u of m.lados[1]) if (u.afixos && !u.morto) variacoesNoPasso(m, u, dt);
  envenenar(m, dt);
  cargas(m, dt);
  // a barra de cima: o General; senão, o herói inimigo com a máquina de golpes mais perto de você (fica o mesmo
  // enquanto estiver de pé, para a barra não pular)
  const gen = g9.general && g9.general.u;
  if (gen && !gen.morto) m.chefe = gen;
  else if (!m.chefe || m.chefe.morto) {
    let melhor = null, dm = Infinity;
    for (const u of m.lados[1]) if (u.heroi9 && u.h8 && !u.morto && dist2(u, m.heroi) < dm) { dm = dist2(u, m.heroi); melhor = u; }
    m.chefe = melhor;
  }
}

function chegarOnda(m, o) {
  if (m.t < o.proxima || m.t > o.ate) return;
  const lado = o.lados[o.i % o.lados.length], p = o.pontos[lado];
  const ids = Object.keys(PELOTOES), id = ids[Math.floor(m.g9.r() * ids.length)], P = PELOTOES[id];
  o.i++;
  o.proxima += o.cada;
  const n = pelotaoEm(m, p[0], p[1], P.blocos);
  if (!n) return;
  m.g9.pelotoes.push(id);
  m.stats.pelotoes[id] = (m.stats.pelotoes[id] || 0) + 1;
  m.eventos.push({ tipo: "pelotao9", x: p[0], y: p[1], nome: P.nome, n });
  S.registrar(m, `Chega uma onda pelo ${lado === "portao" ? "portão" : lado}: ${P.nome.toLowerCase()} (${n}).`);
}

// um pelotão em bloco, perto de (px, py): cada tipo em colunas, o primeiro bloco na frente (para o lado do herói)
function pelotaoEm(m, px, py, blocos) {
  const k = m.escala, sentido = px >= m.heroi.x ? 1 : -1, g = CAMPO.margem + 4;
  let x = px, total = 0;
  for (const [tipo, q] of blocos) {
    const n = Math.min(q * k, HORDA.limite - m.unidades.length);
    if (n <= 0) continue;
    const cols = Math.max(1, Math.ceil(Math.sqrt(n / 2))), linhas = Math.ceil(n / cols), alt = (linhas - 1) * 11;
    const cy = Math.max(g + alt / 2, Math.min(CAMPO.altura - g - alt / 2, py));
    for (let i = 0; i < n; i++) {
      const col = i % cols, lin = Math.floor(i / cols);
      const p = pontoLivre(m, x + col * 11 * sentido + (m.g9.r() - 0.5) * 3, cy + (lin - (linhas - 1) / 2) * 11 + (m.g9.r() - 0.5) * 3, 4);
      const u = S.novaUnidade(m, 1, tipo, Math.max(g, Math.min(CAMPO.largura - g, p.x)), Math.max(g, Math.min(CAMPO.altura - g, p.y)));
      u.px = u.x; u.py = u.y;
    }
    x += (cols + 1) * 11 * sentido;
    total += n;
  }
  m.stats.inimigos += total;
  return total;
}

function entrarHerois(m, g9) {
  const H = g9.heroisCfg;
  for (let i = 0; i < g9.herois.length; i++) {
    const e = g9.herois[i];
    if (e.entrou) continue;
    if (H.seguidos) {
      const antes = g9.herois[i - 1];
      const pronto = antes ? antes.caiuT != null && m.t >= antes.caiuT + H.espera : m.t >= H.espera;
      if (!pronto) return;
    } else if (m.t < e.t) continue;
    entrarHeroi(m, e, H.ponto);
    if (H.seguidos) return;
  }
}

function entrarHeroi(m, e, ponto) {
  const tipo = HEROIS9[e.id].tipo, p = pontoLivre(m, ponto[0], ponto[1], 6);
  const u = S.novaUnidade(m, 1, tipo, p.x, p.y);
  if (tipo === "ardis") {
    u.def = { ...TIPOS.ardis, ...ARDIS9 };
    u.vida = u.vidaMax = ARDIS9.vida;
    m.ardis = u;
  } else prepararHarg8(u, CFG[tipo]);
  if (tipo === "lider") m.lider = u;
  u.heroi9 = true;
  u.afixos = e.variacoes;
  for (const v of e.variacoes) {
    if (v === "inabalavel") { u.inabalavel = true; u.massa = 60; }
    if (v === "implacavel") {
      u.ritmo9 = VARIACOES.implacavel.ritmo; u.velF = VARIACOES.implacavel.vel;
      // Ardis foge de você: mais rápida que o seu herói, ninguém a alcançaria (fica abaixo dos 68 do Mago)
      if (tipo === "ardis") u.def = { ...u.def, vel: Math.min(62, u.def.vel * VARIACOES.implacavel.vel) };
    }
  }
  // no treino, a vida volta cheia a cada herói: cada um se aprende do começo
  if (m.g9.heroisCfg.seguidos && !m.heroi.morto) m.heroi.vida = m.heroi.vidaMax;
  e.entrou = true; e.u = u;
  m.stats.inimigos++;
  const nomes = e.variacoes.map((v) => VARIACOES[v].nome);
  m.eventos.push({ tipo: "heroi9Entra", id: u.id, nome: u.def.nome, variacoes: e.variacoes, nomes, x: u.x, y: u.y });
  S.registrar(m, `${u.def.nome} entra na batalha: ${nomes.join(", ").toLowerCase()}.`);
}

// o General: as ondas acabaram, os heróis caíram e o campo ficou vazio; `espera` s depois, ele atravessa o portão
function chamarGeneral(m, g9) {
  const G = g9.general;
  if (G.estado !== "espera") return;
  const ondasFim = !g9.ondas || g9.ondas.proxima > g9.ondas.ate;   // nenhuma onda marcada para depois
  const heroisFim = g9.herois.every((e) => e.entrou && e.u.morto);
  if (!ondasFim || !heroisFim || m.lados[1].some((u) => !u.morto)) { G.vazioT = null; return; }
  if (G.vazioT == null) {
    G.vazioT = m.t;
    m.eventos.push({ tipo: "general9Vem" });
    S.registrar(m, "O campo ficou vazio. Alguém atravessa o portão.");
    return;
  }
  if (m.t < G.vazioT + G.espera) return;
  const p = pontoLivre(m, G.ponto[0], G.ponto[1], 10), u = S.novaUnidade(m, 1, "general", p.x, p.y);
  prepararHarg8(u, GENERAL9);
  u.heroi9 = true; u.general = true;
  G.u = u; G.estado = "veio"; G.veioT = m.t;
  if (m.g9.heroisCfg.seguidos && !m.heroi.morto) m.heroi.vida = m.heroi.vidaMax;
  m.stats.inimigos++;
  m.eventos.push({ tipo: "general9Entra", id: u.id, nome: u.def.nome, x: u.x, y: u.y });
  S.registrar(m, `${u.def.nome} entra na batalha.`);
}

// ------------------------------------------------------------------------------------------------ as variações
function variacoesNoPasso(m, u, dt) {
  const A = u.afixos;
  if (u.inabalavel) {
    // nada o prende: os controles que outra regra pôs neste passo somem antes de ele agir
    u.atordoado = 0; u.imobAte = 0; u.gelo = 0; u.lentoAte = 0; u.provocacao = null; u.abalado = 0; u.congelado = 0;
  }
  if (u.ritmo9 && u.tipo === "ardis") {
    for (const k of ["dardoCd", "colunaCd", "passoCd", "correnteCd", "barreiraCd", "grilhaoCd"]) if (u[k] != null) u[k] -= dt * (u.ritmo9 - 1);
  }
  if (A.includes("explosivo")) rastro(m, u);
}

// o rastro explosivo: quem corre mais de 300 px/s (a investida, o bote) deixa uma carga a cada `espaco` px; quem some
// (o passo de Ardis, o recuo de Vesna) deixa três em volta de onde estava
function rastro(m, u) {
  const V = VARIACOES.explosivo, r = u.rastro9 || (u.rastro9 = { x: u.x, y: u.y, resto: 0 });
  const d = Math.hypot(u.x - r.x, u.y - r.y);
  if (d > 40) {
    for (let i = 0; i < 3; i++) {
      const a = (i / 3) * Math.PI * 2 + 0.5;
      novaCarga(m, u, r.x + Math.cos(a) * 9, r.y + Math.sin(a) * 9, V, 0);
    }
    r.resto = 0;
  } else if (d > 5) {
    r.resto += d;
    while (r.resto >= V.espaco) {
      r.resto -= V.espaco;
      const k = r.resto / d;
      novaCarga(m, u, u.x - (u.x - r.x) * k, u.y - (u.y - r.y) * k, V, 0);
    }
  } else r.resto = 0;
  r.x = u.x; r.y = u.y;
}

// uma carga no chão: o círculo aparece e explode `arma` s depois; `alvo` 0 fere os nossos, "todos" fere qualquer lado
function novaCarga(m, fonte, x, y, C, alvo, extra = {}) {
  const c = { x, y, raio: C.raio, t: 0, dur: C.arma, dano: C.dano, danoHeroi: C.danoHeroi, emp: C.empurrao, atord: C.atordoa || 0,
    alvo, fonte, ...extra };
  m.g9.cargas.push(c);
  return c;
}

function cargas(m, dt) {
  const fica = [];
  for (const c of m.g9.cargas) {
    c.t += dt;
    if (c.t < c.dur) { fica.push(c); continue; }
    const lados = c.alvo === "todos" ? [m.lados[0], m.lados[1]] : [m.lados[c.alvo]];
    let n = 0;
    for (const lado of lados) for (const v of lado) {
      // a mesma regra do círculo desenhado no chão (o pé dentro do círculo)
      if (v.morto || v === c.dono || (v.x - c.x) ** 2 + (v.y - c.y) ** 2 > c.raio ** 2) continue;
      if (bloqueado(m, c.x, c.y, v.x, v.y, true)) continue;
      const dx = v.x - c.x, dy = v.y - c.y, d = Math.hypot(dx, dy) || 1, heroico = v === m.heroi || v.def.elite;
      S.ferir(m, v, heroico ? c.danoHeroi : c.dano, c.fonte, { dx: dx / d, dy: dy / d, emp: c.emp, atord: c.atord, forte: c.emp > 100, hab: "carga9" });
      n++;
    }
    m.eventos.push({ tipo: "explosao", x: c.x, y: c.y, raio: c.raio, de: "ignicao" });
    if (c.dono && !c.dono.morto) { c.dono.barril9 = null; c.dono.estourou = true; S.ferir(m, c.dono, 999, c.dono, { hab: "carga9" }); }
    if (c.barril) m.stats.barris = (m.stats.barris || 0) + n;
    else m.stats.cargas = (m.stats.cargas || 0) + n;
  }
  m.g9.cargas = fica;
}

/** sim.ferir chama depois do dano: o que as variações de quem bateu deixam (o gelo, o veneno, a cura). */
export function aoAcertar9(m, fonte, u, dano, o) {
  if (u.lado === fonte.lado || dano <= 0 || o.sutil || o.hab === "carga9") return;
  const A = fonte.afixos;
  if (A.includes("vampirico") && !fonte.morto) {
    const c = Math.min(fonte.vidaMax - fonte.vida, dano * VARIACOES.vampirico.cura);
    if (c > 0) { fonte.vida += c; m.stats.vampirico = (m.stats.vampirico || 0) + c; m.eventos.push({ tipo: "cura9", x: fonte.x, y: fonte.y, valor: c }); }
  }
  if (u.vida <= 0 || u.morto) return;
  const heroico = u === m.heroi || u.def.elite;
  if (A.includes("gelido")) {
    const G = VARIACOES.gelido;
    if (heroico) {
      if (m.t - (u.gelo9 ?? -99) <= G.janela) {
        u.gelo9 = -99;
        if (aplicarControle(m, u, "atordoado", G.congela, fonte) > 0) {
          u.congelado9 = m.t + G.congela;
          m.eventos.push({ tipo: "congela9", x: u.x, y: u.y, id: u.id, heroi: u === m.heroi });
        }
      } else {
        u.gelo9 = m.t;
        aplicarControle(m, u, "lento", G.lento.dura, fonte, { fator: G.lento.fator });
      }
    } else {
      u.atordoado = Math.max(u.atordoado || 0, G.congelaTropa);
      u.congelado9 = m.t + G.congelaTropa;
      m.eventos.push({ tipo: "congela", x: u.x, y: u.y });
    }
  }
  if (A.includes("venenoso")) {
    const V = VARIACOES.venenoso.veneno, v = u.veneno9 || (u.veneno9 = { doses: 0, ate: 0, tick: V.cada, fonte });
    if (m.t > v.ate) { v.doses = 0; v.tick = V.cada; }
    v.doses = Math.min(V.max, v.doses + 1);
    v.ate = m.t + V.dura;
    v.fonte = fonte;
    m.g9.envenenados.add(u);
  }
}

function envenenar(m, dt) {
  const V = VARIACOES.venenoso.veneno;
  for (const u of m.g9.envenenados) {
    const v = u.veneno9;
    if (u.morto || m.t > v.ate) { m.g9.envenenados.delete(u); continue; }
    v.tick -= dt;
    if (v.tick > 0) continue;
    v.tick += V.cada;
    const dano = V.tique * v.doses;
    S.ferir(m, u, dano, v.fonte, { sutil: true, hab: "veneno9", tipoDano: "continuo" });
    m.stats.veneno = (m.stats.veneno || 0) + dano;
    m.eventos.push({ tipo: "veneno9", x: u.x, y: u.y, heroi: u === m.heroi, valor: dano });
  }
}

// ------------------------------------------------------------------------------------------------ o sapador
/** O sapador decide e age (sim chama para quem tem `especial9`). Devolve true quando cuidou do passo. */
export function sapador9(m, u, dt) {
  const B = u.def.barril;
  if (u.barril9) { u.vx = u.vy = 0; return true; }   // o pavio aceso: parado até explodir
  if (m.fase !== "luta") return false;
  u.reavaliar9 = (u.reavaliar9 ?? 0) - dt;
  if (u.reavaliar9 <= 0 || !u.alvo9 || u.alvo9.morto) {
    u.reavaliar9 = 0.5;
    let melhor = null, dm = B.busca * B.busca;
    for (const v of m.lados[0]) if (!v.morto && dist2(u, v) < dm) { dm = dist2(u, v); melhor = v; }
    u.alvo9 = melhor;
  }
  const a = u.alvo9;
  if (!a) return false;   // ninguém ao alcance: anda como a infantaria
  const d = Math.sqrt(dist2(u, a));
  if (d > u.raio + a.raio + B.perto) { S.andarPara(u, a.x, a.y, u.def.vel); return true; }
  // acende o pavio: o círculo no chão, a explosão fere os nossos e o derruba
  u.vx = u.vy = 0;
  u.barril9 = novaCarga(m, u, u.x, u.y, { ...B, arma: B.arma }, 0, { dono: u, barril: true });
  m.eventos.push({ tipo: "pavio9", x: u.x, y: u.y, id: u.id });
  return true;
}

/** sim.morrer chama para quem cai: o barril do sapador, os heróis inimigos e o General. */
export function aoCair9(m, u) {
  if (u.def.barril && !u.estourou) {
    // derrubado, o barril cai e explode logo depois, ferindo qualquer lado (o pavio aceso vira o barril caído)
    if (u.barril9) m.g9.cargas = m.g9.cargas.filter((c) => c !== u.barril9);
    const B = u.def.barril;
    novaCarga(m, u, u.x, u.y, { ...B, arma: B.cai }, "todos", { barril: true, caido: true });
    m.eventos.push({ tipo: "barril9", x: u.x, y: u.y });
  }
  if (!u.heroi9) return;
  const e = m.g9.herois.find((h) => h.u === u);
  if (e) e.caiuT = m.t;
  if (u === m.lider) m.lider = null;
  if (u === m.chefe) m.chefe = null;
  m.eventos.push({ tipo: "heroi9Caiu", id: u.id, nome: u.def.nome, x: u.x, y: u.y, general: !!u.general });
  S.registrar(m, `${u.def.nome} caiu.`);
  // a vitória, uma vez, e só se você ainda está de pé (caído antes, a derrota já valeu)
  if (u.general && !m.resultado) {
    m.resultado = "vitoria";
    m.fimEm = m.t + 3;
    m.stats.generalT = m.t - m.g9.general.veioT;
  }
}

/** O que a tela mostra de um herói inimigo da guerra: as variações (o nome e a cor), prontas. */
export function variacoesDe(u) {
  return (u && u.afixos || []).map((v) => ({ id: v, nome: VARIACOES[v].nome, cor: VARIACOES[v].cor }));
}

/** O texto da primeira vez de cada variação (a tela mostra numa faixa). */
export function explicacao9(v) { return VARIACOES[v] && VARIACOES[v].explica; }

/** O que sobra da guerra para o fim e o diagnóstico: o sorteio, as ondas e os heróis (com as variações). */
export function resumo9(m) {
  const g9 = m.g9;
  if (!g9) return null;
  return { sorteio: g9.sorteio, pelotoes: g9.pelotoes.map((p) => PELOTOES[p].nome),
    herois: g9.herois.map((e) => ({ nome: TIPOS[HEROIS9[e.id].tipo].nome, variacoes: e.variacoes.map((v) => VARIACOES[v].nome),
      entrou: e.entrou, caiu: e.caiuT != null ? num(e.caiuT) : null })),
    general: g9.general ? g9.general.estado : null };
}

/** A guerra em uma linha, pronta para a tela: a fase (ondas, limpar, vem, general, fim), as ondas que já vieram, os
 *  heróis caídos, quantos inimigos faltam (antes do General) e o número do sorteio. */
export function estado9(m) {
  const g9 = m.g9;
  if (!g9) return null;
  const o = g9.ondas, total = o ? Math.floor((o.ate - (o.primeira ?? o.cada)) / o.cada) + 1 : 0, feitas = o ? o.i : 0;
  const H = g9.herois, caidos = H.filter((e) => e.caiuT != null).length, G = g9.general;
  const restam = m.lados[1].filter((u) => !u.morto && !u.general).length;
  const ondasFim = !o || o.proxima > o.ate;
  let fase, texto;
  if (G && G.estado === "veio") { fase = G.u.morto ? "fim" : "general"; texto = G.u.morto ? `${G.u.def.nome} caiu` : `${G.u.def.nome}: derrube-o para vencer`; }
  else if (G && G.vazioT != null) { fase = "vem"; texto = "Campo vazio: o General atravessa o portão"; }
  else if (ondasFim && caidos === H.length) { fase = "limpar"; texto = restam === 1 ? "Falta 1 inimigo; depois, o General" : `Faltam ${restam} inimigos; depois, o General`; }
  else {
    fase = "ondas";
    texto = (o ? `Ondas ${feitas} de ${total} · ` : "") + `heróis inimigos caídos: ${caidos} de ${H.length}`;
  }
  return { fase, texto, sorteio: g9.sorteio, restam, ondas: { feitas, total }, herois: { caidos, total: H.length } };
}

/** Os heróis inimigos de pé agora (na ordem em que entraram) e o General: os que a barra de cima mostra. */
export function chefes9(m) {
  const g9 = m.g9;
  if (!g9) return [];
  const gen = g9.general && g9.general.u;
  if (gen && !gen.morto) return [gen];
  return g9.herois.filter((e) => e.entrou && !e.u.morto).map((e) => e.u);
}
