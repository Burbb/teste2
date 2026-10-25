// Confere o "Carregar jogo" integrado (a R, 1.209.0) no jogo de verdade (cenarios_saves.py, saves temporários), a
// 1920×945 e a 1280×720: sem saves, uma, várias, muitas, a mais recente que não abre e nenhuma que abre. Em cada uma:
// o Voltar usável junto com a lista, a janela sem rolar a página, o foco inicial (a mais recente que abre; sem
// nenhuma, o Voltar), o anel do foco, o Tab, as setas e Home/End, a dica do nome cortado no mouse e no foco, o Esc, o
// save que não abre (a mensagem, nada carrega), o clique duplo e o Enter carregando uma vez só. Fotos em
// ../capturas/<janela>-int-<caso>.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/carregar-jogo/auxiliares/conferir.mjs
// (CASOS=vazia,uma,varias,muitas,recente_ruim,so_ruins; JANELAS=1920,1280)
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
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };
const LONGO = "Maria da Conceição Albuquerque de Figuei";

async function subir(caso) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_saves.py")], { cwd: raiz,
    env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CASO: caso } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 400 && !url; k++) await espera(100);
  if (!url) throw new Error(`o caso ${caso} não subiu`);
  return { proc, url };
}
async function pagina(b, W, H) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.erros = []; p.cargas = [];
  p.on("pageerror", (e) => p.erros.push(String(e)));
  // a escolha do save vai ao motor como o índice da opção (App.acao); conta as que saem com a lista aberta
  p.on("request", (r) => { if (r.url().includes("/responder")) { const v = JSON.parse(r.postData() || "{}").valor; p.cargas.push(v); } });
  return p;
}
const focado = (p) => p.evaluate(() => { const e = document.activeElement;
  return { cartao: e.closest(".sv-cartao") ? e.querySelector(".sv-nome").textContent : null, voltar: e.matches(".sv-voltar"),
    naoAbre: e.matches(".sv-nao-abre"), anel: getComputedStyle(e).outlineStyle !== "none" && parseFloat(getComputedStyle(e).outlineWidth) >= 2 }; });
