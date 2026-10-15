// Conferência do martelo e da Pena de Fênix de 32×32 no jogo (1.93.0, desenhos.js pelo Icones), sem nenhum arquivo do
// protótipo, em janela normal (1500×950) e baixa (1280×720):
//   - o mercado (cenário mercado com AMOSTRAS=1: um Martelo na mochila e uma Pena de Fênix na bolsa): a prateleira de
//     suprimentos, a bolsa da ficha, a mochila na aba Vender, a dica de comparação do martelo e o Inventário;
//   - o cartão do saque com um martelo (cenário vila com ACHADO=martelo) e o martelo voando para o corpo ao equipar.
// Em cada página, conta onde o desenho da pena aparece (só em espaços de item; o Vigor e o Poder ficam com os deles).
// Guarda em capturas-itens/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_itens.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-itens");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
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
const parado = (p) => p.waitForFunction(() => typeof pergunta !== "undefined" && pergunta && !processando, null, { timeout: 30000 });
async function recortar(p, sel, nome, folga = 6) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, Math.floor(r.x - f)), y: Math.max(0, Math.floor(r.y - f)), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
// onde estão os desenhos novos: a pena e o martelo, e o tamanho de cada um na tela
const onde = (p) => p.evaluate(() => {
  const pena = new Set([1, 2, 4].map((e) => Desenhos.url("pena", e))), martelo = new Set([1, 2, 4].map((e) => Desenhos.url("martelo", e)));
  const lugar = (i) => (i.closest(".slot-px, .achado-arte, .voo-item, .item-voando, .rb-icone, .roda-janela, .dica") || i.parentElement).className.split(" ")[0];
  const r = (i) => Math.round(i.getBoundingClientRect().width);
  const imgs = [...document.querySelectorAll("img")];
  return { pena: imgs.filter((i) => pena.has(i.getAttribute("src"))).map((i) => `${lugar(i)}:${r(i)}`),
    martelo: imgs.filter((i) => martelo.has(i.getAttribute("src"))).map((i) => `${lugar(i)}:${r(i)}`),
    vigor: !!document.querySelector('img[src*="vital-vigor"]'), poder: !!document.querySelector('img[src*="attr-poder"]') };
});
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  return p;
}
// 1. o mercado
{
  const { proc, url } = await subir("mercado", { CLASSE: "guerreiro", AMOSTRAS: "1" });
  for (const jan of Object.keys(JANELAS)) {
    const nome = `mercado-${jan}`;
    const p = await pagina(url, jan, nome);
    await parado(p); await espera(800);
    await p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
    await recortar(p, "#lista-suprimentos", `${nome}-suprimentos`, 4);
    await recortar(p, "#heroi", `${nome}-ficha`, 0);
    relatorio.push({ nome: `${nome} suprimentos`, ...(await onde(p)) });
    await (await p.$('[data-aba="vender"]')).click(); await espera(700);
    await recortar(p, "#lista-vender", `${nome}-vender`, 4);
    const martelo = await p.$("#lista-vender .slot-px");
    if (martelo) {  // a dica do martelo, com o equipado ao lado (a comparação)
      await martelo.hover(); await espera(900);
      const c = await p.evaluate(() => { const rs = ["#dica-item", "#dica-equipado"].map((s) => document.querySelector(s)).filter((e) => e && !e.hidden && e.getBoundingClientRect().width).map((e) => e.getBoundingClientRect());
        if (!rs.length) return null; const x = Math.min(...rs.map((r) => r.left)), y = Math.min(...rs.map((r) => r.top));
        return { x: Math.max(0, Math.floor(x - 4)), y: Math.max(0, Math.floor(y - 4)), width: Math.ceil(Math.max(...rs.map((r) => r.right)) - x + 8), height: Math.ceil(Math.max(...rs.map((r) => r.bottom)) - y + 8) }; });
      if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}-dica-martelo.png`), clip: c }); else console.log(`  (sem a dica em ${nome})`);
    }
    relatorio.push({ nome: `${nome} vender`, ...(await onde(p)) });
    await p.mouse.move(5, 5);
    await p.close();
    const q = await pagina(url, jan, `${nome}-inventario`);
    await parado(q); await espera(500);
    await q.keyboard.press("i"); await espera(1200);
    await q.screenshot({ path: path.join(SAIDA, `${nome}-inventario.png`) });
    relatorio.push({ nome: `${nome} inventário`, ...(await onde(q)) });
    await q.close();
  }
  proc.kill();
}
// 2. o cartão do saque com um martelo e o voo ao equipar
for (const jan of Object.keys(JANELAS)) {  // um jogo por janela: equipar muda o jogo
  const { proc, url } = await subir("vila", { ACHADO: "martelo" });
  {
    const nome = `saque-${jan}`;
    const p = await pagina(url, jan, nome);
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(1500);
    await recortar(p, ".janela-achado", `${nome}-cartao`, 6);
    relatorio.push({ nome: `${nome} cartão`, ...(await onde(p)) });
    await p.evaluate(() => {
      new MutationObserver((ms, o) => { const v = document.querySelector(".voo-item"); if (!v) return;
        setTimeout(() => { document.getAnimations().forEach((a) => a.pause()); window.__voo = true; }, 120); o.disconnect(); })
        .observe(document.body, { childList: true });
    });
    const eq = await p.$('#prompt .escolha:has-text("Equipar")');
    if (eq) await eq.click(); else await p.keyboard.press("1");
    try {
      await p.waitForFunction(() => window.__voo, null, { timeout: 8000 });
      await recortar(p, ".voo-item", `${nome}-voo`, 16);
      relatorio.push({ nome: `${nome} voo`, ...(await onde(p)) });
      await p.evaluate(() => document.getAnimations().forEach((a) => a.play()));
    } catch { console.log(`  ${nome}: o voo não apareceu`); }
    await espera(1500);
    await recortar(p, "#heroi", `${nome}-ficha-depois`, 0);
    relatorio.push({ nome: `${nome} depois`, ...(await onde(p)) });
    for (let k = 0; k < 20 && !(await p.$("#prompt .escolha")); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
    await p.keyboard.press("i"); await espera(1200);
    await p.screenshot({ path: path.join(SAIDA, `${nome}-inventario.png`) });
    relatorio.push({ nome: `${nome} inventário`, ...(await onde(p)) });
    await p.close();
  }
  proc.kill();
}
await b.close();
relatorio.forEach((r) => console.log(r.nome, "· pena", JSON.stringify(r.pena), "· martelo", JSON.stringify(r.martelo), "· Vigor", r.vigor, "· Poder", r.poder));
writeFileSync(path.join(SAIDA, "onde.json"), JSON.stringify(relatorio, null, 1));
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
