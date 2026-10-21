// Os animais do patrulheiro na luta e no painel da comitiva, a 1920×945 (21/10/2026), com os mesmos dados: o Urso
// Pardo e o Falcão Peregrino, atual × as propostas A e B; o Lobo Cinzento, atual × o retrato do Lobo já integrado
// (1.163.0, rpg/web/static/hud/icones/retrato-lobo-16.png), sem mudar nada nele. Nas propostas, só a página troca a
// imagem da carta aliada do animal (.aliados .carta[data-tipo]) e a do ícone dele no painel (.membro.fera); o jogo
// continua com os sprites "fera" e "voador". Situações, uma por animal: uma luta do patrulheiro nível 4 com esse animal
// contra um lobo, um bandido e uma aranha (o cenário tutorial com NIVEL, ANIMAL e GRUPO), fotografando o palco e a
// página inteira (o painel da comitiva com o animal).
// O modo "t" (21/10/2026): a transposição das duas referências geradas (urso-t, falcao-t).
//   [ANIMAIS=urso,falcao,lobo] [SO=t] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.join(raiz, "ferramentas/prototipos/hud/criaturas/animais/proposta");
const png = (arq) => "data:image/png;base64," + readFileSync(arq).toString("base64");
const dados = (id) => png(path.join(aqui, `${id}-16.png`));
// os modos de cada animal e a imagem que a página põe no lugar (o "atual" não troca nada)
const MODOS = {
  urso: { atual: null, a: dados("urso-a"), b: dados("urso-b"), t: dados("urso-t"), final: null },
  falcao: { atual: null, a: dados("falcao-a"), b: dados("falcao-b"), t: dados("falcao-t"), final: null },
  lobo: { atual: null, reaproveitado: png(path.join(raiz, "rpg/web/static/hud/icones/retrato-lobo-16.png")), final: null },
  // a luta extra do modo final: o falcão do herói contra duas harpias e um lobo (os voadores e o lobo inimigo continuam)
  voadores: { final: null },
  // 1.165.0: o Lobo Cinzento contra três lobos (o mesmo rosto dos dois lados, de propósito)
  lobos: { final: null },
};
const ANIMAIS = (process.env.ANIMAIS || "urso,falcao,lobo").split(",");
// SO=t: só esses modos (a transposição das referências, "t", sem regravar as fotos das outras)
const SO = process.env.SO ? process.env.SO.split(",") : null;
const SITUACOES = ANIMAIS.map((tipo) => ({ nome: tipo, tipo, cenario: "tutorial",
  amb: { TUTORIAL: "0", CLASSE: "arqueiro", NIVEL: "4", ANIMAL: tipo, NIVEL_LUTA: "2", GRUPO: "lobo:1,bandido:1,aranha:1" },
  espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"], ["body", "pagina"]] }));
// o modo "final" (1.164.0): o jogo como está, sem troca, com os arquivos de produção; e a luta extra dos voadores
if (ANIMAIS.includes("voadores")) SITUACOES.splice(SITUACOES.findIndex((s) => s.tipo === "voadores"), 1, { nome: "voadores",
  tipo: "voadores", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "arqueiro", NIVEL: "4", ANIMAL: "falcao", NIVEL_LUTA: "2",
    GRUPO: "harpia:2,lobo:1" }, espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"], ["body", "pagina"]] });
if (ANIMAIS.includes("lobos")) SITUACOES.splice(SITUACOES.findIndex((s) => s.tipo === "lobos"), 1, { nome: "lobos",
  tipo: "lobos", cenario: "tutorial", amb: { TUTORIAL: "0", CLASSE: "arqueiro", NIVEL: "4", ANIMAL: "lobo", NIVEL_LUTA: "2",
    GRUPO: "lobo:3" }, espera: '.carta[data-uid="j"]', fotos: [["#palco", "palco"], ["body", "pagina"]] });
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
// o registro acumula: um modo fotografado de novo substitui só a entrada dele
const arqRegistro = path.join(saida, "registro.json");
const registro = existsSync(arqRegistro) ? JSON.parse(readFileSync(arqRegistro, "utf-8")) : {};
for (const sit of SITUACOES) {
  for (const [modo, src] of Object.entries(MODOS[sit.tipo]).filter(([m]) => !SO || SO.includes(m))) {
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
      if (src) await p.evaluate(([tipo, src]) => {
        const aplica = () => {
          for (const im of document.querySelectorAll(`.aliados .carta[data-tipo="${tipo}"] .icone img, .membro.fera .icone img`))
            if (im.src !== src) im.src = src;
        };
        aplica(); new MutationObserver(aplica).observe(document.body, { subtree: true, childList: true, characterData: true });
      }, [sit.tipo, src]);
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
      registro[`${sit.nome}/${modo}`] = { erros, avisos, cartas: await p.evaluate(() => [...document.querySelectorAll(".carta, .membro.fera")]
        .map((c) => { const im = c.querySelector(".icone img") || {};
          // o nome, o começo do endereço e a medida: o lado na tela / o lado do arquivo (o modo final: o jogo integrado)
          return (c.classList.contains("fera") ? "painel: " : "carta: ") + ((c.querySelector(".carta-nome span, .nome, b") || {}).textContent || "").trim().slice(0, 30) + ": "
            + (im.getAttribute ? im.getAttribute("src") : "").slice(0, 40) + ` ${im.width}/${im.naturalWidth}`; })) };
      await p.close();
    } finally { proc.kill(); }
  }
}
await b.close();
writeFileSync(arqRegistro, JSON.stringify(registro, null, 1));
for (const [k, v] of Object.entries(registro)) if (ANIMAIS.includes(k.split("/")[0])) console.log(k, v.cartas.length, "cartas", v.erros, v.avisos);
