// Testes do Campo Livre 8 (node --test): Harg reconstruído (campo8.js). Os três tempos de cada golpe e a direção
// marcada, a esquiva de lado e o recuo em linha reta, a Investida pela linha, a abertura, a postura (a quebra, a firmeza
// depois, os controles que viram postura), a fase 2 e o papel dele na guerra. As regras, não a diversão.
import { test } from "node:test";
import assert from "node:assert/strict";
import { criarMundo, passo, entradaVazia, ferir } from "../tela/sim.js";
import { aplicarControle } from "../tela/campo7.js";
import { HARG8 } from "../tela/conteudo.js";
import { criarRobo, pensar } from "../tela/robo.js";

const G = HARG8.golpes;
function duelo(heroi = "guerreiro") {
  const m = criarMundo({ heroi, encontro: "duelo" });
  m.fase = "luta";
  for (const g of Object.values(m.grupos)) g.ativo = true;
  const l = m.lider, h = m.heroi;
  l.h8.pausa = 0; l.h8.investidaCd = 99; l.h8.rodopioCd = 99;
  return { m, l, h };
}
function rodar(m, s, ent = entradaVazia(), cada = null) {
  for (let t = 0; t < s && m.fase !== "fim"; t += 1 / 60) { passo(m, ent); if (cada) cada(m); m.eventos.length = 0; }
}
// espera Harg começar o golpe `id` (com o herói parado a `d` px)
function ateGolpe(m, l, id, limite = 4) {
  for (let t = 0; t < limite; t += 1 / 60) { passo(m, entradaVazia()); m.eventos.length = 0; if (l.h8.golpe && l.h8.golpe.id === id) return l.h8.golpe; }
  return null;
}

test("os três tempos: a preparação vira para o alvo só no começo; depois a direção fica, a execução e a recuperação", () => {
  const { m, l, h } = duelo();
  h.x = l.x - 30; h.y = l.y;
  l.h8.seq = 3;   // o Talho sozinho
  const g = ateGolpe(m, l, "talho");
  assert.ok(g, "não começou o Talho");
  // passada a parte em que ele vira, você muda de lado: a direção não acompanha e o golpe sai no vazio
  rodar(m, G.talho.preparo * G.talho.rastreia + 0.02);
  const dir = g.dir;
  h.x = l.x + 30;
  const etapas = new Set();
  rodar(m, G.talho.preparo * (1 - G.talho.rastreia) + G.talho.exec + 0.1, entradaVazia(), () => { if (l.h8.golpe) etapas.add(l.h8.golpe.etapa); });
  assert.equal(g.dir, dir, "corrigiu a direção depois da parte de mira");
  assert.ok(etapas.has("exec") && etapas.has("rec"), `etapas ${[...etapas]}`);
  assert.equal(h.vida, h.vidaMax, "acertou do outro lado");
});

test("o Talho: quem fica apanha; quem sai na diagonal, para trás e para o lado, depois do aviso escapa", () => {
  for (const sai of [false, true]) {
    const { m, l, h } = duelo();
    h.x = l.x - 28; h.y = l.y;
    l.h8.seq = 3;
    const g = ateGolpe(m, l, "talho");
    assert.ok(g);
    const ent = entradaVazia();
    if (sai) { rodar(m, 0.2); ent.cima = true; ent.esq = true; }
    rodar(m, G.talho.preparo + G.talho.exec, ent);
    if (sai) assert.equal(h.vida, h.vidaMax, "saiu e apanhou");
    else assert.ok(h.vida <= h.vidaMax - G.talho.danoHeroi, "ficou parado e não apanhou");
  }
});

test("a Varredura Longa alcança quem só recua em linha reta", () => {
  const { m, l, h } = duelo();
  h.x = l.x - 40; h.y = l.y;
  l.h8.seq = 2;   // a terceira sequência da fase 1: a Varredura
  const g = ateGolpe(m, l, "varredura", 6);
  assert.ok(g, "não veio a Varredura");
  // você reage depois de 0,3 s (o tempo de uma pessoa) e recua em linha reta
  rodar(m, 0.3);
  const ent = entradaVazia(); ent.esq = true;
  rodar(m, 0.7, ent);
  assert.ok(h.vida < h.vidaMax, "recuar reto escapou da Varredura");
});

test("a Investida atravessa a infantaria, derruba quem está na faixa e para no herói; depois a abertura", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "guerra" });
  m.fase = "luta"; m.ondas = null; m.levas.forEach((lv) => (lv.t = 0));
  for (const g of Object.values(m.grupos)) g.ativo = true;
  passo(m, entradaVazia());
  const l = m.lider, h = m.heroi;
  m.unidades = m.unidades.filter((u) => u === h || u === l || u.lado === 0 && u.tipo === "soldado");
  m.morel = m.odette = null;
  const sold = m.unidades.filter((u) => u.tipo === "soldado").slice(0, 4);
  m.unidades = [h, l, ...sold];
  l.x = 300; l.y = 280; h.x = 160; h.y = 280; l.h8.investidaCd = 0; l.h8.pausa = 9; l.modo = "heroi"; l.focoU = h; l.focoT = 99; l.focoDesde = 0;
  sold.forEach((s, i) => { s.x = 230 + i * 12; s.y = 280; s.congelado = 99; });
  let acertou = false, abriu = false;
  rodar(m, 2.5, entradaVazia(), (mm) => { for (const e of mm.eventos) { if (e.tipo === "hargContato" && e.golpe === "investida" && e.heroi) acertou = true; if (e.tipo === "hargAbertura") abriu = true; } });
  assert.ok(sold.filter((s) => s.morto).length >= 3, `derrubou ${sold.filter((s) => s.morto).length} de 4 na faixa`);
  assert.ok(acertou && abriu, "não parou no herói ou não abriu");
});

