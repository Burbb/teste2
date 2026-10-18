// O protótipo da rolagem narrativa (plano 23, item 1.4): atual × proposta com os mesmos dados.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/rolagem/fotografar.mjs [procurar]
// O caso: o evento do baú abandonado (rpg/eventos/comuns.py, bau_abandonado), "Abrir com cuidado" (teste de Percepção,
// dificuldade 12), forçado pelo cenário "relatorio" (tests/navegador/cenarios.py) com EVENTO e SEMENTE. A semente decide
// o d20 do motor: SUCESSO e FALHA abaixo saem com o mesmo herói e a mesma escolha ("procurar" lista as sementes 1 a 20).
// A janela: 1920×945, a área do jogo numa janela maximizada no monitor 1920×1080 (tirando a barra de tarefas e a do
// navegador). Fotos no começo da rolagem, no resultado e depois; uma gravação da proposta (sucesso e falha); e as
// conferências: pular no meio, texto instantâneo e movimento reduzido.
import { spawn } from "child_process";
import { readFileSync, mkdirSync, writeFileSync, readdirSync, rmSync, renameSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas"), VIDEOS = path.join(SAIDA, "videos");
for (const d of [SAIDA, VIDEOS]) { mkdirSync(d, { recursive: true }); for (const f of readdirSync(d)) if (/\.(png|webm)$/.test(f)) rmSync(path.join(d, f)); }
const JANELA = { width: 1920, height: 945 };
const SUCESSO = process.env.SEMENTE_SUCESSO || "11", FALHA = process.env.SEMENTE_FALHA || "4";
const JS = readFileSync(path.join(aqui, "rolagem.js"), "utf8"), CSS = readFileSync(path.join(aqui, "rolagem.css"), "utf8");
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

async function subir(semente, velocidade = "normal") {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "relatorio"], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: velocidade, EVENTO: "bau_abandonado", VEZES: "1", SEMENTE: semente } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
async function proposta(p) {
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch();
    const corpo = (await res.text()) + `\n;(() => { const s = document.createElement("style"); s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
}
// o menu do lugar → Explorar → o baú → "Abrir com cuidado"; devolve quando a escolha foi feita
async function abrirBau(p) {
  const opcao = (re) => p.waitForFunction((s) => !processando && pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => new RegExp(s).test(o.texto)), re, { timeout: 30000 });
  const escolher = (re) => p.evaluate((s) => responder(pergunta.id, pergunta.opcoes.findIndex((o) => new RegExp(s).test(o.texto))), re);
  await opcao("^Explorar"); await espera(500);
  await escolher("^Explorar");
  await opcao("^Abrir com cuidado"); await espera(700);
  await escolher("^Abrir com cuidado");
}
// o resultado pelo histórico (H): a página pode já ter seguido para a cena seguinte
const resultado = (p) => p.evaluate(() => { const r = [...document.querySelectorAll("#historico-lista p")].map((e) => e.textContent).filter((t) => / contra \d+ — /.test(t)).pop(); return r || "sem rolagem"; });

async function caso(b, { semente, modo, nome, fotos = [350, 1250, 2300], reduzido = false, video = null }) {
  const { proc, url } = await subir(semente);
  try {
    const ctx = await b.newContext({ viewport: JANELA, reducedMotion: reduzido ? "reduce" : "no-preference", ...(video ? { recordVideo: { dir: VIDEOS, size: JANELA } } : {}) });
    const p = await ctx.newPage();
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo === "proposta") await proposta(p);
    await p.goto(url);
    // o ritmo: do aparecer da tirinha no texto até o que vem depois dela (a consequência)
    await p.evaluate(() => { window.__t = {}; new MutationObserver((ms) => { for (const m of ms) for (const n of m.addedNodes) {
      if (n.classList && n.classList.contains("rolagem")) window.__t.rolagem = performance.now();
      else if (window.__t.rolagem && !window.__t.depois) window.__t.depois = performance.now(); } }).observe(document.getElementById("texto"), { childList: true }); });
    await abrirBau(p);
    const t0 = Date.now();
    for (const [i, ms] of fotos.entries()) { await espera(Math.max(0, ms - (Date.now() - t0))); await p.screenshot({ path: path.join(SAIDA, `${nome}-${i + 1}-${ms}ms.png`) }); }
    await espera(800);
    const r = { nome, semente, resultado: await resultado(p), da_rolagem_a_consequencia_ms: await p.evaluate(() => Math.round(window.__t.depois - window.__t.rolagem)), erros };
    const v = p.video();
    await ctx.close();
    if (video && v) renameSync(await v.path(), path.join(VIDEOS, `${video}.webm`));
    console.log(JSON.stringify(r));
    return r;
  } finally { proc.kill(); }
}

const b = await chromium.launch();
if (process.argv[2] === "procurar") {
  for (let s = 1; s <= 20; s++) {
    const { proc, url } = await subir(String(s), "instantaneo");
    const p = await b.newPage({ viewport: JANELA });
    try { await p.goto(url); await abrirBau(p); await espera(1500); console.log(s, await resultado(p)); } catch (e) { console.log(s, "erro", String(e).slice(0, 80)); }
    await p.close(); proc.kill();
  }
  await b.close(); process.exit(0);
}

const rel = [];
// atual × proposta, mesmos dados
for (const [rotulo, semente] of [["sucesso", SUCESSO], ["falha", FALHA]])
  for (const modo of ["atual", "proposta"]) rel.push(await caso(b, { semente, modo, nome: `${rotulo}-${modo}` }));
// movimento reduzido (proposta)
rel.push(await caso(b, { semente: FALHA, modo: "proposta", nome: "falha-proposta-reduzido", fotos: [350, 1250], reduzido: true }));
// pular no meio do giro: o clique corta como hoje (quanto tempo o centro fica depois do clique)
{
  const { proc, url } = await subir(SUCESSO);
  try {
    const p = await b.newPage({ viewport: JANELA });
    await proposta(p); await p.goto(url); await abrirBau(p);
    await p.waitForSelector(".rp-palco", { timeout: 5000 }); await espera(300);
    const t = Date.now(); await p.mouse.click(960, 600);
    await p.waitForFunction(() => !document.querySelector(".rp-palco"), null, { timeout: 5000 });
    const r = { nome: "pular", centro_some_ms_depois_do_clique: Date.now() - t, resultado: await resultado(p) };
    console.log(JSON.stringify(r)); rel.push(r); await p.close();
  } finally { proc.kill(); }
}
// texto instantâneo: nada no centro, a tirinha de sempre
{
  const { proc, url } = await subir(SUCESSO, "instantaneo");
  try {
    const p = await b.newPage({ viewport: JANELA });
    await proposta(p); await p.goto(url);
    await p.evaluate(() => { window.__viuCentro = false; new MutationObserver(() => { if (document.querySelector(".rp-palco")) window.__viuCentro = true; }).observe(document.body, { childList: true }); });
    await abrirBau(p); await espera(1500);
    const r = { nome: "instantaneo", apareceu_no_centro: await p.evaluate(() => window.__viuCentro), resultado: await resultado(p) };
    console.log(JSON.stringify(r)); rel.push(r); await p.close();
  } finally { proc.kill(); }
}
// a gravação da proposta: o sucesso e a falha, um depois do outro
{
  const ctx = await b.newContext({ viewport: JANELA, recordVideo: { dir: VIDEOS, size: { width: 1280, height: 630 } } });
  const p = await ctx.newPage(); await proposta(p);
  for (const semente of [SUCESSO, FALHA]) {
    const { proc, url } = await subir(semente);
    try { await p.goto(url); await abrirBau(p); await espera(3200); } finally { proc.kill(); }
  }
  const v = p.video(); await ctx.close();
  renameSync(await v.path(), path.join(VIDEOS, "proposta-sucesso-e-falha.webm"));
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(rel, null, 1));
