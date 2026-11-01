// PROTÓTIPO de campo livre: um jogador automático simples, para os testes de equilíbrio (Node), a medição de
// desempenho e os vídeos (?robo=1). Ele preenche a mesma entrada que o teclado e o mouse preenchem: as teclas de
// movimento, o ponto do mouse, o botão do ataque e os apertos das habilidades. Não é a IA de ninguém no jogo.
import { ordenar } from "./sim.js";

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
  // o golpe do campeão anunciado em cima do herói: sair dele
  for (const e of ini) {
    if (e.tipo === "campeao" && e.acao && e.acao.forma && (h.x - e.x) ** 2 + (h.y - e.y) ** 2 < 34 * 34) {
      andar(ent, h.x - e.x, h.y - e.y);
      return;
    }
  }
  const aliados = m.centros[0];
  // decide uma habilidade a cada 0,25 s, como quem olha o campo, e não a cada quadro
  const decide = m.t >= (r.decisao || 0);
  if (decide) r.decisao = m.t + (r.nivel === "medio" ? 0.6 : 0.25);
  const erro = r.nivel === "medio" ? 12 : 0, rng = () => (Math.sin(m.t * 91.7 + r.erro++) * 0.5) * erro;
  if (h.nomeHeroi === "guerreiro") {
    const k = h.kit;
    if (decide && h.recurso >= k.salto.custo && g.n >= 6 && dg <= k.salto.alcance) {
      ent.mx = g.x + rng(); ent.my = g.y + rng(); ent.apertos.push("salto"); return;
    }
    const em = contar(ini, h.x, h.y, k.varredura.raio - 2);
    if (decide && em.n >= 4 && h.cds.varredura <= 0) { ent.mx = em.x + rng(); ent.my = em.y + rng(); ent.apertos.push("varredura"); }
    else if (decide && h.cds.investida <= 0 && g.n >= 4 && dg > 55 && dg < 150 && vida > 0.4) {
      ent.mx = g.x + rng(); ent.my = g.y + rng(); ent.apertos.push("investida");
    }
    if (vida < 0.3 && aliados) andar(ent, aliados.x - h.x, aliados.y - h.y);
    else if (dg > 16) andar(ent, g.x - h.x, g.y - h.y);
    else andar(ent, perto.x - h.x, perto.y - h.y);
    ent.atacar = dp < 26;
    return;
  }
  // o mago
  const k = h.kit;
  if (decide && dp < 22 && h.cds.piscar <= 0) {
    ent.mx = h.x - (perto.x - h.x) * 4; ent.my = h.y - (perto.y - h.y) * 4; ent.apertos.push("piscar"); return;
  }
  const em = contar(ini, h.x, h.y, 70);
  if (decide && em.n >= 5 && h.recurso >= k.muralha.custo + 15 && h.cds.muralha <= 0) {
    const a = Math.atan2(em.y - h.y, em.x - h.x);
    ent.mx = h.x + Math.cos(a) * 40; ent.my = h.y + Math.sin(a) * 40; ent.apertos.push("muralha"); return;
  }
  if (decide && g.n >= 3 && dg <= k.bola.alcance && h.recurso >= k.bola.custo && h.cds.bola <= 0) {
    ent.mx = g.x + rng(); ent.my = g.y + rng(); ent.apertos.push("bola");
  }
  if (vida < 0.35 && aliados) andar(ent, aliados.x - h.x, aliados.y - h.y);
  else if (dp < 70) andar(ent, h.x - perto.x, h.y - perto.y);
  else if (dp > 125) andar(ent, g.x - h.x, g.y - h.y);
  else andar(ent, -(perto.y - h.y), perto.x - h.x);
  ent.atacar = dp < 170 && !ent.apertos.length;
}
