// O peitoral e as botas de couro (os desenhos "gibao" e "bota"), rodada 1 da proposta (protótipo): fotografa o jogo de
// verdade com os desenhos atuais (os sprites 16×16) e com a proposta (couro-aseprite/rodada1/gibao-32 e -64,
// bota-32 e -64, com os @2x), com os mesmos dados. Na proposta, a página recebe um icones.js com as duas peças
// registradas como a integração faria (TAMANHOS em 32 e 64 e o papel de equipamento em ITEM) e os arquivos vêm da
// pasta da proposta; o jogo não muda. Os lugares, para o Arqueiro, em janela normal (1500×950) e baixa (1280×720):
//   - mercado (CLASSE=arqueiro, VESTIR=gibao,bota, AMOSTRA=<peça>, SEMENTE=1): a tela inteira, a ficha (32), a aba
//     Vender (32) e a dica com a comparação (Shift), uma rodada por peça;
//   - saque (vila, CLASSE=arqueiro, ACHADO=<peça>): a tela inteira e o cartão do achado (64). O "você usa" fica com a
//     peça de ferro que o cenário veste (48 nativo): nesta rodada o couro não tem 48, e a página não mostra um.
// A versão "rodada2" (couro-aseprite/rodada2/: o fechamento novo do gibão de 32 e os tamanhos 40 e 48) acrescenta o
// Inventário (o corpo e a mochila em 40) e, no saque, veste a mesma peça (VESTIR=<peça>) para o "você usa" mostrar o 48
// nativo, e fotografa o voo ao equipar:
//   SAIDA=ferramentas/prototipos/hud/couro-aseprite/rodada2/capturas/jogo VERSOES=atual,rodada2
// A versão "x2" é a rodada 2 com o 64 trocado pelo 32 final ampliado exatamente 2× (o *-32@2x.png, vizinho mais
// próximo, sem retoque), para comparar no cartão do saque se o 64 trabalhado faz diferença; LUGARES=saque fotografa só
// o saque:
//   SAIDA=ferramentas/prototipos/hud/couro-aseprite/rodada2/capturas/jogo-x2 VERSOES=rodada2,x2 LUGARES=saque
// Guarda em SAIDA (padrão: couro-aseprite/capturas/jogo) como <janela>-<versao>-<peça>-<lugar>.png e os recortes
// pequenos como zoom-...; comparar_couro.py monta as comparações.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_couro.mjs
// (PYTHON=<executável> troca o Python que sobe os cenários; o padrão é python no Windows e python3 nos outros)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const VERSAO = { proposta: { pasta: path.join(aqui, "couro-aseprite", "rodada1"), tamanhos: [32, 64] },
  rodada2: { pasta: path.join(aqui, "couro-aseprite", "rodada2"), tamanhos: [32, 40, 48, 64] },
  x2: { pasta: path.join(aqui, "couro-aseprite", "rodada2"), tamanhos: [32, 40, 48, 64], x2: true } };
