// Conferência dos desenhos de item no jogo de verdade (o escudo e o Unguento de Prata da 1.94.0; o equipamento em 40 px
// no Inventário da 1.95.0; o machado e a Bomba de Fumaça da 1.99.0; o arco da 1.101.0; o cajado da 1.106.0; o orbe da 1.107.0; o grimório da 1.108.0; a varinha da 1.109.0), sem nenhum arquivo do protótipo, em janela normal (1500×950) e baixa (1280×720):
//   - o mercado (cenário mercado, AMOSTRAS=2, SEMENTE=1: um escudo na mochila, um unguento na bolsa e outro na
//     prateleira): a prateleira de suprimentos, a compra, a bolsa da ficha e a aba Vender com a dica de comparação;
//   - o cartão do saque com um escudo e a comparação com o que se usa (cenário vila, ACHADO=escudo) e o voo ao equipar;
//   - o baú aberto com um unguento dentro (cenário baus, SUPRIMENTO=unguento): o quadro do que saiu;
//   - o Inventário com o corpo e a mochila cheios (cenário tutorial, VITRINE=2): o equipamento, os anéis, a bolsa, a
//     dica e a comparação dos dois anéis; o voo de um unguento ganho até a bolsa (itemVoa, a mesma chamada do chip de
//     um evento). A Curandeira continua com o desenho dela (conferido em cada página: "curandeira");
//   - os anéis (cenário aneis: dois vestidos, um achado guardado e outro na mochila): a dica que compara com os dois,
//     arrastar um anel para o segundo espaço, dois cliques para vestir, o teclado (i abre, Esc fecha);
//   - os desenhos que ainda não têm 40 px (cenário mercado, CLASSE=arqueiro, AMOSTRAS=1: o martelo desenhado em 32 e
//     os sprites 16×16 do arco, do cajado...), que ficam em 32 px, centrados, no Inventário.
//   - o machado e a Bomba de Fumaça (1.99.0, SO=machado): o Inventário com o machado vestido e na mochila, a bomba
//     na bolsa, as dicas e a comparação; a compra da bomba, a compra, a venda e a recompra do machado no mercado; o
//     cartão do saque e o voo ao equipar; o quadro do baú com a bomba e o voo dela até a bolsa; a janelinha de Itens
//     da luta; o movimento normal e o reduzido (os voos); e os outros papéis da caveira (a lixeira, o Bestiário) e
//     do machado (Redemoinho, Fúria), que continuam com o sprite do jogo.
// Em cada página, conta onde cada desenho aparece e em que tamanho. Guarda em SAIDA (padrão: capturas-itens/ ao lado).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/arte/fotografar_itens.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele; SO=mercado,saque,bau,inventario para escolher)
// (PYTHON=<executável> troca o Python que sobe os cenários; o padrão é python no Windows e python3 nos outros)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-itens"));
const SO = new Set((process.env.SO || "mercado,saque,bau,inventario,aneis,antigos,machado,arco,cajado,orbe,livro,varinha").split(","));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(cenario, amb = {}) {
  const proc = spawn(process.env.PYTHON || (process.platform === "win32" ? "python" : "python3"), ["-m", "tests.navegador.cenarios", cenario],
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
    if (!m || !/^(escudo|unguento|anel|cota|espada|elmo|manopla|perneiras|botas-ferro|maca|amuleto|aljava|machado|bomba|arco|cajado|orbe|livro|varinha)$/.test(m[1])) continue;
    (linhas[m[1]] = linhas[m[1]] || []).push(`${lugar(i)}:${m[2]}${m[3] || ""}→${r(i)}`);
  }
  // os papéis que não mudam: a Curandeira, a caveira (a lixeira e os outros usos) e o machado das habilidades
  const sprite = (n) => [...document.querySelectorAll("img")].filter((i) => i.getAttribute("src") === Sprites.url(n)).map(lugar);
  const caveira = sprite("caveira"), machado = sprite("machado"), arco = sprite("arco"), cajado = sprite("cajado");
  return { ...linhas, curandeira: typeof Icones !== "undefined" && Icones.porDesenho("unguento") === "" ? "sprite do jogo" : "TROCADA",
    ...(caveira.length ? { "sprite-caveira": caveira } : {}), ...(machado.length ? { "sprite-machado": machado } : {}),
    ...(arco.length ? { "sprite-arco": arco } : {}), ...(cajado.length ? { "sprite-cajado": cajado } : {}) };
});
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, nome, opcoes = {}) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H }, ...opcoes });
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
// o tamanho de cada desenho no corpo e na mochila do Inventário: a família de ferro (40), o resto (32)
const medidas = (p) => p.evaluate(() => [...document.querySelectorAll(".tela.inventario .espaco img, .tela.inventario .celula img")].map((i) => {
  const s = i.getAttribute("src") || "", m = s.match(/hud\/icones\/([a-z-]+)-(\d+)/);
  const tipo = m ? `${m[1]}-${m[2]}` : s.startsWith("data:") || s.startsWith("blob:") ? (i.classList.contains("desenho") ? "desenhado" : "sprite") : s.slice(-20);
  const r = i.getBoundingClientRect(), c = i.parentElement.getBoundingClientRect();
  return `${i.closest(".espaco") ? "corpo" : "mochila"}:${tipo}:${Math.round(r.width)}px:centro${Math.round(r.left + r.width / 2 - c.left - c.width / 2)},${Math.round(r.top + r.height / 2 - c.top - c.height / 2)}${i.classList.contains("fantasma") ? ":vazio" : ""}`;
}));
// 5. os anéis: a comparação com os dois, arrastar, dois cliques, o teclado
if (SO.has("aneis")) {
  for (const jan of Object.keys(JANELAS)) {
    const { proc, url } = await subir("aneis", { ANEIS: "2" });
    const nome = `aneis-${jan}`;
    const p = await pagina(url, jan, nome);
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2500);
    await recortar(p, ".janela-achado", `${nome}-achado`, 6);
    const guardar = await p.$('.achado-acoes button:has-text("Guardar"), #prompt .escolha:has-text("Guardar")');
    if (guardar) await guardar.click(); else console.log(`  ${nome}: sem o Guardar`);
    await espera(1500); await parado(p);
    await p.keyboard.press("i"); await espera(1200);
    const aberto = await p.$(".tela.inventario");
    await recortar(p, ".tela.inventario", `${nome}-inventario`, 4);
    relatorio.push({ nome: `${nome} inventário`, medidas: await medidas(p) });
    const anel = await p.$('[data-mochila] img[src*="anel-"]');
    if (anel) await dica(p, anel, `${nome}-dica-dois-aneis`);
    await p.mouse.move(5, 5); await espera(300);
    // arrastar o primeiro anel da mochila para o segundo espaço de anel
    const antes = await p.evaluate(() => App.estado.heroi.equip.anel2 && App.estado.heroi.equip.anel2.nome);
    await p.locator("[data-mochila]").first().dragTo(p.locator('[data-espaco="anel2"]'));
    await espera(1500);
    const depois = await p.evaluate(() => App.estado.heroi.equip.anel2 && App.estado.heroi.equip.anel2.nome);
    relatorio.push({ nome: `${nome} arrastar`, anel2: `${antes} → ${depois}`, trocou: antes !== depois });
    await recortar(p, ".tela.inventario", `${nome}-depois-de-arrastar`, 4);
    // dois cliques num anel da mochila com os dois espaços ocupados: o menu pergunta qual substituir (o foco já está
    // no primeiro); o Enter escolhe
    const mochilaAntes = await p.evaluate(() => App.estado.heroi.mochila.map((x) => x.nome).join(", "));
    await p.locator("[data-mochila]").first().dblclick(); await espera(700);
    await recortar(p, ".menu-espaco", `${nome}-menu-substituir`, 4);
    await p.keyboard.press("Enter"); await espera(1500);
    const mochilaDepois = await p.evaluate(() => App.estado.heroi.mochila.map((x) => x.nome).join(", "));
    relatorio.push({ nome: `${nome} dois cliques e Enter`, mochila: `${mochilaAntes} → ${mochilaDepois}` });
    await recortar(p, ".tela.inventario", `${nome}-depois-de-vestir`, 4);
    await p.mouse.click(5, 5); await espera(300);
    await p.keyboard.press("Escape"); await espera(900);
    const fechou = !(await p.$(".tela.inventario"));
    await p.keyboard.press("i"); await espera(1200);
    relatorio.push({ nome: `${nome} teclado`, abriu: !!aberto, esc_fecha: fechou, i_abre: !!(await p.$(".tela.inventario")) });
    await p.close();
    proc.kill();
  }
}
// 6. os desenhos sem 40 px: o martelo (32, desenhado em código) e os sprites 16×16 de outras classes
if (SO.has("antigos")) {
  const { proc, url } = await subir("mercado", { CLASSE: "arqueiro", AMOSTRAS: "1" });
  for (const jan of Object.keys(JANELAS)) {
    const nome = `antigos-${jan}`;
    const p = await pagina(url, jan, nome);
    await parado(p); await espera(800);
    await p.keyboard.press("Escape"); await espera(1500); await parado(p);  // sai do mercado para a vila
    await p.keyboard.press("i"); await espera(1200);
    await recortar(p, ".tela.inventario", `${nome}-inventario`, 4);
    relatorio.push({ nome: `${nome} inventário`, medidas: await medidas(p) });
    await p.close();
  }
  proc.kill();
}
// 7. o machado e a Bomba de Fumaça (1.99.0), com o movimento normal e o reduzido
const zoom = async (p, el, nome) => {  // um espaço só, para ver o desenho no lugar
  if (!el) return console.log(`  (sem ${nome})`);
  await el.scrollIntoViewIfNeeded(); await espera(250);
  const c = await el.boundingBox();
  await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: { x: Math.floor(c.x - 2), y: Math.floor(c.y - 2), width: Math.ceil(c.width + 4), height: Math.ceil(c.height + 4) } });
};
const ate = async (p, sel) => {  // passa as orientações e os "continuar" até `sel` aparecer
  for (let k = 0; k < 60 && !(await p.$(sel)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(900);
};
const bolsa = (p, id) => p.evaluate((k) => (App.estado.heroi.bolsa.find((x) => x.id === k) || {}).qtd || 0, id);
if (SO.has("machado")) {
  const VITRINE = { TUTORIAL: "0", VITRINE: "1", ARMA: "machado", VISTAS: "A1,V2,N1,D1,K1,M1,L1" };
  for (const jan of Object.keys(JANELAS)) for (const mov of ["normal", "reduzido"]) {
    const opc = mov === "reduzido" ? { reducedMotion: "reduce" } : {}, n = (c) => `machado-${jan}-${mov}-${c}`;
    // o Inventário, as dicas, a lixeira, o voo de uma bomba ganha até a bolsa
    let { proc, url } = await subir("tutorial", VITRINE);
    let p = await pagina(url, jan, n("vitrine"), opc);
    await ate(p, "#predios .predio");
    if (mov === "normal") { await p.screenshot({ path: path.join(SAIDA, `${n("tela-vila")}.png`) }); await recortar(p, "#heroi", n("ficha"), 0); }
    relatorio.push({ nome: n("ficha"), ...(await onde(p)) });
    await pegarVoo(p, ".item-voando", mov === "reduzido" ? 60 : 380);
    await p.evaluate(() => itemVoa(document.querySelector("#texto") || document.querySelector("#pagina"), "bomba_fumaca"));
    await voo(p, ".item-voando", n("voo-bomba"));
    await espera(1200);
    await p.keyboard.press("i"); await espera(1300); await p.mouse.move(2, 2); await espera(300);
    if (mov === "normal") {
      await p.screenshot({ path: path.join(SAIDA, `${n("tela-inventario")}.png`) });
      await recortar(p, ".tela.inventario", n("inventario"), 4);
      relatorio.push({ nome: n("inventario"), medidas: await medidas(p), ...(await onde(p)) });
      const im = await p.evaluate(() => App.estado.heroi.mochila.findIndex((x) => x.icone === "machado"));
      await zoom(p, await p.$('.tela.inventario [data-espaco="arma"]'), n("corpo"));
      await zoom(p, await p.$(`.tela.inventario [data-mochila="${im}"]`), n("mochila"));
      await zoom(p, await p.$('.tela.inventario [data-usar="bomba_fumaca"]'), n("bolsa"));
      await zoom(p, await p.$(".tela.inventario .lixeira"), n("lixeira"));
      await p.keyboard.down("Shift");
      await dica(p, await p.$(`.tela.inventario [data-mochila="${im}"]`), n("dica-machado-comparacao"));
      await p.keyboard.up("Shift");
      await dica(p, await p.$('.tela.inventario [data-usar="bomba_fumaca"]'), n("dica-bomba"));
    }
    await p.close(); proc.kill();
    // a luta: a janelinha de Itens, com a bomba (e a troca de arma, com o machado da mochila)
    if (mov === "normal") {
      ({ proc, url } = await subir("tutorial", { ...VITRINE, LUTA: "lobo", QUANTOS: "1" }));
      p = await pagina(url, jan, n("luta"), opc);
      await ate(p, '#roda .roda-botao[data-slot="itens"]');
      await (await p.$('#roda .roda-botao[data-slot="itens"]')).click(); await espera(900); await p.mouse.move(2, 2); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${n("tela-luta-itens")}.png`) });
      await recortar(p, ".roda-janela", n("luta-itens"), 6);
      relatorio.push({ nome: n("luta-itens"), ...(await onde(p)) });
      await p.close(); proc.kill();
    }
    // o mercado: comprar uma bomba; comprar, vender e recomprar o machado
    if (mov === "normal") {
      ({ proc, url } = await subir("mercado", { CLASSE: "guerreiro", AMOSTRAS: "3", SEMENTE: "1", ARMA: "machado" }));
      p = await pagina(url, jan, n("mercado"), opc);
      await parado(p); await espera(900); await p.mouse.move(2, 2); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${n("tela-mercado")}.png`) });
      await recortar(p, "#lista-suprimentos", n("mercado-suprimentos"), 4);
      const antes = await bolsa(p, "bomba_fumaca");
      await (await p.$('#lista-suprimentos [data-comprar="bomba_fumaca"] .total, #lista-suprimentos [data-comprar="bomba_fumaca"]')).click();
      await espera(1500); await parado(p);
      relatorio.push({ nome: n("compra-bomba"), bolsa: `${antes} → ${await bolsa(p, "bomba_fumaca")}` });
      await recortar(p, "#heroi", n("mercado-ficha-depois"), 0);
      // comprar o machado da banca (o equipamento à venda)
      await (await p.$('[data-aba="equipamentos"]')).click(); await espera(700); await p.mouse.move(2, 2); await espera(300);
      await recortar(p, "#lista-equipamentos", n("mercado-equipamentos"), 4);
      const loja = await p.$$("[data-comprar-item]").then(async (es) => { for (const e of es) if (/machado-/.test(await e.innerHTML())) return e; return null; });
      await zoom(p, loja, n("banca-machado"));
      const naMochila = () => p.evaluate(() => App.estado.heroi.mochila.filter((x) => x.icone === "machado").length);
      const m0 = await naMochila();
      if (loja) { await loja.click(); await espera(1500); await parado(p); }
      relatorio.push({ nome: n("compra-machado"), mochila: `${m0} → ${await naMochila()} machado(s)` });
      await (await p.$('[data-aba="vender"]')).click(); await espera(800);
      const mochilaAntes = await p.evaluate(() => App.estado.heroi.mochila.length);
      const iv = await p.evaluate(() => App.estado.heroi.mochila.findIndex((x) => x.icone === "machado"));
      await dica(p, await p.$(`[data-mochila-loja="${iv}"]`), n("mercado-dica-machado"));
      await zoom(p, await p.$(`[data-mochila-loja="${iv}"]`), n("vender-machado"));
      await p.mouse.move(2, 2); await espera(200);
      await (await p.$(`[data-mochila-loja="${iv}"]`)).click(); await espera(1500); await parado(p);
      await p.mouse.move(2, 2); await espera(400);
      await recortar(p, ".tela.loja", n("mercado-vendido"), 4);
      await zoom(p, await p.$("[data-recomprar]"), n("recomprar-machado"));
      relatorio.push({ nome: n("venda"), mochila: `${mochilaAntes} → ${await p.evaluate(() => App.estado.heroi.mochila.length)}`, ...(await onde(p)) });
      await (await p.$("[data-recomprar]")).click(); await espera(1500); await parado(p);
      relatorio.push({ nome: n("recompra"), mochila: await p.evaluate(() => App.estado.heroi.mochila.filter((x) => x.icone === "machado").length) + " machado(s) na mochila" });
      await p.close(); proc.kill();
    }
    // o saque: o cartão (64 e 48) e o voo ao equipar
    ({ proc, url } = await subir("vila", { ACHADO: "machado", ARMA: "machado" }));
    p = await pagina(url, jan, n("saque"), opc);
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
    if (mov === "normal") await p.screenshot({ path: path.join(SAIDA, `${n("tela-saque")}.png`) });
    await recortar(p, ".janela-achado", n("saque-cartao"), 6);
    relatorio.push({ nome: n("saque-cartao"), ...(await onde(p)) });
    await pegarVoo(p, ".voo-item", mov === "reduzido" ? 40 : 160);
    const eq = await p.$('#prompt .escolha:has-text("Equipar"), .achado-acoes button:has-text("Equipar")');
    if (eq) await eq.click(); else await p.keyboard.press("1");
    await voo(p, ".voo-item", n("saque-voo"));
    await espera(1500);
    await recortar(p, "#heroi", n("saque-ficha-depois"), 0);
    relatorio.push({ nome: n("saque-equipou"), arma: await p.evaluate(() => App.estado.heroi.equip.arma.nome) });
    await p.close(); proc.kill();
    // o baú: o quadro com a bomba
    ({ proc, url } = await subir("baus", { BAUS: "1", SUPRIMENTO: "bomba_fumaca" }));
    p = await pagina(url, jan, n("bau"), opc);
    await parado(p); await espera(800);
    const b0 = await bolsa(p, "bomba_fumaca");
    await (await p.$('#heroi [data-bolsa="bau"]')).click();
    await p.waitForSelector(".achado-espolio", { timeout: 15000 }).catch(() => console.log(`  ${n("bau")}: sem o quadro do baú`));
    await espera(700);
    if (mov === "normal") await p.screenshot({ path: path.join(SAIDA, `${n("tela-bau")}.png`) });
    await recortar(p, ".achado-espolio", n("bau-espolio"), 40);
    relatorio.push({ nome: n("bau"), ...(await onde(p)) });
    await espera(2500);
    relatorio.push({ nome: n("bau-bolsa"), bolsa: `${b0} → ${await bolsa(p, "bomba_fumaca")}` });
    await p.close(); proc.kill();
  }
  // o Bestiário e a derrota (a caveira), o Redemoinho e a Fúria (o machado): continuam com o sprite do jogo
  const { proc, url } = await subir("tutorial", VITRINE);
  const p = await pagina(url, "normal", "machado-papeis");
  await ate(p, "#predios .predio");
  relatorio.push({ nome: "machado-papeis", caveira: await p.evaluate(() => Icones.porDesenho("caveira") === "" ? "sprite do jogo" : "TROCADA"),
    bomba_pelo_desenho: await p.evaluate(() => Icones.porDesenho("caveira") === "" && Icones.consumivel("bomba_fumaca") !== "" ? "só pelo id" : "ERRO"),
    machado_item: await p.evaluate(() => Icones.item("machado") !== "" ? "arquivo" : "ERRO") });
  await p.close(); proc.kill();
}
// 8. o arco (1.101.0), o cajado (1.106.0), o orbe (1.107.0), o grimório (1.108.0) e a varinha (1.109.0), SO=arco, SO=cajado,
//    SO=orbe, SO=livro ou SO=varinha: a classe com a arma vestida e outra na mochila
//    (cenário mercado, AMOSTRA e ARMA): a ficha, a venda, a dica com a comparação, vender e recomprar, o Inventário em
//    40; o cartão do saque, o voo ao equipar e o guardar na mochila (vila, ACHADO); a roda da luta, com o Atacar no sprite do jogo (e o Tiro Duplo do
//    Arqueiro na janelinha de Habilidades)
for (const [peca, classe] of [["arco", "arqueiro"], ["cajado", "mago"], ["orbe", "mago"], ["livro", "mago"], ["varinha", "mago"]]) {
  if (!SO.has(peca)) continue;
  for (const jan of Object.keys(JANELAS)) {
    const n = (c) => `${peca}-${jan}-${c}`;
    let { proc, url } = await subir("mercado", { CLASSE: classe, AMOSTRA: peca, ARMA: peca, SEMENTE: "1" });
    let p = await pagina(url, jan, n("mercado"));
    await parado(p); await espera(900); await p.mouse.move(2, 2); await espera(300);
    await recortar(p, "#heroi", n("ficha"), 0);
    await (await p.$('[data-aba="vender"]')).click(); await espera(800); await p.mouse.move(2, 2); await espera(300);
    await recortar(p, "#lista-vender", n("vender"), 4);
    await p.keyboard.down("Shift");
    await dica(p, await p.$('[data-mochila-loja="0"]'), n("dica-comparacao"));
    await p.keyboard.up("Shift");
    relatorio.push({ nome: n("mercado"), ...(await onde(p)) });
    // vender a da mochila e recomprar (o vendido aparece em "Recomprar" com o mesmo desenho; recomprado, volta à mochila)
    const vende = await p.$('[data-mochila-loja="0"]');
    if (vende) {
      await vende.click(); await espera(1500); await p.mouse.move(2, 2); await espera(300);
      await recortar(p, ["#lista-vender"], n("vendido"), 4);
      relatorio.push({ nome: n("vendido"), ...(await onde(p)) });
      const volta = await p.$("[data-recomprar]");
      if (volta) {
        await volta.click(); await espera(1500); await p.mouse.move(2, 2); await espera(300);
        await recortar(p, ["#lista-vender"], n("recomprado"), 4);
        relatorio.push({ nome: n("recomprado"), ...(await onde(p)) });
      } else console.log(`  ${n("vendido")}: sem o Recomprar`);
    }
    await p.mouse.move(2, 2); await p.keyboard.press("Escape"); await espera(1500); await parado(p);
    await p.keyboard.press("i"); await espera(1300); await p.mouse.move(2, 2); await espera(300);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela-inventario")}.png`) });
    await recortar(p, ".tela.inventario", n("inventario"), 4);
    relatorio.push({ nome: n("inventario"), medidas: await medidas(p) });
    await p.close(); proc.kill();
    ({ proc, url } = await subir("vila", { CLASSE: classe, ACHADO: peca, ARMA: peca }));
    p = await pagina(url, jan, n("saque"));
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
    await recortar(p, ".janela-achado", n("saque-cartao"), 6);
    relatorio.push({ nome: n("saque-cartao"), ...(await onde(p)) });
    await pegarVoo(p, ".voo-item");
    const eq = await p.$('#prompt .escolha:has-text("Equipar"), .achado-acoes button:has-text("Equipar")');
    if (eq) await eq.click(); else await p.keyboard.press("1");
    await voo(p, ".voo-item", n("saque-voo"));
    await p.close(); proc.kill();
    // guardar o achado: ele vai para a mochila do Inventário, em 40, ao lado da que já estava lá
    ({ proc, url } = await subir("vila", { CLASSE: classe, ACHADO: peca, ARMA: peca }));
    p = await pagina(url, jan, n("guardar"));
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
    const gu = await p.$('#prompt .escolha:has-text("Guardar"), .achado-acoes button:has-text("Guardar")');
    if (gu) await gu.click(); else await p.keyboard.press("2");
    await espera(2500); await parado(p).catch(() => {});
    for (let k = 0; k < 10; k++) {  // o cenário segue a história ("Continuar") antes de deixar abrir o Inventário
      const c = await p.$("#prompt .continuar");
      if (!c) break;
      await c.click().catch(() => {}); await espera(900);
    }
    await parado(p).catch(() => {});
    if (await p.$(".contrato-arte")) { await p.keyboard.press("Escape"); await espera(1500); await parado(p).catch(() => {}); }  // e abre o mural
    await p.keyboard.press("i"); await espera(1300); await p.mouse.move(2, 2); await espera(300);
    await recortar(p, ".tela.inventario", n("guardado-inventario"), 4);
    relatorio.push({ nome: n("guardado-inventario"), ...(await onde(p)) });
    await p.close(); proc.kill();
    ({ proc, url } = await subir("tutorial", { TUTORIAL: "0", CLASSE: classe, ARMA: peca, LUTA: "lobo", QUANTOS: "2", VISTAS: "A1,V2,N1,D1,K1,M1,L1" }));
    p = await pagina(url, jan, n("luta"));
    for (let k = 0; k < 60 && !(await p.$("#roda .roda-botao")); k++) {
      for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
      await espera(300);
    }
    await espera(900);
    const hab = await p.$('#roda .roda-botao[data-slot="habilidades"]');
    if (hab) { await hab.click(); await espera(600); }
    await p.mouse.move(2, 2); await espera(300);
    await recortar(p, ["#roda > *", ".roda-janela", "#heroi"], n("luta"), 6);
    relatorio.push({ nome: n("luta"), ...(await onde(p)) });
    await p.close(); proc.kill();
  }
}
await b.close();
for (const r of relatorio) console.log(r.nome, "·", Object.entries(r).filter(([k]) => k !== "nome").map(([k, v]) => `${k} ${JSON.stringify(v)}`).join(" · "));
writeFileSync(path.join(SAIDA, "onde.json"), JSON.stringify(relatorio, null, 1));
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
