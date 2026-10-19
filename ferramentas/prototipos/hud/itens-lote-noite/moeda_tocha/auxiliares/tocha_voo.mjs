// O recebimento de uma tocha fora da luta (o chip "+1 Tocha" e o ícone voando até as tochas do topo, itemVoa): a
// mensagem do jogo pelo efeito(), na vila do cenário do mercado, em velocidade normal. Registra o arquivo e o tamanho
// do ícone que voa e fotografa o voo e a chegada.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node tocha_voo.mjs <raiz do repositório> <pasta de saída> <rótulo>
import { spawn } from "child_process";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const [raiz, saida, rotulo] = process.argv.slice(2);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn("python", ["-m", "tests.navegador.cenarios", "mercado"], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", CLASSE: "guerreiro" } });
let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
for (let k = 0; k < 300 && !url; k++) await espera(100);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
await p.goto(url); await p.waitForSelector(".tela.loja", { timeout: 20000 }); await espera(1200);
await p.keyboard.press("Escape"); await p.waitForSelector('#predios:not(.focado) .predio[data-predio="mercado"]', { timeout: 8000 }); await espera(800);
await p.evaluate(() => { efeito({ tipo: "item", texto: "+1 Tocha", item: "tocha" }); });
const nome = (f) => path.join(saida, `${rotulo}-1920x945-${f}.png`);
const voando = [];
for (const [ms, f] of [[160, "voo-1"], [260, "voo-2"]]) {
  await espera(ms);
  voando.push(...await p.evaluate(() => [...document.querySelectorAll(".item-voando img")].map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${i.getAttribute("width")}px`)));
  await p.screenshot({ path: nome(f), clip: { x: 560, y: 60, width: 560, height: 520 } });
}
await espera(1500);
await p.screenshot({ path: nome("recebida"), clip: { x: 560, y: 60, width: 560, height: 520 } });
console.log(JSON.stringify({ voando: [...new Set(voando)], tochas: await p.evaluate(() => App.estado.heroi.tochas), erros }));
await b.close(); proc.kill();
