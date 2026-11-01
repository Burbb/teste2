// Batalhas sem tela, com o jogador automático: duração, resultado, vida, abates do herói e das tropas e o custo do
// passo. Uso: node ferramentas/simular.mjs [repetições] [normal|maior]
import { criarMundo, passo, entradaVazia, resumo } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";

const n = Number(process.argv[2] || 3), qtd = process.argv[3] || "normal";
function rodar(heroi, robo, semente) {
  const m = criarMundo({ heroi, quantidade: qtd, semente });
  const ent = entradaVazia(), r = criarRobo(robo);
  const t0 = performance.now();
  let passos = 0;
  while (m.fase !== "fim" && m.t < 240) { pensar(r, m, ent); passo(m, ent); m.eventos.length = 0; passos++; }
  const ms = (performance.now() - t0) / passos;
  return { ...resumo(m), msPasso: ms };
}
for (const [heroi, robo, rotulo] of [["guerreiro", {}, "guerreiro"], ["guerreiro", { nivel: "medio" }, "guerreiro m"],
  ["mago", {}, "mago"], ["mago", { nivel: "medio" }, "mago m"], ["guerreiro", { passivo: true }, "só as tropas"]]) {
  for (let i = 0; i < n; i++) {
    const s = rodar(heroi, robo, 20261031 + i);
    const usos = Object.entries(s.usos).map(([k, v]) => `${k} ${v.usos}/${v.acertos}/${v.abates}`).join(" ");
    console.log(`${rotulo.padEnd(13)} #${i} ${String(s.resultado).padEnd(8)} ${s.t.toFixed(1).padStart(6)} s  vida ${s.vida.toFixed(0).padStart(3)}` +
      `  herói ${String(s.abatesHeroi).padStart(3)}  tropas ${String(s.abatesAliados).padStart(3)}  perdas ${String(s.perdas).padStart(3)}/${s.aliados}` +
      `  sofreu ${s.danoSofrido.toFixed(0).padStart(3)}  maior golpe ${s.maiorGolpe}  ${s.msPasso.toFixed(3)} ms/passo  [${usos}]`);
  }
}
