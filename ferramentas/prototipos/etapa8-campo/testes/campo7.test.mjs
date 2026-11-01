// Testes do Campo Livre 7 (node --test): a navegação (a rota, o desvio, a posição útil, o inacessível), a escolha de
// alvo dos heróis inimigos, a Investida Curta em três tempos, os controles com a proteção contra repetição e as
// provocações. Cada cenário parte de um encontro de verdade e deixa só quem interessa à regra conferida.
import { test } from "node:test";
import assert from "node:assert/strict";
import { criarMundo, passo, entradaVazia, ferir, ordenar, alvoAssistido, formaDaAcao } from "../tela/sim.js";
import { rumo, mundoAtual, bloqueado, dentroObstaculo, prepararCenario } from "../tela/campo6.js";
import { aplicarControle, estadoControle } from "../tela/campo7.js";
import { TIPOS, CONTROLE, CENARIOS } from "../tela/conteudo.js";
import { criarRobo, pensar } from "../tela/robo.js";

const d2 = (a, b) => (a.x - b.x) ** 2 + (a.y - b.y) ** 2;
const dist = (a, b) => Math.sqrt(d2(a, b));

function mundo(enc, manter = () => false, opcoes = {}) {
  const m = criarMundo({ heroi: "guerreiro", encontro: enc, ...opcoes });
  m.unidades = m.unidades.filter((u) => u === m.heroi || manter(u));
  for (const g of Object.values(m.grupos)) g.ativo = true;
  m.fase = "luta"; m.ondas = null; m.levas = []; m.reforco.chegou = true;
  m.heroi.x = 60; m.heroi.y = 540;
  m.stats.inimigos = 1;
  return m;
}
function rodar(m, s, ent = entradaVazia(), cada = null) {
  for (let t = 0; t < s && m.fase !== "fim"; t += 1 / 60) { passo(m, ent); if (cada) cada(m); m.eventos.length = 0; }
}
// quanto tempo `u` passou encostado numa construção querendo andar sem sair do lugar
function medidorDeParede(u) {
  const r = { s: 0, maior: 0, trecho: 0 };
  r.medir = (m) => {
    const quer = Math.hypot(u.vx, u.vy), andou = Math.hypot(u.x - u.px, u.y - u.py) * 60;
    if (!u.morto && quer > 8 && andou < quer * 0.25 && dentroObstaculo(m, u.x, u.y, u.raio + 1.5)) { r.s += 1 / 60; r.trecho += 1 / 60; r.maior = Math.max(r.maior, r.trecho); }
    else r.trecho = 0;
  };
  return r;
}
// um inimigo parado e quieto (para servir de alvo sem lutar), num mundo que não acaba
function inimigoParado(m, tipo, x, y) {
  const fonte = criarMundo({ heroi: "guerreiro", encontro: "vila", composicao: { aliados: "comum", inimigos: "completa" } });
  const u = fonte.unidades.find((v) => v.lado === 1 && v.tipo === tipo);
  u.x = u.px = x; u.y = u.py = y; u.grupo = null; u.posto = { x, y }; u.congelado = 999; u.id = 9000 + m.unidades.length;
  m.unidades.push(u);
  return u;
}

// ---------------------------------------------------------------------------------------------- a navegação
test("a rota: quem está colado na muralha ainda vê os cantos e sai pelo portão (era o que prendia Odette)", () => {
  const m = mundo("vila", (u) => u.tipo === "odette" || u.tipo === "morel");
  inimigoParado(m, "soldado", 60, 40);
  const od = m.odette, h = m.heroi;
  // Odette no canto entre a muralha e a torre, do lado de dentro; você do lado de fora, na estrada
  od.x = od.px = 812.5; od.y = od.py = 209.5; h.x = 720; h.y = 300; m.morel.x = 700; m.morel.y = 320;
  const med = medidorDeParede(od);
  let perto = Infinity;
  rodar(m, 9, entradaVazia(), (mm) => { med.medir(mm); perto = Math.min(perto, bloqueado(mm, od.x, od.y, h.x, h.y, true) ? Infinity : dist(od, h)); });
  assert.ok(med.maior < 1, `ficou ${med.maior.toFixed(1)} s seguidos contra a muralha`);
  assert.ok(perto <= 100, `chegou a uma posição com visão de você (${perto.toFixed(0)} px)`);
  assert.ok(od.x < 790, "saiu pelo portão para o seu lado");
});

