// Lutas sem tela com a IA dos dois lados (o jogador automático controla os três aliados): resultado, rodadas, vida
// que sobrou, mortos de cada lado, o tempo da IA por vez e as vezes inimigas sem ação nem movimento.
// Uso: node ferramentas/simular.mjs [encontro|todos] [classe|todas]
import { criarLuta, atual, encerrarVez } from "../tela/regras.js";
import { jogarVez } from "../tela/ia.js";
import { BUILDS, ENCONTROS } from "../tela/conteudo.js";

const [encArg = "todos", clsArg = "todas"] = process.argv.slice(2);
const encs = encArg === "todos" ? Object.keys(ENCONTROS) : [encArg];
const clss = clsArg === "todas" ? Object.keys(BUILDS) : [clsArg];
for (const enc of encs) for (const classe of clss) for (const [nome, b] of Object.entries(BUILDS[classe])) {
  const m = criarLuta({ heroi: { classe, kit: b.kit, talentos: b.talentos }, encontro: enc });
  let maxMs = 0, soma = 0, vezes = 0, paradas = 0;
  while (!m.fim && m.rodada <= 30) {
    const u = atual(m), t0 = performance.now();
    const f = jogarVez(m);
    const ms = performance.now() - t0;
    maxMs = Math.max(maxMs, ms); soma += ms; vezes++;
    if (u.lado === 1 && !f.length && u.vivo) paradas++;
    if (!m.fim) encerrarVez(m);
  }
  const vivos = (l) => m.unidades.filter((u) => u.lado === l && u.vivo);
  const pv = vivos(0).map((u) => `${u.nome} ${u.pv}`).join(", ");
  console.log(`${enc.padEnd(9)} ${classe.padEnd(9)} ${nome.padEnd(10)} ${String(m.fim || "sem fim").padEnd(8)} rodadas ${String(m.rodada).padStart(2)}  aliados vivos ${vivos(0).length} (${pv})  inimigos vivos ${vivos(1).length}  IA ${(soma / vezes).toFixed(0)} ms/vez (pior ${maxMs.toFixed(0)})  vezes inimigas paradas ${paradas}`);
}
