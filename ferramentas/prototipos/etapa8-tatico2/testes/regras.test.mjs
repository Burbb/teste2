// Testes do Tático 2 (node --test): as regras e a IA, sem tela. Cada cenário parte de uma luta de verdade e troca o
// mapa e as posições para isolar a regra conferida.
import test from "node:test";
import assert from "node:assert/strict";
import { criarLuta, atual, alcancaveis, alvosValidos, podeLancar, lancar, mover, encerrarVez, iniciarVez, prever, visao,
  areaDe, unidade, custoSaida, temEstado, talentosValidos } from "../tela/regras.js";
import { jogarVez, melhorOpcao } from "../tela/ia.js";
import { BUILDS, ENCONTROS, CLASSES } from "../tela/conteudo.js";

const luta = (classe = "guerreiro", build, encontro = "aberto") => {
  const b = BUILDS[classe][build || Object.keys(BUILDS[classe])[0]];
  return criarLuta({ heroi: { classe, kit: b.kit, talentos: b.talentos }, encontro });
};

/** Troca o mapa e as posições: `pos` = { id: [x, y] }; quem não está em `pos` sai da luta. A vez fica com `vez`. */
function cenario(m, mapa, pos, vez) {
  m.h = mapa.length; m.w = mapa[0].length;
  m.celulas = mapa.join("").split("");
  m.chao = {}; m.armadilhas = []; m.preparos = [];
  for (const u of m.unidades) {
    if (pos[u.id]) { [u.x, u.y] = pos[u.id]; u.vivo = true; u.pv = u.pvMax; u.estados = []; u.cds = {}; }
    else { u.vivo = false; u.x = -9; u.y = -9; }
  }
  m.vez = m.ordem.indexOf(vez);
  iniciarVez(m);
  m.eventos = []; m.fim = null;
  return m;
}
const vazio = (w, h) => Array.from({ length: h }, () => ".".repeat(w));

test("a ordem: alterna aliado e inimigo pela iniciativa; Morel e Odette têm a própria vez", () => {
  const m = luta("mago");
  const lados = m.ordem.map((id) => unidade(m, id).lado);
  for (let i = 0; i < 6; i++) assert.notEqual(lados[i], lados[i + 1], "alterna nas seis primeiras");
  assert.ok(m.ordem.includes("morel") && m.ordem.includes("odette"));
  const ini = m.ordem.filter((id) => unidade(m, id).lado === 0).map((id) => unidade(m, id).ini);
  assert.deepEqual(ini, [...ini].sort((a, b) => b - a), "aliados pela iniciativa");
});

test("PA e PM: custos, recargas, vezes por turno e por alvo; tudo volta no começo da vez", () => {
  const m = cenario(luta("guerreiro", "Arremesso"), vazio(8, 8), { heroi: [2, 2], bandido1: [3, 2] }, "heroi");
  const u = unidade(m, "heroi");
  assert.equal(u.pa, 6); assert.equal(u.pm, 3);
  assert.ok(lancar(m, u, "golpe", 3, 2)); assert.equal(u.pa, 3);
  assert.ok(lancar(m, u, "golpe", 3, 2)); assert.equal(u.pa, 0);
  assert.equal(podeLancar(m, u, "golpe").ok, false, "sem PA");
  assert.match(podeLancar(m, u, "golpe").motivo, /PA|turno/);
  const m2 = cenario(luta("guerreiro", "Arremesso"), vazio(8, 8), { heroi: [2, 2], bandido1: [3, 2] }, "heroi");
  const h = unidade(m2, "heroi");
  assert.ok(lancar(m2, h, "empurrao", 3, 2));
  assert.equal(podeLancar(m2, h, "empurrao").ok, false, "recarga 1: uma vez por turno");
  encerrarVez(m2);
  while (atual(m2).id !== "heroi") encerrarVez(m2);
  assert.equal(h.pa, 6); assert.equal(podeLancar(m2, h, "empurrao").ok, true, "volta na vez seguinte");
  // a Prece: 1 por alvo a cada vez
  const m3 = cenario(luta(), vazio(8, 8), { odette: [1, 1], heroi: [2, 1], lobo1: [7, 7] }, "odette");
  const o = unidade(m3, "odette");
  unidade(m3, "heroi").pv = 20;
  assert.ok(lancar(m3, o, "prece", 2, 1));
  assert.ok(!alvosValidos(m3, o, "prece").some(([x, y]) => x === 2 && y === 1), "a mesma pessoa não recebe a segunda Prece");
  assert.ok(alvosValidos(m3, o, "prece").some(([x, y]) => x === 1 && y === 1), "Odette pode se curar");
});

