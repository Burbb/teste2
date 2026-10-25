// Fotografa os quadros de orientação no jogo de verdade (cenarios_orientacao.py): os de hoje, A e B, com o mesmo
// estado, a 1920×945 e a 1280×720. Mede em cada um: o texto do quadro, de que lado está a seta, se o quadro cabe na
// janela, se cobre o controle explicado (o contorno), o tamanho da letra e o foco no "Entendi" pelo Tab. Guarda
// ../capturas/<janela>-<versão>-<caso>.png e ../capturas/medidas.json.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/orientacao/auxiliares/fotografar.mjs
// (VERSOES=atual,a,b; CASOS=a1,v1,...; JANELAS=1920,1280)
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const CASOS = (process.env.CASOS || "a1,v2,b1,k2,v4,t1,n1,al,e1").split(",");

async function subir(caso, proposta) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_orientacao.py"), caso],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: proposta } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o caso ${caso} não subiu`);
  return { proc, url };
}
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
async function ateQuadro(p) {
  for (let k = 0; k < 60; k++) {
    if (await p.$(".orientacao:not([hidden])")) return true;
    const luta = await p.$(`${MENU}:has-text("Começar a luta")`); if (luta) await luta.click().catch(() => {});
    // na luta (AL): agir para os outros agirem (o quadro vale enquanto a animação deles corre)
    const at = await p.$('#roda .roda-botao[data-slot="atacar"]'); if (at) { await at.click().catch(() => {}); const alvo = await p.$("#arena .carta.alvejavel"); if (alvo) await alvo.click().catch(() => {}); }
    await espera(300);
  }
  return false;
}
const medir = (p) => p.evaluate(() => {
  const q = document.querySelector(".orientacao:not([hidden])"), a = document.querySelector(".orientacao-anel:not([hidden])");
  if (!q) return null;
  const r = q.getBoundingClientRect(), ra = a && a.getBoundingClientRect();
  const cobre = ra ? Math.max(0, Math.min(r.right, ra.right) - Math.max(r.left, ra.left)) * Math.max(0, Math.min(r.bottom, ra.bottom) - Math.max(r.top, ra.top)) : 0;
  return { texto: q.querySelector(".orientacao-texto")?.innerText.replace(/\s+/g, " ").trim(), seta: (q.className.match(/seta-\w+/) || ["nenhuma"])[0],
    caixa: [r.left, r.top, r.width, r.height].map(Math.round), alvo: ra ? [ra.left, ra.top, ra.width, ra.height].map(Math.round) : null,
    naJanela: r.left >= 0 && r.top >= 0 && r.right <= innerWidth && r.bottom <= innerHeight, cobreAlvo: Math.round(cobre),
    letra: parseFloat(getComputedStyle(q).fontSize), entendi: !!q.querySelector(".orientacao-entendi"), encerrar: !!q.querySelector(".orientacao-encerrar") };
});

const arq = path.join(SAIDA, "medidas.json");
const medidas = existsSync(arq) ? JSON.parse(readFileSync(arq, "utf8")).medidas : {};
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  for (const caso of CASOS) {
    for (const v of (process.env.VERSOES || "atual,a,b").split(",")) {
      const { proc, url } = await subir(caso, v === "atual" ? "" : v);
      const p = await b.newPage({ viewport: { width: W, height: H } });
      p.on("pageerror", (e) => erros.push(`${jan}-${v}-${caso}: ${e}`));
      try {
        await p.goto(url);
        if (!(await ateQuadro(p))) throw new Error("o quadro não apareceu");
        await espera(700);
        await p.mouse.move(2, 2);
        await p.screenshot({ path: path.join(SAIDA, `${jan}-${v}-${caso}.png`) });
        const m = await medir(p);
        medidas[`${jan}-${v}-${caso}`] = m;
        console.log(jan, v, caso, JSON.stringify(m));
      } catch (e) { erros.push(`${jan}-${v}-${caso}: ${e.message.split("\n")[0]}`); console.log("  erro", jan, v, caso, e.message.split("\n")[0]); }
      await p.close(); proc.kill();
    }
  }
}
await b.close();
writeFileSync(arq, JSON.stringify({ medidas, erros }, null, 1));
console.log(erros.length ? erros : "sem erros");
