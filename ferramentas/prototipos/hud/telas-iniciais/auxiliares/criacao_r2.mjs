// Confere e fotografa a criação em etapas (a candidata R2) no jogo de verdade (cenarios_telas.py com PROPOSTA=r2; os
// saves numa pasta temporária), a 1920×945 e a 1280×720. Fotos em ../capturas/<janela>-r2-<tela>.png. Confere:
// escolher sem avançar (clique, teclas, setas), a escolha que fica depois que o mouse sai, o Avançar só com escolha,
// o Enter segurado e o clique duplo que não atravessam etapas, o Voltar que preserva nome, classe, modo e tutorial, o
// Esc que volta ao título, a ordem do Tab e o foco visível, nomes longos com acento, as três classes, os dois modos, o
// tutorial ligado e desligado, e o começo da campanha (o motor diz o que recebeu: a linha [criacao] do cenário).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/telas-iniciais/auxiliares/criacao_r2.mjs
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
  const proc = spawn(PY, [path.join(aqui, "cenarios_telas.py")], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", PROPOSTA: "r2" } });
  const s = { proc, url: null, recebido: [] };
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) s.url = m[0]; });
  proc.stderr.on("data", (d) => { for (const l of String(d).split("\n")) if (l.startsWith("[criacao]")) s.recebido.push(l.trim()); });
  for (let k = 0; k < 300 && !s.url; k++) await espera(100);
  if (!s.url) throw new Error("o cenário não subiu");
  return s;
}
const etapa = (p) => p.evaluate(() => { const a = document.querySelector(".cr-etapas [aria-current]"); return a ? a.textContent.replace(/\d/, "").trim() : null; });
const marcado = (p) => p.evaluate(() => document.querySelector('.cr-etapa.atual .cr-cartao[aria-checked="true"]')?.dataset.valor || null);
const ativo = (p) => p.evaluate(() => { const e = document.activeElement; return e ? (e.id || e.dataset.valor || e.className.split(" ")[0]) : null; });
const focoVisivel = (p) => p.evaluate(() => { const c = getComputedStyle(document.activeElement); return c.outlineStyle !== "none" && parseFloat(c.outlineWidth) >= 2; });
const resumo = (p) => p.evaluate(() => document.querySelector(".cr-resumo")?.innerText.replace(/\s+/g, " ").trim());
const pausa = () => espera(460);  // a guarda do botão de uma etapa nova (400 ms)

