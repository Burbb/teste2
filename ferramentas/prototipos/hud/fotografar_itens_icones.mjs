// O experimento de itens e ícones no jogo de verdade: o Guerreiro no Vau do Turvo com a vitrine (cenário tutorial,
// VITRINE=1: machado, espada, escudo e anel na mochila, escudo e anel vestidos, unguento e bomba de fumaça na bolsa),
// com os desenhos atuais e com os candidatos (itens-icones-no-jogo.js, posto só nesta página; o jogo não muda).
// Fotografa a ficha, a doca, o Inventário, o Mercado, a janelinha de Itens na luta e a tela inteira perto da capela, em
// janela normal (1500×950) e baixa (1280×720). Guarda em capturas-itens-icones/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_itens_icones.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-itens-icones");
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
async function ate(p, sel) {
  for (let k = 0; k < 60 && !(await p.$(sel)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(900);
}
async function foto(p, sel, nome) {
  await p.mouse.move(2, 2); await espera(250);
  const c = sel && await p.evaluate((s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return { x: Math.floor(r.left), y: Math.floor(r.top), width: Math.ceil(r.width), height: Math.ceil(r.height) }; }, sel);
  await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), ...(c ? { clip: c } : {}) });
}
async function vestir(p, versao) {
  if (versao === "candidatos") for (const f of ["arte-teste.js", "itens-icones-teste.js", "itens-icones-no-jogo.js"]) await p.addScriptTag({ path: path.join(aqui, f) });
  await espera(300);
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const base = { TUTORIAL: "0", VITRINE: "1", VISTAS: "A1,V2,N1,D1,K1,M1", OURO: "200" };
for (const jan of Object.keys(JANELAS)) for (const versao of ["atual", "candidatos"]) {
  const [W, H] = JANELAS[jan], n = (c) => `${jan}-${versao}-${c}`;
  // a vila: ficha, doca, Inventário, Mercado
  {
    const { proc, url } = await subir("tutorial", base);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    p.on("pageerror", (e) => erros.push(`${jan} ${versao}: ${e}`));
    await p.goto(url); await vestir(p, versao);
    await ate(p, "#predios .predio");
    await foto(p, "#heroi", n("ficha"));
    await foto(p, "#doca", n("doca"));
    await (await p.$('#doca .atalho[data-rotulo="Inventário"]')).click(); await espera(1200);
    await foto(p, "#cena", n("mochila"));
    await p.keyboard.press("Escape"); await espera(900);
    await ate(p, "#predios .predio");
    await (await p.$('#predios .predio[data-predio="mercado"]')).click(); await espera(1500);
    await foto(p, "#cena", n("mercado"));
    await p.close(); proc.kill();
  }
  // perto da capela: a tela inteira
  {
    const { proc, url } = await subir("tutorial", { ...base, LUGAR: "capela" });
    const p = await b.newPage({ viewport: { width: W, height: H } });
    p.on("pageerror", (e) => erros.push(`${jan} ${versao} capela: ${e}`));
    await p.goto(url); await vestir(p, versao);
    await ate(p, "#prompt .escolha");
    await foto(p, null, n("capela"));
    await p.close(); proc.kill();
  }
  // a luta: a janelinha de Itens
  {
    const { proc, url } = await subir("tutorial", { ...base, LUTA: "lobo", NIVEL_LUTA: "2", VIDA: "0.6" });
    const p = await b.newPage({ viewport: { width: W, height: H } });
    p.on("pageerror", (e) => erros.push(`${jan} ${versao} luta: ${e}`));
    await p.goto(url); await vestir(p, versao);
    await ate(p, "#roda .roda-botao");
    await (await p.$('#roda .roda-botao:has(.rb-nome:text-is("Itens"))')).click(); await espera(500);
    await foto(p, "#palco", n("luta-itens"));
    await p.close(); proc.kill();
  }
  console.log(jan, versao, "ok");
}
await b.close();
console.log(erros.length ? erros.join("\n") : "sem erros");
