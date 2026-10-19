// A conferência da 1.139.0 com os arquivos do jogo e o save temporário do cenário: o topo sem poções (o frasco vazio,
// 24), a compra de uma Poção de Vida no mercado (a passagem para "com poções") e o gole pela bolsa da ficha (a passagem
// de volta), medindo a caixa do recurso em cada estado; e um Antídoto comprado, na bolsa (32).
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node frasco_topo.mjs <raiz do repositório> <pasta das fotos>
import { spawn } from "child_process";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const [raiz, saida] = process.argv.slice(2);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const amb = { TUTORIAL: "0", CLASSE: "guerreiro", VIDA: "0.5", BOLSA: "pocao_vida=0", OURO: "300" };
const proc = spawn("python", ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await espera(100);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
await p.goto(url); await p.waitForFunction(() => !processando && pergunta, null, { timeout: 30000 }); await espera(1500);
const topo = (rotulo) => p.evaluate((r) => {
  const c = document.querySelector('.recurso[data-rec="pocoes"]'), b = c.getBoundingClientRect(), i = c.querySelector("img");
  return { estado: r, caixa: [b.x, b.y, b.width, b.height].map((v) => Math.round(v * 100) / 100), icone: (i.currentSrc || i.src).split("/").pop().slice(0, 24),
    lado: Math.round(i.getBoundingClientRect().width), qtd: c.querySelector(".qtd").textContent, vazio: c.classList.contains("vazio"),
    pocoes: App.estado.heroi.pocoes, hp: App.estado.heroi.hp };
}, rotulo);
const foto = async (nome) => { const bb = await (await p.$("#hud")).boundingBox(); await p.screenshot({ path: path.join(saida, `no-jogo-1.139.0-1920x945-${nome}.png`), clip: bb }); };
const rel = [await topo("sem poções")]; await foto("topo-sem");
// a passagem para "com poções": comprar uma no mercado do lugar
const mercado = await p.$('#predios .predio[data-predio="mercado"]');
if (mercado) {
  await mercado.click(); await p.waitForSelector('[data-comprar="pocao_vida"]', { timeout: 10000 }); await espera(1000);
  await p.click('[data-comprar="pocao_vida"] .merc-nome'); await espera(1500);
  await p.click('[data-comprar="antidoto"] .merc-nome'); await espera(1500);
  rel.push(await topo("com poções (comprada)")); await foto("topo-com");
  await p.keyboard.press("Escape"); await espera(1200);
  rel.push({ bolsa_ficha: await p.evaluate(() => [...document.querySelectorAll("#heroi [data-bolsa] img")].map((i) => (i.currentSrc || i.src).split("/").pop().slice(0, 24) + " " + Math.round(i.getBoundingClientRect().width))) });
  const bb = await (await p.$("#heroi .bolsa, #heroi [data-bolsa]")).boundingBox();
  await p.screenshot({ path: path.join(saida, "no-jogo-1.139.0-1920x945-bolsa.png"), clip: { x: bb.x - 10, y: bb.y - 10, width: 260, height: bb.height + 20 } });
  // a passagem de volta: beber a poção pela bolsa (em você, se a tela perguntar)
  await p.click('#heroi [data-bolsa="pocao_vida"]'); await espera(800);
  const alvo = await p.$('.menu-item:has-text("Você"), .menu-item:has-text("você"), .alvo-heroi');
  if (alvo) { await alvo.click(); await espera(800); }
  await espera(1500);
  rel.push(await topo("sem poções (bebida)")); await foto("topo-depois");
} else rel.push("sem mercado no lugar");
console.log(JSON.stringify({ rel, erros }, null, 1));
await b.close(); proc.kill();
