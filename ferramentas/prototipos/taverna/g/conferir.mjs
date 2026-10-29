// Confere as candidatas da taverna no jogo de verdade (demo.py, save temporário), a 1920×945 e a 1280×720: entra
// pelo prédio da taverna no Vau e, em cada candidata (CANDS, padrão "g2,g"; "h" também serve; trocadas pelo painel, no mesmo estado
// do jogo) e em cada estado do save (o homem do canto, a despensa esperando, Morel conhecido, recrutado, sem ouro),
// fotografa a cena com o balcão embaixo e confere: os pontos (o Taverneiro sempre, a Despensa
// só enquanto ela espera; nenhum da escada, da rua ou de Morel), os nomes dentro da arte, sem cobrir o rosto nem as
// mãos, o ponto levando ao cartão certo, os cartões à vista sem rolar, o Tab chegando aos pontos, o Esc e o Voltar
// voltando à vila, e o console sem erro. Guarda as fotos em <SAIDA> (padrão: g/capturas, fora do git).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/taverna/g/conferir.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = process.env.SAIDA || path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

const proc = spawn(PY, [path.join(raiz, "ferramentas", "prototipos", "taverna", "demo.py")], { cwd: raiz,
  env: { ...process.env, VELOCIDADE: "rapido", SEM_NAVEGADOR: "1", DEMO_PORTA: process.env.DEMO_PORTA || "8796", PYTHONIOENCODING: "utf-8" } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m && !url) url = m[0]; });
proc.stderr.on("data", (d) => process.stderr.write(d));
for (let k = 0; k < 400 && !url; k++) await espera(100);
if (!url) { proc.kill(); throw new Error("a demonstração não subiu"); }

