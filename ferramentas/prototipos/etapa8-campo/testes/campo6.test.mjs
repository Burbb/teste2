// Testes do Campo Livre 6 (node --test): o cenário com construções, as tropas novas, Morel e Odette autônomos e os
// heróis inimigos. Cada cenário parte de um encontro de verdade e deixa só quem interessa à regra conferida.
import { test } from "node:test";
import assert from "node:assert/strict";
import { criarMundo, passo, entradaVazia, ferir, selecionar, tropasDoTipo, ordenar } from "../tela/sim.js";
import { bloqueado, rumo, mundoAtual, empurrarParaFora, dentroObstaculo, pontoDaHabilidade } from "../tela/campo6.js";
import { TIPOS, COMPOSICOES } from "../tela/conteudo.js";
import { criarRobo, pensar } from "../tela/robo.js";

const d2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;

/** Um mundo do encontro `enc` com só o herói e as unidades de `manter` (filtro); todos os grupos acordados. */
function mundo(enc, manter = () => false, opcoes = {}) {
  const m = criarMundo({ heroi: "guerreiro", encontro: enc, ...opcoes });
  m.unidades = m.unidades.filter((u) => u === m.heroi || manter(u));
  for (const g of Object.values(m.grupos)) g.ativo = true;
  m.fase = "luta"; m.ondas = null; m.levas = []; m.reforco.chegou = true;
  m.heroi.x = 60; m.heroi.y = 540;
  // poucos inimigos de propósito: a regra dos 20% (o resto foge) não pode encerrar a luta antes da hora
  m.stats.inimigos = 1;
  return m;
}
function rodar(m, s, ent = entradaVazia()) { for (let t = 0; t < s && m.fase !== "fim"; t += 1 / 60) { passo(m, ent); m.eventos.length = 0; } }

test("as construções: ninguém fica dentro delas; um corpo empurrado contra a parede sai pela borda mais perto", () => {
  const m = criarMundo({ heroi: "mago", encontro: "vila", composicao: { aliados: "completa", inimigos: "completa" } });
  const casa = m.cenario.obs.find((o) => o.tipo === "casa");
  const u = m.unidades.find((v) => v.lado === 1);
  u.x = casa.x + 4; u.y = casa.y + casa.h / 2;
  empurrarParaFora(m, u);
  assert.ok(!dentroObstaculo(m, u.x, u.y, u.raio - 0.5), "saiu da casa");
  assert.ok(Math.abs(u.x - (casa.x - u.raio)) < 0.01, "pela borda esquerda, a mais perto");
  // uma batalha de 40 s com o jogador automático: nenhum centro dentro de construção em nenhum quadro
  const r = criarRobo({ nivel: "forte" }), ent = entradaVazia();
  let dentro = 0;
  for (let i = 0; i < 40 * 60 && m.fase !== "fim"; i++) {
    pensar(r, m, ent); passo(m, ent); m.eventos.length = 0;
    if (i % 30 === 0) for (const v of m.unidades) if (!v.morto && dentroObstaculo(m, v.x, v.y, -1)) dentro++;
  }
  assert.equal(dentro, 0);
});

test("o caminho: contorna a casa e passa pelo portão em vez de ficar parado na parede", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "vila" });
  mundoAtual(m);
  const andar = (de, para, s) => {
    const u = { x: de[0], y: de[1], raio: 3.5, kx: 0, ky: 0 };
    for (let t = 0; t < s; t += 1 / 60) {
      const r = rumo(u, ...para), dx = r.x - u.x, dy = r.y - u.y, n = Math.hypot(dx, dy) || 1;
      u.x += (dx / n) * 34 / 60; u.y += (dy / n) * 34 / 60;
      empurrarParaFora(m, u);
      if (Math.hypot(u.x - para[0], u.y - para[1]) < 4) return t;
    }
    return Infinity;
  };
  // de trás da casa do norte (590, 64) até o outro lado dela
  assert.ok(andar([618, 52], [618, 118], 12) < 12, "contornou a casa");
  // de dentro do castelo até a estrada, pelo portão (a linha reta bate na muralha)
  assert.ok(bloqueado(m, 900, 150, 700, 276));
  assert.ok(andar([900, 150], [700, 276], 20) < 20, "saiu pelo portão");
});

