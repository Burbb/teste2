// Os comandos da luta e a amostra da exploração na linguagem do seletor D refinado (protótipo, comandos/): o jogo como
// está e as propostas, com os mesmos dados (um jogo novo com a mesma semente para cada foto). O jogo não muda: a página
// da proposta recebe as folhas de comandos/ por cima e, para a amostra, a cópia do escolhas.js com a troca de
// comandos/comandos.mjs.
// As versões:
//   atual      o jogo de hoje;
//   comandos   os comandos novos com as cartas de hoje (comandos.css);
//   cartas     os comandos novos e o acabamento contido das cartas (comandos.css + cartas.css);
//   (a exploração: atual e "comandos", que leva exploracao.css)
// As lutas (cenário tutorial, contra lobos de nível 9, depois de uma rodada de Atacar para o registro real ficar por
// baixo; o herói no nível 12):
//   dia      Guerreiro berserker com Morel e Odette, 3 lobos, no Vau de manhã (o cenário claro);
//   noite    Mago necromante com Morel e Odette, 3 lobos, no Charco à noite (o escuro);
//   arqueiro Arqueiro sombra com Morel, 2 lobos, no Bosque à tarde (os nomes e o custo em flechas no seletor).
// A exploração (cenário tutorial e covil, sem luta):
//   bosque   o Bosque de dia, com Morel (Explorar, Acampar, Viajar);
//   charco   o Charco à noite, com um contrato aceito ali (o grupo Contratos e "à noite é mais perigoso");
//   capela   a Capela Afogada à noite, por fora: a ação da missão com os riscos da tocha e da noite (duas linhas);
//   covil    o covil de um guardião ainda vivo, à tarde: "Enfrentar Sarric, o Profeta das Cinzas (guardião)", o texto real
//            mais longo desse menu (a fonte pixel não entra: vai sair do jogo);
//   esforco  o mesmo covil com a primeira opção alongada só na página da foto (TESTE DE ESFORÇO, texto que o jogo não
//            tem): nenhum texto real dessa tela quebra de linha nas janelas conferidas, e a quebra precisa ser vista.
// Em 1500×950, 1280×720 e 1920×1080. Na luta, cada versão: a tela inteira; a roda parada; o mouse em Atacar; o
// pressionado; o foco do teclado (Tab até Atacar); Habilidades aberto; o foco e o aberto juntos (Shift+Tab de volta ao
// botão com o seletor aberto); Itens aberto (alternar); a escolha de uma habilidade de um alvo → a mira → Voltar. Mede se
// abrir mexe nas cartas ou na rolagem, se a roda cobre carta, o tempo até o clique valer, e os efeitos que passam da
// moldura (a carta ampliada, os números). Na luta do dia em 1500×950: cinco cliques depressa, a tecla segurada, o
// clique durante a entrada, Habilidades ↔ Itens depressa e o movimento reduzido.
// Guarda em capturas-comandos/ (relatorio.json com as medidas); comparar_comandos.py monta as comparações.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_comandos.mjs
// (VERSOES=atual,comandos,cartas, LUTAS=dia,noite,arqueiro, EXPLORA=bosque,charco,capela,covil,esforco, JANELAS=normal,baixa,grande (a luta), JANELAS_EXPLORA=normal,baixa,grande,escala,
// SAIDA=<pasta>; PYTHON=<executável> troca o Python que sobe os cenários)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
import { escolhas, ponte } from "./comandos/comandos.mjs";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-comandos"));
if (!process.env.MANTER) rmSync(SAIDA, { recursive: true, force: true });  // MANTER=1: refaz só as fotos pedidas, sem apagar as outras
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const filtro = (nome, todos) => (process.env[nome] ? process.env[nome].split(",") : todos);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");