test("caminhos: não atravessa ninguém nem obstáculos; o bloqueio cobra 1 PM por inimigo (2 se pesado)", () => {
  const m = cenario(luta(), ["......", ".#....", "......", "......"], { heroi: [0, 0], bandido1: [1, 0], brutamontes1: [9, 9] }, "heroi");
  const u = unidade(m, "heroi");
  assert.equal(custoSaida(m, u, 0, 0), 1);
  const r = alcancaveis(m, u);
  assert.equal(r.get("0,1").custo, 2, "sair do contato custa 1 + 1");
  assert.ok(!r.has("1,0"), "não entra na casa ocupada");
  assert.ok(!r.has("1,1"), "o pilar não é casa");
  assert.ok(!r.has("0,3"), "0,3 custaria 4: além dos 3 PM");
  // o pesado conta 2; a Muralha Viva também
  const m2 = cenario(luta(), vazio(6, 4), { heroi: [0, 0], morel: [5, 3] }, "heroi");
  const morel = unidade(m2, "morel");
  const b = m2.unidades.find((x) => x.id === "bandido1"); b.vivo = true; b.x = 1; b.y = 0;
  assert.equal(custoSaida(m2, b, 1, 0), 2, "o Guerreiro da Muralha tem Muralha Viva: conta 2");
  morel.x = 1; morel.y = 1;
  assert.equal(custoSaida(m2, b, 1, 0), 4, "o herói (2) e Morel, pesado (2)");
  // o lobo não sofre bloqueio
  const lobo = m2.unidades.find((x) => x.id === "lobo1"); lobo.vivo = true; lobo.x = 0; lobo.y = 1;
  assert.equal(custoSaida(m2, lobo, 0, 1), 0);
});

test("andar gasta os PM do caminho e o chão em chamas fere quem entra", () => {
  const m = cenario(luta(), vazio(6, 6), { heroi: [0, 0], lobo1: [5, 5] }, "heroi");
  const u = unidade(m, "heroi");
  m.chao["1,0"] = { e: "fogo", ate: 99, dono: "lobo1" };
  assert.ok(mover(m, u, 2, 0));
  assert.equal(u.pm, 1); assert.equal(u.x, 2);
  assert.equal(u.pv, u.pvMax - 5, "passou pelo fogo");
});

test("linha de visão: pilar e combatente no meio bloqueiam; água e rocha baixa não; canto permissivo", () => {
  const m = cenario(luta(), [".......", "...#...", ".......", "...~r..", "......."], { heroi: [0, 1], bandido1: [6, 1], lobo1: [3, 4], lobo2: [6, 4], atirador1: [0, 4] }, "heroi");
  assert.equal(visao(m, 0, 1, 6, 1), false, "o pilar no meio");
  assert.equal(visao(m, 0, 3, 6, 3), true, "água e rocha baixa deixam ver");
  assert.equal(visao(m, 0, 4, 6, 4), false, "o lobo 1 no meio tapa");
  assert.equal(visao(m, 2, 1, 3, 2), true, "passa pelo canto do pilar: só um lado bloqueia");
  assert.equal(visao(m, 2, 0, 4, 2), false, "a diagonal pelo centro do pilar");
  const u = unidade(m, "heroi");
  assert.ok(!alvosValidos(m, u, "investida").some(([x, y]) => x === 6 && y === 1), "sem visão, sem alvo");
});

test("áreas: cruz, círculo, raio (para no pilar) e atravessada", () => {
  const m = cenario(luta("mago", "Piromante"), vazio(9, 9), { heroi: [4, 4], lobo1: [8, 8] }, "heroi");
  const u = unidade(m, "heroi");
  const k = (a) => ({ ...u.kit.faisca, area: a, alvo: "casa" });
  assert.equal(areaDe(m, u, k({ f: "cruz", r: 1 }), 4, 1).length, 5);
  assert.equal(areaDe(m, u, k({ f: "circulo", r: 2 }), 4, 1).length, 13 - 1, "losango de raio 2 cortado na borda (y < 0)");
  m.celulas[4 * 9 + 7] = "#";
  assert.deepEqual(areaDe(m, u, k({ f: "raio", r: 5 }), 5, 4), [[5, 4], [6, 4]], "o raio para no pilar");
  assert.deepEqual(areaDe(m, u, k({ f: "perp", r: 1 }), 4, 2).sort(), [[3, 2], [4, 2], [5, 2]], "atravessada à mira");
});

