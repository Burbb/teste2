// Testes do Campo Livre 9 (node --test): a guerra nova (campo9.js). As variações sorteadas e as combinações delas, os
// barris e as cargas, as áreas que acertam serem as do aviso, a passagem das ondas para o General, o sorteio que se
// repete, os golpes novos sem erro, a derrota e a vitória em cada fase. As regras, não a diversão.
import { test } from "node:test";
import assert from "node:assert/strict";
import { criarMundo, passo, entradaVazia, ferir, dentro } from "../tela/sim.js";
import { aplicarControle } from "../tela/campo7.js";
import { VARIACOES, GENERAL9, VESNA9 } from "../tela/conteudo.js";
import { estado9, resumo9 } from "../tela/campo9.js";
import { criarRobo, pensar } from "../tela/robo.js";

function rodar(m, s, ent = entradaVazia(), cada = null) {
  for (let t = 0; t < s && m.fase !== "fim"; t += 1 / 60) { passo(m, ent); if (cada) cada(m); m.eventos.length = 0; }
}
// o treino com as variações escolhidas para o primeiro herói (no lugar das sorteadas); devolve o mundo e o herói, já em campo
function treinoCom(variacoes, sorteio = 1) {
  const m = criarMundo({ heroi: "guerreiro", encontro: "treino9", sorteio });
  m.g9.herois[0].variacoes = variacoes;
  for (let i = 0; i < 400 && !m.g9.herois[0].entrou; i++) { passo(m, entradaVazia()); m.eventos.length = 0; }
  return { m, u: m.g9.herois[0].u, h: m.heroi };
}
// derruba quem entra (os heróis e, entradas todas, o resto) até o General chegar
function ateGeneral(m) {
  for (let i = 0; i < 20000 && !m.g9.general.u; i++) {
    passo(m, entradaVazia());
    for (const u of m.lados[1]) if (!u.morto && !u.general && (u.heroi9 || m.g9.herois.every((e) => e.entrou))) ferir(m, u, 99999, m.heroi, {});
    m.eventos.length = 0;
  }
  return m.g9.general.u;
}

test("as variações: inabalável não fica preso nem quebra; gélido deixa lento e congela no segundo acerto; venenoso, vampírico, implacável", () => {
  // inabalável: nenhum controle pega, a postura não sobe, o empurrão quase não o move
  {
    const { m, u } = treinoCom(["inabalavel"]);
    assert.equal(aplicarControle(m, u, "atordoado", 1, m.heroi), 0);
    assert.equal(aplicarControle(m, u, "lento", 2, m.heroi, { fator: 0.5 }), 0);
    ferir(m, u, 5, m.heroi, { forte: true, atord: 1, emp: 300, dx: 1, dy: 0 });
    passo(m, entradaVazia());
    assert.ok(!(u.atordoado > 0) && !(u.lentoAte > m.t), "ficou preso");
    if (u.h8) assert.equal(u.h8.postura, 0, "a postura subiu");
    assert.ok(u.massa >= 60);
  }
  // gélido: o primeiro acerto deixa lento; o segundo em 4 s congela (atordoado)
  {
    const { m, u, h } = treinoCom(["gelido"]);
    ferir(m, h, 1, u, { dx: 1, dy: 0 });
    assert.ok(h.lentoAte > m.t && !(h.atordoado > 0), "o primeiro não deixou lento");
    rodar(m, 1);
    ferir(m, h, 1, u, { dx: 1, dy: 0 });
    assert.ok(h.atordoado > 0 && h.congelado9 > m.t, "o segundo não congelou");
  }
  // venenoso: cada acerto soma uma dose (até três); o veneno tira vida sozinho e acaba em 3 s
  {
    const { m, u, h } = treinoCom(["venenoso"]);
    const V = VARIACOES.venenoso.veneno;
    for (let i = 0; i < 5; i++) ferir(m, h, 1, u, { dx: 1, dy: 0 });
    assert.equal(h.veneno9.doses, V.max);
    u.h8 ? (u.h8.pausa = 99, u.h8.investidaCd = 99, u.h8.recuoCd = 99) : null;
    u.x = h.x + 300;
    const antes = h.vida;
    rodar(m, V.dura + 0.5);
    assert.ok(Math.abs(antes - h.vida - V.tique * V.max * (V.dura / V.cada)) <= V.tique * V.max + 0.01, `o veneno tirou ${antes - h.vida}`);
  }
  // vampírico: recupera a metade do dano que causa (não com o veneno, não acima da vida máxima)
  {
    const { m, u, h } = treinoCom(["vampirico", "venenoso"]);
    u.vida = u.vidaMax - 50;
    ferir(m, h, 20, u, { dx: 1, dy: 0 });
    assert.equal(u.vida, u.vidaMax - 40);
    const v = u.vida;
    u.x = h.x + 300; if (u.h8) { u.h8.pausa = 99; u.h8.investidaCd = 99; u.h8.recuoCd = 99; }
    rodar(m, 2);
    assert.ok(u.vida <= v + 0.01, "o veneno curou o vampírico");
  }
  // implacável: mais rápido e com as recargas mais curtas
  {
    const { u } = treinoCom(["implacavel"]);
    assert.equal(u.velF, VARIACOES.implacavel.vel);
    assert.equal(u.ritmo9, VARIACOES.implacavel.ritmo);
  }
});

