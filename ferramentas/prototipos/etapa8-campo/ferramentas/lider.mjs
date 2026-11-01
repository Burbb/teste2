// O comportamento do Capitão numa batalha sem tela, com o jogador automático: onde ele gasta o tempo (andando,
// parado, preparando, no ar, atordoado, cravado), quanto tempo fica a menos de 40 px do herói, quantas vezes muda de
// escolha (herói ou tropas), quantas habilidades usa e quantas pegam o herói, quanto dano causa e quantas tropas perdemos.
// Uso: node ferramentas/lider.mjs [guerreiro|mago|ambos] [escala] [forte|medio] [encontro]
import { criarMundo, passo, entradaVazia, PASSO } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";

const quem = process.argv[2] || "ambos", escala = process.argv[3] || "1", nivel = process.argv[4] || "forte";
const encontro = process.argv[5] || "capitao";

function estado(L) {
  if (L.voando) return "no ar";
  if (L.acao) return L.acao.tipo || "machado";
  if (L.atordoado > 0) return "atordoado";
  if (L.ofegante > 0) return "cravado/ofegante";
  if (L.congelado > 0) return "estremece";
  return Math.hypot(L.vx, L.vy) > 1 ? "andando" : "parado";
}

function medir(heroi, semente) {
  const m = criarMundo({ heroi, encontro, semente, quantidade: escala });
  const ent = entradaVazia(), r = criarRobo({ nivel });
  const L = m.lider, d = {
    vivo: 0, perto: 0, trocas: 0, machados: 0, machadosHeroi: 0, rodopios: 0, rodopiosHeroi: 0, cargas: 0,
    cargasHeroi: 0, saltos: 0, saltosHeroi: 0, interrompido: 0, resistiu: 0, estados: {},
  };
  let modo = null;
  while (m.fase !== "fim" && m.t < 180) {
    pensar(r, m, ent);
    passo(m, ent);
    for (const e of m.eventos) {
      if (e.tipo === "golpeCampeao" && e.lider) { d.machados++; if (e.heroi) d.machadosHeroi++; }
      if (e.tipo === "liderRodopio") { d.rodopios++; if (e.heroi) d.rodopiosHeroi++; }
      if (e.tipo === "carga") d.cargas++;
      if (e.tipo === "fimCarga" && e.heroi) d.cargasHeroi++;
      if (e.tipo === "liderSalto") d.saltos++;
      if (e.tipo === "liderPouso" && e.heroi) d.saltosHeroi++;
      if (e.tipo === "interrompe" && !L.morto && Math.hypot(e.x - L.x, e.y - L.y) < 1) d.interrompido++;
      if (e.tipo === "resiste" && !L.morto && Math.hypot(e.x - L.x, e.y - L.y) < 1) d.resistiu++;
    }
    m.eventos.length = 0;
    if (L.morto) continue;
    d.vivo += PASSO;
    if (Math.hypot(L.x - m.heroi.x, L.y - m.heroi.y) < 40) d.perto += PASSO;
    if (L.modo !== modo) { if (modo) d.trocas++; modo = L.modo; }
    const e = estado(L);
    d.estados[e] = (d.estados[e] || 0) + PASSO;
  }
  return { ...d, danoHeroi: m.stats.liderHeroi, danoTropas: m.stats.liderTropas, t: m.t, resultado: m.resultado,
    vidaHeroi: Math.max(0, m.heroi.vida), perdas: m.stats.perdas, aliados: m.stats.aliados };
}

const f = (v, c = 0) => v.toFixed(c);
for (const heroi of quem === "ambos" ? ["guerreiro", "mago"] : [quem]) for (const s of [20261031, 20261032, 20261033]) {
  const d = medir(heroi, s);
  const est = Object.entries(d.estados).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${f(v)}`).join(", ");
  console.log(`${heroi.padEnd(9)} ${s}: ${d.resultado} ${f(d.t)} s (vida do herói ${f(d.vidaHeroi)}) · Capitão vivo ${f(d.vivo)} s` +
    ` · a <40 px ${f(d.perto, 1)} s · trocas de escolha ${d.trocas} · machado ${d.machados} (${d.machadosHeroi} no herói)` +
    ` · rodopio ${d.rodopios} (${d.rodopiosHeroi}) · arremetida ${d.saltos} (${d.saltosHeroi}) · carga ${d.cargas} (${d.cargasHeroi})` +
    ` · interrompido ${d.interrompido}, resistiu ${d.resistiu} · dano no herói ${f(d.danoHeroi)}, nas tropas ${f(d.danoTropas)}` +
    ` · perdas ${d.perdas}/${d.aliados}\n    tempo: ${est}`);
}
