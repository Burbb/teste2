// O primeiro par das criaturas na luta e no Bestiário, a 1920×945, atual × proposta, com os mesmos dados (21/10/2026).
// Na proposta, só a página troca a imagem do retrato das cartas e do Bestiário cujo nome é o da criatura (o jogo não
// tem papel por espécie ainda; o retrato sai do traço). Situações: o Afogado numa luta com um esqueleto e uma
// sanguessuga (o cenário tutorial com GRUPO) e no Bestiário (covil com BESTIARIO); a Ilse na luta real do fundo da
// capela (o cenário capela no ossuário: "Descer ao fundo alagado" e "Lutar para destruí-la").
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.join(raiz, "ferramentas/prototipos/hud/criaturas/afogado_ilse/proposta");
const dados = (id) => "data:image/png;base64," + readFileSync(path.join(aqui, `${id}-16.png`)).toString("base64");
const TROCA = [["^Afogado", dados("afogado")], ["Bruxa Afogada|^Ilse", dados("ilse")]];
const SITUACOES = [
  { nome: "afogado-luta", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "guerreiro", NIVEL_LUTA: "2", GRUPO: "afogado:2,esqueleto:1,sanguessuga:1" },
    espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "afogado-bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila",
    BESTIARIO: "afogado:3,esqueleto:3,sanguessuga:2,aranha:2" }, passos: [{ tecla: "b" }], espera: ".cartao .cab",
    fotos: [["body", "pagina"]] },
  { nome: "ilse-luta", cenario: "capela", amb: { SALA: "ossuario", ETAPA: "fundo" },
    passos: [{ clicar: "Descer ao fundo alagado" }, { clicar: "Lutar para destruí-la" }], espera: '.carta[data-uid="j"]',
    fotos: [["body", "pagina"], ["#palco", "palco"]] },
];
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const registro = {};
for (const sit of SITUACOES) {
  for (const modo of ["atual", "proposta"]) {
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
      if (modo === "proposta") await p.evaluate((troca) => {
        const aplica = () => {
          for (const [padrao, src] of troca) {
            const re = new RegExp(padrao);
            for (const c of document.querySelectorAll(".carta")) {
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
      }, TROCA);
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
      registro[`${sit.nome}/${modo}`] = { erros, avisos, cartas: await p.evaluate(() => [...document.querySelectorAll(".carta, .cartao")]
        .map((c) => ((c.querySelector(".carta-nome span, b") || {}).textContent || "").trim() + ": "
          + ((c.querySelector(".icone img, .cab img") || {}).src || "").slice(0, 30))) };
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1));
for (const [k, v] of Object.entries(registro)) console.log(k, v.cartas.length, "cartas", v.erros, v.avisos);
