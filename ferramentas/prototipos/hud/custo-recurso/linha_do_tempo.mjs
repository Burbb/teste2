// Etapa 1B, o custo do recurso: a linha do tempo do que a tela mostra quando uma habilidade com custo é usada.
// Sobe uma luta (cenário tutorial), escolhe a habilidade, mira, cancela, escolhe de novo e confirma o alvo; a cada
// quadro (requestAnimationFrame) anota os números da vida e do recurso na HUD do topo e na carta do herói, e quando
// cada lance (Batalha.lance) e cada estado (aplicarEstado) começam e acabam. Nada no jogo muda: só se lê a página.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/custo-recurso/linha_do_tempo.mjs [rotulo]
// HAB=drenar_vida CLASSE=mago ESPEC=necromante (padrão), VELOCIDADE=rapido|normal, SAIDA=<arquivo.json>
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const ROTULO = process.argv[2] || "agora";
const HAB = process.env.HAB || "drenar_vida";
const amb = { TUTORIAL: "0", VISTAS: "A1,V2,N1,D1,K1,M1,L1", NIVEL: "12", NIVEL_LUTA: "9", VIDA: "0.5", REC: "1",
  CLASSE: process.env.CLASSE || "mago", ESPEC: process.env.ESPEC || "necromante", LUTA: process.env.LUTA_FAMILIA || "caido", QUANTOS: "2",
  ...(process.env.ANIMAL ? { ANIMAL: process.env.ANIMAL } : {}) };
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, VELOCIDADE: process.env.VELOCIDADE || "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await espera(100);
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const p = await b.newPage({ viewport: { width: 1500, height: 950 } });
const erros = [];
p.on("pageerror", (e) => erros.push(String(e)));
await p.goto(url);
const naVez = () => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="atacar"]'));
for (let k = 0; k < 200 && !(await naVez()); k++) {
  for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
  await espera(250);
}
await espera(500);
// o relógio: os números à vista a cada quadro e os começos e fins de lances e estados
await p.evaluate(() => {
  const ler = () => {
    const hud = (v) => document.querySelector(`#hud-linha .vital[data-vital="${v}"] .num`)?.textContent || "";
    const c = Batalha.elCarta("j");
    return { hud_vida: hud("hp"), hud_rec: hud("rec"), carta_vida: c?.querySelector(".carta-hp .num, .hp-num, .vida .num")?.textContent || c?.querySelector(".barra-vida + .num, .num")?.textContent || "",
      carta_rec: c?.querySelector(".carta-rec .num")?.textContent || "" };
  };
  window.__linha = []; window.__t0 = performance.now();
  let ultimo = "";
  const anotar = (o) => window.__linha.push({ t: Math.round(performance.now() - window.__t0), ...o });
  const quadro = () => { const v = ler(), k = JSON.stringify(v); if (k !== ultimo) { ultimo = k; anotar({ tela: v }); } requestAnimationFrame(quadro); };
  requestAnimationFrame(quadro);
  const lance = Batalha.lance;
  Batalha.lance = async (m) => { anotar({ lance: m.tipo, inicio: true, ...(m.rec !== undefined ? { rec: m.rec } : {}), ...(m.hp !== undefined ? { hp: m.hp } : {}) }); const r = await lance(m); anotar({ lance: m.tipo, fim: true }); return r; };
  const ap = window.aplicarEstado;
  window.aplicarEstado = (e, ...x) => { anotar({ estado: e && e.heroi ? `vida ${e.heroi.hp} ${e.heroi.recurso} ${e.heroi.rec}` : "?" }); return ap(e, ...x); };
  window.__marcar = (o) => anotar({ marca: o });
});
const marcar = (o) => p.evaluate((o) => window.__marcar(o), o);
// escolher a habilidade, mirar e cancelar; escolher de novo e confirmar
await marcar("clique em Habilidades");
await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click(); await espera(500);
await marcar(`clique em ${HAB}`);
await (await p.$(`.roda-janela .rj-linha[data-hab="${HAB}"]`)).click(); await espera(800);
await marcar("na mira (cancelável)");
const naMira = await p.evaluate(() => !!document.querySelector(".roda-mira"));
if (naMira) {
  await marcar("Voltar da mira (cancelar)");
  await (await p.$(".mira-voltar")).click(); await espera(800);
  await marcar("de volta à roda");
  await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click(); await espera(500);
  await (await p.$(`.roda-janela .rj-linha[data-hab="${HAB}"]`)).click(); await espera(800);
  await marcar("confirma o alvo");
  await (await p.$("#batalha .carta.alvejavel")).click();
}
for (let k = 0; k < 200 && !(await naVez()); k++) await espera(100);
await espera(600);
await marcar("a vez do herói de novo");
const linha = await p.evaluate(() => window.__linha);
const saida = process.env.SAIDA || path.join(aqui, "capturas", `linha-${HAB}-${ROTULO}.json`);
mkdirSync(path.dirname(saida), { recursive: true });
writeFileSync(saida, JSON.stringify({ hab: HAB, rotulo: ROTULO, velocidade: process.env.VELOCIDADE || "rapido", erros, linha }, null, 1));
for (const x of linha) {
  if (x.tela) console.log(`${String(x.t).padStart(6)} ms  TELA  topo: vida ${x.tela.hud_vida}  rec ${x.tela.hud_rec}  | carta: vida ${x.tela.carta_vida}  rec ${x.tela.carta_rec}`);
  else if (x.marca) console.log(`${String(x.t).padStart(6)} ms  ---- ${x.marca}`);
  else if (x.estado) console.log(`${String(x.t).padStart(6)} ms  estado ${x.estado}`);
  else console.log(`${String(x.t).padStart(6)} ms  lance ${x.lance} ${x.inicio ? "começa" : "acaba"}${x.rec !== undefined ? ` rec=${x.rec}` : ""}${x.hp !== undefined ? ` hp=${x.hp}` : ""}`);
}
if (erros.length) console.log("ERROS", erros);
await b.close(); proc.kill();
