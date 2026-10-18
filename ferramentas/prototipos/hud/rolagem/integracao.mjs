// A rolagem no centro INTEGRADA (1.117.0): o jogo como está, sem nada desta pasta na página. Os mesmos casos do
// protótipo (fotografar.mjs): o sucesso e a falha por 1, pular, texto instantâneo e movimento reduzido.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/rolagem/integracao.mjs
// O caso: o evento do baú abandonado (rpg/eventos/comuns.py, bau_abandonado), "Abrir com cuidado" (teste de Percepção,
// dificuldade 12), forçado pelo cenário "relatorio" (tests/navegador/cenarios.py) com EVENTO e SEMENTE. A semente decide
// o d20 do motor: SUCESSO e FALHA abaixo saem com o mesmo herói e a mesma escolha (fotografar.mjs procurar).
// A janela: 1920×945, a área do jogo numa janela maximizada no monitor 1920×1080. Fotos no começo da rolagem, no
// resultado e depois; o "precisa de N" (do motor) no giro; o tempo da tirinha à consequência; pular, texto instantâneo
// e movimento reduzido.
import { spawn } from "child_process";
import { mkdirSync, writeFileSync, readdirSync, rmSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas-integracao");
mkdirSync(SAIDA, { recursive: true }); for (const f of readdirSync(SAIDA)) if (/\.png$/.test(f)) rmSync(path.join(SAIDA, f));
const JANELA = { width: 1920, height: 945 };
const SUCESSO = process.env.SEMENTE_SUCESSO || "11", FALHA = process.env.SEMENTE_FALHA || "4";
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

async function caso(b, { semente, nome, fotos = [350, 1250, 2300], reduzido = false }) {
  const { proc, url } = await subir(semente);
  try {
    const ctx = await b.newContext({ viewport: JANELA, reducedMotion: reduzido ? "reduce" : "no-preference" });
    const p = await ctx.newPage();
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    await p.goto(url);
    // o ritmo: do aparecer da tirinha no texto até o que vem depois dela (a consequência)
    await p.evaluate(() => { window.__t = {}; new MutationObserver((ms) => { for (const m of ms) for (const n of m.addedNodes) {
      if (n.classList && n.classList.contains("rolagem")) window.__t.rolagem = performance.now();
      else if (window.__t.rolagem && !window.__t.depois) window.__t.depois = performance.now(); } }).observe(document.getElementById("texto"), { childList: true }); });
    await abrirBau(p);
    const t0 = Date.now();
    let precisa = null;
    for (const [i, ms] of fotos.entries()) {
      await espera(Math.max(0, ms - (Date.now() - t0)));
      if (!i) precisa = await p.evaluate(() => { const e = document.querySelector(".rc-precisa"); return e && e.textContent; });
      await p.screenshot({ path: path.join(SAIDA, `${nome}-${i + 1}-${ms}ms.png`) });
    }
    await espera(800);
    const r = { nome, semente, girando: precisa, resultado: await resultado(p), da_rolagem_a_consequencia_ms: await p.evaluate(() => Math.round(window.__t.depois - window.__t.rolagem)), erros };
    await ctx.close();
    console.log(JSON.stringify(r));
    return r;
  } finally { proc.kill(); }
}

const b = await chromium.launch();
const rel = [];
// o sucesso e a falha por 1
for (const [rotulo, semente] of [["sucesso", SUCESSO], ["falha", FALHA]]) rel.push(await caso(b, { semente, nome: rotulo }));
// movimento reduzido
rel.push(await caso(b, { semente: FALHA, nome: "falha-reduzido", fotos: [350, 1250], reduzido: true }));
// pular no meio do giro: o clique corta como hoje (quanto tempo o centro fica depois do clique)
{
  const { proc, url } = await subir(SUCESSO);
  try {
    const p = await b.newPage({ viewport: JANELA });
    await p.goto(url); await abrirBau(p);
    await p.waitForSelector(".rolagem-centro", { timeout: 5000 }); await espera(300);
    const t = Date.now(); await p.mouse.click(960, 600);
    await p.waitForFunction(() => !document.querySelector(".rolagem-centro"), null, { timeout: 5000 });
    const r = { nome: "pular", centro_some_ms_depois_do_clique: Date.now() - t, resultado: await resultado(p) };
    console.log(JSON.stringify(r)); rel.push(r); await p.close();
  } finally { proc.kill(); }
}
// texto instantâneo: nada no centro, a tirinha de sempre
{
  const { proc, url } = await subir(SUCESSO, "instantaneo");
  try {
    const p = await b.newPage({ viewport: JANELA });
    await p.goto(url);
    await p.evaluate(() => { window.__viuCentro = false; new MutationObserver(() => { if (document.querySelector(".rolagem-centro")) window.__viuCentro = true; }).observe(document.body, { childList: true }); });
    await abrirBau(p); await espera(1500);
    const r = { nome: "instantaneo", apareceu_no_centro: await p.evaluate(() => window.__viuCentro), resultado: await resultado(p) };
    console.log(JSON.stringify(r)); rel.push(r); await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(rel, null, 1));
