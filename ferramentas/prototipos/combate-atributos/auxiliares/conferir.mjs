// Confere e fotografa a demo do combate e dos atributos (protótipo; nada no jogo) a 1920×945 e a 1280×720: sobe o
// servidor numa porta livre com os resultados numa pasta temporária e, em cada janela, confere que a página não rola e
// que nada corta (o topo numa linha, as cartas de ação inteiras), o teclado (número escolhe a ação e o alvo, Esc volta,
// tecla segurada não repete a ação), o clique duplo (uma ação só), o reinício (sem eventos acumulados), o movimento
// reduzido, e fotografa as situações da folha em ../capturas/<janela>-*.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir.mjs
import { spawn } from "child_process";
import { mkdirSync, mkdtempSync } from "fs";
import { tmpdir } from "os";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

const proc = spawn(PY, [path.join(aqui, "..", "servidor.py")], { cwd: raiz,
  env: { ...process.env, DEMO_PORTA: "0", DEMO_SAVES: mkdtempSync(path.join(tmpdir(), "combate-atributos-")), PYTHONIOENCODING: "utf-8" } });
let URL = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m && !URL) URL = m[0]; });
for (let k = 0; k < 100 && !URL; k++) await espera(100);
if (!URL) { console.log("o servidor não subiu"); process.exit(1); }

const estado = (p) => p.evaluate(() => Demo.estado);
async function abrir(p, encontro, dist) {
  await p.goto(URL);
  await p.waitForSelector("#doca .acao");
  await p.selectOption("#encontro", encontro);
  await p.selectOption("#distribuicao", dist);
  await p.waitForFunction(([e, d]) => Demo.estado && Demo.estado.encontro === e && Demo.estado.distribuicao === d, [encontro, dist]);
  await espera(150);
}
// joga pelo teclado: o número da ação e, se pedir alvo, o número do alvo
async function tecla(p, ...ks) { for (const k of ks) { await p.keyboard.press(k); await espera(120); } }
// passa vezes com o ataque básico (ação 1, alvo 1), ou com Defender, até a condição valer
async function ate(p, cond, max = 40, defendendo = false) {
  for (let i = 0; i < max; i++) {
    const e = await estado(p);
    if (await p.evaluate(cond, e)) return true;
    if (e.fim) return false;
    await tecla(p, defendendo ? String(e.acoes.findIndex((a) => a.id === "defender") + 1) : "1");
    if (await p.$(".carta[data-alvo]")) await tecla(p, "1");
  }
  return false;
}
async function semCorte(p, nome) {
  const r = await p.evaluate(() => {
    const de = document.documentElement, topo = document.querySelector("#topo");
    const cortadas = [...document.querySelectorAll(".acao, .carta, .passo")].filter((b) => b.scrollHeight > b.clientHeight + 2 || b.scrollWidth > b.clientWidth + 2).map((b) => b.textContent.trim().slice(0, 30));
    return { rola: de.scrollHeight > innerHeight || de.scrollWidth > innerWidth, topo: topo.getBoundingClientRect().height, cortadas };
  });
  conferir(!r.rola, `${nome}: a página não rola`);
  conferir(r.topo < 64, `${nome}: o topo numa linha (${Math.round(r.topo)} px)`);
  conferir(!r.cortadas.length, `${nome}: nada cortado${r.cortadas.length ? " (" + r.cortadas.join(" | ") + ")" : ""}`);
}
const foto = (p, janela, nome) => p.screenshot({ path: path.join(SAIDA, `${janela}-${nome}.png`) });

