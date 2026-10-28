// Etapa 5, levantamento: como o jogo mostra hoje a taverna, o templo e a curandeira (e a forja, a única com interior),
// a 1920×945, no cenário "grupo" (o Vau do Turvo com Morel e Odette). Guarda em capturas-hoje/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/interiores-vila/fotografar_hoje.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas-hoje");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

const proc = spawn("python", ["-m", "tests.navegador.cenarios", "grupo"], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz } });
const url = await new Promise((ok) => proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) ok(m[0]); }));
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1920, height: 945 } })).newPage();
const erros = [];
p.on("pageerror", (e) => erros.push(String(e)));
await p.goto(url); await espera(2500);
await p.waitForSelector('[data-predio="taverna"]', { timeout: 20000 }).catch(() => {});
await p.mouse.move(2, 2);
await p.screenshot({ path: path.join(SAIDA, "0-vila.png") });
for (const [predio, nome] of [["taverna", "1-taverna"], ["templo", "2-templo"], ["curandeiro", "3-curandeira"], ["ferreiro", "4-forja"]]) {
  const el = await p.waitForSelector(`[data-predio="${predio}"]`, { timeout: 10000 }).catch(() => null);
  if (!el) { console.log("sem prédio", predio); continue; }
  await el.click(); await espera(2200); await p.mouse.move(2, 2);
  await p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
  // Esc volta à vila (a câmera sai do prédio): até os prédios estarem soltos de novo
  for (let k = 0; k < 4 && !(await p.$('#predios:not(.focado) .predio[data-predio="taverna"]')); k++) { await p.keyboard.press("Escape"); await espera(1200); }
}
console.log("erros", erros);
await b.close(); proc.kill();
