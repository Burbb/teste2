// Confere e fotografa a criação em etapas no jogo de verdade (a R2, integrada na 1.208.0: cenarios_telas.py, o jogo
// como está, com os saves numa pasta temporária), a 1920×945 e a 1280×720. Fotos em ../capturas/<janela>-r2-<tela>.png.
// Confere: escolher sem avançar (clique, teclas, setas), a escolha que fica depois que o mouse sai, o Avançar só com
// escolha, o Enter segurado e o clique duplo que não atravessam etapas, o Enter novo que responde na hora, o Voltar que
// preserva nome, classe, modo e tutorial, o Esc que volta ao título, a ordem do Tab e o foco visível, nomes longos com
// acento, as três classes, os dois modos, o tutorial ligado e desligado, a resposta que vai ao motor uma vez só (o que a
// página manda ao /responder), a campanha que começa com o que se escolheu, e salvar e carregar a campanha criada.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/telas-iniciais/auxiliares/criacao.mjs
// (JANELAS=1920,1280)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const LONGO = "Maria da Conceição Albuquerque de Figueiredo Brás";  // 49 letras: o campo guarda 40
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

async function subir() {
  const proc = spawn(PY, [path.join(aqui, "cenarios_telas.py")], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", PROPOSTA: "" } });
  const s = { proc, url: null };
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) s.url = m[0]; });
  for (let k = 0; k < 300 && !s.url; k++) await espera(100);
  if (!s.url) throw new Error("o cenário não subiu");
  return s;
}
/** Uma página que anota as respostas da criação mandadas ao motor (as que levam a classe ou o voltar dela). */
async function pagina(b, W, H) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.enviadas = []; p.erros = [];
  p.on("pageerror", (e) => p.erros.push(String(e)));
  p.on("request", (r) => {
    if (!r.url().includes("/responder")) return;
    const v = JSON.parse(r.postData() || "{}").valor;
    if (v && typeof v === "object" && ("classe" in v || "voltar" in v)) p.enviadas.push(v);
  });
  return p;
}
const etapa = (p) => p.evaluate(() => { const a = document.querySelector(".cr-etapas [aria-current]"); return a ? a.textContent.replace(/\d/, "").trim() : null; });
const marcado = (p) => p.evaluate(() => document.querySelector('.cr-etapa.atual .cr-cartao[aria-checked="true"]')?.dataset.valor || null);
const ativo = (p) => p.evaluate(() => { const e = document.activeElement; return e ? (e.id || e.dataset.valor || e.className.split(" ")[0]) : null; });
const focoVisivel = (p) => p.evaluate(() => { const c = getComputedStyle(document.activeElement); return c.outlineStyle !== "none" && parseFloat(c.outlineWidth) >= 2; });
const resumo = (p) => p.evaluate(() => document.querySelector(".cr-resumo")?.innerText.replace(/\s+/g, " ").trim());
const igual = (a, b) => JSON.stringify(a) === JSON.stringify(b);

