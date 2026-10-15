// Conferência dos desenhos de item no jogo de verdade (o escudo e o Unguento de Prata da 1.94.0; o equipamento em 40 px
// no Inventário da 1.95.0), sem nenhum arquivo do protótipo, em janela normal (1500×950) e baixa (1280×720):
//   - o mercado (cenário mercado, AMOSTRAS=2, SEMENTE=1: um escudo na mochila, um unguento na bolsa e outro na
//     prateleira): a prateleira de suprimentos, a compra, a bolsa da ficha e a aba Vender com a dica de comparação;
//   - o cartão do saque com um escudo e a comparação com o que se usa (cenário vila, ACHADO=escudo) e o voo ao equipar;
//   - o baú aberto com um unguento dentro (cenário baus, SUPRIMENTO=unguento): o quadro do que saiu;
//   - o Inventário com o corpo e a mochila cheios (cenário tutorial, VITRINE=2): o equipamento, os anéis, a bolsa, a
//     dica e a comparação dos dois anéis; o voo de um unguento ganho até a bolsa (itemVoa, a mesma chamada do chip de
//     um evento). A Curandeira continua com o desenho dela (conferido em cada página: "curandeira").
// Em cada página, conta onde cada desenho aparece e em que tamanho. Guarda em SAIDA (padrão: capturas-itens/ ao lado).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/arte/fotografar_itens.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele; SO=mercado,saque,bau,inventario para escolher)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-itens"));
const SO = new Set((process.env.SO || "mercado,saque,bau,inventario").split(","));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
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
const parado = (p) => p.waitForFunction(() => typeof pergunta !== "undefined" && pergunta && !processando, null, { timeout: 30000 });
async function recortar(p, sel, nome, folga = 6) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, Math.floor(r.x - f)), y: Math.max(0, Math.floor(r.y - f)), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
// onde cada desenho de item aparece: o arquivo (sem o @2x), o lugar e o tamanho na tela; e o que ainda é sprite do jogo
const onde = (p) => p.evaluate(() => {
  const lugar = (i) => (i.closest(".slot-px, .achado-arte, .voo-item, .item-voando, .achado-espolio, .loja-topo, .rb-icone, .dica, .servico") || i.parentElement).className.split(" ").slice(0, 2).join(".");
  const r = (i) => Math.round(i.getBoundingClientRect().width);
  const linhas = {};
  for (const i of document.querySelectorAll("img")) {
    const s = i.getAttribute("src") || "";
    const m = s.match(/hud\/icones\/([a-z-]+)-(\d+)(@2x)?\.png/);
    if (!m || !/^(escudo|unguento|anel|cota|espada|elmo|manopla|perneiras|botas-ferro|maca|amuleto|aljava)$/.test(m[1])) continue;
    (linhas[m[1]] = linhas[m[1]] || []).push(`${lugar(i)}:${m[2]}${m[3] || ""}→${r(i)}`);
  }
  return { ...linhas, curandeira: typeof Icones !== "undefined" && Icones.porDesenho("unguento") === "" ? "sprite do jogo" : "TROCADA" };
});
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  p.on("requestfailed", (r) => { if (!/ERR_ABORTED/.test(r.failure().errorText)) erros.push(`${nome}: falhou ${r.url()}`); });
  p.on("response", (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) erros.push(`${nome}: ${r.status()} ${r.url()}`); });
  await p.goto(url);
  return p;
}
// pausa as animações quando `sel` aparece (para fotografar o voo no meio do caminho)
const pegarVoo = (p, sel, ms = 160) => p.evaluate(([s, ms]) => { window.__voo = false;
  new MutationObserver((_, o) => { if (!document.querySelector(s)) return;
    setTimeout(() => { document.getAnimations().forEach((a) => a.pause()); window.__voo = true; }, ms); o.disconnect(); })
    .observe(document.body, { childList: true, subtree: true }); }, [sel, ms]);
