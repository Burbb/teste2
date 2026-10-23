// As fotos do Barqueiro do Charco em 32 nativos (protótipo; nada no jogo), a 1920×945: o guardião na luta pelo cenário
// "tutorial" dos testes de navegador (CHEFE=barqueiro_do_charco, GRUPO=afogado:1), rodado numa cópia da branch
// claude/barqueiro-do-charco (onde o guardião do covil já é o Barqueiro, ainda sem retrato próprio), ao lado do Afogado
// (o retrato de produção). Modos: "atual" (o que a branch mostra: a caveira) e "n32" (o estudo), trocado só na página.
//   [MODOS=atual,n32] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz da branch> <pasta das fotos>
import { spawn } from "child_process";
import { mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.dirname(fileURLToPath(import.meta.url));
const url64 = (arq) => "data:image/png;base64," + readFileSync(path.join(aqui, arq)).toString("base64");
const TROCA = { n32: [url64("../proposta/barqueiro-n32-32.png"), url64("../proposta/barqueiro-n32-32@2x.png")] };
const AMB = { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "5", GRUPO: "afogado:1", CHEFE: "barqueiro_do_charco" };
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const registro = {};
for (const modo of (process.env.MODOS || "atual,n32").split(",")) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...AMB } });
  let url = null; proc.stdout.on("data", (d) => { const k = String(d).match(/http:\S+/); if (k) url = k[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: 1920, height: 945 }, deviceScaleFactor: 1 });
    const erros = [];
    p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (k) => { if (k.type() === "error" || k.type() === "warning") erros.push(k.text()); });
    await p.goto(url);
    await espera(2500);
    if (TROCA[modo]) await p.evaluate(([src, src2]) => {
      const marca = `<img class="sprite desenho" src="${src}" srcset="${src2} 2x" width="32" height="32" style="--s:32" alt="" draggable="false">`;
      const aplica = () => {
        for (const c of document.querySelectorAll(".inimigos .carta")) {
          const n = c.querySelector(".carta-nome span"), ic = c.querySelector(".icone");
          if (!n || !ic || !/^Barqueiro do Charco/.test(n.textContent.trim())) continue;
          const im = ic.querySelector("img");
          if (!im || im.getAttribute("src") !== src) ic.innerHTML = marca;
        }
      };
      aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true });
    }, TROCA[modo]);
    await espera(1500);
    await p.locator("#palco").first().screenshot({ path: path.join(saida, `luta-barqueiro-${modo}.png`) });
    registro[modo] = await p.evaluate(() => {
      const o = document.querySelector("#palco").getBoundingClientRect();
      const cartas = [...document.querySelectorAll(".aliados .carta, .inimigos .carta")].map((c) => {
        const r = c.getBoundingClientRect(), im = c.querySelector(".icone img, .icone canvas");
        const ri = im && im.getBoundingClientRect();
        return { nome: c.querySelector(".carta-nome span").textContent.trim(),
          caixa: [r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top].map(Math.round),
          retrato: ri && { css: [ri.width, ri.height].map((v) => +v.toFixed(2)),
            arquivo: im.currentSrc ? (im.currentSrc.startsWith("data:") ? "data:" + im.currentSrc.length : im.currentSrc) : im.tagName } };
      });
      return { cartas };
    });
    registro[modo].erros = erros;
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1) + "\n");
for (const [k, v] of Object.entries(registro)) console.log(k, JSON.stringify(v.cartas.map((c) => [c.nome, c.retrato])), v.erros);
