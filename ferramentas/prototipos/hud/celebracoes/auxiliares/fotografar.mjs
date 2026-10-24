// As celebrações da etapa 2 (23/10/2026): o espólio, a subida de nível e os achados por raridade, nos cenários de teste
// (cenarios_teste.py), com instantâneos ao longo de cada festa (o ritmo), um vídeo da página e o registro do console.
// PROTOTIPO=1 serve as cópias da proposta (../prototipo/) no lugar das telas do jogo, só nesta página. MOVIMENTO=reduzido
// emula o movimento reduzido. JANELA=1280x720 troca a janela.
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta> [<situação>,...]
import { spawn } from "child_process";
import { mkdirSync, readFileSync, writeFileSync, renameSync, existsSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida, so] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const INSTANTES = (process.env.INSTANTES || "60,250,500,900,1600").split(",").map(Number);  // ms depois de a festa aparecer
// Cada situação: o cenário de teste, a classe e os passos. "festa": espera a festa (seletor), fotografa os instantes,
// e fecha (clique no Continuar, tecla, ou "duplo": um clique duplo, que deve fechar uma festa só).
// O achado: as fotos contam de quando a janela abre (o cartão novo); os botões chegam depois (o tempo vai no registro).
const ACHADO = "#sobre-achado .achado-cartao.novo:not([data-visto])", BOTOES = "#sobre-achado .achado-acoes button:not(.reserva)";
const FESTA = "#celebracao .festa";
const SITUACOES = [
  { nome: "nivel", cenario: "nivel", classe: "guerreiro", passos: [
    { festa: ".festa-espolio .continuar", foto: "espolio", fechar: "clique" },
    { festa: "#celebracao .festa-nivel, #celebracao .festa", foto: "nivel", fechar: "clique" }] },
  { nome: "dois-niveis", cenario: "dois_niveis", classe: "mago", passos: [
    { festa: ".festa-espolio .continuar", foto: "espolio", fechar: "clique" },
    { festa: "#celebracao .festa-nivel, #celebracao .festa", foto: "nivel2", fechar: "duplo" },
    { festa: "#celebracao .festa-nivel, #celebracao .festa", foto: "nivel3", fechar: "tecla" }] },
  { nome: "raridades", cenario: "raridades", classe: "arqueiro", passos: [
    { festa: ACHADO, foto: "comum", fechar: "deixar" },
    { festa: ACHADO, foto: "magico", fechar: "deixar" },
    { festa: ACHADO, foto: "raro", fechar: "deixar" },
    { festa: ACHADO, foto: "lendario", fechar: "deixar" }] },
  { nome: "nivel4", cenario: "nivel4", classe: "arqueiro", passos: [
    { festa: ".festa-espolio .continuar", foto: "espolio", fechar: "clique" },
    { festa: FESTA, foto: "nivel", fechar: "tecla" }] },
  { nome: "sigilo", cenario: "sigilo", classe: "guerreiro", passos: [{ festa: FESTA, foto: "sigilo", fechar: "clique" }] },
  { nome: "especializacao", cenario: "especializacao", classe: "mago", passos: [{ festa: FESTA, foto: "spec", fechar: "clique" }] },
  // SIMULAÇÃO: os limites da tela (textos longos, seis ganhos de dois dígitos), fora das regras
  { nome: "limites", cenario: "limites", classe: "guerreiro", passos: [
    { festa: FESTA, foto: "nivel", fechar: "clique" },
    { festa: ACHADO, foto: "lendario", fechar: "deixar" }] },
  // Os vídeos para avaliação (fora da lista padrão): duas festas reais em sequência em cada um
  { nome: "video-nivel-spec", cenario: "nivel_especializacao", classe: "mago", video: true, passos: [
    { festa: ".festa-espolio .continuar", foto: "espolio", fechar: "clique" },
    { festa: FESTA, foto: "nivel", fechar: "clique" },
    { festa: FESTA, foto: "spec", fechar: "clique" }] },
  { nome: "video-raridades-sigilo", cenario: "raridades_sigilo", classe: "arqueiro", video: true, passos: [
    { festa: ACHADO, foto: "comum", fechar: "deixar" },
    { festa: ACHADO, foto: "magico", fechar: "deixar" },
    { festa: ACHADO, foto: "raro", fechar: "deixar" },
    { festa: ACHADO, foto: "lendario", fechar: "deixar" },
    { festa: FESTA, foto: "sigilo", fechar: "clique" }] },
  // As especializações, cada uma na classe dela (fora da lista padrão: "spec-paladino", ...), e os itens do Estouro
  ...["piromante", "paladino", "berserker", "patrulheiro", "sombra", "necromante"].map((k) => ({ nome: `spec-${k}`, cenario: `spec_${k}`, classe: "mago", extra: true,
    passos: [{ festa: FESTA, foto: k, fechar: "clique" }] })),
  { nome: "itens-estouro", cenario: "itens_estouro", classe: "guerreiro", extra: true, passos: [
    { festa: ACHADO, foto: "raro1", fechar: "deixar" }, { festa: ACHADO, foto: "lendario1", fechar: "deixar" },
    { festa: ACHADO, foto: "raro2", fechar: "deixar" }, { festa: ACHADO, foto: "lendario2", fechar: "deixar" }] },
  // O clique rápido: um clique fora dos botões assim que a janela surge (antes de os botões chegarem). Não deve escolher
  // nada nem fechar a janela: no achado, adianta a cerimônia; na festa, completa a revelação. Fora da lista padrão.
  { nome: "rapido", cenario: "raridades", classe: "arqueiro", rapido: true, passos: [
    { cedo: "#sobre-achado .achado-cartao.novo", festa: "#sobre-achado .achado-acoes button:not(.reserva)", foto: "comum", fechar: "deixar" },
    { cedo: "#sobre-achado .achado-cartao.novo", festa: "#sobre-achado .achado-acoes button:not(.reserva)", foto: "magico", fechar: "deixar" },
    { cedo: "#sobre-achado .achado-cartao.novo", festa: "#sobre-achado .achado-acoes button:not(.reserva)", foto: "raro", fechar: "deixar" },
    { cedo: "#sobre-achado .achado-cartao.novo", festa: "#sobre-achado .achado-acoes button:not(.reserva)", foto: "lendario", fechar: "deixar" }] },
  { nome: "rapido-nivel", cenario: "nivel", classe: "guerreiro", rapido: true, passos: [
    { festa: ".festa-espolio .continuar", foto: "espolio", fechar: "clique" },
    { cedo: "#celebracao .festa", festa: "#celebracao .festa", foto: "nivel", fechar: "tecla" }] },
].filter((s) => (so ? so.split(",").includes(s.nome) : !s.rapido && !s.video && !s.extra));
const QUAL = process.env.PROTOTIPO || "";  // "1": a primeira proposta; o nome de uma direção: a segunda rodada
const PROTO = !QUAL ? null : ["1", "brilho"].includes(QUAL) ? path.join(AQUI, "../prototipo") : path.join(AQUI, "../prototipo-v2", QUAL);
const [vw, vh] = (process.env.JANELA || "1920x945").split("x").map(Number);
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const registro = {};
for (const sit of SITUACOES) {
  const proc = spawn(PY, [path.join(AQUI, "cenarios_teste.py"), sit.cenario], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "normal", CLASSE: sit.classe } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(String(d)));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  const ctx = await b.newContext({ viewport: { width: vw, height: vh }, recordVideo: { dir: saida, size: { width: vw, height: vh } },
    reducedMotion: process.env.MOVIMENTO === "reduzido" ? "reduce" : "no-preference" });
  const p = await ctx.newPage();
  const erros = [], avisos = [], linha = [];
  let fechando = false;
  p.on("pageerror", (e) => erros.push(String(e)));
  p.on("console", (m) => { if ((m.type() === "error" || m.type() === "warning") && !m.text().startsWith("Failed to load resource")) avisos.push(m.text()); });
  p.on("response", (r) => { if (r.status() === 404) avisos.push(`404: ${r.url().replace(/^https?:\/\/[^/]+/, "")}`); });
  p.on("requestfailed", (r) => { if (!r.url().endsWith("/responder")) erros.push(`falhou: ${r.url()} ${(r.failure() || {}).errorText}`); });
  await p.addInitScript(() => {  // na página: quando cada cartão de achado e os botões dele chegam (sem o atraso das fotos)
    window.__marcos = [];
    new MutationObserver(() => {
      const c = document.querySelector("#sobre-achado .achado-cartao.novo:not([data-m])");
      if (c) { c.setAttribute("data-m", "1"); window.__marcos.push(["cartão", performance.now()]); }
      const b = document.querySelector("#sobre-achado .achado-acoes button:not(.reserva):not([data-m])");
      if (b) { b.setAttribute("data-m", "1"); window.__marcos.push(["botões", performance.now()]); }
    }).observe(document, { childList: true, subtree: true });
  });
  await p.addInitScript(() => {  // o /responder julgado pelo fetch na página (ver ../../mapa/auxiliares/fotografar.mjs)
    const original = window.fetch; window.__respostas = [];
    window.fetch = (...a) => original(...a).then((r) => { if (String(a[0]).includes("/responder") && !r.ok) window.__respostas.push(`status ${r.status}`); return r; },
      (e) => { if (String(a[0]).includes("/responder")) window.__respostas.push(`rejeitado: ${e}`); throw e; });
  });
  if (PROTO) {
    for (const [url, arq] of [["**/static/telas/celebracoes.js", "celebracoes.js"], ["**/static/telas/achado.js", "achado.js"]])
      await p.route(url, (rota) => rota.fulfill({ contentType: "application/javascript", body: readFileSync(path.join(PROTO, arq), "utf8") }));
  }
  const t0 = Date.now();
  try {
    await p.goto(url);
    // no jogo (sem PROTOTIPO): APRESENTACAO=relicario troca a apresentação das celebrações (o Estouro é o padrão)
    if (process.env.APRESENTACAO) await p.evaluate((n) => typeof Festa !== "undefined" && Festa.usar(n), process.env.APRESENTACAO);
    await (await p.waitForSelector("button:has-text('Começar o teste')", { timeout: 30000 })).click();  // a partida do cenário de teste
    if (process.env.PULAR_TEXTO) {  // os vídeos curtos: uma tecla adianta o texto de abertura, como o jogador faria
      const primeiro = sit.passos[0].festa;
      for (let k = 0; k < 40 && !(await p.$(primeiro)); k++) { await p.keyboard.press("x"); await espera(250); }
    }
    for (const passo of sit.passos) {
      if (passo.cedo) {  // o clique rápido, fora dos botões, logo que a janela surge
        const j = await p.waitForSelector(passo.cedo, { timeout: 30000 }).catch(() => null);
        if (j) {
          const t = Date.now();
          await p.mouse.click(Math.round(vw * 0.12), Math.round(vh * 0.5));
          linha.push(`${passo.foto}: clique rápido fora em ${Date.now() - t0} ms`);
          await espera(120);
          linha.push(`${passo.foto}: depois do clique rápido, a janela continua: ${!!(await p.$(passo.cedo))}`);
        } else erros.push(`não apareceu cedo: ${passo.cedo}`);
      }
      const alvo = await p.waitForSelector(passo.festa, { timeout: 30000 }).catch(() => null);
      if (!alvo) { erros.push(`não apareceu: ${passo.festa} (${passo.foto})`); break; }
      const apareceu = Date.now();
      if (passo.festa === ACHADO) await alvo.evaluate((e) => e.setAttribute("data-visto", "1"));  // o próximo é outro
      linha.push(`${passo.foto}: apareceu em ${apareceu - t0} ms`);
      for (const ms of INSTANTES) {
        const falta = apareceu + ms - Date.now();
        if (falta > 0) await espera(falta);
        await p.screenshot({ path: path.join(saida, `${sit.nome}-${passo.foto}-${String(ms).padStart(4, "0")}.png`) });
      }
      // fechar: o gesto do jogador
      if (passo.fechar === "deixar") {  // o último botão da janela (deixar o item); depois, a janela some antes da próxima
        await p.waitForSelector(BOTOES, { timeout: 30000 }).catch(() => null);
        const botoes = await p.$$(BOTOES);
        if (botoes.length) await botoes[botoes.length - 1].click(); else erros.push(`sem botões no achado (${passo.foto})`);
      } else if (passo.fechar === "tecla") await p.keyboard.press("Enter");
      else {
        const c = await p.$("#celebracao .continuar, .festa-espolio .continuar");
        const r = c ? await c.boundingBox() : null;
        if (passo.fechar === "duplo" && r) await p.mouse.dblclick(r.x + r.width / 2, r.y + r.height / 2);
        else if (r) await p.mouse.click(r.x + r.width / 2, r.y + r.height / 2);
      }
      linha.push(`${passo.foto}: fechado (${passo.fechar}) em ${Date.now() - t0} ms`);
      if (passo.fechar !== "deixar") await espera(350);
      if (passo.fechar === "duplo") {  // o clique duplo fecha uma festa só: a próxima continua aberta (ou está chegando)
        await espera(500);
        linha.push(`depois do clique duplo, há festa aberta: ${!!(await p.$("#celebracao:not([hidden]) .festa"))}`);
      }
    }
    await espera(800);
    for (const x of await p.evaluate(() => window.__respostas || [])) erros.push(`/responder: ${x}`);
    let cartao = null;  // os botões de cada achado, em ms depois do cartão dele
    const achados = [];
    for (const [o, t] of await p.evaluate(() => window.__marcos || [])) { if (o === "cartão") cartao = t; else if (cartao !== null) { achados.push(Math.round(t - cartao)); cartao = null; } }
    if (achados.length) linha.push(`achados: botões ${achados.join(", ")} ms depois do cartão`);
  } finally {
    fechando = true;
    const video = p.video();
    await ctx.close();
    if (video) { const v = await video.path(); const destino = path.join(saida, `${sit.nome}.webm`); if (existsSync(v)) renameSync(v, destino); }
    proc.kill();
  }
  registro[sit.nome] = { erros, avisos, linha };
  console.log(sit.nome, erros.length ? erros : "", avisos.length ? avisos : "", linha.join(" | "));
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1));