async function abrirCriacao(p, url) {
  await p.goto(url);
  await p.waitForSelector('#prompt .escolha:has-text("Novo jogo")', { timeout: 30000 });
  await p.click('#prompt .escolha:has-text("Novo jogo")');
  await p.waitForSelector("#cr-campo", { timeout: 20000 });
}
/** Depois do "Começar campanha": a abertura até o Vau (o Continuar da missão, "Agora não" na despensa). */
async function ateOVau(p) {
  for (let t = 0; t < 120; t++) {
    if (await p.$('#cena-cab .cena-titulo:has-text("Vau do Turvo")') && await p.$('#doca .atalho[data-rotulo="Sair"]')) return true;
    const ok = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (ok) await ok.click().catch(() => {});
    const nao = await p.$('#prompt .escolhas:not(.escolhido) .escolha:has-text("Agora não")'); if (nao) await nao.click().catch(() => {});
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
    await espera(250);
  }
  return false;
}
/** Salvar e sair pela doca, voltar ao título e carregar o save do herói pelo cartão da lista. */
async function salvarECarregar(p, nome, classe, modo, jan) {
  await p.click('#doca .atalho[data-rotulo="Sair"]');
  await (await p.waitForSelector('#prompt .escolha:has-text("Salvar e sair")', { timeout: 15000 })).click();
  const carregar = '#prompt .escolhas:not(.escolhido) .escolha:has-text("Carregar")';
  for (let t = 0; t < 80 && !(await p.$(carregar)); t++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(250); }
  if (!(await p.$(carregar))) await p.screenshot({ path: path.join(SAIDA, `${jan}-r2-erro-sair.png`) });
  await p.waitForSelector(carregar, { timeout: 5000 });
  await p.click('#prompt .escolha:has-text("Carregar")');
  const cartao = await p.waitForSelector(`.save-cartao:has-text("${nome.slice(0, 12)}")`, { timeout: 15000 });
  const texto = (await cartao.textContent()).replace(/\s+/g, " ");
  conferir(new RegExp(`Vale do Turvo · ${modo}`).test(texto), `o cartão do save diz a região e o modo (${modo})`);
  await p.screenshot({ path: path.join(SAIDA, `${jan}-r2-7-saves-${modo}.png`) });
  await cartao.click();
  await p.waitForFunction((n) => document.querySelector("#heroi .heroi-nome")?.innerText === n, nome, { timeout: 20000 });
  const titulo = await p.$eval("#heroi .heroi-titulo", (e) => e.innerText);
  conferir(titulo.startsWith(classe), `o save carregado é o mesmo herói (${nome}, ${titulo.replace(/\s+/g, " ")})`);
}

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  console.log(`== ${jan}`);
  const foto = async (p, nome, mouseFora = true) => { if (mouseFora) await p.mouse.move(2, 2); await espera(300); await p.screenshot({ path: path.join(SAIDA, `${jan}-r2-${nome}.png`) }); };
  const cabe = async (p, nome) => {
    const m = await p.evaluate(() => { const r = document.querySelector(".cr").getBoundingClientRect(), pg = document.querySelector("#pagina");
      const cortado = [...document.querySelectorAll(".cr *")].some((e) => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== "visible" && !e.matches(".cr-resumo, .cr-resumo span"));
      return { dentro: r.left >= 0 && r.top >= 0 && r.right <= innerWidth && r.bottom <= innerHeight, rola: pg.scrollHeight > pg.clientHeight + 1, cortado, alt: Math.round(r.height), larg: Math.round(r.width) }; });
    conferir(m.dentro && !m.rola && !m.cortado, `${nome}: o painel (${m.larg}×${m.alt}) cabe na janela, sem rolar nem cortar`);
    return m;
  };

  // ---------------------------------------------------------------- 1. o caminho principal (Ana, Arqueiro, Resgate, tutorial)
  let s = await subir();
  let p = await pagina(b, W, H);
  await abrirCriacao(p, s.url);
  const alturas = [];
  await foto(p, "1-nome");
  alturas.push((await cabe(p, "nome")).alt);
  conferir(await ativo(p) === "cr-campo", "o campo do nome chega com o foco");
  await p.keyboard.type("Ana");
  // o Enter segurado: um aperto avança uma etapa só (as repetições e o Enter que não foi solto não contam)
  await p.keyboard.down("Enter"); await espera(60);
  for (let k = 0; k < 6; k++) { await p.keyboard.down("Enter"); await espera(120); }
  await espera(500);
  for (let k = 0; k < 3; k++) { await p.keyboard.down("Enter"); await espera(150); }
  await p.keyboard.up("Enter");
  conferir(await etapa(p) === "Classe", "Enter segurado no nome: avança só até a Classe");
  conferir(await marcado(p) === null && await p.$eval(".cr-avancar", (e) => e.disabled), "a Classe chega sem escolha e com o Avançar desligado");
  await foto(p, "2-classe-sem-escolha");
  alturas.push((await cabe(p, "classe")).alt);
  conferir(await resumo(p) === "Ana", "o resumo mostra o nome: Ana");
  await p.evaluate(() => document.activeElement.blur());  // a foto da passagem do mouse, sem o foco do teclado junto
  await p.hover('.cr-classe[data-valor="guerreiro"]');
  await foto(p, "2-classe-mouse", false);
  await p.click('.cr-classe[data-valor="arqueiro"]');
  await p.mouse.move(2, 2); await espera(200);
  conferir(await etapa(p) === "Classe" && await marcado(p) === "arqueiro", "o clique no Arqueiro escolhe e fica na Classe");
  conferir(await p.$eval('.cr-classe[data-valor="arqueiro"]', (e) => getComputedStyle(e).borderTopColor) !== await p.$eval('.cr-classe[data-valor="mago"]', (e) => getComputedStyle(e).borderTopColor),
    "a escolha continua à vista depois que o mouse sai (a aresta de latão)");
  await foto(p, "2-classe-arqueiro");
  await p.keyboard.press("3"); await espera(150);
  conferir(await etapa(p) === "Classe" && await marcado(p) === "mago" && await ativo(p) === "mago", "a tecla 3 escolhe o Mago (e leva o foco), sem avançar");
  await p.keyboard.press("ArrowLeft"); await espera(150);
  conferir(await marcado(p) === "arqueiro", "a seta para a esquerda volta ao Arqueiro");
  conferir(await focoVisivel(p), "o cartão com o foco do teclado tem o anel de 2 px");
  await foto(p, "2-classe-foco-teclado");
  await p.keyboard.press("Tab"); const t1 = await ativo(p);
  await p.keyboard.press("Tab"); const t2 = await ativo(p);
  conferir(t1 === "cr-voltar" && t2 === "cr-avancar", `Tab: cartões → Voltar → Avançar (${t1}, ${t2})`);
  conferir(await focoVisivel(p), "o Avançar com o foco tem o anel de 2 px");
  for (const c of ["guerreiro", "mago", "arqueiro"]) { await p.click(`.cr-classe[data-valor="${c}"]`); await espera(100); conferir(await marcado(p) === c, `escolhe ${c}`); }
  // o clique duplo no Avançar: chega ao Modo e para (o segundo clique não começa a campanha)
  await p.dblclick(".cr-avancar"); await espera(900);
  conferir(await etapa(p) === "Modo" && p.enviadas.length === 0, "clique duplo no Avançar: só até o Modo, nada vai ao motor");
  conferir(await marcado(p) === "resgate", "o Modo chega com o Resgate (o padrão)");
  conferir(await resumo(p) === "Ana · Arqueiro · Resgate", `o resumo: ${await resumo(p)}`);
  await foto(p, "3-modo");
  alturas.push((await cabe(p, "modo")).alt);
  conferir(new Set(alturas).size === 1, `a mesma altura nas três etapas (${alturas.join(", ")})`);
  await p.keyboard.press("2"); await espera(120);
  await p.click("#cr-tutorial"); await espera(120);
  conferir(await marcado(p) === "hardcore" && !(await p.$eval("#cr-tutorial", (e) => e.checked)), "Hardcore e o tutorial desligado");
  await foto(p, "3-modo-hardcore-sem-tutorial");
  await p.keyboard.press("Escape"); await espera(200);
  conferir(await etapa(p) === "Classe" && await marcado(p) === "arqueiro", "Esc no Modo: volta à Classe com o Arqueiro");
  await p.click(".cr-voltar"); await espera(200);
  conferir(await etapa(p) === "Nome" && await p.$eval("#cr-campo", (e) => e.value) === "Ana", "Voltar na Classe: o nome continua Ana");
  // o Enter novo, solto e apertado de novo, responde na hora (sem espera por tempo)
  await p.keyboard.press("Enter");
  const t0 = Date.now(); await p.keyboard.press("Enter"); const ateModo = await etapa(p);
  conferir(ateModo === "Modo" && Date.now() - t0 < 300, `dois Enter seguidos (soltos): Nome → Classe → Modo na hora (${ateModo}, ${Date.now() - t0} ms)`);
  conferir(await marcado(p) === "hardcore" && !(await p.$eval("#cr-tutorial", (e) => e.checked)), "avançando de novo, o Modo continua Hardcore e sem tutorial");
  await p.click('.cr-etapas button[data-etapa="1"]'); await espera(200);
  conferir(await etapa(p) === "Classe", "o clique em Classe, na barra de etapas, volta a ela");
  await p.click(".cr-avancar"); await espera(200);
  await p.keyboard.press("1"); await p.click("#cr-tutorial"); await espera(120);  // de volta ao Resgate com tutorial
  // Começar campanha: dois Enter seguidos começam uma vez só
  await p.keyboard.press("Enter"); await p.keyboard.press("Enter");
  await p.waitForSelector("#heroi .heroi-nome", { state: "attached", timeout: 30000 }); await espera(1500);
  conferir(p.enviadas.length === 1 && igual(p.enviadas[0], { nome: "Ana", classe: "arqueiro", modo: "resgate", tutorial: true }),
    `uma resposta só ao motor: ${JSON.stringify(p.enviadas)}`);
  conferir(!(await p.$(".cr")) && !(await p.evaluate(() => document.body.classList.contains("criando"))), "a criação some quando a campanha começa");
  conferir(await p.evaluate(() => estado.heroi.nome === "Ana" && estado.heroi.recurso === "Foco" && estado.orientacao.ligado), "o jogo começou com Ana, o Arqueiro e o tutorial ligado");
  await foto(p, "4-campanha");
  conferir(await ateOVau(p), "a abertura chega ao Vau do Turvo");
  await salvarECarregar(p, "Ana", "Arqueiro", "resgate", jan);
  conferir(p.erros.length === 0, `sem erros na página ${p.erros.join(" ")}`);
  await p.close(); s.proc.kill();

  // ---------------------------------------------------------------- 2. nome longo com acento, Mago, Hardcore, sem tutorial
  s = await subir();
  p = await pagina(b, W, H);
  await abrirCriacao(p, s.url);
  await p.fill("#cr-campo", LONGO);
  conferir((await p.$eval("#cr-campo", (e) => e.value)).length === 40, "o campo guarda 40 letras do nome longo");
  await foto(p, "5-nome-longo");
  await p.click(".cr-avancar");
  await p.click('.cr-classe[data-valor="mago"]'); await p.click(".cr-avancar");
  await p.click('.cr-modo[data-valor="hardcore"]'); await p.click("#cr-tutorial");
  await foto(p, "5-modo-nome-longo");
  await cabe(p, "modo com nome longo");
  conferir(await p.evaluate(() => document.querySelector(".cr-resumo").getBoundingClientRect().right <= document.querySelector(".cr-comecar").getBoundingClientRect().left),
    "o resumo com o nome longo não invade o Começar campanha");
  await p.dblclick(".cr-comecar");
  await p.waitForSelector("#heroi .heroi-nome", { state: "attached", timeout: 30000 }); await espera(1500);
  conferir(p.enviadas.length === 1 && igual(p.enviadas[0], { nome: LONGO.slice(0, 40), classe: "mago", modo: "hardcore", tutorial: false }),
    `clique duplo no Começar: uma resposta só: ${JSON.stringify(p.enviadas)}`);
  conferir(await p.evaluate((n) => estado.heroi.nome === n && estado.heroi.recurso === "Mana" && !estado.orientacao.ligado, LONGO.slice(0, 40)),
    "o jogo começou com o nome longo, o Mago e o tutorial desligado");
  conferir(!(await p.$(".orientacao:not([hidden])")), "sem tutorial, nenhum quadro de orientação");
  await foto(p, "5-campanha-nome-longo");
  conferir(await ateOVau(p), "a abertura chega ao Vau do Turvo");
  await salvarECarregar(p, LONGO.slice(0, 40), "Mago", "hardcore", jan);
  await p.close(); s.proc.kill();

  // ---------------------------------------------------------------- 3. Esc no nome volta ao título; Guerreiro com o nome em branco
  s = await subir();
  p = await pagina(b, W, H);
  await abrirCriacao(p, s.url);
  await p.keyboard.press("Escape");
  await p.waitForSelector('#prompt .escolhas:not(.escolhido) .escolha:has-text("Novo jogo")', { timeout: 20000 });
  conferir(!(await p.$(".cr")) && igual(p.enviadas, [{ voltar: true }]), "Esc no nome volta ao título, sem começar nada");
  await p.click('#prompt .escolha:has-text("Novo jogo")'); await p.waitForSelector("#cr-campo");
  await p.keyboard.press("Enter");
  conferir(await resumo(p) === "Aventureiro", "o nome em branco vira Aventureiro no resumo");
  await p.keyboard.press("1"); await p.keyboard.press("Enter"); await p.keyboard.press("Enter");
  await p.waitForSelector("#heroi .heroi-nome", { state: "attached", timeout: 30000 }); await espera(2500);
  conferir(igual(p.enviadas[1], { nome: "", classe: "guerreiro", modo: "resgate", tutorial: true }) && p.enviadas.length === 2,
    `a resposta com o nome em branco: ${JSON.stringify(p.enviadas[1])}`);
  conferir(await p.evaluate(() => estado.heroi.nome === "Aventureiro" && estado.heroi.recurso === "Vigor"), "o motor fez o Aventureiro, Guerreiro");
  await foto(p, "6-campanha-guerreiro");
  await p.close(); s.proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
