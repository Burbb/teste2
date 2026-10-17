// Protótipo da vida máxima bloqueada (etapa 1B): fotos e medidas dos três estados e de duas mudanças reais.
// O jogo roda pelo cenario.py desta pasta (o estado do herói com `vida_bloqueio`, das contas do motor) e a página
// recebe vida.css e vida.js por cima; nada do jogo é trocado.
//   saudavel    sem penalidade (a barra de sempre), 1280×720
//   limite      corte profundo, queimadura grave e fome: vida no limite (cheia até onde dá), 1280×720 e 1500×950
//   abaixo      os mesmos, com vida abaixo do limite, 1280×720; a dica da vida aberta
//   luta        os mesmos numa luta (a carta do herói e o topo), 1280×720: uma rodada de verdade (o herói apanha)
//   curandeira  corte profundo, na vila: tratar na Curandeira (o motor tira o ferimento e devolve a diferença da vida)
//   equipar     corte profundo: a peça com +vida máxima vestida pelo achado (o saudável e o limite sobem juntos)
// Em cada foto, a medida: o que a barra mostra (preenchido, vazio e bloqueado, em pontos de vida) contra o estado.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/vida-bloqueada/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync, readdirSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
for (const f of readdirSync(SAIDA)) if (/\.(png|json)$/.test(f)) rmSync(path.join(SAIDA, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";
const BASE = { TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel" };
const FERIDO = { FERIMENTOS: "corte,queimadura", FOME: "1" };
const relatorio = [], erros = [];

async function subir(amb) {
  const proc = spawn(PY, [path.join(aqui, "cenario.py"), "tutorial"], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[cenario] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, [W, H], nome) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  await p.waitForFunction(() => typeof estado !== "undefined" && estado && estado.heroi, null, { timeout: 20000 });
  await p.addStyleTag({ path: path.join(aqui, "vida.css") });
  await p.addScriptTag({ path: path.join(aqui, "vida.js") });
  await espera(600);
  return p;
}
async function pronto(p) {  // sem cena correndo nem quadro de orientação por cima
  for (let k = 0; k < 120; k++) {
    if (await p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
}
// o que a barra mostra, em pontos de vida, contra o estado do motor
const medir = (p) => p.evaluate(() => {
  const h = estado.heroi, bq = h.vida_bloqueio, total = bq ? bq.saudavel : h.max_hp;
  const ler = (bar, num) => {
    if (!bar) return null;
    const cs = getComputedStyle(bar), B = { width: bar.getBoundingClientRect().width - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth) }, enc = bar.querySelector(".enchimento").getBoundingClientRect(), z = bar.querySelector(":scope > .bloqueio");
    const zr = z ? z.getBoundingClientRect() : { width: 0 };
    const pts = (px) => Math.round((px / B.width) * total * 10) / 10;
    return { preenchido: pts(enc.width), bloqueado: pts(zr.width), vazio: Math.round((total - pts(enc.width) - pts(zr.width)) * 10) / 10, numero: num ? num.textContent.trim() : "",
      marca_do_limite: z ? getComputedStyle(z, "::before").backgroundColor : "—", hachura: z ? getComputedStyle(z).backgroundImage.startsWith("repeating-linear-gradient") : false };
  };
  const v = document.querySelector('#hud-linha .vital[data-vital="hp"]'), c = typeof Batalha !== "undefined" && Batalha.elCarta("j");
  return { estado: { vida: h.hp, limite: h.max_hp, saudavel: bq ? bq.saudavel : h.max_hp, fontes: bq ? bq.fontes.map((f) => `${f.nome} −${f.pct}% (−${f.perda})`).join(", ") : "nenhuma" },
    topo: ler(v && v.querySelector(".barra-px"), v && v.querySelector(".num")), carta: c ? ler(c.querySelector(".carta-hp .barra-px"), c.querySelector(".carta-hp .num")) : null };
});
const foto = (p, nome, recorte) => p.screenshot({ path: path.join(SAIDA, `${nome}.png`), ...(recorte ? { clip: recorte } : {}) });
const recorteTopo = (p) => p.evaluate(() => { const r = document.getElementById("hud-linha").getBoundingClientRect(); return { x: 0, y: Math.max(0, r.top - 8), width: Math.min(innerWidth, r.right + 8), height: r.height + 16 }; });

async function caso(nome, amb, tam, passos) {
  const { proc, url } = await subir(amb);
  try {
    const p = await pagina(url, tam, nome);
    await pronto(p);
    const r = { nome, janela: `${tam[0]}×${tam[1]}` };
    await passos(p, r);
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}

// os três estados, no topo
await caso("saudavel", { ...BASE, VIDA: "1" }, [1280, 720], async (p, r) => {
  r.medida = await medir(p); await foto(p, "saudavel-1280x720"); await foto(p, "saudavel-topo", await recorteTopo(p));
});
await caso("limite", { ...BASE, ...FERIDO, VIDA: "1" }, [1280, 720], async (p, r) => {
  r.medida = await medir(p); await foto(p, "limite-1280x720"); await foto(p, "limite-topo", await recorteTopo(p));
});
await caso("limite-1500", { ...BASE, ...FERIDO, VIDA: "1" }, [1500, 950], async (p, r) => {
  r.medida = await medir(p); await foto(p, "limite-1500x950"); await foto(p, "limite-1500-topo", await recorteTopo(p));
});
await caso("abaixo", { ...BASE, ...FERIDO, VIDA: "0.6" }, [1280, 720], async (p, r) => {
  r.medida = await medir(p); await foto(p, "abaixo-1280x720"); await foto(p, "abaixo-topo", await recorteTopo(p));
  // parada, a página não reescreve nada (sem laço entre o observador e o número)
  const e0 = await p.evaluate(() => window.__vidaEscritas || 0); await espera(1500);
  r.escritas_em_1500ms_parada = (await p.evaluate(() => window.__vidaEscritas || 0)) - e0;
  await p.hover('#hud-linha .vital[data-vital="hp"] .barra-px'); await espera(700);
  r.dica = await p.evaluate(() => { const d = document.getElementById("dica-item"); return d && !d.hidden ? d.innerText : ""; });
  await foto(p, "abaixo-dica-1280x720");
});
// na luta: a carta do herói e o topo; uma rodada de verdade, o herói apanha
await caso("luta", { ...BASE, ...FERIDO, VIDA: "0.6", LUTA: "lobo", QUANTOS: "2", NIVEL_LUTA: "6" }, [1280, 720], async (p, r) => {
  for (let k = 0; k < 120 && !(await p.$('#roda .roda-botao[data-slot="atacar"]')); k++) { await pronto(p); await espera(200); }
  r.antes = await medir(p); await foto(p, "luta-antes-1280x720");
  // durante a rodada, a cada quadro: o número da carta nunca passa do limite nem sobe sem cura
  await p.evaluate(() => { window.__nums = []; let u = ""; const q = () => { const c = Batalha.elCarta("j"); const t = c && c.querySelector(".carta-hp .num").textContent; if (t !== u) { u = t; window.__nums.push(t); } requestAnimationFrame(q); }; requestAnimationFrame(q); });
  await (await p.$('#roda .roda-botao[data-slot="atacar"]')).click();
  for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
  const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
  for (let k = 0; k < 120 && !(await p.evaluate(() => !!document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando)); k++) await espera(150);
  await espera(900); await p.mouse.move(5, 715);
  r.numeros_na_carta_durante_a_rodada = await p.evaluate(() => window.__nums.join(" → "));
  r.depois = await medir(p); await foto(p, "luta-depois-1280x720");
});
// mudanças reais: tratar na Curandeira; vestir a peça com +vida máxima
await caso("curandeira", { ...BASE, FERIMENTOS: "corte", VIDA: "0.7", OURO: "200", GRATIS_USADO: "" }, [1280, 720], async (p, r) => {
  r.antes = await medir(p); await foto(p, "curandeira-antes-topo", await recorteTopo(p));
  await p.click('#predios .predio[data-predio="curandeiro"]'); await espera(1200); await pronto(p);
  await p.click('#texto .curandeira [data-tratar="corte"] >> nth=-1');
  await p.waitForFunction(() => estado.heroi.ferimentos.length === 0, null, { timeout: 15000 }).catch(() => {});
  await espera(1200);
  r.depois = await medir(p); await foto(p, "curandeira-depois-topo", await recorteTopo(p)); await foto(p, "curandeira-depois-1280x720");
});
await caso("equipar", { ...BASE, FERIMENTOS: "corte", VIDA: "0.7", PECA_VIDA: "1" }, [1280, 720], async (p, r) => {
  await p.waitForSelector("#sobre-achado .achado-acoes button:not(.reserva)", { timeout: 20000 }); await espera(700);
  r.antes = await medir(p); await foto(p, "equipar-antes-1280x720");
  r.botao = await p.evaluate(() => document.querySelector("#sobre-achado .achado-acoes button:not(.reserva)").textContent);
  await p.click("#sobre-achado .achado-acoes button:not(.reserva)"); await espera(1500);
  r.depois = await medir(p); await foto(p, "equipar-depois-topo", await recorteTopo(p));
});
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
console.log(erros.length ? `ERROS ${erros.join(" | ")}` : "sem erros");
