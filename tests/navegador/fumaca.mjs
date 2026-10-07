// Teste de fumaça da interface web: sobe cenários preparados (cenarios.py), joga pela tela como uma pessoa
// e falha se aparecer erro no console ou se algo essencial não estiver lá.
//
//   node tests/navegador/fumaca.mjs          (na raiz do repositório; precisa do pacote playwright)
//
// Sai com código 0 se tudo passou, 1 se algo falhou e 77 se não há como rodar (playwright/navegador ausentes).
import { spawn } from "child_process";
import path from "path";

let chromium;
try {
  ({ chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright"));
} catch (e) {
  console.log("PULAR: pacote playwright não encontrado");
  process.exit(77);
}

const RAIZ = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const falhas = [];
const conferir = (ok, msg) => { if (!ok) falhas.push(msg); console.log((ok ? "  ok  " : "  FALHOU ") + msg); };

async function subir(cenario) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario], { cwd: RAIZ, env: { VELOCIDADE: "rapido", ...process.env, PYTHONPATH: RAIZ } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(d));
  for (let k = 0; k < 100 && !url; k++) await new Promise((r) => setTimeout(r, 100));
  if (!url) throw new Error("o servidor do cenário não subiu: " + cenario);
  return { proc, url };
}

async function abrir(browser, url) {
  const page = await browser.newPage({ viewport: { width: 1500, height: 950 } });
  const erros = [];
  page.on("pageerror", (e) => erros.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
  await page.goto(url);
  const esperar = async (sel, ms = 20000) => {
    for (let t = 0; t < ms; t += 100) {
      const e = await page.$(sel);
      if (e) return e;
      const c = await page.$("#prompt .continuar");
      if (c) await c.click().catch(() => {});
      await page.waitForTimeout(100);
    }
    return null;
  };
  return { page, erros, esperar };
}

async function cenarioCombate(browser) {
  console.log("cenário: combate");
  const { proc, url } = await subir("combate");
  const { page, erros, esperar } = await abrir(browser, url);
  try {
    conferir(!!(await esperar(".acoes-combate .escolha")), "as ações de combate aparecem");
    conferir((await page.$$("#batalha .carta")).length >= 3, "a arena mostra herói, comitiva e inimigo");
    await (await page.$('.acoes-combate .escolha:has-text("Habilidades")')).click();
    conferir(!!(await esperar(".grade-acoes .carta-acao")), "habilidades viram cartas");
    conferir(!!(await page.$(".voltar-carta")), "a carta de Voltar fica junto das habilidades");
    const bola = await page.$('.carta-acao:has-text("Bola de Fogo")');
    conferir(!!bola, "a Bola de Fogo está entre as cartas");
    await bola.click();
    conferir(!!(await esperar(".ef.fam-fogo", 15000)), "o alvo fica em chamas");
    // termina a luta atacando
    for (let k = 0; k < 120; k++) {
      if (!(await page.evaluate(() => document.body.classList.contains("em-combate")))) break;
      const b = await page.$(".acoes-combate .escolha");
      if (b) await b.click().catch(() => {});
      const c = await page.$("#prompt .continuar");
      if (c) await c.click().catch(() => {});
      await page.waitForTimeout(250);
    }
    conferir(!(await page.evaluate(() => document.body.classList.contains("em-combate"))), "a luta termina");
    conferir(await page.evaluate(() => { const d = document.getElementById("dica-item"); return !d || d.hidden; }),
      "nenhuma dica fica presa depois da luta");
    conferir(!!(await esperar(".rastro-contrato.cacavel")), "o contrato do lugar oferece seguir os rastros");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioTitulo(browser) {
  console.log("cenário: título e carregar save");
  const { proc, url } = await subir("titulo");
  const { page, erros, esperar } = await abrir(browser, url);
  try {
    conferir(!!(await esperar('#prompt .escolha:has-text("Carregar")')), "o menu principal oferece carregar");
    await (await page.$('#prompt .escolha:has-text("Carregar")')).click();
    await (await esperar('#prompt .escolha:has-text("jean")')).click();
    conferir(!!(await esperar(".atalhos .atalho")), "o save carrega e o lugar aparece com a doca de atalhos");
    conferir((await page.$$(".atalhos .doca-sep")).length >= 1, "a doca separa os atalhos em grupos");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

let browser;
try {
  browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
} catch (e) {
  console.log("PULAR: não foi possível abrir o navegador (" + String(e).split("\n")[0] + ")");
  process.exit(77);
}
try {
  await cenarioCombate(browser);
  await cenarioTitulo(browser);
} catch (e) {
  falhas.push(String(e));
  console.log("ERRO", e);
} finally {
  await browser.close();
}
console.log(falhas.length ? `${falhas.length} falha(s)` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
