// A Rainha Aracnídea e o Esqueleto a 1920×945 (21/10/2026), atual × as propostas A e B, com os mesmos dados. Nas
// propostas, só a página troca a imagem das cartas inimigas e dos cartões do Bestiário pelo nome: "Rainha Aracnídea" e
// os que começam por "Esqueleto" (o inimigo, o de guarda e os invocados). O servo do Necromante é um aliado e fica de
// fora da troca (outro papel). Situações: a Rainha (o guardião, pelo CHEFE do cenário) com duas aranhas invocadas (o
// retrato da 1.167.0); uma luta do mago necromante com dois esqueletos, um carniçal e um afogado e um servo de pé; o
// Lich Menor (chefe) com dois esqueletos invocados; o Bestiário com o esqueleto, o carniçal, a aranha e o afogado.
//   [MODOS=atual,a,b] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.join(raiz, "ferramentas/prototipos/hud/criaturas/rainha_esqueleto/proposta");
const dados = (id) => "data:image/png;base64," + readFileSync(path.join(aqui, `${id}-16.png`)).toString("base64");
const TROCAS = { a: [["^Rainha Aracnídea$", dados("rainha-a")], ["^Esqueleto( |$)", dados("esqueleto-a")]],
  b: [["^Rainha Aracnídea$", dados("rainha-b")], ["^Esqueleto( |$)", dados("esqueleto-b")]] };
const MODOS = (process.env.MODOS || "atual,a,b").split(",");
const SITUACOES = [
  { nome: "rainha", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "4", CHEFE: "rainha_aracnidea",
    INVOCADOS: "1", GRUPO: "aranha:2" }, espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "luta", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "mago", NIVEL: "6", ESPEC: "necromante", SERVOS: "1",
    NIVEL_LUTA: "4", GRUPO: "esqueleto:2,carnical:1,afogado:1" }, espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "lich", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "4", CHEFE: "lich_menor",
    INVOCADOS: "1", GRUPO: "esqueleto:2" }, espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila",
    BESTIARIO: "esqueleto:3,carnical:2,aranha:2,afogado:2" }, passos: [{ tecla: "b" }], espera: ".cartao .cab",
    fotos: [["body", "pagina"]] },
];
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
// o registro acumula: um modo fotografado de novo substitui só a entrada dele
const arqRegistro = path.join(saida, "registro.json");
const registro = existsSync(arqRegistro) ? JSON.parse(readFileSync(arqRegistro, "utf-8")) : {};
for (const sit of SITUACOES) {
  for (const modo of MODOS.filter((m) => (!sit.so || sit.so.includes(m)) && !(sit.nao || []).includes(m))) {
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
      // as caixas (relativas ao palco na luta, à página no Bestiário) de cada carta inimiga e de cada cartão, pelo nome
      const caixas = await p.evaluate((palco) => {
        const o = palco ? document.querySelector("#palco").getBoundingClientRect() : { left: 0, top: 0 };
        return [...document.querySelectorAll(".inimigos .carta, .cartao")].map((c) => {
          const r = c.getBoundingClientRect(), im = (c.querySelector(".icone img, .cab img") || c).getBoundingClientRect();
          const n = ((c.querySelector(".carta-nome span, b") || {}).textContent || "").trim();
          return { nome: n, caixa: [r.left - o.left, r.top - o.top, r.right - o.left, r.bottom - o.top].map(Math.round),
                   retrato: [im.left - o.left, im.top - o.top, im.right - o.left, im.bottom - o.top].map(Math.round) };
        });
      }, sit.fotos[0][0] === "#palco");  // a foto do palco: as caixas relativas a ele
      registro[`${sit.nome}/${modo}`] = { erros, avisos, caixas, cartas: await p.evaluate(() => [...document.querySelectorAll(".carta, .cartao")]
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
