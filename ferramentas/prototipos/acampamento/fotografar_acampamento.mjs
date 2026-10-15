// O acampamento do lado de fora da Capela Afogada, atual × protótipo, no jogo de verdade, em janela normal (1500×950)
// e baixa (1280×720), em tamanho real. O protótipo entra pelo cenário (cenario_acampamento.py, PROTOTIPO=1: uma cópia
// da pasta static com acampamento-no-jogo.js colado ao fim de telas/fogueira.js); o jogo não muda.
//   - a capela de fora, antes de acampar (a referência);
//   - a fogueira com o Mago, Morel e Odette na roda e Yara no acampamento (atual e protótipo);
//   - no protótipo: o menu de um companheiro, deixar no acampamento, levar de volta, um ferido, o animal do
//     patrulheiro, a conversa (e a volta para a fogueira) e o Dormir até o amanhecer (a paisagem volta);
//   - as horas e o clima (manhã, crepúsculo, chuva).
// Guarda em capturas/ (ou SAIDA).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/acampamento/fotografar_acampamento.mjs
// (CHROMIUM=<executável>; SO=base,interacoes,condicoes)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas"));
const SO = new Set((process.env.SO || "base,interacoes,condicoes").split(","));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
async function subir(amb = {}) {
  const proc = spawn("python3", [path.join(aqui, "cenario_acampamento.py"), "capela_fora"],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[cenário] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const fechar = async (p) => { for (let k = 0; k < 6; k++) { const e = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (!e) break; await e.click().catch(() => {}); await espera(250); } };
async function abrir(W, H, nome, amb) {
  const { proc, url } = await subir(amb);
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/404/.test(m.text())) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  await p.waitForSelector('#prompt .escolha:has-text("Acampar")', { timeout: 30000 }); await fechar(p);
  return { p, proc };
}
async function acampar(p) {
  await (await p.$('#prompt .escolha:has-text("Acampar")')).click();
  await p.waitForSelector(".tela.acampamento", { timeout: 20000 }); await espera(1500); await fechar(p); await espera(400);
}
const foto = (p, nome) => p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
async function topo(p, nome) {
  const v = await p.$("#vista");
  if (v && await v.isVisible()) await p.screenshot({ path: path.join(SAIDA, `${nome}-topo.png`), clip: await v.boundingBox() });
  const palco = await p.$(".fogueira-palco");
  if (palco && await palco.isVisible()) await palco.screenshot({ path: path.join(SAIDA, `${nome}-palco.png`) });
}
// quem aparece na cena (os botões sobre a arte) e o que o rodapé diz: as figuras correspondem a quem está presente
const quem = (p) => p.evaluate(() => ({
  figuras: [...document.querySelectorAll("#acamp-capa .figura, .fogueira-palco .figura")].map((f) => `${f.dataset.cid || "fera"}${f.classList.contains("reserva") ? "(fica)" : ""}`),
  rodape: (document.querySelector(".fogueira-rodape") || {}).innerText,
}));
async function clicarFigura(p, cid) {
  await p.click(`#acamp-capa .figura[data-cid="${cid}"], .fogueira-palco .figura[data-cid="${cid}"]`); await espera(500);
}
async function escolherNoMenu(p, texto) {
  await p.click(`.menu-item button:has-text("${texto}")`);
  await espera(1800); await fechar(p);
}
const JANELAS = [[1500, 950, "normal"], [1280, 720, "baixa"]];
for (const [W, H, jan] of JANELAS) {
  if (SO.has("base")) for (const versao of ["atual", "prototipo"]) {
    const { p, proc } = await abrir(W, H, `${jan}-${versao}`, { PROTOTIPO: versao === "atual" ? "0" : "1" });
    if (versao === "atual") { await espera(800); await foto(p, `${jan}-0-capela-de-fora`); }
    await acampar(p);
    await foto(p, `${jan}-1-${versao}`);
    await topo(p, `${jan}-1-${versao}`);
    console.log(`${jan} ${versao}:`, JSON.stringify(await quem(p)));
    await p.close(); proc.kill();
  }
  if (SO.has("interacoes")) {
    const { p, proc } = await abrir(W, H, `${jan}-interacoes`, { FERIDO: "odete" });
    await acampar(p);
    await foto(p, `${jan}-2-ferida`);
    await clicarFigura(p, "morel");
    await foto(p, `${jan}-3-menu-morel`);
    await escolherNoMenu(p, "Deixar no acampamento");
    await foto(p, `${jan}-4-morel-fica`);
    console.log(`${jan} Morel deixado:`, JSON.stringify(await quem(p)));
    await clicarFigura(p, "yara");
    await foto(p, `${jan}-5-menu-yara`);
    await escolherNoMenu(p, "Levar");
    console.log(`${jan} Yara levada:`, JSON.stringify(await quem(p)));
    await foto(p, `${jan}-6-yara-vai`);
    // conversar: a página da conversa sai da fogueira; terminada, volta para ela
    await clicarFigura(p, "yara");
    const conversa = await p.$('.menu-item button:has-text("Conversar")');
    if (conversa) {
      await conversa.click(); await espera(1500); await fechar(p);
      await foto(p, `${jan}-7-conversa`);
      for (let k = 0; k < 40 && !(await p.$(".tela.acampamento")); k++) {
        const c = await p.$("#prompt .continuar") || await p.$("#prompt .escolha:last-child");
        if (c) await c.click().catch(() => {}); await espera(500); await fechar(p);
      }
      await espera(1200);
      await foto(p, `${jan}-8-de-volta`);
      console.log(`${jan} de volta da conversa:`, JSON.stringify(await quem(p)));
    } else { console.log(`${jan}: sem Conversar no menu da Yara`); await p.keyboard.press("Escape"); await p.mouse.click(5, 5); }
    await p.click("#acamp-capa .dormir-barraca", { force: true }); await espera(4500); await fechar(p);  // o selo balança (boiar)
    await foto(p, `${jan}-9-amanhecer`);
    console.log(`${jan} amanhecer: capa=${!!(await p.$("#acamp-capa"))} ambiente=${await p.evaluate(() => Vista.temAmbiente())}`);
    await p.close(); proc.kill();
    const fera = await abrir(W, H, `${jan}-fera`, { CLASSE: "arqueiro", FERA: "1", COMITIVA: "morel", RESERVA: "yara,odete" });
    await acampar(fera.p);
    await foto(fera.p, `${jan}-a-arqueiro-fera`);
    await topo(fera.p, `${jan}-a-arqueiro-fera`);
    await fera.p.close(); fera.proc.kill();
    const so = await abrir(W, H, `${jan}-sozinho`, { COMITIVA: "", RESERVA: "" });
    await acampar(so.p);
    await foto(so.p, `${jan}-b-sozinho`);
    await so.p.close(); so.proc.kill();
  }
  if (SO.has("condicoes") && jan === "normal") for (const [nome, amb] of [["manha", { PERIODO: "0" }], ["crepusculo", { PERIODO: "2" }], ["chuva", { CLIMA: "chuva" }]]) {
    const { p, proc } = await abrir(W, H, `${jan}-${nome}`, amb);
    await acampar(p);
    await topo(p, `${jan}-c-${nome}`);
    await p.close(); proc.kill();
  }
}
await b.close();
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
