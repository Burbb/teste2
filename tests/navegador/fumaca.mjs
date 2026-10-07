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
    conferir(!!(await esperar("#roda .roda-botao")), "na sua vez, as ações surgem em volta da sua carta");
    conferir(await page.evaluate(() => document.querySelector('#batalha .carta[data-uid="j"]').classList.contains("foco")), "sua carta vem para a frente");
    conferir((await page.$$("#batalha .carta")).length >= 4, "a arena mostra herói, comitiva e inimigos");
    await page.keyboard.press("p");
    conferir(!!(await esperar("#sobre-grimorio:not([hidden]) .g-faixa")), "o Grimório abre com P e mostra o dano");
    await page.keyboard.press("Escape");
    conferir(await page.evaluate(() => document.getElementById("sobre-grimorio").hidden), "Esc fecha o Grimório");
    await (await page.$('.roda-botao[data-slot="habilidades"]')).click();
    conferir(!!(await esperar('.roda-janela .rj-linha[data-hab="bola_fogo"]')), "Habilidades abre a janelinha com nome e custo");
    await page.keyboard.press("Escape");
    conferir(!(await page.$(".roda-janela")) && !!(await page.$("#roda .roda-botao")), "Esc fecha a janelinha e as ações continuam");
    await (await page.$('.roda-botao[data-slot="itens"]')).click();
    conferir(!!(await esperar('.roda-janela .rj-linha[data-slot="item"]')), "Itens abre a janelinha com os itens");
    await (await page.$(".rj-fechar")).click();
    conferir(!!(await esperar('#roda .roda-botao[data-slot="atacar"]')), "fechar os itens devolve as ações");
    await (await page.$('.roda-botao[data-slot="habilidades"]')).click();
    await (await esperar('.rj-linha[data-hab="bola_fogo"]')).click();
    conferir(!!(await esperar(".carta.alvejavel")), "a habilidade acende os alvos");
    await (await esperar("#roda .mira-voltar")).click();
    conferir(!!(await esperar('#roda .roda-botao[data-slot="atacar"]')), "Voltar na escolha do alvo devolve as ações");
    await (await page.$('.roda-botao[data-slot="habilidades"]')).click();
    await (await esperar('.rj-linha[data-hab="bola_fogo"]')).click();
    await (await esperar('.carta.alvejavel:has-text("Javali")')).click();
    conferir(!!(await esperar(".ef.fam-fogo", 15000)), "clicar no inimigo dispara: o alvo fica em chamas");
    // termina a luta atacando (clicando no alvo quando houver mais de um)
    for (let k = 0; k < 160; k++) {
      if (!(await page.evaluate(() => document.body.classList.contains("em-combate")))) break;
      const b = await page.$('#roda .roda-botao[data-slot="atacar"]');
      if (b) await b.click().catch(() => {});
      const alvo = await page.$(".carta.alvejavel");
      if (alvo) await alvo.click().catch(() => {});
      const c = await page.$("#prompt .continuar");
      if (c) await c.click().catch(() => {});
      await page.waitForTimeout(250);
    }
    conferir(!(await page.evaluate(() => document.body.classList.contains("em-combate"))), "a luta termina");
    await page.mouse.move(4, 400);  // o HUD volta ao topo: o mouse sai de cima dele para a dica ter motivo de fechar
    await page.waitForTimeout(400);
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
    conferir(!(await page.$('#prompt .escolha:has-text("Como jogar")')), "o menu não tem mais Como jogar");
    const cartao = await esperar('.save-cartao:has-text("Jean")');
    conferir(!!cartao, "os saves aparecem como cartões");
    conferir(!!(await page.$('#prompt .escolha:has-text("Voltar")')), "dá para voltar da lista de saves");
    await cartao.click();
    conferir(!!(await esperar(".atalhos .atalho")), "o save carrega e o lugar aparece com a doca de atalhos");
    conferir((await page.$$(".atalhos .doca-sep")).length >= 1, "a doca separa os atalhos em grupos");
    conferir(!(await page.$("#texto .eco")), "entrar no save não deixa ecos do menu na página");
    // A doca continua viva dentro das telas que ela abre: do Inventário direto para o Bestiário, sem Voltar.
    const cab = () => page.evaluate(() => document.getElementById("cena-cab").textContent);
    const ate = async (re) => { for (let k = 0; k < 40 && !re.test(await cab()); k++) await page.waitForTimeout(100); return re.test(await cab()); };
    await (await page.$('#doca .atalho[data-rotulo="Inventário"]')).click();
    conferir(await ate(/Jean/), "o atalho Inventário abre a ficha");
    await page.waitForTimeout(400);
    conferir(!(await page.$("#doca.inativa")), "dentro do Inventário a doca segue acesa");
    conferir(!!(await page.$('#doca .atalho.atual[data-rotulo="Inventário"]')), "a doca marca a tela aberta");
    await (await page.$('#doca .atalho[data-rotulo="Bestiário"]')).click();
    conferir(await ate(/Bestiário/), "do Inventário, o atalho Bestiário abre o Bestiário direto");
    await page.waitForTimeout(300);
    await page.keyboard.press("d");
    conferir(await ate(/Diário/), "a tecla D também troca de tela de dentro de outra");
    await page.waitForTimeout(300);
    await (await page.$('#doca .atalho[data-rotulo="Diário"]')).click();
    conferir(!!(await esperar('#prompt .escolha:has-text("Viajar")')), "clicar no atalho da tela aberta volta ao lugar");
    await (await page.$('#doca .atalho[data-rotulo="Mapa"]')).click();
    conferir(await page.evaluate(() => !document.getElementById("sobre-mapa").hidden), "o atalho Mapa abre o mapa por cima, sem sair do lugar");
    await page.keyboard.press("Escape");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioVila(browser) {
  console.log("cenário: saque, mural e mercado");
  const { proc, url } = await subir("vila");
  const { page, erros, esperar } = await abrir(browser, url);
  try {
    conferir(!!(await esperar(".achado-cartao.novo")), "o item encontrado aparece como cartão");
    conferir(!!(await page.$(".achado-cartao.atual")), "o item que você usa aparece ao lado");
    conferir(!(await page.$('#prompt .escolha:has-text("Deixar para trás")')), "sem 'deixar para trás' com a mochila livre");
    await (await esperar('#prompt .escolha:has-text("Guardar")')).click();
    const aceitar = await esperar("[data-aceitar]");
    await page.evaluate(() => { const p = document.getElementById("pagina"); p.scrollTop = p.scrollHeight; });
    await page.waitForTimeout(300);
    const antes = await page.evaluate(() => document.getElementById("pagina").scrollTop);
    await aceitar.evaluate((b) => b.click());  // clique sem o "rolar até o botão" do Playwright
    await esperar(".contrato.recem");
    await page.waitForTimeout(400);
    const depois = await page.evaluate(() => document.getElementById("pagina").scrollTop);
    conferir(Math.abs(depois - antes) < 4, `aceitar um contrato não pula a página (${antes} → ${depois})`);
    await page.keyboard.press("Escape");
    const mercado = await esperar('#prompt .escolha:has-text("Mercado")');
    const vida = () => page.evaluate(() => App.estado.heroi.hp);
    const antesPocao = await vida();
    let abriu = 0;
    for (let k = 0; k < 3; k++) {  // cliques seguidos: o menu "em quem usar" abre toda vez (antes, um sim e um não)
      await (await page.$('#heroi [data-bolsa="pocao_vida"]')).click();
      await page.waitForTimeout(150);
      if (await page.$(".menu-uso")) abriu++;
    }
    conferir(abriu === 3, `clicar na poção sempre abre o "em quem usar" (${abriu}/3)`);
    await (await page.$('.menu-uso button[data-em=""]')).click();
    for (let k = 0; k < 30 && (await vida()) === antesPocao; k++) await page.waitForTimeout(100);
    conferir((await vida()) > antesPocao, "a poção da bolsa lateral se usa com um clique");
    await page.waitForTimeout(300);
    await (await esperar('#prompt .escolha:has-text("Mercado")') || mercado).click();
    const mais = await esperar('[data-comprar="tocha"] [data-q="1"]');
    const qtd = () => page.evaluate(() => Number(document.querySelector('[data-comprar="tocha"] .qtd-ctrl b').textContent));
    await mais.hover(); await page.mouse.down();
    await page.waitForTimeout(600);
    await page.evaluate(() => document.querySelector('[data-comprar="bandagem"]').click());  // a loja se redesenha com o botão apertado
    await page.waitForTimeout(500);
    const parado = await qtd(); await page.waitForTimeout(500);
    await page.mouse.up();
    conferir(parado === (await qtd()), "segurar + não segue somando depois que a loja se redesenha");
    await (await page.$('[data-comprar="tocha"] [data-q="-1"]')).click();
    await page.waitForTimeout(300);
    conferir((await qtd()) === parado - 1, "o − desce a quantidade");
    // Botão direito num item da mochila vende na hora (sem menu) e não sai do mercado.
    const ouro = () => page.evaluate(() => App.estado.heroi.ouro);
    const antesVenda = await ouro();
    await (await page.$("[data-mochila-loja]")).click({ button: "right" });
    for (let k = 0; k < 30 && (await ouro()) === antesVenda; k++) await page.waitForTimeout(100);
    conferir((await ouro()) > antesVenda && !(await page.$(".menu-item")), "botão direito vende o item da mochila na hora");
    conferir(!!(await esperar("[data-comprar]")), "o botão direito não tira você do mercado");
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
  await cenarioVila(browser);
} catch (e) {
  falhas.push(String(e));
  console.log("ERRO", e);
} finally {
  await browser.close();
}
console.log(falhas.length ? `${falhas.length} falha(s)` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
