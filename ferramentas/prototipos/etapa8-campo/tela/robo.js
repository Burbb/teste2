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
  let g = r.grupo || { x: perto.x, y: perto.y, n: 1 };
  let dg = Math.hypot(g.x - h.x, g.y - h.y);
  const vida = h.vida / h.vidaMax;
  ent.mx = perto.x; ent.my = perto.y;
  // os avisos do Capitão só são vistos depois de um tempo de reação (uma pessoa não sai no mesmo quadro)
  const reacao = r.nivel === "medio" ? 0.35 : 0.15, viu = (e, total) => total - e.acao.t >= reacao;
  // Campo Livre 8: os golpes de Harg reconstruído. Com o herói dentro do aviso (visto depois do tempo de reação), o
  // forte sai para o lado da direção do golpe; o médio recua em linha reta (o erro comum, que a Varredura e a Investida
  // castigam). Na abertura (a recuperação comprometida) ou com a postura quebrada, os dois vão nele e batem.
  // Campo Livre 9: o mesmo para todos com a máquina de golpes (Harg, Vesna, o General): os golpes em estágios (os anéis,
  // a cruz, o leque) contam só os estágios que ainda não estouraram; nas faixas, sai para o lado da faixa. A esquiva
  // continua na execução (o contato vem no fim dela). Nos anéis (o Terremoto), o forte vai para a beira de dentro do
  // anel em que está e entra no anel de dentro logo que ele estoura; no anel do meio, sai com a mobilidade (a pé não dá
  // tempo); no último, sai por fora se a beira de fora estiver mais perto. O médio só se afasta.
  for (const l of ini) {
    if (!l.h8 || l.morto) continue;
    const g = l.h8.golpe;
    if (g && (g.etapa === "preparo" && g.total - g.t >= reacao || g.etapa === "exec")) {
      const fs = g.formasEstagio;
      if (fs && fs.every((e) => e.length === 1 && e[0].tipo === "anel")) {
        const c = fs[0][0], dx = h.x - c.x || 1, dy = h.y - c.y, d = Math.hypot(dx, dy), e = g.etapa === "exec" ? g.estagio : 0;
        const k = fs.findIndex((a, j) => j >= e && d >= a[0].r0 - 3 && d <= a[0].raio + 3);
        if (k >= 0) {
          const a = fs[k][0];
          let sai = 1;
          if (r.nivel === "forte") {
            if (k === e) sai = k > 0 ? -1 : 1;
            else if (k === fs.length - 1 && a.raio - d < d - a.r0) sai = 1;
            else sai = d - a.r0 > 5 ? -1 : 0;
            const mob = h.slots.mobilidade;
            // perto do estouro (a invulnerabilidade da Investida cobre os últimos 0,25 s)
            if (k === 0 && h.cds[mob] <= 0 && !h.acao && g.etapa === "preparo" && g.t <= 0.2) { ent.mx = h.x + (dx / d) * 120; ent.my = h.y + (dy / d) * 120; ent.apertos.push(mob); return; }
          }
          andar(ent, sai * dx, sai * dy);
          ent.mx = l.x; ent.my = l.y;
          return;
        }
      }
      const pendentes = g.formasEstagio ? g.formasEstagio.slice(g.etapa === "exec" ? g.estagio : 0).flat() : [r.nivel === "forte" && g.onda ? g.onda : g.forma];
      const largo = (f) => f.tipo === "faixa" ? { ...f, largura: f.largura + 4 } : { ...f, raio: f.raio + 4, r0: Math.max(0, (f.r0 || 0) - 4) };
      const f = pendentes.find((f) => dentro(largo(f), h.x, h.y));
      if (f) {
        // Harg (o do 8 e o frágil): como no Campo Livre 8 (o forte sai para o lado da direção do golpe; o médio recua)
        if (!l.h8.cfg.stats) {
          if (r.nivel === "forte") {
            const px = -Math.sin(g.dir), py = Math.cos(g.dir), lado = (h.x - l.x) * px + (h.y - l.y) * py >= 0 ? 1 : -1;
            andar(ent, px * lado - Math.cos(g.dir) * 0.3, py * lado - Math.sin(g.dir) * 0.3);
          } else andar(ent, h.x - l.x, h.y - l.y);
        } else if (f.tipo === "anel") {
          const fora = g.etapa === "exec" && g.estagio > 0 && r.nivel === "forte";
          andar(ent, (fora ? -1 : 1) * (h.x - f.x || 1), (fora ? -1 : 1) * (h.y - f.y));
        } else if (f.tipo === "faixa") {
          const ux = f.x2 - f.x1, uy = f.y2 - f.y1, lado = (h.x - f.x1) * -uy + (h.y - f.y1) * ux >= 0 ? 1 : -1;
          if (r.nivel === "forte") andar(ent, -uy * lado, ux * lado); else andar(ent, h.x - l.x, h.y - l.y);
        } else if (r.nivel === "forte" && f.tipo === "arco") {
          const px = -Math.sin(g.dir), py = Math.cos(g.dir), lado = (h.x - l.x) * px + (h.y - l.y) * py >= 0 ? 1 : -1;
          andar(ent, px * lado - Math.cos(g.dir) * 0.3, py * lado - Math.sin(g.dir) * 0.3);
        } else andar(ent, h.x - f.x || h.x - l.x, h.y - f.y || h.y - l.y);
        ent.mx = l.x; ent.my = l.y;
        return;
      }
    }
    const dl = Math.hypot(l.x - h.x, l.y - h.y);
    if ((l.h8.quebrado > 0 || m.t < (l.h8.abertoAte || 0)) && dl < 120) {
      ent.mx = l.x; ent.my = l.y;
      if (h.nomeHeroi === "guerreiro") { if (dl > 18) andar(ent, l.x - h.x, l.y - h.y); else andar(ent, 0, 0); ent.atacar = dl < 60; }
      else { andar(ent, 0, 0); ent.atacar = dl < h.kit.bola.alcance; }
      for (const slot of ["h1", "h2", "h3", "ult"]) {
        const id = h.slots[slot], k = h.kit[id];
        if (k && h.cds[id] <= 0 && (!k.custo || h.recurso >= k.custo) && (k.alcance || 60) >= dl) { ent.apertos.push(id); break; }
      }
      return;
    }
  }
  // as cargas no chão (o barril do sapador, o rastro explosivo): sair do círculo
  // (e, no Campo Livre 9, as magias anunciadas: a Coluna de Ardis, a Bola dos magos de batalha)
  const circulos = [...((m.g9 && m.g9.cargas) || []), ...(m.g9 ? (m.magias || []).filter((z) => z.lado === 1) : [])];
  for (const c of circulos) {
    if ((h.x - c.x) ** 2 + (h.y - c.y) ** 2 > (c.raio + 4) ** 2 || c.t < reacao) continue;
    andar(ent, h.x - c.x || 1, h.y - c.y);
    return;
  }
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
  // Campo Livre 9: um herói inimigo a até 220 px vira o alvo (o grupo e o mais perto passam a ser ele)
  let alvoHeroi = null;
  for (const e of ini) if (e.heroi9 && !e.morto && Math.hypot(e.x - h.x, e.y - h.y) < (alvoHeroi ? Math.hypot(alvoHeroi.x - h.x, alvoHeroi.y - h.y) : 220)) alvoHeroi = e;
  if (alvoHeroi) { g = { x: alvoHeroi.x, y: alvoHeroi.y, n: 8 }; perto = alvoHeroi; dp = Math.hypot(perto.x - h.x, perto.y - h.y); dg = dp; }
  const aliados = m.lados[0].length > 1 ? m.centros[0] : null;   // sozinho (o treino), não há para onde recuar
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
