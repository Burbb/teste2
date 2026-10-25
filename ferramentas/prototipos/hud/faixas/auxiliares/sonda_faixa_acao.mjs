// A animação dos rótulos da luta (.faixa-acao: o golpe, os selos, a surpresa) medida na página do jogo: cria um rótulo
// de cada variante, pausa a animação e lê a transformação e a opacidade calculadas em vários instantes. Serve para
// conferir que separar o nome da animação (1.205.0: "faixa" era o mesmo nome em 03-batalha.css e em 06, e a de 06
// valia também aqui) não muda o que se vê. Grava ../capturas/faixa-acao-<rotulo>.json.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node .../sonda_faixa_acao.mjs <rotulo>
import { spawn } from "child_process";
import { writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const rotulo = process.argv[2] || "medida";
const proc = spawn(process.platform === "win32" ? "python" : "python3", ["-m", "tests.navegador.cenarios", "combate"],
  { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, VELOCIDADE: "rapido" } });
let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await espera(100);
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
await p.goto(url); await espera(2500);
const r = await p.evaluate(() => {
  const saida = {};
  for (const classe of ["", "inimiga", "boa", "selos", "selos ruim", "espinhos", "ruim", "surpresa", "surpresa ruim"]) {
    const amostras = [];
    for (const ms of [0, 60, 120, 225, 400, 800, 1200, 1350, 1440, 1499]) {
      const e = document.createElement("div");
      e.className = "faixa-acao " + classe;
      e.textContent = "Golpe";
      e.style.animationPlayState = "paused";
      e.style.animationDelay = `-${ms}ms`;
      document.body.appendChild(e);
      const cs = getComputedStyle(e);
      amostras.push({ ms, nome: cs.animationName, transform: cs.transform, opacity: cs.opacity, dur: cs.animationDuration });
      e.remove();
    }
    saida[classe || "base"] = amostras;
  }
  return saida;
});
writeFileSync(path.join(aqui, "..", "capturas", `faixa-acao-${rotulo}.json`), JSON.stringify(r, null, 1));
console.log(JSON.stringify(r.base.map((a) => [a.ms, a.nome, a.transform, a.opacity])));
await b.close(); proc.kill();
