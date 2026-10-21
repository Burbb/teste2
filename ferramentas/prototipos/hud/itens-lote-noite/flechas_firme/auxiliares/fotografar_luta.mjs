// A flecha da carta do Arqueiro (F1) e o Firme (R1) na luta, atual × proposta, com os mesmos dados (20/10/2026).
// O cenário covil (tests/navegador/cenarios.py) põe o Arqueiro numa luta contra dois lobos, com o Firme, o Em guarda e a
// Esquiva no herói e o lobo atordoado (EFEITOS, EFEITOS_INIMIGO), para ver o Firme ao lado dos outros estados.
// Na proposta, só a página troca duas imagens, pelos seletores dos dois papéis: a da quantidade de flechas na carta do
// herói (.carta-flechas img) e a do estado Firme (.ef[data-ef="firme"] img). O jogo fica intacto: os outros usos do
// desenho "flecha" (custo das habilidades, orientação, projéteis) e do "cadeado" (talento, bloqueio de vida, mercado)
// não são tocados. Três modos com os mesmos dados: atual, proposta (a F1 e a R1) e rodada2 (a F2 e a R2).
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node fotografar_luta.mjs <raiz do repositório> <pasta das fotos>
import { spawn } from "child_process";
import { readFileSync, mkdirSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const prop = path.join(raiz, "ferramentas/prototipos/hud/itens-lote-noite/flechas_firme/proposta");
const dados = (n) => "data:image/png;base64," + readFileSync(path.join(prop, n)).toString("base64");
const TROCAS = {
  proposta: { ".carta-flechas img.sprite": dados("flecha_contador-16.png"), '.ef[data-ef="firme"] img.sprite': dados("firme-16.png") },
  rodada2: { ".carta-flechas img.sprite": dados("flecha_contador_f2-16.png"), '.ef[data-ef="firme"] img.sprite': dados("firme_r2-16.png") },
};
const AMB = { CLASSE: "arqueiro", LUTA: "lobo", NIVEL_LUTA: "2", QUANTOS: "2", VIDA: "40", PERIODO: "0",
              EFEITOS: "firme:2,guarda:2:0.3,esquiva:2:0.2", EFEITOS_INIMIGO: "atordoado:2" };
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const registro = {};
// MODOS=atual: só os arquivos do jogo (a conferência da integração, 1.155.0)
for (const modo of (process.env.MODOS || "atual,proposta,rodada2").split(",")) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "covil"], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...AMB } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    await p.goto(url);
    await p.waitForSelector('.carta[data-uid="j"] .carta-flechas:not([hidden]) img', { timeout: 30000 });
    await p.waitForSelector('.carta[data-uid="j"] .ef[data-ef="firme"]', { timeout: 30000 });
    await espera(1500);
    if (TROCAS[modo]) {
      await p.evaluate((troca) => {
        const aplica = () => { for (const [sel, src] of Object.entries(troca)) for (const im of document.querySelectorAll(sel)) if (im.src !== src) im.src = src; };
        aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["src"] });
      }, TROCAS[modo]);
      await espera(500);
    }
    const heroi = p.locator('.carta[data-uid="j"]');
    await heroi.screenshot({ path: path.join(saida, `${modo}-1920x945-carta.png`) });
    const palco = p.locator("#palco");
    await palco.screenshot({ path: path.join(saida, `${modo}-1920x945-luta.png`) });
    registro[modo] = await p.evaluate(() => ({
      flechas: document.querySelector('.carta[data-uid="j"] .carta-flechas').textContent.trim(),
      flecha_img: (() => { const i = document.querySelector('.carta[data-uid="j"] .carta-flechas img'); return [i.naturalWidth, i.getBoundingClientRect().width]; })(),
      estados: [...document.querySelectorAll('.carta .ef')].map((e) => e.dataset.ef + ":" + e.title.split(" ·")[0]),
      firme_img: (() => { const i = document.querySelector('.ef[data-ef="firme"] img'); return [i.naturalWidth, i.getBoundingClientRect().width]; })(),
    }));
    registro[modo].erros = erros;
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
console.log(JSON.stringify(registro, null, 1));