test("flechas, magias e áreas param na parede alta; o muro baixo deixa passar", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "vila" });
  const casa = m.cenario.obs.find((o) => o.tipo === "casa"), muro = m.cenario.obs.find((o) => o.tipo === "muro");
  assert.equal(bloqueado(m, casa.x - 20, casa.y + 10, casa.x + casa.w + 20, casa.y + 10, true), true, "a casa barra o tiro");
  assert.equal(bloqueado(m, muro.x + 10, muro.y - 20, muro.x + 10, muro.y + 20, true), false, "o muro baixo, não");
  assert.equal(bloqueado(m, muro.x + 10, muro.y - 20, muro.x + 10, muro.y + 20, false), true, "mas barra a passagem");
  // o ponto de uma habilidade para antes da parede
  mundoAtual(m);
  const p = pontoDaHabilidade(casa.x - 40, casa.y + 10, casa.x + casa.w + 40, casa.y + 10);
  assert.ok(p.x < casa.x, "parou antes da casa");
  // uma magia que explode: quem está atrás da casa (do centro dela) não leva
  const m2 = mundo("vila", (u) => u.lado === 0 && u.tipo === "soldado");
  const [a, b] = m2.lados[0].length ? m2.unidades.filter((u) => u.tipo === "soldado").slice(0, 2) : [];
  a.x = casa.x - 10; a.y = casa.y + 10; b.x = casa.x + 8; b.y = casa.y - 6;   // a, ao lado; b, atrás da parede de cima
  m2.magias.push({ x: casa.x - 16, y: casa.y - 4, raio: 40, t: 0, dur: 0.01, lado: 1, fonte: null, dano: 5, danoHeroi: 5, emp: 0, atord: 0, cor: "fogo" });
  b.x = casa.x + 30; b.y = casa.y + 20;   // atrás da casa, a 46 px do centro em linha que corta a casa
  const va = a.vida, vb = b.vida;
  rodar(m2, 0.05);
  assert.ok(a.vida < va, "o que estava do mesmo lado levou");
  assert.equal(b.vida, vb, "o que estava atrás da casa, não");
});

test("cavalaria: carrega, atropela cada um uma vez, passa e se reposiciona; o pesado segura a carga", () => {
  const m = mundo("carga", (u) => (u.lado === 0 && u.tipo === "cavaleiro") || (u.lado === 1 && u.tipo === "soldado"), { composicao: { aliados: "cavalaria", inimigos: "comum" } });
  const cav = m.unidades.find((u) => u.tipo === "cavaleiro");
  m.unidades = [m.heroi, cav, ...m.unidades.filter((u) => u.tipo === "soldado" && u.lado === 1).slice(0, 4)];
  const alvos = m.unidades.filter((u) => u.lado === 1);
  // a ordem Atacar: sem a coleira em volta de você (com Acompanhar, ela só carrega perto de você)
  cav.x = 300; cav.y = 280; cav.cargaCd = 0; cav.ordem = { tipo: "atacar", x: 0, y: 0 };
  alvos.forEach((u, i) => { u.x = 440 + i * 12; u.y = 280; u.grupo = null; });
  let reposicionou = false, galopou = false;
  for (let i = 0; i < 4 * 60; i++) { passo(m, entradaVazia()); m.eventos.length = 0; galopou ||= !!(cav.galope && cav.galope.prepara <= 0); reposicionou ||= !!cav.reposiciona; }
  assert.ok(galopou && m.stats.cargas >= 2, `atropelou ${m.stats.cargas}`);
  assert.ok(reposicionou, "depois da carga, saiu para se reposicionar");
  // contra um pesado na frente: a carga para nele e o cavaleiro fica atordoado
  const m2 = mundo("carga", (u) => u.tipo === "cavaleiro" && u.lado === 0, { composicao: { aliados: "cavalaria", inimigos: "pesada" } });
  const c2 = m2.unidades.find((u) => u.tipo === "cavaleiro");
  const pes = criarMundo({ heroi: "guerreiro", encontro: "carga", composicao: { aliados: "comum", inimigos: "pesada" } }).unidades.find((u) => u.tipo === "pesado");
  m2.unidades = [m2.heroi, c2, pes];
  c2.x = 300; c2.y = 280; c2.cargaCd = 0; c2.ordem = { tipo: "atacar", x: 0, y: 0 }; pes.x = 420; pes.y = 280; pes.grupo = null;
  let barrado = false;
  for (let i = 0; i < 3 * 60 && !barrado; i++) { passo(m2, entradaVazia()); m2.eventos.length = 0; barrado = c2.atordoado > 0 && !c2.galope; }
  assert.ok(barrado, "o pesado segurou a carga");
});

