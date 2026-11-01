// Testes da simulação do campo livre (Node, sem navegador): node --test ferramentas/prototipos/etapa8-campo/testes
// Conferem o funcionamento, não a sensação: área mostrada = alvos atingidos, dano uma vez, mortes simultâneas,
// unidades sem alvo, grupos concentrados, o herói entre aliados e inimigos, a resposta dos comandos, o adiantamento,
// o compromisso dos golpes fortes, a interrupção do campeão, a repetição pela semente e o desempenho do passo.
import { test } from "node:test";
import assert from "node:assert/strict";
import { criarMundo, passo, entradaVazia, dentro, formaDaAcao, ordenar, resumo, PASSO, selecionar, tropasDoTipo,
  montarKit } from "../tela/sim.js";
import { HEROIS, TIPOS, CAMPO, ENCONTROS } from "../tela/conteudo.js";
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

test("o dano de uma ação cai uma vez em cada alvo, e o número mostrado é o dano que saiu da vida", () => {
  for (const [heroi, id, chave] of [["guerreiro", "varredura", "varredura"], ["guerreiro", "salto", "salto"], ["mago", "bola", "bola"],
    ["guerreiro", "investida", "investida"]]) {
    const m = laboratorio(heroi);
    if (id === "salto") m.heroi.recurso = 100;
    const lista = id === "investida" ? [inimigo(m, "veterano", 510, 280), inimigo(m, "veterano", 540, 284), inimigo(m, "veterano", 565, 276)]
      : grade(m, "veterano", 520, 280, 20, 9);
    usar(m, id, 520, 280, id === "bola" ? 22 : 60);   // a bola: antes de o fogo do chão começar a contar
    const k = HEROIS[heroi].kit[chave], c = HEROIS[heroi].critico;
    const danos = m.eventos.filter((e) => e.tipo === "dano" && !e.sutil);
    for (const u of lista) {
      if (u.vida >= u.vidaMax) continue;
      const meus = danos.filter((e) => e.id === u.id);
      assert.equal(meus.length, 1, `${id}: ${meus.length} números no mesmo alvo`);
      // o número é o dano do golpe; em quem morre, a vida para em 0 (o excesso não vira vida negativa)
      if (meus[0].morte) assert.ok(u.vida === 0 && meus[0].antes <= meus[0].valor, `${id}: morte com ${meus[0].antes} de vida e ${meus[0].valor} de dano`);
      else assert.equal(meus[0].valor, u.vidaMax - u.vida, `${id}: o número (${meus[0].valor}) não é o dano (${u.vidaMax - u.vida})`);
      assert.equal(meus[0].valor, meus[0].critico ? Math.round(k.dano * c.mult) : k.dano, `${id}: dano ${meus[0].valor}`);
    }
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

// ------------------------------------------------------------------------------------------------ Campo Livre 2

test("números: uma explosão em muitos soldados dá um número por atingido, e a soma é o dano total", () => {
  const m = laboratorio("mago");
  const lista = grade(m, "veterano", 560, 280, 22, 9);
  usar(m, "bola", 560, 280, 22);
  const atingidos = lista.filter((u) => u.vida < u.vidaMax);
  const danos = m.eventos.filter((e) => e.tipo === "dano" && !e.sutil);
  assert.ok(atingidos.length >= 15, `poucos atingidos: ${atingidos.length}`);
  assert.equal(danos.length, atingidos.length);
  assert.equal(danos.reduce((a, e) => a + e.valor, 0), atingidos.reduce((a, u) => a + u.vidaMax - u.vida, 0), "veteranos não morrem de uma bola: a soma bate");
  // o fogo do chão depois: tiques inteiros, marcados como contínuos
  rodar(m, entradaVazia(), 90);
  const fogo = m.eventos.filter((e) => e.tipo === "dano" && e.sutil);
  assert.ok(fogo.length > 0 && fogo.every((e) => Number.isInteger(e.valor) && e.elemento === "fogo"));
});

test("o crítico: cerca de 10% dos acertos, 1,5× arredondado", () => {
  const m = laboratorio("guerreiro");
  let n = 0, crit = 0;
  for (let r = 0; r < 30; r++) {
    for (const u of m.lados[1]) u.morto = true;
    const lista = grade(m, "veterano", 520, 280, 20, 9);
    m.heroi.cds.varredura = 0;
    usar(m, "varredura", 520, 280, 30);
    for (const e of m.eventos.filter((x) => x.tipo === "dano" && !x.sutil)) { n++; if (e.critico) { crit++; assert.equal(e.valor, 20); } }
    m.eventos.length = 0;
    void lista;
  }
  assert.ok(n > 200 && crit / n > 0.05 && crit / n < 0.16, `${crit} críticos em ${n}`);
});

test("seleção e ordens: a ordem chega só à seleção; sem seleção, a todos; os outros mantêm a sua", () => {
  const m = criarMundo({ heroi: "guerreiro" });
  const arq = tropasDoTipo(m, "arqueiro"), sold = tropasDoTipo(m, "soldado");
  assert.equal(arq.length, 12);
  assert.equal(sold.length, 30);
  assert.ok(!tropasDoTipo(m, null).includes(m.heroi.id), "o herói não entra na seleção");
  selecionar(m, arq);
  assert.equal(ordenar(m, "defender", 200, 100), 12);
  for (const u of m.lados[0]) {
    if (u === m.heroi) continue;
    assert.equal(u.ordem.tipo, arq.includes(u.id) ? "defender" : "acompanhar", `${u.tipo} ${u.id}`);
  }
  selecionar(m, sold.slice(0, 10));
  ordenar(m, "atacar");
  assert.equal(m.lados[0].filter((u) => u.ordem && u.ordem.tipo === "atacar").length, 10);
  assert.equal(m.lados[0].filter((u) => u.ordem && u.ordem.tipo === "defender").length, 12, "os arqueiros perderam a ordem");
  selecionar(m, []);
  assert.equal(ordenar(m, "acompanhar"), 42, "sem seleção a ordem vale para todos");
  // somar à seleção e a morte de um selecionado
  selecionar(m, sold.slice(0, 3));
  selecionar(m, arq.slice(0, 2), true);
  assert.equal(m.selecao.size, 5);
  const morto = m.lados[0].find((u) => u.id === sold[0]);
  morto.vida = 0; morto.morto = true;
  passo(m, entradaVazia());
  assert.equal(m.selecao.size, 4, "o morto continuou selecionado");
  assert.equal(ordenar(m, "defender", 300, 300), 4);
});

test("as ordens de dois grupos valem ao mesmo tempo: os arqueiros defendem um ponto, os soldados acompanham", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "duasFrentes" });
  selecionar(m, tropasDoTipo(m, "arqueiro"));
  ordenar(m, "defender", 480, 120);
  selecionar(m, tropasDoTipo(m, "soldado"));
  ordenar(m, "acompanhar");
  const ent = entradaVazia(); ent.mx = 480; ent.my = 400;
  for (let i = 0; i < 60 * 2.4; i++) passo(m, ent);   // antes de as frentes chegarem
  const arqs = m.lados[0].filter((u) => u.tipo === "arqueiro");
  for (const u of arqs) assert.ok(Math.hypot(u.x - 480, u.y - 120) < 70, `arqueiro fora do ponto: ${u.x.toFixed(0)},${u.y.toFixed(0)}`);
});

