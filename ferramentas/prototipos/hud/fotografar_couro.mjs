// O peitoral e as botas de couro (os desenhos "gibao" e "bota"), rodada 1 da proposta (protótipo): fotografa o jogo de
// verdade com os desenhos atuais (os sprites 16×16) e com a proposta (couro-aseprite/rodada1/gibao-32 e -64,
// bota-32 e -64, com os @2x), com os mesmos dados. Na proposta, a página recebe um icones.js com as duas peças
// registradas como a integração faria (TAMANHOS em 32 e 64 e o papel de equipamento em ITEM) e os arquivos vêm da
// pasta da proposta; o jogo não muda. Os lugares, para o Arqueiro, em janela normal (1500×950) e baixa (1280×720):
//   - mercado (CLASSE=arqueiro, VESTIR=gibao,bota, AMOSTRA=<peça>, SEMENTE=1): a tela inteira, a ficha (32), a aba
//     Vender (32) e a dica com a comparação (Shift), uma rodada por peça;
//   - saque (vila, CLASSE=arqueiro, ACHADO=<peça>): a tela inteira e o cartão do achado (64). O "você usa" fica com a
//     peça de ferro que o cenário veste (48 nativo): nesta rodada o couro não tem 48, e a página não mostra um.
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
const PROPOSTA = path.join(aqui, "couro-aseprite", "rodada1");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "couro-aseprite", "capturas", "jogo"));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const iconesProposta = [
  ['const TAMANHOS = {', 'const TAMANHOS = {"gibao": [32, 64], "bota": [32, 64], '],
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
  if (versao === "proposta") {
    await p.route(/\/static\/icones\.js(\?|$)/, (r) => r.fulfill({ body: iconesProposta, contentType: "application/javascript" }));
    await p.route(/\/static\/hud\/icones\/(gibao|bota)-[^/]+\.png/, (r) => r.fulfill({
      path: path.join(PROPOSTA, path.basename(new URL(r.request().url()).pathname)), contentType: "image/png" }));
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
  // 1. o mercado: a ficha e a mochila em 32
  let { proc, url } = await subir("mercado", { CLASSE: "arqueiro", VESTIR: "gibao,bota", AMOSTRA: peca, SEMENTE: "1" });
  let p = await pagina(url, jan, versao, n("mercado"));
  await parado(p); await espera(900); await p.mouse.move(2, 2); await espera(300);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-mercado")}.png`) });
  await recortar(p, "#heroi", n("ficha"), 0);
  await zoom(p, await p.$(`#heroi [data-mini="${peca === "gibao" ? "armadura" : "pes"}"]`), `zoom-${n("ficha")}`);
  await (await p.$('[data-aba="vender"]')).click(); await espera(800); await p.mouse.move(2, 2); await espera(300);
  await recortar(p, "#lista-vender", n("mercado-vender"), 4);
  await zoom(p, await p.$('[data-mochila-loja="0"]'), `zoom-${n("vender")}`);
  await dica(p, await p.$('[data-mochila-loja="0"]'), n("mercado-dica"));
  await marcar(p, n("mercado"));
  await p.close(); proc.kill();
  // 2. o saque: o cartão do achado em 64
  ({ proc, url } = await subir("vila", { CLASSE: "arqueiro", ACHADO: peca }));
  p = await pagina(url, jan, versao, n("saque"));
  await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
  await p.mouse.move(2, 2); await espera(200);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-saque")}.png`) });
  await recortar(p, ".janela-achado", n("saque-cartao"), 6);
  await zoom(p, await p.$(".janela-achado .achado-cartao.novo .achado-arte"), `zoom-${n("saque-64")}`);
  await marcar(p, n("saque"));
  await p.close(); proc.kill();
  console.log(jan, versao, peca, "ok");
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
for (const r of relatorio) console.log(JSON.stringify(r));
console.log(erros.length ? erros.join("\n") : "sem erros");