test("empurrão: anda as casas livres; bater fere pelas casas que faltaram e quem foi atingido leva a metade", () => {
  const m = cenario(luta("guerreiro", "Arremesso", "passagem"), [".......", ".......", "......."], { heroi: [1, 1], bandido1: [2, 1], bandido2: [4, 1] }, "heroi");
  const u = unidade(m, "heroi"), a = unidade(m, "bandido1"), b = unidade(m, "bandido2");
  const p = prever(m, "heroi", "empurrao", 2, 1);
  lancar(m, u, "empurrao", 2, 1);
  assert.deepEqual([a.x, a.y], [3, 1], "andou 1 e bateu no bandido 2");
  // Golpe de Escudo: 5 + 2 casas que faltaram × 8 (Impacto dobra os 4)
  assert.equal(a.pv, a.pvMax - 5 - 16);
  assert.equal(b.pv, b.pvMax - 8, "a metade da colisão");
  assert.equal(p.mud.find((d) => d.id === "bandido1").dPv, -21, "a prévia disse o mesmo");
  assert.deepEqual(p.mud.find((d) => d.id === "bandido1").para, [3, 1]);
});

test("puxar e avançar: a Corrente traz até vizinho; a Investida para na casa vizinha e não sofre bloqueio", () => {
  const m = cenario(luta("guerreiro", "Arremesso"), vazio(9, 3), { heroi: [1, 1], bandido1: [6, 1], lobo1: [0, 1] }, "heroi");
  const u = unidade(m, "heroi"), b = unidade(m, "bandido1");
  lancar(m, u, "corrente", 6, 1);
  assert.deepEqual([b.x, b.y], [2, 1]);
  const m2 = cenario(luta("guerreiro", "Arremesso"), vazio(9, 3), { heroi: [1, 1], bandido1: [5, 1], lobo1: [0, 1] }, "heroi");
  const h = unidade(m2, "heroi");
  assert.ok(lancar(m2, h, "investida", 5, 1));
  assert.deepEqual([h.x, h.y], [4, 1]);
  assert.equal(h.pm, 3, "a Investida não gasta PM nem cobra o bloqueio do lobo");
  // Embalo: o próximo Golpe de Espada nesta vez causa +6
  const pv = unidade(m2, "bandido1").pv;
  lancar(m2, h, "golpe", 5, 1);
  assert.equal(unidade(m2, "bandido1").pv, pv - 18);
});

test("estados: a duração conta nas vezes de quem carrega; Lento tira PM; Escudo Erguido vai até a próxima vez sua", () => {
  const m = cenario(luta("guerreiro", "Muralha"), vazio(8, 3), { heroi: [1, 1], bandido1: [2, 1] }, "heroi");
  const u = unidade(m, "heroi"), b = unidade(m, "bandido1");
  lancar(m, u, "atordoar", 2, 1);
  lancar(m, u, "escudo", 1, 1);
  assert.ok(temEstado(b, "desequilibrado") && temEstado(u, "protegido"));
  encerrarVez(m);
  while (atual(m).id !== "bandido1") encerrarVez(m);
  assert.equal(b.pm, b.pmMax - 2, "Desequilibrado: perde 2 PM");
  const pv = u.pv;
  lancar(m, b, "faca", 1, 1);
  assert.equal(u.pv, pv - 4, "Escudo Erguido: metade de 7, arredondada");
  encerrarVez(m);
  assert.ok(!temEstado(b, "desequilibrado"), "acabou no fim da vez dele");
  while (atual(m).id !== "heroi") encerrarVez(m);
  assert.ok(!temEstado(u, "protegido"), "acabou no começo da vez seguinte do herói");
});

