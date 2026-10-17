// A composição compacta das lutas cheias (protótipo, compacta/): a produção (1.113.0) e as duas alternativas, com os
// mesmos dados (um jogo novo com a mesma semente para cada foto). O jogo não muda: a página da proposta recebe as
// trocas de compacta.mjs no escolhas.js e no batalha.js e a folha da alternativa por cima.
//   producao  o jogo como está;
//   a         "arena compacta": a partir de 5 cartas num lado, os efeitos na linha do nome e as cartas mais juntas; o
//             seletor em três colunas quando as duas não cabem embaixo;
//   b         "seletor na ficha": a arena como está; o seletor que não cabe inteiro embaixo da arena abre sobre a coluna
//             da ficha do herói, numa coluna só.
// As lutas (cenário tutorial; o herói no nível 12; depois de uma rodada de Atacar, para os efeitos aparecerem):
//   poucos   Guerreiro paladino com Morel contra um rato e 2 lobos (a composição de sempre: tem de ficar igual);
//   cinco    Arqueiro patrulheiro com o lobo, Morel e Odette (4 aliados) contra 5 lobos;
//   maior    Mago necromante com Morel, Odette e 3 servos (6 aliados, o máximo das regras) contra 5 caídos e o xamã (6, o
//            maior bando), à noite, com a bolsa cheia (o menu de Itens com 7 linhas);
//   longos   Guerreiro berserker com Morel e Odette contra 4 esqueletos com os nomes mais longos do jogo.
// Em 1280×720, 1500×950 e 1920×1080: a tela parada; Habilidades aberto (a tela inteira, quantas faixas à vista, se a lista
// rola, a altura da descrição), o mouse na habilidade de descrição mais longa e na mais curta; Itens (alternou); a mira
// e o Voltar; a saída e a entrada de um combatente SIMULADAS durante a mira (o estado da luta com um a menos e um a mais,
// desenhado pelo jogo); e, SIMULADO, todos os combatentes com três ou quatro efeitos (os nomes longos e muitos efeitos).
// Mede o que cobre o quê, o que se mexe ao abrir e fechar, os nomes cortados, a altura da arena e o espaço do seletor.
// O teclado (a tecla 2 abre, as setas andam, Esc fecha) e o movimento reduzido na luta maior em 1280×720.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/compacta/fotografar.mjs
// (VERSOES=producao,a,b, LUTAS=..., JANELAS=baixa,normal,grande, SAIDA=<pasta>, PYTHON=<executável>, MANTER=1)
import { spawn } from "child_process";
import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
import { batalha, escolhas, FOLHAS } from "./compacta.mjs";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas"));
mkdirSync(SAIDA, { recursive: true });
if (!process.env.MANTER) for (const f of readdirSync(SAIDA)) if (/\.(png|json)$/.test(f)) rmSync(path.join(SAIDA, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const filtro = (nome, todos) => (process.env[nome] ? process.env[nome].split(",") : todos);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const JS_ESC = readFileSync(path.join(raiz, "rpg/web/static/app/escolhas.js"), "utf8");
const JS_BAT = readFileSync(path.join(raiz, "rpg/web/static/batalha.js"), "utf8");
const VERSOES = filtro("VERSOES", ["producao", "a", "b"]);
const JANELAS = Object.entries({ baixa: [1280, 720], normal: [1500, 950], grande: [1920, 1080] }).filter(([j]) => filtro("JANELAS", ["baixa", "normal", "grande"]).includes(j));
const BASE = { TUTORIAL: "0", VISTAS: "A1,V2,N1,D1,K1,M1,L1", NIVEL: "12", NIVEL_LUTA: "9", REC: "0.6" };
const TODAS = {
  poucos: { ...BASE, CLASSE: "guerreiro", ESPEC: "paladino", COMITIVA: "morel", GRUPO: "rato:1,lobo:2", NIVEL_LUTA: "4", LUGAR: "vau", PERIODO: "0" },
  cinco: { ...BASE, CLASSE: "arqueiro", ESPEC: "patrulheiro", ANIMAL: "lobo", COMITIVA: "morel,odete", LUTA: "lobo", QUANTOS: "5", LUGAR: "bosque", PERIODO: "2" },
  maior: { ...BASE, CLASSE: "mago", ESPEC: "necromante", COMITIVA: "morel,odete", SERVOS: "3", GRUPO: "caido:5,xama_caido:1", LUGAR: "charco", PERIODO: "3",
    BOLSA: "pocao_vida=3,tonico=2,bandagem=2,antidoto=1,bomba_fumaca=1,unguento=1,pena_fenix=1" },
  longos: { ...BASE, CLASSE: "guerreiro", ESPEC: "berserker", COMITIVA: "morel,odete", LUTA: "esqueleto", QUANTOS: "4", LONGOS: "1", LUGAR: "vau", PERIODO: "0" },
};
const LUTAS = Object.entries(TODAS).filter(([l]) => filtro("LUTAS", Object.keys(TODAS)).includes(l));
const UM_ALVO = ["bola_fogo", "drenar_vida", "execucao", "flecha_envenenada", "golpe_pesado", "golpe_sagrado", "investida", "lanca_gelo", "marcar_presa", "tiro_certeiro", "comando_fera", "furia_cega", "sede_sangue"];

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
async function pagina(url, [W, H], versao, nome, opcoes = {}) {
  const p = await b.newPage({ viewport: { width: W, height: H }, ...opcoes });
  if (versao !== "producao") {
    await p.route(/\/static\/app\/escolhas\.js(\?|$)/, (r) => r.fulfill({ body: escolhas(JS_ESC, versao), contentType: "application/javascript" }));
    await p.route(/\/static\/batalha\.js(\?|$)/, (r) => r.fulfill({ body: batalha(JS_BAT, versao), contentType: "application/javascript" }));
  }
  const anotar = (t) => { erros.push(t); console.log(`ERRO NO CONSOLE ${t}`); };
  p.on("pageerror", (e) => anotar(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) anotar(`${nome}: ${m.text()}`); });
  await p.goto(url);
  if (versao !== "producao") for (const f of FOLHAS[versao]) await p.addStyleTag({ path: path.join(aqui, f) });
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
const disposicao = (p) => p.evaluate(() => JSON.stringify({
  cartas: [...document.querySelectorAll("#batalha .carta")].map((c) => { const r = c.getBoundingClientRect(); return [c.dataset.uid, Math.round(r.left), Math.round(r.top)]; }),
  rolagem: [document.scrollingElement, ...document.querySelectorAll("*")].filter((e) => e && e.scrollTop > 0).map((e) => `${e.id || e.className}:${Math.round(e.scrollTop)}`),
}));
const mexe = (a, b) => (a === b ? "nada se mexe" : "MUDOU");
// a arena: a altura, o que cobre o quê, os nomes cortados, os efeitos à vista
const arena = (p) => p.evaluate(() => {
  const a = document.getElementById("arena").getBoundingClientRect();
  const cartas = [...document.querySelectorAll("#batalha .carta")].map((c) => [c.dataset.uid, c.getBoundingClientRect(), c]);
  const outros = [...[...document.querySelectorAll("#roda .roda-botao")].map((b) => ["cmd:" + b.dataset.slot, b.getBoundingClientRect()]),
    ...[...document.querySelectorAll(".roda-mira")].map((m) => ["mira", m.getBoundingClientRect()]), ...[...document.querySelectorAll("#arena > .mods-arena .mod")].map((m) => ["aviso", m.getBoundingClientRect()]),
    ...[...document.querySelectorAll(".roda-janela")].map((j) => ["seletor", j.getBoundingClientRect()])];
  const toca = (x, q) => x.right > q.left + 1 && x.left < q.right - 1 && x.bottom > q.top + 1 && x.top < q.bottom - 1;
  const cobre = [];
  for (const [n, r] of outros) for (const [m, q] of cartas) if (toca(r, q)) cobre.push(`${n}×${m}`);
  for (let i = 0; i < cartas.length; i++) for (let k = i + 1; k < cartas.length; k++) if (toca(cartas[i][1], cartas[k][1])) cobre.push(`${cartas[i][0]}×${cartas[k][0]}`);
  const nomes = cartas.map(([, , c]) => c.querySelector(".carta-nome span")).filter(Boolean);
  return { arena: Math.round(a.height), registro: Math.round(document.getElementById("pagina").getBoundingClientRect().height), compacta: document.getElementById("arena").classList.contains("compacta"),
    cobre: cobre.join(", ") || "nada", nomes_cortados: nomes.filter((e) => e.scrollWidth > e.clientWidth + 1).map((e) => `${e.textContent} (${e.clientWidth}/${e.scrollWidth} px)`).join("; ") || "nenhum",
    nome_mais_estreito: Math.min(...nomes.map((e) => e.clientWidth)), efeitos: document.querySelectorAll("#batalha .carta .ef").length };
});
// o seletor: onde abriu, quantas faixas inteiras à vista, se a lista rola, a descrição
const seletor = (p) => p.evaluate(() => {
  const j = document.querySelector(".roda-janela"); if (!j) return "fechado";
  const l = j.querySelector(".rj-lista"), r = j.getBoundingClientRect(), m = l.getBoundingClientRect();
  const fs = [...l.querySelectorAll(".rj-linha")];
  const inteiras = fs.filter((e) => { const q = e.getBoundingClientRect(); return q.top >= m.top - 1 && q.bottom <= m.bottom + 1 && q.top >= 0 && q.bottom <= innerHeight; }).length;
  const d = j.querySelector(".rj-descricao"), c = j.querySelector(".rj-desc-caixa");
  const lugar = j.classList.contains("lateral") ? "sobre a ficha" : j.classList.contains("tres") ? "embaixo, em três colunas" : "embaixo";
  const nomesCortados = fs.map((e) => e.querySelector(".rj-nome")).filter((e) => e && (e.scrollWidth > e.clientWidth + 1)).length;
  return { lugar, tamanho: `${Math.round(r.width)}×${Math.round(r.height)}`, faixas: `${inteiras} de ${fs.length} inteiras à vista`, lista_rola: l.scrollHeight > l.clientHeight + 1,
    descricao: d ? `${Math.round(d.getBoundingClientRect().height)} px${c && c.classList.contains("rola") ? ", rola" : ""}${c && c.scrollHeight > c.clientHeight + 1 ? " (texto maior que a área)" : ""}` : "—", nomes_cortados: nomesCortados };
});

for (const [luta, amb] of LUTAS) {
  for (const [jan, tam] of JANELAS) for (const versao of VERSOES) {
    const H = tam[1], n = (c) => `${jan}-${luta}-${versao}-${c}`, r = { nome: `${jan}-${luta}-${versao}` };
    const { proc, url } = await subir(amb);
    try {
      const p = await pagina(url, tam, versao, r.nome);
      await vez(p);
      await (await slot(p, "atacar")).click();
      for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
      const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
      await espera(700); await vez(p); await p.mouse.move(5, H - 5); await espera(800);
      await p.screenshot({ path: path.join(SAIDA, `${n("1-tela")}.png`) });
      r.parado = await arena(p);
      const ref = await disposicao(p);
      // Habilidades: a descrição mais longa e a mais curta
      await (await slot(p, "habilidades")).click(); await espera(600); await p.mouse.move(5, H - 5); await espera(200);
      r.habilidades = await seletor(p);
      r.abrir_mexe = mexe(ref, await disposicao(p));
      r.abrir_cobre = (await arena(p)).cobre;
      const linhas = await p.$$(".roda-janela .rj-linha");
      // mede o tamanho de cada descrição pondo o mouse em cada uma; fica a mais longa e a mais curta
      let maior = { k: 0, h: 0 }, menor = { k: 0, h: 1e9 };
      for (let k = 0; k < linhas.length; k++) {
        await linhas[k].hover(); await espera(120);
        const h = await p.evaluate(() => { const c = document.querySelector(".rj-desc-caixa"); return c ? c.scrollHeight : 0; });
        if (h > maior.h) maior = { k, h }; if (h < menor.h) menor = { k, h };
      }
      await linhas[maior.k].hover(); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${n("2-habilidades-longa")}.png`) });
      r.descricao_longa = await seletor(p);
      await linhas[menor.k].hover(); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${n("3-habilidades-curta")}.png`) });
      // alternar para Itens
      await p.mouse.move(5, H - 5);
      await (await slot(p, "itens")).click(); await espera(600); await p.mouse.move(5, H - 5); await espera(200);
      r.itens = await seletor(p);
      r.alternar_mexe = mexe(ref, await disposicao(p));
      await p.screenshot({ path: path.join(SAIDA, `${n("4-itens")}.png`) });
      await (await slot(p, "itens")).click(); await espera(400);
      r.fechar_mexe = mexe(ref, await disposicao(p));
      // a mira: uma habilidade de um alvo; o lembrete e o Voltar; a saída e a entrada SIMULADAS
      await (await slot(p, "habilidades")).click(); await espera(500);
      const hab = await p.evaluate((um) => (document.querySelector(um.map((h) => `.roda-janela .rj-linha:not(.bloqueada)[data-hab="${h}"]`).join(", ")) || {}).dataset?.hab || null, UM_ALVO);
      if (hab) await (await p.$(`.roda-janela .rj-linha[data-hab="${hab}"]`)).click(); else { await p.keyboard.press("Escape"); await (await slot(p, "atacar")).click(); }
      await espera(900); await p.mouse.move(5, H - 5); await espera(250);
      r.mira = (await arena(p)).cobre;
      await p.screenshot({ path: path.join(SAIDA, `${n("5-mira")}.png`) });
      r.saida_entrada_simuladas = await p.evaluate(async () => {
        const pos = () => Object.fromEntries([...document.querySelectorAll("#batalha .carta")].map((c) => { const q = c.getBoundingClientRect(); return [c.dataset.uid, [Math.round(q.left), Math.round(q.top)]]; }));
        const cb = JSON.parse(JSON.stringify(estado.combate)), vivos = cb.inimigos.filter((e) => e.vivo);
        if (vivos.length < 2) return "menos de dois vivos";
        const sai = vivos[0].uid, p0 = pos();
        Batalha.desenhar({ ...cb, inimigos: cb.inimigos.filter((e) => e.uid !== sai) }, estado.heroi);
        const p1 = pos(), m1 = Object.keys(p1).filter((u) => p0[u] && (p0[u][0] !== p1[u][0] || p0[u][1] !== p1[u][1]));
        await Batalha.lance({ tipo: "nada" }); await new Promise((res) => setTimeout(res, 450));
        const base = cb.inimigos.filter((e) => e.uid !== sai), novo = { ...vivos[1], uid: "reforco-simulado", nome: "Lobo A (invocado)", invocado: true };
        const p2 = pos(); Batalha.desenhar({ ...cb, inimigos: [...base, novo] }, estado.heroi); const p3 = pos();
        const m3 = Object.keys(p2).filter((u) => p3[u] && (p2[u][0] !== p3[u][0] || p2[u][1] !== p3[u][1]));
        return `saída: as outras que mexeram durante a mira: ${m1.join(", ") || "nenhuma"}; entrada: as outras que mexeram: ${m3.join(", ") || "nenhuma"}`;
      });
      const v = await p.$(".mira-voltar"); if (v) await v.click(); else await p.keyboard.press("Escape");
      await vez(p); await espera(400);
      r.voltar = (await slot(p, "habilidades")) ? "a roda de volta" : "ERRO";
      // SIMULADO: três ou quatro efeitos em cada combatente (os nomes longos e muitos efeitos)
      r.efeitos_simulados = await p.evaluate(() => {
        const ids = Object.keys(estado.estados || {}).length ? Object.keys(estado.estados) : ["sangrando", "envenenado", "fortalecido", "marcado"];
        const pegar = (k) => ids.slice(k % 3, (k % 3) + 3 + (k % 2)).map((id) => ({ id, nome: id, turnos: 2 + (k % 3), efeito: id }));
        const cb = JSON.parse(JSON.stringify(estado.combate));
        cb.inimigos.forEach((e, k) => { if (e.vivo) e.efeitos = pegar(k); });
        cb.aliados.forEach((e, k) => { if (e.vivo) e.efeitos = pegar(k + 1); });
        cb.heroi.efeitos = pegar(0);
        Batalha.desenhar(cb, estado.heroi);
        return "três ou quatro efeitos em cada um (estado da luta alterado só na tela)";
      });
      await espera(600); await p.mouse.move(5, H - 5);
      r.com_efeitos = await arena(p);
      await p.screenshot({ path: path.join(SAIDA, `${n("6-efeitos-simulados")}.png`) });
      await (await slot(p, "habilidades")).click(); await espera(600); await p.mouse.move(5, H - 5); await espera(200);
      r.habilidades_com_efeitos = await seletor(p);
      await p.screenshot({ path: path.join(SAIDA, `${n("7-efeitos-simulados-habilidades")}.png`) });
      relatorio.push(r);
      console.log(JSON.stringify(r));
      await p.close();
    } finally { proc.kill(); }
  }
}
// o teclado e o movimento reduzido: a luta maior em 1280×720
for (const versao of VERSOES) {
  const r = { nome: `teclado-${versao}` };
  const { proc, url } = await subir(TODAS.maior);
  try {
    const p = await pagina(url, [1280, 720], versao, r.nome, { reducedMotion: "reduce" });
    await vez(p); await espera(500);
    await p.keyboard.press("2"); await espera(500);
    r.tecla_2 = await p.evaluate(() => { const a = document.activeElement; return `${document.querySelectorAll(".roda-janela").length} seletor; foco: ${a.closest(".rj-linha") ? a.querySelector(".rj-nome").textContent : a.tagName}`; });
    for (let k = 0; k < 6; k++) await p.keyboard.press("ArrowDown");
    await espera(200);
    r.setas = await p.evaluate(() => { const a = document.activeElement, q = a.getBoundingClientRect(), l = a.closest(".rj-lista")?.getBoundingClientRect();
      return `foco na ${[...document.querySelectorAll(".rj-linha")].indexOf(a) + 1}ª (${a.querySelector(".rj-nome")?.textContent}); ${l && q.top >= l.top - 1 && q.bottom <= l.bottom + 1 ? "inteira à vista" : "FORA DA VISTA"}; ${a.matches(":focus-visible") ? "foco visível" : "sem foco visível"}`; });
    r.animacao = await p.evaluate(() => getComputedStyle(document.querySelector(".roda-janela .rj-linha")).animationName);
    await p.screenshot({ path: path.join(SAIDA, `teclado-${versao}.png`) });
    await p.keyboard.press("Escape"); await espera(300);
    r.esc = await p.evaluate(() => `${document.querySelectorAll(".roda-janela").length} seletor; foco: ${document.activeElement.dataset.slot || document.activeElement.tagName}`);
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, process.env.MANTER ? "relatorio-parcial.json" : "relatorio.json"), JSON.stringify({ versoes: VERSOES, relatorio, erros }, null, 1));
console.log(erros.length ? erros.join("\n") : "sem erros");
