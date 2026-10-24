// Um vídeo só com vários cenários em sequência (24/10/2026): a mesma página passa de um servidor de teste para o
// outro (cada um com a sua versão e os seus saves temporários), a faixa do canto diz qual é, e cada festa ou achado fica
// `PERMANECE` ms na tela depois de aparecer. Serve o "antes × depois" e as especializações por apresentação.
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node video_sequencia.mjs <raiz> <saida.webm> <versão:cenário:classe>[,...]
import { spawn } from "child_process";
import { renameSync, existsSync, mkdirSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida, lista] = process.argv.slice(2);
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const PERMANECE = Number(process.env.PERMANECE || 4500);
const ROTULOS = { estouro3: "B3 · antes", estouro4: "B4 · depois", relicario4: "A4 · Relicário", "": "jogo atual",
  estouro5a: "Estouro · identidade 1", estouro5b: "Estouro · identidade 2", relicario5a: "Relicário · identidade 1", relicario5b: "Relicário · identidade 2",
  estouro5c: "Estouro · final candidata", relicario5c: "Relicário · final candidata",
  estouro5d: "Estouro · alternativa A", estouro5e: "Estouro · alternativa B", estouro5f: "Estouro · alternativa C",
  relicario5d: "Relicário · alternativa A", relicario5e: "Relicário · alternativa B", relicario5f: "Relicário · alternativa C" };
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const pasta = path.join(path.dirname(saida), "_video"); mkdirSync(pasta, { recursive: true });
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1920, height: 945 }, recordVideo: { dir: pasta, size: { width: 1920, height: 945 } } });
const p = await ctx.newPage();
const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
for (const item of lista.split(",")) {
  const [versao, cenario, classe] = item.split(":");
  const rotulo = process.env[`ROTULO_${versao}`] || ROTULOS[versao] || versao;
  const proc = spawn(process.platform === "win32" ? "python" : "python3", [path.join(AQUI, "cenarios_teste.py"), cenario], {
    cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CLASSE: classe, PROTOTIPO: versao, ROTULO: rotulo, PAINEL: "http://127.0.0.1:8765/" } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  await p.goto(url);
  await (await p.waitForSelector("button:has-text('Começar o teste')")).click();
  // as janelas deste cenário: uma festa (fecha com Enter) ou um achado novo (fecha deixando o item)
  for (let n = 0; n < 8; n++) {
    let alvo = null;
    for (let k = 0; k < 120 && !alvo; k++) {
      alvo = await p.$("#celebracao:not([hidden]) .festa, #sobre-achado .achado-cartao.novo:not([data-visto]), .festa-espolio .continuar");
      if (!alvo) { if (k < 40) await p.keyboard.press("x"); await espera(150); }
    }
    if (!alvo) break;
    const espolio = await alvo.evaluate((e) => e.matches(".festa-espolio .continuar"));
    if (espolio) { await espera(1200); await alvo.click(); await espera(400); continue; }
    const achado = await alvo.evaluate((e) => e.matches(".achado-cartao.novo"));
    if (achado) await alvo.evaluate((e) => e.setAttribute("data-visto", "1"));
    await espera(PERMANECE);
    if (achado) { await p.waitForSelector("#sobre-achado .achado-acoes button:not(.reserva)"); const bs = await p.$$("#sobre-achado .achado-acoes button:not(.reserva)"); await bs[bs.length - 1].click(); }
    else await p.keyboard.press("Enter");
    await espera(500);
    if (!(await p.$("#celebracao:not([hidden]) .festa, #sobre-achado .achado-cartao.novo:not([data-visto]), .festa-espolio")) ) { await espera(900);
      if (!(await p.$("#celebracao:not([hidden]) .festa, #sobre-achado .achado-cartao.novo:not([data-visto]), .festa-espolio"))) break; }
  }
  proc.kill();
}
const video = p.video();
await ctx.close(); await b.close();
const v = await video.path();
if (existsSync(v)) renameSync(v, saida);
console.log(saida, erros.length ? erros : "sem erros");