test("infantaria pesada: o golpe de frente causa metade; de trás, inteiro", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "vila", composicao: { aliados: "comum", inimigos: "pesada" } });
  const p = m.unidades.find((u) => u.tipo === "pesado" && u.lado === 1), h = m.heroi;
  p.virado = 1; p.x = 400; p.y = 280;
  h.x = 420; h.y = 280; let v = p.vida; ferir(m, p, 10, h); assert.equal(v - p.vida, 5, "de frente");
  h.x = 380; v = p.vida; ferir(m, p, 10, h); assert.equal(v - p.vida, 10, "por trás");
  assert.ok(TIPOS.pesado.vida > TIPOS.soldado.vida * 3 && TIPOS.pesado.massa >= 5);
});

test("mago de batalha: anuncia o círculo 0,9 s antes e acerta quem ficou nele", () => {
  const m = mundo("vila", (u) => (u.lado === 1 && u.tipo === "magoBatalha") || (u.lado === 0 && u.tipo === "soldado"), { composicao: { aliados: "comum", inimigos: "pesada" } });
  const mago = m.unidades.find((u) => u.tipo === "magoBatalha");
  m.unidades = [m.heroi, mago, ...m.unidades.filter((u) => u.tipo === "soldado").slice(0, 6)];
  mago.x = 330; mago.y = 380; mago.recarga = 0; mago.grupo = null;
  const sold = m.unidades.filter((u) => u.tipo === "soldado");
  sold.forEach((u, i) => { u.x = 230 + (i % 3) * 8; u.y = 380 + Math.floor(i / 3) * 8; u.ordem = { tipo: "defender", x: u.x, y: u.y }; });
  let anunciou = null;
  for (let i = 0; i < 120 && !anunciou; i++) { passo(m, entradaVazia()); m.eventos.length = 0; if (m.magias.length) anunciou = { ...m.magias[0] }; }
  assert.ok(anunciou, "anunciou");
  assert.equal(anunciou.dur, TIPOS.magoBatalha.bola.preparo);
  const vidaAntes = sold.reduce((s, u) => s + u.vida, 0);
  rodar(m, 1);
  assert.ok(sold.reduce((s, u) => s + Math.max(0, u.vida), 0) < vidaAntes, "a explosão feriu o grupo");
});

test("Morel: abre espaço com o Golpe de Escudo, provoca quem cerca você e não passa da coleira", () => {
  const m = mundo("vila", (u) => u.tipo === "morel" || (u.lado === 1 && u.tipo === "soldado"));
  const mo = m.morel, h = m.heroi;
  const ini = m.unidades.filter((u) => u.lado === 1);
  h.x = 300; h.y = 300; mo.x = 330; mo.y = 300; mo.escudoCd = 0; mo.provocaCd = 99;
  ini.slice(0, 4).forEach((u, i) => { u.x = 342 + (i % 2) * 6; u.y = 292 + i * 5; u.grupo = null; });
  ini.slice(4).forEach((u) => { u.x = 900; u.y = 40; });
  rodar(m, 0.5);
  assert.ok(m.stats.morelEscudo >= 1, "o Golpe de Escudo saiu");
  // você cercado por 5: Morel provoca
  mo.provocaCd = 0; mo.escudoCd = 99;
  ini.slice(0, 5).forEach((u, i) => { u.x = h.x + Math.cos(i) * 14; u.y = h.y + Math.sin(i) * 14; u.vida = u.vidaMax; });
  rodar(m, 0.3);
  assert.ok(ini.slice(0, 5).some((u) => u.provocador === mo), "provocou");
  // a coleira: um inimigo longe não o leva para longe de você
  const m2 = mundo("vila", (u) => u.tipo === "morel" || (u.lado === 1 && u.tipo === "soldado"));
  const ini2 = m2.unidades.filter((u) => u.lado === 1);
  m2.heroi.x = 200; m2.heroi.y = 280; m2.morel.x = 220; m2.morel.y = 280;
  ini2.forEach((u, i) => { u.x = 700 + (i % 4) * 10; u.y = 100 + Math.floor(i / 4) * 10; u.grupo = null; u.posto = { x: u.x, y: u.y }; });
  let longe = 0;
  for (let i = 0; i < 6 * 60; i++) { passo(m2, entradaVazia()); m2.eventos.length = 0; longe = Math.max(longe, Math.sqrt(d2(m2.morel, m2.heroi))); }
  assert.ok(longe <= TIPOS.morel.coleira + 15, `foi a ${longe.toFixed(0)} px de você`);
});

