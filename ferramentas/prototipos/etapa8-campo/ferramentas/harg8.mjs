// Campo Livre 8: o confronto com Harg sem tela, com o jogador automático (o forte sai para o lado dos avisos; o médio
// recua em linha reta; os dois batem nas aberturas). Por batalha: o resultado, o tempo, a vida do herói, quantos golpes
// de Harg acertaram o herói (por golpe), as quebras de postura, a parte do dano em Harg feita na abertura ou na quebra,
// quantos dos nossos ele derrubou, o tempo do herói sob controle e a fatia do tempo de Harg em cada alvo.
// Uso: node ferramentas/harg8.mjs [encontros] [heróis] [níveis]
import { criarMundo, passo, entradaVazia } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";

const [encArg = "duelo,guerra", heroiArg = "guerreiro,mago", nivelArg = "forte,medio"] = process.argv.slice(2);
for (const enc of encArg.split(",")) for (const heroi of heroiArg.split(",")) for (const nivel of nivelArg.split(",")) {
  const m = criarMundo({ heroi, encontro: enc });
  const r = criarRobo({ nivel });
  const noHeroi = {}, foco = {};
  let danoAberto = 0, danoTotal = 0, preso = 0, vidaAntes = null, l = null;
  while (m.fase !== "fim" && m.t < 180) {
    const e = entradaVazia();
    pensar(r, m, e);
    l = m.unidades.find((u) => u.tipo === "lider" && !u.morto) || l;
    vidaAntes = l && !l.morto ? l.vida : null;
    passo(m, e);
    if (l && vidaAntes !== null) {
      const d = Math.max(0, vidaAntes - Math.max(0, l.vida));
      danoTotal += d;
      if (l.h8 && (l.h8.quebrado > 0 || m.t < (l.h8.abertoAte || 0))) danoAberto += d;
      if (!l.morto && l.modo) foco[l.modo] = (foco[l.modo] || 0) + 1 / 60;
    }
    for (const ev of m.eventos) if (ev.tipo === "hargContato" && ev.heroi) noHeroi[ev.golpe] = (noHeroi[ev.golpe] || 0) + 1;
    m.eventos.length = 0;
    if (!m.heroi.morto && (m.heroi.atordoado > 0 || m.heroi.imobAte > m.t)) preso += 1 / 60;
  }
  const tot = Object.values(foco).reduce((a, b) => a + b, 0) || 1;
  console.log(`${enc} ${heroi} ${nivel}: ${m.resultado || "sem fim"} ${m.t.toFixed(0)} s, herói ${Math.max(0, Math.round(m.heroi.vida))}/${m.heroi.vidaMax}` +
    ` | Harg acertou o herói: ${JSON.stringify(noHeroi)} | quebras ${m.stats.hargQuebras || 0}, dano em Harg na abertura ou quebra ${Math.round((100 * danoAberto) / (danoTotal || 1))}%` +
    ` | Harg derrubou ${m.stats.hargMortos || 0} | herói sob controle ${preso.toFixed(1)} s | foco ${Object.entries(foco).map(([k, v]) => `${k} ${Math.round((100 * v) / tot)}%`).join(" ")}`);
}
