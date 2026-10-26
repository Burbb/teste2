// Confere e fotografa a v4 da demo do combate e dos atributos (a v3 sem a Marca, com o Golpe Oportuno e a Chuva de
// Brasas) a 1920×945 e a 1280×720: a comparação do fogo em Preparar, a Chuva pondo Queimadura no grupo e a Conflagração
// consumindo antes de expirar num encontro normal, o Morel sem Marcar e com o Golpe Oportuno, e o que a v3 já conferia:
// tela Preparar (tipo e escala de cada habilidade, dano por alvo com as resistências, o manto mudando o dano recebido,
// a combinação de Queimadura, a ultimate ou "sem ultimate equipada"), a luta (sem rolagem nem corte, previsão igual ao
// dano real por tipo, a ultimate disponível e depois "já usada", a ameaça do Bruto ininterruptível sinalizada), o
// teclado, a tecla segurada, o clique duplo, o reinício, os resultados com os detalhes, o movimento reduzido e os
// caminhos para a v2 e a v1. Grava ../capturas/v4-*.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/combate-atributos/auxiliares/conferir4.mjs
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
async function prep(p) { await p.goto(URL); await p.waitForSelector("#prep .lutar"); await espera(300); }
async function mudouFicha(p, acao) {
  const antes = JSON.stringify(await ficha(p));
  await acao();
  await p.waitForFunction((a) => JSON.stringify(Demo.ficha) !== a, antes).catch(() => {});
  await espera(150);
}
const build = (p, id) => mudouFicha(p, () => p.click(`[data-build="${id}"]`));
async function lutar(p, encontro) {
  await p.selectOption("#prep-encontro", encontro);
  await p.click("#prep .lutar");
  await p.waitForFunction((e) => Demo.estado && Demo.estado.encontro === e && !document.querySelector("#prep:not([hidden])"), encontro);
  await espera(200);
}
async function ate(p, cond, max = 80, defendendo = false) {
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
const foto = (p, janela, nome) => p.screenshot({ path: path.join(SAIDA, `v4-${janela}-${nome}.png`) });
const realDe = (ev) => +ev.texto.split(": ").pop().split(" ")[0];

const b = await chromium.launch();
try {
  for (const [janela, w, h] of [["1920", 1920, 945], ["1280", 1280, 720]]) {
    console.log(`\n${janela}×${h}`);
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    const erros = [];
    p.on("pageerror", (e) => erros.push(e.message));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });

    // Preparar
    await prep(p);
    await build(p, "chama");
    await semCorte(p, "Preparar", ".build, .hab, .atr li");
    conferir((await p.$$("#prep .hab .tipo-dano")).length >= 8, "cada habilidade de dano mostra o tipo");
    const fC = await ficha(p);
    const chu = fC.dano.find((d) => d.id === "chuva"), bra = fC.dano.find((d) => d.id === "brasa");
    conferir(chu.alvos.cao.normal < chu.alvos.bruto.normal && bra.alvos.cao.normal < bra.alvos.bruto.normal,
      "a resistência ao fogo aparece no dano previsto (Chuva e Brasa no Cão)");
    conferir(fC.fogo && fC.fogo.length >= 8 && /O fogo jogado de verdade/.test(await p.textContent(".fichao")), "a comparação do fogo aparece em Preparar");
    conferir(fC.kit.includes("chuva") && (await p.$$('[data-hab="chuva"]')).length === 1, "a Chuva de Brasas está no kit da Chama");
    await foto(p, janela, "1-preparar-chama");
    // a Chuva no grupo e a Conflagração antes de expirar, num encontro normal (o xamã, o soldado e o afogado)
    await lutar(p, "e3");
    await ate(p, (e) => e.aguardando === "heroi", 80, true);
    let ef = await estado(p);
    await tecla(p, String(ef.acoes.findIndex((a) => a.id === "chuva") + 1));
    ef = await estado(p);
    const queimando = ef.inimigos.filter((o) => o.vivo && o.estados.some((x) => x.id === "queimadura")).length;
    conferir(queimando >= 2, `a Chuva põe Queimadura em cada inimigo (${queimando})`);
    await ate(p, (e) => e.aguardando === "heroi", 80, true);
    await semCorte(p, "fogo no grupo");
    await foto(p, janela, "2-chuva-no-grupo");
    ef = await estado(p);
    const iC = ef.acoes.findIndex((a) => a.id === "conflagracao");
    conferir(!ef.acoes[iC].motivo, "a Conflagração está disponível com a reserva básica");
    await tecla(p, String(iC + 1));
    ef = await estado(p);
    conferir(!ef.inimigos.some((o) => o.estados.some((x) => x.id === "queimadura")) && /Queimadura restante/.test(await p.textContent("#registro")), "a Conflagração consome as Queimaduras (o registro mostra a conta)");
    await ate(p, (e) => e.aguardando === "morel", 80, true);
    ef = await estado(p);
    conferir(!ef.acoes.some((a) => a.id === "marcar") && ef.acoes.some((a) => a.id === "oportuno"), "Morel sem Marcar, com o Golpe Oportuno");
    await foto(p, janela, "3-conflagracao");
    await tecla(p, "p");
    await mudouFicha(p, () => p.selectOption('[data-equip="manto"]', "salamandra"));
    const m = (await ficha(p)).equipamento.manto.linhas;
    conferir(m.find((l) => l.id === "salamandra").recebido[0].dano < m.find((l) => l.id === "comum").recebido[0].dano, "o Manto de salamandra reduz o Sopro de Brasa");
    conferir(/fogo/i.test((await ficha(p)).derivados.find((d) => d.id === "res_fogo").nome) && (await ficha(p)).derivados.find((d) => d.id === "res_fogo").valor === "35%", "a resistência ao fogo aparece na ficha (35%)");
    await build(p, "baluarte");
    conferir(/Avanço do Baluarte/.test(await p.textContent(".fichao")), "o Baluarte mostra o Avanço na tabela de dano");
    await foto(p, janela, "4-preparar-baluarte");
    await build(p, "precisao");
    conferir(/Sem ultimate equipada/.test(await p.textContent(".fichao")), "sem ultimate: a ficha diz");
    await build(p, "forca");
    await p.click('[data-hab="desafio"]', { force: true });
    conferir(!(await p.evaluate(() => Demo.cfg.kit.includes("desafio"))), "kit no orçamento");
    await p.click('[data-hab="juramento"]', { force: true });
    conferir(!(await p.evaluate(() => Demo.cfg.kit.includes("juramento"))), "no máximo uma ultimate");

    // a luta: previsão por tipo e a ultimate
    await lutar(p, "e2");
    await semCorte(p, "luta");
    await foto(p, janela, "5-luta");
    conferir(/disponível/.test(await p.textContent('.carta[data-id="heroi"] .ult')), "a ultimate aparece disponível desde o início");
    await ate(p, (e) => e.aguardando === "heroi", 80, true);
    let e = await estado(p);
    const iGP = e.acoes.findIndex((a) => a.id === "golpe_pesado");
    await tecla(p, String(iGP + 1));
    conferir((await p.$$(".carta[data-alvo] .previsto")).length === 3, "na escolha de alvo, cada carta mostra o dano previsto");
    await foto(p, janela, "6-alvo-previsto");
    const alvo = e.acoes[iGP].alvos[0], pv = e.acoes[iGP].previsoes[alvo];
    const n0 = e.eventos.length;
    await tecla(p, "1");
    e = await estado(p);
    const ev = e.eventos.slice(n0).find((x) => x.tipo === "dano" && x.alvo === alvo);
    conferir(realDe(ev) === (/crítico/.test(ev.conta) ? pv.critico : pv.normal), `o dano real é o previsto (${realDe(ev)})`);
    await ate(p, (e) => e.aguardando === "heroi", 80, true);
    e = await estado(p);
    await tecla(p, String(e.acoes.findIndex((a) => a.ultimate) + 1));
    await ate(p, (e) => e.aguardando === "heroi", 80, true);
    conferir(/já usada/.test(await p.textContent('.carta[data-id="heroi"] .ult')) && /já usada/.test(await p.textContent("#doca .acao.ult")), "depois de usada: \"já usada nesta luta\" na carta e na ação");
    await foto(p, janela, "7-ultimate-usada");
    // tecla segurada e clique duplo
    let e0 = await estado(p);
    const iDef = e0.acoes.findIndex((a) => a.id === "defender");
    for (let k = 0; k < 6; k++) await p.keyboard.down(String(iDef + 1));
    await p.keyboard.up(String(iDef + 1));
    await espera(400);
    const conta = (x) => x.eventos.filter((v) => v.tipo === "acao" && v.ator === "heroi").length;
    conferir(conta(await estado(p)) === conta(e0) + 1, "tecla segurada faz uma ação só");
    await ate(p, (e) => e.aguardando === "heroi", 80, true);
    e0 = await estado(p);
    await p.dblclick(`#doca .acao[data-i="${iDef}"]`);
    await espera(500);
    conferir(conta(await estado(p)) === conta(e0) + 1, "clique duplo faz uma ação só");
    // o Bruto furioso: ininterruptível e sinalizado
    conferir(await ate(p, (e) => e.ameacas.some((a) => a.de === "bruto#1"), 120, true), "o Bruto anuncia o Golpe Esmagador");
    await semCorte(p, "ameaça");
    await foto(p, janela, "8-ameaca");
    // reiniciar três vezes
    await tecla(p, "r");
    await espera(300);
    const nr = (await estado(p)).eventos.length;
    for (let k = 0; k < 3; k++) { await tecla(p, "r"); await espera(250); }
    conferir((await estado(p)).eventos.length === nr && (await estado(p)).rodada === 1, "reiniciar 3 vezes não acumula eventos");

    // os cães de brasa com o manto
    await tecla(p, "p");
    await build(p, "runa");
    await lutar(p, "e4");
    conferir(/Resiste fogo 60%/.test(await p.textContent("#frente")), "o Cão mostra a resistência ao fogo");
    await foto(p, janela, "9-caes");
    await ate(p, (e) => !!e.fim, 200);
    await foto(p, janela, "10-fim");

    // as janelas
    await p.click('#topo [data-abrir="comparar"]');
    await p.waitForSelector(".comparar table");
    conferir((await p.$$("#modal tr.difere")).length >= 12, "comparar destaca o que muda entre as builds");
    await foto(p, janela, "11-comparar");
    await p.keyboard.press("Escape");
    await p.click('#topo [data-abrir="resultados"]');
    await p.waitForSelector("#modal h2");
    await p.click("#modal .detalhe");
    await p.waitForSelector("#modal .detalhes");
    conferir(/→/.test(await p.textContent("#modal .linha")) && /Ultimate de Jean/.test(await p.textContent("#modal thead")), "resultados com a ultimate, as ameaças e o recurso antes → depois");
    await foto(p, janela, "12-resultados");
    await p.keyboard.press("Escape");
    await p.click('#topo a[href="/v3/"]');
    await p.waitForSelector("#prep .lutar");
    conferir(/v3/.test(await p.title()) && (await p.evaluate(() => fetch("/api3/catalogo").then((r) => r.json()))).habilidades.every((h) => h.id !== "chuva"), "a v3 abre pelo botão do topo, como estava");
    await p.goto(URL + "v2/");
    await p.waitForSelector("#prep .lutar");
    conferir(/v2/.test(await p.title()), "a v2 continua em /v2/");
    await p.goto(URL + "v1/");
    await p.waitForSelector("#doca .acao");
    conferir(/v1/.test(await p.title()), "a v1 continua em /v1/");
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