async function parado(p) {
  for (let k = 0; k < 80 && !(await p.$(MENU)); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
  await espera(500);
}
const naTaverna = (p) => p.waitForFunction(() => window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna"
  && document.querySelectorAll("#folha .servico").length > 0, null, { timeout: 15000 }).then(() => true, () => false);
const naVila = (p) => p.waitForFunction(() => !(window.Cenas && Cenas.atual()) && !!document.querySelector('[data-predio="taverna"]'),
  null, { timeout: 15000 }).then(() => true, () => false);
async function entrar(p) {
  await p.click('[data-predio="taverna"]');
  const ok = await naTaverna(p);
  await espera(900);
  return ok;
}
async function trocarEstado(p, id) {
  await p.click("#faixa-tav .abre");
  await p.click(`#faixa-tav-painel [data-tav="${id}"]`);
  await espera(600);
  await parado(p);
  if (!(await p.evaluate(() => window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna"))) await entrar(p);
  await naTaverna(p);
  await espera(700);
}
const ESPERADO = {  // os pontos da G em cada estado e o que os cartões mostram
  homem_do_canto: ["taverneiro"], despensa: ["taverneiro", "despensa"], conhecido: ["taverneiro"],
  recrutado: ["taverneiro"], sem_ouro: ["taverneiro"],
};

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
try {
  for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
    const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
    console.log(`== ${W}×${H}`);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
    await p.goto(url); await parado(p);
    conferir(await entrar(p), "entra na taverna pelo prédio");
    conferir(await p.evaluate(() => document.body.dataset.tavCand === "g2"), "a demonstração abre na G refinada");
    for (const cand of (process.env.CANDS || "g2,g").split(",")) {
    if (await p.evaluate(() => document.body.dataset.tavCand) !== cand) {  // a troca pelo painel, no mesmo estado
      await p.click("#faixa-tav .abre"); await p.click(`#faixa-tav-painel [data-cand="${cand}"]`); await espera(500);
      conferir(await p.evaluate((c) => document.body.dataset.tavCand === c && Cenas.atual().d.cena === "taverna", cand),
        `a troca para a ${cand.toUpperCase()} pelo painel, sem sair da taverna`);
    }
    const [fx, fy] = cand === "h" ? [-10, -6] : [0, 0];  // onde o taverneiro cai em cada uma
    for (const est of Object.keys(ESPERADO)) {
      if (est !== "homem_do_canto") await trocarEstado(p, est);  // a demonstração abre (e a volta deixa) no homem do canto
      await p.mouse.move(2, 2); await espera(300);
      const lay = await p.evaluate(() => {
        const vista = document.getElementById("vista").getBoundingClientRect(), pg = document.getElementById("pagina");
        const doca = document.getElementById("doca"), fimDoca = doca ? doca.getBoundingClientRect().top : innerHeight;
        const cartoes = [...document.querySelectorAll("#folha .servico, #folha .escolha")].filter((e) => e.offsetParent);
        const baixo = Math.max(...cartoes.map((e) => e.getBoundingClientRect().bottom));
        return { pontos: [...document.querySelectorAll("#pontos-cena .ci-ponto")].map((e) => e.dataset.ponto),
          cartoes: [...document.querySelectorAll("#folha .servico")].map((e) => e.dataset.servico || e.textContent.trim().slice(0, 30)),
          arte: Math.round(vista.height), cabem: baixo <= Math.min(fimDoca, pg.getBoundingClientRect().bottom) + 1,
          rola: pg.scrollHeight > pg.clientHeight + 1 };
      });
      console.log(`  [${est}]`, JSON.stringify(lay));
      conferir(JSON.stringify(lay.pontos) === JSON.stringify(ESPERADO[est]), `${cand} ${est}: os pontos ${lay.pontos.join(", ")}`);
      conferir(lay.cabem, `${cand} ${est}: os cartões e o Voltar acima da doca, sem rolar`);
      // os nomes com F4 (Destacar interações): dentro da arte, longe do rosto e das mãos
      await p.evaluate(() => document.body.classList.add("destacar-interacoes")); await espera(250);
      const bal = await p.evaluate(([fx, fy]) => {
        const r = document.getElementById("vista").getBoundingClientRect(), q = Vista.caixaDaArte();
        const ar = (x, y, w, h) => ({ l: q.esq + q.dx + x * q.ex, t: q.topo + q.dy + y * q.ey, r: q.esq + q.dx + (x + w) * q.ex, b: q.topo + q.dy + (y + h) * q.ey });
        const rosto = ar(149 + fx, 17 + fy, 22, 27), maos = ar(146 + fx, 50 + fy, 30, 16);
        const cruza = (a, c) => a.left < c.r && a.right > c.l && a.top < c.b && a.bottom > c.t;
        return [...document.querySelectorAll("#pontos-cena .ci-balao")].map((e) => { const a = e.getBoundingClientRect();
          return { texto: e.textContent, dentro: a.left >= r.left - 1 && a.right <= r.right + 1 && a.top >= r.top - 1,
            livre: !cruza(a, rosto) && !cruza(a, maos) }; });
      }, [fx, fy]);
      conferir(bal.every((x) => x.dentro && x.livre), `${cand} ${est}: os nomes dentro da arte, sem cobrir rosto nem mãos (${bal.map((x) => x.texto).join(", ")})`);
      await p.screenshot({ path: path.join(SAIDA, `${jan}-${cand}-${est}-nomes.png`) });
      await p.evaluate(() => document.body.classList.remove("destacar-interacoes"));
      await p.screenshot({ path: path.join(SAIDA, `${jan}-${cand}-${est}.png`) });
      // cada ponto leva ao cartão dele
      for (const [ponto, servico] of [["taverneiro", "rumores"], ["despensa", "despensa"]]) {
        if (!lay.pontos.includes(ponto)) continue;
        await p.click(`#pontos-cena .ci-ponto[data-ponto="${ponto}"]`); await espera(250);
        const foco = await p.evaluate(() => { const c = document.activeElement.closest("#folha .servico"); return c ? c.dataset.servico : null; });
        conferir(foco === servico, `${cand} ${est}: o ponto ${ponto} leva ao cartão ${servico} (${foco})`);
      }
    }
    await trocarEstado(p, "homem_do_canto");
    }
    // o teclado chega aos pontos; Esc volta à vila; o Voltar também
    await p.evaluate(() => document.activeElement && document.activeElement.blur());
    let chegou = false;
    for (let k = 0; k < 50 && !chegou; k++) { await p.keyboard.press("Tab"); chegou = await p.evaluate(() => !!document.activeElement.closest("#pontos-cena .ci-ponto")); }
    conferir(chegou, "o Tab chega ao ponto do Taverneiro");
    await p.screenshot({ path: path.join(SAIDA, `${jan}-foco-ponto.png`) });
    await p.keyboard.press("Escape");
    conferir(await naVila(p), "o Esc volta à vila");
    await parado(p);
    conferir(await entrar(p), "entra de novo");
    const voltar = await p.$("#folha .escolha:has-text('Voltar')") || await p.$("text=Voltar à vila");
    if (voltar) { await voltar.click(); conferir(await naVila(p), "o Voltar à vila volta à vila"); } else conferir(false, "o Voltar à vila à vista");
    await parado(p);
    await entrar(p);
    await p.click("#faixa-tav .abre"); await p.click("#faixa-tav-painel [data-reduzido]"); await espera(400);
    const a1 = await p.evaluate(() => document.getElementById("vista").toDataURL());
    await espera(900);
    const a2 = await p.evaluate(() => document.getElementById("vista").toDataURL());
    conferir(a1 === a2, "com a pose parada, o fogo e o lampião param");
    await p.click("#faixa-tav-painel [data-reduzido]"); await p.click("#faixa-tav .abre");  // o painel continua aberto
    await trocarEstado(p, "homem_do_canto");
    conferir(erros.length === 0, `o console sem erro${erros.length ? ": " + erros.join(" | ") : ""}`);
    await p.close();
  }
} finally {
  await b.close();
  proc.kill();
}
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
