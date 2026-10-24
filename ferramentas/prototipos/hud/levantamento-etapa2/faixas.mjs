// As faixas de passagem e o cartão de novidade da missão, como aparecem (telas/celebracoes.js): o componente real,
// chamado na página de um cenário de teste só para desenhar (a partida não muda), a 1920×945. capturas/20-*.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/levantamento-etapa2/faixas.mjs
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
const proc = spawn(process.platform === "win32" ? "python" : "python3", ["-m", "tests.navegador.cenarios", "tutorial"],
  { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, TUTORIAL: "0", LUGAR: "vau" } });
let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await espera(100);
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
await p.goto(url);
for (let k = 0; k < 80 && !(await p.$(MENU)); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
await espera(800);
for (const [nome, m] of [["20-vitoria", { tipo: "vitoria", dados: {} }], ["21-guardiao", { tipo: "vitoria", dados: { chefe: true } }],
  ["22-mestre", { tipo: "mestre", dados: { plural: "lobos", retrato: "lobo" } }]]) {
  p.evaluate((m) => { Telas.celebrar(m, false); }, m);
  await espera(650); await p.mouse.move(2, 2);
  await p.screenshot({ path: path.join(aqui, "capturas", `${nome}.png`) }); console.log("  ", nome);
  await espera(2600);
}
await b.close(); proc.kill();
