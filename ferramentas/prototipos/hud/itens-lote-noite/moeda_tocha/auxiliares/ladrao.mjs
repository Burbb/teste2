// A moeda que o ladrão leva (projetil "moeda", 32): luta contra bandidos até um roubar; registra o arquivo e o tamanho de
// cada projétil de moeda e fotografa no meio do voo. Velocidade normal: no modo rápido o projétil não aparece.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ladrao.mjs <raiz do repositório> <saida.png>
import { spawn } from "child_process";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const [raiz, saida] = process.argv.slice(2);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const amb = { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL: "8", LUTA: "bandido", QUANTOS: "3", NIVEL_LUTA: "7", LUTA_APOS_ESCOLHA: "1", OURO: "300", SEMENTE: process.env.SEMENTE || "3" };
const proc = spawn("python", ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await espera(100);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
await p.goto(url);
await p.evaluate(() => {
  window.__moedas = [];
  new MutationObserver((ms) => { for (const m of ms) for (const n of m.addedNodes) {
    if (n.classList && n.classList.contains("projetil")) { const i = n.querySelector("img"); if (i) setTimeout(() => window.__moedas.push(`${(i.currentSrc || i.src).split("/").pop().slice(0, 30)} ${Math.round(i.getBoundingClientRect().width)}px`), 30); }
  } }).observe(document.body, { childList: true, subtree: true });
});
await (await p.waitForSelector('#prompt .escolha:has-text("Começar a luta")', { timeout: 30000 })).click();
let foto = false;
for (let k = 0; k < 200 && !foto; k++) {
  if (!(await p.evaluate(() => document.body.classList.contains("em-combate"))) && k > 10) break;
  const bt = await p.$('#roda .roda-botao[data-slot="atacar"]'); if (bt) await bt.click().catch(() => {});
  const alvo = await p.$(".carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
  for (let t = 0; t < 30; t++) {
    const tem = await p.evaluate(() => [...document.querySelectorAll(".projetil img")].some((i) => /moeda/.test(i.currentSrc || i.src) || i.closest(".projetil")?.dataset?.moeda));
    const roubo = await p.evaluate(() => window.__moedas.length);
    if (roubo) { await espera(60); await p.screenshot({ path: saida }); foto = true; break; }
    await espera(80);
  }
}
await espera(1500);
console.log(JSON.stringify({ foto, moedas: await p.evaluate(() => window.__moedas), erros }));
await b.close(); proc.kill();