async function abrirCriacao(p, url) {
  await p.goto(url);
  await p.waitForSelector('#prompt .escolha:has-text("Novo jogo")', { timeout: 30000 });
  await p.click('#prompt .escolha:has-text("Novo jogo")');
  await p.waitForSelector("#cr-campo", { timeout: 20000 });
  await pausa();
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
  let p = await b.newPage({ viewport: { width: W, height: H } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
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
  // escolher não avança: o clique, as teclas, as setas
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
  // a ordem do Tab segue a tela: o grupo de cartões, o Voltar, o Avançar
  await p.keyboard.press("Tab"); const t1 = await ativo(p);
  await p.keyboard.press("Tab"); const t2 = await ativo(p);
  conferir(t1 === "cr-voltar" && t2 === "cr-avancar", `Tab: cartões → Voltar → Avançar (${t1}, ${t2})`);
  conferir(await focoVisivel(p), "o Avançar com o foco tem o anel de 2 px");
  // as três classes, uma por vez (as fotos de cada)
  for (const c of ["guerreiro", "mago", "arqueiro"]) { await p.click(`.cr-classe[data-valor="${c}"]`); await espera(100); conferir(await marcado(p) === c, `escolhe ${c}`); }
  // o clique duplo no Avançar: chega ao Modo e para (não começa a campanha)
  await p.dblclick(".cr-avancar"); await espera(900);
  conferir(await etapa(p) === "Modo" && s.recebido.length === 0, "clique duplo no Avançar: só até o Modo, a campanha não começa");
  conferir(await marcado(p) === "resgate", "o Modo chega com o Resgate (o padrão de hoje)");
  conferir(await resumo(p) === "Ana · Arqueiro · Resgate", `o resumo: ${await resumo(p)}`);
  await foto(p, "3-modo");
  alturas.push((await cabe(p, "modo")).alt);
  conferir(new Set(alturas).size === 1, `a mesma altura nas três etapas (${alturas.join(", ")})`);
  // trocar o modo e o tutorial, voltar e conferir que nada se perdeu
  await p.keyboard.press("2"); await espera(120);
  await p.click("#cr-tutorial"); await espera(120);
  conferir(await marcado(p) === "hardcore" && !(await p.$eval("#cr-tutorial", (e) => e.checked)), "Hardcore e o tutorial desligado");
  await foto(p, "3-modo-hardcore-sem-tutorial");
  await p.keyboard.press("Escape"); await espera(200);
  conferir(await etapa(p) === "Classe" && await marcado(p) === "arqueiro", "Esc no Modo: volta à Classe com o Arqueiro");
  await p.click(".cr-voltar"); await espera(200);
  conferir(await etapa(p) === "Nome" && await p.$eval("#cr-campo", (e) => e.value) === "Ana", "Voltar na Classe: o nome continua Ana");
  await pausa(); await p.click(".cr-avancar"); await pausa(); await p.click(".cr-avancar"); await espera(200);
  conferir(await marcado(p) === "hardcore" && !(await p.$eval("#cr-tutorial", (e) => e.checked)), "avançando de novo, o Modo continua Hardcore e sem tutorial");
  // a barra de etapas: a feita volta com o clique
  await p.click('.cr-etapas button[data-etapa="1"]'); await espera(200);
  conferir(await etapa(p) === "Classe", "o clique em Classe, na barra de etapas, volta a ela");
  await pausa(); await p.click(".cr-avancar"); await espera(200);
  await p.keyboard.press("1"); await p.click("#cr-tutorial"); await espera(120);  // de volta ao Resgate com tutorial
  // Começar campanha: Enter apertado de propósito (solto antes) começa uma vez
  await espera(800);
  await p.keyboard.press("Enter"); await p.keyboard.press("Enter");
  await p.waitForSelector("#heroi .heroi-nome", { state: "attached", timeout: 30000 }); await espera(1500);
  conferir(s.recebido.length === 1 && s.recebido[0] === "[criacao] nome='Ana' classe=arqueiro modo=resgate tutorial=True", `o motor recebeu: ${s.recebido.join(" / ")}`);
  conferir(!(await p.$(".cr")) && !(await p.evaluate(() => document.body.classList.contains("criando"))), "a criação some quando a campanha começa");
  conferir((await p.$eval("#heroi .heroi-nome", (e) => e.innerText)) === "Ana", "a ficha mostra Ana");
  await foto(p, "4-campanha");
  conferir(erros.length === 0, `sem erros na página ${erros.join(" ")}`);
  await p.close(); s.proc.kill();

  // ---------------------------------------------------------------- 2. nome longo com acento, Mago, Hardcore, sem tutorial
  s = await subir();
  p = await b.newPage({ viewport: { width: W, height: H } });
  await abrirCriacao(p, s.url);
  await p.fill("#cr-campo", LONGO);
  conferir((await p.$eval("#cr-campo", (e) => e.value)).length === 40, "o campo guarda 40 letras do nome longo");
  await foto(p, "5-nome-longo");
  await p.click(".cr-avancar"); await pausa();
  await p.click('.cr-classe[data-valor="mago"]'); await p.click(".cr-avancar"); await pausa();
  await p.click('.cr-modo[data-valor="hardcore"]'); await p.click("#cr-tutorial");
  await foto(p, "5-modo-nome-longo");
  await cabe(p, "modo com nome longo");
  const larguraResumo = await p.evaluate(() => { const r = document.querySelector(".cr-resumo").getBoundingClientRect(), a = document.querySelector(".cr-comecar").getBoundingClientRect(); return r.right <= a.left; });
  conferir(larguraResumo, "o resumo com o nome longo não invade o Começar campanha (reticências)");
  await espera(400); await p.click(".cr-comecar");
  await p.waitForSelector("#heroi .heroi-nome", { state: "attached", timeout: 30000 }); await espera(1500);
  conferir(s.recebido[0] === `[criacao] nome='${LONGO.slice(0, 40)}' classe=mago modo=hardcore tutorial=False`, `o motor recebeu: ${s.recebido.join(" / ")}`);
  conferir(!(await p.$(".orientacao:not([hidden])")), "sem tutorial, nenhum quadro de orientação");
  await foto(p, "5-campanha-nome-longo");
  await p.close(); s.proc.kill();

  // ---------------------------------------------------------------- 3. Guerreiro com o nome em branco; Esc no nome volta ao título
  s = await subir();
  p = await b.newPage({ viewport: { width: W, height: H } });
  await abrirCriacao(p, s.url);
  await p.keyboard.press("Escape");
  await p.waitForSelector('#prompt .escolhas:not(.escolhido) .escolha:has-text("Novo jogo")', { timeout: 20000 });
  conferir(!(await p.$(".cr")) && s.recebido.length === 0, "Esc no nome volta ao título, sem começar nada");
  await p.click('#prompt .escolha:has-text("Novo jogo")'); await p.waitForSelector("#cr-campo"); await pausa();
  await p.keyboard.press("Enter"); await pausa();
  conferir(await resumo(p) === "Aventureiro", "o nome em branco vira Aventureiro no resumo");
  await p.keyboard.press("1"); await espera(100); await p.keyboard.press("Enter"); await espera(800);
  await p.keyboard.press("Enter");
  await p.waitForSelector("#heroi .heroi-nome", { state: "attached", timeout: 30000 }); await espera(2500);
  conferir(s.recebido[0] === "[criacao] nome='Aventureiro' classe=guerreiro modo=resgate tutorial=True", `o motor recebeu: ${s.recebido.join(" / ")}`);
  await foto(p, "6-campanha-guerreiro");
  await p.close(); s.proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
