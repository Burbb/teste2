// As fotos da rodada depois do Caído CA (protótipo; nada no jogo), a 1920×945 e com os mesmos dados em cada modo: uma
// luta (o Arqueiro com o Falcão Peregrino do lado; dois caídos com o retrato de produção e o xamã) e o Bestiário. Modos:
// "atual" (o jogo), "antes" (o GA, a HA e o XA da rodada anterior), "a", "b" e "c" (o GA2 nos três; a H1, H2, H3; o
// X1, X2, X3) e "d", a segunda rodada (o GA3, a Harpia T e o X1r), trocados só na página, nas cartas inimigas e nos
// cartões do Bestiário, pelo nome.
//   [MODOS=atual,a,b] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.dirname(fileURLToPath(import.meta.url));
const dados = (pasta, id) => "data:image/png;base64," + readFileSync(path.join(aqui, pasta, `${id}-16.png`)).toString("base64");
// cada criatura: o nome na carta e o desenho de cada modo
const P = "../proposta";
const BICHOS = [
  ["^Grifo", { antes: ["../../harpia_grifo/proposta", "grifo-ga"], a: [P, "grifo-ga2"], b: [P, "grifo-ga2"], c: [P, "grifo-ga2"], d: [P, "grifo-ga3"] }],
  ["^Harpia", { antes: ["../../harpia_grifo/proposta", "harpia-ha"], a: [P, "harpia-h1"], b: [P, "harpia-h2"], c: [P, "harpia-h3"], d: [P, "harpia-t"] }],
  ["^Xamã", { antes: ["../../caidos/proposta", "xama-caido-xa"], a: [P, "xama-caido-x1"], b: [P, "xama-caido-x2"], c: [P, "xama-caido-x3"], d: [P, "xama-caido-x1r"] }],
];
const TROCAS = Object.fromEntries(["antes", "a", "b", "c", "d"].map((m) => [m, BICHOS.map(([n, ms]) => [n, dados(...ms[m])])]));
const MODOS = (process.env.MODOS || "atual,antes,a,b,c").split(",");
const GRUPO = "harpia:1,grifo:1,caido:2,xama_caido:1";
const SITUACOES = [
  { nome: "luta", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "arqueiro", NIVEL: "4", ESPEC: "patrulheiro", ANIMAL: "falcao", NIVEL_LUTA: "4", GRUPO }, espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila",
    BESTIARIO: "harpia:2,grifo:2,caido:3,xama_caido:2,bruxa_brejo:2,cultista:2" }, passos: ["b"], espera: ".cartao .cab", foto: "body" },
];
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const arqRegistro = path.join(saida, "registro.json");
const registro = existsSync(arqRegistro) ? JSON.parse(readFileSync(arqRegistro, "utf-8")) : {};
for (const sit of SITUACOES) {
  for (const modo of MODOS) {
    const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
      env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...sit.amb } });
    let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
    for (let k = 0; k < 300 && !url; k++) await espera(100);
    try {
      const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
      const erros = [];
      p.on("pageerror", (e) => erros.push(String(e)));
      p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") erros.push(m.text()); });
      await p.goto(url);
      await espera(2500);
      if (TROCAS[modo]) await p.evaluate((troca) => {
        const aplica = () => {
          for (const [padrao, src] of troca) {
            const re = new RegExp(padrao);
            for (const c of document.querySelectorAll(".inimigos .carta")) {
              const n = c.querySelector(".carta-nome span"), im = c.querySelector(".icone img");
              if (n && im && re.test(n.textContent.trim()) && im.src !== src) im.src = src;
            }
            for (const c of document.querySelectorAll(".cartao")) {
              const n = c.querySelector("b"), im = c.querySelector(".cab img");
              if (n && im && re.test(n.textContent.trim()) && im.src !== src) im.src = src;
            }
          }
        };
        aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true, characterData: true });
      }, TROCAS[modo]);
      for (const tecla of sit.passos || []) { await p.keyboard.press(tecla); await espera(1500); }
      await p.waitForSelector(sit.espera, { timeout: 30000 }).catch(() => erros.push(`não apareceu: ${sit.espera}`));
      await espera(1500);
      const alvo = sit.foto === "body" ? p : p.locator(sit.foto).first();
      await alvo.screenshot({ path: path.join(saida, `${sit.nome}-${modo}.png`) }).catch((e) => erros.push(String(e)));
      const caixas = await p.evaluate((palco) => {
        const o = palco ? document.querySelector("#palco").getBoundingClientRect() : { left: 0, top: 0 };
        return [...document.querySelectorAll(".inimigos .carta, .cartao")].map((c) => {
          const r = c.getBoundingClientRect();
          const n = ((c.querySelector(".carta-nome span, b") || {}).textContent || "").trim();
          return { nome: n, caixa: [r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top].map(Math.round) };
        });
      }, sit.foto === "#palco");
      registro[`${sit.nome}/${modo}`] = { erros, caixas };
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
writeFileSync(arqRegistro, JSON.stringify(registro, null, 1));
for (const [k, v] of Object.entries(registro)) console.log(k, v.caixas.length, "cartas", v.erros);