test("Morel não fica esbarrando na muralha por um inimigo do outro lado: volta para perto de você pelo caminho", () => {
  const m = mundo("vila", (u) => u.tipo === "morel");
  const mo = m.morel, h = m.heroi;
  const s = inimigoParado(m, "soldado", 830, 150);
  s.congelado = 0; s.posto = { x: 830, y: 150 };
  h.x = 740; h.y = 150; mo.x = mo.px = 775; mo.y = mo.py = 150;
  const med = medidorDeParede(mo);
  rodar(m, 5, entradaVazia(), (mm) => med.medir(mm));
  assert.ok(med.s < 0.5, `${med.s.toFixed(1)} s contra a muralha`);
  assert.ok(dist(mo, h) <= TIPOS.morel.coleira + 20, "continua perto de você");
});

test("o arqueiro sem visão do alvo procura um ponto de tiro e atira", () => {
  const m = mundo("vila", (u) => u.lado === 0 && u.tipo === "arqueiro");
  const arqs = m.unidades.filter((u) => u.tipo === "arqueiro");
  const a = arqs[0];
  m.unidades = [m.heroi, a];
  const alvo = inimigoParado(m, "soldado", 830, 250);
  a.x = a.px = 720; a.y = a.py = 170; a.ordem = { tipo: "atacar", x: 830, y: 250, alvoU: alvo };
  assert.ok(bloqueado(m, a.x, a.y, alvo.x, alvo.y, true), "a torre está no meio");
  let atirou = false;
  rodar(m, 6, entradaVazia(), () => { if (a.acao && !bloqueado(m, a.x, a.y, alvo.x, alvo.y, true)) atirou = true; });
  assert.ok(atirou, "atirou de um ponto com visão");
});

test("um grupo numeroso passa pelo portão, muda de ordem no caminho e chega", () => {
  const m = mundo("vila", (u) => u.lado === 0 && u.tipo === "soldado");
  inimigoParado(m, "soldado", 60, 40);
  const tropa = m.unidades.filter((u) => u.lado === 0 && u.tipo === "soldado");
  assert.ok(tropa.length >= 30);
  tropa.forEach((u, i) => { u.x = u.px = 640 + (i % 6) * 8; u.y = u.py = 250 + Math.floor(i / 6) * 8; });
  m.heroi.x = 600; m.heroi.y = 276;
  for (const u of tropa) m.selecao.add(u.id);
  ordenar(m, "defender", 880, 190);
  rodar(m, 3);
  // no meio do caminho, a ordem muda: de volta para fora, ao sul
  ordenar(m, "defender", 700, 450);
  const meds = tropa.map(medidorDeParede);
  rodar(m, 14, entradaVazia(), (mm) => meds.forEach((x) => x.medir(mm)));
  const chegaram = tropa.filter((u) => !u.morto && Math.hypot(u.x - 700, u.y - 450) <= 70).length;
  assert.ok(chegaram >= tropa.length * 0.9, `${chegaram} de ${tropa.length} chegaram`);
  assert.ok(Math.max(...meds.map((x) => x.maior)) < 2, "alguém ficou preso na parede");
  // e de novo para dentro, pelo portão
  ordenar(m, "defender", 880, 190);
  rodar(m, 16);
  const dentro = tropa.filter((u) => !u.morto && Math.hypot(u.x - 880, u.y - 190) <= 80).length;
  assert.ok(dentro >= tropa.length * 0.9, `${dentro} de ${tropa.length} entraram`);
});

test("o inacessível: um destino num lugar fechado é reconhecido, e quem não sai do lugar desiste por um tempo", () => {
  CENARIOS.caixaTeste = { nome: "teste", obstaculos: [
    { tipo: "casa", x: 400, y: 200, w: 120, h: 10, alto: 20 }, { tipo: "casa", x: 400, y: 330, w: 120, h: 10, alto: 20 },
    { tipo: "casa", x: 400, y: 200, w: 10, h: 140, alto: 20 }, { tipo: "casa", x: 510, y: 200, w: 10, h: 140, alto: 20 }] };
  const m = mundo("vila", (u) => u.lado === 0 && u.tipo === "soldado");
  prepararCenario(m, "caixaTeste");
  mundoAtual(m);
  const u = m.unidades.find((v) => v.tipo === "soldado");
  u.x = 300; u.y = 270;
  rumo(u, 460, 270);
  assert.ok(u.inacessivel && Math.hypot(u.inacessivel.x - 460, u.inacessivel.y - 270) < 1, "o meio da caixa é inacessível");
  delete CENARIOS.caixaTeste;
});

