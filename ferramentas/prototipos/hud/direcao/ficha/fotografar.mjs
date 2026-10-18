// Prova de fidelidade da coluna da ficha: aplicada ao jogo de produção (só a coluna do herói), na janela de sempre
// (1920×945, a área do jogo no monitor 1920×1080), no mesmo caso da proposta anterior (a Capela Afogada de dia, o
// arqueiro patrulheiro nível 5).
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/direcao/ficha/fotografar.mjs [medir]
// Grava em capturas/: a tela inteira, o recorte da ficha, a dica de um atributo e a dos testes; e mede a coluna e o
// centro (o centro tem de ficar do mesmo tamanho que no jogo). "medir" só mede (para gerar a arte no tamanho certo).
import { spawn } from "child_process";
import { readFileSync, mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "capturas"), ARTE = path.join(aqui, "arte");
mkdirSync(SAIDA, { recursive: true });
const JANELA = { width: 1920, height: 945 };
const so_medir = process.argv[2] === "medir";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

export async function anexarFicha(p) {
  const JS = readFileSync(path.join(aqui, "ficha.js"), "utf8"), CSS = readFileSync(path.join(aqui, "ficha.css"), "utf8");
  await p.route(/\/static\/app\/controles\.js(\?|$)/, async (r) => {
    const res = await r.fetch();
    const corpo = (await res.text()) + `\n;(() => { const s = document.createElement("style"); s.id = "ficha-prova"; s.textContent = ${JSON.stringify(CSS)}; document.head.appendChild(s); })();\n${JS}`;
    r.fulfill({ response: res, body: corpo, headers: { ...res.headers(), "content-type": "application/javascript" } });
  });
  // a arte da prova, servida da pasta arte/
  await p.route(/\/proto-ficha\//, async (r) => {
    const nome = decodeURIComponent(new URL(r.request().url()).pathname.split("/").pop());
    try { r.fulfill({ body: readFileSync(path.join(ARTE, nome)), contentType: "image/png" }); } catch { r.fulfill({ status: 404, body: "" }); }
  });
}

async function subir() {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "capela"], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const medir = (p) => p.evaluate(() => {
  const r = (s) => { const q = document.querySelector(s).getBoundingClientRect(); return [Math.round(q.left), Math.round(q.top), Math.round(q.width), Math.round(q.height)]; };
  const h = document.querySelector("#heroi");
  return { rola_a_ficha: h.scrollHeight - h.clientHeight, heroi: r("#heroi"), palco: r("#palco"), mundo: r("#mundo"), arena_ou_vista: r("#vista") };
});

const b = await chromium.launch();
const rel = {};
for (const modo of so_medir ? ["ficha"] : ["jogo", "ficha"]) {
  const { proc, url } = await subir();
  try {
    const p = await b.newPage({ viewport: JANELA });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo === "ficha") await anexarFicha(p);
    await p.goto(url);
    await p.waitForFunction(() => !processando && pergunta, null, { timeout: 30000 }); await espera(1500);
    rel[modo] = { medidas: await medir(p), erros };
    if (!so_medir) {
      await p.screenshot({ path: path.join(SAIDA, `${modo}-tela.png`) });
      const [x, y, w, h] = rel[modo].medidas.heroi;
      await p.screenshot({ path: path.join(SAIDA, `${modo}-ficha.png`), clip: { x: Math.max(0, x - 40), y: 0, width: w + 80, height: JANELA.height } });
      if (modo === "ficha") {
        // as interações da coluna: a dica de um atributo, a dos testes, um espaço de item e o foco do teclado
        await p.hover('#heroi .atributo[data-atributo="Agilidade"]'); await espera(500);
        await p.screenshot({ path: path.join(SAIDA, "ficha-dica-atributo.png"), clip: { x: 0, y: 0, width: 900, height: JANELA.height } });
        await p.hover("#heroi .testes-ficha"); await espera(500);
        await p.screenshot({ path: path.join(SAIDA, "ficha-dica-testes.png"), clip: { x: 0, y: 0, width: 900, height: JANELA.height } });
        await p.hover("#heroi .equip-mini .slot-px:not(.vazio)"); await espera(500);
        rel[modo].dica_item = await p.evaluate(() => { const d = document.getElementById("dica-item"); return !!(d && !d.hidden && d.offsetParent !== null && d.textContent.trim()); });
        await p.mouse.move(960, 600);
        await p.focus("#heroi .testes-ficha");
        rel[modo].foco = await p.evaluate(() => { const cs = getComputedStyle(document.activeElement); return `${document.activeElement.className}: ${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineColor}`; });
        await p.screenshot({ path: path.join(SAIDA, "ficha-foco.png"), clip: { x: 60, y: 300, width: 400, height: 160 } });
      }
    }
    rel[modo].erros = erros;
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
console.log(JSON.stringify(rel, null, 1));
if (!so_medir) writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(rel, null, 1));
