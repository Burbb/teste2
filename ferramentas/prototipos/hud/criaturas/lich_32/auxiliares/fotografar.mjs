// As fotos do Lich Menor em 32 nativos e em 16 (protótipo; nada no jogo), a 1920×945, com os mesmos dados em cada modo:
// o guardião na luta (CHEFE=lich_menor) com um Esqueleto inimigo e o servo aliado do Erguer Servo (o cenario_lich.py de
// chefes_e_especiais), os dois com os retratos de produção. Modos: "atual" (o jogo), "l1b" (a base de identidade, o 16
// ×2), "n32" (o estudo nativo de 32) e "n16" (a adaptação, no 32 da carta), trocados só na página, só na carta do Lich.
//   [MODOS=atual,l1b,n32,n16] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.dirname(fileURLToPath(import.meta.url));
const url64 = (arq) => "data:image/png;base64," + readFileSync(path.join(aqui, arq)).toString("base64");
const PARES = {
  l1b: ["../../chefes_e_especiais/proposta/lich-l1b-32.png", "../../chefes_e_especiais/proposta/lich-l1b-32@2x.png"],
  n32: ["../proposta/lich-n32-32.png", "../proposta/lich-n32-32@2x.png"],
  n16: ["../proposta/lich-n16-32.png", "../proposta/lich-n16-32@2x.png"],
};
const TROCA = Object.fromEntries(Object.entries(PARES).map(([m, [a, b]]) => [m, [url64(a), url64(b)]]));
const TELAS = [{ nome: "100", width: 1920, height: 945, dpr: 1 }];
const MODOS = (process.env.MODOS || "atual,l1b,n32,n16").split(",");
const AMB = { TUTORIAL: "0", CLASSE: "mago", NIVEL_LUTA: "5", GRUPO: "esqueleto:1", CHEFE: "lich_menor" };
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const arqReg = path.join(saida, "registro.json");
const registro = process.env.MODOS && existsSync(arqReg) ? JSON.parse(readFileSync(arqReg, "utf-8")) : {};  // só os modos pedidos mudam
for (const tela of TELAS) {
  for (const modo of MODOS) {
    const proc = spawn(PY, [path.join(aqui, "../../chefes_e_especiais/auxiliares/cenario_lich.py"), "tutorial"], { cwd: raiz,
      env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...AMB } });
    let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
    for (let k = 0; k < 300 && !url; k++) await espera(100);
    try {
      const p = await b.newPage({ viewport: { width: tela.width, height: tela.height }, deviceScaleFactor: tela.dpr });
      const erros = [];
      p.on("pageerror", (e) => erros.push(String(e)));
      p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") erros.push(m.text()); });
      await p.goto(url);
      await espera(2500);
      if (TROCA[modo]) await p.evaluate(([src, src2]) => {
        const marca = `<img class="sprite desenho" src="${src}" srcset="${src2} 2x" width="32" height="32" style="--s:32" alt="" draggable="false">`;
        const aplica = () => {
          for (const c of document.querySelectorAll(".inimigos .carta")) {
            const n = c.querySelector(".carta-nome span"), ic = c.querySelector(".icone");
            if (!n || !ic || !/^Lich Menor/.test(n.textContent.trim())) continue;
            const im = ic.querySelector("img");
            if (!im || im.getAttribute("src") !== src) ic.innerHTML = marca;
          }
        };
        aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true });
      }, TROCA[modo]);
      await p.waitForSelector('.aliados .carta[data-tipo="servo"]', { timeout: 30000 }).catch(() => erros.push("o servo não apareceu"));
      await espera(1500);
      await p.locator("#palco").first().screenshot({ path: path.join(saida, `luta-lich-${modo}.png`) });
      registro[`${modo}/${tela.nome}`] = await p.evaluate(() => {
        const o = document.querySelector("#palco").getBoundingClientRect(), dpr = window.devicePixelRatio;
        const cartas = [...document.querySelectorAll(".aliados .carta, .inimigos .carta")].map((c) => {
          const r = c.getBoundingClientRect(), im = c.querySelector(".icone img, .icone canvas");
          const ri = im && im.getBoundingClientRect();
          return { nome: c.querySelector(".carta-nome span").textContent.trim(),
            caixa: [r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top].map(Math.round),
            retrato: ri && { css: [ri.width, ri.height].map((v) => +v.toFixed(2)), aparelho: [ri.width * dpr, ri.height * dpr].map((v) => +v.toFixed(2)),
              arquivo: im.currentSrc ? (im.currentSrc.startsWith("data:") ? "data:" + im.currentSrc.length : im.currentSrc) : im.tagName } };
        });
        return { dpr, cartas };
      });
      registro[`${modo}/${tela.nome}`].erros = erros;
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1) + "\n");
for (const [k, v] of Object.entries(registro)) console.log(k, JSON.stringify(v.cartas.map((c) => [c.nome, c.retrato])), v.erros);
