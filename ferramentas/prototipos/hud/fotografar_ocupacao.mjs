// O estudo da ocupação dos ícones no inventário (experimento): o mesmo inventário, com os mesmos equipamentos (cenário
// tutorial com VITRINE=2: o escudo, o anel e a armadura vestidos, a espada na mão; na mochila, espada, escudo e anel, sem o
// machado),
// na apresentação atual (32 px) e na alternativa (40 px, ocupacao-no-jogo.js). O escudo é o final nas duas (o roteiro
// responde aos pedidos do escudo com escudo-pixel/). Fotografa o Inventário e a tela inteira, em janela normal
// (1500×950) e baixa (1280×720), e recorta em tamanho real o escudo, o anel e a armadura vestidos e a mochila; mede o
// espaço, a imagem exibida e a área ocupada pelos pixels. Guarda em capturas-ocupacao/ (e medidas.json).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_ocupacao.mjs
import { spawn } from "child_process";
import { mkdirSync, existsSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-ocupacao");
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
async function ate(p, sel) {
  for (let k = 0; k < 60 && !(await p.$(sel)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(900);
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const erros = [], medidas = {};
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of Object.keys(JANELAS)) for (const versao of ["atual", "alternativa"]) {
  const [W, H] = JANELAS[jan], n = (c) => path.join(SAIDA, `${jan}-${versao}-${c}.png`);
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", VITRINE: "2", VISTAS: "A1,V2,N1,D1,K1,M1", OURO: "200" });
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(`${jan} ${versao}: ${e}`));
  await p.route(/\/__prototipo\//, (rota) => rota.fulfill({
    path: path.join(aqui, new URL(rota.request().url()).pathname.replace("/__prototipo/", "")), contentType: "image/png" }));
  await p.route(/\/static\/hud\/icones\/escudo-[^/]+\.png/, (rota) => {
    const arq = path.join(aqui, "escudo-pixel", path.basename(new URL(rota.request().url()).pathname));
    return existsSync(arq) ? rota.fulfill({ path: arq, contentType: "image/png" }) : rota.continue();
  });
  if (versao === "alternativa") p.on("load", () => p.addScriptTag({ path: path.join(aqui, "ocupacao-no-jogo.js") }).catch(() => {}));
  await p.goto(url);
  await ate(p, "#predios .predio");
  await (await p.$('#doca .atalho[data-rotulo="Inventário"]')).click(); await espera(1500);
  await p.mouse.move(2, 2); await espera(300);
  await p.screenshot({ path: n("tela") });
  const caixa = async (sel, f = 0) => p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return { x: Math.floor(r.left - f), y: Math.floor(r.top - f), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) }; }, [sel, f]);
  await p.screenshot({ path: n("inventario"), clip: await caixa("#cena") });
  await p.screenshot({ path: n("corpo"), clip: await caixa(".tela.inventario .boneco", 4) });
  await p.screenshot({ path: n("mochila"), clip: await caixa(".tela.inventario .mochila-grade", 2) });
  for (const [esp, nome] of [["secundaria", "escudo"], ["anel1", "anel"], ["armadura", "armadura"]])
    await p.screenshot({ path: n(nome), clip: await caixa(`.tela.inventario [data-espaco="${esp}"]`, 2) });
  // as medidas: o espaço, a imagem exibida (o retângulo da <img>) e o arquivo (o que o navegador baixou)
  medidas[`${jan}-${versao}`] = await p.evaluate(() => [...document.querySelectorAll(".tela.inventario .espaco:not(.vazio), .tela.inventario .celula:not(.vazia)")].map((s) => {
    const i = s.querySelector("img"), a = s.getBoundingClientRect(), c = i.getBoundingClientRect();
    return { onde: s.dataset.espaco || `mochila ${s.dataset.mochila}`, espaco: Math.round(a.width), imagem: Math.round(c.width),
      arquivo: i.currentSrc.replace(/.*\//, ""), natural: i.naturalWidth };
  }));
  await p.close(); proc.kill();
  console.log(jan, versao, "ok");
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.json"), JSON.stringify(medidas, null, 1));
console.log(erros.length ? erros.join("\n") : "sem erros");
