// O seletor de habilidades (experimento): a janelinha que abre em "Habilidades", no jogo como está e nas três
// propostas (seletor/: A lista integrada, B grade compacta, C losangos), na mesma luta, com os mesmos dados, os mesmos
// ícones e o mesmo caminho (escolher a habilidade, depois o alvo). Só nesta página: a folha da proposta e uma cópia do
// escolhas.js com duas linhas a mais (a janelinha diz se é de Habilidades ou de Itens, e a linha indisponível traz o
// motivo que o motor já manda, para aparecer escrito); o jogo não muda.
// As lutas (cenário tutorial, contra lobos, com Morel e Odette na comitiva):
//   guerreiro   Guerreiro paladino de nível 12 (as 7 habilidades de hoje), com pouco Vigor (umas sem recurso);
//   arqueiro    Arqueiro sombra de nível 12: os nomes mais longos (Flecha Envenenada, Chuva de Flechas) e flechas;
//   capacidade  o Guerreiro com as habilidades das duas especializações (10): nenhuma proposta pode contar com 7.
// Em janela normal (1500×950) e baixa (1280×720), cada versão: a tela inteira com o painel aberto, o painel, o mouse
// numa habilidade, o foco do teclado (a tecla 2 abre, Tab entra), a escolha (o clique leva à escolha do alvo) e o
// cancelamento (Voltar devolve a roda; Esc fecha o painel). Mede o que o painel cobre (cartas, barras, a roda), se a
// lista precisa rolar e se algum nome ou custo é cortado; confere o caminho (relatorio.json).
// Guarda em capturas-seletor/; comparar_seletor.py monta as comparações.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_seletor.mjs
// (VERSOES=atual,a,b,c, LUTAS=guerreiro,arqueiro,capacidade e SAIDA=<pasta> para escolher)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-seletor"));
rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const filtro = (nome, todos) => (process.env[nome] ? process.env[nome].split(",") : todos);
// a cópia do escolhas.js das propostas: o tipo da janelinha e o motivo escrito na linha indisponível
const trocar = (texto, trocas) => trocas.reduce((t, [a, b]) => { if (!t.includes(a)) throw new Error(`escolhas.js mudou: não achei ${a}`); return t.replace(a, b); }, texto);
const escolhas = trocar(readFileSync(path.join(raiz, "rpg/web/static/app/escolhas.js"), "utf8"), [
  ['  const j = el("div", "roda-janela");\n', '  const j = el("div", "roda-janela");\n  j.dataset.tipo = titulo === "Habilidades" ? "habilidades" : "itens";\n'],
  ['<span class="rj-info">${l.info || ""}</span>', '<span class="rj-info">${l.info || ""}</span>${l.bloqueio ? `<span class="rj-motivo">${esc(l.bloqueio)}</span>` : ""}'],
]);
const VERSOES = filtro("VERSOES", ["atual", "a", "b", "c"]);
const FOLHA = { a: "a-lista.css", b: "b-grade.css", c: "c-losangos.css" };
const BASE = { TUTORIAL: "0", LUTA: "lobo", COMITIVA: "morel,odete", NIVEL: "12", VISTAS: "A1,V2,N1,D1,K1,M1,L1" };
const LUTAS = {
  guerreiro: { ...BASE, CLASSE: "guerreiro", ESPEC: "paladino", QUANTOS: "2", REC: "0.3" },
  arqueiro: { ...BASE, CLASSE: "arqueiro", ESPEC: "sombra", QUANTOS: "3", REC: "0.3" },
  capacidade: { ...BASE, CLASSE: "guerreiro", ESPEC: "paladino", QUANTOS: "2", REC: "0.3", HABILIDADES: "todas" },
};
// as habilidades de um alvo só (a escolha leva à escolha do alvo e o Voltar desfaz; nada é jogado)
const UM_ALVO = new Set(["bola_fogo", "comando_fera", "combustao", "drenar_vida", "execucao", "fenix", "flecha_envenenada", "furia_cega",
  "golpe_pesado", "golpe_sagrado", "investida", "lanca_gelo", "marcar_presa", "sede_sangue", "tiro_certeiro", "tiro_duplo"]);
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
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, versao, nome) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  if (versao !== "atual") await p.route(/\/static\/app\/escolhas\.js(\?|$)/, (r) => r.fulfill({ body: escolhas, contentType: "application/javascript" }));
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  if (versao !== "atual") for (const f of ["comum.css", FOLHA[versao]]) await p.addStyleTag({ path: path.join(aqui, "seletor", f) });
  return p;
}
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector("#roda .roda-botao"));
async function vez(p) {
  for (let k = 0; k < 200; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
async function recortar(p, sels, nome, folga = 10) {
  const c = await p.evaluate(([ss, f]) => {
    const rs = ss.flatMap((s) => [...document.querySelectorAll(s)]).filter((e) => e.getClientRects().length && getComputedStyle(e).visibility !== "hidden" && getComputedStyle(e).opacity !== "0").map((e) => e.getBoundingClientRect()).filter((r) => r.width);
    if (!rs.length) return null;
    const x0 = Math.max(0, Math.min(...rs.map((r) => r.left)) - f), y0 = Math.max(0, Math.min(...rs.map((r) => r.top)) - f);
    return { x: Math.floor(x0), y: Math.floor(y0), width: Math.ceil(Math.min(innerWidth, Math.max(...rs.map((r) => r.right)) + f) - x0),
      height: Math.ceil(Math.min(innerHeight, Math.max(...rs.map((r) => r.bottom)) + f) - y0) };
  }, [[].concat(sels), folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c }); else console.log(`  (sem ${sels} em ${nome})`);
}
// o que o painel aberto cobre, se rola, se corta texto, o tamanho
const medir = (p) => p.evaluate(() => {
  const j = document.querySelector(".roda-janela");
  if (!j) return { aberto: false };
  const R = j.getBoundingClientRect(), cruza = (r) => Math.max(0, Math.min(R.right, r.right) - Math.max(R.left, r.left)) * Math.max(0, Math.min(R.bottom, r.bottom) - Math.max(R.top, r.top));
  const cobre = [...document.querySelectorAll("#arena .carta")].filter((c) => cruza(c.getBoundingClientRect()) > 0)
    .map((c) => (c.querySelector(".nome, b") || c).textContent.trim().split("\n")[0].slice(0, 20));
  const roda = [...document.querySelectorAll("#roda .roda-botao")].filter((c) => cruza(c.getBoundingClientRect()) > 0).length;
  const lista = j.querySelector(".rj-lista");
  const cortados = [...j.querySelectorAll(".rj-nome, .rj-info, .rj-motivo")].filter((e) => e.scrollWidth > e.clientWidth + 1 || e.getBoundingClientRect().right > R.right + 0.5).map((e) => e.textContent.trim());
  const linhas = [...j.querySelectorAll(".rj-linha")];
  return { aberto: true, tamanho: `${Math.round(R.width)}×${Math.round(R.height)}`, posicao: `${Math.round(R.left)},${Math.round(R.top)}`,
    habilidades: linhas.length, bloqueadas: linhas.filter((l) => l.classList.contains("bloqueada")).length,
    rola: lista.scrollHeight > lista.clientHeight + 1, cobre_cartas: cobre, cobre_roda: roda, fora_da_tela: R.bottom > innerHeight || R.right > innerWidth,
    cortados, menor_alvo: Math.min(...linhas.map((l) => Math.round(Math.min(l.getBoundingClientRect().width, l.getBoundingClientRect().height)))) };
});
for (const [luta, amb] of Object.entries(LUTAS).filter(([l]) => filtro("LUTAS", Object.keys(LUTAS)).includes(l))) {
  const { proc, url } = await subir("tutorial", amb);
  try {
    for (const jan of Object.keys(JANELAS)) for (const versao of VERSOES) {
      const [, H] = JANELAS[jan], n = (c) => `${jan}-${luta}-${versao}-${c}`, r = { nome: n("caminho") };
      const p = await pagina(url, jan, versao, n(""));
      await vez(p); await p.mouse.move(5, H - 5); await espera(800);
      // 1. abrir pelo clique: a tela inteira, o painel e as medidas
      await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click(); await espera(600);
      await p.mouse.move(5, H - 5); await espera(300);
      await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
      await recortar(p, ["#roda > *", ".roda-janela"], n("1-aberto"));
      Object.assign(r, await medir(p));
      // 2. o mouse numa habilidade disponível (com a dica que já existe)
      const livre = await p.$(".roda-janela .rj-linha:not(.bloqueada)");
      if (livre) { await livre.hover(); await espera(700); await recortar(p, ["#roda > *", ".roda-janela", "#dica-item"], n("2-mouse")); }
      // e numa indisponível: o motivo na linha (nas propostas) e na dica
      const presa = await p.$(".roda-janela .rj-linha.bloqueada");
      if (presa) { await presa.hover(); await espera(700); await recortar(p, ["#roda > *", ".roda-janela", "#dica-item"], n("3-indisponivel")); }
      // 3. Esc fecha
      await p.mouse.move(5, H - 5); await p.keyboard.press("Escape"); await espera(400);
      r.esc_fecha = !(await p.$(".roda-janela"));
      // 4. pelo teclado: a tecla 2 abre, Tab entra no painel
      await p.keyboard.press("2"); await espera(600);
      r.tecla_abre = !!(await p.$(".roda-janela"));
      for (let k = 0; k < 15 && !(await p.evaluate(() => !!document.activeElement.closest(".roda-janela .rj-linha"))); k++) await p.keyboard.press("Tab");
      r.tab_entra = await p.evaluate(() => (document.activeElement.closest(".rj-linha") || {}).textContent || "");
      await espera(300);
      await recortar(p, ["#roda > *", ".roda-janela"], n("4-teclado"));
      await p.keyboard.press("Escape"); await espera(400);
      // 5. a escolha: uma habilidade de um alvo, disponível → a escolha do alvo; o Voltar devolve a roda
      await (await p.$('#roda .roda-botao[data-slot="habilidades"]')).click(); await espera(500);
      const alvo = await p.evaluate((ids) => { const l = [...document.querySelectorAll(".roda-janela .rj-linha:not(.bloqueada)")].find((e) => ids.includes(e.dataset.hab)); return l ? l.dataset.hab : null; }, [...UM_ALVO]);
      if (alvo) {
        await (await p.$(`.roda-janela .rj-linha[data-hab="${alvo}"]`)).click(); await espera(1000);
        await p.mouse.move(5, H - 5); await espera(300);
        r.escolha = `${alvo} → ${(await p.$(".roda-mira")) ? "escolha do alvo" : "SEM A MIRA"}`;
        await recortar(p, ["#arena"], n("5-alvo"), 2);
        const v = await p.$(".mira-voltar");
        if (v) await v.click(); else await p.keyboard.press("Escape");
        await vez(p);
        r.cancelar = (await p.$('#roda .roda-botao[data-slot="habilidades"]')) && !(await p.$(".roda-janela")) ? "a roda de volta, sem painel" : "ERRO";
      } else r.escolha = "nenhuma habilidade de um alvo disponível";
      relatorio.push(r);
      await p.close();
      console.log(luta, jan, versao, "ok");
    }
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify(relatorio, null, 1));
for (const r of relatorio) console.log(JSON.stringify(r));
console.log(erros.length ? erros.join("\n") : "sem erros");