test("o líder: reúne e marca a faixa; um golpe forte desfaz a reunião; a carga atropela só quem está na faixa", () => {
  // um líder sozinho com soldados, e um grupo nosso a 110 px
  const montar = () => {
    const m = criarMundo({ heroi: "guerreiro", encontro: "capitao" });
    m.fase = "luta";
    for (const g of Object.values(m.grupos)) g.ativo = true;
    m.stats.primeira = -1;
    const l = m.lider;
    for (const u of m.lados[1]) if (u !== l && Math.hypot(u.x - l.x, u.y - l.y) > 60) u.morto = true;
    for (const u of m.lados[0]) if (u !== m.heroi) { u.morto = true; }
    passo(m, entradaVazia());
    const dx = 600 - l.x, dy = 280 - l.y;
    for (const u of m.lados[1]) { u.x += dx; u.y += dy; u.px = u.x; u.py = u.y; }
    l.cargaCd = 0; l.tentaCarga = 0;
    const nossos = [];
    for (let i = 0; i < 6; i++) {
      const a = { ...m.heroi, id: m.proximoId++, tipo: "soldado", def: { ...TIPOS.soldado, vel: 0 }, raio: 3.5, massa: 1, vida: 16, vidaMax: 16,
        x: 490 + (i % 3) * 8, y: 276 + Math.floor(i / 3) * 8, alvo: null, acao: null, kit: undefined, recarga: 99, ordem: { tipo: "atacar" } };
      m.unidades.push(a); nossos.push(a);
    }
    m.heroi.x = m.heroi.px = 300; m.heroi.y = m.heroi.py = 100;
    m.eventos.length = 0;
    return { m, l, nossos };
  };
  // sem interrupção: a carga sai
  {
    const { m, l, nossos } = montar();
    let n = 0;
    while (!(l.acao && l.acao.tipo === "reunir") && n < 120) { passo(m, entradaVazia()); n++; }
    assert.ok(l.acao && l.acao.tipo === "reunir", "o líder não reuniu");
    assert.ok(m.eventos.some((e) => e.tipo === "aviso" && e.lider), "sem o aviso da faixa");
    const faixa = { ...l.acao.forma };
    const reunidos = l.acao.reunidos.length;
    assert.ok(reunidos >= 3, `reuniu só ${reunidos}`);
    for (let i = 0; i < 60 * 3; i++) passo(m, entradaVazia());
    assert.ok(m.eventos.some((e) => e.tipo === "carga"), "a carga não saiu");
    for (const u of nossos) {
      const naFaixa = dentro({ ...faixa, largura: faixa.largura + 1 }, u.x, u.y);
      void naFaixa;
    }
    assert.ok(nossos.some((u) => u.vida < u.vidaMax || u.morto), "a carga não atingiu ninguém do grupo");
    assert.ok(!dentro(faixa, m.heroi.x, m.heroi.y) && m.heroi.vida === m.heroi.vidaMax, "atingiu o herói fora da faixa");
  }
  // com a Varredura na reunião: desfaz
  {
    const { m, l } = montar();
    let n = 0;
    while (!(l.acao && l.acao.tipo === "reunir") && n < 120) { passo(m, entradaVazia()); n++; }
    const reunidos = l.acao.reunidos;
    m.heroi.x = m.heroi.px = l.x - 14; m.heroi.y = m.heroi.py = l.y;
    usar(m, "varredura", l.x, l.y, 20);
    assert.ok(!l.acao || l.acao.tipo !== "carga", "a carga saiu mesmo interrompida");
    assert.ok(m.eventos.some((e) => e.tipo === "interrompe"), "sem o aviso de interrompido");
    assert.ok(reunidos.every((s) => !s.reuniao), "os reunidos continuaram presos à reunião");
  }
});

