// O levantamento dos usos reais das escolhas da página (o <ol class="escolhas"> de app/escolhas.js), antes de mudar a
// apresentação: em cada cenário, cada lista que aparece, com a pergunta, as opções, as metas de cada uma (o que o motor
// manda), o teste, o bloqueio e o contexto (luta, título, tela desenhada aberta, vila). Fotografa a lista.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/escolhas-faixas/levantar.mjs
// (SAIDA=<pasta>, PYTHON=<executável>)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "levantamento"));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const VISTAS = "A1,V2,N1,D1,K1,M1,L1";
// [nome, cenário, ambiente, passos (cliques por texto de opção, em ordem)]
const CASOS = [
  ["selvagem", "tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "bosque", PERIODO: "0" }, []],
  ["viajar", "tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "bosque", PERIODO: "0" }, ["Viajar"]],
  ["vila", "tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "vau", PERIODO: "1" }, []],
  ["passear", "tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "vau", PERIODO: "1" }, ["Passear pela vila"]],
  ["evento-enfermos", "covil", { EVENTO: "os_enfermos", PERIODO: "1" }, []],
  ["evento-mendigo", "covil", { EVENTO: "mendigo_misterioso", PERIODO: "1" }, []],
  ["evento-crianca", "covil", { EVENTO: "crianca_perdida", PERIODO: "1" }, []],
  ["evento-madeira", "covil", { EVENTO: "madeira_para_flechas", CLASSE: "arqueiro", PERIODO: "1" }, []],
  ["evento-odete", "covil", { EVENTO: "odete_na_estrada", PERIODO: "1" }, []],
  ["missao-canal", "missao", {}, []],
  ["capela-tocha", "capela", { ETAPA: "capela", PERIODO: "3", TOCHAS: "2" }, []],
  ["capela-escura", "capela", { ETAPA: "capela", PERIODO: "3", TOCHAS: "0" }, []],
  ["praca", "praca", {}, []],
  ["retorno", "retorno", {}, []],
  ["fogueira", "fogueira", {}, []],
  ["contrato", "tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "charco", PERIODO: "3", CONTRATO: "aceito", CONTRATO_EM: "charco" }, []],
  ["mercado", "mercado", {}, []],
  ["encruzilhada", "encruzilhada", {}, []],
  ["resgate", "resgate", {}, []],
  ["abertura", "abertura", {}, []],
  ["titulo", "titulo", {}, []],
];
async function subir(cenario, amb) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const parado = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando);
async function ate(p) {
  for (let k = 0; k < 80; k++) {
    if (await parado(p)) { if (await p.$("#prompt .escolha, #prompt .continuar, .caixa-confirmar, .janela-achado")) return; }
    const c = await p.$("#prompt .continuar"); if (c && await parado(p)) { await c.click().catch(() => {}); }
    const e = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (e) await e.click().catch(() => {});
    await espera(250);
  }
}
const ler = (p) => p.evaluate(() => {
  const l = document.querySelector("#prompt ol.escolhas");
  const ctx = { luta: !!(estado && estado.combate), titulo: document.body.classList.contains("modo-titulo"),
    tela: document.querySelector(".tela:not([hidden])")?.className || "", cena: document.getElementById("cena")?.dataset.tipo || "",
    vila: !!document.querySelector(".vila-predio, .predio-balao"), doca: document.querySelectorAll("#doca .atalho").length };
  if (!l) return { ctx, lista: null, continuar: !!document.querySelector("#prompt .continuar") };
  const ops = (pergunta.opcoes || []).map((o, i) => ({ i, texto: o.texto, meta: o.meta ? Object.keys(o.meta) : [], teste: o.teste ? `${o.teste.atributo} ${o.teste.mod}` : "" }));
  const botoes = [...l.querySelectorAll(".escolha")].map((b) => ({ texto: b.querySelector(".op-texto")?.textContent.trim() || b.textContent.trim().slice(0, 40), classes: b.className,
    altura: Math.round(b.getBoundingClientRect().height), teste: b.querySelector(".teste")?.textContent || "", nota: b.querySelector(".op-nota")?.textContent || "",
    riscos: [...b.querySelectorAll(".op-risco")].map((x) => x.textContent).join(" | "), icone: !!b.querySelector("img.sprite, img"), abre: !!b.querySelector(".op-abre"), tecla: b.querySelector(".tecla")?.textContent || "" }));
  return { ctx, pergunta: document.querySelector("#prompt .pergunta-rotulo")?.textContent || "", classes: l.className, grupos: [...l.querySelectorAll(".op-grupo")].map((g) => g.textContent), ops, botoes };
});
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const resultado = [];
for (const [nome, cenario, amb, passos] of CASOS) {
  const { proc, url } = await subir(cenario, amb);
  try {
    const p = await b.newPage({ viewport: { width: 1500, height: 950 } });
    await p.goto(url);
    await ate(p);
    for (const t of passos) {
      const bt = await p.$(`#prompt .escolha:has-text("${t}")`);
      if (bt) { await bt.click(); await espera(500); await ate(p); }
    }
    await espera(600);
    const r = { nome, cenario, amb, ...(await ler(p)) };
    if (await p.$("#prompt ol.escolhas")) await p.locator("#prompt").screenshot({ path: path.join(SAIDA, `${nome}.png`) }).catch(() => {});
    await p.screenshot({ path: path.join(SAIDA, `${nome}-tela.png`) });
    resultado.push(r);
    console.log(JSON.stringify(r).slice(0, 600));
    await p.close();
  } catch (e) { console.log(nome, "ERRO", String(e)); } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, "levantamento.json"), JSON.stringify(resultado, null, 1));
