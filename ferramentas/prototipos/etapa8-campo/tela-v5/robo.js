// PROTÓTIPO de campo livre: um jogador automático simples, para os testes de equilíbrio (Node), a medição de
// desempenho e os vídeos (?robo=1). Ele preenche a mesma entrada que o teclado e o mouse preenchem: as teclas de
// movimento, o ponto do mouse, o botão do ataque e os apertos das habilidades. Não é a IA de ninguém no jogo.
import { ordenar, dentro } from "./sim.js";

// `nivel`: "forte" decide a cada 0,25 s e mira no centro do grupo mais denso; "medio" decide a cada 0,6 s, erra a mira
// em até 12 px e vai para o grupo mais perto (mais parecido com uma primeira partida de uma pessoa).
export function criarRobo({ ordemAtacar = 6, passivo = false, nivel = "forte" } = {}) {
  return { proximo: 0, grupo: null, ordemAtacar, passivo, ordenou: false, nivel, erro: 0 };
}

function grupoMaisDenso(inimigos, raio) {
  let melhor = null;
  const r2 = raio * raio, n = inimigos.length, passo = Math.max(1, Math.floor(n / 60));
  for (let i = 0; i < n; i += passo) {
    const e = inimigos[i];
    let k = 0, sx = 0, sy = 0;
    for (const o of inimigos) {
      if ((o.x - e.x) ** 2 + (o.y - e.y) ** 2 <= r2) { k++; sx += o.x; sy += o.y; }
    }
    if (!melhor || k > melhor.n) melhor = { x: sx / k, y: sy / k, n: k };
  }
  return melhor;
}

function grupoMaisPerto(inimigos, h, raio) {
  let perto = null, dp = Infinity;
  for (const e of inimigos) { const q = (e.x - h.x) ** 2 + (e.y - h.y) ** 2; if (q < dp) { dp = q; perto = e; } }
  return contar(inimigos, perto.x, perto.y, raio);
}

function contar(inimigos, x, y, r) {
  let k = 0, sx = 0, sy = 0;
  for (const o of inimigos) if ((o.x - x) ** 2 + (o.y - y) ** 2 <= r * r) { k++; sx += o.x; sy += o.y; }
  return { n: k, x: k ? sx / k : x, y: k ? sy / k : y };
}

function andar(ent, dx, dy) {
  const n = Math.hypot(dx, dy);
  ent.esq = ent.dir = ent.cima = ent.baixo = false;
  if (n < 0.5) return;
  const ux = dx / n, uy = dy / n;
  ent.dir = ux > 0.38; ent.esq = ux < -0.38; ent.baixo = uy > 0.38; ent.cima = uy < -0.38;
}

