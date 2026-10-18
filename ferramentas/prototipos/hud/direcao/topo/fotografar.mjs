// O estudo da HUD com o topo pintado (em avaliação, nada no jogo): jogo × topo com os mesmos dados, na janela de sempre
// (1920×945, a área do jogo no monitor 1920×1080), nas cenas das rodadas anteriores:
//   exploração: a Capela Afogada de dia (arqueiro patrulheiro nível 5), a tela inteira e a dica "Testes do d20";
//   luta: o paladino nível 8 com Morel contra 3 lobos (semente 7), a tela inteira, o seletor de Habilidades aberto e a
//   mira, e o golpe que segue para o turno 2.
//   estados: a mesma luta com o herói mordido e com fome (a vida máxima bloqueada) e com 10% do Vigor (habilidades
//   indisponíveis, com o motivo do motor): a tela inteira e o seletor aberto numa indisponível.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/direcao/topo/fotografar.mjs [jogo|topo]
// O topo é o conjunto (../ficha: ficha.css/js e pintura.css/js; ../conjunto: conjunto.css/js; ../direcao.js) +
// topo.css. Também mede: o centro (tem de seguir com 1088 px), a barra (46 px), se a página rola, e os estados.
import { spawn } from "child_process";
import { readFileSync, mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), direcao = path.resolve(aqui, ".."), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
const JANELA = { width: 1920, height: 945 };
const modos = process.argv[2] ? [process.argv[2]] : ["jogo", "topo"];
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";
const CASOS = {
  exploracao: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }],
  estados: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7", SEMENTE: "7", FERIMENTOS: "mordida", FOME: "2", REC: "0.1" }],
  luta: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7", SEMENTE: "7" }],
};

