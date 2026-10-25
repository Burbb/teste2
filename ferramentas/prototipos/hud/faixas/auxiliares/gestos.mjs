// Confere o ritmo e os gestos das faixas no jogo de verdade (cenarios_faixas.py), nas faixas de hoje e nas propostas
// (VERSOES=atual,r, o padrão; atual,a,b para as da rodada anterior; JOGO=1: o jogo já com a integração, conferido como
// as propostas), a 1920×945:
// - a sequência real (o lobo guardião, o quinto lobo, o herói a 1 XP de subir): a ordem dos acontecimentos na tela
//   (Guardião derrotado → Mestre caçador → o quadro do espólio → a subida de nível → o achado) e os tempos entre eles,
//   iguais nas três (nenhuma espera a mais);
// - cliques e a tecla "1" durante as faixas não escolhem nada na tela seguinte (o achado continua esperando);
// - as faixas não recebem cliques (pointer-events) e saem sozinhas; o movimento reduzido mostra a mesma faixa, parada;
// - nas propostas, cada anúncio sai antes do próximo (hoje, o Guardião e o Mestre ficam juntos ~0,1 s).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/faixas/auxiliares/gestos.mjs
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

async function subir(caso, proposta) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_faixas.py"), caso],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "normal", PYTHONPATH: raiz, PROPOSTA: proposta } });  // o ritmo de verdade
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  return { proc, url };
}
async function escolher(p, texto) {
  for (let k = 0; k < 80; k++) {
    const e = await p.$(`${MENU}:has-text("${texto}")`);
    if (e) { await e.click(); return; }
    await espera(250);
  }
}

