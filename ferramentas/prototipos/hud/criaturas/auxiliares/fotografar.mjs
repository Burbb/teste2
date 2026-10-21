// O levantamento visual das criaturas (21/10/2026): capturas representativas a 1920×945, com os arquivos do jogo, dos
// lugares onde inimigos, chefes, animais e invocações aparecem. Os cenários são os de tests/navegador/cenarios.py
// (tutorial com GRUPO, ANIMAL, SERVOS, COMITIVA e CONTRATO; covil com BESTIARIO; vila com o mural; capela com a SALA).
// Cada situação: o cenário, as variáveis, os passos (tecla, clicar), o seletor que espera e as fotos (um seletor ou a
// página). O registro mede o tamanho de cada retrato na tela (o pedido ao sprite, o nativo e o desenhado).
//   PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos> [<nome>,...]
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida, so] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const LUTA = { TUTORIAL: "0", NIVEL_LUTA: "2" };
const SITUACOES = [
  { nome: "luta-mista-a", cenario: "tutorial", amb: { ...LUTA, CLASSE: "guerreiro", GRUPO: "lobo:1,bandido:1,esqueleto:1,espectro:1,caido:1,golem:1" },
    espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "luta-mista-b", cenario: "tutorial", amb: { ...LUTA, CLASSE: "guerreiro", GRUPO: "harpia:1,ent_jovem:1,abominacao:1,troll:1,afogado:1,cultista:1" },
    espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "aliados", cenario: "tutorial", amb: { ...LUTA, CLASSE: "arqueiro", NIVEL: "4", ESPEC: "patrulheiro", ANIMAL: "urso",
    COMITIVA: "morel,odete", LUTA: "lobo", QUANTOS: "1", SERVOS: "1" },
    espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"], ["body", "pagina"]] },
  { nome: "falcao", cenario: "tutorial", amb: { ...LUTA, CLASSE: "arqueiro", NIVEL: "4", ESPEC: "patrulheiro", ANIMAL: "falcao",
    LUTA: "lobo", QUANTOS: "1" }, espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"]] },
  { nome: "bestiario", cenario: "covil", amb: { CLASSE: "guerreiro", LUGAR: "vila",
    BESTIARIO: "lobo:5,aranha:3,bandido:4,afogado:2,esqueleto:3,espectro:2,golem:1,harpia:2,ent_jovem:1,caido:2,cria_vazio:1,troll:1" },
    passos: [{ tecla: "b" }], espera: ".cartao .cab", fotos: [["body", "pagina"]] },
  { nome: "contratos", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "guerreiro", CONTRATO: "aceito" },
    espera: ".rastro-arte", fotos: [["body", "pagina"]] },
  { nome: "capela-fundo", cenario: "capela", amb: { SALA: "fundo", ETAPA: "fundo" }, espera: "#cena canvas, #vista",
    fotos: [["body", "pagina"]] },
  { nome: "sacristia", cenario: "capela", amb: { SALA: "sacristia", ETAPA: "sacristia", BAU: "1" }, espera: "#cena canvas, #vista",
    fotos: [["body", "pagina"]] },
].filter((s) => !so || so.split(",").includes(s.nome));
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const registro = {};
for (const sit of SITUACOES) {
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
    for (const passo of sit.passos || []) {
      if (passo.tecla) await p.keyboard.press(passo.tecla);
      if (passo.clicar) await p.click(`text=${passo.clicar}`, { timeout: 15000 });
      await espera(1200);
    }
    await p.waitForSelector(sit.espera, { timeout: 30000 }).catch(() => erros.push(`não apareceu: ${sit.espera}`));
    await espera(1200);
    for (const [sel, nome] of sit.fotos) {
      const alvo = sel === "body" ? p : p.locator(sel).first();
      await alvo.screenshot({ path: path.join(saida, `${sit.nome}-${nome}.png`) }).catch((e) => erros.push(String(e)));
    }
    // o tamanho de cada retrato de criatura e de companheiro na tela: nativo (a imagem), pedido (o --s do sprite) e desenhado
    registro[sit.nome] = { erros, avisos, retratos: await p.evaluate(() => [...document.querySelectorAll(
      ".carta .icone img, .cartao .cab img, .contrato-arte img, .rastro-arte img, .membro .icone img")].map((i) => {
        const r = i.getBoundingClientRect(), dono = i.closest(".carta, .cartao, .membro, .contrato, .rastreador");
        return { onde: i.closest(".carta") ? "carta da luta" : i.closest(".cartao") ? "bestiário" : i.closest(".contrato-arte") ? "mural"
                 : i.closest(".rastro-arte") ? "rastreador" : "painel da comitiva",
                 quem: dono ? (dono.querySelector(".carta-nome span, b, .nome") || {}).textContent : "",
                 nativo: `${i.naturalWidth}×${i.naturalHeight}`, pedido: getComputedStyle(i).getPropertyValue("--s").trim() || i.getAttribute("width"),
                 tela: `${r.width.toFixed(1)}×${r.height.toFixed(1)}`, arquivo: i.src.startsWith("data:") ? "sprite em código" : i.getAttribute("src") };
      })) };
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(saida, "registro.json"), JSON.stringify(registro, null, 1));
for (const [k, v] of Object.entries(registro)) console.log(k, v.retratos.length, "retratos", v.erros.length ? v.erros : "", v.avisos.length ? v.avisos : "");
