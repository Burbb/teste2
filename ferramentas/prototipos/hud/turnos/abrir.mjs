// Abre o protótipo da etapa 1C para jogar: uma janela do Chromium (com tela), a luta pedida e turnos.js/turnos.css
// anexados à página (o jogo não muda). Feche a janela para encerrar.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/turnos/abrir.mjs [luta] [producao]
// luta: iniciativa (padrão: paladino com Morel contra 3 lobos, com a sua iniciativa), emboscada (a deles) ou cheia
// (necromante com a comitiva e 3 servos contra 5 caídos e o xamã, com a sua iniciativa). "producao" abre sem o protótipo,
// para comparar. A janela tem 1280×720; com REDUZIDO=1, movimento reduzido.
import { spawn } from "child_process";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const luta = process.argv[2] || "iniciativa", producao = process.argv[3] === "producao";
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";
const LOBOS = { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" };
const AMB = {
  iniciativa: { ...LOBOS, EMBOSCADA: "jogador" },
  emboscada: { ...LOBOS, EMBOSCADA: "inimigo" },
  cheia: { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "mago", ESPEC: "necromante", NIVEL: "12", NIVEL_LUTA: "9", REC: "0.7", COMITIVA: "morel,odete",
    SERVOS: "3", GRUPO: "caido:5,xama_caido:1", LUGAR: "charco", PERIODO: "3", EMBOSCADA: "jogador" },
}[luta];
if (!AMB) throw new Error(`luta desconhecida: ${luta} (iniciativa, emboscada ou cheia)`);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, VELOCIDADE: "normal", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...AMB } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await new Promise((r) => setTimeout(r, 100));
if (!url) throw new Error("o cenário não subiu");
const b = await chromium.launch({ headless: false, args: ["--window-size=1296,800"] });
const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, reducedMotion: process.env.REDUZIDO ? "reduce" : "no-preference" });
const p = await ctx.newPage();
if (!producao) {
  const JS = readFileSync(path.join(aqui, "turnos.js"), "utf8"), CSS = readFileSync(path.join(aqui, "turnos.css"), "utf8");
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch();
    const corpo = (await res.text()) + `\n;(() => { const s = document.createElement("style"); s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
}
await p.goto(url);
console.log(`${producao ? "Produção" : "Protótipo"} aberto (${luta}). Clique em "Começar a luta". Feche a janela para encerrar.`);
await new Promise((r) => b.on("disconnected", r));
proc.kill();
