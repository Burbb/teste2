// Fotografa o livro da capela no jogo de verdade (cenarios_livro.py, caso "primeira"): o livro de hoje e as propostas
// A, B e C, com os mesmos dados, a 1920×945 e a 1280×720. Na C, também a segunda entrada. Guarda em ../capturas/
// (<janela>-<versão>[-2].png) e as medidas em ../capturas/medidas.json (a caixa do livro, se o texto cabe na página,
// a letra que a página de fato usou).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/livro-capela/auxiliares/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");

async function subir(proposta, caso = "primeira") {
  const proc = spawn(PY, [path.join(aqui, "cenarios_livro.py"), caso],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: proposta } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[livro] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const medidas = {}, erros = [];
for (const [jan, W, H] of [["1920", 1920, 945], ["1280", 1280, 720]]) {
  for (const v of (process.env.VERSOES || "atual,a,b,c").split(",")) {
    const { proc, url } = await subir(v === "atual" ? "" : v);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    p.on("pageerror", (e) => erros.push(`${jan}-${v}: ${e}`));
    p.on("response", (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) erros.push(`${jan}-${v}: ${r.status()} ${r.url()}`); });
    await p.goto(url);
    for (let k = 0; k < 80 && !(await p.$(`${MENU}:has-text("Ler o livro da capela")`)); k++) {
      for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
      await espera(300);
    }
    await p.click(`${MENU}:has-text("Ler o livro da capela")`);
    await p.waitForSelector("#sobre-leitura:not([hidden])", { timeout: 20000 });
    await p.evaluate(() => document.fonts.ready);
    await espera(700);
    await p.mouse.move(2, 2);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-${v}.png`) });
    const medir = () => p.evaluate(() => {
      const caixa = document.querySelector("#sobre-leitura .lv-livro, #sobre-leitura .leitura-livro").getBoundingClientRect();
      const pags = [...document.querySelectorAll("#sobre-leitura .lv-pagina, #sobre-leitura .grimorio-pagina")].map((e) => ({
        cabe: e.scrollHeight <= e.clientHeight + 1, sobra: e.clientHeight - e.scrollHeight,
        letra: getComputedStyle(e.querySelector("p") || e).fontFamily }));
      const tudo = document.querySelector("#sobre-leitura .lv-quadro, #sobre-leitura .leitura-livro").getBoundingClientRect();
      return { livro: [Math.round(caixa.width), Math.round(caixa.height)],
        quadro: [tudo.left, tudo.top, tudo.width, tudo.height].map(Math.round), dentroDaJanela: tudo.top >= 0 && tudo.bottom <= innerHeight,
        pags, fonte: document.fonts.check('21px "Fondamento"') };
    });
    medidas[`${jan}-${v}`] = await medir();
    if (v === "c") {
      await p.click("#sobre-leitura .lv-prox");
      await espera(500);
      await p.mouse.move(2, 2);
      await p.screenshot({ path: path.join(SAIDA, `${jan}-${v}-2.png`) });
      medidas[`${jan}-${v}-2`] = await medir();
    }
    await p.close(); proc.kill();
  }
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.json"), JSON.stringify({ medidas, erros }, null, 1));
console.log(JSON.stringify({ medidas, erros }, null, 1));