const PASTA = path.join(aqui, "comandos");
const PONTE = ponte(readFileSync(path.join(raiz, "rpg/web/static/css/18-seletor-habilidades.css"), "utf8"));
const ESCOLHAS = escolhas(readFileSync(path.join(raiz, "rpg/web/static/app/escolhas.js"), "utf8"));
const FOLHAS = { atual: [], comandos: ["comandos.css", "exploracao.css"], cartas: ["comandos.css", "exploracao.css", "cartas.css"] };
const VERSOES = filtro("VERSOES", ["atual", "comandos", "cartas"]);
// "escala": 1280×720 com a escala de 125% do Windows (a página tem 1024×576 px de CSS): só com JANELAS=...,escala
const JANELAS = Object.entries({ normal: [1500, 950], baixa: [1280, 720], grande: [1920, 1080], escala: [1024, 576] }).filter(([j]) => filtro("JANELAS", ["normal", "baixa", "grande"]).includes(j));
const ESCALA = { escala: { deviceScaleFactor: 1.25 } };
// a exploração também em "escala" (por padrão): é onde a opção longa quebra de linha naturalmente
const JANELAS_EXPLORA = Object.entries({ normal: [1500, 950], baixa: [1280, 720], grande: [1920, 1080], escala: [1024, 576] }).filter(([j]) => filtro("JANELAS_EXPLORA", ["normal", "baixa", "grande", "escala"]).includes(j));
const VISTAS = "A1,V2,N1,D1,K1,M1,L1";
const LUTA = { TUTORIAL: "0", LUTA: "lobo", NIVEL: "12", NIVEL_LUTA: "9", VISTAS, REC: "0.5" };
const TODAS_LUTAS = {
  dia: { ...LUTA, CLASSE: "guerreiro", ESPEC: "berserker", COMITIVA: "morel,odete", QUANTOS: "3", LUGAR: "vau", PERIODO: "0", REC: "0" },
  noite: { ...LUTA, CLASSE: "mago", ESPEC: "necromante", COMITIVA: "morel,odete", QUANTOS: "3", LUGAR: "charco", PERIODO: "3", REC: "0.12" },
  arqueiro: { ...LUTA, CLASSE: "arqueiro", ESPEC: "sombra", COMITIVA: "morel", QUANTOS: "2", LUGAR: "bosque", PERIODO: "2", REC: "0" },
};
const LUTAS = Object.entries(TODAS_LUTAS).filter(([l]) => filtro("LUTAS", Object.keys(TODAS_LUTAS)).includes(l));
const TODAS_EXPLORA = {
  bosque: ["tutorial", { TUTORIAL: "0", VISTAS, COMITIVA: "morel", LUGAR: "bosque", PERIODO: "0" }],
  charco: ["tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "charco", PERIODO: "3", CONTRATO: "aceito", CONTRATO_EM: "charco" }],
  capela: ["capela", { ETAPA: "capela", PERIODO: "3", TOCHAS: "2" }],
  covil: ["covil", { PERIODO: "1" }],
  esforco: ["covil", { PERIODO: "1" }, "Enfrentar Sarric, o Profeta das Cinzas (guardião), que guarda o covil desde a queda da cidadela e não aceita rendição"],
};
const EXPLORA = Object.entries(TODAS_EXPLORA).filter(([l]) => filtro("EXPLORA", Object.keys(TODAS_EXPLORA)).includes(l));
const UM_ALVO = ["bola_fogo", "comando_fera", "combustao", "drenar_vida", "execucao", "fenix", "flecha_envenenada", "furia_cega",
  "golpe_pesado", "golpe_sagrado", "investida", "lanca_gelo", "marcar_presa", "sede_sangue", "tiro_certeiro", "tiro_duplo"];

async function subir(cenario, amb) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const relatorio = [], comportamentos = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, [W, H], versao, nome, opcoes = {}) {
  const p = await b.newPage({ viewport: { width: W, height: H }, ...opcoes });
  if (versao !== "atual") await p.route(/\/static\/app\/escolhas\.js(\?|$)/, (r) => r.fulfill({ body: ESCOLHAS, contentType: "application/javascript" }));
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  if (versao !== "atual") {
    await p.addStyleTag({ content: PONTE });
    for (const f of FOLHAS[versao]) await p.addStyleTag({ path: path.join(PASTA, f) });
  }
  return p;
}
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="habilidades"]'));
async function vez(p) {
  for (let k = 0; k < 200; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
const noMenu = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && pergunta.tipo === "opcoes" && !!document.querySelector("#prompt .escolha"));
async function menu(p) {
  for (let k = 0; k < 120; k++) {
    if (await noMenu(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("o menu do lugar não chegou");
}
async function rodada(p, foto) {  // uma rodada de Atacar: o registro real por baixo; foto(): o golpe no meio
  await (await p.$('#roda .roda-botao[data-slot="atacar"]')).click();
  for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
  const alvo = await p.$("#batalha .carta.alvejavel");
  if (alvo) await alvo.click();
  if (foto) { await espera(260); await foto(); }
  await espera(500);
  await vez(p);
}
async function recortar(p, sels, nome, folga = 10) {
  const c = await p.evaluate(([ss, f]) => {
    const rs = ss.flatMap((s) => [...document.querySelectorAll(s)]).filter((e) => e.getClientRects().length && getComputedStyle(e).visibility !== "hidden")
      .map((e) => e.getBoundingClientRect()).filter((r) => r.width);
    if (!rs.length) return null;
    const x0 = Math.max(0, Math.min(...rs.map((r) => r.left)) - f), y0 = Math.max(0, Math.min(...rs.map((r) => r.top)) - f);
    return { x: Math.floor(x0), y: Math.floor(y0), width: Math.ceil(Math.min(innerWidth, Math.max(...rs.map((r) => r.right)) + f) - x0),
      height: Math.ceil(Math.min(innerHeight, Math.max(...rs.map((r) => r.bottom)) + f) - y0) };
  }, [[].concat(sels), folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
}
// o lugar das cartas e a rolagem de tudo o que rola: abrir e fechar o seletor não pode mexer nisso
const disposicao = (p) => p.evaluate(() => JSON.stringify({
  cartas: [...document.querySelectorAll("#batalha .carta")].map((c) => { const r = c.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width)]; }),
  rolagem: [document.scrollingElement, ...document.querySelectorAll("*")].filter((e) => e && e.scrollTop > 0).map((e) => `${e.id || e.className}:${Math.round(e.scrollTop)}`),
}));
// o que mudou entre duas disposições (as cartas que andaram, as rolagens diferentes)
function diferenca(a, b) {
  if (a === b) return "nada se mexe";
  const A = JSON.parse(a), B = JSON.parse(b), d = [];
  A.cartas.forEach((c, i) => { if (JSON.stringify(c) !== JSON.stringify(B.cartas[i])) d.push(`carta ${i}: ${c} → ${B.cartas[i]}`); });
  if (JSON.stringify(A.rolagem) !== JSON.stringify(B.rolagem)) d.push(`rolagem: ${A.rolagem} → ${B.rolagem}`);
  return "MUDOU: " + d.join("; ");
}
// a roda: o tamanho de cada comando, se algum cobre uma carta, se algum nome é cortado, se passa da arena
const medirRoda = (p) => p.evaluate(() => {
  const arena = document.getElementById("roda").getBoundingClientRect();
  const bs = [...document.querySelectorAll("#roda .roda-botao")];
  const cartas = [...document.querySelectorAll("#batalha .carta")].map((c) => [c.querySelector(".carta-nome")?.textContent.trim(), c.getBoundingClientRect()]);
  const cobre = [];
  for (const bt of bs) {
    const r = bt.getBoundingClientRect();
    for (const [n, c] of cartas) if (r.right > c.left + 1 && r.left < c.right - 1 && r.bottom > c.top + 1 && r.top < c.bottom - 1) cobre.push(`${bt.dataset.slot}×${n}`);
  }
  // a menor folga horizontal entre um comando e uma carta inimiga na mesma altura
  const folgas = [];
  for (const bt of bs) { const r = bt.getBoundingClientRect(); for (const c of document.querySelectorAll("#batalha .carta.inimigo")) { const q = c.getBoundingClientRect(); if (r.bottom > q.top && r.top < q.bottom) folgas.push(Math.round(q.left - r.right)); } }
  return { folga_inimigos: folgas.length ? Math.min(...folgas) + " px" : "nenhuma na mesma altura", comandos: bs.map((bt) => { const r = bt.getBoundingClientRect(); return `${bt.dataset.slot} ${Math.round(r.width)}×${Math.round(r.height)}`; }).join(", "),
    cobre_carta: cobre.length ? cobre.join(", ") : "nenhuma",
    fora_da_arena: bs.filter((bt) => { const r = bt.getBoundingClientRect(); return r.right > arena.right + 0.5 || r.bottom > arena.bottom + 0.5 || r.top < arena.top - 0.5; }).map((bt) => bt.dataset.slot).join(", ") || "nenhum",
    cortados: bs.map((bt) => bt.querySelector(".rb-nome")).filter((e) => e && e.scrollWidth > e.clientWidth + 1).map((e) => e.textContent).join(", ") || "nenhum" };
});
const focado = (p) => p.evaluate(() => { const a = document.activeElement; return a === document.body ? "nada (body)" : `${a.className.split(" ")[0]}${a.dataset.slot ? "[" + a.dataset.slot + "]" : ""}: ${a.textContent.trim().slice(0, 30)}`; });
const slot = (p, s) => p.$(`#roda .roda-botao[data-slot="${s}"]`);
const recRoda = ["#roda .roda-botao", '#batalha .carta[data-uid="j"]'];

for (const [luta, amb] of LUTAS) {
  for (const [jan, tam] of JANELAS) for (const versao of VERSOES) {
    const H = tam[1], n = (c) => `${jan}-${luta}-${versao}-${c}`, r = { nome: `${jan}-${luta}-${versao}` };
    const { proc, url } = await subir("tutorial", amb);
    try {
      const p = await pagina(url, tam, versao, r.nome, ESCALA[jan]);
      await vez(p);
      // o golpe no meio: o número de dano e o efeito passam da moldura da arena (precisam continuar à vista)
      await rodada(p, () => recortar(p, ["#arena"], n("0-golpe"), 40));
      await p.mouse.move(5, H - 5);
      await espera(800);
      // 1. a tela inteira e a roda parada
      await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
      await recortar(p, ["#arena"], n("arena"), 2);
      await recortar(p, recRoda, n("1-normal"));
      Object.assign(r, await medirRoda(p));
      // 2. o mouse em Atacar (a dica do jogo) e o pressionado (solta fora: nada acontece)
      const atk = await slot(p, "atacar");
      await atk.hover(); await espera(500);
      await recortar(p, recRoda, n("2-mouse"));
      await p.mouse.down(); await espera(120);
      await recortar(p, recRoda, n("3-pressionado"));
      await p.mouse.move(5, H - 5); await p.mouse.up(); await espera(250);
      r.soltar_fora = (await naVez(p)) && !(await p.$(".roda-mira")) ? "nada escolhido" : "ERRO";
      // 3. o foco real do teclado: Tab até Atacar (o clique do pressionado deixou o foco de mouse nele: sai antes)
      await p.evaluate(() => document.activeElement && document.activeElement.blur());
      for (let k = 0; k < 40 && !(await p.evaluate(() => document.activeElement?.dataset?.slot === "atacar")); k++) await p.keyboard.press("Tab");
      r.tab_chega = `${await focado(p)} (${await p.evaluate(() => document.activeElement.matches(":focus-visible") ? "foco visível" : "SEM foco visível")})`;
      await espera(200);
      await recortar(p, recRoda, n("4-foco"));
      // (a referência das cartas e das rolagens: depois do Tab, que rola o painel do herói ao passar por ele)
      const antes = await disposicao(p);
      // 4. Habilidades aberto pelo clique; depois o foco no botão com o menu aberto (Shift+Tab a partir da faixa)
      await p.mouse.move(5, H - 5);
      await (await slot(p, "habilidades")).click(); await espera(450);
      await p.mouse.move(5, H - 5); await espera(200);
      r.abrir_mexe = diferenca(antes, await disposicao(p));
      await recortar(p, [...recRoda, ".roda-janela"], n("5-aberto"));
      await p.screenshot({ path: path.join(SAIDA, `${n("tela-aberto")}.png`) });
      await (await slot(p, "habilidades")).focus();
      await p.keyboard.press("Shift"); await espera(200);  // um gesto de teclado: o foco passa a contar como do teclado
      r.foco_e_aberto = await p.evaluate(() => { const a = document.activeElement; return `${a.dataset.slot} focado (${a.matches(":focus-visible") ? "foco visível" : "sem foco visível"}), ${a.classList.contains("ativo") ? "aberto" : "fechado"}`; });
      await recortar(p, recRoda, n("6-foco-aberto"));
      // 5. alternar: Itens com Habilidades aberto troca o menu; Itens de novo fecha
      await (await slot(p, "itens")).click(); await espera(450);
      await p.mouse.move(5, H - 5); await espera(200);
      r.alternar = `${await p.$eval(".roda-janela", (j) => j.dataset.tipo).catch(() => "nenhum")} aberto, ${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es)`;
      await recortar(p, [...recRoda, ".roda-janela"], n("7-itens"));
      await (await slot(p, "itens")).click(); await espera(300);
      r.fechar_itens = (await p.$(".roda-janela")) ? "AINDA ABERTO" : "fechado";
      r.fechar_mexe = diferenca(antes, await disposicao(p));
      // 6. a escolha: uma habilidade de um alvo → a mira; o Voltar devolve a roda
      await (await slot(p, "habilidades")).click(); await espera(450);
      const hab = await p.evaluate((um) => (document.querySelector(`.roda-janela .rj-linha:not(.bloqueada)${um.map((h) => `[data-hab="${h}"]`).join(", .roda-janela .rj-linha:not(.bloqueada)")}`) || {}).dataset?.hab || null, UM_ALVO);
      if (hab) {
        await (await p.$(`.roda-janela .rj-linha[data-hab="${hab}"]`)).click(); await espera(900);
        await p.mouse.move(5, H - 5); await espera(250);
        r.escolha = `${hab} → ${(await p.$(".roda-mira")) ? "mira" : "sem mira"}; comandos na tela: ${await p.$$eval("#roda .roda-botao", (x) => x.length)}`;
        await recortar(p, ["#arena"], n("8-mira"), 2);
        const v = await p.$(".mira-voltar");
        if (v) await v.click(); else await p.keyboard.press("Escape");
        await vez(p); await espera(400);
        r.voltar = (await slot(p, "habilidades")) && !(await p.$(".roda-janela")) ? "a roda de volta" : "ERRO";
        r.voltar_mexe = diferenca(antes, await disposicao(p));
        await recortar(p, recRoda, n("9-volta"));
      } else r.escolha = "nenhuma habilidade de um alvo disponível";
      relatorio.push(r);
      console.log(JSON.stringify(r));
      await p.close();
    } finally { proc.kill(); }
  }

  // Os comportamentos (a luta do dia, 1500×950): depressa, tecla segurada, clique na entrada, alternar, movimento reduzido
  if (luta === "dia") for (const versao of VERSOES) {
    const c = { versao }, tam = [1500, 950];
    const { proc, url } = await subir("tutorial", amb);
    try {
      let p = await pagina(url, tam, versao, `comportamentos-${versao}`);
      await vez(p); await espera(500);
      const hb = await slot(p, "habilidades");
      for (let k = 0; k < 5; k++) { await hb.click(); await espera(40); }
      await espera(300);
      c.depressa = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es) depois de 5 cliques (esperado 1)`;
      await p.keyboard.press("Escape"); await espera(300);
      await p.keyboard.down("2"); for (let k = 0; k < 6; k++) { await espera(35); await p.keyboard.down("2"); } await p.keyboard.up("2"); await espera(300);
      c.tecla_segurada = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es) (esperado 1)`;
      await p.keyboard.press("Escape"); await espera(300);
      // Habilidades ↔ Itens depressa: termina com um seletor só, o do último
      for (const s of ["habilidades", "itens", "habilidades", "itens"]) { await (await slot(p, s)).click(); await espera(30); }
      await espera(300);
      c.alternar_depressa = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es), ${await p.$eval(".roda-janela", (j) => j.dataset.tipo).catch(() => "nenhum")} (esperado 1, itens)`;
      await p.keyboard.press("Escape"); await espera(300);
      // o primeiro quadro: o clique 20 ms depois de a roda aparecer vale (sem espera para aceitar)
      await (await slot(p, "habilidades")).click(); await espera(400);
      const hab = await p.evaluate((um) => (document.querySelector(`.roda-janela .rj-linha:not(.bloqueada)${um.map((h) => `[data-hab="${h}"]`).join(", .roda-janela .rj-linha:not(.bloqueada)")}`) || {}).dataset?.hab || null, UM_ALVO);
      await (await p.$(`.roda-janela .rj-linha[data-hab="${hab}"]`)).click(); await espera(900);
      const v = await p.$(".mira-voltar"); if (v) await v.click();
      for (let k = 0; k < 100 && !(await slot(p, "atacar")); k++) await espera(10);
      await espera(20);
      await p.evaluate(() => document.querySelector('#roda .roda-botao[data-slot="habilidades"]').click());
      await espera(250);
      c.clique_na_entrada = (await p.$(".roda-janela")) ? "aceito (20 ms depois de a roda voltar)" : "PERDIDO";
      await p.keyboard.press("Escape"); await espera(300);
      // a entrada fotografada no meio (40 ms)
      await (await slot(p, "habilidades")).click();
      await (await p.$(".mira-voltar"))?.click();
      await p.keyboard.press("Escape"); await espera(300);
      await p.close();
      p = await pagina(url, tam, versao, `entrada-${versao}`);
      await vez(p);
      await recortar(p, recRoda, `comportamento-${versao}-entrada`);
      await p.close();
      p = await pagina(url, tam, versao, `reduzido-${versao}`, { reducedMotion: "reduce" });
      await vez(p);
      await recortar(p, recRoda, `comportamento-${versao}-reduzido-entrada`);
      const atk = await slot(p, "atacar");
      await atk.hover(); await p.mouse.down(); await espera(100);
      c.reduzido_pressionado = await p.evaluate(() => getComputedStyle(document.querySelector('#roda .roda-botao[data-slot="atacar"]')).translate);
      c.reduzido_animacao = await p.evaluate(() => getComputedStyle(document.querySelector('#roda .roda-botao[data-slot="atacar"]')).animationName);
      await recortar(p, recRoda, `comportamento-${versao}-reduzido-pressionado`);
      await p.mouse.move(5, 940); await p.mouse.up();
      await p.close();
      comportamentos.push(c);
      console.log(JSON.stringify(c));
    } finally { proc.kill(); }
  }
}

// A exploração: atual × amostra, nas mesmas janelas
for (const [lugar, [cenario, amb, alongar]] of EXPLORA) {
  for (const [jan, tam] of JANELAS_EXPLORA) for (const versao of VERSOES.filter((v) => v !== "cartas")) {
    const H = tam[1], n = (c) => `${jan}-explora-${lugar}-${versao}-${c}`, r = { nome: `${jan}-explora-${lugar}-${versao}` };
    const { proc, url } = await subir(cenario, amb);
    try {
      const p = await pagina(url, tam, versao, r.nome, ESCALA[jan]);
      await menu(p);
      if (alongar) await p.evaluate((t) => { document.querySelector("#prompt .escolha .op-texto").textContent = t; }, alongar);
      await p.mouse.move(5, H - 5);
      await espera(800);
      await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
      await recortar(p, ["#prompt"], n("1-normal"));
      Object.assign(r, await p.evaluate(() => {
        const l = document.querySelector("#prompt .escolhas"), bs = [...l.querySelectorAll(".escolha")];
        const alt = (e) => Math.round(e.getBoundingClientRect().height);
        return { amostra: l.classList.contains("amostra-faixas"), opcoes: bs.map((e) => `${e.querySelector(".op-texto")?.textContent.trim()} (${alt(e)} px${e.querySelector(".op-texto").getClientRects().length > 1 ? ", " + e.querySelector(".op-texto").getClientRects().length + " linhas" : ""})`),
          fonte: getComputedStyle(bs[0]).fontSize,
          cortados: bs.map((e) => e.querySelector(".rotulo")).filter((e) => e.scrollWidth > e.clientWidth + 1).length,
          sobrepostas: bs.some((e, i) => i && e.getBoundingClientRect().top < bs[i - 1].getBoundingClientRect().bottom - 0.5) };
      }));
      const bs = await p.$$("#prompt .escolha");
      // o mouse na mais alta (a de duas linhas, quando há) e na primeira; o pressionado; o foco pelo teclado
      const alta = await p.evaluate(() => { const bs = [...document.querySelectorAll("#prompt .escolha")]; let k = 0; bs.forEach((e, i) => { if (e.offsetHeight > bs[k].offsetHeight) k = i; }); return k; });
      await bs[alta].hover(); await espera(400);
      await recortar(p, ["#prompt"], n("2-mouse"));
      await p.mouse.down(); await espera(120);
      await recortar(p, ["#prompt"], n("3-pressionado"));
      await p.mouse.move(5, H - 5); await p.mouse.up(); await espera(300);
      r.soltar_fora = (await noMenu(p)) ? "nada escolhido" : "ERRO";
      await p.evaluate(() => document.activeElement && document.activeElement.blur());
      for (let k = 0; k < 40 && !(await p.evaluate(() => !!document.activeElement.closest("#prompt .escolha"))); k++) await p.keyboard.press("Tab");
      await p.keyboard.press("ArrowDown").catch(() => {});
      r.foco = await focado(p);
      await recortar(p, ["#prompt"], n("4-foco"));
      // a área de clique: o meio da faixa de cada opção é a própria opção (nada de vão ambíguo entre elas)
      // (só as opções inteiras na área da página que se vê: a que está atrás da doca ou abaixo da dobra é alcançada rolando)
      r.clique = await p.evaluate(() => {
        const pg = document.getElementById("pagina").getBoundingClientRect(), doca = document.getElementById("doca")?.getBoundingClientRect();
        const pe = Math.min(pg.bottom, innerHeight, doca && doca.height ? doca.top : Infinity);  // a área da página que se vê (acima da doca)
        const vistas = [...document.querySelectorAll("#prompt .escolha")].filter((e) => { const q = e.getBoundingClientRect(); return q.top >= pg.top && q.bottom <= pe; });
        const ruins = vistas.filter((e) => { const q = e.getBoundingClientRect(); return ![[0.5, 0.5], [0.08, 0.5], [0.95, 0.5], [0.5, 0.1], [0.5, 0.9]].every(([fx, fy]) => document.elementFromPoint(q.left + q.width * fx, q.top + q.height * fy)?.closest(".escolha") === e); });
        return `${vistas.length - ruins.length} de ${vistas.length} opções à vista respondem em todos os pontos${ruins.length ? "; AMBÍGUAS: " + ruins.map((e) => e.textContent.trim().slice(0, 25)).join(", ") : ""}`;
      });
      relatorio.push(r);
      console.log(JSON.stringify(r));
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
writeFileSync(path.join(SAIDA, process.env.MANTER ? "relatorio-parcial.json" : "relatorio.json"), JSON.stringify({ relatorio, comportamentos, erros }, null, 1));
console.log(erros.length ? erros.join("\n") : "sem erros");
