// A conferência da 1.142.0 com os arquivos do jogo e os saves temporários dos cenários (o de equipar.mjs do anel): o
// Mago acha uma Sandália com outra vestida; o cartão do saque compara e "Equipar agora" veste (os atributos antes e
// depois, a ficha e o Inventário); numa segunda partida, "Guardar na mochila" guarda (a vestida fica, a mochila ganha
// uma). Registra os arquivos de cada lugar, os atributos e as fotos. Depois do saque, a cena pede "Continuar" e o
// cenário abre o mural: o roteiro passa pelos dois antes de abrir o Inventário.
// Serve a outra peça pelos argumentos opcionais (a Besta Leve, 1.143.0: mago → arqueiro, sandalia → besta, pes → arma).
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node equipar.mjs <raiz do repositório> <pasta das fotos> [classe desenho espaço versão]
import { spawn } from "child_process";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const [raiz, saida, CLASSE = "mago", DESENHO = "sandalia", ESPACO = "pes", VERSAO = "1.142.0"] = process.argv.slice(2);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir() {
  const proc = spawn("python", ["-m", "tests.navegador.cenarios", "vila"], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CLASSE, ACHADO: DESENHO, VESTIDO: DESENHO } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  return { proc, url };
}
const arquivos = (p, sel) => p.evaluate((s) => [...document.querySelectorAll(s)].map((i) => `${(i.currentSrc || i.src).split("/").pop().slice(0, 24)} ${Math.round(i.getBoundingClientRect().width)}`), sel);
const heroi = (p) => p.evaluate((ESPACO) => { const h = App.estado.heroi; return { ...h.atributos, vida: h.max_hp, recurso: h.max_rec,
  vestido: h.equip?.[ESPACO]?.nome || null, mochila: (h.mochila || []).map((i) => i.nome) }; }, ESPACO);
const b = await chromium.launch();
const rel = {};
for (const [caso, botao] of [["equipar", "Equipar agora"], ["guardar", "Guardar na mochila"]]) {
  const { proc, url } = await subir();
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url); await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2500);
  const antes = await heroi(p);
  const saque = await arquivos(p, ".janela-achado img");
  const bb = await (await p.$(".janela-achado")).boundingBox();
  if (caso === "equipar") await p.screenshot({ path: path.join(saida, `no-jogo-${VERSAO}-1920x945-saque.png`), clip: { x: bb.x - 6, y: bb.y - 6, width: bb.width + 12, height: bb.height + 12 } });
  await (await p.waitForSelector(`#sobre-achado .botao-janela:has-text("${botao}")`, { timeout: 10000 })).click();
  await espera(2500);
  for (let k = 0; k < 10 && (await p.$("#sobre-achado")); k++) await espera(300);
  const depois = await heroi(p);
  const ficha = await arquivos(p, `#heroi img[src*="/${DESENHO}-"]`);
  const fb = await (await p.$("#heroi")).boundingBox();
  await p.screenshot({ path: path.join(saida, `no-jogo-${VERSAO}-1920x945-ficha-${caso}.png`), clip: { x: fb.x, y: fb.y + 355, width: fb.width, height: 120 } });
  // a cena espera o "Continuar" e depois abre o mural do cenário: os dois antes do Inventário
  for (let k = 0; k < 4 && !(await p.$(".tela.inventario")); k++) {
    const cont = await p.$('button:has-text("Continuar")');
    if (cont) { await cont.click(); await espera(1500); }
    await p.keyboard.press("Escape"); await espera(700);
    await p.evaluate(() => pedirAtalho("Inventário")); await espera(1500);
  }
  const inv = await arquivos(p, `img[src*="/${DESENHO}-"]`);
  const pb = await (await p.$("#palco")).boundingBox();
  await p.screenshot({ path: path.join(saida, `no-jogo-${VERSAO}-1920x945-inventario-${caso}.png`), clip: { x: pb.x + 150, y: pb.y + 140, width: 330, height: 380 } });
  rel[caso] = { antes, depois, saque, ficha, inventario: inv, erros };
  await p.close(); proc.kill();
}
await b.close();
console.log(JSON.stringify(rel, null, 1));
