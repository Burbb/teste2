// O que fica por cima do cenário acompanha a arte quando a janela muda de tamanho, sem recarregar: os prédios da vila
// (a área clicável, o balão e a ponta dele) e os pontos de uma cena (a capela, com o F4). Alterna a mesma página entre
// janela grande e pequena várias vezes e compara, em cada tamanho, as posições com as de uma página carregada direto
// nele (a referência). Depois das alternâncias, confere mouse, teclado e clique (no balão e no próprio cenário).
// Fotografa cada passo em PASTA (padrão: não fotografa).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node tests/navegador/redimensionar.mjs [PASTA]
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const PASTA = process.argv[2] || "";
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok " : "FALHOU"} ${msg}`); if (!ok) falhas++; };
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
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const TAMANHOS = { grande: [1920, 1009], pequena: [1280, 720], media: [1405, 850] };
const SEQUENCIA = ["grande", "pequena", "grande", "media", "pequena", "grande", "pequena"];

// as posições na tela de tudo o que fica por cima da arte, para comparar com a referência
const LER = (sel) => [...document.querySelectorAll(sel)].map((e) => {
  const r = e.getBoundingClientRect(), n = e.querySelector(".balao-nome, .ci-balao").getBoundingClientRect();
  return { id: e.dataset.predio || e.dataset.ponto, area: [r.left, r.top, r.width, r.height].map(Math.round), balao: [Math.round(n.left + n.width / 2), Math.round(n.bottom)] };
});
const diferenca = (a, ref) => Math.max(0, ...ref.map((r) => { const x = a.find((y) => y.id === r.id); if (!x) return 999;
  return Math.max(...r.area.map((v, i) => Math.abs(v - x.area[i])), ...r.balao.map((v, i) => Math.abs(v - x.balao[i]))); }));

async function abrir(url, tam, pronto) {
  const [W, H] = TAMANHOS[tam];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto(url);
  await pronto(p);
  return p;
}
async function percorrer(nome, url, sel, pronto) {
  console.log(`cenário: ${nome}`);
  const ref = {};
  for (const tam of new Set(SEQUENCIA)) {
    const p = await abrir(url, tam, pronto);
    await espera(900);
    ref[tam] = await p.evaluate(LER, sel);
    await p.close();
  }
  const p = await abrir(url, SEQUENCIA[0], pronto);
  await espera(900);
  for (const [i, tam] of SEQUENCIA.entries()) {
    const [W, H] = TAMANHOS[tam];
    await p.setViewportSize({ width: W, height: H });
    await espera(700);
    if (PASTA) await p.screenshot({ path: path.join(PASTA, `${nome}-${i}-${tam}.png`) });
    const d = diferenca(await p.evaluate(LER, sel), ref[tam]);
    conferir(d <= 1, `${nome}, passo ${i} (${tam}, ${W}×${H}): balões, pontas e áreas a ${d} px da página aberta nesse tamanho`);
  }
  return p;
}

// ------------------------------------------------------------------ a vila
{
  const { proc, url } = await subir("tutorial", { VISTAS: "A1,V2,N1,D1" });
  const pronto = async (p) => {
    for (let k = 0; k < 40 && !(await p.$("#predios .predio")); k++) {
      for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
      await espera(300);
    }
  };
  const p = await percorrer("vila", url, "#predios .predio", pronto);
  const naVila = () => p.evaluate(() => document.getElementById("cena").dataset.tipo === "local" && !!document.querySelector("#predios .predio") && !document.querySelector("#predios").classList.contains("focado"));
  const voltar = async () => { for (let k = 0; k < 8 && !(await naVila()); k++) { await p.keyboard.press("Escape"); await espera(600); } await espera(500); };
  const titulo = () => p.evaluate(() => (document.querySelector("#cena-cab .cena-titulo") || {}).textContent || "");
  // mouse: o balão do prédio sob o mouse acende
  const merc = await p.$('#predios .predio[data-predio="mercado"]');
  await merc.hover(); await espera(200);
  conferir(await p.evaluate(() => document.querySelector('#predios .predio[data-predio="mercado"]').matches(":hover")), "o mouse sobre o Mercado acende o prédio dele");
  // clique no balão
  await (await p.$('#predios .predio[data-predio="mercado"] .balao-nome')).click(); await espera(1500);
  conferir(/Mercado/.test(await titulo()), "o clique no balão do Mercado entra no Mercado");
  await voltar();
  // clique no próprio cenário, no meio do prédio (fora do botão: o clique cai no canvas e vila.js acha o prédio)
  const alvo = await p.evaluate(() => { const r = document.querySelector('#predios .predio[data-predio="mercado"]').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
  const quem = await p.evaluate(([x, y]) => predioNoPonto(x, y), alvo);
  conferir(quem === "mercado", `o ponto do cenário no meio do Mercado é o Mercado (${quem})`);
  // teclado: o foco num prédio e Enter entra nele
  await p.focus('#predios .predio[data-predio="mercado"]'); await p.keyboard.press("Enter"); await espera(1500);
  conferir(/Mercado/.test(await titulo()), "Enter no Mercado (teclado) entra no Mercado");
  await voltar();
  await p.close(); proc.kill();
}

// ------------------------------------------------------------------ a capela, com os pontos destacados (F4)
{
  const { proc, url } = await subir("capela", { ETAPA: "fundo" });
  const pronto = async (p) => {
    for (let k = 0; k < 40 && !(await p.$("#pontos-cena:not([hidden]) .ci-ponto")); k++) {
      for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
      await espera(300);
    }
  };
  const p = await percorrer("capela", url, "#pontos-cena .ci-ponto:not(.parado)", pronto);
  await p.keyboard.press("F4"); await espera(400);
  conferir(await p.evaluate(() => document.body.classList.contains("destacar-interacoes")), "o F4 liga o destaque das interações");
  if (PASTA) await p.screenshot({ path: path.join(PASTA, "capela-f4.png") });
  await p.keyboard.press("F4"); await espera(300);
  await p.close(); proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
