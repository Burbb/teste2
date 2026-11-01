// Capturas rápidas de uma batalha com o jogador automático: node ferramentas/olhar.mjs <saída> <largura> <altura> <heroi> <tempos...>
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [saida, w, h, heroi, ...tempos] = process.argv.slice(2);
const URL = process.env.CAMPO_URL || "http://127.0.0.1:8801/";
const nav = await chromium.launch();
const p = await nav.newPage({ viewport: { width: +w, height: +h } });
const erros = [];
p.on("pageerror", (e) => erros.push(e.message));
p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
await p.goto(`${URL}?heroi=${heroi}&auto=1&robo=1`);
let t0 = Date.now();
for (const t of tempos) {
  const espera = +t * 1000 - (Date.now() - t0);
  if (espera > 0) await p.waitForTimeout(espera);
  await p.screenshot({ path: `${saida}/${heroi}-${w}-${t}.png` });
}
console.log(JSON.stringify(await p.evaluate(() => window.__campo.diagnostico())));
console.log(erros.join("\n") || "sem erros");
await nav.close();
