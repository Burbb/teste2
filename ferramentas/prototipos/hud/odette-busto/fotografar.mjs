// Busto da Odette (candidata): fotografa o Inventário do grupo na aba da Odette com o busto de hoje e com a candidata
// (candidata.js, posta na página só aqui; o jogo não muda), os mesmos dados, em 1920×945 (busto de 80 px) e 1280×720
// (64 px). Guarda as páginas e os recortes do boneco em capturas/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/odette-busto/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

const b = await chromium.launch();
const erros = [];
for (const [w, h] of [[1920, 945], [1280, 720]]) {
  // um cenário novo por tamanho: a página anterior deixou o jogo no Inventário
  const proc = spawn("python", ["-m", "tests.navegador.cenarios", "grupo"], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz } });
  const url = await new Promise((ok) => proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) ok(m[0]); }));
  const p = await (await b.newContext({ viewport: { width: w, height: h } })).newPage();
  p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url); await espera(2000);
  await p.click('#doca .atalho[data-rotulo="Inventário"]'); await espera(1200);
  await p.click('.grupo-abas .grupo-aba[data-aba="odete"]'); await espera(800);
  await p.mouse.move(2, 2);
  for (const lado of ["antes", "depois"]) {
    if (lado === "depois") { await p.addScriptTag({ path: path.join(aqui, "candidata.js") }); await espera(600); }
    await p.screenshot({ path: path.join(SAIDA, `${w}-${lado}.png`) });
    const r = await (await p.$(".boneco")).boundingBox();
    await p.screenshot({ path: path.join(SAIDA, `${w}-${lado}-boneco.png`), clip: r });
  }
  console.log(w, "candidata posta:", await p.evaluate(() => !!document.querySelector(".boneco-retrato .candidata")));
  await p.close(); proc.kill();
}
console.log("erros", erros);
await b.close();
