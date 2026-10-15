// Teste dos retratos das três classes (experimento): fotografa o jogo de verdade com o Guerreiro aprovado e os
// candidatos de Mago e Arqueiro (arte-teste.js, postos na página por retrato-no-jogo.js só aqui; o jogo não muda).
// Para cada classe, em janela normal (1500×950) e baixa (1280×720, onde o busto da ficha cai para 64 px): a ficha e o
// topo ao lado da capela e da vila (fotografias paradas) e a luta, na vez do herói (a carta cresce) e com a mira aberta
// pelo teclado (interações). Guarda as páginas e os recortes em capturas-retratos-classes/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_retratos_classes.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-retratos-classes");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(cenario, amb = {}) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 150 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const parado = (p) => p.waitForFunction(() => typeof pergunta !== "undefined" && pergunta && !processando, null, { timeout: 30000 });
const fechar = async (p) => { for (let k = 0; k < 6; k++) { const e = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (!e) break; await e.click().catch(() => {}); await espera(250); } };
async function vez(p) {
  for (let k = 0; k < 160; k++) {
    await fechar(p);
    if (await p.evaluate(() => pergunta && !processando && !!document.querySelector("#roda .roda-botao"))) return true;
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
    await espera(250);
  }
  return false;
}
const caixa = (p, sel, folga = 6) => p.evaluate(([sel, folga]) => {
  const e = document.querySelector(sel); if (!e) return null;
  const r = e.getBoundingClientRect();
  return { x: Math.max(0, r.x - folga), y: Math.max(0, r.y - folga), width: r.width + 2 * folga, height: r.height + 2 * folga };
}, [sel, folga]);
async function recortar(p, sel, nome, folga) { const c = await caixa(p, sel, folga); if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); }
const medir = (p) => p.evaluate(() => [["ficha", "#heroi .retrato-grande img"], ["topo", ".hud-retrato img"], ["carta", ".carta.heroi .icone img"]]
  .map(([n, s]) => { const i = document.querySelector(s); const r = i && i.getBoundingClientRect();
    return r && r.width ? `${n} ${Math.round(r.width)}px${i.classList.contains("arte-teste") ? "" : " (sem candidato)"}` : null; }).filter(Boolean).join(", "));

const CLASSES = {
  guerreiro: { luta: ["muralha", { NIVEL: "6" }] },
  mago: { luta: ["combate", {}] },
  arqueiro: { luta: ["tiro_duplo", {}] },
};
const JANELAS = [[1500, 950, "normal"], [1280, 720, "baixa"]];
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, W, H) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(String(e)));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(m.text()); });
  await p.goto(url);
  return p;
}
const vestir = async (p) => {
  await p.addScriptTag({ path: path.join(aqui, "arte-teste.js") });
  await p.addScriptTag({ path: path.join(aqui, "retrato-no-jogo.js") });
  await espera(600);
};
for (const [classe, def] of Object.entries(CLASSES)) {
  for (const [W, H, janela] of JANELAS) {
    // parado: a ficha e o topo ao lado da capela e da vila
    for (const [lugar, cen, amb] of [["capela", "capela", { CLASSE: classe }], ["vila", "tutorial", { CLASSE: classe, TUTORIAL: "0" }]]) {
      const { proc, url } = await subir(cen, amb);
      const p = await pagina(url, W, H);
      await parado(p); await espera(1200); await fechar(p);
      await vestir(p);
      const base = `${classe}-${lugar}-${janela}`;
      await p.screenshot({ path: path.join(SAIDA, `${base}.png`) });
      await recortar(p, "#heroi .identidade", `${base}-ficha`, 8);
      await recortar(p, "#hud", `${base}-topo`, 4);
      console.log(`${base} (parado): ${await medir(p)}`);
      await p.close(); proc.kill();
    }
    // a luta: a vez do herói (a carta cresce) e a mira aberta pelo teclado
    const [cen, amb] = def.luta;
    const { proc, url } = await subir(cen, amb);
    const p = await pagina(url, W, H);
    await parado(p).catch(() => {});
    await vestir(p);
    const naVez = await vez(p);
    await espera(900);
    const base = `${classe}-luta-${janela}`;
    await p.screenshot({ path: path.join(SAIDA, `${base}-vez.png`) });
    await recortar(p, ".carta.heroi", `${base}-carta-vez`, 6);
    const tam = await p.evaluate(() => { const i = document.querySelector(".carta.heroi .icone img"); return i ? Math.round(i.getBoundingClientRect().width) : 0; });
    console.log(`${base} (interação: vez do herói ${naVez ? "chegou" : "não chegou"}): ${await medir(p)}; carta na vez ${tam}px`);
    await p.keyboard.press("1"); await espera(800);
    await p.screenshot({ path: path.join(SAIDA, `${base}-mira.png`) });
    console.log(`${base} (interação: tecla 1, a mira): ${await medir(p)}`);
    await p.close(); proc.kill();
  }
}
await b.close();
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