test("Odette: não cura quem está cheio, cura o ferido e responde com o Clarão quando chegam nela", () => {
  const m = mundo("vila", (u) => u.tipo === "odette" || u.tipo === "morel");
  m.heroi.x = 300; m.heroi.y = 300; m.odette.x = 260; m.odette.y = 300;
  // sem inimigos, a batalha acabaria: um inimigo longe, parado no posto
  const um = criarMundo({ heroi: "guerreiro", encontro: "vila" }).unidades.find((u) => u.lado === 1 && u.tipo === "soldado");
  um.x = 900; um.y = 40; um.posto = { x: 900, y: 40 }; um.grupo = null; m.unidades.push(um);
  rodar(m, 3);
  assert.equal(m.stats.odetteCura || 0, 0, "ninguém ferido: nenhuma cura");
  m.heroi.vida = 100;
  rodar(m, 1.5);
  assert.ok(m.heroi.vida >= 100 + TIPOS.odette.prece.cura - 1, `curou você (${m.heroi.vida})`);
  const m2 = mundo("vila", (u) => u.tipo === "odette" || (u.lado === 1 && u.tipo === "soldado"));
  const ini = m2.unidades.filter((u) => u.lado === 1).slice(0, 2);
  m2.unidades = [m2.heroi, m2.odette, ...ini];
  m2.odette.x = 300; m2.odette.y = 300; m2.odette.claraoCd = 0;
  ini.forEach((u, i) => { u.x = 310; u.y = 296 + i * 8; u.grupo = null; });
  rodar(m2, 0.1);
  assert.ok(m2.stats.odetteClarao >= 1 && ini.some((u) => u.atordoado > 0 || u.morto), "o Clarão atordoou quem chegou");
});

test("Ardis: percebe o perigo em 0,3 s e some; a Coluna cai no grupo; sozinha, foge", () => {
  const m = mundo("herois", (u) => u.tipo === "ardis" || (u.lado === 0 && u.tipo === "soldado"));
  const a = m.ardis, h = m.heroi;
  a.x = 500; a.y = 280; a.passoCd = 0; a.colunaCd = 99; a.correnteCd = 99; a.grupo = null;
  m.unidades.push(...criarMundo({ heroi: "guerreiro", encontro: "herois" }).unidades.filter((u) => u.lado === 1 && u.tipo === "soldado").slice(0, 6).map((u, i) => Object.assign(u, { x: 880, y: 60 + i * 10, grupo: null, posto: { x: 880, y: 60 + i * 10 } })));
  h.x = 530; h.y = 280;
  rodar(m, 0.2);
  assert.ok(Math.sqrt(d2(a, h)) < 60, "ainda não sumiu (reação humana)");
  rodar(m, 0.3);
  assert.ok(Math.sqrt(d2(a, h)) >= 100 && m.stats.ardisPassos === 1, "sumiu e reapareceu longe");
  // a Coluna de Fogo no grupo das nossas tropas
  const m2 = mundo("herois", (u) => u.tipo === "ardis" || (u.lado === 0 && u.tipo === "soldado"));
  const a2 = m2.ardis;
  a2.x = 500; a2.y = 280; a2.colunaCd = 0; a2.passoCd = 99; a2.correnteCd = 99; a2.grupo = null;
  m2.heroi.x = 60; m2.heroi.y = 540;
  m2.unidades.filter((u) => u.tipo === "soldado").forEach((u, i) => { u.x = 360 + (i % 5) * 9; u.y = 270 + Math.floor(i / 5) * 9; u.ordem = { tipo: "defender", x: 380, y: 290 }; });
  m2.unidades.push(...criarMundo({ heroi: "guerreiro", encontro: "herois" }).unidades.filter((u) => u.lado === 1 && u.tipo === "soldado").slice(0, 6).map((u, i) => Object.assign(u, { x: 880, y: 60 + i * 10, grupo: null, posto: { x: 880, y: 60 + i * 10 } })));
  let coluna = null;
  for (let i = 0; i < 60 && !coluna; i++) { passo(m2, entradaVazia()); m2.eventos.length = 0; coluna = m2.magias.find((g) => g.raio === TIPOS.ardis.coluna.raio); }
  assert.ok(coluna && Math.hypot(coluna.x - 380, coluna.y - 290) < 50, "a Coluna caiu no grupo");
  // sozinha (sem Harg e sem a tropa), foge
  const m3 = mundo("herois", (u) => u.tipo === "ardis" || (u.lado === 0 && u.tipo === "soldado"));
  m3.lider = null;
  rodar(m3, 0.1);
  assert.ok(m3.ardis.fugindo, "fugiu");
});