// ---------------------------------------------------------------------------------------------- a escolha de alvo
function duelo7() {
  const m = mundo("herois", (u) => u.tipo === "lider" || u.tipo === "morel" || u.tipo === "odette");
  const l = m.lider, h = m.heroi;
  l.x = l.px = 500; l.y = l.py = 280; l.arremCd = 99; l.cargaCd = 99; l.rodopioCd = 99; l.dashCd = 99; l.bradoCd = 99; l.grupo = null;
  m.morel.x = 470; m.morel.y = 280; m.morel.desafioCd = 99; m.odette.x = 300; m.odette.y = 400;
  h.x = 300; h.y = 280;
  return { m, l, h, mo: m.morel };
}

test("o herói inimigo: atraído por quem o fere, perde o interesse em quem recua e deixa outro assumir", () => {
  const { m, l, h, mo } = duelo7();
  // Morel colado nele e batendo; você a 200 px, parado: ele fica com Morel
  rodar(m, 2.5);
  assert.equal(l.focoU, mo, `escolheu ${l.modo}`);
  // você chega e bate forte: em até 2 s ele vem atrás de você
  h.x = l.x - 40; h.y = l.y;
  let veio = null;
  for (let i = 0; i < 120 && !veio; i++) { if (i % 20 === 0) ferir(m, l, 30, h, { dx: 1, dy: 0 }); passo(m, entradaVazia()); m.eventos.length = 0; if (l.focoU === h) veio = i / 60; }
  assert.ok(veio !== null, "não veio atrás de você");
  // você recua para longe e para de bater; Morel continua nele: ele larga você
  h.x = 120; h.y = 520;
  let largou = null;
  for (let i = 0; i < 12 * 60 && largou === null; i++) {
    if (i % 48 === 0) ferir(m, l, 7, mo, { dx: 1, dy: 0 });
    passo(m, entradaVazia()); m.eventos.length = 0;
    if (l.focoU !== h) largou = i / 60;
  }
  assert.ok(largou !== null && largou >= TIPOS.lider.focoIA.minimo - 0.1, `largou você em ${largou} s`);
});

test("o herói inimigo não troca de alvo a cada instante (inércia e tempo mínimo)", () => {
  const { m, l, h, mo } = duelo7();
  // você e Morel quase à mesma distância, ninguém batendo: no máximo uma troca em 8 s
  h.x = l.x - 60; h.y = l.y + 4; mo.x = l.x + 60; mo.y = l.y - 4;
  let trocas = 0, antes = null;
  rodar(m, 8, entradaVazia(), () => { if (antes !== null && l.focoU !== antes) trocas++; antes = l.focoU; h.x = l.x - 60; h.y = l.y + 4; });
  assert.ok(trocas <= 1, `${trocas} trocas`);
});

test("com o jogador automático, os heróis inimigos se dividem entre você, Morel, Odette e as tropas por motivos do campo", () => {
  const vistos = new Set();
  let menor = Infinity;
  for (const [comp, heroi] of [["comum", "guerreiro"], ["completa", "mago"]]) {
    const m = criarMundo({ heroi, encontro: "herois", composicao: { aliados: comp, inimigos: comp } });
    const r = criarRobo({ nivel: "forte" }), ent = entradaVazia(), ult = {};
    while (m.fase !== "fim" && m.t < 70) {
      pensar(r, m, ent); passo(m, ent);
      const motivos = new Set(m.eventos.filter((e) => e.tipo === "controle" || e.tipo === "desafio").map((e) => e.id));
      m.eventos.length = 0;
      for (const u of [m.lider, m.ardis]) {
        if (!u || u.morto || !u.modo) continue;
        vistos.add(u.modo);
        const c = u.modo + (u.focoU ? u.focoU.id : "");
        // fora a provocação (uma regra explícita), as trocas respeitam o tempo mínimo menos a inércia de 1 s
        if (ult[u.id] && ult[u.id].c !== c && !(u.provocacao && u.provocacao.ate > m.t) && !motivos.has(u.id)) menor = Math.min(menor, m.t - ult[u.id].t);
        if (!ult[u.id] || ult[u.id].c !== c) ult[u.id] = { c, t: m.t };
      }
    }
    assert.equal(m.resultado, "vitoria", `${comp} ${heroi}`);
  }
  for (const k of ["heroi", "morel", "odette", "tropas"]) assert.ok(vistos.has(k), `ninguém foi atrás de ${k}`);
  assert.ok(menor >= 0.9, `uma troca em ${menor.toFixed(2)} s`);
});