test("as combinações de duas variações, em cada herói, rodam sem erro, sem NaN e sem uma regra chamando a outra sem fim", () => {
  const ids = Object.keys(VARIACOES);
  for (let a = 0; a < ids.length; a++) for (let b = a + 1; b < ids.length; b++) for (const sorteio of [1, 2, 3]) {
    const m = criarMundo({ heroi: sorteio === 2 ? "mago" : "guerreiro", encontro: "treino9", sorteio });
    m.g9.herois[0].variacoes = [ids[a], ids[b]];
    const r = criarRobo({ nivel: "forte" }), ent = entradaVazia();
    let maxEventos = 0;
    while (m.t < 14 && m.fase !== "fim") { pensar(r, m, ent); passo(m, ent); maxEventos = Math.max(maxEventos, m.eventos.length); m.eventos.length = 0; }
    const u = m.g9.herois[0].u;
    assert.ok(u, `${ids[a]}+${ids[b]} (${sorteio}): o herói não entrou`);
    for (const v of m.unidades) assert.ok(Number.isFinite(v.x) && Number.isFinite(v.y) && Number.isFinite(v.vida), `${ids[a]}+${ids[b]}: NaN em ${v.tipo}`);
    assert.ok(u.vida <= u.vidaMax && m.heroi.vida <= m.heroi.vidaMax);
    assert.ok(maxEventos < 400, `${ids[a]}+${ids[b]}: ${maxEventos} eventos num passo`);
    assert.ok(m.g9.cargas.every((c) => c.alvo === 0 || c.alvo === "todos"));
  }
});

