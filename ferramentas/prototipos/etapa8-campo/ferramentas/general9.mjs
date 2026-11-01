// O General do Campo Livre 9 golpe a golpe, com o jogador automático: para cada golpe, a distância em que começou, se
// acertou você e se havia saída. "A pé": existe um caminho que, partindo de onde você estava quando o aviso apareceu,
// depois de `reação` s (0,25: uma pessoa atenta), na sua velocidade (com a lentidão do momento), fica fora de cada forma
// no instante em que ela estoura (os estágios do Terremoto e da Cruz, um depois do outro). "Com a mobilidade": a
// mobilidade estava pronta e, com ela, havia saída (o salto dela num dos intervalos; num golpe de um estágio só, a
// invulnerabilidade dela, bem cronometrada, também serve). O cálculo é uma grade de 2 px com a distância em 8 direções
// (até 8% otimista nas diagonais); paredes e corpos não entram. Compara o que o robô fez com o que dava para fazer.
// Uso: node ferramentas/general9.mjs [heróis] [níveis] [sorteios] [reação] [montagem pronta]
//      node ferramentas/general9.mjs guerreiro,mago forte 1,2,3,4 0.25
//      node ferramentas/general9.mjs mago forte 1,2,3,4,5,6 0.25 "Fogo em cadeia"
const T = new URL("../tela/", import.meta.url).href;
const S = await import(T + "sim.js"), R = await import(T + "robo.js"), C = await import(T + "conteudo.js");
const [heroiArg = "guerreiro,mago", nivelArg = "forte", sortArg = "1,2,3,4", reacaoArg = "0.25", montagemArg = ""] = process.argv.slice(2);
const REACAO = Number(reacaoArg), G = C.GENERAL9.golpes, PASSO = 2;

// os pontos (na grade) que dá para ocupar no instante de cada estágio; vazio no fim: não havia saída
function saida(h0, v, inicio, estagios, salto = 0) {
  const tFim = estagios[estagios.length - 1].t, alc = v * Math.max(0, tFim - inicio) + salto + 4;
  const n = Math.ceil((2 * alc) / PASSO) + 1, ox = h0.x - alc, oy = h0.y - alc, idx = (i, j) => j * n + i;
  // duas camadas: a mobilidade ainda não usada (a) e já usada (b); o valor é a distância andada que sobrou
  let a = new Float32Array(n * n).fill(-1), b = new Float32Array(n * n).fill(-1);
  const i0 = Math.round((h0.x - ox) / PASSO), j0 = Math.round((h0.y - oy) / PASSO);
  let t = inicio;
  a[idx(i0, j0)] = 0;
  const espalhar = (camada, d) => {
    // a distância de cada ponto ao conjunto (duas passadas, 8 direções), mantendo quem fica a até `d`
    const dist = new Float32Array(n * n).fill(Infinity);
    for (let k = 0; k < n * n; k++) if (camada[k] >= 0) dist[k] = 0;
    const D = Math.SQRT2 * PASSO;
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      let q = dist[idx(i, j)];
      if (i > 0) q = Math.min(q, dist[idx(i - 1, j)] + PASSO);
      if (j > 0) { q = Math.min(q, dist[idx(i, j - 1)] + PASSO); if (i > 0) q = Math.min(q, dist[idx(i - 1, j - 1)] + D); if (i < n - 1) q = Math.min(q, dist[idx(i + 1, j - 1)] + D); }
      dist[idx(i, j)] = q;
    }
    for (let j = n - 1; j >= 0; j--) for (let i = n - 1; i >= 0; i--) {
      let q = dist[idx(i, j)];
      if (i < n - 1) q = Math.min(q, dist[idx(i + 1, j)] + PASSO);
      if (j < n - 1) { q = Math.min(q, dist[idx(i, j + 1)] + PASSO); if (i < n - 1) q = Math.min(q, dist[idx(i + 1, j + 1)] + D); if (i > 0) q = Math.min(q, dist[idx(i - 1, j + 1)] + D); }
      dist[idx(i, j)] = q;
    }
    return dist;
  };
  for (const e of estagios) {
    const dt = Math.max(0, e.t - t);
    t = e.t;
    const da = espalhar(a, v * dt), db = espalhar(b, v * dt);
    const na = new Float32Array(n * n).fill(-1), nb = new Float32Array(n * n).fill(-1);
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      const k = idx(i, j), x = ox + i * PASSO, y = oy + j * PASSO;
      if (e.formas.some((f) => S.dentro(f, x, y))) continue;
      if (da[k] <= v * dt) na[k] = 0;
      if (db[k] <= v * dt || salto && da[k] <= v * dt + salto) nb[k] = 0;
    }
    a = na; b = nb;
  }
  return { pe: a.some((q) => q >= 0), mob: b.some((q) => q >= 0) || a.some((q) => q >= 0) };
}

