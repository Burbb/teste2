// O segundo par das criaturas na luta e no Bestiário, a 1920×945 (21/10/2026), atual × as propostas A e B, com os
// mesmos dados. Nas propostas, só a página troca a imagem do retrato das cartas inimigas e do Bestiário cujo nome é o
// da criatura (o jogo escolhe pelo traço: o lobo é o "fera", o bandido o "humano"). Situações: uma luta com dois
// lobos, uma aranha (também "fera"), dois bandidos e um cultista (também "humano"), com o Lobo Cinzento do patrulheiro
// do lado do herói (também "fera": não troca); e o Bestiário com as mesmas espécies.
//   [MODOS=atual,a,b | r2-base,r2-brutamontes,r2-chapeu,r2-faca] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.join(raiz, "ferramentas/prototipos/hud/criaturas/lobo_bandido/proposta");
const dados = (id) => "data:image/png;base64," + readFileSync(path.join(aqui, `${id}-16.png`)).toString("base64");
// o nome inteiro da espécie (o afixo, quando há, vem depois: "Lobo feroz"); o animal do herói ("Lobo Cinzento") fica
// de fora porque a troca é só nas cartas inimigas
const TROCAS = { a: [["^Lobo( |$)", dados("lobo-a")], ["^Bandido( |$)", dados("bandido-a")]],
  b: [["^Lobo( |$)", dados("lobo-b")], ["^Bandido( |$)", dados("bandido-b")]],
  // a segunda rodada: o Lobo A só com a base nova (o bandido de hoje), e o Lobo A ajustado com cada Bandido novo
  "r2-base": [["^Lobo( |$)", dados("lobo-a-base")]] };
for (const bd of ["brutamontes", "chapeu", "faca"])
  TROCAS[`r2-${bd}`] = [["^Lobo( |$)", dados("lobo-a-ajustado")], ["^Bandido( |$)", dados(`bandido-${bd}`)]];
const MODOS = (process.env.MODOS || "atual,a,b").split(",");
const SITUACOES = [
  { nome: "luta", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "arqueiro", NIVEL: "4", ANIMAL: "lobo", NIVEL_LUTA: "2",
    GRUPO: "lobo:2,aranha:1,bandido:2,cultista:1" }, espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila",
    BESTIARIO: "lobo:3,bandido:3,aranha:2,cultista:2" }, passos: [{ tecla: "b" }], espera: ".cartao .cab",
    fotos: [["body", "pagina"]] },
];
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
// o registro acumula: um modo fotografado de novo substitui só a entrada dele
const arqRegistro = path.join(saida, "registro.json");
const registro = existsSync(arqRegistro) ? JSON.parse(readFileSync(arqRegistro, "utf-8")) : {};
for (const sit of SITUACOES) {
  for (const modo of MODOS) {
    const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
      env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", PERIODO: "0", ...sit.amb } });
    let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
    for (let k = 0; k < 300 && !url; k++) await espera(100);
    try {
      const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
      const erros = [], avisos = [];
      p.on("pageerror", (e) => erros.push(String(e)));
      p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") avisos.push(m.text()); });
      await p.goto(url);
      await espera(2500);
      if (TROCAS[modo]) await p.evaluate((troca) => {
        const aplica = () => {
          for (const [padrao, src] of troca) {
            const re = new RegExp(padrao);
            for (const c of document.querySelectorAll(".inimigos .carta")) {
              const n = c.querySelector(".carta-nome span");
              const im = c.querySelector(".icone img");
              if (n && im && re.test(n.textContent.trim()) && im.src !== src) im.src = src;
            }
            for (const c of document.querySelectorAll(".cartao")) {
              const n = c.querySelector("b"), im = c.querySelector(".cab img");
              if (n && im && re.test(n.textContent.trim()) && im.src !== src) im.src = src;
            }
          }
        };
        aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true, characterData: true });
      }, TROCAS[modo]);
      for (const passo of sit.passos || []) {
        if (passo.tecla) await p.keyboard.press(passo.tecla);
        if (passo.clicar) {   // o texto pode vir depois de "Continuar": clica no que aparecer primeiro
          for (let k = 0; k < 20; k++) {
            if (await p.$(`text=${passo.clicar}`)) { await p.click(`text=${passo.clicar}`); break; }
            const cont = await p.$("text=Continuar");
            if (cont) await cont.click().catch(() => {});
            await espera(800);
          }
        }
        await espera(1500);
      }
      await p.waitForSelector(sit.espera, { timeout: 30000 }).catch(() => erros.push(`não apareceu: ${sit.espera}`));
      await espera(1500);
      for (const [sel, nome] of sit.fotos) {
        const alvo = sel === "body" ? p : p.locator(sel).first();
        await alvo.screenshot({ path: path.join(saida, `${sit.nome}-${modo}-${nome}.png`) }).catch((e) => erros.push(String(e)));
      }
      registro[`${sit.nome}/${modo}`] = { erros, avisos, cartas: await p.evaluate(() => [...document.querySelectorAll(".carta, .cartao, .rastro-contrato")]
        .map((c) => { const im = c.querySelector(".icone img, .cab img, .rastro-arte img") || {};
          // o nome, o começo do endereço e a medida: o lado na tela / o lado do arquivo (o modo final: o jogo integrado)
          return ((c.querySelector(".carta-nome span, b, .rastro-contrato > :not(.rastro-arte)") || {}).textContent || "").trim().slice(0, 40) + ": "
            + (im.getAttribute ? im.getAttribute("src") : "").slice(0, 40) + ` ${im.width}/${im.naturalWidth}`; })) };
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
writeFileSync(arqRegistro, JSON.stringify(registro, null, 1));
for (const [k, v] of Object.entries(registro)) if (MODOS.includes(k.split("/")[1])) console.log(k, v.cartas.length, "cartas", v.erros, v.avisos);
