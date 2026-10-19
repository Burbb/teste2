// A conferência das interações da integração da 1.138.0 (a Bandagem, a Poção de Vida, o Tônico, a Calça de Viagem e o
// Manto), com os arquivos do jogo e os saves temporários dos cenários (tests/navegador/cenarios.py):
//   1. no mercado (Guerreiro): comprar um Tônico, uma Poção de Vida e uma Bandagem; as quantidades, o ouro e os
//      arquivos que a bolsa da ficha e o ícone que voa até ela carregam;
//   2. na vila (Mago) com o Manto achado: "Equipar agora"; o desenho no corpo e na ficha.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node interacoes.mjs <raiz do repositório>
import { spawn } from "child_process";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const raiz = process.argv[2];
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(cenario, amb) {
  const proc = spawn("python", ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  return { proc, url };
}
const arquivos = (p, sel) => p.evaluate((s) => [...document.querySelectorAll(s)].map((i) => `${(i.currentSrc || i.src).split("/").pop().slice(0, 28)} ${Math.round(i.getBoundingClientRect().width)}`), sel);
const b = await chromium.launch();
const rel = {};

// 1. o mercado
{
  const { proc, url } = await subir("mercado", { CLASSE: "guerreiro" });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url); await p.waitForSelector('[data-comprar="tonico"]', { timeout: 20000 }); await espera(1200);
  await p.evaluate(() => {
    window.__voos = [];
    new MutationObserver((ms) => { for (const m of ms) for (const n of m.addedNodes) {
      if (n.classList && n.classList.contains("item-voando")) { const i = n.querySelector("img"); if (i) window.__voos.push((i.currentSrc || i.src).split("/").pop().slice(0, 28)); }
    } }).observe(document.body, { childList: true, subtree: true });
  });
  const estado = () => p.evaluate(() => ({ ouro: App.estado.heroi.ouro, bolsa: Object.fromEntries(App.estado.heroi.bolsa.map((x) => [x.id, x.qtd])) }));
  const antes = await estado();
  const precos = await p.evaluate(() => Object.fromEntries(["tonico", "pocao_vida", "bandagem"].map((id) => [id, Number(document.querySelector(`[data-comprar="${id}"]`).dataset.preco)])));
  for (const id of ["tonico", "pocao_vida", "bandagem"]) { await p.click(`[data-comprar="${id}"] .merc-nome`); await espera(1500); }
  const depois = await estado();
  rel.mercado = { antes, depois, precos, gasto: antes.ouro - depois.ouro, esperado: precos.tonico + precos.pocao_vida + precos.bandagem,
    cartoes: await arquivos(p, '[data-comprar] .slot-px img'), bolsa_ficha: await arquivos(p, "#heroi [data-bolsa] img"),
    topo: await arquivos(p, '.recurso[data-rec="pocoes"] img, .recurso[data-rec="bandagens"] img'), voos: await p.evaluate(() => window.__voos), erros };
  await p.close(); proc.kill();
}
// 2. o Manto achado, vestido
{
  const { proc, url } = await subir("vila", { CLASSE: "mago", ACHADO: "manto", VESTIDO: "manto" });
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url); await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2500);
  const saque = await arquivos(p, ".janela-achado img");
  const equipar = await p.waitForSelector('#sobre-achado .botao-janela:not(.reserva):has-text("Equipar")', { timeout: 10000 });
  await equipar.click(); await espera(2500);
  rel.manto = { saque, vestido: await p.evaluate(() => (App.estado.heroi.equip || {}).armadura?.nome || null),
    ficha: await arquivos(p, "#heroi img.desenho"), erros };
  await p.close(); proc.kill();
}
await b.close();
console.log(JSON.stringify(rel, null, 1));
