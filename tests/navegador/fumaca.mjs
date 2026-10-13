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

async function subir(cenario, ambiente = {}) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario], { cwd: RAIZ, env: { VELOCIDADE: "rapido", ...process.env, ...ambiente, PYTHONPATH: RAIZ } });
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
      // O Continuar de uma cena de missão não aceita toque na rajada: espera a guarda e toca uma vez.
      if (c && (await c.evaluate((b) => b.classList.contains("confirmar")).catch(() => false))) {
        // Espera a guarda olhando: o que se esperava pode chegar nela, e aí a cena dele não é fechada (nem a guarda gasta).
        for (let k = 0; k < 7; k++) {
          await page.waitForTimeout(100);
          const achou = await page.$(sel);
          if (achou) return achou;
        }
      }
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
    // As abas: Suprimentos é a inicial; as setas trocam (sem falar com o motor: nada de tempo, estoque ou sorteio).
    conferir(await page.evaluate(() => document.querySelector('.loja-aba[aria-selected="true"]').dataset.aba) === "suprimentos",
      "o mercado abre na aba Suprimentos");
    const diaAntes = await page.evaluate(() => App.estado.mundo.dia + "|" + App.estado.mundo.periodo);
    await page.focus('.loja-aba[data-aba="suprimentos"]');
    await page.keyboard.press("ArrowRight");
    conferir(await page.evaluate(() => !document.querySelector('[data-painel="equipamentos"]').hidden && document.activeElement.dataset.aba === "equipamentos"),
      "a seta leva o foco e a lista para a aba Equipamentos");
    await page.click('.loja-aba[data-aba="vender"]');
    conferir(await page.evaluate((d) => App.estado.mundo.dia + "|" + App.estado.mundo.periodo === d, diaAntes) && !(await page.evaluate(() => processando)),
      "trocar de aba não passa tempo nem espera o motor");
    // A aba Vender é a grade da mochila: todos os espaços (os vazios fora do Tab), "Mochila N/12" e nada de recompra
    // antes da primeira venda.
    const grade = await page.evaluate(() => {
      const p = document.querySelector('[data-painel="vender"]');
      return { celulas: p.querySelectorAll(".mochila-grade:not(.recompra) .celula").length, itens: p.querySelectorAll("[data-mochila-loja]").length,
        vaziosNoTab: [...p.querySelectorAll(".celula.vazia")].filter((e) => e.tabIndex >= 0).length, mochila: App.estado.heroi.mochila.length,
        rotulo: p.querySelector(".loja-mochila").textContent.replace(/\s+/g, " ").trim(), recompra: !!p.querySelector(".loja-recompra"), velho: /Vendidos agora/.test(p.textContent) };
    });
    conferir(grade.celulas === 12 && grade.itens === grade.mochila && grade.vaziosNoTab === 0 && grade.rotulo === `Mochila ${grade.mochila}/12` && !grade.recompra && !grade.velho,
      `Vender: a grade com os 12 espaços, "Mochila N/12" e sem recompra antes de vender (${JSON.stringify(grade)})`);
    // Clique num item da mochila vende na hora (sem menu), não sai do mercado, e o vendido fica para recomprar.
    const ouro = () => page.evaluate(() => App.estado.heroi.ouro);
    const antesVenda = await ouro();
    await (await page.$("[data-mochila-loja]")).click();
    for (let k = 0; k < 30 && (await ouro()) === antesVenda; k++) await page.waitForTimeout(100);
    conferir((await ouro()) > antesVenda && !(await page.$(".menu-item")), "clique vende o item da mochila na hora");
    conferir(!!(await esperar("[data-comprar]")), "vender não tira você do mercado");
    let recomprar = await esperar("[data-recomprar]", 3000);
    conferir(!!recomprar && /Recomprar/i.test(await page.textContent(".loja-recompra h5")), "o item vendido aparece em \"Recomprar\"");
    conferir(await page.evaluate(() => document.querySelector('.loja-aba[aria-selected="true"]').dataset.aba) === "vender",
      "depois de vender, a aba Vender continua aberta");
    // Trocar de aba não encerra a recompra (ela vale até sair do mercado).
    await page.click('.loja-aba[data-aba="suprimentos"]');
    await page.click('.loja-aba[data-aba="vender"]');
    recomprar = await page.$("[data-recomprar]");
    if (recomprar) {
      await recomprar.click();
      for (let k = 0; k < 30 && (await ouro()) !== antesVenda; k++) await page.waitForTimeout(100);
      conferir((await ouro()) === antesVenda, "recomprar devolve o item pelo mesmo preço");
    }
    // O templo: depois de cuidar de alguém, o balcão continua aberto, com o ouro de agora e só quem ainda precisa.
    // Sai do mercado. O Esc só vale com a tela parada numa pergunta: dado enquanto o mercado ainda se redesenha (a
    // recompra acabou de chegar), ele só adianta o texto e a tela continua no mercado (era a falha intermitente).
    const telaParada = () => page.waitForFunction(() => !processando && pergunta, null, { timeout: 8000 }).catch(() => {});
    for (let k = 0; k < 3 && (await page.evaluate(() => tituloAtual)) === "Mercado"; k++) {
      await telaParada();
      await page.keyboard.press("Escape");
      await page.waitForTimeout(400);
    }
    const servicos = () => page.$$eval("#prompt .balcao-predio .servico", (bs) => bs.length);
    const templo = await esperar('#predios .predio[data-predio="templo"]', 8000);
    if (templo) await templo.click();
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
    const caixa = await page.$("#prompt .caixa-escolha input");
    conferir(!!caixa && (await caixa.isChecked()) && /Mostrar tutorial/.test(await page.textContent("#prompt .caixa-escolha")),
      "junto do modo, a caixa \"Mostrar tutorial\", marcada");
    await caixa.click();  // esta campanha segue sem orientações (a abertura é a mesma)
    await resgate.click();
    conferir(!!(await esperar('#texto :text("Resgate: se você cair")', 8000)), "o prólogo diz o modo escolhido");
    // A abertura da missão pede confirmação: o texto termina num Continuar e a página não vira sozinha.
    conferir(!!(await esperar('#cena-cab .cena-titulo:has-text("A Febre do Turvo")', 10000)), "a abertura da missão toca depois do prólogo");
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 20000 });
    await page.waitForTimeout(6500);  // mais que a leitura mais longa de uma página que vira sozinha (5,5 s)
    conferir(/A Febre do Turvo/.test(await page.textContent("#cena-cab .cena-titulo")) && !!(await page.$("#prompt .continuar.confirmar")),
      "a abertura fica aberta esperando o Continuar");
    // Depois, o pedido do taverneiro (a despensa), o mesmo com ou sem tutorial; "Agora não" deixa para depois.
    const agoraNao = await esperar('#prompt .escolha:has-text("Agora não")', 15000);
    conferir(!!agoraNao && !!(await page.$('#prompt .escolha:has-text("Descer à despensa")')) && !(await page.evaluate(() => estado.orientacao.ligado)),
      "a despensa é oferecida (sem tutorial, sem quadros)");
    await agoraNao.click();
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
    // A missão (E3): a abertura já tocou; o rastreador e a opção da vila mostram o primeiro passo.
    const objetivo = () => page.evaluate(() => (document.querySelector("#mundo .rastro-missao .rastro-objetivo") || {}).textContent || "");
    conferir(/fonte nova/.test(await objetivo()) && !!(await page.$('#prompt .escolha:has-text("Examinar a fonte nova")')),
      "a missão aparece no rastreador e o exame da fonte nova no menu da vila");
    const atalho = await esperar("#mundo .rastro-missao.cacavel", 5000);
    await page.evaluate(() => { velocidade = "instantaneo"; });  // o texto aparece todo de uma vez
    if (atalho) await atalho.click();
    conferir(!!(await esperar('#cena-cab .cena-titulo:has-text("A fonte nova")', 10000)), "o cartão da missão leva ao exame da fonte");
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 10000 });
    await page.waitForTimeout(1200);
    conferir(/A fonte nova/.test(await page.textContent("#cena-cab .cena-titulo")), "no instantâneo, o exame da fonte espera o Continuar");
    await page.keyboard.press("Enter");  // um Enter explícito continua na hora
    conferir(!!(await esperar('#predios .predio[data-predio="estrada"]', 20000)) && /Bosque do Moinho/.test(await objetivo())
      && !(await page.$('#prompt .escolha:has-text("Examinar a fonte nova")')), "depois do exame, o objetivo aponta o canal e o exame some");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioMissao(browser) {
  console.log("cenário: missão no Bosque do Moinho (o canal)");
  const { proc, url } = await subir("missao");
  const { page, erros, esperar } = await abrir(browser, url);
  const titulo = () => page.evaluate(() => (document.querySelector("#cena-cab .cena-titulo") || {}).textContent || "");
  const alvo = () => page.evaluate(() => (estado.missoes || []).map((m) => m.lugar).join(","));
  try {
    conferir(!!(await esperar('#prompt .escolha:has-text("Seguir a água e examinar o canal")')) && (await alvo()) === "Bosque do Moinho",
      "no bosque, na etapa do canal, a ação aparece e o marcador está aqui");
    await page.evaluate(() => { velocidade = "normal"; });
    await page.click('#prompt .escolha:has-text("Seguir a água e examinar o canal")');
    await page.waitForFunction(() => /O Canal do Moinho/.test(document.querySelector("#cena-cab .cena-titulo").textContent), null, { timeout: 10000 });
    await page.waitForTimeout(300);
    const correndo = await page.evaluate(() => processando);
    await page.keyboard.down("Enter");  // o Enter que adianta o texto, segurado: revela e para no Continuar
    for (let i = 0; i < 8; i++) { await page.evaluate(() => document.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", repeat: true, bubbles: true }))); await page.waitForTimeout(60); }
    await page.keyboard.up("Enter");
    await page.mouse.dblclick(700, 450);  // e um clique duplo na página, fora dos controles, não faz nada
    conferir(correndo && /O Canal do Moinho/.test(await titulo()) && !!(await page.$("#prompt .continuar.confirmar")),
      "adiantar o texto (clique duplo, Enter segurado) revela e para no Continuar, sem fechar a cena do canal");
    await page.waitForTimeout(6500);
    conferir(/O Canal do Moinho/.test(await titulo()), "deixada aberta, a cena do canal não fecha por tempo");
    await page.click("#prompt .continuar");
    conferir(!!(await esperar('#prompt .escolha:has-text("Explorar")')) && (await alvo()) === "Capela Afogada"
      && !(await page.$('#prompt .escolha:has-text("Seguir a água")')), "depois do Continuar, o objetivo e o marcador vão para a capela");
    await page.keyboard.press("d");
    const sabe = await esperar(".missao-recente", 10000);
    const descobertas = await page.$$eval(".missao-historico li li", (ls) => ls.map((l) => l.textContent).filter((t) => !/^Objetivo:/.test(t)));
    conferir(!!sabe && /Capela Afogada/.test(await page.textContent(".missao-recente")) && descobertas.length === 3,
      `o Diário mostra o mais recente (o canal entra na capela) e guarda as três descobertas no histórico (${descobertas.length})`);
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioRecarga(browser) {
  console.log("cenário: carregar um save e ver a tela inteira antes de qualquer ação");
  const { proc, url } = await subir("recarga");
  const { page, erros } = await abrir(browser, url);
  // O que precisa estar na tela no primeiro instante do lugar: herói, doca, mapa e (na campanha) a missão.
  const tela = () => page.evaluate(() => ({
    titulo: document.body.classList.contains("modo-titulo"), semHeroi: document.body.classList.contains("sem-heroi"),
    estado: !!estado, heroi: (document.querySelector("#heroi") || {}).textContent || "",
    doca: document.querySelectorAll("#doca .atalho").length, mapa: !!document.querySelector("#mundo #mapa-mini > *"),
    missao: (document.querySelector("#mundo .rastro-missao .rastro-objetivo") || {}).textContent || "",
    lugar: (document.querySelector("#mundo .local-nome") || {}).textContent || "", tempo: document.querySelector("#tempo").textContent }));
  const inteira = (t, nome) => !t.titulo && !t.semHeroi && t.estado && t.heroi.includes(nome) && t.doca >= 5 && t.mapa;
  const carregar = async (nome) => {
    await (await page.waitForSelector('#prompt .escolha:has-text("Carregar")', { timeout: 20000 })).click();
    await (await page.waitForSelector(`.save-cartao:has-text("${nome}")`)).click();
    await page.waitForSelector('#prompt .escolha:has-text("Viajar"), #predios .predio', { timeout: 20000 });
    return tela();  // logo que as opções aparecem, sem clicar em nada
  };
  const sairSalvando = async () => {
    await (await page.waitForSelector('#doca .atalho[data-rotulo="Sair"]')).click();
    await (await page.waitForSelector('#prompt .escolha:has-text("Salvar e sair")')).click();
    for (let t = 0; t < 60 && !(await page.$('#prompt .escolha:has-text("Carregar")')); t++) {
      const c = await page.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
      await page.waitForTimeout(200);
    }
  };
  try {
    let t = await carregar("Maria");
    conferir(inteira(t, "Maria") && /Capela Afogada/.test(t.missao) && t.lugar === "Bosque do Moinho" && /Dia 25 · Noite · Chuva/.test(t.tempo),
      `a campanha carregada aparece inteira: painéis, doca, mapa e missão (${t.lugar}, ${t.tempo})`);
    await sairSalvando();
    t = await carregar("Maria");
    conferir(inteira(t, "Maria") && /Capela Afogada/.test(t.missao) && t.lugar === "Bosque do Moinho",
      "salvar, sair e carregar o mesmo save: a tela volta inteira (antes, só o centro até a primeira ação)");
    await page.reload();
    await page.waitForSelector('#prompt .escolha:has-text("Viajar")', { timeout: 20000 });
    t = await tela();
    conferir(inteira(t, "Maria") && /Capela Afogada/.test(t.missao), "recarregar a página mantém a tela inteira");
    await sairSalvando();
    t = await carregar("Jean");
    conferir(inteira(t, "Jean") && !t.missao, "o save do mundo gerado também carrega inteiro, sem missão");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioCapela(browser) {
  console.log("cenário: dentro da Capela Afogada (a sacristia, e salvar e carregar lá dentro)");
  const { proc, url } = await subir("capela");
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const objetivo = () => page.evaluate(() => (estado.missoes || [])[0].objetivo);
  const baus = () => page.evaluate(() => (estado.heroi.bolsa.find((b) => b.id === "bau") || { qtd: 0 }).qtd);
  try {
    await page.waitForSelector(`${MENU}:has-text("Atravessar o salão alagado")`, { timeout: 20000 });
    conferir(/sacristia/.test(await objetivo()) && !!(await page.$("#mundo .rastro-missao")), "na capela, com o salão vencido: o passo seguinte é a sacristia");
    const antes = await baus();
    await page.click(`${MENU}:has-text("Atravessar o salão alagado")`);
    // a luta da sala: ataca até acabar; o espólio fecha com Continuar depois da guarda dele
    for (let k = 0; k < 400 && !(await page.$("#prompt .continuar.confirmar")); k++) {
      if (await page.evaluate(() => document.body.classList.contains("em-combate"))) {
        const b = await page.$('#roda .roda-botao[data-slot="atacar"]'); if (b) await b.click().catch(() => {});
        const alvo = await page.$(".carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
      }
      const f = await page.$(".festa-espolio .continuar"); if (f) { await page.waitForTimeout(1000); await f.click().catch(() => {}); }
      const achado = await page.$('#sobre-achado .botao-janela:not(.reserva)'); if (achado) await achado.click().catch(() => {});
      const fim = await page.$("#prompt .continuar:not(.confirmar)"); if (fim) await fim.click().catch(() => {});  // o fim da luta
      await page.waitForTimeout(250);
    }
    conferir(/A Sacristia/.test(await page.textContent("#cena-cab .cena-titulo")) && /Ilse/.test(await page.textContent("#texto")),
      "vencida a luta, a sacristia mostra o livro da capela, com Ilse, e espera o Continuar");
    const cartoes = await page.$$eval("#texto .novidade-missao", (cs) => cs.map((c) => c.textContent));
    conferir(cartoes.length === 1 && /Ilse/.test(cartoes[0]) && /Objetivo/.test(cartoes[0]) && /ossuário/.test(cartoes[0]),
      `um cartão só junta o que a sacristia mostrou e o objetivo novo (${cartoes.length})`);
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    await page.waitForSelector(`${MENU}:has-text("Descer ao ossuário")`, { timeout: 20000 });
    conferir(/ossuário/.test(await objetivo()) && !(await page.$(`${MENU}:has-text("Atravessar o salão")`)) && (await baus()) >= antes + 1,
      "o objetivo passa ao ossuário, a sacristia some do menu e o baú dela está na bolsa");
    const bausDepois = await baus();
    await (await page.waitForSelector('#doca .atalho[data-rotulo="Sair"]')).click();
    await (await page.waitForSelector(`${MENU}:has-text("Salvar e sair")`)).click();
    for (let t = 0; t < 60 && !(await page.$(`${MENU}:has-text("Carregar")`)); t++) {
      const c = await page.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
      await page.waitForTimeout(200);
    }
    await (await page.waitForSelector(`${MENU}:has-text("Carregar")`, { timeout: 20000 })).click();
    await (await page.waitForSelector(".save-cartao")).click();
    await page.waitForSelector(`${MENU}:has-text("Descer ao ossuário")`, { timeout: 20000 });
    conferir(!(await page.$(`${MENU}:has-text("Atravessar o salão")`)) && /ossuário/.test(await objetivo()) && (await baus()) === bausDepois
      && !!(await page.$("#doca .atalho")) && !(await page.evaluate(() => document.body.classList.contains("sem-heroi"))),
      "salvar, sair e carregar lá dentro: a sala vencida continua vencida, o baú não se repete e a tela vem inteira");
    conferir(await page.evaluate(() => document.querySelector("#pontos-cena").dataset.cena === "neutra" && /Sacristia/.test(document.querySelector("#cena-cab").textContent)),
      "carregado na sacristia: o fundo neutro no topo (sem arte de outra sala) e a sala no subtítulo");
    await page.keyboard.press("d");
    await page.waitForSelector(".missao-pistas", { timeout: 10000 });
    const diario = await page.textContent(".missao-diario");
    conferir(/Ilse/.test(diario) && /Sigilo do Turvo/.test(diario) && !/O que você já fez/.test(diario),
      "o Diário sabe de Ilse e do Sigilo, e ainda não tem nada feito (saber o nome não prepara o rito)");
    conferir(/Mais recente/.test(diario) && /Perguntas em aberto/.test(diario) && !/Vó Berta contou/.test(diario)
      && !!(await page.$(".missao-diario details.missao-historico:not([open])")),
      "o Diário mostra o mais recente e as perguntas em aberto, sem a receita do rito antes de Berta, e o histórico fechado");
    conferir(!(await page.$("#texto .novidade-missao")), "carregar o save não repete o cartão da sacristia");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioSarilho(browser) {
  console.log("cenário: as correntes do sarilho (uma ação só, os métodos dentro, e voltar sem gastar nada)");
  const { proc, url } = await subir("capela", { ETAPA: "fundo" });
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const foto = () => page.evaluate(() => JSON.stringify([estado.heroi.bolsa, estado.heroi.hp, estado.mundo.dia, estado.mundo.periodo_n, estado.missoes]));
  try {
    await page.waitForSelector(`${MENU}:has-text("Soltar as correntes")`, { timeout: 20000 });
    const menu = await page.$$eval(MENU, (bs) => bs.map((b) => [b.querySelector(".rotulo").textContent, b.className, !!b.querySelector(".op-abre")]));
    const grupos = await page.$$eval("#prompt .escolhas .op-grupo", (gs) => gs.map((g) => g.textContent));
    const correntes = menu.filter(([t]) => /correntes/i.test(t));
    conferir(correntes.length === 1 && /op-missao/.test(correntes[0][1]) && grupos[0] === "Missão" && !(await page.$("#prompt .op-etiqueta")),
      "as correntes são uma ação só, no grupo da missão (um rótulo para o grupo, nenhuma etiqueta por linha)");
    // (o lodo de Caspar se recolhe no fundo, 1.80.0: não está no menu do ossuário)
    conferir(menu.slice(0, 2).map(([t]) => t).join("|") === "Soltar as correntes|Descer ao fundo alagado"
      && menu.slice(0, 2).map(([, , a]) => a).join() === "true,true" && grupos.length === 2 && !menu.slice(2).some(([, , a]) => a),
      "nomes curtos; seta só nas que abrem outra escolha; a descida por último; um fio antes das ações de sempre");
    const antes = await foto();
    await page.click(`${MENU}:has-text("Soltar as correntes")`);
    await page.waitForSelector(`${MENU}:has-text("Deixar como está")`, { timeout: 20000 });
    const metodos = await page.$$eval(MENU, (bs) => bs.map((b) => `${b.querySelector(".rotulo").textContent} ${(b.querySelector(".teste") || {}).textContent || ""}`));
    conferir(metodos.length === 3 && /^Desenrolar as correntes à mão/.test(metodos[0]) && /barulhento/.test(metodos[0]) && !/afogados/.test(metodos.join(" "))
      && /^Arrancar a trava/.test(metodos[1]) && /Se não ceder/.test(metodos[1]) && /FOR [+−]\d+/.test(metodos[1]),
      `dentro: à mão e o método da classe, cada um com o risco embaixo, e deixar como está (${metodos.length})`);
    const cena = await page.textContent("#texto");
    conferir(/trava de ferro/.test(cena) && !/descanso|preparo/.test(cena), "o mecanismo é descrito, sem ensinar o rito antes de Berta");
    await page.screenshot({ path: process.env.CAPTURAS ? `${process.env.CAPTURAS}/sarilho-${(await page.viewportSize()).width}.png` : "/dev/null" }).catch(() => {});
    await page.click(`${MENU}:has-text("Deixar como está")`);
    await page.waitForSelector(`${MENU}:has-text("Soltar as correntes")`, { timeout: 20000 });
    conferir((await foto()) === antes && !(await page.$("#texto .novidade-missao")) && !(await page.$("#prompt .continuar")),
      "voltar não gasta nada, não mostra cartão e devolve o menu da capela");
    // A cena do ossuário (1.72.0): o sarilho é um ponto da sala que faz a mesma ação do menu. Desde a 1.77.0 a sala é
    // a arte do topo (os pontos numa camada por cima dela); no texto, nada desenhado.
    const SAR = '.ci-ponto[data-ponto="sarilho"]';
    const sala = () => page.evaluate(() => { const e = document.querySelector("#pontos-cena"); return e.dataset.cena === "ossuario" ? e.dataset.correntes + (e.dataset.foco ? "/perto" : "") : e.dataset.cena; });
    conferir((await sala()) === "presas" && !!(await page.$('#pontos-cena:not([hidden]) .ci-ponto[data-ponto="sarilho"]:not(.parado) .ci-balao'))
      && !(await page.$("#texto canvas")), "a arte do topo é o ossuário com o sarilho (correntes presas), o ponto por cima; o texto sem imagem");
    await page.hover(SAR);
    conferir(await page.$eval(SAR, (b) => b.classList.contains("aceso")), "o mouse em cima acende o sarilho");
    await page.mouse.move(2, 2);
    await page.focus(SAR);
    conferir(await page.$eval(SAR, (b) => b.classList.contains("aceso") && b.matches(":focus-visible, :focus")), "o foco do teclado acende do mesmo jeito");
    await page.keyboard.press("Enter");
    await page.waitForSelector(`${MENU}:has-text("Deixar como está")`, { timeout: 20000 });
    conferir((await sala()) === "presas/perto" && (await foto()) === antes, "Enter no sarilho aproxima e abre as mesmas formas de soltar, sem gastar nada");
    await page.click(`${MENU}:has-text("Deixar como está")`);
    await page.waitForSelector(`${MENU}:has-text("Soltar as correntes")`, { timeout: 20000 });
    await page.click(SAR);
    await page.waitForSelector(`${MENU}:has-text("Deixar como está")`, { timeout: 20000 });
    conferir((await foto()) === antes, "o clique também só abre as alternativas");
    await page.click(`${MENU}:has-text("Deixar como está")`);
    await page.waitForSelector(`${MENU}:has-text("Soltar as correntes")`, { timeout: 20000 });
    conferir((await sala()) === "presas" && (await foto()) === antes, "de volta: a sala de antes, nada gasto");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioCapelaFora(browser) {
  console.log("cenário: a capela por fora e o salão alagado (pontos, olhar de perto, a cena de cada momento)");
  const { proc, url } = await subir("capela", { ETAPA: "capela" });
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const foto = () => page.evaluate(() => JSON.stringify([estado.heroi.bolsa, estado.heroi.hp, estado.mundo.dia, estado.mundo.periodo_n, estado.missoes]));
  const cenas = () => page.evaluate(() => { const e = document.querySelector("#pontos-cena"); return e ? e.dataset.cena + (e.dataset.agua ? ":" + e.dataset.agua : "") : ""; });
  try {
    await page.waitForSelector(`${MENU}:has-text("Entrar na capela")`, { timeout: 20000 });
    conferir((await cenas()) === "exterior" && !!(await page.$('.ci-ponto[data-ponto="buraco"]:not(.parado) .ci-balao'))
      && !!(await page.$('.ci-ponto[data-ponto="sapos"]:not(.parado)')), "antes de entrar, a página mostra a capela por fora, com o buraco e os sapos à vista");
    const antes = await foto();
    // Os sapos: só olhar. Aproxima, Afastar volta, e nada muda.
    await page.focus('.ci-ponto[data-ponto="sapos"]'); await page.keyboard.press("Enter");
    await page.waitForSelector(".ci-afastar:not([hidden])", { timeout: 5000 });
    conferir(await page.evaluate(() => document.querySelector("#pontos-cena").classList.contains("perto") && document.activeElement.classList.contains("ci-afastar")),
      "Enter nos sapos aproxima a vista e leva o foco ao Afastar");
    conferir(/patas a mais/.test(await page.textContent("#texto .olhar-perto").catch(() => "")) && !(await page.$("#prompt .continuar")),
      "de perto, uma linha curta embaixo do texto (sem Continuar)");
    await page.keyboard.press("Enter");
    await page.waitForFunction(() => !document.querySelector("#pontos-cena").classList.contains("perto"), null, { timeout: 5000 });
    conferir((await foto()) === antes && !!(await page.$(`${MENU}:has-text("Entrar na capela")`)) && !(await page.$("#texto .olhar-perto")),
      "afastar volta à vista inteira, tira a linha, sem gastar nada nem mudar a missão");
    // O buraco faz a ação do menu: a cena do salão, com a água inquieta.
    await page.hover('.ci-ponto[data-ponto="buraco"]');
    conferir(await page.$eval('.ci-ponto[data-ponto="buraco"]', (b) => b.classList.contains("aceso")), "o mouse acende o buraco");
    await page.click('.ci-ponto[data-ponto="buraco"]');
    await page.waitForFunction(() => /Salão Alagado/.test(document.querySelector("#cena-cab .cena-titulo")?.textContent || ""), null, { timeout: 10000 });
    await page.waitForTimeout(300);
    conferir((await cenas()) === "salao:inquieta", "entrar pelo buraco abre o salão alagado, com a água inquieta (o ambiente que o texto descreve)");
    // A luta do salão: a arte do topo (o salão) vira o chão da arena; os pontos saem enquanto ela dura.
    await page.waitForFunction(() => document.body.classList.contains("em-combate") && document.querySelector("#arena > #vista"), null, { timeout: 20000 });
    conferir(await page.evaluate(() => document.querySelector("#pontos-cena").hidden && Vista.temAmbiente()),
      "na luta, o salão é o fundo da arena e os pontos ficam fora de alcance");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
  // Vencido o salão: a página mostra o salão quieto, com a porta da sacristia fazendo a ação do menu.
  const s2 = await subir("capela", { ETAPA: "sacristia" });
  const p2 = await abrir(browser, s2.url);
  try {
    await p2.page.waitForSelector(`${MENU}:has-text("Atravessar o salão")`, { timeout: 20000 });
    conferir(await p2.page.evaluate(() => { const e = document.querySelector("#pontos-cena"); return e.dataset.cena + ":" + e.dataset.agua; }) === "salao:quieta"
      && !!(await p2.page.$('.ci-ponto[data-ponto="porta"]:not(.parado)')), "vencido o salão, a página mostra o salão quieto com a porta da sacristia");
  } finally {
    conferir(p2.erros.length === 0, "sem erros no console" + (p2.erros.length ? ": " + p2.erros.slice(0, 3).join(" | ") : ""));
    await p2.page.close();
    s2.proc.kill();
  }
}
async function cenarioCustosEExausto(browser) {
  console.log("cenário: custo da bandagem, a proteção que levanta e a exaustão no mato");
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  let { proc, url } = await subir("covil", { EVENTO: "odete_na_estrada", BOLSA: "bandagem=0" });
  let { page, erros } = await abrir(browser, url);
  try {
    const b = await page.waitForSelector('#prompt .escolha:has-text("Estancar o sangue")', { timeout: 20000 });
    const info = await b.evaluate((x) => ({ desab: x.disabled, aria: x.getAttribute("aria-disabled"), texto: x.textContent }));
    conferir(info.desab && info.aria === "true" && /Você não tem bandagem na bolsa/.test(info.texto),
      "sem bandagem, a ajuda da Odette fica à vista, desabilitada e com o motivo escrito");
    await b.click({ force: true }).catch(() => {});
    await page.keyboard.press("1");
    await page.waitForTimeout(600);
    conferir(!!(await page.$(`${MENU}:has-text("Estancar o sangue")`)), "nem clique nem a tecla escolhem a indisponível");
    await page.click(`${MENU}:has-text("Perguntar quem ela é")`);
    await page.waitForFunction(() => /Ele ainda respira/.test(document.querySelector("#texto").textContent), null, { timeout: 10000 });
    await page.waitForSelector(`${MENU}:has-text("Segurar a ferida")`, { timeout: 10000 });
    const rotulos = await page.$$eval(MENU, (bs) => bs.map((x) => x.textContent));
    conferir(rotulos.length === 4 && !rotulos.some((r) => /Perguntar/.test(r)) && rotulos.some((r) => /Estancar/.test(r)),
      "perguntar o nome devolve as ações, sem a pergunta, e a ajuda continua possível");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
  ({ proc, url } = await subir("covil", { PROTECAO: "mendigo", LUTA: "troll" }));
  ({ page, erros } = await abrir(browser, url));
  try {
    let viu = false;
    for (let k = 0; k < 300 && !viu; k++) {
      viu = await page.evaluate(() => /calor que ficou no seu peito/.test(document.body.textContent));
      const bt = await page.$('#roda .roda-botao[data-slot="atacar"]'); if (bt) await bt.click().catch(() => {});
      const alvo = await page.$(".carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
      await page.waitForTimeout(100);
    }
    conferir(viu && !!(await page.waitForSelector(".chip.protecao", { timeout: 5000 }).catch(() => null)),
      "ao cair, a proteção do mendigo levanta o herói, com a frase dela e o aviso de que se foi");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
  ({ proc, url } = await subir("covil", { PERIODO: "3", LUGAR: "selvagem", SEMENTE: "9" }));
  ({ page, erros } = await abrir(browser, url));
  try {
    await (await page.waitForSelector(`${MENU}:has-text("Explorar")`, { timeout: 20000 })).click();
    await (await page.waitForSelector(`${MENU}:has-text("Recusar")`, { timeout: 20000 })).click();
    let continuares = 0;
    for (let k = 0; k < 120 && !(await page.$(".dormir-barraca")); k++) {
      const c = await page.$("#prompt .continuar");
      if (c) { await page.waitForTimeout(700); continuares++; await c.click().catch(() => {}); await page.waitForTimeout(400); }
      await page.waitForTimeout(150);
    }
    conferir(!!(await page.$(".dormir-barraca")) && continuares === 1,
      `exausto no mato: um Continuar para o fim do evento e a fogueira em seguida (${continuares})`);
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioCapelaSalas(browser) {
  console.log("cenário: andar pela capela (as salas vencidas, sem custo, pelos pontos e pelo menu; nomes só no mouse ou no destaque)");
  const { proc, url } = await subir("capela", { ETAPA: "fundo" });
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const foto = () => page.evaluate(() => JSON.stringify([estado.heroi.bolsa, estado.heroi.hp, estado.mundo.dia, estado.mundo.periodo_n, estado.missoes]));
  const sala = () => page.evaluate(() => { const e = document.querySelector("#pontos-cena"); return e.dataset.cena + (e.dataset.agua ? ":" + e.dataset.agua : ""); });
  const ir = async (texto, espera) => { await page.click(`${MENU}:has-text("${texto}")`); await page.waitForSelector(`${MENU}:has-text("${espera}")`, { timeout: 20000 }); await page.waitForTimeout(200); };
  try {
    await page.waitForSelector(`${MENU}:has-text("Subir à sacristia")`, { timeout: 20000 });
    const antes = await foto();
    conferir((await sala()) === "ossuario" && await page.evaluate(() => [...document.querySelectorAll("#pontos-cena .ci-balao")].every((b) => getComputedStyle(b).visibility === "hidden")),
      "no ossuário, os pontos sem nome fixo sobre a arte");
    await page.hover('.ci-ponto[data-ponto="escada"]');
    conferir(await page.$eval('.ci-ponto[data-ponto="escada"] .ci-balao', (b) => getComputedStyle(b).visibility === "visible" && /Escada/.test(b.textContent)),
      "o mouse na escada mostra o nome dela");
    await page.mouse.move(2, 2);
    await page.keyboard.press("F4");
    await page.waitForTimeout(200);
    conferir(await page.evaluate(() => document.body.classList.contains("destacar-interacoes")
      && [...document.querySelectorAll("#pontos-cena .ci-ponto:not(.parado) .ci-balao")].every((b) => getComputedStyle(b).visibility === "visible")),
      "F4 (destacar interações) mostra os nomes de todos os pontos");
    await page.keyboard.press("F4");
    await page.waitForTimeout(200);
    conferir(!(await page.evaluate(() => document.body.classList.contains("destacar-interacoes"))), "F4 de novo desliga");
    // a escada leva à sacristia (fundo neutro), o menu ao salão e à brecha; o buraco de volta ao salão, sem luta
    await page.click('.ci-ponto[data-ponto="escada"]');
    await page.waitForSelector(`${MENU}:has-text("Voltar ao salão alagado")`, { timeout: 20000 });
    await page.waitForTimeout(200);
    conferir((await sala()) === "neutra" && /Sacristia/.test(await page.textContent("#cena-cab")), "a escada sobe à sacristia: fundo neutro e a sala no subtítulo");
    await ir("Voltar ao salão alagado", "Sair pela brecha");
    conferir((await sala()) === "salao:quieta", "o salão vencido, quieto");
    await ir("Sair pela brecha", "Entrar no salão pelo buraco");
    conferir((await sala()) === "exterior", "pela brecha, do lado de fora");
    await page.click('.ci-ponto[data-ponto="buraco"]');
    await page.waitForSelector(`${MENU}:has-text("Sair pela brecha")`, { timeout: 20000 });
    conferir(!(await page.evaluate(() => document.body.classList.contains("em-combate"))) && !(await page.$("#prompt .continuar")),
      "o buraco leva de volta ao salão vencido sem luta e sem Continuar");
    await ir("Ir à sacristia", "Descer ao ossuário pelo alçapão");
    await ir("Descer ao ossuário pelo alçapão", "Soltar as correntes");
    conferir((await sala()) === "ossuario" && (await foto()) === antes,
      "ida e volta pela capela inteira: nada gasto, nenhum dia ou período a mais, a missão igual");
    // O lodo de Caspar (1.80.0): não no ossuário; na água do fundo, junto de Ilse, sem começar a luta.
    conferir(!(await page.$(`${MENU}:has-text("Recolher uma amostra")`)), "no ossuário, nada de recolher o lodo");
    const tempo = () => page.evaluate(() => JSON.stringify([estado.mundo.dia, estado.mundo.periodo_n, estado.heroi.bolsa]));
    const t0 = await tempo();
    await page.click('.ci-ponto[data-ponto="descida"]');
    await page.waitForSelector(`${MENU}:has-text("Recolher uma amostra do lodo")`, { timeout: 20000 });
    conferir((await sala()) === "neutra" && /Fundo da Capela/.test(await page.textContent("#cena-cab .cena-titulo")),
      "a descida: o fundo (neutro) com Ilse na água, e a amostra entre as escolhas");
    await page.click(`${MENU}:has-text("Recolher uma amostra do lodo")`);
    await page.waitForSelector(`${MENU}:has-text("Voltar por enquanto")`, { timeout: 20000 });
    conferir(!(await page.evaluate(() => document.body.classList.contains("em-combate"))) && !(await page.$(`${MENU}:has-text("Recolher uma amostra")`))
      && /frasco/.test(await page.textContent("#texto")), "recolhida a amostra, Ilse continua na água: sem luta, e a escolha some");
    await page.click(`${MENU}:has-text("Voltar por enquanto")`);
    await (await page.waitForSelector("#prompt .continuar", { timeout: 20000 })).click();
    await page.waitForSelector(`${MENU}:has-text("Subir à sacristia")`, { timeout: 20000 });
    conferir((await sala()) === "ossuario" && (await tempo()) === t0 && !(await page.$(`${MENU}:has-text("Recolher uma amostra")`)),
      "de volta ao ossuário, sem tempo nem gasto, e a amostra não se recolhe de novo");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioGuardia(browser) {
  console.log("cenário: a guardiã (o rito com tudo pronto, e salvar e carregar depois)");
  const { proc, url } = await subir("capela", { ETAPA: "fundo", PREPARO: "pronto", NIVEL: "6" });
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const missao = () => page.evaluate(() => (estado.missoes || [])[0]);
  try {
    await page.waitForSelector(`${MENU}:has-text("Descer ao fundo")`, { timeout: 20000 });
    conferir(await page.$eval("#pontos-cena", (e) => e.dataset.correntes === "soltas" && !!e.querySelector(".ci-ponto.parado")),
      "com as correntes soltas, o ossuário já as desenha soltas e o sarilho não oferece ação");
    await (await page.waitForSelector(`${MENU}:has-text("Descer ao fundo")`, { timeout: 20000 })).click();
    await page.waitForSelector(`${MENU}:has-text("Lutar para destruí-la")`, { timeout: 20000 });
    conferir(!!(await page.$(`${MENU}:has-text("Chamar Ilse pelo nome")`)), "com a verdade, a fita e as correntes, a descida oferece o rito e a luta para destruir");
    await page.click(`${MENU}:has-text("Chamar Ilse pelo nome")`);
    let momento = null;
    for (let k = 0; k < 400 && !(await page.$("#prompt .continuar.confirmar")); k++) {
      if (!momento && (await page.$(`${MENU}:has-text("Dizer o nome dela")`))) {
        momento = await page.evaluate(() => estado.combate.inimigos.map((i) => [i.hp, i.max_hp])[0]);
        await page.click(`${MENU}:has-text("Dizer o nome dela")`);
        continue;
      }
      if (await page.evaluate(() => document.body.classList.contains("em-combate"))) {
        const b = await page.$('#roda .roda-botao[data-slot="atacar"]'); if (b) await b.click().catch(() => {});
        const alvo = await page.$(".carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
      }
      const f = await page.$(".festa .continuar, .festa-espolio .continuar"); if (f) { await page.waitForTimeout(1000); await f.click().catch(() => {}); }
      const achado = await page.$('#sobre-achado .botao-janela:not(.reserva)'); if (achado) await achado.click().catch(() => {});
      const fim = await page.$("#prompt .continuar:not(.confirmar)"); if (fim) await fim.click().catch(() => {});
      await page.waitForTimeout(250);
    }
    conferir(!!momento && momento[0] === Math.floor(momento[1] * 0.5), `o momento do rito chega com ela exatamente na metade (${momento && momento.join("/")})`);
    conferir(/Ilse/.test(await page.textContent("#cena-cab .cena-titulo")) && /guardiã dele/.test(await page.textContent("#texto")),
      "ela descansa: o relato de Ilse, esperando o Continuar");
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    for (let k = 0; k < 60 && !(await page.$(`${MENU}:has-text("Explorar")`)); k++) {
      const f = await page.$(".festa .continuar, .festa-espolio .continuar"); if (f) { await page.waitForTimeout(1000); await f.click().catch(() => {}); }
      await page.waitForTimeout(250);
    }
    let m = await missao();
    conferir(m.desfecho === "descansada" && /Voltar ao Vau/.test(m.objetivo) && (await page.evaluate(() => estado.heroi.sigilos)) === 1
      && !(await page.$(`${MENU}:has-text("Descer ao fundo")`)), "desfecho guardado, o Sigilo na mão e o objetivo de voltar ao Vau");
    await (await page.waitForSelector('#doca .atalho[data-rotulo="Sair"]')).click();
    await (await page.waitForSelector(`${MENU}:has-text("Salvar e sair")`)).click();
    for (let t = 0; t < 60 && !(await page.$(`${MENU}:has-text("Carregar")`)); t++) {
      const c = await page.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
      await page.waitForTimeout(200);
    }
    await (await page.waitForSelector(`${MENU}:has-text("Carregar")`)).click();
    await (await page.waitForSelector(".save-cartao")).click();
    await page.waitForSelector(`${MENU}:has-text("Explorar")`, { timeout: 20000 });
    m = await missao();
    conferir(m.desfecho === "descansada" && !(await page.$(`${MENU}:has-text("Descer ao fundo")`)) && (await page.evaluate(() => estado.heroi.sigilos)) === 1,
      "carregado: ela segue descansada, sem descida nem Sigilo repetido");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioRetorno(browser) {
  console.log("cenário: de volta ao Vau depois de dar descanso a Ilse (conclusão, Fonte, Pita, a herança)");
  const { proc, url } = await subir("retorno", { DESFECHO: "descansada", DIAS: "0" });
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const diario = async () => {
    await page.keyboard.press("d");
    await page.waitForSelector(".quadro-missao", { timeout: 10000 });
    // o quadro inteiro: as em andamento, a pendência à vista e as concluídas (recolhidas)
    const t = await page.evaluate(() => {
      const q = document.querySelector(".quadro-missao"), det = q.querySelector(".missoes-concluidas");
      return { texto: q.textContent, pendencia: [...q.querySelectorAll(".missao-pendencia")].map((p) => p.textContent).join(" "),
        concluidas: det ? det.textContent : "", recolhida: !!det && !det.open };
    });
    await page.keyboard.press("Escape");
    await page.waitForSelector('#predios .predio[data-predio="taverna"]', { timeout: 20000 });
    await page.waitForTimeout(600);
    return t;
  };
  try {
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 20000 });
    const volta = await page.textContent("#texto");
    conferir(/De Volta ao Vau/.test(await page.textContent("#cena-cab .cena-titulo")) && /lodo assentou/.test(volta) && !/de noite|noite inteira/.test(volta),
      "a volta ao Vau toca a cena do descanso, esperando o Continuar, sem contar uma noite que não veio");
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    // Logo depois, a praça: Caspar reivindica o fim da febre. Sem prova, a denúncia não aparece; responder depois.
    await page.waitForSelector(`${MENU}:has-text("Ainda não")`, { timeout: 20000 });
    conferir(/A Praça do Vau/.test(await page.textContent("#cena-cab .cena-titulo")) && !(await page.$(`${MENU}:has-text("Denunciar")`))
      && /falta prova/.test(await page.textContent("#texto")), "a praça de Caspar vem depois da volta; sem prova, sem denúncia");
    await page.click(`${MENU}:has-text("Ainda não")`);
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 20000 });
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    await page.waitForSelector('#predios .predio[data-predio="taverna"]', { timeout: 20000 });
    await page.waitForTimeout(600);
    const ativas = () => page.evaluate(() => estado.missoes.map((m) => m.id).join(","));
    conferir((await ativas()) === "vigilia_de_caspar" && /Ninguém piorou desde que a água mudou/.test(await page.textContent("#texto")),
      "a febre concluída sai do rastreador; fica a resposta a Caspar, e a vila fala da Fonte que clareia");
    conferir((await page.evaluate(() => estado.local.atendentes.curandeiro)).startsWith("Pita"), "Marta de cama: Pita atende na curandeira");
    let d = await diario();
    conferir(/Concluídas \(1\)/.test(d.concluidas) && d.recolhida && /Ilse descansou/.test(d.concluidas) && /Vó Berta ainda espera/.test(d.pendencia)
      && !/Vó Berta ainda espera/.test(d.concluidas),
      "o Diário guarda a conclusão (recolhida) e deixa à vista que a herança espera");
    await page.click('#predios .predio[data-predio="taverna"]');
    await (await page.waitForSelector('.balcao-predio .servico:has-text("Contar a Vó Berta")', { timeout: 10000 })).click();
    for (let k = 0; k < 80 && !(await page.$("#prompt .continuar.confirmar")); k++) {
      const ach = await page.$('#sobre-achado .botao-janela:not(.reserva)');
      if (ach) { await page.waitForTimeout(700); await ach.click().catch(() => {}); }
      await page.waitForTimeout(250);
    }
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    await page.waitForSelector('#predios .predio[data-predio="taverna"]', { timeout: 20000 });
    await page.waitForTimeout(600);
    d = await diario();
    await page.click('#predios .predio[data-predio="taverna"]');
    await page.waitForSelector(".balcao-predio .servico", { timeout: 10000 });
    conferir(!/Vó Berta ainda espera/.test(d.texto) && !(await page.$('.balcao-predio .servico:has-text("Vó Berta")')),
      "a herança, depois de concluir, sai uma vez e o cartão some");
    await page.keyboard.press("Escape");
    await page.waitForTimeout(800);
    await (await page.waitForSelector('#doca .atalho[data-rotulo="Sair"]')).click();
    await (await page.waitForSelector(`${MENU}:has-text("Salvar e sair")`)).click();
    for (let t = 0; t < 60 && !(await page.$(`${MENU}:has-text("Carregar")`)); t++) {
      const c = await page.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
      await page.waitForTimeout(200);
    }
    await (await page.waitForSelector(`${MENU}:has-text("Carregar")`)).click();
    await (await page.waitForSelector(".save-cartao")).click();
    await page.waitForSelector('#predios .predio[data-predio="taverna"]', { timeout: 20000 });
    await page.waitForTimeout(600);
    conferir(!/De Volta ao Vau|A Praça/.test(await page.textContent("#cena-cab .cena-titulo")) && (await ativas()) === "vigilia_de_caspar"
      && !!(await page.$("#doca .atalho")), "carregado: sem repetir a cena, a febre continua concluída e a tela vem inteira");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioCaspar(browser) {
  console.log("cenário: a praça de Caspar (destruir e denunciar, com prova e Yara no grupo)");
  const { proc, url } = await subir("retorno", { DESFECHO: "destruida", DIAS: "1", LODO: "1", YARA: "grupo" });
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  try {
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 20000 });  // a volta ao Vau
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    await page.waitForSelector(`${MENU}:has-text("Denunciar")`, { timeout: 20000 });
    conferir(!!(await page.$(`${MENU}:has-text("Apoiar Caspar")`)) && !!(await page.$(`${MENU}:has-text("Calar-se")`)),
      "com o lodo e o canal, a praça oferece apoiar, denunciar e calar");
    await page.click(`${MENU}:has-text("Denunciar")`);
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 20000 });
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    // Na tela seguinte, o fim do capítulo: uma cena curta, uma vez, que diz que o capítulo acabou e o Vale segue aberto
    await page.waitForFunction(() => /O Vale do Turvo/.test(document.querySelector("#cena-cab .cena-titulo")?.textContent || ""),
      null, { timeout: 20000 });
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 20000 });
    await page.waitForTimeout(800);
    const fim = await page.textContent("#texto");
    conferir(/fim do capítulo disponível/.test(fim) && /Ilse/.test(fim) && /Caspar (foi embora|ficou no Vau)/.test(fim) && /Yara/.test(fim),
      "o fim do capítulo: Ilse, Caspar e Yara, e o aviso de que o Vale continua aberto");
    for (const largura of [1500, 1280]) {
      await page.setViewportSize({ width: largura, height: largura === 1500 ? 950 : 720 });
      await page.waitForTimeout(300);
      await page.screenshot({ path: process.env.CAPTURAS ? `${process.env.CAPTURAS}/fim-capitulo-${largura}.png` : "/dev/null" }).catch(() => {});
    }
    await page.setViewportSize({ width: 1500, height: 950 });
    await page.click("#prompt .continuar");
    await page.waitForSelector('#predios .predio[data-predio="taverna"]', { timeout: 20000 });
    await page.waitForTimeout(600);
    const praca = await page.textContent("#texto");
    conferir((await page.evaluate(() => estado.missoes.length)) === 0 && /praça/.test(praca),
      "decidido: nenhuma missão ativa, e a vila fala da praça depois da decisão");
    conferir(/Primeiro capítulo concluído/.test(await page.textContent("#mundo")),
      "o rastreador mostra o capítulo concluído no lugar da missão");
    await page.screenshot({ path: process.env.CAPTURAS ? `${process.env.CAPTURAS}/fim-capitulo-vila.png` : "/dev/null" }).catch(() => {});
    await page.keyboard.press("d");
    // Concluída, a Vigília fica em "Concluídas", recolhida: abre-se como o jogador abriria
    await page.waitForSelector(".missoes-concluidas > summary", { timeout: 10000 });
    conferir(!(await page.$eval(".missoes-concluidas", (el) => el.open)), "a missão decidida vai para Concluídas, recolhida");
    conferir(/Primeiro capítulo concluído/.test(await page.textContent(".missao-capitulo")), "o Diário abre com o capítulo concluído");
    await page.click(".missoes-concluidas > summary");
    await page.waitForSelector('.missao-diario[data-missao="vigilia_de_caspar"]', { timeout: 10000 });
    const d = await page.textContent('.missao-diario[data-missao="vigilia_de_caspar"]');
    conferir(/Ilse: os ossos dela ficaram no fundo da capela/.test(d) && /Caspar: /.test(d) && /Yara: /.test(d),
      "o Diário conta à parte o que houve com Ilse, com Caspar e com a Yara");
    conferir(await page.evaluate(() => (estado.heroi.comitiva || []).some((c) => c.id === "yara")) && !!(await page.$('[data-conversar="yara"], #heroi :text("Yara")')),
      "a Yara continua no grupo e à vista no painel");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioResgate(browser) {
  console.log("cenário: a recuperação da campanha (infecção no Charco, com a comitiva)");
  const { proc, url } = await subir("resgate", { CAUSA: "infeccao", CONTRATOS: "1" });
  const { page, erros, esperar } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  try {
    const [provisoes, ouroAntes] = await (async () => { await page.waitForSelector(`${MENU}:has-text("Acampar")`, { timeout: 20000 });
      return page.evaluate(() => [estado.heroi.provisoes, estado.heroi.ouro]); })();
    await page.click(`${MENU}:has-text("Acampar")`);
    for (let k = 0; k < 160 && !/ouro sumiu/.test(await page.textContent("#texto")); k++) {
      const dormir = await page.$(".dormir-barraca"); if (dormir) await dormir.click().catch(() => {});
      const q = page.locator("button:visible", { hasText: "Continuar" }).first();
      if (await q.count()) await q.click({ timeout: 1000 }).catch(() => {});
      await page.waitForTimeout(200);
    }
    const texto = await page.textContent("#texto");
    const h = await page.evaluate(() => ({ local: estado.local.nome, prov: estado.heroi.provisoes, hp: estado.heroi.hp,
      feridas: (estado.heroi.ferimentos || []).map((f) => f.nome || f.id).join(",") }));
    conferir(/Pita trocou as faixas e deu caldo a você e à comitiva/.test(texto) && /limpou a ferida infeccionada/.test(texto),
      "a infecção derruba e leva ao resgate, com Pita cuidando de todos");
    conferir(h.local === "Vau do Turvo" && h.prov === provisoes && h.hp > 0 && !/Infec/.test(h.feridas),
      `no Vau, sem gastar a bolsa e sem a infecção (${JSON.stringify(h)})`);
    // O contrato cumprido antes da queda paga na página do Vau, depois do resgate (antes, só saindo e voltando).
    const ouro = ouroAntes - Math.floor(ouroAntes * 0.3);  // o que fica depois da cobrança do resgate
    const festa = await esperar(".festa-contratos", 20000);
    conferir(!!festa && !(await page.$(".festa-espolio")), "acordado no Vau, o contrato cumprido paga num quadro só, na página da vila");
    if (festa) {
      await page.waitForTimeout(1800);
      await page.click(".festa-contratos .continuar").catch(() => {});
      for (let k = 0; k < 30 && (await page.evaluate(() => estado.heroi.ouro)) <= ouro; k++) await page.waitForTimeout(100);
      conferir((await page.evaluate(() => estado.heroi.ouro)) > ouro, "e o ouro do contrato entra, depois da cobrança do resgate");
    }
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioBroquel(browser) {
  console.log("cenário: o Broquel do Vigia (a oferta única do ferreiro, o cartão com o Revide e a reação na luta)");
  let { proc, url } = await subir("capela", { CLASSE: "guerreiro", ETAPA: "fundo", LUGAR: "vau_do_turvo", NIVEL: "5" });
  let { page, erros, esperar } = await abrir(browser, url);
  try {
    const forja = await esperar('#predios .predio[data-predio="ferreiro"]');
    await page.waitForTimeout(600);
    await forja.click();
    await page.waitForSelector(".balcao-predio .servico", { timeout: 10000 });
    const cartoes = await page.$$eval(".balcao-predio .servico", (x) => x.map((e) => e.textContent));
    conferir(cartoes.length === 2 && /Reforçar/.test(cartoes[0]) && /broquel que trouxeram da capela/.test(cartoes[1]),
      "save que já venceu o ossuário: a forja mostra o reforço e o broquel, um cartão cada");
    await page.click('.balcao-predio .servico:has-text("broquel")');
    const achado = await esperar(".achado-cartao", 15000);
    await page.waitForTimeout(1200);
    const texto = await achado.evaluate((x) => x.textContent);
    conferir(/Revide: com o escudo erguido/.test(texto) && /▲ Revide/.test(texto),
      "o cartão diz a regra (Revide) e a comparação mostra o ganho dela");
    await (await esperar('#sobre-achado .botao-janela:not(.reserva):has-text("Guardar")', 8000)).click();
    await (await esperar('#predios .predio[data-predio="ferreiro"]')).click();
    conferir(!!(await page.waitForSelector(".forja", { timeout: 10000 }).catch(() => null)),
      "recebido o broquel, a forja volta a ser só o reforço (a oferta não se repete)");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
  ({ proc, url } = await subir("broquel", {}));
  ({ page, erros, esperar } = await abrir(browser, url));
  try {
    await page.evaluate(() => { window.__revides = 0;
      new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => {
        if (n.nodeType === 1 && (n.textContent || "").trim() === "Revide") window.__revides++;
      }))).observe(document.getElementById("batalha"), { childList: true, subtree: true }); });
    await (await esperar('.roda-botao[data-slot="habilidades"]')).click();
    await (await esperar('.rj-linha[data-hab="erguer_escudo"]')).click();
    for (let k = 0; k < 200 && !(await page.evaluate(() => window.__revides > 0)); k++) {
      const bt = await page.$('#roda .roda-botao[data-slot="atacar"]'); if (bt) await bt.click().catch(() => {});
      const a = await page.$(".carta.alvejavel"); if (a) await a.click().catch(() => {});
      await page.waitForTimeout(60);
    }
    conferir(await page.evaluate(() => window.__revides > 0), "com o escudo erguido, o golpe corpo a corpo volta como Revide, com o nome na carta");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioYara(browser) {
  console.log("cenário: a Yara depois da praça (barrada no Vau e de volta na estrada; livre no Charco)");
  let { proc, url } = await subir("praca", { POSTURA: "apoiar", YARA: "grupo" });
  let { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const yara = () => page.evaluate(() => (estado.heroi.comitiva || []).find((c) => c.id === "yara"));
  try {
    // O save já tem tudo resolvido: no Vau, o fim do capítulo vem primeiro, uma vez
    await page.waitForFunction(() => /O Vale do Turvo/.test(document.querySelector("#cena-cab .cena-titulo")?.textContent || ""),
      null, { timeout: 20000 });
    await page.waitForSelector("#prompt .continuar.confirmar", { timeout: 20000 });
    await page.waitForTimeout(800);
    await page.click("#prompt .continuar");
    await page.waitForSelector('#predios .predio[data-predio="taverna"]', { timeout: 20000 });
    await page.waitForSelector('#heroi .membro[data-cid="yara"]', { timeout: 20000 });
    await page.waitForTimeout(600);
    let y = await yara();
    conferir(!!y && y.fora && /espera fora do Vau/.test(y.fora.curto) && !y.conversa
      && !!(await page.$('#heroi .membro.ferido[data-cid="yara"]')) && !(await page.$('[data-conversar="yara"]')),
      "apoiada a vigília, a Yara continua na comitiva, mas o painel diz que espera fora do Vau (sem conversa ali)");
    conferir(/Yara espera do lado de fora/.test(await page.textContent("#texto")), "a vila conta onde ela está");
    await page.click('.caminho:has-text("Charco dos Juncos")');
    for (let t = 0; t < 150; t++) {
      const onde = await page.evaluate(() => !estado.local.estrada && estado.local.nome);
      if (onde === "Charco dos Juncos" && !(await page.$("#prompt .continuar"))) break;
      const c = await page.$("#prompt .continuar"); if (c) { await page.waitForTimeout(300); await c.click().catch(() => {}); }
      await page.waitForTimeout(200);
    }
    await page.waitForTimeout(800);
    y = await yara();
    conferir(!!y && !y.fora && y.conversa && !(await page.$('#heroi .membro.ferido[data-cid="yara"]')),
      "fora do Vau ela volta para o seu lado, e quer conversar sobre a praça");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
  ({ proc, url } = await subir("praca", { POSTURA: "denunciado", LUGAR: "charco_dos_juncos" }));
  ({ page, erros } = await abrir(browser, url));
  try {
    await page.waitForSelector(`${MENU}:has-text("Aceitar Yara")`, { timeout: 20000 });
    conferir(/A Moça do Charco/.test(await page.textContent("#cena-cab .cena-titulo")) && !/lenha|forcado/.test(await page.textContent("#texto")),
      "denunciada a perseguição, a Yara que você não conhecia está livre no Charco, sem fogueira");
    await page.click(`${MENU}:has-text("Aceitar Yara")`);
    for (let t = 0; t < 60 && !(await page.$(`${MENU}:has-text("Explorar")`)); t++) {
      const c = await page.$(".festa .continuar, #prompt .continuar"); if (c) { await page.waitForTimeout(700); await c.click().catch(() => {}); }
      await page.waitForTimeout(250);
    }
    conferir(!!(await yara()), "aceita, ela entra na comitiva");
    await (await page.waitForSelector('#doca .atalho[data-rotulo="Sair"]')).click();
    await (await page.waitForSelector(`${MENU}:has-text("Salvar e sair")`)).click();
    for (let t = 0; t < 60 && !(await page.$(`${MENU}:has-text("Carregar")`)); t++) {
      const c = await page.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
      await page.waitForTimeout(200);
    }
    await (await page.waitForSelector(`${MENU}:has-text("Carregar")`)).click();
    await (await page.waitForSelector(".save-cartao")).click();
    await page.waitForSelector(`${MENU}:has-text("Explorar")`, { timeout: 20000 });
    await page.waitForTimeout(600);
    conferir(!/A Moça do Charco/.test(await page.textContent("#cena-cab .cena-titulo"))
      && (await page.evaluate(() => estado.heroi.comitiva.filter((c) => c.id === "yara").length)) === 1,
      "carregado: o encontro não se repete e a Yara está lá uma vez só");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioGolpePreparado(browser) {
  console.log("cenário: o golpe preparado no ossuário (aviso na escolha, ficha, Investida que interrompe)");
  const { proc, url } = await subir("capela", { ETAPA: "ossuario", NIVEL: "3", SEMENTE: "7" });
  const { page, erros } = await abrir(browser, url);
  const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
  const PREP = '#batalha .carta.inimigo:has(.preparando:not([hidden]))';
  try {
    await (await page.waitForSelector(`${MENU}:has-text("Descer ao ossuário")`, { timeout: 20000 })).click();
    let viu = false, turno = 0;
    for (let k = 0; k < 300 && !viu; k++) {
      const roda = await page.$('#roda .roda-botao[data-slot="atacar"]');
      if (roda) {
        await page.waitForTimeout(600);
        const prep = await page.$(PREP);
        if (prep) {
          viu = true;
          conferir(/Esqueleto de Guarda/.test(await prep.textContent()) && !!(await page.$('#roda .roda-botao[data-slot="habilidades"]')),
            "na sua vez, a carta de quem prepara mostra o aviso, e as ações estão abertas para responder");
          conferir(await prep.evaluate((carta) => { const a = carta.querySelector(".preparando").getBoundingClientRect();
            const topo = document.elementFromPoint(a.x + a.width / 2, a.y + a.height / 2); return !!topo && carta.contains(topo); }),
            "nada cobre o aviso (nem a faixa de ação de outro inimigo)");
          const caixa = await prep.boundingBox();
          await page.mouse.move(5, 5);
          await page.mouse.move(caixa.x + caixa.width / 2, caixa.y + 12, { steps: 5 });
          await page.waitForTimeout(900);
          conferir(/Prepara um golpe esmagador/.test(await page.evaluate(() => { const d = document.getElementById("dica-item"); return d && !d.hidden ? d.textContent : ""; })),
            "a ficha do inimigo diz que ele prepara o golpe e como responder");
          await page.mouse.move(700, 880);
          await (await page.$('.roda-botao[data-slot="habilidades"]')).click();
          await (await page.waitForSelector('.rj-linha[data-hab="investida"]')).click();
          await (await page.waitForSelector(`.carta.alvejavel:has(.preparando:not([hidden]))`, { timeout: 5000 })).click();
          for (let t = 0; t < 60 && !(await page.$('#roda .roda-botao[data-slot="atacar"]')); t++) await page.waitForTimeout(200);
          conferir(/perde o golpe que preparava/.test(await page.textContent("#texto")) && !(await page.$(PREP)),
            "a Investida atordoa e interrompe: o golpe se perde e o aviso sai da carta");
          break;
        }
        turno++;
        await roda.click().catch(() => {});
        await page.waitForTimeout(200);
        const alvos = await page.$$(".carta.alvejavel");
        const alvo = alvos[1] || alvos[0];
        if (alvo) await alvo.click().catch(() => {});
      }
      const c = await page.$("#prompt .continuar");
      if (c) await c.click().catch(() => {});
      await page.waitForTimeout(150);
    }
    conferir(viu, "o Esqueleto de Guarda prepara o golpe na luta do ossuário");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioEncruzilhada(browser) {
  console.log("cenário: a Encruzilhada (comparar, olhar de perto, voltar sem efeito, confirmar uma vez)");
  const { proc, url } = await subir("encruzilhada", { CLASSE: "guerreiro" });
  const { page, erros, esperar } = await abrir(browser, url);
  try {
    conferir(!!(await esperar(".especializacao .esp-olhar")), "a escolha mostra os dois caminhos lado a lado");
    const cartas = await page.$$eval(".esp-caminho", (cs) => cs.map((c) => c.textContent));
    conferir(cartas.length === 2 && /Defesa\s*−2/.test(cartas[1]) && /grito de terror/.test(cartas[0]) && /definitiva/.test(await page.textContent(".especializacao")),
      "cada carta tem atributos, habilidades, o que dá e limites (Berserker perde Defesa; Paladino resiste ao terror); a escolha é definitiva");
    const heroi = () => page.evaluate(() => JSON.stringify(App.estado.heroi));
    const antes = await heroi();
    await (await page.$(".esp-olhar[data-caminho=berserker]")).click();
    await page.waitForSelector(".esp-caminho.foco .esp-confirmar", { timeout: 10000 });
    await page.keyboard.press("Escape");
    await page.waitForSelector(".esp-olhar[data-caminho=paladino]", { timeout: 10000 });
    conferir(antes === await heroi(), "olhar de perto e voltar não mudam o herói");
    const vida = JSON.parse(antes).max_hp;
    await (await page.$(".esp-olhar[data-caminho=paladino]")).click();
    await (await page.waitForSelector(".esp-caminho.foco .esp-confirmar", { timeout: 10000 })).click();
    await esperar("#doca .atalho");
    const depois = await page.evaluate(() => ({ spec: App.estado.heroi.spec, max_hp: App.estado.heroi.max_hp }));
    conferir(depois.spec === "paladino" && depois.max_hp === vida + 15, `confirmar aplica o caminho uma vez (vida ${vida} → ${depois.max_hp})`);
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioTiroDuplo(browser) {
  console.log("cenário: o Tiro Duplo (o 1º derruba o alvo, o 2º segue para o mais ferido)");
  const { proc, url } = await subir("tiro_duplo");
  const { page, erros, esperar } = await abrir(browser, url);
  try {
    conferir(!!(await esperar('#roda .roda-botao[data-slot="habilidades"]')), "a luta abre com as ações do Patrulheiro");
    await (await page.$('#roda .roda-botao[data-slot="habilidades"]')).click();
    await (await page.waitForSelector('.rj-linha[data-hab="tiro_duplo"]')).click();
    await (await page.waitForSelector('.carta.alvejavel:has-text("Alfa")', { timeout: 5000 })).click();
    await esperar('#roda .roda-botao[data-slot="habilidades"]');
    const texto = await page.textContent("#texto");
    const vidas = await page.evaluate(() => Object.fromEntries(App.estado.combate.inimigos.map((e) => [e.nome, e.hp])));
    conferir(/Você atinge Alfa/.test(texto) && /Você atinge Gama/.test(texto) && !/Você atinge Beta/.test(texto) && vidas.Alfa === 0,
      "o 1º disparo derruba Alfa e o 2º vai em Gama, o mais ferido; Beta, inteiro, não leva flecha");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioAbertura(browser) {
  console.log("cenário: a abertura guiada (a despensa, os quadros da primeira luta, a Ajuda e o Mural)");
  const { proc, url } = await subir("abertura", { CLASSE: "mago" });
  const { page, erros, esperar } = await abrir(browser, url);
  const quadro = () => page.evaluate(() => { const q = document.querySelector(".orientacao:not([hidden])"); return q ? q.querySelector(".orientacao-texto").textContent : ""; });
  // O quadro nunca cobre uma carta da arena (vida, inimigos) nem as ações da roda.
  const cobre = () => page.evaluate(() => {
    const q = document.querySelector(".orientacao:not([hidden])");
    if (!q) return false;
    const b = q.getBoundingClientRect();
    return [...document.querySelectorAll("#arena .carta, #roda .roda-botao")].some((c) => {
      const r = c.getBoundingClientRect();
      return r.width && !(b.right <= r.left || b.left >= r.right || b.bottom <= r.top || b.top >= r.bottom);
    });
  });
  const ateQuadro = async (re, ms = 6000) => { for (let t = 0; t < ms; t += 100) { if (re.test(await quadro())) return true; await page.waitForTimeout(100); } return false; };
  try {
    await (await esperar('#prompt .escolha:has-text("Descer à despensa")', 30000)).click();
    conferir(await ateQuadro(/Clique em Habilidades \(tecla 2\)/, 15000) && !(await cobre()), "C1: o quadro aponta Habilidades, sem cobrir carta nem ação");
    await page.click('#roda .roda-botao[data-slot="habilidades"]');
    conferir(await ateQuadro(/Clique em Bola de Fogo/), "C2: aberta a janelinha, o quadro aponta a habilidade da classe");
    await page.keyboard.press("1");  // a mesma coisa pelo teclado
    conferir(await ateQuadro(/escolher o alvo/) && !(await cobre()), "C3: na mira, o quadro pede o alvo sem cobrir os inimigos");
    await page.click("#arena .carta.alvejavel");
    conferir(await ateQuadro(/Bola de Fogo\s*−14 Mana\s*Atacar não gasta Mana\. Ao acertar, \+2 Mana\./),
      "C4: depois do golpe, o nome, o custo real e o que o Atacar faz, em linhas separadas");
    const antes = await page.evaluate(() => JSON.stringify(pergunta));
    await page.click(".orientacao-entendi");
    await page.waitForTimeout(300);
    conferir(!(await quadro()) && antes === (await page.evaluate(() => JSON.stringify(pergunta))) && (await page.evaluate(() => estado.orientacao.ligado)),
      "Entendi fecha só o quadro: a pergunta da luta continua a mesma e as orientações seguem ligadas");
    await page.keyboard.press("F1");
    conferir(!(await page.$("#sobre-ajuda[hidden]")) && /Bola de Fogo gasta 14 de Mana/.test(await page.textContent("#ajuda-corpo")) === false,
      "F1 abre a Ajuda (antes de a luta acabar, ela ainda não lista a luta)");
    await page.click("#ajuda-corpo .ajuda-chave");
    await page.waitForTimeout(300);
    conferir(!(await quadro()) && /desligado/.test(await page.textContent("#ajuda-corpo .ajuda-chave")), "na Ajuda, desligar tira os quadros na hora");
    await page.keyboard.press("Escape");
    conferir(!!(await page.$("#sobre-ajuda[hidden]")), "Esc fecha a Ajuda");
    for (let k = 0; k < 80 && (await page.evaluate(() => !!(estado && estado.combate))); k++) {
      const atk = await page.$('#roda .roda-botao[data-slot="atacar"]'); if (atk) { await atk.click().catch(() => {}); await page.waitForTimeout(250); }
      const alvo = await page.$("#arena .carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
      const fe = await page.$(".festa-espolio .continuar"); if (fe) { await page.waitForTimeout(600); await fe.click().catch(() => {}); }
      await page.waitForTimeout(200);
    }
    let mural = null, vistaTaverna = false;
    for (let k = 0; k < 120 && !(mural = await page.$('#predios .predio[data-predio="mural"]:visible')) ; k++) {  // o espólio e o texto até a vila
      const fe = await page.$("#celebracao:not([hidden]) .continuar"); if (fe) { await page.waitForTimeout(700); await fe.click().catch(() => {}); }
      const c = await page.$("#prompt .continuar"); if (c) {
        if (!vistaTaverna && /primeira caneca é por minha conta/.test(await page.textContent("#pagina"))) {  // a cena espera o clique
          await page.waitForTimeout(2500);
          vistaTaverna = !!(await page.$("#prompt .continuar"));
        }
        await page.waitForTimeout(900); await c.click().catch(() => {});
      }
      await page.waitForTimeout(200);
    }
    await page.waitForTimeout(500);
    conferir(vistaTaverna, "a cena depois da despensa (caneca e mural) espera o Continuar");
    conferir(!!mural && !(await quadro()), "na vila, desligado: nenhum quadro");
    await page.keyboard.press("F1");
    await page.click("#ajuda-corpo .ajuda-chave");
    await page.keyboard.press("Escape");
    conferir(await ateQuadro(/Clique no mural para ver os contratos disponíveis\./), "religado na Ajuda: V1 aponta o Mural");
    conferir(await page.evaluate(() => {  // abaixo do cenário: nem o desenho do mural nem o nome dele ficam por baixo
      const q = document.querySelector(".orientacao:not([hidden])").getBoundingClientRect();
      const m = document.querySelector('#predios .predio[data-predio="mural"]');
      const longe = (r) => q.right <= r.left || q.left >= r.right || q.bottom <= r.top || q.top >= r.bottom;
      return longe(m.getBoundingClientRect()) && longe(m.querySelector(".balao-nome").getBoundingClientRect())
        && q.top >= document.querySelector("#vista").getBoundingClientRect().bottom && !/clique: contratos/.test(document.body.innerText);
    }), "o quadro do V1 fica abaixo do cenário, sem cobrir o mural nem o nome; sem a legenda \"clique: contratos\"");
    const card = await page.$('.predio[data-predio="taverna"]');
    conferir(!!card, "a taverna está na vila (a despensa feita, Morel à espera nela)");
    await page.click(".orientacao-encerrar");
    await page.waitForTimeout(400);
    conferir(!(await quadro()) && !(await page.evaluate(() => estado.orientacao.ligado)), "Encerrar tutorial desliga e o quadro some");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioFogueira(browser) {
  console.log("cenário: a fogueira (quem vai, quem fica, a nota do acampamento) e a fome fora da barra");
  const { proc, url } = await subir("fogueira", { COMITIVA: "morel", RESERVA: "odete", FOME: "1" });
  const { page, erros, esperar } = await abrir(browser, url);
  try {
    await esperar('#prompt .escolha:has-text("Acampar")', 30000);
    const hud = () => page.evaluate(() => ({ cond: document.querySelector(".hud-condicoes").innerText.trim(),
      alto: Math.round(document.querySelector("#hud").getBoundingClientRect().height), fome: !!document.querySelector(".hud-fome") }));
    const antes = await hud();
    conferir(antes.cond === "Com fome" && !antes.fome, "a fome mora embaixo das barras (não em cima da vida)");
    await page.click('#prompt .escolha:has-text("Acampar")');
    await esperar(".fogueira-rodape", 20000);
    const rod = await page.textContent(".fogueira-rodape");
    conferir(/Clique num companheiro para conversar ou ajustar a comitiva\./.test(rod) && /Comitiva 1\/2/.test(rod)
      && /Vai com você:\s*Morel/.test(rod) && /No acampamento:\s*Odette/.test(rod) && !/Descansa/.test(rod),
      "embaixo da fogueira: a instrução, o contador, quem vai e quem fica (a nota do acampamento fica no menu)");
    await page.click('.figura[data-cid="morel"]');
    conferir(/Deixar no acampamento\s*Descansa, não come das suas provisões/.test(await page.textContent(".menu-item")),
      "no menu de quem vai, a nota junto do \"Deixar no acampamento\"");
    await page.mouse.click(5, 5);
    // O botão flutua sem parar (boiar, 4 px): sem esperar que ele pare, o clique no centro o acerta do mesmo jeito.
    await page.click(".dormir-barraca", { force: true });
    for (let k = 0; k < 150 && (await page.evaluate(() => !estado || estado.heroi.fome || !pergunta || !!document.querySelector(".fogueira-palco"))); k++) {
      const c = await page.$("#prompt .continuar"); if (c) { await page.waitForTimeout(300); await c.click().catch(() => {}); }
      await page.waitForTimeout(150);
    }
    const depois = await hud();
    conferir(depois.cond === "" && depois.alto === antes.alto, "o amanhecer come a provisão: a fome some e o painel não muda de altura");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioTutorial(browser) {
  console.log("cenário: a segunda parte da abertura guiada (item achado, recuperar, noite e explorar)");
  const quadro = (page) => page.evaluate(() => { const q = document.querySelector(".orientacao:not([hidden])"); return q ? q.innerText.replace(/\s+/g, " ") : ""; });
  const cobre = (page) => page.evaluate(() => {  // controles, barras, cartas, nomes e a página que está à vista
    const q = document.querySelector(".orientacao:not([hidden])").getBoundingClientRect(), pg = document.querySelector("#pagina").getBoundingClientRect();
    return [...document.querySelectorAll("#prompt .escolha, #texto > *, #hud .vital, #hud .recurso, #doca .atalho, #predios .predio, #predios .balao-nome, .achado-cartao, .achado-acoes button")].some((e) => {
      let r = e.getBoundingClientRect();
      if (e.closest("#pagina")) r = { left: r.left, right: r.right, top: Math.max(r.top, pg.top), bottom: Math.min(r.bottom, pg.bottom) };
      return r.bottom > r.top && r.right > r.left && !(q.right <= r.left || q.left >= r.right || q.bottom <= r.top || q.top >= r.bottom);
    });
  });
  const ate = async (page, re, ms = 20000) => { for (let k = 0; k < ms; k += 150) { if (re.test(await quadro(page))) return true; await page.waitForTimeout(150); } return false; };
  {
    const { proc, url } = await subir("tutorial", { ITEM: "1", VIDA: "0.4" });
    const { page, erros } = await abrir(browser, url);
    try {
      conferir(await ate(page, /A linha "contra…" compara o achado/) && !(await cobre(page)), "E1: no item achado, a comparação e as escolhas, sem cobrir a janela");
      await page.keyboard.press("2");  // Guardar, pelo teclado
      conferir(await ate(page, /^O Templo recupera sua vida\. Seu primeiro atendimento é grátis\./) && !(await cobre(page)),
        "decidido o item, o E1 sai; na vila, V2 aponta o Templo (a vida baixa), sem cobrir prédio nem página");
      await page.click('#predios .predio[data-predio="estrada"]');
      conferir(await ate(page, /Cada amanhecer come 1 provisão sua/), "V3: ao escolher o destino, as provisões do topo");
      await page.click(".orientacao-entendi");
      await page.waitForTimeout(600);
      conferir(!(await quadro(page)) && (await page.evaluate(() => estado.orientacao.atual === null)), "Entendi fecha o V3, e nenhum outro quadro entra na mesma tela");
    } finally {
      conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
      await page.close();
      proc.kill();
    }
  }
  {
    const { proc, url } = await subir("tutorial", { LUGAR: "charco", PERIODO: "3" });
    const { page, erros } = await abrir(browser, url);
    try {
      conferir(await ate(page, /^A noite deixa os inimigos mais fortes\./) && !(await cobre(page)) && (await pontaNoAlvo(page)) <= 2,
        "N1: fora da vila, à noite, a linha da noite nos riscos do lugar, com a seta encostando nela, sem cobrir a página");
      await page.keyboard.press("1");  // explorar, pelo teclado: a ocasião passa
      for (let k = 0; k < 80 && !(await page.$("#prompt .escolha")); k++) {
        const c = await page.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
        if (await page.evaluate(() => !!(estado && estado.combate))) break;
        await page.waitForTimeout(200);
      }
      conferir(!/Noite:/.test(await quadro(page)), "respondido o menu, o N1 não volta");
    } finally {
      conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
      await page.close();
      proc.kill();
    }
  }
}

/** A ponta da seta do quadro (ou da haste) até o controle destacado, em px (0: encosta nele); null sem destaque. */
const pontaNoAlvo = (page) => page.evaluate(() => {
  const q = document.querySelector(".orientacao:not([hidden])"), a = document.querySelector(".orientacao-anel:not([hidden])");
  if (!q || !a) return null;
  const b = q.getBoundingClientRect(), r = a.getBoundingClientRect(), s = parseFloat(getComputedStyle(q).getPropertyValue("--seta")) || 0;
  const lado = (q.className.match(/seta-(\w+)/) || [])[1], h = document.querySelector(".orientacao-haste:not([hidden])");
  let x = b.left + s, y = lado === "cima" ? b.bottom + 6 : b.top - 6;
  if (lado === "direita") { x = b.left - 6; y = b.top + s; }
  if (lado === "esquerda") { x = b.right + 6; y = b.top + s; }
  if (h) { const k = h.getBoundingClientRect(); x = k.left + 1; y = lado === "baixo" ? k.top : k.bottom; }
  return Math.round(Math.max(r.left - x, 0, x - r.right) + Math.max(r.top - y, 0, y - r.bottom));
});

async function cenarioCiclos(browser) {
  console.log("cenário: os ciclos básicos (o primeiro atendimento grátis do templo e o primeiro contrato)");
  const { proc, url } = await subir("tutorial", { VIDA: "0.4", VISTAS: "A1" });
  const { page, erros } = await abrir(browser, url);
  const quadro = () => page.evaluate(() => { const q = document.querySelector(".orientacao:not([hidden])"); return q ? q.innerText.replace(/\s+/g, " ") : ""; });
  const ate = async (re, ms = 20000) => { for (let k = 0; k < ms; k += 150) { if (re.test(await quadro())) return true; await page.waitForTimeout(150); } return false; };
  try {
    conferir(await ate(/^O Templo recupera sua vida\. Seu primeiro atendimento é grátis\./) && !/Taverna|Vigor|fome/.test(await quadro()),
      "V2: o Templo e o primeiro atendimento grátis, sem misturar a Taverna");
    const ouro = await page.evaluate(() => estado.heroi.ouro);
    await page.click('#predios .predio[data-predio="templo"]');
    const servico = await page.waitForSelector('.servico:has-text("Primeiro atendimento — grátis")', { timeout: 10000 }).catch(() => null);
    conferir(!!servico && /grátis/.test(await servico.textContent()), "no templo, o serviço diz \"Primeiro atendimento — grátis\"");
    await servico.click();
    await page.waitForFunction(() => estado.heroi.hp === estado.heroi.max_hp, null, { timeout: 10000 }).catch(() => {});
    conferir((await page.evaluate(() => estado.heroi.hp === estado.heroi.max_hp)) && (await page.evaluate(() => estado.heroi.ouro)) === ouro,
      "a cura grátis devolve a vida toda e não cobra");
    await (await page.waitForSelector(':is(button, .escolha):has-text("Voltar à vila")', { timeout: 10000 })).click();
    await page.waitForTimeout(1200);
    await page.click('#predios .predio[data-predio="mural"]');
    conferir(await ate(/^Aceite este contrato para começar\./) && (await pontaNoAlvo(page)) <= 2,
      "K1: no mural, \"Aceite este contrato para começar.\", com a seta encostando no cartão destacado");
    const id = await page.evaluate(() => estado.orientacao.atual.ancora.split(":")[1]);
    await page.click(`[data-aceitar="${id}"]`);
    await page.waitForTimeout(800);
    conferir(!/Aceite este contrato/.test(await quadro()) && (await page.evaluate(() => (estado.contratos || []).length)) === 1,
      "aceito o contrato, o quadro do mural sai");
    await page.keyboard.press("Escape");
    conferir(await ate(/^Clique neste contrato para viajar até .+\./) && (await pontaNoAlvo(page)) <= 2,
      "K2: na vila, o cartão do contrato à direita, com a seta encostando nele");
    await page.evaluate(() => { document.querySelector("#mundo").scrollTop += 60; });
    await page.waitForTimeout(400);
    conferir((await pontaNoAlvo(page)) <= 2, "rolando a coluna, o quadro acompanha o cartão");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioApresentacao(browser) {
  console.log("cenário: revelar o texto (A0) e a derrota na luta preparada do cenário tutorial");
  {
    const { proc, url } = await subir("tutorial", { VISTAS: "A1" });
    const { page, erros } = await abrir(browser, url);
    const quadro = () => page.evaluate(() => { const q = document.querySelector(".orientacao:not([hidden])"); return q ? q.innerText.replace(/\s+/g, " ") : ""; });
    try {
      await page.waitForFunction(() => pergunta && pergunta.tipo === "opcoes" && !processando, null, { timeout: 20000 });
      await page.keyboard.press("2");  // Examinar a fonte nova: texto e Continuar
      await page.waitForFunction(() => processando && !!document.querySelector(".orientacao:not([hidden])"), null, { timeout: 10000 }).catch(() => {});
      conferir(/^Clique para mostrar o texto inteiro\. Depois, use Continuar para avançar\./.test(await quadro()),
        "A0: com o texto correndo numa cena que acaba em Continuar, o quadro de revelar");
      const pg = await page.evaluate(() => { const r = document.querySelector("#pagina").getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
      await page.mouse.click(pg[0], pg[1]);  // na página (na paisagem, o clique escolheria um prédio)
      await page.waitForFunction(() => pergunta && pergunta.tipo === "continuar" && !processando, null, { timeout: 10000 });
      await page.waitForTimeout(300);
      conferir(/Clique para mostrar/.test(await quadro()) && (await pontaNoAlvo(page)) <= 2, "revelado o texto, o mesmo quadro aponta o Continuar");
      await page.click("#prompt .continuar");
      await page.waitForTimeout(1200);
      conferir(!/Clique para mostrar/.test(await quadro()) && !(await page.evaluate(() => "A0" in estado.orientacao.apresentacao)),
        "depois do Continuar, o A0 não volta");
    } finally {
      conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
      await page.close();
      proc.kill();
    }
  }
  {
    const { proc, url } = await subir("tutorial", { LUTA: "lobo", QUANTOS: "3", VIDA: "0.05", CONTRATO: "aceito", VISTAS: "A1" });
    const { page, erros } = await abrir(browser, url);
    try {
      let faixa = "", escuro = false, logs = false;
      for (let k = 0; k < 300; k++) {
        const s = await page.evaluate(() => ({ luta: !!(estado && estado.combate), pode: !!pergunta && !processando, menu: !!document.querySelector("#predios .predio") && !!pergunta && pergunta.tipo === "opcoes" && !processando,
          faixa: [...document.querySelectorAll(".faixa-festa")].map((f) => f.textContent.trim()).join("|"), escuro: document.body.classList.contains("derrotado") && !!estado && estado.heroi.hp === 0,
          logs: !!estado && !estado.combate && !!pergunta && pergunta.tipo === "continuar" && estado.heroi.hp === 0 }));
        if (s.faixa) faixa = faixa || s.faixa;
        escuro = escuro || s.escuro;
        logs = logs || s.logs;  // um Continuar com o herói ainda em 0: a página dos registros da luta segurando a tela
        if (s.menu && !s.luta && k > 5) break;
        const c = await page.$("#prompt .continuar");
        if (c) await c.click().catch(() => {});
        else if (s.luta && s.pode) {
          await page.keyboard.press("1");
          await page.waitForTimeout(150);
          const alvo = await page.$("#arena .carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
        }
        await page.waitForTimeout(200);
      }
      const fim = await page.evaluate(() => ({ local: estado.local.nome, contratos: (estado.contratos || []).length, hp: estado.heroi.hp, menu: !!pergunta && pergunta.tipo === "opcoes" }));
      conferir(fim.menu && fim.local === "Vau do Turvo" && fim.hp > 0 && fim.contratos === 1,
        "derrota na luta preparada: o resgate de sempre, de volta ao menu do Vau, com o contrato");
      conferir(faixa === "Você caiu" && escuro && !(await page.evaluate(() => document.body.classList.contains("derrotado"))),
        "a derrota: a faixa \"Você caiu\", o cenário escuro com o herói em 0 e, de volta ao menu, a luz de sempre");
      conferir(!logs && (await page.evaluate(() => /Você tombou diante de/.test(document.querySelector("#historico-lista").textContent))),
        "da queda direto ao resgate, sem um Continuar segurando os registros da luta (eles ficam no Histórico)");
    } finally {
      conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
      await page.close();
      proc.kill();
    }
  }
}

async function cenarioMercado(browser) {
  console.log("cenário: o mercado com abas e a banca (tela baixa, teclado, clique duplo, sair e voltar)");
  const { proc, url } = await subir("mercado", { MOCHILA: "11" });
  const page = await browser.newPage({ viewport: { width: 1280, height: 700 } });
  const erros = [];
  page.on("pageerror", (e) => erros.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
  await page.goto(url);
  const ate = async (f, ms = 10000) => { for (let t = 0; t < ms; t += 100) { if (await f()) return true; await page.waitForTimeout(100); } return false; };
  const parado = () => ate(() => page.evaluate(() => !processando && !!pergunta && pergunta.tipo === "opcoes"));
  try {
    await ate(() => page.$(".tela.loja")); await parado(); await page.waitForTimeout(600);
    // Só a lista rola: a página fica parada, com o ouro, as abas e o Sair à vista.
    const medidas = () => page.evaluate(() => {
      const pg = document.querySelector("#pagina"), vis = (s) => { const r = document.querySelector(s).getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight; };
      return { pagina: pg.scrollHeight - pg.clientHeight, abas: vis(".loja-abas"), ouro: vis(".ouro-loja"), sair: vis("#barra-tela .voltar-seta") };
    });
    await page.evaluate(() => { const l = document.querySelector('[data-lista="suprimentos"]'); l.scrollTop = l.scrollHeight; });
    const m = await medidas();
    conferir(m.pagina <= 1 && m.abas && m.ouro && m.sair, `em 1280×700, só a lista rola; abas, ouro e Sair à vista (${JSON.stringify(m)})`);
    // A banca é uma faixa em cima de tudo (em qualquer largura), em pixel inteiro, sem esticar o desenho.
    const fx = await page.evaluate(() => {
      const b = document.querySelector(".loja-banca").getBoundingClientRect(), t = document.querySelector(".loja-topo").getBoundingClientRect();
      const c = document.querySelector(".banca-cena"), r = c.getBoundingClientRect();
      return { acima: b.bottom <= t.top, larga: b.width > b.height * 4, escala: r.width / c.width, escalaV: r.height / c.height };
    });
    conferir(fx.acima && fx.larga && Math.abs(fx.escala - 2) < 0.02 && Math.abs(fx.escalaV - 2) < 0.02, `a banca é a faixa em cima, em pixel 2× (${JSON.stringify(fx)})`);
    // O esgotado diz por quê, por escrito (não só a cor).
    const esgotado = await page.evaluate(() => [...document.querySelectorAll(".mercadoria.suprimento.caro .merc-motivo")].map((e) => e.textContent).join(" | "));
    conferir(/Esgotado/.test(esgotado) || /Ouro insuficiente/.test(esgotado), `o que não se compra diz o motivo no cartão (${esgotado})`);
    conferir(!/reabastece/.test(esgotado), "no cartão, o esgotado diz só \"Esgotado\" (quando volta fica na dica)");
    // "Na bolsa" e "Estoque", cada um com o seu nome.
    const contas = await page.evaluate(() => document.querySelector('[data-comprar="tocha"] .merc-contas').textContent.replace(/\s+/g, " ").trim());
    conferir(/^Na bolsa: \d+ ?Estoque: \d+$/.test(contas), `o que você tem e o que o mercador tem, separados (${contas})`);
    // Enter num cartão compra a quantidade escolhida; o ouro e o "você tem" acompanham.
    const ouro = () => page.evaluate(() => App.estado.heroi.ouro);
    const o0 = await ouro();
    await page.focus('[data-comprar="tocha"]'); await page.keyboard.press("Enter"); await parado(); await page.waitForTimeout(300);
    conferir((await ouro()) < o0 && /Na bolsa: 4/.test(await page.evaluate(() => document.querySelector('[data-comprar="tocha"] .merc-contas').textContent)),
      "Enter no cartão compra; o ouro e o que você tem atualizam");
    // Clique duplo num item à venda vende um só (o que cai no lugar dele não vai junto).
    await page.click('.loja-aba[data-aba="vender"]');
    const mochila = () => page.evaluate(() => App.estado.heroi.mochila.length);
    const n0 = await mochila();
    const alvo = await page.$('[data-mochila-loja="0"]'); await alvo.scrollIntoViewIfNeeded();
    const bb = await alvo.boundingBox();
    await page.mouse.dblclick(bb.x + 20, bb.y + 20); await parado(); await page.waitForTimeout(700);
    conferir((await mochila()) === n0 - 1, `clique duplo vende um item só (${n0} → ${await mochila()})`);
    // Sair e voltar: a aba volta a Suprimentos e a recompra começa vazia.
    await page.keyboard.press("Escape");
    conferir(await ate(() => page.$('#predios .predio[data-predio="mercado"]'), 8000), "Esc sai do mercado para a vila");
    await page.waitForTimeout(600);
    await page.click('#predios .predio[data-predio="mercado"]');
    await ate(() => page.$(".tela.loja")); await parado();
    conferir(await page.evaluate(() => document.querySelector('.loja-aba[aria-selected="true"]').dataset.aba === "suprimentos" && !document.querySelector("[data-recomprar]")),
      "de volta ao mercado: aba Suprimentos, sem a recompra da visita anterior");
  } finally {
    conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
    await page.close();
    proc.kill();
  }
}

async function cenarioFeridas(browser) {
  console.log("cenário: ferimentos e descanso (F1, F2, a Curandeira com o primeiro tratamento grátis, D1)");
  const quadro = (page) => page.evaluate(() => { const q = document.querySelector(".orientacao:not([hidden])"); return q ? q.innerText.replace(/\s+/g, " ") : ""; });
  const ate = async (page, re, ms = 15000) => { for (let k = 0; k < ms; k += 150) { if (re.test(await quadro(page))) return true; await page.waitForTimeout(150); } return false; };
  {
    const { proc, url } = await subir("tutorial", { LUGAR: "charco", VISTAS: "A1,A0,AL,N1,V5", FERIMENTOS: "corte", BANDAGENS: "2", VIDA: "0.5" });
    const { page, erros } = await abrir(browser, url);
    try {
      conferir(await ate(page, /^Corte profundo −10% de vida máxima\. Precisa de descanso ou tratamento para sarar\./) && (await pontaNoAlvo(page)) <= 2,
        "F1: o nome, o efeito real e o que faz sarar, a seta no ferimento");
      await page.click(".orientacao-entendi");
      await page.click('#doca .atalho[data-rotulo="Inventário"]');
      await page.waitForTimeout(600);
      await page.keyboard.press("Escape");
      conferir(await ate(page, /^A bandagem protege a ferida contra infecção\. O ferimento ainda precisa sarar\./) && (await pontaNoAlvo(page)) <= 2,
        "F2: na cena seguinte, a bandagem da bolsa");
      // O clique só vale com o menu aceitando o uso (sem cena correndo): sob carga, ele espera a vez em vez de cair
      // no "Agora não".
      for (let k = 0; k < 8 && (await page.evaluate(() => estado.heroi.bandagens)) === 2; k++) {
        await page.waitForFunction(() => !processando && pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => o.meta && o.meta.usar === "bandagem"), null, { timeout: 10000 }).catch(() => {});
        await page.click('#heroi .slot-px[data-bolsa="bandagem"]');
        await page.waitForTimeout(700);
      }
      await page.waitForFunction(() => estado.heroi.ferimentos.every((f) => !f.aberto), null, { timeout: 10000 }).catch(() => {});
      conferir(await page.evaluate(() => !/aberto/.test(document.querySelector("#heroi .ferimento").textContent)) && !/bandagem protege/.test(await quadro(page)),
        "usada a bandagem, a ficha mostra a ferida tratada e o quadro sai");
      const vidaAntes = await page.evaluate(() => estado.heroi.hp);
      const slot = await page.evaluate(() => { const e = document.querySelector('#heroi .slot-px[data-bolsa="bandagem"]'); return e && { inutil: e.classList.contains("inutil"), trata: e.classList.contains("trata") }; });
      conferir(slot && slot.inutil && !slot.trata, "enfaixada a única ferida aberta, a bandagem fica à vista, apagada e sem pulsar");
      await page.click('#heroi .slot-px[data-bolsa="bandagem"]');
      await page.waitForTimeout(500);
      const depois = await page.evaluate(() => ({ qtd: estado.heroi.bandagens, hp: estado.heroi.hp, aviso: [...document.querySelectorAll(".aviso-flutuante")].map((e) => e.textContent).join(" ") }));
      conferir(depois.qtd === 1 && depois.hp === vidaAntes && /Nenhuma ferida aberta para enfaixar/.test(depois.aviso),
        "o clique na bandagem sem ferida diz o motivo e não gasta nada (nem cura vida)");
    } finally {
      conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
      await page.close();
      proc.kill();
    }
  }
  {
    const { proc, url } = await subir("tutorial", { VISTAS: "A1,A0,F1,F2", FERIMENTOS: "corte,costelas", OURO: "0" });
    const { page, erros } = await abrir(browser, url);
    try {
      conferir(await ate(page, /^A Curandeira trata ferimentos na hora; o Templo só recupera vida\./) && (await pontaNoAlvo(page)) <= 2,
        "F3: na vila, a Curandeira (e o Templo só recupera vida)");
      await page.click('#predios .predio[data-predio="curandeiro"]');
      conferir(await ate(page, /^Clique neste cartão para tratar o corte\./) && !/grátis/.test(await quadro(page)),
        "F4: o cartão do ferimento (o grátis fica no cartão, não no quadro)");
      const gratis = await page.evaluate(() => [...document.querySelectorAll("#texto .curandeira [data-tratar]")].map((c) => /Primeiro tratamento — grátis/.test(c.textContent)));
      await page.click('#texto .curandeira [data-tratar="costelas"] >> nth=-1');
      await page.waitForFunction(() => estado.heroi.ferimentos.length === 1 && !!document.querySelector("#texto .curandeira [data-tratar]") && !!pergunta && !processando, null, { timeout: 15000 }).catch(() => {});
      const depois = await page.evaluate(() => ({ ouro: estado.heroi.ouro, cartao: [...document.querySelectorAll("#texto .curandeira [data-tratar]")].pop().textContent }));
      conferir(gratis.length === 2 && gratis.every(Boolean) && depois.ouro === 0 && !/grátis/.test(depois.cartao) && /15/.test(depois.cartao),
        "com zero de ouro: um tratamento grátis, e o outro cartão volta ao preço de sempre na mesma tela");
    } finally {
      conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
      await page.close();
      proc.kill();
    }
  }
  {
    const { proc, url } = await subir("tutorial", { VIDA: "0.5", REC: "0.2", VISTAS: "A1,A0,AL", OURO: "40" });
    const { page, erros } = await abrir(browser, url);
    try {
      await page.waitForFunction(() => pergunta && pergunta.tipo === "opcoes" && !processando && document.querySelector('#predios .predio[data-predio="taverna"]'), null, { timeout: 20000 });
      await page.waitForTimeout(600);
      await page.click('#predios .predio[data-predio="taverna"]');
      const d1 = await ate(page, /^Clique neste cartão para dormir aqui até o amanhecer\./) && (await pontaNoAlvo(page)) <= 2;
      const cartao = await page.evaluate(() => [...document.querySelectorAll('.servico[data-servico="dormir"] .serv-linha')].map((l) => l.textContent.replace(/\s+/g, " ").trim()));
      conferir(d1 && JSON.stringify(cartao) === JSON.stringify(["Custo: 10 ouro", "Recuperação: +21 vida · Vigor completo", "Provisões: nenhuma consumida"]),
        "D1: na taverna, o quadro diz a ação; o cartão Dormir, o custo, a recuperação e as provisões das regras");
      await page.click('.servico[data-servico="dormir"]');
      await page.waitForFunction(() => estado.heroi.hp === 51 && estado.heroi.rec === estado.heroi.max_rec, null, { timeout: 30000 }).catch(() => {});
      conferir(await page.evaluate(() => estado.heroi.hp === 51 && estado.heroi.rec === estado.heroi.max_rec), "dormir devolve exatamente o que o quadro disse (30 → 51 de vida, todo o Vigor)");
    } finally {
      conferir(erros.length === 0, "sem erros no console" + (erros.length ? ": " + erros.slice(0, 3).join(" | ") : ""));
      await page.close();
      proc.kill();
    }
  }
}

async function cenarioAnimacao(browser) {
  console.log("cenário: o quadro de acelerar a animação (AL), com Entendi pelo teclado");
  const { proc, url } = await subir("tutorial", { LUTA: "lobo", QUANTOS: "2", VISTAS: "A1,A0" });
  const { page, erros } = await abrir(browser, url);
  try {
    await page.waitForFunction(() => pergunta && !processando && document.querySelector("#roda .roda-botao"), null, { timeout: 20000 });
    await page.keyboard.press("1");
    await page.waitForTimeout(200);
    await (await page.$("#arena .carta.alvejavel"))?.click();
    await page.waitForFunction(() => /acelerar a animação/.test((document.querySelector(".orientacao:not([hidden])") || {}).textContent || ""), null, { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(150);  // o foco vai para o Entendi no quadro seguinte da tela
    const antes = await page.evaluate(() => ({ foco: document.activeElement && document.activeElement.className, turno: estado.combate.turno }));
    conferir(antes.foco === "orientacao-entendi", "AL: com a vez dos lobos correndo, o quadro com Entendi (o foco nele)");
    await page.keyboard.press("Enter");
    await page.waitForFunction(() => pergunta && !processando, null, { timeout: 15000 });
    await page.waitForTimeout(500);
    const depois = await page.evaluate(() => ({ q: !!document.querySelector(".orientacao:not([hidden])"), turno: estado.combate.turno, ap: "AL" in estado.orientacao.apresentacao, perg: pergunta.tipo }));
    conferir(!depois.q && !depois.ap && depois.turno === antes.turno + 1 && depois.perg === "opcoes",
      "Enter no Entendi fecha só o quadro: a vez do herói chega normalmente, sem ação escolhida, e ele não volta");
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
  const baus = () => page.evaluate(() => (App.estado.heroi.bolsa.find((b) => b.id === "bau") || { qtd: 0 }).qtd);
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
    const naBolsa = await baus();
    await pilha.click(); await pilha.click().catch(() => {});  // dois cliques rápidos na pilha
    const continuar = await esperar(".festa-espolio .continuar", 20000);
    const resumo = await page.evaluate(() => ({ qtd: document.querySelector(".festa-espolio .eb-qtd")?.textContent,
      icones: document.querySelectorAll(".festa-espolio .eb-pilha > span").length,
      equips: [...document.querySelectorAll(".festa-espolio .equip-espolio")].map((x) => x.textContent) }));
    conferir(!!continuar && naBolsa === 3 && resumo.qtd === `×${naBolsa}` && resumo.icones === naBolsa,
      `a pilha abre num quadro só, com a pilha e o ×N dos baús que saíram (${resumo.qtd}, ${resumo.icones} ícones, ${naBolsa} na bolsa)`);
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
  await cenarioMercado(browser);
  await cenarioCampanha(browser);
  await cenarioMissao(browser);
  await cenarioRecarga(browser);
  await cenarioCapela(browser);
  await cenarioSarilho(browser);
  await cenarioCapelaFora(browser);
  await cenarioCapelaSalas(browser);
  await cenarioCustosEExausto(browser);
  await cenarioGuardia(browser);
  await cenarioRetorno(browser);
  await cenarioCaspar(browser);
  await cenarioResgate(browser);
  await cenarioYara(browser);
  await cenarioBroquel(browser);
  await cenarioGolpePreparado(browser);
  await cenarioEncruzilhada(browser);
  await cenarioTiroDuplo(browser);
  await cenarioBaus(browser);
  await cenarioAbertura(browser);
  await cenarioFogueira(browser);
  await cenarioTutorial(browser);
  await cenarioCiclos(browser);
  await cenarioApresentacao(browser);
  await cenarioAnimacao(browser);
  await cenarioFeridas(browser);
} catch (e) {
  falhas.push(String(e));
  console.log("ERRO", e);
} finally {
  await browser.close();
}
console.log(falhas.length ? `${falhas.length} falha(s)` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
