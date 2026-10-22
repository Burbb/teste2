// A conferência da integração (1.179.0), com os arquivos de produção e nada trocado na página, a 1920×945: a luta com
// o Mercenário e o Lobo Gélido (a carta, 32), o Bestiário (48), os contratos de caça dos dois (o rastreador, 32, e o
// cartaz do mural, 48) e o mercado com suprimentos esgotados (o caixote no motivo "Esgotado", o cadeado nos outros).
// Registra o arquivo de cada retrato e de cada motivo e qualquer pedido à pasta ferramentas/ (não pode haver).
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar_jogo.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
mkdirSync(saida, { recursive: true });
const GRUPO = "mercenario:1,lobo_gelido:1,lobo:1,bandido:1,cultista:1,esqueleto:1";
const SITUACOES = [
  { nome: "luta", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "4", GRUPO }, espera: '.carta[data-uid="j"]',
    ler: () => [...document.querySelectorAll(".inimigos .carta")].map((c) => `${c.querySelector(".carta-nome span").textContent.trim()}: ${(c.querySelector(".icone img") || {}).src || "(sprite)"}`) },
  { nome: "bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila", BESTIARIO: "mercenario:2,lobo_gelido:2,lobo:3,bandido:3" },
    passos: ["b"], espera: ".cartao .cab",
    ler: () => [...document.querySelectorAll(".cartao")].map((c) => `${c.querySelector("b").textContent.trim()}: ${(c.querySelector(".cab img") || {}).src}`) },
  { nome: "contratos", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila", CONTRATOS: "mercenario,lobo_gelido" },
    espera: "#predios .predio", mural: true,
    ler: () => [...document.querySelectorAll("img")].filter((i) => /retrato-/.test(i.src)).map((i) => `${i.closest(".contrato, .rastro, #rastreador, aside, section")?.className || i.parentElement.className}: ${i.src} ${i.width}`) },
  { nome: "mercado", cenario: "mercado", amb: { OURO: "20" }, espera: ".tela.loja .mercadoria.suprimento", comprar: true,
    ler: () => [...document.querySelectorAll(".tela.loja .merc-motivo")].map((m) => `${m.textContent.trim()}: ${m.querySelector("img").src.slice(0, 60)}`) },
];
const b = await chromium.launch();
const arqReg = path.join(saida, "registro.json");
const registro = process.env.SO && existsSync(arqReg) ? JSON.parse(readFileSync(arqReg, "utf-8")) : {};
for (const sit of SITUACOES.filter((s) => !process.env.SO || process.env.SO.split(",").includes(s.nome))) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
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
    await p.waitForSelector(sit.espera, { timeout: 30000 }).catch(() => erros.push(`não apareceu: ${sit.espera}`));
    if (sit.mural) {
      await espera(800);
      await p.screenshot({ path: path.join(saida, `${sit.nome}-rastreador.png`), clip: { x: 1490, y: 330, width: 330, height: 200 } });
      await p.click('#predios .predio[data-predio="mural"]').catch((e) => erros.push(String(e)));
      await p.waitForSelector(".contrato.ativo", { timeout: 10000 }).catch(() => erros.push("sem o cartaz ativo"));
    }
    if (sit.comprar) {  // o suprimento mais barato com estoque, comprado até acabar
      const alvo = await p.evaluate(() => [...document.querySelectorAll(".tela.loja .mercadoria.suprimento:not(.caro)")]
        .map((e) => ({ id: e.dataset.comprar, preco: +e.dataset.preco, estoque: +e.querySelector(".merc-estoque b").textContent }))
        .filter((x) => x.estoque > 0).sort((a, z) => a.preco * a.estoque - z.preco * z.estoque)[0]);
      for (let k = 0; k < alvo.estoque; k++) {
        await p.waitForFunction(() => pergunta && pergunta.tipo === "opcoes" && !processando, null, { timeout: 10000 });
        await p.click(`.tela.loja .mercadoria.suprimento[data-comprar="${alvo.id}"] .merc-nome`);
        await espera(450);
      }
      await p.mouse.move(5, 500);
    }
    await espera(2600);
    await p.screenshot({ path: path.join(saida, `${sit.nome}.png`) });
    registro[sit.nome] = { arquivos: await p.evaluate(sit.ler), erros, ferramentas };
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1) + "\n");
console.log(JSON.stringify(registro, null, 1));
