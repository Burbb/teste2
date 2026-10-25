// Confere os gestos dos quadros de orientação no jogo de verdade (cenarios_orientacao.py), nos de hoje e nas propostas
// A e B, a 1920×945 (as propostas só mudam o acabamento: os gestos têm de sair iguais aos de hoje):
// - o Tab chega ao "Entendi" e ao "Encerrar tutorial", e o foco se vê (um contorno);
// - Enter no "Entendi" fecha só o quadro: a pergunta do menu continua a mesma (nada escolhido);
// - um clique no texto do quadro não escolhe nada no jogo;
// - "Encerrar tutorial" desliga as orientações (o quadro some e não volta na mesma tela).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/orientacao/auxiliares/gestos.mjs
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

async function abrir(b, caso, proposta) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_orientacao.py"), caso],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: proposta } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url);
  await p.waitForSelector(".orientacao:not([hidden])", { timeout: 30000 });
  await espera(600);
  return { p, proc, erros };
}
const estadoMenu = (p) => p.evaluate(() => ({ id: (typeof pergunta !== "undefined" && pergunta) ? pergunta.id : null,
  quadro: !!document.querySelector(".orientacao:not([hidden])") }));

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const v of (process.env.VERSOES || "atual,a,b").split(",")) {
  console.log(`== ${v}`);
  // A1: um quadro com "Entendi" (informativo)
  let { p, proc, erros } = await abrir(b, "a1", v === "atual" ? "" : v);
  const antes = await estadoMenu(p);
  await p.mouse.click(...(await p.evaluate(() => { const r = document.querySelector(".orientacao-texto").getBoundingClientRect(); return [r.left + 10, r.top + 8]; })));
  await espera(300);
  const depoisClique = await estadoMenu(p);
  conferir(depoisClique.quadro && depoisClique.id === antes.id, "um clique no texto do quadro não escolhe nada");
  const focados = [];
  for (let k = 0; k < 40 && focados.length < 2; k++) {
    await p.keyboard.press("Tab");
    const f = await p.evaluate(() => { const e = document.activeElement; if (!e?.closest(".orientacao")) return null;
      const cs = getComputedStyle(e); return { classe: e.className, contorno: cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0 }; });
    if (f && !focados.some((x) => x.classe === f.classe)) focados.push(f);
  }
  conferir(focados.some((f) => /entendi/.test(f.classe)) && focados.some((f) => /encerrar/.test(f.classe)),
    `o Tab chega aos dois botões (${focados.map((f) => f.classe).join(", ")})`);
  conferir(focados.length > 0 && focados.every((f) => f.contorno), "o foco se vê nos dois (um contorno)");
  await p.focus(".orientacao-entendi");
  await p.keyboard.press("Enter");
  await espera(400);
  const depoisEnter = await estadoMenu(p);
  conferir(!depoisEnter.quadro && depoisEnter.id === antes.id, "Enter no Entendi fecha só o quadro (o menu continua o mesmo)");
  conferir(erros.length === 0, "sem erros na página");
  await p.close(); proc.kill();
  // B1: um quadro sem "Entendi" (cumpre-se pela ação): "Encerrar tutorial"
  ({ p, proc, erros } = await abrir(b, "b1", v === "atual" ? "" : v));
  const antesB = await estadoMenu(p);
  await p.click(".orientacao-encerrar");
  await espera(800);
  const depoisB = await estadoMenu(p);
  conferir(!depoisB.quadro && depoisB.id === antesB.id, "Encerrar tutorial: o quadro some e nada é escolhido");
  await p.close(); proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
