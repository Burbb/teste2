// O custo das cadeias (Estilhaçar, Brasa, Explosão de Sangue) numa horda grande: a horda 4× com o jogador automático
// forte, em cada montagem pronta e na mesma montagem sem talentos. O tempo de cada passo da simulação (média, p99 e o
// pior), as explosões (total e o maior número num golpe), os congelados e estilhaçados e o máximo de combatentes.
// O limite das cadeias é de regra (CADEIA.maxPorGolpe, as profundidades), nunca de desempenho: nada aqui reduz dano nem
// alvos. Uso: node ferramentas/cadeias.mjs [segundos] [escala]
import { criarMundo, passo, entradaVazia } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";
import { MONTAGENS } from "../tela/conteudo.js";

const segundos = Number(process.argv[2] || 100), escala = process.argv[3] || "4";

function rodar(heroi, kit) {
  const m = criarMundo({ heroi, encontro: "horda", quantidade: escala, kit }), ent = entradaVazia(), r = criarRobo({ nivel: "forte" });
  const tempos = [];
  let maior = 0, maxVivos = 0;
  while (m.fase !== "fim" && m.t < segundos) {
    pensar(r, m, ent);
    const t0 = performance.now();
    passo(m, ent);
    tempos.push(performance.now() - t0);
    for (const n of m.cadeias.values()) maior = Math.max(maior, n);
    if (tempos.length % 30 === 0) maxVivos = Math.max(maxVivos, m.unidades.filter((u) => !u.morto && !u.saiu).length);
    m.eventos.length = 0;
  }
  tempos.sort((a, b) => a - b);
  const media = tempos.reduce((s, v) => s + v, 0) / tempos.length;
  return { m, media, p99: tempos[Math.floor(tempos.length * 0.99)], pior: tempos[tempos.length - 1], maior, maxVivos };
}

console.log(`horda ${escala}×, ${segundos} s, jogador automático forte`);
for (const heroi of ["guerreiro", "mago"]) for (const [nome, mt] of Object.entries(MONTAGENS[heroi])) {
  for (const [rot, kit] of [[nome, mt], [`${nome} sem talentos`, { ...mt, talentos: [] }]]) {
    const r = rodar(heroi, kit), s = r.m.stats;
    console.log(`${heroi.padEnd(10)} ${rot.padEnd(32)} ${String(r.m.resultado || "em curso").padEnd(9)} ${r.m.t.toFixed(0).padStart(3)} s` +
      `  passo ${r.media.toFixed(2)} ms (p99 ${r.p99.toFixed(2)}, pior ${r.pior.toFixed(1)})  combatentes ${String(r.maxVivos).padStart(4)}` +
      `  abates herói ${String(s.abatesHeroi).padStart(4)}  explosões ${String(s.explosoes).padStart(4)} (maior golpe ${r.maior})` +
      `  congelados ${s.congelados}  estilhaçados ${s.estilhacados}`);
  }
}