// ---------------------------------------------------------------------------------------------- a Investida Curta
test("a Investida Curta: preparação legível e parada, execução rápida sem corrigir a direção, recuperação aberta", () => {
  const { m, l, h } = duelo7();
  m.morel.x = 900; m.morel.y = 40; m.odette.x = 900; m.odette.y = 80;
  l.dashCd = 0; l.modo = "heroi"; l.focoU = h; l.focoDesde = 0; l.focoT = 99;
  h.x = l.x - 150; h.y = l.y;
  const fases = [];
  let aviso = null, dir0 = null, vel = 0, x0 = null;
  const ent = entradaVazia();
  for (let i = 0; i < 90; i++) {
    passo(m, ent);
    aviso ||= m.eventos.find((e) => e.tipo === "aviso" && e.investida);
    m.eventos.length = 0;
    const g = l.dash7;
    if (g) {
      fases.push(g.fase);
      if (dir0 === null) { dir0 = [g.dx, g.dy]; ent.cima = true; }   // você sai para o lado assim que a faixa aparece
      if (g.fase === "preparo") assert.ok(Math.hypot(l.vx, l.vy) < 1, "andou na preparação");
      if (g.fase === "exec") { vel = Math.max(vel, Math.hypot(l.vx, l.vy)); assert.ok(Math.abs(g.dx - dir0[0]) < 1e-9 && Math.abs(g.dy - dir0[1]) < 1e-9, "corrigiu a direção"); x0 ??= l.x; }
      if (g.fase === "rec") assert.ok(l.vulneravel > 0, "a recuperação não deixa aberto");
    }
  }
  const D = TIPOS.lider.investida7;
  assert.ok(aviso && aviso.preparo === D.preparo && aviso.forma.tipo === "faixa", "a faixa no chão antes");
  assert.ok(fases.filter((f) => f === "preparo").length >= Math.floor(D.preparo * 60) - 1, "a preparação durou");
  assert.ok(vel >= D.vel - 1, `execução a ${vel.toFixed(0)} px/s`);
  assert.ok(fases.filter((f) => f === "rec").length >= Math.floor(D.recupera * 60) - 1, "a recuperação durou");
});

test("a Investida acerta quem fica: dano, empurrão e a preparação do golpe perdida", () => {
  const { m, l, h } = duelo7();
  m.morel.x = 900; m.morel.y = 40; m.odette.x = 900; m.odette.y = 80;
  l.dashCd = 0; l.modo = "heroi"; l.focoU = h; l.focoDesde = 0; l.focoT = 99;
  h.x = l.x - 120; h.y = l.y;
  let acertou = false;
  for (let i = 0; i < 60 && !acertou; i++) {
    // você prepara a Ruptura (um golpe com preparação) sem sair do lugar
    const ent = entradaVazia(); ent.mx = l.x; ent.my = l.y;
    if (l.dash7 && l.dash7.fase === "exec" && !h.acao) ent.apertos = [h.slots.h1];
    passo(m, ent);
    acertou = m.eventos.some((e) => e.tipo === "investidaAcerta" && e.heroi);
    m.eventos.length = 0;
  }
  assert.ok(acertou, "acertou você parado");
  assert.ok(h.vida < h.vidaMax, "levou dano");
  assert.ok(!h.acao || h.acao.fase !== "preparo", "a preparação continuou");
});

