// As fotos da Árvore Anciã e do Golem Primordial (protótipo; nada no jogo), a 1920×945 e com os mesmos dados em cada
// modo: a luta de cada guardião (CHEFE=, com o nome e a chave dele) junto do comum correspondente (a árvore desperta, o
// golem de pedra) e de outro da região. Modos: "atual" (o jogo), "a" (AA1 e GP1) e "b" (AA2 e GP2), trocados só na
// página, nas cartas inimigas, pelo nome; na segunda rodada, "r1", "r2" e "r3" (as três tentativas de copiar cada
// referência em close) e "r2a", "r2b" e "r2c" (as variações da R2). Os guardiões não entram no Bestiário.
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
  ["^Árvore Anciã", { a: [P, "anciaa-aa1"], b: [P, "anciaa-aa2"], r1: [P, "anciaa-r1"], r2: [P, "anciaa-r2"],
    r3: [P, "anciaa-r3"], r2a: [P, "anciaa-r2a"], r2b: [P, "anciaa-r2b"], r2c: [P, "anciaa-r2c"] }],
  ["^Golem Primordial", { a: [P, "primordial-gp1"], b: [P, "primordial-gp2"], r1: [P, "primordial-r1"],
    r2: [P, "primordial-r2"], r3: [P, "primordial-r3"],
    r2a: [P, "primordial-r2a"], r2b: [P, "primordial-r2b"], r2c: [P, "primordial-r2c"] }],
];
const TROCAS = Object.fromEntries(["a", "b", "r1", "r2", "r3", "r2a", "r2b", "r2c"].map((m) =>
  [m, BICHOS.filter(([, ms]) => ms[m]).map(([n, ms]) => [n, dados(...ms[m])])]));
const MODOS = (process.env.MODOS || "atual,a,b").split(",");
const LUTA = { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "5" };
const SITUACOES = [
  { nome: "luta-anciaa", cenario: "tutorial", amb: { ...LUTA, GRUPO: "ent_jovem:1,lobo:1", CHEFE: "ent_anciao" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-primordial", cenario: "tutorial", amb: { ...LUTA, GRUPO: "golem:1,esqueleto:1", CHEFE: "golem_primordial" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
];
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const arqRegistro = path.join(saida, "registro.json");
const registro = existsSync(arqRegistro) ? JSON.parse(readFileSync(arqRegistro, "utf-8")) : {};
for (const sit of SITUACOES) {
  for (const modo of MODOS) {
    const proc = spawn(PY, sit.script ? [path.join(aqui, sit.script), sit.cenario] : ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
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
