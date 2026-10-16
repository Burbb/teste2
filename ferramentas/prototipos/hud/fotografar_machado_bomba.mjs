// A proposta do machado e da Bomba de Fumaça (experimento): fotografa o jogo de verdade com o desenho atual (o sprite
// 16×16 "machado" e a "caveira") e com a proposta em pixel art (machado-bomba-pixel/, de
// ferramentas/arte/desenhar_machado_pixel.py e desenhar_bomba_pixel.py), com os mesmos dados.
// Na proposta, a página recebe um icones.js com os dois registrados como a integração faria (os tamanhos em TAMANHOS,
// o machado em ITEM, a bomba em CONSUMIVEL e em SO_PELO_ID) e os arquivos vêm da pasta da proposta; o jogo não muda.
// Os lugares, em janela normal (1500×950) e baixa (1280×720):
//   - vitrine (tutorial, VITRINE=1, ARMA=machado: um machado vestido e outro na mochila, duas bombas na bolsa): a
//     tela da vila, a ficha, o voo de uma bomba ganha até a bolsa, o Inventário (o corpo e a mochila em 40, a bolsa em
//     32), a dica do machado na mochila e a da bomba na bolsa, e a caveira da lixeira (outro papel, não muda);
//   - luta (o mesmo, com uma luta contra um lobo): a janelinha de Itens da roda, com a bomba;
//   - mercado (AMOSTRAS=3, SEMENTE=1, ARMA=machado: a bomba na prateleira, um machado na mochila): a prateleira de
//     suprimentos, a ficha, a aba Vender e a dica do machado com a comparação;
//   - saque (vila, ACHADO=machado, ARMA=machado): o cartão do achado (64) com o que você usa (48), o voo ao equipar;
//   - baú (baus, SUPRIMENTO=bomba_fumaca): o quadro do que saiu.
// Em cada página, conta onde cada desenho aparece e em que tamanho (relatorio.json). Guarda em capturas-machado-bomba/;
// cada foto como <janela>-<versao>-<lugar>.png, e os recortes pequenos dos espaços (para a prancha ampliada) como
// zoom-<janela>-<versao>-<lugar>.png. comparar_machado_bomba.py monta as comparações lado a lado.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_machado_bomba.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele; SO=vitrine,luta,mercado,saque,bau)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-machado-bomba"), PROPOSTA = path.join(aqui, "machado-bomba-pixel");
const SO = new Set((process.env.SO || "vitrine,luta,mercado,saque,bau").split(","));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

