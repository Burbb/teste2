// As fotos do Espantalho Possuído (protótipo; nada no jogo), a 1920×945, pelo código real do evento (o espantalho do
// milharal, pelo cenario_excecoes.py de chefes_e_especiais, que força a sorte e põe o herói no nível 5), com os mesmos
// dados em cada modo: "atual" (o jogo: o sprite da planta, pela origem), "t" (a transposição de 16 da rodada anterior,
// no arquivo de 32 que ela teria), "n32" (o estudo nativo de 32) e "n16" (a proposta de 16, no 32 da carta); no refino,
// "n32r" e "n16r" (o quadro mais perto, o chapéu reto e o rosto afunilado). Os desenhos
// entram na carta com o mesmo elemento que o Icones.criatura(…, 32) monta, trocados só na página. Registra a caixa de
// cada carta, o tamanho do retrato na tela e no aparelho, e os erros do console.
//   [MODOS=atual,t,n32,n16,n32r,n16r] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
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
  t: ["../../chefes_e_especiais/proposta/espantalho-t-32.png", "../../chefes_e_especiais/proposta/espantalho-t-32@2x.png"],
  n32: ["../proposta/espantalho-n32-32.png", "../proposta/espantalho-n32-32@2x.png"],
  n16: ["../proposta/espantalho-n16-32.png", "../proposta/espantalho-n16-32@2x.png"],
  n32r: ["../proposta/espantalho-n32r-32.png", "../proposta/espantalho-n32r-32@2x.png"],
  n16r: ["../proposta/espantalho-n16r-32.png", "../proposta/espantalho-n16r-32@2x.png"],
};
const TROCA = Object.fromEntries(Object.entries(PARES).map(([m, [a, b]]) => [m, [url64(a), url64(b)]]));
const TELAS = [{ nome: "100", width: 1920, height: 945, dpr: 1 }];
const MODOS = (process.env.MODOS || "atual,t,n32,n16,n32r,n16r").split(",");
const AMB = { EVENTO: "espantalho", VEZES: "1" };
const EXCECOES = path.join(aqui, "../../chefes_e_especiais/auxiliares/cenario_excecoes.py");
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const arqReg = path.join(saida, "registro.json");
const registro = process.env.MODOS && existsSync(arqReg) ? JSON.parse(readFileSync(arqReg, "utf-8")) : {};  // só os modos pedidos mudam
for (const tela of TELAS) {
  for (const modo of MODOS) {
    const proc = spawn(PY, [EXCECOES, "relatorio"], { cwd: raiz,
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
            if (!n || !ic || !/^Espantalho Possuído/.test(n.textContent.trim())) continue;
            const im = ic.querySelector("img");
            if (!im || im.getAttribute("src") !== src) ic.innerHTML = marca;
          }
        };
        aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true });
      }, TROCA[modo]);
      for (let k = 0; k < 80 && !(await p.$(".inimigos .carta")); k++) {  // o Explorar (que cai no EVENTO) e a escolha
        await p.evaluate(() => {
          if (processando || !pergunta || pergunta.tipo !== "opcoes") return;
          const i = pergunta.opcoes.findIndex((o) => !(o.meta && o.meta.indisponivel));
          if (i >= 0) responder(pergunta.id, i);
        });
        await espera(400);
      }
      await p.waitForSelector(".inimigos .carta", { timeout: 30000 }).catch(() => erros.push("a luta não abriu"));
      await espera(1500);
      await p.locator("#palco").first().screenshot({ path: path.join(saida, `espantalho-${modo}.png`) });
      registro[`${modo}/${tela.nome}`] = await p.evaluate(() => {
        const o = document.querySelector("#palco").getBoundingClientRect(), dpr = window.devicePixelRatio;
        const cartas = [...document.querySelectorAll(".inimigos .carta")].map((c) => {
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
