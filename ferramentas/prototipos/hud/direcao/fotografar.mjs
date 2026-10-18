// A nova direção visual da HUD (plano 23, estudo em avaliação): atual × proposta com os mesmos dados.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/direcao/fotografar.mjs [atual|proposta]
// A proposta é direcao.css (e direcao.js, só a marcação da dica dos testes) anexada à página; o jogo não muda.
// A janela: 1920×945, a área do jogo numa janela maximizada no monitor 1920×1080 do Jean.
// Os casos (tests/navegador/cenarios.py):
//   exploração: a Capela Afogada de dia (arqueiro patrulheiro nível 5), com a dica "Testes do d20" aberta;
//   luta: o paladino nível 8 com Morel contra 3 lobos, no começo da vez e com o seletor de Habilidades aberto.
// Também confere o que a proposta não pode estragar: o foco do teclado visível, as dicas, a mira, a ação.
import { spawn } from "child_process";
import { readFileSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas");
const JANELA = { width: 1920, height: 945 };
const modos = process.argv[2] ? [process.argv[2]] : ["atual", "proposta"];
mkdirSync(SAIDA, { recursive: true });
for (const f of readdirSync(SAIDA)) if (/\.png$/.test(f) && modos.some((m) => f.startsWith(m))) rmSync(path.join(SAIDA, f));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";
const CASOS = {
  exploracao: { cenario: "capela", amb: { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" } },
  luta: { cenario: "tutorial", amb: { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7", SEMENTE: "7" } },
};

async function subir(caso) {
  const { cenario, amb } = CASOS[caso];
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
export async function anexar(p) {
  const JS = readFileSync(path.join(aqui, "direcao.js"), "utf8"), CSS = readFileSync(path.join(aqui, "direcao.css"), "utf8");
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch();
    const corpo = (await res.text()) + `\n;(() => { const s = document.createElement("style"); s.id = "direcao"; s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
}
const parado = (p) => p.waitForFunction(() => !processando && pergunta, null, { timeout: 30000 });

const b = await chromium.launch();
const rel = [];
for (const modo of modos) {
  // a exploração, com a dica dos testes aberta
  {
    const { proc, url } = await subir("exploracao");
    try {
      const p = await b.newPage({ viewport: JANELA });
      const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
      if (modo === "proposta") await anexar(p);
      await p.goto(url); await parado(p); await espera(1500);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-1-exploracao.png`) });
      await p.hover(".testes-ficha"); await espera(600);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-2-dica-testes.png`) });
      // o foco do teclado num caminho do mundo e numa escolha
      await p.mouse.move(5, 5); await p.keyboard.press("Tab"); await espera(200);
      const foco = await p.evaluate(() => { const a = document.activeElement; const cs = a && getComputedStyle(a); return a ? `${a.tagName}.${a.className} outline ${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineColor} sombra ${cs.boxShadow.slice(0, 60)}` : null; });
      rel.push({ modo, caso: "exploracao", erros, foco });
      await p.close();
    } finally { proc.kill(); }
  }
  // a luta: o começo da vez e o seletor aberto
  {
    const { proc, url } = await subir("luta");
    try {
      const p = await b.newPage({ viewport: JANELA });
      const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
      if (modo === "proposta") await anexar(p);
      await p.goto(url);
      await p.waitForSelector('#prompt .escolha:has-text("Começar a luta")'); await p.click('#prompt .escolha:has-text("Começar a luta")');
      await p.waitForFunction(() => document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando, null, { timeout: 30000 });
      await espera(1800);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-3-luta.png`) });
      await p.click('#roda .roda-botao[data-slot="habilidades"]'); await espera(500);
      const linha = await p.$(".roda-janela .rj-linha:not(.indisponivel)"); if (linha) await linha.hover(); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${modo}-4-seletor.png`) });
      // a ação continua: Voltar e atacar um lobo
      await p.keyboard.press("Escape"); await espera(300);
      await p.click('#roda .roda-botao[data-slot="atacar"]'); await espera(300);
      const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) { await alvo.hover(); await espera(200); await p.screenshot({ path: path.join(SAIDA, `${modo}-5-mira.png`) }); await alvo.click(); }
      await p.waitForFunction(() => estado && estado.combate && estado.combate.turno >= 2 || !estado.combate, null, { timeout: 20000 }).catch(() => {});
      rel.push({ modo, caso: "luta", erros, turno: await p.evaluate(() => estado && estado.combate && estado.combate.turno) });
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
for (const r of rel) console.log(JSON.stringify(r));
writeFileSync(path.join(SAIDA, `relatorio-${modos.join("-")}.json`), JSON.stringify(rel, null, 1));
