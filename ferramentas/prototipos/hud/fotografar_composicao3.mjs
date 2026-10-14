// Refaz composicao3.js, o entorno da HUD 3: o DOM do jogo na campanha (o Bosque do Moinho, com a missão da febre e
// dois contratos no painel do mundo), a página da cena de missão logo depois (texto longo) e a janela do anel achado
// (a comparação de equipamento do cenário "aneis"). Só fotografia: o protótipo não fala com o motor.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_composicao3.mjs
import { spawn } from "child_process";
import { writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(args, amb = {}) {
  const proc = spawn("python3", args, { cwd: raiz, env: { ...process.env, VELOCIDADE: "normal", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 100 && !url; k++) await espera(100);
  return { proc, url };
}
const parado = (page, f) => page.waitForFunction(f || (() => !processando && pergunta), null, { timeout: 30000 });
const imagens = () => document.querySelectorAll("#mundo canvas, #palco canvas:not(#vista)").forEach((c) => {
  const img = document.createElement("img");
  img.src = c.toDataURL(); img.className = c.className; img.id = c.id;
  img.setAttribute("style", (c.getAttribute("style") || "") + `;width:${c.clientWidth}px;height:${c.clientHeight}px;image-rendering:pixelated`);
  c.replaceWith(img);
});
const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const foto = {};
{
  const { proc, url } = await subir([path.join(aqui, "cenario_hud3.py"), "hud3"]);
  const page = await browser.newPage({ viewport: { width: 1500, height: 950 } });
  await page.goto(url);
  await parado(page, () => !processando && pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => /^Explorar/.test(o.texto)));
  await espera(2500);
  foto.local = await page.evaluate((imagensSrc) => {
    new Function(`(${imagensSrc})()`)();
    return { corpo: { classe: document.body.className, bioma: document.body.dataset.bioma, periodo: document.body.dataset.periodo },
      topo: document.querySelector("#topo").innerHTML, palco: document.querySelector("#palco").innerHTML,
      mundo: document.querySelector("#mundo").innerHTML, vista: { local: App.estado.local, mundo: App.estado.mundo } };
  }, imagens.toString());
  // A cena de missão: seguir a água até o canal (o texto longo da página, com o Continuar dela).
  await page.evaluate(() => { const i = pergunta.opcoes.findIndex((o) => /^Seguir a água/.test(o.texto)); responder(pergunta.id, i); });
  await parado(page, () => !processando && pergunta && pergunta.tipo === "continuar");
  await espera(1500);
  foto.evento = await page.evaluate(() => ({ folha: document.querySelector("#folha").innerHTML }));
  await page.close(); proc.kill();
}
{
  const { proc, url } = await subir(["-m", "tests.navegador.cenarios", "aneis"], { ANEIS: "2" });
  const page = await browser.newPage({ viewport: { width: 1500, height: 950 } });
  await page.goto(url);
  await page.waitForSelector("#sobre-achado .achado-acoes button:not(.reserva)", { timeout: 30000 });
  await espera(1200);
  foto.modal = await page.evaluate(() => document.querySelector("#sobre-achado").outerHTML);
  await page.close(); proc.kill();
}
writeFileSync(path.join(aqui, "composicao3.js"), "// O entorno da HUD 3, fotografado do jogo por fotografar_composicao3.mjs (campanha com missão e contratos, a cena\n// de missão seguinte e a janela do anel achado). Não é jogo: só o entorno para avaliar a linguagem visual.\nwindow.COMPOSICAO3 = " + JSON.stringify(foto) + ";\n");
console.log("composicao3.js refeito", Object.keys(foto));
await browser.close();
