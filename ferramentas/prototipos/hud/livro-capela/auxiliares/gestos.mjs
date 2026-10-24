// Confere os gestos do livro no jogo de verdade (cenarios_livro.py), nas três propostas e no livro de hoje:
// - a primeira leitura grava as mesmas pistas (Ilse e o Sigilo) e mostra o mesmo cartão; reler não muda nada;
// - as teclas do menu não escolhem nada embaixo do livro; um clique no véu não chega ao jogo;
// - A, A refinada e B: Esc, Enter e espaço fecham, o véu fecha (como hoje), o Tab fica no Fechar;
// - C: Próxima e Anterior (botões e setas), o foco previsível, o Anterior volta à primeira entrada, o véu não fecha,
//   o Tab circula só nos botões do livro, Esc fecha de qualquer entrada.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/livro-capela/auxiliares/gestos.mjs
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

async function subir(proposta, caso) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_livro.py"), caso],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: proposta } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});

async function abrirPagina(v, caso) {
  const { proc, url } = await subir(v === "atual" ? "" : v, caso);
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = [];
  p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url);
  for (let k = 0; k < 80 && !(await p.$(`${MENU}:has-text("Ler o livro da capela")`)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(300);
  return { p, proc, erros };
}
const pistas = (p) => p.evaluate(() => JSON.stringify((estado.missoes || []).map((m) => m.pistas)));
const aberto = (p) => p.$("#sobre-leitura:not([hidden])").then((e) => !!e);
const ler = async (p) => { await p.click(`${MENU}:has-text("Ler o livro da capela")`); await p.waitForSelector("#sobre-leitura:not([hidden])", { timeout: 20000 }); await espera(400); };
const depois = async (p) => {
  await (await p.waitForSelector("#prompt .continuar", { timeout: 20000 })).click();
  await p.waitForSelector(`${MENU}:has-text("Descer ao ossuário")`, { timeout: 20000 });
  await espera(300);
};

let referencia = null;  // as pistas do livro de hoje (VERSOES começa por "atual" para comparar)
for (const v of (process.env.VERSOES || "atual,a,a2,capela,b,c").split(",")) {
  console.log(`== ${v}`);
  let { p, proc, erros } = await abrirPagina(v, "primeira");
  const antes = await pistas(p);
  await ler(p);
  await p.keyboard.press("2");  // a tecla do menu ("Descer ao ossuário") não escolhe nada embaixo do livro
  await espera(300);
  conferir(await aberto(p), "a tecla 2 não escolhe nada embaixo do livro");
  if (v === "c") {
    const foco = () => p.evaluate(() => document.activeElement.className);
    conferir(/lv-prox/.test(await foco()) && /Entrada 1 de 2/.test(await p.textContent(".lv-conta")), "C abre na entrada 1, com o foco no Próxima");
    conferir(await p.$eval(".lv-ant", (e) => e.disabled), "C: na entrada 1, o Anterior está desligado");
    await p.mouse.click(30, 470);  // o véu, à esquerda do livro (por cima do painel do herói)
    await espera(200);
    conferir(await aberto(p), "C: o clique no véu não fecha nem chega ao jogo");
    await p.keyboard.press("Enter");  // o Próxima com o foco
    await espera(400);
    conferir(/Entrada 2 de 2/.test(await p.textContent(".lv-conta")) && /Que Deus nos perdoe/.test(await p.textContent(".lv-pagina")),
      "C: Enter no Próxima mostra a segunda entrada inteira");
    conferir(/lv-fechar/.test(await foco()), "C: na última entrada, o foco passa ao Fechar");
    await p.keyboard.press("Tab"); const f1 = await foco();
    await p.keyboard.press("Tab"); const f2 = await foco();
    conferir(/lv-ant/.test(f1) && /lv-fechar/.test(f2), "C: o Tab circula só entre os botões ligados do livro (Anterior, Fechar)");
    await p.keyboard.press("ArrowLeft");
    await espera(400);
    conferir(/Entrada 1 de 2/.test(await p.textContent(".lv-conta")) && /guardiã desta casa/.test(await p.textContent(".lv-pagina")),
      "C: a seta para a esquerda volta à primeira entrada");
    conferir(/lv-prox/.test(await foco()), "C: de volta à primeira, o foco no Próxima");
    await p.keyboard.press("ArrowRight"); await espera(300);
    await p.click(".lv-ant"); await espera(300);
    conferir(/Entrada 1 de 2/.test(await p.textContent(".lv-conta")), "C: o botão Anterior volta à primeira entrada");
    await p.keyboard.press("PageDown"); await espera(300);
    conferir(/Entrada 2 de 2/.test(await p.textContent(".lv-conta")), "C: PageDown vai à segunda");
    await p.keyboard.press("Escape");
  } else if (["a", "a2", "capela", "b"].includes(v)) {
    const foco = await p.evaluate(() => document.activeElement.className);
    await p.keyboard.press("Tab");
    conferir(/lv-fechar/.test(foco) && /lv-fechar/.test(await p.evaluate(() => document.activeElement.className)), `${v.toUpperCase()}: o foco no Fechar, e o Tab fica nele`);
    await p.keyboard.press("Escape");
  } else {
    await p.keyboard.press("Escape");
  }
  await espera(300);
  conferir(!(await aberto(p)), "Esc fecha");
  await p.waitForSelector("#prompt .continuar", { timeout: 20000 });
  const cartao = await p.textContent("#texto .novidade-missao").catch(() => "");
  conferir(/Ilse/.test(cartao) && /Sigilo do Turvo/.test(cartao), "a primeira leitura mostra o cartão de Ilse e do Sigilo");
  await depois(p);
  const agora = await pistas(p);
  conferir(antes !== agora, "a primeira leitura grava as pistas");
  if (v === "atual") referencia = agora; else conferir(agora === referencia, "as pistas iguais às do livro de hoje (nada a mais, nada a menos)");
  // reler: nada muda; nas A e B, pelo Enter e pelo véu; na C, pelo botão Fechar
  await ler(p);
  if (["a", "a2", "capela", "b"].includes(v)) {
    await p.keyboard.press("Enter"); await espera(300);
    conferir(!(await aberto(p)), `${v.toUpperCase()}: Enter fecha`);
    await depois(p);
    await ler(p);
    await p.mouse.click(30, 470); await espera(300);
    conferir(!(await aberto(p)), `${v.toUpperCase()}: o véu fecha, como hoje`);
    conferir(!!(await p.$("#prompt .continuar")) && !(await p.$("#texto .novidade-missao:last-of-type ~ *:has-text('Descer')")),
      `${v.toUpperCase()}: o clique no véu só fecha, não escolhe nada embaixo`);
  } else if (v === "c") {
    await p.click(".lv-fechar"); await espera(300);
    conferir(!(await aberto(p)), "C: o botão Fechar fecha");
  } else {
    await p.click("#sobre-leitura .grimorio-fechar"); await espera(300);
  }
  await depois(p);
  conferir((await pistas(p)) === agora, "reler não muda as pistas");
  conferir(erros.length === 0, "sem erros na página" + (erros.length ? ": " + erros.slice(0, 2).join(" | ") : ""));
  await p.close(); proc.kill();
}
// o movimento reduzido: o livro já aberto, sem animação de abrir nem de virar
{
  const { proc, url } = await subir("c", "releitura");
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, reducedMotion: "reduce" });
  await p.goto(url);
  for (let k = 0; k < 80 && !(await p.$(`${MENU}:has-text("Ler o livro da capela")`)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await ler(p);
  conferir(await p.$eval(".lv-quadro", (e) => getComputedStyle(e).animationName === "none"), "movimento reduzido: o livro abre sem animação");
  await p.keyboard.press("ArrowRight"); await espera(100);
  conferir(await p.$eval(".lv-pagina", (e) => getComputedStyle(e).animationName === "none"), "movimento reduzido: a entrada troca sem animação");
  await p.close(); proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
