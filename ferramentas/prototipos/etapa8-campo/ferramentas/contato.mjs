// A sequência dos ataques inimigos no herói: aproximar → começar o ataque → chegar ao contato → aplicar o dano. Cada
// ataque que um inimigo começa com o herói como alvo é acompanhado até acabar: acertou (o herói perdeu vida por ele),
// errou (chegou ao contato e o herói não estava ao alcance), cancelado (atordoado, interrompido, morto, firme...).
// Cinco situações: o herói parado no meio de soldados, andando, esquivando a preparação do Capitão, em duelo com ele,
// e o choque da primeira batalha com o jogador automático.
// Uso: node ferramentas/contato.mjs
import { criarMundo, passo, entradaVazia } from "../tela/sim.js";
import { criarRobo, pensar } from "../tela/robo.js";
import { TIPOS } from "../tela/conteudo.js";

function laboratorio(heroi, n, raio) {
  const m = criarMundo({ heroi, encontro: "capitao" });
  m.fase = "luta";
  for (const g of Object.values(m.grupos)) g.ativo = true;
  m.stats.primeira = -1;
  const h = m.heroi, l = m.lider;
  for (const u of m.unidades) if (u !== h && u !== l) u.morto = true;
  passo(m, entradaVazia());
  h.x = h.px = 480; h.y = h.py = 280;
  l.x = l.px = 900; l.y = l.py = 40; l.atordoado = 9999;   // o Capitão fora, a não ser que a situação o queira
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2, d = TIPOS.soldado;
    const u = { id: m.proximoId++, lado: 1, tipo: "soldado", def: d, x: h.x + Math.cos(a) * raio, y: h.y + Math.sin(a) * raio,
      vx: 0, vy: 0, kx: 0, ky: 0, raio: d.raio, massa: d.massa, vida: 999, vidaMax: 999, alvo: null, reavaliar: 0, acao: null,
      recarga: Math.random() * 0.5, atordoado: 0, congelado: 0, flash: 0, virado: 1, passo: 0, abalado: 0, mostra: 0,
      fugindo: false, saiu: false, morto: false, atacantes: 0, aura: false, slot: 0 };
    u.px = u.x; u.py = u.y;
    m.unidades.push(u); m.lados[1].push(u);
  }
  return m;
}

function acompanhar(m, ent, segundos, mexer) {
  const h = m.heroi, abertos = new Map(), r = { comecou: 0, acertou: 0, errou: 0, cancelado: 0, dano: 0, porTipo: {} };
  const conta = (tipo, k) => { r[k]++; (r.porTipo[tipo] ||= { comecou: 0, acertou: 0, errou: 0, cancelado: 0 })[k]++; };
  const fim = m.t + segundos;
  while (m.t < fim && !h.morto && m.fase !== "fim") {
    if (mexer) mexer(m, ent);
    passo(m, ent);
    const acertos = new Set(m.eventos.filter((e) => e.tipo === "heroiAtingido").map((e) => e.fonteId));
    for (const e of m.eventos) if (e.tipo === "heroiAtingido") r.dano += e.valor;
    m.eventos.length = 0;
    for (const u of m.unidades) {
      if (u.lado !== 1) continue;
      const a = u.acao, antes = abertos.get(u.id);
      if (antes && antes !== a) {
        abertos.delete(u.id);
        if (acertos.has(u.id)) conta(u.tipo, "acertou");
        else if (antes.t <= 0.0001 && !u.morto) conta(u.tipo, "errou");
        else conta(u.tipo, "cancelado");
      }
      if (a && a.alvo === h && !abertos.has(u.id) && (!a.tipo || a.tipo === "rodopio")) { abertos.set(u.id, a); conta(u.tipo, "comecou"); }
    }
  }
  return r;
}

const linha = (nome, r) => console.log(`${nome.padEnd(44)} começou ${String(r.comecou).padStart(3)} · acertou ${String(r.acertou).padStart(3)} · errou ${String(r.errou).padStart(3)}` +
  ` · cancelado ${String(r.cancelado).padStart(3)} · dano no herói ${r.dano.toFixed(0).padStart(4)}   ${JSON.stringify(r.porTipo)}`);

// 1. parado no meio de 8 soldados
{ const m = laboratorio("guerreiro", 8, 18); linha("parado, 8 soldados em volta", acompanhar(m, entradaVazia(), 10)); }
// 2. andando em quadrado no meio de 14 soldados
{ const m = laboratorio("guerreiro", 14, 30), ent = entradaVazia();
  linha("andando, 14 soldados", acompanhar(m, ent, 10, (m, e) => { const k = Math.floor(m.t) % 4; e.dir = k === 0; e.baixo = k === 1; e.esq = k === 2; e.cima = k === 3; })); }
// 3 e 4. o Capitão: duelo parado (o herói só golpeia) e esquivando (anda para longe quando a preparação aparece)
for (const esquiva of [false, true]) {
  const m = laboratorio("guerreiro", 0, 0), l = m.lider, h = m.heroi, ent = entradaVazia();
  l.atordoado = 0; l.x = l.px = h.x + 40; l.y = l.py = h.y; l.arremCd = 99; l.cargaCd = 99;
  linha(esquiva ? "Capitão, esquivando as preparações" : "Capitão, duelo parado", acompanhar(m, ent, 15, (m, e) => {
    e.mx = l.x; e.my = l.y; e.esq = e.dir = e.cima = e.baixo = false;
    if (esquiva && l.acao && l.acao.forma) { const dx = h.x - l.x; e.dir = dx > 0; e.esq = dx <= 0; }
  }));
}
// 5. o choque da primeira batalha, jogador automático médio
{ const m = criarMundo({ heroi: "guerreiro" }), ent = entradaVazia(), r = criarRobo({ nivel: "medio" });
  linha("primeira batalha, jogador médio, 30 s", acompanhar(m, ent, 30, (m, e) => pensar(r, m, e))); }
