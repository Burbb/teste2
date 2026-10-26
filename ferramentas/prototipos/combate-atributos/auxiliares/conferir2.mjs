// Confere e fotografa a v2 da demo (em /v2/; a v3 tem conferir3.mjs) do combate e dos atributos (protótipo; nada no jogo) a 1920×945 e a 1280×720: sobe
// o servidor numa porta livre com os resultados numa pasta temporária e confere a tela Preparar (orçamento do kit, uma
// ultimate, a ficha mudando com a build, a arma mudando o dano, Presença sem efeito na luta), a luta (sem rolagem nem
// corte, a previsão no alvo igual ao dano real, a chance de resistir na ameaça, a ultimate com Ímpeto), o teclado, a
// tecla segurada, o clique duplo, o reinício, o movimento reduzido e o caminho para a v1. Grava ../capturas/v2-*.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir2.mjs
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
const ficha = (p) => p.evaluate(() => Demo.ficha);
async function tecla(p, ...ks) { for (const k of ks) { await p.keyboard.press(k); await espera(120); } }
async function prep(p) { await p.goto(URL + "v2/"); await p.waitForSelector("#prep .lutar"); await espera(300); }
async function build(p, id) {
  const antes = JSON.stringify(await ficha(p));
  await p.click(`[data-build="${id}"]`);
  await p.waitForFunction((a) => JSON.stringify(Demo.ficha) !== a, antes).catch(() => {});
  await espera(150);
}
async function lutar(p, encontro) {
  await p.selectOption("#prep-encontro", encontro);
  await p.click("#prep .lutar");
  await p.waitForFunction((e) => Demo.estado && Demo.estado.encontro === e && !document.querySelector("#prep:not([hidden])"), encontro);
  await espera(200);
}
async function ate(p, cond, max = 60, defendendo = false) {
  for (let i = 0; i < max; i++) {
    const e = await estado(p);
    if (await p.evaluate(cond, e)) return true;
    if (e.fim) return false;
    await tecla(p, defendendo ? String(e.acoes.findIndex((a) => a.id === "defender") + 1) : "1");
    if (await p.$(".carta[data-alvo]")) await tecla(p, "1");
  }
  return false;
}
async function semCorte(p, nome, seletores = ".acao, .carta, .passo") {
  const r = await p.evaluate((sel) => {
    const de = document.documentElement, topo = document.querySelector("#topo");
    const cortadas = [...document.querySelectorAll(sel)].filter((b) => b.offsetParent && (b.scrollHeight > b.clientHeight + 2 || b.scrollWidth > b.clientWidth + 2)).map((b) => b.textContent.trim().slice(0, 30));
    const g = document.querySelector("#grupo");
    if (g && g.offsetParent && g.scrollHeight > g.clientHeight + 2) cortadas.push("o grupo não cabe na coluna");
    return { rola: de.scrollHeight > innerHeight || de.scrollWidth > innerWidth, topo: topo.getBoundingClientRect().height, cortadas };
  }, seletores);
  conferir(!r.rola, `${nome}: a página não rola`);
  conferir(r.topo < 64, `${nome}: o topo numa linha (${Math.round(r.topo)} px)`);
  conferir(!r.cortadas.length, `${nome}: nada cortado${r.cortadas.length ? " (" + r.cortadas.join(" | ") + ")" : ""}`);
}
const foto = (p, janela, nome) => p.screenshot({ path: path.join(SAIDA, `v2-${janela}-${nome}.png`) });
const danoFicha = (f, id) => (f.dano.find((d) => d.id === id) || {}).normal;

