// O ciclo da F no jogo de verdade (cenario_forja.py com PROPOSTA=f): entra na forja e fotografa a arte do topo logo
// depois de cada passo do relógio da vista, por dois ciclos (106 fotos), a 1920×945 e a 1280×720, e confere que há um
// relógio só, a 100 ms (a animação não acumula nem acelera). A foto leva tempo: umas chegam um passo depois (o desenho
// de cada quadro, um a um, é conferido no exportar_f.py --conferir). Grava as 53 primeiras em
// ../capturas/ciclo-<janela>-NNN.png (a arte no tamanho do jogo).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/forja/auxiliares/ciclo_f.mjs
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
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

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const [jan, W, H] of [["1920", 1920, 945], ["1280", 1280, 720]]) {
  console.log(`== ${jan}`);
  // uma campanha nova por janela (a outra ficou dentro da forja)
  const proc = spawn(PY, [path.join(aqui, "cenario_forja.py")], { cwd: raiz,
    env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", PROPOSTA: "f" } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 400 && !url; k++) await espera(100);
  const p = await b.newPage({ viewport: { width: W, height: H } });
  // o relógio da vista: cada passo dele fica registrado (o quadro e a hora), para conferir que anda de um em um
  await p.addInitScript(() => {
    window.__passos = [];
    const si = window.setInterval;
    window.setInterval = (f, ms, ...r) => si(() => { f(...r); if (ms === 100) window.__passos.push(performance.now()); }, ms);
  });
  await p.goto(url);
  for (let k = 0; k < 80 && !(await p.$("#prompt .escolhas:not(.escolhido) .escolha")); k++) await espera(300);
  await espera(800);
  await p.click('[data-predio="ferreiro"]');
  await p.waitForSelector(".forja .servico", { timeout: 15000 });
  await espera(1200); await p.mouse.move(2, 2);
  const r = await p.$eval("#vista", (e) => { const q = e.getBoundingClientRect(); return { x: q.left, y: q.top, width: q.width, height: q.height }; });
  // fotografa logo depois de cada passo do relógio
  const fotos = [];
  let ultimo = await p.evaluate(() => window.__passos.length);
  while (fotos.length < 106) {
    await p.waitForFunction((n) => window.__passos.length > n, ultimo, { polling: 5 });
    const n = await p.evaluate(() => window.__passos.length);
    fotos.push({ salto: n - ultimo, img: await p.screenshot({ clip: r }) });
    ultimo = n;
  }
  const saltos = fotos.slice(1).filter((f) => f.salto !== 1).length;
  console.log(`   ${saltos} de 105 fotos chegaram depois de mais de um passo (a foto leva tempo; o desenho de cada quadro é conferido no exportar_f.py)`);
  fotos.forEach((f, i) => { if (i < 53) writeFileSync(path.join(SAIDA, `ciclo-${jan}-${String(i).padStart(3, "0")}.png`), f.img); });
  const intervalos = await p.evaluate(() => window.__passos.slice(-60).map((t, i, a) => (i ? t - a[i - 1] : 0)).slice(1));
  const medio = intervalos.reduce((a, x) => a + x, 0) / intervalos.length;
  conferir(Math.abs(medio - 100) < 15, `um relógio só, a 100 ms (média ${medio.toFixed(1)} ms)`);
  await p.close();
  proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
