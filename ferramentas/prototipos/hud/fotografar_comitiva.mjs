// Teste da comitiva (experimento): fotografa o jogo de verdade com os sprites de hoje de Morel, Odette e Yara e com os
// candidatos (arte-teste.js, postos na página por comitiva-no-jogo.js só aqui; o jogo não muda). Em janela normal
// (1500×950) e baixa (1280×720): a fogueira com cada herói (Morel e Odette juntos, Yara no acampamento, Morel ferido),
// o painel da comitiva ao lado (vida, aprovação, ferimento), a tela da Comitiva (tecla C, com o foco do teclado) e a
// luta (as cartas). Guarda em capturas-comitiva/.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_comitiva.mjs
// (SO=luta: só as lutas)
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-comitiva");
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
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, W, H) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(String(e)));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(m.text()); });
  await p.goto(url);
  return p;
}
const fechar = async (p) => { for (let k = 0; k < 6; k++) { const e = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (!e) break; await e.click().catch(() => {}); await espera(250); } };
const vestir = async (p, versao) => {
  if (versao !== "candidato") return;
  await p.addScriptTag({ path: path.join(aqui, "arte-teste.js") });
  await p.addScriptTag({ path: path.join(aqui, "comitiva-no-jogo.js") });
  await espera(500);
};
const recorte = async (p, sel, nome, folga = 6) => {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, r.x - f), y: Math.max(0, r.y - f), width: r.width + 2 * f, height: r.height + 2 * f } : null; }, [sel, folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
};
const contar = (p) => p.evaluate(() => `${document.querySelectorAll("img.arte-teste").length} imagens do candidato`);
const JANELAS = [[1500, 950, "normal"], [1280, 720, "baixa"]];
for (const [W, H, jan] of JANELAS) {
  for (const versao of ["hoje", "candidato"]) {
    // a fogueira e o painel da comitiva, com cada herói
    for (const classe of process.env.SO === "luta" ? [] : jan === "normal" ? ["guerreiro", "mago", "arqueiro"] : ["guerreiro"]) {
      const { proc, url } = await subir("fogueira", { CLASSE: classe, FERIDO: "morel" });
      const p = await pagina(url, W, H);
      await p.waitForSelector('#prompt .escolha:has-text("Acampar")', { timeout: 30000 }); await fechar(p);
      await vestir(p, versao);
      const base = `${jan}-${versao}-${classe}`;
      await recorte(p, "#heroi .secao:has(.membro)", `${base}-painel-membro`);
      await p.screenshot({ path: path.join(SAIDA, `${base}-lugar.png`) });
      if (classe === "guerreiro") {  // a tela da Comitiva pela tecla C, e o foco do teclado num cartão
        await p.keyboard.press("c"); await espera(1200);
        await p.screenshot({ path: path.join(SAIDA, `${base}-tela-comitiva.png`) });
        for (let k = 0; k < 40; k++) { await p.keyboard.press("Tab"); if (await p.evaluate(() => !!document.activeElement.closest(".tela.comitiva, .comitiva"))) break; }
        await espera(200); await p.screenshot({ path: path.join(SAIDA, `${base}-tela-comitiva-foco.png`) });
        console.log(`${base} tela da Comitiva: foco em ${await p.evaluate(() => document.activeElement.className)}; ${await contar(p)}`);
        await p.keyboard.press("Escape"); await espera(800);
      }
      await (await p.waitForSelector('#prompt .escolha:has-text("Acampar")')).click();
      await p.waitForSelector(".fogueira-rodape", { timeout: 20000 }); await espera(1500);
      await p.screenshot({ path: path.join(SAIDA, `${base}-fogueira.png`) });
      await recorte(p, ".tela canvas", `${base}-fogueira-cena`, 0);
      console.log(`${base} fogueira: ${await contar(p)}`);
      await p.close(); proc.kill();
    }
    // a luta, com os companheiros nas cartas
    for (const [nome, com] of [["morel-odette", "morel,odete"], ["yara-morel", "yara,morel"]]) {
      const { proc, url } = await subir("tutorial", { TUTORIAL: "0", COMITIVA: com, LUTA: "lobo", NIVEL_LUTA: "2", VIDA: "1" });
      const p = await pagina(url, W, H);
      await vestir(p, versao);
      for (let k = 0; k < 120 && !(await p.$("#roda .roda-botao")); k++) { await fechar(p); const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(250); }
      await espera(900);
      const base = `${jan}-${versao}-luta-${nome}`;
      await p.screenshot({ path: path.join(SAIDA, `${base}.png`) });
      await recorte(p, "#arena", `${base}-arena`, 0);
      console.log(`${base}: ${await contar(p)}`);
      await p.close(); proc.kill();
    }
  }
}
await b.close();
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
