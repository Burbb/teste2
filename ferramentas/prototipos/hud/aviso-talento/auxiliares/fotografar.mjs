// Fotografa o aviso de ponto de talento na ficha (a coluna do herói), no jogo de verdade (o cenário `tutorial`, com
// PONTOS e o tutorial desligado; saves numa pasta temporária): parado, com o mouse, com o foco do Tab, e confere que o
// clique e o Enter abrem os Talentos. PROPOSTA=r põe o CSS do protótipo (cenario_aviso.py). Guarda ../capturas/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/aviso-talento/auxiliares/fotografar.mjs
// (VERSOES=atual,r; JANELAS=1920,1280; PONTOS=1)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

async function subir(proposta) {
  const proc = spawn(PY, [path.join(aqui, "cenario_aviso.py")], { cwd: raiz,
    env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: proposta, TUTORIAL: "0", PONTOS: process.env.PONTOS || "1" } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  for (const v of (process.env.VERSOES || "atual,r").split(",")) {
    console.log(`== ${jan} ${v}`);
    const { proc, url } = await subir(v === "atual" ? "" : v);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    await p.goto(url);
    await p.waitForSelector("#heroi .talento-aviso", { timeout: 30000 });
    await p.waitForSelector("#prompt .escolhas:not(.escolhido) .escolha", { timeout: 30000 });
    await espera(800);
    const caixa = await p.evaluate(() => { const r = document.querySelector("#heroi .identidade").getBoundingClientRect(),
      s = document.querySelector("#heroi .atributos").getBoundingClientRect();
      return { x: Math.max(0, r.left - 12), y: Math.max(0, r.top - 10), width: r.width + 24, height: s.top - r.top + 30 }; });
    await p.mouse.move(2, 2);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-${v}-parado.png`), clip: caixa });
    await p.hover("#heroi .talento-aviso"); await espera(250);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-${v}-mouse.png`), clip: caixa });
    await p.mouse.move(2, 2);
    let focado = false;
    for (let k = 0; k < 60 && !focado; k++) { await p.keyboard.press("Tab"); focado = await p.evaluate(() => !!document.activeElement?.closest(".talento-aviso")); }
    conferir(focado, "o Tab chega ao aviso");
    await espera(200);
    const foco = await p.evaluate(() => { const cs = getComputedStyle(document.activeElement); return cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0 || cs.borderColor; });
    console.log("   foco:", foco);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-${v}-foco.png`), clip: caixa });
    await p.keyboard.press("Enter"); await espera(1200);
    conferir(await p.evaluate(() => !document.querySelector("#sobre-talentos").hidden), "Enter no aviso abre os Talentos");
    await p.keyboard.press("Escape"); await espera(800);
    await p.click("#heroi .talento-aviso"); await espera(1200);
    conferir(await p.evaluate(() => !document.querySelector("#sobre-talentos").hidden), "o clique no aviso abre os Talentos");
    console.log("   texto:", await p.evaluate(() => document.querySelector("#heroi .talento-aviso").innerText.trim()),
      "· dica:", await p.evaluate(() => { const e = document.querySelector("#heroi .talento-aviso"); return e.title || e.dataset.dica || "(nenhuma)"; }));
    conferir(erros.length === 0, "sem erros na página");
    await p.close(); proc.kill();
  }
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
