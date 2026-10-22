// O Esgotado no lugar dele (22/10/2026): o mercado com um suprimento comprado até o fim do estoque (o motivo
// "Esgotado") e outros caros demais ("Ouro insuficiente", que continua no cadeado). Três fotos iguais a 1920×945 (a
// janela do Jean): o atual (o cadeado), o caixote e o cesto. A proposta entra só na página, só no ícone do motivo
// "Esgotado" (o papel próprio): o jogo e o cadeado dos outros usos ficam como estão.
//   PLAYWRIGHT_MODULO=<file:///.../index.mjs> node fotografar.mjs
import { spawn } from "child_process";
import { readFileSync, mkdirSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const PASTA = path.resolve(AQUI, "..");
const RAIZ = path.resolve(AQUI, "../../../../../..");
const SAIDA = path.join(PASTA, "capturas");
mkdirSync(SAIDA, { recursive: true });
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const PYTHON = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const dataUrl = (id) => "data:image/png;base64," + readFileSync(path.join(PASTA, "proposta", `${id}-16.png`)).toString("base64");
const VERSOES = [["atual", null], ["caixote", dataUrl("esgotado-caixote")], ["cesto", dataUrl("esgotado-cesto")]];

const proc = spawn(PYTHON, ["-m", "tests.navegador.cenarios", "mercado"], { cwd: RAIZ, env: { ...process.env, VELOCIDADE: "rapido", OURO: "20", PYTHONPATH: RAIZ } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 100 && !url; k++) await new Promise((r) => setTimeout(r, 100));
const browser = await chromium.launch();
const registro = {};
try {
  const page = await browser.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = [];
  page.on("pageerror", (e) => erros.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
  await page.goto(url);
  await page.waitForSelector(".tela.loja .mercadoria.suprimento", { timeout: 20000 });
  await page.waitForTimeout(900);
  // o suprimento mais barato com estoque: comprado até acabar (um por clique, esperando a tela voltar)
  const alvo = await page.evaluate(() => {
    const c = [...document.querySelectorAll(".tela.loja .mercadoria.suprimento:not(.caro)")]
      .map((e) => ({ id: e.dataset.comprar, preco: +e.dataset.preco, estoque: +e.querySelector(".merc-estoque b").textContent }))
      .filter((x) => x.estoque > 0).sort((a, b) => a.preco * a.estoque - b.preco * b.estoque);
    return c[0];
  });
  for (let k = 0; k < alvo.estoque; k++) {
    await page.waitForFunction(() => pergunta && pergunta.tipo === "opcoes" && !processando, null, { timeout: 10000 });
    await page.click(`.tela.loja .mercadoria.suprimento[data-comprar="${alvo.id}"] .merc-nome`);
    await page.waitForTimeout(450);
  }
  await page.waitForFunction(() => pergunta && pergunta.tipo === "opcoes" && !processando, null, { timeout: 10000 });
  await page.mouse.move(5, 500);
  await page.waitForTimeout(2600);  // os avisos da compra somem
  registro.alvo = alvo;
  registro.motivos = await page.$$eval(".tela.loja .merc-motivo", (ms) => ms.map((m) => m.textContent.trim()));
  const caixa = await page.evaluate(() => {
    const r = document.querySelector(".tela.loja [data-painel='suprimentos']").getBoundingClientRect();
    return { x: Math.floor(r.left) - 4, y: Math.floor(r.top) - 4, width: Math.ceil(r.width) + 8, height: Math.min(Math.ceil(r.height) + 8, 520) };
  });
  for (const [nome, src] of VERSOES) {
    const n = await page.evaluate((src) => {
      let n = 0;
      document.querySelectorAll(".tela.loja .merc-motivo").forEach((m) => {
        const img = m.querySelector("img.sprite");
        if (!img.dataset.orig) img.dataset.orig = img.src;
        if (m.textContent.trim().startsWith("Esgotado")) { img.src = src || img.dataset.orig; n++; }
      });
      return n;
    }, src);
    await page.waitForTimeout(200);
    await page.screenshot({ path: path.join(SAIDA, `mercado-${nome}.png`) });
    await page.screenshot({ path: path.join(SAIDA, `suprimentos-${nome}.png`), clip: caixa });
    registro[nome] = { trocados: n, tamanho: await page.$eval(".tela.loja .merc-motivo img.sprite", (i) => `${i.getBoundingClientRect().width}×${i.getBoundingClientRect().height}`) };
  }
  registro.erros = erros;
  await page.close();
} finally {
  await browser.close();
  proc.kill();
}
writeFileSync(path.join(SAIDA, "registro.json"), JSON.stringify(registro, null, 2) + "\n");
console.log(JSON.stringify(registro, null, 2));
