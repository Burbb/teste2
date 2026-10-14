// Refaz composicao4c.js, os dois entornos novos da HUD 4 completa: uma luta do Guerreiro (o cenário "muralha": nível 6,
// Paladino, no Bosque do Moinho, contra dois bandidos e um cultista) e a capela (o cenário "capela" com o mesmo
// Guerreiro de nível 6, de manhã, com a nave vencida). Só fotografia: o protótipo não fala com o motor.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_composicao4c.mjs
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
// As telas desenhadas em canvas (o mapa miúdo, a sala da capela, a arena) viram imagem: a fotografia não tem o código
// que as desenha.
const imagens = () => document.querySelectorAll("#mundo canvas, #palco canvas:not(#vista)").forEach((c) => {
  const img = document.createElement("img");
  img.src = c.toDataURL(); img.className = c.className; img.id = c.id;
  img.setAttribute("style", (c.getAttribute("style") || "") + `;width:${c.clientWidth}px;height:${c.clientHeight}px;image-rendering:pixelated`);
  c.replaceWith(img);
});
// `sala`: a capela pinta a sala no mesmo canvas da paisagem (cenas.js); a fotografia guarda a imagem dele.
const fotografar = (page, sala = false) => page.evaluate(([imagensSrc, sala]) => {
  const v = document.querySelector("#vista");
  const vistaImagem = sala ? { src: v.toDataURL(), largura: v.width, altura: v.height } : null;
  new Function(`(${imagensSrc})()`)();
  return { vistaImagem, corpo: { classe: document.body.className, bioma: document.body.dataset.bioma, periodo: document.body.dataset.periodo },
    topo: document.querySelector("#topo").innerHTML, palco: document.querySelector("#palco").innerHTML,
    mundo: document.querySelector("#mundo").innerHTML, vista: { local: App.estado.local, mundo: App.estado.mundo } };
}, [imagens.toString(), sala]);
const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const foto = {};
{
  const { proc, url } = await subir(["-m", "tests.navegador.cenarios", "muralha"], { NIVEL: "6" });
  const page = await browser.newPage({ viewport: { width: 1500, height: 950 } });
  await page.goto(url);
  // a vez do herói, com os quadros de orientação do começo já fechados
  for (let k = 0; k < 60; k++) {
    const ok = await page.evaluate(() => document.body.classList.contains("em-combate") && !!pergunta && !processando
      && !!document.querySelector("#roda .roda-botao") && !document.querySelector(".orientacao:not([hidden])"));
    if (ok) break;
    const entendi = await page.$(".orientacao:not([hidden]) .orientacao-entendi");
    if (entendi) await entendi.click().catch(() => {});
    await espera(300);
  }
  // uma troca de golpes (atacar o primeiro bandido), para o registro e as vidas não ficarem no turno zero
  await page.keyboard.press("1");
  await espera(400);
  await (await page.$("#arena .carta.alvejavel"))?.click();
  for (let k = 0; k < 80; k++) {
    const ok = await page.evaluate(() => !!pergunta && !processando && estado.combate && estado.combate.turno >= 2 && !!document.querySelector("#roda .roda-botao"));
    if (ok) break;
    const entendi = await page.$(".orientacao:not([hidden]) .orientacao-entendi");
    if (entendi) await entendi.click().catch(() => {});
    await espera(300);
  }
  await espera(2000);
  foto.combate = await fotografar(page);
  await page.close(); proc.kill();
}
{
  const { proc, url } = await subir(["-m", "tests.navegador.cenarios", "capela"], { NIVEL: "6", CLASSE: "guerreiro", ESPEC: "paladino" });
  const page = await browser.newPage({ viewport: { width: 1500, height: 950 } });
  await page.goto(url);
  await page.waitForSelector('#prompt .escolhas:not(.escolhido) .escolha:has-text("Atravessar o salão alagado")', { timeout: 30000 });
  await espera(2500);
  foto.capela = await fotografar(page, true);
  await page.close(); proc.kill();
}
writeFileSync(path.join(aqui, "composicao4c.js"), "// Os entornos novos da HUD 4 completa, fotografados do jogo por fotografar_composicao4c.mjs (a luta do Guerreiro\n// no Bosque do Moinho e a capela). Não é jogo: só o entorno para avaliar a linguagem visual.\nwindow.COMPOSICAO4C = " + JSON.stringify(foto) + ";\n");
console.log("composicao4c.js refeito", Object.keys(foto));
await browser.close();
