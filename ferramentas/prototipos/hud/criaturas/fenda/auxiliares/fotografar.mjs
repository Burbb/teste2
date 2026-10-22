// As fotos do Cão infernal e da Cria do Vazio (protótipo; nada no jogo), a 1920×945 e com os mesmos dados em cada modo:
// a luta do cão (com o lobo gélido, um caído e o xamã), a luta das crias (com o espectro e um cultista), as crias
// invocadas pelo antagonista (cenario_vazio.py, ANTAGONISTA=1) e o Bestiário. Modos: "atual" (o jogo), "a" e "b" (as
// propostas A e B das duas; "c", a segunda passada: a Cria A2 e o Cão T; "d", o Cão N, com a
// Cria A2, que está no jogo desde a 1.185.0; "e", o Cão N2, o retoque do rosto; "f", "g" e "h", os
// rosnados RA, RB e RC; "i", a RA2, a boca da RA refeita), trocados só na página, nas cartas inimigas e nos cartões do Bestiário, pelo nome.
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
// cada criatura: o nome na carta (a cria invocada leva a letra e "(invocado)" depois) e o desenho de cada modo
const P = "../proposta";
const BICHOS = [
  ["^Cão infernal", { a: [P, "cao-infernal-a"], b: [P, "cao-infernal-b"], c: [P, "cao-infernal-t"], d: [P, "cao-infernal-n"], e: [P, "cao-infernal-n2"], f: [P, "cao-infernal-ra"],
    g: [P, "cao-infernal-rb"], h: [P, "cao-infernal-rc"], i: [P, "cao-infernal-ra2"] }],
  ["^Cria do Vazio", { a: [P, "cria-vazio-a"], b: [P, "cria-vazio-b"], c: [P, "cria-vazio-a2"], d: [P, "cria-vazio-a2"], e: [P, "cria-vazio-a2"], f: [P, "cria-vazio-a2"],
    g: [P, "cria-vazio-a2"], h: [P, "cria-vazio-a2"], i: [P, "cria-vazio-a2"] }],
];
const TROCAS = Object.fromEntries(["a", "b", "c", "d", "e", "f", "g", "h", "i"].map((m) => [m, BICHOS.map(([n, ms]) => [n, dados(...ms[m])])]));
const MODOS = (process.env.MODOS || "atual,a,b").split(",");
const LUTA = { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "4" };
const SITUACOES = [
  { nome: "luta-cao", cenario: "tutorial", amb: { ...LUTA, GRUPO: "cao_infernal:1,lobo_gelido:1,caido:1,xama_caido:1" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-cria", cenario: "tutorial", amb: { ...LUTA, GRUPO: "cria_vazio:2,espectro:1,cultista:1" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-invocada", cenario: "tutorial", script: "cenario_vazio.py", amb: { ...LUTA, NIVEL_LUTA: "6", GRUPO: "cria_vazio:1", ANTAGONISTA: "1" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila",
    BESTIARIO: "cao_infernal:2,cria_vazio:2,lobo:2,lobo_gelido:2,caido:3,xama_caido:2,espectro:2,cultista:2" },
    passos: ["b"], espera: ".cartao .cab", foto: "body" },
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