async function voo(p, sel, nome) {
  try {
    await p.waitForFunction(() => window.__voo, null, { timeout: 8000 });
    await recortar(p, sel, nome, 16);
    relatorio.push({ nome, ...(await onde(p)) });
    await p.evaluate(() => document.getAnimations().forEach((a) => a.play()));
  } catch { console.log(`  ${nome}: o voo não apareceu`); }
}
async function dica(p, alvo, nome) {  // a dica do item com o equipado ao lado (a comparação)
  await p.mouse.move(5, 5); await espera(300);
  await alvo.hover(); await espera(900);
  const c = await p.evaluate(() => { const rs = ["#dica-item", "#dica-equipado", "#dica-equipado2"].map((s) => document.querySelector(s)).filter((e) => e && !e.hidden && e.getBoundingClientRect().width).map((e) => e.getBoundingClientRect());
    if (!rs.length) return null; const x = Math.min(...rs.map((r) => r.left)), y = Math.min(...rs.map((r) => r.top));
    return { x: Math.max(0, Math.floor(x - 4)), y: Math.max(0, Math.floor(y - 4)), width: Math.ceil(Math.max(...rs.map((r) => r.right)) - x + 8), height: Math.ceil(Math.max(...rs.map((r) => r.bottom)) - y + 8) }; });
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem a dica em ${nome})`);
  relatorio.push({ nome, ...(await onde(p)) });
}

// 1. o mercado
if (SO.has("mercado")) {
  for (const jan of Object.keys(JANELAS)) {  // um jogo por janela: comprar muda o jogo
    const { proc, url } = await subir("mercado", { CLASSE: "guerreiro", AMOSTRAS: "2", SEMENTE: "1" });
    const nome = `mercado-${jan}`;
    const p = await pagina(url, jan, nome);
    await parado(p); await espera(800);
    await p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
    await recortar(p, "#lista-suprimentos", `${nome}-suprimentos`, 4);
    await recortar(p, "#heroi", `${nome}-ficha`, 0);
    relatorio.push({ nome: `${nome} suprimentos`, ...(await onde(p)) });
    const unguento = await p.$('#lista-suprimentos [data-comprar="unguento"]:not(.caro)');
    if (unguento) {  // a compra: a bolsa passa a ter dois
      await unguento.click(); await espera(1200);
      await recortar(p, '#lista-suprimentos [data-comprar="unguento"]', `${nome}-comprado`, 4);
      await recortar(p, "#heroi", `${nome}-ficha-depois`, 0);
    } else console.log(`  ${nome}: o mercador não tem unguento hoje (a prateleira mostra esgotado)`);
    await (await p.$('[data-aba="vender"]')).click(); await espera(700);
    await recortar(p, "#lista-vender", `${nome}-vender`, 4);
    const escudo = await p.$("#lista-vender .slot-px");
    if (escudo) await dica(p, escudo, `${nome}-dica-escudo`);
    await p.close();
    proc.kill();
  }
}
// 2. o cartão do saque com um escudo, a comparação e o voo ao equipar
if (SO.has("saque")) {
  for (const jan of Object.keys(JANELAS)) {  // um jogo por janela: equipar muda o jogo
    const { proc, url } = await subir("vila", { ACHADO: "escudo" });
    const nome = `saque-${jan}`;
    const p = await pagina(url, jan, nome);
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2500);
    await recortar(p, ".janela-achado", `${nome}-cartao`, 6);
    relatorio.push({ nome: `${nome} cartão`, ...(await onde(p)) });
    await pegarVoo(p, ".voo-item");
    const eq = await p.$('#prompt .escolha:has-text("Equipar"), .achado-acoes button:has-text("Equipar")');
    if (eq) await eq.click(); else await p.keyboard.press("1");
    await voo(p, ".voo-item", `${nome}-voo`);
    await espera(1500);
    await recortar(p, "#heroi", `${nome}-ficha-depois`, 0);
    await p.close();
    proc.kill();
  }
}
// 3. o baú aberto com um unguento: o quadro do que saiu e o voo para a bolsa
if (SO.has("bau")) {
  for (const jan of Object.keys(JANELAS)) {
    const { proc, url } = await subir("baus", { BAUS: "1", SUPRIMENTO: "unguento" });
    const nome = `bau-${jan}`;
    const p = await pagina(url, jan, nome);
    await parado(p); await espera(800);
    await (await p.$('#heroi [data-bolsa="bau"]')).click();
    await p.waitForSelector(".achado-espolio", { timeout: 15000 }).catch(() => console.log(`  ${nome}: sem o quadro do baú`));
    await espera(600);
    const quadro = await p.evaluate(() => { const e = document.querySelector(".achado-espolio"); const q = e && e.closest(".espolio, .conquista, .quadro-espolio, .caixa-espolio, [class*=espolio]:not(.achado-espolio)"); return q ? "." + q.className.split(" ").join(".") : null; });
    await recortar(p, quadro || ".achado-espolio", `${nome}-quadro`, 8);
    relatorio.push({ nome: `${nome} quadro`, ...(await onde(p)) });
    await p.close();
    proc.kill();
  }
}
// 4. o Inventário cheio (o escudo, o anel e a cota vestidos; espada, escudo e anel na mochila; unguento na bolsa)
if (SO.has("inventario")) {
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", VITRINE: "2" });
  for (const jan of Object.keys(JANELAS)) {
    const nome = `inventario-${jan}`;
    const p = await pagina(url, jan, nome);
    await parado(p); await espera(800);
    await recortar(p, "#heroi", `${nome}-ficha`, 0);
    relatorio.push({ nome: `${nome} ficha`, ...(await onde(p)) });
    await pegarVoo(p, ".item-voando", 380);  // um unguento ganho num evento: sai do texto e voa até a bolsa
    await p.evaluate(() => itemVoa(document.querySelector("#texto") || document.querySelector("#pagina"), "unguento"));
    await voo(p, ".item-voando", `${nome}-voo-unguento`);
    await espera(1200);
    await p.keyboard.press("i"); await espera(1200);
    await p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
    await recortar(p, ".tela.inventario, .inventario", `${nome}-tela`, 4);
    relatorio.push({ nome: `${nome} tela`, ...(await onde(p)) });
    const anel = await p.$('[data-mochila] img[src*="anel-"]');
    if (anel) await dica(p, anel, `${nome}-dica-anel`);  // a comparação dos dois anéis (um vestido, um vazio)
    const escudoCorpo = await p.$('[data-espaco="secundaria"], [data-slot="secundaria"]');
    if (escudoCorpo) await dica(p, escudoCorpo, `${nome}-dica-escudo-vestido`);
    await p.keyboard.press("Escape"); await espera(600);
    if (jan === "normal") {  // a Curandeira do Vau: o balcão dela continua com o desenho do jogo
      const entrou = await p.evaluate(() => { try { entrarNoPredio("curandeiro"); return true; } catch { return false; } });
      await espera(1200);
      if (entrou) { await recortar(p, "#prompt", `${nome}-curandeira`, 4); relatorio.push({ nome: `${nome} curandeira`, ...(await onde(p)) }); }
    }
    await p.close();
  }
  proc.kill();
}
await b.close();
for (const r of relatorio) console.log(r.nome, "·", Object.entries(r).filter(([k]) => k !== "nome").map(([k, v]) => `${k} ${JSON.stringify(v)}`).join(" · "));
writeFileSync(path.join(SAIDA, "onde.json"), JSON.stringify(relatorio, null, 1));
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