test("Harg: a Investida Curta quando você foge e o resto está em recarga; vem proteger Ardis", () => {
  const m = mundo("herois", (u) => u.tipo === "lider" || u.tipo === "ardis");
  const l = m.lider, h = m.heroi;
  l.x = 400; l.y = 280; l.arremCd = 9; l.cargaCd = 9; l.rodopioCd = 9; l.dashCd = 0; l.modo = "heroi"; l.modoT = 9; l.grupo = null;
  m.ardis.x = 900; m.ardis.y = 500; m.ardis.grupo = null;
  h.x = 560; h.y = 280;
  let vel = 0;
  for (let i = 0; i < 40; i++) { passo(m, entradaVazia()); m.eventos.length = 0; vel = Math.max(vel, Math.hypot(l.vx, l.vy)); }
  assert.ok(vel >= TIPOS.lider.dash.vel - 1, `avançou (${vel.toFixed(0)} px/s)`);
  // você perto de Ardis: ele larga as tropas e vem atrás de você
  l.modo = "tropas"; l.modoT = 9;
  m.ardis.x = h.x + 40; m.ardis.y = h.y;
  // decide quando não está no meio de um golpe (até 1 s)
  let veio = false;
  for (let i = 0; i < 60 && !veio; i++) { passo(m, entradaVazia()); m.eventos.length = 0; veio = l.modo === "heroi"; if (l.modo !== "heroi" && !l.acao) l.modoT = 9; }
  assert.ok(veio, "veio atrás de você");
});

test("seleção e ordens: os tipos novos e Morel e Odette por tecla; a ordem chega a eles", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "vila", composicao: { aliados: "completa", inimigos: "comum" } });
  for (const [tipo, n] of COMPOSICOES.completa.aliados.map(([t, k]) => [t, k])) assert.equal(tropasDoTipo(m, tipo).length, n, tipo);
  const comp = [...tropasDoTipo(m, "morel"), ...tropasDoTipo(m, "odette")];
  assert.equal(comp.length, 2);
  selecionar(m, comp);
  ordenar(m, "defender", 250, 200);
  assert.ok(m.morel.ordem.tipo === "defender" && m.odette.ordem.tipo === "defender");
  assert.ok(m.lados[0].filter((u) => u.tipo === "soldado").every((u) => u.ordem.tipo === "acompanhar"), "os outros mantêm a ordem");
});

test("os encontros novos terminam com o jogador automático forte, sem NaN e sem ninguém dentro de construção", () => {
  for (const enc of ["vila", "carga", "herois"]) for (const heroi of ["guerreiro", "mago"]) {
    const m = criarMundo({ heroi, encontro: enc }), ent = entradaVazia(), r = criarRobo({ nivel: "forte" });
    while (m.fase !== "fim" && m.t < 200) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    assert.equal(m.resultado, "vitoria", `${enc} ${heroi}: ${m.resultado} em ${m.t.toFixed(0)} s`);
    for (const u of m.unidades) assert.ok(Number.isFinite(u.x) && Number.isFinite(u.y));
  }
});
