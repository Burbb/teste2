// Teste do retrato do Guerreiro (experimento): fotografa o jogo de verdade com o retrato de hoje e com o candidato de
// capacete fechado (arte-teste.js, posto na página por retrato-no-jogo.js só aqui; o jogo não muda). Três lugares, cada
// um em janela normal (1500×950) e baixa (1280×720, onde o busto da ficha cai para 64 px): a capela (a ficha e o topo
// ao lado da sala), a banca do mercado (a ficha ao lado do mercador) e uma luta (a carta do herói). Guarda as páginas
// e os recortes em capturas-retrato/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_retrato.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-retrato");
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
/** Na luta, espera a vez do herói (a roda com os botões), passando as orientações e os Continuar do caminho. */
async function vez(p) {
  for (let k = 0; k < 120; k++) {
    const ok = await p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector("#roda .roda-botao"));
    if (ok) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
const caixa = (p, sel, folga = 6) => p.evaluate(([sel, folga]) => {
  const e = document.querySelector(sel); if (!e) return null;
  const r = e.getBoundingClientRect();
  return { x: Math.max(0, r.x - folga), y: Math.max(0, r.y - folga), width: r.width + 2 * folga, height: r.height + 2 * folga };
}, [sel, folga]);
async function recortar(p, sel, nome, folga) {
  const c = await caixa(p, sel, folga);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
  else console.log(`  (sem ${sel} em ${nome})`);
}

const LUGARES = [
  { nome: "capela", cenario: "capela", amb: {}, pronto: parado,
    recortes: [["#heroi .identidade", "ficha", 8], ["#hud", "topo", 4], ["#palco", "capela", 0]] },
  { nome: "mercado", cenario: "mercado", amb: { CLASSE: "guerreiro" }, pronto: parado,
    recortes: [["#heroi .identidade", "ficha", 8], [".loja-banca", "banca", 0], [".loja-topo", "balcao", 4]] },
  { nome: "luta", cenario: "muralha", amb: { NIVEL: "6" }, pronto: vez,
    recortes: [[".carta.heroi", "carta", 6], ["#arena", "arena", 0]] },
];
const JANELAS = [[1500, 950, "normal"], [1280, 720, "baixa"]];
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const lugar of LUGARES) {
  const { proc, url } = await subir(lugar.cenario, lugar.amb);
  for (const [W, H, janela] of JANELAS) {
    for (const versao of ["atual", "candidato"]) {
      const p = await b.newPage({ viewport: { width: W, height: H } });
      p.on("pageerror", (e) => erros.push(`${lugar.nome} ${janela} ${versao}: ${e}`));
      p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${lugar.nome} ${janela} ${versao}: ${m.text()}`); });
      await p.goto(url);
      await lugar.pronto(p);
      if (versao === "candidato") {
        await p.addScriptTag({ path: path.join(aqui, "arte-teste.js") });
        await p.addScriptTag({ path: path.join(aqui, "retrato-no-jogo.js") });
      }
      await espera(1500);
      const base = `${lugar.nome}-${janela}-${versao}`;
      await p.screenshot({ path: path.join(SAIDA, `${base}.png`) });
      for (const [sel, rotulo, folga] of lugar.recortes) await recortar(p, sel, `${base}-${rotulo}`, folga);
      // o que está de fato na tela: o tamanho de cada retrato e se é o candidato
      const medida = await p.evaluate(() => [["ficha", "#heroi .retrato-grande img"], ["topo", ".hud-retrato img"], ["carta", ".carta.heroi .icone img"]]
        .map(([n, s]) => { const i = document.querySelector(s); return i && i.getBoundingClientRect().width ? `${n} ${Math.round(i.getBoundingClientRect().width)}px${i.classList.contains("arte-teste") ? " (candidato)" : ""}` : null; })
        .filter(Boolean).join(", "));
      console.log(`${base}: ${medida}`);
      await p.close();
    }
  }
  proc.kill();
}
await b.close();
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
