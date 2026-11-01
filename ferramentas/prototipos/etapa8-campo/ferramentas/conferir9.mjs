// Playwright, Campo Livre 9: abre a tela de verdade nas duas janelas de referência (1920 × 1080 e 1280 × 720) e confere a
// guerra nova: a escolha (a guerra como encontro inicial, as opções na chave própria, as variações explicadas); a guerra
// com o Guerreiro e com o Mago (as ondas, os heróis com as variações na barra e em cima da cabeça, a linha da guerra);
// o treino com os avisos de cada golpe em estágios (os anéis do Terremoto, a Cruz, o Leque de Vesna), o salto marcado
// no ar, a corrente do puxão, as cargas e os barris; a chegada do General, a vitória e o painel do fim com o sorteio; R
// (outro sorteio) e T (o mesmo); a seleção, as ordens e o comando com a câmera estável; o Campo Livre 8 em /v8/; nenhum
// erro no console. Para chegar rápido a cada cena, a simulação corre na própria página (o mesmo módulo que a tela usa)
// e os golpes são escolhidos à mão; a foto sai com a luta parada naquele instante (sem a tela de pausa). Capturas
// pontuais.
// Uso: PLAYWRIGHT_MODULO=file:///.../index.mjs node ferramentas/conferir9.mjs [porta] [pasta]
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const PORTA = process.argv[2] || "8801", SAIDA = process.argv[3] || "capturas";
const BASE = `http://127.0.0.1:${PORTA}/`;
const nav = await chromium.launch();
const falhas = [];
const ok = (c, msg) => { if (!c) falhas.push(msg); console.log(c ? "  ok " : "  FALHA ", msg); };
const r1 = (v) => Math.round(v * 10) / 10;

// as ajudas dentro da página: correr a simulação, derrubar quem entra, escolher o golpe do General ou de Vesna
const AJUDA = `window.__c9 = {
  async carregar() { this.S = await import("/sim.js"); this.R = await import("/robo.js"); this.C = await import("/campo9.js"); return true; },
  correr(seg, robo) {
    const m = __campo.mundo(), ent = this.S.entradaVazia(), r = this.r || (this.r = this.R.criarRobo({ nivel: "forte" })), fim = m.t + seg;
    while (m.t < fim && m.fase !== "fim") { if (robo) this.R.pensar(r, m, ent); this.S.passo(m, ent); m.eventos.length = 0; }
    return m.t;
  },
  ateGeneral() {
    const m = __campo.mundo();
    for (let i = 0; i < 20000 && !(m.g9.general.u); i++) {
      this.S.passo(m, this.S.entradaVazia());
      for (const u of m.lados[1]) if (!u.morto && !u.general && (u.heroi9 || m.g9.herois.every((e) => e.entrou))) this.S.ferir(m, u, 99999, m.heroi, {});
      m.eventos.length = 0;
    }
    return !!m.g9.general.u;
  },
  quem(tipo) { return __campo.mundo().lados[1].find((u) => !u.morto && u.tipo === tipo); },
  segurar(tipo) { const u = this.quem(tipo); u.h8.golpe = null; u.h8.fila = []; u.h8.pausa = 99; u.h8.investidaCd = 99; u.h8.rodopioCd = 99; u.h8.recuoCd = 99; u.h8.passo = null; },
  posicionar(tipo, dist, ang) {
    const m = __campo.mundo(), u = this.quem(tipo), h = m.heroi;
    h.x = h.px = u.x + Math.cos(ang) * dist; h.y = h.py = u.y + Math.sin(ang) * dist; h.vida = h.vidaMax;
  },
  forcar(tipo, id) { const u = this.quem(tipo); if (id === "salto") { u.h8.investidaCd = 0; } else { u.h8.fila = [id]; u.h8.pausa = 0; } },
};`;

async function preparar(p, url) {
  await p.goto(BASE + url, { waitUntil: "networkidle" });
  await p.evaluate(AJUDA);
  await p.evaluate(() => window.__c9.carregar());
}
const parar = (p) => p.evaluate(() => { window.__campo.st.pausado = true; });
const seguir = (p) => p.evaluate(() => { window.__campo.st.pausado = false; });
async function foto(p, nome) { await p.waitForTimeout(80); await p.screenshot({ path: `${SAIDA}/${nome}.png` }); }
// espera o golpe `id` de `tipo` chegar no ponto pedido (`etapa`, a fração da preparação ou o estágio) e para a luta
async function ateGolpe(p, tipo, id, quando) {
  try {
    await p.waitForFunction(([tipo, id, q]) => {
      const u = window.__c9.quem(tipo), g = u && u.h8.golpe;
      if (!g || g.id !== id) return false;
      if (q.estagio != null) return g.etapa === "exec" && g.estagio === q.estagio;
      if (q.voando) return g.etapa === "exec" && u.voando;
      return g.etapa === "preparo" && g.t <= g.preparo * (1 - q.fracao);
    }, [tipo, id, quando], { polling: "raf", timeout: 8000 });
  } catch { return false; }
  await parar(p);
  return true;
}

