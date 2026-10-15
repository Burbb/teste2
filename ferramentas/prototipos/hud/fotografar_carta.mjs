// Ajuste da carta pequena do Morel (experimento): fotografa a carta no jogo de verdade, na mesma luta e com os mesmos
// dados, com cada versão (a carta de 16×16 aprovada a 2×, a de 32×32 do experimento anterior, a nova de 32×32 e a
// redução do 40×40 a 32), na vez do herói com a ampliação do jogo (36 px) e com o rosto inteiro (32 px), em janela
// normal (1500×950) e baixa (1280×720), com movimento normal e reduzido; mede o tamanho e a posição do rosto na tela.
// Depois, a carta do Morel como companheiro (32 px, sem foco), e a ficha e o topo na capela com o 80×80 novo.
// O Morel ocupa o lugar do herói só neste teste (resolucao-no-jogo.js). Guarda em capturas-carta/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_carta.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-carta");
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
async function vez(p) {
  for (let k = 0; k < 120; k++) {
    if (await p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector("#roda .roda-botao"))) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
const parado = (p) => p.waitForFunction(() => typeof pergunta !== "undefined" && pergunta && !processando, null, { timeout: 30000 });
async function recortar(p, sel, nome, folga = 6) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, r.x - f), y: Math.max(0, r.y - f), width: r.width + 2 * f, height: r.height + 2 * f } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
const vestir = async (p, R) => {
  await p.evaluate((r) => { window.RESOLUCAO = r; }, R);
  for (const f of ["arte-teste.js", "resolucao-teste.js", "morel-anterior.js", "resolucao-no-jogo.js"]) await p.addScriptTag({ path: path.join(aqui, f) });
  await espera(700);
};
const medir = (p, sel) => p.evaluate((s) => {
  const i = document.querySelector(s); if (!i) return null;
  const r = i.getBoundingClientRect(), carta = i.closest(".carta");
  return { w: +r.width.toFixed(2), h: +r.height.toFixed(2), x: +r.x.toFixed(2), y: +r.y.toFixed(2), nativo: i.naturalWidth,
    foco: carta.classList.contains("foco"), transform: getComputedStyle(carta).transform };
}, sel);
const CARTAS = { "16-aprovada": "morel-ant-carta", "32-anterior": "morel-80-ant-carta", "32-nova": "morel-80-carta", "40-reduzida": "morel-40-32" };
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const medidas = [];
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, mov) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H }, reducedMotion: mov === "reduzido" ? "reduce" : "no-preference" });
  p.on("pageerror", (e) => erros.push(`${jan} ${mov}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${jan} ${mov}: ${m.text()}`); });
  await p.goto(url);
  return p;
}
// 1. a carta do herói (o Morel no lugar dele): cada versão, ampliada pelo jogo e inteira
{
  const { proc, url } = await subir("muralha", { NIVEL: "6" });
  const combos = [];
  for (const jan of ["normal", "baixa"]) for (const mov of ["normal", "reduzido"]) for (const c of Object.keys(CARTAS))
    if (c === "32-nova" || c === "32-anterior" || (jan === "normal" && mov === "normal")) combos.push([jan, mov, c]);
  for (const [jan, mov, c] of combos) {
    for (const inteiro of [false, true]) {
      const p = await pagina(url, jan, mov);
      await vez(p);
      await vestir(p, { itens: "32", morel: "80", carta: CARTAS[c], inteiro });
      await espera(500);
      const nome = `heroi-${jan}-${mov}-${c}-${inteiro ? "32px" : "36px"}`;
      await recortar(p, ".carta.heroi", nome, 8);
      const m = await medir(p, ".carta.heroi .icone img");
      medidas.push({ nome, ...m }); console.log(nome, JSON.stringify(m));
      // a interação continua: a tecla 1 abre a mira e o foco sai da carta
      if (c === "32-nova" && mov === "normal") { await p.keyboard.press("1"); await espera(500); await recortar(p, "#arena", `${nome}-mira`, 0); await p.keyboard.press("Escape"); }
      await p.close();
    }
  }
  proc.kill();
}
// 2. a carta do Morel companheiro (o tamanho que ele usa de verdade: 32 px, sem foco)
{
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", COMITIVA: "morel,odete", LUTA: "lobo", NIVEL_LUTA: "2", VIDA: "1" });
  for (const jan of ["normal", "baixa"]) for (const c of Object.keys(CARTAS)) {
    const p = await pagina(url, jan, "normal");
    await vez(p);
    await vestir(p, { itens: "32", morel: "40", comp: CARTAS[c] });
    const nome = `companheiro-${jan}-${c}`;
    await recortar(p, "#arena .aliados", nome, 4);
    const m = await p.evaluate(() => { const i = document.querySelector("#arena .aliados .carta:not(.heroi) img.arte-teste"); if (!i) return null;
      const r = i.getBoundingClientRect(); return { w: r.width, h: r.height, foco: i.closest(".carta").classList.contains("foco") }; });
    medidas.push({ nome, ...m }); console.log(nome, JSON.stringify(m));
    await p.close();
  }
  proc.kill();
}
// 3. o conjunto do 80×80 novo: a ficha e o topo na capela
{
  const { proc, url } = await subir("capela", {});
  for (const jan of ["normal", "baixa"]) {
    const p = await pagina(url, jan, "normal");
    await parado(p);
    await vestir(p, { itens: "32", morel: "80" });
    await recortar(p, "#heroi .identidade", `ficha-${jan}`, 8);
    await recortar(p, ".hud-retrato", `topo-${jan}`, 6);
    await p.screenshot({ path: path.join(SAIDA, `capela-${jan}.png`) });
    await p.close();
  }
  proc.kill();
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.json"), JSON.stringify(medidas, null, 1));
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