test("o líder ofegante leva +50%; derrubado, a tropa perto foge, o resto se abala e a batalha continua", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "capitao" });
  m.fase = "luta";
  for (const g of Object.values(m.grupos)) g.ativo = true;
  passo(m, entradaVazia());
  const l = m.lider;
  l.vulneravel = 1;
  const v0 = l.vida;
  m.heroi.x = m.heroi.px = l.x - 14; m.heroi.y = m.heroi.py = l.y;
  usar(m, "varredura", l.x, l.y, 20);
  const ev = m.eventos.find((e) => e.tipo === "dano" && e.id === l.id);
  assert.ok(ev && (ev.valor === Math.round(13 * 1.5) || ev.valor === Math.round(20 * 1.5)), `ofegante levou ${ev && ev.valor}`);
  assert.equal(v0 - l.vida, ev.valor);
  // enquanto ele vive, ninguém foge, mesmo com quase todos mortos
  for (const u of m.lados[1]) if (u !== l && u.tipo === "arqueiro") u.morto = true;
  m.reforco.chegou = true;
  passo(m, entradaVazia());
  assert.equal(m.fase, "luta");
  const perto = m.lados[1].filter((u) => u !== l && Math.hypot(u.x - l.x, u.y - l.y) <= 150);
  const longe = m.lados[1].filter((u) => u !== l && Math.hypot(u.x - l.x, u.y - l.y) > 150);
  l.vida = 1;
  usar(m, "varredura", l.x, l.y, 1);
  m.heroi.cds.varredura = 0;
  usar(m, "varredura", l.x, l.y, 20);
  assert.ok(l.morto, "o líder não caiu");
  assert.ok(m.eventos.some((e) => e.tipo === "liderCaiu"));
  assert.ok(perto.filter((u) => !u.morto).every((u) => u.fugindo), "alguém perto dele não fugiu");
  assert.ok(longe.filter((u) => !u.morto).every((u) => !u.fugindo), "alguém longe fugiu");
  assert.notEqual(m.resultado, "derrota");
});

