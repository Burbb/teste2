// Batalhas sem tela, com o jogador automático, em todos os encontros: resultado, duração, vida, abates do herói e das
// tropas e o que as tropas fizeram além de matar (inimigos ocupados, dano que seguraram, flechas que receberam).
// Uso: node ferramentas/simular.mjs [repetições] [normal|maior] [forte|medio]
import { criarMundo, passo, entradaVazia, resumo } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";
import { ENCONTROS } from "../tela/conteudo.js";

const n = Number(process.argv[2] || 1), qtd = process.argv[3] || "normal", nivel = process.argv[4] || "forte";
const KITS = { guerreiro: [["original", {}], ["sangrenta+grito", { varredura: "sangrenta", investida: "grito" }]],
  mago: [["original", {}], ["incendiaria+anel", { bola: "incendiaria", muralha: "anel" }]] };

function rodar(heroi, encontro, kit, robo, semente) {
  const m = criarMundo({ heroi, quantidade: qtd, semente, encontro, kit });
  const ent = entradaVazia(), r = criarRobo(robo);
  const t0 = performance.now();
  let passos = 0;
  while (m.fase !== "fim" && m.t < 240) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; passos++; }
  return { ...resumo(m), msPasso: (performance.now() - t0) / passos };
}
const linha = (rot, s) => console.log(`${rot.padEnd(42)} ${String(s.resultado).padEnd(8)} ${s.t.toFixed(0).padStart(4)} s  vida ${s.vida.toFixed(0).padStart(3)}` +
  `  herói ${String(s.abatesHeroi).padStart(3)}  tropas ${String(s.abatesAliados).padStart(3)}  perdas ${String(s.perdas).padStart(3)}/${s.aliados}` +
  `  ocupados ${s.ocupados.toFixed(0).padStart(4)}  seguraram ${s.danoTropas.toFixed(0).padStart(4)}  flechas tropas/herói ${s.flechasTropas}/${s.flechasHeroi}` +
  `  ${s.msPasso.toFixed(3)} ms/passo`);
for (const enc of Object.keys(ENCONTROS)) {
  for (const heroi of ["guerreiro", "mago"]) for (const [nomeKit, kit] of KITS[heroi]) for (let i = 0; i < n; i++) {
    linha(`${enc} · ${heroi} · ${nomeKit}${n > 1 ? ` #${i}` : ""}`, rodar(heroi, enc, kit, { nivel }, 20261031 + i));
  }
  linha(`${enc} · só as tropas`, rodar("guerreiro", enc, {}, { passivo: true }, 20261031));
}
