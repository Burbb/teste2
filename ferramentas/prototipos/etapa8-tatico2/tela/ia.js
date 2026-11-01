// PROTÓTIPO tático (nada no jogo): a IA de uma vez. Serve aos inimigos e, nos testes e na medição, ao jogador
// automático dos aliados. Cada decisão compara opções completas: andar até uma casa alcançável e lançar uma habilidade
// num alvo válido dali; o valor de cada opção vem da prévia (regras.prever, a mesma conta da ação) mais o valor da casa
// para o papel de quem age. Repete enquanto houver PA e uma opção que valha a pena; no fim, usa os PM que sobraram
// para se posicionar (o corpo a corpo pelo caminho de verdade até o alvo, quem atira longe do corpo a corpo e com
// visão, o apoio perto dos aliados). Não vê as armadilhas do jogador. Provocado, só ataca quem provocou (se puder).
import { atual, alcancaveis, alvosValidos, prever, lancar, mover, encerrarVez, dist, inimigosDe, aliadosDe, unidade,
  temEstado, livre, passavel, VIZ, visao, alcanceDe, podeLancar } from "./regras.js";

const chave = (x, y) => `${x},${y}`;
const VALOR_ESTADO = { imobilizado: 7, desequilibrado: 4, congelado: 4, lento: 3, marcado: 4, ofuscado: 3, provocado: 5,
  protegido: 4, barreira: 4, abencoado: 4, inspirado: 4, coberto: 3, olhoAguia: 2 };

/** Faz a vez inteira de quem está na ordem (até 6 ações). Retorna as ações feitas (para o registro e a tela). */
export function jogarVez(m) {
  const u = atual(m), feitas = [];
  for (let i = 0; i < 6 && !m.fim && u.vivo; i++) {
    const op = melhorOpcao(m, u);
    if (!op) break;
    if (op.casa && (op.casa[0] !== u.x || op.casa[1] !== u.y)) { mover(m, u, ...op.casa); feitas.push({ t: "andar", para: op.casa }); }
    if (!u.vivo || m.fim) break;
    if (!lancar(m, u, op.hab, ...op.alvo)) break;
    feitas.push({ t: "lancar", hab: op.hab, alvo: op.alvo, valor: op.valor });
  }
  if (u.vivo && !m.fim && u.pm > 0) {
    const c = melhorCasa(m, u);
    if (c && (c[0] !== u.x || c[1] !== u.y)) { mover(m, u, ...c); feitas.push({ t: "andar", para: c, posicao: true }); }
  }
  return feitas;
}

/** Joga a vez e passa a vez. */
export function jogarEPassar(m) {
  const f = jogarVez(m);
  if (!m.fim) encerrarVez(m);
  return f;
}

/** A melhor opção (andar + lançar) de agora, ou null se nenhuma vale a pena. */
export function melhorOpcao(m, u) {
  const casas = [...alcancaveis(m, u).values()];
  const prov = temEstado(u, "provocado"), provocador = prov && unidade(m, prov.fonte);
  let melhor = null;
  for (const id of Object.keys(u.kit)) {
    if (!podeLancar(m, u, id).ok) continue;
    const k = u.kit[id];
    for (const c of casas) {
      const alvos = alvosDe(m, u, id, k, c);
      for (const [tx, ty] of alvos) {
        const p = prever(m, u.id, id, tx, ty, [c.x, c.y]);
        if (!p) continue;
        if (provocador && provocador.vivo && ofensiva(k) && !p.mud.some((d) => d.id === provocador.id && d.dPv < 0)) continue;
        const v = valorPrevia(m, u, p, k) + 0.35 * valorCasa(m, u, c.x, c.y, p.luta) - 0.4 * c.custo;
        if (!melhor || v > melhor.valor) melhor = { valor: v, hab: id, alvo: [tx, ty], casa: [c.x, c.y] };
      }
    }
  }
  return melhor && melhor.valor > 2 ? melhor : null;
}

const ofensiva = (k) => k.alvo === "inimigo" || k.efeitos.some((e) => e.t === "dano");

