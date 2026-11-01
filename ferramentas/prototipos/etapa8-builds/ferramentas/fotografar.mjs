// Capturas do protótipo X1 nas duas janelas de referência (1920×945 e 1280×720): a montagem, uma luta com alvo
// escolhido, o fim e o registro. Precisa do servidor no ar (servidor.py) e do Playwright:
//   PLAYWRIGHT_MODULO=file:///.../playwright/index.mjs node ferramentas/fotografar.mjs <pasta-de-saída>
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const saida = process.argv[2] || ".";
const URL = process.env.X1_URL || "http://127.0.0.1:8797/";
const navegador = await chromium.launch();
const erros = [];
for (const [w, h] of [[1920, 945], [1280, 720]]) {
  const p = await navegador.newPage({ viewport: { width: w, height: h } });
  p.on("pageerror", (e) => erros.push(`${w}: ${e.message}`));
  p.on("console", (m) => { if (m.type() === "error") erros.push(`${w}: ${m.text()}`); });
  await p.goto(URL);
  await p.evaluate(() => localStorage.clear());
  await p.goto(URL);
  await p.waitForSelector(".no");
  await p.click('[data-ex="fornalha"]');
  await p.waitForTimeout(250);
  await p.screenshot({ path: `${saida}/montar-${w}.png` });
  // um filtro e o realce de um talento
  await p.click('[data-filtro="prop"][data-valor="Queimadura"]');
  await p.waitForTimeout(200);
  await p.hover('[data-no="estouro"]');
  await p.waitForTimeout(150);
  await p.screenshot({ path: `${saida}/montar-filtro-${w}.png` });
  await p.click('[data-filtro="prop"][data-valor=""]');
  await p.waitForTimeout(150);
  await p.click('[data-est="t1"]');
  await p.waitForTimeout(250);
  await p.click('[data-ex="fornalha_t1"]');
  await p.waitForTimeout(250);
  await p.screenshot({ path: `${saida}/montar-t1-${w}.png` });
  await p.click('[data-est="t4"]');
  await p.waitForTimeout(200);
  await p.click('[data-ex="fornalha"]');
  await p.waitForTimeout(200);
  await p.selectOption("#encontro", "lobos");
  await p.waitForTimeout(200);
  await p.click("#lutar");
  await p.waitForSelector(".acao");
  // Morel ataca, Jean escolhe a Brasa (alvo à espera)
  await p.click('[data-acao="atacar"]');
  await p.click('.carta.alvo');
  await p.waitForTimeout(200);
  await p.click('[data-acao="brasa"]');
  await p.waitForTimeout(200);
  await p.screenshot({ path: `${saida}/luta-${w}.png` });
  // joga até o fim: a primeira ação disponível que golpeia, no primeiro alvo
  for (let i = 0; i < 80; i++) {
    if (await p.$("#fim:not([hidden])")) break;
    if (await p.$(".carta.alvo")) { await p.click(".carta.alvo"); await p.waitForTimeout(60); continue; }
    const pref = ["combustao", "chuva", "brasa", "oportuno", "atacar", "bastao", "defender"];
    let feito = false;
    for (const id of pref) {
      const b = await p.$(`[data-acao="${id}"]:not([disabled])`);
      if (b) { await b.click(); feito = true; break; }
    }
    if (!feito) break;
    await p.waitForTimeout(60);
  }
  await p.waitForTimeout(200);
  await p.screenshot({ path: `${saida}/fim-${w}.png` });
  await p.click("#ver-log").catch(() => {});
  await p.screenshot({ path: `${saida}/log-${w}.png` });
  await p.click('[data-tela="registro"]');
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${saida}/registro-${w}.png` });
  // o Berserker na Fúria contra o troll: o botão de sair, o golpe preparado à vista
  await p.click('[data-tela="montar"]');
  await p.click('[data-spec="berserker"]');
  await p.waitForTimeout(200);
  await p.click('[data-ex="furia"]');
  await p.waitForTimeout(200);
  await p.selectOption("#encontro", "troll");
  await p.waitForTimeout(200);
  await p.screenshot({ path: `${saida}/montar-berserker-${w}.png` });
  await p.fill("#semente", "7");
  await p.click("#lutar");
  await p.waitForSelector(".acao");
  for (const id of ["atacar", "rugido", "bastao", "atacar"]) {
    await p.waitForTimeout(150);
    await p.click(`[data-acao="${id}"]:not([disabled])`, { timeout: 3000 }).catch(() => erros.push(`${w}: sem ${id}`));
  }
  await p.waitForTimeout(200);
  // passar o mouse por todas as ações não pode mover a doca
  const antes = await p.$eval(".acoes", (e) => e.getBoundingClientRect().top);
  for (const b of await p.$$(".acao")) await b.hover();
  const depois = await p.$eval(".acoes", (e) => e.getBoundingClientRect().top);
  if (antes !== depois) erros.push(`${w}: a doca andou ${depois - antes}px com o mouse`);
  await p.screenshot({ path: `${saida}/luta-furia-${w}.png` });
  // o Invocador: o Fogo-fátuo e a Sentinela no grupo, contra os lobos
  await p.click('[data-tela="montar"]');
  await p.click('[data-spec="piromante"]');
  await p.waitForTimeout(200);
  await p.click('[data-ex="invocador"]');
  await p.waitForTimeout(200);
  await p.selectOption("#encontro", "lobos");
  await p.waitForTimeout(150);
  await p.fill("#semente", "3");
  await p.click("#lutar");
  await p.waitForSelector(".acao");
  for (const id of ["atacar", "fogo_fatuo", "bastao", "atacar", "sentinela"]) {
    await p.waitForTimeout(150);
    await p.click(`[data-acao="${id}"]:not([disabled])`, { timeout: 3000 }).catch(() => {});
    if (await p.$(".carta.alvo")) await p.click(".carta.alvo");
  }
  await p.waitForTimeout(200);
  await p.screenshot({ path: `${saida}/luta-invocador-${w}.png` });
  await p.close();
}
await navegador.close();
console.log(erros.length ? "ERROS:\n" + erros.join("\n") : "sem erros no console");
