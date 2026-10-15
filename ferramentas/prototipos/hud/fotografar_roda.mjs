// O acabamento da roda de ações (experimento): fotografa a roda da luta de verdade (Guerreiro contra um lobo, cenário
// tutorial) em cada estado (parada, mouse em cima, pressionada, Habilidades aberta, Itens aberta, indisponível e foco
// do teclado), em janela normal (1500×950) e baixa (1280×720), em três versões:
//   atual        o jogo como está;
//   icones       os candidatos de itens-icones-teste.js no lugar dos desenhos (itens-icones-no-jogo.js);
//   acabamento   os candidatos e a folha roda-alternativa.css (só nesta página; o jogo não a carrega).
// "Indisponível" é simulado (a classe .bloqueada posta no Fugir, a mesma que o jogo usa), porque esta luta não tem uma
// ação travada. Guarda os recortes em tamanho real em capturas-roda/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_roda.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-roda");
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
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector("#roda .roda-botao"));
async function vez(p) {
  for (let k = 0; k < 160; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
// o recorte: a roda inteira e a janelinha, se aberta, com folga
async function recortar(p, nome) {
  const c = await p.evaluate(() => {
    const els = [...document.querySelectorAll("#roda > *, .roda-janela")].filter((e) => e.offsetParent !== null);
    const rs = els.map((e) => e.getBoundingClientRect()).filter((r) => r.width);
    const x0 = Math.min(...rs.map((r) => r.left)) - 14, y0 = Math.min(...rs.map((r) => r.top)) - 14;
    const x1 = Math.max(...rs.map((r) => r.right)) + 14, y1 = Math.max(...rs.map((r) => r.bottom)) + 14;
    return { x: Math.max(0, Math.floor(x0)), y: Math.max(0, Math.floor(y0)), width: Math.ceil(x1 - Math.max(0, x0)), height: Math.ceil(y1 - Math.max(0, y0)) };
  });
  await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
}
const botao = (p, nome) => p.$(`#roda .roda-botao:has(.rb-nome:text-is("${nome}"))`);
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const { proc, url } = await subir("tutorial", { TUTORIAL: "0", CLASSE: "guerreiro", LUTA: "lobo", NIVEL_LUTA: "2", VIDA: "1" });
try {
  for (const jan of Object.keys(JANELAS)) for (const versao of ["atual", "icones", "acabamento"]) {
    const [W, H] = JANELAS[jan];
    const p = await b.newPage({ viewport: { width: W, height: H } });
    p.on("pageerror", (e) => erros.push(`${jan} ${versao}: ${e}`));
    await p.goto(url);
    if (versao !== "atual") for (const f of ["arte-teste.js", "itens-icones-teste.js", "itens-icones-no-jogo.js"]) await p.addScriptTag({ path: path.join(aqui, f) });
    if (versao === "acabamento") await p.addStyleTag({ path: path.join(aqui, "roda-alternativa.css") });
    await vez(p);
    await p.mouse.move(5, H - 5);
    await espera(700);
    const nome = (estado) => `${jan}-${versao}-${estado}`;
    await recortar(p, nome("parada"));
    await (await botao(p, "Habilidades")).hover(); await espera(250);
    await recortar(p, nome("mouse"));
    const atk = await (await p.$("#roda .roda-botao")).boundingBox();
    await p.mouse.move(atk.x + 22, atk.y + atk.height / 2); await p.mouse.down(); await espera(120);
    await recortar(p, nome("pressionada"));
    await p.mouse.up(); await espera(300); await p.keyboard.press("Escape"); await espera(300);
    await vez(p);
    for (const [acao, estado] of [["Habilidades", "habilidades"], ["Itens", "itens"]]) {
      await (await botao(p, acao)).click(); await espera(400);
      await p.mouse.move(5, H - 5); await espera(200);
      await recortar(p, nome(estado));
      await p.keyboard.press("Escape"); await espera(300);
    }
    await p.evaluate(() => { const f = [...document.querySelectorAll("#roda .roda-botao")].find((e) => /Fugir/.test(e.textContent)); f && f.classList.add("bloqueada"); });
    await espera(150);
    await recortar(p, nome("indisponivel"));
    await p.evaluate(() => document.querySelectorAll("#roda .bloqueada").forEach((e) => e.classList.remove("bloqueada")));
    for (let k = 0; k < 30 && !(await p.evaluate(() => !!document.activeElement.closest(".roda-botao"))); k++) await p.keyboard.press("Tab");
    await p.keyboard.press("Tab"); await espera(250);
    await recortar(p, nome("teclado"));
    console.log(nome("ok"), await p.evaluate(() => (document.activeElement.textContent || "").trim()));
    await p.close();
  }
} finally {
  await b.close(); proc.kill();
}
console.log(erros.length ? erros.join("\n") : "sem erros");