test("o barril: aceso fere só os nossos; derrubado, fere os dois lados; o rastro explosivo não fere os dele", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "guerra9", sorteio: 2 });
  m.fase = "luta";
  const nosso = m.lados[0].find((u) => u.tipo === "soldado"), deles = m.lados[1].find((u) => u.tipo === "soldado");
  const sap = m.lados[1].find((u) => u.tipo === "soldado" && u !== deles);
  for (const u of [nosso, deles, sap]) { u.atordoado = 99; u.vida = 1000; u.vidaMax = 1000; }
  const pos = (u, x, y) => { u.x = u.px = x; u.y = u.py = y; };
  pos(nosso, 150, 100); pos(deles, 160, 100);
  // o barril aceso (alvo 0) e o rastro: só os nossos
  m.g9.cargas.push({ x: 155, y: 100, raio: 30, t: 0, dur: 0.05, dano: 10, danoHeroi: 10, emp: 0, atord: 0, alvo: 0, fonte: sap, barril: true });
  rodar(m, 0.1);
  assert.ok(nosso.vida < 1000 && deles.vida === 1000, `aceso: nosso ${nosso.vida}, deles ${deles.vida}`);
  // o barril caído: os dois
  nosso.vida = deles.vida = 1000;
  m.g9.cargas.push({ x: 155, y: 100, raio: 30, t: 0, dur: 0.05, dano: 10, danoHeroi: 10, emp: 0, atord: 0, alvo: "todos", fonte: sap, barril: true });
  rodar(m, 0.1);
  assert.ok(nosso.vida < 1000 && deles.vida < 1000, `caído: nosso ${nosso.vida}, deles ${deles.vida}`);
  // a borda: o pé fora do círculo não leva (a mesma regra do círculo desenhado)
  nosso.vida = 1000; pos(nosso, 155 + 30.5, 100);
  m.g9.cargas.push({ x: 155, y: 100, raio: 30, t: 0, dur: 0.05, dano: 10, danoHeroi: 10, emp: 0, atord: 0, alvo: "todos", fonte: sap });
  rodar(m, 0.1);
  assert.equal(nosso.vida, 1000, "levou fora do círculo");
  // o sapador de verdade: derrubado no meio dos dele, o barril cai e fere quem estiver em volta, dos dois lados
  const m2 = criarMundo({ heroi: "guerreiro", encontro: "guerra9", sorteio: 2 });
  m2.fase = "luta";
  const s2 = m2.lados[1].find((u) => u.tipo === "soldado");
  s2.def = { ...s2.def, barril: { arma: 0.9, cai: 0.45, perto: 10, busca: 260, raio: 30, dano: 14, danoHeroi: 26, empurrao: 0, atordoa: 0 } };
  const vizinho = m2.lados[1].find((u) => u.tipo === "soldado" && u !== s2);
  vizinho.x = vizinho.px = s2.x + 6; vizinho.y = vizinho.py = s2.y; vizinho.atordoado = 99;
  ferir(m2, s2, 999, m2.heroi, {});
  assert.equal(m2.g9.cargas.length, 1);
  assert.equal(m2.g9.cargas[0].alvo, "todos");
  rodar(m2, 0.6);
  assert.ok(vizinho.morto || vizinho.vida < vizinho.vidaMax, "o barril caído não feriu o vizinho do sapador");
});

test("o que acerta é o que o aviso mostrou: cada golpe do General, estágio por estágio", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "guerra9", sorteio: 3 });
  const g = ateGeneral(m);
  assert.ok(g, "o General não veio");
  const h = m.heroi;
  h.vidaMax = h.vida = 1e6;
  for (const id of ["ceifa", "estocada", "correntes", "terremoto", "cruz", "salto"]) {
    // a nossa tropa espalhada em volta dele (parada), você colado
    const tropa = m.lados[0].filter((u) => u !== h && !u.morto);
    g.x = g.px = 480; g.y = g.py = 300; h.x = h.px = 480 - 40; h.y = h.py = 300; h.vida = h.vidaMax;
    tropa.forEach((u, i) => {
      const a = i * 2.4, r = 12 + ((i * 37) % 200);
      u.x = u.px = 480 + Math.cos(a) * r; u.y = u.py = 300 + Math.sin(a) * r; u.atordoado = 99; u.vida = u.vidaMax = 1000; u.kx = u.ky = 0;
    });
    const s = g.h8;
    s.golpe = null; s.passo = null; s.quebrado = 0; s.postura = 0; s.rodopioCd = 99;   // sem o Terremoto contra o cerco
    // o salto vem antes das sequências (sem pausa, ele começaria outro golpe na tropa em volta)
    if (id === "salto") { s.investidaCd = 0; s.pausa = 99; h.x = h.px = 480 - 200; } else { s.fila = [id]; s.pausa = 0; s.investidaCd = 99; }
    if (id === "cruz") s.fase = 2;
    let formas = null, golpe = null;
    const vidas = new Map(tropa.map((u) => [u.id, u.vida]));
    for (let i = 0; i < 300; i++) {
      passo(m, entradaVazia()); m.eventos.length = 0;
      if (!golpe && s.golpe && s.golpe.id === id) golpe = s.golpe;
      if (golpe && !formas && golpe.etapa === "exec") {
        // as formas e onde cada um estava quando o golpe começou a estourar (os empurrões vêm depois)
        formas = golpe.formasEstagio ? golpe.formasEstagio.flat() : [golpe.forma];
        for (const u of tropa) u.antes9 = { x: u.x, y: u.y };
      }
      if (golpe && golpe.etapa === "rec") break;
    }
    assert.ok(formas, `${id}: não executou`);
    for (const u of tropa) {
      if (u.x < 0) continue;
      const levou = u.vida < vidas.get(u.id) || u.morto, estava = formas.some((f) => dentro(f, u.antes9.x, u.antes9.y));
      assert.equal(levou, estava, `${id}: ${u.tipo} em ${Math.round(u.antes9.x)},${Math.round(u.antes9.y)} ${estava ? "dentro do aviso não levou" : "fora do aviso levou"}`);
    }
    s.golpe = null; s.fila = []; s.pausa = 99; s.fase = 1;
  }
});

