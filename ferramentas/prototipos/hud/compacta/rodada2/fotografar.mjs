// A composição compacta, rodada 2 (protótipo; o jogo não muda): a B da rodada 1 corrigida (b), a B com o custo numa
// linha própria na coluna da ficha (b2) e a b2 com o registro na coluna do mundo (r), com os mesmos dados.
// As lutas (cenário tutorial; o herói no nível 12, à noite no Charco, depois de uma rodada de Atacar):
//   arqueiro  Arqueiro patrulheiro com o lobo, Morel e Odette (4) contra 5 caídos e o xamã (6, o maior bando real);
//   maior     Mago necromante com Morel, Odette e 3 servos (6) contra os mesmos 6, com a bolsa cheia (Itens com 7).
// Cada luta: a tela; Habilidades com o mouse na descrição mais longa (as medidas de cada faixa: linhas do nome, altura,
// onde fica o custo); Itens; escolher uma habilidade de um alvo (a mira: o seletor tem de sair e a ficha voltar); e os
// EFEITOS REAIS: os de um momento de verdade do motor (../capturas/efeitos-reais.json, o pior momento daquela
// especialização contra o maior bando), postos nas mesmas posições das cartas, com Habilidades aberto (o registro).
// O teclado, o movimento reduzido, a ficha coberta (clique e Tab) e o redimensionar com o seletor aberto: b2, a luta
// maior, 1280×720. Uma janela maior (1500×950): b2 e r na luta maior com os efeitos reais.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/compacta/rodada2/fotografar.mjs
// (CASOS=arqueiro-b,maior-b2,... para refazer só alguns; MANTER=1 não apaga as fotos)
import { spawn } from "child_process";
import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
import { batalha, escolhas, VERSOES } from "./r2.mjs";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
if (!process.env.MANTER) for (const f of readdirSync(SAIDA)) if (/\.(png|json)$/.test(f)) rmSync(path.join(SAIDA, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const JS_ESC = readFileSync(path.join(raiz, "rpg/web/static/app/escolhas.js"), "utf8");
const JS_BAT = readFileSync(path.join(raiz, "rpg/web/static/batalha.js"), "utf8");
const REAIS = JSON.parse(readFileSync(path.join(aqui, "../capturas/efeitos-reais.json"), "utf8")).pior_por_spec;
const BASE = { TUTORIAL: "0", VISTAS: "A1,V2,N1,D1,K1,M1,L1", NIVEL: "12", NIVEL_LUTA: "9", REC: "0.6", LUGAR: "charco", PERIODO: "3",
  GRUPO: "caido:5,xama_caido:1", BOLSA: "pocao_vida=3,tonico=2,bandagem=2,antidoto=1,bomba_fumaca=1,unguento=1,pena_fenix=1" };
const LUTAS = {
  arqueiro: { amb: { ...BASE, CLASSE: "arqueiro", ESPEC: "patrulheiro", ANIMAL: "lobo", COMITIVA: "morel,odete" }, real: "patrulheiro" },
  maior: { amb: { ...BASE, CLASSE: "mago", ESPEC: "necromante", COMITIVA: "morel,odete", SERVOS: "3" }, real: "necromante" },
};
// [luta, versão, janela]
const TODOS = [["arqueiro", "b", [1280, 720]], ["arqueiro", "b2", [1280, 720]], ["arqueiro", "r", [1280, 720]],
  ["maior", "b", [1280, 720]], ["maior", "b2", [1280, 720]], ["maior", "r", [1280, 720]],
  ["maior", "b2", [1500, 950]], ["maior", "r", [1500, 950]]];
const nomeCaso = ([l, v, [W]]) => `${W === 1280 ? "baixa" : "normal"}-${l}-${v}`;
const CASOS = process.env.CASOS ? TODOS.filter((c) => process.env.CASOS.split(",").includes(`${c[0]}-${c[1]}`)) : TODOS;
const UM_ALVO = ["bola_fogo", "drenar_vida", "lanca_gelo", "marcar_presa", "tiro_certeiro", "comando_fera", "tiro_duplo"];

async function subir(amb) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[tutorial] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, tam, versao, nome, opcoes = {}) {
  const p = await b.newPage({ viewport: { width: tam[0], height: tam[1] }, ...opcoes });
  await p.route(/\/static\/app\/escolhas\.js(\?|$)/, (r) => r.fulfill({ body: escolhas(JS_ESC, versao), contentType: "application/javascript" }));
  await p.route(/\/static\/batalha\.js(\?|$)/, (r) => r.fulfill({ body: batalha(JS_BAT, versao), contentType: "application/javascript" }));
  const anotar = (t) => { erros.push(t); console.log(`ERRO NO CONSOLE ${t}`); };
  p.on("pageerror", (e) => anotar(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) anotar(`${nome}: ${m.text()}`); });
  await p.goto(url);
  for (const f of VERSOES[versao].css) await p.addStyleTag({ path: path.join(aqui, f) });
  for (const f of VERSOES[versao].js) await p.addScriptTag({ path: path.join(aqui, f) });
  return p;
}
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="atacar"]'));
async function vez(p) {
  for (let k = 0; k < 240; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
const slot = (p, s) => p.$(`#roda .roda-botao[data-slot="${s}"]`);
const posicoes = (p) => p.evaluate(() => JSON.stringify([...document.querySelectorAll("#batalha .carta")].map((c) => { const r = c.getBoundingClientRect(); return [c.dataset.uid, Math.round(r.left), Math.round(r.top)]; })));
// a arena e o registro: alturas, onde o registro está, quantas linhas dele se leem, os nomes cortados
const arena = (p) => p.evaluate(() => {
  const a = document.getElementById("arena").getBoundingClientRect(), pg = document.getElementById("pagina"), r = pg.getBoundingClientRect();
  const lh = parseFloat(getComputedStyle(document.getElementById("texto")).lineHeight) || 24;
  const nomes = [...document.querySelectorAll("#batalha .carta .carta-nome span")];
  return { arena: Math.round(a.height), registro: `${Math.round(r.height)} px × ${Math.round(r.width)} px (~${Math.max(0, Math.floor(r.height / lh))} linhas)`,
    registro_no_mundo: document.body.classList.contains("registro-no-mundo"),
    nomes_cortados: nomes.filter((e) => e.scrollWidth > e.clientWidth + 1).map((e) => e.textContent).join("; ") || "nenhum",
    efeitos: document.querySelectorAll("#batalha .carta .ef").length };
});
// o seletor: onde abriu, as faixas (linhas de cada nome, altura, o custo), a descrição
const seletor = (p) => p.evaluate(() => {
  const j = document.querySelector(".roda-janela"); if (!j) return "fechado";
  const l = j.querySelector(".rj-lista"), m = l.getBoundingClientRect();
  const fs = [...l.querySelectorAll(".rj-linha")];
  const inteiras = fs.filter((e) => { const q = e.getBoundingClientRect(); return q.top >= m.top - 1 && q.bottom <= m.bottom + 1 && q.bottom <= innerHeight; }).length;
  const faixas = fs.map((e) => {
    const n = e.querySelector(".rj-nome"), i = e.querySelector(".rj-info"), lh = parseFloat(getComputedStyle(n).lineHeight);
    const nr = n.getBoundingClientRect(), ir = i.getBoundingClientRect();
    return { nome: n.textContent, linhas_do_nome: Math.round(nr.height / lh), altura: Math.round(e.getBoundingClientRect().height),
      custo: i.textContent.trim() ? (ir.top >= nr.bottom - 2 ? "embaixo" : "ao lado") : "—", custo_x: Math.round(ir.left), estoura: n.scrollWidth > n.clientWidth + 1 };
  });
  const d = j.querySelector(".rj-descricao"), c = j.querySelector(".rj-desc-caixa"), t = c && c.querySelector("b");
  const lado = j.classList.contains("lateral") ? "sobre a ficha" : "embaixo";
  return { lugar: lado, faixas_inteiras: `${inteiras} de ${fs.length}`, lista_rola: l.scrollHeight > l.clientHeight + 1, lista: Math.round(m.height),
    nomes_em_3_linhas: faixas.filter((f) => f.linhas_do_nome >= 3).map((f) => f.nome), nomes_estouram: faixas.filter((f) => f.estoura).map((f) => f.nome),
    custos_alinhados: new Set(faixas.filter((f) => f.custo !== "—").map((f) => f.custo_x)).size <= 1,
    descricao: d ? `${Math.round(d.getBoundingClientRect().height)} px${c.scrollHeight > c.clientHeight + 1 ? " (rola: o texto passa da área)" : ""}` : "—",
    examinada: t ? t.textContent : "nenhuma", faixas };
});
// os efeitos de um momento real do motor, nas mesmas posições (herói, aliados e inimigos na ordem)
const porEfeitos = (p, real) => p.evaluate((m) => {
  const cb = JSON.parse(JSON.stringify(estado.combate));
  const vivosA = cb.aliados.filter((a) => a.vivo), vivosI = cb.inimigos.filter((e) => e.vivo);
  cb.heroi.efeitos = (m.heroi && m.heroi.efeitos) || [];
  vivosA.forEach((a, k) => { a.efeitos = (m.aliados[k] && m.aliados[k].efeitos) || []; });
  vivosI.forEach((e, k) => { e.efeitos = (m.inimigos[k] && m.inimigos[k].efeitos) || []; });
  Batalha.desenhar(cb, estado.heroi);
  return vivosI.length;
}, real.momento);

for (const caso of CASOS) {
  const [luta, versao, tam] = caso, nome = nomeCaso(caso), H = tam[1], n = (c) => `${nome}-${c}`, r = { nome };
  const { amb } = LUTAS[luta], real = REAIS[LUTAS[luta].real];
  const { proc, url } = await subir(amb);
  try {
    const p = await pagina(url, tam, versao, nome);
    await vez(p);
    if (tam[0] === 1280) {  // a rodada de ataque, as fotos dos menus e a mira (na janela maior, só os efeitos reais)
      await (await slot(p, "atacar")).click();
      for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
      const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
      await espera(700); await vez(p); await p.mouse.move(5, H - 5); await espera(800);
      r.parado = await arena(p);
      await p.screenshot({ path: path.join(SAIDA, `${n("1-tela")}.png`) });
      const antes = await posicoes(p);
      await (await slot(p, "habilidades")).click(); await espera(600);
      const linhas = await p.$$(".roda-janela .rj-linha");
      let maior = { k: 0, h: 0 };
      for (let k = 0; k < linhas.length; k++) {
        await linhas[k].hover(); await espera(120);
        const h = await p.evaluate(() => { const c = document.querySelector(".rj-desc-caixa"); return c ? c.scrollHeight : 0; });
        if (h > maior.h) maior = { k, h };
      }
      await linhas[maior.k].hover(); await espera(300);
      r.habilidades = await seletor(p);
      r.abrir_mexe = antes === (await posicoes(p)) ? "nada se mexe" : "MUDOU";
      await p.screenshot({ path: path.join(SAIDA, `${n("2-habilidades")}.png`) });
      await p.mouse.move(5, H - 5);
      await (await slot(p, "itens")).click(); await espera(600); await p.mouse.move(5, H - 5); await espera(200);
      r.itens = await seletor(p);
      await p.screenshot({ path: path.join(SAIDA, `${n("3-itens")}.png`) });
      await (await slot(p, "itens")).click(); await espera(400);
      r.fechar_mexe = antes === (await posicoes(p)) ? "nada se mexe" : "MUDOU";
      // escolher uma habilidade de um alvo: na mira, o seletor tem de ter saído e a ficha voltado
      await (await slot(p, "habilidades")).click(); await espera(500);
      const hab = await p.evaluate((um) => (document.querySelector(um.map((h) => `.roda-janela .rj-linha:not(.bloqueada)[data-hab="${h}"]`).join(", ")) || {}).dataset?.hab || null, UM_ALVO);
      if (hab) await (await p.$(`.roda-janela .rj-linha[data-hab="${hab}"]`)).click();
      await espera(900); await p.mouse.move(5, H - 5); await espera(250);
      r.mira = await p.evaluate(() => `${document.querySelectorAll(".roda-janela").length} seletor na tela; ficha ${document.getElementById("heroi").inert ? "INERTE" : "de volta"}; ${document.querySelector(".roda-mira") ? "a mira à vista" : "SEM MIRA"}`);
      await p.screenshot({ path: path.join(SAIDA, `${n("4-mira")}.png`) });
      const v = await p.$(".mira-voltar"); if (v) await v.click(); else await p.keyboard.press("Escape");
      await vez(p); await espera(400);
    }
    // os efeitos reais, Habilidades aberto
    r.efeitos_reais = `${real.spec}, semente ${real.seed}, turno ${real.momento.turno}: ${[real.momento.heroi, ...real.momento.aliados, ...real.momento.inimigos].filter(Boolean).map((c) => `${c.nome} [${c.efeitos.map((e) => e.id).join(", ")}]`).join("; ")}`;
    await porEfeitos(p, real); await espera(700); await p.mouse.move(5, H - 5); await espera(300);
    r.com_efeitos = await arena(p);
    await p.screenshot({ path: path.join(SAIDA, `${n("5-efeitos-reais")}.png`) });
    await (await slot(p, "habilidades")).click(); await espera(600);
    const ls = await p.$$(".roda-janela .rj-linha"); if (ls.length) { await ls[Math.min(4, ls.length - 1)].hover(); await espera(300); }
    r.efeitos_habilidades = await seletor(p);
    r.efeitos_habilidades_arena = await arena(p);
    await p.screenshot({ path: path.join(SAIDA, `${n("6-efeitos-reais-habilidades")}.png`) });
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}

// b2, a luta maior, 1280×720, movimento reduzido: o teclado, a ficha coberta, o redimensionar, o Esc
if (!process.env.CASOS) {
  const r = { nome: "teclado-ficha-redimensionar-b2" };
  const { proc, url } = await subir(LUTAS.maior.amb);
  try {
    const p = await pagina(url, [1280, 720], "b2", r.nome, { reducedMotion: "reduce" });
    await vez(p); await espera(500);
    await p.keyboard.press("2"); await espera(500);
    r.tecla_2 = await p.evaluate(() => { const a = document.activeElement, j = document.querySelector(".roda-janela"); return `${j ? (j.classList.contains("lateral") ? "seletor sobre a ficha" : "seletor embaixo") : "sem seletor"}; foco: ${a.closest(".rj-linha") ? a.querySelector(".rj-nome").textContent : a.tagName}`; });
    r.animacao = await p.evaluate(() => getComputedStyle(document.querySelector(".roda-janela .rj-linha")).animationName);
    for (let k = 0; k < 4; k++) await p.keyboard.press("ArrowDown");
    await espera(200);
    const foco = () => p.evaluate(() => { const a = document.activeElement, q = a.getBoundingClientRect(), l = a.closest(".rj-lista")?.getBoundingClientRect();
      const t = document.querySelector(".rj-desc-caixa b");
      return `foco na ${[...document.querySelectorAll(".rj-linha")].indexOf(a) + 1}ª (${a.querySelector(".rj-nome")?.textContent}); ${l && q.top >= l.top - 1 && q.bottom <= l.bottom + 1 && q.bottom <= innerHeight ? "inteira à vista" : "FORA DA VISTA"}; ${a.matches(":focus-visible") ? "foco visível" : "sem foco visível"}; descrição: ${t ? t.textContent : "nenhuma"}`; });
    r.setas = await foco();
    await p.screenshot({ path: path.join(SAIDA, "teclado-b2-1-setas.png") });
    // a ficha coberta: o que está no centro dela, o clique num controle dela e o Tab
    r.ficha_coberta = await p.evaluate(() => {
      const f = document.getElementById("heroi"), q = f.getBoundingClientRect();
      const pontos = [[q.left + q.width / 2, q.top + 60], [q.left + q.width / 2, q.top + q.height / 2], [q.left + 30, q.bottom - 40]];
      const em = pontos.map(([x, y]) => (document.elementFromPoint(x, y)?.closest(".roda-janela") ? "seletor" : "FICHA")).join(", ");
      const focaveis = [...f.querySelectorAll("button, [tabindex], a, input")].length;
      return `nos três pontos da ficha: ${em}; ficha inerte: ${f.inert ? "sim" : "NÃO"} (${focaveis} controles nela)`;
    });
    // cada controle da ficha: o que está por cima do centro dele (uma faixa ou a área neutra do seletor, nunca a ficha)
    r.controles_da_ficha = await p.evaluate(() => [...document.querySelectorAll("#heroi :is(button, [tabindex], a, input)")].map((c) => {
      const q = c.getBoundingClientRect(), t = document.elementFromPoint(q.left + q.width / 2, q.top + q.height / 2);
      const nome = (c.textContent.trim() || c.title || c.className).slice(0, 24);
      return `${nome}: ${!t ? "nada" : t.closest(".rj-linha") ? "faixa do seletor" : t.closest(".roda-janela") ? "área do seletor" : "A FICHA"}`;
    }).join("; "));
    // um clique na área neutra do seletor por cima da ficha (o título): nada da ficha abre e o seletor fica
    const neutro = await p.evaluate(() => { const t = document.querySelector(".roda-janela .rj-titulo span").getBoundingClientRect(); return [t.left + 10, t.top + t.height / 2]; });
    await p.mouse.click(neutro[0], neutro[1]); await espera(400);
    r.clique_na_area_neutra = await p.evaluate(() => `${document.querySelector(".sobreposicao:not([hidden])") ? "ABRIU ALGO" : "nada abriu"}; ${document.querySelector(".roda-janela") ? "o seletor continua" : "O SELETOR FECHOU"}`);
    if (!(await p.$(".roda-janela"))) { await p.keyboard.press("2"); await espera(400); }
    await (await p.$(".roda-janela .rj-linha")).focus();
    for (let k = 0; k < 4; k++) await p.keyboard.press("ArrowDown");
    const tabs = [];
    for (let k = 0; k < 14; k++) { await p.keyboard.press("Tab"); tabs.push(await p.evaluate(() => (document.activeElement.closest("#heroi") ? "FICHA" : document.activeElement.closest(".roda-janela") ? "seletor" : document.activeElement.closest("#mundo") ? "mundo" : document.activeElement.closest("#batalha, #roda") ? "arena" : document.activeElement.tagName.toLowerCase()))); }
    r.tab_14_vezes = tabs.join(" → ");
    // volta o foco à 5ª e redimensiona com o seletor aberto
    await p.keyboard.press("Escape"); await espera(300); await p.keyboard.press("2"); await espera(400);
    for (let k = 0; k < 4; k++) await p.keyboard.press("ArrowDown");
    await espera(200);
    const antes = await foco();
    const tamanhos = [[1366, 768], [1280, 650], [1280, 720]];
    r.redimensionar = [];
    for (const [W, Hh] of tamanhos) {
      await p.setViewportSize({ width: W, height: Hh }); await espera(700);
      const abertas = await posicoes(p);
      const cobre = await p.evaluate(() => { const j = document.querySelector(".roda-janela"), f = document.getElementById("heroi"); if (!j) return "sem seletor"; const a = j.getBoundingClientRect(), b = f.getBoundingClientRect();
        return Math.abs(a.left - b.left) < 2 && Math.abs(a.top - b.top) < 2 && Math.abs(a.width - b.width) < 2 && Math.abs(a.height - b.height) < 3 ? "cobre a ficha certinho" : `FORA DA FICHA (${Math.round(a.left)},${Math.round(a.top)} ${Math.round(a.width)}×${Math.round(a.height)} contra ${Math.round(b.left)},${Math.round(b.top)} ${Math.round(b.width)}×${Math.round(b.height)})`; });
      const depois = await foco();
      await p.screenshot({ path: path.join(SAIDA, `teclado-b2-2-redimensionado-${W}x${Hh}.png`) });
      // fecha e reabre no mesmo tamanho: as cartas com o seletor aberto têm de estar onde estão com ele fechado
      await p.keyboard.press("Escape"); await espera(300);
      const fechadas = await posicoes(p);
      await p.keyboard.press("2"); await espera(400);
      for (let k = 0; k < 4; k++) await p.keyboard.press("ArrowDown");
      await espera(200);
      r.redimensionar.push(`${W}×${Hh}: ${cobre}; ${depois === antes ? "a examinada e o foco como antes" : depois}; cartas ${abertas === fechadas ? "no mesmo lugar com o seletor aberto e fechado" : "MEXERAM por causa do seletor"}`);
    }
    await p.keyboard.press("Escape"); await espera(300);
    r.esc = await p.evaluate(() => `${document.querySelectorAll(".roda-janela").length} seletor; foco: ${document.activeElement.dataset.slot || document.activeElement.tagName}; ficha ${document.getElementById("heroi").inert ? "INERTE" : "de volta"}`);
    // o mouse: clicar fora (na arena) fecha e devolve a ficha
    await (await slot(p, "habilidades")).click(); await espera(400);
    const vazio = await p.evaluate(() => { const a = document.getElementById("arena").getBoundingClientRect(); return [a.left + a.width * 0.55, a.bottom - 20]; });
    await p.mouse.click(vazio[0], vazio[1]); await espera(400);
    r.clique_fora = await p.evaluate(() => `${document.querySelectorAll(".roda-janela").length} seletor; ficha ${document.getElementById("heroi").inert ? "INERTE" : "de volta"}`);
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, process.env.MANTER ? "relatorio-parcial.json" : "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