const dica = (p) => p.evaluate(() => { const d = document.getElementById("dica-item"); return d && !d.hidden ? d.textContent.trim() : null; });
async function abrirLista(p, url) {
  await p.goto(url);
  await p.waitForSelector('#prompt .escolha:has-text("Novo jogo")', { timeout: 30000 });
  await p.evaluate(() => { window.__t = {}; const f = window.fetch;
    window.fetch = (...a) => { if (String(a[0]).includes("/responder") && !__t.envio) __t.envio = performance.now(); return f(...a); };
    const passo = () => { const v = document.querySelector(".sv-voltar"); const n = performance.now();
      if (!__t.lista && document.querySelector(".sv")) __t.lista = n;
      if (v && !__t.voltar && pergunta && pergunta.opcoes && pergunta.opcoes.some((o) => o.meta && o.meta.voltar)) __t.voltar = n;
      if (!__t.voltar) requestAnimationFrame(passo); };
    requestAnimationFrame(passo); });
  await p.click('#prompt .escolha:has-text("Carregar")');
  await p.waitForFunction(() => __t.voltar, null, { timeout: 15000 });
  await espera(500);
  return p.evaluate(() => ({ lista: Math.round(__t.lista - __t.envio), voltar: Math.round(__t.voltar - __t.envio) }));
}
const voltouAoTitulo = (p) => p.waitForSelector('#prompt .escolhas:not(.escolhido) .escolha:has-text("Novo jogo")', { timeout: 15000 }).then(() => true, () => false);

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  for (const caso of (process.env.CASOS || "vazia,uma,varias,muitas,recente_ruim,so_ruins").split(",")) {
    console.log(`== ${jan} ${caso}`);
    let { proc, url } = await subir(caso);
    let p = await pagina(b, W, H);
    try {
      if (caso === "vazia") {
        await p.goto(url); await p.waitForSelector('#prompt .escolha:has-text("Novo jogo")', { timeout: 30000 });
        conferir(!(await p.$('#prompt .escolha:has-text("Carregar")')), "sem saves, o título não oferece \"Carregar jogo\"");
        await p.screenshot({ path: path.join(SAIDA, `${jan}-int-vazia.png`) });
        continue;
      }
      const t = await abrirLista(p, url);
      conferir(t.voltar - t.lista < 50, `o Voltar usável junto com a lista (lista ${t.lista} ms, Voltar ${t.voltar} ms)`);
      const lay = await p.evaluate(() => { const s = document.querySelector(".sv").getBoundingClientRect(), pg = document.querySelector("#pagina");
        return { dentro: s.top >= 0 && s.bottom <= innerHeight, rola: pg.scrollHeight > pg.clientHeight + 1,
          voltarNaTela: document.querySelector(".sv-voltar").getBoundingClientRect().bottom <= innerHeight }; });
      conferir(lay.dentro && !lay.rola && lay.voltarNaTela, "a janela cabe sem rolar a página, com o Voltar à vista");
      await p.mouse.move(2, 2);
      await p.screenshot({ path: path.join(SAIDA, `${jan}-int-${caso}.png`) });
      const f0 = await focado(p);
      const esperado = { uma: "Maria", varias: "Maria", muitas: "Maria", recente_ruim: "Maria" }[caso];
      if (caso === "so_ruins") conferir(f0.voltar, "nenhuma partida abre: o foco começa no Voltar");
      else conferir(f0.cartao === esperado && !f0.naoAbre, `o foco começa na mais recente que abre (${f0.cartao})`);
      // o teclado
      if (caso !== "so_ruins") {
        await p.keyboard.press("Tab"); const fT = await focado(p);
        conferir(fT.voltar && fT.anel, "Tab: do cartão ao Voltar, com o anel");
        await p.keyboard.press("Shift+Tab"); conferir((await focado(p)).cartao === esperado, "Shift+Tab volta ao mesmo cartão");
      }
      if (["varias", "muitas", "recente_ruim"].includes(caso)) {
        await p.keyboard.press("End"); const fE = await focado(p);
        conferir(!!fE.cartao && fE.anel, `End vai ao último cartão (${fE.cartao})`);
        await p.keyboard.press("Home"); const fH = await focado(p);
        conferir(!!fH.cartao, `Home vai ao primeiro (${fH.cartao})`);
        if (caso === "recente_ruim") conferir(fH.naoAbre, "o primeiro, o do mundo gerado, continua acessível pelo teclado");
        // até o nome longo, pela seta: a dica com o nome inteiro no foco
        let k = 0; while ((await focado(p)).cartao !== LONGO && k++ < 30) await p.keyboard.press("ArrowDown");
        await espera(300);
        conferir((await dica(p)) === LONGO, `o nome cortado: a dica no foco do teclado (${await dica(p)})`);
        await p.screenshot({ path: path.join(SAIDA, `${jan}-int-${caso}-dica-foco.png`) });
        const c = await p.$(`.sv-cartao:has-text("${LONGO.slice(0, 20)}")`);
        await p.keyboard.press("Home"); await espera(200);
        await c.hover(); await espera(300);
        conferir((await dica(p)) === LONGO, "o nome cortado: a dica com o mouse");
        await p.mouse.move(2, 2); await espera(300);
        const curto = await p.$('.sv-cartao:has-text("Bento")'); await curto.hover(); await espera(300);
        conferir((await dica(p)) === null, "o nome que cabe não ganha dica");
        await p.mouse.move(2, 2);
      }
      if (caso === "so_ruins") {
        await p.keyboard.press("Enter");
        conferir(await voltouAoTitulo(p) && !(await p.$("#heroi .heroi-nome")), "Enter no Voltar: volta ao título, nada carrega");
      } else {
        await p.keyboard.press("Escape");
        conferir(await voltouAoTitulo(p), "Esc volta ao título");
      }
      // o que não abre: a mensagem, nada carrega
      if (caso !== "uma") {
        await abrirLista(p, url).catch(() => null);
        p.cargas = [];
        await p.click('.sv-cartao:has-text("Jean")');
        conferir(!!(await p.waitForSelector('#texto :text("Este save não abre")', { timeout: 10000 }).catch(() => null)), "o save do mundo gerado: a mensagem curta");
        await espera(800);
        conferir(!(await p.$("#heroi .heroi-nome")), "e nada carrega");
      }
      if (caso === "so_ruins") continue;
      // o clique duplo carrega uma vez
      await p.close(); proc.kill(); ({ proc, url } = await subir(caso)); p = await pagina(b, W, H);
      await abrirLista(p, url); p.cargas = [];
      await p.dblclick('.sv-cartao:has-text("Maria")');
      await p.waitForFunction(() => document.querySelector("#heroi .heroi-nome")?.innerText === "Maria", null, { timeout: 20000 });
      await espera(800);
      conferir(p.cargas.filter((v) => typeof v === "number").length === 1, `clique duplo: carrega uma vez (${JSON.stringify(p.cargas.slice(0, 3))})`);
      // o Enter na partida com o foco carrega
      if (caso === "varias") {
        await p.close(); proc.kill(); ({ proc, url } = await subir(caso)); p = await pagina(b, W, H);
        await abrirLista(p, url); p.cargas = [];
        await p.keyboard.press("ArrowDown"); await p.keyboard.press("Enter"); await p.keyboard.press("Enter");
        await p.waitForFunction(() => !!document.querySelector("#heroi .heroi-nome")?.innerText, null, { timeout: 20000 });
        await espera(800);
        conferir(p.cargas.filter((v) => typeof v === "number").length === 1 && (await p.$eval("#heroi .heroi-nome", (e) => e.innerText)) === "Bento",
          "a seta e Enter (duas vezes): carrega a segunda partida, uma vez");
      }
    } catch (e) { conferir(false, `${jan} ${caso}: ${e.message.split("\n")[0]}`); }
    conferir(p.erros.length === 0, `sem erros na página ${p.erros.join(" ")}`);
    await p.close(); proc.kill();
  }
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
