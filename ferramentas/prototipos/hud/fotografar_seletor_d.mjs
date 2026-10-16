// O seletor de habilidades D, faixas de tinta (experimento): o jogo como está ("atual") e a proposta ("d"), na mesma
// luta, com os mesmos dados. Na versão d a página recebe a cópia do escolhas.js de seletor/d-escolhas.mjs e a folha
// seletor/d-faixas.css; o jogo não muda.
// As lutas (cenário tutorial, contra lobos, com Morel e Odette na comitiva, pouco recurso para umas habilidades ficarem
// sem; todas no nível 12, onde cada classe tem 7):
//   guerreiro   Guerreiro berserker (a classe da referência);
//   arqueiro    Arqueiro sombra: os nomes mais longos (Flecha Envenenada, Chuva de Flechas) e o custo em flechas;
//   mago        Mago necromante: a Mana;
//   capacidade  o Guerreiro com as habilidades das duas especializações (10): o seletor não pode contar com 7.
// Em 1500×950, 1920×1080 e 1280×720, cada versão: a tela inteira com o seletor aberto, o seletor, o mouse numa
// habilidade (com a dica) e numa indisponível, o pressionado, o teclado (a tecla 2 abre; na d a primeira faixa já chega
// com o foco e as setas andam; no jogo de hoje, o Tab), a escolha (a habilidade de um alvo leva à mira) e o Voltar.
// Mede: se abrir e fechar mexe nas cartas ou na rolagem, se o seletor cobre a arena, se a lista rola, se algum texto é
// cortado, onde a dica abre e onde fica o foco depois da escolha.
// Na luta do guerreiro em 1500×950, ainda: abrir e fechar depressa, o clique duplo numa habilidade, a tecla segurada,
// o clique durante a entrada das faixas e o movimento reduzido.
// Do jogo de hoje guarda só a tela e o seletor aberto (os estados dele estão em capturas-seletor/), mas confere o
// mesmo caminho. Guarda em capturas-seletor-d/ (relatorio.json com as medidas); comparar_seletor_d.py monta as comparações.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_seletor_d.mjs
// (VERSOES=atual,d,d2 (d2: a D refinada, seletor/d2-faixas.css por cima da D), RODADA=1 (uma rodada de Atacar antes,
// para o registro real ficar por baixo), LUTAS=guerreiro,arqueiro,mago,capacidade, JANELAS=normal,grande,baixa e SAIDA=<pasta> para escolher)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
import { escolhasD } from "./seletor/d-escolhas.mjs";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-seletor-d"));
rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const filtro = (nome, todos) => (process.env[nome] ? process.env[nome].split(",") : todos);

const FOLHA_D = path.join(aqui, "seletor", "d-faixas.css"), FOLHA_D2 = path.join(aqui, "seletor", "d2-faixas.css");
const VERSOES = filtro("VERSOES", ["atual", "d"]);
// d e d2 aplicam as trocas no escolhas.js de antes da 1.103.0 (as propostas); desde a integração, "atual" já é a D
// refinada no jogo, e só ela roda no escolhas.js de hoje
const ESCOLHAS_D = VERSOES.some((v) => v !== "atual") ? escolhasD(readFileSync(path.join(raiz, "rpg/web/static/app/escolhas.js"), "utf8")) : null;
const BASE = { TUTORIAL: "0", LUTA: "lobo", COMITIVA: "morel,odete", NIVEL: "12", VISTAS: "A1,V2,N1,D1,K1,M1,L1", REC: "0.3", QUANTOS: "2" };
if (process.env.RODADA) BASE.NIVEL_LUTA = "9";  // lobos que aguentam a rodada (a luta continua, com o registro escrito)
const TODAS = {
  guerreiro: { ...BASE, CLASSE: "guerreiro", ESPEC: "berserker" },
  arqueiro: { ...BASE, CLASSE: "arqueiro", ESPEC: "sombra", QUANTOS: "3" },
  mago: { ...BASE, CLASSE: "mago", ESPEC: "necromante", REC: "0.12" },  // a Mana é grande: menos, para umas ficarem sem
  capacidade: { ...BASE, CLASSE: "guerreiro", ESPEC: "paladino", HABILIDADES: "todas" },
};
if (process.env.RODADA) for (const l of ["guerreiro", "arqueiro", "capacidade"]) TODAS[l].REC = "0";  // a rodada devolve Vigor e Foco: começar sem
const LUTAS = Object.entries(TODAS).filter(([l]) => filtro("LUTAS", Object.keys(TODAS)).includes(l));
const JANELAS = Object.entries({ normal: [1500, 950], grande: [1920, 1080], baixa: [1280, 720] }).filter(([j]) => filtro("JANELAS", ["normal", "grande", "baixa"]).includes(j));
// as habilidades de um alvo só (a escolha leva à mira e o Voltar desfaz; nada é jogado)
const UM_ALVO = ["bola_fogo", "comando_fera", "combustao", "drenar_vida", "execucao", "fenix", "flecha_envenenada", "furia_cega",
  "golpe_pesado", "golpe_sagrado", "investida", "lanca_gelo", "marcar_presa", "sede_sangue", "tiro_certeiro", "tiro_duplo"];