// Os alvos de uma habilidade a partir de outra casa (move o combatente na cópia de consulta e volta).
function alvosDe(m, u, id, k, c) {
  const ox = u.x, oy = u.y;
  u.x = c.x; u.y = c.y;
  let res = alvosValidos(m, u, id);
  u.x = ox; u.y = oy;
  // as áreas em casas vazias só valem perto de alguém (corta as contas inúteis)
  if (k.alvo === "casa" || k.alvo === "livre") {
    const todos = m.unidades.filter((w) => w.vivo);
    const r = (k.area && k.area.r) || 1;
    res = res.filter(([x, y]) => todos.some((w) => w !== u && dist(w.x, w.y, x, y) <= r + 1) || k.esp === "armadilha");
    if (k.esp === "armadilha") res = res.filter(([x, y]) => inimigosDe(m, u).some((w) => dist(w.x, w.y, x, y) <= 3));
    if (k.esp === "piscar") res = res.filter(([x, y]) => inimigosDe(m, u).every((w) => dist(w.x, w.y, x, y) >= 3));
  }
  return res;
}

/** O valor de uma prévia para quem age: dano nos outros, abates, estados, cura útil, sem ferir os seus. */
export function valorPrevia(m, u, p, k) {
  let v = 0;
  for (const d of p.mud) {
    const a = unidade(m, d.id), inimigo = a.lado !== u.lado;
    if (inimigo) {
      const peso = 1 + 0.4 * (1 - a.pv / a.pvMax) + (a.pvMax < 50 ? 0.15 : 0) + (u.foco === a.id ? 0.2 : 0);
      v += -d.dPv * peso;
      if (d.morre) v += 18 + a.pvMax * 0.15;
      for (const e of d.estados) v += VALOR_ESTADO[e] || 2;
      // empurrar um inimigo para longe de um aliado ferido, ou puxar para perto do nosso corpo a corpo
      if (d.para[0] !== d.de[0] || d.para[1] !== d.de[1]) v += 1.5;
    } else {
      v += d.dPv * (d.dPv < 0 ? 1.6 : 1.1);
      if (d.morre) v -= 40;
      for (const e of d.estados) {
        // proteções só valem para quem está ameaçado
        const ameacado = inimigosDe(m, a).some((w) => dist(w.x, w.y, a.x, a.y) <= w.pmMax + 2);
        if (e === "olhoAguia") v += 0.5;
        else v += (VALOR_ESTADO[e] || 2) * (ameacado ? 1 : 0.25);
      }
    }
  }
  // chão: fogo e veneno sob inimigos valem, sob aliados custam
  for (const [x, y] of p.chao) {
    const w = p.luta.unidades.find((z) => z.vivo && z.x === x && z.y === y);
    if (w) v += w.lado !== u.lado ? 3 : -4;
    else if (inimigosDe(m, u).some((z) => dist(z.x, z.y, x, y) <= 2)) v += 0.8;
  }
  // o golpe preparado: vale pelos inimigos nas casas marcadas (podem sair: 60%)
  if (p.preparo) for (const [x, y] of p.preparo) {
    const w = m.unidades.find((z) => z.vivo && z.x === x && z.y === y);
    if (w && w.lado !== u.lado) v += 10 * (temEstado(w, "imobilizado") ? 1 : 0.6);
  }
  // a armadilha: vale pela passagem provável (o inimigo mais perto vindo)
  if (k.esp === "armadilha") v += 4;
  return v;
}

