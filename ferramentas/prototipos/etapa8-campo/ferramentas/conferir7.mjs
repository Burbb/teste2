// Playwright, Campo Livre 7: abre a tela de verdade e confere, nas duas janelas de referência (1920 × 1080 e 1280 ×
// 720): a escolha monta (os nove encontros, as opções de aparência, escala e violência); a seleção por tipo e o modo de
// comando continuam (sem regressão); a amostra do portão roda e troca de aparência e de escala pelas teclas (F8, F9, V)
// no meio da luta; a provocação e os controles aparecem na HUD com o texto do motor; o Campo Livre 6 abre em /v6/;
// nenhum erro no console. Mede o custo (simulação e desenho, separados) na vila a 2× com a aparência sombria e a
// violência intensa. Capturas pontuais: a amostra nas três aparências no mesmo quadro (pausado, sem o painel).
// Uso: PLAYWRIGHT_MODULO=file:///.../index.mjs node ferramentas/conferir7.mjs [porta] [pasta]
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
  const ini = await p.evaluate(() => ({
    titulo: document.title, encontros: document.querySelectorAll("#encontros .encontro").length,
    arte: document.querySelectorAll('#tela-inicio [data-op="arte"] option').length, escala: document.querySelectorAll('#tela-inicio [data-op="escala"] option').length,
    violencia: document.querySelectorAll('#tela-inicio [data-op="violencia"] option').length,
    topo: document.querySelector("#tela-inicio .caixa").getBoundingClientRect().top,
  }));
  ok(ini.titulo.startsWith("Campo Livre 7") && ini.encontros === 9 && ini.arte === 3 && ini.escala === 2 && ini.violencia === 4 && ini.topo >= 0,
    `a escolha monta ${JSON.stringify(ini)}`);
  // sem regressão: a vila, a seleção por tipo e o modo de comando
  await p.click('#encontros .encontro[data-enc="vila"]');
  await p.selectOption("#op-comp-aliados", "completa");
  await p.click("#lutar");
  await p.waitForTimeout(4500);   // depois da formação (2,5 s), quando a câmera já segue o herói
  for (const [tecla, nome] of [["F1", "soldados"], ["F3", "cavaleiros"], ["F7", "Morel e Odette"]]) {
    await p.keyboard.press(tecla);
    await p.waitForTimeout(120);
    const sel = await p.textContent("#p-selecao");
    ok(/Seleção: \d+/.test(sel), `${tecla} seleciona ${nome}`);
    await p.keyboard.press("x");
  }
  await p.keyboard.press("F4");
  await p.keyboard.down("Shift");
  await p.waitForTimeout(120);
  const modo = await p.textContent("#modo");
  await p.mouse.click(w * 0.45, h * 0.5, { button: "right" });
  await p.waitForTimeout(200);
  const ordens = await p.textContent("#p-ordens");
  await p.keyboard.up("Shift");
  // no comando, a câmera fica estável em relação ao herói (sem o olhar para o mouse nem tremor)
  const rel = () => p.evaluate(() => { const c = window.__campo.st.cam, h = window.__campo.mundo().heroi; return { x: c.x - h.x, y: c.y - h.y }; });
  await p.keyboard.down("Shift"); await p.waitForTimeout(600);
  const c1 = await rel();
  await p.mouse.move(w * 0.9, h * 0.2); await p.waitForTimeout(500);
  const c2 = await rel();
  await p.keyboard.up("Shift");
  const mexeu = Math.hypot(c2.x - c1.x, c2.y - c1.y);
  ok(/Comando/.test(modo) && /Defender aqui\D*\d+/.test(ordens) && mexeu < 3, `modo de comando, Defender e a câmera estável com o mouse andando (${r1(mexeu)} px)`);
  // a amostra do portão: as teclas trocam a aparência, a escala e a violência no meio da luta, sem mudar a luta
  await p.goto(BASE + "?enc=amostra&auto=1&robo=1", { waitUntil: "networkidle" });
  await p.waitForTimeout(3000);
  const antes = await p.evaluate(() => ({ arte: window.__campo.opcoes.arte, n: window.__campo.mundo().unidades.length }));
  await p.keyboard.press("F8");
  await p.waitForTimeout(400);
  const f8 = await p.evaluate(() => ({ arte: window.__campo.opcoes.arte, faixa: document.querySelector("#faixa").textContent }));
  await p.keyboard.press("F8");
  await p.keyboard.press("F9");
  await p.keyboard.press("v");
  await p.waitForTimeout(400);
  const depois = await p.evaluate(() => ({ arte: window.__campo.opcoes.arte, escala: window.__campo.opcoes.escala, violencia: window.__campo.opcoes.violencia }));
  ok(antes.arte === "atual" && f8.arte === "sobria" && /Aparência/.test(f8.faixa) && depois.arte === "sombria" && depois.escala === "menor" && depois.violencia === 3,
    `F8, F9 e V trocam: ${JSON.stringify({ f8: f8.arte, ...depois })}`);
  // a provocação e um controle na HUD (o texto pronto do motor) e a marca no campo
  const cc = await p.evaluate(async () => {
    const m = window.__campo.mundo(), h = m.heroi, l = m.lider;
    h.provocacao = { por: l, ate: m.t + 2.5, total: 2.5 };
    h.lentoAte = m.t + 2; h.lentoF = 0.3;
    await new Promise((r) => setTimeout(r, 300));
    const el = document.querySelector("#cc"), r = el.getBoundingClientRect();
    return { visivel: !el.hidden, texto: el.textContent, r: { left: r.left, top: r.top, right: r.right, bottom: r.bottom } };
  });
  ok(cc.visivel && /Provocado por Harg/.test(cc.texto) && /Lento/.test(cc.texto) && cc.r.right <= w, `a HUD mostra os controles: ${cc.texto}`);
  // a mesma cena nas três aparências, no mesmo quadro (pausado, sem o painel da pausa)
  if (w === 1920) {
    await p.keyboard.press("p");
    await p.waitForTimeout(200);
    await p.evaluate(() => { for (const el of document.querySelectorAll("#tela-pausa, .tela")) el.style.visibility = "hidden"; });
    for (const [arte, escala] of [["atual", "atual"], ["sobria", "atual"], ["sombria", "atual"], ["sombria", "menor"]]) {
      await p.evaluate(([a, e]) => window.__campo.configurar({ arte: a, escala: e }), [arte, escala]);
      await p.waitForTimeout(200);
      await p.screenshot({ path: `${SAIDA}/cl7-amostra-${arte}${escala === "menor" ? "-menor" : ""}-${w}.png` });
    }
    await p.evaluate(() => { for (const el of document.querySelectorAll("#tela-pausa, .tela")) el.style.visibility = ""; });
    await p.keyboard.press("p");
  }
  // o custo com muitos soldados, a aparência sombria e a violência intensa: a vila a 2×, 14 s com o jogador automático
  await p.goto(BASE + "?enc=vila&qtd=2&compA=completa&compI=completa&auto=1&robo=1&arte=sombria&violencia=3", { waitUntil: "networkidle" });
  await p.waitForTimeout(14000);
  const d = await p.evaluate(() => window.__campo.diagnostico());
  ok(d.fps >= 50, `vila 2× sombria, violência intensa: ${r1(d.fps)} qps, simulação ${r1(d.simMedio)} ms (p95 ${r1(d.simP95)}), desenho ${r1(d.desenhoMedio)} ms (p95 ${r1(d.desenhoP95)}), ${d.unidades} unidades, ${d.particulas} partículas`);
  if (w === 1920) await p.screenshot({ path: `${SAIDA}/cl7-vila-sombria-${w}.png` });
  // o Campo Livre 6 ainda abre em /v6/
  await p.goto(BASE + "v6/", { waitUntil: "networkidle" });
  const v6 = await p.evaluate(() => ({ titulo: document.title, encontros: document.querySelectorAll("#encontros .encontro").length }));
  ok(v6.titulo.startsWith("Campo Livre 6") && v6.encontros === 8, `o Campo Livre 6 abre em /v6/ (${v6.titulo}, ${v6.encontros} encontros)`);
  ok(!erros.length, `sem erros no console ${erros.slice(0, 3).join(" | ")}`);
  await p.close();
}
await nav.close();
console.log(falhas.length ? `${falhas.length} FALHAS` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
