// Diagnóstico da navegação (Campo Livre 7): quanto tempo cada um passa encostado numa construção querendo andar e sem
// sair do lugar (o "esbarrar na muralha"), por tipo, e os episódios mais longos de Morel e Odette.
// Uso: node ferramentas/navegacao-diag.mjs [encontros] [heróis] [escala]
import { criarMundo, passo, entradaVazia } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";
import { dentroObstaculo } from "../tela/campo6.js";

const [encArg = "vila,herois", heroiArg = "guerreiro,mago", escala = "1"] = process.argv.slice(2);
const DT = 1 / 60;
for (const enc of encArg.split(",")) for (const heroi of heroiArg.split(",")) {
  const m = criarMundo({ heroi, encontro: enc, quantidade: escala, composicao: { aliados: "completa", inimigos: "completa" } });
  const r = criarRobo({ nivel: "forte" });
  const preso = {}, ep = new Map(), episodios = [];
  while (m.fase !== "fim" && m.t < 120) {
    const ent = entradaVazia();
    pensar(r, m, ent);
    passo(m, ent);
    for (const u of m.unidades) {
      if (u.morto || u === m.heroi) continue;
      const quer = Math.hypot(u.vx, u.vy), andou = Math.hypot(u.x - u.px, u.y - u.py) / DT;
      const parede = dentroObstaculo(m, u.x, u.y, u.raio + 1.5);
      const travado = quer > 8 && andou < quer * 0.25 && parede;
      if (travado) {
        preso[u.tipo] = (preso[u.tipo] || 0) + DT;
        const e = ep.get(u.id) || { tipo: u.tipo, ini: m.t, x: u.x, y: u.y, alvo: u.alvo ? u.alvo.tipo : "-" };
        e.fim = m.t; ep.set(u.id, e);
      } else if (ep.has(u.id)) { const e = ep.get(u.id); if (e.fim - e.ini > 1) episodios.push(e); ep.delete(u.id); }
    }
  }
  for (const e of ep.values()) if (e.fim - e.ini > 1) episodios.push(e);
  const comp = episodios.filter((e) => e.tipo === "morel" || e.tipo === "odette").sort((a, b) => (b.fim - b.ini) - (a.fim - a.ini));
  console.log(`${enc} ${heroi} ${m.resultado || "sem fim"} ${m.t.toFixed(0)} s | travado contra parede (s): ` +
    Object.entries(preso).map(([k, v]) => `${k} ${v.toFixed(1)}`).join(", ") +
    ` | episódios > 1 s: ${episodios.length} (Morel/Odette ${comp.length})`);
  for (const e of comp.slice(0, 5)) console.log(`   ${e.tipo} ${e.ini.toFixed(1)}–${e.fim.toFixed(1)} s em (${e.x.toFixed(0)}, ${e.y.toFixed(0)}) alvo ${e.alvo}`);
}
