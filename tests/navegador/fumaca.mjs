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
    conferir(await page.evaluate(() => {
      Batalha.balao("odete", "Sister Odette", "Odette ergue o símbolo. \"Perdoa, mas vai doer.\"");
      const b = document.querySelector(".balao").getBoundingClientRect();
      const outros = [...document.querySelectorAll('#arena .carta:not([data-cid="odete"]), #roda > *')].map((o) => o.getBoundingClientRect());
      document.querySelectorAll(".balao").forEach((x) => x.remove());
      return outros.every((o) => b.right <= o.left || b.left >= o.right || b.bottom <= o.top || b.top >= o.bottom);
    }), "o balão de fala da comitiva não cobre outra carta nem as ações");
    // Pular no meio do golpe final solta a câmera lenta na hora (antes, a arena seguia lenta e de perto até a luta
    // seguinte).
    conferir(await page.evaluate(async () => {
      const arena = document.getElementById("arena"), alvo = arena.querySelector(".carta.inimigo"), m = { final: true };
      await Sensacao.antesDoGolpe(m, arena, alvo);
      const lenta = arena.classList.contains("foco-final");
      pular = true;
      await Sensacao.golpe(m, arena, alvo);
      pular = false;
      return lenta && !arena.classList.contains("foco-final") && arena.getAnimations({ subtree: true }).every((a) => a.playbackRate === 1);
    }), "pular no meio do golpe final solta a câmera lenta");
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
    // O palco não pula: o efeito novo aumenta a carta, e as cartas e a arena vão ao lugar novo devagar (batalha.js).
    // Mede o lugar de layout (sem os avanços dos golpes, que são de propósito), quadro a quadro.
    await page.evaluate(() => {
      window.__palco = { carta: 0, arena: 0 }; let ant = null; const fim = performance.now() + 2500;
      const passo = () => {
        const a = document.getElementById("arena"); const agora = { h: a.offsetHeight, c: {} };
        a.querySelectorAll(".carta").forEach((c) => { agora.c[c.dataset.uid] = c.offsetTop; });
        if (ant) {
          window.__palco.arena = Math.max(window.__palco.arena, Math.abs(agora.h - ant.h));
          for (const u in agora.c) if (u in ant.c) window.__palco.carta = Math.max(window.__palco.carta, Math.abs(agora.c[u] - ant.c[u]));
        }
        ant = agora;
        if (performance.now() < fim) requestAnimationFrame(passo);
      };
      requestAnimationFrame(passo);
    });
    await (await esperar('.carta.alvejavel:has-text("Javali")')).click();
    conferir(!!(await esperar(".ef.fam-fogo", 15000)), "clicar no inimigo dispara: o alvo fica em chamas");
    await page.waitForTimeout(2600);
    const palco = await page.evaluate(() => window.__palco);
    conferir(palco.carta <= 12 && palco.arena <= 16, `o efeito novo não faz o palco pular (maior passo num quadro: carta ${palco.carta}px, arena ${palco.arena}px)`);
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
    // O espólio fica até o Continuar (antes sumia sozinho, e o clique de adiantar o pulava sem ver).
    const continuarEspolio = await esperar(".festa-espolio .continuar", 8000);
    await page.waitForTimeout(1200);
    conferir(!!continuarEspolio && !!(await page.$(".festa-espolio")), "o espólio espera o Continuar");
    if (continuarEspolio) await continuarEspolio.click().catch(() => {});
    for (let t = 0; t < 20 && (await page.$(".festa-espolio")); t++) await page.waitForTimeout(100);
    // A luta pode deixar um item (o saque é sorteado): a janela dele vem logo depois do espólio.
    const guardar = await esperar('#sobre-achado .botao-janela:not(.reserva):has-text("Guardar")', 8000);
    if (guardar) { await guardar.click(); for (let t = 0; t < 30 && (await page.$("#sobre-achado")); t++) await page.waitForTimeout(100); }
    conferir(await page.evaluate(() => document.getElementById("vista").parentElement.id === "cena"),
      "a paisagem sai da arena e volta para o topo da cena, fora da área que rola");
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
    // Espaço de leitura (numa tela de notebook): a tela de menu abre no topo e sem a arte; título e Voltar ficam numa
    // barra fora da área que rola; a doca cabe numa linha; o painel do mundo continua à vista.
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.waitForTimeout(300);
    const layout = await page.evaluate(() => {
      const fundos = [...document.querySelectorAll("#doca .atalho")].map((b) => b.getBoundingClientRect().bottom);
      return { topo: document.getElementById("pagina").scrollTop, voltar: !!document.querySelector("#barra-tela .voltar-seta"),
        voltarNaPagina: !!document.querySelector("#pagina .voltar-seta"), arte: getComputedStyle(document.getElementById("vista")).display,
        docaAltura: Math.max(...fundos) - Math.min(...fundos), mundo: getComputedStyle(document.getElementById("mundo")).display };
    });
    conferir(layout.topo === 0, `o Inventário abre no topo da página (${layout.topo})`);
    conferir(layout.voltar && !layout.voltarNaPagina, "o Voltar fica na barra do topo, fora da área que rola");
    conferir(layout.arte === "none", "a tela de menu não mostra a arte do lugar");
    conferir(layout.docaAltura < 8, `a doca cabe numa linha só (${Math.round(layout.docaAltura)})`);
    conferir(layout.mundo !== "none", "em 1280 px o painel do mundo continua à vista");
    await page.setViewportSize({ width: 1500, height: 950 });
    await (await page.$('#doca .atalho[data-rotulo="Bestiário"]')).click();
    conferir(await ate(/Bestiário/), "do Inventário, o atalho Bestiário abre o Bestiário direto");
    await page.waitForTimeout(300);
    await page.keyboard.press("d");
    conferir(await ate(/Diário/), "a tecla D também troca de tela de dentro de outra");
    await page.waitForTimeout(300);
    await (await page.$('#doca .atalho[data-rotulo="Diário"]')).click();
    conferir(!!(await esperar('#prompt .escolha:has-text("Viajar"), #predios .predio[data-predio="estrada"]')), "clicar no atalho da tela aberta volta ao lugar");
    // O histórico é o diário da jornada: abrir telas pela doca e voltar não deixa rastro, nem repete o lugar.
    const hist = await page.$$eval("#historico-lista > p", (ps) => ps.map((p) => p.textContent));
    conferir(!hist.some((t) => /^› (Voltar|Personagem|Bestiário|Diário|Fechar)/.test(t) || /^(Jean|Bestiário|Diário)$/.test(t)),
      "telas da doca e o Voltar não entram no histórico");
    const lugar = await page.evaluate(() => document.querySelector("#cena-cab .cena-titulo").textContent);
    const vezes = hist.filter((t) => t === lugar).length;
    conferir(vezes === 1, `o nome do lugar aparece uma vez só no histórico (${lugar}: ${vezes})`);
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
  // A moldura do item achado, quadro a quadro, da revelação até uns quadros depois de os botões chegarem.
  await page.evaluate(() => {
    window.__moldura = new Set(); let depois = 0;
    const passo = () => {
      const j = document.querySelector("#sobre-achado .janela-achado");
      if (j) { const r = j.getBoundingClientRect(); window.__moldura.add(`${Math.round(r.width)}x${Math.round(r.height)} em ${Math.round(r.left)},${Math.round(r.top)}`); }
      if (document.querySelector("#sobre-achado .botao-janela:not(.reserva)")) depois++;
      if (depois < 20) requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  });
  try {
    conferir(!!(await esperar("#sobre-achado .achado-cartao.novo")), "o item encontrado aparece como cartão, numa janela própria");
    conferir(!!(await page.$("#sobre-achado .achado-cartao.atual")), "o item que você usa aparece ao lado");
    conferir(!(await page.$("#texto .tela.achado")), "o cartão do item não fica no log");
    conferir(!(await page.$('#sobre-achado .botao-janela:not(.reserva):has-text("Deixar para trás")')), "sem 'deixar para trás' com a mochila livre");
    const guardar = await esperar('#sobre-achado .botao-janela:not(.reserva):has-text("Guardar")');
    await page.waitForTimeout(500);
    const molduras = await page.evaluate(() => [...window.__moldura]);
    conferir(molduras.length === 1, `a moldura do item fica do mesmo tamanho da revelação aos botões (${molduras.join(" | ")})`);
    await guardar.click();
    for (let t = 0; t < 30 && (await page.$("#sobre-achado")); t++) await page.waitForTimeout(100);
    conferir(!(await page.$("#sobre-achado")), "guardar fecha a janela do item");
    const aceitar = await esperar("[data-aceitar]");
    // Cartazes do mural com a mesma altura e o botão no pé: três cliques seguidos, sem mexer o mouse, pegam os três.
    // (Medidos sem o mouse em cima: o cartaz sob o mouse se endireita e sobe.)
    await page.mouse.move(4, 400);
    await page.waitForTimeout(250);
    const fundos = await page.$$eval(".mural .quadro [data-aceitar]", (bs) => bs.map((b) => Math.round(b.getBoundingClientRect().bottom)));
    conferir(fundos.length < 2 || Math.max(...fundos) - Math.min(...fundos) <= 4, `os botões de aceitar ficam na mesma linha (${fundos.join(", ")})`);
    await page.evaluate(() => { const p = document.getElementById("pagina"); p.scrollTop = p.scrollHeight; });
    await page.waitForTimeout(300);
    const antes = await page.evaluate(() => document.getElementById("pagina").scrollTop);
    await aceitar.evaluate((b) => b.click());  // clique sem o "rolar até o botão" do Playwright
    await esperar(".contrato.recem");
    await page.waitForTimeout(400);
    const depois = await page.evaluate(() => document.getElementById("pagina").scrollTop);
    conferir(Math.abs(depois - antes) < 4, `aceitar um contrato não pula a página (${antes} → ${depois})`);
    // Abandonar pergunta numa janela por cima (antes ficava no pé da página, esquecida); Esc é "não".
    const meus = () => page.$$eval("[data-abandonar]", (x) => x.length);
    const tinha = await meus();
    await (await esperar("[data-abandonar]")).click();
    conferir(!!(await esperar("#janela-confirmar .botao-janela.perigo")), "abandonar um contrato pergunta numa janela própria");
    await page.keyboard.press("Escape");
    for (let t = 0; t < 20 && (await page.$("#janela-confirmar")); t++) await page.waitForTimeout(100);
    await page.waitForTimeout(400);
    conferir(!(await page.$("#janela-confirmar")) && (await meus()) === tinha, "Esc fecha a janela e o contrato fica");
    await page.keyboard.press("Escape");
    // Na vila, os serviços estão nos prédios da paisagem: a taverna abre as opções dela, e Esc volta à vila.
    const mercado = await esperar('#predios .predio[data-predio="mercado"]');
    conferir(!(await page.$('#prompt .escolha:has-text("Mercado")')), "na vila, os serviços ficam nos prédios, não na lista");
    await (await page.$('#predios .predio[data-predio="taverna"]')).click();
    conferir(!!(await esperar("#prompt .voltar-vila", 3000)) && !!(await page.$('#prompt .servico:has-text("Dormir")')), "a taverna mostra as opções dela e o Voltar à vila");
    await page.keyboard.press("Escape");
    conferir(!!(await esperar('#predios:not(.focado) .predio[data-predio="mercado"]', 3000)) && !(await page.$("#prompt .voltar-vila")), "Esc sai da taverna e volta à vila");
    // Uma tela da doca (o bestiário) por cima da vila: os balões dos prédios saem com a paisagem e voltam depois.
    await page.locator('#doca button:has-text("Bestiário")').first().click();
    await esperar('#barra-tela .cena-titulo:has-text("Bestiário")', 3000);
    await page.waitForTimeout(300);
    conferir(await page.evaluate(() => { const p = document.getElementById("predios"); return p.hidden || !p.querySelector(".predio"); }),
      "no bestiário, os balões dos prédios da vila não ficam na tela");
    await (await esperar("#prompt .continuar", 3000))?.click();
    conferir(!!(await esperar('#predios:not(.focado) .predio[data-predio="mercado"]', 3000)), "saindo do bestiário, a vila volta com os prédios");
    await page.waitForTimeout(300);
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
    // O balão com o nome também entra no prédio (antes, só o desenho do prédio aceitava o clique).
    await (await esperar('#predios .predio[data-predio="mercado"] .balao-nome') || mercado).click();
    const mais = await esperar('[data-comprar="tocha"] [data-q="1"]');
    conferir(!!mais, "clicar no balão com o nome do prédio entra nele");
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
    // Clique num item da mochila vende na hora (sem menu), não sai do mercado, e o vendido fica para recomprar.
    const ouro = () => page.evaluate(() => App.estado.heroi.ouro);
    const antesVenda = await ouro();
    await (await page.$("[data-mochila-loja]")).click();
    for (let k = 0; k < 30 && (await ouro()) === antesVenda; k++) await page.waitForTimeout(100);
    conferir((await ouro()) > antesVenda && !(await page.$(".menu-item")), "clique vende o item da mochila na hora");
    conferir(!!(await esperar("[data-comprar]")), "vender não tira você do mercado");
    const recomprar = await esperar("[data-recomprar]", 3000);
    conferir(!!recomprar, "o item vendido aparece em \"Vendidos agora\"");
    if (recomprar) {
      await recomprar.click();
      for (let k = 0; k < 30 && (await ouro()) !== antesVenda; k++) await page.waitForTimeout(100);
      conferir((await ouro()) === antesVenda, "recomprar devolve o item pelo mesmo preço");
    }
    // O templo: depois de cuidar de alguém, o balcão continua aberto, com o ouro de agora e só quem ainda precisa.
    await page.keyboard.press("Escape");  // sai do mercado
    const templo = await esperar('#predios .predio[data-predio="templo"]', 8000);
    if (templo) await templo.click();
    const servicos = () => page.$$eval("#prompt .balcao-predio .servico", (bs) => bs.length);
    const naFila = (await esperar("#prompt .balcao-predio .servico", 8000)) ? await servicos() : 0;
    const ouroAntes = await ouro();
    if (naFila) await (await page.$("#prompt .balcao-predio .servico:not(.caro)")).click();
    let restam = naFila;
    // entre a resposta e a pergunta seguinte o prompt fica vazio um instante: espera o balcão voltar
    for (let k = 0; k < 50 && (restam === naFila || restam < 0); k++) { await page.waitForTimeout(100); restam = (await page.$("#prompt .balcao-predio")) ? await servicos() : -1; }
    conferir(naFila >= 1 && restam === naFila - 1 && (await ouro()) < ouroAntes,
      `depois de cuidar de alguém, o templo continua no balcão, com menos gente e menos ouro (${naFila} → ${restam})`);
    const volta = await page.$("#prompt .balcao-predio .voltar-vila");
    if (volta) await volta.click();
    conferir(!!(await esperar('#predios .predio[data-predio="mercado"]', 5000)) && !(await page.$("#prompt .balcao-predio")),
      "Voltar à vila sai do balcão do templo");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioCampanha(browser) {
  console.log("cenário: campanha (protótipo do Vale do Turvo)");
  const { proc, url } = await subir("campanha");
  const { page, erros, esperar } = await abrir(browser, url);
  try {
    conferir(!!(await esperar('#prompt .escolha:has-text("Campanha")')) && !!(await page.$('#prompt .escolha:has-text("Novo jogo")')),
      "o título oferece o novo jogo e a campanha");
    await (await page.$('#prompt .escolha:has-text("Carregar")')).click();
    const maria = await esperar('.save-cartao:has-text("Maria")');
    conferir(!!maria && /Vale do Turvo · resgate/.test(await maria.textContent()), "o save da campanha diz a região e o modo");
    const jean = await page.$('.save-cartao:has-text("Jean")');
    conferir(!!jean && /brando/.test(await jean.textContent()) && !/Vale do Turvo/.test(await jean.textContent()),
      "o save do mundo gerado continua como era");
    await (await page.$('#prompt .escolha:has-text("Voltar")')).click();
    await (await esperar('#prompt .escolha:has-text("Campanha")')).click();
    // Sem `esperar` aqui: ele clica em qualquer .continuar, e o "Confirmar" do nome também é um. Se o botão chegasse
    // um instante antes do campo, o teste confirmava o nome padrão sozinho (a falha que aparecia às vezes).
    await (await page.waitForSelector(".entrada-texto input", { timeout: 20000 })).fill("Ana");
    await page.keyboard.press("Enter");
    await (await esperar('#prompt .escolha:has-text("Arqueiro")')).click();
    const resgate = await esperar('#prompt .escolha:has-text("Resgate")');
    conferir(!!resgate && !!(await page.$('#prompt .escolha:has-text("Hardcore")')), "a criação pergunta o modo: resgate ou hardcore");
    await resgate.click();
    conferir(!!(await esperar('#texto :text("Resgate: se você cair")', 8000)), "o prólogo diz o modo escolhido");
    conferir(!!(await esperar('#cena-cab .cena-titulo:has-text("Vau do Turvo")')) && !!(await esperar('#predios .predio[data-predio="estrada"]')),
      "a campanha começa no Vau do Turvo, com a vila desenhada");
    conferir(await page.evaluate(() => estado.mapa.nos.map((n) => n.nome).sort().join(",")) === "Bosque do Moinho,Charco dos Juncos,Estrada de Varn,Vau do Turvo",
      "o mapa mostra a vila e as estradas dela; a capela ainda está na névoa");
    await (await page.$('#predios .predio[data-predio="estrada"]')).click();
    const varn = await esperar('#prompt .escolha:has-text("Estrada de Varn")');
    conferir(!!varn && /fechada/.test(await varn.textContent()) && !/Nv\./.test(await varn.textContent()), "a Estrada de Varn aparece como saída fechada");
    await varn.click();
    conferir(!!(await esperar('#texto :text("não leva a lugar nenhum")', 8000)), "escolher a saída fechada explica e não viaja");
    conferir(!!(await esperar('#predios .predio[data-predio="estrada"]')) && (await page.evaluate(() => estado.local.nome)) === "Vau do Turvo",
      "depois do aviso, continua na vila");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioBaus(browser) {
  console.log("cenário: baús abertos juntos");
  const { proc, url } = await subir("baus");
  const { page, erros, esperar } = await abrir(browser, url);
  await page.evaluate(() => {  // quantos quadros de espólio aparecem, e a moldura de cada item achado, quadro a quadro
    window.__festas = 0; window.__janelas = {};
    new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => { if (n.nodeType === 1 && (n.matches(".festa-espolio") || n.querySelector(".festa-espolio"))) window.__festas++; })))
      .observe(document.body, { childList: true, subtree: true });
    const passo = () => {
      const j = document.querySelector("#sobre-achado:not(.saindo) .janela-achado");
      if (j) { const r = j.getBoundingClientRect(), n = j.querySelector(".achado-cartao.novo b").textContent;
        (window.__janelas[n] = window.__janelas[n] || new Set()).add(`${Math.round(r.width)}x${Math.round(r.height)}@${Math.round(r.left)},${Math.round(r.top)}`); }
      requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  });
  try {
    const pilha = await esperar('#heroi [data-bolsa="bau"]');
    await page.waitForTimeout(600);
    await pilha.click(); await pilha.click().catch(() => {});  // dois cliques rápidos na pilha
    const continuar = await esperar(".festa-espolio .continuar", 20000);
    const resumo = await page.evaluate(() => ({ rotulo: document.querySelector(".festa-espolio .rotulo-festa").textContent,
      equips: [...document.querySelectorAll(".festa-espolio .equip-espolio")].map((x) => x.textContent) }));
    conferir(!!continuar && resumo.rotulo === "Baús ×3", `a pilha abre num quadro só: ${resumo.rotulo}`);
    conferir(resumo.equips.length >= 2, `o resumo lista os equipamentos (${resumo.equips.join(", ")})`);
    await page.waitForTimeout(1000);  // depois da guarda do espólio
    for (let t = 0; t < 20 && (await page.$(".festa-espolio .continuar")); t++) { await page.click(".festa-espolio .continuar").catch(() => {}); await page.waitForTimeout(300); }
    const vistos = [];
    for (;;) {
      const guardar = await esperar('#sobre-achado .botao-janela:not(.reserva):has-text("Guardar")', 6000);
      if (!guardar) break;
      vistos.push(await page.$eval("#sobre-achado .achado-cartao.novo b", (b) => b.textContent));
      await page.waitForTimeout(400);
      await guardar.click();
      for (let t = 0; t < 40 && (await page.$("#sobre-achado:not(.saindo)")); t++) await page.waitForTimeout(100);
    }
    conferir(vistos.join("|") === resumo.equips.join("|"), "depois do resumo, cada equipamento vem na janela dele, na mesma ordem");
    await page.waitForTimeout(600);
    const fim = await page.evaluate(() => ({ festas: window.__festas, baus: (App.estado.heroi.bolsa.find((b) => b.id === "bau") || {}).qtd || 0,
      instaveis: Object.entries(window.__janelas).filter(([, s]) => s.size !== 1).map(([n]) => n) }));
    conferir(fim.festas === 1 && fim.baus === 0, `um quadro de espólio só e a pilha vazia (${fim.festas} quadro, ${fim.baus} baús)`);
    conferir(!fim.instaveis.length, "a moldura de cada item fica estável" + (fim.instaveis.length ? `: ${fim.instaveis.join(", ")}` : ""));
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
  await cenarioCampanha(browser);
  await cenarioBaus(browser);
} catch (e) {
  falhas.push(String(e));
  console.log("ERRO", e);
} finally {
  await browser.close();
}
console.log(falhas.length ? `${falhas.length} falha(s)` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