for (const [w, h] of [[1920, 1080], [1280, 720]]) {
  const p = await nav.newPage({ viewport: { width: w, height: h } });
  const erros = [];
  p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
  p.on("pageerror", (e) => erros.push("pageerror: " + e.message));
  console.log(`== ${w}×${h}`);
  // ---- a escolha: a guerra como encontro inicial, as opções na chave do 9 (as do 8 não entram)
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.evaluate(() => { localStorage.clear(); localStorage.setItem("campo-livre-8-opcoes", JSON.stringify({ encontro: "duelo", heroi: "mago", tremor: 0 })); });
  await p.goto(BASE, { waitUntil: "networkidle" });
  const ini = await p.evaluate(() => ({ titulo: document.title, encontros: document.querySelectorAll("#encontros .encontro").length,
    escolhido: document.querySelector(".encontro.escolhido").dataset.enc, heroi: window.__campo.opcoes.heroi, tremor: window.__campo.opcoes.tremor,
    variacoes: document.querySelectorAll("#enc-info .vars9 > span").length, v8: !!document.querySelector('a[href="/v8/"]') }));
  ok(ini.titulo.startsWith("Campo Livre 9") && ini.escolhido === "guerra9" && ini.heroi === "guerreiro" && ini.tremor === 150 && ini.variacoes === 6 && ini.v8,
    `a escolha: a guerra começa escolhida, as opções do 8 não entram, as seis variações explicadas ${JSON.stringify(ini)}`);
  await foto(p, `cl9-escolha-${w}`);
  await p.evaluate(() => { const c = window.__campo; c.opcoes.encontro = "guerra9"; localStorage.setItem("campo-livre-9-opcoes", JSON.stringify(c.opcoes)); });

  // ---- a guerra com o Guerreiro: as ondas, o primeiro herói com a variação, a linha da guerra
  await preparar(p, "?enc=guerra9&auto=1&robo=1&sorteio=4");
  await p.evaluate(() => window.__c9.correr(21.5, true));
  await p.waitForTimeout(1200);
  const g1 = await p.evaluate(() => ({ chefe: !document.querySelector("#chefe").hidden, nome: document.querySelector("#chefe b").textContent,
    vars: document.querySelectorAll("#chefe .var9").length, linha: document.querySelector("#p-guerra").textContent, selo: document.querySelector("#selo").textContent,
    pelotoes: window.__campo.mundo().g9.pelotoes.length }));
  ok(g1.chefe && g1.vars >= 1 && /Ondas \d de 8/.test(g1.linha) && /guerra nº 4/.test(g1.selo) && g1.pelotoes >= 2,
    `a guerra: ${g1.nome} na barra com ${g1.vars} variação, "${g1.linha}", "${g1.selo}"`);
  await parar(p); await foto(p, `cl9-guerra-heroi-${w}`); await seguir(p);
  // o terceiro herói, com duas variações
  await p.evaluate(() => window.__c9.correr(52, true));
  await p.waitForTimeout(1000);
  const g3 = await p.evaluate(() => ({ vars: Math.max(...[...document.querySelectorAll("#chefe .vars, #chefe2 .vars")].map((v) => v.children.length)), t: window.__campo.mundo().t }));
  ok(g3.vars === 2, `o terceiro herói com duas variações na barra (aos ${r1(g3.t)} s)`);
  if (w === 1920) { await parar(p); await foto(p, `cl9-guerra-duas-variacoes-${w}`); await seguir(p); }
  // o campo vazio: o General vem; derrubado, a vitória e o painel do fim
  const veio = await p.evaluate(() => window.__c9.ateGeneral());
  await p.waitForTimeout(1500);
  const gv = await p.evaluate(() => ({ chefe: document.querySelector("#chefe b").textContent, geral: document.querySelector("#chefe").classList.contains("general"),
    linha: document.querySelector("#p-guerra").textContent, gerados: window.__campo.mundo().unidades.filter((u) => u.general).length }));
  ok(veio && gv.geral && gv.gerados === 1 && /General/.test(gv.linha), `o General veio uma vez: "${gv.chefe}", "${gv.linha}"`);
  await parar(p); await foto(p, `cl9-guerra-general-${w}`); await seguir(p);
  await p.evaluate(() => { const m = window.__campo.mundo(); window.__c9.S.ferir(m, m.g9.general.u, 99999, m.heroi, {}); });
  await p.waitForTimeout(4200);
  const fim = await p.evaluate(() => ({ tela: window.__campo.st.tela, titulo: document.querySelector("#fim-titulo").textContent,
    painel: document.querySelector("#fim-guerra").textContent, repetir: !document.querySelector("#tela-fim [data-repetir]").hidden,
    vitorias: window.__campo.mundo().registro.filter((r) => r.texto === "Vitória.").length }));
  ok(fim.tela === "fim" && /General caiu/.test(fim.titulo) && /Guerra nº 4/.test(fim.painel) && fim.repetir && fim.vitorias === 1,
    `a vitória uma vez e o fim com o sorteio: "${fim.titulo}", repetir à vista`);
  await foto(p, `cl9-fim-${w}`);
  // R: outro sorteio; T: o mesmo
  await p.keyboard.press("t"); await p.waitForTimeout(300);
  const s1 = await p.evaluate(() => window.__campo.mundo().g9.sorteio);
  await p.keyboard.press("r"); await p.waitForTimeout(300);
  const s2 = await p.evaluate(() => window.__campo.mundo().g9.sorteio);
  await p.keyboard.press("t"); await p.waitForTimeout(300);
  const s3 = await p.evaluate(() => ({ s: window.__campo.mundo().g9.sorteio, ordem: window.__campo.mundo().g9.herois.map((e) => e.id + e.variacoes.join("+")).join(",") }));
  ok(s1 === 4 && s2 !== 4 && s3.s === s2, `T repete (4 → ${s1}); R sorteia outra (${s2}); T repete essa (${s3.s})`);
  // a pausa com o painel da guerra
  await p.keyboard.press("p"); await p.waitForTimeout(200);
  const pz = await p.evaluate(() => ({ painel: !document.querySelector("#pausa-guerra").hidden && /Guerra nº/.test(document.querySelector("#pausa-guerra").textContent) }));
  ok(pz.painel, "a pausa mostra a guerra sorteada");
  if (w === 1920) await foto(p, `cl9-pausa-${w}`);
  await p.keyboard.press("p");
  // sem regressão: a seleção por tipo, o comando com a câmera estável
  await p.evaluate(() => window.__c9.correr(4, false));
  await p.keyboard.press("F1"); await p.waitForTimeout(120);
  const sel = await p.textContent("#p-selecao");
  await p.keyboard.press("2"); await p.waitForTimeout(120);
  const ordens = await p.textContent("#p-ordens");
  await p.keyboard.press("x");
  // no comando, o mouse não desloca o olhar da câmera (o herói pode estar andando: mede-se o olhar, não a câmera)
  const rel = () => p.evaluate(() => ({ ...window.__campo.st.olhar }));
  await p.keyboard.down("Shift"); await p.waitForTimeout(600);
  const c1 = await rel(); await p.mouse.move(w * 0.9, h * 0.2); await p.waitForTimeout(500);
  const c2 = await rel(); const modo = await p.textContent("#modo");
  await p.keyboard.up("Shift");
  ok(/Seleção: \d+/.test(sel) && /Atacar/.test(ordens) && /Comando/.test(modo) && Math.hypot(c2.x - c1.x, c2.y - c1.y) < 3,
    `seleção (${sel.trim().slice(0, 30)}), a ordem ("${ordens.trim().slice(0, 40)}") e o comando ("${modo.trim().slice(0, 20)}") com a câmera estável (${r1(Math.hypot(c2.x - c1.x, c2.y - c1.y))} px)`);
  const d = await p.evaluate(() => window.__campo.diagnostico());
  ok(d.fps >= 50, `a guerra 1×: ${r1(d.fps)} qps, simulação ${r1(d.simMedio)} ms, desenho ${r1(d.desenhoMedio)} ms (p95 ${r1(d.desenhoP95)}), ${d.unidades} unidades`);

  // ---- a guerra com o Mago
  await preparar(p, "?enc=guerra9&heroi=mago&auto=1&robo=1&sorteio=7");
  await p.evaluate(() => window.__c9.correr(22, true));
  await p.waitForTimeout(1500);
  const mg = await p.evaluate(() => ({ heroi: window.__campo.mundo().nomeHeroi, chefe: !document.querySelector("#chefe").hidden, vivo: !window.__campo.mundo().heroi.morto }));
  ok(mg.heroi === "mago" && mg.chefe && mg.vivo, `a guerra com o Mago (${JSON.stringify(mg)})`);
  if (w === 1920) { await parar(p); await foto(p, `cl9-guerra-mago-${w}`); }

  // ---- as cargas: o barril aceso (fere os nossos), o barril caído (fere qualquer lado), o rastro
  await preparar(p, "?enc=guerra9&auto=1&sorteio=4");
  await p.waitForTimeout(600);
  await p.evaluate(() => {
    const m = window.__campo.mundo(), h = m.heroi, c = (x, y, raio, t, dur, alvo, extra) => ({ x, y, raio, t, dur, dano: 1, danoHeroi: 1, emp: 0, atord: 0, alvo, fonte: h, ...extra });
    m.g9.cargas.push(c(h.x + 50, h.y - 30, 30, 0.5, 0.9, 0, { barril: true }), c(h.x + 50, h.y + 40, 30, 0.1, 0.45, "todos", { barril: true, caido: true }),
      c(h.x - 40, h.y + 10, 16, 0.4, 0.8, 0), c(h.x - 20, h.y + 22, 16, 0.2, 0.8, 0));
    window.__campo.st.pausado = true;
  });
  await foto(p, `cl9-cargas-${w}`);
  const cg = await p.evaluate(() => {
    // o pixel no meio do barril caído e um ponto fora: a área aparece pintada onde a regra fere
    return window.__campo.mundo().g9.cargas.length;
  });
  ok(cg === 4, "as cargas no chão (o barril aceso, o caído com a borda listrada, o rastro)");

  // ---- o treino: Vesna e o Leque; o General e os golpes em estágios, o salto, a corrente
  await preparar(p, "?enc=treino9&auto=1&sorteio=1");
  await p.waitForFunction(() => !!window.__c9.quem("vesna"), null, { timeout: 8000 });
  await p.evaluate(() => { window.__c9.segurar("vesna"); window.__c9.posicionar("vesna", 90, Math.PI); });
  await p.waitForTimeout(900);
  await p.evaluate(() => window.__c9.forcar("vesna", "leque"));
  ok(await ateGolpe(p, "vesna", "leque", { fracao: 0.5 }), "o Leque de Facas de Vesna: as três faixas no chão");
  await foto(p, `cl9-leque-${w}`);
  await seguir(p);
  await p.evaluate(() => window.__c9.ateGeneral());
  const cenas = [["terremoto", 80, { fracao: 0.6 }, "terremoto"], ["terremoto", 80, { estagio: 1 }, "terremoto-segundo-anel"],
    ["cruz", 70, { fracao: 0.6 }, "cruz"], ["salto", 200, { voando: true }, "salto-no-ar"], ["correntes", 110, { fracao: 0.6 }, "correntes"]];
  for (const [id, dist, quando, nome] of cenas) {
    if (w === 1280 && !["terremoto", "cruz"].includes(nome)) continue;
    await seguir(p);
    await p.evaluate(([id, dist]) => {
      const c = window.__c9, g = c.quem("general");
      c.segurar("general"); c.posicionar("general", dist, Math.PI * 0.85);
      if (id === "cruz") g.h8.fase = 2;
    }, [id, dist]);
    await p.waitForTimeout(800);
    await p.evaluate((id) => window.__c9.forcar("general", id), id);
    const viu = await ateGolpe(p, "general", id, quando);
    const forma = await p.evaluate(() => { const g = window.__c9.quem("general").h8.golpe; return g ? (g.formasEstagio ? g.formasEstagio.map((f) => f.length).join("+") : g.forma.tipo) : "-"; });
    ok(viu, `o aviso: ${nome} (${forma})`);
    await foto(p, `cl9-${nome}-${w}`);
  }
  if (w === 1920) {
    // a corrente: o puxão prende e a corrente fica à vista
    await seguir(p);
    const puxou = await p.waitForFunction(() => window.__campo.efeitos().correntes.length > 0, null, { polling: "raf", timeout: 4000 }).then(() => true, () => false);
    await parar(p);
    ok(puxou, "a corrente do puxão, dele até você");
    await foto(p, `cl9-corrente-${w}`);
  }

  // ---- o Campo Livre 8 em /v8/
  await p.goto(BASE + "v8/", { waitUntil: "networkidle" });
  const v8 = await p.evaluate(() => document.title);
  ok(v8.startsWith("Campo Livre 8"), `o Campo Livre 8 abre em /v8/ (${v8})`);
  ok(!erros.length, `sem erros no console ${erros.slice(0, 3).join(" | ")}`);
  await p.close();
}
await nav.close();
console.log(falhas.length ? `${falhas.length} FALHAS` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
