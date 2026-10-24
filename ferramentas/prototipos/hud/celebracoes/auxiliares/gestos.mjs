// Os gestos das celebrações, conferidos na página (24/10/2026): Enter, Esc, a tecla segurada, o clique duplo, o clique
// rápido no achado, a transição para a escolha seguinte sem o clique atravessar e a limpeza dos efeitos ao fechar.
// Cada verificação diz "ok" ou o que achou.
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> PROTOTIPO=<direção> node gestos.mjs <raiz>
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz] = process.argv.slice(2);
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const resultados = [];
const conferir = (nome, ok, detalhe = "") => resultados.push(`${ok ? "ok  " : "FALHA"} ${nome}${detalhe ? ` (${detalhe})` : ""}`);

async function abrir(b, cenario, classe, preparar = null) {
  const proc = spawn(process.platform === "win32" ? "python" : "python3", [path.join(AQUI, "cenarios_teste.py"), cenario],
    { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CLASSE: classe } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  const p = await (await b.newContext({ viewport: { width: 1920, height: 945 } })).newPage();
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.addInitScript(() => {  // as respostas que a página manda (uma escolha é um /responder)
    window.__respostas = 0; const f = window.fetch;
    window.fetch = (...a) => { if (String(a[0]).includes("/responder")) window.__respostas++; return f(...a); };
  });
  await p.goto(url);
  if (preparar) await p.evaluate(preparar);
  await (await p.waitForSelector("button:has-text('Começar o teste')")).click();
  for (let k = 0; k < 40 && !(await p.$("#celebracao .festa, .festa-espolio, #sobre-achado .achado-cartao")); k++) { await p.keyboard.press("x"); await espera(250); }
  return { p, proc, erros };
}
const festaAberta = (p) => p.evaluate(() => !!document.querySelector("#celebracao:not([hidden]) .festa"));
const palcos = (p) => p.evaluate(() => document.querySelectorAll(".fx-palco").length);

const b = await chromium.launch();
// 1. dois níveis: a tecla segurada não fecha; Esc fecha um; o clique duplo fecha um só; Enter fecha; a limpeza
{
  const { p, proc, erros } = await abrir(b, "dois_niveis", "mago");
  await (await p.waitForSelector(".festa-espolio .continuar")).click();
  await p.waitForSelector("#celebracao .festa"); await espera(500);
  await p.evaluate(() => document.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", repeat: true, bubbles: true })));
  await espera(200);
  conferir("tecla segurada não fecha a festa", await festaAberta(p));
  await p.keyboard.press("Escape"); await espera(250);
  const depoisEsc = await p.evaluate(() => document.querySelector("#celebracao .festa-nivel, #celebracao .fa2-nivel, #celebracao .fb2-nivel")?.textContent.includes("3"));
  conferir("Esc fecha o nível 2 e o nível 3 abre", !!depoisEsc);
  await espera(500);
  const c = await p.$("#celebracao .continuar"), r = await c.boundingBox();
  await p.mouse.dblclick(r.x + r.width / 2, r.y + r.height / 2); await espera(600);
  const respostas = await p.evaluate(() => window.__respostas);
  conferir("clique duplo fecha uma festa só e não atravessa", !(await festaAberta(p)) && (await palcos(p)) === 0, `palcos: ${await palcos(p)}`);
  await espera(1500);
  conferir("nenhuma escolha mandada pelo clique que fechou (até 1,5 s depois)", (await p.evaluate(() => window.__respostas)) === respostas);
  conferir("a tela não ficou deslocada pelo tremor", (await p.evaluate(() => document.body.style.translate || "")) === "");
  conferir("sem erros na página", !erros.length, erros.join("; "));
  await p.context().close(); proc.kill();
}
// 2. raridades: o clique rápido adianta sem escolher; Enter durante a entrada não escolhe; a janela anterior some
{
  const { p, proc, erros } = await abrir(b, "raridades", "arqueiro", () => {
    window.__t = [];
    new MutationObserver(() => {
      const c = document.querySelector("#sobre-achado .achado-cartao.novo:not([data-q])");
      if (c) { c.setAttribute("data-q", 1); const t0 = performance.now(); window.__t.push(["cartão", 0]);
        setTimeout(() => { const o = { bubbles: true, cancelable: true, clientX: 200, clientY: 470, detail: 1 };
          const alvo = document.elementFromPoint(200, 470); alvo.dispatchEvent(new PointerEvent("pointerdown", o)); alvo.dispatchEvent(new MouseEvent("click", o));
          document.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true })); window.__t.push(["gesto", Math.round(performance.now() - t0)]); }, 50);
        const ob = new MutationObserver(() => { if (document.querySelector("#sobre-achado .achado-acoes button:not(.reserva)")) { window.__t.push(["botões", Math.round(performance.now() - t0)]); ob.disconnect(); } });
        ob.observe(document.getElementById("sobre-achado"), { childList: true, subtree: true }); }
    }).observe(document.body, { childList: true, subtree: true });
  });
  const tempos = [];
  for (let k = 0; k < 4; k++) {
    const botoes = await p.waitForSelector("#sobre-achado .achado-acoes button:not(.reserva)");
    await espera(300);
    const aberto = await p.evaluate(() => !!document.querySelector("#sobre-achado .achado-acoes button:not(.reserva)"));
    if (!aberto) { conferir("o gesto rápido não escolheu", false); break; }
    tempos.push(await p.evaluate(() => (window.__t.filter((x) => x[0] === "botões").pop() || [0, -1])[1]));
    const bs = await p.$$("#sobre-achado .achado-acoes button:not(.reserva)");
    await bs[bs.length - 1].click(); await espera(400);
    void botoes;
  }
  conferir("clique e Enter rápidos adiantam a entrada sem escolher", tempos.length === 4 && tempos.every((x) => x >= 0 && x < 250), `botões em ${tempos.join(", ")} ms`);
  await espera(800);
  conferir("os palcos das janelas fechadas saíram", (await palcos(p)) <= 0, `palcos: ${await palcos(p)}`);
  conferir("sem erros na página", !erros.length, erros.join("; "));
  await p.context().close(); proc.kill();
}
// 3. Sigilo: o clique que fecha não atravessa para a escolha seguinte
{
  const { p, proc, erros } = await abrir(b, "sigilo", "guerreiro");
  await p.waitForSelector("#celebracao .festa"); await espera(800);
  const antes = await p.evaluate(() => window.__respostas);
  const c = await p.$("#celebracao .continuar"), r = await c.boundingBox();
  await p.mouse.click(r.x + r.width / 2, r.y + r.height / 2); await espera(1500);
  conferir("fechar o Sigilo não manda escolha", (await p.evaluate(() => window.__respostas)) === antes);
  conferir("o palco do Sigilo saiu", (await palcos(p)) === 0, `palcos: ${await palcos(p)}`);
  conferir("sem erros na página", !erros.length, erros.join("; "));
  await p.context().close(); proc.kill();
}
// 4. as especializações: Esc fecha, o palco sai; no Patrulheiro, o clique que fecha não escolhe o companheiro
for (const spec of ["sombra", "patrulheiro"]) {
  const { p, proc, erros } = await abrir(b, `spec_${spec}`, "arqueiro");
  await p.waitForSelector("#celebracao .festa"); await espera(900);
  const antes = await p.evaluate(() => window.__respostas);
  if (spec === "sombra") { await p.keyboard.press("Escape"); }
  else { const c = await p.$("#celebracao .continuar"), r = await c.boundingBox(); await p.mouse.dblclick(r.x + r.width / 2, r.y + r.height / 2); }
  await espera(1500);
  conferir(`${spec}: a festa fechou e o palco saiu`, !(await festaAberta(p)) && (await palcos(p)) === 0, `palcos: ${await palcos(p)}`);
  conferir(`${spec}: nenhuma escolha mandada pelo gesto que fechou`, (await p.evaluate(() => window.__respostas)) === antes);
  conferir(`${spec}: sem erros na página`, !erros.length, erros.join("; "));
  await p.context().close(); proc.kill();
}
await b.close();
console.log(`${process.env.PROTOTIPO || "jogo atual"}:\n  ${resultados.join("\n  ")}`);
