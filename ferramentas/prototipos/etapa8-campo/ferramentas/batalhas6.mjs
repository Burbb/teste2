// Campo Livre 6: os encontros novos sem tela, com o jogador automático: resultado, tempo, vida do herói, de Morel e de
// Odette, perdas, os heróis inimigos e o que cada peça nova fez (cargas, magias, flechas na parede, cura de Odette,
// passos de Ardis, provocações de Morel), e o custo do passo da simulação (média e o pior).
// Uso: node ferramentas/batalhas6.mjs [encontros separados por vírgula] [composições] [heróis] [escala]
import { criarMundo, passo, entradaVazia } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";

const [encArg = "vila,carga,herois", compArg = "comum,completa", heroiArg = "guerreiro,mago", escala = "1"] = process.argv.slice(2);
for (const enc of encArg.split(",")) for (const comp of compArg.split(",")) for (const heroi of heroiArg.split(",")) {
  const m = criarMundo({ heroi, encontro: enc, quantidade: escala, composicao: { aliados: comp, inimigos: comp } });
  const harg = m.lider;
  const r = criarRobo({ nivel: "forte" });
  let n = 0, pior = 0, maxU = 0;
  const t0 = performance.now();
  while (m.fase !== "fim" && m.t < 150) {
    const ent = entradaVazia();
    pensar(r, m, ent);
    const a = performance.now();
    passo(m, ent);
    pior = Math.max(pior, performance.now() - a);
    maxU = Math.max(maxU, m.unidades.length);
    n++;
  }
  const st = m.stats, v = (u) => (!u ? "-" : u.morto ? "caiu" : Math.round(u.vida));
  console.log(`${enc.padEnd(7)} ${comp.padEnd(9)} ${heroi.padEnd(9)} ${String(m.resultado || "sem fim").padEnd(8)} ${m.t.toFixed(0).padStart(3)} s` +
    `  herói ${Math.max(0, Math.round(m.heroi.vida))}  Morel ${v(m.morel)}  Odette ${v(m.odette)}  aliados ${m.lados[0].length - 1 - (m.morel && !m.morel.morto ? 1 : 0) - (m.odette && !m.odette.morto ? 1 : 0)}/${st.aliados - (m.morel ? 2 : 0)}` +
    `  Harg ${v(harg)}  Ardis ${v(m.ardis)}  cargas ${st.cargas || 0}  magias ${st.magias || 0}  flechas na parede ${st.flechasParede || 0}` +
    `  cura de Odette ${Math.round(st.odetteCura || 0)}  passos de Ardis ${st.ardisPassos || 0}  provocados ${st.morelProvoca || 0}` +
    `  máx ${maxU} no campo  ${((performance.now() - t0) / n).toFixed(2)} ms/passo (pior ${pior.toFixed(1)})`);
}
