// As ordens fazem diferença? A mesma batalha (mesma semente, o mesmo jogador automático no herói) com estratégias de
// ordens diferentes: nenhuma ordem (todos acompanham o herói), a do jogador automático (Atacar aos 6 s) e algumas
// ordens oportunas dadas por roteiro. Mede o resultado, as perdas, quem derrubou quem, o dano que o Capitão fez nas
// tropas e quantos arqueiros sobreviveram. Não mede diversão: compara consequências.
// Uso: node ferramentas/ordens.mjs [forte|medio]
import { criarMundo, passo, entradaVazia, resumo, ordenar, selecionar, tropasDoTipo } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";

const nivel = process.argv[2] || "forte";
const tipo = (m, t) => { selecionar(m, tropasDoTipo(m, t)); };
const todos = (m) => selecionar(m, []);

// cada estratégia: [nome, o tempo em que o jogador automático dá Atacar (Infinity: nunca), roteiro(m, t) chamado a cada passo]
const ESTRATEGIAS = {
  original: [
    ["sem ordens (acompanham)", Infinity, null],
    ["Atacar aos 6 s (o padrão do robô)", 6, null],
    ["arqueiros defendem atrás, soldados atacam", Infinity, (m, t, s) => {
      if (t > 1 && !s.a) { s.a = 1; tipo(m, "arqueiro"); ordenar(m, "defender", 230, 280); tipo(m, "soldado"); ordenar(m, "atacar"); todos(m); }
    }],
    ["arqueiros no porta-estandarte, soldados atacam", Infinity, (m, t, s) => {
      const e = m.lados[1].find((u) => u.tipo === "estandarte");
      if (t > 3 && !s.a && e) { s.a = 1; tipo(m, "arqueiro"); ordenar(m, "atacar", undefined, undefined, e); tipo(m, "soldado"); ordenar(m, "atacar"); todos(m); }
    }],
  ],
  capitao: [
    ["sem ordens (acompanham)", Infinity, null],
    ["Atacar aos 6 s (o padrão do robô)", 6, null],
    ["arqueiros no Capitão", Infinity, (m, t, s) => {
      if (t > 3 && !s.a && m.lider) { s.a = 1; tipo(m, "arqueiro"); ordenar(m, "atacar", undefined, undefined, m.lider); todos(m); }
    }],
    ["tropas saem da frente do Capitão quando ele vem", Infinity, (m, t, s) => {
      // quando o Capitão chega a 120 px de um grupo, quem está perto dele vai para 220 px dele, do outro lado do herói
      // (fora do alcance em que ele caça tropas, 170 px); o herói o segura; depois de 6 s, voltam a acompanhar
      const l = m.lider;
      if (!l || l.morto) return;
      if (!s.recuou && t - (s.volta || -99) > 4) {
        const perto = m.lados[0].filter((u) => u !== m.heroi && Math.hypot(u.x - l.x, u.y - l.y) < 120);
        if (perto.length >= 6) {
          selecionar(m, perto.map((u) => u.id));
          const h = m.heroi, dx = h.x - l.x, dy = h.y - l.y, n = Math.hypot(dx, dy) || 1;
          ordenar(m, "defender", Math.max(20, Math.min(940, l.x + (dx / n) * 220)), Math.max(20, Math.min(540, l.y + (dy / n) * 220)));
          todos(m); s.recuou = t;
        }
      } else if (s.recuou && t - s.recuou > 6) { ordenar(m, "acompanhar"); s.recuou = 0; s.volta = t; }
    }],
    ["tropas longe do duelo (Defender a 250 px dele)", Infinity, (m, t, s) => {
      // enquanto o Capitão está a até 160 px do herói, o exército segura um ponto a 250 px dele, do outro lado do herói;
      // quando ele se afasta do herói (ou cai), todos voltam a acompanhar
      const l = m.lider, h = m.heroi, duelo = l && !l.morto && Math.hypot(l.x - h.x, l.y - h.y) < 160;
      if (duelo && !s.longe) {
        const dx = h.x - l.x, dy = h.y - l.y, n = Math.hypot(dx, dy) || 1;
        ordenar(m, "defender", Math.max(20, Math.min(940, l.x + (dx / n) * 250)), Math.max(20, Math.min(540, l.y + (dy / n) * 250)));
        s.longe = true;
      } else if (!duelo && s.longe) { ordenar(m, "acompanhar"); s.longe = false; }
    }],
  ],
};

for (const [enc, lista] of Object.entries(ESTRATEGIAS)) for (const heroi of ["guerreiro", "mago"]) {
  console.log(`\n${enc} · ${heroi} · jogador ${nivel}`);
  for (const [nome, ordemAtacar, roteiro] of lista) {
    const m = criarMundo({ heroi, encontro: enc }), ent = entradaVazia(), r = criarRobo({ nivel, ordemAtacar }), s = {};
    while (m.fase !== "fim" && m.t < 180) {
      pensar(r, m, ent);
      if (roteiro) roteiro(m, m.t, s);
      passo(m, ent);
      m.eventos.length = 0;
    }
    const z = resumo(m), arq = m.lados[0].filter((u) => u.tipo === "arqueiro").length;
    console.log(`  ${nome.padEnd(48)} ${String(z.resultado ?? "em curso").padEnd(7)} ${z.t.toFixed(0).padStart(3)} s · vida ${z.vida.toFixed(0).padStart(3)} · herói ${String(z.abatesHeroi).padStart(3)}` +
      ` · tropas ${String(z.abatesAliados).padStart(3)} · perdas ${String(z.perdas).padStart(2)}/${z.aliados} · arqueiros vivos ${arq}` +
      (enc === "capitao" ? ` · Capitão nas tropas ${z.liderTropas.toFixed(0)}, no herói ${z.liderHeroi.toFixed(0)}` : ""));
  }
}
