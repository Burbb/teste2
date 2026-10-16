// O menu de Itens em faixas (protótipo): o jogo como está ("atual", a janelinha de Itens ao lado dos botões) e a
// proposta ("proposta": seletor/itens-faixas.mjs e itens-faixas.css, só nesta página), na mesma luta, com os mesmos
// dados. Lutas (cenário tutorial, contra lobos de nível 9, com Morel e Odette; uma rodada de Atacar antes, para o
// registro real ficar por baixo e os aliados estarem feridos):
//   guerreiro  bolsa variada: poções, bandagem, tônico, antídoto (não serve sem veneno), bomba de fumaça, e uma arma
//              na mochila (a troca de arma);
//   arqueiro   poções e tônicos (quem recebe a poção: a mira dos aliados);
//   mago       só uma bomba de fumaça (poucos itens);
//   vazio      nada na bolsa que sirva.
// Em 1500×950 e 1280×720: a tela inteira com o menu aberto, o menu, o mouse num item (a descrição) e num que não serve
// (o motivo), a tecla 3 com as setas, a escolha da poção (a mira dos aliados ou o uso direto, a regra de hoje) e o
// Voltar. Mais o movimento reduzido no guerreiro. Mede se o menu cobre a arena, se rola e se corta texto.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_itens_faixas.mjs
// (VERSOES=atual,proposta, LUTAS=..., JANELAS=normal,baixa, SAIDA=<pasta>)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
import { escolhasItens } from "./seletor/itens-faixas.mjs";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-itens-faixas"));
rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const filtro = (nome, todos) => (process.env[nome] ? process.env[nome].split(",") : todos);
const ESCOLHAS = escolhasItens(readFileSync(path.join(raiz, "rpg/web/static/app/escolhas.js"), "utf8"));
const VERSOES = filtro("VERSOES", ["atual", "proposta"]);
const BASE = { TUTORIAL: "0", LUTA: "lobo", COMITIVA: "morel,odete", NIVEL: "12", NIVEL_LUTA: "9", QUANTOS: "2", VISTAS: "A1,V2,N1,D1,K1,M1,L1", VIDA: "0.6" };
const ZERO = "pocao_vida=0,tonico=0,antidoto=0,bandagem=0,bomba_fumaca=0";
const TODAS = {
  guerreiro: { ...BASE, CLASSE: "guerreiro", ESPEC: "berserker", BOLSA: `${ZERO},pocao_vida=2,bandagem=1,tonico=1,antidoto=1,bomba_fumaca=1`, TROCA: "1" },
  arqueiro: { ...BASE, CLASSE: "arqueiro", ESPEC: "sombra", BOLSA: `${ZERO},pocao_vida=3,tonico=2` },
  mago: { ...BASE, CLASSE: "mago", ESPEC: "necromante", BOLSA: `${ZERO},bomba_fumaca=1` },
  vazio: { ...BASE, CLASSE: "guerreiro", ESPEC: "paladino", BOLSA: ZERO },
};
const LUTAS = Object.entries(TODAS).filter(([l]) => filtro("LUTAS", Object.keys(TODAS)).includes(l));
const JANELAS = Object.entries({ normal: [1500, 950], baixa: [1280, 720] }).filter(([j]) => filtro("JANELAS", ["normal", "baixa"]).includes(j));
function subir(amb) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  return new Promise((ok, falha) => {
    let url = null;
    proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m && !url) { url = m[0]; ok({ proc, url }); } });
    proc.stderr.on("data", (d) => process.stderr.write(`[tutorial] ${d}`));
    setTimeout(() => { if (!url) falha(new Error("o cenário não subiu")); }, 30000);
  });
}
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="itens"]'));
async function vez(p) {
  for (let k = 0; k < 200; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
async function pagina(url, [W, H], versao, nome, opcoes = {}) {
  const p = await b.newPage({ viewport: { width: W, height: H }, ...opcoes });
  if (versao === "proposta") await p.route(/\/static\/app\/escolhas\.js(\?|$)/, (r) => r.fulfill({ body: ESCOLHAS, contentType: "application/javascript" }));
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  if (versao === "proposta") await p.addStyleTag({ path: path.join(aqui, "seletor", "itens-faixas.css") });
  await vez(p);
  // uma rodada de Atacar: o registro real por baixo, os aliados feridos
  await (await p.$('#roda .roda-botao[data-slot="atacar"]')).click();
  for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
  const alvo = await p.$("#batalha .carta.alvejavel");
  if (alvo) await alvo.click();
  await espera(500);
  await vez(p);
  await p.mouse.move(5, H - 5);
  await espera(600);
  return p;
}
async function recortar(p, sels, nome, folga = 8) {
  const c = await p.evaluate(([ss, f]) => {
    const rs = ss.flatMap((s) => [...document.querySelectorAll(s)]).filter((e) => e.getClientRects().length && getComputedStyle(e).visibility !== "hidden")
      .map((e) => e.getBoundingClientRect()).filter((r) => r.width);
    if (!rs.length) return null;
    const x0 = Math.max(0, Math.min(...rs.map((r) => r.left)) - f), y0 = Math.max(0, Math.min(...rs.map((r) => r.top)) - f);
    return { x: Math.floor(x0), y: Math.floor(y0), width: Math.ceil(Math.min(innerWidth, Math.max(...rs.map((r) => r.right)) + f) - x0),
      height: Math.ceil(Math.min(innerHeight, Math.max(...rs.map((r) => r.bottom)) + f) - y0) };
  }, [[].concat(sels), folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
}
const medir = (p) => p.evaluate(() => {
  const j = document.querySelector(".roda-janela");
  if (!j) return { aberto: false };
  const R = j.getBoundingClientRect(), roda = document.getElementById("roda").getBoundingClientRect(), lista = j.querySelector(".rj-lista");
  const linhas = [...j.querySelectorAll(".rj-linha")];
  return { aberto: true, tamanho: `${Math.round(R.width)}×${Math.round(R.height)}`, cobre_arena: R.top < roda.bottom - 1 && j.dataset.menu === "itens",
    itens: linhas.map((l) => `${l.querySelector(".rj-nome").textContent}${l.classList.contains("bloqueada") ? " (não serve)" : ""}`).join(", "),
    rola: lista.scrollHeight > lista.clientHeight + 1, vazio: !!j.querySelector(".rj-vazio"),
    cortados: [...j.querySelectorAll(".rj-nome, .rj-info, .rj-motivo")].filter((e) => e.scrollWidth > e.clientWidth + 1).map((e) => e.textContent) };
});
const focado = (p) => p.evaluate(() => { const a = document.activeElement; return a === document.body ? "nada" : `${a.className.split(" ")[0]}: ${a.textContent.trim().slice(0, 26)}`; });
for (const [luta, amb] of LUTAS) for (const [jan, tam] of JANELAS) for (const versao of VERSOES) {
  const { proc, url } = await subir(amb);  // um jogo novo a cada foto (a mesma semente): os mesmos dados nas duas versões
  try {
    const H = tam[1], n = (c) => `${jan}-${luta}-${versao}-${c}`, r = { nome: `${jan}-${luta}-${versao}` };
    const p = await pagina(url, tam, versao, r.nome);
    const botao = await p.$('#roda .roda-botao[data-slot="itens"]');
    await botao.click(); await espera(450); await p.mouse.move(5, H - 5); await espera(250);
    await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
    await recortar(p, ["#roda", ".roda-janela"], n("1-aberto"));
    Object.assign(r, await medir(p));
    if (!r.aberto) r.botao = "não abriu (o botão treme: nada na bolsa serve)";
    const livre = await p.$(".roda-janela .rj-linha:not(.bloqueada)");
    if (livre) { await livre.hover(); await espera(600); await recortar(p, ["#roda", ".roda-janela", "#dica-item"], n("2-mouse")); }
    const presa = await p.$(".roda-janela .rj-linha.bloqueada");
    if (presa) { await presa.hover(); await espera(600); await recortar(p, ["#roda", ".roda-janela", "#dica-item"], n("3-nao-serve")); }
    await p.mouse.move(5, H - 5); await p.keyboard.press("Escape"); await espera(300);
    r.esc_fecha = !(await p.$(".roda-janela"));
    await p.keyboard.press("3"); await espera(450);
    r.tecla_abre = !!(await p.$(".roda-janela"));
    await p.keyboard.press("ArrowDown"); await espera(150);
    r.foco = await focado(p);
    await recortar(p, ["#roda", ".roda-janela"], n("4-teclado"));
    await p.keyboard.press("Escape"); await espera(300);
    // a poção: a mira dos aliados (quem recebe) ou o uso direto, como hoje; o Voltar desfaz
    const pocao = async () => { await (await p.$('#roda .roda-botao[data-slot="itens"]')).click(); await espera(400); return p.$('.roda-janela .rj-linha[data-slot="item"]:not(.bloqueada)'); };
    const l = await pocao();
    if (l) {
      const nome = await l.evaluate((e) => e.querySelector(".rj-nome").textContent);
      if (/Poção/.test(nome)) {
        await l.click(); await espera(900); await p.mouse.move(5, H - 5); await espera(200);
        r.escolha = `${nome} → ${(await p.$(".roda-mira")) ? "a mira (quem recebe)" : "usada direto"}`;
        await recortar(p, ["#arena"], n("5-destino"), 2);
        const v = await p.$(".mira-voltar"); if (v) { await v.click(); await vez(p); }
      } else { r.escolha = `(não escolhido: ${nome})`; await p.keyboard.press("Escape"); }
    }
    relatorio.push(r);
    console.log(JSON.stringify(r));
    await p.close();
    if (luta === "guerreiro" && jan === "normal") {  // o movimento reduzido: aberto aos 40 ms
      const q = await pagina(url.replace(/$/, ""), tam, versao, `${r.nome}-reduzido`, { reducedMotion: "reduce" }).catch(() => null);
      if (q) { await (await q.$('#roda .roda-botao[data-slot="itens"]')).click(); await espera(40); await recortar(q, [".roda-janela"], n("6-reduzido-40ms")); await q.close(); }
    }
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(relatorio, null, 1));
console.log(erros.length ? erros.join("\n") : "sem erros");