const b = await chromium.launch();
try {
  for (const [janela, w, h] of [["1920", 1920, 945], ["1280", 1280, 720]]) {
    console.log(`\n${janela}×${h}`);
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    const erros = [];
    p.on("pageerror", (e) => erros.push(e.message));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });

    // Preparar: as builds, o kit, a ficha, o equipamento, a Presença
    await prep(p);
    await build(p, "forca");
    await semCorte(p, "Preparar", ".build, .hab, .atr li");
    await foto(p, janela, "1-preparar-forca");
    const fF = await ficha(p);
    await build(p, "precisao");
    const fP = await ficha(p);
    conferir(danoFicha(fF, "golpe_pesado") !== undefined && fF.derivados.find((d) => d.id === "fisico").valor > fP.derivados.find((d) => d.id === "fisico").valor,
      "Força tem mais potência física que Precisão; a ficha muda com a build");
    conferir(fP.derivados.find((d) => d.id === "iniciativa").valor < fF.derivados.find((d) => d.id === "iniciativa").valor, "Precisão age antes");
    await foto(p, janela, "2-preparar-precisao");
    await build(p, "runa");
    const fR = await ficha(p);
    conferir(danoFicha(fR, "lamina") > danoFicha(fR, "atacar") * 2, "Runa: a Lâmina Rúnica (Intelecto) muito acima do ataque com a arma (Força 2)");
    await build(p, "forca");
    // o kit: cheio (10 pontos), uma caríssima recusada; a outra ultimate recusada
    const pts = await p.evaluate(() => Demo.cfg.kit.length);
    await p.click('[data-hab="desafio"]', { force: true });
    conferir((await p.evaluate(() => Demo.cfg.kit.length)) === pts, "kit no orçamento: o Desafio (3 pontos) não entra num kit de 10 de 10");
    await p.click('[data-hab="tempestade"]', { force: true });
    conferir(!(await p.evaluate(() => Demo.cfg.kit.includes("tempestade"))), "no máximo uma ultimate");
    conferir(/Já há uma ultimate/.test(await p.textContent('[data-hab="tempestade"]')), "o motivo aparece na habilidade recusada");
    // a arma muda o dano; a Presença não
    const a0 = danoFicha(await ficha(p), "atacar");
    await p.selectOption('[data-equip="arma"]', "mestre");
    await p.waitForFunction((v) => Demo.ficha && Demo.ficha.equip.arma === "mestre", a0);
    const a1 = danoFicha(await ficha(p), "atacar");
    conferir(a1 > a0, `a Espada de mestre aumenta o Atacar (${a0} → ${a1})`);
    await foto(p, janela, "3-preparar-arma");
    await p.selectOption('[data-equip="arma"]', "comum");
    await p.waitForFunction(() => Demo.ficha && Demo.ficha.equip.arma === "comum");
    const d0 = JSON.stringify((await ficha(p)).dano);
    await p.click('[data-pres="1"]');
    await p.waitForFunction(() => Demo.ficha && Demo.ficha.presenca === Demo.cfg.presenca);
    conferir(JSON.stringify((await ficha(p)).dano) === d0, "Presença não muda o dano previsto");
    await p.click('[data-pres="-1"]');

    // a luta: o encontro 1
    await lutar(p, "e1");
    await semCorte(p, "luta");
    await foto(p, janela, "4-luta");
    conferir(await ate(p, (e) => e.aguardando === "heroi"), "a vez de Jean");
    let e = await estado(p);
    const iGP = e.acoes.findIndex((a) => a.id === "golpe_pesado");
    await tecla(p, String(iGP + 1));
    const cartas = await p.$$eval(".carta[data-alvo] .previsto", (x) => x.map((n) => n.textContent));
    conferir(cartas.length === 2 && cartas.every((t) => /de dano/.test(t)), "na escolha de alvo, cada carta mostra o dano previsto");
    await foto(p, janela, "5-alvo-previsto");
    const alvo = e.acoes[iGP].alvos[0], pv = e.acoes[iGP].previsoes[alvo];
    const n0 = e.eventos.length;
    await tecla(p, "1");
    e = await estado(p);
    const ev = e.eventos.slice(n0).find((x) => x.tipo === "dano" && x.alvo === alvo);
    const real = +ev.texto.split(": ").pop().split(" ")[0];
    conferir(real === (/crítico/.test(ev.conta) ? pv.critico : pv.normal), `o dano real é o previsto (${real}; previsto ${pv.normal}, crítico ${pv.critico})`);
    await tecla(p, "Escape");
    // tecla segurada e clique duplo
    await ate(p, (e) => e.aguardando === "heroi");
    let e0 = await estado(p);
    const iDef = e0.acoes.findIndex((a) => a.id === "defender");
    for (let k = 0; k < 6; k++) await p.keyboard.down(String(iDef + 1));
    await p.keyboard.up(String(iDef + 1));
    await espera(400);
    const conta = (x) => x.eventos.filter((v) => v.tipo === "acao" && v.ator === "heroi").length;
    conferir(conta(await estado(p)) === conta(e0) + 1, "tecla segurada faz uma ação só");
    await ate(p, (e) => e.aguardando === "heroi");
    e0 = await estado(p);
    await p.dblclick(`#doca .acao[data-i="${iDef}"]`);
    await espera(500);
    conferir(conta(await estado(p)) === conta(e0) + 1, "clique duplo faz uma ação só");
    // reiniciar três vezes
    await tecla(p, "r");
    await espera(300);
    const nr = (await estado(p)).eventos.length;
    for (let k = 0; k < 3; k++) { await tecla(p, "r"); await espera(250); }
    const er = await estado(p);
    conferir(er.eventos.length === nr && er.rodada === 1, `reiniciar 3 vezes não acumula eventos (${er.eventos.length} = ${nr})`);

    // o encontro 2 com o Baluarte: a ameaça mostra a chance final de resistir
    await tecla(p, "p");
    await build(p, "baluarte");
    await lutar(p, "e2");
    conferir(await ate(p, (e) => e.ameacas.length > 0, 60, true), "o Bruto anuncia o Golpe Esmagador");
    const am = (await estado(p)).ameacas[0];
    conferir(am.resiste !== undefined && /resistir: \d+%/.test(await p.textContent(".ameaca")), `a ameaça mostra a chance final de resistir (${Math.round(am.resiste * 100)}%)`);
    await semCorte(p, "ameaça");
    await foto(p, janela, "6-ameaca-tenacidade");

    // a ultimate: o teste com Ímpeto cheio
    await tecla(p, "p");
    await build(p, "forca");
    await lutar(p, "t5");
    await ate(p, (e) => e.aguardando === "heroi");
    const iU = (await estado(p)).acoes.findIndex((a) => a.ultimate);
    conferir(iU >= 0 && !(await estado(p)).acoes[iU].motivo, "com 3 de Ímpeto a ultimate fica disponível");
    await foto(p, janela, "7-ultimate");
    await tecla(p, String(iU + 1));
    conferir((await estado(p)).aliados[0].impeto === 0, "a ultimate gasta o Ímpeto");
    await ate(p, (e) => !!e.fim);
    conferir(await p.isVisible("#fim"), "o fim mostra o resumo");
    await foto(p, janela, "8-fim");

    // as janelas
    await p.click('#topo [data-abrir="comparar"]');
    await p.waitForSelector(".comparar table");
    conferir((await p.$$("#modal tr.difere")).length >= 12, "comparar destaca o que muda entre as builds");
    await foto(p, janela, "9-comparar");
    await p.keyboard.press("Escape");
    await p.click('#topo [data-abrir="situacao"]');
    await p.waitForSelector(".opcoes");
    conferir(/Presença/.test(await p.textContent(".opcoes")), "a Presença aparece fora da luta");
    await p.click('.opcoes [data-op="falar"]');
    await p.waitForSelector(".resultado");
    await foto(p, janela, "10-fora-da-luta");
    await p.keyboard.press("Escape");
    await p.click('#topo [data-abrir="resultados"]');
    await p.waitForSelector("#modal h2");
    conferir((await p.$$("#modal .resultados tbody tr")).length >= 3, "resultados com build, kit e recurso");
    await foto(p, janela, "11-resultados");
    await p.keyboard.press("Escape");

    // a v1 continua lá
    await p.click('#topo a[href="/v1/"]');
    await p.waitForSelector("#doca .acao");
    conferir(/v1/.test(await p.title()), "a v1 abre pelo botão do topo");
    conferir(!erros.length, `sem erros no console${erros.length ? ": " + erros.join(" | ") : ""}`);
    await ctx.close();
  }

  console.log("\nmovimento reduzido");
  const ctx = await b.newContext({ viewport: { width: 1920, height: 945 }, reducedMotion: "reduce" });
  const p = await ctx.newPage();
  await prep(p);
  await lutar(p, "e1");
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
