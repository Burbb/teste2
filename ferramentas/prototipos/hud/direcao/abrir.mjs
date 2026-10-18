// Abre o estudo da nova direção visual da HUD para jogar: uma janela do Chromium (com tela) com direcao.css e
// direcao.js anexados à página (o jogo não muda). Feche a janela para encerrar.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/direcao/abrir.mjs [exploracao|luta] [producao]
// exploracao (padrão): a Capela Afogada de dia, arqueiro patrulheiro nível 5. luta: o paladino nível 8 com Morel contra
// 3 lobos (clique em "Começar a luta"). "producao" abre sem o estudo, para comparar. A janela tem 1920×945 (a área do
// jogo no monitor 1920×1080); com REDUZIDO=1, movimento reduzido.
import { spawn } from "child_process";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const caso = process.argv[2] || "exploracao", producao = process.argv[3] === "producao";
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";
const CASOS = {
  exploracao: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }],
  luta: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7", SEMENTE: "7" }],
};
if (!CASOS[caso]) throw new Error(`caso desconhecido: ${caso} (exploracao ou luta)`);
const [cenario, amb] = CASOS[caso];
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "normal", ...amb } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await new Promise((r) => setTimeout(r, 100));
if (!url) throw new Error("o cenário não subiu");
const b = await chromium.launch({ headless: false, args: ["--window-size=1936,1025"] });
const ctx = await b.newContext({ viewport: { width: 1920, height: 945 }, reducedMotion: process.env.REDUZIDO ? "reduce" : "no-preference" });
const p = await ctx.newPage();
if (!producao) {
  const JS = readFileSync(path.join(aqui, "direcao.js"), "utf8"), CSS = readFileSync(path.join(aqui, "direcao.css"), "utf8");
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch();
    const corpo = (await res.text()) + `\n;(() => { const s = document.createElement("style"); s.id = "direcao"; s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
}
await p.goto(url);
console.log(`${producao ? "Produção" : "Estudo"} aberto (${caso}). Feche a janela para encerrar.`);
await new Promise((r) => b.on("disconnected", r));
proc.kill();