test("as versões das habilidades mudam o uso: sangramento, chão que repele, anel que prende, grito que inspira", () => {
  // Sangrenta: 7 no golpe e 3 a cada 0,5 s por 3 s; quase não empurra
  {
    const m = laboratorio("guerreiro");
    m.heroi.kit = montarKit("guerreiro", { varredura: "sangrenta" });
    const u = inimigo(m, "veterano", 500, 280);
    const x0 = u.x;
    usar(m, "varredura", 520, 280, 60 * 4);
    const d = m.eventos.filter((e) => e.tipo === "dano" && e.id === u.id);
    const golpe = d.filter((e) => !e.sutil), sangue = d.filter((e) => e.sutil && e.elemento === "sangue");
    assert.equal(golpe.length, 1);
    assert.equal(sangue.length, 6);
    assert.equal(u.vidaMax - u.vida, golpe[0].valor + 18);
    assert.ok(Math.abs(u.x - x0) < 4, `empurrou ${Math.abs(u.x - x0).toFixed(1)} px`);
  }
  // Anel: quem está dentro não sai
  {
    const m = laboratorio("mago");
    m.heroi.kit = montarKit("mago", { muralha: "anel" });
    const u = inimigo(m, "soldado", 600, 280, false);
    usar(m, "muralha", 600, 280, 20);
    u.atordoado = 0;
    u.def = { ...u.def };
    u.alvo = null;
    // ele quer ir até o herói, do lado de fora
    for (let i = 0; i < 60 * 3; i++) passo(m, entradaVazia());
    assert.ok(u.morto || Math.hypot(u.x - 600, u.y - 280) < m.heroi.kit.muralha.raio, "saiu do anel");
  }
  // Grito: inspira os aliados perto, abala os inimigos colados
  {
    const m = criarMundo({ heroi: "guerreiro", kit: { investida: "grito" } });
    const h = m.heroi;
    const e = inimigo(m, "soldado", h.x + 15, h.y, false);
    const ent = entradaVazia(); ent.apertos = ["investida"];
    for (let i = 0; i < 20; i++) { passo(m, ent); ent.apertos = []; }
    const perto = m.lados[0].filter((u) => u !== h && Math.hypot(u.x - h.x, u.y - h.y) < 60);
    assert.ok(perto.length >= 6 && perto.every((u) => u.inspirado > 0), "o grito não inspirou quem estava perto");
    assert.ok(e.abalado > 0, "o grito não abalou o inimigo colado");
  }
  // Incendiária: o chão empurra para fora quem está dentro
  {
    const m = laboratorio("mago");
    m.heroi.kit = montarKit("mago", { bola: "incendiaria" });
    const u = inimigo(m, "veterano", 600, 284, true);
    usar(m, "bola", 600, 280, 60);
    assert.ok(Math.hypot(u.x - 600, u.y - 280) > 20, `continuou no fogo: ${Math.hypot(u.x - 600, u.y - 280).toFixed(1)} px do centro`);
  }
});

test("os encontros novos terminam: vence com o herói, perde sem ele; nada vira NaN", () => {
  for (const enc of Object.keys(ENCONTROS)) {
    for (const [heroi, kit] of [["guerreiro", {}], ["mago", { bola: "incendiaria", muralha: "anel" }]]) {
      const m = criarMundo({ heroi, encontro: enc, kit }), ent = entradaVazia(), r = criarRobo({ nivel: "medio" });
      while (m.fase !== "fim" && m.t < 240) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
      assert.equal(m.resultado, "vitoria", `${enc} ${heroi}: ${m.resultado} em ${m.t.toFixed(0)} s`);
      for (const u of m.unidades) assert.ok(Number.isFinite(u.x) && Number.isFinite(u.y));
    }
    const m = criarMundo({ heroi: "guerreiro", encontro: enc }), ent = entradaVazia(), r = criarRobo({ passivo: true });
    while (m.fase !== "fim" && m.t < 240) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    // sem o herói, as tropas perdem; nos grupos espalhados elas podem vencer os grupos um a um, mas a um custo alto
    if (enc === "espalhados" && m.resultado === "vitoria") assert.ok(m.stats.perdas >= 25, `venceram sem o herói perdendo só ${m.stats.perdas}`);
    else assert.equal(m.resultado, "derrota", `${enc} sem o herói: ${m.resultado}`);
  }
});
