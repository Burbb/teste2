// O teste do Unguento de Prata (experimento): fotografa o jogo de verdade com o unguento atual (o sprite do jogo),
// com o primeiro candidato (desenhar_itens.py), com a primeira proposta em pixel art (o pote de louça com rótulo,
// unguento-pixel-v1/) e com o conceito novo (o pote de boticário, desenhar_unguento_pixel.py → unguento-pixel/), com os
// mesmos dados (unguento-no-jogo.js troca a imagem só onde o unguento é o assunto). Nas propostas, o escudo é o final
// (escudo-pixel/), para ver os objetos novos juntos; nas outras, o atual.
//   - a ficha (a bolsa), o Inventário (a bolsa) e o Mercado (Suprimentos), no cenário tutorial com VITRINE=1 (um
//     unguento na bolsa, o broquel vestido);
//   - a tela inteira: a vila com o Guerreiro e o cenário, e o Inventário.
// Em janela normal (1500×950) e baixa (1280×720). Guarda em capturas-unguento/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_unguento.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync, existsSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-unguento");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(cenario, amb = {}) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 150 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
async function pagina(b, url, W, H, versao) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  // os arquivos do protótipo (as propostas) e, nelas, o escudo final no lugar do atual
  await p.route(/\/__prototipo\//, (rota) => rota.fulfill({
    path: path.join(aqui, new URL(rota.request().url()).pathname.replace("/__prototipo/", "")), contentType: "image/png" }));
  if (PROPOSTA[versao]) await p.route(/\/static\/hud\/icones\/escudo-[^/]+\.png/, (rota) => {
    const arq = path.join(aqui, "escudo-pixel", path.basename(new URL(rota.request().url()).pathname));
    return existsSync(arq) ? rota.fulfill({ path: arq, contentType: "image/png" }) : rota.continue();
  });
  if (versao !== "atual") {
    await p.addInitScript((c) => { window.UNGUENTO_TESTE = c; }, { versao, ...(PROPOSTA[versao] || {}) });
    p.on("load", async () => {
      for (const f of ["arte-teste.js", "itens-icones-teste.js", "unguento-no-jogo.js"]) await p.addScriptTag({ path: path.join(aqui, f) }).catch(() => {});
    });
  }
  await p.goto(url);
  return p;
}
async function ate(p, sel) {
  for (let k = 0; k < 60 && !(await p.$(sel)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(900);
}
async function foto(p, sel, nome) {
  await p.mouse.move(2, 2); await espera(250);
  const c = sel && await p.evaluate((s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return { x: Math.floor(r.left), y: Math.floor(r.top), width: Math.ceil(r.width), height: Math.ceil(r.height) }; }, sel);
  await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), ...(c ? { clip: c } : {}) });
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const erros = [], tamanhos = new Set();
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
// as propostas em pixel art: a pasta e os lados de cada uma
const PROPOSTA = { anterior: { pasta: "unguento-pixel-v1", lados: [32, 48, 64] }, conceito: { pasta: "unguento-pixel", lados: [32, 64] } };
const VERSOES = (process.env.VERSOES || "atual,primeiro,anterior,conceito").split(",");
for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) {
  const [W, H] = JANELAS[jan], n = (c) => `${jan}-${versao}-${c}`;
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", VITRINE: "1", VISTAS: "A1,V2,N1,D1,K1,M1", OURO: "200" });
  const p = await pagina(b, url, W, H, versao);
  p.on("pageerror", (e) => erros.push(`${jan} ${versao}: ${e}`));
  await ate(p, "#predios .predio");
  await foto(p, null, n("tela-vila"));
  await foto(p, "#heroi", n("ficha"));
  await (await p.$('#doca .atalho[data-rotulo="Inventário"]')).click(); await espera(1200);
  await foto(p, null, n("tela-inventario"));
  await foto(p, "#cena", n("inventario"));
  await p.keyboard.press("Escape"); await espera(900);
  await ate(p, "#predios .predio");
  await (await p.$('#predios .predio[data-predio="mercado"]')).click(); await espera(1500);
  const sup = await p.$('.tela.loja .aba:has-text("Suprimentos"), .tela.loja button:has-text("Suprimentos")');
  if (sup) { await sup.click(); await espera(700); }
  await foto(p, "#cena", n("mercado"));
  for (const t of await p.evaluate(() => window.__unguentos || [])) tamanhos.add(t);
  await p.close(); proc.kill();
  console.log(jan, versao, "ok");
}
await b.close();
console.log(`tamanhos trocados: ${[...tamanhos].sort().join(", ") || "nenhum"}`);
console.log(erros.length ? erros.join("\n") : "sem erros");
