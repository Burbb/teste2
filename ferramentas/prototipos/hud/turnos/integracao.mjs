// A iniciativa e os turnos INTEGRADOS (1.116.0; o lugar novo do anúncio e a placa parada no impacto, 1.116.1): o jogo como está, sem nada desta pasta na página. Lutas de verdade
// (cenário tutorial com EMBOSCADA, LUTA_APOS_ESCOLHA, LUTA/GRUPO, COMITIVA, SERVOS e SEMENTE; nada simulado na luta):
//   iniciativa    paladino com Morel contra 3 lobos, a sua iniciativa: o turno 1 (só você), Habilidades, a mira e o
//                 Voltar, o ataque que usa a iniciativa, o turno 2 (1280×720 e 1500×950; e com movimento reduzido)
//   emboscada     o mesmo, com a emboscada deles (o golpe livre do lobo mais rápido antes do turno 1)
//   sem vantagem  o mesmo, sem surpresa: o turno 1 comum
//   cheia         necromante com Morel, Odette e 3 servos contra 5 caídos e o xamã, a sua iniciativa: Meditar no turno
//                 livre (a iniciativa passa), a Maldição em área, o turno 3 (1280×720 e 1500×950)
//   atordoado     paladino com Morel contra 3 aranhas (SEMENTE=7): no turno 2 você começa preso na teia e perde a vez
// Mede o que o protótipo mediu (anúncios por mensagem de turno, o que cobre, o tempo até a vez) e, desde o carregamento
// da página, quantas partículas de festa (i.particula) aparecem: o estouro que saía antes da luta. A festa de nível ao
// vivo (uma mensagem "celebrar" dada à tela, fora do replay) continua com o estouro dela.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/turnos/integracao.mjs
import { spawn } from "child_process";
import { mkdirSync, readdirSync, renameSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, process.env.SAIDA_PASTA || "capturas-1.116.1"), VIDEOS = path.join(SAIDA, "videos");
mkdirSync(VIDEOS, { recursive: true });
for (const d of [SAIDA, VIDEOS]) for (const f of readdirSync(d)) if (/\.(png|json|webm)$/.test(f)) rmSync(path.join(d, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";
const LOBOS = { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" };
const CHEIA = { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "mago", ESPEC: "necromante", NIVEL: "12", NIVEL_LUTA: "9", REC: "0.7", COMITIVA: "morel,odete", SERVOS: "3",
  GRUPO: "caido:5,xama_caido:1", LUGAR: "charco", PERIODO: "3", EMBOSCADA: "jogador" };
const relatorio = [], erros = [];

async function subir(amb) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[cenario] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
// uma página: a versão (producao/proposta); o relógio dos turnos (a mensagem do motor, o anúncio, a vez clicável)
async function pagina(url, [W, H], versao, nome, { reduzido = false, video = false } = {}) {
  const ctx = await b.newContext({ viewport: { width: W, height: H }, reducedMotion: reduzido ? "reduce" : "no-preference",
    ...(video ? { recordVideo: { dir: VIDEOS, size: { width: W, height: H } } } : {}) });
  const p = await ctx.newPage();
  // as partículas de festa criadas desde o carregamento da página (o estouro que saía antes da luta)
  await p.addInitScript(() => { window.__particulas = 0; document.addEventListener("DOMContentLoaded", () => new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => { if (n.classList && n.classList.contains("particula")) window.__particulas++; }))).observe(document.body, { childList: true })); });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  // o relógio (nas duas versões): quando cada "turno" chega e quando a vez fica clicável depois dele
  const relogio = `;(() => { window.__turnos = []; const t0 = window.turno; window.turno = (m, ...x) => { window.__turnos.push({ n: m.n, t: performance.now(), vez: null }); return t0(m, ...x); };
    window.__anuncios = []; new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => { if (n.classList && n.classList.contains("turnos-anuncio")) { const t0 = performance.now(), txt = n.textContent.replace(/\\s+/g, " ").trim(); window.__anuncios.push(txt); const i = window.__anuncios.length - 1;
      const fim = new MutationObserver(() => { if (!n.isConnected) { fim.disconnect(); window.__anuncios[i] = txt + " (" + Math.round(performance.now() - t0) + " ms à vista)"; } }); fim.observe(n.parentNode, { childList: true }); } })))
      .observe(document.documentElement, { childList: true, subtree: true });
    const olhar = () => { const u = window.__turnos[window.__turnos.length - 1]; if (u && u.vez === null && typeof pergunta !== "undefined" && pergunta && !processando && document.querySelector('#roda .roda-botao[data-slot="atacar"]')) u.vez = Math.round(performance.now() - u.t); requestAnimationFrame(olhar); }; requestAnimationFrame(olhar); })();`;
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch(); let corpo = await res.text();
    corpo += relogio;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
  await p.goto(url);
  // a luta começa com a página aberta (LUTA_APOS_ESCOLHA): a surpresa e o turno 1 chegam ao vivo, como no jogo
  await p.waitForSelector('#prompt .escolha:has-text("Começar a luta")', { timeout: 30000 });
  await espera(400);
  await p.click('#prompt .escolha:has-text("Começar a luta")');
  return { p, ctx };
}
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="atacar"]'));
async function vez(p) {
  for (let k = 0; k < 240; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(100);
  }
  throw new Error("a vez do herói não chegou");
}
const slot = (p, s) => p.$(`#roda .roda-botao[data-slot="${s}"]`);
// o que o protótipo põe na tela e o que ele cobre
const olhar = (p) => p.evaluate(() => {
  const r = (e) => e.getBoundingClientRect(), toca = (a, q) => a.right > q.left + 1 && a.left < q.right - 1 && a.bottom > q.top + 1 && a.top < q.bottom - 1;
  const nossos = [...document.querySelectorAll(".turnos-anuncio, .turnos-placa")].filter((e) => getComputedStyle(e).visibility !== "hidden")
    .map((e) => [e.classList.contains("turnos-placa") ? `placa (${e.dataset.lugar === "fora" ? "presa à borda de baixo da arena" : "no pé da faixa dos comandos"})`
      : "anúncio (borda de cima da área de combate)", r(e), e.textContent.replace(/\s+/g, " ").trim()]);
  const outros = [...[...document.querySelectorAll("#batalha .carta")].map((c) => [`carta ${c.querySelector(".carta-nome span").textContent}`, r(c)]),
    ...[...document.querySelectorAll("#roda .roda-botao")].map((c) => [`comando ${c.dataset.slot}`, r(c)]),
    ...[...document.querySelectorAll(".roda-mira, .roda-janela")].map((c) => [c.classList.contains("roda-mira") ? "mira" : "seletor", r(c)]),
    ...[...document.querySelectorAll("#arena > .mods-arena .mod")].map((c) => ["aviso da cena", r(c)])];
  const cobre = [], comandos = [];
  for (const [n, q] of nossos) for (const [m, w] of outros) if (toca(q, w)) (m.startsWith("comando") && n.startsWith("anúncio") ? comandos : cobre).push(`${n.split(" (")[0]} × ${m}`);
  const an = [...document.querySelectorAll(".turnos-anuncio")].find((e) => getComputedStyle(e).visibility !== "hidden"), pl = document.querySelector(".turnos-placa"), ar = document.getElementById("arena").getBoundingClientRect();
  const pg = document.getElementById("pagina").getBoundingClientRect();
  // o texto do topo (data, sinais, menu): folhas com texto ou ícone
  const topo = [...document.querySelectorAll("#topo *")].filter((e) => !e.children.length && e.getClientRects().length && (e.textContent.trim() || e.tagName === "svg" || e.tagName === "IMG")).map(r);
  const cortado = an ? [...an.children].some((e) => e.scrollWidth > e.clientWidth + 1) : false;
  const anuncio = an ? { centro_do_anuncio_menos_centro_da_arena: Math.round((r(an).left + r(an).right) / 2 - (ar.left + ar.right) / 2), sobre_o_texto_do_topo: topo.some((q) => toca(r(an), q)), texto_cortado: cortado, sobre_a_placa: !!(pl && getComputedStyle(pl).visibility !== "hidden" && toca(r(an), r(pl))), sobre_o_registro: toca(r(an), pg), caixa: [r(an).left, r(an).top, r(an).right, r(an).bottom].map(Math.round) } : null;
  return { mostra: nossos.map(([n, , t]) => `${n}: ${t}`), cobre: cobre.join(", ") || "nada", comandos_sob_o_anuncio: comandos.join(", ") || "nenhum", anuncio };
});
const foto = (p, nome) => p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
const esperarTurno = (p, n) => p.waitForFunction((n) => (window.__turnos || []).some((x) => x.n === n), n, { timeout: 30000 });
async function encerrar(p, ctx, r, nomeVideo) {
  r.turnos = await p.evaluate(() => window.__turnos.map((x) => `turno ${x.n}: a vez clicável ${x.vez} ms depois`));
  r.anuncios_mostrados = await p.evaluate(() => window.__anuncios);
  r.particulas_de_festa = await p.evaluate(() => window.__particulas);
  const v = p.video();
  await ctx.close();
  if (v && nomeVideo) renameSync(await v.path(), path.join(VIDEOS, `${nomeVideo}.webm`));
}

