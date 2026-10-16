// O acabamento da roda de ações (experimento): fotografa a roda da luta de verdade, com os mesmos dados, em duas
// versões:
//   atual        o jogo como está (15-hud-luta.css);
//   alternativa  a folha roda-alternativa.css por cima (só nesta página; o jogo não a carrega).
// Os ícones são os do jogo nas duas (o lote de ícones recusado em 10/2026 não entra). Cada estado, em janela normal
// (1500×950) e baixa (1280×720):
//   parada, mouse em cima (Habilidades), pressionada (Atacar, o botão do mouse descido), Habilidades aberta (com a
//   linha sem recurso, a indisponível de verdade, e o mouse numa linha), Itens aberta, mirando (Atacar → escolha do
//   alvo), foco do teclado (Tab); com a comitiva (Morel e Odette na luta); e com o movimento reduzido.
// A luta: cenário tutorial, Guerreiro contra dois lobos (a escolha do alvo), com pouco Vigor (REC) para Habilidades ter uma linha bloqueada.
// Guarda em capturas-roda/<janela>-<versao>-<estado>.png (o recorte da roda e da janelinha, ou a arena inteira) e a
// tela inteira parada; comparar_roda.py monta atual × alternativa lado a lado.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_roda.mjs
// (CHROMIUM=<executável do navegador>, se o Playwright não achar o dele)
import { spawn } from "child_process";
import { mkdirSync, rmSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.join(aqui, "capturas-roda");
rmSync(SAIDA, { recursive: true, force: true });
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
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector("#roda .roda-botao"));
async function vez(p) {
  for (let k = 0; k < 160; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
// o recorte: a roda inteira, a janelinha e o lembrete da mira, com folga (ou a arena inteira)
async function recortar(p, nome, arena = false) {
  const c = await p.evaluate((a) => {
    const els = a ? [document.querySelector("#arena"), ...document.querySelectorAll(".roda-janela")]
      : [...document.querySelectorAll("#roda > *, .roda-janela")].filter((e) => e.offsetParent !== null);
    const rs = els.filter(Boolean).map((e) => e.getBoundingClientRect()).filter((r) => r.width);
    const f = a ? 4 : 14;
    const x0 = Math.min(...rs.map((r) => r.left)) - f, y0 = Math.min(...rs.map((r) => r.top)) - f;
    const x1 = Math.max(...rs.map((r) => r.right)) + f, y1 = Math.max(...rs.map((r) => r.bottom)) + f;
    return { x: Math.max(0, Math.floor(x0)), y: Math.max(0, Math.floor(y0)), width: Math.ceil(x1 - Math.max(0, x0)), height: Math.ceil(y1 - Math.max(0, y0)) };
  }, arena);
  await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
}
const botao = (p, slot) => p.$(`#roda .roda-botao[data-slot="${slot}"]`);
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const VERSOES = ["atual", "alternativa"];
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, versao, opcoes = {}) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H }, ...opcoes });
  p.on("pageerror", (e) => erros.push(`${jan} ${versao}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${jan} ${versao}: ${m.text()}`); });
  await p.goto(url);
  if (versao === "alternativa") await p.addStyleTag({ path: path.join(aqui, "roda-alternativa.css") });
  await vez(p);
  await p.mouse.move(5, H - 5);
  await espera(800);
  return p;
}
const LUTA = { TUTORIAL: "0", CLASSE: "guerreiro", LUTA: "lobo", QUANTOS: "2", REC: "0.3", VISTAS: "A1,V2,N1,D1,K1,M1,L1" };
// 1. sozinho: os estados da roda
let { proc, url } = await subir("tutorial", LUTA);
try {
  for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) {
    const [, H] = JANELAS[jan], nome = (estado) => `${jan}-${versao}-${estado}`;
    const p = await pagina(url, jan, versao);
    await p.screenshot({ path: path.join(SAIDA, `${nome("tela")}.png`) });
    await recortar(p, nome("1-parada"));
    await (await botao(p, "habilidades")).hover(); await espera(300);
    await recortar(p, nome("2-mouse"));
    // pressionado: o botão do mouse desce no Atacar; sai de cima antes de soltar (sem clicar)
    const atk = await (await botao(p, "atacar")).boundingBox();
    await p.mouse.move(atk.x + 22, atk.y + atk.height / 2); await p.mouse.down(); await espera(150);
    await recortar(p, nome("3-pressionada"));
    await p.mouse.move(5, H - 5); await p.mouse.up(); await espera(300);
    // Habilidades aberta, com o mouse numa linha; Itens aberta
    await (await botao(p, "habilidades")).click(); await espera(500);
    const linha = await p.$(".roda-janela .rj-linha:not(.bloqueada)");
    if (linha) await linha.hover(); await espera(300);
    await recortar(p, nome("4-habilidades"));
    await p.keyboard.press("Escape"); await espera(300);
    await (await botao(p, "itens")).click(); await espera(500);
    await p.mouse.move(5, H - 5); await espera(250);
    await recortar(p, nome("5-itens"));
    await p.keyboard.press("Escape"); await espera(300);
    // mirando: Atacar abre a escolha do alvo; Voltar devolve a roda
    await (await botao(p, "atacar")).click(); await espera(900);
    await p.mouse.move(5, H - 5); await espera(300);
    await recortar(p, nome("6-mirando"), true);
    const voltar = await p.$(".mira-voltar");
    if (voltar) await voltar.click(); else await p.keyboard.press("Escape");
    await vez(p); await p.mouse.move(5, H - 5); await espera(500);
    // o foco do teclado: Tab até a roda, mais um (Habilidades)
    for (let k = 0; k < 40 && !(await p.evaluate(() => !!document.activeElement.closest(".roda-botao"))); k++) await p.keyboard.press("Tab");
    await p.keyboard.press("Tab"); await espera(300);
    await recortar(p, nome("7-teclado"));
    console.log(nome("ok"), await p.evaluate(() => (document.activeElement.textContent || "").trim()));
    await p.close();
    // o movimento reduzido: parada e o mouse em cima
    const r = await pagina(url, jan, versao, { reducedMotion: "reduce" });
    await recortar(r, nome("8-reduzido-parada"));
    await (await botao(r, "habilidades")).hover(); await espera(300);
    await recortar(r, nome("9-reduzido-mouse"));
    await r.close();
  }
} finally { proc.kill(); }
// 2. com a comitiva: a arena inteira, a roda parada e Habilidades aberta
({ proc, url } = await subir("tutorial", { ...LUTA, COMITIVA: "morel,odete" }));
try {
  for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) {
    const [, H] = JANELAS[jan], nome = (estado) => `${jan}-${versao}-${estado}`;
    const p = await pagina(url, jan, versao);
    await recortar(p, nome("a-comitiva"), true);
    await (await botao(p, "habilidades")).click(); await espera(500);
    await p.mouse.move(5, H - 5); await espera(250);
    await recortar(p, nome("b-comitiva-habilidades"), true);
    await p.screenshot({ path: path.join(SAIDA, `${nome("tela-comitiva")}.png`) });
    await p.keyboard.press("Escape"); await espera(300);
    await p.close();
  }
} finally { proc.kill(); await b.close(); }
console.log(erros.length ? erros.join("\n") : "sem erros");
