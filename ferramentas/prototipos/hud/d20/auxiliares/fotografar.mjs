// O d20 no CONTEXTO REAL (protótipo; nada no jogo): o jogo atual e as propostas A (Marfim) e B (Vidro) com os mesmos
// dados, pelos casos de cenarios_d20.py (o Explorar cai no baú abandonado; a escolha leva ao teste do motor; a semente
// decide o d20) e pelo laboratório (SIMULAÇÃO: mensagens do teste montadas à mão, para as regras do 20 e do 1 que o
// herói de teste não alcança). Fotos no giro, no resultado e depois (a tirinha no texto); os erros da página.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/d20/auxiliares/fotografar.mjs
// VERSOES=",a,b" (vazio = o jogo atual), CASOS="sucesso,falha,...", JANELAS="1920x945,1280x720", REDUZIDO=1.
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const VERSOES = (process.env.VERSOES ?? ",a,b").split(",");
const REAIS = ["sucesso", "falha", "critico", "desastre", "forca", "escuro", "longo"];
const SIMULADOS = ["sim_so20", "sim_so1", "sim_carisma"];
const CASOS = (process.env.CASOS || [...REAIS, ...SIMULADOS].join(",")).split(",");
const JANELAS = (process.env.JANELAS || "1920x945,1280x720").split(",").map((j) => { const [w, h] = j.split("x").map(Number); return { width: w, height: h }; });
const REDUZIDO = !!process.env.REDUZIDO;
const nomeV = (v) => v || "atual";

export async function subir(caso, versao, velocidade = "normal") {
  const proc = spawn(PY, [path.join(aqui, "cenarios_d20.py"), caso.startsWith("sim_") ? "laboratorio" : caso], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: velocidade, PROPOSTA: versao } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
// a escolha cuja etiqueta casa com `re`, quando a página está parada nela
export const opcao = (p, re) => p.waitForFunction((s) => !processando && pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => new RegExp(s).test(o.texto)), re, { timeout: 30000 });
export const escolher = (p, re) => p.evaluate((s) => responder(pergunta.id, pergunta.opcoes.findIndex((o) => new RegExp(s).test(o.texto))), re);
// do começo do teste até a escolha que rola o dado (no laboratório, a simulação do caso)
export async function rolar(p, caso) {
  if (!caso.startsWith("sim_")) { await opcao(p, "^Começar"); await espera(400); await escolher(p, "^Começar"); }
  if (caso.startsWith("sim_")) { await opcao(p, `^SIMULAÇÃO.*\\[${caso}\\]`); await espera(500); await escolher(p, `\\[${caso}\\]`); return; }
  const alvo = caso === "forca" ? "^Arrombar" : "^Abrir com cuidado";
  await opcao(p, alvo); await espera(600); await escolher(p, alvo);
}
export const resultado = (p) => p.evaluate(() => [...document.querySelectorAll("#historico-lista p")].map((e) => e.textContent).filter((t) => / contra \d+ — /.test(t)).pop() || "sem rolagem");
export async function medirRitmo(p) {
  await p.evaluate(() => { window.__t = {}; new MutationObserver((ms) => { for (const m of ms) for (const n of m.addedNodes) {
    if (n.classList && n.classList.contains("rolagem")) window.__t.rolagem = performance.now();
    else if (window.__t.rolagem && !window.__t.depois) window.__t.depois = performance.now(); } }).observe(document.getElementById("texto"), { childList: true }); });
}

async function um(b, caso, versao, janela) {
  // a velocidade lenta do jogo (a mesma imagem; o resultado fica 910 ms em vez de 650, tempo para a câmera); o ritmo
  // de verdade é medido por gestos.mjs, na velocidade normal
  const { proc, url } = await subir(caso, versao, "lento");
  const rotulo = `${caso}-${nomeV(versao)}-${janela.width}${REDUZIDO ? "-reduzido" : ""}`;
  try {
    const ctx = await b.newContext({ viewport: janela, reducedMotion: REDUZIDO ? "reduce" : "no-preference" });
    const p = await ctx.newPage();
    const erros = []; p.on("pageerror", (e) => erros.push(String(e))); p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
    await p.goto(url);
    await medirRitmo(p);
    await rolar(p, caso);
    await p.waitForSelector(".rolagem-centro", { timeout: 8000 });
    await espera(420);
    await p.screenshot({ path: path.join(SAIDA, `${rotulo}-1-giro.png`) });
    await p.waitForSelector(".rolagem-centro.pousou", { timeout: 4000 });
    const caixa = await p.evaluate(() => { const g = document.querySelector(".rolagem-centro .rc-grupo").getBoundingClientRect(); return { x: g.left, y: g.top, w: g.width, h: g.height }; });
    await espera(REDUZIDO ? 60 : 280);
    await p.screenshot({ path: path.join(SAIDA, `${rotulo}-2-resultado.png`) });
    await p.waitForFunction(() => !document.querySelector(".rolagem-centro"), null, { timeout: 5000 });
    await espera(900);
    await p.screenshot({ path: path.join(SAIDA, `${rotulo}-3-depois.png`) });
    const r = { caso, versao: nomeV(versao), janela: `${janela.width}x${janela.height}`, reduzido: REDUZIDO, resultado: await resultado(p),
      grupo: caixa, erros };
    console.log(JSON.stringify(r));
    await ctx.close();
    return r;
  } finally { proc.kill(); }
}

if (import.meta.url === `file:///${process.argv[1].replace(/\\/g, "/")}` || process.argv[1].endsWith("fotografar.mjs")) {
  const b = await chromium.launch();
  const rel = [];
  for (const caso of CASOS) for (const janela of JANELAS) for (const v of VERSOES) {
    try { rel.push(await um(b, caso, v, janela)); } catch (e) { console.log(JSON.stringify({ caso, versao: nomeV(v), erro: String(e) })); rel.push({ caso, versao: nomeV(v), erro: String(e) }); }
  }
  await b.close();
  writeFileSync(path.join(SAIDA, `relatorio${REDUZIDO ? "-reduzido" : ""}.json`), JSON.stringify(rel, null, 1));
}
