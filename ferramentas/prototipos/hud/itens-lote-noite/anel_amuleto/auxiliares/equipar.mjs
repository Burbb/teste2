// A conferência da 1.140.0 com os arquivos do jogo e os saves temporários dos cenários: o Mago acha um anel com o
// Anel 1 ocupado e o Anel 2 vazio; o cartão do saque compara e "Equipar no Anel 2 (vazio)" veste; depois, os dois
// espaços ocupados na ficha e no Inventário. O mesmo para o amuleto ("Equipar agora"). Registra os arquivos de cada
// lugar, os atributos antes e depois e as fotos.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node equipar.mjs <raiz do repositório> <pasta das fotos>
import { spawn } from "child_process";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const [raiz, saida] = process.argv.slice(2);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(amb) {
  const proc = spawn("python", ["-m", "tests.navegador.cenarios", "vila"], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CLASSE: "mago", ...amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  return { proc, url };
}
const arquivos = (p, sel) => p.evaluate((s) => [...document.querySelectorAll(s)].map((i) => `${(i.currentSrc || i.src).split("/").pop().slice(0, 24)} ${Math.round(i.getBoundingClientRect().width)}`), sel);
const heroi = (p) => p.evaluate(() => { const h = App.estado.heroi; return { atk: h.atk, defesa: h.defesa, agi: h.agi, poder: h.poder, hp_max: h.hp_max,
  anel1: h.equip?.anel1?.nome || null, anel2: h.equip?.anel2?.nome || null, amuleto: h.equip?.amuleto?.nome || null }; });
const b = await chromium.launch();
const rel = {};
for (const [peca, botao] of [["anel", "Equipar no Anel 2"], ["amuleto", "Equipar agora"]]) {
  const { proc, url } = await subir({ ACHADO: peca, VESTIDO: peca });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url); await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2500);
  const antes = await heroi(p);
  const saque = await arquivos(p, ".janela-achado img");
  const bb = await (await p.$(".janela-achado")).boundingBox();
  await p.screenshot({ path: path.join(saida, `no-jogo-1.140.0-1920x945-comparacao-${peca}.png`), clip: { x: bb.x - 6, y: bb.y - 6, width: bb.width + 12, height: bb.height + 12 } });
  await (await p.waitForSelector(`#sobre-achado .botao-janela:not(.reserva):has-text("${botao}")`, { timeout: 10000 })).click();
  await espera(2500);
  for (let k = 0; k < 10 && (await p.$("#sobre-achado")); k++) await espera(300);
  const depois = await heroi(p);
  const ficha = await arquivos(p, `#heroi img[src*="/${peca}-"]`);
  const fb = await (await p.$("#heroi")).boundingBox();
  await p.screenshot({ path: path.join(saida, `no-jogo-1.140.0-1920x945-ficha-${peca}.png`), clip: { x: fb.x, y: fb.y + 355, width: fb.width, height: 120 } });
  await p.evaluate(() => pedirAtalho("Inventário")); await espera(1200);
  const inv = await arquivos(p, `img[src*="/${peca}-"]`);
  const pb = await (await p.$("#palco")).boundingBox();
  await p.screenshot({ path: path.join(saida, `no-jogo-1.140.0-1920x945-inventario-${peca}.png`), clip: { x: pb.x + 150, y: pb.y + 140, width: 330, height: 380 } });
  rel[peca] = { antes, depois, saque, ficha, inventario: inv, erros };
  await p.close(); proc.kill();
}
await b.close();
console.log(JSON.stringify(rel, null, 1));