async function subir(amb) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", "tutorial"],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[tutorial] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const relatorio = [], comportamentos = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, [W, H], versao, nome, opcoes = {}, rodada = false) {
  const p = await b.newPage({ viewport: { width: W, height: H }, ...opcoes });
  if (versao !== "atual") await p.route(/\/static\/app\/escolhas\.js(\?|$)/, (r) => r.fulfill({ body: ESCOLHAS_D, contentType: "application/javascript" }));
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  if (versao !== "atual") await p.addStyleTag({ path: FOLHA_D });
  if (versao === "d2") await p.addStyleTag({ path: FOLHA_D2 });  // a D refinada: as bordas e o fundo, por cima da D
  await vez(p);
  for (let k = 0; k < (rodada ? Number(process.env.RODADA) || 1 : 0); k++) {  // RODADA=n rodadas de Atacar antes: o registro real por baixo
    await (await p.$('#roda .roda-botao[data-slot="atacar"]')).click();
    for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
    const alvo = await p.$("#batalha .carta.alvejavel");
    if (alvo) await alvo.click();
    await espera(500);
    await vez(p);
  }
  await p.mouse.move(5, H - 5);
  await espera(700);
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
async function recortar(p, sels, nome, folga = 8) {
  // o jogo de antes da 1.103.0: só a tela e o seletor aberto (os estados dele estão em capturas-seletor/); ANTIGO=1
  if (process.env.ANTIGO && /-atual-[2-9]-/.test(nome)) return;
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
const abrir = async (p) => { await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click(); await espera(450); };
const medir = (p) => p.evaluate((umAlvo) => {
  const j = document.querySelector(".roda-janela");
  if (!j) return { aberto: false };
  const R = j.getBoundingClientRect(), roda = document.getElementById("roda").getBoundingClientRect(), lista = j.querySelector(".rj-lista");
  const linhas = [...j.querySelectorAll(".rj-linha")];
  const cortados = [...j.querySelectorAll(".rj-nome, .rj-info, .rj-motivo")].filter((e) => e.scrollWidth > e.clientWidth + 1 || e.getBoundingClientRect().right > R.right + 0.5)
    .map((e) => e.textContent.trim());
  const duasLinhas = [...j.querySelectorAll(".rj-nome")].filter((e) => e.getBoundingClientRect().height > parseFloat(getComputedStyle(e).lineHeight) * 1.5).map((e) => e.textContent.trim());
  const cartas = [...document.querySelectorAll("#batalha .carta")].filter((c) => { const r = c.getBoundingClientRect(); return r.bottom > R.top + 1 && r.top < R.bottom && r.right > R.left && r.left < R.right; });
  return { aberto: true, tamanho: `${Math.round(R.width)}×${Math.round(R.height)}`, posicao: `${Math.round(R.left)},${Math.round(R.top)}`,
    cobre_arena: Math.max(0, Math.round(roda.bottom - R.top)), cobre_cartas: cartas.length, fora_da_tela: R.bottom > innerHeight + 0.5,
    habilidades: linhas.length, indisponiveis: linhas.filter((l) => l.classList.contains("bloqueada")).length,
    rola: lista.scrollHeight > lista.clientHeight + 1, cortados, nomes_em_duas_linhas: duasLinhas,
    menor_alvo: Math.min(...linhas.map((l) => Math.round(Math.min(l.getBoundingClientRect().width, l.getBoundingClientRect().height)))),
    um_alvo: (linhas.find((l) => !l.classList.contains("bloqueada") && umAlvo.includes(l.dataset.hab)) || {}).dataset?.hab || null };
}, UM_ALVO);
const focado = (p) => p.evaluate(() => { const a = document.activeElement; return a === document.body ? "nada (body)" : `${a.className.split(" ")[0]}: ${a.textContent.trim().slice(0, 30)}`; });
const dicaCobre = (p) => p.evaluate(() => {
  const d = document.getElementById("dica-item"), j = document.querySelector(".roda-janela");
  if (!d || d.hidden || !j) return "sem dica";
  const a = d.getBoundingClientRect(), R = j.getBoundingClientRect();
  const area = Math.max(0, Math.min(a.right, R.right) - Math.max(a.left, R.left)) * Math.max(0, Math.min(a.bottom, R.bottom) - Math.max(a.top, R.top));
  return `cobre ${Math.round((100 * area) / (R.width * R.height))}% do seletor`;
});

for (const [luta, amb] of LUTAS) {
  const { proc, url } = await subir(amb);
  try {
    for (const [jan, tam] of JANELAS) for (const versao of VERSOES) {
      const H = tam[1], n = (c) => `${jan}-${luta}-${versao}-${c}`, r = { nome: `${jan}-${luta}-${versao}` };
      // com RODADA, cada foto num jogo novo (a mesma semente): a rodada jogada dá o mesmo registro nas duas versões
      const novo = process.env.RODADA ? await subir(amb) : null;
      const p = await pagina(novo ? novo.url : url, tam, versao, r.nome, {}, !!novo);
      const antes = await disposicao(p);
      // 1. aberto pelo clique: a tela inteira, o seletor e as medidas
      await abrir(p);
      await p.mouse.move(5, H - 5); await espera(300);
      r.abrir_mexe = (await disposicao(p)) !== antes;
      await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
      await recortar(p, ["#roda", ".roda-janela"], n("1-aberto"));
      Object.assign(r, await medir(p));
      // a borda de baixo: nenhuma linha do registro cortada ao meio, com o registro em várias posições de rolagem
      // (alturas e quebras de linha diferentes encostando na borda); a rolagem volta para onde estava
      r.fragmentos = await p.evaluate(async () => {
        const pg = document.getElementById("pagina"), j = document.querySelector(".roda-janela"), antes = pg.scrollTop, achados = [];
        const conta = () => { const B = j.getBoundingClientRect().bottom, rr = document.createRange(), w = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT); let n = 0;
          for (let t = w.nextNode(); t; t = w.nextNode()) { if (!t.textContent.trim()) continue; rr.selectNodeContents(t);
            for (const q of rr.getClientRects()) if (q.height && q.top < B - 3 && q.bottom > B + 3) n++; } return n; };  // cortada de verdade: o encosto de 3 px das caixas não conta
        const posicoes = [antes, ...[7, 13, 22, 37, 58, 91].map((d) => Math.max(0, antes - d))];
        for (const y of posicoes) { pg.scrollTop = y; await new Promise((r) => setTimeout(r, 60)); achados.push(`${Math.round(pg.scrollTop)}:${conta()}`); }
        pg.scrollTop = antes; await new Promise((r) => setTimeout(r, 60));
        return { rolagem_max: pg.scrollHeight - pg.clientHeight, cortadas_por_posicao: achados.join(" "), voltou: pg.scrollTop === antes };
      });
      r.disposicao_depois_da_rolagem = (await disposicao(p)) === antes ? "igual" : "MUDOU";
      // 2. o mouse numa habilidade (a dica) e numa indisponível (o motivo)
      const livre = await p.$(".roda-janela .rj-linha:not(.bloqueada)");
      if (livre) { await livre.hover(); await espera(650); r.dica = await dicaCobre(p); await recortar(p, ["#roda", ".roda-janela", "#dica-item"], n("2-mouse")); }
      const presa = await p.$(".roda-janela .rj-linha.bloqueada");
      if (presa) { await presa.hover(); await espera(650); await recortar(p, ["#roda", ".roda-janela", "#dica-item"], n("3-indisponivel")); }
      // 3. pressionado (o botão segura, solta fora da linha: nada é escolhido)
      if (livre) {
        await livre.hover(); await p.mouse.down(); await espera(120);
        await recortar(p, [".roda-janela"], n("4-pressionado"));
        const t = await (await p.$(".roda-janela .rj-titulo")).boundingBox();
        await p.mouse.move(t.x + 4, t.y + t.height / 2); await p.mouse.up(); await espera(200);
        r.soltar_fora = (await p.$(".roda-janela")) && !(await p.$(".roda-mira")) ? "nada escolhido" : "ERRO";
      }
      // 4. Esc fecha (e fechar não mexe nas cartas nem na rolagem)
      await p.mouse.move(5, H - 5); await p.keyboard.press("Escape"); await espera(350);
      r.esc_fecha = !(await p.$(".roda-janela"));
      r.fechar_mexe = (await disposicao(p)) !== antes;
      // 5. pelo teclado: a tecla 2 abre; na d o foco já está na primeira faixa e as setas andam; no jogo, o Tab
      await p.keyboard.press("2"); await espera(450);
      r.tecla_abre = !!(await p.$(".roda-janela"));
      if (versao === "atual") for (let k = 0; k < 15 && !(await p.evaluate(() => !!document.activeElement.closest(".roda-janela .rj-linha"))); k++) await p.keyboard.press("Tab");
      r.foco_ao_abrir = await focado(p);
      await recortar(p, ["#roda", ".roda-janela"], n("5-teclado"));
      if (await p.$('.roda-janela[data-tipo="habilidades"]')) {  // o seletor de faixas (a D, a refinada e o jogo desde a 1.103.0)
        await p.keyboard.press("ArrowDown"); await p.keyboard.press("ArrowRight"); await espera(200);
        r.setas = await focado(p);
        await recortar(p, ["#roda", ".roda-janela"], n("6-setas"));
      }
      await p.keyboard.press("Escape"); await espera(350);
      r.foco_depois_do_esc = await focado(p);
      // 6. a escolha: uma habilidade de um alvo → a mira; o Voltar devolve a roda
      await abrir(p);
      const alvo = (await medir(p)).um_alvo;
      if (alvo) {
        await (await p.$(`.roda-janela .rj-linha[data-hab="${alvo}"]`)).click(); await espera(900);
        await p.mouse.move(5, H - 5); await espera(250);
        r.escolha = `${alvo} → ${(await p.$(".roda-mira")) ? "mira" : "sem mira (um inimigo só: executa direto, a regra do jogo)"}; seletor ${(await p.$(".roda-janela")) ? "AINDA NA TELA" : "fora"}; foco: ${await focado(p)}`;
        await recortar(p, ["#arena"], n("7-alvo"), 2);
        const v = await p.$(".mira-voltar");
        if (v) await v.click(); else await p.keyboard.press("Escape");
        await vez(p);
        r.cancelar = (await p.$('#roda .roda-botao[data-slot="habilidades"]')) && !(await p.$(".roda-janela")) ? "a roda de volta, sem seletor" : "ERRO";
        // reabrir depois de cancelar: o mesmo seletor, as mesmas linhas
        await abrir(p);
        r.reabrir = `${await p.$$eval(".roda-janela .rj-linha", (x) => x.length)} linhas`;
        await p.keyboard.press("Escape"); await espera(300);
      } else r.escolha = "nenhuma habilidade de um alvo disponível";
      relatorio.push(r);
      console.log(JSON.stringify(r));
      await p.close();
      if (novo) novo.proc.kill();
    }

    // Os comportamentos (guerreiro, 1500×950): depressa, clique duplo, tecla segurada, clique na entrada, movimento reduzido
    if (luta === "guerreiro") for (const versao of VERSOES) {
      const c = { versao }, tam = [1500, 950];
      let p = await pagina(url, tam, versao, `comportamentos-${versao}`);
      const botao = await p.$('#roda .roda-botao[data-slot="habilidades"]');
      for (let k = 0; k < 5; k++) { await botao.click(); await espera(40); }  // cinco cliques: abre, fecha, abre, fecha, abre
      await espera(300);
      c.depressa = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es) na tela depois de 5 cliques (esperado 1)`;
      await p.keyboard.press("Escape"); await espera(300);
      // a tecla segurada: só o primeiro aperto conta
      await p.keyboard.down("2"); for (let k = 0; k < 6; k++) { await espera(35); await p.keyboard.down("2"); } await p.keyboard.up("2"); await espera(300);
      c.tecla_segurada = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es) (esperado 1)`;
      await p.keyboard.press("Escape"); await espera(300);
      // o clique duplo numa habilidade de um alvo: uma escolha só, na mira
      await abrir(p);
      const alvo = (await medir(p)).um_alvo;
      await (await p.$(`.roda-janela .rj-linha[data-hab="${alvo}"]`)).dblclick(); await espera(900);
      c.clique_duplo = `${(await p.$(".roda-mira")) ? "na mira" : "SEM MIRA"}; ${await p.evaluate(() => document.querySelectorAll("#batalha .carta.inimigo .vida, #batalha .carta.inimigo").length)} cartas inimigas; vez do herói: ${await p.evaluate(() => !!pergunta && !processando)}`;
      const v = await p.$(".mira-voltar"); if (v) await v.click(); await vez(p);
      // o clique durante a entrada (30 ms depois de abrir): vale na hora
      await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click();
      await espera(30);
      await p.evaluate((h) => document.querySelector(`.roda-janela .rj-linha[data-hab="${h}"]`).click(), alvo);
      await espera(700);
      c.clique_na_entrada = (await p.$(".roda-mira")) ? "aceito (foi para a mira)" : "PERDIDO";
      const v2 = await p.$(".mira-voltar"); if (v2) await v2.click(); await vez(p);
      // a escolha pelo teclado: a tecla abre, Enter na faixa focada; o foco não fica num controle que sumiu
      await p.keyboard.press("2"); await espera(300);
      if (versao === "atual") for (let k = 0; k < 15 && !(await p.evaluate(() => !!document.activeElement.closest(".roda-janela .rj-linha"))); k++) await p.keyboard.press("Tab");
      await p.keyboard.press("Enter"); await espera(800);
      c.saida_pelo_teclado = `${(await p.$(".roda-mira")) ? "mira" : "sem mira"}; foco: ${await focado(p)}; controles do seletor que sobraram: ${await p.$$eval(".roda-janela button", (x) => x.length)}`;
      const v3 = await p.$(".mira-voltar"); if (v3) await v3.click(); await vez(p);
      // a entrada fotografada no meio (40 ms): com movimento e sem
      await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click(); await espera(40);
      await recortar(p, [".roda-janela"], `comportamento-${versao}-entrada-40ms`);
      await p.close();
      p = await pagina(url, tam, versao, `reduzido-${versao}`, { reducedMotion: "reduce" });
      await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click(); await espera(40);
      await recortar(p, [".roda-janela"], `comportamento-${versao}-reduzido-40ms`);
      const livre = await p.$(".roda-janela .rj-linha:not(.bloqueada)");
      await livre.hover(); await p.mouse.down(); await espera(100);
      c.reduzido_pressionado = await p.evaluate(() => getComputedStyle(document.querySelector(".roda-janela .rj-linha:active") || document.body).translate);
      await recortar(p, [".roda-janela"], `comportamento-${versao}-reduzido-pressionado`);
      await p.mouse.move(5, 940); await p.mouse.up();
      await p.close();
      comportamentos.push(c);
      console.log(JSON.stringify(c));
    }
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, comportamentos }, null, 1));
console.log(erros.length ? erros.join("\n") : "sem erros");
