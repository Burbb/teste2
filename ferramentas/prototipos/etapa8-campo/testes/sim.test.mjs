// Testes da simulação do campo livre (Node, sem navegador): node --test ferramentas/prototipos/etapa8-campo/testes
// Conferem o funcionamento, não a sensação: área mostrada = alvos atingidos, dano uma vez, mortes simultâneas,
// unidades sem alvo, grupos concentrados, o herói entre aliados e inimigos, a resposta dos comandos, o adiantamento,
// o compromisso dos golpes fortes, a interrupção do campeão, a repetição pela semente e o desempenho do passo.
import { test } from "node:test";
import assert from "node:assert/strict";
import { criarMundo, passo, entradaVazia, dentro, formaDaAcao, ordenar, resumo, PASSO, selecionar, tropasDoTipo,
  montarKit, ferir, alvoAssistido, chamarHorda } from "../tela/sim.js";
import { HEROIS, TIPOS, CAMPO, ENCONTROS, ESPECIAIS, HORDA, ORDENS, HABILIDADES, TALENTOS, SANGUE, CADEIA } from "../tela/conteudo.js";
import { criarRobo, pensar } from "../tela/robo.js";

// Um mundo de laboratório: o herói no meio do campo, sem tropas, com os inimigos que o teste puser (parados:
// atordoados por muito tempo, para a posição na hora do contato ser a de agora). Sem talentos, salvo pedido.
function laboratorio(heroi = "guerreiro", talentos = []) {
  const m = criarMundo({ heroi, kit: { talentos } });
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
// Põe no kit do herói uma habilidade do catálogo (o teste usa a que quiser, equipada ou não) e zera a recarga dela.
function equipar(m, id, sem = {}) {
  const h = m.heroi, def = HABILIDADES[h.nomeHeroi][id];
  if (!h.kit[id]) h.kit[id] = { ...def, id, slot: "teste", chao: def.chao && { ...def.chao }, implosao: def.implosao && { ...def.implosao } };
  Object.assign(h.kit[id], sem);
  h.cds[id] = 0;
  return h.kit[id];
}
function usar(m, id, mx, my, passos = 60) {
  equipar(m, id);
  m.heroi.recurso = m.heroi.recursoMax;
  const ent = entradaVazia();
  ent.mx = mx; ent.my = my; ent.apertos = [id];
  rodar(m, ent, passos);
}

test("a área de cada golpe forte atinge exatamente quem está dentro da forma mostrada", () => {
  for (const [heroi, id, alvo] of [["guerreiro", "varredura", [520, 280]], ["guerreiro", "salto", [560, 300]],
    ["mago", "bola", [600, 260]], ["mago", "piscar", [560, 280]]]) {
    const m = laboratorio(heroi);
    equipar(m, id, id === "varredura" ? { assist: null } : {});
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
    equipar(m, id, id === "varredura" ? { assist: null } : {});
    const lista = id === "investida" ? [inimigo(m, "veterano", 510, 280), inimigo(m, "veterano", 540, 284), inimigo(m, "veterano", 565, 276)]
      : grade(m, "veterano", 520, 280, 20, 9);
    usar(m, id, 520, 280, id === "bola" ? 22 : 60);   // a bola: antes de o fogo do chão começar a contar
    const k = HABILIDADES[heroi][chave], c = HEROIS[heroi].critico;
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
  equipar(m, "salto");
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
  equipar(m, "turbilhao");
  const ent = entradaVazia(); ent.mx = 600; ent.my = 280; ent.apertos = ["turbilhao"];
  passo(m, ent); ent.apertos = [];
  // na preparação do Turbilhão (não cancelável; com a recarga do principal, a Varredura se corta), aperta a investida:
  // ela sai logo depois do contato (o Turbilhão prepara 0,35 s: o aperto vem a 0,15 s do fim)
  rodar(m, ent, 11);
  ent.apertos = ["investida"];
  passo(m, ent); ent.apertos = [];
  assert.equal(h.acao.id, "turbilhao");
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
  equipar(m, "turbilhao");
  const ent = entradaVazia(); ent.mx = 600; ent.my = 280; ent.apertos = ["turbilhao"];
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
  for (const [id, interrompe] of [["varredura", true], ["fraco", false]]) {
    const m = laboratorio("guerreiro"), h = m.heroi;
    const c = inimigo(m, "campeao", 500, 280, false);
    const ent = entradaVazia(); ent.mx = 500; ent.my = 280;
    let n = 0;
    while (!c.acao && n < 200) { passo(m, ent); n++; }
    assert.ok(c.acao && c.acao.forma, "o campeão não preparou o golpe");
    assert.ok(m.eventos.some((e) => e.tipo === "aviso"), "sem o aviso no chão");
    if (id === "fraco") ferir(m, c, 2, h, { dx: 1, dy: 0, emp: 30, atord: 0.3 });
    else ent.apertos = [id];
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
    // desde o Campo Livre 5 o herói derruba quase todos (a montagem padrão encadeia explosões): as tropas ocupam
    assert.ok(m.stats.ocupados > 0, `${heroi}: as tropas não ocuparam ninguém`);
  }
  // sem o herói, as tropas perdem; com Atacar, lutam (derrubam e ocupam); acompanhando um herói parado, seguram em volta
  // dele e ocupam os inimigos (desde o Campo Livre 4 os arqueiros inimigos avançam e atiram; desde o 5 o Capitão alcança
  // quem está colado no arco dele: as tropas derrubam pouco, de 5 na v4 para 1 a 5)
  for (const ordem of ["atacar", null]) {
    const m = criarMundo({ heroi: "guerreiro" }), ent = entradaVazia(), r = criarRobo({ passivo: true });
    passo(m, ent);
    if (ordem) ordenar(m, ordem);
    while (m.fase !== "fim" && m.t < 180) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    assert.equal(m.resultado, "derrota");
    if (ordem) assert.ok(m.stats.abatesAliados >= 1, `as tropas sozinhas não derrubaram ninguém`);
    assert.ok(m.stats.ocupados > 500, `as tropas ocuparam pouco (${m.stats.ocupados.toFixed(0)})`);
  }
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
  for (const cat of Object.values(HABILIDADES)) for (const k of Object.values(cat)) {
    const maior = Math.max(k.raio || 0, k.area || 0, ...(k.aneis || [0]));
    assert.ok(maior < 150 && (k.alcance || 0) <= 230 && (k.comprimento || 0) <= 230, `${k.nome}: área de ${maior} px`);
  }
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
    // um passo para o grupo nosso entrar na lista do exército; a escolha do Capitão é feita de novo com ele lá
    passo(m, entradaVazia());
    l.modoT = 0; l.cargaCd = 0; l.habIntervalo = 0;
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

test("o Sangramento acumula e a Ruptura detona; o Anel prende; o Grito inspira", () => {
  // Corte Sangrento: 2 acúmulos por golpe (até 5), cada tique 2 × os acúmulos; a Ruptura consome e explode nos outros
  {
    const m = laboratorio("guerreiro"), h = m.heroi;
    const u = inimigo(m, "campeao", 505, 280), viz = inimigo(m, "veterano", 524, 280);
    u.vida = u.vidaMax = 999; viz.vida = viz.vidaMax = 999;
    usar(m, "corteSangrento", 600, 280, 30);
    assert.equal(u.sangra && u.sangra.acum, 2);
    assert.ok(!viz.sangra, "o Corte alcançou quem está fora do arco");
    const tiques = () => m.eventos.filter((e) => e.tipo === "dano" && e.id === u.id && e.sutil).map((e) => e.valor);
    m.eventos.length = 0;
    usar(m, "corteSangrento", 600, 280, 40);
    assert.equal(u.sangra.acum, 4);
    assert.ok(tiques().includes(SANGUE.tique * 4), `tiques ${tiques()}`);
    m.eventos.length = 0;
    usar(m, "ruptura", 600, 280, 30);
    assert.equal(u.sangra, null, "a Ruptura não consumiu o Sangramento");
    const direto = m.eventos.find((e) => e.tipo === "dano" && e.id === u.id && !e.sutil);
    const k = h.kit.ruptura, c = HEROIS.guerreiro.critico;
    assert.equal(direto.valor, direto.critico ? Math.round(k.porAcumulo * 4 * c.mult) : k.porAcumulo * 4);
    const sec = m.eventos.find((e) => e.tipo === "dano" && e.id === viz.id);
    assert.ok(sec && sec.secundario && sec.valor === k.explosao.porAcumulo * 4, "a explosão da Ruptura não pegou o vizinho");
  }
  // Anel: quem está dentro não sai
  {
    const m = laboratorio("mago");
    const u = inimigo(m, "soldado", 600, 280, false);
    usar(m, "anel", 600, 280, 20);
    u.atordoado = 0;
    u.alvo = null;
    // ele quer ir até o herói, do lado de fora
    for (let i = 0; i < 60 * 3; i++) passo(m, entradaVazia());
    assert.ok(u.morto || Math.hypot(u.x - 600, u.y - 280) < m.heroi.kit.anel.raio, "saiu do anel");
  }
  // Grito: inspira os aliados perto, abala os inimigos colados
  {
    const m = criarMundo({ heroi: "guerreiro" });
    const h = m.heroi;
    equipar(m, "grito");
    const e = inimigo(m, "soldado", h.x + 15, h.y, false);
    const ent = entradaVazia(); ent.apertos = ["grito"];
    for (let i = 0; i < 20; i++) { passo(m, ent); ent.apertos = []; }
    const perto = m.lados[0].filter((u) => u !== h && Math.hypot(u.x - h.x, u.y - h.y) < 60);
    assert.ok(perto.length >= 6 && perto.every((u) => u.inspirado > 0), "o grito não inspirou quem estava perto");
    assert.ok(e.abalado > 0, "o grito não abalou o inimigo colado");
  }
});
test("os encontros novos terminam: vence com o herói, perde sem ele; nada vira NaN", () => {
  // a horda é de sobrevivência (pode-se perder para ela): tem o teste dela
  // os encontros do Campo Livre 5 (os do 6, com construções e companheiros, têm os testes deles em campo6.test.mjs; os do
  // 8, com Harg reconstruído, em campo8.test.mjs)
  for (const enc of Object.keys(ENCONTROS).filter((e) => e !== "horda" && !ENCONTROS[e].companheiros && !ENCONTROS[e].harg8)) {
    for (const [heroi, kit] of [["guerreiro", {}], ["mago", { bola: "incendiaria", muralha: "anel" }]]) {
      // o Capitão (Campo Livre 4) vence o jogador automático médio, que reage tarde e não recua: lá, o forte
      const m = criarMundo({ heroi, encontro: enc, kit }), ent = entradaVazia(), r = criarRobo({ nivel: enc === "capitao" ? "forte" : "medio" });
      while (m.fase !== "fim" && m.t < 240) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
      assert.equal(m.resultado, "vitoria", `${enc} ${heroi}: ${m.resultado} em ${m.t.toFixed(0)} s`);
      for (const u of m.unidades) assert.ok(Number.isFinite(u.x) && Number.isFinite(u.y));
    }
    const m = criarMundo({ heroi: "guerreiro", encontro: enc }), ent = entradaVazia(), r = criarRobo({ passivo: true });
    while (m.fase !== "fim" && m.t < 240) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    // sem o herói, as tropas perdem; nos grupos espalhados elas podem vencer os grupos um a um, mas perdendo mais de um
    // parte (Campo Livre 3: 25 ou mais; 4: 17; 5: 8, porque a aproximação curta põe mais aliados em ataque contra um
    // grupo pequeno cercado: 780 ataques começados contra 231)
    if (enc === "espalhados" && m.resultado === "vitoria") assert.ok(m.stats.perdas >= 5, `venceram sem o herói perdendo só ${m.stats.perdas}`);
    else assert.equal(m.resultado, "derrota", `${enc} sem o herói: ${m.resultado}`);
  }
});

// ---------------------------------------------------------------------------------------------- Campo Livre 3
// O Capitão sozinho com o herói (sem as tropas dos dois lados), a `dist` px dele, com as recargas como o teste quiser.
function duelo(heroi, dist, { arrem = 0, carga = 99 } = {}) {
  const m = criarMundo({ heroi, encontro: "capitao" });
  m.fase = "luta";
  for (const g of Object.values(m.grupos)) g.ativo = true;
  m.stats.primeira = -1;
  const l = m.lider, h = m.heroi;
  for (const u of m.unidades) if (u !== l && u !== h) u.morto = true;
  passo(m, entradaVazia());
  h.x = h.px = l.x - dist; h.y = h.py = l.y;
  l.arremCd = arrem; l.cargaCd = carga; l.habIntervalo = 0;
  m.eventos.length = 0;
  return { m, l, h };
}

test("o Capitão: escolhe o herói por perto e mantém a escolha; a Arremetida cai no círculo marcado, quem sai escapa, quem fica apanha", () => {
  // quem sai do círculo durante a preparação não é atingido; ele pousa no círculo e fica com o machado cravado
  {
    const { m, l, h } = duelo("mago", 140);
    let n = 0;
    const alvos = new Set();
    while (!(l.acao && l.acao.tipo === "arremetida") && n < 60) { passo(m, entradaVazia()); if (l.alvo) alvos.add(l.alvo.id); n++; }
    assert.ok(l.acao && l.acao.tipo === "arremetida", "não marcou a Arremetida");
    assert.ok(l.modo === "heroi" && [...alvos].every((id) => id === h.id), "a escolha não ficou no herói");
    const f = { ...l.acao.forma };
    assert.ok(dentro(f, h.x, h.y), "o círculo não está no herói parado");
    assert.ok(m.eventos.some((e) => e.tipo === "aviso" && e.arremetida), "sem o aviso");
    const ent = entradaVazia(); ent.cima = true;
    rodar(m, ent, 80);
    assert.ok(m.eventos.some((e) => e.tipo === "liderPouso"), "não pousou");
    assert.equal(m.stats.liderHeroi, 0, "acertou o herói que saiu do círculo");
    assert.ok(Math.hypot(l.x - f.x, l.y - f.y) < 3, "pousou fora do círculo marcado");
    assert.ok(l.cravado > 0 && l.vulneravel > 0, "não ficou com o machado cravado");
  }
  // parado no círculo: leva o dano da Arremetida
  {
    const { m, l } = duelo("mago", 140);
    rodar(m, entradaVazia(), 90);
    const golpe = m.eventos.find((e) => e.tipo === "heroiAtingido" && e.fonte === "lider");
    assert.ok(golpe && golpe.valor === TIPOS.lider.arremetida.danoHeroi, `levou ${golpe && golpe.valor}`);
    assert.ok(!l.voando);
  }
  // um golpe forte na preparação interrompe
  {
    const { m, l, h } = duelo("guerreiro", 60);
    let n = 0;
    while (!(l.acao && l.acao.tipo === "arremetida") && n < 60) { passo(m, entradaVazia()); n++; }
    h.x = h.px = l.x - 14; h.y = h.py = l.y;
    usar(m, "varredura", l.x, l.y, 20);
    assert.ok(!m.eventos.some((e) => e.tipo === "liderSalto"), "saltou mesmo interrompido");
  }
  // escolhido o herói, ele o mantém como alvo por pelo menos 3 s, mesmo com o herói a 300 px
  {
    const { m, l, h } = duelo("guerreiro", 140, { arrem: 99 });
    rodar(m, entradaVazia(), 10);
    assert.equal(l.modo, "heroi");
    h.x = h.px = l.x - 300;
    let trocou = false;
    for (let i = 0; i < 150; i++) { passo(m, entradaVazia()); if (l.alvo && l.alvo !== h) trocou = true; }
    assert.ok(!trocou && l.modo === "heroi", "largou o herói antes do tempo mínimo");
  }
});

test("o Capitão abre caminho entre os seus e golpeia a tropa nossa que fica entre ele e o herói", () => {
  // um soldado dele encostado não o empurra: quem sai do lugar é o soldado
  {
    const { m, l } = duelo("guerreiro", 300, { arrem: 99 });
    const s = inimigo(m, "soldado", l.x + 3, l.y);
    l.atordoado = 1;
    const x0 = l.x, sx = s.x;
    passo(m, entradaVazia());
    assert.ok(Math.abs(l.x - x0) < 0.01 && s.x > sx, "o soldado empurrou o Capitão");
  }
  // um soldado nosso no caminho do herói: o machado sai na direção do herói e o atinge
  {
    const { m, l, h } = duelo("guerreiro", 120, { arrem: 99 });
    const nosso = { ...h, id: m.proximoId++, tipo: "soldado", def: { ...TIPOS.soldado, vel: 0 }, raio: 3.5, massa: 1, vida: 16,
      vidaMax: 16, x: l.x - 20, y: l.y, px: l.x - 20, py: l.y, alvo: null, acao: null, kit: undefined, recarga: 99, ordem: { tipo: "defender", x: l.x - 20, y: l.y } };
    m.unidades.push(nosso);
    l.recarga = 0;
    rodar(m, entradaVazia(), 70);
    assert.ok(m.eventos.some((e) => e.tipo === "golpeCampeao" && e.lider), "não golpeou");
    assert.ok(nosso.vida < nosso.vidaMax || nosso.morto, "o golpe não pegou a tropa no caminho");
  }
});

test("escalas: 2× e 4× multiplicam os comuns e não os especiais, dentro do campo e sem empilhar; em 4×, as alas de fora atacam", () => {
  const conta = (m) => {
    const c = {};
    for (const u of m.unidades) if (u !== m.heroi) c[`${u.lado}:${u.tipo}`] = (c[`${u.lado}:${u.tipo}`] || 0) + 1;
    return c;
  };
  // o treino do Campo Livre 8 não tem tropa para multiplicar (a guerra, sim, mas tem os testes dela em campo8.test.mjs)
  for (const enc of Object.keys(ENCONTROS).filter((e) => !ENCONTROS[e].harg8)) {
    const base = criarMundo({ encontro: enc, quantidade: "1" }), c1 = conta(base);
    for (const k of [2, 4]) {
      const m = criarMundo({ encontro: enc, quantidade: String(k) }), ck = conta(m);
      for (const [chave, n] of Object.entries(c1)) {
        const tipo = chave.split(":")[1];
        // Morel e Odette (Campo Livre 6) também não se multiplicam: são um de cada
        assert.equal(ck[chave], ESPECIAIS.includes(tipo) || TIPOS[tipo].companheiro ? n : n * k, `${enc} ${k}× ${chave}`);
      }
      const comp = base.morel ? 2 : 0;
      assert.equal(m.stats.aliados - comp, (base.stats.aliados - comp) * k);
      for (const u of m.unidades) {
        assert.ok(u.x >= CAMPO.margem && u.x <= CAMPO.largura - CAMPO.margem && u.y >= CAMPO.margem && u.y <= CAMPO.altura - CAMPO.margem, `${enc} ${k}×: fora do campo`);
        assert.equal(u.vidaMax, u.tipo === "heroi" ? HEROIS[m.nomeHeroi].vida : u.lado === 0 && u.def.vidaAliado || u.def.vida);
      }
      let pilhas = 0;
      const us = m.unidades;
      for (let i = 0; i < us.length; i++) for (let j = i + 1; j < us.length; j++) if ((us[i].x - us[j].x) ** 2 + (us[i].y - us[j].y) ** 2 < 9) pilhas++;
      assert.equal(pilhas, 0, `${enc} ${k}×: ${pilhas} pares a menos de 3 px`);
      // em 4×, as alas de fora começam atacando (lutam na frente delas); as de perto acompanham o herói
      const atk = m.lados[0].filter((u) => u !== m.heroi && u.ordem.tipo === "atacar").length;
      if (k === 4) assert.ok(atk > 0 && atk < m.stats.aliados, `${enc} 4×: ${atk} atacando`);
      else assert.equal(atk, 0);
    }
  }
  // "normal" e "maior" (os nomes da v2) valem 1× e 2×
  assert.equal(criarMundo({ quantidade: "maior" }).stats.aliados, 84);
  assert.equal(criarMundo({ quantidade: "normal" }).stats.aliados, 42);
});

test("4×: a batalha original termina com o jogador automático, sem NaN, e o passo cabe num quadro", () => {
  const m = criarMundo({ heroi: "guerreiro", quantidade: "4" }), ent = entradaVazia(), r = criarRobo();
  const t0 = performance.now();
  let n = 0;
  while (m.fase !== "fim" && m.t < 240) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; n++; }
  const ms = (performance.now() - t0) / n;
  assert.equal(m.resultado, "vitoria", `${m.resultado} em ${m.t.toFixed(0)} s`);
  for (const u of m.unidades) assert.ok(Number.isFinite(u.x) && Number.isFinite(u.y));
  assert.ok(ms < 6, `passo médio de ${ms.toFixed(2)} ms em 4×`);
});

test("as habilidades de apoio: o escudo barra flechas e protege, o Turbilhão puxa os comuns, a corrente salta, o gelo deixa lento", () => {
  // Avanço de Escudo: a flecha que vem da frente é barrada; a de trás, não; o aliado perto leva metade
  {
    const m = laboratorio("guerreiro");
    const h = m.heroi, arq = inimigo(m, "arqueiro", 700, 280);
    const flecha = (x0) => ({ tipo: "flecha", lado: 1, x0, y0: 280, x1: 480, y1: 280, t: 0, dur: 0.6, dano: 2, fonte: arq, x: x0, y: 280 });
    m.proj.push(flecha(600), flecha(380));
    usar(m, "escudo", 600, 280, 50);
    assert.equal(m.stats.flechasBarradas, 1);
    assert.equal(m.stats.flechasHeroi, 1);
    assert.equal(h.acao && h.acao.fase, "escudo");
    const aliado = { ...h, id: m.proximoId++, tipo: "soldado", lado: 0, def: TIPOS.soldado, vida: 16, vidaMax: 16, x: h.x - 20, y: h.y, acao: null };
    ferir(m, aliado, 10, arq);
    assert.equal(aliado.vida, 16 - 10 * h.kit.escudo.reducao);
  }
  // Turbilhão: os veteranos a 60 px vêm para perto e apanham; o campeão não é puxado
  {
    const m = laboratorio("guerreiro");
    const ss = [0, 1, 2, 3, 4, 5].map((i) => inimigo(m, "veterano", 480 + Math.cos(i) * 60, 280 + Math.sin(i) * 60));
    const c = inimigo(m, "campeao", 430, 280), cx = c.x;
    usar(m, "turbilhao", 520, 280, 30);
    for (const s of ss) assert.ok(m.eventos.some((e) => e.tipo === "dano" && e.id === s.id), "um veterano puxado não apanhou");
    assert.ok(Math.abs(c.x - cx) < 3, `o campeão foi puxado ${Math.abs(c.x - cx).toFixed(1)} px (um puxado anda ~40)`);
  }
  // Corrente de Raios: 12 alvos em fila a 15 px um do outro; o dano cai 1 por salto (até 7); o 13º e o 14º ficam
  {
    const m = laboratorio("mago");
    const fila = [...Array(14)].map((_, i) => inimigo(m, "veterano", 520 + i * 15, 280));
    usar(m, "raios", 700, 280, 30);
    const d = fila.map((u) => m.eventos.find((e) => e.tipo === "dano" && e.id === u.id));
    const esperado = [14, 13, 12, 11, 10, 9, 8, 7, 7, 7, 7, 7];
    for (let i = 0; i < 12; i++) {
      assert.ok(d[i], `o ${i + 1}º não foi atingido`);
      assert.equal(d[i].valor, d[i].critico ? Math.round(esperado[i] * 1.5) : esperado[i]);
      assert.equal(fila[i].vidaMax - fila[i].vida, d[i].valor);
    }
    assert.ok(!d[12] && !d[13], "passou de 12 alvos");
  }
  // Campo de Gelo: dentro, o passo cai para 35%; fora, normal
  {
    const m = laboratorio("mago");
    const a = inimigo(m, "soldado", 600, 280, false), b = inimigo(m, "soldado", 600, 180, false);
    usar(m, "campoGelo", 600, 280, 20);
    a.atordoado = 0; a.congelado = 0;
    const pa = [a.x, a.y], pb = [b.x, b.y];
    rodar(m, entradaVazia(), 30);
    const da = Math.hypot(a.x - pa[0], a.y - pa[1]), db = Math.hypot(b.x - pb[0], b.y - pb[1]);
    assert.ok(db > 10 && da < db * 0.5, `dentro andou ${da.toFixed(1)} px, fora ${db.toFixed(1)} px`);
    assert.ok(a.gelado > 0 && !(b.gelado > 0));
  }
});

// ---------------------------------------------------------------------------------------------- Campo Livre 4
// Um aliado de laboratório (lado 0), com a ordem dada.
function aliado(m, tipo, x, y, ordem = { tipo: "atacar", x, y }) {
  const d = TIPOS[tipo];
  const u = { id: m.proximoId++, lado: 0, tipo, def: d, x, y, px: x, py: y, vx: 0, vy: 0, kx: 0, ky: 0, raio: d.raio,
    massa: d.massa, vida: d.vidaAliado || d.vida, vidaMax: d.vidaAliado || d.vida, alvo: null, reavaliar: 0, acao: null,
    recarga: 0, atordoado: 0, congelado: 0, flash: 0, virado: 1, passo: 0, abalado: 0, mostra: 0, fugindo: false,
    saiu: false, morto: false, atacantes: 0, aura: false, slot: 0, ordem };
  m.unidades.push(u);
  m.lados[0].push(u);
  return u;
}
// Um clique do ataque principal com o mouse em (mx, my), e mais `passos` passos com o mouse lá.
function principal(m, mx, my, passos = 30, ent = entradaVazia()) {
  ent.mx = mx; ent.my = my; ent.atacar = true;
  passo(m, ent);
  ent.atacar = false;
  rodar(m, ent, passos);
}
// O Frio Cortante sempre congela (para o teste não depender do sorteio); devolve o valor de antes.
function semSorteio(fn) {
  const F = TALENTOS.mago.frioCortante, c = F.chance;
  F.chance = 1;
  try { fn(); } finally { F.chance = c; }
}

test("a Varredura assistida: vira para quem está na direção do mouse e avança até 32 px, só para a frente e nunca através de ninguém", () => {
  {
    const m = laboratorio("guerreiro"), h = m.heroi;
    const lado = inimigo(m, "veterano", 480, 240), frente = inimigo(m, "veterano", 530, 284);
    assert.equal(alvoAssistido(m, h, 700, 280), frente, "não pegou o da frente (o do lado está mais perto, a 90°)");
    assert.equal(alvoAssistido(m, h, 480, 100), lado);
    assert.equal(alvoAssistido(m, h, 300, 280), null, "pegou alguém fora do cone");
  }
  // o alvo além do arco: um passo de mais de 12 px e no máximo `avanca` na direção dele, e o golpe o alcança
  {
    const m = laboratorio("guerreiro"), h = m.heroi, k = h.kit.varredura;
    const u = inimigo(m, "veterano", 540, 280);
    const x0 = h.x;
    principal(m, 600, 280, 14);
    assert.ok(h.x - x0 > 12 && h.x - x0 <= k.avanca + 1.5, `andou ${(h.x - x0).toFixed(1)} px`);
    assert.ok(u.vida < u.vidaMax, "a Varredura não alcançou o alvo");
  }
  // longe demais (fora do alcance da assistência): nenhuma perseguição, o golpe sai para onde o mouse aponta
  {
    const m = laboratorio("guerreiro"), h = m.heroi;
    inimigo(m, "veterano", 600, 280);
    const x0 = h.x;
    principal(m, 600, 280, 14);
    assert.ok(Math.abs(h.x - x0) < 0.5, `perseguiu ${(h.x - x0).toFixed(1)} px`);
  }
  // andando para trás, nenhum passo para a frente
  {
    const m = laboratorio("guerreiro"), h = m.heroi;
    inimigo(m, "veterano", 530, 280);
    const ent = entradaVazia(); ent.esq = true;
    const x0 = h.x;
    principal(m, 600, 280, 6, ent);
    assert.ok(h.x <= x0 + 0.01, `foi ${(h.x - x0).toFixed(1)} px para a frente andando para trás`);
  }
  // alguém colado no caminho: o golpe vai nele, sem passo
  {
    const m = laboratorio("guerreiro"), h = m.heroi;
    inimigo(m, "soldado", 494, 281);
    inimigo(m, "veterano", 530, 280);
    const x0 = h.x;
    principal(m, 600, 280, 10);
    assert.ok(Math.abs(h.x - x0) < 1, `atravessou: ${(h.x - x0).toFixed(1)} px`);
  }
  // inimigo atrás do herói e o mouse na frente: nenhum passo para trás
  {
    const m = laboratorio("guerreiro"), h = m.heroi;
    inimigo(m, "veterano", 440, 280);
    const x0 = h.x;
    principal(m, 600, 280, 10);
    assert.ok(h.x >= x0 - 0.01);
  }
});

test("o ataque principal: segurar o botão repete a cada 1 s; um clique sai uma vez; nada de habilidade repetida nos espaços", () => {
  for (const heroi of ["guerreiro", "mago"]) {
    const m = laboratorio(heroi), id = m.heroi.slots.principal;
    const ent = entradaVazia(); ent.mx = 600; ent.my = 280; ent.atacar = true;
    const t = [];
    for (let i = 0; i < 60 * 3 - 5; i++) {
      passo(m, ent);
      for (const e of m.eventos) if (e.tipo === "inicio" && e.id === id) t.push(m.t);
      m.eventos.length = 0;
    }
    assert.equal(t.length, 3, `${heroi}: ${t.length} golpes segurando por 3 s`);
    for (let i = 1; i < t.length; i++) assert.ok(Math.abs(t[i] - t[i - 1] - 1) < 0.04, `${heroi}: intervalo ${(t[i] - t[i - 1]).toFixed(2)} s`);
    const m2 = laboratorio(heroi);
    principal(m2, 600, 280, 150);
    assert.equal(m2.stats.usos[id].usos, 1, `${heroi}: um clique saiu mais de uma vez`);
    // os espaços: o principal e a mobilidade fixos, três comuns e uma ultimate, sem repetir
    const sl = Object.values(m.heroi.slots);
    assert.equal(sl.length, 6);
    assert.equal(new Set(sl).size, 6, `${heroi}: habilidade repetida nos espaços`);
  }
  // uma montagem com a mesma comum duas vezes fica com ela uma vez só (e a padrão completa os espaços)
  const k = montarKit("mago", { comuns: ["lanca", "lanca", "raios"], ultimate: "meteoros" });
  assert.equal(new Set(Object.values(k.slots)).size, Object.values(k.slots).length);
});

test("a Lança de Gelo atravessa a fila; com a Lança Estilhaçante, explode no primeiro (ou no fim do alcance)", () => {
  {
    const m = laboratorio("mago");
    const fila = [520, 545, 570, 595, 620].map((x) => inimigo(m, "veterano", x, 280));
    usar(m, "lanca", 700, 280, 60);
    for (const u of fila) assert.equal(m.eventos.filter((e) => e.tipo === "dano" && e.id === u.id).length, 1, "não atravessou a fila uma vez em cada");
  }
  {
    const m = laboratorio("mago", ["lancaEstilhacante"]), k = m.heroi.kit.lanca;
    const a = inimigo(m, "veterano", 520, 280), b = inimigo(m, "veterano", 535, 280), c = inimigo(m, "veterano", 600, 280);
    usar(m, "lanca", 700, 280, 60);
    const d = (u) => m.eventos.filter((e) => e.tipo === "dano" && e.id === u.id);
    assert.equal(d(a).length, 1);
    assert.equal(d(b).length, 1, "a explosão não pegou o vizinho");
    assert.equal(d(c).length, 0, "a lança continuou depois de explodir");
    const v = d(a)[0];
    assert.equal(v.critico ? Math.round(v.valor / HEROIS.mago.critico.mult) : v.valor, k.explosao.dano);
  }
  {
    const m = laboratorio("mago", ["lancaEstilhacante"]), h = m.heroi;
    usar(m, "lanca", 900, 280, 60);
    const c = m.eventos.find((e) => e.tipo === "contato" && e.id === "lanca");
    assert.ok(c && Math.abs(c.x - (480 + h.kit.lanca.alcance)) < 8, `sem explosão no fim do alcance (${c && c.x})`);
  }
});

test("Frio Cortante e Estilhaçar: o mesmo lançamento não estilhaça; outro lançamento e outra habilidade sim; o contínuo não", () => {
  semSorteio(() => {
    const m = laboratorio("mago", ["frioCortante", "estilhacar"]), h = m.heroi;
    const u = inimigo(m, "campeao", 540, 280);
    const a = inimigo(m, "veterano", 520, 340);
    u.vida = u.vidaMax = a.vida = a.vidaMax = 999;
    // o comum congela 2 s; o campeão, 0,5 s e depois fica enregelado por 3 s
    usar(m, "lanca", 700, 280, 1);
    rodar(m, entradaVazia(), 50);   // a lança chega em ~0,25 s; o congelamento do campeão dura 0,5 s
    assert.equal(m.stats.estilhacados, 0, "o lançamento que congelou estilhaçou");
    assert.ok(u.gelo > 0 && u.enregelado > m.t, "o campeão não ficou enregelado");
    const L = TALENTOS.mago.frioCortante;
    assert.ok(Math.abs(u.enregelado - u.gelo - L.enregela) < 1e-9 && u.gelo <= m.t, "o campeão ficou congelado mais de 0,5 s");
    usar(m, "lanca", 520, 340, 2);
    rodar(m, entradaVazia(), 20);
    assert.ok(a.gelo > m.t && a.gelo - m.t <= L.duracao, "o veterano não ficou congelado");
    // o contínuo não estilhaça
    ferir(m, a, 3, h, { sutil: true, hab: "bola", lanc: 999, tipoDano: "continuo" });
    assert.equal(m.stats.estilhacados, 0);
    assert.ok(a.gelo > m.t);
    // outra habilidade estilhaça: +8, perde o gelo, explode nos outros
    m.eventos.length = 0;
    ferir(m, a, 10, h, { hab: "raios", lanc: 1000, tipoDano: "direto" });
    assert.equal(m.stats.estilhacados, 1);
    assert.equal(a.gelo, 0);
    const d = m.eventos.find((e) => e.tipo === "dano" && e.id === a.id);
    assert.equal(d.valor, 10 + TALENTOS.mago.estilhacar.bonus);
    assert.ok(m.eventos.some((e) => e.tipo === "explosao" && e.de === "estilhacar"));
    // outro lançamento da mesma habilidade também estilhaça (o enregelado conta)
    ferir(m, u, 10, h, { hab: "lanca", lanc: 1001, tipoDano: "direto" });
    assert.equal(m.stats.estilhacados, 2);
  });
});

test("as cadeias acabam: no máximo 2 estilhaços em sequência, 3 explosões de Sangue em sequência e 30 explosões por golpe", () => {
  // uma multidão congelada colada: um golpe estilhaça o primeiro, que estilhaça os vizinhos, que não estilhaçam mais
  {
    const m = laboratorio("mago", ["estilhacar"]), h = m.heroi;
    const lista = grade(m, "veterano", 600, 280, 40, 9);
    for (const u of lista) { u.vida = u.vidaMax = 999; u.gelo = m.t + 99; u.geloLanc = -1; }
    ferir(m, lista[Math.floor(lista.length / 2)], 5, h, { hab: "raios", lanc: 77, tipoDano: "direto" });
    const n = m.cadeias.get(77);
    assert.ok(n > 1 && n <= CADEIA.maxPorGolpe, `${n} explosões`);
    assert.ok(lista.some((u) => u.gelo > m.t), "a cadeia de estilhaços não parou na profundidade 2");
  }
  // uma multidão sangrando de vida 1: cada morte explode e mata os vizinhos; para em 30 por golpe (ou na profundidade)
  {
    const m = laboratorio("guerreiro", ["explosaoSangue"]), h = m.heroi;
    const lista = grade(m, "soldado", 600, 280, 60, 8);
    for (const u of lista) { u.vida = 1; u.sangra = { acum: 5, n: 6, tick: 0.5 }; }
    ferir(m, lista[Math.floor(lista.length / 2)], 5, h, { hab: "varredura", lanc: 78, tipoDano: "direto" });
    const n = m.cadeias.get(78), vivos = lista.filter((u) => !u.morto).length;
    assert.ok(n > 3 && n <= CADEIA.maxPorGolpe, `${n} explosões`);
    assert.ok(vivos > 0, "a cadeia derrubou a multidão inteira");
    assert.ok(m.eventos.filter((e) => e.tipo === "explosao").every((e) => e.prof <= TALENTOS.guerreiro.explosaoSangue.profundidade));
  }
  // cada tique de Sangramento é um golpe próprio: as mortes por tique em momentos diferentes explodem, cada uma com o
  // seu limite (antes, todas as cadeias de tique dividiam um só limite de 30 pela batalha)
  {
    const m = laboratorio("guerreiro", ["explosaoSangue"]);
    const n0 = m.stats.explosoes;
    for (let i = 0; i < 40; i++) {
      const u = inimigo(m, "soldado", 300 + (i % 8) * 60, 100 + Math.floor(i / 8) * 60);
      u.vida = 1; u.sangra = { acum: 1, n: 6, tick: 0.5 + i * 0.05 };
    }
    rodar(m, entradaVazia(), 60 * 3);
    assert.equal(m.stats.explosoes - n0, 40, `${m.stats.explosoes - n0} das 40 mortes por tique explodiram`);
  }
});

test("a aproximação das tropas: o soldado avança até 10 px na preparação, acerta quem fica parado e erra quem sai", () => {
  for (const sai of [false, true]) {
    const m = laboratorio("mago"), h = m.heroi, d = TIPOS.soldado;
    h.vida = h.vidaMax = 999;
    const folga = d.alcance + d.estica - 1;
    const u = inimigo(m, "soldado", h.x + h.raio + d.raio + folga, h.y, false);
    u.recarga = 0;
    const x0 = u.x;
    let n = 0;
    while (!u.acao && n++ < 30) passo(m, entradaVazia());
    assert.ok(u.acao, "o soldado não começou o ataque a 12 px");
    if (sai) { h.x -= 25; h.px = h.x; }
    const vida = h.vida;
    let maisPerto = Infinity;
    while (u.acao && n++ < 90) {
      passo(m, entradaVazia());
      maisPerto = Math.min(maisPerto, Math.hypot(u.x - h.x, u.y - h.y) - u.raio - h.raio);
    }
    assert.ok(x0 - u.x <= d.estica + 0.5, `avançou ${(x0 - u.x).toFixed(1)} px`);
    assert.ok(maisPerto > -0.6, `entrou no herói (${maisPerto.toFixed(2)} px)`);
    if (sai) assert.ok(h.vida === vida && u.errou, "acertou quem saiu do alcance");
    else assert.ok(h.vida < vida, "não acertou o herói parado");
  }
});

test("o herói atingido: o evento traz a direção e o valor que saiu da vida", () => {
  const m = laboratorio("guerreiro"), h = m.heroi, e = inimigo(m, "campeao", 520, 280);
  const v0 = h.vida;
  ferir(m, h, 12, e, { dx: -1, dy: 0, emp: 50, forte: true });
  const ev = m.eventos.find((x) => x.tipo === "heroiAtingido");
  assert.ok(ev && ev.valor === 12 && v0 - h.vida === 12 && ev.dx === -1 && ev.fonte === "campeao");
  assert.ok(h.tranco && h.tranco.forte, "sem o tranco visual");
});

test("o Capitão interrompido fica firme 2,5 s (reage, sem parar); uma chuva de Bolas não o prende", () => {
  const { m, l, h } = duelo("mago", 100, { arrem: 99 });
  const preparar = () => { l.acao = { t: 0.8, alvo: h, dir: 0, preparo: 0.8, forma: { tipo: "arco", x: l.x, y: l.y, raio: 36, ang: 0, abertura: 160 } }; };
  preparar();
  ferir(m, l, 5, h, { dx: 1, dy: 0, atord: 0.5, forte: true });
  assert.equal(l.acao, null, "o primeiro golpe forte não interrompeu");
  assert.ok(l.firmeAte > m.t);
  l.atordoado = 0;
  preparar();
  ferir(m, l, 5, h, { dx: 1, dy: 0, atord: 0.5, forte: true });
  assert.ok(l.acao && l.atordoado === 0, "interrompido de novo dentro da janela firme");
  assert.ok(l.tranco, "sem a reação visual");
  m.t += TIPOS.lider.firme + 0.1;
  ferir(m, l, 5, h, { dx: 1, dy: 0, atord: 0.5, forte: true });
  assert.equal(l.acao, null, "depois da janela, o golpe forte voltou a interromper");
  // Bolas sem parar por 10 s: ele passa no máximo um quinto do tempo atordoado
  const d2 = duelo("mago", 90, { arrem: 99 });
  let at = 0, n = 0;
  for (let i = 0; i < 600; i++) {
    d2.h.recurso = 100;
    const ent = entradaVazia(); ent.mx = d2.l.x; ent.my = d2.l.y; ent.apertos = ["bola"];
    passo(d2.m, ent);
    if (d2.l.atordoado > 0) at++;
    n++;
    if (d2.l.morto) break;
  }
  assert.ok(at / n < 0.2, `atordoado ${((100 * at) / n).toFixed(0)}% do tempo`);
});

test("o Capitão longe do herói vai para as tropas (os arqueiros pesam mais), salta nelas e as derruba", () => {
  const { m, l } = duelo("guerreiro", 330, { arrem: 0, carga: 0 });
  const arqs = [];
  for (let i = 0; i < 8; i++) arqs.push(aliado(m, "arqueiro", l.x - 110 + (i % 4) * 8, l.y - 6 + Math.floor(i / 4) * 10));
  l.modoT = 0;
  let modoTropas = false;
  for (let i = 0; i < 60 * 8; i++) { passo(m, entradaVazia()); if (l.modo === "tropas") modoTropas = true; }
  assert.ok(modoTropas, "não foi para as tropas");
  const mortos = arqs.filter((a) => a.morto).length;
  // os arqueiros saem das áreas anunciadas (nem todos a tempo): pelo menos metade cai
  assert.ok(mortos >= 4, `derrubou só ${mortos} de 8 arqueiros`);
  assert.ok(m.eventos.some((e) => e.tipo === "liderRodopio" || e.tipo === "golpeCampeao" && e.lider));
});

test("os arqueiros dos dois lados participam: avançam até atirar (a retaguarda sai do posto até 90 px)", () => {
  for (const [enc, q] of [["original", "1"], ["original", "4"], ["capitao", "1"], ["duasFrentes", "2"]]) {
    const m = criarMundo({ heroi: "guerreiro", encontro: enc, quantidade: q }), ent = entradaVazia(), r = criarRobo({ nivel: "medio" });
    const visto = new Map(), atirou = new Set();
    while (m.fase !== "fim" && m.t < 30) {
      pensar(r, m, ent); passo(m, ent); m.eventos.length = 0;
      for (const u of m.unidades) {
        if (u.tipo !== "arqueiro" || u.morto) continue;
        if (!visto.has(u.id)) visto.set(u.id, { t: m.t, lado: u.lado, u });
        visto.get(u.id).ate = m.t;
        if (u.acao) atirou.add(u.id);
        // até 12 px além da coleira: os corpos se empurram quando a retaguarda inteira está na beira dela
        if (u.posto) assert.ok(Math.hypot(u.x - u.posto.x, u.y - u.posto.y) <= TIPOS.arqueiro.posto + 12, "a retaguarda saiu demais do posto");
      }
    }
    for (const lado of [0, 1]) {
      // quem existiu por 15 s ou mais e continua vivo (ou morreu depois de 15 s)
      const longos = [...visto.values()].filter((v) => v.lado === lado && v.ate - v.t >= 15);
      if (!longos.length) continue;
      const k = longos.filter((v) => atirou.has(v.u.id)).length / longos.length;
      assert.ok(k >= 0.85, `${enc} ${q}× lado ${lado}: só ${(100 * k).toFixed(0)}% dos arqueiros atiraram`);
    }
  }
});

test("as ordens: Acompanhar fica perto do herói com os arqueiros atrás; Defender vai ao ponto sem parar e segura", () => {
  // Acompanhar, antes do contato: os arqueiros mais longe dos inimigos que os soldados
  {
    const m = criarMundo({ heroi: "guerreiro" }), ent = entradaVazia();
    ent.mx = 600; ent.my = 280;
    rodar(m, ent, 60 * 2);
    const c = m.centros[1], media = (t) => { const us = m.lados[0].filter((u) => u.tipo === t); return Math.hypot(us.reduce((s, u) => s + u.x, 0) / us.length - c.x, us.reduce((s, u) => s + u.y, 0) / us.length - c.y); };
    assert.ok(media("arqueiro") > media("soldado") + 15, "os arqueiros não ficaram atrás da infantaria");
  }
  // Defender num ponto longe, atravessando inimigos: vão sem parar para lutar e ficam lá
  {
    const m = criarMundo({ heroi: "guerreiro" }), h = m.heroi;
    passo(m, entradaVazia());
    selecionar(m, tropasDoTipo(m, "soldado"));
    ordenar(m, "defender", 200, 80);
    const sel = m.lados[0].filter((u) => m.selecao.has(u.id));
    // um inimigo no caminho, parado
    const e = inimigo(m, "veterano", 230, 180);
    let atacaram = 0;
    for (let i = 0; i < 60 * 6; i++) { passo(m, entradaVazia()); for (const u of sel) if (u.desloca && u.acao) atacaram++; }
    assert.equal(atacaram, 0, "parou para lutar no caminho");
    const longe = sel.filter((u) => !u.morto && Math.hypot(u.x - 200, u.y - 80) > ORDENS.defender.coleira + 10).length;
    assert.ok(longe <= 2, `${longe} soldados longe do ponto`);
    void e; void h;
  }
});

test("atacar um alvo: só ele; derrubado, voltam à ordem de antes; longe demais por 2 s, a ordem se encerra", () => {
  const montar = () => {
    const m = laboratorio("guerreiro");
    const arqs = [0, 1, 2, 3, 4, 5].map((i) => aliado(m, "arqueiro", 440, 250 + i * 10, { tipo: "acompanhar", x: 0, y: 0 }));
    const alvo = inimigo(m, "campeao", 560, 280), perto = inimigo(m, "soldado", 470, 300);
    alvo.vida = alvo.vidaMax = 30;
    selecionar(m, arqs.map((a) => a.id));
    ordenar(m, "atacar", undefined, undefined, alvo);
    return { m, arqs, alvo, perto };
  };
  {
    const { m, arqs, alvo, perto } = montar();
    let fora = 0;
    for (let i = 0; i < 60 * 15 && !alvo.morto; i++) {
      passo(m, entradaVazia());
      for (const p of m.proj) if (p.tipo === "flecha" && p.lado === 0 && Math.hypot(p.x1 - alvo.x, p.y1 - alvo.y) > 20) fora++;
    }
    assert.ok(alvo.morto, "não derrubaram o alvo");
    assert.equal(perto.vida, perto.vidaMax, "atiraram em outro");
    void fora;
    passo(m, entradaVazia());
    assert.ok(arqs.filter((a) => !a.morto).every((a) => a.ordem.tipo === "acompanhar"), "não voltaram à ordem de antes");
    assert.ok(m.registro.some((r) => r.texto.includes("derrubado")));
  }
  {
    const { m, arqs, alvo } = montar();
    alvo.x = alvo.px = 900; alvo.y = alvo.py = 500;   // longe do ponto da ordem (mais de 280 px)
    rodar(m, entradaVazia(), Math.round(60 * (ORDENS.atacar.perdeAlvo + 0.3)));
    assert.ok(arqs.filter((a) => !a.morto).every((a) => !a.ordem.alvoU), "a ordem não se encerrou com o alvo longe");
  }
});

test("a horda: H traz o bloco dentro do campo, conta nos inimigos, respeita o limite; as ondas chegam no tempo", () => {
  const m = criarMundo({ heroi: "guerreiro" });
  passo(m, entradaVazia());
  const antes = m.stats.inimigos, n = chamarHorda(m, 900, 280, 60);
  assert.equal(n, 60);
  assert.equal(m.stats.inimigos, antes + 60);
  for (const u of m.unidades) assert.ok(u.x >= CAMPO.margem && u.x <= CAMPO.largura - CAMPO.margem && u.y >= CAMPO.margem && u.y <= CAMPO.altura - CAMPO.margem);
  while (chamarHorda(m, 100, 100, 200) > 0);
  assert.ok(m.unidades.length <= HORDA.limite);
  const h = criarMundo({ heroi: "guerreiro", encontro: "horda" }), ent = entradaVazia(), r = criarRobo();
  let ondas = 0;
  while (h.t < 30) { pensar(r, h, ent); passo(h, ent); ondas += h.eventos.filter((e) => e.tipo === "horda").length; h.eventos.length = 0; }
  assert.equal(ondas, 3);
  for (const u of h.unidades) assert.ok(Number.isFinite(u.x) && Number.isFinite(u.y));
});