test("Morel cobre e Odette abençoa: o dano se divide e a bênção absorve", () => {
  // a ordem: Mago, Bandido, Odette, ..., Morel: Odette abençoa, Morel cobre, e o bandido ataca na rodada seguinte
  const m = cenario(luta("mago"), vazio(8, 3), { morel: [1, 1], heroi: [2, 1], odette: [2, 0], bandido1: [3, 1] }, "odette");
  const morel = unidade(m, "morel"), h = unidade(m, "heroi"), b = unidade(m, "bandido1");
  assert.ok(lancar(m, unidade(m, "odette"), "bencao", 2, 1));
  while (atual(m).id !== "morel") encerrarVez(m);
  assert.ok(lancar(m, morel, "cobrir", 2, 1));
  while (atual(m).id !== "bandido1") encerrarVez(m);
  lancar(m, b, "faca", 2, 1);
  // 7 de dano: 4 vão para Morel (metade arredondada para cima), 3 sobram e a Bênção (8) absorve
  assert.equal(morel.pv, morel.pvMax - 4);
  assert.equal(h.pv, h.pvMax);
  assert.equal(temEstado(h, "abencoado").v, 5);
});

test("talentos: só os que têm a habilidade pedida, no máximo 2; e mudam a regra", () => {
  assert.deepEqual(talentosValidos("mago", ["faisca"], ["labareda", "seletivas", "estilhacar"]), ["seletivas", "estilhacar"]);
  const m = cenario(luta("mago", "Piromante"), vazio(9, 5), { heroi: [1, 2], morel: [5, 2], bandido1: [5, 1], lobo1: [8, 4] }, "heroi");
  const u = unidade(m, "heroi");
  assert.equal(u.kit.bola.efeitos[1].turnos, 3, "Labareda: 2 + 1 rodada");
  lancar(m, u, "bola", 5, 2);
  assert.equal(unidade(m, "morel").pv, unidade(m, "morel").pvMax, "Chamas Seletivas: Morel no centro da Bola não leva");
  assert.equal(unidade(m, "bandido1").pv, unidade(m, "bandido1").pvMax - 9);
  // Estilhaçar: o fogo consome o gelo com +8
  const m2 = cenario(luta("mago", "Criomante"), vazio(9, 3), { heroi: [1, 1], bandido1: [4, 1] }, "heroi");
  const h = unidade(m2, "heroi"), b = unidade(m2, "bandido1");
  lancar(m2, h, "congelar", 4, 1);
  lancar(m2, h, "faisca", 4, 1);
  assert.equal(b.pv, b.pvMax - 4 - 6 - 8);
  assert.ok(!temEstado(b, "congelado"));
});

test("chão e barris: o fogo direto explode o barril, que fere em cruz e acende o chão", () => {
  const m = cenario(luta("mago", "Piromante"), [".......", "...o...", "......."], { heroi: [0, 1], bandido1: [3, 0], lobo1: [4, 1] }, "heroi");
  const u = unidade(m, "heroi");
  lancar(m, u, "bola", 2, 1);
  assert.equal(m.celulas[1 * 7 + 3], ".", "o barril sumiu");
  assert.ok(m.chao["3,0"] && m.chao["4,1"], "o chão em volta pega fogo");
  assert.equal(unidade(m, "lobo1").pv, unidade(m, "lobo1").pvMax - 8);
});

test("armadilha: o inimigo não a vê, para nela, leva o dano e fica Imobilizado", () => {
  const m = cenario(luta("arqueiro", "Caçador"), vazio(9, 3), { heroi: [0, 1], bandido1: [6, 1] }, "heroi");
  const u = unidade(m, "heroi");
  assert.ok(lancar(m, u, "armadilha", 3, 1));
  encerrarVez(m);
  while (atual(m).id !== "bandido1") encerrarVez(m);
  const b = unidade(m, "bandido1");
  mover(m, b, 2, 1);
  assert.deepEqual([b.x, b.y], [3, 1], "parou na armadilha");
  assert.equal(b.pv, b.pvMax - 8);
  assert.ok(temEstado(b, "imobilizado"));
});

test("golpe preparado: marca as casas e cai no começo da vez seguinte de quem preparou; quem sai escapa", () => {
  const m = cenario(luta("guerreiro", undefined, "passagem"), vazio(8, 5), { brutamontes1: [3, 2], heroi: [4, 2], morel: [4, 3] }, "brutamontes1");
  const br = unidade(m, "brutamontes1");
  assert.ok(lancar(m, br, "esmagar", 4, 2));
  assert.equal(m.preparos.length, 1);
  encerrarVez(m);
  while (atual(m).id !== "heroi") encerrarVez(m);
  // sair do lado do Brutamontes (pesado) custa 1 + 2 PM: com 3, o herói só chega a 5,2, fora das casas marcadas
  assert.ok(!alcancaveis(m, unidade(m, "heroi")).has("6,2"));
  assert.ok(mover(m, unidade(m, "heroi"), 5, 2));
  while (atual(m).id !== "brutamontes1") encerrarVez(m);
  assert.equal(unidade(m, "heroi").pv, unidade(m, "heroi").pvMax, "saiu: escapou");
  assert.equal(unidade(m, "morel").pv, unidade(m, "morel").pvMax - 16, "ficou: levou");
});

