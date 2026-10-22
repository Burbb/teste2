// A conferência da integração da Harpia e do Xamã Caído (1.184.0), com os arquivos de produção e nada trocado na
// página, a 1920×945: a harpia junto do grifo e o xamã junto dos caídos (e do cão infernal, que continua no sprite de
// demônio), o Bestiário e os contratos de caça (o rastreador e o cartaz do mural). Antes servia ao Grifo (1.183.0,
// capturas-1183/); a 1.184.0 grava em capturas-1184/.
// Registra o arquivo de cada retrato e de cada motivo e qualquer pedido à pasta ferramentas/ (não pode haver).
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar_jogo.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
mkdirSync(saida, { recursive: true });
const ler = () => [...document.querySelectorAll(".inimigos .carta")].map((c) => `${c.querySelector(".carta-nome span").textContent.trim()}: ${(c.querySelector(".icone img") || {}).src || "(sprite)"}`);
const SITUACOES = [
  { nome: "luta-harpia", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "arqueiro", NIVEL_LUTA: "4", GRUPO: "harpia:2,grifo:1" },
    espera: '.carta[data-uid="j"]', ler },
  { nome: "luta-xama", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "4", GRUPO: "caido:3,xama_caido:1,cao_infernal:1" },
    espera: '.carta[data-uid="j"]', ler },
  { nome: "bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila",
    BESTIARIO: "harpia:3,grifo:3,caido:5,xama_caido:2,cao_infernal:2,cultista:2" },
    passos: ["b"], espera: ".cartao .cab",
    ler: () => [...document.querySelectorAll(".cartao")].map((c) => `${c.querySelector("b").textContent.trim()}: ${(c.querySelector(".cab img") || {}).src}`) },
  { nome: "contratos", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila", CONTRATOS: "harpia,xama_caido" },
    espera: "#predios .predio", mural: true,
    ler: () => [...document.querySelectorAll("img")].filter((i) => /retrato-/.test(i.src)).map((i) => `${i.closest(".contrato, aside, section")?.className || i.parentElement.className}: ${i.src} ${i.width}`) },
];
const b = await chromium.launch();
const arqReg = path.join(saida, "registro.json");
const registro = process.env.SO && existsSync(arqReg) ? JSON.parse(readFileSync(arqReg, "utf-8")) : {};
for (const sit of SITUACOES.filter((s) => !process.env.SO || process.env.SO.split(",").includes(s.nome))) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...sit.amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
    const erros = [], ferramentas = [];
    p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
    p.on("request", (r) => { if (/ferramentas|prototipos/.test(r.url())) ferramentas.push(r.url()); });
    await p.goto(url);
    await espera(2500);
    for (const tecla of sit.passos || []) { await p.keyboard.press(tecla); await espera(1500); }
    await p.waitForSelector(sit.espera, { timeout: 30000 }).catch(() => erros.push(`não apareceu: ${sit.espera}`));
    if (sit.mural) {
      await espera(800);
      await p.screenshot({ path: path.join(saida, `${sit.nome}-rastreador.png`), clip: { x: 1490, y: 330, width: 330, height: 200 } });
      await p.click('#predios .predio[data-predio="mural"]').catch((e) => erros.push(String(e)));
      await p.waitForSelector(".contrato.ativo", { timeout: 10000 }).catch(() => erros.push("sem o cartaz ativo"));
    }
    await espera(2600);
    await p.screenshot({ path: path.join(saida, `${sit.nome}.png`) });
    registro[sit.nome] = { arquivos: await p.evaluate(sit.ler), erros, ferramentas };
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1) + "\n");
console.log(JSON.stringify(registro, null, 1));
