// Testes da simulação do campo livre (Node, sem navegador): node --test ferramentas/prototipos/etapa8-campo/testes
// Conferem o funcionamento, não a sensação: área mostrada = alvos atingidos, dano uma vez, mortes simultâneas,
// unidades sem alvo, grupos concentrados, o herói entre aliados e inimigos, a resposta dos comandos, o adiantamento,
// o compromisso dos golpes fortes, a interrupção do campeão, a repetição pela semente e o desempenho do passo.
import { test } from "node:test";
import assert from "node:assert/strict";
import { criarMundo, passo, entradaVazia, dentro, formaDaAcao, ordenar, resumo, PASSO } from "../tela/sim.js";
import { HEROIS, TIPOS, CAMPO } from "../tela/conteudo.js";
import { criarRobo, pensar } from "../tela/robo.js";

// Um mundo de laboratório: o herói no meio do campo, sem tropas, com os inimigos que o teste puser (parados:
// atordoados por muito tempo, para a posição na hora do contato ser a de agora).
function laboratorio(heroi = "guerreiro") {
  const m = criarMundo({ heroi });
  for (const u of m.unidades) if (u !== m.heroi) u.morto = true;
  passo(m, entradaVazia());
  m.heroi.x = m.heroi.px = 480; m.heroi.y = m.heroi.py = 280;
  m.heroi.vx = m.heroi.vy = 0;
  m.fase = "luta";
  m.stats.primeira = -1;        // sem segunda leva e, portanto, sem fim por fuga no meio do teste (antes dos 30 s)
  m.eventos.length = 0;
  return m;
}
function inimigo(m, tipo, x, y, parado = true) {
  const d = TIPOS[tipo];
  const u = { id: m.proximoId++, lado: 1, tipo, def: d, x, y, px: x, py: y, vx: 0, vy: 0, kx: 0, ky: 0, raio: d.raio,
    massa: d.massa, vida: d.vida, vidaMax: d.vida, alvo: null, reavaliar: 0, acao: null, recarga: 0, atordoado: parado ? 99 : 0,
    congelado: 0, flash: 0, virado: -1, passo: 0, abalado: 0, mostra: 0, fugindo: false, saiu: false, morto: false,
    atacantes: 0, aura: false, slot: 0 };
  m.unidades.push(u);
  m.lados[1].push(u);
  return u;
}
function grade(m, tipo, cx, cy, raio, esp = 9) {
  const lista = [];
  for (let y = cy - raio; y <= cy + raio; y += esp) for (let x = cx - raio; x <= cx + raio; x += esp) {
    if (Math.hypot(x - m.heroi.x, y - m.heroi.y) < 9) continue;
    lista.push(inimigo(m, tipo, x + 0.37, y + 0.21));
  }
  return lista;
}
function rodar(m, ent, n) { for (let i = 0; i < n; i++) { passo(m, ent); ent.apertos = []; } }
function usar(m, id, mx, my, passos = 60) {
  const ent = entradaVazia();
  ent.mx = mx; ent.my = my; ent.apertos = [id];
  rodar(m, ent, passos);
}

test("a área de cada golpe forte atinge exatamente quem está dentro da forma mostrada", () => {
  for (const [heroi, id, alvo] of [["guerreiro", "varredura", [520, 280]], ["guerreiro", "salto", [560, 300]],
    ["mago", "bola", [600, 260]], ["mago", "piscar", [560, 280]]]) {
    const m = laboratorio(heroi);
    m.heroi.recurso = 100;
    const forma = formaDaAcao(m.heroi, id, alvo[0], alvo[1]);
    const fc = forma.tipo === "circulo" ? forma : { ...forma };
    const lista = grade(m, "veterano", Math.round(fc.x ?? m.heroi.x), Math.round(fc.y ?? m.heroi.y), (fc.raio || 40) + 12, 9);
    const dentroAntes = new Set(lista.filter((u) => dentro(forma, u.x, u.y)).map((u) => u.id));
    usar(m, id, alvo[0], alvo[1], 90);
    const atingidos = new Set(lista.filter((u) => u.vida < u.vidaMax).map((u) => u.id));
    assert.ok(dentroAntes.size >= 8, `${id}: o teste precisa de gente dentro (${dentroAntes.size})`);
    assert.deepEqual([...atingidos].sort(), [...dentroAntes].sort(), `${id}: atingidos diferentes da área`);
  }
});

