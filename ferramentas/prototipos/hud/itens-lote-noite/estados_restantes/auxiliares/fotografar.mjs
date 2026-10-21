// Os estados do lote da madrugada na luta, atual × proposta, com os mesmos dados (21/10/2026). Derivado de
// flechas_firme/auxiliares/fotografar_luta.mjs: os cenários de tests/navegador/cenarios.py (o covil, com EFEITOS e
// EFEITOS_INIMIGO; o tutorial, para o servo do Necromante) e a troca só na página, pelo seletor do chip de cada estado
// (.ef[data-ef="<id>"] img.sprite). O jogo fica intacto: os sprites e os outros papéis deles não são tocados.
// A situação vem de situacoes.json (por lote): o cenário, as variáveis, a habilidade usada antes da foto (opcional) e
// os estados que a foto procura; cada carta que tem um deles é fotografada, e o palco inteiro também.
// Uma situação com "gira": true é o teste da rotação do selo do Atordoado (só nesta página): os modos proposta-gira e
// proposta-gira-reduzido (o mesmo com prefers-reduced-motion: reduce); o selo do Atordoado ganha a espiral proposta e uma
// volta em 4 passos de 90° (sem borrar o pixel), só sem movimento reduzido; o chip fica parado.
// MODOS=atual: só os arquivos do jogo (a conferência de uma integração). Uma situação com "selo": true usa a habilidade e
// fotografa o selo do estado que chega (.faixa-acao.selos) sobre a carta; nas de alvo único, clica no primeiro inimigo
// se o jogo pedir o alvo.
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <lote> <pasta das fotos>
import { spawn } from "child_process";
import { readFileSync, mkdirSync, existsSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, lote, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.join(raiz, "ferramentas/prototipos/hud/itens-lote-noite/estados_restantes");
// SO=<nome>,...: só essas situações do lote
const SITUACOES = JSON.parse(readFileSync(path.join(aqui, "auxiliares/situacoes.json"), "utf8"))[lote]
  .filter((s) => !process.env.SO || process.env.SO.split(",").includes(s.nome));
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
  const modos = sit.gira ? ["proposta-gira", "proposta-gira-reduzido"]
    : process.env.MODOS ? process.env.MODOS.split(",") : ["atual", ...Object.keys(TROCAS)];
  for (const modo of modos) {
    const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
      env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...sit.amb } });
    let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
    for (let k = 0; k < 300 && !url; k++) await espera(100);
    try {
      const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
      const erros = [], avisos = [];
      p.on("pageerror", (e) => erros.push(String(e)));
      p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") avisos.push(m.text()); });
      if (modo === "proposta-gira-reduzido") await p.emulateMedia({ reducedMotion: "reduce" });
      await p.goto(url);
      // "clicar": o botão que começa a luta com a página aberta (LUTA_APOS_ESCOLHA do cenário tutorial), para ver ao vivo
      // o que acontece no começo dela (a surpresa da emboscada); o selo é esperado desde antes do clique
      let seloCedo = null;
      if (sit.clicar) {
        await p.waitForSelector(`text=${sit.clicar}`, { timeout: 30000 });
        if (sit.selo) seloCedo = p.waitForSelector(".faixa-acao.selos", { timeout: 20000 });
        await p.click(`text=${sit.clicar}`);
      }
      await p.waitForSelector('.carta[data-uid="j"]', { timeout: 30000 });
      if (sit.gira) await p.evaluate((espiral) => {
        const css = document.createElement("style");
        css.textContent = "@keyframes gira-estado { to { transform: rotate(360deg); } }"
          + "@media (prefers-reduced-motion: no-preference) { .faixa-acao.selos img.gira { animation: gira-estado .6s steps(4, end) 1; } }";
        document.head.append(css);
        const estrela = new DOMParser().parseFromString(Sprites.img("estrela", 1), "text/html").querySelector("img").getAttribute("src");
        new MutationObserver(() => {
          for (const im of document.querySelectorAll(".faixa-acao.selos img")) if (im.getAttribute("src") === estrela) { im.src = espiral; im.classList.add("gira"); }
          for (const im of document.querySelectorAll('.ef[data-ef="atordoado"] img.sprite')) if (im.src !== espiral) im.src = espiral;
        }).observe(document.body, { subtree: true, childList: true });
      }, "data:image/png;base64," + readFileSync(png("atordoado")).toString("base64"));
      if (sit.habilidade || seloCedo) {   // usa a habilidade pela roda e pelo seletor, como o jogador
        if (sit.habilidade) {
          await espera(1500);
          await p.click('.roda-botao[data-slot="habilidades"]', { timeout: 30000 });
          await p.click(sit.habilidade.split("|").map((h) => `.rj-linha[data-hab="${h}"]`).join(","), { timeout: 10000 });
        }
        if (sit.selo) {
          // o alvo, quando o jogo pede (clique num inimigo); o selo dura 1,5 s: a foto sai assim que ele aparece
          const alvo = p.locator('.carta[data-uid^="c"]').first();
          const selo = seloCedo || p.waitForSelector(".faixa-acao.selos", { timeout: 20000 });
          await espera(seloCedo ? 0 : 700);
          if (!seloCedo && !(await p.$(".faixa-acao.selos"))) await alvo.click({ timeout: 5000 }).catch(() => {});
          const s = await selo;
          // a rotação: o ângulo da imagem do selo em quatro instantes (a matriz do transform), e quatro fotos seguidas
          const giro = [];
          if (sit.gira) for (let k = 0; k < 4; k++) {
            giro.push(await p.evaluate(() => { const i = document.querySelector(".faixa-acao.selos img.gira");
              return i ? `${getComputedStyle(i).animationName} ${getComputedStyle(i).transform}` : "sem a espiral"; }));
            await s.screenshot({ path: path.join(saida, `${sit.nome}-${modo}-quadro${k}.png`) }).catch(() => {});
            await espera(120);
          }
          await espera(200);
          const dono = sit.carta === "inimigo" ? await p.evaluate(() => document.querySelector('.carta:not([data-uid="j"])').dataset.uid)
            : sit.carta || await s.evaluate((el) => el.closest(".carta") ? el.closest(".carta").dataset.uid : null);
          const c = dono ? await p.locator(`.carta[data-uid="${dono}"]`).boundingBox() : await s.boundingBox(), b = await s.boundingBox();
          const x = Math.min(c.x, b.x) - 8, y = Math.min(c.y, b.y) - 8;
          await p.screenshot({ path: path.join(saida, `${sit.nome}-${modo}-selo.png`),
            clip: { x, y, width: Math.max(c.x + c.width, b.x + b.width) - x + 8, height: Math.max(c.y + c.height, b.y + b.height) - y + 8 } });
          registro[`${sit.nome}/${modo}`] = { selo: await s.evaluate((el) => [...el.querySelectorAll("img")].map((i) => i.getAttribute("src").slice(0, 60))),
                                              dono, giro, erros, avisos };
          await p.close();
          continue;
        }
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
          return i ? `${id} ${i.naturalWidth}px → ${i.getBoundingClientRect().width.toFixed(1)}px ${i.src.startsWith("data:") ? "(sprite ou troca da página)" : i.getAttribute("src")}` : `${id} ausente`; }),
      }), sit.estados);
      Object.assign(registro[`${sit.nome}/${modo}`], { cartas: uids, erros, avisos });
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
console.log(JSON.stringify(registro, null, 1));
