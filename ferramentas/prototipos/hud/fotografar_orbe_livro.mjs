// A proposta do orbe e do livro do Mago (protótipo): fotografa o jogo de verdade com o desenho atual (os sprites 16×16
// "orbe" e "livro") e com a proposta em pixel art (orbe-livro-pixel/, de ferramentas/arte/desenhar_orbe_pixel.py e
// desenhar_livro_pixel.py), com os mesmos dados. Na proposta, a página recebe um icones.js com os dois registrados como
// a integração faria (os tamanhos em TAMANHOS e o papel de equipamento em ITEM) e os arquivos vêm da pasta da
// proposta; o jogo não muda. Os outros papéis do sprite "livro" (o atalho do Diário, que tem desenho próprio, um
// talento, o livro da capela) não passam pelo ITEM: o relatório conta onde cada desenho aparece.
// Os lugares, para o Mago com o orbe e com o livro (as armas Orbe e Grimório; os apoios Foco Arcano e Tomo usam o
// mesmo desenho), em janela normal (1500×950) e baixa (1280×720):
//   - mercado (AMOSTRA=<desenho>, ARMA=<desenho>, SEMENTE=1: a arma vestida e outra na frente da mochila): a tela
//     inteira (a banca e a ficha com o herói), a ficha, a aba Vender e a dica com a comparação (Shift); depois o
//     Inventário (a tela inteira, o corpo e a mochila em 40);
//   - saque (vila, CLASSE=mago, ACHADO e ARMA): a tela inteira com o cartão sobre a vila, o cartão do achado (64) com o
//     que você usa (48) e o voo ao equipar.
// Guarda em capturas-orbe-livro/<janela>-<versao>-<desenho>-<lugar>.png e os recortes pequenos como zoom-...;
// comparar_orbe_livro.py monta as comparações.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_orbe_livro.mjs
// (PROPOSTA=<pasta> e SAIDA=<pasta> trocam a pasta dos desenhos e a das fotos; DESENHOS=orbe fotografa só o orbe)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-orbe-livro"));
const PROPOSTA = path.resolve(process.env.PROPOSTA || path.join(aqui, "orbe-livro-pixel"));
rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const TROCAS = [
  ['const TAMANHOS = {', 'const TAMANHOS = {"orbe": [32, 40, 48, 64], "livro": [32, 40, 48, 64], '],
  ['cajado: "cajado" };', 'cajado: "cajado", orbe: "orbe", livro: "livro" };'],
];
const iconesProposta = TROCAS.reduce((t, [a, b]) => {
  if (!t.includes(a)) throw new Error(`icones.js mudou: não achei ${a}`);
  return t.replace(a, b);
}, readFileSync(path.join(raiz, "rpg/web/static/icones.js"), "utf8"));
async function subir(cenario, amb = {}) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const VERSOES = ["atual", "proposta"];
const DESENHOS = ["orbe", "livro"].filter((d) => !process.env.DESENHOS || process.env.DESENHOS.split(",").includes(d));
const classe = "mago";
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, versao, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  if (versao === "proposta") {
    await p.route(/\/static\/icones\.js(\?|$)/, (r) => r.fulfill({ body: iconesProposta, contentType: "application/javascript" }));
    await p.route(/\/static\/hud\/icones\/(orbe|livro)-[^/]+\.png/, (r) => r.fulfill({
      path: path.join(PROPOSTA, path.basename(new URL(r.request().url()).pathname)), contentType: "image/png" }));
  }
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  p.on("response", (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) erros.push(`${nome}: ${r.status()} ${r.url()}`); });
  await p.goto(url);
  return p;
}
const parado = (p) => p.waitForFunction(() => typeof pergunta !== "undefined" && pergunta && !processando, null, { timeout: 30000 });
async function ate(p, sel) {
  for (let k = 0; k < 60 && !(await p.$(sel)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(900);
}
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
  const sprite = { [Sprites.url("orbe")]: "sprite-orbe", [Sprites.url("livro")]: "sprite-livro" };
  const linhas = {};
  for (const i of document.querySelectorAll("img")) {
    const s = i.getAttribute("src") || "", m = s.match(/hud\/icones\/(orbe|livro)-(\d+)(@2x)?\.png/);
    const qual = m ? `${m[1]}-${m[2]}${m[3] || ""}` : sprite[s];
    if (qual) (linhas[qual] = linhas[qual] || []).push(`${lugar(i)}→${r(i)}`);
  }
  return linhas;
});
const marcar = async (p, nome) => relatorio.push({ nome, ...(await onde(p)) });
const pegarVoo = (p, sel, ms = 160) => p.evaluate(([s, ms]) => { window.__voo = false;
  new MutationObserver((_, o) => { if (!document.querySelector(s)) return;
    setTimeout(() => { document.getAnimations().forEach((a) => a.pause()); window.__voo = true; }, ms); o.disconnect(); })
    .observe(document.body, { childList: true, subtree: true }); }, [sel, ms]);
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

for (const desenho of DESENHOS) for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) {
  const n = (c) => `${jan}-${versao}-${desenho}-${c}`;
  // 1. o mercado e o Inventário
  let { proc, url } = await subir("mercado", { CLASSE: classe, AMOSTRA: desenho, ARMA: desenho, SEMENTE: "1" });
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
  await p.mouse.move(2, 2); await p.keyboard.press("Escape"); await espera(1500); await parado(p);
  await p.keyboard.press("i"); await espera(1300); await p.mouse.move(2, 2); await espera(300);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-inventario")}.png`) });
  await recortar(p, ".tela.inventario", n("inventario"), 4);
  await zoom(p, await p.$('.tela.inventario [data-espaco="arma"]'), `zoom-${n("corpo")}`);
  await zoom(p, await p.$('.tela.inventario [data-mochila="0"]'), `zoom-${n("mochila")}`);
  await marcar(p, n("inventario"));
  await p.close(); proc.kill();
  // 2. o saque: o cartão e o voo ao equipar
  ({ proc, url } = await subir("vila", { CLASSE: classe, ACHADO: desenho, ARMA: desenho }));
  p = await pagina(url, jan, versao, n("saque"));
  await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
  await p.mouse.move(2, 2); await espera(200);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-saque")}.png`) });
  await recortar(p, ".janela-achado", n("saque-cartao"), 6);
  await zoom(p, await p.$(".janela-achado .achado-cartao.novo .achado-arte"), `zoom-${n("saque-64")}`);
  await zoom(p, await p.$(".janela-achado .achado-cartao.atual .achado-arte"), `zoom-${n("saque-48")}`);
  await marcar(p, n("saque-cartao"));
  await pegarVoo(p, ".voo-item");
  const eq = await p.$('#prompt .escolha:has-text("Equipar"), .achado-acoes button:has-text("Equipar")');
  if (eq) await eq.click(); else await p.keyboard.press("1");
  try {
    await p.waitForFunction(() => window.__voo, null, { timeout: 8000 });
    await recortar(p, ".voo-item", n("saque-voo"), 16);
    await marcar(p, n("saque-voo"));
    await p.evaluate(() => document.getAnimations().forEach((a) => a.play()));
  } catch { console.log(`  ${n("saque-voo")}: o voo não apareceu`); }
  await p.close(); proc.kill();
  console.log(desenho, jan, versao, "ok");
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(relatorio, null, 1));
for (const r of relatorio) console.log(JSON.stringify(r));
console.log(erros.length ? erros.join("\n") : "sem erros");