test("o dano de uma ação cai uma vez em cada alvo", () => {
  for (const [heroi, id, chave] of [["guerreiro", "varredura", "varredura"], ["guerreiro", "salto", "salto"], ["mago", "bola", "bola"],
    ["guerreiro", "investida", "investida"]]) {
    const m = laboratorio(heroi);
    if (id === "salto") m.heroi.recurso = 100;
    const lista = id === "investida" ? [inimigo(m, "veterano", 510, 280), inimigo(m, "veterano", 540, 284), inimigo(m, "veterano", 565, 276)]
      : grade(m, "veterano", 520, 280, 20, 9);
    usar(m, id, 520, 280, id === "bola" ? 22 : 60);   // a bola: antes de o fogo do chão começar a contar
    const k = HEROIS[heroi].kit[chave];
    for (const u of lista) if (u.vida < u.vidaMax) assert.equal(u.vidaMax - u.vida, k.dano, `${id}: dano ${u.vidaMax - u.vida}`);
    assert.ok(lista.some((u) => u.vida < u.vidaMax), `${id}: ninguém atingido`);
  }
});

test("mortes simultâneas: quem morre sai de uma vez e ninguém continua mirando um morto", () => {
  const m = laboratorio("guerreiro");
  m.heroi.recurso = 100;
  const lista = grade(m, "soldado", 540, 280, 24, 8);
  // aliados que miravam os que vão morrer
  const aliados = [];
  for (let i = 0; i < 6; i++) {
    const a = { ...lista[0], id: m.proximoId++, lado: 0, tipo: "soldado", def: TIPOS.soldado, x: 600 + i * 9, y: 330, px: 600, py: 330,
      vida: 16, vidaMax: 16, alvo: lista[i], atordoado: 0, acao: null, morto: false, recarga: 0 };
    m.unidades.push(a); aliados.push(a);
  }
  const antes = m.lados[1].length;
  const ent = entradaVazia(); ent.mx = 540; ent.my = 280; ent.apertos = ["salto"];
  let mortes = 0, passoDasMortes = new Set();
  for (let i = 0; i < 60; i++) {
    passo(m, ent); ent.apertos = [];
    const n = m.eventos.filter((e) => e.tipo === "morte").length;
    if (n) passoDasMortes.add(i);
    mortes += n;
    m.eventos.length = 0;
  }
  assert.ok(mortes >= 15, `poucas mortes de uma vez: ${mortes}`);
  assert.equal(passoDasMortes.size, 1, "as mortes do salto deviam cair no mesmo passo");
  assert.equal(m.lados[1].length, antes - mortes);
  assert.equal(m.stats.abatesHeroi, mortes);
  for (const a of aliados) assert.ok(!a.alvo || !a.alvo.morto, "um aliado ficou mirando um morto");
  for (const u of m.unidades) assert.ok(Number.isFinite(u.x) && Number.isFinite(u.y));
});

test("sem alvo: as tropas voltam para a ordem e ninguém trava nem vira NaN", () => {
  const m = criarMundo({ heroi: "guerreiro" });
  for (const u of m.lados[1]) u.morto = true;        // ninguém do outro lado (e a segunda leva não vem)
  m.stats.primeira = -1;
  m.t = -1e9;
  const ent = entradaVazia();
  ordenar(m, "defender", 200, 200);
  rodar(m, ent, 600);
  const aliados = m.lados[0].filter((u) => u !== m.heroi);
  for (const u of aliados) {
    assert.equal(u.alvo, null);
    assert.ok(Math.hypot(u.x - 200, u.y - 200) < 80, `fora do ponto de defesa: ${u.x.toFixed(0)},${u.y.toFixed(0)}`);
  }
  ordenar(m, "acompanhar");
  rodar(m, ent, 600);
  for (const u of aliados) assert.ok(Math.hypot(u.x - m.heroi.x, u.y - m.heroi.y) < 90, "não acompanhou o herói");
});

