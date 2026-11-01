// O recurso (Fúria, Mana) em duas sequências de uso, com a montagem padrão de cada herói, num campo de laboratório
// cheio de inimigos parados (vida alta, para não acabarem):
// - normal: o principal segurado e cada comum assim que volta da recarga, uma por vez, a cada 0,4 s no máximo;
// - concentrada: as três comuns juntas (uma atrás da outra, sem esperar) assim que todas voltam, e a ultimate.
// Mede o menor recurso, quanto tempo ele ficou abaixo do custo da comum mais cara e quantas vezes uma comum pronta
// esperou por recurso. Em cada montagem pronta e na mais cara de cada herói (as três comuns de maior custo).
// Uso: node ferramentas/recursos.mjs [segundos]
import { criarMundo, passo, entradaVazia } from "../tela/sim.js";
import { TIPOS, MONTAGENS, HABILIDADES } from "../tela/conteudo.js";

const segundos = Number(process.argv[2] || 30);

function laboratorio(heroi, kit) {
  const m = criarMundo({ heroi, kit });
  for (const u of m.unidades) if (u !== m.heroi) u.morto = true;
  passo(m, entradaVazia());
  const h = m.heroi;
  h.x = h.px = 480; h.y = h.py = 280;
  m.fase = "luta";
  m.stats.primeira = -1;
  h.vida = h.vidaMax = 1e6;
  for (let y = 200; y <= 360; y += 10) for (let x = 400; x <= 620; x += 10) {
    if (Math.hypot(x - 480, y - 280) < 14) continue;
    const d = TIPOS.veterano;
    const u = { id: m.proximoId++, lado: 1, tipo: "veterano", def: d, x, y, px: x, py: y, vx: 0, vy: 0, kx: 0, ky: 0,
      raio: d.raio, massa: d.massa, vida: 1e6, vidaMax: 1e6, alvo: null, reavaliar: 0, acao: null, recarga: 0,
      atordoado: 1e6, congelado: 0, flash: 0, virado: -1, passo: 0, abalado: 0, mostra: 0, fugindo: false, saiu: false,
      morto: false, atacantes: 0, aura: false, slot: 0 };
    m.unidades.push(u); m.lados[1].push(u);
  }
  return m;
}

function sequencia(heroi, kit, modo) {
  const m = laboratorio(heroi, kit), h = m.heroi, ent = entradaVazia();
  ent.mx = 560; ent.my = 280; ent.atacar = true;
  const comuns = ["h1", "h2", "h3"].map((s) => h.slots[s]), ult = h.slots.ult;
  const maisCara = Math.max(...comuns.map((id) => h.kit[id].custo || 0));
  let menor = h.recurso, abaixo = 0, esperas = 0, usos = 0, prox = 0;
  const fila = [];
  while (m.t < segundos) {
    ent.apertos = [];
    const prontas = comuns.filter((id) => !(h.cds[id] > 0));
    if (modo === "normal" && m.t >= prox && prontas.length) {
      ent.apertos = [prontas[0]];
      prox = m.t + 0.4;
    }
    if (modo === "concentrada" && !fila.length && prontas.length === 3) fila.push(...comuns);
    if (modo === "concentrada" && fila.length && !h.acao) ent.apertos = [fila[0]];
    if (!(h.cds[ult] > 0) && !h.acao) ent.apertos.push(ult);
    // uma comum pronta, apertada, que não sai por falta de recurso
    for (const id of ent.apertos) if (h.kit[id].custo && h.recurso < h.kit[id].custo && !(h.cds[id] > 0)) esperas++;
    const antes = { ...h.cds };
    passo(m, ent);
    for (const id of comuns) if ((h.cds[id] || 0) > (antes[id] || 0)) { usos++; if (fila[0] === id) fila.shift(); }
    menor = Math.min(menor, h.recurso);
    if (h.recurso < maisCara) abaixo += 1 / 60;
    m.eventos.length = 0;
  }
  return { menor, abaixo, esperas, usos, porMinuto: (usos * 60) / segundos };
}

const caras = (heroi) => Object.entries(HABILIDADES[heroi]).filter(([, k]) => k.tipo === "comum")
  .sort((a, b) => b[1].custo - a[1].custo).slice(0, 3).map(([id]) => id);
console.log(`${segundos} s de uso contínuo`);
for (const heroi of ["guerreiro", "mago"]) {
  const kits = [...Object.entries(MONTAGENS[heroi]), [`mais cara (${caras(heroi).join(", ")})`,
    { comuns: caras(heroi), talentos: heroi === "mago" ? ["menteRapida"] : [] }]];
  for (const [nome, kit] of kits) for (const modo of ["normal", "concentrada"]) {
    const r = sequencia(heroi, kit, modo);
    console.log(`${heroi.padEnd(10)} ${nome.padEnd(44)} ${modo.padEnd(12)} menor ${r.menor.toFixed(0).padStart(3)}  abaixo da comum mais cara ${r.abaixo.toFixed(1).padStart(4)} s` +
      `  esperas por recurso ${String(r.esperas).padStart(3)} passos  comuns usadas ${r.usos} (${r.porMinuto.toFixed(0)} por minuto)`);
  }
}