const LUGARES = (process.env.LUGARES || "mercado,saque").split(",");
const R2 = /rodada2|x2/.test(process.env.VERSOES || "");   // com a rodada 2, o atual passa pelos mesmos lugares
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "couro-aseprite", "capturas", "jogo"));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const iconesProposta = (tam) => [
  ['const TAMANHOS = {', `const TAMANHOS = {"gibao": ${JSON.stringify(tam)}, "bota": ${JSON.stringify(tam)}, `],
  ['varinha: "varinha" };', 'varinha: "varinha", gibao: "gibao", bota: "bota" };'],
].reduce((t, [a, b]) => {
  if (!t.includes(a)) throw new Error(`icones.js mudou: não achei ${a}`);
  return t.replace(a, b);
}, readFileSync(path.join(raiz, "rpg/web/static/icones.js"), "utf8"));
async function subir(cenario, amb = {}) {
  const py = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
  const proc = spawn(py, ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const VERSOES = process.env.VERSOES ? process.env.VERSOES.split(",") : ["atual", "proposta"];
const PECAS = ["gibao", "bota"];
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, versao, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  const v = VERSAO[versao];
  if (v) {
    await p.route(/\/static\/icones\.js(\?|$)/, (r) => r.fulfill({ body: iconesProposta(v.tamanhos), contentType: "application/javascript" }));
    await p.route(/\/static\/hud\/icones\/(gibao|bota)-[^/]+\.png/, (r) => {
      let nome = path.basename(new URL(r.request().url()).pathname);
      if (v.x2) nome = nome.replace(/-64(@2x)?\.png$/, "-32@2x.png");   // o 64 vira o 32 ampliado 2×
      return r.fulfill({ path: path.join(v.pasta, nome), contentType: "image/png" });
    });
  }
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  p.on("response", (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) erros.push(`${nome}: ${r.status()} ${r.url()}`); });
  await p.goto(url);
  return p;
}
const parado = (p) => p.waitForFunction(() => typeof pergunta !== "undefined" && pergunta && !processando, null, { timeout: 30000 });
const caixa = (p, sels, folga) => p.evaluate(([ss, f]) => {
  const rs = ss.flatMap((s) => [...document.querySelectorAll(s)]).filter((e) => !e.hidden && e.getBoundingClientRect().width).map((e) => e.getBoundingClientRect());
  if (!rs.length) return null;
  const x = Math.min(...rs.map((r) => r.left)), y = Math.min(...rs.map((r) => r.top));
  return { x: Math.max(0, Math.floor(x - f)), y: Math.max(0, Math.floor(y - f)),
    width: Math.ceil(Math.max(...rs.map((r) => r.right)) - x + 2 * f), height: Math.ceil(Math.max(...rs.map((r) => r.bottom)) - y + 2 * f) };
}, [sels, folga]);
async function recortar(p, sels, nome, folga = 6) {
  const c = await caixa(p, [].concat(sels), folga);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sels} em ${nome})`);
}
async function zoom(p, el, nome) {
  if (!el) return console.log(`  (sem o elemento de ${nome})`);
  await el.scrollIntoViewIfNeeded(); await espera(250);
  await p.evaluate((e) => e.setAttribute("data-foto", "1"), el);
  await recortar(p, "[data-foto]", nome, 2);
  await p.evaluate((e) => e.removeAttribute("data-foto"), el);
}
// onde cada desenho aparece (o arquivo ou o sprite do jogo, o lugar e o tamanho na tela)
const onde = (p) => p.evaluate(() => {
  const lugar = (i) => (i.closest(".slot-px, .achado-arte, .voo-item, .rj-linha, .roda-botao, .carta, .espaco") || i.parentElement).className.split(" ").slice(0, 2).join(".");
  const r = (i) => Math.round(i.getBoundingClientRect().width);
  const sprite = { [Sprites.url("gibao")]: "sprite-gibao", [Sprites.url("bota")]: "sprite-bota" };
  const linhas = {};
  for (const i of document.querySelectorAll("img")) {
    const s = i.getAttribute("src") || "", m = s.match(/hud\/icones\/(gibao|bota|cota|botas-ferro)-(\d+)(@2x)?\.png/);
    const qual = m ? `${m[1]}-${m[2]}${m[3] || ""}` : sprite[s];
    if (qual) (linhas[qual] = linhas[qual] || []).push(`${lugar(i)}→${r(i)}`);
  }
  return linhas;
});
const pegarVoo = (p, sel, ms = 160) => p.evaluate(([s, ms]) => { window.__voo = false;
  new MutationObserver((_, o) => { if (!document.querySelector(s)) return;
    setTimeout(() => { document.getAnimations().forEach((a) => a.pause()); window.__voo = true; }, ms); o.disconnect(); })
    .observe(document.body, { childList: true, subtree: true }); }, [sel, ms]);
const marcar = async (p, nome) => relatorio.push({ nome, ...(await onde(p)) });
async function dica(p, alvo, nome) {
  if (!alvo) return console.log(`  (sem o item da dica em ${nome})`);
  await p.mouse.move(5, 5); await espera(300);
  await p.keyboard.down("Shift");
  await alvo.hover(); await espera(900);
  await p.evaluate((e) => e.setAttribute("data-foto", "1"), alvo);
  await recortar(p, ["[data-foto]", "#dica-item", "#dica-equipado", "#dica-equipado2"], nome, 6);
  await p.evaluate((e) => e.removeAttribute("data-foto"), alvo);
  await p.keyboard.up("Shift");
}

for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) for (const peca of PECAS) {
  const n = (c) => `${jan}-${versao}-${peca}-${c}`;
  let proc, url, p;
  if (LUGARES.includes("mercado")) {
  // 1. o mercado: a ficha e a mochila em 32
  ({ proc, url } = await subir("mercado", { CLASSE: "arqueiro", VESTIR: "gibao,bota", AMOSTRA: peca, SEMENTE: "1" }));
  p = await pagina(url, jan, versao, n("mercado"));
  await parado(p); await espera(900); await p.mouse.move(2, 2); await espera(300);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-mercado")}.png`) });
  await recortar(p, "#heroi", n("ficha"), 0);
  await zoom(p, await p.$(`#heroi [data-mini="${peca === "gibao" ? "armadura" : "pes"}"]`), `zoom-${n("ficha")}`);
  await (await p.$('[data-aba="vender"]')).click(); await espera(800); await p.mouse.move(2, 2); await espera(300);
  await recortar(p, "#lista-vender", n("mercado-vender"), 4);
  await zoom(p, await p.$('[data-mochila-loja="0"]'), `zoom-${n("vender")}`);
  await dica(p, await p.$('[data-mochila-loja="0"]'), n("mercado-dica"));
  await marcar(p, n("mercado"));
  if (R2) {  // o Inventário: o corpo e a mochila em 40
    await p.mouse.move(2, 2); await p.keyboard.press("Escape"); await espera(1500); await parado(p);
    await p.keyboard.press("i"); await espera(1300); await p.mouse.move(2, 2); await espera(300);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-inventario")}.png`) });
    await recortar(p, ".tela.inventario", n("inventario"), 4);
    await zoom(p, await p.$(`.tela.inventario [data-espaco="${peca === "gibao" ? "armadura" : "pes"}"]`), `zoom-${n("corpo")}`);
    await zoom(p, await p.$('.tela.inventario [data-mochila="0"]'), `zoom-${n("mochila")}`);
    await marcar(p, n("inventario"));
  }
  await p.close(); proc.kill();
  }
  if (!LUGARES.includes("saque")) continue;
  // 2. o saque: o cartão do achado em 64
  ({ proc, url } = await subir("vila", { CLASSE: "arqueiro", ACHADO: peca, ...(R2 ? { VESTIR: peca } : {}) }));
  p = await pagina(url, jan, versao, n("saque"));
  await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
  await p.mouse.move(2, 2); await espera(200);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-saque")}.png`) });
  await recortar(p, ".janela-achado", n("saque-cartao"), 6);
  await zoom(p, await p.$(".janela-achado .achado-cartao.novo .achado-arte"), `zoom-${n("saque-64")}`);
  if (R2) await zoom(p, await p.$(".janela-achado .achado-cartao.atual .achado-arte"), `zoom-${n("saque-48")}`);
  await marcar(p, n("saque"));
  if (R2) {  // o voo ao equipar, parado no meio do caminho
    await pegarVoo(p, ".voo-item");
    const eq = await p.$('#prompt .escolha:has-text("Equipar"), .achado-acoes button:has-text("Equipar")');
    if (eq) await eq.click(); else await p.keyboard.press("1");
    try {
      await p.waitForFunction(() => window.__voo, null, { timeout: 8000 });
      await recortar(p, ".voo-item", n("saque-voo"), 16);
      await marcar(p, n("saque-voo"));
      await p.evaluate(() => document.getAnimations().forEach((a) => a.play()));
    } catch { console.log(`  ${n("saque-voo")}: o voo não apareceu`); }
  }
  await p.close(); proc.kill();
  console.log(jan, versao, peca, "ok");
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
for (const r of relatorio) console.log(JSON.stringify(r));
console.log(erros.length ? erros.join("\n") : "sem erros");
