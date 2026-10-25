// Fotografa as faixas no jogo de verdade (cenarios_faixas.py): a de hoje, A e B, com os mesmos dados, a 1920×945 e a
// 1280×720, no meio da faixa (depois da entrada). Mede, em cada uma: se a faixa fica dentro do palco (sem passar das
// colunas), se o título cabe numa linha e o tamanho do subtítulo. Guarda ../capturas/<janela>-<versão>-<caso>.png e
// ../capturas/medidas.json.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/faixas/auxiliares/fotografar.mjs
// (VERSOES=atual,a,b; CASOS=vitoria,sequencia,...; JANELAS=1920,1280; NOME_ATUAL=jogo: o nome das fotos do jogo)
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const FAIXA = ".faixa-festa, .fx-faixa";

async function subir(caso, proposta) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_faixas.py"), caso],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: proposta } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => { if (process.env.LOG) process.stderr.write(`[faixas] ${d}`); });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o caso ${caso} não subiu`);
  return { proc, url };
}
async function escolher(p, texto) {
  for (let k = 0; k < 80; k++) {
    const e = await p.$(`${MENU}:has-text("${texto}")`);
    if (e) { await e.click(); return true; }
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
    await espera(250);
  }
  return false;
}
// ataca até a luta acabar (o golpe pode errar): para quando aparece uma faixa ou a roda some de vez
async function atacar(p) {
  for (let k = 0; k < 15; k++) {
    const b = await p.waitForSelector('#roda .roda-botao[data-slot="atacar"]', { timeout: 8000 }).catch(() => null);
    if (!b || (await p.$(".faixa-festa, .fx-faixa"))) return;
    await b.click().catch(() => {});
    await p.mouse.move(2, 2);
    for (let t = 0; t < 20 && !(await p.$(".faixa-festa, .fx-faixa")) && !(await p.$('#roda .roda-botao[data-slot="atacar"]')); t++) await espera(150);
    if (await p.$(".faixa-festa, .fx-faixa")) return;
  }
}
// espera uma faixa com `texto` aparecer, deixa a entrada acabar e mede
async function faixa(p, texto, depois = 520) {
  const h = await p.waitForFunction((t) => [...document.querySelectorAll(".faixa-festa, .fx-faixa")].find((e) => e.textContent.includes(t)), texto, { timeout: 30000, polling: 30 });
  await espera(depois);
  return p.evaluate((el) => {
    if (!el.isConnected) return null;
    const r = el.getBoundingClientRect(), c = document.getElementById("cena").getBoundingClientRect();
    const tit = el.querySelector("b"), sub = el.querySelector(".fa-sub, .fb-sub, .fr-sub, .faixa-festa > span");
    return { caixa: [r.left, r.top, r.width, r.height].map(Math.round), palco: [c.left, c.width].map(Math.round),
      dentro: r.left >= c.left - 1 && r.right <= c.right + 1,
      tituloUmaLinha: tit ? tit.getBoundingClientRect().height < parseFloat(getComputedStyle(tit).fontSize) * 1.6 : null,
      tituloPx: tit ? parseFloat(getComputedStyle(tit).fontSize) : null, subPx: sub ? parseFloat(getComputedStyle(sub).fontSize) : null };
  }, h);
}

const PASSOS = {  // o que fazer na página e as faixas que vêm (o texto que as acha, o nome da foto)
  vitoria: { fazer: async (p) => { await escolher(p, "Começar"); await atacar(p); }, faixas: [["Vitória", "vitoria"]] },
  sequencia: { fazer: async (p) => { await escolher(p, "Começar"); await atacar(p); }, faixas: [["Guardião", "guardiao"], ["Mestre caçador", "mestre"]] },
  queda: { fazer: async (p) => { await escolher(p, "Começar"); await atacar(p); }, faixas: [["Você", "queda"]] },
  comitiva: { fazer: async (p) => { await escolher(p, "Começar"); }, faixas: [["se junta", "comitiva"]] },
  exausto_mato: { fazer: async (p) => { await escolher(p, "Começar"); }, faixas: [["Exausto", "exausto"]] },
  exausto_vila: { fazer: async (p) => { await escolher(p, "Começar"); }, faixas: [["Exausto", "exausto-vila"]] },
  exausto_capela: { fazer: async (p) => { await escolher(p, "Começar"); }, faixas: [["Exausto", "exausto-capela"]] },
  saindo: { fazer: async (p) => { await escolher(p, "Sair e acampar"); }, faixas: [["Saindo", "saindo"]] },
};

const arq = path.join(SAIDA, "medidas.json");
const medidas = existsSync(arq) ? JSON.parse(readFileSync(arq, "utf8")).medidas : {};
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  for (const caso of (process.env.CASOS || Object.keys(PASSOS).join(",")).split(",")) {
    for (const v of (process.env.VERSOES || "atual,a,b").split(",")) {
      const nv = v === "atual" ? (process.env.NOME_ATUAL || "atual") : v;  // NOME_ATUAL=jogo: o jogo depois de uma integração
      const { proc, url } = await subir(caso, v === "atual" ? "" : v);
      const p = await b.newPage({ viewport: { width: W, height: H } });
      p.on("pageerror", (e) => erros.push(`${jan}-${v}-${caso}: ${e}`));
      try {
        await p.goto(url);
        await PASSOS[caso].fazer(p);
        for (const [texto, nome] of PASSOS[caso].faixas) {
          const m = await faixa(p, texto);
          await p.mouse.move(2, 2);
          await p.screenshot({ path: path.join(SAIDA, `${jan}-${nv}-${nome}.png`) });
          medidas[`${jan}-${nv}-${nome}`] = m;
          console.log(jan, nv, nome, JSON.stringify(m));
        }
      } catch (e) { erros.push(`${jan}-${v}-${caso}: ${e.message.split("\n")[0]}`); console.log("  erro", jan, v, caso, e.message.split("\n")[0]); }
      await p.close(); proc.kill();
    }
  }
}
await b.close();
writeFileSync(arq, JSON.stringify({ medidas, erros }, null, 1));
console.log(erros.length ? erros : "sem erros");