// ---------------------------------------------------------------------------------------------- os controles
test("a proteção contra repetição: 100%, 60%, 30%, firme; a janela se fecha e volta a valer; a lentidão não conta", () => {
  const m = mundo("herois", (u) => u.tipo === "lider");
  const h = m.heroi, l = m.lider;
  const f = CONTROLE.fatores;
  const ds = [0, 1, 2, 3].map(() => { const d = aplicarControle(m, h, "atordoado", 1, l); h.atordoado = 0; return d; });
  assert.deepEqual(ds.map((d) => Math.round(d * 100) / 100), [f[0], f[1], f[2], 0]);
  assert.ok(estadoControle(m, h).some((c) => c.id === "protecao" && c.firme), "a tela diz que está firme");
  // a lentidão não gasta a proteção nem acumula
  assert.ok(aplicarControle(m, h, "lento", 2, l, { fator: 0.3 }) > 0);
  assert.equal(aplicarControle(m, h, "lento", 2, l, { fator: 0.2 }), 0, "a mais fraca não troca a mais forte");
  rodar(m, CONTROLE.janela + 0.1);
  assert.equal(aplicarControle(m, h, "imobilizado", 1, l), 1, "a janela fechou");
});

test("imobilizado não anda nem usa a mobilidade, mas ataca; lento anda menos", () => {
  const m = mundo("herois", (u) => u.tipo === "lider");
  inimigoParado(m, "soldado", 900, 40);
  const h = m.heroi, l = m.lider;
  l.x = 900; l.y = 500; l.congelado = 99;
  h.x = 300; h.y = 300;
  aplicarControle(m, h, "imobilizado", 1, l);
  const ent = entradaVazia(); ent.dir = true; ent.mx = 340; ent.my = 300; ent.apertos = ["investida"]; ent.atacar = true;
  passo(m, ent); ent.apertos = [];
  for (let i = 0; i < 20; i++) passo(m, ent);
  assert.ok(Math.abs(h.x - 300) < 0.5, "andou imobilizado");
  assert.ok((m.stats.usos.investida || { usos: 0 }).usos === 0, "usou a Investida imobilizado");
  assert.ok((m.stats.usos.varredura || { usos: 0 }).usos >= 1, "não atacou");
  const m2 = mundo("herois", (u) => u.tipo === "lider");
  m2.lider.congelado = 99; m2.lider.x = 900; m2.lider.y = 500;
  m2.heroi.x = 300; m2.heroi.y = 300;
  aplicarControle(m2, m2.heroi, "lento", 2, m2.lider, { fator: 0.4 });
  const e2 = entradaVazia(); e2.dir = true;
  for (let i = 0; i < 60; i++) passo(m2, e2);
  assert.ok(m2.heroi.x - 300 < TIPOS.lider.vel && m2.heroi.x - 300 > 30, `andou ${(m2.heroi.x - 300).toFixed(0)} px em 1 s`);
});

test("nas batalhas com o jogador automático, o herói nunca fica muito tempo seguido sob controle", () => {
  for (const [comp, heroi] of [["completa", "guerreiro"], ["cavalaria", "mago"]]) {
    for (const enc of ["herois", "carga"]) {
      const m = criarMundo({ heroi, encontro: enc, composicao: { aliados: comp, inimigos: comp } });
      const r = criarRobo({ nivel: "medio" }), ent = entradaVazia();
      let trecho = 0, maior = 0, total = 0;
      while (m.fase !== "fim" && m.t < 60) {
        pensar(r, m, ent); passo(m, ent); m.eventos.length = 0;
        const h = m.heroi;
        if (!h.morto && (h.atordoado > 0 || h.imobAte > m.t)) { trecho += 1 / 60; total += 1 / 60; maior = Math.max(maior, trecho); } else trecho = 0;
      }
      assert.ok(maior <= 1.3, `${enc} ${comp} ${heroi}: ${maior.toFixed(2)} s seguidos`);
      assert.ok(total / m.t < 0.15, `${enc} ${comp} ${heroi}: ${((100 * total) / m.t).toFixed(0)}% do tempo`);
    }
  }
});

