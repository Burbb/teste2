// As fotos dos seis chefes restantes e dos três especiais (protótipo; nada no jogo), a 1920×945 e com os mesmos dados em
// cada modo: cada guardião na luta (CHEFE=, com o nome e a chave dele) com um comum da região; o Espantalho Possuído e o
// Mímico pelo código real dos eventos (cenario_excecoes.py); o servo esquelético na carta aliada (SERVOS=1). Modos:
// "atual" (o jogo), "a" e "b" (as duas propostas de cada), trocados só na página, nas cartas (inimigas e aliadas), pelo
// nome. Nenhum deles entra no Bestiário.
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
  ["^Hidra do Brejo", { a: [P, "hidra-h1"], b: [P, "hidra-h2"] }],
  ["^Dragão de Gelo", { a: [P, "dragao-d1"], b: [P, "dragao-d2"] }],
  ["^Senhor da Guerra", { a: [P, "senhor-s1"], b: [P, "senhor-s2"] }],
  ["^Profeta das Cinzas", { a: [P, "profeta-p1"], b: [P, "profeta-p2"] }],
  ["^Bruxa Afogada", { a: [P, "bruxa-afogada-b1"], b: [P, "bruxa-afogada-b2"] }],
  ["^Lich Menor", { a: [P, "lich-l1"], b: [P, "lich-l2"] }],
  ["^Espantalho Possuído", { a: [P, "espantalho-e1"], b: [P, "espantalho-e2"] }],
  ["^Mímico", { a: [P, "mimico-m1"], b: [P, "mimico-m2"] }],
  ["^Esqueleto \\(Invocado\\)", { a: [P, "servo-sv1"], b: [P, "servo-sv2"] }],
];
const TROCAS = Object.fromEntries(["a", "b"].map((m) =>
  [m, BICHOS.filter(([, ms]) => ms[m]).map(([n, ms]) => [n, dados(...ms[m])])]));
const MODOS = (process.env.MODOS || "atual,a,b").split(",");
const LUTA = { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "5" };
const SITUACOES = [
  { nome: "luta-hidra", cenario: "tutorial", amb: { ...LUTA, GRUPO: "sapo:1", CHEFE: "hidra_do_brejo" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-dragao", cenario: "tutorial", amb: { ...LUTA, GRUPO: "lobo_gelido:1", CHEFE: "dragao_de_gelo" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-senhor", cenario: "tutorial", amb: { ...LUTA, GRUPO: "bandido:1", CHEFE: "senhor_da_guerra" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-profeta", cenario: "tutorial", amb: { ...LUTA, GRUPO: "cultista:1", CHEFE: "profeta_das_cinzas" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-bruxa", cenario: "tutorial", amb: { ...LUTA, GRUPO: "afogado:1", CHEFE: "bruxa_afogada" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "luta-lich", cenario: "tutorial", amb: { ...LUTA, GRUPO: "esqueleto:1", CHEFE: "lich_menor" },
    espera: '.carta[data-uid="j"]', foto: "#palco" },
  { nome: "espantalho", cenario: "relatorio", script: "cenario_excecoes.py", amb: { EVENTO: "espantalho", VEZES: "1" },
    evento: true, espera: ".inimigos .carta", foto: "#palco" },
  { nome: "mimico", cenario: "relatorio", script: "cenario_excecoes.py", amb: { EVENTO: "bau_abandonado", VEZES: "1" },
    evento: true, espera: ".inimigos .carta", foto: "#palco" },
  { nome: "servo", cenario: "tutorial", amb: { ...LUTA, LUTA: "esqueleto", QUANTOS: "1", SERVOS: "1" },
    espera: '.aliados .carta[data-tipo="servo"]', foto: "#palco" },
];
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const arqRegistro = path.join(saida, "registro.json");
const registro = existsSync(arqRegistro) ? JSON.parse(readFileSync(arqRegistro, "utf-8")) : {};
for (const sit of SITUACOES.filter((s) => !process.env.SO || process.env.SO.split(",").includes(s.nome))) {  // SO=: só estas
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
            for (const c of document.querySelectorAll(".inimigos .carta, .aliados .carta")) {
              const n = c.querySelector(".carta-nome span"), im = c.querySelector(".icone img"), ic = c.querySelector(".icone");
              if (!n || !re.test(n.textContent.trim())) continue;
              if (im && im.src !== src) im.src = src;
              else if (!im && ic) ic.innerHTML = `<img src="${src}" width="32" height="32" style="image-rendering:pixelated">`;
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
      if (sit.evento) {
        for (let k = 0; k < 80 && !(await p.$(".inimigos .carta")); k++) {
          await p.evaluate(() => {
            if (processando || !pergunta || pergunta.tipo !== "opcoes") return;
            const i = pergunta.opcoes.findIndex((o) => !(o.meta && o.meta.indisponivel));
            if (i >= 0) responder(pergunta.id, i);
          });
          await espera(400);
        }
      }
      await p.waitForSelector(sit.espera, { timeout: 30000 }).catch(() => erros.push(`não apareceu: ${sit.espera}`));
      await espera(1500);
      const alvo = sit.foto === "body" ? p : p.locator(sit.foto).first();
      await alvo.screenshot({ path: path.join(saida, `${sit.nome}-${modo}.png`) }).catch((e) => erros.push(String(e)));
      const caixas = await p.evaluate((palco) => {
        const o = palco ? document.querySelector("#palco").getBoundingClientRect() : { left: 0, top: 0 };
        return [...document.querySelectorAll(".inimigos .carta, .aliados .carta, .cartao")].map((c) => {
          const r = c.getBoundingClientRect();
          const n = ((c.querySelector(".carta-nome span, b") || {}).textContent || "").trim();
          return { nome: n, lado: c.closest(".aliados") ? "aliado" : "inimigo",
            caixa: [r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top].map(Math.round) };
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
