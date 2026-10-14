// Refaz composicao.js: sobe o jogo no cenário "relatorio" (um lugar selvagem com paisagem), espera o menu do lugar e
// guarda o DOM do topo, da cena e do painel do mundo (o mapa vira imagem). Só o entorno da ficha no protótipo.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_composicao.mjs
import { spawn } from "child_process";
import { writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const proc = spawn("python3", ["-m", "tests.navegador.cenarios", "relatorio"], { cwd: raiz,
  env: { ...process.env, PERIODO: process.env.PERIODO || "2", SEMENTE: process.env.SEMENTE || "4", VELOCIDADE: "normal", PYTHONPATH: raiz } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 100 && !url; k++) await new Promise((r) => setTimeout(r, 100));
const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const page = await browser.newPage({ viewport: { width: 1500, height: 950 } });
await page.goto(url);
await page.waitForFunction(() => !processando && pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => /^Explorar/.test(o.texto)), null, { timeout: 30000 });
await new Promise((r) => setTimeout(r, 2500));
const foto = await page.evaluate(() => {
  document.querySelectorAll("#mundo canvas, #palco canvas:not(#vista)").forEach((c) => {
    const img = document.createElement("img");
    img.src = c.toDataURL(); img.className = c.className; img.id = c.id;
    img.setAttribute("style", (c.getAttribute("style") || "") + `;width:${c.clientWidth}px;height:${c.clientHeight}px;image-rendering:pixelated`);
    c.replaceWith(img);
  });
  return { corpo: { classe: document.body.className, bioma: document.body.dataset.bioma, periodo: document.body.dataset.periodo },
    topo: document.querySelector("#topo").innerHTML, palco: document.querySelector("#palco").innerHTML,
    mundo: document.querySelector("#mundo").innerHTML, vista: { local: App.estado.local, mundo: App.estado.mundo } };
});
writeFileSync(path.join(aqui, "composicao.js"), "// Fotografia do centro e da direita da HUD atual (o DOM do jogo num lugar de verdade), feita por\n// fotografar_composicao.mjs. Não é jogo: só o entorno para avaliar a ficha na composição.\nwindow.COMPOSICAO = " + JSON.stringify(foto) + ";\n");
console.log("composicao.js refeito");
proc.kill(); await browser.close();