async function iniciativa(versao, tam, opcoes = {}) {
  const t = `${tam[0]}x${tam[1]}${opcoes.reduzido ? "-reduzido" : ""}`, nome = `iniciativa-${versao}-${t}`, r = { nome };
  const { proc, url } = await subir({ ...LOBOS, EMBOSCADA: "jogador" });
  try {
    const { p, ctx } = await pagina(url, tam, versao, nome, opcoes);
    // o anúncio do turno 1 (o protótipo, com a iniciativa) 250 ms depois da mensagem
    await esperarTurno(p, 1); await espera(250);
    r.turno1 = await olhar(p); await foto(p, `${nome}-1-turno1`);
    await vez(p); await espera(1500); await p.mouse.move(5, tam[1] - 5);
    r.depois_do_anuncio = await olhar(p); await foto(p, `${nome}-2-iniciativa-disponivel`);
    await (await slot(p, "habilidades")).click(); await espera(600);
    r.habilidades = await olhar(p); await foto(p, `${nome}-3-habilidades`);
    const hab = await p.$('.roda-janela .rj-linha:not(.bloqueada)[data-hab="golpe_pesado"], .roda-janela .rj-linha:not(.bloqueada)[data-hab="golpe_sagrado"]');
    if (hab) { await hab.click(); await espera(700); r.mira = await olhar(p); await foto(p, `${nome}-4-mira`); const v = await p.$(".mira-voltar"); if (v) await v.click(); await vez(p); await espera(300); }
    // o ataque que usa a iniciativa
    await (await slot(p, "atacar")).click();
    for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(50);
    const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
    await p.waitForFunction(() => /usada|passou/i.test((document.querySelector(".turnos-placa") || {}).innerText || "") || !document.querySelector(".turnos-placa"), null, { timeout: 8000 }).catch(() => {});
    r.golpe = await olhar(p); await foto(p, `${nome}-5-golpe`);
    await esperarTurno(p, 2); await espera(250);
    r.turno2 = await olhar(p); await foto(p, `${nome}-6-turno2`);
    await vez(p); await espera(1500);
    r.turno2_depois = await olhar(p); await foto(p, `${nome}-7-turno2-placa`);
    await encerrar(p, ctx, r, opcoes.video ? nome : null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}
async function emboscada(versao, tam, opcoes = {}) {
  const nome = `emboscada-${versao}-${tam[0]}x${tam[1]}`, r = { nome };
  const { proc, url } = await subir({ ...LOBOS, EMBOSCADA: "inimigo" });
  try {
    const { p, ctx } = await pagina(url, tam, versao, nome, opcoes);
    await p.waitForFunction(() => !!document.querySelector(".turnos-anuncio.emboscada") || !!document.querySelector("#batalha .carta.surpreso"), null, { timeout: 20000 }).catch(() => {});
    await espera(200);
    r.emboscada = await olhar(p); await foto(p, `${nome}-1-emboscada`);
    await esperarTurno(p, 1); await espera(250);
    r.turno1 = await olhar(p); await foto(p, `${nome}-2-turno1`);
    await vez(p); await espera(1500);
    r.depois = await olhar(p); await foto(p, `${nome}-3-placa`);
    await encerrar(p, ctx, r, opcoes.video ? nome : null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}
async function cheia(versao, tam) {
  const nome = `cheia-${versao}-${tam[0]}x${tam[1]}`, r = { nome };
  const { proc, url } = await subir(CHEIA);
  try {
    const { p, ctx } = await pagina(url, tam, versao, nome);
    await esperarTurno(p, 1); await espera(250);
    r.turno1 = await olhar(p); await foto(p, `${nome}-1-turno1`);
    await vez(p); await espera(1300);
    // o turno livre gasto em Meditar: a iniciativa passa sem golpe
    await (await slot(p, "habilidades")).click(); await espera(500);
    await (await p.$('.roda-janela .rj-linha[data-hab="meditar"]')).click();
    await p.waitForFunction(() => /passou/i.test((document.querySelector(".turnos-placa") || {}).innerText || "") || (window.__turnos || []).some((x) => x.n === 2), null, { timeout: 10000 }).catch(() => {});
    r.meditar = await olhar(p); await foto(p, `${nome}-2-iniciativa-passou`);
    // turno 2: a comitiva e os servos agiram antes? (o turno livre é só seu; eles entram no 2) — e a Maldição em área
    await esperarTurno(p, 2); await vez(p); await espera(300);
    r.turno2 = await olhar(p);
    await (await slot(p, "habilidades")).click(); await espera(500);
    await (await p.$('.roda-janela .rj-linha[data-hab="maldicao"]')).click();
    await esperarTurno(p, 3); await espera(250);
    r.turno3 = await olhar(p); await foto(p, `${nome}-3-turno3-efeitos`);
    await vez(p); await espera(1500);
    r.turno3_depois = await olhar(p); await foto(p, `${nome}-4-turno3-placa`);
    await (await slot(p, "habilidades")).click(); await espera(600);
    r.habilidades = await olhar(p); await foto(p, `${nome}-5-habilidades`);
    await encerrar(p, ctx, r, null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}

async function semVantagem(tam) {
  const nome = `sem-vantagem-${tam[0]}x${tam[1]}`, r = { nome };
  const { proc, url } = await subir({ ...LOBOS });
  try {
    const { p, ctx } = await pagina(url, tam, "jogo", nome);
    await esperarTurno(p, 1); await espera(250);
    r.turno1 = await olhar(p); await foto(p, `${nome}-1-turno1`);
    await vez(p); await espera(1500);
    r.depois = await olhar(p); await foto(p, `${nome}-2-placa`);
    await encerrar(p, ctx, r, null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}
// o turno perdido: atacar o primeiro alvo até começar um turno preso na teia; o anúncio diz, e a roda não vem
async function atordoado(tam, opcoes = {}) {
  const nome = `atordoado-${tam[0]}x${tam[1]}${opcoes.reduzido ? "-reduzido" : ""}`, r = { nome, turnos_presos: [] };
  const { proc, url } = await subir({ ...LOBOS, LUTA: "aranha", SEMENTE: "7" });
  try {
    const { p, ctx } = await pagina(url, tam, "jogo", nome, opcoes);
    for (let t = 1; t <= 4; t++) {
      await esperarTurno(p, t); await espera(250);
      const preso = await p.evaluate(() => ((estado.combate && estado.combate.heroi.efeitos) || []).filter((e) => estado.estados[e.id] && estado.estados[e.id].perde_turno).map((e) => e.nome));
      const visto = await olhar(p);
      if (preso.length) {
        r.turnos_presos.push(t);
        r[`turno${t}_preso`] = visto; await foto(p, `${nome}-turno${t}-preso`);
        // durante o turno perdido, a roda de comandos não aparece (nada sugere que você pode agir)
        await espera(500);
        r[`turno${t}_comandos_a_vista`] = await p.evaluate(() => document.querySelectorAll("#roda .roda-botao").length);
        continue;
      }
      r[`turno${t}`] = visto;
      await vez(p);
      await (await slot(p, "atacar")).click();
      for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(50);
      const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
    }
    await encerrar(p, ctx, r, opcoes.video ? nome : null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}
// a festa de nível ao vivo continua com o estouro dela (uma mensagem "celebrar" dada à tela fora do replay; a mesma
// mensagem refazendo a página não solta nada)
async function festa() {
  const r = { nome: "festa-de-nivel" };
  const { proc, url } = await subir({ ...LOBOS });
  try {
    const { p, ctx } = await pagina(url, [1280, 720], "jogo", "festa");
    await vez(p);
    const m = { t: "celebrar", tipo: "nivel", dados: { nivel: 9, ganhos: { Vida: 8 }, habilidades: [], especializacao: false } };
    r.ao_vivo = await p.evaluate(async (m) => {
      const n0 = document.querySelectorAll(".particula").length;
      Telas.celebrar(m, false);
      await new Promise((x) => setTimeout(x, 120));
      const n = document.querySelectorAll(".particula").length - n0, b = document.querySelector("#celebracao .continuar");
      if (b) b.click();
      return `${n} partículas, a janela da festa ${b ? "aberta" : "AUSENTE"}`;
    }, m);
    await espera(1700);
    r.refazendo = await p.evaluate(async (m) => {
      const n0 = document.querySelectorAll(".particula").length;
      await Telas.celebrar(m, true);
      await new Promise((x) => setTimeout(x, 120));
      return `${document.querySelectorAll(".particula").length - n0} partículas, a janela ${document.getElementById("celebracao").hidden ? "fechada" : "ABERTA"}`;
    }, m);
    await encerrar(p, ctx, r, null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}

// a finalização: o golpe que encerra a luta chega perto (zoom) e o impacto treme a arena; a placa e o anúncio, que são
// interface, ficam parados. A cada quadro: quanto a arena se mexeu e quanto a placa e o anúncio se mexeram.
async function finalizacao(tam, opcoes = {}) {
  const nome = `finalizacao-${tam[0]}x${tam[1]}${opcoes.reduzido ? "-reduzido" : ""}`, r = { nome };
  const { proc, url } = await subir({ ...LOBOS, QUANTOS: "2", NIVEL_LUTA: "1", EMBOSCADA: "jogador" });
  try {
    const { p, ctx } = await pagina(url, tam, "jogo", nome, opcoes);
    await esperarTurno(p, 1); await vez(p); await espera(400);
    // a cada quadro, até a luta acabar: a arena (se mexendo ou não), a placa e o anúncio
    await p.evaluate(() => {
      window.__quadros = [];
      const q = () => {
        const a = document.getElementById("arena");
        if (!a) return;
        const pl = document.querySelector(".turnos-placa"), an = document.querySelector(".turnos-anuncio");
        const cs = getComputedStyle(a), ra = a.getBoundingClientRect(), rp = pl && pl.getBoundingClientRect(), rn = an && an.getBoundingClientRect();
        window.__quadros.push({ arena: [ra.left, ra.top, ra.width], mexendo: a.classList.contains("foco-final") || cs.transform !== "none" || cs.translate !== "none",
          placa: rp && rp.width ? [rp.left, rp.top] : null, anuncio: rn && rn.width && getComputedStyle(an).visibility !== "hidden" ? [an.offsetLeft, an.offsetTop] : null  /* o lugar dele (a entrada dele mesmo desliza de propósito) */, ok: !!(estado && estado.combate) });
        if (estado && estado.combate) requestAnimationFrame(q);
      };
      requestAnimationFrame(q);
    });
    for (let t = 0; t < 8 && (await p.evaluate(() => !!(estado && estado.combate))); t++) {
      if (!(await p.evaluate(() => !!document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando))) { await espera(200); continue; }
      await (await slot(p, "atacar")).click();
      for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(50);
      const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
      // o golpe final: a câmera chega perto (foco-final); a foto no meio do zoom
      for (let k = 0; k < 30; k++) {
        if (await p.evaluate(() => document.getElementById("arena") && document.getElementById("arena").classList.contains("foco-final"))) { await espera(250); await foto(p, `${nome}-zoom`); break; }
        await espera(60);
      }
      await espera(400);
    }
    await espera(1500);
    r.quadros = await p.evaluate(() => {
      const qs = window.__quadros, calmo = qs.find((x) => !x.mexendo) || qs[0], mex = qs.filter((x) => x.mexendo);
      // a referência de cada quadro que se mexe: o último quadro calmo antes dele (a placa pode mudar de turno no meio)
      let ultimoCalmo = calmo, arena = 0, placa = 0, anuncio = 0;
      const d = (a, b) => (a && b ? Math.max(Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1])) : 0);
      for (const x of qs) {
        if (!x.mexendo) { ultimoCalmo = x; continue; }
        arena = Math.max(arena, Math.abs(x.arena[0] - ultimoCalmo.arena[0]), Math.abs(x.arena[1] - ultimoCalmo.arena[1]), Math.abs(x.arena[2] - ultimoCalmo.arena[2]));
        placa = Math.max(placa, d(x.placa, ultimoCalmo.placa));
        anuncio = Math.max(anuncio, d(x.anuncio, ultimoCalmo.anuncio));
      }
      return `${qs.length} quadros, ${mex.length} com a arena se mexendo (zoom do golpe final ou tremida): a arena se deslocou ou cresceu até ${arena.toFixed(1)} px; a placa se moveu ${placa.toFixed(1)} px; o anúncio, ${anuncio.toFixed(1)} px`;
    });
    r.fim = await p.evaluate(() => (estado && estado.combate ? "a luta seguia" : "a luta acabou"));
    await encerrar(p, ctx, r, null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}
// redimensionar no meio da luta: a placa acompanha a arena; o anúncio seguinte, no centro entre os grupos
async function redimensionar() {
  const r = { nome: "redimensionar", passos: [] };
  const { proc, url } = await subir(CHEIA);
  try {
    const { p, ctx } = await pagina(url, [1500, 950], "jogo", "redimensionar");
    await esperarTurno(p, 1); await vez(p); await espera(1300);
    for (const [W, H] of [[1280, 720], [1500, 950]]) {
      await p.setViewportSize({ width: W, height: H }); await espera(900);
      r.passos.push({ janela: `${W}×${H}`, ...(await olhar(p)) });
      await foto(p, `redimensionar-${W}x${H}`);
    }
    // o turno seguinte já no tamanho novo
    await (await slot(p, "habilidades")).click(); await espera(400);
    await (await p.$('.roda-janela .rj-linha[data-hab="meditar"]')).click();
    await esperarTurno(p, 2); await espera(250);
    r.turno2 = await olhar(p); await foto(p, "redimensionar-turno2");
    await encerrar(p, ctx, r, null);
  } finally { proc.kill(); }
  relatorio.push(r); console.log(JSON.stringify(r));
}

await iniciativa("jogo", [1280, 720]);
await iniciativa("jogo", [1500, 950]);
await iniciativa("jogo", [1280, 720], { reduzido: true });
await emboscada("jogo", [1280, 720]);
await emboscada("jogo", [1500, 950]);
await semVantagem([1280, 720]);
await cheia("jogo", [1280, 720]);
await cheia("jogo", [1500, 950]);
await atordoado([1280, 720]);
await atordoado([1500, 950]);
await atordoado([1280, 720], { reduzido: true });
await festa();
await finalizacao([1280, 720]);
await finalizacao([1500, 950]);
await finalizacao([1280, 720], { reduzido: true });
await redimensionar();
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
console.log(erros.length ? `ERROS ${erros.join(" | ")}` : "sem erros");