// o que a tela mostra a cada 50 ms, como uma linha do tempo de marcos
const MARCOS = () => {
  const vis = (e) => !!e && e.getClientRects().length > 0;
  const todas = [...document.querySelectorAll(".faixa-festa, .fx-faixa")];
  const faixa = todas.filter((e) => !e.classList.contains("troca")).map((e) => e.querySelector("b")?.textContent.trim()).join("|");
  return { faixa, juntas: todas.filter((e) => !e.classList.contains("troca")).length, saindo: todas.filter((e) => e.classList.contains("troca")).length, roda: !!document.querySelector('#roda .roda-botao[data-slot="atacar"]'),
    espolio: vis(document.querySelector("#celebracao .festa-espolio")),
    achado: vis(document.querySelector("#sobre-achado:not(.saindo)")), nivel: vis(document.querySelector(".festa.fb2, .festa.fa2")) };
};

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const linhas = {};
const VERS = (process.env.VERSOES || "atual,r").split(",");
for (const v of VERS) {
  console.log(`== ${v}`);
  const { proc, url } = await subir("sequencia", v === "atual" ? "" : v);
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url);
  await escolher(p, "Começar");
  const ordem = [], t = {};
  let t0 = null, clicou = false, esperouAchado = false, juntas = 0, trocaMs = 0;
  const fim = Date.now() + 40000;
  while (Date.now() < fim) {
    const m = await p.evaluate(MARCOS);
    if (t0 === null && m.faixa) t0 = Date.now();
    if (t0 === null) {  // a luta: ataca até ela acabar (o golpe pode errar)
      if (m.roda) { await p.click('#roda .roda-botao[data-slot="atacar"]').catch(() => {}); await p.mouse.move(2, 2); }
      await espera(50);
      continue;
    }
    juntas = Math.max(juntas, m.juntas);
    if (m.saindo) trocaMs += 50;
    for (const f of m.faixa.split("|").filter(Boolean)) if (!(("faixa:" + f) in t)) { t["faixa:" + f] = Date.now() - t0; ordem.push("faixa:" + f); }
    for (const k of ["espolio", "nivel", "achado"]) if (m[k] && !(k in t)) { t[k] = Date.now() - t0; ordem.push(k); }
    // durante a primeira faixa: três cliques no palco e a tecla 1 (a primeira opção de uma tela de menu)
    if (m.faixa && !clicou) {
      clicou = true;
      const pe = await p.evaluate(() => getComputedStyle(document.querySelector(".faixa-festa, .fx-faixa")).pointerEvents);
      conferir(pe === "none", `a faixa não recebe cliques (pointer-events: ${pe})`);
      for (let i = 0; i < 3; i++) await p.mouse.click(960, 260);
      await p.keyboard.press("1");
    }
    if (m.achado && !esperouAchado) {
      esperouAchado = true;
      await espera(1500);
      conferir((await p.evaluate(MARCOS)).achado, "o achado continua esperando a escolha (os cliques e a tecla das faixas não escolheram nada)");
      await p.click("#sobre-achado .achado-acoes button").catch(() => {});
      break;
    }
    // o quadro do espólio e a festa do nível: o Continuar depois de 1,5 s à vista, como quem lê (um clique logo de
    // cara adianta o que vem: o gesto de sempre, igual nas três)
    for (const k of ["espolio", "nivel"]) if (m[k] && !m.achado && Date.now() - t0 - t[k] > 1500 && !t["fechou-" + k]) {
      t["fechou-" + k] = Date.now() - t0;
      await p.click("#celebracao .festa .continuar").catch(() => {});
    }
    await espera(50);
  }
  linhas[v] = { ordem, t };
  console.log(`    faixas inteiras juntas, no máximo: ${juntas}; a anterior saindo durante a troca: ~${trocaMs} ms`);
  if (v !== "atual" || process.env.JOGO) conferir(juntas <= 1 && trocaMs <= 200, "cada anúncio sai antes do próximo (a troca do Guardião para o Mestre, limpa)");
  console.log("    ordem:", ordem.join(" → "));
  console.log("    tempos (ms desde a primeira faixa):", JSON.stringify(t));
  conferir(ordem[0]?.startsWith("faixa:Guardião") && ordem.some((o) => o.startsWith("faixa:Mestre")), "Guardião derrotado e depois Mestre caçador");
  const ixE = ordem.indexOf("espolio"), ixA = ordem.indexOf("achado"), ixN = ordem.indexOf("nivel");
  conferir(ixE > 0 && ixN > ixE && ixA > ixN, "depois das faixas: o espólio, a subida de nível e o achado, nessa ordem (a do jogo)");
  conferir(erros.length === 0, "sem erros na página" + (erros.length ? ": " + erros[0] : ""));
  await p.close(); proc.kill();
}
// os mesmos tempos nas três (a fila é a de hoje; a faixa nova só desenha): a diferença fica no ruído do roteiro
const chave = (v, k) => linhas[v].t[k];
for (const k of ["faixa:Mestre caçador", "espolio", "nivel", "achado"]) {
  const vs = VERS.map((v) => chave(v, k));
  conferir(vs.every((x) => typeof x === "number") && Math.max(...vs) - Math.min(...vs) <= 250, `"${k}" chega no mesmo tempo em todas (${vs.join(", ")} ms)`);
}
// o movimento reduzido: a mesma faixa, parada, no mesmo tempo
for (const v of VERS.filter((x) => x !== "atual" || process.env.JOGO)) {
  const { proc, url } = await subir("comitiva", v === "atual" ? "" : v);
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, reducedMotion: "reduce" });
  await p.goto(url); await escolher(p, "Começar");
  await p.waitForSelector(".fx-faixa, .faixa-festa", { timeout: 20000 });
  await espera(700);  // no meio da duração (1,6 s): a faixa continua inteira, sem animar
  const st = await p.$eval(".fx-faixa, .faixa-festa", (e) => ({ anim: getComputedStyle(e).animationName, texto: e.textContent.replace(/\s+/g, " ").trim(),
    fx: !!document.querySelector(".fx-faixa-palco") }));
  conferir(st.anim === "none" && /Irmã Odette se junta a você/.test(st.texto) && /clériga desertora/.test(st.texto) && !st.fx,
    `${v.toUpperCase()}, movimento reduzido: a faixa inteira, parada, sem efeitos (${st.texto})`);
  await p.close(); proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
