// A proposta da varinha do Mago desenhada no Aseprite pelo MCP (protótipo): fotografa o jogo de verdade com o desenho
// atual (o sprite 16×16 "varinha") e com a proposta (varinha-aseprite/varinha-32 e -64, com os @2x), com os mesmos
// dados. Na proposta, a página recebe um icones.js com a varinha registrada como a integração faria (os tamanhos em
// TAMANHOS e o papel de equipamento em ITEM) e os arquivos vêm da pasta da proposta; o jogo não muda.
// Os lugares pedidos, para o Mago com a varinha, em janela normal (1500×950) e baixa (1280×720):
//   - mercado (AMOSTRA=varinha, ARMA=varinha, SEMENTE=1: a varinha vestida e outra na frente da mochila): a tela
//     inteira, a ficha (32), a aba Vender (32) e a dica com a comparação (Shift);
//   - saque (vila, CLASSE=mago, ACHADO=varinha e ARMA=varinha): a tela inteira e o cartão do achado (64), com o que
//     você usa ao lado (48: a varinha não tem 48 desenhado, vai o mais perto, como o jogo faz com qualquer peça).
// Guarda em varinha-aseprite/capturas/<janela>-<versao>-<lugar>.png e os recortes pequenos como zoom-...;
// comparar_varinha.py monta as comparações.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_varinha.mjs
// (PYTHON=<executável> troca o Python que sobe os cenários; o padrão é "python")
import { spawn } from "child_process";
import { mkdirSync, readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const PROPOSTA = path.join(aqui, "varinha-aseprite");
const SAIDA = path.join(PROPOSTA, "capturas", "jogo");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const TROCAS = [
  ['const TAMANHOS = {', 'const TAMANHOS = {"varinha": [32, 64], '],
  ['livro: "livro" };', 'livro: "livro", varinha: "varinha" };'],
];
const iconesProposta = TROCAS.reduce((t, [a, b]) => {
  if (!t.includes(a)) throw new Error(`icones.js mudou: não achei ${a}`);
  return t.replace(a, b);
}, readFileSync(path.join(raiz, "rpg/web/static/icones.js"), "utf8"));
async function subir(cenario, amb = {}) {
  const proc = spawn(process.env.PYTHON || "python", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const VERSOES = ["atual", "proposta"];
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, versao, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  if (versao === "proposta") {
    await p.route(/\/static\/icones\.js(\?|$)/, (r) => r.fulfill({ body: iconesProposta, contentType: "application/javascript" }));
    await p.route(/\/static\/hud\/icones\/varinha-[^/]+\.png/, (r) => r.fulfill({
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
// onde o desenho aparece (o arquivo ou o sprite do jogo, o lugar e o tamanho na tela)
const onde = (p) => p.evaluate(() => {
  const lugar = (i) => (i.closest(".slot-px, .achado-arte, .voo-item, .rj-linha, .roda-botao, .carta, .espaco") || i.parentElement).className.split(" ").slice(0, 2).join(".");
  const r = (i) => Math.round(i.getBoundingClientRect().width);
  const sprite = Sprites.url("varinha"), linhas = {};
  for (const i of document.querySelectorAll("img")) {
    const s = i.getAttribute("src") || "", m = s.match(/hud\/icones\/(varinha)-(\d+)(@2x)?\.png/);
    const qual = m ? `${m[1]}-${m[2]}${m[3] || ""}` : s === sprite ? "sprite-varinha" : null;
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

for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) {
  const n = (c) => `${jan}-${versao}-${c}`;
  // 1. o mercado: a ficha e a mochila em 32
  let { proc, url } = await subir("mercado", { CLASSE: "mago", AMOSTRA: "varinha", ARMA: "varinha", SEMENTE: "1" });
  let p = await pagina(url, jan, versao, n("mercado"));
  await parado(p); await espera(900); await p.mouse.move(2, 2); await espera(300);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-mercado")}.png`) });
  await recortar(p, "#heroi", n("ficha"), 0);
  await zoom(p, await p.$(`#heroi [data-mini="arma"]`), `zoom-${n("ficha-arma")}`);
  await (await p.$('[data-aba="vender"]')).click(); await espera(800); await p.mouse.move(2, 2); await espera(300);
  await recortar(p, "#lista-vender", n("mercado-vender"), 4);
  await zoom(p, await p.$('[data-mochila-loja="0"]'), `zoom-${n("vender")}`);
  await dica(p, await p.$('[data-mochila-loja="0"]'), n("mercado-dica"));
  await marcar(p, n("mercado"));
  await p.close(); proc.kill();
  // 2. o saque: o cartão do achado em 64
  ({ proc, url } = await subir("vila", { CLASSE: "mago", ACHADO: "varinha", ARMA: "varinha" }));
  p = await pagina(url, jan, versao, n("saque"));
  await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
  await p.mouse.move(2, 2); await espera(200);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-saque")}.png`) });
  await recortar(p, ".janela-achado", n("saque-cartao"), 6);
  await zoom(p, await p.$(".janela-achado .achado-cartao.novo .achado-arte"), `zoom-${n("saque-64")}`);
  await zoom(p, await p.$(".janela-achado .achado-cartao.atual .achado-arte"), `zoom-${n("saque-48")}`);
  await marcar(p, n("saque"));
  await p.close(); proc.kill();
  console.log(jan, versao, "ok");
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(relatorio, null, 1));
for (const r of relatorio) console.log(JSON.stringify(r));
console.log(erros.length ? erros.join("\n") : "sem erros");
