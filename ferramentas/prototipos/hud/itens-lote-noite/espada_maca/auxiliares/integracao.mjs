// A conferência da 1.145.0 com os arquivos do jogo (sem trocar nada pela página) e os saves temporários dos cenários:
// o Guerreiro com a espada e com a maça na ficha (32) e no Inventário (40); a arma tirada (dois cliques no espaço da
// arma, a ação "tirar" do jogo), para a silhueta da arma vazia na ficha e no Inventário; e a roda da luta, com o Atacar
// (o desenho da espada). Registra os arquivos de cada lugar e as fotos.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node integracao.mjs <raiz do repositório> <pasta das fotos>
import { spawn } from "child_process";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const [raiz, saida] = process.argv.slice(2);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(amb) {
  const proc = spawn("python", ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CLASSE: "guerreiro", TUTORIAL: "0", PERIODO: "0", ...amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  return { proc, url };
}
const arquivos = (p, sel) => p.evaluate((s) => [...document.querySelectorAll(s)].map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${Math.round(i.getBoundingClientRect().width)}`), sel);
const b = await chromium.launch();
const rel = {};
for (const arma of ["espada", "maca"]) {
  const { proc, url } = await subir({ ARMA: arma });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url); await p.waitForSelector("#heroi", { timeout: 30000 }); await espera(2500);
  const fb = await (await p.$("#heroi")).boundingBox();
  const ficha = await arquivos(p, '#heroi img[src*="/espada-"], #heroi img[src*="/maca-"]');
  await p.screenshot({ path: path.join(saida, `no-jogo-1.145.0-1920x945-ficha-${arma}.png`), clip: { x: fb.x, y: fb.y + 355, width: fb.width, height: 120 } });
  await p.evaluate(() => pedirAtalho("Inventário")); await espera(1500);
  const pb = await (await p.$("#palco")).boundingBox();
  const inv = await arquivos(p, '#palco img[src*="/espada-"], #palco img[src*="/maca-"]');
  await p.screenshot({ path: path.join(saida, `no-jogo-1.145.0-1920x945-inventario-${arma}.png`), clip: { x: pb.x + 150, y: pb.y + 140, width: 330, height: 380 } });
  const r = { ficha, inventario: inv, erros };
  if (arma === "espada") {   // a arma vazia: tirar a espada (dois cliques no espaço) e ver a silhueta
    await p.dblclick('[data-espaco="arma"]'); await espera(1800);
    r.vazio_inventario = await arquivos(p, '[data-espaco="arma"] img');
    r.arma_vestida = await p.evaluate(() => (App.estado.heroi.equip.arma || {}).nome || null);
    await p.screenshot({ path: path.join(saida, "no-jogo-1.145.0-1920x945-inventario-arma-vazia.png"), clip: { x: pb.x + 150, y: pb.y + 140, width: 330, height: 380 } });
    await p.keyboard.press("Escape"); await espera(900);
    r.vazio_ficha = await arquivos(p, '#heroi [data-mini="arma"] img');
    await p.screenshot({ path: path.join(saida, "no-jogo-1.145.0-1920x945-ficha-arma-vazia.png"), clip: { x: fb.x, y: fb.y + 355, width: fb.width, height: 120 } });
  }
  rel[arma] = r;
  await p.close(); proc.kill();
}
// a roda da luta: o Atacar do Guerreiro
{
  const { proc, url } = await subir({ LUTA_APOS_ESCOLHA: "1", VISTAS: "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4", NIVEL: "8", ESPEC: "paladino",
    COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7", ARMA: "espada" });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url); await p.waitForSelector("#prompt .escolha", { timeout: 30000 }); await espera(1500);
  const comecar = await p.$('#prompt .escolha:has-text("Começar a luta")');
  if (comecar) await comecar.click();
  await p.waitForFunction(() => document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando, null, { timeout: 30000 }); await espera(1200);
  const pb = await (await p.$("#palco")).boundingBox();
  await p.screenshot({ path: path.join(saida, "no-jogo-1.145.0-1920x945-luta.png"), clip: { x: pb.x + 250, y: pb.y + 10, width: 220, height: 215 } });
  rel.atacar = { roda: await arquivos(p, '#roda .roda-botao[data-slot="atacar"] img'), erros };
  await p.close(); proc.kill();
}
await b.close();
console.log(JSON.stringify(rel, null, 1));