test("a abertura depois da Martelada: parado, leva +50% e o dobro de postura", () => {
  const { m, l, h } = duelo();
  h.x = l.x - 30; h.y = l.y;
  l.h8.seq = 1;   // Talho, Martelada
  ateGolpe(m, l, "martelada", 6);
  rodar(m, G.martelada.preparo + G.martelada.exec + 0.05, (() => { const e = entradaVazia(); e.cima = true; return e; })());
  assert.ok(l.h8.abertoAte > m.t && l.vulneravel > 0, "sem abertura");
  const v0 = l.vida, p0 = l.h8.postura;
  ferir(m, l, 20, h, {});
  assert.equal(v0 - l.vida, 30, "a abertura não dá +50%");
  assert.ok(l.h8.postura - p0 >= 20 * 2 - 0.01, "a abertura não dá o dobro de postura");
});

test("a postura: enche, quebra (de joelhos, aberto, sem o golpe), e depois fica firme; nada de atordoamento permanente", () => {
  const { m, l, h } = duelo();
  h.x = l.x - 30; h.y = l.y;
  ateGolpe(m, l, "talho");
  let quebras = 0, quebradoT = 0, n = 0;
  for (let i = 0; i < 60 * 14; i++) {
    if (i % 12 === 0 && !l.morto) ferir(m, l, 30, h, { forte: true });
    passo(m, entradaVazia());
    for (const e of m.eventos) if (e.tipo === "hargQuebra") quebras++;
    m.eventos.length = 0;
    if (l.h8.quebrado > 0) quebradoT += 1 / 60;
    n++;
    l.vida = Math.max(l.vida, 400);   // o teste é da postura, não da morte
    h.vida = h.vidaMax;
  }
  assert.ok(quebras >= 2, `${quebras} quebras`);
  assert.ok(quebradoT / (n / 60) < 0.45, `de joelhos ${((100 * quebradoT * 60) / n).toFixed(0)}% do tempo apanhando sem parar`);
  // um controle não o prende: vira postura
  const m2 = duelo().m, l2 = m2.lider, p = l2.h8.postura;
  assert.equal(aplicarControle(m2, l2, "atordoado", 1, m2.heroi), 0);
  assert.ok(l2.h8.postura > p && !(l2.atordoado > 0), "o controle prendeu Harg ou não encheu a postura");
});

test("a fase 2: abaixo de 55%, o Rugido; depois as sequências mais longas e a Martelada com a onda", () => {
  const { m, l, h } = duelo();
  h.x = l.x - 30; h.y = l.y;
  l.vida = l.vidaMax * 0.5;
  assert.ok(ateGolpe(m, l, "rugido"), "sem o Rugido");
  rodar(m, G.rugido.preparo + G.rugido.exec + G.rugido.recupera + 0.05);
  assert.equal(l.h8.fase, 2);
  // a primeira sequência da fase 2: três golpes, terminando na Martelada com a onda
  h.vida = h.vidaMax; h.x = l.x - 28; h.y = l.y;
  let maior = 0, onda = false;
  for (let i = 0; i < 60 * 4; i++) {
    h.vida = h.vidaMax;
    passo(m, entradaVazia()); m.eventos.length = 0;
    if (l.h8.golpe) { maior = Math.max(maior, l.h8.fila.length + 1); if (l.h8.golpe.onda) onda = true; }
  }
  assert.ok(maior >= 3, `a maior sequência teve ${maior}`);
  assert.ok(onda, "a Martelada da fase 2 sem a onda");
});

test("na guerra, Harg derruba soldados aos montes, troca de alvo por motivo e o herói não fica preso", () => {
  for (const heroi of ["guerreiro", "mago"]) {
    const m = criarMundo({ heroi, encontro: "guerra" });
    const r = criarRobo({ nivel: "forte" }), ent = entradaVazia(), focos = new Set();
    let preso = 0;
    while (m.fase !== "fim" && m.t < 120) {
      pensar(r, m, ent); passo(m, ent); m.eventos.length = 0;
      if (m.lider && !m.lider.morto && m.lider.modo) focos.add(m.lider.modo);
      if (m.heroi.atordoado > 0 || m.heroi.imobAte > m.t) preso += 1 / 60;
    }
    assert.equal(m.resultado, "vitoria", heroi);
    assert.ok((m.stats.hargMortos || 0) >= 15, `${heroi}: Harg derrubou ${m.stats.hargMortos}`);
    assert.ok(focos.size >= 2, `${heroi}: só ${[...focos]}`);
    assert.ok(preso < 2, `${heroi}: ${preso.toFixed(1)} s preso`);
  }
});

test("o treino: quem sai dos avisos para o lado vence; quem só recua em linha reta apanha muito mais", () => {
  const vida = {};
  for (const nivel of ["forte", "medio"]) {
    const m = criarMundo({ heroi: "guerreiro", encontro: "duelo" });
    const r = criarRobo({ nivel }), ent = entradaVazia();
    while (m.fase !== "fim" && m.t < 120) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    vida[nivel] = Math.max(0, m.heroi.vida);
    if (nivel === "forte") assert.equal(m.resultado, "vitoria");
  }
  assert.ok(vida.forte - vida.medio >= 80, JSON.stringify(vida));
});