test("um grupo concentrado num ponto se espalha sem pilha nem NaN", () => {
  const m = laboratorio("guerreiro");
  const lista = [];
  for (let i = 0; i < 80; i++) lista.push(inimigo(m, "soldado", 300, 300, false));
  for (const u of lista) u.def = { ...u.def, vel: 0 };   // só a separação age
  rodar(m, entradaVazia(), 120);
  let pior = 0;
  for (let i = 0; i < lista.length; i++) for (let j = i + 1; j < lista.length; j++) {
    const a = lista[i], b = lista[j], d = Math.hypot(a.x - b.x, a.y - b.y);
    pior = Math.max(pior, a.raio + b.raio - d);
    assert.ok(Number.isFinite(a.x) && Number.isFinite(a.y));
  }
  assert.ok(pior < 1.5, `sobreposição de ${pior.toFixed(2)} px depois de 2 s`);
});

test("o herói atravessa os próprios aliados sem perder velocidade; uma multidão inimiga o freia", () => {
  const m = laboratorio("guerreiro");
  const h = m.heroi;
  for (let i = 0; i < 40; i++) {
    const a = { id: m.proximoId++, lado: 0, tipo: "soldado", def: { ...TIPOS.soldado, vel: 0 }, x: 500 + (i % 8) * 8, y: 262 + Math.floor(i / 8) * 8,
      px: 0, py: 0, vx: 0, vy: 0, kx: 0, ky: 0, raio: 3.5, massa: 1, vida: 16, vidaMax: 16, alvo: null, reavaliar: 99, acao: null, recarga: 0,
      atordoado: 0, congelado: 0, flash: 0, virado: 1, passo: 0, abalado: 0, mostra: 0, morto: false, slot: 0 };
    m.unidades.push(a);
  }
  const ent = entradaVazia(); ent.dir = true; ent.mx = 900; ent.my = 280;
  const x0 = h.x;
  rodar(m, ent, 60);
  assert.ok(h.x - x0 > HEROIS.guerreiro.vel * 0.9, `entre aliados andou só ${(h.x - x0).toFixed(1)} px em 1 s`);
  // agora uma parede de inimigos à frente
  const m2 = laboratorio("guerreiro"), h2 = m2.heroi;
  const muro = grade(m2, "soldado", 540, 280, 40, 8);
  for (const u of muro) { u.atordoado = 0; u.def = { ...u.def, vel: 0, dano: 0 }; u.recarga = 99; }
  const ent2 = entradaVazia(); ent2.dir = true; ent2.mx = 900; ent2.my = 280;
  const x2 = h2.x;
  rodar(m2, ent2, 60);
  const andou = h2.x - x2;
  assert.ok(andou < HEROIS.guerreiro.vel * 0.7, `atravessou a multidão rápido demais: ${andou.toFixed(1)} px em 1 s`);
  assert.ok(andou > 5, `ficou preso: ${andou.toFixed(1)} px`);
});

test("resposta: acelera em até 5 passos, para em até 4, e o golpe começa no passo do aperto", () => {
  const m = laboratorio("guerreiro"), h = m.heroi, v = HEROIS.guerreiro.vel;
  const ent = entradaVazia(); ent.dir = true; ent.mx = 900; ent.my = 280;
  let n = 0;
  while (h.vx < v * 0.99 && n < 20) { passo(m, ent); n++; }
  assert.ok(n <= 5, `levou ${n} passos para a velocidade máxima`);
  ent.dir = false;
  n = 0;
  while (Math.abs(h.vx) > 0.01 && n < 20) { passo(m, ent); n++; }
  assert.ok(n <= 4, `levou ${n} passos para parar`);
  ent.apertos = ["varredura"];
  passo(m, ent);
  assert.equal(h.acao && h.acao.id, "varredura");
});

test("o comando apertado durante outra ação espera até 0,2 s e sai", () => {
  const m = laboratorio("guerreiro"), h = m.heroi;
  const ent = entradaVazia(); ent.mx = 600; ent.my = 280; ent.apertos = ["varredura"];
  passo(m, ent); ent.apertos = [];
  // na preparação da varredura (não cancelável), aperta a investida: ela sai logo depois do contato
  rodar(m, ent, 3);
  ent.apertos = ["investida"];
  passo(m, ent); ent.apertos = [];
  assert.equal(h.acao.id, "varredura");
  let n = 0;
  while (h.acao && h.acao.id !== "investida" && n < 30) { passo(m, ent); n++; }
  assert.equal(h.acao && h.acao.id, "investida", "a investida guardada não saiu");
  // e um aperto que não pode sair em 0,2 s se perde
  const m2 = laboratorio("guerreiro");
  m2.heroi.cds.investida = 1;
  const e2 = entradaVazia(); e2.apertos = ["investida"];
  rodar(m2, e2, 30);
  rodar(m2, e2, 50);
  assert.notEqual(m2.heroi.acao && m2.heroi.acao.id, "investida");
});

