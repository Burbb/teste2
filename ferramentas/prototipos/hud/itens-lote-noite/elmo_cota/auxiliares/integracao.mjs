// A conferência da 1.146.0 com os arquivos do jogo (sem trocar nada pela página) e o save temporário do cenário vila:
// o Guerreiro com uma cota vestida tira a armadura (dois cliques no espaço do peito, a ação "tirar" do jogo), para a
// silhueta do peito vazio no Inventário (40) e na ficha (32). O saque, equipar e guardar saem do equipar.mjs do anel
// (guerreiro armadura armadura 1.146.0 cota). Registra os arquivos de cada lugar e as fotos.
// Serve a outra peça pelos argumentos opcionais (a manopla, 1.147.0: maos manopla 1.147.0 manopla maos-vazias).
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node integracao.mjs <raiz do repositório> <pasta das fotos> [espaço desenho versão arquivo rótulo]
import { spawn } from "child_process";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const [raiz, saida, ESPACO = "armadura", DESENHO = "armadura", VERSAO = "1.146.0", ARQUIVO = "cota", ROTULO = "peito-vazio"] = process.argv.slice(2);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn("python", ["-m", "tests.navegador.cenarios", "vila"], { cwd: raiz,
  env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CLASSE: "guerreiro", ACHADO: DESENHO, VESTIDO: DESENHO } });
let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await espera(100);
const arquivos = (p, sel) => p.evaluate((s) => [...document.querySelectorAll(s)].map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${Math.round(i.getBoundingClientRect().width)}`), sel);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
await p.goto(url); await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2000);
await (await p.waitForSelector('#sobre-achado .botao-janela:has-text("Guardar na mochila")', { timeout: 10000 })).click();
await espera(2500);
for (let k = 0; k < 4 && !(await p.$(".tela.inventario")); k++) {
  const cont = await p.$('button:has-text("Continuar")');
  if (cont) { await cont.click(); await espera(1500); }
  await p.keyboard.press("Escape"); await espera(700);
  await p.evaluate(() => pedirAtalho("Inventário")); await espera(1500);
}
const pb = await (await p.$("#palco")).boundingBox();
const rel = { vestida: await arquivos(p, `[data-espaco="${ESPACO}"] img`) };
await p.dblclick(`[data-espaco="${ESPACO}"]`); await espera(1800);
rel.vestida_depois = await p.evaluate((e) => (App.estado.heroi.equip[e] || {}).nome || null, ESPACO);
rel.vazio_inventario = await arquivos(p, `[data-espaco="${ESPACO}"] img`);
rel.mochila = await arquivos(p, `#palco img[src*="/${ARQUIVO}-"]`);
await p.screenshot({ path: path.join(saida, `no-jogo-${VERSAO}-1920x945-inventario-${ROTULO}.png`), clip: { x: pb.x + 150, y: pb.y + 140, width: 330, height: 380 } });
await p.keyboard.press("Escape"); await espera(900);
const fb = await (await p.$("#heroi")).boundingBox();
rel.vazio_ficha = await arquivos(p, `#heroi [data-mini="${ESPACO}"] img`);
const mb = await (await p.$(`#heroi [data-mini="${ESPACO}"]`)).boundingBox();
await p.screenshot({ path: path.join(saida, `no-jogo-${VERSAO}-1920x945-ficha-${ROTULO}.png`), clip: { x: fb.x, y: ESPACO === "armadura" ? fb.y + 355 : Math.max(fb.y, mb.y - 40), width: fb.width, height: 120 } });
rel.erros = erros;
await p.close(); proc.kill(); await b.close();
console.log(JSON.stringify(rel, null, 1));