test("a guerra: o General vem uma vez, só sem ondas por vir e sem ninguém do lado inimigo; ninguém foge; a vitória uma vez", () => {
  for (const [heroi, sorteio] of [["guerreiro", 1], ["mago", 5]]) {
    // o mago no sorteio 5: um cão encurralava Odette num canto e o General nunca vinha (a correção está em campo6.odette)
    const m = criarMundo({ heroi, encontro: "guerra9", sorteio });
    const r = criarRobo({ nivel: "forte" }), ent = entradaVazia();
    let generais = 0, vitorias = 0, fugiu = false, cedo = null;
    while (m.fase !== "fim" && m.t < 400) {
      pensar(r, m, ent); passo(m, ent);
      for (const e of m.eventos) {
        if (e.tipo === "general9Entra") {
          generais++;
          const vivos = m.lados[1].filter((u) => !u.morto && !u.general).length;
          if (m.g9.ondas.proxima <= m.g9.ondas.ate || vivos || !m.g9.herois.every((h) => h.u && h.u.morto)) cedo = { t: m.t, vivos };
        }
        if (e.tipo === "fuga") fugiu = true;
      }
      if (m.lados[1].some((u) => u.fugindo)) fugiu = true;
      m.eventos.length = 0;
    }
    vitorias = m.registro.filter((x) => x.texto === "Vitória.").length;
    assert.equal(generais, 1, `${heroi} ${sorteio}: o General veio ${generais} vezes`);
    assert.equal(cedo, null, `${heroi} ${sorteio}: veio cedo ${JSON.stringify(cedo)}`);
    assert.ok(!fugiu, `${heroi} ${sorteio}: alguém fugiu`);
    assert.equal(m.fase, "fim");
    if (m.resultado === "vitoria") assert.equal(vitorias, 1);
    assert.equal(estado9(m).fase, m.resultado === "vitoria" ? "fim" : estado9(m).fase);
  }
});

test("o sorteio se repete: o mesmo número dá as mesmas ondas, a mesma ordem, as mesmas variações e a mesma luta", () => {
  const rodada = (sorteio) => {
    const m = criarMundo({ heroi: "guerreiro", encontro: "guerra9", sorteio, semente: sorteio });
    const r = criarRobo({ nivel: "forte" }), ent = entradaVazia();
    while (m.t < 60) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; }
    const z = resumo9(m);
    return JSON.stringify({ z, pos: m.unidades.filter((u) => !u.morto).map((u) => [u.tipo, Math.round(u.x), Math.round(u.y)]) });
  };
  assert.equal(rodada(48213), rodada(48213));
  assert.notEqual(rodada(48213), rodada(1234));
});