test("golpe forte: a preparação prende os pés; depois do contato, andar corta a recuperação", () => {
  const m = laboratorio("guerreiro"), h = m.heroi;
  const ent = entradaVazia(); ent.mx = 600; ent.my = 280; ent.apertos = ["varredura"];
  passo(m, ent); ent.apertos = [];
  ent.baixo = true;
  const y0 = h.y;
  while (h.acao && h.acao.fase === "preparo") passo(m, ent);
  assert.ok(Math.abs(h.y - y0) < 0.5, "andou durante a preparação");
  passo(m, ent);
  assert.equal(h.acao, null, "andar não cortou a recuperação");
  rodar(m, ent, 10);
  assert.ok(h.y - y0 > 3, "não voltou a andar");
});

test("o campeão anuncia o golpe e um golpe forte do herói o interrompe; um fraco, não", () => {
  for (const [id, interrompe] of [["varredura", true], ["basico", false]]) {
    const m = laboratorio("guerreiro"), h = m.heroi;
    const c = inimigo(m, "campeao", 500, 280, false);
    const ent = entradaVazia(); ent.mx = 500; ent.my = 280;
    let n = 0;
    while (!c.acao && n < 200) { passo(m, ent); n++; }
    assert.ok(c.acao && c.acao.forma, "o campeão não preparou o golpe");
    assert.ok(m.eventos.some((e) => e.tipo === "aviso"), "sem o aviso no chão");
    if (id === "basico") ent.atacar = true; else ent.apertos = [id];
    for (let i = 0; i < 16; i++) { passo(m, ent); ent.apertos = []; }
    if (interrompe) assert.equal(c.acao, null, "a varredura não interrompeu");
    else assert.ok(c.acao || c.mostra > 0, "o corte fraco interrompeu o campeão");
    assert.ok(c.vida > 0, "o campeão não devia morrer de um golpe");
  }
});

test("a mesma semente e os mesmos comandos dão a mesma batalha", () => {
  const um = () => {
    const m = criarMundo({ heroi: "mago" }), ent = entradaVazia(), r = criarRobo();
    for (let i = 0; i < 60 * 20; i++) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    return JSON.stringify(resumo(m));
  };
  assert.equal(um(), um());
});

test("a batalha termina: o herói com o jogador automático vence; sem o herói, as tropas perdem", () => {
  for (const heroi of ["guerreiro", "mago"]) {
    const m = criarMundo({ heroi }), ent = entradaVazia(), r = criarRobo({ nivel: "medio" });
    while (m.fase !== "fim" && m.t < 180) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    assert.equal(m.resultado, "vitoria", `${heroi}: ${m.resultado} em ${m.t.toFixed(0)} s`);
    assert.ok(m.stats.abatesAliados > 0, `${heroi}: as tropas não derrubaram ninguém`);
  }
  const m = criarMundo({ heroi: "guerreiro" }), ent = entradaVazia(), r = criarRobo({ passivo: true });
  while (m.fase !== "fim" && m.t < 180) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
  assert.equal(m.resultado, "derrota");
  assert.ok(m.stats.abatesAliados >= 5, `as tropas sozinhas derrubaram só ${m.stats.abatesAliados}`);
});

test("desempenho do passo: a batalha maior cabe com folga num quadro", () => {
  const m = criarMundo({ heroi: "guerreiro", quantidade: "maior" }), ent = entradaVazia(), r = criarRobo();
  for (let i = 0; i < 60 * 3; i++) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }   // até o contato
  const t0 = performance.now();
  let n = 0;
  while (n < 60 * 10 && m.fase !== "fim") { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; n++; }
  const ms = (performance.now() - t0) / n;
  assert.ok(ms < 4, `passo médio de ${ms.toFixed(2)} ms na batalha maior`);
  assert.ok(n > 300, `a batalha maior acabou cedo demais para medir (${n} passos)`);
});

test("as constantes do campo cabem nas formas: nenhuma área maior que a tela", () => {
  for (const h of Object.values(HEROIS)) for (const k of Object.values(h.kit)) assert.ok((k.raio || 0) < 80 && (k.alcance || 0) < 200);
  assert.ok(CAMPO.largura >= 900 && PASSO === 1 / 60);
});