// A tabela (node ferramentas/general9.mjs tabela [reação]): cada golpe dos heróis da guerra e do General, sem robô. Ele
// na origem, virado para a direita; você parado na frente dele, colado (os dois corpos encostados) e na distância em que
// ele começa o golpe; o aviso aparece em t = 0 e você reage depois de `reação` s. Mirado em você (o pior caso).
// O salto: o centro segue você durante a parte de mira e fica onde você estava nesse instante.
if (heroiArg === "tabela") {
  const reacao = Number(nivelArg === "forte" ? 0.25 : nivelArg), H = C.HEROIS;
  const GRAUS = Math.PI / 180;
  const formas = (g, ox) => {
    // as formas do golpe com ele em (0, 0), na direção 0 (as mesmas contas de campo8.js)
    const a = g.dash ? 0 : g.avanco || 0;
    if (g.estagios) return g.estagios.map((e, j) => ({ dt: j * g.intervalo, formas: e.formas.flatMap((f) => {
      const angs = f.forma === "cruz" ? [0, 90, 180, 270].map((k) => (k + (f.ang || 0)) * GRAUS) : [(f.ang || 0) * GRAUS];
      return angs.map((an) => f.forma === "anel" ? { tipo: "anel", x: 0, y: 0, r0: f.r0, raio: f.raio }
        : { tipo: "faixa", x1: 0, y1: 0, x2: Math.cos(an) * f.alcance, y2: Math.sin(an) * f.alcance, largura: f.largura });
    }) }));
    if (g.salto) return [{ dt: 0, formas: [{ tipo: "circulo", x: ox, y: 0, raio: g.raio }] }];
    if (g.forma === "arco") return [{ dt: 0, formas: [{ tipo: "arco", x: a, y: 0, raio: g.raio, ang: 0, abertura: g.abertura }] }];
    if (g.forma === "circulo") return [{ dt: 0, formas: [{ tipo: "circulo", x: a + g.distancia, y: 0, raio: g.raio }] }];
    return [{ dt: 0, formas: [{ tipo: "faixa", x1: a, y1: 0, x2: a + (g.alcance || 0), y2: 0, largura: g.largura }] }];
  };
  console.log(`Cada golpe mirado em você, parado; reação ${reacao} s. "a pé": há saída andando; "mob": só com a mobilidade.`);
  console.log("quem      golpe              estoura (s)   colado: Guerreiro/Mago   na distância de início: Guerreiro/Mago");
  for (const [quem, cfg, raioU] of [["Harg", C.HARG9, 6.5], ["Vesna", C.VESNA9, 4.5], ["General", C.GENERAL9, 9]]) {
    for (const [id, g] of Object.entries(cfg.golpes)) {
      if (!g.danoHeroi || id === "rugido" || id === "brado") continue;
      const t0 = g.preparo + (g.dash ? 0 : g.salto ? g.exec : g.estagios ? 0 : g.exec);
      const inicio = g.salto ? Math.max(reacao, g.preparo * g.rastreia) : reacao;
      const alcIni = g.dash || g.salto ? g.min : g.alcanceIA ?? (g.raio || 0) + (g.avanco || 0) + (g.distancia || 0);
      const res = [];
      for (const d of [raioU + 5, Math.max(raioU + 5, alcIni)]) for (const heroi of ["guerreiro", "mago"]) {
        // a investida chega até você depois de correr a distância (a faixa estoura ao passar)
        const est = formas(g, d).map((e) => ({ t: t0 + e.dt + (g.dash ? Math.max(0, d - raioU) / g.vel : 0), formas: e.formas }));
        if (est.every((e) => !e.formas.some((f) => S.dentro(f, d, 0)))) { res.push("fora"); continue; }
        res.push(saida({ x: d, y: 0 }, H[heroi].vel, inicio, est).pe ? "a pé" : "mob");
      }
      const tempos = formas(g, 0).map((e) => (t0 + e.dt).toFixed(2).replace(".", ",")).join(" / ");
      console.log(`${quem.padEnd(9)} ${g.nome.padEnd(18)} ${tempos.padEnd(13)} ${(res[0] + "/" + res[1]).padEnd(24)} ${res[2]}/${res[3]} (a ${Math.round(Math.max(raioU + 5, alcIni))} px)`);
    }
  }
  process.exit(0);
}

