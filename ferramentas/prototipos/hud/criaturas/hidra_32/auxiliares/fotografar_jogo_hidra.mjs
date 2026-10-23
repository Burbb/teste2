// A conferência da integração da Hidra do Brejo (1.197.0), com os arquivos de produção e nada trocado na página, a
// 1920×945: a guardiã na luta (CHEFE=hidra_do_brejo, com o nome e a chave dela) com o sapo e a sanguessuga (os outros do
// pântano, que continuam com os deles). Registra o arquivo de cada retrato, a caixa das cartas e qualquer pedido à pasta
// ferramentas/ (não pode haver).
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar_jogo_hidra.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.dirname(fileURLToPath(import.meta.url));
mkdirSync(saida, { recursive: true });
const ler = () => [...document.querySelectorAll(".inimigos .carta")].map((c) => `${c.querySelector(".carta-nome span").textContent.trim()}: ${(c.querySelector(".icone img") || {}).src || "(sprite)"}`);
const LUTA = { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "5" };
const SITUACOES = [
  { nome: "luta-hidra", cenario: "tutorial", amb: { ...LUTA, GRUPO: "sapo:1,sanguessuga:1", CHEFE: "hidra_do_brejo" },
    espera: '.carta[data-uid="j"]', ler },
];
const b = await chromium.launch();
const arqReg = path.join(saida, "registro.json");
const registro = process.env.SO && existsSync(arqReg) ? JSON.parse(readFileSync(arqReg, "utf-8")) : {};
for (const sit of SITUACOES.filter((s) => !process.env.SO || process.env.SO.split(",").includes(s.nome))) {
  const proc = spawn(PY, sit.script ? [path.join(aqui, sit.script), sit.cenario] : ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...sit.amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
    const erros = [], ferramentas = [];
    p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
    p.on("request", (r) => { if (/ferramentas|prototipos/.test(r.url())) ferramentas.push(r.url()); });
    await p.goto(url);
    await espera(2500);
    for (const tecla of sit.passos || []) { await p.keyboard.press(tecla); await espera(1500); }
    if (sit.evento) {  // o Explorar (que cai no EVENTO) e a primeira escolha do evento, até a luta abrir
      for (let k = 0; k < 80 && !(await p.$(".inimigos .carta")); k++) {
        await p.evaluate(() => {
          if (processando || !pergunta || pergunta.tipo !== "opcoes") return;
          const i = pergunta.opcoes.findIndex((o) => !(o.meta && o.meta.indisponivel));
          if (i >= 0) responder(pergunta.id, i);
        });
        await espera(400);
      }
    }
    await p.waitForSelector(sit.espera, { timeout: 30000 }).catch(() => erros.push(`não apareceu: ${sit.espera}`));
    if (sit.mural) {
      await espera(800);
      await p.screenshot({ path: path.join(saida, `${sit.nome}-rastreador.png`), clip: { x: 1490, y: 330, width: 330, height: 200 } });
      await p.click('#predios .predio[data-predio="mural"]').catch((e) => erros.push(String(e)));
      await p.waitForSelector(".contrato.ativo", { timeout: 10000 }).catch(() => erros.push("sem o cartaz ativo"));
    }
    await espera(2600);
    await p.screenshot({ path: path.join(saida, `${sit.nome}.png`) });
    const caixas = await p.evaluate(() => [...document.querySelectorAll(".inimigos .carta")].map((c) => {
      const r = c.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map(Math.round); }));
    registro[sit.nome] = { arquivos: await p.evaluate(sit.ler), caixas, erros, ferramentas };
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1) + "\n");
console.log(JSON.stringify(registro, null, 1));