/** O valor de estar na casa (x, y), pelo papel de quem age. */
export function valorCasa(m, u, x, y, luta = m) {
  const ins = inimigosDe(luta, u), ali = aliadosDe(luta, u).filter((w) => w.id !== u.id);
  if (!ins.length) return 0;
  const ds = ins.map((w) => dist(w.x, w.y, x, y)), perto = Math.min(...ds);
  const vizinhos = ds.filter((d) => d === 1).length;
  let v = 0;
  const ch = luta.chao[chave(x, y)];
  if (ch && ch.dono && unidade(luta, ch.dono) && unidade(luta, ch.dono).lado !== u.lado) v -= 8;
  else if (ch) v -= 4;
  for (const p of luta.preparos) {
    const dono = unidade(luta, p.dono);
    if (dono && dono.lado !== u.lado && p.celulas.some(([a, b]) => a === x && b === y)) v -= 14;
  }
  const papel = u.papel;
  if (papel === "perto" || papel === "pesado") {
    v -= 2 * perto;
    if (u.foco) { const f = unidade(luta, u.foco); if (f && f.vivo) v -= 0.8 * dist(f.x, f.y, x, y); }
    // o pesado fica entre os inimigos e quem atira de trás
    if (papel === "pesado") v += 0.5 * Math.min(3, vizinhos);
  } else {
    const ideal = papel === "apoio" ? 4 : 5;
    v -= 1.2 * Math.abs(perto - ideal);
    v -= 6 * vizinhos;
    const corpo = ins.filter((w) => (w.papel === "perto" || w.papel === "pesado") && dist(w.x, w.y, x, y) <= w.pmMax + 1).length;
    v -= 2.5 * corpo;
    // ter alguém a quem atirar dali na próxima vez
    const tiro = ins.some((w) => dist(w.x, w.y, x, y) <= 6 && visao(luta, x, y, w.x, w.y));
    if (tiro) v += 3;
    if (papel === "apoio" && ali.length) v -= 0.6 * Math.max(0, Math.min(...ali.map((w) => dist(w.x, w.y, x, y))) - 3);
  }
  return v;
}

/** A melhor casa para gastar os PM que sobraram. */
export function melhorCasa(m, u) {
  const casas = [...alcancaveis(m, u).values()];
  if (u.papel === "perto" || u.papel === "pesado") {
    // o caminho de verdade até o alvo (contorna obstáculos e os próprios aliados), não a distância em linha reta
    const campo = campoAte(m, u);
    let melhor = null;
    for (const c of casas) {
      const d = campo.get(chave(c.x, c.y)) ?? 99;
      const v = -3 * d + valorCasa(m, u, c.x, c.y) * 0.3 - 0.1 * c.custo;
      if (!melhor || v > melhor.v) melhor = { v, x: c.x, y: c.y };
    }
    return melhor && [melhor.x, melhor.y];
  }
  let melhor = null;
  for (const c of casas) {
    const v = valorCasa(m, u, c.x, c.y) - 0.15 * c.custo;
    if (!melhor || v > melhor.v) melhor = { v, x: c.x, y: c.y };
  }
  return melhor && [melhor.x, melhor.y];
}

// A distância a pé até ficar vizinho do alvo (o foco, ou o inimigo mais fraco ao alcance da vista). Os próprios
// aliados contam como passáveis com custo 3 (vão sair do caminho), para não travar atrás deles num corredor.
function campoAte(m, u) {
  const ins = inimigosDe(m, u);
  let alvo = u.foco && unidade(m, u.foco);
  const prov = temEstado(u, "provocado");
  if (prov && unidade(m, prov.fonte) && unidade(m, prov.fonte).vivo) alvo = unidade(m, prov.fonte);
  if (!alvo || !alvo.vivo) alvo = ins.sort((a, b) => (a.pv / a.pvMax) * 10 + dist(a.x, a.y, u.x, u.y) - ((b.pv / b.pvMax) * 10 + dist(b.x, b.y, u.x, u.y)))[0];
  const res = new Map(), fila = [];
  for (const [dx, dy] of VIZ) {
    const x = alvo.x + dx, y = alvo.y + dy;
    if (passavel(m, x, y)) { res.set(chave(x, y), 0); fila.push([x, y, 0]); }
  }
  while (fila.length) {
    fila.sort((a, b) => a[2] - b[2]);
    const [x, y, d] = fila.shift();
    if (res.get(chave(x, y)) < d) continue;
    for (const [dx, dy] of VIZ) {
      const nx = x + dx, ny = y + dy;
      if (!passavel(m, nx, ny)) continue;
      const w = m.unidades.find((z) => z.vivo && z.x === nx && z.y === ny);
      const passo = w && w !== u ? (w.lado === u.lado ? 3 : 6) : 1;
      const nd = d + passo;
      if (res.has(chave(nx, ny)) && res.get(chave(nx, ny)) <= nd) continue;
      res.set(chave(nx, ny), nd);
      fila.push([nx, ny, nd]);
    }
  }
  return res;
}

// usado nos testes: a casa vazia mais perto (para conferir que nada fica parado sem motivo)
export function temCasaLivreVizinha(m, u) { return VIZ.some(([dx, dy]) => livre(m, u.x + dx, u.y + dy)); }
export { alcanceDe };
