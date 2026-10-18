// Abre o protótipo da rolagem narrativa para jogar: uma janela do Chromium (com tela) no evento do baú abandonado, com
// rolagem.js/rolagem.css anexados à página (o jogo não muda). Explore, escolha "Abrir com cuidado" (Percepção). Feche a
// janela para encerrar.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/rolagem/abrir.mjs [semente] [producao]
// semente: 11 (padrão, sucesso por 1: 13 contra 12) ou 4 (falha por 1: 11 contra 12); 20 sai Crítico, 12 sai Desastre.
// "producao" abre sem o protótipo, para comparar. A janela tem 1920×945 (a área do jogo no monitor 1920×1080); com
// REDUZIDO=1, movimento reduzido. EVENTO=acampamento_bandidos troca o evento (Destreza e Carisma, que levam à luta).
import { spawn } from "child_process";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const semente = process.argv[2] || "11", producao = process.argv[3] === "producao";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "relatorio"], { cwd: raiz,
  env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "normal", EVENTO: process.env.EVENTO || "bau_abandonado", VEZES: "1", SEMENTE: semente } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await new Promise((r) => setTimeout(r, 100));
if (!url) throw new Error("o cenário não subiu");
const b = await chromium.launch({ headless: false, args: ["--window-size=1936,1025"] });
const ctx = await b.newContext({ viewport: { width: 1920, height: 945 }, reducedMotion: process.env.REDUZIDO ? "reduce" : "no-preference" });
const p = await ctx.newPage();
if (!producao) {
  const JS = readFileSync(path.join(aqui, "rolagem.js"), "utf8"), CSS = readFileSync(path.join(aqui, "rolagem.css"), "utf8");
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch();
    const corpo = (await res.text()) + `\n;(() => { const s = document.createElement("style"); s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
}
await p.goto(url);
console.log(`${producao ? "Produção" : "Protótipo"} aberto (semente ${semente}). Explorar → "Abrir com cuidado". Feche a janela para encerrar.`);
await new Promise((r) => b.on("disconnected", r));
proc.kill();
