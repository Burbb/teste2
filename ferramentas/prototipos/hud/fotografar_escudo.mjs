// O teste do escudo (experimento): fotografa o jogo de verdade com o escudo atual da HUD e com o candidato de
// desenhar_escudo.py (escudo-teste/), com os mesmos dados. O jogo não muda: o roteiro responde aos pedidos de
// /static/hud/icones/escudo-*.png com os arquivos do candidato, que têm os mesmos nomes e tamanhos.
//   - 32 px: a ficha, o Inventário (o corpo e a mochila) e o Mercado (a aba Vender, com a mochila), no cenário
//     tutorial com VITRINE=1 (um broquel vestido e outro na mochila);
//   - 64 e 48 px: o cartão do saque e o voo ao equipar (cenário vila com ACHADO=escudo);
//   - a tela inteira: a vila com o Guerreiro e o cenário, e o Inventário.
// Em janela normal (1500×950) e baixa (1280×720). Guarda em capturas-escudo/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_escudo.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync, existsSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-escudo"), CANDIDATO = path.join(aqui, "escudo-teste");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(cenario, amb = {}) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 150 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const trocados = [];
async function pagina(b, url, W, H, versao) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  if (versao === "candidato") await p.route(/\/static\/hud\/icones\/escudo-[^/]+\.png/, (rota) => {
    const arq = path.join(CANDIDATO, path.basename(new URL(rota.request().url()).pathname));
    if (!existsSync(arq)) return rota.continue();
    trocados.push(path.basename(arq));
    return rota.fulfill({ path: arq, contentType: "image/png" });
  });
  await p.goto(url);
  return p;
}
async function ate(p, sel) {
  for (let k = 0; k < 60 && !(await p.$(sel)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await espera(900);
}
async function foto(p, sel, nome, folga = 0) {
  await p.mouse.move(2, 2); await espera(250);
  const c = sel && await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return { x: Math.max(0, Math.floor(r.left - f)), y: Math.max(0, Math.floor(r.top - f)), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) }; }, [sel, folga]);
  if (sel && !c) { console.log(`  (sem ${sel} em ${nome})`); return; }
  await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), ...(c ? { clip: c } : {}) });
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of Object.keys(JANELAS)) for (const versao of ["atual", "candidato"]) {
  const [W, H] = JANELAS[jan], n = (c) => `${jan}-${versao}-${c}`;
  // a vila do Vau, com o broquel vestido e outro na mochila
  {
    const { proc, url } = await subir("tutorial", { TUTORIAL: "0", VITRINE: "1", VISTAS: "A1,V2,N1,D1,K1,M1", OURO: "200" });
    const p = await pagina(b, url, W, H, versao);
    p.on("pageerror", (e) => erros.push(`${jan} ${versao}: ${e}`));
    await ate(p, "#predios .predio");
    await foto(p, null, n("tela-vila"));
    await foto(p, "#heroi", n("ficha"));
    await (await p.$('#doca .atalho[data-rotulo="Inventário"]')).click(); await espera(1200);
    await foto(p, null, n("tela-inventario"));
    await foto(p, "#cena", n("inventario"));
    await p.keyboard.press("Escape"); await espera(900);
    await ate(p, "#predios .predio");
    await (await p.$('#predios .predio[data-predio="mercado"]')).click(); await espera(1500);
    const vender = await p.$('.tela.loja .aba:has-text("Vender"), .tela.loja button:has-text("Vender")');
    if (vender) { await vender.click(); await espera(700); }
    await foto(p, "#cena", n("mercado"));
    await p.close(); proc.kill();
  }
  // o cartão do saque (64 px) e o voo ao equipar (48 px)
  {
    const { proc, url } = await subir("vila", { ACHADO: "escudo" });
    const p = await pagina(b, url, W, H, versao);
    p.on("pageerror", (e) => erros.push(`${jan} ${versao} saque: ${e}`));
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(1500);
    await foto(p, ".janela-achado", n("saque"), 6);
    await p.evaluate(() => {
      new MutationObserver((ms, o) => { const v = document.querySelector(".voo-item"); if (!v) return;
        setTimeout(() => { document.getAnimations().forEach((a) => a.pause()); window.__voo = true; }, 120); o.disconnect(); })
        .observe(document.body, { childList: true });
    });
    const eq = await p.$('#prompt .escolha:has-text("Equipar")');
    if (eq) await eq.click(); else await p.keyboard.press("1");
    try {
      await p.waitForFunction(() => window.__voo, null, { timeout: 8000 });
      await foto(p, ".voo-item", n("voo"), 16);
      await p.evaluate(() => document.getAnimations().forEach((a) => a.play()));
    } catch { console.log(`  ${jan} ${versao}: o voo não apareceu`); }
    await p.close(); proc.kill();
  }
  console.log(jan, versao, "ok");
}
await b.close();
console.log(`arquivos do candidato servidos: ${[...new Set(trocados)].sort().join(", ") || "nenhum"}`);
console.log(erros.length ? erros.join("\n") : "sem erros");
