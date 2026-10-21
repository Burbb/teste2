// Os estados do lote da madrugada na luta, atual × proposta, com os mesmos dados (21/10/2026). Derivado de
// flechas_firme/auxiliares/fotografar_luta.mjs: os cenários de tests/navegador/cenarios.py (o covil, com EFEITOS e
// EFEITOS_INIMIGO; o tutorial, para o servo do Necromante) e a troca só na página, pelo seletor do chip de cada estado
// (.ef[data-ef="<id>"] img.sprite). O jogo fica intacto: os sprites e os outros papéis deles não são tocados.
// A situação vem de situacoes.json (por lote): o cenário, as variáveis, a habilidade usada antes da foto (opcional) e
// os estados que a foto procura; cada carta que tem um deles é fotografada, e o palco inteiro também.
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <lote> <pasta das fotos>
import { spawn } from "child_process";
import { readFileSync, mkdirSync, existsSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, lote, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.join(raiz, "ferramentas/prototipos/hud/itens-lote-noite/estados_restantes");
const SITUACOES = JSON.parse(readFileSync(path.join(aqui, "auxiliares/situacoes.json"), "utf8"))[lote];
const png = (id) => path.join(aqui, `proposta/estado-${id}-16.png`);
// a proposta troca todo estado do lote que já tem desenho; VARIANTES=orbita,... acrescenta um modo por variante
// (proposta-<variante>), com estado-<id>-<variante>-16.png onde ela existe e a proposta principal nos outros
const troca = (v) => Object.fromEntries(SITUACOES.flatMap((s) => s.estados).map((id) => [id, v && existsSync(png(`${id}-${v}`)) ? png(`${id}-${v}`) : png(id)])
  .filter(([, arq]) => existsSync(arq))
  .map(([id, arq]) => [`.ef[data-ef="${id}"] img.sprite`, "data:image/png;base64," + readFileSync(arq).toString("base64")]));
const VARIANTES = (process.env.VARIANTES || "").split(",").filter(Boolean);
const TROCAS = { proposta: troca(null), ...Object.fromEntries(VARIANTES.map((v) => [`proposta-${v}`, troca(v)])) };
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const registro = {};
for (const sit of SITUACOES) {
  for (const modo of ["atual", ...Object.keys(TROCAS)]) {
    const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
      env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...sit.amb } });
    let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
    for (let k = 0; k < 300 && !url; k++) await espera(100);
    try {
      const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
      const erros = [], avisos = [];
      p.on("pageerror", (e) => erros.push(String(e)));
      p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") avisos.push(m.text()); });
      await p.goto(url);
      await p.waitForSelector('.carta[data-uid="j"]', { timeout: 30000 });
      if (sit.habilidade) {   // usa a habilidade pela roda e pelo seletor, como o jogador
        await espera(1500);
        await p.click('.roda-botao[data-slot="habilidades"]', { timeout: 30000 });
        await p.click(`.rj-linha[data-hab="${sit.habilidade}"]`, { timeout: 10000 });
      }
      await p.waitForSelector(`.carta .ef[data-ef="${sit.estados[0]}"]`, { timeout: 30000 });
      await espera(sit.habilidade ? 2500 : 1500);
      if (TROCAS[modo]) {
        await p.evaluate((troca) => {
          const aplica = () => { for (const [sel, src] of Object.entries(troca)) for (const im of document.querySelectorAll(sel)) if (im.src !== src) im.src = src; };
          aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["src"] });
        }, TROCAS[modo]);
        await espera(500);
      }
      // cada carta com um dos estados procurados, uma vez
      const uids = await p.evaluate((ids) => [...new Set([...document.querySelectorAll(".carta")]
        .filter((c) => ids.some((id) => c.querySelector(`.ef[data-ef="${id}"]`))).map((c) => c.dataset.uid))], sit.estados);
      for (const [k, uid] of uids.slice(0, sit.cartas || 1).entries())
        await p.locator(`.carta[data-uid="${uid}"]`).screenshot({ path: path.join(saida, `${sit.nome}-${modo}-carta${k}.png`) });
      await p.locator("#palco").screenshot({ path: path.join(saida, `${sit.nome}-${modo}-luta.png`) });
      registro[`${sit.nome}/${modo}`] = await p.evaluate((ids) => ({
        estados: [...document.querySelectorAll(".carta .ef")].map((e) => `${e.closest(".carta").dataset.uid}:${e.dataset.ef}`),
        imagens: ids.map((id) => { const i = document.querySelector(`.ef[data-ef="${id}"] img`);
          return i ? `${id} ${i.naturalWidth}px → ${i.getBoundingClientRect().width.toFixed(1)}px ${i.src.startsWith("data:image/png;base64,iVBOR") && i.naturalWidth === 16 ? "(png 16)" : ""}` : `${id} ausente`; }),
      }), sit.estados);
      Object.assign(registro[`${sit.nome}/${modo}`], { cartas: uids, erros, avisos });
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
console.log(JSON.stringify(registro, null, 1));
