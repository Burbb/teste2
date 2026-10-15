// O padrão das cartas de combate (experimento): fotografa a luta de verdade com os seis retratos, na versão anterior
// (a carta de 16×16 a 2×) e na candidata (cartas-teste.js, posta na página por cartas-no-jogo.js só aqui; o jogo não
// muda). Três composições alternam o herói e os pares de companheiros (Guerreiro com Morel e Odette, Mago com Yara e
// Morel, Arqueiro com Odette e Yara), em janela normal (1500×950) e baixa (1280×720), com movimento normal e reduzido,
// na vez do herói (a carta dele em foco, o rosto em 32 px exatos e alinhado ao pixel). Mede o rosto e o nicho na tela e
// confere que a tecla 1 ainda abre a mira. Guarda em capturas-cartas/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_cartas.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-cartas");
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
async function recortar(p, sel, nome, folga = 6) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, Math.floor(r.x - f)), y: Math.max(0, Math.floor(r.y - f)), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
const COMPOSICOES = [["guerreiro", "morel,odete"], ["mago", "yara,morel"], ["arqueiro", "odete,yara"]];
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const medidas = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const [classe, com] of COMPOSICOES) {
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", CLASSE: classe, COMITIVA: com, LUTA: "lobo", NIVEL_LUTA: "2", VIDA: "1" });
  for (const jan of Object.keys(JANELAS)) for (const mov of ["normal", "reduzido"]) for (const versao of ["anterior", "candidata"]) {
    const [W, H] = JANELAS[jan];
    const p = await b.newPage({ viewport: { width: W, height: H }, reducedMotion: mov === "reduzido" ? "reduce" : "no-preference" });
    p.on("pageerror", (e) => erros.push(`${classe} ${jan} ${mov} ${versao}: ${e}`));
    p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${classe} ${jan} ${mov} ${versao}: ${m.text()}`); });
    await p.goto(url);
    await p.evaluate((v) => { window.CARTAS = { versao: v }; }, versao);
    for (const f of ["arte-teste.js", "resolucao-teste.js", "cartas-teste.js", "cartas-no-jogo.js"]) await p.addScriptTag({ path: path.join(aqui, f) });
    await vez(p);
    await espera(700);
    const nome = `${classe}-${jan}-${mov}-${versao}`;
    await recortar(p, "#arena .aliados", `${nome}-aliados`, 10);
    await recortar(p, "#arena", `${nome}-arena`, 0);
    const m = await p.evaluate(() => {
      const r = (e) => { const b = e.getBoundingClientRect(); return [+b.x.toFixed(2), +b.y.toFixed(2), +b.width.toFixed(2), +b.height.toFixed(2)]; };
      const h = document.querySelector(".carta.heroi"), ic = h.querySelector(".icone"), im = ic.querySelector("img");
      const comp = [...document.querySelectorAll(".carta:not(.heroi) .icone img.carta-teste")].map((i) => r(i));
      return { foco: h.classList.contains("foco"), nicho: r(ic), rosto: r(im), companheiros: comp };
    });
    // a interação continua: a tecla 1 abre a mira, Esc volta à roda
    await p.keyboard.press("1"); await espera(500);
    const mira = await p.evaluate(() => !!document.querySelector(".carta.alvejavel"));
    await p.keyboard.press("Escape"); await espera(500);
    const voltou = await naVez(p);
    medidas.push({ nome, ...m, mira, voltou }); console.log(nome, JSON.stringify({ ...m, mira, voltou }));
    await p.close();
  }
  proc.kill();
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.js"), `// as medidas de fotografar_cartas.mjs, para cartas-teste.html (um script abre direto do disco; um JSON, não)\nwindow.MEDIDAS = ${JSON.stringify(medidas, null, 1)};\n`);
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
