// O comportamento do Capitão numa batalha sem tela, com o jogador automático: quanto tempo ele mira o herói, a
// distância média, quantas vezes troca de alvo, quantas habilidades usa e quantas pegam o herói, quanto tempo fica
// travado (querendo andar sem sair do lugar) e quanto dano causa no herói e nas tropas.
// Uso: node ferramentas/lider.mjs [guerreiro|mago|ambos] [escala] [forte|medio]
import { criarMundo, passo, entradaVazia, PASSO } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";

const quem = process.argv[2] || "ambos", escala = process.argv[3] || "1", nivel = process.argv[4] || "forte";

function medir(heroi, semente) {
  const m = criarMundo({ heroi, encontro: "capitao", semente, quantidade: escala });
  const ent = entradaVazia(), r = criarRobo({ nivel });
  const L = m.lider, d = {
    vivo: 0, noHeroi: 0, distSoma: 0, trocas: 0, travado: 0, perto: 0, machados: 0, machadosHeroi: 0, cargas: 0,
    cargasHeroi: 0, saltos: 0, saltosHeroi: 0, primeiroContato: null, caiuEm: null,
  };
  let alvo = null;
  while (m.fase !== "fim" && m.t < 180) {
    pensar(r, m, ent);
    const x0 = L.x, y0 = L.y;
    passo(m, ent);
    for (const e of m.eventos) {
      if (e.tipo === "golpeCampeao" && e.lider !== false && Math.hypot(e.x - L.x, e.y - L.y) < 1) { d.machados++; if (e.heroi) d.machadosHeroi++; }
      if (e.tipo === "carga" && e.lider !== false) d.cargas++;
      if (e.tipo === "fimCarga" && e.heroi) d.cargasHeroi++;
      if (e.tipo === "liderSalto") d.saltos++;
      if (e.tipo === "liderPouso" && e.heroi) d.saltosHeroi++;
      if (e.tipo === "liderGrito") d.gritos++;
    }
    m.eventos.length = 0;
    if (!L.morto) {
      d.vivo += PASSO;
      const dh = Math.hypot(L.x - m.heroi.x, L.y - m.heroi.y);
      d.distSoma += dh * PASSO;
      if (dh < 40) { d.perto += PASSO; if (d.primeiroContato === null) d.primeiroContato = m.t; }
      if (L.alvo === m.heroi) d.noHeroi += PASSO;
      if (L.alvo !== alvo) { if (alvo && L.alvo) d.trocas++; alvo = L.alvo; }
      const quer = Math.hypot(L.vx, L.vy), andou = Math.hypot(L.x - x0, L.y - y0) / PASSO;
      if (quer > 10 && andou < quer * 0.35) d.travado += PASSO;
    } else if (d.caiuEm === null) d.caiuEm = m.t;


  }
  return { heroi, ...d, danoHeroi: m.stats.liderHeroi, danoTropas: m.stats.liderTropas, t: m.t, resultado: m.resultado };
}

const f = (v, c = 0) => (v === null ? "—" : v.toFixed(c));
for (const heroi of quem === "ambos" ? ["guerreiro", "mago"] : [quem]) for (const s of [20261031, 20261032, 20261033]) {
  const d = medir(heroi, s);
  console.log(`${heroi.padEnd(9)} semente ${s}: ${d.resultado} ${f(d.t)} s · vivo ${f(d.vivo)} s (caiu ${f(d.caiuEm)}) · mira o herói ${f(100 * d.noHeroi / d.vivo)}%` +
    ` · distância média ${f(d.distSoma / d.vivo)} px · a menos de 40 px ${f(d.perto, 1)} s (primeira vez ${f(d.primeiroContato, 1)} s)` +
    ` · trocas de alvo ${d.trocas} (${f(d.trocas / d.vivo * 60)}/min) · travado ${f(d.travado, 1)} s` +
    ` · machado ${d.machados} (${d.machadosHeroi} no herói) · carga ${d.cargas} (${d.cargasHeroi} no herói) · arremetida ${d.saltos} (${d.saltosHeroi} no herói)` +
    ` · dano dele em você ${f(d.danoHeroi)}, nas tropas ${f(d.danoTropas)}`);
}
