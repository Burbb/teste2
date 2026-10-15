// Conferência da comitiva integrada (1.92.0): fotografa o jogo de verdade, sem nenhum arquivo do protótipo, e mede.
//   - Lutas: o Guerreiro com Morel e Odette, o Mago com Yara e Morel, o Arqueiro com Odette e Yara, em janela normal
//     (1500×950) e baixa (1280×720), com movimento normal e reduzido, na vez do herói (o rosto em 32 px exatos, no pixel
//     inteiro); a tecla 1 abre a mira e o Esc volta; um companheiro avançando para agir (a borda acesa); o cartão de
//     reação (Batalha.opiniao, o componente do jogo chamado direto).
//   - Fogueira (cenário fogueira, Morel ferido): o painel da comitiva, a tela da Comitiva (tecla C e Tab), a faixa de
//     quem se junta (Telas.celebrar, chamado direto), o aviso com o rosto (Telas.toast, chamado direto) e a fogueira.
//   - Em toda página: nenhuma <img> com o sprite antigo de Morel, Odette ou Yara.
// Guarda em capturas-integracao/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_integracao.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-integracao");
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
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector("#roda .roda-botao"));
async function vez(p) {
  for (let k = 0; k < 160; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
async function recortar(p, sel, nome, folga = 6) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, Math.floor(r.x - f)), y: Math.max(0, Math.floor(r.y - f)), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
// as <img> com o sprite antigo de um companheiro (o que a tela usava antes de retratos.js)
const antigos = (p) => p.evaluate(() => { const v = new Set(["morel", "odete", "yara"].map((id) => Sprites.url(id)));
  return [...document.querySelectorAll("img")].filter((i) => v.has(i.getAttribute("src"))).length; });
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const medidas = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, mov, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H }, reducedMotion: mov === "reduzido" ? "reduce" : "no-preference" });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  return p;
}
// 1. as lutas
for (const [classe, com, nomes] of [["guerreiro", "morel,odete", ["Morel", "Odette"]], ["mago", "yara,morel", ["Yara", "Morel"]], ["arqueiro", "odete,yara", ["Odette", "Yara"]]]) {
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", CLASSE: classe, COMITIVA: com, LUTA: "lobo", NIVEL_LUTA: "2", VIDA: "1" });
  for (const jan of Object.keys(JANELAS)) for (const mov of ["normal", "reduzido"]) {
    const nome = `luta-${classe}-${jan}-${mov}`;
    const p = await pagina(url, jan, mov, nome);
    await vez(p); await espera(600);
    await recortar(p, "#arena .aliados", `${nome}-aliados`, 10);
    await recortar(p, "#arena", `${nome}-arena`, 0);
    const m = await p.evaluate(() => {
      const r = (e) => { const b = e.getBoundingClientRect(); return [+b.x.toFixed(2), +b.y.toFixed(2), +b.width.toFixed(2), +b.height.toFixed(2)]; };
      const h = document.querySelector(".carta.heroi"), ic = h.querySelector(".icone");
      return { foco: h.classList.contains("foco"), nicho: r(ic), rosto: r(ic.querySelector("img")),
        companheiros: [...document.querySelectorAll(".carta:not(.heroi)[data-cid] .icone img")].map((i) => [i.closest(".carta").dataset.cid, i.naturalWidth, ...r(i).slice(2)]) };
    });
    await p.keyboard.press("1"); await espera(500);
    const mira = await p.evaluate(() => !!document.querySelector(".carta.alvejavel"));
    await p.keyboard.press("Escape"); await espera(500);
    const voltou = await naVez(p);
    const velhos = await antigos(p);
    if (jan === "normal" && mov === "normal") {
      // o cartão de reação (o componente do jogo, chamado direto) e um companheiro avançando
      await p.evaluate((n) => Batalha.opiniao(n[0], n[1], 2), [com.split(",")[0], nomes[0]]); await espera(700);
      await recortar(p, ".cartao-comitiva", `${nome}-reacao`, 6);
      await p.evaluate(() => {
        new MutationObserver((ms, o) => {
          if (!document.querySelector("#arena .aliados .carta.agindo:not(.heroi)")) return;
          document.getAnimations().forEach((a) => a.pause()); window.__parado = true; o.disconnect();
        }).observe(document.getElementById("arena"), { subtree: true, attributes: true, attributeFilter: ["class"] });
      });
      await p.keyboard.press("1"); await espera(500);
      const alvo = await p.$("#arena .inimigos .carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
      try { await p.waitForFunction(() => window.__parado, null, { timeout: 20000 }); await recortar(p, "#arena .aliados", `${nome}-agindo`, 10);
        await p.evaluate(() => document.getAnimations().forEach((a) => a.play())); } catch { console.log(`  ${nome}: nenhum companheiro agiu a tempo`); }
    }
    medidas.push({ nome, ...m, mira, voltou, velhos }); console.log(nome, JSON.stringify({ ...m, mira, voltou, velhos }));
    await p.close();
  }
  proc.kill();
}
// 2. a fogueira, o painel, a Comitiva, a faixa e o aviso
for (const [classe, jan, mov] of [["guerreiro", "normal", "normal"], ["mago", "normal", "normal"], ["arqueiro", "normal", "normal"], ["guerreiro", "baixa", "normal"], ["guerreiro", "baixa", "reduzido"]]) {
  const { proc, url } = await subir("fogueira", { CLASSE: classe, FERIDO: "morel" });
  const nome = `acampamento-${classe}-${jan}-${mov}`;
  const p = await pagina(url, jan, mov, nome);
  await p.waitForSelector('#prompt .escolha:has-text("Acampar")', { timeout: 30000 });
  for (let k = 0; k < 6; k++) { const e = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (!e) break; await e.click().catch(() => {}); await espera(250); }
  await espera(400);
  await recortar(p, "#heroi .secao:has(.membro)", `${nome}-painel`, 6);
  const v1 = await antigos(p);
  if (classe === "guerreiro") {
    // a faixa antes da tela da Comitiva: o Esc que fecha a tela também pula as animações seguintes
    await p.evaluate(() => { Telas.celebrar({ tipo: "comitiva", dados: { id: "yara", nome: "Yara", titulo: "bruxa do pântano" } }, false); }); await espera(450);
    await recortar(p, ".faixa-festa", `${nome}-faixa`, 6);
    await p.evaluate(() => Telas.toast("", "Dá para conversar quando estiver num lugar seguro (vila ou acampamento).", "odete", true)); await espera(400);
    await recortar(p, "#toasts", `${nome}-aviso`, 4);
    await espera(2600);
    await p.keyboard.press("c"); await espera(1000);
    await p.screenshot({ path: path.join(SAIDA, `${nome}-comitiva.png`) });
    await recortar(p, ".tela .cartas", `${nome}-comitiva-cartoes`, 8);
    var v2 = await antigos(p);
    await p.keyboard.press("Escape"); await espera(700);
  }
  await (await p.waitForSelector('#prompt .escolha:has-text("Acampar")')).click();
  await p.waitForSelector(".fogueira-rodape", { timeout: 20000 }); await espera(1500);
  await p.screenshot({ path: path.join(SAIDA, `${nome}-fogueira.png`) });
  await recortar(p, ".tela canvas", `${nome}-fogueira-cena`, 0);
  const v3 = await antigos(p);
  medidas.push({ nome, velhos: [v1, v2 ?? null, v3] }); console.log(nome, "imagens antigas (painel, comitiva, fogueira):", v1, v2 ?? "-", v3);
  await p.close(); proc.kill();
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.js"), `// as medidas de fotografar_integracao.mjs\nwindow.MEDIDAS = ${JSON.stringify(medidas, null, 1)};\n`);
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