for (const heroi of heroiArg.split(",")) for (const nivel of nivelArg.split(",")) {
  const porGolpe = {};
  let vitorias = 0, total = 0;
  const linhas = [];
  for (const sort of sortArg.split(",").map(Number)) {
    const kit = montagemArg ? structuredClone(C.MONTAGENS[heroi][montagemArg]) : {};
    const m = S.criarMundo({ heroi, encontro: "treino9", sorteio: sort, kit });
    const rb = R.criarRobo({ nivel }), ent = S.entradaVazia(), h = m.heroi;
    const abertos = new Map(), feitos = [];
    let gen = null, dano = 0;
    while (m.fase !== "fim" && m.t < 400) {
      R.pensar(rb, m, ent); S.passo(m, ent);
      for (const e of m.eventos) {
        if (e.tipo === "general9Entra") gen = m.unidades.find((u) => u.id === e.id);
        if (!gen || e.id !== gen.id && e.tipo !== "heroiAtingido") continue;
        if (e.tipo === "aviso") abertos.set(e.h8, { id: e.h8, t0: m.t, d0: Math.hypot(h.x - gen.x, h.y - gen.y), h0: { x: h.x, y: h.y },
          v: h.def.vel * (h.lentoAte > m.t ? 1 - h.lentoF : 1), preso: Math.max(h.atordoado || 0, (h.imobAte || 0) - m.t, 0),
          mobPronta: h.cds[h.slots.mobilidade] <= 0, acertou: 0 });
        if (e.tipo === "hargExec") { const a = abertos.get(e.golpe); if (a) { const gp = gen.h8.golpe, g = G[e.golpe];
          a.estagios = gp.formasEstagio ? gp.formasEstagio.map((f, j) => ({ t: m.t + j * g.intervalo, formas: f }))
            : [{ t: m.t + (g.dash ? 0 : g.exec), formas: [gp.forma] }]; } }
      }
      for (const e of m.eventos) if (e.tipo === "heroiAtingido" && gen && e.fonteId === gen.id && e.hab) {
        const a = abertos.get(e.hab.replace("harg-", "")); if (a) a.acertou += e.valor;
        dano += e.valor;
      }
      m.eventos.length = 0;
      // fecha os golpes que acabaram (o General voltou a decidir ou começou outro)
      for (const [id, a] of abertos) if (a.estagios && (!gen.h8.golpe || gen.h8.golpe.id !== id || gen.h8.golpe.etapa === "rec")) { feitos.push(a); abertos.delete(id); }
    }
    total++;
    if (m.resultado === "vitoria") vitorias++;
    for (const a of feitos) {
      const inicio = a.t0 + Math.max(REACAO, a.preso), sx = saida(a.h0, a.v, inicio, a.estagios, a.mobPronta ? C.HABILIDADES[heroi][h.slots.mobilidade].distancia : 0);
      const um = a.estagios.length === 1, pe = sx.pe, mob = a.mobPronta && (um || sx.mob);
      const p = porGolpe[a.id] || (porGolpe[a.id] = { n: 0, acertos: 0, dano: 0, pe: 0, mob: 0, acertouComSaida: 0, semSaida: 0, d: [] });
      p.n++; p.d.push(a.d0);
      if (pe) p.pe++;
      if (pe || mob) p.mob++;
      if (a.acertou) { p.acertos++; p.dano += a.acertou; if (pe || mob) p.acertouComSaida++; else p.semSaida++; }
    }
    linhas.push(`  sorteio ${sort}: ${m.resultado}, General ${gen ? `${Math.round(Math.max(0, gen.vida))}/${gen.vidaMax}` : "não veio"}, dano dele em você ${Math.round(dano)}`);
  }
  console.log(`${heroi} ${nivel}${montagemArg ? ` (${montagemArg})` : ""}, reação ${REACAO} s: ${vitorias}/${total} vitórias`);
  for (const l of linhas) console.log(l);
  console.log("  golpe            vezes  distância (mediana)  acertou  dano   saída a pé  saída com mobilidade  acertou com saída  acertou sem saída");
  for (const [id, p] of Object.entries(porGolpe)) {
    const med = p.d.sort((x, y) => x - y)[Math.floor(p.d.length / 2)];
    console.log(`  ${id.padEnd(16)} ${String(p.n).padStart(5)}  ${String(Math.round(med)).padStart(19)}  ${String(p.acertos).padStart(7)}  ${String(Math.round(p.dano)).padStart(4)}   ${String(p.pe).padStart(10)}  ${String(p.mob).padStart(20)}  ${String(p.acertouComSaida).padStart(17)}  ${String(p.semSaida).padStart(17)}`);
  }
}
