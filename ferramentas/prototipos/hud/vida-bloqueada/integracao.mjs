// A vida máxima bloqueada INTEGRADA (1.115.0): o jogo como está, sem folha nem script de protótipo por cima. O
// cenario.py desta pasta só oferece, no caso "equipar", a peça com +vida máxima pelo achado (PECA_VIDA); o estado do
// herói é o do jogo.
//   estados     sem penalidade, no limite e abaixo dele (corte profundo, queimadura grave e fome), em 1280×720 e
//               1500×950: o topo, as barras (o comprimento igual com e sem bloqueio), o número, a etiqueta e a dica
//   pocao       abaixo do limite, com Morel: a poção da bolsa, a linha "Em você" e a cura que para no limite; depois,
//               no limite, o motivo da poção que não serve
//   luta        uma rodada em que o herói apanha: o número da carta a cada quadro (só desce)
//   curandeira  tratar o corte: o motor devolve a parte dele como vida; o bloqueio sai
//   equipar     vestir a peça com +vida máxima: o saudável e o limite sobem juntos
//   movimento reduzido em todos.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/vida-bloqueada/integracao.mjs
import { spawn } from "child_process";
import { mkdirSync, readdirSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.join(aqui, "capturas-integracao");
mkdirSync(SAIDA, { recursive: true });
for (const f of readdirSync(SAIDA)) if (/\.(png|json)$/.test(f)) rmSync(path.join(SAIDA, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";
const BASE = { TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel" };
const FERIDO = { FERIMENTOS: "corte,queimadura", FOME: "1" };
const relatorio = [], erros = [];

async function subir(amb, viaCenario) {
  const args = viaCenario ? [path.join(aqui, "cenario.py"), "tutorial"] : ["-m", "tests.navegador.cenarios", "tutorial"];
  const proc = spawn(PY, args, { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[cenario] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, [W, H], nome) {
  const p = await b.newPage({ viewport: { width: W, height: H }, reducedMotion: "reduce" });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  await p.waitForFunction(() => typeof estado !== "undefined" && estado && estado.heroi, null, { timeout: 20000 });
  await espera(600);
  return p;
}
async function pronto(p) {
  for (let k = 0; k < 120; k++) {
    if (await p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
}
// o que a barra mostra, em pontos de vida, contra o estado do motor; e o comprimento das barras do topo
const medir = (p) => p.evaluate(() => {
  const h = estado.heroi, vb = h.vida_bloqueio, total = vb ? vb.saudavel : h.max_hp;
  const ler = (bar, num) => {
    if (!bar || !bar.getClientRects().length) return null;
    const cs = getComputedStyle(bar), W = bar.getBoundingClientRect().width - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth);
    const enc = bar.querySelector(".enchimento").getBoundingClientRect().width, z = bar.querySelector(":scope > .bloqueio");
    const pts = (px) => Math.round((px / W) * total * 10) / 10;
    return { preenchido: pts(enc), bloqueado: pts(z ? z.getBoundingClientRect().width : 0), numero: num ? num.textContent.trim() : "" };
  };
  const v = document.querySelector('#hud-linha .vital[data-vital="hp"]'), r = document.querySelector('#hud-linha .vital[data-vital="rec"]');
  const c = typeof Batalha !== "undefined" && Batalha.elCarta("j");
  const larg = (x) => (x ? Math.round(x.querySelector(".barra-px").getBoundingClientRect().width * 10) / 10 : null);
  const cond = document.querySelector(".hud-condicoes"), etiqueta = document.querySelector(".condicao.bloqueio-vida");
  return { estado: { vida: h.hp, limite: h.max_hp, saudavel: total, bloqueio: vb ? `−${vb.bloqueado}: ${vb.fontes.map((f) => `${f.nome} −${f.pct}% (−${f.perda})`).join(", ")}` : "nenhum" },
    topo: ler(v && v.querySelector(".barra-px"), v && v.querySelector(".num")), barra_vida_px: larg(v), barra_recurso_px: larg(r),
    etiqueta: etiqueta ? etiqueta.textContent.trim() : "—",
    etiqueta_inteira: etiqueta ? etiqueta.getBoundingClientRect().right <= cond.getBoundingClientRect().right + 0.5 : null,
    carta: c ? ler(c.querySelector(".carta-hp .barra-px"), c.querySelector(".carta-hp .num")) : null };
});
const foto = (p, nome, recorte) => p.screenshot({ path: path.join(SAIDA, `${nome}.png`), ...(recorte ? { clip: recorte } : {}) });
const recorteTopo = (p) => p.evaluate(() => { const r = document.getElementById("hud-linha").getBoundingClientRect(); return { x: 0, y: Math.max(0, r.top - 8), width: Math.min(innerWidth, r.right + 8), height: r.height + 16 }; });
async function caso(nome, amb, tam, passos, viaCenario = false) {
  const { proc, url } = await subir(amb, viaCenario);
  try {
    const p = await pagina(url, tam, nome);
    await pronto(p);
    const r = { nome, janela: `${tam[0]}×${tam[1]}` };
    await passos(p, r);
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}

for (const tam of [[1280, 720], [1500, 950]]) {
  const t = `${tam[0]}x${tam[1]}`;
  await caso(`saudavel-${t}`, { ...BASE, VIDA: "1" }, tam, async (p, r) => { r.medida = await medir(p); await foto(p, `saudavel-${t}-topo`, await recorteTopo(p)); await foto(p, `saudavel-${t}`); });
  await caso(`limite-${t}`, { ...BASE, ...FERIDO, VIDA: "1" }, tam, async (p, r) => {
    r.medida = await medir(p); await foto(p, `limite-${t}-topo`, await recorteTopo(p)); await foto(p, `limite-${t}`);
    // a poção no limite: o motivo do motor (sem "vida cheia" a 104/146)
    r.motivo_da_pocao = await p.evaluate(() => (estado.heroi.bolsa || []).filter((x) => x.id === "pocao_vida").map((x) => x.motivo).join(" | "));
  });
  await caso(`abaixo-${t}`, { ...BASE, ...FERIDO, VIDA: "0.6" }, tam, async (p, r) => {
    r.medida = await medir(p); await foto(p, `abaixo-${t}-topo`, await recorteTopo(p));
    await p.hover('#hud-linha .vital[data-vital="hp"] .barra-px'); await espera(600);
    r.dica = await p.evaluate(() => { const d = document.getElementById("dica-item"); return d && !d.hidden ? d.innerText : ""; });
    await foto(p, `abaixo-${t}-dica`);
  });
}
// a cura comum até o limite: a poção da bolsa com Morel por perto (a linha "Em você")
await caso("pocao", { ...BASE, ...FERIDO, VIDA: "0.9", FERIDO: "morel" }, [1280, 720], async (p, r) => {
  r.antes = await medir(p);
  await p.click('#heroi .slot-px[data-bolsa="pocao_vida"]'); await espera(500);
  r.em_voce = await p.evaluate(() => { const m = document.querySelector(".menu-uso"); return m ? m.innerText.replace(/\s+/g, " ") : "SEM MENU"; });
  await foto(p, "pocao-menu-1280x720");
  const reco = await p.evaluate(() => { const m = document.querySelector(".menu-uso").getBoundingClientRect(); return { x: Math.max(0, m.left - 10), y: Math.max(0, m.top - 60), width: Math.min(innerWidth - Math.max(0, m.left - 10), m.width + 330), height: m.height + 90 }; });
  await foto(p, "pocao-menu-recorte", reco);
  await p.click('.menu-uso button[data-em=""]');
  await p.waitForFunction((hp) => estado.heroi.hp !== hp, r.antes.estado.vida, { timeout: 10000 }).catch(() => {});
  await espera(1200);
  r.depois = await medir(p); await foto(p, "pocao-depois-topo", await recorteTopo(p));
  r.cura_obedece_o_limite = r.depois.estado.vida <= r.depois.estado.limite ? `sim (${r.antes.estado.vida} → ${r.depois.estado.vida}, limite ${r.depois.estado.limite})` : "NÃO";
});
// na luta: a carta do herói a cada quadro durante uma rodada em que ele apanha
await caso("luta", { ...BASE, ...FERIDO, VIDA: "0.6", LUTA: "lobo", QUANTOS: "2", NIVEL_LUTA: "6" }, [1280, 720], async (p, r) => {
  for (let k = 0; k < 120 && !(await p.$('#roda .roda-botao[data-slot="atacar"]')); k++) { await pronto(p); await espera(200); }
  r.antes = await medir(p); await foto(p, "luta-antes-1280x720");
  await p.evaluate(() => { window.__nums = []; let u = ""; const q = () => { const c = Batalha.elCarta("j"); const t = c && c.querySelector(".carta-hp .num").textContent; if (t !== u) { u = t; window.__nums.push(t); } requestAnimationFrame(q); }; requestAnimationFrame(q); });
  await (await p.$('#roda .roda-botao[data-slot="atacar"]')).click();
  for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
  const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
  for (let k = 0; k < 120 && !(await p.evaluate(() => !!document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando)); k++) await espera(150);
  await espera(900); await p.mouse.move(5, 715);
  r.numeros_na_carta = await p.evaluate(() => window.__nums.join(" → "));
  r.depois = await medir(p); await foto(p, "luta-depois-1280x720");
});
// as mudanças reais
await caso("curandeira", { ...BASE, FERIMENTOS: "corte", VIDA: "0.7", OURO: "200" }, [1280, 720], async (p, r) => {
  r.antes = await medir(p); await foto(p, "curandeira-antes-topo", await recorteTopo(p));
  await p.click('#predios .predio[data-predio="curandeiro"]'); await espera(1200); await pronto(p);
  await p.click('#texto .curandeira [data-tratar="corte"] >> nth=-1');
  await p.waitForFunction(() => estado.heroi.ferimentos.length === 0, null, { timeout: 15000 }).catch(() => {});
  await espera(1200);
  r.depois = await medir(p); await foto(p, "curandeira-depois-topo", await recorteTopo(p));
});
await caso("equipar", { ...BASE, FERIMENTOS: "corte", VIDA: "0.7", PECA_VIDA: "1" }, [1280, 720], async (p, r) => {
  await p.waitForSelector("#sobre-achado .achado-acoes button:not(.reserva)", { timeout: 20000 }); await espera(700);
  r.antes = await medir(p);
  await p.click("#sobre-achado .achado-acoes button:not(.reserva)"); await espera(1500);
  r.depois = await medir(p); await foto(p, "equipar-depois-topo", await recorteTopo(p));
}, true);
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
console.log(erros.length ? `ERROS ${erros.join(" | ")}` : "sem erros");