// O icones.js da proposta: o de produção com os dois registrados, como na integração. Cada troca precisa achar o
// texto (se o icones.js mudar, o roteiro avisa em vez de fotografar o atual achando que é a proposta).
const TROCAS = [
  ['const TAMANHOS = {', 'const TAMANHOS = {"machado": [32, 40, 48, 64], "bomba": [32], '],
  ['aljava: "aljava", martelo: "martelo" };', 'aljava: "aljava", martelo: "martelo", machado: "machado" };'],
  ['pena_fenix: "pena", unguento: "unguento" };', 'pena_fenix: "pena", unguento: "unguento", bomba_fumaca: "bomba" };'],
  ['new Set(["pena_fenix", "unguento"])', 'new Set(["pena_fenix", "unguento", "bomba_fumaca"])'],
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
const VERSOES = (process.env.VERSOES || "atual,proposta").split(",");
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, versao, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  if (versao === "proposta") {
    await p.route(/\/static\/icones\.js(\?|$)/, (r) => r.fulfill({ body: iconesProposta, contentType: "application/javascript" }));
    await p.route(/\/static\/hud\/icones\/(machado|bomba)-[^/]+\.png/, (r) => r.fulfill({
      path: path.join(PROPOSTA, path.basename(new URL(r.request().url()).pathname)), contentType: "image/png" }));
  }
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  p.on("response", (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) erros.push(`${nome}: ${r.status()} ${r.url()}`); });
  await p.goto(url);
  return p;
}
const parado = (p) => p.waitForFunction(() => typeof pergunta !== "undefined" && pergunta && !processando, null, { timeout: 30000 });
async function ate(p, sel) {  // passa as orientações e os "continuar" até `sel` aparecer
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
// onde cada desenho de machado e de bomba aparece (o arquivo, ou o sprite do jogo, o lugar e o tamanho na tela), e os
// outros papéis dos mesmos sprites (a caveira da lixeira e dos retratos, o machado do Redemoinho e da Fúria)
const onde = (p) => p.evaluate(() => {
  const lugar = (i) => (i.closest(".slot-px, .achado-arte, .voo-item, .item-voando, .achado-espolio, .rj-linha, .mercadoria, .carta, .espaco, .roda-botao, .estado") || i.parentElement).className.split(" ").slice(0, 2).join(".");
  const r = (i) => Math.round(i.getBoundingClientRect().width);
  const sprite = { [Sprites.url("machado")]: "sprite-machado", [Sprites.url("caveira")]: "sprite-caveira" };
  const linhas = {};
  for (const i of document.querySelectorAll("img")) {
    const s = i.getAttribute("src") || "", m = s.match(/hud\/icones\/(machado|bomba)-(\d+)(@2x)?\.png/);
    const qual = m ? `${m[1]}-${m[2]}${m[3] || ""}` : sprite[s];
    if (qual) (linhas[qual] = linhas[qual] || []).push(`${lugar(i)}→${r(i)}`);
  }
  return linhas;
});
const marcar = async (p, nome) => relatorio.push({ nome, ...(await onde(p)) });
// pausa as animações quando `sel` aparece (para fotografar o voo no meio do caminho)
const pegarVoo = (p, sel, ms = 160) => p.evaluate(([s, ms]) => { window.__voo = false;
  new MutationObserver((_, o) => { if (!document.querySelector(s)) return;
    setTimeout(() => { document.getAnimations().forEach((a) => a.pause()); window.__voo = true; }, ms); o.disconnect(); })
    .observe(document.body, { childList: true, subtree: true }); }, [sel, ms]);
async function voo(p, sel, nome) {
  try {
    await p.waitForFunction(() => window.__voo, null, { timeout: 8000 });
    await recortar(p, sel, nome, 16);
    await marcar(p, nome);
    await p.evaluate(() => document.getAnimations().forEach((a) => a.play()));
  } catch { console.log(`  ${nome}: o voo não apareceu`); }
}
async function dica(p, alvo, nome) {  // o espaço com o item e a dica dele (com o equipado ao lado, quando compara)
  if (!alvo) return console.log(`  (sem o item da dica em ${nome})`);
  await p.mouse.move(5, 5); await espera(300);
  await alvo.hover(); await espera(900);
  await p.evaluate((e) => e.setAttribute("data-foto", "1"), alvo);
  await recortar(p, ["[data-foto]", "#dica-item", "#dica-equipado", "#dica-equipado2"], nome, 6);
  await p.evaluate((e) => e.removeAttribute("data-foto"), alvo);
  await marcar(p, nome);
}
async function zoom(p, el, nome) {  // o recorte pequeno de um elemento (para a prancha ampliada)
  if (!el) return console.log(`  (sem o elemento de ${nome})`);
  await el.scrollIntoViewIfNeeded(); await espera(250);  // na janela baixa, a bolsa e a prateleira ficam abaixo da dobra
  await p.evaluate((e) => e.setAttribute("data-foto", "1"), el);
  await recortar(p, "[data-foto]", nome, 2);
  await p.evaluate((e) => e.removeAttribute("data-foto"), el);
}
// o primeiro elemento de `sel` cuja dica ou texto fala de `nome`
const pelo = (p, sel, nome) => p.evaluateHandle(([s, n]) => [...document.querySelectorAll(s)].find((e) =>
  new RegExp(n, "i").test(`${e.textContent} ${e.getAttribute("aria-label") || ""} ${e.dataset.usar || ""} ${e.dataset.bolsa || ""} ${e.dataset.comprar || ""} ${e.querySelector("img") ? e.querySelector("img").getAttribute("src") : ""}`)) || null, [sel, nome])
  .then((h) => h.asElement());

const VITRINE = { TUTORIAL: "0", VITRINE: "1", ARMA: "machado", VISTAS: "A1,V2,N1,D1,K1,M1,L1" };
for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) {
  const n = (c) => `${jan}-${versao}-${c}`;
  // 1. a vitrine: a ficha, o voo da bomba, o Inventário e as dicas
  if (SO.has("vitrine")) {
    const { proc, url } = await subir("tutorial", VITRINE);
    const p = await pagina(url, jan, versao, n("vitrine"));
    await ate(p, "#predios .predio");
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-vila")}.png`) });
    await recortar(p, "#heroi", n("ficha"), 0);
    await marcar(p, n("ficha"));
    await pegarVoo(p, ".item-voando", 380);  // uma bomba ganha num evento: sai do texto e voa até a bolsa
    await p.evaluate(() => itemVoa(document.querySelector("#texto") || document.querySelector("#pagina"), "bomba_fumaca"));
    await voo(p, ".item-voando", n("voo-bomba"));
    await espera(1200);
    await (await p.$('#doca .atalho[data-rotulo="Inventário"]')).click(); await espera(1300);
    await p.mouse.move(2, 2); await espera(300);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-inventario")}.png`) });
    await recortar(p, ".tela.inventario", n("inventario"), 4);
    await marcar(p, n("inventario"));
    await zoom(p, await p.$('.tela.inventario [data-espaco="arma"]'), `zoom-${n("corpo-machado")}`);
    const im = await p.evaluate(() => App.estado.heroi.mochila.findIndex((x) => x.icone === "machado"));
    const mochila = await p.$(`.tela.inventario [data-mochila="${im}"]`);
    await zoom(p, mochila, `zoom-${n("mochila-machado")}`);
    await zoom(p, await p.$('.tela.inventario [data-usar="bomba_fumaca"]'), `zoom-${n("bolsa-bomba")}`);
    await zoom(p, await p.$(".tela.inventario .lixeira"), `zoom-${n("lixeira")}`);
    await dica(p, mochila, n("dica-machado"));
    await dica(p, await p.$('.tela.inventario [data-usar="bomba_fumaca"]'), n("dica-bomba"));
    await p.close(); proc.kill();
  }
  // 2. a luta: a janelinha de Itens da roda, com a bomba
  if (SO.has("luta")) {
    const { proc, url } = await subir("tutorial", { ...VITRINE, LUTA: "lobo", QUANTOS: "1" });
    const p = await pagina(url, jan, versao, n("luta"));
    await ate(p, '#roda .roda-botao[data-slot="itens"]');
    await (await p.$('#roda .roda-botao[data-slot="itens"]')).click(); await espera(900);
    await p.mouse.move(2, 2); await espera(300);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-luta-itens")}.png`) });
    await recortar(p, ".roda-janela", n("luta-itens"), 6);
    await zoom(p, await pelo(p, ".roda-janela .rj-linha", "Fumaça"), `zoom-${n("luta-bomba")}`);
    await marcar(p, n("luta-itens"));
    await p.close(); proc.kill();
  }
  // 3. o mercado: a prateleira com a bomba, a ficha, a aba Vender e a dica do machado
  if (SO.has("mercado")) {
    const { proc, url } = await subir("mercado", { CLASSE: "guerreiro", AMOSTRAS: "3", SEMENTE: "1", ARMA: "machado" });
    const p = await pagina(url, jan, versao, n("mercado"));
    await parado(p); await espera(900);
    await p.mouse.move(2, 2); await espera(300);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-mercado")}.png`) });
    await recortar(p, "#lista-suprimentos", n("mercado-suprimentos"), 4);
    await zoom(p, await p.$('#lista-suprimentos [data-comprar="bomba_fumaca"]'), `zoom-${n("prateleira-bomba")}`);
    await recortar(p, "#heroi", n("mercado-ficha"), 0);
    await marcar(p, n("mercado-suprimentos"));
    await (await p.$('[data-aba="vender"]')).click(); await espera(800);
    await recortar(p, "#lista-vender", n("mercado-vender"), 4);
    const venda = await pelo(p, "#lista-vender .slot-px", "machado");
    await zoom(p, venda, `zoom-${n("vender-machado")}`);
    await dica(p, venda, n("mercado-dica-machado"));
    await p.close(); proc.kill();
  }
  // 4. o saque: o cartão com o machado achado (64) e o que você usa (48), e o voo ao equipar
  if (SO.has("saque")) {
    const { proc, url } = await subir("vila", { ACHADO: "machado", ARMA: "machado" });
    const p = await pagina(url, jan, versao, n("saque"));
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-saque")}.png`) });
    await recortar(p, ".janela-achado", n("saque-cartao"), 6);
    await zoom(p, await p.$(".janela-achado .achado-cartao.novo .achado-arte"), `zoom-${n("saque-64")}`);
    await zoom(p, await p.$(".janela-achado .achado-cartao.atual .achado-arte"), `zoom-${n("saque-48")}`);
    await marcar(p, n("saque-cartao"));
    await pegarVoo(p, ".voo-item");
    const eq = await p.$('#prompt .escolha:has-text("Equipar"), .achado-acoes button:has-text("Equipar")');
    if (eq) await eq.click(); else await p.keyboard.press("1");
    await voo(p, ".voo-item", n("saque-voo"));
    await espera(1500);
    await recortar(p, "#heroi", n("saque-ficha-depois"), 0);
    await p.close(); proc.kill();
  }
  // 5. o baú: o quadro do que saiu, com a bomba
  if (SO.has("bau")) {
    const { proc, url } = await subir("baus", { BAUS: "1", SUPRIMENTO: "bomba_fumaca" });
    const p = await pagina(url, jan, versao, n("bau"));
    await parado(p); await espera(800);
    await (await p.$('#heroi [data-bolsa="bau"]')).click();
    await p.waitForSelector(".achado-espolio", { timeout: 15000 }).catch(() => console.log(`  ${n("bau")}: sem o quadro do baú`));
    await espera(700);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-bau")}.png`) });
    const quadro = await p.evaluate(() => { const e = document.querySelector(".achado-espolio"); const q = e && e.closest(".espolio, .conquista, .quadro-espolio, .caixa-espolio, [class*=espolio]:not(.achado-espolio)"); return q ? "." + q.className.split(" ").join(".") : null; });
    await recortar(p, quadro || ".achado-espolio", n("bau-quadro"), 8);
    await zoom(p, await pelo(p, ".achado-espolio", "Fumaça"), `zoom-${n("bau-bomba")}`);
    await marcar(p, n("bau-quadro"));
    await p.close(); proc.kill();
  }
  console.log(jan, versao, "ok");
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(relatorio, null, 1));
for (const r of relatorio) console.log(JSON.stringify(r));
console.log(erros.length ? erros.join("\n") : "sem erros");
