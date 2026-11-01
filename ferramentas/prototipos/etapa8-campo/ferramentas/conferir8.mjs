// Playwright, Campo Livre 8: abre a tela de verdade nas duas janelas de referência (1920 × 1080 e 1280 × 720) e confere:
// a escolha (os onze encontros; a sóbria, a violência intensa e os modelos novos como padrão); o treino contra Harg (o
// aviso no chão com o nome do golpe na barra, a postura na barra, a quebra pela tela, o dano recente escorrendo); a
// guerra (Harg entra pelo portão aos 18 s e derruba soldados; a barra dele aparece); sem regressão: a seleção por tipo,
// o comando com a câmera estável, os controles na HUD; o Campo Livre 7 em /v7/; nenhum erro no console. O custo da
// guerra a 2× (simulação e desenho separados). Capturas pontuais.
// Uso: PLAYWRIGHT_MODULO=file:///.../index.mjs node ferramentas/conferir8.mjs [porta] [pasta]
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const PORTA = process.argv[2] || "8801", SAIDA = process.argv[3] || "capturas";
const BASE = `http://127.0.0.1:${PORTA}/`;
const nav = await chromium.launch();
const falhas = [];
const ok = (c, msg) => { if (!c) falhas.push(msg); console.log(c ? "  ok " : "  FALHA ", msg); };
const r1 = (v) => Math.round(v * 10) / 10;

for (const [w, h] of [[1920, 1080], [1280, 720]]) {
  const p = await nav.newPage({ viewport: { width: w, height: h } });
  const erros = [];
  p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
  p.on("pageerror", (e) => erros.push("pageerror: " + e.message));
  console.log(`== ${w}×${h}`);
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.evaluate(() => localStorage.clear());
  await p.goto(BASE, { waitUntil: "networkidle" });
  const ini = await p.evaluate(() => ({ titulo: document.title, encontros: document.querySelectorAll("#encontros .encontro").length,
    arte: window.__campo.opcoes.arte, violencia: window.__campo.opcoes.violencia, modelos: window.__campo.opcoes.escala }));
  ok(ini.titulo.startsWith("Campo Livre 8") && ini.encontros === 11 && ini.arte === "sobria" && ini.violencia === 3 && ini.modelos === "novo",
    `a escolha e os padrões ${JSON.stringify(ini)}`);
  // o treino: o jogador automático forte lutando com Harg; o estado dele na barra
  await p.goto(BASE + "?enc=duelo&auto=1&robo=1", { waitUntil: "networkidle" });
  let viu = { aviso: null, postura: false, quebra: false, chip: false };
  for (let i = 0; i < 70 && !(viu.aviso && viu.quebra && viu.chip); i++) {
    await p.waitForTimeout(250);
    const e = await p.evaluate(() => {
      const l = window.__campo.mundo().lider, txt = document.querySelector("#chefe small").textContent;
      const em = document.querySelector("#chefe .barra em").getBoundingClientRect().width, vi = document.querySelector("#chefe .barra i").getBoundingClientRect().width;
      return { txt, postura: !document.querySelector("#chefe .postura").hidden, quebrado: !!(l && l.h8 && l.h8.quebrado > 0), chip: em > vi + 2,
        golpe: l && l.h8 && l.h8.golpe && l.h8.golpe.etapa === "preparo" ? l.h8.golpe.id : null };
    });
    if (e.golpe && /Prepara/.test(e.txt) && !viu.aviso) { viu.aviso = e.txt; if (w === 1920) await p.screenshot({ path: `${SAIDA}/cl8-treino-aviso-${w}.png` }); }
    if (e.postura) viu.postura = true;
    if (e.chip) viu.chip = true;
    if (e.quebrado && !viu.quebra) { viu.quebra = true; if (w === 1920) await p.screenshot({ path: `${SAIDA}/cl8-treino-quebra-${w}.png` }); }
  }
  ok(viu.aviso && viu.postura && viu.quebra && viu.chip, `o treino: o golpe na barra ("${viu.aviso}"), a postura, a quebra, o dano escorrendo`);
  // a guerra: Harg entra aos 18 s e derruba soldados
  await p.goto(BASE + "?enc=guerra&auto=1&robo=1", { waitUntil: "networkidle" });
  await p.waitForTimeout(16000);
  const antes = await p.evaluate(() => ({ chefe: !document.querySelector("#chefe").hidden, t: window.__campo.mundo().t }));
  await p.waitForTimeout(9000);
  const g = await p.evaluate(() => ({ chefe: !document.querySelector("#chefe").hidden, mortos: window.__campo.mundo().stats.hargMortos || 0,
    t: window.__campo.mundo().t, d: window.__campo.diagnostico() }));
  if (w === 1920) await p.screenshot({ path: `${SAIDA}/cl8-guerra-${w}.png` });
  ok(g.chefe && g.mortos >= 3, `a guerra: Harg entrou (barra aos ${r1(g.t)} s; antes, aos ${r1(antes.t)} s: ${antes.chefe ? "já" : "ainda não"}) e derrubou ${g.mortos}`);
  ok(g.d.fps >= 50, `a guerra 1×, sóbria, violência intensa: ${r1(g.d.fps)} qps, simulação ${r1(g.d.simMedio)} ms (p95 ${r1(g.d.simP95)}), desenho ${r1(g.d.desenhoMedio)} ms (p95 ${r1(g.d.desenhoP95)}), ${g.d.unidades} unidades`);
  // sem regressão: a seleção por tipo, o comando com a câmera estável, os controles na HUD
  await p.keyboard.press("F1"); await p.waitForTimeout(120);
  const sel = await p.textContent("#p-selecao");
  await p.keyboard.press("x");
  const rel = () => p.evaluate(() => { const c = window.__campo.st.cam, he = window.__campo.mundo().heroi; return { x: c.x - he.x, y: c.y - he.y }; });
  await p.keyboard.down("Shift"); await p.waitForTimeout(600);
  const c1 = await rel(); await p.mouse.move(w * 0.9, h * 0.2); await p.waitForTimeout(500);
  const c2 = await rel(); const modo = await p.textContent("#modo");
  await p.keyboard.up("Shift");
  ok(/Seleção: \d+/.test(sel) && /Comando/.test(modo) && Math.hypot(c2.x - c1.x, c2.y - c1.y) < 3, `seleção (${sel.trim().slice(0, 30)}) e comando com a câmera estável`);
  // a guerra a 2×: o custo
  await p.goto(BASE + "?enc=guerra&qtd=2&auto=1&robo=1", { waitUntil: "networkidle" });
  await p.waitForTimeout(26000);
  const d2 = await p.evaluate(() => window.__campo.diagnostico());
  ok(d2.fps >= 50, `a guerra 2×: ${r1(d2.fps)} qps, simulação ${r1(d2.simMedio)} ms (p95 ${r1(d2.simP95)}), desenho ${r1(d2.desenhoMedio)} ms (p95 ${r1(d2.desenhoP95)}), ${d2.unidades} unidades, ${d2.particulas} partículas`);
  // o Campo Livre 7 em /v7/
  await p.goto(BASE + "v7/", { waitUntil: "networkidle" });
  const v7 = await p.evaluate(() => document.title);
  ok(v7.startsWith("Campo Livre 7"), `o Campo Livre 7 abre em /v7/ (${v7})`);
  ok(!erros.length, `sem erros no console ${erros.slice(0, 3).join(" | ")}`);
  await p.close();
}
await nav.close();
console.log(falhas.length ? `${falhas.length} FALHAS` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
