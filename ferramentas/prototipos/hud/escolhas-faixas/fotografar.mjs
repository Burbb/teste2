// As escolhas da página em faixas (1.113.0): a produção de antes (o commit ANTES, padrão 31d56c0, a 1.112.0, numa cópia
// de trabalho separada, criada aqui se faltar) e a de agora, com os mesmos dados, em 1500×950 e 1280×720.
// Os casos (todos reais, do jogo; nada é alongado nem simulado):
//   selvagem      o Bosque de dia: Explorar, Acampar, Viajar (já em faixas desde a 1.111.0);
//   viajar        "Para onde?" depois de Viajar: os destinos com o ícone do lugar;
//   vila          o Vau: Passear pela vila e a ação da missão (os serviços ficam nos prédios);
//   passear       o evento de Passear ("Aceitar?");
//   acampar       depois de Acampar: a fogueira é uma tela desenhada, com os controles dela (Dormir, a comitiva); a
//                 lista de escolhas não aparece ali (fotografada para conferir que nada dela virou faixa);
//   enfermos      evento com nota e com o item que a opção gasta (o ícone da poção);
//   enfermos-sem  o mesmo sem poção: a opção indisponível, com o motivo do motor;
//   mercador-sem  o mercador ambulante sem ouro: as compras indisponíveis ("Ouro insuficiente");
//   bandidos      evento com teste de Carisma (a etiqueta do teste, com o bônus);
//   odete         diálogo da comitiva com teste de Vontade, nota, item gasto e textos longos;
//   missao        o Bosque na etapa do canal: a ação da missão no grupo "Missão";
//   capela-tocha  a entrada da Capela à noite com tocha: os riscos embaixo da ação;
//   capela-escura a mesma sem tocha: o risco mais longo;
//   correntes     a Capela no ossuário: as ações que abrem outra escolha (›).
// Em cada um: a tela inteira, a lista parada, o mouse na opção mais alta, numa com teste e numa indisponível, o
// pressionado, o foco do teclado (Tab), e as medidas: o conteúdo de cada opção (texto, tecla, teste, nota, riscos, motivo,
// ícone, seta, bloqueio) igual antes e depois, as alturas, o contraste das etiquetas sobre o marfim, os cortes e as
// sobreposições, os pontos de clique. No fim, a tecla do número escolhe a opção certa (evento do mendigo, "Ignorar").
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/escolhas-faixas/fotografar.mjs
// (VERSOES=antes,depois, CASOS=..., JANELAS=normal,baixa, SAIDA=<pasta>, ANTES=<commit>, ANTES_RAIZ=<checkout>,
// PYTHON=<executável>, MANTER=1)
import { execFileSync, spawn } from "child_process";
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "fs";
import { tmpdir } from "os";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas"));
mkdirSync(SAIDA, { recursive: true });
if (!process.env.MANTER) for (const f of readdirSync(SAIDA)) if (/\.(png|json)$/.test(f)) rmSync(path.join(SAIDA, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const filtro = (nome, todos) => (process.env[nome] ? process.env[nome].split(",") : todos);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const ANTES = process.env.ANTES || "31d56c0";
const RAIZ_ANTES = process.env.ANTES_RAIZ || path.join(tmpdir(), `unquiet-antes-${ANTES}`);
if (!existsSync(path.join(RAIZ_ANTES, "rpg"))) execFileSync("git", ["worktree", "add", "--detach", RAIZ_ANTES, ANTES], { cwd: raiz, stdio: "inherit" });
copyFileSync(path.join(raiz, "tests/navegador/cenarios.py"), path.join(RAIZ_ANTES, "tests/navegador/cenarios.py"));
const RAIZES = { antes: RAIZ_ANTES, depois: raiz };
const VERSOES = filtro("VERSOES", ["antes", "depois"]);
const JANELAS = Object.entries({ normal: [1500, 950], baixa: [1280, 720] }).filter(([j]) => filtro("JANELAS", ["normal", "baixa"]).includes(j));
const VISTAS = "A1,V2,N1,D1,K1,M1,L1";
const T = { TUTORIAL: "0", VISTAS };
const TODOS = {
  selvagem: ["tutorial", { ...T, LUGAR: "bosque", PERIODO: "0" }, []],
  viajar: ["tutorial", { ...T, LUGAR: "bosque", PERIODO: "0" }, ["Viajar"]],
  vila: ["tutorial", { ...T, LUGAR: "vau", PERIODO: "1" }, []],
  passear: ["tutorial", { ...T, LUGAR: "vau", PERIODO: "1" }, ["Passear pela vila"]],
  acampar: ["tutorial", { ...T, LUGAR: "bosque", PERIODO: "2" }, ["Acampar e descansar"]],
  enfermos: ["covil", { EVENTO: "os_enfermos", PERIODO: "1" }, []],
  "enfermos-sem": ["covil", { EVENTO: "os_enfermos", PERIODO: "1", BOLSA: "pocao_vida=0" }, []],
  "mercador-sem": ["covil", { EVENTO: "mercador_ambulante", PERIODO: "1", OURO: "0" }, []],
  bandidos: ["covil", { EVENTO: "acampamento_bandidos", PERIODO: "1" }, []],
  odete: ["covil", { EVENTO: "odete_na_estrada", PERIODO: "1" }, []],
  missao: ["missao", {}, []],
  "capela-tocha": ["capela", { ETAPA: "capela", PERIODO: "3", TOCHAS: "2" }, []],
  "capela-escura": ["capela", { ETAPA: "capela", PERIODO: "3", TOCHAS: "0" }, []],
  correntes: ["capela", { ETAPA: "fundo", SALA: "ossuario", PERIODO: "1", TOCHAS: "2" }, []],
};
const CASOS = Object.entries(TODOS).filter(([c]) => filtro("CASOS", Object.keys(TODOS)).includes(c));

async function subir(versao, cenario, amb) {
  const cwd = RAIZES[versao];
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario],
    { cwd, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: cwd, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${versao} ${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} (${versao}) não subiu`);
  return { proc, url };
}
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const parado = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando);
async function ate(p) {  // até a lista de escolhas, passando pelo Continuar e pelos quadros de orientação
  for (let k = 0; k < 100; k++) {
    if ((await parado(p)) && (await p.$("#prompt ol.escolhas .escolha"))) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e && (await parado(p))) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a lista de escolhas não chegou");
}
async function recortar(p, sel, nome, folga = 8) {
  const c = await p.evaluate(([s, f]) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
    return r.width ? { x: Math.max(0, Math.floor(r.x - f)), y: Math.max(0, Math.floor(r.y - f)), width: Math.ceil(Math.min(innerWidth - Math.max(0, r.x - f), r.width + 2 * f)), height: Math.ceil(Math.min(innerHeight - Math.max(0, r.y - f), r.height + 2 * f)) } : null; }, [sel, folga]);
  if (c && c.height > 0) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
}
// o conteúdo de cada opção (o que não pode mudar) e a forma (o que muda de propósito)
const opcoes = (p) => p.evaluate(() => [...document.querySelectorAll("#prompt ol.escolhas .escolha")].map((b) => ({
  conteudo: { tecla: b.querySelector(".tecla")?.textContent || "", texto: b.querySelector(".op-texto")?.textContent || "", teste: b.querySelector(".teste")?.textContent || "",
    nota: [...b.querySelectorAll(".op-nota:not(.op-motivo)")].map((x) => x.textContent).join(" / "), motivo: b.querySelector(".op-motivo")?.textContent || "",
    riscos: [...b.querySelectorAll(".op-risco")].map((x) => x.textContent).join(" | "), icone: b.querySelector("img")?.getAttribute("src")?.slice(0, 40) || "",
    abre: !!b.querySelector(".op-abre"), bloqueada: b.disabled, classes: [...b.classList].filter((c) => c !== "escolha").sort().join(" ") },
  altura: Math.round(b.getBoundingClientRect().height), linhas: b.querySelector(".op-texto")?.getClientRects().length || 0 })));
// o contraste de um texto sobre o fundo dele (WCAG), com o fundo efetivo: o da própria etiqueta ou o da faixa
const contraste = (p, sel) => p.evaluate((s) => {
  const e = document.querySelector(s); if (!e) return null;
  const rgb = (c) => (c.match(/[\d.]+/g) || []).map(Number);
  const lum = ([r, g, b]) => [r, g, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }).reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
  // o fundo efetivo: a etiqueta por cima da faixa (o ::before, quando há) ou do botão, por cima da página escura
  const sobre = (c, base) => { const al = c.length > 3 ? c[3] : 1; return [0, 1, 2].map((i) => c[i] * al + base[i] * (1 - al)); };
  const bt = e.closest(".escolha"), faixa = rgb(getComputedStyle(bt, "::before").backgroundColor), botao = rgb(getComputedStyle(bt).backgroundColor);
  let base = [20, 21, 25];
  if (botao.length) base = sobre(botao, base);
  if (faixa.length && getComputedStyle(bt, "::before").content !== "none") base = sobre(faixa, base);
  const cor = rgb(getComputedStyle(e).color), fundo = sobre(rgb(getComputedStyle(e).backgroundColor), base);
  const a = lum(cor), bb = lum(fundo);
  return Math.round(((Math.max(a, bb) + 0.05) / (Math.min(a, bb) + 0.05)) * 100) / 100;
}, sel);

for (const [caso, [cenario, amb, passos]] of CASOS) {
  for (const [jan, [W, H]] of JANELAS) for (const versao of VERSOES) {
    const n = (c) => `${jan}-${caso}-${versao}-${c}`, r = { nome: `${jan}-${caso}-${versao}` };
    const { proc, url } = await subir(versao, cenario, amb);
    try {
      const p = await b.newPage({ viewport: { width: W, height: H } });
      p.on("pageerror", (e) => { erros.push(`${r.nome}: ${e}`); console.log(`ERRO NO CONSOLE ${r.nome}: ${e}`); });
      p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) { erros.push(`${r.nome}: ${m.text()}`); console.log(`ERRO NO CONSOLE ${r.nome}: ${m.text()}`); } });
      await p.goto(url);
      await ate(p);
      for (const t of passos) {
        const bt = await p.$(`#prompt .escolha:has-text("${t}")`);
        if (bt) { await bt.click(); await espera(600); await ate(p).catch(() => {}); }
      }
      await p.mouse.move(5, H - 5); await espera(800);
      await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
      if (!(await p.$("#prompt ol.escolhas .escolha"))) {  // uma tela desenhada (a fogueira): sem a lista
        r.sem_lista = await p.evaluate(() => `sem lista de escolhas; a tela: ${document.querySelector(".tela:not([hidden]), .acampamento, #acampamento")?.className || document.getElementById("cena")?.dataset.tipo}; faixas na página: ${document.querySelectorAll(".faixas").length}`);
        relatorio.push(r); console.log(JSON.stringify(r)); await p.close(); continue;
      }
      await recortar(p, "#prompt", n("1-parado"));
      Object.assign(r, await p.evaluate(() => {
        const l = document.querySelector("#prompt ol.escolhas"), bs = [...l.querySelectorAll(".escolha")];
        return { pergunta: document.querySelector("#prompt .pergunta-rotulo")?.textContent || "", faixas: l.classList.contains("faixas"), fonte: getComputedStyle(bs[0]).fontSize,
          cortados: bs.map((e) => e.querySelector(".rotulo")).filter((e) => e && e.scrollWidth > e.clientWidth + 1).length,
          sobrepostas: bs.some((e, i) => i && e.getBoundingClientRect().top < bs[i - 1].getBoundingClientRect().bottom - 0.5) };
      }));
      r.opcoes = await opcoes(p);
      // o mouse: na mais alta, numa com teste e numa indisponível (quando há); o contraste das etiquetas sob o marfim
      const bs = await p.$$("#prompt ol.escolhas .escolha");
      const alta = await p.evaluate(() => { const bs = [...document.querySelectorAll("#prompt ol.escolhas .escolha")]; let k = 0; bs.forEach((e, i) => { if (e.offsetHeight > bs[k].offsetHeight) k = i; }); return k; });
      await bs[alta].hover(); await espera(400); await recortar(p, "#prompt", n("2-mouse"));
      const comTeste = await p.evaluate(() => [...document.querySelectorAll("#prompt ol.escolhas .escolha")].findIndex((b) => b.querySelector(".teste")));
      if (comTeste >= 0) {
        await bs[comTeste].hover(); await espera(400); await recortar(p, "#prompt", n("2b-mouse-teste"));
        r.contraste_teste_marfim = await contraste(p, "#prompt ol.escolhas .escolha:hover .teste");
      }
      const comRisco = await p.$("#prompt ol.escolhas .escolha .op-risco");
      if (comRisco) { await (await p.$("#prompt ol.escolhas .escolha:has(.op-risco)")).hover(); await espera(400); r.contraste_risco_marfim = await contraste(p, "#prompt ol.escolhas .escolha:hover .op-risco"); }
      const bloq = await p.evaluate(() => [...document.querySelectorAll("#prompt ol.escolhas .escolha")].findIndex((b) => b.disabled));
      if (bloq >= 0) { await bs[bloq].hover({ force: true }); await espera(400); await recortar(p, "#prompt", n("2c-mouse-indisponivel")); r.contraste_motivo = await contraste(p, "#prompt ol.escolhas .escolha:hover .op-motivo"); }
      const abre = await p.$("#prompt ol.escolhas .escolha .op-abre");
      if (abre) { await (await p.$("#prompt ol.escolhas .escolha:has(.op-abre)")).hover(); await espera(400); r.contraste_seta_marfim = await contraste(p, "#prompt ol.escolhas .escolha:hover .op-abre"); }
      await bs[alta].hover(); await p.mouse.down(); await espera(120); await recortar(p, "#prompt", n("3-pressionado"));
      await p.mouse.move(5, H - 5); await p.mouse.up(); await espera(300);
      r.soltar_fora = (await parado(p)) && (await p.$("#prompt ol.escolhas .escolha")) ? "nada escolhido" : "ERRO";
      await p.evaluate(() => document.activeElement && document.activeElement.blur());
      for (let k = 0; k < 40 && !(await p.evaluate(() => !!document.activeElement.closest("#prompt .escolha"))); k++) await p.keyboard.press("Tab");
      r.foco = await p.evaluate(() => { const a = document.activeElement; return a.closest("#prompt .escolha") ? `${a.querySelector(".op-texto")?.textContent} (${a.matches(":focus-visible") ? "foco visível" : "SEM foco visível"})` : "nada"; });
      await recortar(p, "#prompt", n("4-foco"));
      r.clique = await p.evaluate(() => {
        const pg = document.getElementById("pagina").getBoundingClientRect(), doca = document.getElementById("doca")?.getBoundingClientRect();
        const pe = Math.min(pg.bottom, innerHeight, doca && doca.height ? doca.top : Infinity);
        const vistas = [...document.querySelectorAll("#prompt ol.escolhas .escolha")].filter((e) => { const q = e.getBoundingClientRect(); return q.top >= pg.top && q.bottom <= pe; });
        const ruins = vistas.filter((e) => { const q = e.getBoundingClientRect(); return ![[0.5, 0.5], [0.08, 0.5], [0.95, 0.5], [0.5, 0.1], [0.5, 0.9]].every(([fx, fy]) => document.elementFromPoint(q.left + q.width * fx, q.top + q.height * fy)?.closest(".escolha") === e); });
        return `${vistas.length - ruins.length} de ${vistas.length} opções à vista respondem em todos os pontos${ruins.length ? "; AMBÍGUAS" : ""}`;
      });
      relatorio.push(r);
      console.log(JSON.stringify({ ...r, opcoes: r.opcoes.length }));
      await p.close();
    } finally { proc.kill(); }
  }
}
// a tecla do número escolhe a opção certa (o mendigo: "Ignorar" é a 3), nas duas versões
for (const versao of VERSOES) {
  const { proc, url } = await subir(versao, "covil", { EVENTO: "mendigo_misterioso", PERIODO: "1" });
  try {
    const p = await b.newPage({ viewport: { width: 1500, height: 950 } });
    await p.goto(url); await ate(p); await espera(500);
    const antes = await p.evaluate(() => pergunta.opcoes.map((o) => o.texto).join(" | "));
    await p.keyboard.press("3"); await espera(1500);
    // depois da tecla: a escolha registrada no histórico (o eco "› Ignorar") e a pergunta seguinte
    const depois = await p.evaluate(() => ({ eco: [...document.querySelectorAll(".h-eco, #historico .eco, .eco")].map((e) => e.textContent.trim()).slice(-1)[0] || "",
      pergunta: typeof pergunta !== "undefined" && pergunta && pergunta.opcoes ? pergunta.opcoes.map((o) => o.texto).join(" | ") : (document.querySelector("#prompt .continuar") ? "(Continuar)" : "") }));
    relatorio.push({ nome: `tecla-${versao}`, opcoes_antes: antes, escolhida: depois.eco, a_seguir: depois.pergunta });
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
// o conteúdo de cada opção, antes × depois (tem de ser igual)
const porNome = Object.fromEntries(relatorio.filter((r) => r.opcoes).map((r) => [r.nome, r]));
const conteudo = {};
for (const r of relatorio.filter((r) => r.opcoes && r.nome.endsWith("-depois"))) {
  const a = porNome[r.nome.replace(/-depois$/, "-antes")];
  if (!a) continue;
  const A = JSON.stringify(a.opcoes.map((o) => ({ ...o.conteudo, classes: o.conteudo.classes }))), B = JSON.stringify(r.opcoes.map((o) => o.conteudo));
  conteudo[r.nome.replace(/-depois$/, "")] = A === B ? "igual" : `DIFERENTE: ${A} → ${B}`;
}
writeFileSync(path.join(SAIDA, process.env.MANTER ? "relatorio-parcial.json" : "relatorio.json"), JSON.stringify({ antes: ANTES, versoes: VERSOES, conteudo, relatorio, erros }, null, 1));
console.log(JSON.stringify(conteudo));
console.log(erros.length ? erros.join("\n") : "sem erros");
