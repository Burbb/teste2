// O grimório fechado da nova referência do Jean (protótipo, só o 64): fotografa o cartão do saque do jogo de verdade
// com o desenho de hoje (o sprite 16×16 "livro") e com a proposta (livro-fechado-ref/livro-64.png, de
// ferramentas/arte/desenhar_grimorio_fechado_pixel.py), com os mesmos dados. Na proposta, a página recebe um
// icones.js com o livro registrado só em 64 (TAMANHOS e ITEM) e o arquivo vem da pasta; o jogo não muda. O 64 só fica
// parado no cartão do saque, então é o único lugar fotografado: o Mago acha um Grimório (ACHADO=livro) vestindo o
// cajado aprovado (ARMA=cajado), que aparece ao lado no "você usa" em 48. Em 1500×950 e 1280×720.
// Guarda em capturas-livro-fechado/<janela>-<versao>-<lugar>.png e o recorte ampliável do 64 como zoom-...
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_livro_fechado.mjs
import { spawn } from "child_process";
import { mkdirSync, readFileSync, rmSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-livro-fechado"), PASTA = path.join(aqui, "livro-fechado-ref");
rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const TROCAS = [['const TAMANHOS = {', 'const TAMANHOS = {"livro": [64], '], ['orbe: "orbe" };', 'orbe: "orbe", livro: "livro" };']];
const iconesProposta = TROCAS.reduce((t, [a, b]) => {
  if (!t.includes(a)) throw new Error(`icones.js mudou: não achei ${a}`);
  return t.replace(a, b);
}, readFileSync(path.join(raiz, "rpg/web/static/icones.js"), "utf8"));
async function subir(cenario, amb) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function recortar(p, sel, nome, folga) {
  const c = await p.evaluate(([s, f]) => {
    const e = document.querySelector(s);
    if (!e) return null;
    const r = e.getBoundingClientRect();
    return { x: Math.max(0, Math.floor(r.left - f)), y: Math.max(0, Math.floor(r.top - f)), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) };
  }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
for (const jan of Object.keys(JANELAS)) for (const versao of ["atual", "fechado"]) {
  const n = (c) => `${jan}-${versao}-${c}`;
  const { proc, url } = await subir("vila", { CLASSE: "mago", ACHADO: "livro", ARMA: "cajado" });
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  if (versao === "fechado") {
    await p.route(/\/static\/icones\.js(\?|$)/, (r) => r.fulfill({ body: iconesProposta, contentType: "application/javascript" }));
    await p.route(/\/static\/hud\/icones\/livro-[^/]+\.png/, (r) => r.fulfill({
      path: path.join(PASTA, path.basename(new URL(r.request().url()).pathname)), contentType: "image/png" }));
  }
  p.on("pageerror", (e) => erros.push(`${n("saque")}: ${e}`));
  p.on("response", (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) erros.push(`${n("saque")}: ${r.status()} ${r.url()}`); });
  await p.goto(url);
  await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2600);
  await p.mouse.move(2, 2); await espera(200);
  await p.screenshot({ path: path.join(SAIDA, `${n("tela-saque")}.png`) });
  await recortar(p, ".janela-achado", n("saque-cartao"), 6);
  await recortar(p, ".janela-achado .achado-cartao.novo .achado-arte", `zoom-${n("saque-64")}`, 2);
  // o arquivo e o tamanho do livro no cartão (a proposta tem que vir de livro-64.png, em 64 px)
  const qual = await p.evaluate(() => [...document.querySelectorAll(".janela-achado img")].map((i) =>
    `${(i.getAttribute("src") || "").split("/").pop().slice(0, 40)}→${Math.round(i.getBoundingClientRect().width)}`));
  console.log(jan, versao, qual.join(" "));
  await p.close(); proc.kill();
}
await b.close();
console.log(erros.length ? erros.join("\n") : "sem erros");
