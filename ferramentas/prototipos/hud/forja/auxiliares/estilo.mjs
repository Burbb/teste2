// As cenas aprovadas do jogo que são a referência de estilo da forja G, fotografadas no jogo de verdade a 1920×945 (a
// arte como aparece, no tamanho real): a cidade (o Vau, cenario_forja.py sem proposta), o mercado (o prédio do mercado
// no Vau: a banca com o mercador), a capela (o ossuário) e a prisão da Ilse (o fundo alagado), pelo cenário `capela` dos
// testes com SALA. Grava ../capturas/estilo-<cena>.png (só a arte) para a folha de comparação.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/forja/auxiliares/estilo.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";

async function subir(args, amb) {
  const proc = spawn(PY, args, { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 400 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
async function parado(p) {
  for (let k = 0; k < 80 && !(await p.$(MENU)); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
  await espera(900);
}
const foto = async (p, sel, nome) => {
  const r = await p.$eval(sel, (e) => { const q = e.getBoundingClientRect(); return { x: q.left, y: q.top, width: q.width, height: q.height }; });
  await p.mouse.move(2, 2); await espera(400);
  await p.screenshot({ path: path.join(SAIDA, `estilo-${nome}.png`), clip: r });
  console.log("  ", nome, Math.round(r.width), "×", Math.round(r.height));
};

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const nova = () => b.newPage({ viewport: { width: 1920, height: 945 } });
// a cidade e o mercado
{
  const { proc, url } = await subir([path.join(aqui, "cenario_forja.py")], { PROPOSTA: "" });
  const p = await nova(); await p.goto(url); await parado(p);
  await foto(p, "#vista", "cidade");
  await p.click('[data-predio="mercado"]');
  await p.waitForSelector(".banca-cena", { timeout: 15000 }); await espera(1500);
  await foto(p, ".banca-cena", "mercado");
  await p.close(); proc.kill();
}
// a capela (o ossuário) e a prisão da Ilse (o fundo)
for (const [sala, nome] of [["ossuario", "capela"], ["fundo", "ilse"]]) {
  const { proc, url } = await subir([path.join(raiz, "tests", "navegador", "cenarios.py"), "capela"], { SALA: sala, ETAPA: sala === "fundo" ? "fundo" : "ossuario" });
  const p = await nova(); await p.goto(url); await parado(p); await espera(1500);
  await foto(p, "#vista", nome);
  await p.close(); proc.kill();
}
await b.close();
console.log("ok");
