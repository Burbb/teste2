// Protótipo da etapa 1C (iniciativa e turnos): a produção e a proposta com os mesmos dados, em lutas de verdade
// (cenário tutorial com EMBOSCADA, LUTA/GRUPO, COMITIVA e SERVOS; nada simulado). A proposta é turnos.js e turnos.css
// anexados ao fim do controles.js da página (antes de a luta começar a chegar), sem trocar nada do jogo.
//   iniciativa   paladino com Morel contra 3 lobos, com a sua iniciativa: o turno 1 (só você), Habilidades aberto, a mira
//                e o Voltar, o ataque que usa a iniciativa, o turno 2 (1280×720 e 1500×950; e com movimento reduzido)
//   emboscada    o mesmo, com a emboscada deles: o golpe livre do lobo mais rápido antes do turno 1
//   cheia        necromante com Morel, Odette e 3 servos contra 5 caídos e o xamã, à noite, com a sua iniciativa: o
//                turno 1 gasto em Meditar (a iniciativa passa sem golpe), a Maldição em área no turno 2 (efeitos em
//                todas as cartas), o turno 3; a comitiva e os servos agem sem anúncio de turno
// Mede: quantos anúncios para quantas mensagens "turno" do motor; o que o anúncio e a placa cobrem (cartas, comandos,
// mira, seletor, o aviso da cena); o tempo da mensagem "turno" até a vez ficar clicável (igual nas duas versões).
// Grava vídeos curtos (webm) da produção e da proposta, para o ritmo.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/turnos/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync, readdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas"), VIDEOS = path.join(SAIDA, "videos");
mkdirSync(VIDEOS, { recursive: true });
for (const d of [SAIDA, VIDEOS]) for (const f of readdirSync(d)) if (/\.(png|json|webm)$/.test(f)) rmSync(path.join(d, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const JS = readFileSync(path.join(aqui, "turnos.js"), "utf8"), CSS = readFileSync(path.join(aqui, "turnos.css"), "utf8");
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
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  // o relógio (nas duas versões): quando cada "turno" chega e quando a vez fica clicável depois dele
  const relogio = `;(() => { window.__turnos = []; const t0 = window.turno; window.turno = (m, ...x) => { window.__turnos.push({ n: m.n, t: performance.now(), vez: null }); return t0(m, ...x); };
    window.__anuncios = []; new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => { if (n.classList && n.classList.contains("turnos-anuncio")) window.__anuncios.push(n.innerText.replace(/\\s+/g, " ").trim()); })))
      .observe(document.documentElement, { childList: true, subtree: true });
    const olhar = () => { const u = window.__turnos[window.__turnos.length - 1]; if (u && u.vez === null && typeof pergunta !== "undefined" && pergunta && !processando && document.querySelector('#roda .roda-botao[data-slot="atacar"]')) u.vez = Math.round(performance.now() - u.t); requestAnimationFrame(olhar); }; requestAnimationFrame(olhar); })();`;
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch(); let corpo = await res.text();
    // a proposta entra antes do relógio, para o relógio medir a mensagem passando por ela também
    if (versao === "proposta") corpo += `\n;(() => { const s = document.createElement("style"); s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
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
    .map((e) => [`${e.classList.contains("turnos-placa") ? "placa" : "anúncio"} (${e.dataset.lugar === "fora" ? "abaixo da arena" : "na arena"})`, r(e), e.innerText.replace(/\s+/g, " ").trim()]);
  const outros = [...[...document.querySelectorAll("#batalha .carta")].map((c) => [`carta ${c.querySelector(".carta-nome span").textContent}`, r(c)]),
    ...[...document.querySelectorAll("#roda .roda-botao")].map((c) => [`comando ${c.dataset.slot}`, r(c)]),
    ...[...document.querySelectorAll(".roda-mira, .roda-janela")].map((c) => [c.classList.contains("roda-mira") ? "mira" : "seletor", r(c)]),
    ...[...document.querySelectorAll("#arena > .mods-arena .mod")].map((c) => ["aviso da cena", r(c)])];
  const cobre = [];
  for (const [n, q, t] of nossos) for (const [m, w] of outros) if (toca(q, w)) cobre.push(`${n} × ${m}`);
  return { mostra: nossos.map(([n, , t]) => `${n}: ${t}`), cobre: cobre.join(", ") || "nada" };
});
const foto = (p, nome) => p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
const esperarTurno = (p, n) => p.waitForFunction((n) => (window.__turnos || []).some((x) => x.n === n), n, { timeout: 30000 });
async function encerrar(p, ctx, r, nomeVideo) {
  r.turnos = await p.evaluate(() => window.__turnos.map((x) => `turno ${x.n}: a vez clicável ${x.vez} ms depois`));
  r.anuncios_mostrados = await p.evaluate(() => window.__anuncios);
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

for (const versao of ["producao", "proposta"]) {
  await iniciativa(versao, [1280, 720], { video: true });
  await emboscada(versao, [1280, 720], { video: versao === "proposta" });
  await cheia(versao, [1280, 720]);
}
await iniciativa("proposta", [1500, 950]);
await cheia("proposta", [1500, 950]);
await iniciativa("proposta", [1280, 720], { reduzido: true, video: true });
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
console.log(erros.length ? `ERROS ${erros.join(" | ")}` : "sem erros");