export function pensar(r, m, ent) {
  ent.apertos = [];
  ent.atacar = false;
  const h = m.heroi, ini = m.lados[1];
  if (h.morto || m.fase === "fim" || !ini.length) { andar(ent, 0, 0); return; }
  if (r.passivo) { andar(ent, 0, 0); ent.mx = h.x + 10; ent.my = h.y; return; }
  if (!r.ordenou && m.t >= r.ordemAtacar) { ordenar(m, "atacar"); r.ordenou = true; }
  if (m.t >= r.proximo) {
    r.grupo = r.nivel === "medio" ? grupoMaisPerto(ini, m.heroi, 30) : grupoMaisDenso(ini, 30);
    r.proximo = m.t + (r.nivel === "medio" ? 0.6 : 0.25);
  }
  let perto = null, dp = Infinity;
  for (const e of ini) { const q = (e.x - h.x) ** 2 + (e.y - h.y) ** 2; if (q < dp) { dp = q; perto = e; } }
  dp = Math.sqrt(dp);
  const g = r.grupo || { x: perto.x, y: perto.y, n: 1 };
  const dg = Math.hypot(g.x - h.x, g.y - h.y);
  const vida = h.vida / h.vidaMax;
  ent.mx = perto.x; ent.my = perto.y;
  // os avisos do Capitão só são vistos depois de um tempo de reação (uma pessoa não sai no mesmo quadro)
  const reacao = r.nivel === "medio" ? 0.35 : 0.15, viu = (e, total) => total - e.acao.t >= reacao;
  // o golpe do campeão (ou o machado do Capitão) anunciado com o herói dentro do arco desenhado: sair dele
  for (const e of ini) {
    if (e.acao && e.acao.forma && (e.tipo === "campeao" || e.tipo === "lider" && !e.acao.tipo && viu(e, e.acao.preparo || e.def.preparo)) &&
        dentro({ ...e.acao.forma, raio: e.acao.forma.raio + 3 }, h.x, h.y)) {
      andar(ent, h.x - e.x, h.y - e.y);
      return;
    }
    // os círculos do Capitão (a Arremetida, o Rodopio) com o herói dentro: sair, para longe do centro
    const circulo = e.tipo === "lider" && e.acao && (e.acao.tipo === "arremetida" && e.acao.fase === "preparo" &&
      viu(e, e.def.arremetida.preparo) || e.acao.tipo === "rodopio" && viu(e, e.def.rodopio.preparo));
    if (circulo && dentro({ ...e.acao.forma, raio: e.acao.forma.raio + 3 }, h.x, h.y)) {
      const f = e.acao.forma, dx = h.x - f.x, dy = h.y - f.y;
      andar(ent, Math.abs(dx) + Math.abs(dy) > 0.5 ? dx : 1, dy);
      return;
    }
  }
  // a faixa da carga do líder marcada no chão com o herói dentro: sair de lado; o Guerreiro com a Varredura pronta
  // e o líder perto tenta interromper a reunião
  for (const e of ini) {
    if (!e.acao || e.acao.tipo !== "reunir" || !viu(e, e.def.carga.reunir)) continue;
    const dl = Math.hypot(e.x - h.x, e.y - h.y);
    // perto da reunião, o golpe principal a desfaz (o Guerreiro com a Varredura pronta)
    if (h.nomeHeroi === "guerreiro" && dl < 30 && h.cds.varredura <= 0) { ent.mx = e.x; ent.my = e.y; ent.atacar = true; return; }
    if (dentro(e.acao.forma, h.x, h.y)) { andar(ent, -Math.sin(e.acao.dir), Math.cos(e.acao.dir)); return; }
  }
  const aliados = m.centros[0];
  // decide uma habilidade a cada 0,25 s, como quem olha o campo, e não a cada quadro
  const decide = m.t >= (r.decisao || 0);
  if (decide) r.decisao = m.t + (r.nivel === "medio" ? 0.6 : 0.25);
  const erro = r.nivel === "medio" ? 12 : 0, rng = () => (Math.sin(m.t * 91.7 + r.erro++) * 0.5) * erro;
  // as habilidades equipadas, cada uma pela dica dela (`ia`), uma por decisão
  if (decide) for (const slot of ["ult", "h1", "h2", "h3"]) {
    const id = h.slots[slot], k = h.kit[id];
    if (!k || !k.ia || h.cds[id] > 0 || (k.custo && h.recurso < k.custo) || h.acao && h.acao.fase === "preparo") continue;
    const alvo = escolherUso(m, h, k, g, dg, ini);
    if (!alvo) continue;
    ent.mx = alvo.x + rng(); ent.my = alvo.y + rng(); ent.apertos.push(id);
    break;
  }
  if (h.nomeHeroi === "guerreiro") {
    // a Investida para chegar a um grupo
    if (decide && !ent.apertos.length && h.cds.investida <= 0 && g.n >= 4 && dg > 55 && dg < 150 && vida > 0.4) {
      ent.mx = g.x + rng(); ent.my = g.y + rng(); ent.apertos.push("investida");
    }
    if (vida < 0.3 && aliados) andar(ent, aliados.x - h.x, aliados.y - h.y);
    else if (dg > 16) andar(ent, g.x - h.x, g.y - h.y);
    else andar(ent, perto.x - h.x, perto.y - h.y);
    // o principal: a Varredura com o inimigo ao alcance da aproximação (o mouse no grupo, a aproximação faz o resto)
    if (!ent.apertos.length) { ent.atacar = dp < h.kit.varredura.assist.alcance; if (ent.atacar) { ent.mx = perto.x; ent.my = perto.y; } }
    return;
  }
  // o mago: o Piscar para fugir de quem chega colado; a Bola de Fogo no grupo ao alcance
  if (decide && dp < 22 && h.cds.piscar <= 0) {
    ent.mx = h.x - (perto.x - h.x) * 4; ent.my = h.y - (perto.y - h.y) * 4; ent.apertos.push("piscar"); return;
  }
  if (vida < 0.35 && aliados) andar(ent, aliados.x - h.x, aliados.y - h.y);
  else if (dp < 70) andar(ent, h.x - perto.x, h.y - perto.y);
  else if (dp > 125) andar(ent, g.x - h.x, g.y - h.y);
  else andar(ent, -(perto.y - h.y), perto.x - h.x);
  if (!ent.apertos.length) {
    const alvo = dg <= h.kit.bola.alcance ? g : perto;
    ent.mx = alvo.x + rng(); ent.my = alvo.y + rng();
    ent.atacar = Math.hypot(alvo.x - h.x, alvo.y - h.y) < h.kit.bola.alcance;
  }
}

// Onde usar uma habilidade agora, pela dica `ia` dela; null: não vale a pena.
function escolherUso(m, h, k, g, dg, ini) {
  const ia = k.ia, alcance = k.alcance || k.comprimento || 200;
  if (ia.usa === "grupo") return g.n >= ia.min && dg <= alcance ? g : null;
  if (ia.usa === "perto") { const c = contar(ini, h.x, h.y, ia.raio); return c.n >= ia.min ? c : null; }
  if (ia.usa === "linha") {
    // quantos estão perto da linha até o grupo
    const ux = (g.x - h.x) / (dg || 1), uy = (g.y - h.y) / (dg || 1);
    let n = 0;
    for (const e of ini) { const px = e.x - h.x, py = e.y - h.y, t = px * ux + py * uy; if (t > 0 && t < alcance && Math.abs(px * uy - py * ux) < 14) n++; }
    return n >= ia.min ? g : null;
  }
  if (ia.usa === "parede") { const c = contar(ini, h.x, h.y, 70); if (c.n < ia.min) return null; const a = Math.atan2(c.y - h.y, c.x - h.x); return { x: h.x + Math.cos(a) * 40, y: h.y + Math.sin(a) * 40 }; }
  if (ia.usa === "sangue") { let n = 0; for (const e of ini) if (e.sangra && Math.hypot(e.x - h.x, e.y - h.y) < k.raio) n++; return n >= ia.min ? h : null; }
  if (ia.usa === "aliados") { const al = m.lados[0].filter((a) => a !== h && Math.hypot(a.x - h.x, a.y - h.y) < k.raio).length; return al >= ia.min ? h : null; }
  if (ia.usa === "arqueiros") {
    const arq = ini.filter((e) => e.tipo === "arqueiro" && Math.hypot(e.x - h.x, e.y - h.y) < 170);
    return arq.length >= ia.min ? contar(arq, arq[0].x, arq[0].y, 60) : null;
  }
  return null;
}
