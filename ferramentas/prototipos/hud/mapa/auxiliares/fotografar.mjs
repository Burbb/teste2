// O levantamento e as propostas da 1E.4 (23/10/2026): o mapa e o minimapa da campanha a 1920×945. Cada situação: o
// cenário de tests/navegador/cenarios.py, as variáveis e as fotos (a página, o painel do mundo, o minimapa e o mapa
// grande, aberto com M). O registro mede o canvas (o nativo e o exibido), os botões dos lugares e o console.
// PROTOTIPO=1: o mapa.js da proposta (../prototipo/mapa.js) no lugar do do jogo e as peças de ../proposta/ em
// /proposta-mapa/, só nesta página (o jogo continua intacto); MINI (o lado do símbolo no minimapa, 32 ou 24) e POS
// ("a", a seta; "b", o herói na plaqueta) escolhem a variante.
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos> [<nome>,...]
import { spawn } from "child_process";
import { mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida, so] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const BASE = { TUTORIAL: "0", CLASSE: "guerreiro" };
const SITUACOES = [
  // no Vau, de manhã: o Charco e o Bosque visitados, a Capela e a Estrada de Varn só conhecidas; o contrato no Bosque
  { nome: "vau-manha", cenario: "tutorial", amb: { ...BASE, LUGAR: "vau", PERIODO: "0", CONTRATO: "aceito" } },
  // no Bosque, à noite: a Capela a um trecho, a tinta da noite
  { nome: "bosque-noite", cenario: "tutorial", amb: { ...BASE, LUGAR: "bosque", PERIODO: "3", ETAPA: "capela" } },
  // depois da praça: tudo visitado menos a Estrada de Varn (fechada); as estradas percorridas
  { nome: "praca-tudo", cenario: "praca", amb: {} },
  // o procedural (fora da prioridade): só para ver o que ele compartilha com a campanha (o covil, a cidadela, a legenda)
  { nome: "procedural-covil", cenario: "covil", amb: { CLASSE: "guerreiro", PERIODO: "0" } },
].filter((s) => !so || so.split(",").includes(s.nome));
const prototipo = process.env.PROTOTIPO ? readFileSync(path.join(AQUI, "../prototipo/mapa.js"), "utf8") : null;
const variante = { mini: Number(process.env.MINI || 32), pos: process.env.POS || "a" };
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const registro = {};
for (const sit of SITUACOES) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...sit.amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
    const erros = [], avisos = [];
    p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") avisos.push(m.text()); });
    p.on("requestfailed", (r) => erros.push(`falhou: ${r.url()}`));
    if (prototipo) {
      await p.addInitScript((v) => { window.__MAPA = v; }, variante);
      await p.route("**/static/mapa.js", (rota) => rota.fulfill({ contentType: "application/javascript", body: prototipo }));
      await p.route("**/proposta-mapa/*", (rota) => rota.fulfill({ contentType: "image/png",
        body: readFileSync(path.join(AQUI, "../proposta", path.basename(new URL(rota.request().url()).pathname))) }));
    }
    await p.goto(url);
    await p.waitForSelector("#mapa-mini canvas", { timeout: 30000 }).catch(() => erros.push("não apareceu o minimapa"));
    if (prototipo) await p.evaluate(() => { window.legendaMapa = () => MapaPx.legenda(); });  // a legenda da proposta
    await espera(2000);
    const medir = () => p.evaluate(() => [...document.querySelectorAll(".mapa-px")].map((m) => {
      const c = m.querySelector("canvas"), r = c.getBoundingClientRect();
      return { onde: m.closest("#mapa-mini") ? "minimapa" : m.closest("#mapa-grande") ? "mapa grande" : "página",
        nativo: `${c.width}×${c.height}`, exibido: `${r.width.toFixed(1)}×${r.height.toFixed(1)}`, escala: (r.width / c.width).toFixed(3),
        simbolos: [...m.querySelectorAll("img.simbolo-lugar")].map((i) => `${i.naturalWidth}→${i.getBoundingClientRect().width}`),
        lugares: [...m.querySelectorAll(".no-btn")].map((n) => ({ id: n.dataset.id, classes: n.className,
          centro: [Math.round(n.getBoundingClientRect().x + n.getBoundingClientRect().width / 2 - m.getBoundingClientRect().x),
            Math.round(n.getBoundingClientRect().y + n.getBoundingClientRect().height / 2 - m.getBoundingClientRect().y)],
          botao: `${n.getBoundingClientRect().width}×${n.getBoundingClientRect().height}`, rotulo: n.getAttribute("aria-label") })) };
    }));
    if (!prototipo && !process.env.SEM_SPRITES) {
      // os desenhos de hoje para as folhas: os sprites 16 do mapa e a figura 16 de cada classe (a da direção B)
      const pasta = path.join(saida, "../sprites");
      mkdirSync(pasta, { recursive: true });
      const urls = await p.evaluate(() => Object.fromEntries([
        ...["vila", "pantano", "floresta", "ruinas", "planicie", "montanha", "cidadela", "covil", "vencido"].map((n) => [n, Sprites.canvas(n).toDataURL()]),
        ...["guerreiro", "mago", "arqueiro"].map((c) => [`figura-${c}`, Retratos.canvas(c, "figura", 1).toDataURL()])]));
      for (const [n, u] of Object.entries(urls)) writeFileSync(path.join(pasta, `${n}.png`), Buffer.from(u.split(",")[1], "base64"));
    }
    const fotos = [];
    await p.screenshot({ path: path.join(saida, `${sit.nome}-pagina.png`) }); fotos.push("pagina");
    await p.locator("#mundo").screenshot({ path: path.join(saida, `${sit.nome}-mundo.png`) }); fotos.push("mundo");
    await p.locator("#mapa-mini .mapa-px").screenshot({ path: path.join(saida, `${sit.nome}-mini.png`) }); fotos.push("mini");
    const mini = await medir();
    await p.mouse.move(5, 5);
    await p.keyboard.press("m");
    await p.waitForSelector("#mapa-grande canvas", { timeout: 10000 }).catch(() => erros.push("não abriu o mapa grande"));
    await espera(900);
    await p.screenshot({ path: path.join(saida, `${sit.nome}-mapa.png`) }); fotos.push("mapa");
    await p.locator("#mapa-grande .mapa-px").screenshot({ path: path.join(saida, `${sit.nome}-grande.png`) }); fotos.push("grande");
    await p.locator("#sobre-mapa .sobre-caixa").screenshot({ path: path.join(saida, `${sit.nome}-janela.png`) }); fotos.push("janela");
    registro[sit.nome] = { erros, avisos, fotos, medidas: [...mini, ...(await medir()).filter((m) => m.onde === "mapa grande")] };
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1));
for (const [k, v] of Object.entries(registro)) console.log(k, v.fotos.join(","), v.erros.length ? v.erros : "", v.avisos.length ? v.avisos : "");
