// Fotografa e confere a forja no jogo de verdade (cenario_forja.py, saves temporários): hoje, A e B (VERSOES=atual,a,b),
// a 1920×945 e a 1280×720. Entra pelo prédio do ferreiro no Vau, fotografa, e confere: os nomes dos pontos à vista sem
// o mouse, o ponto do ferreiro levando o foco ao cartão de reforço, um reforço de verdade (o ouro desce, o cartão
// muda), a arte continuando depois do reforço, a Saída voltando à vila e a volta à forja, o Tab chegando aos pontos e
// aos cartões, Esc saindo, e com movimento reduzido o quadro parado. Guarda ../capturas/<janela>-<versão>-*.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/forja/auxiliares/fotografar.mjs
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
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

async function subir(proposta, amb = {}) {
  const proc = spawn(PY, [path.join(aqui, "cenario_forja.py")], { cwd: raiz,
    env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", PROPOSTA: proposta, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 400 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
async function parado(p) {
  for (let k = 0; k < 80 && !(await p.$(MENU)); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
  await espera(700);
}
async function entrar(p) {
  await p.click('[data-predio="ferreiro"]');
  await p.waitForSelector(".forja .servico", { timeout: 15000 });
  await espera(1200);
}
const ouro = (p) => p.evaluate(() => estado.heroi.ouro);
// de volta à vila: a tela do lugar (não a de menu da forja), com os prédios e o menu
const naVila = (p) => p.waitForFunction(() => document.getElementById("cena").dataset.tipo === "local" && !document.querySelector(".forja")
  && !!document.querySelector('[data-predio="ferreiro"]'), null, { timeout: 15000 }).then(() => true, () => false);

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  for (const v of (process.env.VERSOES || "atual,a,b").split(",")) {
    console.log(`== ${jan} ${v}`);
    const { proc, url } = await subir(v === "atual" ? "" : v);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    // conta os relógios que a página cria (sair e entrar na forja não pode criar outro: a arte anda no da vista)
    await p.addInitScript(() => { window.__relogios = 0; const si = window.setInterval; window.setInterval = (...a) => { window.__relogios++; return si(...a); }; });
    const pre = `${jan}-${v}`;
    try {
      await p.goto(url); await parado(p);
      await entrar(p);
      await p.mouse.move(2, 2); await espera(400);
      await p.screenshot({ path: path.join(SAIDA, `${pre}-forja.png`) });
      const lay = await p.evaluate(() => {
        const vista = document.getElementById("vista"), r = vista.getBoundingClientRect(), pg = document.getElementById("pagina");
        const ult = [...document.querySelectorAll(".forja .servico")].pop().getBoundingClientRect();
        const baloes = [...document.querySelectorAll("#pontos-cena .ci-balao")].map((e) => { const s = getComputedStyle(e); const q = e.getBoundingClientRect();
          return { texto: e.textContent, visivel: s.visibility === "visible", dentro: q.left >= r.left - 1 && q.right <= r.right + 1 && q.top >= r.top - 1 }; });
        return { arte: vista.offsetHeight > 0 && getComputedStyle(vista).display !== "none" ? Math.round(r.height) : 0, baloes,
          cartoesAVista: ult.bottom <= pg.getBoundingClientRect().bottom + 1, rola: pg.scrollHeight > pg.clientHeight + 1 };
      });
      console.log("  ", JSON.stringify(lay));
      {  // desde a 1.210.0 a forja do jogo ("atual") também tem o ambiente
        conferir(lay.arte > 100, `a arte da forja no topo (${lay.arte} px de altura)`);
        conferir(lay.baloes.length === 2 && lay.baloes.every((x) => x.visivel && x.dentro), `os nomes dos pontos à vista e dentro da arte (${lay.baloes.map((x) => x.texto).join(", ")})`);
        conferir(lay.cartoesAVista, "os três cartões de reforço à vista sem rolar");
        // o ponto do ferreiro: leva o foco ao cartão
        await p.click('#pontos-cena .ci-ponto[data-ponto="ferreiro"]'); await espera(300);
        conferir(await p.evaluate(() => !!document.activeElement.closest(".forja .servico")), "o clique no Ferreiro leva o foco ao cartão de reforço");
        // o teclado chega aos pontos (os balões no foco)
        await p.evaluate(() => document.activeElement.blur());
        let chegou = false; for (let k = 0; k < 40 && !chegou; k++) { await p.keyboard.press("Tab"); chegou = await p.evaluate(() => !!document.activeElement.closest("#pontos-cena .ci-ponto")); }
        conferir(chegou, "o Tab chega aos pontos da cena");
        await p.screenshot({ path: path.join(SAIDA, `${pre}-foco-ponto.png`) });
      }
      // um reforço de verdade, pelo cartão (o mesmo do jogo)
      const antes = await ouro(p);
      await p.click(".forja .servico:not(.caro):not(.limite)");
      await p.waitForFunction((o) => estado.heroi.ouro < o, antes, { timeout: 15000 });
      await espera(1500);
      const depois = await ouro(p);
      conferir(depois < antes, `reforçar: o ouro desce (${antes} → ${depois})`);
      await p.mouse.move(2, 2);
      await p.screenshot({ path: path.join(SAIDA, `${pre}-depois-do-reforco.png`) });
      conferir(await p.evaluate(() => document.getElementById("cena").classList.contains("com-ambiente")), "a arte continua depois do reforço");
      // a saída: pelo ponto na arte (A e B) ou pelo Voltar (hoje), de volta à vila; e entrar de novo
      await p.click('#pontos-cena .ci-ponto[data-ponto="saida"]');
      conferir(await naVila(p), "sair da forja volta à vila");
      await parado(p);
      conferir(await p.evaluate(() => !document.getElementById("cena").classList.contains("com-ambiente")), "na vila, a paisagem de sempre (o ambiente da forja saiu)");
      const antesRel = await p.evaluate(() => window.__relogios);
      await entrar(p);
      conferir(await p.evaluate(() => window.__relogios) === antesRel, `entrar de novo na forja não cria outro relógio (${antesRel})`);
      await p.keyboard.press("Escape");
      conferir(await naVila(p), "Esc sai da forja");
    } catch (e) { conferir(false, `${pre}: ${e.message.split("\n")[0]}`); }
    conferir(erros.length === 0, `sem erros na página ${erros.join(" ")}`);
    await p.close();
    // movimento reduzido: o quadro parado (duas fotos da arte iguais)
    if (jan === "1920") {
      const p2 = await b.newPage({ viewport: { width: W, height: H }, reducedMotion: "reduce" });
      await p2.goto(url).catch(() => {});
      await parado(p2); await entrar(p2); await p2.mouse.move(2, 2);
      const r = await p2.$eval("#vista", (e) => { const q = e.getBoundingClientRect(); return { x: q.left, y: q.top, width: q.width, height: q.height }; });
      const f1 = await p2.screenshot({ clip: r }); await espera(900); const f2 = await p2.screenshot({ clip: r });
      conferir(Buffer.compare(f1, f2) === 0, "com movimento reduzido, o fogo parado (duas fotos iguais)");
      await p2.screenshot({ path: path.join(SAIDA, `${pre}-reduzido.png`) });
      await p2.close();
    }
    proc.kill();
  }
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
