// Experimento de resolução: fotografa o jogo de verdade com as amostras (resolucao-teste.js, postas na página por
// resolucao-no-jogo.js só aqui; o jogo não muda), em janela normal (1500×950) e baixa (1280×720), nas duas versões:
// "atual" (itens de 32×32, o Morel de 40×40 a 2×) e "maior" (itens de 64×64, o Morel de 80×80 a 1×). Três lugares: a
// capela (a ficha e o topo ao lado da cena), o mercado (o martelo na mochila e a Pena de Fênix na bolsa e na
// prateleira, ao lado dos ícones aprovados; cenário mercado com AMOSTRAS=1) e uma luta (a carta). Guarda em
// capturas-resolucao/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_resolucao.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-resolucao");
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
async function vez(p) {
  for (let k = 0; k < 120; k++) {
    if (await p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector("#roda .roda-botao"))) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
async function recortar(p, sel, nome, folga = 6) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, r.x - f), y: Math.max(0, r.y - f), width: r.width + 2 * f, height: r.height + 2 * f } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
const LUGARES = [
  { nome: "capela", cenario: "capela", amb: {}, pronto: parado, recortes: [["#heroi .identidade", "ficha", 8], ["#hud", "topo", 4]] },
  { nome: "mercado", cenario: "mercado", amb: { CLASSE: "guerreiro", AMOSTRAS: "1" }, pronto: parado,
    recortes: [["#heroi .identidade", "ficha", 8], [".loja-banca", "banca", 0], ["#heroi", "painel", 0]] },
  { nome: "luta", cenario: "muralha", amb: { NIVEL: "6" }, pronto: vez, recortes: [[".carta.heroi", "carta", 6]] },
];
const VERSOES = { atual: { itens: "32", morel: "40" }, maior: { itens: "64", morel: "80" } };
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const lugar of LUGARES) {
  const { proc, url } = await subir(lugar.cenario, lugar.amb);
  for (const [W, H, janela] of [[1500, 950, "normal"], [1280, 720, "baixa"]]) {
    for (const [versao, R] of Object.entries(VERSOES)) {
      const p = await b.newPage({ viewport: { width: W, height: H } });
      p.on("pageerror", (e) => erros.push(`${lugar.nome} ${janela} ${versao}: ${e}`));
      p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${lugar.nome} ${janela} ${versao}: ${m.text()}`); });
      await p.goto(url);
      await lugar.pronto(p);
      await p.evaluate((r) => { window.RESOLUCAO = r; }, R);
      await p.addScriptTag({ path: path.join(aqui, "arte-teste.js") });
      await p.addScriptTag({ path: path.join(aqui, "resolucao-teste.js") });
      await p.addScriptTag({ path: path.join(aqui, "resolucao-no-jogo.js") });
      await espera(1200);
      const base = `${lugar.nome}-${janela}-${versao}`;
      await p.screenshot({ path: path.join(SAIDA, `${base}.png`) });
      for (const [sel, rot, folga] of lugar.recortes) await recortar(p, sel, `${base}-${rot}`, folga);
      if (lugar.nome === "mercado") {  // a aba Vender: o martelo na mochila, ao lado das armas com ícone aprovado
        const aba = await p.$('[data-aba="vender"], [role="tab"]:has-text("Vender"), button:has-text("Vender")');
        if (aba) { await aba.click(); await espera(800); await p.screenshot({ path: path.join(SAIDA, `${base}-vender.png`) }); await recortar(p, "#lista-vender", `${base}-vender-lista`, 4); }
        else console.log("  (sem a aba Vender)");
      }
      const medida = await p.evaluate(() => [...document.querySelectorAll("img.arte-teste")].map((i) => `${Math.round(i.getBoundingClientRect().width)}`).join(" "));
      console.log(`${base}: amostras na tela (px) ${medida}`);
      await p.close();
    }
  }
  proc.kill();
}
await b.close();
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
