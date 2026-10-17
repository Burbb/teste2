// O teste do pen.dev (experimento): as peças de acabamento que a importação do pen.dev perde (a faixa de pincel com
// as pontas, o grão e a inclinação; o paralelogramo da tecla), renderizadas pelo CSS do jogo na bancada e gravadas
// como PNG transparente em images/pecas/, para virar preenchimento de imagem no canvas. Uma por janela e estado; cada
// uma com FOLGA px a mais em volta (a faixa inclinada e a sombra passam da caixa do botão). Precisa do servir.py no ar.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/pen-composicao/pecas.mjs
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const SAIDA = path.join(aqui, "images", "pecas");
mkdirSync(SAIDA, { recursive: true });
const FOLGA = 8;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1000, height: 1600 }, deviceScaleFactor: 1 });
await p.goto(`${process.env.BANCADA || "http://localhost:8771/bancada.html"}?versao=${process.env.VERSAO || "atual"}`);
await p.waitForSelector("body[data-pronta]");
// sem fundo nenhum: só a peça
await p.addStyleTag({ content: `html, :root body.bancada, :root body.bancada .roda-janela.seletor { background: transparent !important; }
  :root body.bancada .roda-janela.seletor::after { display: none; }` });
const medidas = {};
for (const q of await p.$$(".bq-quadro")) {
  const jan = await q.getAttribute("data-janela"), estado = await q.getAttribute("data-estado");
  for (const linha of await q.$$(".rj-linha")) {
    const hab = await linha.getAttribute("data-hab");
    const ativo = await linha.evaluate((l) => l.classList.contains("x-destaque"));
    const tipo = (await linha.evaluate((l) => l.classList.contains("bloqueada"))) ? (ativo ? "indisponivel-destaque" : "indisponivel") : ativo ? "destaque" : "normal";
    const nome = `${jan}-${tipo}`;
    if (medidas[nome]) continue;
    const caixa = await linha.boundingBox(), tecla = await (await linha.$(".tecla")).boundingBox();
    // a faixa: o botão sem o conteúdo (o ::before fica)
    await linha.evaluate((l) => l.querySelectorAll(":scope > *").forEach((e) => (e.style.visibility = "hidden")));
    await p.screenshot({ path: path.join(SAIDA, `faixa-${nome}.png`), omitBackground: true,
      clip: { x: caixa.x - FOLGA, y: caixa.y - FOLGA, width: caixa.width + 2 * FOLGA, height: caixa.height + 2 * FOLGA } });
    // a tecla: o paralelogramo sem o número
    await linha.evaluate((l) => { l.querySelectorAll(":scope > *").forEach((e) => (e.style.visibility = "")); l.classList.add("so-tecla"); });
    await p.addStyleTag({ content: `.so-tecla::before { display: none !important; } .so-tecla > :not(.tecla) { visibility: hidden; } .so-tecla .tecla { color: transparent !important; }` });
    await p.screenshot({ path: path.join(SAIDA, `tecla-${nome}.png`), omitBackground: true,
      clip: { x: tecla.x - FOLGA, y: tecla.y - FOLGA, width: tecla.width + 2 * FOLGA, height: tecla.height + 2 * FOLGA } });
    await linha.evaluate((l) => l.classList.remove("so-tecla"));
    medidas[nome] = { faixa: [Math.round(caixa.width + 2 * FOLGA), Math.round(caixa.height + 2 * FOLGA)], tecla: [Math.round(tecla.width + 2 * FOLGA), Math.round(tecla.height + 2 * FOLGA)], folga: FOLGA };
  }
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.json"), JSON.stringify(medidas, null, 1));
console.log(medidas);
