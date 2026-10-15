// A proposta do Mago na fogueira e das versões pequenas do Morel, no jogo de verdade, atual × candidata, em janela
// normal (1500×950) e baixa (1280×720), em tamanho real. O jogo não muda: na candidata, o roteiro acrescenta
// personagens-teste.js e personagens-no-jogo.js ao fim de /static/retratos.js só nesta página.
//   - a fogueira com o Mago, sozinho e com a comitiva (Morel e Odette na roda, Yara no acampamento);
//   - o painel da comitiva (Morel e Odette, a carta de 32), a tela da Comitiva (cartões, a cabeça de 48), o cartão de
//     reação, a faixa de quem chega e o aviso (os dois pela mesma chamada do jogo, com o Morel);
//   - a luta com o Guerreiro, o Morel e a Odette (a vez do herói em destaque e o Morel avançando) e com o Arqueiro e o
//     Morel.
// Guarda em capturas-personagens/ (ou SAIDA).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/personagens/fotografar_personagens.mjs
// (CHROMIUM=<executável>; VERSOES=atual,candidata; SO=fogueira,luta)
import { spawn } from "child_process";
import { mkdirSync, readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-personagens"));
const SO = new Set((process.env.SO || "fogueira,luta").split(","));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(cenario, amb = {}) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const EXTRA = readFileSync(path.join(aqui, "personagens-teste.js"), "utf8") + '\nwindow.PERSONAGENS = { versao: "candidata" };\n' +
  readFileSync(path.join(aqui, "personagens-no-jogo.js"), "utf8");
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, W, H, versao, nome) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  if (versao === "candidata") await p.route("**/static/retratos.js", async (rota) => {
    const r = await rota.fetch();
    await rota.fulfill({ response: r, body: (await r.text()) + "\n" + EXTRA, headers: { ...r.headers(), "content-type": "application/javascript" } });
  });
  await p.goto(url);
  return p;
}
const fechar = async (p) => { for (let k = 0; k < 6; k++) { const e = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (!e) break; await e.click().catch(() => {}); await espera(250); } };
async function recorte(p, sel, nome, folga = 6) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, Math.floor(r.x - f)), y: Math.max(0, Math.floor(r.y - f)), width: Math.ceil(r.width + 2 * f), height: Math.ceil(r.height + 2 * f) } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sel} em ${nome})`);
}
// o tamanho e o pixel inteiro de cada retrato do Morel na tela (e se é o candidato)
const medir = (p) => p.evaluate(() => [...document.querySelectorAll("img")].filter((i) => /retrato-morel|teste-morel/.test(i.getAttribute("src") || "") || i.closest('[data-cid="morel"]')).map((i) => {
  const r = i.getBoundingClientRect(), lugar = (i.closest(".carta, .membro, .cartao, .cartao-comitiva, .faixa-festa, .toast") || i.parentElement).className.split(" ")[0];
  return `${lugar}:${Math.round(r.width * 100) / 100}px@${Math.round(r.x * 100) / 100},${Math.round(r.y * 100) / 100}${(i.getAttribute("src") || "").includes("data:") ? "" : ""}`;
}));
const JANELAS = [[1500, 950, "normal"], [1280, 720, "baixa"]];
for (const [W, H, jan] of JANELAS) {
  for (const versao of (process.env.VERSOES || "atual,candidata").split(",")) {
    if (SO.has("fogueira")) for (const [nomeCena, amb] of [["sozinho", { COMITIVA: "", RESERVA: "" }], ["comitiva", {}]]) {
      const { proc, url } = await subir("fogueira", { CLASSE: "mago", ...amb });
      const base = `${jan}-${versao}-mago-${nomeCena}`;
      const p = await pagina(url, W, H, versao, base);
      await p.waitForSelector('#prompt .escolha:has-text("Acampar")', { timeout: 30000 }); await fechar(p);
      if (nomeCena === "comitiva") {
        await recorte(p, "#heroi .secao:has(.membro)", `${jan}-${versao}-painel-comitiva`);
        await p.keyboard.press("c"); await espera(1200);
        await recorte(p, ".tela:has(.cartao[data-cid])", `${jan}-${versao}-tela-comitiva`, 4);
        console.log(`${jan}-${versao} Comitiva: ${await medir(p)}`);
        await p.keyboard.press("Escape"); await espera(800);
        // as três chamadas do jogo que mostram o Morel fora da luta: a reação (48), quem chega (48) e o aviso (32)
        await p.evaluate(() => Batalha.opiniao("morel", "Morel", 4)); await espera(500);
        await recorte(p, ".cartao-comitiva", `${jan}-${versao}-cartao-reacao`, 4);
        await p.evaluate(() => Telas.toast("Morel", "Morel aprova.", "morel", true)); await espera(500);
        await recorte(p, "#toasts .toast", `${jan}-${versao}-aviso`, 4);
        await p.evaluate(() => { Telas.celebrar({ tipo: "comitiva", dados: { id: "morel", nome: "Morel", titulo: "o mercenário" } }, false); });
        await espera(700);
        await p.evaluate(() => document.getAnimations().forEach((a) => a.pause()));
        await recorte(p, ".faixa-festa", `${jan}-${versao}-faixa-chegada`, 4);
        console.log(`${jan}-${versao} cartões: ${await medir(p)}`);
        await p.evaluate(() => document.getAnimations().forEach((a) => a.play())); await espera(4200);
      }
      await (await p.waitForSelector('#prompt .escolha:has-text("Acampar")')).click();
      await p.waitForSelector(".fogueira-palco", { timeout: 20000 }); await espera(1500);
      await p.screenshot({ path: path.join(SAIDA, `${base}-fogueira.png`) });
      await recorte(p, ".fogueira-palco", `${base}-fogueira-palco`, 0);
      await p.close(); proc.kill();
    }
    if (SO.has("luta")) for (const [nome, amb] of [["guerreiro-morel-odette", { CLASSE: "guerreiro", COMITIVA: "morel,odete" }], ["arqueiro-morel", { CLASSE: "arqueiro", COMITIVA: "morel" }]]) {
      const { proc, url } = await subir("tutorial", { TUTORIAL: "0", LUTA: "lobo", NIVEL_LUTA: "2", VIDA: "1", ...amb });
      const base = `${jan}-${versao}-luta-${nome}`;
      const p = await pagina(url, W, H, versao, base);
      for (let k = 0; k < 120 && !(await p.$("#roda .roda-botao")); k++) { await fechar(p); const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(250); }
      await espera(1200);
      await p.screenshot({ path: path.join(SAIDA, `${base}.png`) });
      await recorte(p, "#arena", `${base}-arena`, 0);
      await recorte(p, "#heroi .secao:has(.membro)", `${base}-painel`);
      console.log(`${base}: ${await medir(p)}`);
      // o Morel avançando: o herói ataca e, quando a carta de um companheiro avança, as animações param
      await p.evaluate(() => {
        new MutationObserver((ms, o) => {
          if (!document.querySelector("#arena .aliados .carta.agindo:not(:has(.carta-rec))")) return;
          document.getAnimations().forEach((a) => a.pause()); window.__parado = true; o.disconnect();
        }).observe(document.getElementById("arena"), { subtree: true, attributes: true, attributeFilter: ["class"] });
      });
      await p.keyboard.press("1"); await espera(600);
      const alvo = await p.$("#arena .inimigos .carta.alvejavel"); if (alvo) await alvo.click().catch(() => {});
      try {
        await p.waitForFunction(() => window.__parado, null, { timeout: 20000 });
        await recorte(p, "#arena", `${base}-agindo`, 0);
        await p.evaluate(() => document.getAnimations().forEach((a) => a.play()));
      } catch { console.log(`  ${base}: nenhum companheiro agiu a tempo`); }
      await p.close(); proc.kill();
    }
  }
}
await b.close();
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