test("os golpes novos de Vesna e do General saem sem erro e sem NaN; os heróis caem rápido e o General não", () => {
  const m = criarMundo({ heroi: "guerreiro", encontro: "treino9", sorteio: 1 });   // Vesna é a primeira no sorteio 1
  for (let i = 0; i < 400 && !m.g9.herois[0].entrou; i++) { passo(m, entradaVazia()); m.eventos.length = 0; }
  const v = m.g9.herois[0].u, h = m.heroi;
  assert.equal(v.tipo, "vesna");
  h.vidaMax = h.vida = 1e6;
  for (const id of Object.keys(VESNA9.golpes)) {
    v.h8.golpe = null; v.h8.fila = [id]; v.h8.pausa = 0; v.h8.recuoCd = 99; v.h8.investidaCd = id === "investida" ? 0 : 99;
    h.x = h.px = v.x - (id === "investida" ? 100 : id === "leque" ? 90 : 20); h.y = h.py = v.y;
    let viu = false;
    for (let i = 0; i < 200; i++) { passo(m, entradaVazia()); m.eventos.length = 0; if (v.h8.golpe && v.h8.golpe.id === id) viu = true; }
    assert.ok(viu, `Vesna: ${id} não saiu`);
    assert.ok(Number.isFinite(v.x) && Number.isFinite(v.y));
  }
  assert.ok(VESNA9.vida <= 250 && GENERAL9.vida >= 2500);
  const g = ateGeneral(m);
  for (const id of Object.keys(GENERAL9.golpes)) {
    g.h8.golpe = null; g.h8.quebrado = 0; g.h8.fila = id === "salto" ? [] : [id]; g.h8.pausa = 0; g.h8.investidaCd = id === "salto" ? 0 : 99;
    if (id === "brado") { g.h8.fila = []; g.h8.fase = 1; g.vida = g.vidaMax * 0.4; }
    h.x = h.px = g.x - (id === "salto" ? 200 : 40); h.y = h.py = g.y;
    let viu = false;
    for (let i = 0; i < 240; i++) { passo(m, entradaVazia()); m.eventos.length = 0; if (g.h8.golpe && g.h8.golpe.id === id) viu = true; }
    assert.ok(viu, `General: ${id} não saiu`);
    for (const u of m.unidades) assert.ok(Number.isFinite(u.x) && Number.isFinite(u.y), `NaN depois de ${id}`);
  }
});

test("a derrota e a vitória em cada fase: caído nas ondas, diante de um herói ou do General, é derrota; a vitória não vira derrota", () => {
  for (const fase of ["ondas", "heroi", "general"]) {
    const m = criarMundo({ heroi: "guerreiro", encontro: "guerra9", sorteio: 6 });
    if (fase === "ondas") rodar(m, 12);
    if (fase === "heroi") rodar(m, 21);
    if (fase === "general") ateGeneral(m);
    ferir(m, m.heroi, 99999, m.lados[1].find((u) => !u.morto) || null, {});
    // o General cai logo depois: a derrota fica
    if (fase === "general") ferir(m, m.g9.general.u, 99999, m.heroi, {});
    rodar(m, 6);
    assert.equal(m.fase, "fim", fase);
    assert.equal(m.resultado, "derrota", fase);
    // recomeçar é um mundo novo, do começo
    const n = criarMundo({ heroi: "guerreiro", encontro: "guerra9", sorteio: 6 });
    assert.ok(n.t === 0 && !n.resultado && !n.heroi.morto && estado9(n).fase === "ondas");
  }
  // a vitória e, depois, você cai: continua vitória
  const m = criarMundo({ heroi: "guerreiro", encontro: "guerra9", sorteio: 6 });
  ateGeneral(m);
  ferir(m, m.g9.general.u, 99999, m.heroi, {});
  ferir(m, m.heroi, 99999, null, {});
  rodar(m, 6);
  assert.equal(m.resultado, "vitoria");
  assert.equal(m.registro.filter((x) => x.texto === "Vitória.").length, 1);
});