test("a prévia é o efeito: em todas as habilidades das montagens, em alvos reais", () => {
  for (const classe of Object.keys(CLASSES)) for (const build of Object.keys(BUILDS[classe])) {
    const m = cenario(luta(classe, build), vazio(10, 10), { heroi: [2, 5], bandido1: [4, 5], lobo1: [5, 6], atirador1: [6, 5], morel: [2, 6], odette: [1, 5] }, "heroi");
    for (const id of Object.keys(unidade(m, "heroi").kit)) {
      const u = unidade(m, "heroi"), alvos = alvosValidos(m, u, id);
      for (const [x, y] of alvos.slice(0, 6)) {
        const p = prever(m, "heroi", id, x, y), c = structuredClone(m);
        lancar(c, unidade(c, "heroi"), id, x, y);
        for (const d of p.mud) {
          const real = unidade(c, d.id);
          assert.equal(real.pv - unidade(m, d.id).pv, d.dPv, `${classe} ${id} em ${x},${y}: vida de ${d.id}`);
          assert.deepEqual([real.x, real.y], d.para, `${classe} ${id}: posição de ${d.id}`);
        }
      }
    }
  }
});

test("IA: ninguém fica parado sem motivo; quem atira se afasta do corpo a corpo; a cura não é desperdiçada", () => {
  // o atirador encostado num guerreiro: atira e se afasta, ou se afasta para atirar
  const m = cenario(luta(), vazio(10, 10), { atirador1: [5, 5], heroi: [5, 6], morel: [9, 9] }, "atirador1");
  const a = unidade(m, "atirador1");
  jogarVez(m);
  assert.ok(Math.abs(a.x - 5) + Math.abs(a.y - 6) >= 2, "saiu do contato");
  // a xamã com todos de vida cheia não cura
  const m2 = cenario(luta("guerreiro", undefined, "misto"), vazio(10, 10), { xama1: [2, 2], bandido1: [3, 2], heroi: [8, 8] }, "xama1");
  const op = melhorOpcao(m2, unidade(m2, "xama1"));
  assert.ok(!op || op.hab !== "cura", "não cura quem está cheio");
  unidade(m2, "bandido1").pv = 12;
  assert.equal(melhorOpcao(m2, unidade(m2, "xama1")).hab, "cura", "cura o ferido");
  // o corpo a corpo atrás de um muro com uma passagem: anda pelo caminho, não fica parado
  const m3 = cenario(luta(), ["..........", "..........", "####.#####", "..........", ".........."], { bandido1: [1, 0], heroi: [1, 4] }, "bandido1");
  const b = unidade(m3, "bandido1"), antes = Math.abs(b.x - 4) + Math.abs(b.y - 2);
  jogarVez(m3);
  assert.ok(Math.abs(b.x - 4) + Math.abs(b.y - 2) < antes, "foi em direção à passagem");
});

test("IA: provocado, só ataca quem provocou", () => {
  const m = cenario(luta("guerreiro", "Muralha"), vazio(8, 4), { heroi: [2, 1], odette: [4, 2], bandido1: [3, 1] }, "heroi");
  unidade(m, "odette").pv = 10;
  lancar(m, unidade(m, "heroi"), "provocar", 2, 1);
  while (atual(m).id !== "bandido1") encerrarVez(m);
  const op = melhorOpcao(m, unidade(m, "bandido1"));
  assert.ok(op, "tem o que fazer");
  const p = prever(m, "bandido1", op.hab, ...op.alvo, op.casa);
  assert.ok(p.mud.some((d) => d.id === "heroi" && d.dPv < 0), "atacou o herói, não a Odette ferida");
});

test("os três encontros terminam com o jogador automático, sem travar", () => {
  for (const enc of Object.keys(ENCONTROS)) {
    const m = luta("arqueiro", "Atirador", enc);
    let vezes = 0;
    while (!m.fim && m.rodada <= 30) { jogarVez(m); if (!m.fim) encerrarVez(m); vezes++; }
    assert.ok(m.fim, `${enc} termina (${m.rodada} rodadas)`);
    assert.ok(vezes > 8);
  }
});