const b = await chromium.launch();
try {
  for (const [janela, w, h] of [["1920", 1920, 945], ["1280", 1280, 720]]) {
    console.log(`\n${janela}×${h}`);
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    const erros = [];
    p.on("pageerror", (e) => erros.push(e.message));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });

    // 1 · o tutorial: começo, o Bote anunciado, a escolha de alvo, a ficha
    await abrir(p, "e1", "A");
    await semCorte(p, "início");
    await foto(p, janela, "1-inicio");
    conferir(await ate(p, (e) => e.ameacas.length > 0), "o Lobo Alfa anuncia o Bote antes de dar");
    const am = (await estado(p)).ameacas[0];
    conferir(am.previsto && am.previsto.agora > 0 && /Resolve/.test(await p.textContent(".ameaca")), "a ameaça mostra o alvo, o dano previsto e quando resolve");
    await semCorte(p, "Bote anunciado");
    await foto(p, janela, "2-ameaca");
    // a escolha de alvo pelo teclado: quem tem ação de alvo múltiplo
    await ate(p, (e) => e.aguardando === "odete");
    const iCurar = (await estado(p)).acoes.findIndex((a) => a.id === "curar");
    await tecla(p, String(iCurar + 1));
    conferir((await p.$$(".carta[data-alvo]")).length === 3, "Curar pede o alvo: as três cartas do grupo marcadas");
    await foto(p, janela, "3-alvo");
    await tecla(p, "Escape");
    conferir(!(await p.$(".carta[data-alvo]")) && !!(await p.$("#doca .acao")), "Esc volta das cartas de alvo às ações");
    const t0 = (await estado(p)).turno_id;
    await tecla(p, String(iCurar + 1), "2");
    conferir((await estado(p)).turno_id > t0, "número da ação e número do alvo fazem a ação");
    await p.click('#abas [data-aba="ficha"]');
    await semCorte(p, "ficha");
    await foto(p, janela, "4-ficha");
    await p.click('#abas [data-aba="registro"]');

    // tecla segurada: só uma ação
    await ate(p, (e) => e.aguardando === "heroi");
    let e0 = await estado(p);
    const iDef = e0.acoes.findIndex((a) => a.id === "defender");
    for (let k = 0; k < 6; k++) await p.keyboard.down(String(iDef + 1));
    await p.keyboard.up(String(iDef + 1));
    await espera(400);
    let e1 = await estado(p);
    conferir(e1.eventos.filter((x) => x.tipo === "acao" && x.ator === "heroi").length === e0.eventos.filter((x) => x.tipo === "acao" && x.ator === "heroi").length + 1,
      "tecla segurada (repetição do teclado) faz uma ação só");
    // clique duplo: só uma ação
    await ate(p, (e) => e.aguardando === "heroi");
    e0 = await estado(p);
    await p.dblclick(`#doca .acao[data-i="${iDef}"]`);
    await espera(500);
    e1 = await estado(p);
    conferir(e1.eventos.filter((x) => x.tipo === "acao" && x.ator === "heroi").length === e0.eventos.filter((x) => x.tipo === "acao" && x.ator === "heroi").length + 1,
      "clique duplo faz uma ação só");
    conferir(!(await p.textContent("#doca")).includes("Essa vez já passou"), "o segundo clique não aparece como erro");

    // reiniciar três vezes: nada acumulado
    await abrir(p, "e1", "A");
    const n0 = (await estado(p)).eventos.length, reg0 = await p.$$eval("#registro p, #registro h4", (x) => x.length);
    for (let k = 0; k < 3; k++) { await tecla(p, "r"); await espera(250); }
    const er = await estado(p);
    conferir(er.eventos.length === n0 && er.rodada === 1 && (await p.$$eval("#registro p, #registro h4", (x) => x.length)) === reg0,
      `reiniciar 3 vezes não acumula eventos (${er.eventos.length} = ${n0})`);

    // 2 · o Golpe Esmagador anunciado, com as respostas possíveis
    await abrir(p, "e2", "B");
    conferir(await ate(p, (e) => e.ameacas.length > 0), "o Bruto anuncia o Golpe Esmagador");
    await semCorte(p, "Esmagador");
    await foto(p, janela, "5-esmagador");

    // 3 · o xamã: invocação no fim da ordem e o Grito de Terror resolvido (A perde a vez)
    await abrir(p, "e3", "A");
    conferir(await ate(p, (e) => e.ordem.some((o) => o.id.startsWith("afogado") && o.entra)), "a invocação entra no fim da ordem, esperando a rodada seguinte");
    await foto(p, janela, "6-invocacao");
    conferir(await ate(p, (e) => e.eventos.some((x) => x.tipo === "resolve"), 40, true), "o Grito de Terror resolve");
    await semCorte(p, "terror");
    await foto(p, janela, "7-terror");

    // os testes de queda e retorno, com a condição identificada
    await abrir(p, "t2", "A");
    conferir(await p.isVisible("#teste") && /Condições de teste/.test(await p.textContent("#teste")), "o caso de teste mostra a condição artificial");
    const iPena = (await estado(p)).acoes.findIndex((a) => a.id === "item:pena");
    await tecla(p, String(iPena + 1));
    conferir((await estado(p)).aguardando === "morel" && (await estado(p)).rodada === 1, "Pena de Fênix antes da posição: Morel age na mesma rodada");
    await foto(p, janela, "8-retorno-antes");
    await abrir(p, "t3", "A");
    await ate(p, (e) => e.aguardando === "odete");
    await tecla(p, String((await estado(p)).acoes.findIndex((a) => a.id === "reerguer") + 1));
    conferir((await estado(p)).aguardando !== "morel" && /age na próxima/.test(await p.textContent("#registro")), "Reerguer depois da posição: Morel só na próxima rodada");
    await foto(p, janela, "9-retorno-depois");

    // o fim
    await abrir(p, "t4", "A");
    await ate(p, (e) => !!e.fim);
    conferir(await p.isVisible("#fim") && /Vitória/.test(await p.textContent("#fim")), "o fim mostra o resumo");
    await foto(p, janela, "10-fim");

    // as janelas: comparar, fora da luta, resultados
    await p.click('#topo [data-abrir="comparar"]');
    await p.waitForSelector(".comparar table");
    conferir((await p.$$("#modal tr.difere")).length >= 8, "comparar destaca o que muda entre A, B e C");
    const mod = await p.evaluate(() => { const c = document.querySelector("#modal .caixa"); return c.scrollHeight <= c.clientHeight + 2; });
    conferir(mod || janela === "1280", "comparar cabe sem rolar a 1920");
    await foto(p, janela, "11-comparar");
    await p.keyboard.press("Escape");
    await p.click('#topo [data-abrir="situacao"]');
    await p.waitForSelector(".opcoes");
    await p.click('.opcoes [data-op="ler"][data-ajuda]');
    await p.waitForSelector(".resultado");
    await foto(p, janela, "12-fora-da-luta");
    await p.keyboard.press("Escape");
    await p.click('#topo [data-abrir="resultados"]');
    await p.waitForSelector("#modal h2");
    conferir((await p.$$("#modal .resultados tbody tr")).length >= 1, "resultados da sessão anotados");
    await foto(p, janela, "13-resultados");
    await p.keyboard.press("Escape");

    conferir(!erros.length, `sem erros no console${erros.length ? ": " + erros.join(" | ") : ""}`);
    await ctx.close();
  }

  // movimento reduzido: os eventos novos chegam sem animação
  console.log("\nmovimento reduzido");
  const ctx = await b.newContext({ viewport: { width: 1920, height: 945 }, reducedMotion: "reduce" });
  const p = await ctx.newPage();
  await abrir(p, "e1", "A");
  await tecla(p, "1", "1");
  const anim = await p.$$eval("#registro .ev.novo", (x) => x.map((n) => getComputedStyle(n).animationName));
  conferir(anim.length > 0 && anim.every((a) => a === "none"), "sem animação nos eventos novos");
  await ctx.close();
} finally {
  await b.close();
  proc.kill();
}
console.log(falhas ? `\n${falhas} falha(s)` : "\ntudo ok");
process.exit(falhas ? 1 : 0);
