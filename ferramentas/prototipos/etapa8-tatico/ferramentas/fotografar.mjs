// Capturas do protótipo tático nas duas janelas de referência (1920×945 e 1280×720): a preparação, o movimento, o
// alcance com visão bloqueada, a prévia de uma área que pega um aliado, as casas marcadas e o fim. Confere também que
// a grade inteira cabe na janela. Precisa do servidor no ar (TATICO_URL) e do Playwright:
//   PLAYWRIGHT_MODULO=file:///.../playwright/index.mjs TATICO_URL=http://127.0.0.1:8799/ node ferramentas/fotografar.mjs <saída>
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const saida = process.argv[2] || ".";
const URL = process.env.TATICO_URL || "http://127.0.0.1:8799/";
const navegador = await chromium.launch();
const erros = [];
const casa = (p, c) => p.click(`[data-casa="${c}"]`);
for (const [w, h] of [[1920, 945], [1280, 720]]) {
  const p = await navegador.newPage({ viewport: { width: w, height: h } });
  p.on("pageerror", (e) => erros.push(`${w}: ${e.message}`));
  p.on("console", (m) => { if (m.type() === "error") erros.push(`${w}: ${m.text()}`); });
  await p.goto(URL);
  await p.evaluate(() => localStorage.clear());
  await p.goto(URL);
  await p.waitForSelector("#specs button");
  await p.click('[data-spec="piromante"]');
  await p.selectOption("#encontro", "passagem");
  await p.waitForTimeout(150);
  await p.screenshot({ path: `${saida}/preparar-${w}.png` });
  await p.click("#lutar");
  await p.waitForSelector(".casa");
  // a grade inteira à vista
  const caixa = await p.$eval("#grade", (g) => { const r = g.getBoundingClientRect(); return [r.right, r.bottom]; });
  if (caixa[0] > w || caixa[1] > h) erros.push(`${w}: a grade passa da janela (${caixa})`);
  // Morel: o movimento à vista e o caminho
  await p.hover('[data-casa="4,3"]').catch(() => {});
  await p.waitForTimeout(150);
  await p.screenshot({ path: `${saida}/movimento-${w}.png` });
  await casa(p, "3,2");
  await p.waitForTimeout(150);
  await p.click("#encerrar");
  await p.waitForTimeout(200);
  // Jean (Piromante): a Bola de Fogo, com a visão bloqueada pela parede, e a Chuva de Brasas pegando Morel
  await p.click('[data-acao="bola_fogo"]');
  await p.waitForTimeout(150);
  await p.screenshot({ path: `${saida}/alcance-visao-${w}.png` });
  await p.keyboard.press("Escape");
  await p.click('[data-acao="chuva"]');
  await p.waitForTimeout(150);
  await p.hover('[data-casa="4,2"]').catch(() => {});
  await p.waitForTimeout(100);
  await p.hover('[data-casa="3,3"]').catch(() => {});
  await p.waitForTimeout(150);
  await p.screenshot({ path: `${saida}/area-aliado-${w}.png` });
  await p.keyboard.press("Escape");
  // joga até o fim: encerra as vezes (os inimigos avançam, preparam, cercam)
  for (let i = 0; i < 80; i++) {
    if (await p.$("#fim:not([hidden])")) break;
    if (i === 8) await p.screenshot({ path: `${saida}/meio-${w}.png` });
    const pronta = await p.click('[data-acao]:not([disabled])', { timeout: 500 }).then(() => true).catch(() => false);
    if (pronta) {
      await p.waitForTimeout(60);
      const agiu = await p.click(".casa.alvo", { timeout: 500 }).then(() => true).catch(() => false);
      await p.waitForTimeout(60);
      if (agiu) continue;
      await p.keyboard.press("Escape");
    }
    await p.click("#encerrar", { timeout: 500 }).catch(() => {});
    await p.waitForTimeout(60);
  }
  await p.waitForTimeout(200);
  await p.screenshot({ path: `${saida}/fim-${w}.png` });
  await p.click("#ver-log").catch(() => {});
  await p.click('[data-tela="registro"]');
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${saida}/registro-${w}.png` });
  await p.close();
}
await navegador.close();
console.log(erros.length ? "ERROS:\n" + erros.join("\n") : "sem erros no console");