// ---------------------------------------------------------------------------------------------- as provocações
test("o Brado: o ataque principal vai no provocador ao alcance; fora do alcance, sem assistência; morto, acaba", () => {
  const m = mundo("herois", (u) => u.tipo === "lider" || (u.lado === 1 && u.tipo === "pesado"));
  const h = m.heroi, l = m.lider;
  const s = m.unidades.find((u) => u.tipo === "pesado");
  l.x = 400; l.y = 280; l.congelado = 99; s.x = 330; s.y = 280; s.congelado = 99;
  h.x = 310; h.y = 280;
  aplicarControle(m, h, "provocacao", 2.5, l);
  // o mouse no soldado; Harg a 90 px (fora dos 64 do alcance assistido): sem assistência
  assert.equal(alvoAssistido(m, h, s.x, s.y), null);
  // Harg a 50 px: a assistência vai nele mesmo com o mouse no soldado
  l.x = 360;
  assert.equal(alvoAssistido(m, h, s.x, s.y), l);
  assert.ok(estadoControle(m, h).some((c) => c.id === "provocacao" && /ataque principal/.test(c.texto)), "a tela explica");
  // morto o provocador, a provocação acaba
  l.morto = true;
  assert.equal(alvoAssistido(m, h, s.x, s.y), s);
  assert.equal(h.provocacao, null);
  // a Bola do Mago provocado cai nele (ao alcance e à vista)
  const m2 = mundo("herois", (u) => u.tipo === "lider", { heroi: "mago" });
  m2.lider.x = 420; m2.lider.y = 300; m2.lider.congelado = 99; m2.heroi.x = 300; m2.heroi.y = 280;
  aplicarControle(m2, m2.heroi, "provocacao", 2.5, m2.lider);
  mundoAtual(m2);
  const f = formaDaAcao(m2.heroi, "bola", 300, 500);
  assert.ok(Math.hypot(f.x - 420, f.y - 300) < 1, "a Bola foi no provocador");
});

test("o Brado sai quando você derruba a tropa dele por perto; a preparação se anuncia", () => {
  const m = mundo("herois", (u) => u.tipo === "lider" || (u.lado === 1 && u.tipo === "soldado"));
  inimigoParado(m, "soldado", 900, 40);
  const h = m.heroi, l = m.lider;
  l.x = 400; l.y = 280; l.bradoCd = 0; l.arremCd = 99; l.cargaCd = 99; l.rodopioCd = 99; l.dashCd = 99;
  h.x = 320; h.y = 280;
  const tropa = m.unidades.filter((u) => u.lado === 1 && u.tipo === "soldado" && u.y !== 40).slice(0, 4);
  let aviso = null, provocado = false;
  for (let i = 0; i < 90 && !provocado; i++) {
    for (const s of tropa) if (!s.morto && i % 15 === 0) { s.x = 340; s.y = 280; ferir(m, s, 5, h, { dx: 1, dy: 0 }); }
    passo(m, entradaVazia());
    aviso ||= m.eventos.find((e) => e.tipo === "aviso" && e.brado);
    m.eventos.length = 0;
    provocado = !!(h.provocacao && h.provocacao.por === l);
  }
  assert.ok(aviso && aviso.preparo === TIPOS.lider.brado.preparo, "o anel antes do Brado");
  assert.ok(provocado, "não provocou");
});

test("o Desafio de Morel: só quando um herói inimigo pressiona você ou Odette; ele passa a mirar Morel", () => {
  const { m, l, mo } = duelo7();
  const od = m.odette;
  mo.desafioCd = 0;
  // ninguém pressionado: Morel não gasta o Desafio
  l.x = 600; l.y = 280; l.focoU = m.heroi; l.modo = "heroi"; mo.x = 560; mo.y = 300; m.heroi.x = 300; m.heroi.y = 280;
  l.congelado = 0.4;
  rodar(m, 0.3);
  assert.ok(!(l.provocacao && l.provocacao.ate > m.t), "desafiou sem necessidade");
  // Harg colado em Odette: Morel desafia
  od.x = 590; od.y = 280; l.focoU = od; l.modo = "odette"; l.focoDesde = m.t; l.focoT = 9;
  let desafiou = false;
  rodar(m, 1, entradaVazia(), (mm) => { desafiou ||= mm.eventos.some((e) => e.tipo === "desafio"); });
  assert.ok(desafiou, "não desafiou");
  assert.equal(l.focoU, mo, "Harg não passou a mirar Morel");
  assert.ok(mo.posturaAte > m.t, "Morel sem o escudo erguido");
});