export async function anexarTopo(p) {
  const ler = (...c) => readFileSync(path.join(direcao, ...c), "utf8");
  const CSS = [ler("ficha", "ficha.css"), ler("ficha", "pintura.css"), ler("conjunto", "conjunto.css"), ler("topo", "topo.css")].join("\n");
  const JS = [ler("ficha", "ficha.js"), ler("ficha", "pintura.js"), ler("conjunto", "conjunto.js"), ler("direcao.js")].join("\n");
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch();
    const corpo = (await res.text()) + `\n;(() => { const s = document.createElement("style"); s.id = "estudo-topo"; s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
  await p.route(/\/proto-(ficha|conjunto|topo)\//, async (r) => {
    const u = new URL(r.request().url()), nome = decodeURIComponent(u.pathname.split("/").pop());
    const arquivo = u.pathname.includes("/proto-topo/") ? path.join(aqui, "pecas", nome)
      : u.pathname.includes("/proto-conjunto/") ? path.join(direcao, "conjunto", "pecas", nome)
      : nome === "painel-tinta.png" ? path.join(direcao, "Painel vertical em tinta escura.png") : path.join(direcao, "ficha", "arte", nome);
    try { r.fulfill({ body: readFileSync(arquivo), contentType: "image/png" }); } catch { r.fulfill({ status: 404, body: "" }); }
  });
}
async function subir(caso) {
  const [cenario, amb] = CASOS[caso];
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const medir = (p) => p.evaluate(() => {
  const r = (s) => { const e = document.querySelector(s); if (!e) return null; const q = e.getBoundingClientRect(); return [Math.round(q.left), Math.round(q.top), Math.round(q.width), Math.round(q.height)]; };
  const rola = (s) => { const e = document.querySelector(s); return e ? e.scrollHeight - e.clientHeight : null; };
  return { topo: r("#topo"), palco: r("#palco"), heroi: r("#heroi"), mundo: r("#mundo"), rola_pagina: document.documentElement.scrollHeight - innerHeight, rola_ficha: rola("#heroi"), rola_mundo: rola("#mundo") };
});

const b = await chromium.launch();
const rel = {};
for (const modo of modos) {
  rel[modo] = {};
  { // a exploração
    const { proc, url } = await subir("exploracao");
    try {
      const p = await b.newPage({ viewport: JANELA });
      const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
      if (modo === "topo") await anexarTopo(p);
      await p.goto(url); await p.waitForFunction(() => !processando && pergunta, null, { timeout: 30000 }); await espera(1500);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-1-exploracao.png`) });
      await p.hover("#heroi .testes-ficha"); await espera(500);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-2-dica-testes.png`), clip: { x: 0, y: 0, width: 960, height: JANELA.height } });
      // um caminho com o mouse por cima (o lugar acende no mapa) e uma escolha com o mouse por cima
      await p.hover("#mundo .caminho"); await espera(300);
      const acende = await p.evaluate(() => document.querySelectorAll(".no-btn.destacado").length);
      await p.hover("#prompt .escolha"); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-3-hover.png`), clip: { x: 420, y: 380, width: 1500, height: 300 } });
      rel[modo].exploracao = { medidas: await medir(p), caminho_acende_o_mapa: acende, erros };
      await p.close();
    } finally { proc.kill(); }
  }
  { // a luta
    const { proc, url } = await subir("luta");
    try {
      const p = await b.newPage({ viewport: JANELA });
      const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
      if (modo === "topo") await anexarTopo(p);
      await p.goto(url);
      await p.waitForSelector('#prompt .escolha:has-text("Começar a luta")'); await p.click('#prompt .escolha:has-text("Começar a luta")');
      await p.waitForFunction(() => document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando, null, { timeout: 30000 });
      await espera(1800);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-4-luta.png`) });
      await p.click('#roda .roda-botao[data-slot="habilidades"]'); await espera(500);
      const linha = await p.$(".roda-janela .rj-linha:not(.indisponivel)"); if (linha) await linha.hover(); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-5-seletor.png`) });
      await p.keyboard.press("Escape"); await espera(300);
      await p.click('#roda .roda-botao[data-slot="atacar"]'); await espera(300);
      const alvo = await p.$("#batalha .carta.alvejavel");
      if (alvo) { await alvo.hover(); await espera(250); await p.screenshot({ path: path.join(SAIDA, `${modo}-6-mira.png`) }); await alvo.click(); }
      await p.waitForFunction(() => estado && estado.combate && estado.combate.turno >= 2, null, { timeout: 20000 }).catch(() => {});
      rel[modo].luta = { medidas: await medir(p), turno: await p.evaluate(() => estado && estado.combate && estado.combate.turno), erros };
      await p.close();
    } finally { proc.kill(); }
  }
}
for (const modo of modos) { // os estados: a vida máxima bloqueada e a habilidade indisponível
  const { proc, url } = await subir("estados");
  try {
    const p = await b.newPage({ viewport: JANELA });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo === "topo") await anexarTopo(p);
    await p.goto(url);
    await p.waitForSelector('#prompt .escolha:has-text("Começar a luta")'); await p.click('#prompt .escolha:has-text("Começar a luta")');
    await p.waitForFunction(() => document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando, null, { timeout: 30000 });
    await espera(1800);
    await p.screenshot({ path: path.join(SAIDA, `${modo}-7-estados.png`) });
    await p.click('#roda .roda-botao[data-slot="habilidades"]'); await espera(500);
    const ind = await p.$(".roda-janela .rj-linha.bloqueada"); if (ind) await ind.hover(); await espera(300);
    await p.screenshot({ path: path.join(SAIDA, `${modo}-8-indisponivel.png`) });
    const dados = await p.evaluate(() => ({
      vida_bloqueio: estado.heroi.vida_bloqueio || null, hp: [estado.heroi.hp, estado.heroi.max_hp],
      indisponiveis: [...document.querySelectorAll(".roda-janela .rj-linha.bloqueada")].map((e) => e.textContent.replace(/\s+/g, " ").trim()) }));
    (rel[modo] = rel[modo] || {}).estados = { medidas: await medir(p), ...dados, erros };
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
console.log(JSON.stringify(rel, null, 1));
writeFileSync(path.join(SAIDA, `relatorio-${modos.join("-")}.json`), JSON.stringify(rel, null, 1));
