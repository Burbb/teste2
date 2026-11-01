// Campo Livre 7, sem tela, com o jogador automático: em quem os heróis inimigos estiveram (fatia do tempo em você, em
// Morel, em Odette e nas tropas), quantas trocas e o menor intervalo entre duas, e o que os controles fizeram com o
// herói (o tempo total sob controle, o trecho mais longo, as vezes em que a proteção barrou). Também a Investida, o Brado,
// o Desafio de Morel e o Grilhão de Ardis.
// Uso: node ferramentas/alvos7.mjs [encontros] [composições] [heróis] [nível do robô]
import { criarMundo, passo, entradaVazia } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";

const [encArg = "herois", compArg = "comum,completa", heroiArg = "guerreiro,mago", nivel = "forte"] = process.argv.slice(2);
const DT = 1 / 60;
for (const enc of encArg.split(",")) for (const comp of compArg.split(",")) for (const heroi of heroiArg.split(",")) {
  const m = criarMundo({ heroi, encontro: enc, composicao: { aliados: comp, inimigos: comp } });
  const r = criarRobo({ nivel });
  const fatia = { lider: {}, ardis: {} }, trocas = { lider: [], ardis: [] }, ult = {};
  let preso = 0, trecho = 0, maior = 0, firme = 0, provocado = 0, ev = { investidaSai: 0, brado: 0, desafio: 0, grilhaoAcerta: 0, controle: 0 };
  while (m.fase !== "fim" && m.t < 150) {
    const ent = entradaVazia();
    pensar(r, m, ent);
    passo(m, ent);
    for (const e of m.eventos) {
      if (ev[e.tipo] !== undefined) ev[e.tipo]++;
      if (e.tipo === "firme" && e.heroi) firme++;
    }
    m.eventos.length = 0;
    for (const [k, u] of [["lider", m.lider], ["ardis", m.ardis]]) {
      if (!u || u.morto || !u.modo) continue;
      fatia[k][u.modo] = (fatia[k][u.modo] || 0) + DT;
      const chave = u.modo + (u.focoU ? u.focoU.id : "");
      if (ult[k] !== undefined && ult[k].c !== chave) trocas[k].push(m.t - ult[k].t);
      if (!ult[k] || ult[k].c !== chave) ult[k] = { c: chave, t: m.t };
    }
    const h = m.heroi;
    const ctl = !h.morto && (h.atordoado > 0 || h.imobAte > m.t);
    if (ctl) { preso += DT; trecho += DT; maior = Math.max(maior, trecho); } else trecho = 0;
    if (h.provocacao && h.provocacao.ate > m.t) provocado += DT;
  }
  const f = (o) => { const tot = Object.values(o).reduce((a, b) => a + b, 0) || 1; return Object.entries(o).map(([k, v]) => `${k} ${Math.round((100 * v) / tot)}%`).join(" "); };
  const tr = (l) => l.length ? `${l.length} trocas (menor ${Math.min(...l).toFixed(1)} s)` : "0 trocas";
  console.log(`${enc} ${comp} ${heroi}: ${m.resultado} ${m.t.toFixed(0)} s | Harg: ${f(fatia.lider)} · ${tr(trocas.lider)} | Ardis: ${f(fatia.ardis)} · ${tr(trocas.ardis)}`);
  console.log(`   herói sob controle ${preso.toFixed(1)} s (${((100 * preso) / m.t).toFixed(1)}%), trecho mais longo ${maior.toFixed(2)} s, firme ${firme}×, provocado ${provocado.toFixed(1)} s | ` +
    `investidas ${ev.investidaSai}, brados ${ev.brado}, desafios ${ev.desafio}, grilhões que acertaram ${ev.grilhaoAcerta}, controles ${ev.controle}`);
}
